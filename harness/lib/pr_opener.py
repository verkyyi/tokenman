"""PR opener boundary for the harness runner.

Phase 1.2a shipped FakePROpener for tests. 1.2b-ii adds GhPROpener
which runs `gh pr create` against a real remote; the runner has
already created, committed to, and pushed the branch via git_ops.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Optional, Protocol


class PROpenerError(RuntimeError):
    """Raised when opening a PR fails. Wraps captured stderr."""


class PROpener(Protocol):
    """Opens a PR and returns its number."""

    def open(self, *, title: str, body: str, branch: str) -> int: ...


class FakePROpener:
    """In-process fake. Returns a monotonically incrementing integer.

    When sink_dir is supplied, each call is also persisted as
    pr-<n>.json for test inspection.
    """

    def __init__(
        self,
        sink_dir: Optional[Path] = None,
        start: int = 1000,
    ) -> None:
        self._next = start
        self._sink_dir = sink_dir
        self.calls: list[dict] = []

    def open(self, *, title: str, body: str, branch: str) -> int:
        n = self._next
        self._next += 1
        record = {
            "pr": n,
            "title": title,
            "body": body,
            "branch": branch,
        }
        self.calls.append(record)
        if self._sink_dir is not None:
            self._sink_dir.mkdir(parents=True, exist_ok=True)
            (self._sink_dir / f"pr-{n}.json").write_text(
                json.dumps(record, indent=2)
            )
        return n


class GhPROpener:
    """Calls `gh pr create --json number -q .number` and parses the result.

    Assumes the branch already exists locally and has been pushed (the
    runner does this via git_ops.apply_diff_and_push before calling us).
    """

    def __init__(
        self,
        repo_dir: Path,
        base_branch: str = "main",
        gh_bin: str = "gh",
    ) -> None:
        self._repo_dir = repo_dir
        self._base = base_branch
        self._gh = gh_bin

    def open(self, *, title: str, body: str, branch: str) -> int:
        proc = subprocess.run(
            [
                self._gh, "pr", "create",
                "--title", title,
                "--body", body,
                "--head", branch,
                "--base", self._base,
                "--json", "number",
                "-q", ".number",
            ],
            cwd=str(self._repo_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise PROpenerError(
                f"gh pr create failed (exit {proc.returncode}): {proc.stderr.strip()}"
            )
        stripped = proc.stdout.strip()
        try:
            return int(stripped)
        except ValueError:
            raise PROpenerError(
                f"gh pr create produced non-integer stdout: {stripped!r}"
            )
