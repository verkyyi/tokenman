"""Onboarder budget pre-flight: synthesize skipped_budget on breach."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from harness.lib.git_ops import GitIdentity
from harness.lib.onboarder import OnboardingBudget, run_onboarding
from harness.lib.pr_opener import FakePROpener
from harness.lib.skill_executor import StubSkillExecutor


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


def test_session_ceiling_breach_skips_remaining_skills(
    seeded_repo: Path, tmp_path: Path,
) -> None:
    """First skill runs and pushes the running total close to the ceiling;
    second skill's pre-flight check trips and it's recorded as
    skipped_budget without invoking the executor.
    """
    ledger_path = tmp_path / "ledger.jsonl"
    runs_dir = tmp_path / "runs"
    pr_opener = FakePROpener(sink_dir=tmp_path / "prs")
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})

    result = run_onboarding(
        skills=[
            ("stub-readme",        STUB_SKILL_A),
            ("stub-readme-second", STUB_SKILL_B),
        ],
        repo_dir=seeded_repo,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        # per_run_ceiling (10_000) > session_ceiling (5_000) means:
        #   skill A pre-flight: 0 + 10_000 > 5_000 → BREACH
        # so even the FIRST skill is skipped. That's the simplest way to
        # exercise the synth path with deterministic stubs. We assert
        # both skills got skipped_budget entries.
        budget=OnboardingBudget(per_run_ceiling=10_000, session_ceiling=5_000),
        base_branch="main",
        git_identity=GitIdentity("test-bot", "test@local"),
    )

    assert len(result.entries) == 2
    assert [e["status"] for e in result.entries] == [
        "skipped_budget", "skipped_budget",
    ]
    assert [e["skill"] for e in result.entries] == [
        "stub-readme", "stub-readme-second",
    ]
    # No PRs opened, no executor invocations.
    assert pr_opener.calls == []
    # Both entries appended to the ledger.
    lines = [ln for ln in ledger_path.read_text().splitlines() if ln.strip()]
    assert len(lines) == 2
    # breached_ceiling is set.
    assert result.breached_ceiling is True
    # No tokens consumed.
    assert result.total_tokens == 0
