"""Shared pytest fixtures."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest


def pytest_collection_modifyitems(config, items):
    if os.environ.get("TOKENMAN_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="set TOKENMAN_LIVE=1 to run live tests")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=test", "-c", "user.email=t@t", *args],
        cwd=str(cwd), check=True, capture_output=True, text=True,
    )


def _build_local_git_repo(
    *,
    source_tree: Path,
    dest: Path,
    tag: str = "v0.1.0",
) -> Path:
    """Copy source_tree into a fresh git repo at dest, commit, tag.

    Returns dest — a plain clone-able directory (not a bare repo).
    Used as the `source:` URL for remote-source installer tests.
    """
    dest.mkdir(parents=True, exist_ok=True)
    for entry in source_tree.iterdir():
        if entry.is_dir():
            shutil.copytree(entry, dest / entry.name)
        else:
            shutil.copy2(entry, dest / entry.name)
    _git(dest, "init", "-q", "-b", "main")
    _git(dest, "add", "-A")
    _git(dest, "commit", "-q", "-m", "initial")
    _git(dest, "tag", tag)
    return dest


@pytest.fixture
def build_local_git_repo(tmp_path):
    """Factory: create a local git repo from a source tree.

    Returns a callable that takes (source_tree: Path, *, tag="v0.1.0",
    subdir="remote-repo") and returns the path to a clone-able repo
    under tmp_path.
    """
    def _make(
        source_tree: Path,
        *,
        tag: str = "v0.1.0",
        subdir: str = "remote-repo",
    ) -> Path:
        return _build_local_git_repo(
            source_tree=source_tree, dest=tmp_path / subdir, tag=tag,
        )
    return _make


@pytest.fixture
def fake_skill_source():
    """Path to the checked-in fake-skill source tree."""
    return Path(__file__).parent / "fixtures" / "remote-skills" / "fake-skill"
