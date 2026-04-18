"""Unit tests for harness.lib.marketplace."""
from __future__ import annotations

from pathlib import Path

from harness.lib import marketplace

REPO_ROOT = Path(__file__).resolve().parent.parent
FAKE_ROOT = REPO_ROOT / "tests" / "fixtures" / "fake-marketplaces"


def test_list_plugins_reads_wellformed_manifest() -> None:
    plugins = marketplace.list_plugins(root=FAKE_ROOT)
    names = [p["name"] for p in plugins]
    assert "readme-sync" in names
    assert "dep-bumper" in names
    readme = next(p for p in plugins if p["name"] == "readme-sync")
    assert readme["marketplace"] == "one"
    assert readme["description"] == "Keep README in sync with code"


def test_list_plugins_skips_malformed_manifest(capsys) -> None:
    plugins = marketplace.list_plugins(root=FAKE_ROOT)
    assert any(p["marketplace"] == "one" for p in plugins)
    assert not any(p["marketplace"] == "two" for p in plugins)
    captured = capsys.readouterr()
    assert "two" in captured.err or "malformed" in captured.err.lower()


def test_list_plugins_missing_root_returns_empty(tmp_path: Path) -> None:
    plugins = marketplace.list_plugins(root=tmp_path / "does-not-exist")
    assert plugins == []
