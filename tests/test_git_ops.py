"""Unit tests for harness.lib.git_ops."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from harness.lib.git_ops import (
    GitIdentity,
    GitOpsError,
    apply_diff_and_push,
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
    """Initialise a working repo with a bare remote at tmp_path/remote.
    Returns (repo_dir, remote_dir). repo_dir has one commit on main and
    tracks origin=main.
    """
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)

    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    (repo / "README.md").write_text("# Hello\n")
    _git(repo, "config", "user.email", "seed@local")
    _git(repo, "config", "user.name",  "seed")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "seed")
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    return repo, remote


IDENTITY = GitIdentity(name="tokenman-bot", email="tokenman@local")


def test_apply_diff_and_push_creates_branch_commit_push(tmp_path: Path) -> None:
    repo, remote = _make_repo_with_bare_remote(tmp_path)
    diff_text = (
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1 +1,2 @@\n"
        " # Hello\n"
        "+## New section\n"
    )
    apply_diff_and_push(
        repo_dir=repo,
        diff_text=diff_text,
        branch="tokenman/readme-maintainer/r-0001",
        base="main",
        message="[tokenman] readme-maintainer: add section",
        identity=IDENTITY,
    )

    # local branch exists
    branches = _git(repo, "branch", "--list")
    assert "tokenman/readme-maintainer/r-0001" in branches

    # commit author identity is ours
    log = _git(repo, "log", "-1", "--format=%an <%ae> %s", "tokenman/readme-maintainer/r-0001")
    assert "tokenman-bot <tokenman@local>" in log
    assert "add section" in log

    # switching to the branch shows the applied change
    _git(repo, "switch", "tokenman/readme-maintainer/r-0001")
    assert "## New section" in (repo / "README.md").read_text()

    # remote has the pushed branch
    remote_refs = subprocess.run(
        ["git", "ls-remote", str(remote)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "refs/heads/tokenman/readme-maintainer/r-0001" in remote_refs


def test_apply_diff_and_push_raises_on_bad_diff(tmp_path: Path) -> None:
    repo, _ = _make_repo_with_bare_remote(tmp_path)
    bogus_diff = "not a valid unified diff at all\n"
    with pytest.raises(GitOpsError):
        apply_diff_and_push(
            repo_dir=repo,
            diff_text=bogus_diff,
            branch="tokenman/does-not-matter/r-0001",
            base="main",
            message="won't apply",
            identity=IDENTITY,
        )

    # no branch left behind with extra commits
    branches = _git(repo, "branch", "--list")
    if "tokenman/does-not-matter/r-0001" in branches:
        head = _git(repo, "rev-parse", "tokenman/does-not-matter/r-0001").strip()
        base = _git(repo, "rev-parse", "main").strip()
        assert head == base
