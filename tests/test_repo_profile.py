"""Unit tests for harness.lib.repo_profile."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from harness.lib import repo_profile

REPO_ROOT = Path(__file__).resolve().parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def _git_init(repo_dir: Path) -> None:
    subprocess.run(["git", "-C", str(repo_dir), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.name", "seed"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo_dir), "commit", "-m", "seed"],
        check=True, capture_output=True,
    )


def _copy_fixture(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    _git_init(repo)
    return repo


def test_inspect_tiny_python_repo(tmp_path: Path) -> None:
    repo = _copy_fixture(tmp_path)
    profile = repo_profile.inspect(repo)
    assert profile["readme_present"] is True
    assert profile["tests_present"] is True
    assert "pyproject.toml" in profile["deps_files"]
    assert profile["languages"].get("python", 0) >= 1
    assert profile["total_files"] > 0
    assert profile["total_bytes"] > 0
    assert profile["recent_commits_30d"] >= 1


def test_inspect_rejects_non_git_dir(tmp_path: Path) -> None:
    with pytest.raises(repo_profile.RepoProfileError):
        repo_profile.inspect(tmp_path)


def test_inspect_empty_repo(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    profile = repo_profile.inspect(repo)
    assert profile["total_files"] == 0
    assert profile["recent_commits_30d"] == 0
    assert profile["readme_present"] is False
    assert profile["tests_present"] is False


def test_inspect_detects_ci(tmp_path: Path) -> None:
    repo = _copy_fixture(tmp_path)
    (repo / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (repo / ".github" / "workflows" / "test.yml").write_text("name: x\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "add-ci"],
        check=True, capture_output=True,
    )
    profile = repo_profile.inspect(repo)
    assert profile["ci_present"] is True
