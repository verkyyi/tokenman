"""Issue opener boundary for the harness runner."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Optional, Protocol


class IssueOpenerError(RuntimeError):
    """Raised when opening an issue fails. Wraps captured stderr."""


class IssueOpener(Protocol):
    """Opens an issue and returns its number."""

    def open(self, *, title: str, body: str) -> int: ...


class FakeIssueOpener:
    """In-process fake. Returns a monotonically incrementing integer."""

    def __init__(
        self,
        sink_dir: Optional[Path] = None,
        start: int = 2000,
    ) -> None:
        self._next = start
        self._sink_dir = sink_dir
        self.calls: list[dict] = []

    def open(self, *, title: str, body: str) -> int:
        n = self._next
        self._next += 1
        record = {
            "issue": n,
            "title": title,
            "body": body,
        }
        self.calls.append(record)
        if self._sink_dir is not None:
            self._sink_dir.mkdir(parents=True, exist_ok=True)
            (self._sink_dir / f"issue-{n}.json").write_text(json.dumps(record, indent=2))
        return n


class GhIssueOpener:
    """Calls `gh issue create` and parses the resulting issue URL."""

    def __init__(
        self,
        repo_dir: Path,
        gh_bin: str = "gh",
    ) -> None:
        self._repo_dir = repo_dir
        self._gh = gh_bin

    def open(self, *, title: str, body: str) -> int:
        proc = subprocess.run(
            [
                self._gh,
                "issue",
                "create",
                "--title",
                title,
                "--body",
                body,
            ],
            cwd=str(self._repo_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise IssueOpenerError(
                f"gh issue create failed (exit {proc.returncode}): {proc.stderr.strip()}"
            )

        stripped = proc.stdout.strip()
        match = re.search(r"/issues/(\d+)(?:\D*$|$)", stripped)
        if match is None:
            raise IssueOpenerError(
                f"gh issue create produced unexpected stdout: {stripped!r}"
            )
        return int(match.group(1))
