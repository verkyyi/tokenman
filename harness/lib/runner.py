"""Tokenman harness runner — orchestrates a single skill run."""
from __future__ import annotations

import json
import shutil
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic
from typing import Any, Callable, Optional

from harness.lib import git_ops, ledger
from harness.lib.git_ops import GitIdentity, GitOpsError, RuntimeMode
from harness.lib.ledger import LedgerEntry
from harness.lib.pr_opener import PROpener, PROpenerError
from harness.lib.skill_executor import ExecutionResult, SkillExecutor


def _count_diff_lines(diff_text: str) -> int:
    """Count changed content lines, excluding file headers."""
    count = 0
    for line in diff_text.splitlines():
        if line.startswith(("+++ ", "+++\t", "--- ", "---\t")):
            continue
        if line.startswith(("+", "-")):
            count += 1
    return count


def _format_run_id(n: int) -> str:
    return f"r-{n:04d}"


def _iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_generator(result: ExecutionResult, diff_lines: int) -> dict[str, Any]:
    return {
        "prompt_version": result.prompt_version,
        "output_summary": result.summary,
        "diff_lines": diff_lines,
        "tokens": result.tokens,
    }


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
    base_branch: str = "main",
    git_identity: Optional[GitIdentity] = None,
    runtime_mode: RuntimeMode = "local_debug",
) -> LedgerEntry:
    """Run one skill against a repo. Returns the ledger entry appended."""
    now = now or (lambda: datetime.now(timezone.utc))
    skill = skill_name or skill_dir.name
    git_identity = git_identity or GitIdentity("tokenman-bot", "tokenman@local")

    prev_n = ledger.last_run_id(ledger_path)
    run_id = _format_run_id((prev_n or 0) + 1)
    branch = f"tokenman/{skill}/{run_id}"

    t_start = monotonic()
    artifact_dir = runs_dir / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    status = "error"
    generator: Optional[dict[str, Any]] = None
    pr: Optional[int] = None
    stdout = ""
    stderr = ""

    with tempfile.TemporaryDirectory(prefix=f"tokenman-{run_id}-") as scratch_str:
        scratch = Path(scratch_str)

        try:
            checkout_dir = git_ops.prepare_branch_checkout(
                repo_dir=repo_dir,
                scratch_dir=scratch,
                branch=branch,
                base=base_branch,
                runtime_mode=runtime_mode,
            )
        except GitOpsError as exc:
            stderr = f"[runner] worktree setup failed: {exc}\n"
            (artifact_dir / "executor.stdout").write_text(stdout)
            (artifact_dir / "executor.stderr").write_text(stderr)
        else:
            try:
                result = executor.execute(skill_dir, checkout_dir, scratch)
            except Exception as exc:
                stderr = f"[runner] executor raised: {exc}\n{traceback.format_exc()}"
                (artifact_dir / "executor.stdout").write_text(stdout)
                (artifact_dir / "executor.stderr").write_text(stderr)
            else:
                stdout = result.stdout
                stderr = result.stderr
                (artifact_dir / "executor.stdout").write_text(stdout)
                (artifact_dir / "executor.stderr").write_text(stderr)
                if result.proposed_md_path is not None:
                    shutil.copyfile(result.proposed_md_path, artifact_dir / "proposed.md")

                try:
                    diff_text, _changed_paths = git_ops.stage_and_capture_diff(
                        checkout_dir=checkout_dir
                    )
                except GitOpsError as exc:
                    generator = _build_generator(result, 0)
                    stderr = stderr + f"\n[runner] git diff failed: {exc}\n"
                    (artifact_dir / "executor.stderr").write_text(stderr)
                else:
                    diff_lines = _count_diff_lines(diff_text)
                    generator = _build_generator(result, diff_lines)

                    if diff_text:
                        (artifact_dir / "proposed.diff").write_text(diff_text)

                    if result.exit_code != 0:
                        status = "error"
                    elif not diff_text:
                        status = "no_change"
                    else:
                        try:
                            git_ops.commit_and_push(
                                checkout_dir=checkout_dir,
                                message=f"[tokenman] {skill}: {result.summary}",
                                identity=git_identity,
                            )
                            pr = pr_opener.open(
                                title=f"[tokenman] {skill}: {result.summary}",
                                body=result.summary,
                                branch=branch,
                            )
                            status = "pr_opened"
                        except (GitOpsError, PROpenerError) as exc:
                            status = "error"
                            pr = None
                            stderr = stderr + (
                                f"\n[runner] git/pr_opener failed: {exc}\n"
                                f"{traceback.format_exc()}"
                            )
                            (artifact_dir / "executor.stderr").write_text(stderr)
            finally:
                git_ops.cleanup_branch_checkout(
                    repo_dir=repo_dir,
                    checkout_dir=checkout_dir,
                    branch=branch,
                    base=base_branch,
                    runtime_mode=runtime_mode,
                )

    duration_s = int(monotonic() - t_start)

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

    ledger.append(ledger_path, entry)
    (artifact_dir / "ledger.entry").write_text(
        json.dumps(entry, separators=(",", ":")) + "\n"
    )
    return entry
