"""Helpers for parsing and enforcing repo path scopes."""
from __future__ import annotations

import fnmatch


def parse_patterns(raw: str) -> list[str]:
    """Parse newline-delimited glob patterns from workflow inputs."""
    patterns: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        patterns.append(_normalize(stripped))
    return patterns


def _normalize(path_or_pattern: str) -> str:
    normalized = path_or_pattern.replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.lstrip("/")


def matches(path: str, pattern: str) -> bool:
    return fnmatch.fnmatchcase(_normalize(path), _normalize(pattern))


def filter_paths(paths: list[str], patterns: list[str]) -> list[str]:
    if not patterns:
        return list(paths)
    return [path for path in paths if any(matches(path, pattern) for pattern in patterns)]


def outside_scope(paths: list[str], patterns: list[str]) -> list[str]:
    if not patterns:
        return []
    return [path for path in paths if not any(matches(path, pattern) for pattern in patterns)]
