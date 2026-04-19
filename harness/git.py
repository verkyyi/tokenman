"""Git operations for the Tokenman action runtime."""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


RuntimeMode = Literal["actions", "local_debug"]


class GitError(RuntimeError):
    """Raised when a git step fails."""


@dataclass(frozen=True)
class GitIdentity:
    name: str
    email: str


_EXCLUDED_PATHS = [":(exclude).claude/**", ":(exclude).tokenman/**"]


def _run(
    cmd: list[str],
    *,
    cwd: Path,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def prepare_branch_checkout(
    *,
    repo_dir: Path,
    scratch_dir: Path,
    branch: str,
    base: str,
    runtime_mode: RuntimeMode,
) -> Path:
    if runtime_mode == "actions":
        proc = _run(["git", "switch", "-c", branch, base], cwd=repo_dir)
        if proc.returncode != 0:
            raise GitError(f"git switch -c {branch} {base} failed: {proc.stderr.strip()}")
        return repo_dir

    worktree_dir = scratch_dir / "worktree"
    worktree_dir.parent.mkdir(parents=True, exist_ok=True)
    proc = _run(
        ["git", "worktree", "add", "-b", branch, str(worktree_dir), base],
        cwd=repo_dir,
    )
    if proc.returncode != 0:
        raise GitError(
            f"git worktree add -b {branch} {worktree_dir} {base} failed: {proc.stderr.strip()}"
        )
    return worktree_dir


def stage_and_capture_diff(*, checkout_dir: Path) -> tuple[str, list[str]]:
    add = _run(["git", "add", "-A", "--", ".", *_EXCLUDED_PATHS], cwd=checkout_dir)
    if add.returncode != 0:
        raise GitError(f"git add failed: {add.stderr.strip()}")

    names = _run(
        ["git", "diff", "--cached", "--name-only", "--", ".", *_EXCLUDED_PATHS],
        cwd=checkout_dir,
    )
    if names.returncode != 0:
        raise GitError(f"git diff --name-only failed: {names.stderr.strip()}")

    changed_paths = [line for line in names.stdout.splitlines() if line.strip()]
    if not changed_paths:
        return "", []

    diff = _run(
        [
            "git",
            "diff",
            "--cached",
            "--binary",
            "--src-prefix=a/",
            "--dst-prefix=b/",
            "--",
            ".",
            *_EXCLUDED_PATHS,
        ],
        cwd=checkout_dir,
    )
    if diff.returncode != 0:
        raise GitError(f"git diff failed: {diff.stderr.strip()}")
    return diff.stdout, changed_paths


def commit_and_push(
    *,
    checkout_dir: Path,
    message: str,
    identity: GitIdentity,
    remote: str = "origin",
) -> None:
    commit = _run(
        [
            "git",
            "-c",
            f"user.name={identity.name}",
            "-c",
            f"user.email={identity.email}",
            "commit",
            "-m",
            message,
        ],
        cwd=checkout_dir,
    )
    if commit.returncode != 0:
        raise GitError(f"git commit failed: {commit.stderr.strip()}")

    push = _run(["git", "push", "-u", remote, "HEAD"], cwd=checkout_dir)
    if push.returncode != 0:
        raise GitError(f"git push failed: {push.stderr.strip()}")


def cleanup_branch_checkout(
    *,
    repo_dir: Path,
    checkout_dir: Path,
    branch: str,
    base: str,
    runtime_mode: RuntimeMode,
) -> None:
    if runtime_mode == "actions":
        _run(["git", "reset", "--hard", "HEAD"], cwd=repo_dir)
        _run(["git", "switch", base], cwd=repo_dir)
        _run(["git", "branch", "-D", branch], cwd=repo_dir)
        return

    _run(["git", "worktree", "remove", "--force", str(checkout_dir)], cwd=repo_dir)
    _run(["git", "branch", "-D", branch], cwd=repo_dir)
