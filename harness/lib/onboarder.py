"""Onboarding orchestrator — loops runner.run_skill across enabled skills,
tracks token budget, synthesises skipped_budget entries on ceiling breach.

See docs/superpowers/specs/2026-04-18-phase-1-4-onboarding-mode-design.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from harness.lib.ledger import LedgerEntry


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
