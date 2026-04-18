"""Deterministic repo inspection for `python -m harness.scope`.

No LLM, no network. Reads the working tree and `git log` only.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TypedDict


class RepoProfileError(Exception):
    """Raised when the target path can't be inspected."""


class RepoProfile(TypedDict):
    languages: dict[str, int]
    total_files: int
    total_bytes: int
    tests_present: bool
    ci_present: bool
    readme_present: bool
    deps_files: list[str]
    recent_commits_30d: int


_LANG_BY_EXT: dict[str, str] = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".java": "java",
    ".kt": "kotlin",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".swift": "swift",
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",
    ".sh": "shell",
}

_DEPS_FILES = [
    "pyproject.toml",
    "requirements.txt",
    "package.json",
    "go.mod",
    "Cargo.toml",
    "Gemfile",
    "pom.xml",
    "build.gradle",
]

_CI_PATHS = [
    ".github/workflows",
    ".circleci/config.yml",
    ".gitlab-ci.yml",
]

_TEST_HINT_DIRS = ["tests", "test", "__tests__"]
_TEST_HINT_PATTERNS = ("test_", "_test.", ".spec.", ".test.")


def _run_git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RepoProfileError(
            f"git {' '.join(args)} failed in {repo}: {proc.stderr.strip()}"
        )
    return proc.stdout


def inspect(repo_dir: Path) -> RepoProfile:
    repo_dir = Path(repo_dir)
    if not (repo_dir / ".git").exists():
        raise RepoProfileError(f"{repo_dir} is not a git repository")

    raw = _run_git(repo_dir, "ls-files", "-z")
    files = [f for f in raw.split("\0") if f]

    languages: dict[str, int] = {}
    total_bytes = 0
    for rel in files:
        ext = Path(rel).suffix.lower()
        lang = _LANG_BY_EXT.get(ext, "other")
        languages[lang] = languages.get(lang, 0) + 1
        try:
            total_bytes += (repo_dir / rel).stat().st_size
        except FileNotFoundError:
            pass

    tests_present = any((repo_dir / d).is_dir() for d in _TEST_HINT_DIRS) or any(
        any(pat in rel for pat in _TEST_HINT_PATTERNS) for rel in files
    )
    ci_present = any((repo_dir / p).exists() for p in _CI_PATHS)
    readme_present = any(
        (repo_dir / name).exists()
        for name in ("README.md", "README.rst", "README.txt", "README")
    )
    deps_files = [name for name in _DEPS_FILES if (repo_dir / name).exists()]

    try:
        _run_git(repo_dir, "rev-parse", "--verify", "HEAD")
        count_raw = _run_git(
            repo_dir, "rev-list", "--count", "--since=30 days ago", "HEAD"
        )
        recent = int(count_raw.strip() or "0")
    except RepoProfileError:
        recent = 0

    return RepoProfile(
        languages=languages,
        total_files=len(files),
        total_bytes=total_bytes,
        tests_present=tests_present,
        ci_present=ci_present,
        readme_present=readme_present,
        deps_files=deps_files,
        recent_commits_30d=recent,
    )
