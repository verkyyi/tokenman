"""Skill executor boundary for the harness runner.

Phase 1.2a ships StubSkillExecutor for subprocess-driven tests.
Phase 3+ adds ClaudeSkillExecutor that invokes `claude -p`.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Protocol


@dataclass
class ExecutionResult:
    exit_code: int
    stdout: str
    stderr: str
    proposed_diff_path: Optional[Path]
    proposed_md_path: Optional[Path]
    summary: str


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

    def __init__(self, extra_env: Optional[dict[str, str]] = None) -> None:
        self._extra_env = dict(extra_env) if extra_env else {}

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult:
        entrypoint = skill_dir / "stub.sh"
        env = {**os.environ, **self._extra_env}
        proc = subprocess.run(
            ["bash", str(entrypoint), str(scratch_dir)],
            cwd=str(repo_dir),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        diff = scratch_dir / "proposed.diff"
        md = scratch_dir / "proposed.md"
        first_stdout_line = next(
            (ln for ln in proc.stdout.splitlines() if ln.strip()),
            f"{skill_dir.name}: exit {proc.returncode}",
        )
        return ExecutionResult(
            exit_code=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            proposed_diff_path=diff if diff.is_file() else None,
            proposed_md_path=md if md.is_file() else None,
            summary=first_stdout_line,
        )
