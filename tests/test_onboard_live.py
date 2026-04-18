"""Live test for `python -m harness.onboard`. Gated by TOKENMAN_LIVE=1."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


pytestmark = pytest.mark.skipif(
    os.environ.get("TOKENMAN_LIVE") != "1",
    reason="set TOKENMAN_LIVE=1 to run live claude -p onboarding test",
)


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


def test_onboard_live_against_tiny_repo(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    remote = tmp_path / "remote.git"
    _seed_git_repo(repo, remote)

    summary_path = tmp_path / "onboarding-summary.md"
    ledger_path = tmp_path / "ledger.jsonl"
    runs_dir = tmp_path / "runs"

    proc = subprocess.run(
        [
            sys.executable, "-m", "harness.onboard",
            "--repo", str(repo),
            "--skill", "readme-maintainer",
            "--ledger-path", str(ledger_path),
            "--runs-dir", str(runs_dir),
            "--output-path", str(summary_path),
            "--non-interactive",
        ],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=240,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
    assert summary_path.is_file()
    content = summary_path.read_text()
    assert "## What ran" in content
    assert "readme-maintainer" in content

    lines = [ln for ln in ledger_path.read_text().splitlines() if ln.strip()]
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["skill"] == "readme-maintainer"
    assert entry["status"] in {"pr_opened", "no_change", "error"}
