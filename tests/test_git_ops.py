"""Unit tests for harness.lib.git_ops."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from harness.lib.git_ops import (
    GitIdentity,
    GitOpsError,
    commit_and_push,
    create_branch_worktree,
    remove_worktree,
    stage_and_capture_diff,
)


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def _make_repo_with_bare_remote(tmp_path: Path) -> tuple[Path, Path]:
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)

    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    (repo / "README.md").write_text("# Hello\n")
    _git(repo, "config", "user.email", "seed@local")
    _git(repo, "config", "user.name", "seed")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "seed")
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    return repo, remote


IDENTITY = GitIdentity(name="tokenman-bot", email="tokenman@local")


def test_worktree_diff_commit_and_push_creates_branch_commit_push(tmp_path: Path) -> None:
    repo, remote = _make_repo_with_bare_remote(tmp_path)
    worktree = tmp_path / "worktree"
    branch = "tokenman/readme-maintainer/r-0001"

    create_branch_worktree(
        repo_dir=repo,
        worktree_dir=worktree,
        branch=branch,
        base="main",
    )
    (worktree / "README.md").write_text("# Hello\n## New section\n")
    diff_text, changed_paths = stage_and_capture_diff(checkout_dir=worktree)
    assert changed_paths == ["README.md"]
    assert "## New section" in diff_text
    commit_and_push(
        checkout_dir=worktree,
        message="[tokenman] readme-maintainer: add section",
        identity=IDENTITY,
    )
    remove_worktree(repo_dir=repo, worktree_dir=worktree, branch=branch)

    branches = _git(repo, "branch", "--list")
    assert branch not in branches

    _git(repo, "fetch", "origin")
    log = _git(
        repo,
        "log",
        "-1",
        "--format=%an <%ae> %s",
        "origin/tokenman/readme-maintainer/r-0001",
    )
    assert "tokenman-bot <tokenman@local>" in log
    assert "add section" in log

    remote_refs = subprocess.run(
        ["git", "ls-remote", str(remote)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "refs/heads/tokenman/readme-maintainer/r-0001" in remote_refs


def test_stage_and_capture_diff_excludes_runtime_paths(tmp_path: Path) -> None:
    repo, _ = _make_repo_with_bare_remote(tmp_path)
    worktree = tmp_path / "worktree"
    branch = "tokenman/test/r-0001"

    create_branch_worktree(
        repo_dir=repo,
        worktree_dir=worktree,
        branch=branch,
        base="main",
    )
    (worktree / ".claude" / "skills").mkdir(parents=True)
    (worktree / ".claude" / "skills" / "ignored.txt").write_text("x\n")
    (worktree / ".tokenman").mkdir()
    (worktree / ".tokenman" / "ignored.txt").write_text("y\n")
    diff_text, changed_paths = stage_and_capture_diff(checkout_dir=worktree)
    assert diff_text == ""
    assert changed_paths == []
    remove_worktree(repo_dir=repo, worktree_dir=worktree, branch=branch)


def test_create_branch_worktree_raises_on_missing_base(tmp_path: Path) -> None:
    repo, _ = _make_repo_with_bare_remote(tmp_path)
    with pytest.raises(GitOpsError):
        create_branch_worktree(
            repo_dir=repo,
            worktree_dir=tmp_path / "worktree",
            branch="tokenman/test/r-0001",
            base="does-not-exist",
        )
