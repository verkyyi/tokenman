# Phase 1.3 — Scoping flow implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `python -m harness.scope` — a CLI that inspects a consumer repo, queries Claude-Code plugin marketplaces, asks the user a handful of questions, calls `claude -p` once, and writes `.tokenman/initial-scope.md`.

**Architecture:** Deterministic Python for facts (repo profile + marketplace manifest parsing) plus one LLM call for drafting the scope markdown. Allowlist backstop keeps the §5.1 catalog guarantee. Interactive flow with `--non-interactive` and `--dry-run` escape hatches for tests.

**Tech Stack:** Python 3.10+, `subprocess`, `pyyaml`, `pytest`. Follows the patterns established in `harness/lib/skill_executor.py` and `harness/run/__main__.py` from Phase 1.2b.

**Spec:** `docs/superpowers/specs/2026-04-18-phase-1-3-scoping-flow-design.md`

**Branch:** `phase-1-3` off `main`.

---

## File inventory (from spec §11)

New:
- `harness/scope/__init__.py`
- `harness/scope/__main__.py`
- `harness/lib/repo_profile.py`
- `harness/lib/marketplace.py`
- `harness/lib/scope_drafter.py`
- `harness/prompts/scoping.v1.md`
- `tests/test_repo_profile.py`
- `tests/test_marketplace.py`
- `tests/test_scope_drafter.py`
- `tests/test_scope_cli.py`
- `tests/test_scope_live.py`
- `tests/fixtures/fake-marketplaces/one/.claude-plugin/marketplace.json`
- `tests/fixtures/fake-marketplaces/two/.claude-plugin/marketplace.json`
- `tests/fixtures/scope-captures/minimal.json`

Reused as-is:
- `tests/fixtures/tiny-python-repo/`

Touched:
- `README.md` — one-line usage mention.

---

## Task 1: Worktree + module skeleton

**Goal:** create the `phase-1-3` worktree, stub out the module tree so later tasks can `pytest --collect-only` without ImportError, and commit an empty-but-valid skeleton.

**Files:**
- Create: `harness/scope/__init__.py`
- Create: `harness/scope/__main__.py`
- Create: `harness/lib/repo_profile.py`
- Create: `harness/lib/marketplace.py`
- Create: `harness/lib/scope_drafter.py`
- Create: `harness/prompts/scoping.v1.md`

- [ ] **Step 1: Create worktree and branch**

```bash
git -C /home/dev/projects/tokenman worktree add -b phase-1-3 /home/dev/projects/tokenman-phase-1-3 main
cd /home/dev/projects/tokenman-phase-1-3
```

- [ ] **Step 2: Create `harness/scope/__init__.py`**

```python
"""Discovery + scope-proposal flow — spec §6.3. Phase 1.3."""
```

- [ ] **Step 3: Create `harness/scope/__main__.py`** (stub — full CLI lands in Task 8)

```python
"""`python -m harness.scope` — writes .tokenman/initial-scope.md.

See docs/superpowers/specs/2026-04-18-phase-1-3-scoping-flow-design.md.
"""
from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    raise SystemExit("harness.scope CLI is not yet implemented (Phase 1.3)")


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Create `harness/lib/repo_profile.py`** (stub)

```python
"""Deterministic repo inspection for `python -m harness.scope`."""
from __future__ import annotations
```

- [ ] **Step 5: Create `harness/lib/marketplace.py`** (stub)

```python
"""Read Claude-Code plugin marketplace manifests."""
from __future__ import annotations
```

- [ ] **Step 6: Create `harness/lib/scope_drafter.py`** (stub)

```python
"""Orchestrate the single `claude -p` call that drafts initial-scope.md."""
from __future__ import annotations
```

- [ ] **Step 7: Create `harness/prompts/scoping.v1.md`** (placeholder — real content in Task 5)

```markdown
# Scoping framing — v1 (placeholder)

Replaced in Phase 1.3 Task 5.
```

- [ ] **Step 8: Confirm the skeleton imports cleanly**

Run: `python -c 'import harness.scope, harness.lib.repo_profile, harness.lib.marketplace, harness.lib.scope_drafter'`
Expected: exit 0, no output.

- [ ] **Step 9: Commit**

```bash
git add harness/scope harness/lib/repo_profile.py harness/lib/marketplace.py harness/lib/scope_drafter.py harness/prompts/scoping.v1.md
git commit -m "feat(scoping): scaffold harness/scope module skeleton

Empty stubs for the four new modules and the prompt file. Concrete
implementation lands in subsequent commits (Phase 1.3)."
```

---

## Task 2: `repo_profile.py` (TDD)

**Goal:** deterministic repo inspection returning a `RepoProfile` TypedDict.

**Files:**
- Test: `tests/test_repo_profile.py`
- Modify: `harness/lib/repo_profile.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_repo_profile.py`:

```python
"""Unit tests for harness.lib.repo_profile."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from harness.lib import repo_profile

REPO_ROOT = Path(__file__).resolve().parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def _git_init(repo_dir: Path) -> None:
    subprocess.run(["git", "-C", str(repo_dir), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.name", "seed"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo_dir), "commit", "-m", "seed"],
        check=True, capture_output=True,
    )


def _copy_fixture(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    _git_init(repo)
    return repo


def test_inspect_tiny_python_repo(tmp_path: Path) -> None:
    repo = _copy_fixture(tmp_path)
    profile = repo_profile.inspect(repo)
    assert profile["readme_present"] is True
    assert profile["tests_present"] is True
    assert "pyproject.toml" in profile["deps_files"]
    assert profile["languages"].get("python", 0) >= 1
    assert profile["total_files"] > 0
    assert profile["total_bytes"] > 0
    assert profile["recent_commits_30d"] >= 1


def test_inspect_rejects_non_git_dir(tmp_path: Path) -> None:
    with pytest.raises(repo_profile.RepoProfileError):
        repo_profile.inspect(tmp_path)


def test_inspect_empty_repo(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    profile = repo_profile.inspect(repo)
    assert profile["total_files"] == 0
    assert profile["recent_commits_30d"] == 0
    assert profile["readme_present"] is False
    assert profile["tests_present"] is False


def test_inspect_detects_ci(tmp_path: Path) -> None:
    repo = _copy_fixture(tmp_path)
    (repo / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (repo / ".github" / "workflows" / "test.yml").write_text("name: x\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "add-ci"],
        check=True, capture_output=True,
    )
    profile = repo_profile.inspect(repo)
    assert profile["ci_present"] is True
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_repo_profile.py -v`
Expected: all four fail with `AttributeError: module 'harness.lib.repo_profile' has no attribute 'inspect'` or similar.

- [ ] **Step 3: Implement `harness/lib/repo_profile.py`**

```python
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


# Extension → canonical language. Unknown extensions bucket into "other".
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

    # File enumeration via git ls-files (empty repos return empty string).
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
            # Tracked but removed in working tree — skip.
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

    # Empty repo → no HEAD → rev-list fails. Handle by checking HEAD exists.
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/test_repo_profile.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add harness/lib/repo_profile.py tests/test_repo_profile.py
git commit -m "feat(scoping): add repo_profile.inspect for deterministic repo facts"
```

---

## Task 3: `marketplace.py` (TDD)

**Goal:** enumerate plugins across configured Claude-Code marketplaces; tolerate missing/malformed manifests.

**Files:**
- Create: `tests/fixtures/fake-marketplaces/one/.claude-plugin/marketplace.json`
- Create: `tests/fixtures/fake-marketplaces/two/.claude-plugin/marketplace.json`
- Create: `tests/test_marketplace.py`
- Modify: `harness/lib/marketplace.py`

- [ ] **Step 1: Create fake marketplace fixtures**

Create `tests/fixtures/fake-marketplaces/one/.claude-plugin/marketplace.json`:

```json
{
  "name": "one",
  "plugins": [
    {
      "name": "readme-sync",
      "description": "Keep README in sync with code",
      "category": "docs",
      "homepage": "https://example.com/readme-sync"
    },
    {
      "name": "dep-bumper",
      "description": "Bump deps safely",
      "category": "maintenance"
    }
  ]
}
```

Create `tests/fixtures/fake-marketplaces/two/.claude-plugin/marketplace.json` (malformed on purpose):

```json
{ not valid json
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_marketplace.py`:

```python
"""Unit tests for harness.lib.marketplace."""
from __future__ import annotations

from pathlib import Path

from harness.lib import marketplace

REPO_ROOT = Path(__file__).resolve().parent.parent
FAKE_ROOT = REPO_ROOT / "tests" / "fixtures" / "fake-marketplaces"


def test_list_plugins_reads_wellformed_manifest() -> None:
    plugins = marketplace.list_plugins(root=FAKE_ROOT)
    names = [p["name"] for p in plugins]
    assert "readme-sync" in names
    assert "dep-bumper" in names
    readme = next(p for p in plugins if p["name"] == "readme-sync")
    assert readme["marketplace"] == "one"
    assert readme["description"] == "Keep README in sync with code"


def test_list_plugins_skips_malformed_manifest(capsys) -> None:
    plugins = marketplace.list_plugins(root=FAKE_ROOT)
    # two/marketplace.json is malformed; its plugins are absent but the
    # wellformed manifest still returned entries.
    assert any(p["marketplace"] == "one" for p in plugins)
    assert not any(p["marketplace"] == "two" for p in plugins)
    captured = capsys.readouterr()
    assert "two" in captured.err or "malformed" in captured.err.lower()


def test_list_plugins_missing_root_returns_empty(tmp_path: Path) -> None:
    plugins = marketplace.list_plugins(root=tmp_path / "does-not-exist")
    assert plugins == []
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `pytest tests/test_marketplace.py -v`
Expected: 3 fail with `AttributeError` on `list_plugins`.

- [ ] **Step 4: Implement `harness/lib/marketplace.py`**

```python
"""Read Claude-Code plugin marketplace manifests.

Reads local caches at ~/.claude/plugins/marketplaces/<name>/.claude-plugin/
marketplace.json. Malformed manifests are skipped with a warning; missing
cache root returns an empty list.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, TypedDict


class Plugin(TypedDict):
    name: str
    description: str
    category: Optional[str]
    homepage: Optional[str]
    marketplace: str


def marketplace_root() -> Path:
    return Path.home() / ".claude" / "plugins" / "marketplaces"


def list_plugins(*, root: Optional[Path] = None, refresh: bool = False) -> list[Plugin]:
    if refresh:
        subprocess.run(
            ["claude", "plugins", "marketplace", "update"],
            capture_output=True,
            text=True,
        )  # best-effort; ignore exit code

    base = root if root is not None else marketplace_root()
    if not base.exists():
        return []

    plugins: list[Plugin] = []
    for manifest_path in sorted(base.glob("*/.claude-plugin/marketplace.json")):
        marketplace_name = manifest_path.parent.parent.name
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(
                f"warning: skipping malformed marketplace {marketplace_name!r}: {exc}",
                file=sys.stderr,
            )
            continue

        for entry in data.get("plugins", []):
            if not isinstance(entry, dict) or "name" not in entry:
                continue
            plugins.append(Plugin(
                name=str(entry["name"]),
                description=str(entry.get("description", "")),
                category=entry.get("category"),
                homepage=entry.get("homepage"),
                marketplace=marketplace_name,
            ))
    return plugins
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `pytest tests/test_marketplace.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add tests/fixtures/fake-marketplaces harness/lib/marketplace.py tests/test_marketplace.py
git commit -m "feat(scoping): add marketplace.list_plugins for registry discovery"
```

---

## Task 4: `scope_drafter.py` — types, Stub executor, draft(), allowlist, retry (TDD)

**Goal:** define the LLM-facing contract (`ScopeDraft` types, `ScopeExecutor` protocol), implement `StubScopeExecutor`, implement `draft()` with allowlist enforcement and one-retry JSON handling.

**Files:**
- Create: `tests/fixtures/scope-captures/minimal.json`
- Create: `tests/test_scope_drafter.py`
- Modify: `harness/lib/scope_drafter.py`

- [ ] **Step 1: Create canned LLM response fixture**

Create `tests/fixtures/scope-captures/minimal.json`:

```json
{
  "profile_prose": "A small Python project with tests and a README.",
  "recommended_skills": [
    {
      "name": "readme-maintainer",
      "reasoning": "The repo has a README and source files; keeping them aligned is a good starter.",
      "default_cadence": "on-change"
    }
  ],
  "skipped_skills": [],
  "candidate_uncurated_plugins": [
    {
      "plugin": "dep-bumper",
      "marketplace": "one",
      "reasoning": "Possibly useful once the catalog adds a dep-bump skill."
    }
  ],
  "suggested_boundaries": {
    "allowed": ["README.md"],
    "forbidden": [".tokenman/**", "harness/**"]
  }
}
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_scope_drafter.py`:

```python
"""Unit tests for harness.lib.scope_drafter."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness.lib import scope_drafter

REPO_ROOT = Path(__file__).resolve().parent.parent
CANNED = REPO_ROOT / "tests" / "fixtures" / "scope-captures" / "minimal.json"


def _profile() -> scope_drafter.RepoProfile:  # type: ignore[name-defined]
    from harness.lib.repo_profile import RepoProfile
    return RepoProfile(
        languages={"python": 3}, total_files=4, total_bytes=500,
        tests_present=True, ci_present=False, readme_present=True,
        deps_files=["pyproject.toml"], recent_commits_30d=2,
    )


def _catalog() -> dict[str, dict]:
    return {
        "readme-maintainer": {
            "source": "./skills/readme-maintainer",
            "version": "0.1.0",
            "tier": "starter",
        }
    }


def _plugins() -> list[dict]:
    return [
        {"name": "readme-sync", "description": "x", "category": None,
         "homepage": None, "marketplace": "one"},
    ]


def _answers() -> dict[str, str]:
    return {"purpose": "cli tool", "concern": "a", "off_limits": "",
            "other": ""}


def test_draft_happy_path() -> None:
    executor = scope_drafter.StubScopeExecutor(canned_result=CANNED.read_text())
    draft = scope_drafter.draft(
        profile=_profile(),
        plugins=_plugins(),
        user_answers=_answers(),
        catalog=_catalog(),
        executor=executor,
    )
    assert draft["recommended_skills"][0]["name"] == "readme-maintainer"
    assert draft["suggested_boundaries"]["allowed"] == ["README.md"]


def test_draft_demotes_non_catalog_skill() -> None:
    # LLM hallucinates a skill not in the catalog — it must be demoted.
    rogue = json.loads(CANNED.read_text())
    rogue["recommended_skills"].append({
        "name": "not-in-catalog",
        "reasoning": "invented",
        "default_cadence": "weekly",
    })
    executor = scope_drafter.StubScopeExecutor(canned_result=json.dumps(rogue))
    draft = scope_drafter.draft(
        profile=_profile(),
        plugins=_plugins(),
        user_answers=_answers(),
        catalog=_catalog(),
        executor=executor,
    )
    names = [s["name"] for s in draft["recommended_skills"]]
    assert "not-in-catalog" not in names
    demoted = [p["plugin"] for p in draft["candidate_uncurated_plugins"]]
    assert "not-in-catalog" in demoted


def test_draft_retries_once_on_invalid_json() -> None:
    executor = scope_drafter.StubScopeExecutor(
        canned_sequence=["not json", CANNED.read_text()]
    )
    draft = scope_drafter.draft(
        profile=_profile(),
        plugins=_plugins(),
        user_answers=_answers(),
        catalog=_catalog(),
        executor=executor,
    )
    assert draft["recommended_skills"][0]["name"] == "readme-maintainer"
    assert executor.call_count == 2


def test_draft_raises_after_retry_exhaustion() -> None:
    executor = scope_drafter.StubScopeExecutor(
        canned_sequence=["not json", "still not json"]
    )
    with pytest.raises(scope_drafter.ScopeDrafterError):
        scope_drafter.draft(
            profile=_profile(),
            plugins=_plugins(),
            user_answers=_answers(),
            catalog=_catalog(),
            executor=executor,
        )


def test_draft_includes_skill_md_in_payload_for_local_catalog_entries(tmp_path: Path) -> None:
    """Local './skills/<name>' entries should have SKILL.md text supplied to the executor."""
    skills_root = tmp_path / "skills" / "readme-maintainer"
    skills_root.mkdir(parents=True)
    (skills_root / "SKILL.md").write_text("SCOPE: README.md only.\n")
    catalog = {
        "readme-maintainer": {
            "source": "./skills/readme-maintainer",
            "version": "0.1.0",
        }
    }

    captured: dict[str, str] = {}

    class CapturingExecutor:
        call_count = 0
        def run(self, *, system_prompt: str, user_payload: str) -> str:
            self.call_count += 1
            captured["payload"] = user_payload
            return CANNED.read_text()

    scope_drafter.draft(
        profile=_profile(),
        plugins=_plugins(),
        user_answers=_answers(),
        catalog=catalog,
        executor=CapturingExecutor(),
        catalog_root=tmp_path,
    )
    assert "SCOPE: README.md only." in captured["payload"]
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `pytest tests/test_scope_drafter.py -v`
Expected: all fail — missing symbols in `scope_drafter`.

- [ ] **Step 4: Implement `harness/lib/scope_drafter.py`**

```python
"""Orchestrate the single `claude -p` call that drafts initial-scope.md.

Responsibilities:
  1. Build the system prompt (from harness/prompts/scoping.v1.md) and
     user payload (JSON blob: repo profile + marketplace plugins +
     catalog + SKILL.md texts + user answers).
  2. Invoke the executor (Claude or Stub); parse its JSON response.
  3. Enforce the catalog allowlist by demoting non-catalog
     `recommended_skills` entries into `candidate_uncurated_plugins`.
  4. Retry once on invalid JSON; raise `ScopeDrafterError` otherwise.
"""
from __future__ import annotations

import json
import subprocess
from importlib.resources import files
from pathlib import Path
from typing import Optional, Protocol, TypedDict

from harness.lib.repo_profile import RepoProfile

_FRAMING_RESOURCE = files("harness.prompts") / "scoping.v1.md"


class ScopeDrafterError(Exception):
    """Raised when the LLM fails to produce a valid ScopeDraft."""


class ScopeExecutorError(Exception):
    """Raised by executors on transport failure."""


class RecommendedSkill(TypedDict):
    name: str
    reasoning: str
    default_cadence: str


class SkippedSkill(TypedDict):
    name: str
    reasoning: str


class CandidatePlugin(TypedDict):
    plugin: str
    marketplace: str
    reasoning: str


class Boundaries(TypedDict):
    allowed: list[str]
    forbidden: list[str]


class ScopeDraft(TypedDict):
    profile_prose: str
    recommended_skills: list[RecommendedSkill]
    skipped_skills: list[SkippedSkill]
    candidate_uncurated_plugins: list[CandidatePlugin]
    suggested_boundaries: Boundaries


class ScopeExecutor(Protocol):
    def run(self, *, system_prompt: str, user_payload: str) -> str: ...


class StubScopeExecutor:
    """Returns canned JSON strings. For unit tests and --dry-run."""

    def __init__(
        self,
        *,
        canned_result: Optional[str] = None,
        canned_sequence: Optional[list[str]] = None,
    ) -> None:
        if canned_sequence is not None:
            self._sequence = list(canned_sequence)
        elif canned_result is not None:
            self._sequence = [canned_result]
        else:
            raise ValueError("provide canned_result or canned_sequence")
        self.call_count = 0

    def run(self, *, system_prompt: str, user_payload: str) -> str:
        self.call_count += 1
        if not self._sequence:
            raise ScopeExecutorError("stub out of canned responses")
        return self._sequence.pop(0)


def _load_framing() -> str:
    return _FRAMING_RESOURCE.read_text(encoding="utf-8")


def _load_skill_md(catalog: dict[str, dict], catalog_root: Path) -> dict[str, Optional[str]]:
    """For each catalog entry with a local source, read its SKILL.md."""
    out: dict[str, Optional[str]] = {}
    for name, entry in catalog.items():
        source = entry.get("source") if isinstance(entry, dict) else None
        if isinstance(source, str) and source.startswith("./"):
            skill_md = (catalog_root / source[2:] / "SKILL.md")
            try:
                out[name] = skill_md.read_text(encoding="utf-8")
            except OSError:
                out[name] = None
        else:
            out[name] = None
    return out


def _build_payload(
    *,
    profile: RepoProfile,
    plugins: list[dict],
    user_answers: dict[str, str],
    catalog: dict[str, dict],
    skill_md: dict[str, Optional[str]],
) -> str:
    enriched_catalog = {}
    for name, entry in catalog.items():
        enriched_catalog[name] = {**entry, "skill_md": skill_md.get(name)}
    return json.dumps({
        "repo_profile": profile,
        "user_answers": user_answers,
        "catalog": enriched_catalog,
        "marketplace_plugins": plugins,
    }, separators=(",", ":"))


def _validate_draft(obj: object) -> ScopeDraft:
    """Raise ScopeDrafterError if obj doesn't match the ScopeDraft shape."""
    if not isinstance(obj, dict):
        raise ScopeDrafterError("LLM output is not a JSON object")
    required = {
        "profile_prose", "recommended_skills", "skipped_skills",
        "candidate_uncurated_plugins", "suggested_boundaries",
    }
    missing = required - obj.keys()
    if missing:
        raise ScopeDrafterError(f"LLM output missing keys: {sorted(missing)}")
    bounds = obj["suggested_boundaries"]
    if not isinstance(bounds, dict) or "allowed" not in bounds or "forbidden" not in bounds:
        raise ScopeDrafterError("suggested_boundaries must have allowed/forbidden")
    return obj  # type: ignore[return-value]


def _enforce_allowlist(draft: ScopeDraft, catalog: dict[str, dict]) -> ScopeDraft:
    allowed_names = set(catalog.keys())
    kept: list[RecommendedSkill] = []
    demoted: list[CandidatePlugin] = list(draft["candidate_uncurated_plugins"])
    for skill in draft["recommended_skills"]:
        if skill["name"] in allowed_names:
            kept.append(skill)
        else:
            demoted.append(CandidatePlugin(
                plugin=skill["name"],
                marketplace="unknown",
                reasoning=skill["reasoning"],
            ))
    return ScopeDraft(
        profile_prose=draft["profile_prose"],
        recommended_skills=kept,
        skipped_skills=draft["skipped_skills"],
        candidate_uncurated_plugins=demoted,
        suggested_boundaries=draft["suggested_boundaries"],
    )


def draft(
    *,
    profile: RepoProfile,
    plugins: list[dict],
    user_answers: dict[str, str],
    catalog: dict[str, dict],
    executor: ScopeExecutor,
    catalog_root: Optional[Path] = None,
    prompt_version: str = "v1",
) -> ScopeDraft:
    if catalog_root is None:
        # Default: the tokenman library repo root. Resolve from this file.
        catalog_root = Path(__file__).resolve().parents[2]
    skill_md = _load_skill_md(catalog, catalog_root)
    payload = _build_payload(
        profile=profile, plugins=plugins, user_answers=user_answers,
        catalog=catalog, skill_md=skill_md,
    )
    framing = _load_framing()

    raw = executor.run(system_prompt=framing, user_payload=payload)
    try:
        parsed = json.loads(raw)
        validated = _validate_draft(parsed)
    except (json.JSONDecodeError, ScopeDrafterError):
        # Retry once.
        retry_framing = (
            framing
            + "\n\nYour previous response was not valid JSON. "
            "Respond with JSON only, matching the schema."
        )
        raw = executor.run(system_prompt=retry_framing, user_payload=payload)
        try:
            parsed = json.loads(raw)
            validated = _validate_draft(parsed)
        except json.JSONDecodeError as exc:
            raise ScopeDrafterError(
                f"LLM output still not valid JSON after retry: {exc}. "
                f"Raw: {raw[:200]}"
            ) from exc

    return _enforce_allowlist(validated, catalog)
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `pytest tests/test_scope_drafter.py -v`
Expected: 5 passed.

- [ ] **Step 6: Commit**

```bash
git add tests/fixtures/scope-captures harness/lib/scope_drafter.py tests/test_scope_drafter.py
git commit -m "feat(scoping): add scope_drafter with allowlist + retry logic"
```

---

## Task 5: `scoping.v1.md` system prompt

**Goal:** write the real framing text. No tests (content, not logic).

**Files:**
- Modify: `harness/prompts/scoping.v1.md`

- [ ] **Step 1: Replace `harness/prompts/scoping.v1.md` with real content**

```markdown
# Tokenman scoping framing — v1

You are producing an initial-scope draft for a repository that has just
installed tokenman. Your output will seed the user's `.tokenman/tokenman.yaml`
configuration, so it must be accurate, conservative, and honest about what
you do not know.

## Input

The user turn contains a single JSON document with four top-level keys:

- `repo_profile` — deterministic facts about the repo (languages, file
  counts, dep files, test/CI/readme presence, recent-commit count).
- `user_answers` — free-form answers to a short interactive prompt:
  `purpose`, `concern`, `off_limits`, `other`.
- `catalog` — the contents of `recommended-skills.yaml` enriched with a
  `skill_md` field per entry (the full text of the skill's SKILL.md if
  available; null otherwise).
- `marketplace_plugins` — plugins discovered in the user's configured
  Claude-Code plugin marketplaces. Each has `name`, `description`,
  `category`, `homepage`, `marketplace`.

## Output

Respond with **JSON only**. No prose outside the JSON document.

Schema:

```json
{
  "profile_prose": "2-4 sentences narrating what this repo is, grounded only in repo_profile and user_answers",
  "recommended_skills": [
    {
      "name": "<must be a key in catalog>",
      "reasoning": "why this skill fits this repo",
      "default_cadence": "<e.g. on-change, weekly>"
    }
  ],
  "skipped_skills": [
    {
      "name": "<must be a key in catalog>",
      "reasoning": "why you considered but did not recommend"
    }
  ],
  "candidate_uncurated_plugins": [
    {
      "plugin": "<name from marketplace_plugins>",
      "marketplace": "<marketplace name>",
      "reasoning": "why it looks relevant + note that it's not in the curated catalog"
    }
  ],
  "suggested_boundaries": {
    "allowed": ["glob or path", "..."],
    "forbidden": ["glob or path", "..."]
  }
}
```

## Rules (non-negotiable)

1. Every entry in `recommended_skills` MUST have a `name` that appears as
   a key in `catalog`. If a marketplace plugin looks interesting but has
   no matching catalog entry, put it in `candidate_uncurated_plugins`
   instead — never in `recommended_skills`.
2. Derive `suggested_boundaries.allowed` and `.forbidden` primarily from
   the `Scope` sections of each recommended skill's `skill_md` text. If a
   skill's `skill_md` is null or has no Scope section, fall back to
   conservative defaults: `allowed` restricted to top-level README and
   `docs/**`; `forbidden` includes `.tokenman/**`, `.github/**`, and
   anything matching `user_answers.off_limits`.
3. `profile_prose` must be grounded strictly in `repo_profile` and
   `user_answers`. Do not invent features or infer technology stacks
   beyond what the profile indicates.
4. If `user_answers.off_limits` is non-empty, every path fragment in it
   must appear in `suggested_boundaries.forbidden`.
5. If `catalog` is empty, `recommended_skills` must be an empty array.
6. Keep `reasoning` strings short (≤2 sentences).
7. Respond with the JSON document and nothing else — no code fences, no
   commentary.
```

- [ ] **Step 2: Commit**

```bash
git add harness/prompts/scoping.v1.md
git commit -m "feat(scoping): write scoping.v1.md system prompt"
```

---

## Task 6: `ClaudeScopeExecutor` — real `claude -p` subprocess

**Goal:** add the production executor that shells out to `claude -p` and parses the JSON wrapper.

**Files:**
- Modify: `harness/lib/scope_drafter.py`
- Modify: `tests/test_scope_drafter.py` (one new unit test using `monkeypatch`)

- [ ] **Step 1: Add a failing unit test for `ClaudeScopeExecutor`**

Append to `tests/test_scope_drafter.py`:

```python
def test_claude_scope_executor_parses_result_field(monkeypatch) -> None:
    import subprocess
    from harness.lib import scope_drafter as sd

    fake_json = json.dumps({"result": '{"profile_prose":"ok"}'})
    calls: dict[str, object] = {}

    class FakeCompleted:
        returncode = 0
        stdout = fake_json
        stderr = ""

    def fake_run(argv, input, capture_output, text, timeout):  # noqa: A002
        calls["argv"] = argv
        calls["input"] = input
        return FakeCompleted()

    monkeypatch.setattr(subprocess, "run", fake_run)
    executor = sd.ClaudeScopeExecutor(claude_bin="claude")
    out = executor.run(system_prompt="SYS", user_payload="USER")
    assert out == '{"profile_prose":"ok"}'
    assert "claude" in calls["argv"][0]
    assert "-p" in calls["argv"]
    assert "USER" == calls["input"]


def test_claude_scope_executor_raises_on_nonzero_exit(monkeypatch) -> None:
    import subprocess
    from harness.lib import scope_drafter as sd

    class FakeCompleted:
        returncode = 1
        stdout = ""
        stderr = "auth failure"

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: FakeCompleted())
    executor = sd.ClaudeScopeExecutor(claude_bin="claude")
    with pytest.raises(sd.ScopeExecutorError):
        executor.run(system_prompt="SYS", user_payload="USER")
```

- [ ] **Step 2: Run to see the test fail**

Run: `pytest tests/test_scope_drafter.py -v -k claude_scope_executor`
Expected: fail — `ClaudeScopeExecutor` missing.

- [ ] **Step 3: Add `ClaudeScopeExecutor` to `harness/lib/scope_drafter.py`**

Append (above `def _load_framing()` or at bottom; pick bottom for clarity):

```python
class ClaudeScopeExecutor:
    """Production executor: shells out to `claude -p` with JSON output."""

    def __init__(
        self,
        *,
        claude_bin: str = "claude",
        timeout_s: int = 180,
    ) -> None:
        self.claude_bin = claude_bin
        self.timeout_s = timeout_s

    def run(self, *, system_prompt: str, user_payload: str) -> str:
        argv = [
            self.claude_bin,
            "-p",
            "--output-format", "json",
            "--append-system-prompt", system_prompt,
        ]
        try:
            proc = subprocess.run(
                argv,
                input=user_payload,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
            )
        except subprocess.TimeoutExpired as exc:
            raise ScopeExecutorError(
                f"claude -p timed out after {self.timeout_s}s"
            ) from exc
        if proc.returncode != 0:
            raise ScopeExecutorError(
                f"claude -p exited {proc.returncode}: {proc.stderr.strip()}"
            )
        try:
            wrapper = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise ScopeExecutorError(
                f"claude -p stdout is not valid JSON: {exc}"
            ) from exc
        result = wrapper.get("result")
        if not isinstance(result, str):
            raise ScopeExecutorError(
                "claude -p JSON output missing string `result` field"
            )
        return result
```

- [ ] **Step 4: Run the tests**

Run: `pytest tests/test_scope_drafter.py -v`
Expected: all passed (previous 5 + 2 new).

- [ ] **Step 5: Commit**

```bash
git add harness/lib/scope_drafter.py tests/test_scope_drafter.py
git commit -m "feat(scoping): add ClaudeScopeExecutor for real claude -p invocation"
```

---

## Task 7: Rendering — `_render_markdown(draft, profile) -> str`

**Goal:** turn a `ScopeDraft` + `RepoProfile` into the `.tokenman/initial-scope.md` markdown.

**Files:**
- Create: `tests/test_scope_cli.py` (render tests only; CLI tests added in Task 8)
- Modify: `harness/scope/__main__.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_scope_cli.py`:

```python
"""Unit tests for harness.scope.__main__ — rendering and CLI shape."""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.repo_profile import RepoProfile
from harness.lib.scope_drafter import ScopeDraft
from harness.scope import __main__ as scope_cli

REPO_ROOT = Path(__file__).resolve().parent.parent
CANNED = REPO_ROOT / "tests" / "fixtures" / "scope-captures" / "minimal.json"


def _profile() -> RepoProfile:
    return RepoProfile(
        languages={"python": 3, "markdown": 1},
        total_files=4, total_bytes=512,
        tests_present=True, ci_present=False, readme_present=True,
        deps_files=["pyproject.toml"], recent_commits_30d=2,
    )


def _draft() -> ScopeDraft:
    return json.loads(CANNED.read_text())  # type: ignore[return-value]


def test_render_markdown_contains_all_sections() -> None:
    md = scope_cli._render_markdown(
        draft=_draft(), profile=_profile(), repo_name="tiny", prompt_version="v1",
    )
    assert "# Tokenman — Initial scope for tiny" in md
    assert "## Repo profile" in md
    assert "## Recommended skills" in md
    assert "## Skills considered but skipped" in md
    assert "## Candidates for catalog" in md
    assert "## Suggested boundaries" in md
    assert "## What's not here yet" in md
    assert "readme-maintainer" in md
    assert "pyproject.toml" in md


def test_render_markdown_empty_sections_use_placeholders() -> None:
    draft = _draft()
    draft["recommended_skills"] = []
    draft["skipped_skills"] = []
    draft["candidate_uncurated_plugins"] = []
    md = scope_cli._render_markdown(
        draft=draft, profile=_profile(), repo_name="tiny", prompt_version="v1",
    )
    assert "No skills from the curated catalog match this repo yet." in md
    assert "None." in md


def test_render_markdown_notes_empty_marketplace(tmp_path: Path) -> None:
    draft = _draft()
    draft["candidate_uncurated_plugins"] = []
    md = scope_cli._render_markdown(
        draft=draft, profile=_profile(), repo_name="tiny",
        prompt_version="v1", marketplaces_empty=True,
    )
    assert "No marketplaces configured" in md
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_scope_cli.py -v`
Expected: fail — `_render_markdown` not present on `scope_cli`.

- [ ] **Step 3: Implement `_render_markdown` in `harness/scope/__main__.py`**

Replace the current stub `__main__.py` with:

```python
"""`python -m harness.scope` — writes .tokenman/initial-scope.md.

See docs/superpowers/specs/2026-04-18-phase-1-3-scoping-flow-design.md.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from harness.lib.repo_profile import RepoProfile
from harness.lib.scope_drafter import ScopeDraft


def _fmt_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.1f} MB"


def _fmt_languages(languages: dict[str, int]) -> str:
    if not languages:
        return "none detected"
    items = sorted(languages.items(), key=lambda kv: -kv[1])
    return ", ".join(f"{lang} ({n})" for lang, n in items[:5])


def _render_markdown(
    *,
    draft: ScopeDraft,
    profile: RepoProfile,
    repo_name: str,
    prompt_version: str,
    marketplaces_empty: bool = False,
    today: datetime | None = None,
) -> str:
    when = (today or datetime.utcnow()).strftime("%Y-%m-%d")

    lines: list[str] = []
    lines.append(f"# Tokenman — Initial scope for {repo_name}")
    lines.append("")
    lines.append(f"_Generated by `python -m harness.scope` on {when}._")
    lines.append(f"_Prompt version: {prompt_version}._")
    lines.append("")

    lines.append("## Repo profile")
    lines.append("")
    lines.append(draft["profile_prose"].strip())
    lines.append("")
    lines.append("**Facts:**")
    lines.append(f"- Languages: {_fmt_languages(profile['languages'])}")
    lines.append(f"- Files: {profile['total_files']}  Size: {_fmt_bytes(profile['total_bytes'])}")
    lines.append(
        f"- Tests: {'yes' if profile['tests_present'] else 'no'}  "
        f"CI: {'yes' if profile['ci_present'] else 'no'}  "
        f"README: {'yes' if profile['readme_present'] else 'no'}"
    )
    lines.append(
        "- Dependency files: "
        + (", ".join(profile["deps_files"]) if profile["deps_files"] else "none")
    )
    lines.append(f"- Commits in last 30 days: {profile['recent_commits_30d']}")
    lines.append("")

    lines.append("## Recommended skills")
    lines.append("")
    if not draft["recommended_skills"]:
        lines.append("No skills from the curated catalog match this repo yet.")
    else:
        for s in draft["recommended_skills"]:
            lines.append(f"- **{s['name']}** — {s['reasoning']}")
            lines.append(f"  _Default cadence:_ {s['default_cadence']}")
    lines.append("")

    lines.append("## Skills considered but skipped")
    lines.append("")
    if not draft["skipped_skills"]:
        lines.append("None.")
    else:
        for s in draft["skipped_skills"]:
            lines.append(f"- **{s['name']}** — {s['reasoning']}")
    lines.append("")

    lines.append("## Candidates for catalog")
    lines.append("")
    lines.append(
        "The scoping pass found plugins that looked relevant but aren't in "
        "`recommended-skills.yaml`. Tokenman will **not** install these. "
        "If you want to use one, open a PR against the tokenman library "
        "adding it to the catalog."
    )
    lines.append("")
    if marketplaces_empty:
        lines.append(
            "_No marketplaces configured. Run `claude plugins marketplace "
            "add <source>` to enable discovery._"
        )
    elif not draft["candidate_uncurated_plugins"]:
        lines.append("None.")
    else:
        for c in draft["candidate_uncurated_plugins"]:
            lines.append(
                f"- **{c['plugin']}** (marketplace: `{c['marketplace']}`) — "
                f"{c['reasoning']}"
            )
    lines.append("")

    lines.append("## Suggested boundaries")
    lines.append("")
    lines.append("### Allowed paths")
    lines.append("")
    allowed = draft["suggested_boundaries"]["allowed"]
    if allowed:
        for p in allowed:
            lines.append(f"- `{p}`")
    else:
        lines.append(
            "None declared — skills operate under their own SKILL.md scopes."
        )
    lines.append("")
    lines.append("### Forbidden paths")
    lines.append("")
    forbidden = draft["suggested_boundaries"]["forbidden"]
    if forbidden:
        for p in forbidden:
            lines.append(f"- `{p}`")
    else:
        lines.append("None.")
    lines.append("")

    lines.append("## What's not here yet")
    lines.append("")
    lines.append(
        "Budget and schedule strategy are declared by the user in "
        "`.tokenman/tokenman.yaml`; automated suggestion lands with Phase 2 "
        "(spec §7). Expected-PR-volume estimation lands with Phase 4 once "
        "the ledger has history to draw on. This scope file is the seed "
        "for that eventual configuration."
    )
    lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    raise SystemExit("harness.scope CLI is not yet implemented (Phase 1.3)")


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the tests**

Run: `pytest tests/test_scope_cli.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add harness/scope/__main__.py tests/test_scope_cli.py
git commit -m "feat(scoping): add _render_markdown for initial-scope.md output"
```

---

## Task 8: CLI wiring — argparse, interactive prompts, editor flow

**Goal:** make `python -m harness.scope` end-to-end usable, including `--dry-run` and `--non-interactive`.

**Files:**
- Modify: `harness/scope/__main__.py`
- Modify: `tests/test_scope_cli.py`

- [ ] **Step 1: Add failing integration tests**

Append to `tests/test_scope_cli.py`:

```python
import shutil
import subprocess
import sys


def _git_init(repo: Path) -> None:
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "seed"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "seed"], check=True, capture_output=True)


def test_cli_dry_run_non_interactive_writes_scope_file(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    shutil.copytree(REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo", repo)
    _git_init(repo)

    out_path = tmp_path / "initial-scope.md"
    proc = subprocess.run(
        [sys.executable, "-m", "harness.scope",
         "--repo", str(repo),
         "--output-path", str(out_path),
         "--dry-run", "--non-interactive"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert proc.returncode == 0, proc.stderr
    assert out_path.exists()
    content = out_path.read_text()
    assert "# Tokenman — Initial scope for" in content
    assert "## Recommended skills" in content


def test_cli_missing_git_exits_nonzero(tmp_path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "harness.scope",
         "--repo", str(tmp_path),
         "--dry-run", "--non-interactive"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert proc.returncode != 0
```

- [ ] **Step 2: Run to see them fail**

Run: `pytest tests/test_scope_cli.py -v -k cli_`
Expected: fail — CLI still raises `"not yet implemented"`.

- [ ] **Step 3: Replace `main` and add helpers in `harness/scope/__main__.py`**

Replace the `main` function at the bottom of `harness/scope/__main__.py`:

```python
import argparse
import json
import os
import subprocess
import tempfile

import yaml

from harness.lib import marketplace, repo_profile, scope_drafter


def _tokenman_root() -> Path:
    """Find the tokenman library repo root (holds recommended-skills.yaml)."""
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / "recommended-skills.yaml").is_file():
            return candidate
    raise SystemExit("recommended-skills.yaml not found; is tokenman installed?")


def _load_catalog(root: Path) -> dict[str, dict]:
    data = yaml.safe_load((root / "recommended-skills.yaml").read_text()) or {}
    if not isinstance(data, dict):
        raise SystemExit("recommended-skills.yaml must be a mapping")
    return data


_QUESTIONS = [
    ("purpose", "What's this repo for? (one line)"),
    ("concern",
     "Main maintenance concern? [a] docs  [b] dep freshness  "
     "[c] dead code  [d] other"),
    ("off_limits", "Paths off-limits? (comma-separated globs, blank to skip)"),
    ("other", "Anything else the scoping agent should know?"),
]


def _ask_interactive(non_interactive: bool) -> dict[str, str]:
    if non_interactive:
        return {key: "" for key, _ in _QUESTIONS}
    answers: dict[str, str] = {}
    print()
    print("A few questions:")
    print()
    for key, prompt in _QUESTIONS:
        answers[key] = input(f"  {prompt}\n  > ").strip()
        print()
    return answers


def _get_stub_result() -> str:
    """Load the canned response used for --dry-run."""
    path = _tokenman_root() / "tests" / "fixtures" / "scope-captures" / "minimal.json"
    return path.read_text()


def _prompt_accept_edit_abort(rendered: str, non_interactive: bool) -> tuple[str, str]:
    """Return (decision, final_markdown). Decision ∈ {accept, abort}."""
    if non_interactive:
        return "accept", rendered
    print("=== Draft initial-scope.md ===")
    print(rendered)
    print("=============================")
    while True:
        choice = input("Accept this draft? [a]ccept / [e]dit / [x] abort > ").strip().lower()
        if choice in ("a", "accept", ""):
            return "accept", rendered
        if choice in ("x", "abort"):
            return "abort", rendered
        if choice in ("e", "edit"):
            editor = os.environ.get("EDITOR", "vi")
            with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as tf:
                tf.write(rendered)
                tmp_path = tf.name
            subprocess.run([editor, tmp_path], check=False)
            edited = Path(tmp_path).read_text()
            Path(tmp_path).unlink(missing_ok=True)
            if not edited.strip():
                return "abort", rendered
            return "accept", edited
        print("  (choose a / e / x)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.scope")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--refresh", action="store_true",
                        help="refresh marketplace caches before reading")
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--output-path", default=None,
                        help="default: <repo>/.tokenman/initial-scope.md")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="use canned LLM response (no claude invocation)")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    output_path = (
        Path(args.output_path).resolve() if args.output_path
        else repo / ".tokenman" / "initial-scope.md"
    )

    try:
        profile = repo_profile.inspect(repo)
    except repo_profile.RepoProfileError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    plugins = marketplace.list_plugins(refresh=args.refresh)
    marketplaces_empty = not plugins

    root = _tokenman_root()
    catalog = _load_catalog(root)

    answers = _ask_interactive(args.non_interactive)

    if args.dry_run:
        executor = scope_drafter.StubScopeExecutor(canned_result=_get_stub_result())
    else:
        executor = scope_drafter.ClaudeScopeExecutor(claude_bin=args.claude_bin)

    try:
        draft = scope_drafter.draft(
            profile=profile, plugins=plugins, user_answers=answers,
            catalog=catalog, executor=executor, catalog_root=root,
        )
    except (scope_drafter.ScopeExecutorError, scope_drafter.ScopeDrafterError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    rendered = _render_markdown(
        draft=draft, profile=profile, repo_name=repo.name,
        prompt_version="v1", marketplaces_empty=marketplaces_empty,
    )

    decision, final_md = _prompt_accept_edit_abort(rendered, args.non_interactive)
    if decision == "abort":
        print("aborted; no file written", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_md)
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

(Remove the old stub `main` that raised; this replaces it.)

- [ ] **Step 4: Run the tests**

Run: `pytest tests/test_scope_cli.py -v`
Expected: 5 passed.

- [ ] **Step 5: Smoke-test the CLI manually**

Run:
```bash
python -m harness.scope --repo tests/fixtures/tiny-python-repo --dry-run --non-interactive --output-path /tmp/scope-smoke.md
cat /tmp/scope-smoke.md
```

(The fixture needs a `.git/` for this to succeed — the integration test already initialises one in a tmp copy, but the raw fixture path won't work. That's expected; the smoke test here is really for the CLI's argparse + error wiring.)

Expected: If fixture has no `.git/`, the command exits 2 with `"is not a git repository"` — that's the right shape. If you want to see the happy path interactively, run:
```bash
tmp=$(mktemp -d) && cp -r tests/fixtures/tiny-python-repo $tmp/repo && git -C $tmp/repo init -b main && git -C $tmp/repo add -A && git -C $tmp/repo -c user.email=x@x -c user.name=x commit -m seed
python -m harness.scope --repo $tmp/repo --dry-run --non-interactive --output-path $tmp/initial-scope.md
cat $tmp/initial-scope.md
```

- [ ] **Step 6: Run the full test suite**

Run: `pytest -v`
Expected: all pre-existing tests still pass + new tests pass.

- [ ] **Step 7: Commit**

```bash
git add harness/scope/__main__.py tests/test_scope_cli.py
git commit -m "feat(scoping): wire CLI with argparse, interactive prompts, and dry-run"
```

---

## Task 9: Live test (opt-in via `TOKENMAN_LIVE=1`)

**Goal:** verify one end-to-end invocation of real `claude -p` produces a valid `ScopeDraft` on the tiny fixture.

**Files:**
- Create: `tests/test_scope_live.py`

- [ ] **Step 1: Write the live test**

Create `tests/test_scope_live.py`:

```python
"""Live test for `python -m harness.scope`. Gated by TOKENMAN_LIVE=1."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


pytestmark = pytest.mark.skipif(
    os.environ.get("TOKENMAN_LIVE") != "1",
    reason="set TOKENMAN_LIVE=1 to run live claude -p scoping test",
)


def test_scope_live_against_tiny_repo(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "seed"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "seed"],
        check=True, capture_output=True,
    )

    out_path = tmp_path / "initial-scope.md"
    proc = subprocess.run(
        [sys.executable, "-m", "harness.scope",
         "--repo", str(repo),
         "--output-path", str(out_path),
         "--non-interactive"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=180,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
    content = out_path.read_text()
    assert "# Tokenman — Initial scope for" in content
    assert "## Recommended skills" in content
    assert "## Suggested boundaries" in content
```

- [ ] **Step 2: Run in both modes**

Run (skipped mode): `pytest tests/test_scope_live.py -v`
Expected: 1 skipped (no `TOKENMAN_LIVE`).

Run (live mode): `TOKENMAN_LIVE=1 pytest tests/test_scope_live.py -v`
Expected: 1 passed in <180s. If it fails due to claude auth or CLI missing, surface the stderr in the assertion — don't silently skip.

- [ ] **Step 3: Commit**

```bash
git add tests/test_scope_live.py
git commit -m "test(scoping): add opt-in live claude -p scoping test"
```

---

## Task 10: README mention + full-suite verification + PR

**Goal:** add a discoverable reference to the new CLI and open a PR.

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Check where the existing usage note lives**

Run: `grep -n "harness.run\|Usage\|python -m harness" README.md || true`
Expected: you'll find either a `## Usage` section or the `harness.run` mention from Phase 1.2b. Plan the one-line edit accordingly.

- [ ] **Step 2: Add the one-line mention**

Add under the existing Usage section (or create a minimal one if none exists). Example insertion — adapt to actual file:

```markdown
- `python -m harness.scope --repo <path>` — draft `.tokenman/initial-scope.md` for a repo (spec §6.3).
```

- [ ] **Step 3: Run the full test suite**

Run: `pytest -v`
Expected: all tests pass; count grows by the tests added in Tasks 2-8 (roughly +14).

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: mention python -m harness.scope in README"
```

- [ ] **Step 5: Push the branch and open a PR**

```bash
git push -u origin phase-1-3
gh pr create --title "Phase 1.3 — scoping flow (python -m harness.scope)" --body "$(cat <<'EOF'
## Summary

- Adds `python -m harness.scope`: inspects the repo, reads configured plugin marketplaces, asks the user 4 interactive questions, calls `claude -p` once, and writes `.tokenman/initial-scope.md`.
- Enforces the `recommended-skills.yaml` allowlist by demoting any LLM-suggested skill that isn't in the catalog to the "candidates for catalog" section.
- Versioned prompt framing at `harness/prompts/scoping.v1.md`.
- MVP only: budget/schedule/PR-volume sections deferred to Phase 2/4 per spec §6.3.

Implements `docs/superpowers/specs/2026-04-18-phase-1-3-scoping-flow-design.md` via the plan at `docs/superpowers/plans/2026-04-18-phase-1-3-scoping-flow.md`.

## Test plan

- [x] `pytest -v` all green
- [x] `TOKENMAN_LIVE=1 pytest tests/test_scope_live.py` passes
- [x] Manual smoke against a tmp-copy of `tests/fixtures/tiny-python-repo`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Self-review notes

- **Spec §6.3 coverage:** §1 (goal), §3 (journey), §4 (architecture), §5.1–§5.6 (components), §6.1 (payload), §7 (deferred), §8 (error handling), §9 (testing), §10 (open questions), §11 (files), §12 (success criteria) all map to tasks above. Deferrals (budget, schedule, PR volume) are explicit.
- **Allowlist guarantee (§5.1):** enforced by Python in `_enforce_allowlist`; Task 4 unit-tests this directly.
- **SKILL.md flow:** Task 4 tests capture the payload and assert SKILL.md content is included.
- **Non-blockers surfaced by 1.2b** (synthetic capture fixture, workflow install step): not in this plan — they belong to their own cleanup tasks.
- **Type consistency:** `RepoProfile`, `ScopeDraft`, `Plugin`, `ScopeExecutor` keep stable shapes across tasks.
