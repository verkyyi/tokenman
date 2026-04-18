"""Integration tests for harness.lib.skill_executor.StubSkillExecutor."""
from __future__ import annotations

from pathlib import Path

import pytest

from harness.lib.skill_executor import StubSkillExecutor


REPO_ROOT = Path(__file__).parent.parent
STUB_SKILL_DIR = REPO_ROOT / "tests" / "fixtures" / "skills" / "stub-readme"
FIXTURE_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def test_stub_no_change_mode(tmp_path: Path) -> None:
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    result = executor.execute(STUB_SKILL_DIR, FIXTURE_REPO, tmp_path)
    assert result.exit_code == 0
    assert result.proposed_diff_path is None
    assert result.proposed_md_path is None
    assert "no changes needed" in result.stdout
    assert result.summary.startswith("stub-readme: no changes")
    assert result.prompt_version == "stub-v1"
    assert result.tokens == 0


def test_stub_propose_diff_mode(tmp_path: Path) -> None:
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
    result = executor.execute(STUB_SKILL_DIR, FIXTURE_REPO, tmp_path)
    assert result.exit_code == 0
    assert result.proposed_diff_path == tmp_path / "proposed.diff"
    assert result.proposed_md_path == tmp_path / "proposed.md"
    assert result.proposed_diff_path.is_file()
    assert result.proposed_md_path.is_file()
    assert "proposed 1 diff" in result.stdout
    assert "Stub-readme added this line" in result.proposed_diff_path.read_text()
    assert result.prompt_version == "stub-v1"
    assert result.tokens == 0


def test_stub_crash_mode(tmp_path: Path) -> None:
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "crash"})
    result = executor.execute(STUB_SKILL_DIR, FIXTURE_REPO, tmp_path)
    assert result.exit_code == 2
    assert "crashing on purpose" in result.stderr
    assert result.proposed_diff_path is None
    assert result.prompt_version == "stub-v1"
    assert result.tokens == 0


def test_stub_default_mode_is_no_change(tmp_path: Path) -> None:
    # No STUB_MODE provided → stub.sh defaults to no_change.
    executor = StubSkillExecutor()
    result = executor.execute(STUB_SKILL_DIR, FIXTURE_REPO, tmp_path)
    assert result.exit_code == 0
    assert result.proposed_diff_path is None
