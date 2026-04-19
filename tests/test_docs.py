"""Tests for docs-maintainer-specific helper functions."""
from __future__ import annotations

from harness import docs


def test_count_diff_lines_ignores_file_headers() -> None:
    diff = (
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1,2 +1,3 @@\n"
        " # Title\n"
        "+\n"
        "+new line\n"
        "-old line\n"
    )
    assert docs.count_diff_lines(diff) == 3


def test_count_diff_lines_empty() -> None:
    assert docs.count_diff_lines("") == 0


def test_count_diff_lines_no_changes() -> None:
    diff = "--- a/x\n+++ b/x\n@@ -1,1 +1,1 @@\n only context\n"
    assert docs.count_diff_lines(diff) == 0


def test_is_docs_path_accepts_doc_conventions() -> None:
    assert docs.is_docs_path("README.md") is True
    assert docs.is_docs_path("docs/payments/guide.md") is True
    assert docs.is_docs_path("documentation/api/schema.json") is True


def test_is_docs_path_rejects_source_files() -> None:
    assert docs.is_docs_path("services/payments/handler.py") is False


def test_build_pr_body_includes_scope_and_context() -> None:
    body = docs.build_pr_body(
        summary="Updated payments docs for recent API changes.",
        changed_paths=["docs/payments/guide.md"],
        write_paths=["docs/payments/**"],
        context_summary="- GitHub event: `push`",
    )

    assert "- Job: `docs-maintainer`" in body
    assert "- Outcome: `pull_request`" in body
    assert "- `docs/payments/guide.md`" in body
    assert "- `docs/payments/**`" in body
    assert "## Context" in body


def test_build_issue_body_includes_reason() -> None:
    body = docs.build_issue_body(
        reason="Generated changes outside the allowed write scope: README.md",
        summary="Claude proposed a broad docs rewrite.",
        changed_paths=["README.md"],
        write_paths=["docs/payments/**"],
        context_summary=None,
    )

    assert "- Outcome: `issue`" in body
    assert "outside the allowed write scope" in body
    assert "- `README.md`" in body
