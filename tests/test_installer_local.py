"""Unit tests for install_skill's local-source (./…) path."""
from __future__ import annotations

from pathlib import Path

import pytest

from harness.lib.installer import InstallResult, install_skill


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def test_local_source_happy_path(tmp_path):
    tokenman_root = tmp_path / "lib"
    _write(tokenman_root / "skills" / "foo" / "SKILL.md", "x")
    target = tmp_path / "consumer" / ".claude" / "skills" / "foo"

    result = install_skill(
        skill_name="foo",
        catalog_entry={"source": "./skills/foo", "version": "0.1.0"},
        target_dir=target,
        tokenman_root=tokenman_root,
    )

    assert isinstance(result, InstallResult)
    assert result.skill_name == "foo"
    assert result.status == "unchanged"
    assert result.exit_code == 0
    assert result.resolved_sha is None
    assert "local" in result.message.lower()
    # Local sources are not copied into the consumer repo.
    assert not target.exists()


def test_local_source_missing_skill_md_errors(tmp_path):
    tokenman_root = tmp_path / "lib"
    (tokenman_root / "skills" / "foo").mkdir(parents=True)
    # No SKILL.md.
    target = tmp_path / "consumer" / ".claude" / "skills" / "foo"

    result = install_skill(
        skill_name="foo",
        catalog_entry={"source": "./skills/foo", "version": "0.1.0"},
        target_dir=target,
        tokenman_root=tokenman_root,
    )

    assert result.status == "errored"
    assert result.exit_code == 4
    assert "SKILL.md" in result.message


def test_result_is_frozen():
    r = InstallResult(
        skill_name="foo",
        status="unchanged",
        resolved_sha=None,
        message="ok",
        exit_code=0,
    )
    with pytest.raises(Exception):
        r.status = "errored"  # type: ignore[misc]
