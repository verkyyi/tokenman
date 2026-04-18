"""Unit tests for harness.lib.onboarder."""
from __future__ import annotations

from datetime import datetime, timezone

from harness.lib.onboarder import OnboardingBudget, OnboardingResult


def test_onboarding_budget_has_per_run_and_session_ceilings() -> None:
    b = OnboardingBudget(per_run_ceiling=30_000, session_ceiling=180_000)
    assert b.per_run_ceiling == 30_000
    assert b.session_ceiling == 180_000


def test_onboarding_budget_is_frozen() -> None:
    b = OnboardingBudget(per_run_ceiling=1, session_ceiling=2)
    try:
        b.per_run_ceiling = 99  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("OnboardingBudget should be frozen")


def test_onboarding_result_carries_entries_totals_and_breach_flag() -> None:
    started = datetime(2026, 4, 18, 10, 0, 0, tzinfo=timezone.utc)
    finished = datetime(2026, 4, 18, 10, 0, 5, tzinfo=timezone.utc)
    r = OnboardingResult(
        entries=[],
        total_tokens=12_345,
        session_ceiling=100_000,
        started_at=started,
        finished_at=finished,
        breached_ceiling=False,
    )
    assert r.total_tokens == 12_345
    assert r.session_ceiling == 100_000
    assert r.started_at == started
    assert r.finished_at == finished
    assert r.breached_ceiling is False
    assert r.entries == []
