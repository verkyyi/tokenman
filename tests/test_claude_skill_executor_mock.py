"""Unit tests for ClaudeSkillExecutor — plumbing only (subprocess mocked)."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

from harness.lib.skill_executor import ClaudeSkillExecutor


def _make_skill_dir(tmp_path: Path) -> Path:
    d = tmp_path / "skills" / "readme-maintainer"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text("# readme-maintainer\n\nEdit README.md.\n")
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

    json_stdout = json.dumps(
        {
            "role": "assistant",
            "result": "no-op, nothing to do",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 50,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
        }
    )

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=json_stdout, stderr=""
        )
        executor = ClaudeSkillExecutor(claude_bin="claude", timeout_s=60)
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    claude_call = m.call_args
    argv = claude_call.args[0]
    assert argv[0] == "claude"
    assert "-p" in argv
    assert "--output-format" in argv and "json" in argv
    assert "--append-system-prompt" in argv
    assert claude_call.kwargs["cwd"] == str(repo)
    assert claude_call.kwargs["timeout"] == 60
    assert any("readme-maintainer" in a for a in argv)

    assert (repo / ".claude" / "skills" / "readme-maintainer" / "SKILL.md").exists()

    assert result.prompt_version == "harness-v1"
    assert result.tokens == 150
    assert result.exit_code == 0
    assert result.proposed_md_path == scratch / "proposed.md"
    assert ("no-op" in result.summary.lower()) or ("nothing" in result.summary.lower())


def test_claude_tokens_sum_with_cache_fields(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    json_stdout = json.dumps(
        {
            "role": "assistant",
            "result": "stopped",
            "usage": {
                "input_tokens": 10,
                "output_tokens": 20,
                "cache_creation_input_tokens": 100,
                "cache_read_input_tokens": 200,
            },
        }
    )

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=json_stdout, stderr=""
        )
        executor = ClaudeSkillExecutor()
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    assert result.tokens == 10 + 20 + 100 + 200


def test_claude_writes_summary_artifact(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    json_stdout = json.dumps(
        {
            "role": "assistant",
            "result": "added a section",
            "usage": {"input_tokens": 1, "output_tokens": 1},
        }
    )

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=json_stdout, stderr=""
        )
        executor = ClaudeSkillExecutor()
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    assert result.proposed_md_path == scratch / "proposed.md"
    assert "added a section" in (scratch / "proposed.md").read_text()


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
    assert result.proposed_md_path == scratch / "proposed.md"
