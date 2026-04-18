"""Unit tests for harness.lib.onboarder."""
from __future__ import annotations

import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from harness.lib import ledger
from harness.lib.git_ops import GitIdentity
from harness.lib.onboarder import (
    OnboardingBudget,
    OnboardingResult,
    _synth_skipped_entry,
    run_onboarding,
)
from harness.lib.pr_opener import FakePROpener
from harness.lib.skill_executor import StubSkillExecutor


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


REPO_ROOT = Path(__file__).resolve().parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"
STUB_SKILL_A = REPO_ROOT / "tests" / "fixtures" / "skills" / "stub-readme"
STUB_SKILL_B = REPO_ROOT / "tests" / "fixtures" / "skills" / "stub-readme-second"


def _seed_git_repo(repo: Path, remote: Path) -> None:
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name",  "seed"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "seed"],
        check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "remote", "add", "origin", str(remote)],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "push", "-u", "origin", "main"],
        check=True, capture_output=True,
    )


@pytest.fixture
def seeded_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    remote = tmp_path / "remote.git"
    _seed_git_repo(repo, remote)
    return repo


def test_run_onboarding_runs_each_skill_in_order(
    seeded_repo: Path, tmp_path: Path,
) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    runs_dir = tmp_path / "runs"
    pr_opener = FakePROpener(sink_dir=tmp_path / "prs")
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})

    result = run_onboarding(
        skills=[
            ("stub-readme", STUB_SKILL_A),
            ("stub-readme-second", STUB_SKILL_B),
        ],
        repo_dir=seeded_repo,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        budget=OnboardingBudget(per_run_ceiling=10_000, session_ceiling=60_000),
        base_branch="main",
        git_identity=GitIdentity("test-bot", "test@local"),
    )

    assert len(result.entries) == 2
    assert [e["skill"] for e in result.entries] == [
        "stub-readme", "stub-readme-second",
    ]
    assert all(e["status"] == "pr_opened" for e in result.entries)
    assert result.total_tokens == sum(e["total_tokens"] for e in result.entries)
    assert result.session_ceiling == 60_000
    assert result.breached_ceiling is False
    assert result.finished_at >= result.started_at
    assert len(pr_opener.calls) == 2
    lines = [ln for ln in ledger_path.read_text().splitlines() if ln.strip()]
    assert len(lines) == 2
