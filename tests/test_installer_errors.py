"""Error paths for install_skill: bad ref, missing SKILL.md, unsupported scheme."""
from __future__ import annotations

from pathlib import Path

from harness.lib.installer import install_skill


def test_unsupported_scheme(tmp_path):
    result = install_skill(
        skill_name="x",
        catalog_entry={"source": "git@github.com:foo/bar", "version": "v1"},
        target_dir=tmp_path / "target",
        tokenman_root=tmp_path / "root",
    )
    assert result.status == "errored"
    assert result.exit_code == 2
    assert "unsupported source scheme" in result.message


def test_missing_source(tmp_path):
    result = install_skill(
        skill_name="x", catalog_entry={"version": "v1"},
        target_dir=tmp_path / "t", tokenman_root=tmp_path,
    )
    assert result.exit_code == 2
    assert "source" in result.message


def test_missing_version(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    result = install_skill(
        skill_name="x", catalog_entry={"source": f"file://{remote}"},
        target_dir=tmp_path / "t", tokenman_root=tmp_path,
    )
    assert result.exit_code == 2
    assert "version" in result.message


def test_bad_ref_exits_3(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    target = tmp_path / "target"
    result = install_skill(
        skill_name="x",
        catalog_entry={"source": f"file://{remote}", "version": "does-not-exist"},
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "errored"
    assert result.exit_code == 3
    assert not target.exists()


def test_clone_failure_exits_3(tmp_path):
    target = tmp_path / "target"
    result = install_skill(
        skill_name="x",
        catalog_entry={"source": f"file://{tmp_path / 'nope'}", "version": "v1"},
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "errored"
    assert result.exit_code == 3
    assert not target.exists()


def test_missing_skill_md_rolls_back(tmp_path, build_local_git_repo):
    # Build a remote repo that lacks SKILL.md.
    empty_src = tmp_path / "empty-source"
    empty_src.mkdir()
    (empty_src / "README.md").write_text("no skill here")
    remote = build_local_git_repo(empty_src, subdir="empty-remote")

    target = tmp_path / "target"
    result = install_skill(
        skill_name="x",
        catalog_entry={"source": f"file://{remote}", "version": "v0.1.0"},
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "errored"
    assert result.exit_code == 4
    assert "SKILL.md" in result.message
    assert not target.exists()
