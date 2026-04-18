"""Unit tests for harness.lib.catalog."""
from __future__ import annotations

from pathlib import Path

import pytest

from harness.lib import catalog
from harness.lib.catalog import SkillResolutionError


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def test_load_catalog_reads_mapping(tmp_path):
    root = tmp_path / "repo"
    _write(root / "recommended-skills.yaml",
           "foo:\n  source: ./skills/foo\n  version: 0.1.0\n")
    result = catalog.load_catalog(root)
    assert result == {"foo": {"source": "./skills/foo", "version": "0.1.0"}}


def test_load_catalog_empty_file_returns_empty(tmp_path):
    root = tmp_path / "repo"
    _write(root / "recommended-skills.yaml", "")
    assert catalog.load_catalog(root) == {}


def test_load_catalog_non_mapping_raises(tmp_path):
    root = tmp_path / "repo"
    _write(root / "recommended-skills.yaml", "- not\n- a\n- mapping\n")
    with pytest.raises(SkillResolutionError, match="must be a mapping"):
        catalog.load_catalog(root)


def test_resolve_skill_dir_local(tmp_path):
    tokenman_root = tmp_path / "lib"
    _write(tokenman_root / "skills" / "foo" / "SKILL.md", "x")
    cat = {"foo": {"source": "./skills/foo", "version": "0.1.0"}}
    path = catalog.resolve_skill_dir(
        skill_name="foo", catalog=cat,
        tokenman_root=tokenman_root, consumer_repo=tmp_path / "consumer",
    )
    assert path == (tokenman_root / "skills" / "foo").resolve()


def test_resolve_skill_dir_unknown_skill_raises(tmp_path):
    with pytest.raises(SkillResolutionError, match="not in recommended-skills.yaml"):
        catalog.resolve_skill_dir(
            skill_name="missing", catalog={},
            tokenman_root=tmp_path, consumer_repo=tmp_path,
        )


def test_resolve_skill_dir_missing_source_raises(tmp_path):
    with pytest.raises(SkillResolutionError, match="no 'source' field"):
        catalog.resolve_skill_dir(
            skill_name="foo", catalog={"foo": {}},
            tokenman_root=tmp_path, consumer_repo=tmp_path,
        )


def test_resolve_skill_dir_remote_installed(tmp_path):
    consumer = tmp_path / "consumer"
    _write(consumer / ".claude" / "skills" / "foo" / "SKILL.md", "x")
    cat = {"foo": {"source": "https://github.com/x/y", "version": "v1"}}
    path = catalog.resolve_skill_dir(
        skill_name="foo", catalog=cat,
        tokenman_root=tmp_path / "lib", consumer_repo=consumer,
    )
    assert path == (consumer / ".claude" / "skills" / "foo").resolve()


def test_resolve_skill_dir_remote_not_installed_raises(tmp_path):
    cat = {"foo": {"source": "https://github.com/x/y", "version": "v1"}}
    with pytest.raises(SkillResolutionError, match="not installed"):
        catalog.resolve_skill_dir(
            skill_name="foo", catalog=cat,
            tokenman_root=tmp_path / "lib", consumer_repo=tmp_path / "consumer",
        )
