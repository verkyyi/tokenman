"""Finalize a Tokenman run after Claude Code Action completes."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic
from typing import Optional

from harness.action.common import env_default, markdown_list, require
from harness.lib import git_ops, ledger, runner
from harness.lib.git_ops import GitIdentity
from harness.lib.issue_opener import GhIssueOpener, IssueOpenerError
from harness.lib.ledger import LedgerEntry
from harness.lib.path_rules import outside_scope
from harness.lib.pr_opener import GhPROpener, PROpenerError


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
            markdown_list(read_paths, empty="No read paths were provided."),
            "",
            "### Write Scope",
            markdown_list(write_paths, empty="No write paths were provided."),
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


def _iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_structured_output(raw: str | None) -> dict[str, str]:
    if not raw:
        return {}
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return doc if isinstance(doc, dict) else {}


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.action.finalize")
    parser.add_argument("--repo", default=env_default("GITHUB_WORKSPACE", "."))
    parser.add_argument("--github-token", default=env_default("INPUT_GITHUB_TOKEN"))
    parser.add_argument(
        "--on-high-confidence",
        default=env_default("INPUT_ON_HIGH_CONFIDENCE", "pull_request"),
    )
    parser.add_argument(
        "--on-low-confidence",
        default=env_default("INPUT_ON_LOW_CONFIDENCE", "issue"),
    )
    parser.add_argument("--state-path", default=env_default("TOKENMAN_STATE_PATH"))
    parser.add_argument("--claude-outcome", default=env_default("TOKENMAN_CLAUDE_OUTCOME", ""))
    parser.add_argument("--structured-output", default=env_default("TOKENMAN_STRUCTURED_OUTPUT", ""))
    parser.add_argument("--execution-file", default=env_default("TOKENMAN_EXECUTION_FILE", ""))
    args = parser.parse_args(argv)

    repo_dir = Path(args.repo).resolve()
    github_token = require("github_token", args.github_token)
    state_path = Path(require("state_path", args.state_path)).resolve()
    state = json.loads(state_path.read_text(encoding="utf-8"))
    artifact_dir = Path(state["artifact_dir"])
    artifact_dir.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("GH_TOKEN", github_token)
    os.environ.setdefault("GITHUB_TOKEN", github_token)

    if args.execution_file:
        execution_path = Path(args.execution_file)
        if execution_path.is_file():
            shutil.copyfile(execution_path, artifact_dir / "claude.execution.json")

    structured_output = _load_structured_output(args.structured_output)
    if args.structured_output:
        (artifact_dir / "structured_output.json").write_text(
            args.structured_output + "\n",
            encoding="utf-8",
        )

    git_identity = GitIdentity(
        "tokenman-bot",
        "tokenman-bot@users.noreply.github.com",
    )
    ledger_target: ledger.LedgerTarget = ledger.StateBranchLedgerStore(
        repo_dir=repo_dir,
        identity=git_identity,
    )
    pr_opener = GhPROpener(repo_dir=repo_dir, base_branch=state["base_branch"])
    issue_opener = GhIssueOpener(repo_dir=repo_dir)

    t_start = monotonic()
    status = "error"
    pr: Optional[int] = None
    issue: Optional[int] = None
    stderr = ""
    generator: dict[str, object] | None = None

    summary = structured_output.get("summary") or "Claude did not return a summary."
    confidence = structured_output.get("confidence") or "low"
    confidence_reason = structured_output.get("reason") or "No confidence rationale was returned."

    try:
        diff_text, changed_paths = git_ops.stage_and_capture_diff(checkout_dir=repo_dir)
        diff_lines = runner._count_diff_lines(diff_text)
        generator = {
            "prompt_version": "tokenman-mvp-v1",
            "output_summary": summary,
            "diff_lines": diff_lines,
            "tokens": 0,
        }

        if diff_text:
            (artifact_dir / "proposed.diff").write_text(diff_text, encoding="utf-8")

        low_confidence_reason: Optional[str] = None
        if args.claude_outcome not in {"success", ""}:
            low_confidence_reason = (
                f"Claude Code Action did not complete successfully: {args.claude_outcome}"
            )

        scope_violations = outside_scope(changed_paths, state["write_paths"])
        if scope_violations:
            low_confidence_reason = (
                "Generated changes outside the allowed write scope: "
                + ", ".join(scope_violations)
            )

        non_doc_paths = (
            [path for path in changed_paths if not runner._is_docs_path(path)]
            if state["job_type"] == "docs_maintainer"
            else []
        )
        if non_doc_paths:
            low_confidence_reason = (
                "Docs-only job proposed non-doc file changes: "
                + ", ".join(non_doc_paths)
            )

        if confidence != "high" and changed_paths:
            low_confidence_reason = confidence_reason

        if not diff_text:
            status = "no_change"
        elif low_confidence_reason is not None:
            if args.on_low_confidence == "issue":
                issue = issue_opener.open(
                    title="[tokenman] docs-maintainer: review needed",
                    body=runner._build_issue_body(
                        skill="docs-maintainer",
                        reason=low_confidence_reason,
                        summary=summary,
                        changed_paths=changed_paths,
                        write_paths=state["write_paths"],
                        context_summary=state["context_summary"],
                    ),
                )
                status = "issue_opened"
            else:
                status = "aborted_gate"
        elif args.on_high_confidence != "pull_request":
            status = "no_change"
        else:
            git_ops.commit_and_push(
                checkout_dir=repo_dir,
                message=f"[tokenman] docs-maintainer: {summary}",
                identity=git_identity,
            )
            pr = pr_opener.open(
                title=f"[tokenman] docs-maintainer: {summary}",
                body=runner._build_pr_body(
                    skill="docs-maintainer",
                    summary=summary,
                    changed_paths=changed_paths,
                    write_paths=state["write_paths"],
                    context_summary=state["context_summary"],
                ),
                branch=state["branch"],
            )
            status = "pr_opened"
    except (git_ops.GitOpsError, PROpenerError, IssueOpenerError) as exc:
        stderr = f"[tokenman] finalize failed: {exc}\n{traceback.format_exc()}"
        (artifact_dir / "tokenman.stderr").write_text(stderr, encoding="utf-8")
        status = "error"
    finally:
        git_ops.cleanup_branch_checkout(
            repo_dir=repo_dir,
            checkout_dir=repo_dir,
            branch=state["branch"],
            base=state["base_branch"],
            runtime_mode="actions",
        )

    entry: LedgerEntry = {
        "run_id": state["run_id"],
        "ts": _iso_utc(datetime.now(timezone.utc)),
        "skill": "docs-maintainer",
        "status": status,
        "pr": pr,
        "issue": issue,
        "generator": generator,
        "evaluator": None,
        "duration_s": int(monotonic() - t_start),
        "total_tokens": 0,
        "verdict": None,
        "verdict_note": None,
    }

    ledger.append(ledger_target, entry)
    (artifact_dir / "ledger.entry").write_text(
        json.dumps(entry, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    _append_step_summary(
        _step_summary(
            entry,
            read_paths=state["read_paths"],
            write_paths=state["write_paths"],
        )
    )
    _write_github_outputs(entry)
    print(json.dumps(entry, separators=(",", ":")))
    return 0 if status in {"pr_opened", "issue_opened", "no_change", "aborted_gate"} else 1


if __name__ == "__main__":
    sys.exit(main())
