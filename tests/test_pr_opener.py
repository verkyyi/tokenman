"""Tests for harness.lib.pr_opener."""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.pr_opener import FakePROpener


def test_fake_pr_opener_returns_incrementing_integers() -> None:
    op = FakePROpener()
    n1 = op.open(title="t1", body="b1", branch="br1", diff="d1")
    n2 = op.open(title="t2", body="b2", branch="br2", diff="d2")
    n3 = op.open(title="t3", body="b3", branch="br3", diff="d3")
    assert n2 == n1 + 1
    assert n3 == n2 + 1


def test_fake_pr_opener_custom_start() -> None:
    op = FakePROpener(start=500)
    n1 = op.open(title="t", body="b", branch="br", diff="d")
    assert n1 == 500


def test_fake_pr_opener_records_calls() -> None:
    op = FakePROpener()
    op.open(title="hello", body="world", branch="tokenman/x/r-0001", diff="--- a\n+++ b\n")
    assert len(op.calls) == 1
    call = op.calls[0]
    assert call["title"] == "hello"
    assert call["body"] == "world"
    assert call["branch"] == "tokenman/x/r-0001"
    assert call["diff"] == "--- a\n+++ b\n"


def test_fake_pr_opener_writes_sink_files(tmp_path: Path) -> None:
    sink = tmp_path / "prs"
    op = FakePROpener(sink_dir=sink, start=2000)
    n = op.open(title="t", body="b", branch="br", diff="d")
    assert n == 2000
    written = sink / "pr-2000.json"
    assert written.is_file()
    data = json.loads(written.read_text())
    assert data["pr"] == 2000
    assert data["title"] == "t"
