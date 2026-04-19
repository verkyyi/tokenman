"""Unit tests for harness.git."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from harness.git import GitError, GitIdentity, commit_and_push, prepare_branch_checkout, stage_and_capture_diff


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
    (repo / "README.md").write_text("# Hello\n", encoding="utf-8")
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
    scratch = tmp_path / "scratch"
    branch = "tokenman/readme-maintainer/r-0001"

    worktree = prepare_branch_checkout(
        repo_dir=repo,
        scratch_dir=scratch,
        branch=branch,
        base="main",
        runtime_mode="local_debug",
    )
    (worktree / "README.md").write_text("# Hello\n## New section\n", encoding="utf-8")
    diff_text, changed_paths = stage_and_capture_diff(checkout_dir=worktree)
    assert changed_paths == ["README.md"]
    assert "## New section" in diff_text
    commit_and_push(
        checkout_dir=worktree,
        message="[tokenman] readme-maintainer: add section",
        identity=IDENTITY,
    )

    subprocess.run(
        ["git", "-C", str(repo), "worktree", "remove", "--force", str(worktree)],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "branch", "-D", branch],
        check=True,
        capture_output=True,
        text=True,
    )

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
    worktree = prepare_branch_checkout(
        repo_dir=repo,
        scratch_dir=tmp_path / "scratch",
        branch="tokenman/test/r-0001",
        base="main",
        runtime_mode="local_debug",
    )
    (worktree / ".claude" / "skills").mkdir(parents=True)
    (worktree / ".claude" / "skills" / "ignored.txt").write_text("x\n", encoding="utf-8")
    (worktree / ".tokenman").mkdir()
    (worktree / ".tokenman" / "ignored.txt").write_text("y\n", encoding="utf-8")
    diff_text, changed_paths = stage_and_capture_diff(checkout_dir=worktree)
    assert diff_text == ""
    assert changed_paths == []


def test_prepare_branch_checkout_raises_on_missing_base(tmp_path: Path) -> None:
    repo, _ = _make_repo_with_bare_remote(tmp_path)
    with pytest.raises(GitError):
        prepare_branch_checkout(
            repo_dir=repo,
            scratch_dir=tmp_path / "scratch",
            branch="tokenman/test/r-0001",
            base="does-not-exist",
            runtime_mode="local_debug",
        )
