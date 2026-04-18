# Phase 1.5 — Skill install flow implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `python -m harness.install`, the shared `harness/lib/catalog.py` helper module, and a `harness/lib/installer.py` that fetches remote skills into `.claude/skills/<name>/` at a pinned ref. Extract `skills/readme-maintainer/` to a standalone repo and flip the catalog to its first real remote entry. After this phase the consumer journey is `scope → install → onboard`.

**Architecture:** Thin CLI (`harness/install/__main__.py`) over a pure installer (`harness/lib/installer.py`) that shells out to `git` for clone/checkout/rev-parse, then copies the tree (minus `.git/`) into a target dir and writes a `.tokenman-skill-lock`. Idempotency keyed off the lock's `resolved_sha`. A new `harness/lib/catalog.py` replaces three copies of `_tokenman_root / _load_catalog / _resolve_skill_dir` and raises a `SkillResolutionError` the CLIs convert to exit 2 at their boundaries.

**Tech Stack:** Python 3.10+, `dataclasses`, `subprocess`, `shutil`, `pyyaml`, `pytest`. Reuses the `subprocess.run(["git", …], capture_output=True, text=True)` pattern from `harness/lib/git_ops.py`.

**Spec:** `docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md`

**Branch:** `phase-1-5` off `main` (worktree).

---

## File inventory

**New:**
- `harness/install/__init__.py`
- `harness/install/__main__.py`
- `harness/lib/installer.py`
- `harness/lib/catalog.py`
- `tests/test_installer_local.py`
- `tests/test_installer_remote.py`
- `tests/test_installer_idempotency.py`
- `tests/test_installer_errors.py`
- `tests/test_installer_path_subdir.py`
- `tests/test_install_cli.py`
- `tests/test_install_cli_no_skills.py`
- `tests/test_install_live.py` (opt-in, `TOKENMAN_LIVE=1`)
- `tests/test_catalog.py`
- `tests/test_onboard_errors_when_skill_not_installed.py`
- `tests/fixtures/remote-skills/fake-skill/SKILL.md`
- `tests/fixtures/remote-skills/fake-skill/README.md`

**Touched:**
- `harness/scope/__main__.py` — swap to `harness.lib.catalog` helpers.
- `harness/onboard/__main__.py` — swap to `harness.lib.catalog`; drop "remote sources land in 1.5" exit.
- `harness/lib/scope_drafter.py::_load_skill_md` — handle remote-installed + remote-not-installed cases.
- `tests/conftest.py` — add `build_local_git_repo` + (extract and reuse) `_seed_git_repo`.
- `recommended-skills.yaml` — flip `readme-maintainer` to remote `source:`.
- `skills/README.md` — drop bootstrap note about in-tree skill.
- `.tokenman/CLAUDE.md` — drop forbidden-list entry for `skills/readme-maintainer/`.
- `README.md` — add one-liner for `python -m harness.install`.
- `docs/next-session-prompt.md` — Phase 1.5 complete, Phase 1.6 next.

**Deleted:**
- `skills/readme-maintainer/SKILL.md` (Task 9, after external repo is tagged).
- `skills/readme-maintainer/` (empty dir, removed with the above).

**Reused as-is:**
- `harness/lib/git_ops.py` — pattern reference for `subprocess.run` over `git`.
- `harness/lib/onboarder.py` — `OnboardingResult` pattern for `InstallResult`.
- Existing test fixtures under `tests/fixtures/`.

---

## Task 1: Worktree + module skeleton

**Goal:** Create the `phase-1-5` worktree, stub the new modules so `pytest --collect-only` works, commit an empty-but-valid skeleton.

**Files:**
- Create worktree at `../tokenman-phase-1-5` on branch `phase-1-5` off `main`.
- Create: `harness/install/__init__.py` (empty)
- Create: `harness/install/__main__.py` (stub `main()` returning 1)
- Create: `harness/lib/installer.py` (empty module)
- Create: `harness/lib/catalog.py` (empty module)

- [ ] **Step 1: Create the worktree**

```bash
cd /home/dev/projects/tokenman
git worktree add ../tokenman-phase-1-5 -b phase-1-5 main
cd ../tokenman-phase-1-5
```

Expected: new directory with a clean checkout of `main`.

- [ ] **Step 2: Create empty module files**

```bash
mkdir -p harness/install
: > harness/install/__init__.py
: > harness/lib/catalog.py
```

- [ ] **Step 3: Create installer skeleton**

Write `harness/lib/installer.py`:

```python
"""Skill installer: fetch catalog entries into .claude/skills/<name>/.

See docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md.
"""
from __future__ import annotations

__all__ = ["InstallResult", "install_skill"]
```

- [ ] **Step 4: Create install CLI skeleton**

Write `harness/install/__main__.py`:

```python
"""`python -m harness.install` — populates .claude/skills/ from the catalog.

See docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md.
"""
from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    print("not implemented", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Verify collect + existing tests still pass**

```bash
PYTHONPATH=. pytest --collect-only -q 2>&1 | tail -5
PYTHONPATH=. pytest -q 2>&1 | tail -5
```

Expected: all 102 existing tests pass; no ImportError on the new empty modules.

- [ ] **Step 6: Commit**

```bash
git add harness/install harness/lib/installer.py harness/lib/catalog.py
git commit -m "chore(phase-1-5): add install module skeleton"
```

---

## Task 2: Extract `harness/lib/catalog.py`

**Goal:** Consolidate the three duplicated copies of `_tokenman_root` / `_load_catalog` / `_resolve_skill_dir` into one module. Replace `SystemExit`-based errors with a `SkillResolutionError` the CLIs convert to exit 2 at the boundary. No behavior change.

**Files:**
- Modify: `harness/lib/catalog.py`
- Modify: `harness/scope/__main__.py` (lines 154-167 + usage in `main()`)
- Modify: `harness/onboard/__main__.py` (lines 25-54 + usage in `main()`)
- Create: `tests/test_catalog.py`

- [ ] **Step 1: Write failing test for `load_catalog`**

Write `tests/test_catalog.py`:

```python
"""Unit tests for harness.lib.catalog."""
from __future__ import annotations

from pathlib import Path

import pytest

from harness.lib import catalog
from harness.lib.catalog import SkillResolutionError


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def test_load_catalog_reads_mapping(tmp_path):
    root = tmp_path / "repo"
    _write(root / "recommended-skills.yaml",
           "foo:\n  source: ./skills/foo\n  version: 0.1.0\n")
    result = catalog.load_catalog(root)
    assert result == {"foo": {"source": "./skills/foo", "version": "0.1.0"}}


def test_load_catalog_empty_file_returns_empty(tmp_path):
    root = tmp_path / "repo"
    _write(root / "recommended-skills.yaml", "")
    assert catalog.load_catalog(root) == {}


def test_load_catalog_non_mapping_raises(tmp_path):
    root = tmp_path / "repo"
    _write(root / "recommended-skills.yaml", "- not\n- a\n- mapping\n")
    with pytest.raises(SkillResolutionError, match="must be a mapping"):
        catalog.load_catalog(root)


def test_resolve_skill_dir_local(tmp_path):
    tokenman_root = tmp_path / "lib"
    _write(tokenman_root / "skills" / "foo" / "SKILL.md", "x")
    cat = {"foo": {"source": "./skills/foo", "version": "0.1.0"}}
    path = catalog.resolve_skill_dir(
        skill_name="foo", catalog=cat,
        tokenman_root=tokenman_root, consumer_repo=tmp_path / "consumer",
    )
    assert path == (tokenman_root / "skills" / "foo").resolve()


def test_resolve_skill_dir_unknown_skill_raises(tmp_path):
    with pytest.raises(SkillResolutionError, match="not in recommended-skills.yaml"):
        catalog.resolve_skill_dir(
            skill_name="missing", catalog={},
            tokenman_root=tmp_path, consumer_repo=tmp_path,
        )


def test_resolve_skill_dir_missing_source_raises(tmp_path):
    with pytest.raises(SkillResolutionError, match="no 'source' field"):
        catalog.resolve_skill_dir(
            skill_name="foo", catalog={"foo": {}},
            tokenman_root=tmp_path, consumer_repo=tmp_path,
        )


def test_resolve_skill_dir_remote_installed(tmp_path):
    consumer = tmp_path / "consumer"
    _write(consumer / ".claude" / "skills" / "foo" / "SKILL.md", "x")
    cat = {"foo": {"source": "https://github.com/x/y", "version": "v1"}}
    path = catalog.resolve_skill_dir(
        skill_name="foo", catalog=cat,
        tokenman_root=tmp_path / "lib", consumer_repo=consumer,
    )
    assert path == (consumer / ".claude" / "skills" / "foo").resolve()


def test_resolve_skill_dir_remote_not_installed_raises(tmp_path):
    cat = {"foo": {"source": "https://github.com/x/y", "version": "v1"}}
    with pytest.raises(SkillResolutionError, match="not installed"):
        catalog.resolve_skill_dir(
            skill_name="foo", catalog=cat,
            tokenman_root=tmp_path / "lib", consumer_repo=tmp_path / "consumer",
        )
```

- [ ] **Step 2: Verify tests fail**

```bash
PYTHONPATH=. pytest tests/test_catalog.py -v
```

Expected: all 8 tests fail with `AttributeError: module 'harness.lib.catalog' has no attribute 'load_catalog'`.

- [ ] **Step 3: Implement `harness/lib/catalog.py`**

```python
"""Shared catalog helpers: root lookup, load, resolve skill path.

Replaces three copies previously duplicated in scope/__main__.py and
onboard/__main__.py. Will grow a third caller (install/__main__.py) in
Phase 1.5.
"""
from __future__ import annotations

from pathlib import Path

import yaml


class SkillResolutionError(Exception):
    """Catalog / skill-resolution error. CLIs convert to exit 2."""


def tokenman_root() -> Path:
    """Find the tokenman library repo root (holds recommended-skills.yaml)."""
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / "recommended-skills.yaml").is_file():
            return candidate
    raise SkillResolutionError(
        "recommended-skills.yaml not found; is tokenman installed?"
    )


def load_catalog(root: Path) -> dict[str, dict]:
    data = yaml.safe_load((root / "recommended-skills.yaml").read_text()) or {}
    if not isinstance(data, dict):
        raise SkillResolutionError("recommended-skills.yaml must be a mapping")
    return data


def resolve_skill_dir(
    *,
    skill_name: str,
    catalog: dict,
    tokenman_root: Path,
    consumer_repo: Path,
) -> Path:
    """Return the on-disk path a runner should pass to the executor.

    - Local source ('./…')   → <tokenman_root>/<path>.
    - Remote source ('https:…') → <consumer_repo>/.claude/skills/<name>/
      if present; otherwise raises SkillResolutionError("not installed; …").
    """
    entry = catalog.get(skill_name)
    if entry is None:
        raise SkillResolutionError(
            f"skill {skill_name!r} not in recommended-skills.yaml"
        )
    source = entry.get("source")
    if source is None:
        raise SkillResolutionError(
            f"skill {skill_name!r} has no 'source' field"
        )
    if source.startswith("./"):
        return (tokenman_root / source[2:]).resolve()
    if source.startswith(("https://", "http://")):
        installed = (consumer_repo / ".claude" / "skills" / skill_name).resolve()
        if (installed / "SKILL.md").is_file():
            return installed
        raise SkillResolutionError(
            f"skill {skill_name!r} not installed; "
            "run `python -m harness.install` first"
        )
    raise SkillResolutionError(
        f"skill {skill_name!r} has unsupported source scheme: {source!r}"
    )
```

- [ ] **Step 4: Verify catalog tests pass**

```bash
PYTHONPATH=. pytest tests/test_catalog.py -v
```

Expected: 8 passed.

- [ ] **Step 5: Port `harness/scope/__main__.py` to use `catalog`**

Edit `harness/scope/__main__.py`:

- Remove lines 154-167 (local `_tokenman_root` and `_load_catalog`).
- Add import: `from harness.lib import catalog`.
- Replace `root = _tokenman_root()` with `root = catalog.tokenman_root()`.
- Replace `catalog = _load_catalog(root)` with `catalog_data = catalog.load_catalog(root)` (rename local var to avoid clashing with the module name).
- Update references to the renamed variable in the remainder of `main()`.
- At the top of `main()` wrap the `tokenman_root()` / `load_catalog()` calls in `try/except SkillResolutionError` and print / return 2 on failure.

Concretely, the relevant block in `main()` becomes:

```python
try:
    root = catalog.tokenman_root()
    catalog_data = catalog.load_catalog(root)
except catalog.SkillResolutionError as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 2
```

And the call to `scope_drafter.draft(...)` uses `catalog=catalog_data` (scope_drafter's param name stays).

- [ ] **Step 6: Port `harness/onboard/__main__.py` to use `catalog`**

Edit `harness/onboard/__main__.py`:

- Remove lines 25-54 (local `_tokenman_root`, `_load_catalog`, `_resolve_skill_dir`).
- Add import: `from harness.lib import catalog`.
- Replace the `_tokenman_root()` / `_load_catalog(root)` / `_resolve_skill_dir(...)` call sites with `catalog.tokenman_root()` / `catalog.load_catalog(...)` / `catalog.resolve_skill_dir(...)`.
- Catch `catalog.SkillResolutionError` where `SystemExit` was previously caught; keep exit code 2.

The old block:

```python
try:
    skills = [
        (name, _resolve_skill_dir(name, catalog, root))
        for name in skill_names
    ]
except SystemExit as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 2
```

Becomes:

```python
repo_for_resolve = repo  # consumer repo root
try:
    skills = [
        (name, catalog.resolve_skill_dir(
            skill_name=name, catalog=catalog_data,
            tokenman_root=root, consumer_repo=repo_for_resolve,
        ))
        for name in skill_names
    ]
except catalog.SkillResolutionError as exc:
    print(f"error: {exc}", file=sys.stderr)
    return 2
```

Rename the `catalog` local variable in `main()` to `catalog_data` to avoid clashing with the imported module.

- [ ] **Step 7: Verify full suite still passes**

```bash
PYTHONPATH=. pytest -q 2>&1 | tail -5
```

Expected: all existing tests plus the 8 new `test_catalog.py` tests pass. Prior "remote source Phase 1.5" tests (in onboard) may now fail because `resolve_skill_dir` raises a different message — that's fixed in Task 8. For Task 2, the test assertions are on exit code + "remote" substring; keep the substring in the new message via the old wrapper, OR update those assertions now.

If existing onboard tests fail on the new error message, update the assertions in this same commit to match the new `"not installed"` / `"unsupported source scheme"` wording. Prefer updating tests over preserving the old message — the new message is more useful.

- [ ] **Step 8: Commit**

```bash
git add harness/lib/catalog.py tests/test_catalog.py \
        harness/scope/__main__.py harness/onboard/__main__.py
git commit -m "refactor(harness): extract harness/lib/catalog.py shared helpers"
```

---

## Task 3: `InstallResult` dataclass + local-source install

**Goal:** Land the `InstallResult` dataclass and the local-source arm of `install_skill`. No git operations yet — local sources are resolved in place and return `status=unchanged`.

**Files:**
- Modify: `harness/lib/installer.py`
- Create: `tests/test_installer_local.py`

- [ ] **Step 1: Write failing tests**

Write `tests/test_installer_local.py`:

```python
"""Unit tests for install_skill's local-source (./…) path."""
from __future__ import annotations

from pathlib import Path

import pytest

from harness.lib.installer import InstallResult, install_skill


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def test_local_source_happy_path(tmp_path):
    tokenman_root = tmp_path / "lib"
    _write(tokenman_root / "skills" / "foo" / "SKILL.md", "x")
    target = tmp_path / "consumer" / ".claude" / "skills" / "foo"

    result = install_skill(
        skill_name="foo",
        catalog_entry={"source": "./skills/foo", "version": "0.1.0"},
        target_dir=target,
        tokenman_root=tokenman_root,
    )

    assert isinstance(result, InstallResult)
    assert result.skill_name == "foo"
    assert result.status == "unchanged"
    assert result.exit_code == 0
    assert result.resolved_sha is None
    assert "local" in result.message.lower()
    # Local sources are not copied into the consumer repo.
    assert not target.exists()


def test_local_source_missing_skill_md_errors(tmp_path):
    tokenman_root = tmp_path / "lib"
    (tokenman_root / "skills" / "foo").mkdir(parents=True)
    # No SKILL.md.
    target = tmp_path / "consumer" / ".claude" / "skills" / "foo"

    result = install_skill(
        skill_name="foo",
        catalog_entry={"source": "./skills/foo", "version": "0.1.0"},
        target_dir=target,
        tokenman_root=tokenman_root,
    )

    assert result.status == "errored"
    assert result.exit_code == 4
    assert "SKILL.md" in result.message


def test_result_is_frozen():
    r = InstallResult(
        skill_name="foo",
        status="unchanged",
        resolved_sha=None,
        message="ok",
        exit_code=0,
    )
    with pytest.raises(Exception):
        r.status = "errored"  # type: ignore[misc]
```

- [ ] **Step 2: Verify tests fail**

```bash
PYTHONPATH=. pytest tests/test_installer_local.py -v
```

Expected: ImportError — `InstallResult` / `install_skill` not defined.

- [ ] **Step 3: Implement the dataclass + local-source arm**

Replace `harness/lib/installer.py`:

```python
"""Skill installer: fetch catalog entries into .claude/skills/<name>/.

See docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

__all__ = ["InstallResult", "install_skill"]


@dataclass(frozen=True)
class InstallResult:
    skill_name: str
    status: Literal["installed", "unchanged", "errored"]
    resolved_sha: Optional[str]
    message: str
    exit_code: int


def install_skill(
    *,
    skill_name: str,
    catalog_entry: dict,
    target_dir: Path,
    tokenman_root: Path,
    force: bool = False,
) -> InstallResult:
    source = catalog_entry.get("source")
    if source is None:
        return InstallResult(
            skill_name=skill_name, status="errored",
            resolved_sha=None, exit_code=2,
            message="catalog entry has no 'source' field",
        )

    if source.startswith("./"):
        return _install_local(
            skill_name=skill_name,
            local_path=(tokenman_root / source[2:]).resolve(),
        )

    return InstallResult(
        skill_name=skill_name, status="errored",
        resolved_sha=None, exit_code=2,
        message=f"unsupported source scheme: {source!r}",
    )


def _install_local(*, skill_name: str, local_path: Path) -> InstallResult:
    if not (local_path / "SKILL.md").is_file():
        return InstallResult(
            skill_name=skill_name, status="errored",
            resolved_sha=None, exit_code=4,
            message=f"local source has no SKILL.md at {local_path}",
        )
    return InstallResult(
        skill_name=skill_name, status="unchanged",
        resolved_sha=None, exit_code=0,
        message=f"local source resolved in place at {local_path}",
    )
```

- [ ] **Step 4: Verify tests pass**

```bash
PYTHONPATH=. pytest tests/test_installer_local.py -v
```

Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add harness/lib/installer.py tests/test_installer_local.py
git commit -m "feat(install): add InstallResult + local-source install_skill"
```

---

## Task 4: Conftest git helper + remote happy path

**Goal:** Add a reusable `build_local_git_repo` conftest helper that stands up a local bare repo with a tagged commit, then implement the remote-source happy path: clone → checkout → rev-parse → copy (minus `.git/`) → write lock → verify SKILL.md.

**Files:**
- Modify: `tests/conftest.py`
- Create: `tests/fixtures/remote-skills/fake-skill/SKILL.md`
- Create: `tests/fixtures/remote-skills/fake-skill/README.md`
- Modify: `harness/lib/installer.py`
- Create: `tests/test_installer_remote.py`

- [ ] **Step 1: Add the fake-skill fixture**

Write `tests/fixtures/remote-skills/fake-skill/SKILL.md`:

```markdown
---
name: fake-skill
description: Test fixture — not a real skill.
---

# fake-skill

This fixture exists to exercise the install flow's remote path.
```

Write `tests/fixtures/remote-skills/fake-skill/README.md`:

```markdown
# fake-skill

Test fixture for tokenman's install flow tests.
```

- [ ] **Step 2: Add `build_local_git_repo` helper to conftest**

Read the current `tests/conftest.py`. If it doesn't exist, create it; otherwise extend it. Add:

```python
"""Shared pytest fixtures."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=test", "-c", "user.email=t@t", *args],
        cwd=str(cwd), check=True, capture_output=True, text=True,
    )


def _build_local_git_repo(
    *,
    source_tree: Path,
    dest: Path,
    tag: str = "v0.1.0",
) -> Path:
    """Copy `source_tree` into a fresh git repo at `dest`, commit, tag.

    Returns `dest` — a plain clone-able directory (not a bare repo).
    Used as the `source:` URL for remote-source installer tests.
    """
    dest.mkdir(parents=True, exist_ok=True)
    for entry in source_tree.iterdir():
        if entry.is_dir():
            shutil.copytree(entry, dest / entry.name)
        else:
            shutil.copy2(entry, dest / entry.name)
    _git(dest, "init", "-q", "-b", "main")
    _git(dest, "add", "-A")
    _git(dest, "commit", "-q", "-m", "initial")
    _git(dest, "tag", tag)
    return dest


@pytest.fixture
def build_local_git_repo(tmp_path):
    """Factory fixture: returns _build_local_git_repo bound to tmp_path roots."""
    def _make(source_tree: Path, *, tag: str = "v0.1.0", subdir: str = "remote-repo") -> Path:
        return _build_local_git_repo(
            source_tree=source_tree, dest=tmp_path / subdir, tag=tag,
        )
    return _make


@pytest.fixture
def fake_skill_source():
    """Path to the checked-in fake-skill source tree."""
    return Path(__file__).parent / "fixtures" / "remote-skills" / "fake-skill"
```

If `tests/conftest.py` already exists, merge these fixtures in rather than overwriting. Also inspect existing test files for `_seed_git_repo` duplicates (flagged in handoff). If the duplicate lives in multiple test modules, extract one copy to conftest in this same step. Look for it with:

```bash
PYTHONPATH=. grep -rn "_seed_git_repo" tests/ | head
```

If it's used in 5+ files, pick the most complete copy, move it to conftest as a `@pytest.fixture` (or module-level helper), and update callers. Otherwise, skip the extraction and let the duplicates ride.

- [ ] **Step 3: Write failing tests for remote happy path**

Write `tests/test_installer_remote.py`:

```python
"""Unit tests for install_skill's remote-source happy path."""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.installer import install_skill


def test_remote_happy_path(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    target = tmp_path / "consumer" / ".claude" / "skills" / "fake-skill"
    tokenman_root = tmp_path / "lib"
    tokenman_root.mkdir()

    result = install_skill(
        skill_name="fake-skill",
        catalog_entry={"source": f"file://{remote}", "version": "v0.1.0"},
        target_dir=target,
        tokenman_root=tokenman_root,
    )

    assert result.status == "installed", result.message
    assert result.exit_code == 0
    assert result.resolved_sha and len(result.resolved_sha) == 40

    assert (target / "SKILL.md").is_file()
    assert (target / "README.md").is_file()
    assert not (target / ".git").exists()

    lock = json.loads((target / ".tokenman-skill-lock").read_text())
    assert lock["source"] == f"file://{remote}"
    assert lock["version"] == "v0.1.0"
    assert lock["resolved_sha"] == result.resolved_sha
    assert lock["installed_at"].endswith("Z")


def test_remote_checkout_by_sha(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    import subprocess
    sha = subprocess.run(
        ["git", "-C", str(remote), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    target = tmp_path / "consumer" / ".claude" / "skills" / "fake-skill"
    tokenman_root = tmp_path / "lib"
    tokenman_root.mkdir()

    result = install_skill(
        skill_name="fake-skill",
        catalog_entry={"source": f"file://{remote}", "version": sha},
        target_dir=target,
        tokenman_root=tokenman_root,
    )

    assert result.status == "installed", result.message
    assert result.resolved_sha == sha
```

- [ ] **Step 4: Verify tests fail**

```bash
PYTHONPATH=. pytest tests/test_installer_remote.py -v
```

Expected: fail — remote path not implemented.

- [ ] **Step 5: Implement the remote arm**

Append to `harness/lib/installer.py` (keep existing code; add new helpers and wire into `install_skill`):

```python
import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

_REMOTE_SCHEMES = ("https://", "http://", "file://", "git://", "ssh://")


def install_skill(
    *,
    skill_name: str,
    catalog_entry: dict,
    target_dir: Path,
    tokenman_root: Path,
    force: bool = False,
) -> InstallResult:
    source = catalog_entry.get("source")
    if source is None:
        return InstallResult(
            skill_name=skill_name, status="errored",
            resolved_sha=None, exit_code=2,
            message="catalog entry has no 'source' field",
        )

    if source.startswith("./"):
        return _install_local(
            skill_name=skill_name,
            local_path=(tokenman_root / source[2:]).resolve(),
        )

    if source.startswith(_REMOTE_SCHEMES):
        return _install_remote(
            skill_name=skill_name,
            catalog_entry=catalog_entry,
            target_dir=target_dir,
            force=force,
        )

    return InstallResult(
        skill_name=skill_name, status="errored",
        resolved_sha=None, exit_code=2,
        message=f"unsupported source scheme: {source!r}",
    )


def _install_remote(
    *,
    skill_name: str,
    catalog_entry: dict,
    target_dir: Path,
    force: bool,
) -> InstallResult:
    source = catalog_entry["source"]
    version = catalog_entry.get("version")
    if not version:
        return InstallResult(
            skill_name=skill_name, status="errored",
            resolved_sha=None, exit_code=2,
            message="catalog entry has no 'version' field",
        )

    subpath = catalog_entry.get("path")

    with tempfile.TemporaryDirectory(prefix="tokenman-install-") as tmp:
        tmpdir = Path(tmp)
        clone_dir = tmpdir / "clone"
        try:
            _git_clone(source, clone_dir)
            _git_checkout(clone_dir, version)
            resolved_sha = _git_rev_parse(clone_dir)
        except _GitError as exc:
            return InstallResult(
                skill_name=skill_name, status="errored",
                resolved_sha=None, exit_code=3,
                message=f"git: {exc}",
            )

        source_tree = clone_dir / subpath if subpath else clone_dir
        if not source_tree.is_dir():
            return InstallResult(
                skill_name=skill_name, status="errored",
                resolved_sha=None, exit_code=4,
                message=f"path {subpath!r} not found in cloned tree",
            )

        target_dir.parent.mkdir(parents=True, exist_ok=True)
        if target_dir.exists():
            shutil.rmtree(target_dir)
        _copy_tree_minus_git(source_tree, target_dir)

        if not (target_dir / "SKILL.md").is_file():
            shutil.rmtree(target_dir, ignore_errors=True)
            return InstallResult(
                skill_name=skill_name, status="errored",
                resolved_sha=None, exit_code=4,
                message="SKILL.md missing after checkout",
            )

        _write_lock(
            target_dir=target_dir, source=source,
            version=version, resolved_sha=resolved_sha,
        )

    return InstallResult(
        skill_name=skill_name, status="installed",
        resolved_sha=resolved_sha, exit_code=0,
        message=f"installed {skill_name} at {version}",
    )


class _GitError(RuntimeError):
    pass


def _git_run(cmd: list[str], *, cwd: Optional[Path] = None) -> str:
    proc = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None,
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        raise _GitError(proc.stderr.strip() or proc.stdout.strip() or "unknown error")
    return proc.stdout.strip()


def _git_clone(source: str, dest: Path) -> None:
    _git_run(["git", "clone", "--quiet", source, str(dest)])


def _git_checkout(repo: Path, ref: str) -> None:
    _git_run(["git", "-C", str(repo), "checkout", "--quiet", ref])


def _git_rev_parse(repo: Path) -> str:
    return _git_run(["git", "-C", str(repo), "rev-parse", "HEAD"])


def _copy_tree_minus_git(src: Path, dst: Path) -> None:
    shutil.copytree(
        src, dst,
        ignore=shutil.ignore_patterns(".git"),
        symlinks=True,
    )


def _write_lock(
    *, target_dir: Path, source: str, version: str, resolved_sha: str,
) -> None:
    lock = {
        "source": source,
        "version": version,
        "resolved_sha": resolved_sha,
        "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    (target_dir / ".tokenman-skill-lock").write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n"
    )
```

Note: keep the existing `_install_local` helper and `InstallResult` dataclass from Task 3.

- [ ] **Step 6: Verify remote tests pass**

```bash
PYTHONPATH=. pytest tests/test_installer_remote.py tests/test_installer_local.py -v
```

Expected: 5 passed.

- [ ] **Step 7: Commit**

```bash
git add tests/fixtures/remote-skills tests/conftest.py \
        harness/lib/installer.py tests/test_installer_remote.py
git commit -m "feat(install): remote-source happy path in install_skill"
```

---

## Task 5: Idempotency + `--force` + drift detection

**Goal:** Second-run behavior. Lock matches resolved sha → `unchanged`, no mutation. Lock missing or mismatched and not `--force` → `exit_code=5`, target untouched. `--force` → rm + reinstall.

**Files:**
- Modify: `harness/lib/installer.py`
- Create: `tests/test_installer_idempotency.py`

- [ ] **Step 1: Write failing tests**

Write `tests/test_installer_idempotency.py`:

```python
"""Idempotency, drift, and --force behavior for install_skill."""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.installer import install_skill


def _install_once(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    target = tmp_path / "consumer" / ".claude" / "skills" / "fake-skill"
    tokenman_root = tmp_path / "lib"
    tokenman_root.mkdir()
    entry = {"source": f"file://{remote}", "version": "v0.1.0"}
    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=tokenman_root,
    )
    assert result.status == "installed"
    return remote, target, tokenman_root, entry, result


def test_unchanged_when_lock_matches(tmp_path, build_local_git_repo, fake_skill_source):
    _, target, root, entry, first = _install_once(tmp_path, build_local_git_repo, fake_skill_source)
    # Touch a file to prove unchanged really doesn't mutate.
    sentinel = target / "SENTINEL"
    sentinel.write_text("keep me")

    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=root,
    )
    assert result.status == "unchanged"
    assert result.exit_code == 0
    assert result.resolved_sha == first.resolved_sha
    assert sentinel.read_text() == "keep me"


def test_drift_without_force_errors(tmp_path, build_local_git_repo, fake_skill_source):
    _, target, root, entry, _ = _install_once(tmp_path, build_local_git_repo, fake_skill_source)
    # Corrupt the lock to simulate drift.
    lock_path = target / ".tokenman-skill-lock"
    lock = json.loads(lock_path.read_text())
    lock["resolved_sha"] = "0" * 40
    lock_path.write_text(json.dumps(lock))
    sentinel = target / "SENTINEL"
    sentinel.write_text("keep me")

    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=root,
    )
    assert result.status == "errored"
    assert result.exit_code == 5
    assert "--force" in result.message
    assert sentinel.read_text() == "keep me"  # not touched


def test_drift_with_force_reinstalls(tmp_path, build_local_git_repo, fake_skill_source):
    _, target, root, entry, first = _install_once(tmp_path, build_local_git_repo, fake_skill_source)
    lock_path = target / ".tokenman-skill-lock"
    lock = json.loads(lock_path.read_text())
    lock["resolved_sha"] = "0" * 40
    lock_path.write_text(json.dumps(lock))
    sentinel = target / "SENTINEL"
    sentinel.write_text("should be removed")

    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=root, force=True,
    )
    assert result.status == "installed"
    assert result.resolved_sha == first.resolved_sha
    assert not sentinel.exists()


def test_missing_lock_treated_as_drift(tmp_path, build_local_git_repo, fake_skill_source):
    _, target, root, entry, _ = _install_once(tmp_path, build_local_git_repo, fake_skill_source)
    (target / ".tokenman-skill-lock").unlink()

    result = install_skill(
        skill_name="fake-skill", catalog_entry=entry,
        target_dir=target, tokenman_root=root,
    )
    assert result.status == "errored"
    assert result.exit_code == 5
```

- [ ] **Step 2: Verify tests fail**

```bash
PYTHONPATH=. pytest tests/test_installer_idempotency.py -v
```

Expected: 4 fail (currently `target.exists()` always triggers a rewrite).

- [ ] **Step 3: Implement idempotency + drift check**

Edit `harness/lib/installer.py`. In `_install_remote`, before any git work, add a fast pre-check that reads the existing lock and compares against the catalog's `version` (where possible) — but we can't know the resolved sha without cloning, so the cheapest route is: clone first (or better, use `git ls-remote`), then decide.

Simpler implementation: always clone, then compare. Replace the `if target_dir.exists(): shutil.rmtree(target_dir)` block with the drift logic:

```python
        # After resolved_sha is known.
        if target_dir.exists():
            existing = _read_existing_lock(target_dir)
            if existing is not None and existing.get("resolved_sha") == resolved_sha:
                return InstallResult(
                    skill_name=skill_name, status="unchanged",
                    resolved_sha=resolved_sha, exit_code=0,
                    message=f"{skill_name} already at {resolved_sha[:12]}",
                )
            if not force:
                return InstallResult(
                    skill_name=skill_name, status="errored",
                    resolved_sha=resolved_sha, exit_code=5,
                    message=(
                        f"{target_dir} exists but does not match "
                        f"{resolved_sha[:12]}; re-run with --force to overwrite"
                    ),
                )
            shutil.rmtree(target_dir)
```

Add the helper:

```python
def _read_existing_lock(target_dir: Path) -> Optional[dict]:
    lock_path = target_dir / ".tokenman-skill-lock"
    if not lock_path.is_file():
        return None
    try:
        return json.loads(lock_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
```

A lock file that's missing OR unreadable returns `None` → treated as drift (the `existing is not None and …` check fails, so we fall through to the `if not force:` branch).

- [ ] **Step 4: Verify all installer tests pass**

```bash
PYTHONPATH=. pytest tests/test_installer_local.py tests/test_installer_remote.py \
                   tests/test_installer_idempotency.py -v
```

Expected: 9 passed (3 + 2 + 4).

- [ ] **Step 5: Commit**

```bash
git add harness/lib/installer.py tests/test_installer_idempotency.py
git commit -m "feat(install): idempotency, drift detection, --force"
```

---

## Task 6: Error paths + optional `path:` subdir

**Goal:** Cover the remaining per-skill error paths — bad ref (exit 3), SKILL.md missing after checkout (exit 4, rollback), unsupported source scheme (exit 2) — and the optional `path:` catalog field.

**Files:**
- Modify: `harness/lib/installer.py` (polish; most code in place from Task 4)
- Create: `tests/test_installer_errors.py`
- Create: `tests/test_installer_path_subdir.py`

- [ ] **Step 1: Write failing error-path tests**

Write `tests/test_installer_errors.py`:

```python
"""Error paths for install_skill: bad ref, missing SKILL.md, unsupported scheme."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from harness.lib.installer import install_skill


def test_unsupported_scheme(tmp_path):
    result = install_skill(
        skill_name="x",
        catalog_entry={"source": "git@github.com:foo/bar", "version": "v1"},
        target_dir=tmp_path / "target",
        tokenman_root=tmp_path / "root",
    )
    assert result.status == "errored"
    assert result.exit_code == 2
    assert "unsupported source scheme" in result.message


def test_missing_source(tmp_path):
    result = install_skill(
        skill_name="x", catalog_entry={"version": "v1"},
        target_dir=tmp_path / "t", tokenman_root=tmp_path,
    )
    assert result.exit_code == 2
    assert "source" in result.message


def test_missing_version(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    result = install_skill(
        skill_name="x", catalog_entry={"source": f"file://{remote}"},
        target_dir=tmp_path / "t", tokenman_root=tmp_path,
    )
    assert result.exit_code == 2
    assert "version" in result.message


def test_bad_ref_exits_3(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    target = tmp_path / "target"
    result = install_skill(
        skill_name="x",
        catalog_entry={"source": f"file://{remote}", "version": "does-not-exist"},
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "errored"
    assert result.exit_code == 3
    assert not target.exists()


def test_clone_failure_exits_3(tmp_path):
    target = tmp_path / "target"
    result = install_skill(
        skill_name="x",
        catalog_entry={"source": f"file://{tmp_path / 'nope'}", "version": "v1"},
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "errored"
    assert result.exit_code == 3
    assert not target.exists()


def test_missing_skill_md_rolls_back(tmp_path, build_local_git_repo):
    # Build a remote repo that lacks SKILL.md.
    empty_src = tmp_path / "empty-source"
    empty_src.mkdir()
    (empty_src / "README.md").write_text("no skill here")
    remote = build_local_git_repo(empty_src, subdir="empty-remote")

    target = tmp_path / "target"
    result = install_skill(
        skill_name="x",
        catalog_entry={"source": f"file://{remote}", "version": "v0.1.0"},
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "errored"
    assert result.exit_code == 4
    assert "SKILL.md" in result.message
    assert not target.exists()
```

- [ ] **Step 2: Write failing `path:` subdir test**

Write `tests/test_installer_path_subdir.py`:

```python
"""install_skill honors an optional `path:` subdir in the catalog entry."""
from __future__ import annotations

from pathlib import Path

from harness.lib.installer import install_skill


def test_path_subdir_copies_only_subtree(tmp_path, build_local_git_repo):
    # Remote layout:
    #   README.md     (not in path:)
    #   skill/SKILL.md
    #   skill/helper.sh
    src = tmp_path / "multi-skill-source"
    (src / "skill").mkdir(parents=True)
    (src / "README.md").write_text("repo-level README")
    (src / "skill" / "SKILL.md").write_text("---\nname: x\n---\n")
    (src / "skill" / "helper.sh").write_text("#!/bin/sh\necho hi\n")

    remote = build_local_git_repo(src, subdir="remote-multi")
    target = tmp_path / "consumer" / ".claude" / "skills" / "x"

    result = install_skill(
        skill_name="x",
        catalog_entry={
            "source": f"file://{remote}",
            "version": "v0.1.0",
            "path": "skill",
        },
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "installed", result.message
    assert (target / "SKILL.md").is_file()
    assert (target / "helper.sh").is_file()
    assert not (target / "README.md").exists()


def test_path_subdir_missing_exits_4(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    target = tmp_path / "target"
    result = install_skill(
        skill_name="x",
        catalog_entry={
            "source": f"file://{remote}",
            "version": "v0.1.0",
            "path": "nowhere",
        },
        target_dir=target, tokenman_root=tmp_path,
    )
    assert result.status == "errored"
    assert result.exit_code == 4
    assert "path" in result.message.lower()
    assert not target.exists()
```

- [ ] **Step 3: Verify tests run**

```bash
PYTHONPATH=. pytest tests/test_installer_errors.py tests/test_installer_path_subdir.py -v
```

Expected: most pass (Task 4's code already handles bad-ref, missing-SKILL.md, subpath). The one likely to fail is `test_clone_failure_exits_3` if the code path wasn't hit; also verify messages.

Fix any failures by tightening messages or the subpath guard. The implementation should already satisfy all 7 error-path tests from Task 4's code; this task is primarily test coverage.

If a test fails because the subpath check happens before clone success OR because `_GitError` doesn't wrap `git clone file://nonexistent`, inspect and patch. Likely patch: move the `_install_remote` function's error messages to be more specific (include `source` URL or ref name).

- [ ] **Step 4: Verify full installer suite passes**

```bash
PYTHONPATH=. pytest tests/test_installer_local.py tests/test_installer_remote.py \
                   tests/test_installer_idempotency.py tests/test_installer_errors.py \
                   tests/test_installer_path_subdir.py -v
```

Expected: 16 passed (3 + 2 + 4 + 6 + 2, give or take 1 for subdir edge cases).

- [ ] **Step 5: Commit**

```bash
git add tests/test_installer_errors.py tests/test_installer_path_subdir.py \
        harness/lib/installer.py
git commit -m "feat(install): error paths (bad ref, missing SKILL.md) and path: subdir"
```

---

## Task 7: `python -m harness.install` CLI

**Goal:** Glue module — argparse, config load, skill resolution, loop over `install_skill`, summary lines, exit-code aggregation. Mirror `harness.onboard` patterns.

**Files:**
- Modify: `harness/install/__main__.py`
- Create: `tests/test_install_cli.py`
- Create: `tests/test_install_cli_no_skills.py`

The CLI needs a `--catalog-path` flag so tests can point at an alternate catalog without touching the real `recommended-skills.yaml`. Task 7 wires that flag in Step 4.

- [ ] **Step 1: Write failing CLI smoke test**

Write `tests/test_install_cli.py`:

```python
"""Smoke tests for `python -m harness.install`."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def _run_cli(*, cwd: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    env_root = Path(__file__).resolve().parents[1]
    return subprocess.run(
        [sys.executable, "-m", "harness.install", *args],
        cwd=str(cwd),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
    )


def test_cli_installs_and_is_idempotent(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    catalog_path = tmp_path / "lib" / "recommended-skills.yaml"
    _write(
        catalog_path,
        textwrap.dedent(f"""
            fake-skill:
              source: file://{remote}
              version: v0.1.0
        """).lstrip(),
    )
    consumer = tmp_path / "consumer"
    consumer.mkdir()

    first = _run_cli(
        cwd=consumer,
        args=[
            "--repo", str(consumer),
            "--catalog-path", str(catalog_path),
            "--skill", "fake-skill",
        ],
    )
    assert first.returncode == 0, first.stderr
    assert "installed" in first.stdout
    target = consumer / ".claude" / "skills" / "fake-skill"
    assert (target / "SKILL.md").is_file()
    lock = json.loads((target / ".tokenman-skill-lock").read_text())
    assert lock["version"] == "v0.1.0"

    second = _run_cli(
        cwd=consumer,
        args=[
            "--repo", str(consumer),
            "--catalog-path", str(catalog_path),
            "--skill", "fake-skill",
        ],
    )
    assert second.returncode == 0, second.stderr
    assert "unchanged" in second.stdout
```

- [ ] **Step 2: Write failing no-skills test**

Write `tests/test_install_cli_no_skills.py`:

```python
"""`python -m harness.install` with no enabled skills exits 2 with a hint."""
from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path


def test_no_skills_exits_2(tmp_path):
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    # No --skill flag, no tokenman.yaml.

    env_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "harness.install", "--repo", str(consumer)],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 2
    assert "no skills" in result.stderr.lower()
    assert "harness.scope" in result.stderr or "--skill" in result.stderr
```

- [ ] **Step 3: Verify tests fail**

```bash
PYTHONPATH=. pytest tests/test_install_cli.py tests/test_install_cli_no_skills.py -v
```

Expected: both fail — CLI prints "not implemented".

- [ ] **Step 4: Implement the CLI**

Replace `harness/install/__main__.py`:

```python
"""`python -m harness.install` — populates .claude/skills/ from the catalog.

See docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml

from harness.lib import catalog, installer


def _enabled_skills_from_config(config_path: Path) -> list[str]:
    if not config_path.is_file():
        return []
    data = yaml.safe_load(config_path.read_text()) or {}
    skills = data.get("skills") or []
    if not isinstance(skills, list):
        return []
    return [s for s in skills if isinstance(s, str)]


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.install")
    parser.add_argument("--repo", default=".",
                        help="consumer repo (install target)")
    parser.add_argument("--config-path", default=None,
                        help="default: <repo>/.tokenman/tokenman.yaml")
    parser.add_argument("--catalog-path", default=None,
                        help="override tokenman library's recommended-skills.yaml "
                             "(defaults to the one in the tokenman library root)")
    parser.add_argument("--skill", action="append", default=[],
                        help="repeatable; overrides config skills list")
    parser.add_argument("--force", action="store_true",
                        help="rm -rf drifted targets before reinstalling")
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would happen; no filesystem writes")
    parser.add_argument("--non-interactive", action="store_true",
                        help="reserved; install has no prompts today")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    config_path = (
        Path(args.config_path).resolve() if args.config_path
        else repo / ".tokenman" / "tokenman.yaml"
    )

    try:
        root = catalog.tokenman_root()
    except catalog.SkillResolutionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.catalog_path:
        catalog_path = Path(args.catalog_path).resolve()
        root = catalog_path.parent
        try:
            catalog_data = catalog.load_catalog(root)
        except catalog.SkillResolutionError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
    else:
        try:
            catalog_data = catalog.load_catalog(root)
        except catalog.SkillResolutionError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    if args.skill:
        skill_names = list(args.skill)
    else:
        skill_names = _enabled_skills_from_config(config_path)

    if not skill_names:
        print(
            "error: no skills enabled. Add skills to "
            f"{config_path} or pass --skill NAME (repeatable). "
            "Run `python -m harness.scope` first to draft a config.",
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        for name in skill_names:
            entry = catalog_data.get(name)
            src = entry.get("source") if entry else "<unknown>"
            ver = entry.get("version") if entry else "<unknown>"
            print(f"[dry-run] would install {name} from {src} @ {ver}")
        return 0

    final_exit = 0
    for name in skill_names:
        entry = catalog_data.get(name)
        if entry is None:
            print(f"{name}: errored(skill not in catalog)")
            final_exit = max(final_exit, 2)
            continue

        target = repo / ".claude" / "skills" / name
        result = installer.install_skill(
            skill_name=name,
            catalog_entry=entry,
            target_dir=target,
            tokenman_root=root,
            force=args.force,
        )

        print(f"{result.skill_name}: {result.status}({result.message})")
        final_exit = max(final_exit, result.exit_code)

    return final_exit


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Verify CLI tests pass**

```bash
PYTHONPATH=. pytest tests/test_install_cli.py tests/test_install_cli_no_skills.py -v
```

Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add harness/install/__main__.py tests/test_install_cli.py \
        tests/test_install_cli_no_skills.py
git commit -m "feat(install): add python -m harness.install CLI"
```

---

## Task 8: Scope + onboard updates for remote sources

**Goal:** Drop the "remote skill sources land in Phase 1.5" exit in scope + onboard (handled now via `catalog.resolve_skill_dir`). Update `scope_drafter._load_skill_md` to look in `.claude/skills/<name>/` for installed remote skills. Add an onboard test covering the "run install first" error.

**Files:**
- Modify: `harness/scope/__main__.py` (any remaining guard)
- Modify: `harness/onboard/__main__.py` (any remaining guard)
- Modify: `harness/lib/scope_drafter.py` (`_load_skill_md`)
- Create: `tests/test_onboard_errors_when_skill_not_installed.py`

- [ ] **Step 1: Confirm scope + onboard no longer carry the old exit**

```bash
PYTHONPATH=. grep -n "remote skill sources land" harness/
PYTHONPATH=. grep -n "Phase 1.5" harness/
```

After Task 2, the only remaining reference should be in spec files — `catalog.resolve_skill_dir` already raises the new message. If the grep surfaces stale TODOs in scope/onboard, delete them.

- [ ] **Step 2: Write failing test: onboard errors when skill not installed**

Write `tests/test_onboard_errors_when_skill_not_installed.py`:

```python
"""onboard exits 2 with a clear message when a remote skill isn't installed."""
from __future__ import annotations

import subprocess
import sys
import os
import textwrap
from pathlib import Path


def test_onboard_errors_when_remote_skill_not_installed(tmp_path):
    consumer = tmp_path / "consumer"
    (consumer / ".tokenman").mkdir(parents=True)

    # Fake tokenman.yaml pointing at a remote skill not yet installed.
    (consumer / ".tokenman" / "tokenman.yaml").write_text(
        textwrap.dedent("""
            skills:
              - some-remote-skill
        """).lstrip()
    )

    # Point the CLI at a catalog we control, where some-remote-skill
    # is a remote source. We achieve that by temporarily modifying the
    # tokenman catalog in a tmp checkout OR by relying on the real
    # catalog once it contains remote entries (post-Task 9).
    #
    # For this test, we assert the catalog lookup error path via the
    # onboard CLI's --skill override and an environment where the
    # catalog has been overridden. Since onboard doesn't currently
    # take --catalog-path, rely on --skill + the catalog's existing
    # readme-maintainer entry (post-Task 9 flip: remote source).
    #
    # Until Task 9 lands the catalog flip, this test uses --skill
    # readme-maintainer and asserts the 'not installed' error surfaces.

    env_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable, "-m", "harness.onboard",
            "--repo", str(consumer),
            "--skill", "readme-maintainer",
            "--dry-run",  # dry-run doesn't hit resolve_skill_dir's remote path
        ],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
    )
    # Dry-run path substitutes the stub — so this assertion is weak;
    # drop the --dry-run flag to exercise the real resolve path.
    # Regenerate the test post-Task 9 to target the real error message.
```

This test has a temporal dependency on Task 9 (the catalog flip). Until readme-maintainer's catalog entry is a remote URL, `resolve_skill_dir` for it returns a local path and the "not installed" branch isn't hit. Two options:

**Option A (preferred):** Move this test file to Task 9 (after the catalog flip) where it can assert against the real remote entry.

**Option B:** Use `--skill` with a made-up name that's not in the catalog at all — asserts the "not in recommended-skills.yaml" path instead of the "not installed" path. That's a weaker assertion but works today.

Pick Option A. Skip this test file in Task 8; add it in Task 9. Task 8's contribution is the scope_drafter update.

- [ ] **Step 3: Update `_load_skill_md` for remote sources**

Read `harness/lib/scope_drafter.py` lines 90-115 to see the current implementation. Replace `_load_skill_md` with:

```python
def _load_skill_md(
    *,
    catalog: dict[str, dict],
    catalog_root: Path,
    consumer_repo: Path,
) -> dict[str, Optional[str]]:
    """Load SKILL.md text for each catalog entry when available.

    - Local './…' source → read from <catalog_root>/<path>/SKILL.md.
    - Remote source, installed → read from
      <consumer_repo>/.claude/skills/<name>/SKILL.md.
    - Remote source, not yet installed → None (the scoping prompt
      tolerates null skill_md, falling back to the catalog entry's
      description).
    """
    out: dict[str, Optional[str]] = {}
    for name, entry in catalog.items():
        source = entry.get("source", "")
        if source.startswith("./"):
            skill_md = (catalog_root / source[2:] / "SKILL.md")
            if skill_md.is_file():
                out[name] = skill_md.read_text(encoding="utf-8")
            else:
                out[name] = None
            continue
        if source.startswith(("https://", "http://")):
            installed = consumer_repo / ".claude" / "skills" / name / "SKILL.md"
            out[name] = installed.read_text(encoding="utf-8") if installed.is_file() else None
            continue
        out[name] = None
    return out
```

Update the call site in `draft(...)` (currently around line 179). Change the caller from:

```python
skill_md = _load_skill_md(catalog, catalog_root)
```

to:

```python
skill_md = _load_skill_md(
    catalog=catalog,
    catalog_root=catalog_root,
    consumer_repo=consumer_repo,
)
```

Then add a `consumer_repo: Path` parameter to `draft(...)`'s signature, keyword-only. The full signature becomes:

```python
def draft(
    *,
    profile: RepoProfile,
    plugins: list[PluginEntry],
    user_answers: dict[str, str],
    catalog: dict[str, dict],
    executor: ScopeExecutor,
    catalog_root: Path,
    consumer_repo: Path,
) -> ScopeDraft: ...
```

Finally update `harness/scope/__main__.py`'s call to `scope_drafter.draft(...)` to pass `consumer_repo=repo`.

- [ ] **Step 4: Update tests for scope_drafter**

```bash
PYTHONPATH=. pytest tests/test_scope_drafter.py tests/test_scope*.py -v
```

Read test failures; patch tests that call `_load_skill_md` or `draft` directly to include the new `consumer_repo` argument.

For test files that use `_load_skill_md` directly, update call sites to the new keyword-arg signature. For `draft(...)` callers, pass `consumer_repo=tmp_path` or a made-up path — when no `.claude/skills/<name>/SKILL.md` exists there, remote entries end up with `None`, matching historic behavior for catalogs that only had local entries.

- [ ] **Step 5: Verify full suite passes**

```bash
PYTHONPATH=. pytest -q 2>&1 | tail -5
```

Expected: all prior tests + Task 2 (8) + Task 3 (3) + Task 4 (2) + Task 5 (4) + Task 6 (8) + Task 7 (3) = 128 passed (give or take, depending on `_seed_git_repo` consolidation in Task 4).

- [ ] **Step 6: Commit**

```bash
git add harness/lib/scope_drafter.py harness/scope/__main__.py \
        harness/onboard/__main__.py tests/
git commit -m "refactor(scope,onboard): remote sources resolve via catalog.resolve_skill_dir"
```

---

## Task 9: Extract readme-maintainer + flip catalog + prune in-tree

**Goal:** Move the skill out of the tokenman repo, flip `recommended-skills.yaml` to point at the new remote, delete the in-tree copy, and land the onboard "not installed" test that was deferred from Task 8.

**Files:**
- (External) Create GitHub repo `verky/readme-maintainer-skill`; seed with `skills/readme-maintainer/*`; tag `v0.1.0`.
- Modify: `recommended-skills.yaml`
- Delete: `skills/readme-maintainer/SKILL.md` (and the empty parent dir)
- Modify: `skills/README.md` — drop the "temporary in-tree" note.
- Modify: `.tokenman/CLAUDE.md` — drop the forbidden-list entry.
- Create: `tests/test_onboard_errors_when_skill_not_installed.py` (deferred from Task 8)

- [ ] **Step 1: Create the standalone repo (external, manual)**

On the host machine / your GitHub account:

```bash
cd /tmp
mkdir readme-maintainer-skill
cp /home/dev/projects/tokenman/skills/readme-maintainer/SKILL.md readme-maintainer-skill/
cd readme-maintainer-skill
git init -b main
git add .
git commit -m "feat: initial readme-maintainer skill v0.1.0"
git tag v0.1.0
# Create public repo on GitHub, then push:
gh repo create verky/readme-maintainer-skill --public --source=. --push
git push origin v0.1.0
```

- [ ] **Step 2: Verify the remote is clonable and the tag exists**

```bash
cd /tmp
rm -rf verify-clone
git clone --depth 1 --branch v0.1.0 \
    https://github.com/verky/readme-maintainer-skill.git verify-clone
ls verify-clone/SKILL.md
```

Expected: SKILL.md present.

- [ ] **Step 3: Flip the catalog entry**

Edit `recommended-skills.yaml`:

```yaml
readme-maintainer:
  source: https://github.com/verky/readme-maintainer-skill
  version: v0.1.0
  tier: starter
  blast_radius: low
  typical_tokens_per_run: 15000
  description: Keeps README aligned with actual repo contents.
  default_cadence: on-change
  evaluator_strictness: medium
```

Remove the `# TEMPORARY: …` and `# TODO(1.2b-split): …` comments.

- [ ] **Step 4: Delete the in-tree skill**

```bash
rm -rf skills/readme-maintainer/
```

- [ ] **Step 5: Update `skills/README.md`**

Read the current file; remove paragraphs that explain the temporary in-tree posture. If the `skills/` dir is now empty except for `README.md`, keep the README but shrink it to a short note: "This directory is kept empty — tokenman does not ship skills. See `recommended-skills.yaml`." Or remove the directory entirely.

Decision: keep `skills/README.md` as a tombstone (short, useful) rather than delete the directory. This avoids future contributors recreating it.

Proposed content for `skills/README.md`:

```markdown
# skills/

Intentionally empty. Tokenman does not ship skills; it curates them.
See `recommended-skills.yaml` for the catalog and
`docs/spec.md` §5 for the rationale.
```

- [ ] **Step 6: Update `.tokenman/CLAUDE.md`**

Read `.tokenman/CLAUDE.md`. Find the forbidden-list entry mentioning `skills/readme-maintainer/` and remove it (or update to reference only the catalog file, not the deleted directory).

- [ ] **Step 7: Update the project CLAUDE.md's "What NOT to do" list**

Read `/home/dev/projects/tokenman/CLAUDE.md`. The "Do not modify files in `harness/`, `scoping/`, `onboarding/`, `recommended-skills.yaml`, or `pricing.yaml` from a dogfood run" paragraph may reference the skills directory indirectly. Leave it unless it explicitly calls out `skills/readme-maintainer/`.

- [ ] **Step 8: Add the deferred onboard test**

Write `tests/test_onboard_errors_when_skill_not_installed.py`:

```python
"""onboard exits 2 when a remote catalog skill isn't installed yet."""
from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path


def test_onboard_errors_without_install(tmp_path):
    consumer = tmp_path / "consumer"
    (consumer / ".tokenman").mkdir(parents=True)
    (consumer / ".tokenman" / "tokenman.yaml").write_text(
        textwrap.dedent("""
            skills:
              - readme-maintainer
        """).lstrip()
    )

    env_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable, "-m", "harness.onboard",
            "--repo", str(consumer),
        ],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
    )

    assert result.returncode == 2, result.stderr
    combined = result.stdout + result.stderr
    assert "not installed" in combined
    assert "python -m harness.install" in combined
```

- [ ] **Step 9: Run the full suite**

```bash
PYTHONPATH=. pytest -q 2>&1 | tail -10
```

Expected: all tests pass, including the new `test_onboard_errors_without_install` and the dry-run happy path for onboard (which substitutes the stub fixture, not the real readme-maintainer).

If any tests fail because they depended on the in-tree readme-maintainer SKILL.md (e.g., scope-drafter tests using it as a local source), patch them to point at the stub-readme fixture under `tests/fixtures/skills/stub-readme/` instead.

- [ ] **Step 10: Commit**

```bash
git add recommended-skills.yaml skills/README.md .tokenman/CLAUDE.md \
        tests/test_onboard_errors_when_skill_not_installed.py
git rm -r skills/readme-maintainer/
git commit -m "feat(catalog): flip readme-maintainer to remote source; prune in-tree"
```

---

## Task 10: Live test + README + handoff refresh + PR

**Goal:** Final cleanup. Add the opt-in live install test, update README, refresh the handoff doc, run the full suite once more, and open the PR.

**Files:**
- Create: `tests/test_install_live.py`
- Modify: `README.md`
- Modify: `docs/next-session-prompt.md`

- [ ] **Step 1: Add the live install test**

Write `tests/test_install_live.py`:

```python
"""Opt-in live test — clones the real readme-maintainer repo.

Enable with TOKENMAN_LIVE=1. Skipped by default to keep the default
test run hermetic.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


pytestmark = pytest.mark.skipif(
    os.environ.get("TOKENMAN_LIVE") != "1",
    reason="opt-in live test; set TOKENMAN_LIVE=1 to run",
)


def test_install_readme_maintainer_live(tmp_path):
    consumer = tmp_path / "consumer"
    consumer.mkdir()

    env_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable, "-m", "harness.install",
            "--repo", str(consumer),
            "--skill", "readme-maintainer",
        ],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr

    target = consumer / ".claude" / "skills" / "readme-maintainer"
    assert (target / "SKILL.md").is_file()
    lock = json.loads((target / ".tokenman-skill-lock").read_text())
    assert lock["version"] == "v0.1.0"
    assert lock["source"] == "https://github.com/verky/readme-maintainer-skill"

    # Idempotent re-run.
    second = subprocess.run(
        [
            sys.executable, "-m", "harness.install",
            "--repo", str(consumer),
            "--skill", "readme-maintainer",
        ],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
        timeout=60,
    )
    assert second.returncode == 0, second.stderr
    assert "unchanged" in second.stdout
```

- [ ] **Step 2: Verify it's properly gated**

```bash
PYTHONPATH=. pytest tests/test_install_live.py -v
```

Expected: 1 skipped (message: "opt-in live test; set TOKENMAN_LIVE=1 to run").

```bash
TOKENMAN_LIVE=1 PYTHONPATH=. pytest tests/test_install_live.py -v
```

Expected: 1 passed (requires network + readme-maintainer-skill repo reachable).

- [ ] **Step 3: Update README**

Read `README.md`. In the Usage section (or wherever `python -m harness.onboard` was mentioned during Phase 1.4), update the consumer journey:

```markdown
1. `python -m harness.scope`    — draft .tokenman/initial-scope.md
2. `python -m harness.install`  — fetch skills into .claude/skills/
3. `python -m harness.onboard`  — run every enabled skill once, open PRs
```

Keep the one-liners short; more detail lives in `docs/spec.md`.

- [ ] **Step 4: Refresh `docs/next-session-prompt.md`**

Update the handoff to mark 1.5 as DONE, note Phase 1.6 (next) topic, and preserve the forward-facing carries that remain open (private-repo auth, --upgrade, parallel clones, pre-fetched SKILL.md). Mirror the shape of the existing handoff.

Key lines to update:
- Phase 1 decomposition status block — add `1.5 — skill install flow (DONE, <sha>)` and mark `1.6 — ... (NEXT)` with whatever the next unit is per spec.
- "What Phase 1.5 delivered" section summarizing the modules, CLIs, tests, and the readme-maintainer extraction.
- "Forward-facing notes from 1.5" preserving: private-repo auth deferred, --upgrade deferred, parallel clones deferred, pre-fetched SKILL.md deferred, GhPROpener still not end-to-end tested, workflow template `claude install` TODO still outstanding.

- [ ] **Step 5: Run the full suite one final time**

```bash
PYTHONPATH=. pytest -q
PYTHONPATH=. pytest -q --collect-only 2>&1 | tail -3
```

Expected: all tests pass; total count reflects new tests added across Tasks 2-10.

- [ ] **Step 6: Push the branch**

```bash
git push -u origin phase-1-5
```

- [ ] **Step 7: Open the PR**

```bash
gh pr create --title "Phase 1.5: skill install flow" --body "$(cat <<'EOF'
## Summary

- New `python -m harness.install`: fetches skills from `recommended-skills.yaml` into `.claude/skills/<name>/` at a pinned ref
- New `harness/lib/installer.py`: pure install logic (git clone/checkout/rev-parse, lock file, idempotency, --force)
- New `harness/lib/catalog.py`: consolidates `_tokenman_root / _load_catalog / _resolve_skill_dir` (previously duplicated across scope + onboard)
- `readme-maintainer` extracted to `verky/readme-maintainer-skill`, catalog flipped to the remote URL
- Scope + onboard updated to treat remote sources as installed-when-present; scope_drafter's `_load_skill_md` reads from `.claude/skills/` for remote entries

See `docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md` for the full design.

## Test plan

- [x] Unit tests for installer (local, remote, idempotency, drift, --force, errors, path: subdir)
- [x] CLI smoke tests for install (happy path, no-skills guard, idempotent re-run)
- [x] Onboard test covering "run install first" error on un-installed remote skill
- [x] Opt-in live test (`TOKENMAN_LIVE=1`) against real `readme-maintainer-skill` repo
- [x] Full pytest run green

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 8: Commit any final doc/README changes**

```bash
git add README.md docs/next-session-prompt.md tests/test_install_live.py
git commit -m "docs(phase-1-5): README + handoff refresh; opt-in live install test"
git push
```

- [ ] **Step 9: Verify PR CI + cleanup local worktree on merge**

After merge:

```bash
cd /home/dev/projects/tokenman
git pull origin main
git worktree remove ../tokenman-phase-1-5
git branch -D phase-1-5
```

---

## Post-merge verification checklist

Smoke-run the consumer journey against a scratch directory to confirm end-to-end:

```bash
cd /tmp && rm -rf smoke-consumer && mkdir smoke-consumer && cd smoke-consumer
git init && echo "# smoke" > README.md && git add . && git commit -m "init"
mkdir -p .tokenman
cat > .tokenman/tokenman.yaml <<YML
skills:
  - readme-maintainer
YML
cd /home/dev/projects/tokenman
PYTHONPATH=. python -m harness.install --repo /tmp/smoke-consumer
ls /tmp/smoke-consumer/.claude/skills/readme-maintainer/
cat /tmp/smoke-consumer/.claude/skills/readme-maintainer/.tokenman-skill-lock
```

Expected: SKILL.md + lock file present; lock's `source` matches the GitHub URL.

---

## Forward-facing carries (preserved for Phase 1.6+)

- Private-repo authentication (SSH / gh token)
- `--upgrade` flow (fetch newer tags than pinned)
- Parallel clones (sequential is fine for 3-5 skills)
- Pre-fetched SKILL.md into the catalog, so scope has skill_md for remote entries on a cold install
- `GhPROpener` still hasn't been exercised against real GitHub end-to-end
- Workflow template's `claude` install step still echoes TODO + `exit 1`
- `tests/fixtures/claude-captures/readme-maintainer.json` still synthetic
