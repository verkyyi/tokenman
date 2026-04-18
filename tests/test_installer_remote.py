"""Unit tests for install_skill's remote-source happy path."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from harness.lib.installer import install_skill


def test_remote_happy_path(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    target = tmp_path / "consumer" / ".claude" / "skills" / "fake-skill"
    tokenman_root = tmp_path / "lib"
    tokenman_root.mkdir()

    result = install_skill(
        skill_name="fake-skill",
        catalog_entry={"source": f"file://{remote}", "version": "v0.1.0"},
        target_dir=target,
        tokenman_root=tokenman_root,
    )

    assert result.status == "installed", result.message
    assert result.exit_code == 0
    assert result.resolved_sha and len(result.resolved_sha) == 40

    assert (target / "SKILL.md").is_file()
    assert (target / "README.md").is_file()
    assert not (target / ".git").exists()

    lock = json.loads((target / ".tokenman-skill-lock").read_text())
    assert lock["source"] == f"file://{remote}"
    assert lock["version"] == "v0.1.0"
    assert lock["resolved_sha"] == result.resolved_sha
    assert lock["installed_at"].endswith("Z")


def test_remote_checkout_by_sha(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    sha = subprocess.run(
        ["git", "-C", str(remote), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    target = tmp_path / "consumer" / ".claude" / "skills" / "fake-skill"
    tokenman_root = tmp_path / "lib"
    tokenman_root.mkdir()

    result = install_skill(
        skill_name="fake-skill",
        catalog_entry={"source": f"file://{remote}", "version": sha},
        target_dir=target,
        tokenman_root=tokenman_root,
    )

    assert result.status == "installed", result.message
    assert result.resolved_sha == sha
