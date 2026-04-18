"""End-to-end tests for the harness.onboard CLI (subprocess invocation)."""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

import harness.onboard.__main__ as onboard_main
from harness.lib.onboarder import OnboardingResult


REPO_ROOT = Path(__file__).resolve().parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


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


def test_cli_dry_run_writes_summary_with_skills_passed_via_flag(
    seeded_repo: Path, tmp_path: Path,
) -> None:
    summary_path = tmp_path / "onboarding-summary.md"
    proc = subprocess.run(
        [
            sys.executable, "-m", "harness.onboard",
            "--repo", str(seeded_repo),
            "--skill", "stub-readme",
            "--skill", "stub-readme-second",
            "--output-path", str(summary_path),
            "--dry-run",
            "--non-interactive",
        ],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
    assert summary_path.is_file()
    content = summary_path.read_text()
    assert "## What ran" in content
    assert "stub-readme" in content
    assert "stub-readme-second" in content
    assert "## Pull requests opened" in content


def test_onboard_main_returns_nonzero_when_any_entry_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_path = tmp_path / "onboarding-summary.md"
    now = datetime.now(timezone.utc)

    monkeypatch.setattr(onboard_main.catalog, "tokenman_root", lambda: REPO_ROOT)
    monkeypatch.setattr(onboard_main.catalog, "load_catalog", lambda _root: {})
    monkeypatch.setattr(onboard_main.summary, "build", lambda **_kwargs: "summary")
    monkeypatch.setattr(
        onboard_main.onboarder,
        "run_onboarding",
        lambda **_kwargs: OnboardingResult(
            entries=[
                {
                    "run_id": "r-0001",
                    "ts": "2026-04-18T00:00:00Z",
                    "skill": "stub-readme",
                    "status": "error",
                    "pr": None,
                    "generator": {
                        "prompt_version": "harness-v1",
                        "output_summary": "failed",
                        "diff_lines": 0,
                        "tokens": 0,
                    },
                    "evaluator": None,
                    "duration_s": 0,
                    "total_tokens": 0,
                    "verdict": None,
                    "verdict_note": None,
                }
            ],
            total_tokens=0,
            session_ceiling=30_000,
            started_at=now,
            finished_at=now,
            breached_ceiling=False,
        ),
    )

    code = onboard_main.main(
        [
            "--repo",
            str(tmp_path),
            "--skill",
            "stub-readme",
            "--output-path",
            str(output_path),
            "--dry-run",
        ]
    )
    assert code == 1
    assert output_path.read_text() == "summary"
