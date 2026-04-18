"""Onboarder rejects an empty skill list with OnboardingError."""
from __future__ import annotations

from pathlib import Path

import pytest

from harness.lib.onboarder import (
    OnboardingBudget,
    OnboardingError,
    run_onboarding,
)
from harness.lib.pr_opener import FakePROpener
from harness.lib.skill_executor import StubSkillExecutor


def test_empty_skills_raises_onboarding_error(tmp_path: Path) -> None:
    with pytest.raises(OnboardingError, match="no skills"):
        run_onboarding(
            skills=[],
            repo_dir=tmp_path,
            ledger_path=tmp_path / "ledger.jsonl",
            runs_dir=tmp_path / "runs",
            executor=StubSkillExecutor(),
            pr_opener=FakePROpener(),
            budget=OnboardingBudget(per_run_ceiling=10, session_ceiling=100),
        )
