"""Tokenman harness runner — orchestrates a single skill run.

Phase 1.2a: ledger-aware, subprocess-driven, PR opener injected. No
`claude -p`, no `gh pr create`; 1.2b swaps in real implementations.
See docs/superpowers/specs/2026-04-18-phase-1-2a-harness-plumbing-design.md.
"""
from __future__ import annotations

import json
import shutil
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic
from typing import Any, Callable, Optional

from harness.lib import ledger
from harness.lib.pr_opener import PROpener
from harness.lib.skill_executor import SkillExecutor


def _count_diff_lines(diff_text: str) -> int:
    """Count lines starting with '+' or '-' but excluding file-header
    lines ('+++ ', '+++\\t', '--- ', '---\\t').
    """
    count = 0
    for line in diff_text.splitlines():
        if line.startswith(("+++ ", "+++\t", "--- ", "---\t")):
            continue
        if line.startswith(("+", "-")):
            count += 1
    return count


def _format_run_id(n: int) -> str:
    """Zero-pad a run number to the schema's canonical r-NNNN shape."""
    return f"r-{n:04d}"


def _iso_utc(dt: datetime) -> str:
    """Render as ISO 8601 UTC with seconds precision and Z suffix."""
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_skill(
    *,
    skill_dir: Path,
    repo_dir: Path,
    ledger_path: Path,
    runs_dir: Path,
    executor: SkillExecutor,
    pr_opener: PROpener,
    skill_name: Optional[str] = None,
    now: Optional[Callable[[], datetime]] = None,
) -> dict:
    """Run one skill against a repo. Returns the ledger entry appended.

    See the data-flow section of the Phase 1.2a design doc for the
    step-by-step contract.
    """
    now = now or (lambda: datetime.now(timezone.utc))
    skill = skill_name or skill_dir.name

    # 2a. Allocate run_id.
    prev_n = ledger.last_run_id(ledger_path)
    run_id = _format_run_id((prev_n or 0) + 1)

    # 2b/2c. Start clock + create artifact dir.
    t_start = monotonic()
    artifact_dir = runs_dir / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    # 2d/2e. Scratch dir + executor invocation.
    with tempfile.TemporaryDirectory(prefix=f"tokenman-{run_id}-") as scratch_str:
        scratch = Path(scratch_str)
        result = executor.execute(skill_dir, repo_dir, scratch)

        # 2f. Persist subprocess output.
        (artifact_dir / "stub.stdout").write_text(result.stdout)
        (artifact_dir / "stub.stderr").write_text(result.stderr)
        if result.proposed_diff_path is not None:
            shutil.copyfile(result.proposed_diff_path, artifact_dir / "proposed.diff")
        if result.proposed_md_path is not None:
            shutil.copyfile(result.proposed_md_path, artifact_dir / "proposed.md")
        diff_text = (
            (artifact_dir / "proposed.diff").read_text()
            if result.proposed_diff_path is not None
            else ""
        )

    # 2g. Decide status + populate fields.
    generator: Optional[dict]
    pr: Optional[int]
    if result.exit_code != 0:
        status: str = "error"
        generator = None
        pr = None
    elif result.proposed_diff_path is None:
        status = "no_change"
        generator = {
            "prompt_version": "stub-v1",
            "output_summary": result.summary,
            "diff_lines": 0,
            "tokens": 0,
        }
        pr = None
    else:
        diff_lines = _count_diff_lines(diff_text)
        generator = {
            "prompt_version": "stub-v1",
            "output_summary": result.summary,
            "diff_lines": diff_lines,
            "tokens": 0,
        }
        try:
            pr = pr_opener.open(
                title=f"[tokenman] {skill}: {result.summary}",
                body=result.summary,
                branch=f"tokenman/{skill}/{run_id}",
                diff=diff_text,
            )
            status = "pr_opened"
        except Exception as exc:
            tb = traceback.format_exc()
            status = "error"
            generator = None
            pr = None
            (artifact_dir / "stub.stderr").write_text(
                result.stderr + f"\n[runner] pr_opener failed: {exc}\n{tb}"
            )

    # 2h. Stop clock.
    duration_s = int(monotonic() - t_start)

    # 2i. Build ledger entry.
    entry: dict[str, Any] = {
        "run_id": run_id,
        "ts": _iso_utc(now()),
        "skill": skill,
        "status": status,
        "pr": pr,
        "generator": generator,
        "evaluator": None,
        "duration_s": duration_s,
        "total_tokens": (generator["tokens"] if generator else 0),
        "verdict": None,
        "verdict_note": None,
    }

    # 2j. Append first — may raise LedgerInvariantError. If it does,
    # we never reach step 2k, so no orphan ledger.entry file gets
    # created. Locked by test_run_skill_leaves_no_ledger_entry_on_append_failure.
    ledger.append(ledger_path, entry)

    # 2k. Per-run ledger copy — only after successful append.
    (artifact_dir / "ledger.entry").write_text(
        json.dumps(entry, separators=(",", ":")) + "\n"
    )

    # 2l. Return.
    return entry
