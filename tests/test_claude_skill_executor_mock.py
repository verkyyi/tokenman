"""Unit tests for ClaudeSkillExecutor — plumbing only (subprocess mocked)."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from harness.lib.skill_executor import ClaudeSkillExecutor


def _make_skill_dir(tmp_path: Path) -> Path:
    """A minimal skill directory with a SKILL.md placeholder."""
    d = tmp_path / "skills" / "readme-maintainer"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(
        "# readme-maintainer\n\nEdit README.md.\n"
    )
    return d


def _make_repo_dir(tmp_path: Path) -> Path:
    d = tmp_path / "repo"
    d.mkdir()
    (d / "README.md").write_text("# Title\n\noriginal body\n")
    return d


def test_claude_invocation_argv_and_env(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    json_stdout = json.dumps({
        "role": "assistant",
        "result": "no-op, nothing to do",
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
        },
    })

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        # First call is `claude -p ...`; second is `diff -ruN ...`.
        m.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout=json_stdout, stderr=""),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]
        executor = ClaudeSkillExecutor(claude_bin="claude", timeout_s=60)
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    # claude call: assert argv shape
    claude_call = m.call_args_list[0]
    argv = claude_call.args[0]
    assert argv[0] == "claude"
    assert "-p" in argv
    assert "--output-format" in argv and "json" in argv
    assert "--append-system-prompt" in argv
    # cwd is the working copy inside scratch
    assert claude_call.kwargs["cwd"].endswith(str(scratch / "working"))
    # timeout passed
    assert claude_call.kwargs["timeout"] == 60
    # user prompt names the skill
    assert any("readme-maintainer" in a for a in argv)

    # Working copy exists and has the skill overlaid at .claude/skills/<name>
    assert (scratch / "working" / "README.md").exists()
    assert (scratch / "working" / ".claude" / "skills" / "readme-maintainer" / "SKILL.md").exists()

    # Result fields
    assert result.prompt_version == "harness-v1"
    assert result.tokens == 150
    assert result.exit_code == 0
    assert result.proposed_diff_path is None  # diff stdout was empty
    assert ("no-op" in result.summary.lower()) or ("nothing" in result.summary.lower())


def test_claude_tokens_sum_with_cache_fields(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    json_stdout = json.dumps({
        "role": "assistant",
        "result": "stopped",
        "usage": {
            "input_tokens": 10,
            "output_tokens": 20,
            "cache_creation_input_tokens": 100,
            "cache_read_input_tokens": 200,
        },
    })

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout=json_stdout, stderr=""),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]
        executor = ClaudeSkillExecutor()
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    assert result.tokens == 10 + 20 + 100 + 200


def test_claude_produces_diff_when_working_differs(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    json_stdout = json.dumps({
        "role": "assistant",
        "result": "added a section",
        "usage": {"input_tokens": 1, "output_tokens": 1},
    })
    fake_diff = (
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1 +1,2 @@\n"
        " # Title\n"
        "+## New\n"
    )

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout=json_stdout, stderr=""),
            # `diff` returns 1 when differences exist; not an error for us.
            subprocess.CompletedProcess(args=[], returncode=1, stdout=fake_diff, stderr=""),
        ]
        executor = ClaudeSkillExecutor()
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    assert result.proposed_diff_path is not None
    assert (scratch / "proposed.diff").read_text() == fake_diff
    assert (scratch / "proposed.md").exists()


def test_claude_timeout_surfaces_as_error(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.side_effect = subprocess.TimeoutExpired(cmd=["claude"], timeout=1)
        executor = ClaudeSkillExecutor(timeout_s=1)
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    assert result.exit_code == -1
    assert "timed out" in result.stderr
    assert result.proposed_diff_path is None
