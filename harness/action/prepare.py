"""Prepare a Tokenman run before invoking Claude Code Action."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

from harness.action.common import (
    base_branch,
    context_summary,
    env_default,
    recent_changed_files,
    render_prompt,
    require,
    write_multiline_output,
)
from harness.lib import ledger
from harness.lib.git_ops import GitIdentity, prepare_branch_checkout
from harness.lib.path_rules import filter_paths, parse_patterns


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.action.prepare")
    parser.add_argument("--repo", default=env_default("GITHUB_WORKSPACE", "."))
    parser.add_argument("--github-token", default=env_default("INPUT_GITHUB_TOKEN"))
    parser.add_argument("--read-paths", default=env_default("INPUT_READ_PATHS"))
    parser.add_argument("--write-paths", default=env_default("INPUT_WRITE_PATHS"))
    parser.add_argument("--job-type", default=env_default("INPUT_JOB_TYPE", "docs_maintainer"))
    parser.add_argument("--base-branch", default=env_default("INPUT_BASE_BRANCH"))
    parser.add_argument("--claude-args", default=env_default("INPUT_CLAUDE_ARGS", ""))
    args = parser.parse_args(argv)

    repo_dir = Path(args.repo).resolve()
    github_token = require("github_token", args.github_token)
    read_paths = parse_patterns(require("read_paths", args.read_paths))
    write_paths = parse_patterns(require("write_paths", args.write_paths))

    os.environ.setdefault("GH_TOKEN", github_token)
    os.environ.setdefault("GITHUB_TOKEN", github_token)

    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    base = base_branch(repo_dir, args.base_branch)
    recent_changes = filter_paths(recent_changed_files(repo_dir), read_paths)
    prompt = render_prompt(
        job_type=args.job_type,
        event_name=event_name,
        ref_name=base,
        read_paths=read_paths,
        write_paths=write_paths,
        recent_changes=recent_changes,
    )
    prompt += (
        "\n\n## Structured response\n\n"
        "Return structured output with these fields only:\n"
        "- `summary`: one sentence describing the doc state or edit\n"
        "- `confidence`: `high` or `low`\n"
        "- `reason`: short justification for the confidence level\n"
    )

    git_identity = GitIdentity(
        "tokenman-bot",
        "tokenman-bot@users.noreply.github.com",
    )
    ledger_target: ledger.LedgerTarget = ledger.StateBranchLedgerStore(
        repo_dir=repo_dir,
        identity=git_identity,
    )
    prev_n = ledger.last_run_id(ledger_target)
    run_id = f"r-{(prev_n or 0) + 1:04d}"
    branch = f"tokenman/docs-maintainer/{run_id}"

    scratch_root = repo_dir / ".tokenman" / "tmp" / run_id
    scratch_root.mkdir(parents=True, exist_ok=True)
    prepare_branch_checkout(
        repo_dir=repo_dir,
        scratch_dir=scratch_root,
        branch=branch,
        base=base,
        runtime_mode="actions",
    )

    runs_dir = repo_dir / ".tokenman" / "runs"
    artifact_dir = runs_dir / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "run_id": run_id,
        "branch": branch,
        "base_branch": base,
        "repo_dir": str(repo_dir),
        "artifact_dir": str(artifact_dir),
        "read_paths": read_paths,
        "write_paths": write_paths,
        "job_type": args.job_type,
        "context_summary": context_summary(
            event_name=event_name,
            ref_name=base,
            read_paths=read_paths,
            write_paths=write_paths,
            recent_changes=recent_changes,
        ),
        "claude_args": args.claude_args or "",
    }
    state_path = repo_dir / ".tokenman" / "current-run.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (artifact_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "confidence": {"type": "string", "enum": ["high", "low"]},
            "reason": {"type": "string"},
        },
        "required": ["summary", "confidence", "reason"],
        "additionalProperties": False,
    }
    base_args = (
        '--json-schema '
        + json.dumps(schema, separators=(",", ":"))
        + " --max-turns 8"
    )
    effective_args = base_args
    if args.claude_args:
        effective_args += f" {args.claude_args}"

    write_multiline_output("prompt", prompt)
    write_multiline_output("claude_args", effective_args)
    write_multiline_output("state_path", str(state_path))
    write_multiline_output("run_id", run_id)
    write_multiline_output("branch", branch)
    write_multiline_output("base_branch", base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
