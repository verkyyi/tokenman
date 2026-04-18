"""Unit tests for harness.scope.__main__ — rendering and CLI shape."""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.repo_profile import RepoProfile
from harness.lib.scope_drafter import ScopeDraft
from harness.scope import __main__ as scope_cli

REPO_ROOT = Path(__file__).resolve().parent.parent
CANNED = REPO_ROOT / "tests" / "fixtures" / "scope-captures" / "minimal.json"


def _profile() -> RepoProfile:
    return RepoProfile(
        languages={"python": 3, "markdown": 1},
        total_files=4, total_bytes=512,
        tests_present=True, ci_present=False, readme_present=True,
        deps_files=["pyproject.toml"], recent_commits_30d=2,
    )


def _draft() -> ScopeDraft:
    return json.loads(CANNED.read_text())  # type: ignore[return-value]


def test_render_markdown_contains_all_sections() -> None:
    md = scope_cli._render_markdown(
        draft=_draft(), profile=_profile(), repo_name="tiny", prompt_version="v1",
    )
    assert "# Tokenman — Initial scope for tiny" in md
    assert "## Repo profile" in md
    assert "## Recommended skills" in md
    assert "## Skills considered but skipped" in md
    assert "## Candidates for catalog" in md
    assert "## Suggested boundaries" in md
    assert "## What's not here yet" in md
    assert "readme-maintainer" in md
    assert "pyproject.toml" in md


def test_render_markdown_empty_sections_use_placeholders() -> None:
    draft = _draft()
    draft["recommended_skills"] = []
    draft["skipped_skills"] = []
    draft["candidate_uncurated_plugins"] = []
    md = scope_cli._render_markdown(
        draft=draft, profile=_profile(), repo_name="tiny", prompt_version="v1",
    )
    assert "No skills from the curated catalog match this repo yet." in md
    assert "None." in md


def test_render_markdown_notes_empty_marketplace(tmp_path: Path) -> None:
    draft = _draft()
    draft["candidate_uncurated_plugins"] = []
    md = scope_cli._render_markdown(
        draft=draft, profile=_profile(), repo_name="tiny",
        prompt_version="v1", marketplaces_empty=True,
    )
    assert "No marketplaces configured" in md


import shutil
import subprocess
import sys


def _git_init_tmp(repo: Path) -> None:
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "seed"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "seed"], check=True, capture_output=True)


def test_cli_dry_run_non_interactive_writes_scope_file(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    shutil.copytree(REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo", repo)
    _git_init_tmp(repo)

    out_path = tmp_path / "initial-scope.md"
    proc = subprocess.run(
        [sys.executable, "-m", "harness.scope",
         "--repo", str(repo),
         "--output-path", str(out_path),
         "--dry-run", "--non-interactive"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert proc.returncode == 0, proc.stderr
    assert out_path.exists()
    content = out_path.read_text()
    assert "# Tokenman — Initial scope for" in content
    assert "## Recommended skills" in content


def test_cli_missing_git_exits_nonzero(tmp_path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "harness.scope",
         "--repo", str(tmp_path),
         "--dry-run", "--non-interactive"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert proc.returncode != 0
