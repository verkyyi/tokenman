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


from harness.lib import ledger
from harness.lib.onboarder import _synth_skipped_entry


def test_synth_skipped_entry_is_schema_valid_skipped_budget() -> None:
    when = datetime(2026, 4, 18, 10, 0, 0, tzinfo=timezone.utc)
    entry = _synth_skipped_entry(
        skill_name="readme-maintainer",
        run_id="r-0042",
        now=when,
    )
    # Should not raise.
    ledger.validate(entry)
    assert entry["run_id"] == "r-0042"
    assert entry["skill"] == "readme-maintainer"
    assert entry["status"] == "skipped_budget"
    assert entry["pr"] is None
    assert entry["generator"] is None
    assert entry["evaluator"] is None
    assert entry["duration_s"] == 0
    assert entry["total_tokens"] == 0
    assert entry["verdict"] is None
    assert entry["verdict_note"] is None
    assert entry["ts"] == "2026-04-18T10:00:00Z"
