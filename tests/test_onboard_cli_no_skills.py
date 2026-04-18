"""harness.onboard CLI exits 2 with a hint when no skills are available."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


@pytest.fixture
def repo_without_config(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    config = repo / ".tokenman" / "tokenman.yaml"
    if config.exists():
        config.unlink()
    return repo


def test_cli_exits_2_when_no_skills(
    repo_without_config: Path, tmp_path: Path,
) -> None:
    proc = subprocess.run(
        [
            sys.executable, "-m", "harness.onboard",
            "--repo", str(repo_without_config),
            "--output-path", str(tmp_path / "summary.md"),
            "--non-interactive",
        ],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert proc.returncode == 2
    assert "no skills" in proc.stderr.lower()
    assert "harness.scope" in proc.stderr or "--skill" in proc.stderr
    assert not (tmp_path / "summary.md").exists()
