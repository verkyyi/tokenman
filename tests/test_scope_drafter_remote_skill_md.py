"""Verify scope_drafter._load_skill_md handles remote + local sources correctly."""
from __future__ import annotations

from pathlib import Path

from harness.lib import scope_drafter


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def test_remote_installed_reads_from_consumer_repo(tmp_path):
    consumer = tmp_path / "consumer"
    _write(consumer / ".claude" / "skills" / "foo" / "SKILL.md", "FOO SKILL MD")
    catalog = {
        "foo": {
            "source": "https://github.com/x/y", "version": "v1",
        },
    }
    result = scope_drafter._load_skill_md(
        catalog=catalog,
        catalog_root=tmp_path / "lib",
        consumer_repo=consumer,
    )
    assert result == {"foo": "FOO SKILL MD"}


def test_remote_not_installed_returns_none(tmp_path):
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    catalog = {
        "foo": {
            "source": "https://github.com/x/y", "version": "v1",
        },
    }
    result = scope_drafter._load_skill_md(
        catalog=catalog,
        catalog_root=tmp_path / "lib",
        consumer_repo=consumer,
    )
    assert result == {"foo": None}


def test_local_source_unchanged(tmp_path):
    catalog_root = tmp_path / "lib"
    _write(catalog_root / "skills" / "foo" / "SKILL.md", "LOCAL FOO")
    catalog = {"foo": {"source": "./skills/foo", "version": "0.1.0"}}
    result = scope_drafter._load_skill_md(
        catalog=catalog,
        catalog_root=catalog_root,
        consumer_repo=tmp_path / "consumer",
    )
    assert result == {"foo": "LOCAL FOO"}


def test_local_source_missing_file_returns_none(tmp_path):
    catalog_root = tmp_path / "lib"
    (catalog_root / "skills" / "foo").mkdir(parents=True)
    # No SKILL.md.
    catalog = {"foo": {"source": "./skills/foo", "version": "0.1.0"}}
    result = scope_drafter._load_skill_md(
        catalog=catalog,
        catalog_root=catalog_root,
        consumer_repo=tmp_path / "consumer",
    )
    assert result == {"foo": None}
