"""Prepare a Tokenman run before invoking Claude Code Action."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from harness import git, ledger, scope


def env_default(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in {None, ""} else default


def require(name: str, value: str | None) -> str:
    if value:
        return value
    raise SystemExit(f"missing required input: {name}")


def write_multiline_output(name: str, value: str) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    delimiter = f"TOKENMAN_{name.upper()}_EOF"
    with Path(output_path).open("a", encoding="utf-8") as handle:
        handle.write(f"{name}<<{delimiter}\n")
        handle.write(value)
        if not value.endswith("\n"):
            handle.write("\n")
        handle.write(f"{delimiter}\n")


def _git_lines(repo_dir: Path, *args: str) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def _markdown_list(items: list[str], *, empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- `{item}`" for item in items)


def _load_prompt_template() -> str:
    return Path(__file__).resolve().parents[1].joinpath("prompt.md").read_text(
        encoding="utf-8"
    )


def _recent_changed_files(repo_dir: Path) -> list[str]:
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    payload_path = os.environ.get("GITHUB_EVENT_PATH")
    payload: dict = {}
    if payload_path and Path(payload_path).is_file():
        try:
            payload = json.loads(Path(payload_path).read_text())
        except json.JSONDecodeError:
            payload = {}

    if event_name == "push":
        before = payload.get("before")
        after = payload.get("after") or os.environ.get("GITHUB_SHA")
        if before and after and set(before) != {"0"}:
            return _git_lines(repo_dir, "diff", "--name-only", f"{before}..{after}")

    if event_name in {"pull_request", "pull_request_target"}:
        pr = payload.get("pull_request") or {}
        base = (pr.get("base") or {}).get("sha")
        head = (pr.get("head") or {}).get("sha")
        if base and head:
            return _git_lines(repo_dir, "diff", "--name-only", f"{base}..{head}")

    changed = _git_lines(repo_dir, "diff", "--name-only", "HEAD~1..HEAD")
    if changed:
        return changed
    return _git_lines(repo_dir, "show", "--pretty=", "--name-only", "HEAD")


def _base_branch(repo_dir: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    env_branch = env_default("GITHUB_BASE_REF") or env_default("GITHUB_REF_NAME")
    if env_branch:
        return env_branch
    current = _git_lines(repo_dir, "branch", "--show-current")
    return current[0] if current else "main"


def _render_prompt(
    *,
    job_type: str,
    event_name: str,
    ref_name: str,
    read_paths: list[str],
    write_paths: list[str],
    recent_changes: list[str],
) -> str:
    rendered = _load_prompt_template()
    replacements = {
        "{{JOB_TYPE}}": job_type,
        "{{EVENT_NAME}}": event_name or "unknown",
        "{{REF_NAME}}": ref_name or "unknown",
        "{{READ_PATHS}}": _markdown_list(
            read_paths, empty="No read paths were provided."
        ),
        "{{WRITE_PATHS}}": _markdown_list(
            write_paths, empty="No write paths were provided."
        ),
        "{{RECENT_CHANGES}}": _markdown_list(
            recent_changes, empty="No recent code changes were detected."
        ),
    }
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def _context_summary(
    *,
    event_name: str,
    ref_name: str,
    read_paths: list[str],
    write_paths: list[str],
    recent_changes: list[str],
) -> str:
    lines = [
        f"- GitHub event: `{event_name or 'unknown'}`",
        f"- Base ref: `{ref_name or 'unknown'}`",
        "- Read scope:",
        _markdown_list(read_paths, empty="No read paths were provided."),
        "- Write scope:",
        _markdown_list(write_paths, empty="No write paths were provided."),
        "- Recent code changes in read scope:",
        _markdown_list(recent_changes, empty="No recent code changes were detected."),
    ]
    return "\n".join(lines)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.prepare")
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
    read_paths = scope.parse_patterns(require("read_paths", args.read_paths))
    write_paths = scope.parse_patterns(require("write_paths", args.write_paths))

    os.environ.setdefault("GH_TOKEN", github_token)
    os.environ.setdefault("GITHUB_TOKEN", github_token)

    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    base = _base_branch(repo_dir, args.base_branch)
    recent_changes = scope.filter_paths(_recent_changed_files(repo_dir), read_paths)
    prompt = _render_prompt(
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

    identity = git.GitIdentity(
        "tokenman-bot",
        "tokenman-bot@users.noreply.github.com",
    )
    ledger_target: ledger.LedgerTarget = ledger.StateBranchLedgerStore(
        repo_dir=repo_dir,
        identity=identity,
    )
    prev_n = ledger.last_run_id(ledger_target)
    run_id = f"r-{(prev_n or 0) + 1:04d}"
    branch = f"tokenman/docs-maintainer/{run_id}"

    scratch_root = repo_dir / ".tokenman" / "tmp" / run_id
    scratch_root.mkdir(parents=True, exist_ok=True)
    git.prepare_branch_checkout(
        repo_dir=repo_dir,
        scratch_dir=scratch_root,
        branch=branch,
        base=base,
        runtime_mode="actions",
    )

    artifact_dir = repo_dir / ".tokenman" / "runs" / run_id
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
        "context_summary": _context_summary(
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
    effective_args = '--json-schema ' + json.dumps(schema, separators=(",", ":")) + " --max-turns 8"
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
