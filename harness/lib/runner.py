"""Tokenman harness runner — orchestrates a single skill run."""
from __future__ import annotations

import json
import shutil
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic
from typing import Any, Callable, Optional

from harness.lib import git_ops, ledger
from harness.lib.git_ops import GitIdentity, GitOpsError, RuntimeMode
from harness.lib.issue_opener import IssueOpener, IssueOpenerError
from harness.lib.ledger import LedgerEntry
from harness.lib.path_rules import outside_scope
from harness.lib.pr_opener import PROpener, PROpenerError
from harness.lib.skill_executor import ExecutionResult, SkillExecutor

_DOC_EXTENSIONS = {
    ".adoc",
    ".asciidoc",
    ".gif",
    ".jpeg",
    ".jpg",
    ".md",
    ".mdx",
    ".png",
    ".rst",
    ".svg",
    ".txt",
    ".webp",
}
_DOC_FILENAMES = {
    "CHANGELOG",
    "CHANGELOG.md",
    "CONTRIBUTING",
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSE.md",
    "README",
    "README.md",
}


def _count_diff_lines(diff_text: str) -> int:
    """Count changed content lines, excluding file headers."""
    count = 0
    for line in diff_text.splitlines():
        if line.startswith(("+++ ", "+++\t", "--- ", "---\t")):
            continue
        if line.startswith(("+", "-")):
            count += 1
    return count


def _format_run_id(n: int) -> str:
    return f"r-{n:04d}"


def _iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_generator(result: ExecutionResult, diff_lines: int) -> dict[str, Any]:
    return {
        "prompt_version": result.prompt_version,
        "output_summary": result.summary,
        "diff_lines": diff_lines,
        "tokens": result.tokens,
    }


def _is_docs_path(path: str) -> bool:
    p = Path(path)
    if p.name in _DOC_FILENAMES:
        return True
    if p.suffix.lower() in _DOC_EXTENSIONS:
        return True
    return any(part in {"doc", "docs", "documentation"} for part in p.parts)


def _markdown_list(items: list[str], *, empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- `{item}`" for item in items)


def _build_pr_body(
    *,
    skill: str,
    summary: str,
    changed_paths: list[str],
    write_paths: Optional[list[str]],
    context_summary: Optional[str],
) -> str:
    lines = [
        "## Tokenman Run",
        "",
        f"- Job: `{skill}`",
        "- Outcome: `pull_request`",
        f"- Summary: {summary}",
        "",
        "## Proposed Changes",
        _markdown_list(changed_paths, empty="No file paths were captured."),
    ]
    if write_paths:
        lines.extend(
            [
                "",
                "## Allowed Write Scope",
                _markdown_list(write_paths, empty="No write scope configured."),
            ]
        )
    if context_summary:
        lines.extend(["", "## Context", context_summary])
    return "\n".join(lines)


def _build_issue_body(
    *,
    skill: str,
    reason: str,
    summary: str,
    changed_paths: list[str],
    write_paths: Optional[list[str]],
    context_summary: Optional[str],
) -> str:
    lines = [
        "## Tokenman could not open a PR",
        "",
        f"- Job: `{skill}`",
        "- Outcome: `issue`",
        f"- Reason: {reason}",
        f"- Claude summary: {summary}",
        "",
        "## Candidate Changed Files",
        _markdown_list(changed_paths, empty="No candidate file paths were captured."),
    ]
    if write_paths:
        lines.extend(
            [
                "",
                "## Allowed Write Scope",
                _markdown_list(write_paths, empty="No write scope configured."),
            ]
        )
    if context_summary:
        lines.extend(["", "## Context", context_summary])
    return "\n".join(lines)


def run_skill(
    *,
    skill_dir: Path,
    repo_dir: Path,
    ledger_path: Path,
    runs_dir: Path,
    executor: SkillExecutor,
    pr_opener: PROpener,
    issue_opener: Optional[IssueOpener] = None,
    skill_name: Optional[str] = None,
    now: Optional[Callable[[], datetime]] = None,
    base_branch: str = "main",
    git_identity: Optional[GitIdentity] = None,
    runtime_mode: RuntimeMode = "local_debug",
    read_paths: Optional[list[str]] = None,
    write_paths: Optional[list[str]] = None,
    on_high_confidence: str = "pull_request",
    on_low_confidence: str = "issue",
    context_summary: Optional[str] = None,
    job_type: str = "generic",
) -> LedgerEntry:
    """Run one skill against a repo. Returns the ledger entry appended."""
    now = now or (lambda: datetime.now(timezone.utc))
    skill = skill_name or skill_dir.name
    git_identity = git_identity or GitIdentity("tokenman-bot", "tokenman@local")

    prev_n = ledger.last_run_id(ledger_path)
    run_id = _format_run_id((prev_n or 0) + 1)
    branch = f"tokenman/{skill}/{run_id}"

    t_start = monotonic()
    artifact_dir = runs_dir / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    status = "error"
    generator: Optional[dict[str, Any]] = None
    pr: Optional[int] = None
    issue: Optional[int] = None
    stdout = ""
    stderr = ""

    with tempfile.TemporaryDirectory(prefix=f"tokenman-{run_id}-") as scratch_str:
        scratch = Path(scratch_str)

        try:
            checkout_dir = git_ops.prepare_branch_checkout(
                repo_dir=repo_dir,
                scratch_dir=scratch,
                branch=branch,
                base=base_branch,
                runtime_mode=runtime_mode,
            )
        except GitOpsError as exc:
            stderr = f"[runner] worktree setup failed: {exc}\n"
            (artifact_dir / "executor.stdout").write_text(stdout)
            (artifact_dir / "executor.stderr").write_text(stderr)
        else:
            try:
                result = executor.execute(skill_dir, checkout_dir, scratch)
            except Exception as exc:
                stderr = f"[runner] executor raised: {exc}\n{traceback.format_exc()}"
                (artifact_dir / "executor.stdout").write_text(stdout)
                (artifact_dir / "executor.stderr").write_text(stderr)
            else:
                stdout = result.stdout
                stderr = result.stderr
                (artifact_dir / "executor.stdout").write_text(stdout)
                (artifact_dir / "executor.stderr").write_text(stderr)
                if result.proposed_md_path is not None:
                    shutil.copyfile(result.proposed_md_path, artifact_dir / "proposed.md")

                try:
                    diff_text, changed_paths = git_ops.stage_and_capture_diff(
                        checkout_dir=checkout_dir
                    )
                except GitOpsError as exc:
                    generator = _build_generator(result, 0)
                    stderr = stderr + f"\n[runner] git diff failed: {exc}\n"
                    (artifact_dir / "executor.stderr").write_text(stderr)
                else:
                    diff_lines = _count_diff_lines(diff_text)
                    generator = _build_generator(result, diff_lines)

                    if diff_text:
                        (artifact_dir / "proposed.diff").write_text(diff_text)

                    if result.exit_code != 0:
                        status = "error"
                    elif not diff_text:
                        status = "no_change"
                    else:
                        scope_violations = outside_scope(changed_paths, write_paths or [])
                        non_doc_paths = (
                            [path for path in changed_paths if not _is_docs_path(path)]
                            if job_type == "docs_maintainer"
                            else []
                        )
                        low_confidence_reason: Optional[str] = None
                        if scope_violations:
                            low_confidence_reason = (
                                "Generated changes outside the allowed write scope: "
                                + ", ".join(scope_violations)
                            )
                        elif non_doc_paths:
                            low_confidence_reason = (
                                "Docs-only job proposed non-doc file changes: "
                                + ", ".join(non_doc_paths)
                            )

                        if low_confidence_reason is not None:
                            if issue_opener is not None and on_low_confidence == "issue":
                                try:
                                    issue = issue_opener.open(
                                        title=f"[tokenman] {skill}: review needed",
                                        body=_build_issue_body(
                                            skill=skill,
                                            reason=low_confidence_reason,
                                            summary=result.summary,
                                            changed_paths=changed_paths,
                                            write_paths=write_paths,
                                            context_summary=context_summary,
                                        ),
                                    )
                                    status = "issue_opened"
                                except IssueOpenerError as exc:
                                    status = "error"
                                    issue = None
                                    stderr = stderr + (
                                        f"\n[runner] issue_opener failed: {exc}\n"
                                        f"{traceback.format_exc()}"
                                    )
                                    (artifact_dir / "executor.stderr").write_text(stderr)
                            else:
                                status = "aborted_gate"
                        elif on_high_confidence != "pull_request":
                            status = "no_change"
                        else:
                            try:
                                git_ops.commit_and_push(
                                    checkout_dir=checkout_dir,
                                    message=f"[tokenman] {skill}: {result.summary}",
                                    identity=git_identity,
                                )
                                pr = pr_opener.open(
                                    title=f"[tokenman] {skill}: {result.summary}",
                                    body=_build_pr_body(
                                        skill=skill,
                                        summary=result.summary,
                                        changed_paths=changed_paths,
                                        write_paths=write_paths,
                                        context_summary=context_summary,
                                    ),
                                    branch=branch,
                                )
                                status = "pr_opened"
                            except (GitOpsError, PROpenerError) as exc:
                                status = "error"
                                pr = None
                                stderr = stderr + (
                                    f"\n[runner] git/pr_opener failed: {exc}\n"
                                    f"{traceback.format_exc()}"
                                )
                                (artifact_dir / "executor.stderr").write_text(stderr)
            finally:
                git_ops.cleanup_branch_checkout(
                    repo_dir=repo_dir,
                    checkout_dir=checkout_dir,
                    branch=branch,
                    base=base_branch,
                    runtime_mode=runtime_mode,
                )

    duration_s = int(monotonic() - t_start)

    entry: dict[str, Any] = {
        "run_id": run_id,
        "ts": _iso_utc(now()),
        "skill": skill,
        "status": status,
        "pr": pr,
        "issue": issue,
        "generator": generator,
        "evaluator": None,
        "duration_s": duration_s,
        "total_tokens": (generator["tokens"] if generator else 0),
        "verdict": None,
        "verdict_note": None,
    }

    ledger.append(ledger_path, entry)
    (artifact_dir / "ledger.entry").write_text(
        json.dumps(entry, separators=(",", ":")) + "\n"
    )
    return entry
