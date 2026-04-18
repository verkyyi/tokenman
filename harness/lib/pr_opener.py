"""PR opener boundary for the harness runner.

Phase 1.2a ships a FakePROpener used in tests. Phase 1.2b adds a
GhPROpener that calls `gh pr create` against a real remote.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Protocol


class PROpener(Protocol):
    """Opens a PR and returns its number."""

    def open(self, *, title: str, body: str, branch: str, diff: str) -> int: ...


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

    def open(self, *, title: str, body: str, branch: str, diff: str) -> int:
        n = self._next
        self._next += 1
        record = {
            "pr": n,
            "title": title,
            "body": body,
            "branch": branch,
            "diff": diff,
        }
        self.calls.append(record)
        if self._sink_dir is not None:
            self._sink_dir.mkdir(parents=True, exist_ok=True)
            (self._sink_dir / f"pr-{n}.json").write_text(
                json.dumps(record, indent=2)
            )
        return n
