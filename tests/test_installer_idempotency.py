"""Idempotency, drift, and --force behavior for install_skill."""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.installer import install_skill


def _install_once(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    target = tmp_path / "consumer" / ".claude" / "skills" / "fake-skill"
    tokenman_root = tmp_path / "lib"
    tokenman_root.mkdir()
    entry = {"source": f"file://{remote}", "version": "v0.1.0"}
    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=tokenman_root,
    )
    assert result.status == "installed"
    return remote, target, tokenman_root, entry, result


def test_unchanged_when_lock_matches(tmp_path, build_local_git_repo, fake_skill_source):
    _, target, root, entry, first = _install_once(tmp_path, build_local_git_repo, fake_skill_source)
    # Touch a file to prove unchanged really doesn't mutate.
    sentinel = target / "SENTINEL"
    sentinel.write_text("keep me")

    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=root,
    )
    assert result.status == "unchanged"
    assert result.exit_code == 0
    assert result.resolved_sha == first.resolved_sha
    assert sentinel.read_text() == "keep me"


def test_drift_without_force_errors(tmp_path, build_local_git_repo, fake_skill_source):
    _, target, root, entry, _ = _install_once(tmp_path, build_local_git_repo, fake_skill_source)
    # Corrupt the lock to simulate drift.
    lock_path = target / ".tokenman-skill-lock"
    lock = json.loads(lock_path.read_text())
    lock["resolved_sha"] = "0" * 40
    lock_path.write_text(json.dumps(lock))
    sentinel = target / "SENTINEL"
    sentinel.write_text("keep me")

    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=root,
    )
    assert result.status == "errored"
    assert result.exit_code == 5
    assert "--force" in result.message
    assert sentinel.read_text() == "keep me"  # not touched


def test_drift_with_force_reinstalls(tmp_path, build_local_git_repo, fake_skill_source):
    _, target, root, entry, first = _install_once(tmp_path, build_local_git_repo, fake_skill_source)
    lock_path = target / ".tokenman-skill-lock"
    lock = json.loads(lock_path.read_text())
    lock["resolved_sha"] = "0" * 40
    lock_path.write_text(json.dumps(lock))
    sentinel = target / "SENTINEL"
    sentinel.write_text("should be removed")

    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=root, force=True,
    )
    assert result.status == "installed"
    assert result.resolved_sha == first.resolved_sha
    assert not sentinel.exists()


def test_missing_lock_treated_as_drift(tmp_path, build_local_git_repo, fake_skill_source):
    _, target, root, entry, _ = _install_once(tmp_path, build_local_git_repo, fake_skill_source)
    (target / ".tokenman-skill-lock").unlink()

    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=root,
    )
    assert result.status == "errored"
    assert result.exit_code == 5
