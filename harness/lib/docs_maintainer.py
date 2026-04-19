"""Docs-maintainer-specific helpers for post-Claude validation and routing."""
from __future__ import annotations

from pathlib import Path


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


def count_diff_lines(diff_text: str) -> int:
    """Count changed content lines, excluding unified-diff file headers."""
    count = 0
    for line in diff_text.splitlines():
        if line.startswith(("+++ ", "+++\t", "--- ", "---\t")):
            continue
        if line.startswith(("+", "-")):
            count += 1
    return count


def is_docs_path(path: str) -> bool:
    candidate = Path(path)
    if candidate.name in _DOC_FILENAMES:
        return True
    if candidate.suffix.lower() in _DOC_EXTENSIONS:
        return True
    return any(part in {"doc", "docs", "documentation"} for part in candidate.parts)


def _markdown_list(items: list[str], *, empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- `{item}`" for item in items)


def build_pr_body(
    *,
    summary: str,
    changed_paths: list[str],
    write_paths: list[str] | None,
    context_summary: str | None,
) -> str:
    lines = [
        "## Tokenman Run",
        "",
        "- Job: `docs-maintainer`",
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


def build_issue_body(
    *,
    reason: str,
    summary: str,
    changed_paths: list[str],
    write_paths: list[str] | None,
    context_summary: str | None,
) -> str:
    lines = [
        "## Tokenman could not open a PR",
        "",
        "- Job: `docs-maintainer`",
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
