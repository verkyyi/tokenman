"""Unit tests for harness.lib.path_rules."""
from __future__ import annotations

from harness.lib import path_rules


def test_parse_patterns_ignores_blank_lines_and_comments() -> None:
    parsed = path_rules.parse_patterns(
        """
        # comment
        ./docs/**

        README.md
        """
    )
    assert parsed == ["docs/**", "README.md"]


def test_matches_supports_recursive_globs() -> None:
    assert path_rules.matches("docs/payments/index.md", "docs/**")
    assert path_rules.matches("docs/payments/nested/page.md", "docs/payments/**")
    assert path_rules.matches("README.md", "README.md")


def test_outside_scope_returns_only_violations() -> None:
    paths = ["docs/index.md", "README.md", "src/main.py"]
    violations = path_rules.outside_scope(paths, ["docs/**", "README.md"])
    assert violations == ["src/main.py"]
