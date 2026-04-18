"""Onboarding orchestrator — loops runner.run_skill across enabled skills,
tracks token budget, synthesises skipped_budget entries on ceiling breach.

See docs/superpowers/specs/2026-04-18-phase-1-4-onboarding-mode-design.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from harness.lib import ledger, runner
from harness.lib.git_ops import GitIdentity
from harness.lib.ledger import LedgerEntry
from harness.lib.pr_opener import PROpener
from harness.lib.skill_executor import SkillExecutor


@dataclass(frozen=True)
class OnboardingBudget:
    """Token ceilings for a single onboarding session.

    `per_run_ceiling` is the worst-case upper bound used by the
    orchestrator's pre-flight check (we never *start* a skill that could
    push us past `session_ceiling`). The executor itself does not
    enforce a mid-run limit in Phase 1.4 — a skill that exceeds
    `per_run_ceiling` mid-run is recorded honestly and counted against
    the session total.
    """

    per_run_ceiling: int
    session_ceiling: int


@dataclass(frozen=True)
class OnboardingResult:
    """Outcome of one onboarding session — every attempted skill in
    `entries` (in invocation order), even if it was skipped or errored.
    """

    entries: List[LedgerEntry]
    total_tokens: int
    session_ceiling: int
    started_at: datetime
    finished_at: datetime
    breached_ceiling: bool


def _iso_utc(dt: datetime) -> str:
    """Render as ISO 8601 UTC with seconds precision and Z suffix."""
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _synth_skipped_entry(
    *,
    skill_name: str,
    run_id: str,
    now: datetime,
) -> LedgerEntry:
    """Build a schema-valid `skipped_budget` ledger entry for a skill we
    never started because the session ceiling would have been breached.
    """
    return {
        "run_id": run_id,
        "ts": _iso_utc(now),
        "skill": skill_name,
        "status": "skipped_budget",
        "pr": None,
        "generator": None,
        "evaluator": None,
        "duration_s": 0,
        "total_tokens": 0,
        "verdict": None,
        "verdict_note": None,
    }


class OnboardingError(RuntimeError):
    """Raised before any skill runs when onboarding cannot proceed."""


def run_onboarding(
    *,
    skills: List[Tuple[str, Path]],
    repo_dir: Path,
    ledger_path: Path,
    runs_dir: Path,
    executor: SkillExecutor,
    pr_opener: PROpener,
    budget: OnboardingBudget,
    base_branch: str = "main",
    git_identity: Optional[GitIdentity] = None,
    now: Optional[Callable[[], datetime]] = None,
) -> OnboardingResult:
    """Run every skill in `skills` in order. Each invocation goes through
    runner.run_skill; the orchestrator tracks the running token total
    and pre-flights each skill against the session ceiling.

    See docs/superpowers/specs/2026-04-18-phase-1-4-onboarding-mode-design.md
    §5.1 for the full contract.
    """
    if not skills:
        raise OnboardingError("no skills to onboard")

    now = now or (lambda: datetime.now(timezone.utc))
    started = now()
    entries: list[LedgerEntry] = []
    total_tokens = 0
    breached = False

    for skill_name, skill_dir in skills:
        # Pre-flight: would starting this skill (worst case) blow the
        # session ceiling? If so, never invoke runner.run_skill — record
        # a synthesized skipped_budget entry instead.
        if total_tokens + budget.per_run_ceiling > budget.session_ceiling:
            breached = True
            prev_n = ledger.last_run_id(ledger_path)
            run_id = f"r-{(prev_n or 0) + 1:04d}"
            skipped = _synth_skipped_entry(
                skill_name=skill_name,
                run_id=run_id,
                now=now(),
            )
            ledger.append(ledger_path, skipped)
            entries.append(skipped)
            continue

        entry = runner.run_skill(
            skill_dir=skill_dir,
            repo_dir=repo_dir,
            ledger_path=ledger_path,
            runs_dir=runs_dir,
            executor=executor,
            pr_opener=pr_opener,
            skill_name=skill_name,
            base_branch=base_branch,
            git_identity=git_identity,
            now=now,
        )
        entries.append(entry)
        total_tokens += entry["total_tokens"]

    finished = now()
    return OnboardingResult(
        entries=entries,
        total_tokens=total_tokens,
        session_ceiling=budget.session_ceiling,
        started_at=started,
        finished_at=finished,
        breached_ceiling=breached,
    )
