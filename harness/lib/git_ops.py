"""Git operations for the tokenman runner.

Factored out of runner.py so the branch/apply/commit/push flow has a
single, unit-testable home. Executed after the executor produces a
proposed.diff and before pr_opener.open runs.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


class GitOpsError(RuntimeError):
    """Raised when any git step fails. Wraps the captured stderr."""


@dataclass(frozen=True)
class GitIdentity:
    name: str
    email: str


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


def apply_diff_and_push(
    *,
    repo_dir: Path,
    diff_text: str,
    branch: str,
    base: str,
    message: str,
    identity: GitIdentity,
    remote: str = "origin",
) -> None:
    """Create `branch` off `base`, apply `diff_text`, commit with
    `identity`, and push to `remote`.

    Rolls back the local branch on failure (deletes it if it was
    created by this call). Raises GitOpsError on any failed step.
    """
    created_branch = False

    sw = _run(["git", "switch", "-c", branch, base], cwd=repo_dir)
    if sw.returncode != 0:
        raise GitOpsError(f"git switch -c {branch} {base} failed: {sw.stderr.strip()}")
    created_branch = True

    try:
        ap = _run(["git", "apply", "--index", "-"], cwd=repo_dir, input_text=diff_text)
        if ap.returncode != 0:
            raise GitOpsError(f"git apply failed: {ap.stderr.strip()}")

        co = _run(
            [
                "git",
                "-c", f"user.name={identity.name}",
                "-c", f"user.email={identity.email}",
                "commit",
                "-m", message,
            ],
            cwd=repo_dir,
        )
        if co.returncode != 0:
            raise GitOpsError(f"git commit failed: {co.stderr.strip()}")

        ps = _run(["git", "push", "-u", remote, branch], cwd=repo_dir)
        if ps.returncode != 0:
            raise GitOpsError(f"git push failed: {ps.stderr.strip()}")

    except Exception:
        if created_branch:
            _run(["git", "switch", base], cwd=repo_dir)
            _run(["git", "branch", "-D", branch], cwd=repo_dir)
        raise
