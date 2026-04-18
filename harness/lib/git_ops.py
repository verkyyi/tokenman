"""Git operations for the tokenman runner."""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


RuntimeMode = Literal["actions", "local_debug"]


class GitOpsError(RuntimeError):
    """Raised when any git step fails. Wraps the captured stderr."""


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


def _switch_in_place_branch(*, repo_dir: Path, branch: str, base: str) -> None:
    proc = _run(["git", "switch", "-c", branch, base], cwd=repo_dir)
    if proc.returncode != 0:
        raise GitOpsError(f"git switch -c {branch} {base} failed: {proc.stderr.strip()}")


def create_branch_worktree(
    *,
    repo_dir: Path,
    worktree_dir: Path,
    branch: str,
    base: str,
) -> None:
    worktree_dir.parent.mkdir(parents=True, exist_ok=True)
    proc = _run(
        ["git", "worktree", "add", "-b", branch, str(worktree_dir), base],
        cwd=repo_dir,
    )
    if proc.returncode != 0:
        raise GitOpsError(
            f"git worktree add -b {branch} {worktree_dir} {base} failed: "
            f"{proc.stderr.strip()}"
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
        _switch_in_place_branch(repo_dir=repo_dir, branch=branch, base=base)
        return repo_dir

    worktree_dir = scratch_dir / "worktree"
    create_branch_worktree(
        repo_dir=repo_dir,
        worktree_dir=worktree_dir,
        branch=branch,
        base=base,
    )
    return worktree_dir


def stage_and_capture_diff(*, checkout_dir: Path) -> tuple[str, list[str]]:
    add = _run(
        ["git", "add", "-A", "--", ".", *_EXCLUDED_PATHS],
        cwd=checkout_dir,
    )
    if add.returncode != 0:
        raise GitOpsError(f"git add failed: {add.stderr.strip()}")

    names = _run(
        ["git", "diff", "--cached", "--name-only", "--", ".", *_EXCLUDED_PATHS],
        cwd=checkout_dir,
    )
    if names.returncode != 0:
        raise GitOpsError(f"git diff --name-only failed: {names.stderr.strip()}")

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
        raise GitOpsError(f"git diff failed: {diff.stderr.strip()}")
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
        raise GitOpsError(f"git commit failed: {commit.stderr.strip()}")

    push = _run(["git", "push", "-u", remote, "HEAD"], cwd=checkout_dir)
    if push.returncode != 0:
        raise GitOpsError(f"git push failed: {push.stderr.strip()}")


def remove_worktree(
    *,
    repo_dir: Path,
    worktree_dir: Path,
    branch: str,
) -> None:
    _run(["git", "worktree", "remove", "--force", str(worktree_dir)], cwd=repo_dir)
    _run(["git", "branch", "-D", branch], cwd=repo_dir)


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

    remove_worktree(repo_dir=repo_dir, worktree_dir=checkout_dir, branch=branch)
