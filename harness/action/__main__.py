"""Run the Tokenman GitHub Action contract from a checked-out repo."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from harness.lib import ledger, runner
from harness.lib.git_ops import GitIdentity
from harness.lib.issue_opener import GhIssueOpener
from harness.lib.path_rules import filter_paths, parse_patterns
from harness.lib.pr_opener import GhPROpener
from harness.lib.skill_executor import ClaudeSkillExecutor


def _env_default(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in {None, ""} else default


def _tokenman_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_prompt_template() -> str:
    return (_tokenman_root() / "prompt.md").read_text(encoding="utf-8")


def _git(
    repo_dir: Path,
    *args: str,
) -> list[str]:
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
            return _git(repo_dir, "diff", "--name-only", f"{before}..{after}")

    if event_name in {"pull_request", "pull_request_target"}:
        pr = payload.get("pull_request") or {}
        base = ((pr.get("base") or {}).get("sha"))
        head = ((pr.get("head") or {}).get("sha"))
        if base and head:
            return _git(repo_dir, "diff", "--name-only", f"{base}..{head}")

    changed = _git(repo_dir, "diff", "--name-only", "HEAD~1..HEAD")
    if changed:
        return changed
    return _git(repo_dir, "show", "--pretty=", "--name-only", "HEAD")


def _markdown_list(items: list[str], *, empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- `{item}`" for item in items)


def _render_prompt(
    *,
    job_type: str,
    event_name: str,
    ref_name: str,
    read_paths: list[str],
    write_paths: list[str],
    recent_changes: list[str],
) -> str:
    template = _load_prompt_template()
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
    rendered = template
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


def _step_summary(entry: dict, *, read_paths: list[str], write_paths: list[str]) -> str:
    status = entry["status"]
    if status == "pr_opened":
        outcome = "pull_request"
    elif status == "issue_opened":
        outcome = "issue"
    elif status in {"no_change", "aborted_gate"}:
        outcome = "no_op"
    else:
        outcome = "error"

    generator = entry.get("generator") or {}
    lines = [
        "## Tokenman",
        "",
        f"- Outcome: `{outcome}`",
        f"- Status: `{status}`",
        f"- Run ID: `{entry['run_id']}`",
    ]
    if entry.get("pr") is not None:
        lines.append(f"- PR: `#{entry['pr']}`")
    if entry.get("issue") is not None:
        lines.append(f"- Issue: `#{entry['issue']}`")
    if generator.get("output_summary"):
        lines.append(f"- Summary: {generator['output_summary']}")
    lines.extend(
        [
            "",
            "### Read Scope",
            _markdown_list(read_paths, empty="No read paths were provided."),
            "",
            "### Write Scope",
            _markdown_list(write_paths, empty="No write paths were provided."),
        ]
    )
    return "\n".join(lines) + "\n"


def _write_github_outputs(entry: dict) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    status = entry["status"]
    if status == "pr_opened":
        outcome = "pull_request"
    elif status == "issue_opened":
        outcome = "issue"
    elif status in {"no_change", "aborted_gate"}:
        outcome = "no_op"
    else:
        outcome = "error"
    with Path(output_path).open("a", encoding="utf-8") as handle:
        handle.write(f"outcome={outcome}\n")
        handle.write(f"run_id={entry['run_id']}\n")
        handle.write(f"status={status}\n")
        handle.write(f"pr_number={entry.get('pr') or ''}\n")
        handle.write(f"issue_number={entry.get('issue') or ''}\n")


def _append_step_summary(text: str) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with Path(summary_path).open("a", encoding="utf-8") as handle:
        handle.write(text)


def _base_branch(repo_dir: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    env_branch = _env_default("GITHUB_BASE_REF") or _env_default("GITHUB_REF_NAME")
    if env_branch:
        return env_branch
    current = _git(repo_dir, "branch", "--show-current")
    return current[0] if current else "main"


def _require(name: str, value: str | None) -> str:
    if value:
        return value
    raise SystemExit(f"missing required input: {name}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.action")
    parser.add_argument("--repo", default=_env_default("GITHUB_WORKSPACE", "."))
    parser.add_argument("--github-token", default=_env_default("INPUT_GITHUB_TOKEN"))
    parser.add_argument("--read-paths", default=_env_default("INPUT_READ_PATHS"))
    parser.add_argument("--write-paths", default=_env_default("INPUT_WRITE_PATHS"))
    parser.add_argument("--job-type", default=_env_default("INPUT_JOB_TYPE", "docs_maintainer"))
    parser.add_argument(
        "--on-high-confidence",
        default=_env_default("INPUT_ON_HIGH_CONFIDENCE", "pull_request"),
    )
    parser.add_argument(
        "--on-low-confidence",
        default=_env_default("INPUT_ON_LOW_CONFIDENCE", "issue"),
    )
    parser.add_argument("--base-branch", default=_env_default("INPUT_BASE_BRANCH"))
    parser.add_argument("--claude-bin", default=_env_default("INPUT_CLAUDE_BIN", "claude"))
    args = parser.parse_args(argv)

    repo_dir = Path(args.repo).resolve()
    github_token = _require("github_token", args.github_token)
    read_paths = parse_patterns(_require("read_paths", args.read_paths))
    write_paths = parse_patterns(_require("write_paths", args.write_paths))

    os.environ.setdefault("GH_TOKEN", github_token)
    os.environ.setdefault("GITHUB_TOKEN", github_token)

    recent_changes = filter_paths(_recent_changed_files(repo_dir), read_paths)
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    ref_name = _base_branch(repo_dir, args.base_branch)
    context_summary = _context_summary(
        event_name=event_name,
        ref_name=ref_name,
        read_paths=read_paths,
        write_paths=write_paths,
        recent_changes=recent_changes,
    )
    prompt = _render_prompt(
        job_type=args.job_type,
        event_name=event_name,
        ref_name=ref_name,
        read_paths=read_paths,
        write_paths=write_paths,
        recent_changes=recent_changes,
    )

    git_identity = GitIdentity(
        "tokenman-bot",
        "tokenman-bot@users.noreply.github.com",
    )
    ledger_target: ledger.LedgerTarget = ledger.StateBranchLedgerStore(
        repo_dir=repo_dir,
        identity=git_identity,
    )
    runs_dir = repo_dir / ".tokenman" / "runs"

    with tempfile.TemporaryDirectory(prefix="tokenman-job-") as tmp:
        skill_dir = Path(tmp) / "docs-maintainer"
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(prompt, encoding="utf-8")

        entry = runner.run_skill(
            skill_dir=skill_dir,
            repo_dir=repo_dir,
            ledger_path=ledger_target,
            runs_dir=runs_dir,
            executor=ClaudeSkillExecutor(claude_bin=args.claude_bin),
            pr_opener=GhPROpener(repo_dir=repo_dir, base_branch=ref_name),
            issue_opener=GhIssueOpener(repo_dir=repo_dir),
            skill_name="docs-maintainer",
            base_branch=ref_name,
            git_identity=git_identity,
            runtime_mode="actions",
            read_paths=read_paths,
            write_paths=write_paths,
            on_high_confidence=args.on_high_confidence,
            on_low_confidence=args.on_low_confidence,
            context_summary=context_summary,
            job_type=args.job_type,
        )

    _append_step_summary(_step_summary(entry, read_paths=read_paths, write_paths=write_paths))
    _write_github_outputs(entry)
    print(json.dumps(entry, separators=(",", ":")))
    return 0 if entry["status"] in {"pr_opened", "issue_opened", "no_change", "aborted_gate"} else 1


if __name__ == "__main__":
    sys.exit(main())
