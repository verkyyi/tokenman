"""Opt-in live test that actually calls `claude -p`.

Skipped unless TOKENMAN_LIVE=1 (configured in tests/conftest.py).
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from harness.lib.skill_executor import ClaudeSkillExecutor


pytestmark = pytest.mark.live


REPO_ROOT = Path(__file__).parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "readme-maintainer"  # added in ii.7
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def test_readme_maintainer_runs_without_crashing(tmp_path: Path) -> None:
    if not SKILL_DIR.exists():
        pytest.skip("skills/readme-maintainer/ not yet present (see ii.7)")

    repo = tmp_path / "repo"
    shutil.copytree(FIXTURE, repo)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    executor = ClaudeSkillExecutor(timeout_s=600)
    result = executor.execute(skill_dir=SKILL_DIR, repo_dir=repo, scratch_dir=scratch)

    # Either claude produced a diff, or it chose not to — both are valid outcomes.
    assert result.exit_code == 0, f"claude exited nonzero: {result.stderr}"
    if result.proposed_diff_path is not None:
        diff = result.proposed_diff_path.read_text()
        assert "README.md" in diff, "skill should scope to README.md only"
    assert result.tokens > 0, "live run should report a nonzero token count"
