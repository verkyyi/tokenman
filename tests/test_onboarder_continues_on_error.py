"""Onboarder continues past per-skill errors."""
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


class _ScriptedExecutor:
    """Wraps StubSkillExecutor; force-crashes the named skills to make
    runner.run_skill emit status=error for them.
    """

    def __init__(self, crash_for: set[str]) -> None:
        self._crash_for = crash_for

    def execute(self, skill_dir, repo_dir, scratch_dir):
        if skill_dir.name in self._crash_for:
            inner = StubSkillExecutor(extra_env={"STUB_MODE": "crash"})
        else:
            inner = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
        return inner.execute(skill_dir, repo_dir, scratch_dir)


def test_onboarding_continues_after_skill_error(
    seeded_repo: Path, tmp_path: Path,
) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    runs_dir = tmp_path / "runs"
    pr_opener = FakePROpener(sink_dir=tmp_path / "prs")
    # Crash skill A; skill B should still run.
    executor = _ScriptedExecutor(crash_for={"stub-readme"})

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
        budget=OnboardingBudget(per_run_ceiling=10_000, session_ceiling=60_000),
        base_branch="main",
        git_identity=GitIdentity("test-bot", "test@local"),
    )

    assert len(result.entries) == 2
    statuses = [e["status"] for e in result.entries]
    skills = [e["skill"] for e in result.entries]
    assert skills == ["stub-readme", "stub-readme-second"]
    assert statuses[0] == "error"
    # Skill B no_change → runner reports no_change.
    assert statuses[1] == "no_change"
    # No PR for the crashing skill, no PR for no_change.
    assert pr_opener.calls == []
