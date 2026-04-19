"""GitHub CLI helpers for PR and issue routing."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path


class GitHubError(RuntimeError):
    """Raised when a GitHub CLI action fails."""


def open_pull_request(
    *,
    repo_dir: Path,
    title: str,
    body: str,
    branch: str,
    base_branch: str = "main",
    gh_bin: str = "gh",
) -> int:
    proc = subprocess.run(
        [
            gh_bin,
            "pr",
            "create",
            "--draft",
            "--title",
            title,
            "--body",
            body,
            "--head",
            branch,
            "--base",
            base_branch,
        ],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise GitHubError(
            f"gh pr create failed (exit {proc.returncode}): {proc.stderr.strip()}"
        )
    return _extract_number(proc.stdout.strip(), kind="pull")


def open_issue(
    *,
    repo_dir: Path,
    title: str,
    body: str,
    gh_bin: str = "gh",
) -> int:
    proc = subprocess.run(
        [
            gh_bin,
            "issue",
            "create",
            "--title",
            title,
            "--body",
            body,
        ],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise GitHubError(
            f"gh issue create failed (exit {proc.returncode}): {proc.stderr.strip()}"
        )
    return _extract_number(proc.stdout.strip(), kind="issue")


def _extract_number(stdout: str, *, kind: str) -> int:
    path = "pull" if kind == "pull" else "issues"
    match = re.search(rf"/{path}/(\d+)(?:\D*$|$)", stdout)
    if match is None:
        raise GitHubError(f"gh {kind} create produced unexpected stdout: {stdout!r}")
    return int(match.group(1))
