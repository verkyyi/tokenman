"""Skill executor boundary for the harness runner.

Phase 1.2a ships StubSkillExecutor for subprocess-driven tests.
Phase 1.2b-ii adds ClaudeSkillExecutor that invokes `claude -p`.
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
    proposed_diff_path: Optional[Path]
    proposed_md_path: Optional[Path]
    summary: str
    prompt_version: str = "unknown"
    tokens: int = 0


class SkillExecutor(Protocol):
    """Invoke a skill against a repo and produce an ExecutionResult."""

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult: ...


class StubSkillExecutor:
    """Runs `stub.sh` inside skill_dir as a subprocess.

    The stub writes proposed.diff / proposed.md (if any) into the
    scratch directory passed as its first positional argument. stdout
    and stderr are captured in full. Not used outside of tests.
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
                ["bash", str(entrypoint), str(scratch_dir)],
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
            stderr = (e.stderr or "") + f"\n[executor] stub.sh timed out after {self._timeout_s}s\n"
            exit_code = -1

        diff = scratch_dir / "proposed.diff"
        md = scratch_dir / "proposed.md"
        first_stdout_line = next(
            (ln for ln in stdout.splitlines() if ln.strip()),
            f"{skill_dir.name}: exit {exit_code}",
        )
        return ExecutionResult(
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            proposed_diff_path=diff if diff.is_file() else None,
            proposed_md_path=md if md.is_file() else None,
            summary=first_stdout_line,
            prompt_version="stub-v1",
            tokens=0,
        )


class ClaudeSkillExecutor:
    """Runs `claude -p` against a scratch copy of the repo and computes
    a proposed diff.

    Phase 1.2b-ii. Satisfies the SkillExecutor Protocol.
    """

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
        working = scratch_dir / "working"
        shutil.copytree(
            repo_dir,
            working,
            ignore=shutil.ignore_patterns(".git", ".tokenman"),
        )
        skill_dst = working / ".claude" / "skills" / skill_dir.name
        shutil.copytree(skill_dir, skill_dst, dirs_exist_ok=True)

        user_prompt = (
            f"Invoke the {skill_dir.name} skill. Edit files in place. "
            "When complete, stop."
        )
        argv = [
            self._claude_bin,
            "-p",
            "--output-format", "json",
            "--append-system-prompt", self._framing,
            user_prompt,
        ]
        env = {**os.environ, **self._extra_env}

        timed_out = False
        try:
            proc = subprocess.run(
                argv,
                cwd=str(working),
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
            stderr = (e.stderr or "") + f"\n[executor] claude -p timed out after {self._timeout_s}s\n"
            exit_code = -1
            timed_out = True

        summary, tokens = self._parse_json_output(stdout, exit_code)

        diff_path: Optional[Path] = None
        if not timed_out:
            diff_proc = subprocess.run(
                [
                    "diff", "-ruN",
                    "--exclude=.claude",
                    "--exclude=.git",
                    "--exclude=.tokenman",
                    str(repo_dir), str(working),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            # `diff` returns 1 if differences exist; 0 if identical; >=2 is an error.
            if diff_proc.returncode >= 2:
                stderr += f"\n[executor] diff failed: {diff_proc.stderr.strip()}"
            diff_output = diff_proc.stdout
            if diff_output.strip():
                diff_path = scratch_dir / "proposed.diff"
                diff_path.write_text(diff_output)

        md_path = scratch_dir / "proposed.md"
        md_path.write_text(summary + "\n")

        return ExecutionResult(
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            proposed_diff_path=diff_path,
            proposed_md_path=md_path,
            summary=summary,
            prompt_version=self._prompt_version,
            tokens=tokens,
        )

    @staticmethod
    def _parse_json_output(stdout: str, exit_code: int) -> tuple[str, int]:
        """Return (summary, tokens) from claude -p --output-format json.

        Defensive: falls back to the first non-empty stdout line for
        summary if JSON parsing fails.
        """
        try:
            doc = json.loads(stdout)
        except json.JSONDecodeError:
            first = next((ln for ln in stdout.splitlines() if ln.strip()),
                         f"claude: exit {exit_code}")
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
