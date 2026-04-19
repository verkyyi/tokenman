"""Skill executor boundary for the harness runner.

Executors edit an isolated checkout in place. The runner is responsible
for diffing, committing, and opening the PR.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Optional, Protocol


_FRAMING_RESOURCE = files("harness.prompts") / "unattended_framing.v1.md"


def _load_framing() -> str:
    return _FRAMING_RESOURCE.read_text(encoding="utf-8")


@dataclass
class ExecutionResult:
    exit_code: int
    stdout: str
    stderr: str
    proposed_md_path: Optional[Path]
    summary: str
    prompt_version: str = "unknown"
    tokens: int = 0


class SkillExecutor(Protocol):
    """Invoke a skill against an isolated editable checkout."""

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult: ...


class StubSkillExecutor:
    """Runs `stub.sh` inside skill_dir as a subprocess.

    The stub edits the repo checkout passed as its second positional
    argument and may write proposed.md into the scratch directory passed
    as its first positional argument. stdout and stderr are captured in
    full. Not used outside of tests.
    """

    def __init__(
        self,
        extra_env: Optional[dict[str, str]] = None,
        timeout_s: int = 30,
    ) -> None:
        self._extra_env = dict(extra_env) if extra_env else {}
        self._timeout_s = timeout_s

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult:
        entrypoint = skill_dir / "stub.sh"
        env = {**os.environ, **self._extra_env}
        try:
            proc = subprocess.run(
                ["bash", str(entrypoint), str(scratch_dir), str(repo_dir)],
                cwd=str(repo_dir),
                env=env,
                capture_output=True,
                text=True,
                check=False,
                timeout=self._timeout_s,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout or ""
            stderr = (e.stderr or "") + (
                f"\n[executor] stub.sh timed out after {self._timeout_s}s\n"
            )
            exit_code = -1

        md = scratch_dir / "proposed.md"
        first_stdout_line = next(
            (ln for ln in stdout.splitlines() if ln.strip()),
            f"{skill_dir.name}: exit {exit_code}",
        )
        return ExecutionResult(
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            proposed_md_path=md if md.is_file() else None,
            summary=first_stdout_line,
            prompt_version="stub-v1",
            tokens=0,
        )


class ClaudeSkillExecutor:
    """Runs `claude -p` against an isolated editable checkout."""

    def __init__(
        self,
        claude_bin: str = "claude",
        timeout_s: int = 600,
        prompt_version: str = "harness-v1",
        extra_env: Optional[dict[str, str]] = None,
        framing_text: Optional[str] = None,
    ) -> None:
        self._claude_bin = claude_bin
        self._timeout_s = timeout_s
        self._prompt_version = prompt_version
        self._extra_env = dict(extra_env) if extra_env else {}
        self._framing = framing_text if framing_text is not None else _load_framing()

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult:
        skill_dst = repo_dir / ".claude" / "skills" / skill_dir.name
        skill_dst.parent.mkdir(parents=True, exist_ok=True)
        if skill_dst.resolve() != skill_dir.resolve():
            shutil.copytree(skill_dir, skill_dst, dirs_exist_ok=True)

        user_prompt = (
            f"Invoke the {skill_dir.name} skill. Edit files in place. "
            "When complete, stop."
        )
        argv = [
            self._claude_bin,
            "-p",
            "--permission-mode",
            "acceptEdits",
            "--output-format",
            "json",
            "--append-system-prompt",
            self._framing,
            user_prompt,
        ]
        env = {**os.environ, **self._extra_env}

        try:
            proc = subprocess.run(
                argv,
                cwd=str(repo_dir),
                env=env,
                capture_output=True,
                text=True,
                timeout=self._timeout_s,
                check=False,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout or ""
            stderr = (e.stderr or "") + (
                f"\n[executor] claude -p timed out after {self._timeout_s}s\n"
            )
            exit_code = -1

        summary, tokens = self._parse_json_output(stdout, exit_code)
        md_path = scratch_dir / "proposed.md"
        md_path.write_text(summary + "\n")

        return ExecutionResult(
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            proposed_md_path=md_path,
            summary=summary,
            prompt_version=self._prompt_version,
            tokens=tokens,
        )

    @staticmethod
    def _parse_json_output(stdout: str, exit_code: int) -> tuple[str, int]:
        """Return (summary, tokens) from claude JSON output."""
        try:
            doc = json.loads(stdout)
        except json.JSONDecodeError:
            first = next(
                (ln for ln in stdout.splitlines() if ln.strip()),
                f"claude: exit {exit_code}",
            )
            return first, 0

        summary = (
            doc.get("result")
            or doc.get("content")
            or doc.get("message")
            or f"claude: exit {exit_code}"
        )
        usage = doc.get("usage") or {}
        tokens = (
            int(usage.get("input_tokens", 0))
            + int(usage.get("output_tokens", 0))
            + int(usage.get("cache_creation_input_tokens", 0))
            + int(usage.get("cache_read_input_tokens", 0))
        )
        return summary, tokens
