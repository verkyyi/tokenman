"""install_skill honors an optional `path:` subdir in the catalog entry."""
from __future__ import annotations

from pathlib import Path

from harness.lib.installer import install_skill


def test_path_subdir_copies_only_subtree(tmp_path, build_local_git_repo):
    # Remote layout:
    #   README.md     (not in path:)
    #   skill/SKILL.md
    #   skill/helper.sh
    src = tmp_path / "multi-skill-source"
    (src / "skill").mkdir(parents=True)
    (src / "README.md").write_text("repo-level README")
    (src / "skill" / "SKILL.md").write_text("---\nname: x\n---\n")
    (src / "skill" / "helper.sh").write_text("#!/bin/sh\necho hi\n")

    remote = build_local_git_repo(src, subdir="remote-multi")
    target = tmp_path / "consumer" / ".claude" / "skills" / "x"

    result = install_skill(
        skill_name="x",
        catalog_entry={
            "source": f"file://{remote}",
            "version": "v0.1.0",
            "path": "skill",
        },
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "installed", result.message
    assert (target / "SKILL.md").is_file()
    assert (target / "helper.sh").is_file()
    assert not (target / "README.md").exists()


def test_path_subdir_missing_exits_4(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    target = tmp_path / "target"
    result = install_skill(
        skill_name="x",
        catalog_entry={
            "source": f"file://{remote}",
            "version": "v0.1.0",
            "path": "nowhere",
        },
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "errored"
    assert result.exit_code == 4
    assert "path" in result.message.lower()
    assert not target.exists()
