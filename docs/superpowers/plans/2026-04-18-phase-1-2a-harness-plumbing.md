# Phase 1.2a Harness Plumbing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the tokenman harness runner, ledger append utility, and stub-skill infrastructure so that 1.2b's swap to real `claude -p` + real `gh pr create` touches only two boundary classes and nothing in the orchestrator.

**Architecture:** Four Python modules in `harness/lib/` (`ledger.py`, `runner.py`, `skill_executor.py`, `pr_opener.py`) each behind a narrow protocol. Tests exercise the full pipeline end-to-end against a deterministic bash-based stub skill at `tests/fixtures/skills/stub-readme/`. No `claude -p`, no `gh`, workflow template stays a Phase 0 stub.

**Tech Stack:** Python 3.10+, `jsonschema` (already a dev dep), `pytest` (already a dev dep), `subprocess` for the skill boundary. Bash for the stub skill's entrypoint. The canonical schema (`harness/lib/ledger.schema.json`) and three schema tests from Phase 1.1 stay unchanged.

**Parent spec:** `docs/superpowers/specs/2026-04-18-phase-1-2a-harness-plumbing-design.md`

---

## Setup: create a dedicated worktree

Phase 1.2a's implementation should happen on an isolated branch. The design doc and this plan already live on `main`; implementation lives on `phase-1-2a`.

- [ ] **Step 1: Verify working tree is clean on main**

Run: `git status`
Expected: `nothing to commit, working tree clean` on branch `main`.

- [ ] **Step 2: Create the worktree**

Run:
```bash
git worktree add ../tokenman-phase-1-2a -b phase-1-2a main
cd ../tokenman-phase-1-2a
```

Expected: new worktree directory exists, on fresh branch `phase-1-2a` based on `main`.

- [ ] **Step 3: Confirm design + plan are visible in the worktree**

Run:
```bash
ls docs/superpowers/specs/2026-04-18-phase-1-2a-harness-plumbing-design.md
ls docs/superpowers/plans/2026-04-18-phase-1-2a-harness-plumbing.md
```
Expected: both files exist (they were committed on main, so the worktree sees them).

From here on, all paths are relative to the worktree root and all commits land on branch `phase-1-2a`.

---

## Commit group 1: ledger append utility

Tasks 1–8. Ends with commit `feat(harness): add ledger append utility with invariant enforcement`.

### Task 1: Package scaffolding

**Files:**
- Create: `harness/__init__.py`
- Create: `harness/lib/__init__.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Create `harness/__init__.py`**

Write the file with exactly this content (a single empty line):

```python
```

- [ ] **Step 2: Create `harness/lib/__init__.py`**

Same — empty file:

```python
```

- [ ] **Step 3: Read existing `pyproject.toml`**

Run: `cat pyproject.toml`
Expected: Phase 1.1 content with `[project]`, `[project.optional-dependencies]`, `[tool.pytest.ini_options]`.

- [ ] **Step 4: Append the packages stanza to `pyproject.toml`**

Add this block at the end of `pyproject.toml`:

```toml

[tool.setuptools.packages.find]
where = ["."]
include = ["harness*"]
```

- [ ] **Step 5: Reinstall and verify imports work**

Run:
```bash
pip install -e '.[dev]' -q
python3 -c "import harness.lib; print('OK')"
```
Expected: `OK` printed; no ModuleNotFoundError.

- [ ] **Step 6: Verify the 1.1 schema test still passes**

Run: `pytest -q`
Expected: 3 tests pass (the existing schema-fixture tests from 1.1). No regressions.

---

### Task 2: Ledger schema loader + structural validator

**Files:**
- Create: `harness/lib/ledger.py`
- Create: `tests/test_ledger_append.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_ledger_append.py` with this initial content:

```python
"""Tests for harness.lib.ledger — schema validation, invariants, append."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from harness.lib import ledger


# A known-valid Phase 1 entry used as the base for variant tests below.
VALID_PR_OPENED: dict = {
    "run_id": "r-0001",
    "ts": "2026-04-18T12:00:00Z",
    "skill": "stub-readme",
    "status": "pr_opened",
    "pr": 1000,
    "generator": {
        "prompt_version": "stub-v1",
        "output_summary": "proposed 1 diff",
        "diff_lines": 3,
        "tokens": 0,
    },
    "evaluator": None,
    "duration_s": 0,
    "total_tokens": 0,
    "verdict": None,
    "verdict_note": None,
}


def test_validate_accepts_canonical_entry() -> None:
    ledger.validate(copy.deepcopy(VALID_PR_OPENED))


def test_validate_rejects_entry_missing_required_field() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    del bad["run_id"]
    with pytest.raises(ledger.LedgerInvariantError):
        ledger.validate(bad)


def test_validate_rejects_bad_run_id_pattern() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["run_id"] = "r-1"
    with pytest.raises(ledger.LedgerInvariantError):
        ledger.validate(bad)
```

- [ ] **Step 2: Run to verify it fails**

Run: `pytest tests/test_ledger_append.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'harness.lib.ledger'` or similar.

- [ ] **Step 3: Create `harness/lib/ledger.py`**

Write this file:

```python
"""Ledger append utility — validates entries against the schema and the
conditional invariants the schema cannot express, then appends JSONL lines.
See docs/spec.md §8.1 and
docs/superpowers/specs/2026-04-18-phase-1-2a-harness-plumbing-design.md.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

import jsonschema


_SCHEMA_PATH = Path(__file__).parent / "ledger.schema.json"


class LedgerInvariantError(ValueError):
    """Raised when a ledger entry violates schema or conditional invariants."""


@lru_cache(maxsize=1)
def _load_schema() -> dict:
    return json.loads(_SCHEMA_PATH.read_text())


def _schema_validator() -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(_load_schema())


def validate(entry: dict, *, previous: Optional[dict] = None) -> None:
    """Validate entry against the JSON schema.

    Conditional invariants (pr <-> status, generator null-ness, token sum,
    run_id monotonic, ts monotonic) are layered on in later tasks.
    """
    errors = list(_schema_validator().iter_errors(entry))
    if errors:
        msgs = "; ".join(f"{list(e.path)}: {e.message}" for e in errors)
        raise LedgerInvariantError(f"schema: {msgs}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_ledger_append.py -v`
Expected: 3 tests PASS.

---

### Task 3: `last_run_id` helper

**Files:**
- Modify: `harness/lib/ledger.py`
- Modify: `tests/test_ledger_append.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_ledger_append.py`:

```python


def test_last_run_id_missing_file(tmp_path: Path) -> None:
    assert ledger.last_run_id(tmp_path / "nope.jsonl") is None


def test_last_run_id_empty_file(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    p.write_text("")
    assert ledger.last_run_id(p) is None


def test_last_run_id_blank_lines_only(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    p.write_text("\n\n   \n")
    assert ledger.last_run_id(p) is None


def test_last_run_id_returns_integer_portion(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    entry = copy.deepcopy(VALID_PR_OPENED)
    entry["run_id"] = "r-0042"
    p.write_text(json.dumps(entry) + "\n")
    assert ledger.last_run_id(p) == 42


def test_last_run_id_uses_last_non_blank_line(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    e1 = copy.deepcopy(VALID_PR_OPENED)
    e1["run_id"] = "r-0001"
    e2 = copy.deepcopy(VALID_PR_OPENED)
    e2["run_id"] = "r-0002"
    e2["ts"] = "2026-04-18T12:00:01Z"
    e2["pr"] = 1001
    p.write_text(json.dumps(e1) + "\n" + json.dumps(e2) + "\n\n")
    assert ledger.last_run_id(p) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_ledger_append.py -v -k last_run_id`
Expected: FAIL — `AttributeError: module 'harness.lib.ledger' has no attribute 'last_run_id'`.

- [ ] **Step 3: Implement**

Append to `harness/lib/ledger.py`:

```python


def _last_entry(ledger_path: Path) -> Optional[dict]:
    """Return the last non-blank JSON line as a dict, or None."""
    if not ledger_path.is_file():
        return None
    lines = [ln for ln in ledger_path.read_text().splitlines() if ln.strip()]
    if not lines:
        return None
    return json.loads(lines[-1])


def last_run_id(ledger_path: Path) -> Optional[int]:
    """Return the integer portion of the last entry's run_id, or None if the
    ledger is missing / empty / all-blank.
    """
    last = _last_entry(ledger_path)
    if last is None:
        return None
    return int(last["run_id"].split("-")[1])
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_ledger_append.py -v`
Expected: 8 tests PASS (3 from Task 2 + 5 new).

---

### Task 4: `append` — structural path only

**Files:**
- Modify: `harness/lib/ledger.py`
- Modify: `tests/test_ledger_append.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_ledger_append.py`:

```python


def test_append_to_missing_ledger_creates_file(tmp_path: Path) -> None:
    p = tmp_path / "sub" / "ledger.jsonl"
    entry = copy.deepcopy(VALID_PR_OPENED)
    ledger.append(p, entry)
    assert p.is_file()
    lines = p.read_text().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == entry


def test_append_appends_without_clobber(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    e1 = copy.deepcopy(VALID_PR_OPENED)
    e1["run_id"] = "r-0001"
    e2 = copy.deepcopy(VALID_PR_OPENED)
    e2["run_id"] = "r-0002"
    e2["ts"] = "2026-04-18T12:00:01Z"
    e2["pr"] = 1001
    ledger.append(p, e1)
    ledger.append(p, e2)
    lines = p.read_text().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["run_id"] == "r-0001"
    assert json.loads(lines[1])["run_id"] == "r-0002"


def test_append_leaves_file_unchanged_on_validation_failure(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    e1 = copy.deepcopy(VALID_PR_OPENED)
    ledger.append(p, e1)
    before = p.read_text()
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["run_id"] = "not-a-run-id"
    with pytest.raises(ledger.LedgerInvariantError):
        ledger.append(p, bad)
    assert p.read_text() == before
```

- [ ] **Step 2: Run to verify they fail**

Run: `pytest tests/test_ledger_append.py -v -k append`
Expected: FAIL — `AttributeError: module 'harness.lib.ledger' has no attribute 'append'`.

- [ ] **Step 3: Implement `append`**

Append to `harness/lib/ledger.py`:

```python


def append(ledger_path: Path, entry: dict) -> None:
    """Validate then append entry as a compact JSON line.

    Creates parent directories and the file if missing. On validation
    failure the file is left unchanged.
    """
    previous = _last_entry(ledger_path)
    validate(entry, previous=previous)

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, separators=(",", ":"))
    with ledger_path.open("a") as f:
        f.write(line + "\n")
        f.flush()
```

Note: at this point `validate` still accepts the `previous=` kwarg but doesn't use it — that lands in Task 8.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_ledger_append.py -v`
Expected: 11 tests PASS (8 prior + 3 new).

---

### Task 5: Invariant 1 — `pr` ↔ `pr_opened`

**Files:**
- Modify: `harness/lib/ledger.py`
- Modify: `tests/test_ledger_append.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_ledger_append.py`:

```python


def test_invariant_pr_non_null_without_pr_opened_rejected() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "no_change"
    bad["generator"] = None  # skip status needs null generator — keeps test focused on pr
    bad["pr"] = 42
    with pytest.raises(ledger.LedgerInvariantError, match="pr"):
        ledger.validate(bad)


def test_invariant_pr_null_with_pr_opened_rejected() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["pr"] = None
    with pytest.raises(ledger.LedgerInvariantError, match="pr"):
        ledger.validate(bad)
```

Note: the first test uses `status="no_change"` with `generator=None`. Once Task 6 lands (generator null-ness invariant), that entry would fail invariant-2 before reaching invariant-1. To keep tests isolated, we'll adjust this test in Task 6 to use a status that still produces an invariant-1 violation first. For now, the invariant-1 check catches it.

- [ ] **Step 2: Run to verify they fail**

Run: `pytest tests/test_ledger_append.py -v -k invariant_pr`
Expected: FAIL — both tests see no error raised.

- [ ] **Step 3: Implement invariant 1 in `validate`**

Replace the body of `validate` in `harness/lib/ledger.py` with:

```python
def validate(entry: dict, *, previous: Optional[dict] = None) -> None:
    """Validate entry against schema + conditional invariants.

    Invariant 1: pr is non-null iff status == 'pr_opened'.
    """
    errors = list(_schema_validator().iter_errors(entry))
    if errors:
        msgs = "; ".join(f"{list(e.path)}: {e.message}" for e in errors)
        raise LedgerInvariantError(f"schema: {msgs}")

    status = entry["status"]
    pr = entry.get("pr")
    if status == "pr_opened" and pr is None:
        raise LedgerInvariantError("pr must be non-null when status == 'pr_opened'")
    if status != "pr_opened" and pr is not None:
        raise LedgerInvariantError(
            f"pr must be null when status == {status!r} (got {pr!r})"
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_ledger_append.py -v`
Expected: 13 tests PASS (11 prior + 2 new).

---

### Task 6: Invariant 2 — generator null-ness by status

**Files:**
- Modify: `harness/lib/ledger.py`
- Modify: `tests/test_ledger_append.py`

- [ ] **Step 1: Update Task 5's first test to isolate invariant-1**

In `tests/test_ledger_append.py`, modify `test_invariant_pr_non_null_without_pr_opened_rejected` to use a status where the generator null-ness invariant would *not* also apply. Since both `error` and `pr_opened` permit a populated generator, use `error`:

Replace:
```python
def test_invariant_pr_non_null_without_pr_opened_rejected() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "no_change"
    bad["generator"] = None  # skip status needs null generator — keeps test focused on pr
    bad["pr"] = 42
    with pytest.raises(ledger.LedgerInvariantError, match="pr"):
        ledger.validate(bad)
```

with:
```python
def test_invariant_pr_non_null_without_pr_opened_rejected() -> None:
    # Use status='error' so the generator null-ness invariant (Task 6) does
    # not also fire; this test isolates invariant 1.
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "error"
    bad["pr"] = 42
    with pytest.raises(ledger.LedgerInvariantError, match="pr"):
        ledger.validate(bad)
```

- [ ] **Step 2: Add failing tests for invariant 2**

Append to `tests/test_ledger_append.py`:

```python


def test_invariant_generator_must_be_null_on_skipped_status() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "skipped_cooldown"
    bad["pr"] = None
    # generator still populated → violation
    with pytest.raises(ledger.LedgerInvariantError, match="generator"):
        ledger.validate(bad)


def test_invariant_generator_must_be_populated_on_no_change() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "no_change"
    bad["pr"] = None
    bad["generator"] = None
    with pytest.raises(ledger.LedgerInvariantError, match="generator"):
        ledger.validate(bad)


def test_invariant_generator_null_on_error_accepted() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "error"
    ok["pr"] = None
    ok["generator"] = None
    ok["total_tokens"] = 0
    ledger.validate(ok)  # must not raise


def test_invariant_generator_populated_on_error_accepted() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "error"
    ok["pr"] = None
    # generator stays populated; total_tokens already matches 0
    ledger.validate(ok)  # must not raise


def test_invariant_generator_null_on_skipped_without_pr_accepted() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "skipped_pause"
    ok["pr"] = None
    ok["generator"] = None
    ok["total_tokens"] = 0
    ledger.validate(ok)  # must not raise
```

- [ ] **Step 3: Run to verify they fail**

Run: `pytest tests/test_ledger_append.py -v -k invariant_generator`
Expected: the two "must raise" tests FAIL (no error raised); the three "accepted" tests pass or fail depending on prior invariants. The must-raise ones are the target.

- [ ] **Step 4: Implement invariant 2**

Add to `validate` in `harness/lib/ledger.py`, after the pr check block:

```python

    gen = entry.get("generator")
    if status.startswith("skipped_"):
        if gen is not None:
            raise LedgerInvariantError(
                f"generator must be null when status == {status!r}"
            )
    elif status == "error":
        # Either null (pre-generator failure) or populated (generator ran
        # then a later stage erred) is acceptable.
        pass
    else:
        # pr_opened, no_change, aborted_gate, aborted_evaluator
        if gen is None:
            raise LedgerInvariantError(
                f"generator must be populated when status == {status!r}"
            )
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_ledger_append.py -v`
Expected: 18 tests PASS (13 prior + 5 new).

---

### Task 7: Invariant 3 — `total_tokens` sum

**Files:**
- Modify: `harness/lib/ledger.py`
- Modify: `tests/test_ledger_append.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_ledger_append.py`:

```python


def test_invariant_total_tokens_mismatch_rejected() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["generator"]["tokens"] = 100
    bad["total_tokens"] = 99  # off-by-one
    with pytest.raises(ledger.LedgerInvariantError, match="total_tokens"):
        ledger.validate(bad)


def test_invariant_total_tokens_match_accepted() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["generator"]["tokens"] = 100
    ok["total_tokens"] = 100
    ledger.validate(ok)


def test_invariant_total_tokens_sums_generator_and_evaluator() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["generator"]["tokens"] = 100
    ok["evaluator"] = {
        "prompt_version": "v1",
        "verdict": "approve",
        "reason": "fine",
        "tokens": 25,
    }
    ok["total_tokens"] = 125
    ledger.validate(ok)


def test_invariant_total_tokens_zero_when_both_null() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "skipped_pause"
    ok["pr"] = None
    ok["generator"] = None
    ok["evaluator"] = None
    ok["total_tokens"] = 0
    ledger.validate(ok)
```

- [ ] **Step 2: Run to verify they fail**

Run: `pytest tests/test_ledger_append.py -v -k total_tokens`
Expected: the "_mismatch_rejected" test FAILs (no error raised); the others pass already.

- [ ] **Step 3: Implement invariant 3**

Add to the end of `validate` in `harness/lib/ledger.py`:

```python

    gen_tokens = gen["tokens"] if gen else 0
    ev = entry.get("evaluator")
    ev_tokens = ev["tokens"] if ev else 0
    expected = gen_tokens + ev_tokens
    if entry["total_tokens"] != expected:
        raise LedgerInvariantError(
            f"total_tokens ({entry['total_tokens']}) != "
            f"generator.tokens ({gen_tokens}) + evaluator.tokens ({ev_tokens})"
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_ledger_append.py -v`
Expected: 22 tests PASS (18 prior + 4 new).

---

### Task 8: Invariants 4 & 5 — `run_id` and `ts` monotonicity

**Files:**
- Modify: `harness/lib/ledger.py`
- Modify: `tests/test_ledger_append.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_ledger_append.py`:

```python


def _seeded_ledger(tmp_path: Path, last_run_id: str, last_ts: str) -> Path:
    p = tmp_path / "ledger.jsonl"
    entry = copy.deepcopy(VALID_PR_OPENED)
    entry["run_id"] = last_run_id
    entry["ts"] = last_ts
    ledger.append(p, entry)
    return p


def test_invariant_run_id_must_strictly_increase(tmp_path: Path) -> None:
    p = _seeded_ledger(tmp_path, "r-0005", "2026-04-18T12:00:00Z")

    same = copy.deepcopy(VALID_PR_OPENED)
    same["run_id"] = "r-0005"
    same["ts"] = "2026-04-18T12:00:05Z"
    same["pr"] = 1001
    with pytest.raises(ledger.LedgerInvariantError, match="run_id"):
        ledger.append(p, same)

    older = copy.deepcopy(VALID_PR_OPENED)
    older["run_id"] = "r-0004"
    older["ts"] = "2026-04-18T12:00:05Z"
    older["pr"] = 1002
    with pytest.raises(ledger.LedgerInvariantError, match="run_id"):
        ledger.append(p, older)


def test_invariant_run_id_increment_accepted(tmp_path: Path) -> None:
    p = _seeded_ledger(tmp_path, "r-0005", "2026-04-18T12:00:00Z")
    nxt = copy.deepcopy(VALID_PR_OPENED)
    nxt["run_id"] = "r-0006"
    nxt["ts"] = "2026-04-18T12:00:05Z"
    nxt["pr"] = 1001
    ledger.append(p, nxt)
    assert ledger.last_run_id(p) == 6


def test_invariant_ts_must_not_go_backward(tmp_path: Path) -> None:
    p = _seeded_ledger(tmp_path, "r-0005", "2026-04-18T12:00:00Z")
    backward = copy.deepcopy(VALID_PR_OPENED)
    backward["run_id"] = "r-0006"
    backward["ts"] = "2026-04-18T11:59:59Z"
    backward["pr"] = 1001
    with pytest.raises(ledger.LedgerInvariantError, match="ts"):
        ledger.append(p, backward)


def test_invariant_ts_equal_to_previous_accepted(tmp_path: Path) -> None:
    # ts monotonicity is non-strict: equality is allowed.
    p = _seeded_ledger(tmp_path, "r-0005", "2026-04-18T12:00:00Z")
    same_ts = copy.deepcopy(VALID_PR_OPENED)
    same_ts["run_id"] = "r-0006"
    same_ts["ts"] = "2026-04-18T12:00:00Z"
    same_ts["pr"] = 1001
    ledger.append(p, same_ts)
```

- [ ] **Step 2: Run to verify they fail**

Run: `pytest tests/test_ledger_append.py -v -k "run_id_must or ts_must"`
Expected: the two must-raise tests FAIL (no error raised).

- [ ] **Step 3: Implement invariants 4 and 5**

Add to the end of `validate` in `harness/lib/ledger.py`:

```python

    if previous is not None:
        prev_run_n = int(previous["run_id"].split("-")[1])
        new_run_n = int(entry["run_id"].split("-")[1])
        if new_run_n <= prev_run_n:
            raise LedgerInvariantError(
                f"run_id {entry['run_id']!r} not strictly greater than "
                f"previous {previous['run_id']!r}"
            )
        if entry["ts"] < previous["ts"]:
            raise LedgerInvariantError(
                f"ts {entry['ts']!r} is before previous ts {previous['ts']!r}"
            )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_ledger_append.py -v`
Expected: 26 tests PASS (22 prior + 4 new).

- [ ] **Step 5: Commit (Commit 1)**

Run:
```bash
git add harness/__init__.py harness/lib/__init__.py harness/lib/ledger.py \
        pyproject.toml tests/test_ledger_append.py
git commit -m "$(cat <<'EOF'
feat(harness): add ledger append utility with invariant enforcement

Introduces harness.lib.ledger with validate(), append(), and
last_run_id(). Enforces five conditional invariants on top of the
Phase 1.1 JSON schema: pr <-> pr_opened, generator null-ness by
status, total_tokens sum, run_id monotonicity, ts monotonicity.
Packages scaffolding (harness/__init__.py, harness/lib/__init__.py,
pyproject.toml packages stanza) makes harness.lib importable.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git status
```
Expected: commit created, working tree clean.

---

## Commit group 2: skill executor and PR opener abstractions

Tasks 9–12. Ends with commit `feat(harness): add skill executor and PR opener abstractions`.

### Task 9: `pr_opener.py`

**Files:**
- Create: `harness/lib/pr_opener.py`
- Create: `tests/test_pr_opener.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_pr_opener.py`:

```python
"""Tests for harness.lib.pr_opener."""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.pr_opener import FakePROpener


def test_fake_pr_opener_returns_incrementing_integers() -> None:
    op = FakePROpener()
    n1 = op.open(title="t1", body="b1", branch="br1", diff="d1")
    n2 = op.open(title="t2", body="b2", branch="br2", diff="d2")
    n3 = op.open(title="t3", body="b3", branch="br3", diff="d3")
    assert n2 == n1 + 1
    assert n3 == n2 + 1


def test_fake_pr_opener_custom_start() -> None:
    op = FakePROpener(start=500)
    n1 = op.open(title="t", body="b", branch="br", diff="d")
    assert n1 == 500


def test_fake_pr_opener_records_calls() -> None:
    op = FakePROpener()
    op.open(title="hello", body="world", branch="tokenman/x/r-0001", diff="--- a\n+++ b\n")
    assert len(op.calls) == 1
    call = op.calls[0]
    assert call["title"] == "hello"
    assert call["body"] == "world"
    assert call["branch"] == "tokenman/x/r-0001"
    assert call["diff"] == "--- a\n+++ b\n"


def test_fake_pr_opener_writes_sink_files(tmp_path: Path) -> None:
    sink = tmp_path / "prs"
    op = FakePROpener(sink_dir=sink, start=2000)
    n = op.open(title="t", body="b", branch="br", diff="d")
    assert n == 2000
    written = sink / "pr-2000.json"
    assert written.is_file()
    data = json.loads(written.read_text())
    assert data["pr"] == 2000
    assert data["title"] == "t"
```

- [ ] **Step 2: Run to verify they fail**

Run: `pytest tests/test_pr_opener.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'harness.lib.pr_opener'`.

- [ ] **Step 3: Implement**

Create `harness/lib/pr_opener.py`:

```python
"""PR opener boundary for the harness runner.

Phase 1.2a ships a FakePROpener used in tests. Phase 1.2b adds a
GhPROpener that calls `gh pr create` against a real remote.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Protocol


class PROpener(Protocol):
    """Opens a PR and returns its number."""

    def open(self, *, title: str, body: str, branch: str, diff: str) -> int: ...


class FakePROpener:
    """In-process fake. Returns a monotonically incrementing integer.

    When sink_dir is supplied, each call is also persisted as
    pr-<n>.json for test inspection.
    """

    def __init__(
        self,
        sink_dir: Optional[Path] = None,
        start: int = 1000,
    ) -> None:
        self._next = start
        self._sink_dir = sink_dir
        self.calls: list[dict] = []

    def open(self, *, title: str, body: str, branch: str, diff: str) -> int:
        n = self._next
        self._next += 1
        record = {
            "pr": n,
            "title": title,
            "body": body,
            "branch": branch,
            "diff": diff,
        }
        self.calls.append(record)
        if self._sink_dir is not None:
            self._sink_dir.mkdir(parents=True, exist_ok=True)
            (self._sink_dir / f"pr-{n}.json").write_text(
                json.dumps(record, indent=2)
            )
        return n
```

- [ ] **Step 4: Run to verify tests pass**

Run: `pytest tests/test_pr_opener.py -v`
Expected: 4 tests PASS.

---

### Task 10: `skill_executor.py`

**Files:**
- Create: `harness/lib/skill_executor.py`

Tests for `StubSkillExecutor` come in Task 12 (after the stub skill exists).

- [ ] **Step 1: Implement**

Create `harness/lib/skill_executor.py`:

```python
"""Skill executor boundary for the harness runner.

Phase 1.2a ships StubSkillExecutor for subprocess-driven tests.
Phase 3+ adds ClaudeSkillExecutor that invokes `claude -p`.
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Protocol


@dataclass
class ExecutionResult:
    exit_code: int
    stdout: str
    stderr: str
    proposed_diff_path: Optional[Path]
    proposed_md_path: Optional[Path]
    summary: str


class SkillExecutor(Protocol):
    """Invoke a skill against a repo and produce an ExecutionResult."""

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult: ...


class StubSkillExecutor:
    """Runs `stub.sh` inside skill_dir as a subprocess.

    The stub writes proposed.diff / proposed.md (if any) into the
    scratch directory passed as its first positional argument. stdout
    and stderr are captured in full. Not used outside of tests.
    """

    def __init__(self, extra_env: Optional[dict[str, str]] = None) -> None:
        self._extra_env = dict(extra_env) if extra_env else {}

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult:
        entrypoint = skill_dir / "stub.sh"
        env = {**os.environ, **self._extra_env}
        proc = subprocess.run(
            ["bash", str(entrypoint), str(scratch_dir)],
            cwd=str(repo_dir),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        diff = scratch_dir / "proposed.diff"
        md = scratch_dir / "proposed.md"
        first_stdout_line = next(
            (ln for ln in proc.stdout.splitlines() if ln.strip()),
            f"{skill_dir.name}: exit {proc.returncode}",
        )
        return ExecutionResult(
            exit_code=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            proposed_diff_path=diff if diff.is_file() else None,
            proposed_md_path=md if md.is_file() else None,
            summary=first_stdout_line,
        )
```

- [ ] **Step 2: Verify imports work**

Run:
```bash
python3 -c "from harness.lib.skill_executor import ExecutionResult, SkillExecutor, StubSkillExecutor; print('OK')"
```
Expected: `OK`.

- [ ] **Step 3: Confirm no regressions**

Run: `pytest -q`
Expected: 30 tests PASS (3 schema from 1.1 + 26 ledger + 4 pr_opener). 0 failures.

---

### Task 11: Stub skill fixture

**Files:**
- Create: `tests/fixtures/skills/README.md`
- Create: `tests/fixtures/skills/stub-readme/SKILL.md`
- Create: `tests/fixtures/skills/stub-readme/stub.sh`

- [ ] **Step 1: Create `tests/fixtures/skills/README.md`**

```markdown
# Skill test fixtures

Stub skills used by `tests/test_skill_executor.py` and
`tests/test_runner.py` to exercise the harness runner without invoking
`claude -p`. These are deliberately minimal — a fake SKILL.md plus a
bash entrypoint (`stub.sh`) that writes canned files based on the
`STUB_MODE` env var.

Not to be confused with `tests/fixtures/tiny-*-repo/`, which hosts
synthetic *consumer* repositories for harness integration tests.

## Adding a new stub

Each stub lives under `tests/fixtures/skills/<name>/` and must contain:

- `SKILL.md` — human-readable notes; the runner does not parse it.
- `stub.sh` — executable bash entrypoint that takes one argument
  (a scratch directory) and writes `proposed.diff` / `proposed.md` into
  it, or exits non-zero.

All stub scripts must pass `shellcheck`.
```

- [ ] **Step 2: Create `tests/fixtures/skills/stub-readme/SKILL.md`**

```markdown
# stub-readme

Stub skill used by the tokenman harness test suite. Does **not** invoke
Claude. The runner in Phase 1.2a does not parse this file — it is
documentation only.

## Modes

Selected via the `STUB_MODE` env var passed by `StubSkillExecutor`:

| Mode | Effect |
|---|---|
| `no_change` (default) | Print a summary, write nothing. |
| `propose_diff` | Print a summary, write canned `proposed.diff` + `proposed.md`. |
| `crash` | Print to stderr, exit 2. |

Any other `STUB_MODE` value exits 3.
```

- [ ] **Step 3: Create `tests/fixtures/skills/stub-readme/stub.sh`**

```bash
#!/usr/bin/env bash
# Stub skill entrypoint. Reads STUB_MODE env var, writes canned output
# into the scratch dir passed as $1. See SKILL.md in this directory.
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "stub-readme: missing scratch-dir arg" >&2
    exit 64
fi

SCRATCH="$1"
MODE="${STUB_MODE:-no_change}"

case "$MODE" in
  no_change)
    echo "stub-readme: no changes needed"
    ;;
  propose_diff)
    cat > "$SCRATCH/proposed.diff" <<'DIFF'
--- a/README.md
+++ b/README.md
@@ -1,2 +1,3 @@
 # Tiny Python Repo
+
+Stub-readme added this line.
DIFF
    cat > "$SCRATCH/proposed.md" <<'MD'
Proposed adding a blank line and a sentence under the README heading.
MD
    echo "stub-readme: proposed 1 diff"
    ;;
  crash)
    echo "stub-readme: crashing on purpose" >&2
    exit 2
    ;;
  *)
    echo "stub-readme: unknown STUB_MODE ${MODE@Q}" >&2
    exit 3
    ;;
esac
```

- [ ] **Step 4: Make the stub executable and shellcheck it**

Run:
```bash
chmod +x tests/fixtures/skills/stub-readme/stub.sh
shellcheck tests/fixtures/skills/stub-readme/stub.sh
```
Expected: no shellcheck output (no findings); exit 0.

- [ ] **Step 5: Smoke-run the stub**

Run:
```bash
tmp=$(mktemp -d)
bash tests/fixtures/skills/stub-readme/stub.sh "$tmp"
echo "---"
STUB_MODE=propose_diff bash tests/fixtures/skills/stub-readme/stub.sh "$tmp"
ls "$tmp"
```
Expected: "stub-readme: no changes needed" then "stub-readme: proposed 1 diff"; `$tmp` contains `proposed.diff` and `proposed.md` after the second run.

---

### Task 12: Integration test for `StubSkillExecutor`

**Files:**
- Create: `tests/test_skill_executor.py`

- [ ] **Step 1: Write the tests**

Create `tests/test_skill_executor.py`:

```python
"""Integration tests for harness.lib.skill_executor.StubSkillExecutor."""
from __future__ import annotations

from pathlib import Path

import pytest

from harness.lib.skill_executor import StubSkillExecutor


REPO_ROOT = Path(__file__).parent.parent
STUB_SKILL_DIR = REPO_ROOT / "tests" / "fixtures" / "skills" / "stub-readme"
FIXTURE_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def test_stub_no_change_mode(tmp_path: Path) -> None:
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    result = executor.execute(STUB_SKILL_DIR, FIXTURE_REPO, tmp_path)
    assert result.exit_code == 0
    assert result.proposed_diff_path is None
    assert result.proposed_md_path is None
    assert "no changes needed" in result.stdout
    assert result.summary.startswith("stub-readme: no changes")


def test_stub_propose_diff_mode(tmp_path: Path) -> None:
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
    result = executor.execute(STUB_SKILL_DIR, FIXTURE_REPO, tmp_path)
    assert result.exit_code == 0
    assert result.proposed_diff_path == tmp_path / "proposed.diff"
    assert result.proposed_md_path == tmp_path / "proposed.md"
    assert result.proposed_diff_path.is_file()
    assert result.proposed_md_path.is_file()
    assert "proposed 1 diff" in result.stdout
    assert "Stub-readme added this line" in result.proposed_diff_path.read_text()


def test_stub_crash_mode(tmp_path: Path) -> None:
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "crash"})
    result = executor.execute(STUB_SKILL_DIR, FIXTURE_REPO, tmp_path)
    assert result.exit_code == 2
    assert "crashing on purpose" in result.stderr
    assert result.proposed_diff_path is None


def test_stub_default_mode_is_no_change(tmp_path: Path) -> None:
    # No STUB_MODE provided → stub.sh defaults to no_change.
    executor = StubSkillExecutor()
    result = executor.execute(STUB_SKILL_DIR, FIXTURE_REPO, tmp_path)
    assert result.exit_code == 0
    assert result.proposed_diff_path is None
```

- [ ] **Step 2: Run the tests**

Run: `pytest tests/test_skill_executor.py -v`
Expected: 4 tests PASS.

- [ ] **Step 3: Run the full test suite for regressions**

Run: `pytest -q`
Expected: 34 tests PASS (3 schema + 26 ledger + 4 pr_opener + 4 skill_executor tests from this task). 0 failures.

- [ ] **Step 4: Commit (Commit 2)**

Run:
```bash
git add harness/lib/pr_opener.py harness/lib/skill_executor.py \
        tests/fixtures/skills/ tests/test_pr_opener.py \
        tests/test_skill_executor.py
git commit -m "$(cat <<'EOF'
feat(harness): add skill executor and PR opener abstractions

Introduces harness.lib.skill_executor (ExecutionResult,
SkillExecutor Protocol, StubSkillExecutor) and harness.lib.pr_opener
(PROpener Protocol, FakePROpener). Adds the stub-readme fixture at
tests/fixtures/skills/stub-readme/ with a bash entrypoint covering
no_change, propose_diff, and crash modes. Tests confirm the
subprocess boundary and the fake PR opener's counter + sink behavior.

Phase 1.2b will replace StubSkillExecutor with ClaudeSkillExecutor
(calls claude -p) and FakePROpener with GhPROpener (calls gh pr
create). The Protocol-shaped interface makes both swap-ins local.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git status
```
Expected: commit created, working tree clean.

---

## Commit group 3: the runner

Tasks 13–18. Ends with commit `feat(harness): add runner that orchestrates a single-skill run`.

### Task 13: Runner helpers (`_count_diff_lines`, `_format_run_id`, `_iso_utc`)

**Files:**
- Create: `harness/lib/runner.py`
- Create: `tests/test_runner.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_runner.py`:

```python
"""Tests for harness.lib.runner."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from harness.lib import runner


# --- helpers --------------------------------------------------------


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
    # '+++' and '---' headers are ignored; hunk header has no +/-; three
    # content lines have +/-: "+", "+new line", "-old line".
    assert runner._count_diff_lines(diff) == 3


def test_count_diff_lines_empty() -> None:
    assert runner._count_diff_lines("") == 0


def test_count_diff_lines_no_changes() -> None:
    diff = "--- a/x\n+++ b/x\n@@ -1,1 +1,1 @@\n only context\n"
    assert runner._count_diff_lines(diff) == 0


def test_format_run_id_pads_to_four() -> None:
    assert runner._format_run_id(1) == "r-0001"
    assert runner._format_run_id(42) == "r-0042"
    assert runner._format_run_id(9999) == "r-9999"


def test_iso_utc_seconds_precision_z_suffix() -> None:
    dt = datetime(2026, 4, 18, 12, 0, 0, tzinfo=timezone.utc)
    assert runner._iso_utc(dt) == "2026-04-18T12:00:00Z"


def test_iso_utc_converts_non_utc() -> None:
    from datetime import timedelta, timezone as tz
    dt = datetime(2026, 4, 18, 14, 0, 0, tzinfo=tz(timedelta(hours=2)))
    assert runner._iso_utc(dt) == "2026-04-18T12:00:00Z"
```

- [ ] **Step 2: Run to verify they fail**

Run: `pytest tests/test_runner.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'harness.lib.runner'`.

- [ ] **Step 3: Create `harness/lib/runner.py` with the helpers only**

```python
"""Tokenman harness runner — orchestrates a single skill run.

Phase 1.2a: ledger-aware, subprocess-driven, PR opener injected. No
`claude -p`, no `gh pr create`; 1.2b swaps in real implementations.
See docs/superpowers/specs/2026-04-18-phase-1-2a-harness-plumbing-design.md.
"""
from __future__ import annotations

from datetime import datetime, timezone


def _count_diff_lines(diff_text: str) -> int:
    """Count lines starting with '+' or '-' but excluding file-header
    lines ('+++ ', '+++\\t', '--- ', '---\\t').
    """
    count = 0
    for line in diff_text.splitlines():
        if line.startswith(("+++ ", "+++\t", "--- ", "---\t")):
            continue
        if line.startswith(("+", "-")):
            count += 1
    return count


def _format_run_id(n: int) -> str:
    """Zero-pad a run number to the schema's canonical r-NNNN shape."""
    return f"r-{n:04d}"


def _iso_utc(dt: datetime) -> str:
    """Render as ISO 8601 UTC with seconds precision and Z suffix."""
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_runner.py -v`
Expected: 6 tests PASS.

---

### Task 14: `run_skill` — `propose_diff` happy path

**Files:**
- Modify: `harness/lib/runner.py`
- Modify: `tests/test_runner.py`

- [ ] **Step 1: Add a helper + failing test**

Append to `tests/test_runner.py`:

```python


# --- run_skill integration -----------------------------------------

import json
import shutil

import pytest

from harness.lib import ledger
from harness.lib.pr_opener import FakePROpener
from harness.lib.skill_executor import StubSkillExecutor


REPO_ROOT = Path(__file__).parent.parent
STUB_SKILL_DIR = REPO_ROOT / "tests" / "fixtures" / "skills" / "stub-readme"
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def _prepare_repo_copy(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Return (repo_dir, ledger_path, runs_dir). Repo is a fresh copy of
    the fixture so fixture files stay pristine.
    """
    repo_dir = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo_dir)
    tokenman_dir = repo_dir / ".tokenman"
    tokenman_dir.mkdir(exist_ok=True)
    ledger_path = tokenman_dir / "ledger.jsonl"
    runs_dir = tokenman_dir / "runs"
    return repo_dir, ledger_path, runs_dir


def _fixed_now() -> datetime:
    return datetime(2026, 4, 18, 12, 0, 0, tzinfo=timezone.utc)


def test_run_skill_propose_diff_opens_pr(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
    pr_opener = FakePROpener(sink_dir=tmp_path / "prs", start=1000)

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name="stub-readme",
        now=_fixed_now,
    )

    # Returned entry
    assert entry["run_id"] == "r-0001"
    assert entry["status"] == "pr_opened"
    assert entry["pr"] == 1000
    assert entry["generator"]["diff_lines"] == 3
    assert entry["generator"]["prompt_version"] == "stub-v1"
    assert entry["evaluator"] is None
    assert entry["total_tokens"] == 0

    # Ledger file
    lines = ledger_path.read_text().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == entry

    # Artifact dir
    art = runs_dir / "r-0001"
    assert (art / "proposed.diff").is_file()
    assert (art / "proposed.md").is_file()
    assert (art / "stub.stdout").is_file()
    assert (art / "stub.stderr").is_file()
    assert (art / "ledger.entry").is_file()
    assert json.loads((art / "ledger.entry").read_text()) == entry

    # PR opener invoked exactly once
    assert len(pr_opener.calls) == 1
    call = pr_opener.calls[0]
    assert call["branch"] == "tokenman/stub-readme/r-0001"
    assert "Stub-readme added this line" in call["diff"]
```

- [ ] **Step 2: Run to verify it fails**

Run: `pytest tests/test_runner.py -v -k propose_diff_opens_pr`
Expected: FAIL — `AttributeError: module 'harness.lib.runner' has no attribute 'run_skill'`.

- [ ] **Step 3: Implement `run_skill`**

Append to `harness/lib/runner.py`:

```python

import json
import shutil
import tempfile
from pathlib import Path
from time import monotonic
from typing import Any, Callable, Optional

from harness.lib import ledger
from harness.lib.pr_opener import PROpener
from harness.lib.skill_executor import SkillExecutor


def run_skill(
    *,
    skill_dir: Path,
    repo_dir: Path,
    ledger_path: Path,
    runs_dir: Path,
    executor: SkillExecutor,
    pr_opener: PROpener,
    skill_name: Optional[str] = None,
    now: Optional[Callable[[], datetime]] = None,
) -> dict:
    """Run one skill against a repo. Returns the ledger entry appended.

    See the data-flow section of the Phase 1.2a design doc for the
    step-by-step contract.
    """
    now = now or (lambda: datetime.now(timezone.utc))
    skill = skill_name or skill_dir.name

    # 2a. Allocate run_id.
    prev_n = ledger.last_run_id(ledger_path)
    run_id = _format_run_id((prev_n or 0) + 1)

    # 2b/2c. Start clock + create artifact dir.
    t_start = monotonic()
    artifact_dir = runs_dir / run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    # 2d/2e. Scratch dir + executor invocation.
    with tempfile.TemporaryDirectory(prefix=f"tokenman-{run_id}-") as scratch_str:
        scratch = Path(scratch_str)
        result = executor.execute(skill_dir, repo_dir, scratch)

        # 2f. Persist subprocess output.
        (artifact_dir / "stub.stdout").write_text(result.stdout)
        (artifact_dir / "stub.stderr").write_text(result.stderr)
        if result.proposed_diff_path is not None:
            shutil.copyfile(result.proposed_diff_path, artifact_dir / "proposed.diff")
        if result.proposed_md_path is not None:
            shutil.copyfile(result.proposed_md_path, artifact_dir / "proposed.md")
        diff_text = (
            (artifact_dir / "proposed.diff").read_text()
            if result.proposed_diff_path is not None
            else ""
        )

    # 2g. Decide status + populate fields.
    generator: Optional[dict]
    pr: Optional[int]
    if result.exit_code != 0:
        status: str = "error"
        generator = None
        pr = None
    elif result.proposed_diff_path is None:
        status = "no_change"
        generator = {
            "prompt_version": "stub-v1",
            "output_summary": result.summary,
            "diff_lines": 0,
            "tokens": 0,
        }
        pr = None
    else:
        diff_lines = _count_diff_lines(diff_text)
        generator = {
            "prompt_version": "stub-v1",
            "output_summary": result.summary,
            "diff_lines": diff_lines,
            "tokens": 0,
        }
        try:
            pr = pr_opener.open(
                title=f"[tokenman] {skill}: {result.summary}",
                body=result.summary,
                branch=f"tokenman/{skill}/{run_id}",
                diff=diff_text,
            )
            status = "pr_opened"
        except Exception as exc:
            status = "error"
            generator = None
            pr = None
            (artifact_dir / "stub.stderr").write_text(
                result.stderr + f"\n[runner] pr_opener failed: {exc}\n"
            )

    # 2h. Stop clock.
    duration_s = int(monotonic() - t_start)

    # 2i. Build ledger entry.
    entry: dict[str, Any] = {
        "run_id": run_id,
        "ts": _iso_utc(now()),
        "skill": skill,
        "status": status,
        "pr": pr,
        "generator": generator,
        "evaluator": None,
        "duration_s": duration_s,
        "total_tokens": (generator["tokens"] if generator else 0),
        "verdict": None,
        "verdict_note": None,
    }

    # 2j. Append (raises on invariant violation).
    ledger.append(ledger_path, entry)

    # 2k. Per-run ledger copy (only after successful append).
    (artifact_dir / "ledger.entry").write_text(
        json.dumps(entry, separators=(",", ":")) + "\n"
    )

    # 2l. Return.
    return entry
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_runner.py -v -k propose_diff_opens_pr`
Expected: PASS.

- [ ] **Step 5: Run full runner tests for regressions**

Run: `pytest tests/test_runner.py -v`
Expected: 7 tests PASS (6 helpers + 1 integration).

---

### Task 15: `run_skill` — `no_change` path

**Files:**
- Modify: `tests/test_runner.py`

- [ ] **Step 1: Add failing test**

Append to `tests/test_runner.py`:

```python


def test_run_skill_no_change_skips_pr_opener(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    pr_opener = FakePROpener(sink_dir=tmp_path / "prs", start=1000)

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name="stub-readme",
        now=_fixed_now,
    )

    assert entry["status"] == "no_change"
    assert entry["pr"] is None
    assert entry["generator"]["diff_lines"] == 0
    assert entry["generator"]["tokens"] == 0
    assert entry["total_tokens"] == 0
    assert pr_opener.calls == []

    art = runs_dir / "r-0001"
    assert not (art / "proposed.diff").exists()
    assert not (art / "proposed.md").exists()
    assert (art / "stub.stdout").is_file()
    assert (art / "stub.stderr").is_file()
    assert (art / "ledger.entry").is_file()
```

- [ ] **Step 2: Run to verify it passes (the implementation already covers this path)**

Run: `pytest tests/test_runner.py -v -k no_change_skips`
Expected: PASS (run_skill from Task 14 handles this branch).

---

### Task 16: `run_skill` — `crash` / error path

**Files:**
- Modify: `tests/test_runner.py`

- [ ] **Step 1: Add failing test**

Append to `tests/test_runner.py`:

```python


def test_run_skill_crash_records_error(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "crash"})
    pr_opener = FakePROpener()

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name="stub-readme",
        now=_fixed_now,
    )

    assert entry["status"] == "error"
    assert entry["generator"] is None
    assert entry["pr"] is None
    assert entry["total_tokens"] == 0
    assert pr_opener.calls == []

    art = runs_dir / "r-0001"
    assert (art / "stub.stdout").is_file()
    stderr_content = (art / "stub.stderr").read_text()
    assert "crashing on purpose" in stderr_content
    assert (art / "ledger.entry").is_file()

    # Ledger entry validates against the schema (sanity via re-parse).
    lines = ledger_path.read_text().splitlines()
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed == entry
```

- [ ] **Step 2: Run to verify it passes**

Run: `pytest tests/test_runner.py -v -k crash_records`
Expected: PASS.

---

### Task 17: `run_skill` — `run_id` allocation with existing ledger

**Files:**
- Modify: `tests/test_runner.py`

- [ ] **Step 1: Add tests**

Append to `tests/test_runner.py`:

```python


def test_run_skill_allocates_r0001_on_empty_ledger(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    pr_opener = FakePROpener()

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        now=_fixed_now,
    )
    assert entry["run_id"] == "r-0001"


def test_run_skill_increments_from_existing_ledger(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)

    # Seed with r-0017 by hand-appending via ledger.append.
    seed = {
        "run_id": "r-0017",
        "ts": "2026-04-18T11:00:00Z",
        "skill": "stub-readme",
        "status": "no_change",
        "pr": None,
        "generator": {
            "prompt_version": "stub-v1",
            "output_summary": "seed",
            "diff_lines": 0,
            "tokens": 0,
        },
        "evaluator": None,
        "duration_s": 0,
        "total_tokens": 0,
        "verdict": None,
        "verdict_note": None,
    }
    ledger.append(ledger_path, seed)

    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    pr_opener = FakePROpener()
    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        now=_fixed_now,
    )
    assert entry["run_id"] == "r-0018"
    assert ledger.last_run_id(ledger_path) == 18
```

- [ ] **Step 2: Run the tests**

Run: `pytest tests/test_runner.py -v -k allocat`
Expected: 2 PASS.

---

### Task 18: `run_skill` — atomic append (no `ledger.entry` on invariant failure)

**Files:**
- Modify: `tests/test_runner.py`

- [ ] **Step 1: Add test**

Append to `tests/test_runner.py`:

```python


def test_run_skill_leaves_no_ledger_entry_on_append_failure(tmp_path: Path) -> None:
    """If ledger.append raises (here: ts monotonicity), the runner
    propagates the exception, the ledger file is unchanged, and the
    per-run ledger.entry file is absent (but subprocess artifacts
    still exist because the skill ran).
    """
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)

    # Seed ledger with a future-dated entry so our fixed now() goes
    # backward and trips invariant 5.
    future = {
        "run_id": "r-0001",
        "ts": "2099-01-01T00:00:00Z",
        "skill": "stub-readme",
        "status": "no_change",
        "pr": None,
        "generator": {
            "prompt_version": "stub-v1",
            "output_summary": "seed",
            "diff_lines": 0,
            "tokens": 0,
        },
        "evaluator": None,
        "duration_s": 0,
        "total_tokens": 0,
        "verdict": None,
        "verdict_note": None,
    }
    ledger.append(ledger_path, future)
    before = ledger_path.read_text()

    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    pr_opener = FakePROpener()
    with pytest.raises(ledger.LedgerInvariantError, match="ts"):
        runner.run_skill(
            skill_dir=STUB_SKILL_DIR,
            repo_dir=repo_dir,
            ledger_path=ledger_path,
            runs_dir=runs_dir,
            executor=executor,
            pr_opener=pr_opener,
            now=_fixed_now,  # 2026 — before 2099
        )

    # Ledger unchanged
    assert ledger_path.read_text() == before

    # Artifacts present (subprocess did run), but per-run ledger.entry absent.
    art = runs_dir / "r-0002"
    assert (art / "stub.stdout").is_file()
    assert (art / "stub.stderr").is_file()
    assert not (art / "ledger.entry").exists()
```

- [ ] **Step 2: Run the test**

Run: `pytest tests/test_runner.py -v -k leaves_no_ledger_entry`
Expected: PASS (the runner's order is append → write ledger.entry; on append failure the second step never runs).

- [ ] **Step 3: Full test suite regression check**

Run: `pytest -q`
Expected: ~40 tests PASS (3 schema + 26 ledger + 4 pr_opener + 4 skill_executor + 12 runner). 0 failures.

- [ ] **Step 4: Manual status.sh smoke check**

Run:
```bash
python3 - <<'PY'
import shutil, tempfile
from pathlib import Path
from datetime import datetime, timezone
from harness.lib import runner
from harness.lib.pr_opener import FakePROpener
from harness.lib.skill_executor import StubSkillExecutor

tmp = Path(tempfile.mkdtemp(prefix="tokenman-smoke-"))
repo = tmp / "repo"
shutil.copytree("tests/fixtures/tiny-python-repo", repo)
(repo / ".tokenman").mkdir(exist_ok=True)
ledger = repo / ".tokenman" / "ledger.jsonl"
runs = repo / ".tokenman" / "runs"

for mode in ("propose_diff", "no_change", "crash"):
    runner.run_skill(
        skill_dir=Path("tests/fixtures/skills/stub-readme"),
        repo_dir=repo,
        ledger_path=ledger,
        runs_dir=runs,
        executor=StubSkillExecutor(extra_env={"STUB_MODE": mode}),
        pr_opener=FakePROpener(sink_dir=tmp / "prs"),
        skill_name="stub-readme",
        now=lambda m=mode: datetime.now(timezone.utc),
    )

print(ledger)
PY

# Now run status.sh against the resulting ledger — expect 3 entries, varied statuses.
bash harness/templates/status.sh /tmp/tokenman-smoke-*/repo/.tokenman/ledger.jsonl
```

Expected: `status.sh` renders a summary with 3 runs (1 pr_opened, 1 no_change, 1 error) without error. Note the output for the PR description.

- [ ] **Step 5: Shellcheck regression**

Run: `shellcheck harness/templates/status.sh tests/fixtures/skills/stub-readme/stub.sh`
Expected: no findings, exit 0 on both.

- [ ] **Step 6: Commit (Commit 3)**

Run:
```bash
git add harness/lib/runner.py tests/test_runner.py
git commit -m "$(cat <<'EOF'
feat(harness): add runner that orchestrates a single-skill run

harness.lib.runner.run_skill allocates a monotonic run_id, executes a
skill via an injected SkillExecutor, persists subprocess stdout/stderr
and any proposed.diff / proposed.md into .tokenman/runs/r-NNNN/,
chooses status based on the skill's exit + output, invokes the
injected PR opener when a diff was proposed, and appends the ledger
entry. A per-run ledger.entry file is written only after a
successful ledger.append so failed runs never leave orphan copies.

Tests cover the propose_diff / no_change / crash paths,
run_id allocation against empty and pre-seeded ledgers, and the
atomicity guarantee on invariant-violation failures.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git status
```
Expected: commit created, working tree clean.

---

## Commit group 4: docs

### Task 19: Update `CONTRIBUTING.md`

**Files:**
- Modify: `CONTRIBUTING.md`

- [ ] **Step 1: Read the current file**

Run: `cat CONTRIBUTING.md`
Note the current structure (Phase 1.1 added a Running tests section).

- [ ] **Step 2: Add a short section about the harness modules**

Add (or update) a subsection titled **"Harness runtime modules"** under the existing testing / source-and-runtime notes. Use this exact block:

```markdown
## Harness runtime modules

The Python harness lives under `harness/lib/`:

- `harness/lib/ledger.schema.json` — canonical ledger shape (from Phase 1.1).
- `harness/lib/ledger.py` — `validate()`, `append()`, `last_run_id()`. Enforces the conditional invariants the JSON Schema cannot express.
- `harness/lib/skill_executor.py` — `ExecutionResult`, `SkillExecutor` Protocol, `StubSkillExecutor` (tests only). Phase 1.2b adds `ClaudeSkillExecutor`.
- `harness/lib/pr_opener.py` — `PROpener` Protocol, `FakePROpener` (tests only). Phase 1.2b adds `GhPROpener`.
- `harness/lib/runner.py` — `run_skill`, the orchestrator.

Tests for each module live at `tests/test_<module>.py`. The stub skill used by executor + runner integration tests lives at `tests/fixtures/skills/stub-readme/`.

Run `pytest` from the repo root after `pip install -e '.[dev]'`.
```

Place it after the existing Running tests section or wherever it fits coherently in the document.

- [ ] **Step 3: Verify Markdown still renders cleanly**

Run: `git diff CONTRIBUTING.md`
Expected: only the additions shown.

- [ ] **Step 4: Commit (Commit 4)**

Run:
```bash
git add CONTRIBUTING.md
git commit -m "$(cat <<'EOF'
docs: note harness-lib modules in CONTRIBUTING

Adds a short map of the Phase 1.2a modules under harness/lib/ and
points contributors at their tests + the stub-skill fixture.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git status
```
Expected: commit created, working tree clean.

---

## Final verification

- [ ] **Step 1: Confirm four commits landed on `phase-1-2a`**

Run: `git log --oneline main..HEAD`
Expected: exactly four commits, in order:
```
<sha> docs: note harness-lib modules in CONTRIBUTING
<sha> feat(harness): add runner that orchestrates a single-skill run
<sha> feat(harness): add skill executor and PR opener abstractions
<sha> feat(harness): add ledger append utility with invariant enforcement
```

- [ ] **Step 2: Full test suite green**

Run: `pytest -q`
Expected: ~40 tests PASS, 0 failures, 0 errors.

- [ ] **Step 3: Shellcheck green**

Run: `shellcheck harness/templates/status.sh tests/fixtures/skills/stub-readme/stub.sh`
Expected: no findings, exit 0.

- [ ] **Step 4: Imports work from a fresh shell**

Run:
```bash
python3 -c "from harness.lib import ledger, runner, skill_executor, pr_opener; print('OK')"
```
Expected: `OK`.

- [ ] **Step 5: PAUSE + workflow template untouched**

Run:
```bash
test -f .tokenman/PAUSE && echo "PAUSE ok"
git diff main -- harness/workflows/tokenman.yml.template
```
Expected: `PAUSE ok` printed; empty diff (workflow template unchanged).

- [ ] **Step 6: Working tree clean**

Run: `git status`
Expected: `nothing to commit, working tree clean`.

- [ ] **Step 7: Ready for integration**

The branch `phase-1-2a` is now ready to merge into `main`, or to be picked up by Phase 1.2b. Next-session handoff should point at the Phase 1.2b work (real `claude -p`, real `gh`, functional workflow template).
