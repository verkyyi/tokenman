"""Unit tests for harness.scope."""
from __future__ import annotations

from harness import scope


def test_parse_patterns_ignores_blank_lines_and_comments() -> None:
    parsed = scope.parse_patterns(
        """
        # comment
        ./docs/**

        README.md
        """
    )
    assert parsed == ["docs/**", "README.md"]


def test_matches_supports_recursive_globs() -> None:
    assert scope.matches("docs/payments/index.md", "docs/**")
    assert scope.matches("docs/payments/nested/page.md", "docs/payments/**")
    assert scope.matches("README.md", "README.md")


def test_outside_scope_returns_only_violations() -> None:
    paths = ["docs/index.md", "README.md", "src/main.py"]
    violations = scope.outside_scope(paths, ["docs/**", "README.md"])
    assert violations == ["src/main.py"]
