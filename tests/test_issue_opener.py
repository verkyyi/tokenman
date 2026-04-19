"""Tests for harness.lib.issue_opener."""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.issue_opener import FakeIssueOpener


def test_fake_issue_opener_returns_incrementing_integers() -> None:
    op = FakeIssueOpener()
    n1 = op.open(title="t1", body="b1")
    n2 = op.open(title="t2", body="b2")
    n3 = op.open(title="t3", body="b3")
    assert n2 == n1 + 1
    assert n3 == n2 + 1


def test_fake_issue_opener_custom_start() -> None:
    op = FakeIssueOpener(start=800)
    n1 = op.open(title="t", body="b")
    assert n1 == 800


def test_fake_issue_opener_records_calls() -> None:
    op = FakeIssueOpener()
    op.open(title="hello", body="world")
    assert len(op.calls) == 1
    call = op.calls[0]
    assert call["title"] == "hello"
    assert call["body"] == "world"


def test_fake_issue_opener_writes_sink_files(tmp_path: Path) -> None:
    sink = tmp_path / "issues"
    op = FakeIssueOpener(sink_dir=sink, start=900)
    n = op.open(title="t", body="b")
    assert n == 900
    written = sink / "issue-900.json"
    assert written.is_file()
    data = json.loads(written.read_text())
    assert data["issue"] == 900
    assert data["title"] == "t"
