# Phase 1.2b Real-Skill Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Swap 1.2a's stub boundary classes for real ones (`ClaudeSkillExecutor`, `GhPROpener`), land the first cataloged skill (`readme-maintainer`), add a runner CLI, and produce a consumer-deployable workflow template.

**Architecture:** Phase split into two reviewable surfaces. **1.2b-i** is a pure mechanical refactor (no behavior change) cleaning up 1.2a review carry-overs. **1.2b-ii** is purely additive: new classes behind existing Protocols, runner grows `git apply/commit/push` before the PR step, `python -m harness.run` entrypoint above `run_skill`, first `skills/readme-maintainer/` + catalog entry, functional `tokenman.yml.template`.

**Tech Stack:** Python 3.10+, `subprocess` for `claude -p` + `gh` + `git` + `diff` + `git apply`, `jsonschema` (already a dev dep), `pytest` with a custom `live` marker for opt-in live tests. Bash `/usr/bin/diff -ruN` for the diff computation. No new pip dependencies.

**Parent spec:** `docs/superpowers/specs/2026-04-18-phase-1-2b-real-skill-integration-design.md`

---

## Setup: create two worktrees

1.2b runs on two branches off `main`, in order. Refactor branch first — merge before starting integration.

- [ ] **Step 1: Verify working tree is clean on `main`**

Run: `git status`
Expected: on branch `main`, working tree clean, no pending commits after the design-doc commit `3827272`.

- [ ] **Step 2: Create the refactor worktree**

Run:
```bash
git worktree add ../tokenman-phase-1-2b-i -b phase-1-2b-i main
cd ../tokenman-phase-1-2b-i
```
Expected: new worktree directory at `../tokenman-phase-1-2b-i`, on fresh branch `phase-1-2b-i` based on `main`.

- [ ] **Step 3: Confirm design + plan are visible**

Run:
```bash
ls docs/superpowers/specs/2026-04-18-phase-1-2b-real-skill-integration-design.md
ls docs/superpowers/plans/2026-04-18-phase-1-2b-real-skill-integration.md
```
Expected: both files exist.

- [ ] **Step 4: Install the package in editable mode**

Run: `pip install -e '.[dev]' -q`
Expected: exit 0. Package importable.

- [ ] **Step 5: Baseline test run**

Run: `pytest -q`
Expected: all 1.2a tests pass. Note the count — it should stay the same after each i.* commit.

The worktree for **1.2b-ii** is created later, after `phase-1-2b-i` is merged to `main`.

---

# Part I — `phase-1-2b-i` branch (mechanical refactor)

Four commits. No behavior changes; tests update to match renames/signatures.

---

## Commit group i.1: thread `prompt_version` and `tokens` through `ExecutionResult`

Ends with commit `refactor(harness): thread prompt_version and tokens through ExecutionResult`.

### Task 1: Extend `ExecutionResult`

**Files:**
- Modify: `harness/lib/skill_executor.py`
- Modify: `tests/test_skill_executor.py`

- [ ] **Step 1: Read current `skill_executor.py`**

Run: `cat harness/lib/skill_executor.py`
Expected: see the `ExecutionResult` dataclass with fields `exit_code, stdout, stderr, proposed_diff_path, proposed_md_path, summary`.

- [ ] **Step 2: Add two fields to `ExecutionResult`**

Edit the dataclass in `harness/lib/skill_executor.py` to add `prompt_version` and `tokens`:

```python
@dataclass
class ExecutionResult:
    exit_code: int
    stdout: str
    stderr: str
    proposed_diff_path: Optional[Path]
    proposed_md_path: Optional[Path]
    summary: str
    prompt_version: str = "unknown"
    tokens: int = 0
```

- [ ] **Step 3: Set `prompt_version="stub-v1"` and `tokens=0` in `StubSkillExecutor.execute`**

Edit the `return ExecutionResult(...)` at the bottom of `StubSkillExecutor.execute` to include both fields:

```python
        return ExecutionResult(
            exit_code=proc.returncode,
            stdout=proc.stdout,
            stderr=proc.stderr,
            proposed_diff_path=diff if diff.is_file() else None,
            proposed_md_path=md if md.is_file() else None,
            summary=first_stdout_line,
            prompt_version="stub-v1",
            tokens=0,
        )
```

- [ ] **Step 4: Update `tests/test_skill_executor.py` to assert the new fields**

Add one assertion to each `StubSkillExecutor` behavioral test. Example in the existing `test_stub_propose_diff_mode` (or equivalent):

```python
    assert result.prompt_version == "stub-v1"
    assert result.tokens == 0
```

Apply the same two-line assertion to every `StubSkillExecutor` test that already inspects the `ExecutionResult`.

- [ ] **Step 5: Run executor tests**

Run: `pytest tests/test_skill_executor.py -v`
Expected: all tests pass; new assertions green.

### Task 2: Runner reads from `ExecutionResult`

**Files:**
- Modify: `harness/lib/runner.py`
- Modify: `tests/test_runner.py`

- [ ] **Step 1: Replace the hardcoded `"stub-v1"` with `result.prompt_version`**

In `harness/lib/runner.py`, find both spots that build the `generator` dict (the `no_change` branch and the `pr_opened` branch) and replace `"prompt_version": "stub-v1"` with `"prompt_version": result.prompt_version`.

Before (both branches):
```python
            "prompt_version": "stub-v1",
```
After:
```python
            "prompt_version": result.prompt_version,
```

- [ ] **Step 2: Replace the hardcoded `"tokens": 0` with `result.tokens`**

In the same two `generator` dicts, replace `"tokens": 0` with `"tokens": result.tokens`. After the change, both `generator` dicts use `result.*` for both fields.

- [ ] **Step 3: Update `total_tokens` calculation if needed**

The line `"total_tokens": (generator["tokens"] if generator else 0),` is already indirect (reads from the dict we just populated), so it needs no change.

- [ ] **Step 4: Update `tests/test_runner.py` assertions**

For each runner test that inspects the returned entry's `generator` block, add:

```python
    assert entry["generator"]["prompt_version"] == "stub-v1"
    assert entry["generator"]["tokens"] == 0
```

- [ ] **Step 5: Run all tests**

Run: `pytest -q`
Expected: every pre-existing test still passes; new assertions green; test count unchanged or slightly higher.

### Task 3: Commit i.1

- [ ] **Step 1: Verify clean diff scope**

Run: `git status && git diff --stat`
Expected: only `harness/lib/skill_executor.py`, `harness/lib/runner.py`, `tests/test_skill_executor.py`, `tests/test_runner.py` modified.

- [ ] **Step 2: Commit**

```bash
git add harness/lib/skill_executor.py harness/lib/runner.py tests/test_skill_executor.py tests/test_runner.py
git commit -m "$(cat <<'EOF'
refactor(harness): thread prompt_version and tokens through ExecutionResult

Removes the runner's hardcoded "stub-v1"/0 values in favor of fields
owned by each executor. Unblocks ClaudeSkillExecutor in 1.2b-ii to
publish its own prompt_version and real token counts without touching
runner.py.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds; `git log -1 --stat` shows the four files.

---

## Commit group i.2: rename `stub.{stdout,stderr}` to `executor.{stdout,stderr}`

Ends with commit `refactor(harness): rename stub.{stdout,stderr} to executor.{stdout,stderr}`.

### Task 4: Rename in `runner.py`

**Files:**
- Modify: `harness/lib/runner.py`
- Modify: `tests/test_runner.py`

- [ ] **Step 1: Replace `stub.stdout` and `stub.stderr` in `harness/lib/runner.py`**

Find these three lines (two writes + one rewrite on pr_opener failure):

```python
        (artifact_dir / "stub.stdout").write_text(result.stdout)
        (artifact_dir / "stub.stderr").write_text(result.stderr)
```
Change to:
```python
        (artifact_dir / "executor.stdout").write_text(result.stdout)
        (artifact_dir / "executor.stderr").write_text(result.stderr)
```

And the pr_opener-failure rewrite:
```python
            (artifact_dir / "stub.stderr").write_text(
                result.stderr + f"\n[runner] pr_opener failed: {exc}\n{tb}"
            )
```
Change to:
```python
            (artifact_dir / "executor.stderr").write_text(
                result.stderr + f"\n[runner] pr_opener failed: {exc}\n{tb}"
            )
```

- [ ] **Step 2: Grep the repo for leftover references**

Run: `grep -rn "stub\.stdout\|stub\.stderr" harness/ tests/ docs/`
Expected: matches only inside docs/superpowers/specs/\*-phase-1-2a-\* (history, don't edit) and `docs/superpowers/specs/\*-phase-1-2b-\*` (this design doc, already uses `executor.*`). No matches inside `harness/` or `tests/`.

If any `.py` file still references the old names, fix those too.

- [ ] **Step 3: Update every `tests/test_runner.py` assertion on `stub.stdout`/`stub.stderr`**

Find and replace every occurrence:

- `"stub.stdout"` → `"executor.stdout"`
- `"stub.stderr"` → `"executor.stderr"`

Apply inside test assertions such as:
```python
    assert (runs_dir / run_id / "executor.stdout").exists()
    assert "crashing on purpose" in (runs_dir / run_id / "executor.stderr").read_text()
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_runner.py -v`
Expected: all tests pass; artifact dir now produces `executor.stdout`/`executor.stderr`.

### Task 5: Commit i.2

- [ ] **Step 1: Verify diff is rename-only**

Run: `git diff`
Expected: the only changes are `stub.*` → `executor.*` inside runner.py and test_runner.py. No other logic touched.

- [ ] **Step 2: Commit**

```bash
git add harness/lib/runner.py tests/test_runner.py
git commit -m "$(cat <<'EOF'
refactor(harness): rename stub.{stdout,stderr} to executor.{stdout,stderr}

"stub.*" encoded the test-only executor's identity into the generic
runner's artifact layout. 1.2b-ii's ClaudeSkillExecutor writes the same
files from its own subprocess; the name should describe the role, not
the implementation. No behavior change.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group i.3: `timeout_s` on executor constructor

Ends with commit `refactor(harness): add timeout_s to executor constructor`.

### Task 6: Add `timeout_s` parameter and behavior

**Files:**
- Modify: `harness/lib/skill_executor.py`
- Modify: `tests/test_skill_executor.py`

- [ ] **Step 1: Add `timeout_s` to `StubSkillExecutor.__init__`**

In `harness/lib/skill_executor.py`, change the constructor:

```python
    def __init__(
        self,
        extra_env: Optional[dict[str, str]] = None,
        timeout_s: int = 30,
    ) -> None:
        self._extra_env = dict(extra_env) if extra_env else {}
        self._timeout_s = timeout_s
```

- [ ] **Step 2: Pass `timeout_s` to `subprocess.run` and handle `TimeoutExpired`**

Replace the body of `execute`:

```python
    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult:
        entrypoint = skill_dir / "stub.sh"
        env = {**os.environ, **self._extra_env}
        try:
            proc = subprocess.run(
                ["bash", str(entrypoint), str(scratch_dir)],
                cwd=str(repo_dir),
                env=env,
                capture_output=True,
                text=True,
                check=False,
                timeout=self._timeout_s,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout or ""
            stderr = (e.stderr or "") + f"\n[executor] stub.sh timed out after {self._timeout_s}s\n"
            exit_code = -1

        diff = scratch_dir / "proposed.diff"
        md = scratch_dir / "proposed.md"
        first_stdout_line = next(
            (ln for ln in stdout.splitlines() if ln.strip()),
            f"{skill_dir.name}: exit {exit_code}",
        )
        return ExecutionResult(
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            proposed_diff_path=diff if diff.is_file() else None,
            proposed_md_path=md if md.is_file() else None,
            summary=first_stdout_line,
            prompt_version="stub-v1",
            tokens=0,
        )
```

`subprocess.TimeoutExpired` surfaces as `exit_code=-1`. The runner already treats non-zero exit codes as `status="error"`, so no runner change needed.

- [ ] **Step 3: Write the failing test**

Add to `tests/test_skill_executor.py`:

```python
import time
import subprocess
import textwrap
from pathlib import Path

import pytest

from harness.lib.skill_executor import StubSkillExecutor


def test_stub_timeout_surfaces_as_error(tmp_path: Path) -> None:
    skill_dir = tmp_path / "slow-skill"
    skill_dir.mkdir()
    (skill_dir / "stub.sh").write_text(textwrap.dedent("""\
        #!/usr/bin/env bash
        sleep 3
        echo "should never print"
    """))
    (skill_dir / "stub.sh").chmod(0o755)
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    scratch_dir = tmp_path / "scratch"
    scratch_dir.mkdir()

    executor = StubSkillExecutor(timeout_s=1)
    result = executor.execute(skill_dir, repo_dir, scratch_dir)

    assert result.exit_code == -1
    assert "timed out" in result.stderr
    assert result.proposed_diff_path is None
```

- [ ] **Step 4: Run the test**

Run: `pytest tests/test_skill_executor.py::test_stub_timeout_surfaces_as_error -v`
Expected: PASS. Also run the full test file to ensure nothing regressed: `pytest tests/test_skill_executor.py -v`.

- [ ] **Step 5: Run the full suite**

Run: `pytest -q`
Expected: all tests pass.

### Task 7: Commit i.3

- [ ] **Step 1: Commit**

```bash
git add harness/lib/skill_executor.py tests/test_skill_executor.py
git commit -m "$(cat <<'EOF'
refactor(harness): add timeout_s to executor constructor

StubSkillExecutor gains a timeout_s kwarg wrapping subprocess.run.
subprocess.TimeoutExpired is surfaced as exit_code=-1 with an appended
stderr note, which the runner already treats as status="error".
1.2b-ii's ClaudeSkillExecutor needs a timeout (claude -p can run
minutes); landing the pattern on the stub keeps the Protocol contract
uniform and gives the runner one error path.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group i.4: drop `diff` from `PROpener`; add `LedgerEntry` TypedDict

Ends with commit `refactor(harness): drop diff from PROpener Protocol; add LedgerEntry TypedDict`.

### Task 8: Update `PROpener` Protocol

**Files:**
- Modify: `harness/lib/pr_opener.py`
- Modify: `harness/lib/runner.py`
- Modify: `tests/test_pr_opener.py`
- Modify: `tests/test_runner.py`

- [ ] **Step 1: Drop `diff` from the Protocol method signature**

Edit `harness/lib/pr_opener.py`:

```python
class PROpener(Protocol):
    """Opens a PR and returns its number."""

    def open(self, *, title: str, body: str, branch: str) -> int: ...
```

- [ ] **Step 2: Drop `diff` from `FakePROpener.open` and stop persisting it**

Replace the method:

```python
    def open(self, *, title: str, body: str, branch: str) -> int:
        n = self._next
        self._next += 1
        record = {
            "pr": n,
            "title": title,
            "body": body,
            "branch": branch,
        }
        self.calls.append(record)
        if self._sink_dir is not None:
            self._sink_dir.mkdir(parents=True, exist_ok=True)
            (self._sink_dir / f"pr-{n}.json").write_text(
                json.dumps(record, indent=2)
            )
        return n
```

`FakePROpener` no longer knows about diffs. If a test needs to assert on the diff, it reads `runs/<run_id>/proposed.diff` from disk.

- [ ] **Step 3: Update the runner's call site**

In `harness/lib/runner.py`, remove the `diff=diff_text` argument from the `pr_opener.open` call:

```python
            pr = pr_opener.open(
                title=f"[tokenman] {skill}: {result.summary}",
                body=result.summary,
                branch=f"tokenman/{skill}/{run_id}",
            )
```

The local variable `diff_text` remains — the runner still uses it (for `diff_lines` counting, and in 1.2b-ii for git apply).

- [ ] **Step 4: Update `tests/test_pr_opener.py`**

Remove any test that asserts on `diff=` in the call args. For tests that use `FakePROpener.open(...)`, drop the `diff=` kwarg from the call. For tests that check the sink_dir JSON file, update expected keys: no longer has `"diff"`.

- [ ] **Step 5: Update `tests/test_runner.py` if it asserts on FakePROpener `diff` payload**

Find any test that does something like `assert pr_opener.calls[0]["diff"] == ...`. Change it to read from the artifact dir instead:
```python
    diff_on_disk = (runs_dir / run_id / "proposed.diff").read_text()
    assert "new line" in diff_on_disk
```

- [ ] **Step 6: Run tests**

Run: `pytest -q`
Expected: all tests pass.

### Task 9: Add `LedgerEntry` TypedDict

**Files:**
- Modify: `harness/lib/ledger.py`
- Modify: `harness/lib/runner.py`

- [ ] **Step 1: Add the TypedDict at the top of `ledger.py`**

Add after the imports (still at module scope, before `_SCHEMA_PATH`):

```python
from typing import Optional, TypedDict


class GeneratorBlock(TypedDict):
    prompt_version: str
    output_summary: str
    diff_lines: int
    tokens: int


class EvaluatorBlock(TypedDict):
    prompt_version: str
    verdict: str
    reason: str
    tokens: int


class LedgerEntry(TypedDict):
    run_id: str
    ts: str
    skill: str
    status: str
    pr: Optional[int]
    generator: Optional[GeneratorBlock]
    evaluator: Optional[EvaluatorBlock]
    duration_s: int
    total_tokens: int
    verdict: Optional[str]
    verdict_note: Optional[str]
```

`Optional` is already imported via `typing`; `TypedDict` needs adding to the existing `from typing import` line. Merge into one import:

```python
from typing import Optional, TypedDict
```

- [ ] **Step 2: Annotate `runner.run_skill` return type**

In `harness/lib/runner.py`, change the import:

```python
from harness.lib.ledger import LedgerEntry
```

Change the function signature:

```python
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
) -> LedgerEntry:
```

Leave the inner `entry: dict[str, Any]` annotation alone — the TypedDict is documentation for callers; internal construction stays dict-shaped.

- [ ] **Step 3: Annotate `ledger.append` argument**

Change:
```python
def append(ledger_path: Path, entry: dict) -> None:
```
To:
```python
def append(ledger_path: Path, entry: LedgerEntry) -> None:
```

- [ ] **Step 4: Run tests**

Run: `pytest -q`
Expected: all tests pass.

- [ ] **Step 5: Verify no type errors**

If the project has `mypy` or similar configured, run it. If not, confirm imports at minimum:

Run: `python3 -c "from harness.lib.ledger import LedgerEntry, GeneratorBlock, EvaluatorBlock; print('ok')"`
Expected: `ok`.

### Task 10: Commit i.4

- [ ] **Step 1: Commit**

```bash
git add harness/lib/pr_opener.py harness/lib/runner.py harness/lib/ledger.py tests/test_pr_opener.py tests/test_runner.py
git commit -m "$(cat <<'EOF'
refactor(harness): drop diff from PROpener Protocol; add LedgerEntry TypedDict

PROpener.open now takes (title, body, branch) only. 1.2b-ii's runner
applies the diff to a branch via git_ops before calling pr_opener; the
diff arg became dead weight. FakePROpener stops recording the diff
field; tests that previously inspected it now read
runs/<id>/proposed.diff from disk instead.

LedgerEntry + GeneratorBlock + EvaluatorBlock TypedDicts are now
documented in ledger.py so callers have ergonomic types; the
append/validate internals remain dict-shaped.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Finish Part I: push, review, merge

- [ ] **Step 1: Final suite run**

Run: `pytest -q`
Expected: all tests green, count unchanged from the initial baseline except for `test_stub_timeout_surfaces_as_error` (+1).

- [ ] **Step 2: Push branch**

Ask the user before pushing. If approved:

```bash
git push -u origin phase-1-2b-i
```

- [ ] **Step 3: Open a PR**

```bash
gh pr create --title "refactor(harness): 1.2b-i mechanical carry-overs" --body "$(cat <<'EOF'
## Summary
Four mechanical refactors from the 1.2a reviewer's list — unblocks 1.2b-ii without mixing the refactor with the real integration work.

- `ExecutionResult` gains `prompt_version` + `tokens`; runner reads them instead of hardcoding
- Artifact files renamed `stub.{stdout,stderr}` → `executor.{stdout,stderr}`
- `StubSkillExecutor(timeout_s=...)` surfaces timeouts as `exit_code=-1`
- `PROpener.open` drops the `diff` arg; `LedgerEntry` TypedDict added

## Test plan
- [x] `pytest -q` green
- [x] One new test (`test_stub_timeout_surfaces_as_error`)
- [ ] Reviewer: manual scan for any leftover `stub.stdout|stub.stderr` refs

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 4: After merge, return to main and prune**

In the main worktree:
```bash
cd ../tokenman
git checkout main
git pull --ff-only
git worktree remove ../tokenman-phase-1-2b-i
git branch -D phase-1-2b-i
```

---

# Part II — `phase-1-2b-ii` branch (integration)

Nine commits. New classes, new skill, CLI, workflow. Start **after** `phase-1-2b-i` is merged to `main`.

- [ ] **Step 0: Create the integration worktree**

From the main worktree:
```bash
git worktree add ../tokenman-phase-1-2b-ii -b phase-1-2b-ii main
cd ../tokenman-phase-1-2b-ii
pip install -e '.[dev]' -q
pytest -q
```
Expected: clean worktree; all Part I tests pass from `main`.

---

## Commit group ii.1: `git_ops` module

Ends with commit `feat(harness): add git_ops module for branch/apply/push`.

### Task 11: Write the failing `git_ops` tests

**Files:**
- Create: `tests/test_git_ops.py`

- [ ] **Step 1: Create the test file**

Write `tests/test_git_ops.py`:

```python
"""Unit tests for harness.lib.git_ops."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from harness.lib.git_ops import (
    GitIdentity,
    GitOpsError,
    apply_diff_and_push,
)


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def _make_repo_with_bare_remote(tmp_path: Path) -> tuple[Path, Path]:
    """Initialise a working repo with a bare remote at tmp_path/remote.
    Returns (repo_dir, remote_dir). repo_dir has one commit on main and
    tracks origin=main.
    """
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)

    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    (repo / "README.md").write_text("# Hello\n")
    _git(repo, "config", "user.email", "seed@local")
    _git(repo, "config", "user.name",  "seed")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "seed")
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-u", "origin", "main")
    return repo, remote


IDENTITY = GitIdentity(name="tokenman-bot", email="tokenman@local")


def test_apply_diff_and_push_creates_branch_commit_push(tmp_path: Path) -> None:
    repo, remote = _make_repo_with_bare_remote(tmp_path)
    diff_text = (
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1 +1,2 @@\n"
        " # Hello\n"
        "+## New section\n"
    )
    apply_diff_and_push(
        repo_dir=repo,
        diff_text=diff_text,
        branch="tokenman/readme-maintainer/r-0001",
        base="main",
        message="[tokenman] readme-maintainer: add section",
        identity=IDENTITY,
    )

    # local branch exists and points at a new commit
    branches = _git(repo, "branch", "--list")
    assert "tokenman/readme-maintainer/r-0001" in branches

    # commit author identity is ours
    log = _git(repo, "log", "-1", "--format=%an <%ae> %s", "tokenman/readme-maintainer/r-0001")
    assert "tokenman-bot <tokenman@local>" in log
    assert "add section" in log

    # the README has the new section applied
    _git(repo, "switch", "tokenman/readme-maintainer/r-0001")
    assert "## New section" in (repo / "README.md").read_text()

    # remote has the pushed branch
    remote_refs = subprocess.run(
        ["git", "ls-remote", str(remote)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "refs/heads/tokenman/readme-maintainer/r-0001" in remote_refs


def test_apply_diff_and_push_raises_on_bad_diff(tmp_path: Path) -> None:
    repo, _ = _make_repo_with_bare_remote(tmp_path)
    bogus_diff = "not a valid unified diff at all\n"
    with pytest.raises(GitOpsError):
        apply_diff_and_push(
            repo_dir=repo,
            diff_text=bogus_diff,
            branch="tokenman/does-not-matter/r-0001",
            base="main",
            message="won't apply",
            identity=IDENTITY,
        )

    # no branch left behind with content
    branches = _git(repo, "branch", "--list")
    # Either the branch was rolled back, or it exists at the base sha — just
    # ensure we never created a commit on it beyond base.
    # (apply_diff_and_push should attempt to clean up on failure.)
    if "tokenman/does-not-matter/r-0001" in branches:
        head = _git(repo, "rev-parse", "tokenman/does-not-matter/r-0001").strip()
        base = _git(repo, "rev-parse", "main").strip()
        assert head == base
```

- [ ] **Step 2: Run the tests**

Run: `pytest tests/test_git_ops.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'harness.lib.git_ops'`.

### Task 12: Implement `git_ops`

**Files:**
- Create: `harness/lib/git_ops.py`

- [ ] **Step 1: Write the module**

Create `harness/lib/git_ops.py`:

```python
"""Git operations for the tokenman runner.

Factored out of runner.py so the branch/apply/commit/push flow has a
single, unit-testable home. Executed after the executor produces a
proposed.diff and before pr_opener.open runs.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


class GitOpsError(RuntimeError):
    """Raised when any git step fails. Wraps the captured stderr."""


@dataclass(frozen=True)
class GitIdentity:
    name: str
    email: str


def _run(
    cmd: list[str],
    *,
    cwd: Path,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def apply_diff_and_push(
    *,
    repo_dir: Path,
    diff_text: str,
    branch: str,
    base: str,
    message: str,
    identity: GitIdentity,
    remote: str = "origin",
) -> None:
    """Create `branch` off `base`, apply `diff_text`, commit with
    `identity`, and push to `remote`.

    Rolls back the local branch on failure (deletes it if it was
    created by this call). Raises GitOpsError on any failed step.
    """
    created_branch = False

    # 1. switch to branch off base
    sw = _run(["git", "switch", "-c", branch, base], cwd=repo_dir)
    if sw.returncode != 0:
        raise GitOpsError(f"git switch -c {branch} {base} failed: {sw.stderr.strip()}")
    created_branch = True

    try:
        # 2. apply diff
        ap = _run(["git", "apply", "--index", "-"], cwd=repo_dir, input_text=diff_text)
        if ap.returncode != 0:
            raise GitOpsError(f"git apply failed: {ap.stderr.strip()}")

        # 3. commit with identity
        co = _run(
            [
                "git",
                "-c", f"user.name={identity.name}",
                "-c", f"user.email={identity.email}",
                "commit",
                "-m", message,
            ],
            cwd=repo_dir,
        )
        if co.returncode != 0:
            raise GitOpsError(f"git commit failed: {co.stderr.strip()}")

        # 4. push
        ps = _run(["git", "push", "-u", remote, branch], cwd=repo_dir)
        if ps.returncode != 0:
            raise GitOpsError(f"git push failed: {ps.stderr.strip()}")

    except Exception:
        if created_branch:
            # best-effort rollback — return to base, delete the branch
            _run(["git", "switch", base], cwd=repo_dir)
            _run(["git", "branch", "-D", branch], cwd=repo_dir)
        raise
```

- [ ] **Step 2: Re-run the tests**

Run: `pytest tests/test_git_ops.py -v`
Expected: both tests pass.

- [ ] **Step 3: Run the full suite**

Run: `pytest -q`
Expected: all existing tests still pass; new git_ops tests green.

### Task 13: Commit ii.1

- [ ] **Step 1: Commit**

```bash
git add harness/lib/git_ops.py tests/test_git_ops.py
git commit -m "$(cat <<'EOF'
feat(harness): add git_ops module for branch/apply/push

apply_diff_and_push creates a branch off base, runs git apply with
--index, commits with an injected identity, and pushes. Rolls back the
local branch on failure. Unit-tested against a tmp bare remote. The
runner calls this before pr_opener.open so GhPROpener can remain a thin
gh pr create wrapper.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group ii.2: wire `git_ops` into `run_skill`

Ends with commit `feat(harness): wire git_ops into run_skill before PR open`.

### Task 14: Update the runner

**Files:**
- Modify: `harness/lib/runner.py`

- [ ] **Step 1: Import `git_ops`**

Add to the imports at the top of `harness/lib/runner.py`:

```python
from harness.lib import git_ops
from harness.lib.git_ops import GitIdentity, GitOpsError
```

Keep the existing `from harness.lib.pr_opener import PROpener` import as-is for this commit. `PROpenerError` does not yet exist (ii.3 adds it); this commit uses a broad `Exception` catch that ii.3 narrows.

- [ ] **Step 2: Add new kwargs to `run_skill`**

Extend the signature:

```python
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
    base_branch: str = "main",
    git_identity: Optional[GitIdentity] = None,
) -> LedgerEntry:
```

Just inside the function body, default the identity:

```python
    git_identity = git_identity or GitIdentity("tokenman-bot", "tokenman@local")
```

- [ ] **Step 3: Replace the `pr_opened` branch's body**

Find the block currently at `elif result.proposed_diff_path is not None:` / `else:` that calls `pr_opener.open(...)`. Replace the happy path + error handling with:

```python
    else:
        diff_lines = _count_diff_lines(diff_text)
        generator = {
            "prompt_version": result.prompt_version,
            "output_summary": result.summary,
            "diff_lines": diff_lines,
            "tokens": result.tokens,
        }
        branch = f"tokenman/{skill}/{run_id}"
        try:
            git_ops.apply_diff_and_push(
                repo_dir=repo_dir,
                diff_text=diff_text,
                branch=branch,
                base=base_branch,
                message=f"[tokenman] {skill}: {result.summary}",
                identity=git_identity,
            )
            pr = pr_opener.open(
                title=f"[tokenman] {skill}: {result.summary}",
                body=result.summary,
                branch=branch,
            )
            status = "pr_opened"
        except Exception as exc:  # narrowed to (GitOpsError, PROpenerError) in ii.3
            import traceback
            tb = traceback.format_exc()
            status = "error"
            generator = None
            pr = None
            (artifact_dir / "executor.stderr").write_text(
                result.stderr + f"\n[runner] git/pr_opener failed: {exc}\n{tb}"
            )
```

Note: the `proposed.diff` artifact continues to exist in `artifact_dir` even on git failure, per the runner's existing order (diff is persisted *before* git is attempted).

- [ ] **Step 4: Update `tests/test_runner.py` to seed a git repo + bare remote**

Rewrite `_prepare_repo_copy` (or add a sibling helper) so `repo_dir` is a real git repo with a bare remote, matching `test_git_ops.py`. Runner integration tests that follow the `pr_opened` branch need the runner's git calls to succeed:

```python
def _prepare_repo_copy_with_remote(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """Return (repo_dir, ledger_path, runs_dir, remote_dir).

    repo_dir is a fresh copy of the fixture + `git init` + initial commit
    + origin pointing at remote_dir (a bare repo).
    """
    repo_dir = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo_dir)
    tokenman_dir = repo_dir / ".tokenman"
    tokenman_dir.mkdir(exist_ok=True)
    ledger_path = tokenman_dir / "ledger.jsonl"
    runs_dir = tokenman_dir / "runs"

    remote_dir = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote_dir)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.name",  "seed"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "commit", "-m", "seed"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "remote", "add", "origin", str(remote_dir)], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "push", "-u", "origin", "main"], check=True, capture_output=True)
    return repo_dir, ledger_path, runs_dir, remote_dir
```

Replace the body of the existing `test_propose_diff_opens_pr` to use the new helper. The stub's canned diff targets `README.md` in the tiny-python fixture; if the stub currently writes a diff against a path the fixture doesn't have, update `tests/fixtures/skills/stub-readme/stub.sh`'s `propose_diff` mode to produce a unified diff that applies cleanly to the fixture's `README.md`.

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_runner.py -v`
Expected: all green. If the stub's canned diff doesn't apply to the fixture's README, iterate on the stub until it does.

- [ ] **Step 6: Confirm the full suite**

Run: `pytest -q`
Expected: all green.

### Task 15: Commit ii.2

- [ ] **Step 1: Commit**

```bash
git add harness/lib/runner.py tests/test_runner.py tests/fixtures/skills/stub-readme/stub.sh
git commit -m "$(cat <<'EOF'
feat(harness): wire git_ops into run_skill before PR open

The runner now creates a branch, applies the proposed.diff, commits
with a configurable identity, and pushes before calling pr_opener.open.
PR opener remains a thin abstraction (real implementation in ii.3);
runner tests now seed a git repo + bare remote. Commit narrows the
pr-path exception handler to (GitOpsError, Exception); ii.3 narrows
Exception to PROpenerError.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group ii.3: `GhPROpener`

Ends with commit `feat(harness): add GhPROpener`.

### Task 16: Write the failing `GhPROpener` tests

**Files:**
- Create: `tests/test_gh_pr_opener.py`

- [ ] **Step 1: Create the test file**

```python
"""Unit tests for harness.lib.pr_opener.GhPROpener."""
from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from harness.lib.pr_opener import GhPROpener, PROpenerError


def test_gh_pr_opener_builds_expected_argv(tmp_path: Path) -> None:
    opener = GhPROpener(repo_dir=tmp_path, base_branch="main", gh_bin="gh")

    with patch("harness.lib.pr_opener.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="4242\n", stderr=""
        )
        pr = opener.open(
            title="[tokenman] readme-maintainer: add section",
            body="Proposed change.",
            branch="tokenman/readme-maintainer/r-0001",
        )

    assert pr == 4242
    args, kwargs = m.call_args
    cmd = args[0]
    assert cmd[0] == "gh"
    assert cmd[1:3] == ["pr", "create"]
    assert "--title" in cmd and "[tokenman] readme-maintainer: add section" in cmd
    assert "--body" in cmd and "Proposed change." in cmd
    assert "--head" in cmd and "tokenman/readme-maintainer/r-0001" in cmd
    assert "--base" in cmd and "main" in cmd
    assert "--json" in cmd and "number" in cmd
    assert "-q" in cmd and ".number" in cmd
    assert kwargs["cwd"] == str(tmp_path)


def test_gh_pr_opener_raises_on_nonzero_exit(tmp_path: Path) -> None:
    opener = GhPROpener(repo_dir=tmp_path)

    with patch("harness.lib.pr_opener.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="",
            stderr="HTTP 422: Validation Failed",
        )
        with pytest.raises(PROpenerError) as exc:
            opener.open(title="t", body="b", branch="br")
        assert "422" in str(exc.value)


def test_gh_pr_opener_parses_number_with_trailing_whitespace(tmp_path: Path) -> None:
    opener = GhPROpener(repo_dir=tmp_path)
    with patch("harness.lib.pr_opener.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="  17\n\n", stderr=""
        )
        assert opener.open(title="t", body="b", branch="br") == 17
```

- [ ] **Step 2: Run and confirm failure**

Run: `pytest tests/test_gh_pr_opener.py -v`
Expected: FAIL with `ImportError: cannot import name 'GhPROpener'` or `PROpenerError`.

### Task 17: Implement `GhPROpener` and `PROpenerError`

**Files:**
- Modify: `harness/lib/pr_opener.py`

- [ ] **Step 1: Add `PROpenerError` and `GhPROpener` to `pr_opener.py`**

Extend the module. The full file becomes:

```python
"""PR opener boundary for the harness runner.

Phase 1.2a shipped FakePROpener for tests. 1.2b-ii adds GhPROpener
which runs `gh pr create` against a real remote; the runner has
already created, committed to, and pushed the branch via git_ops.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Optional, Protocol


class PROpenerError(RuntimeError):
    """Raised when opening a PR fails. Wraps captured stderr."""


class PROpener(Protocol):
    """Opens a PR and returns its number."""

    def open(self, *, title: str, body: str, branch: str) -> int: ...


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

    def open(self, *, title: str, body: str, branch: str) -> int:
        n = self._next
        self._next += 1
        record = {
            "pr": n,
            "title": title,
            "body": body,
            "branch": branch,
        }
        self.calls.append(record)
        if self._sink_dir is not None:
            self._sink_dir.mkdir(parents=True, exist_ok=True)
            (self._sink_dir / f"pr-{n}.json").write_text(
                json.dumps(record, indent=2)
            )
        return n


class GhPROpener:
    """Calls `gh pr create --json number` and parses the result.

    Assumes the branch already exists locally and has been pushed (the
    runner does this via git_ops.apply_diff_and_push before calling us).
    """

    def __init__(
        self,
        repo_dir: Path,
        base_branch: str = "main",
        gh_bin: str = "gh",
    ) -> None:
        self._repo_dir = repo_dir
        self._base = base_branch
        self._gh = gh_bin

    def open(self, *, title: str, body: str, branch: str) -> int:
        proc = subprocess.run(
            [
                self._gh, "pr", "create",
                "--title", title,
                "--body", body,
                "--head", branch,
                "--base", self._base,
                "--json", "number",
                "-q", ".number",
            ],
            cwd=str(self._repo_dir),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise PROpenerError(
                f"gh pr create failed (exit {proc.returncode}): {proc.stderr.strip()}"
            )
        stripped = proc.stdout.strip()
        try:
            return int(stripped)
        except ValueError:
            raise PROpenerError(
                f"gh pr create produced non-integer stdout: {stripped!r}"
            )
```

- [ ] **Step 2: Narrow the runner's exception handler**

In `harness/lib/runner.py`, replace the ii.2 placeholder:

```python
        except (GitOpsError, Exception) as exc:  # narrowed to PROpenerError in ii.3
```

with:

```python
        except (GitOpsError, PROpenerError) as exc:
```

And update the import in `runner.py`:

```python
from harness.lib.pr_opener import PROpener, PROpenerError
```

- [ ] **Step 3: Run tests**

Run: `pytest -q`
Expected: all tests pass, including the three new `GhPROpener` tests.

### Task 18: Commit ii.3

- [ ] **Step 1: Commit**

```bash
git add harness/lib/pr_opener.py harness/lib/runner.py tests/test_gh_pr_opener.py
git commit -m "$(cat <<'EOF'
feat(harness): add GhPROpener

Thin wrapper around `gh pr create --json number -q .number`. Assumes
the branch exists locally and on origin (runner's git_ops guarantees
this). Raises PROpenerError with captured stderr on non-zero exit; the
runner narrows its git-or-pr exception catch to (GitOpsError,
PROpenerError) now that PROpenerError exists.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group ii.4: `ClaudeSkillExecutor` + unattended framing

Ends with commit `feat(harness): add ClaudeSkillExecutor and unattended framing`.

### Task 19: Create framing prompt + `claude` argv assembly

**Files:**
- Create: `harness/prompts/__init__.py`
- Create: `harness/prompts/unattended_framing.v1.md`

- [ ] **Step 1: Create the prompts package**

Create `harness/prompts/__init__.py` as an empty file.

- [ ] **Step 2: Write the framing prompt**

Create `harness/prompts/unattended_framing.v1.md`:

```markdown
You are running unattended as part of the tokenman harness.

Rules:
- No clarifying questions. Proceed with your best interpretation, or stop with no changes if genuinely blocked.
- Stay within the scope declared by the skill you are invoking. Do not make changes outside that scope.
- If the skill is inapplicable to this repository (e.g. the target file doesn't exist, or no change is warranted), stop without editing any files.
- Do not modify `.tokenman/`, `.github/`, or `.claude/`. Read them only if the skill needs them for context.
- Make your change atomically: prefer a single coherent edit over many small ones.
- When complete, summarize what you changed (or why you did nothing) in your final message.
```

- [ ] **Step 3: Update `pyproject.toml` to include the prompts package in the installed files**

The existing `[tool.setuptools.packages.find]` stanza uses `include = ["harness*"]`, which already covers `harness.prompts`. Non-Python files (the `.md`) need `setuptools` to be told explicitly. Add a new stanza at the bottom of `pyproject.toml`:

```toml
[tool.setuptools.package-data]
"harness.prompts" = ["*.md"]
```

Re-install in editable mode to pick up the change:
```bash
pip install -e '.[dev]' -q
```

### Task 20: Write the failing `ClaudeSkillExecutor` mock tests

**Files:**
- Create: `tests/test_claude_skill_executor_mock.py`

- [ ] **Step 1: Create the test file**

```python
"""Unit tests for ClaudeSkillExecutor — plumbing only (subprocess mocked)."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from harness.lib.skill_executor import ClaudeSkillExecutor


REPO_ROOT = Path(__file__).parent.parent


def _make_skill_dir(tmp_path: Path) -> Path:
    """A minimal skill directory with a SKILL.md placeholder."""
    d = tmp_path / "skills" / "readme-maintainer"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(
        "# readme-maintainer\n\nEdit README.md.\n"
    )
    return d


def _make_repo_dir(tmp_path: Path) -> Path:
    d = tmp_path / "repo"
    d.mkdir()
    (d / "README.md").write_text("# Title\n\noriginal body\n")
    return d


def test_claude_invocation_argv_and_env(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    json_stdout = json.dumps({
        "role": "assistant",
        "result": "no-op, nothing to do",
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
        },
    })

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        # First call is `claude -p ...`; second is `diff -ruN ...`.
        m.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout=json_stdout, stderr=""),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]
        executor = ClaudeSkillExecutor(claude_bin="claude", timeout_s=60)
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    # claude call: assert argv shape
    claude_call = m.call_args_list[0]
    argv = claude_call.args[0]
    assert argv[0] == "claude"
    assert "-p" in argv
    assert "--output-format" in argv and "json" in argv
    assert "--append-system-prompt" in argv
    # cwd is the working copy, inside scratch
    assert claude_call.kwargs["cwd"].endswith(str(scratch / "working"))
    # timeout passed
    assert claude_call.kwargs["timeout"] == 60
    # user prompt names the skill
    assert any("readme-maintainer" in a for a in argv)

    # Working copy exists and has the skill overlaid at .claude/skills/<name>
    assert (scratch / "working" / "README.md").exists()
    assert (scratch / "working" / ".claude" / "skills" / "readme-maintainer" / "SKILL.md").exists()

    # Result fields
    assert result.prompt_version == "harness-v1"
    assert result.tokens == 150
    assert result.exit_code == 0
    assert result.proposed_diff_path is None  # diff stdout was empty
    assert "no-op" in result.summary.lower() or "nothing" in result.summary.lower()


def test_claude_tokens_sum_with_cache_fields(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    json_stdout = json.dumps({
        "role": "assistant",
        "result": "stopped",
        "usage": {
            "input_tokens": 10,
            "output_tokens": 20,
            "cache_creation_input_tokens": 100,
            "cache_read_input_tokens": 200,
        },
    })

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout=json_stdout, stderr=""),
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        ]
        executor = ClaudeSkillExecutor()
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    assert result.tokens == 10 + 20 + 100 + 200


def test_claude_produces_diff_when_working_differs(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    json_stdout = json.dumps({
        "role": "assistant",
        "result": "added a section",
        "usage": {"input_tokens": 1, "output_tokens": 1},
    })
    fake_diff = (
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1 +1,2 @@\n"
        " # Title\n"
        "+## New\n"
    )

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout=json_stdout, stderr=""),
            subprocess.CompletedProcess(args=[], returncode=1, stdout=fake_diff, stderr=""),
            # diff exits 1 when differences exist; that's not an error for us.
        ]
        executor = ClaudeSkillExecutor()
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    assert result.proposed_diff_path is not None
    assert (scratch / "proposed.diff").read_text() == fake_diff
    assert (scratch / "proposed.md").exists()


def test_claude_timeout_surfaces_as_error(tmp_path: Path) -> None:
    skill = _make_skill_dir(tmp_path)
    repo = _make_repo_dir(tmp_path)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    with patch("harness.lib.skill_executor.subprocess.run") as m:
        m.side_effect = subprocess.TimeoutExpired(cmd=["claude"], timeout=1)
        executor = ClaudeSkillExecutor(timeout_s=1)
        result = executor.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    assert result.exit_code == -1
    assert "timed out" in result.stderr
    assert result.proposed_diff_path is None
```

- [ ] **Step 2: Run; expect import failure**

Run: `pytest tests/test_claude_skill_executor_mock.py -v`
Expected: FAIL — `ImportError: cannot import name 'ClaudeSkillExecutor'`.

### Task 21: Implement `ClaudeSkillExecutor`

**Files:**
- Modify: `harness/lib/skill_executor.py`

- [ ] **Step 1: Add imports and the class**

Append to `harness/lib/skill_executor.py` (after the existing `StubSkillExecutor`):

```python
import json
import shutil
from importlib.resources import files


_FRAMING_RESOURCE = files("harness.prompts") / "unattended_framing.v1.md"


def _load_framing() -> str:
    return _FRAMING_RESOURCE.read_text(encoding="utf-8")


class ClaudeSkillExecutor:
    """Runs `claude -p` against a scratch copy of the repo and computes
    a proposed diff.

    Phase 1.2b-ii. Satisfies the SkillExecutor Protocol.
    """

    def __init__(
        self,
        claude_bin: str = "claude",
        timeout_s: int = 600,
        prompt_version: str = "harness-v1",
        extra_env: Optional[dict[str, str]] = None,
        framing_text: Optional[str] = None,
    ) -> None:
        self._claude_bin = claude_bin
        self._timeout_s = timeout_s
        self._prompt_version = prompt_version
        self._extra_env = dict(extra_env) if extra_env else {}
        self._framing = framing_text if framing_text is not None else _load_framing()

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult:
        working = scratch_dir / "working"
        shutil.copytree(
            repo_dir,
            working,
            ignore=shutil.ignore_patterns(".git", ".tokenman"),
        )
        skill_dst = working / ".claude" / "skills" / skill_dir.name
        shutil.copytree(skill_dir, skill_dst, dirs_exist_ok=True)

        user_prompt = (
            f"Invoke the {skill_dir.name} skill. Edit files in place. "
            "When complete, stop."
        )
        argv = [
            self._claude_bin,
            "-p",
            "--output-format", "json",
            "--append-system-prompt", self._framing,
            user_prompt,
        ]
        env = {**os.environ, **self._extra_env}

        try:
            proc = subprocess.run(
                argv,
                cwd=str(working),
                env=env,
                capture_output=True,
                text=True,
                timeout=self._timeout_s,
                check=False,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            exit_code = proc.returncode
        except subprocess.TimeoutExpired as e:
            stdout = e.stdout or ""
            stderr = (e.stderr or "") + f"\n[executor] claude -p timed out after {self._timeout_s}s\n"
            exit_code = -1

        summary, tokens = self._parse_json_output(stdout, exit_code)

        diff_proc = subprocess.run(
            [
                "diff", "-ruN",
                "--exclude=.claude",
                "--exclude=.git",
                "--exclude=.tokenman",
                str(repo_dir), str(working),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        # `diff` returns 1 if differences exist; 0 if identical; >=2 is an error.
        if diff_proc.returncode >= 2:
            stderr += f"\n[executor] diff failed: {diff_proc.stderr.strip()}"
        diff_output = diff_proc.stdout
        diff_path: Optional[Path] = None
        if diff_output.strip():
            diff_path = scratch_dir / "proposed.diff"
            diff_path.write_text(diff_output)

        md_path = scratch_dir / "proposed.md"
        md_path.write_text(summary + "\n")

        return ExecutionResult(
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            proposed_diff_path=diff_path,
            proposed_md_path=md_path,
            summary=summary,
            prompt_version=self._prompt_version,
            tokens=tokens,
        )

    @staticmethod
    def _parse_json_output(stdout: str, exit_code: int) -> tuple[str, int]:
        """Return (summary, tokens) from claude -p --output-format json.

        Defensive: falls back to the first non-empty stdout line for
        summary if JSON parsing fails.
        """
        try:
            doc = json.loads(stdout)
        except json.JSONDecodeError:
            first = next((ln for ln in stdout.splitlines() if ln.strip()),
                         f"claude: exit {exit_code}")
            return first, 0

        summary = (
            doc.get("result")
            or doc.get("content")
            or doc.get("message")
            or f"claude: exit {exit_code}"
        )
        usage = doc.get("usage") or {}
        tokens = (
            int(usage.get("input_tokens", 0))
            + int(usage.get("output_tokens", 0))
            + int(usage.get("cache_creation_input_tokens", 0))
            + int(usage.get("cache_read_input_tokens", 0))
        )
        return summary, tokens
```

- [ ] **Step 2: Run the mock tests**

Run: `pytest tests/test_claude_skill_executor_mock.py -v`
Expected: all four tests pass.

- [ ] **Step 3: Run the full suite**

Run: `pytest -q`
Expected: green.

### Task 22: Register the `live` marker

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add the marker config**

Append (or extend the existing `[tool.pytest.ini_options]` block) to register the custom `live` marker:

```toml
[tool.pytest.ini_options]
markers = [
    "live: tests that invoke a real external service (claude, gh). Requires TOKENMAN_LIVE=1.",
]
```

If `[tool.pytest.ini_options]` already exists, merge — don't duplicate the header.

- [ ] **Step 2: Add a `conftest.py` auto-skip for `live` when `TOKENMAN_LIVE` is unset**

Create `tests/conftest.py` (or edit if it already exists):

```python
import os
import pytest


def pytest_collection_modifyitems(config, items):
    if os.environ.get("TOKENMAN_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="set TOKENMAN_LIVE=1 to run live tests")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)
```

### Task 23: Write the live smoke test (skipped in CI)

**Files:**
- Create: `tests/test_claude_skill_executor_live.py`

- [ ] **Step 1: Write the live test**

```python
"""Opt-in live test that actually calls `claude -p`.

Skipped unless TOKENMAN_LIVE=1 (configured in tests/conftest.py).
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from harness.lib.skill_executor import ClaudeSkillExecutor


pytestmark = pytest.mark.live


REPO_ROOT = Path(__file__).parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "readme-maintainer"  # added in ii.7
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def test_readme_maintainer_runs_without_crashing(tmp_path: Path) -> None:
    if not SKILL_DIR.exists():
        pytest.skip("skills/readme-maintainer/ not yet present (see ii.7)")

    repo = tmp_path / "repo"
    shutil.copytree(FIXTURE, repo)
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    executor = ClaudeSkillExecutor(timeout_s=600)
    result = executor.execute(skill_dir=SKILL_DIR, repo_dir=repo, scratch_dir=scratch)

    # Either claude produced a diff, or it chose not to — both are valid outcomes.
    assert result.exit_code == 0, f"claude exited nonzero: {result.stderr}"
    if result.proposed_diff_path is not None:
        diff = result.proposed_diff_path.read_text()
        assert "README.md" in diff, "skill should scope to README.md only"
    assert result.tokens > 0, "live run should report a nonzero token count"
```

- [ ] **Step 2: Confirm it's skipped in the normal run**

Run: `pytest tests/test_claude_skill_executor_live.py -v`
Expected: `SKIPPED [1]`.

- [ ] **Step 3: Confirm it actually runs when enabled (optional — can wait until ii.7 lands the skill)**

```bash
TOKENMAN_LIVE=1 pytest tests/test_claude_skill_executor_live.py -v
```
Expected: the test body runs. If `skills/readme-maintainer/` is not present yet (ii.7), the test is internally `pytest.skip`-ed; that's fine. Re-run after ii.7 and expect PASS if you have `claude` logged in.

### Task 24: Commit ii.4

- [ ] **Step 1: Commit**

```bash
git add \
  harness/prompts/__init__.py \
  harness/prompts/unattended_framing.v1.md \
  harness/lib/skill_executor.py \
  pyproject.toml \
  tests/conftest.py \
  tests/test_claude_skill_executor_mock.py \
  tests/test_claude_skill_executor_live.py
git commit -m "$(cat <<'EOF'
feat(harness): add ClaudeSkillExecutor and unattended framing

ClaudeSkillExecutor satisfies the SkillExecutor Protocol by copying
repo_dir -> scratch/working, overlaying skill_dir into
working/.claude/skills/<name>/, invoking `claude -p --output-format
json --append-system-prompt <framing>`, and computing a diff between
the original repo and the working copy (excluding .claude, .git,
.tokenman).

Framing lives versioned at harness/prompts/unattended_framing.v1.md;
bumping content means a v2.md file and a new prompt_version.

Unit tests use subprocess mocks (4 tests). An opt-in live test is
scaffolded but gated behind TOKENMAN_LIVE=1 via tests/conftest.py;
the recorded-capture replay test lands in ii.5.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group ii.5: recorded `claude` output + replay test

Ends with commit `test(harness): add recorded claude-output fixture and replay test`.

### Task 25: Capture a real invocation

This task requires running `claude` live on the implementer's machine. If the implementer does not have a working `claude` login, commit a hand-crafted fixture that matches the documented JSON shape and flag it in the commit message.

**Files:**
- Create: `tests/fixtures/claude-captures/README.md`
- Create: `tests/fixtures/claude-captures/readme-maintainer.json`

- [ ] **Step 1: Create the capture directory**

```bash
mkdir -p tests/fixtures/claude-captures
```

- [ ] **Step 2: Capture live output** (optional if ii.7 has not landed)

If `skills/readme-maintainer/` exists, run:

```bash
TOKENMAN_LIVE=1 python - <<'PY'
import shutil, tempfile, subprocess, json
from pathlib import Path

from harness.lib.skill_executor import ClaudeSkillExecutor

repo_root = Path.cwd()
skill = repo_root / "skills" / "readme-maintainer"
fixture = repo_root / "tests" / "fixtures" / "tiny-python-repo"

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    repo = td / "repo"
    shutil.copytree(fixture, repo)
    scratch = td / "scratch"
    scratch.mkdir()

    ex = ClaudeSkillExecutor(timeout_s=300)
    result = ex.execute(skill_dir=skill, repo_dir=repo, scratch_dir=scratch)

    Path("tests/fixtures/claude-captures/readme-maintainer.json").write_text(result.stdout)
    print("captured:", result.tokens, "tokens;", "diff" if result.proposed_diff_path else "no-diff")
PY
```

If you don't have `claude` live, skip the live capture and hand-write the fixture using this structure:

```json
{
  "type": "result",
  "subtype": "success",
  "result": "Added a brief Usage section to README.md.",
  "usage": {
    "input_tokens": 1245,
    "output_tokens": 312,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  },
  "duration_ms": 8120,
  "num_turns": 4
}
```

(Flag in the commit message that the fixture is synthetic and mark it as "replace when we capture a real run.")

- [ ] **Step 3: Write the capture README**

```markdown
# `claude -p --output-format json` captures

Each file is a recorded `stdout` from a real (or synthetic) invocation.
Used by `tests/test_claude_skill_executor_replay.py` to validate the
parser against real JSON shape without re-spending tokens.

To refresh: set `TOKENMAN_LIVE=1` and re-run the capture snippet in
`docs/superpowers/plans/2026-04-18-phase-1-2b-real-skill-integration.md`
Task 25 Step 2.
```

### Task 26: Write the replay test

**Files:**
- Create: `tests/test_claude_skill_executor_replay.py`

- [ ] **Step 1: Write the test**

```python
"""Replays a recorded `claude -p --output-format json` stdout through
ClaudeSkillExecutor._parse_json_output. Guards the parser against
JSON-shape drift without spending real tokens.
"""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.skill_executor import ClaudeSkillExecutor


CAPTURE_PATH = (
    Path(__file__).parent / "fixtures" / "claude-captures" / "readme-maintainer.json"
)


def test_parse_real_or_synthetic_capture() -> None:
    raw = CAPTURE_PATH.read_text()
    summary, tokens = ClaudeSkillExecutor._parse_json_output(raw, exit_code=0)

    # The capture is either synthetic (see Task 25 Step 2) or real, but in
    # either case the following invariants must hold.
    assert isinstance(summary, str) and summary.strip(), "summary must be non-empty string"
    assert tokens > 0, "tokens must be positive for a real/synthetic capture"

    # The usage block should have been consumable.
    doc = json.loads(raw)
    usage = doc.get("usage", {})
    expected = (
        int(usage.get("input_tokens", 0))
        + int(usage.get("output_tokens", 0))
        + int(usage.get("cache_creation_input_tokens", 0))
        + int(usage.get("cache_read_input_tokens", 0))
    )
    assert tokens == expected
```

- [ ] **Step 2: Run**

Run: `pytest tests/test_claude_skill_executor_replay.py -v`
Expected: PASS.

- [ ] **Step 3: Full suite**

Run: `pytest -q`
Expected: green.

### Task 27: Commit ii.5

- [ ] **Step 1: Commit**

```bash
git add tests/fixtures/claude-captures/README.md tests/fixtures/claude-captures/readme-maintainer.json tests/test_claude_skill_executor_replay.py
git commit -m "$(cat <<'EOF'
test(harness): add recorded claude-output fixture and replay test

Replays a captured `claude -p --output-format json` stdout through
_parse_json_output. Guards the parser against JSON-shape drift without
spending tokens on every test run. Capture instructions live in the
Phase 1.2b plan (Task 25); refresh any time the shape changes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

If the fixture was synthesized rather than live-captured, note it in the commit message body: `Fixture is currently synthetic; replace with a real capture when claude is available.`

---

## Commit group ii.6: `python -m harness.run` CLI

Ends with commit `feat(harness): add python -m harness.run CLI`.

### Task 28: Write the failing CLI tests

**Files:**
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write the test**

```python
"""End-to-end test for the harness.run CLI (subprocess invocation)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def test_cli_dry_run_produces_ledger_entry(tmp_path: Path) -> None:
    # Prepare a tmp consumer repo, pre-init'd as a git repo w/ bare remote so
    # the runner's git_ops can apply/push a dry-run branch.
    import shutil
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name",  "seed"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "seed"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True)
    subprocess.run(["git", "-C", str(repo), "push", "-u", "origin", "main"], check=True, capture_output=True)

    env = {**os.environ}
    proc = subprocess.run(
        [
            sys.executable, "-m", "harness.run",
            "--skill", "readme-maintainer",
            "--repo", str(repo),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(REPO_ROOT),  # so recommended-skills.yaml resolves
    )

    assert proc.returncode == 0, f"stderr: {proc.stderr}"

    ledger_path = repo / ".tokenman" / "ledger.jsonl"
    assert ledger_path.is_file(), "ledger file must be created"
    lines = [ln for ln in ledger_path.read_text().splitlines() if ln.strip()]
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["run_id"] == "r-0001"
    assert entry["skill"] == "readme-maintainer"
    assert entry["status"] in {"pr_opened", "no_change"}

    # stdout ends with the compact JSON entry
    last_stdout_line = [ln for ln in proc.stdout.splitlines() if ln.strip()][-1]
    assert json.loads(last_stdout_line) == entry
```

- [ ] **Step 2: Run**

Run: `pytest tests/test_cli.py -v`
Expected: FAIL with `No module named harness.run`.

### Task 29: Implement the CLI

**Files:**
- Create: `harness/run/__init__.py`
- Create: `harness/run/__main__.py`

- [ ] **Step 1: Create the package**

`harness/run/__init__.py` — empty.

- [ ] **Step 2: Write the entrypoint**

Create `harness/run/__main__.py`:

```python
"""`python -m harness.run` — runs one skill against a consumer repo.

Thin wrapper around harness.lib.runner.run_skill. Resolves skill_dir
from recommended-skills.yaml. --dry-run swaps ClaudeSkillExecutor for
the stub and GhPROpener for FakePROpener — useful for local iteration
or smoke testing without spending tokens or opening real PRs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import yaml  # PyYAML is not yet a dep — add to pyproject below.

from harness.lib import runner
from harness.lib.pr_opener import FakePROpener, GhPROpener
from harness.lib.skill_executor import ClaudeSkillExecutor, StubSkillExecutor


def _repo_root() -> Path:
    """Return the tokenman library repo root (where recommended-skills.yaml lives).

    The CLI is invoked from the consumer's repo, but the catalog lives in
    the tokenman library install. We find it by walking up from this
    module's location to find recommended-skills.yaml.
    """
    here = Path(__file__).resolve()
    for candidate in [here.parent.parent.parent, *here.parents]:
        if (candidate / "recommended-skills.yaml").is_file():
            return candidate
    raise RuntimeError("recommended-skills.yaml not found; is tokenman installed correctly?")


def _resolve_skill_dir(skill_name: str) -> Path:
    root = _repo_root()
    catalog_path = root / "recommended-skills.yaml"
    catalog = yaml.safe_load(catalog_path.read_text()) or {}
    entry = catalog.get(skill_name)
    if entry is None:
        raise SystemExit(f"skill {skill_name!r} not in recommended-skills.yaml")
    source = entry.get("source")
    if source is None:
        raise SystemExit(f"skill {skill_name!r} has no 'source' field")
    if source.startswith("./"):
        return (root / source[2:]).resolve()
    raise SystemExit(f"only local (./) sources are supported in 1.2b; got {source!r}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.run")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--ledger-path", default=None)
    parser.add_argument("--runs-dir", default=None)
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--base-branch", default="main")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    ledger_path = Path(args.ledger_path) if args.ledger_path else repo / ".tokenman" / "ledger.jsonl"
    runs_dir = Path(args.runs_dir) if args.runs_dir else repo / ".tokenman" / "runs"

    skill_dir = _resolve_skill_dir(args.skill)

    if args.dry_run:
        # Stub executor in dry-run mode: point it at the real skill_dir's
        # parent where a stub.sh lives? Simpler: use the known stub skill
        # at tests/fixtures/skills/stub-readme/ with STUB_MODE=propose_diff.
        root = _repo_root()
        stub_skill = root / "tests" / "fixtures" / "skills" / "stub-readme"
        executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
        pr_opener = FakePROpener(sink_dir=runs_dir.parent / "dry-run-prs")
        effective_skill_dir = stub_skill
        effective_skill_name = args.skill  # reported in the ledger as the real name
    else:
        executor = ClaudeSkillExecutor(claude_bin=args.claude_bin)
        pr_opener = GhPROpener(repo_dir=repo, base_branch=args.base_branch)
        effective_skill_dir = skill_dir
        effective_skill_name = args.skill

    entry = runner.run_skill(
        skill_dir=effective_skill_dir,
        repo_dir=repo,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name=effective_skill_name,
        base_branch=args.base_branch,
    )
    print(json.dumps(entry, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Add `PyYAML` to dev deps**

Edit `pyproject.toml`. In the `[project.optional-dependencies]` block (`dev = [...]`), add `pyyaml`:

```toml
dev = [
    "pytest",
    "jsonschema",
    "pyyaml",
]
```

- [ ] **Step 4: Seed a minimal catalog for the CLI test**

`tests/test_cli.py` invokes the CLI with `--skill readme-maintainer`. The real catalog entry lands in ii.7. For ii.6, temporarily add the entry so the CLI test can resolve the name.

Edit `recommended-skills.yaml` (it currently has only comments). Add at the bottom:

```yaml
readme-maintainer:
  source: ./skills/readme-maintainer
  version: 0.1.0
  tier: starter
  blast_radius: low
  typical_tokens_per_run: 15000
  description: Keeps README aligned with actual repo contents.
  default_cadence: on-change
  evaluator_strictness: medium
```

This duplicates ii.7's planned addition. Ii.7's commit simply becomes "skill content + catalog was already seeded"; the entry stays.

- [ ] **Step 5: Re-install to pick up PyYAML**

```bash
pip install -e '.[dev]' -q
```

- [ ] **Step 6: Run CLI tests**

Run: `pytest tests/test_cli.py -v`
Expected: PASS. Entry has `run_id=r-0001`, `status="pr_opened"` (dry-run stub writes a diff that applies to fixture's README), and the stdout last line equals the ledger entry.

If the stub's canned diff doesn't apply to the fixture's `README.md`, update `tests/fixtures/skills/stub-readme/stub.sh` so it emits a diff that applies cleanly — same tweak as ii.2 Step 4.

- [ ] **Step 7: Full suite**

Run: `pytest -q`
Expected: green.

### Task 30: Commit ii.6

- [ ] **Step 1: Commit**

```bash
git add \
  harness/run/__init__.py \
  harness/run/__main__.py \
  pyproject.toml \
  recommended-skills.yaml \
  tests/test_cli.py
git commit -m "$(cat <<'EOF'
feat(harness): add python -m harness.run CLI

Thin argparse wrapper around runner.run_skill. Resolves skill_dir from
recommended-skills.yaml, constructs ClaudeSkillExecutor + GhPROpener
(or Stub + Fake under --dry-run), invokes the runner, prints the
ledger entry as JSON on stdout. --dry-run points at the stub-readme
fixture so local iteration costs zero tokens and opens zero PRs.

Also: add PyYAML as a dev dep for catalog loading, and seed
recommended-skills.yaml with the readme-maintainer entry (skill
content itself lands in ii.7; the catalog is harmless to seed early).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group ii.7: first skill + bootstrap docs

Ends with commit `feat(skills): add in-tree readme-maintainer skill and catalog entry`.

### Task 31: Create the `skills/` bootstrap directory and README

**Files:**
- Create: `skills/README.md`
- Create: `skills/readme-maintainer/SKILL.md`

- [ ] **Step 1: Write `skills/README.md`**

```markdown
# `skills/` — bootstrap directory

Temporary. This directory is a **bootstrap posture**: `readme-maintainer`
lives in-tree during Phase 1.2b so the harness has a real skill to
invoke without depending on an external repository that doesn't exist
yet.

Spec §5.1 says tokenman **ships zero skills**. This directory violates
that principle on purpose and on a deadline: `readme-maintainer` must
be split out to a standalone repository before Phase 3 opens dogfood
runs against the library itself.

Do not add more skills here. Real skills live in their own repos and
are pinned in `recommended-skills.yaml` by URL.
```

- [ ] **Step 2: Write `skills/readme-maintainer/SKILL.md`**

```markdown
---
name: readme-maintainer
description: Keep the repo's README.md aligned with the actual contents of the repo.
---

# readme-maintainer

**Version:** 0.1.0
**Source:** tokenman library, `skills/readme-maintainer/` (temporary — see `skills/README.md`)

## Scope

Operates on `README.md` only. Does not read or modify other files.

## Shape

In-place edit. Prefer additive changes (new sections) over rewrites. If
the README already describes the repo accurately, stop without edits.

## Size limit

Diff must be ≤ ~100 lines. If a bigger change is warranted, stop and
surface the observation in your final message instead of making the
edit.

## Deterministic gate hints

- Only `README.md` should appear in the diff.
- No new files.
- No deletions of entire top-level sections without an explicit reason.

## Evaluator criteria (medium strictness)

- Changes stay scoped to `README.md`.
- Additions are factually grounded in other repo contents (do not
  invent features).
- Tone is consistent with the existing README.

## Typical token budget

~15 000 tokens per run (generator + evaluator combined).

## Instructions

When invoked:

1. Read `README.md`.
2. Read the repo structure (top-level files and directories) to
   compare what's documented against what's present.
3. If the README omits something significant (e.g. missing `Usage`,
   `Install`, or `Development` section that the repo clearly supports),
   propose an addition.
4. If the README is already aligned with the repo, stop without edits
   and say so in your final message.
5. Stay within the size limit. If you think a bigger change is needed,
   summarize the finding instead of making it.
```

- [ ] **Step 3: Confirm the catalog already points here**

Run: `grep -A1 "^readme-maintainer:" recommended-skills.yaml`
Expected: shows `source: ./skills/readme-maintainer` (seeded in ii.6).

### Task 32: Smoke the live flow if `claude` is available

- [ ] **Step 1: Run the live test**

```bash
TOKENMAN_LIVE=1 pytest tests/test_claude_skill_executor_live.py -v
```
Expected: PASS (runs a real `claude -p` against the skill on the tiny-python-repo fixture). If `claude` is not available, skip — note it in the commit message.

- [ ] **Step 2: Re-capture the recorded fixture if it was synthetic**

If Task 25 used a synthesized fixture, redo Task 25 Step 2 now against the real skill, and `git add tests/fixtures/claude-captures/readme-maintainer.json` for the commit.

### Task 33: Commit ii.7

- [ ] **Step 1: Commit**

```bash
git add skills/README.md skills/readme-maintainer/SKILL.md
# also add tests/fixtures/claude-captures/readme-maintainer.json if refreshed in Task 32
git commit -m "$(cat <<'EOF'
feat(skills): add in-tree readme-maintainer skill and catalog entry

skills/ is a temporary bootstrap (see skills/README.md); the
readme-maintainer skill will move to a standalone repo before Phase 3
dogfood opens. Catalog entry in recommended-skills.yaml was seeded in
ii.6 alongside the CLI; this commit lands the SKILL.md content itself.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group ii.8: functional workflow template

Ends with commit `feat(workflow): make tokenman.yml.template consumer-deployable`.

### Task 34: Rewrite the workflow template

**Files:**
- Modify: `harness/workflows/tokenman.yml.template`

- [ ] **Step 1: Replace the Phase 0 stub**

Overwrite `harness/workflows/tokenman.yml.template` with:

```yaml
# TEMPLATE — installed into consumer repos at `/tokenman init` as
# .github/workflows/tokenman.yml. This file in the library repo never
# runs; the installed copy on a consumer does.
#
# Phase 1.2b-ii: workflow_dispatch only. No PAUSE/cooldown/budget/lock
# checks yet (those are Phase 2). No schedule yet.
#
# Requires: secrets.ANTHROPIC_API_KEY configured on the consumer repo.

name: tokenman
on:
  workflow_dispatch:
    inputs:
      skill:
        description: Skill to run (must exist in recommended-skills.yaml)
        required: true
        default: readme-maintainer

permissions:
  contents: write
  pull-requests: write

jobs:
  tokenman-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install tokenman harness
        run: pip install git+https://github.com/verky/tokenman.git@main

      - name: Install claude CLI
        # TODO(1.2b-impl): resolve the actual install command at
        # implementation time. Candidates include:
        #   npm install -g @anthropic-ai/claude-code
        #   curl -sSL https://claude.ai/install | sh
        # Verify the chosen command during the manual smoke step.
        run: |
          echo "TODO: install claude here"
          exit 1   # fail fast until the TODO is resolved

      - name: Configure git identity for bot commits
        run: |
          git config --global user.email "tokenman-bot@users.noreply.github.com"
          git config --global user.name  "tokenman-bot"

      - name: Run tokenman
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN:          ${{ secrets.GITHUB_TOKEN }}
        run: |
          python -m harness.run \
            --skill "${{ inputs.skill }}" \
            --repo .

      - name: Upload run artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: tokenman-run-${{ github.run_id }}
          path: .tokenman/runs/
          if-no-files-found: warn
```

- [ ] **Step 2: Sanity-check with `actionlint` (optional)**

If `actionlint` is installed locally, run it:
```bash
actionlint harness/workflows/tokenman.yml.template
```
Expected: no errors. Skip if not installed.

### Task 35: Manual smoke plan (human step; not automated)

The smoke gets recorded in the 1.2b-ii PR description, not in the repo.

Checklist to execute before merging:

- [ ] Create a throwaway GitHub repo (e.g. `verky/tokenman-smoke-test`).
- [ ] Add a minimal `README.md` + maybe one Python file so `readme-maintainer` has something to comment on.
- [ ] Add the contents of `harness/workflows/tokenman.yml.template` as `.github/workflows/tokenman.yml`.
- [ ] Resolve the `TODO(1.2b-impl)` install step — commit the actual `claude` install command.
- [ ] Add a `secrets.ANTHROPIC_API_KEY` on the repo.
- [ ] Trigger the workflow from the Actions tab (`workflow_dispatch`, skill=readme-maintainer).
- [ ] Confirm: a PR is opened; artifacts are downloadable; PR contains a plausible edit to `README.md`.
- [ ] Capture the PR URL + artifact URL for the 1.2b-ii PR description.
- [ ] Decide whether to land the resolved `claude` install command into the library template now, or leave the TODO with a comment and resolve it inline in each consumer for now.

### Task 36: Commit ii.8

- [ ] **Step 1: Commit**

```bash
git add harness/workflows/tokenman.yml.template
git commit -m "$(cat <<'EOF'
feat(workflow): make tokenman.yml.template consumer-deployable

Replaces the Phase 0 echo stub. workflow_dispatch only (no schedule;
Phase 2 adds that); installs harness via pip git+, installs claude CLI
(TODO placeholder — resolved during manual smoke), configures a bot
git identity, runs python -m harness.run, uploads .tokenman/runs as
artifacts. No PAUSE/cooldown/budget/lock yet (Phase 2).

Manual smoke against a throwaway repo is recorded in the PR
description, not in the repo.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Commit group ii.9: docs + dogfood boundary

Ends with commit `docs: note skills/ forbidden path and bootstrap posture`.

### Task 37: Update `.tokenman/CLAUDE.md`

**Files:**
- Modify: `.tokenman/CLAUDE.md`

- [ ] **Step 1: Read the current file**

Run: `cat .tokenman/CLAUDE.md`
Expected: existing content listing forbidden paths. Locate the list.

- [ ] **Step 2: Add `skills/` to the forbidden list**

Find the sentence or bullet enumerating forbidden paths (e.g. `harness/`, `scoping/`, `onboarding/`, `recommended-skills.yaml`, `pricing.yaml`). Add `skills/` alongside them. Example change — adjust to match the file's actual wording:

Before:
```
Do not modify files in `harness/`, `scoping/`, `onboarding/`,
`recommended-skills.yaml`, or `pricing.yaml` …
```
After:
```
Do not modify files in `harness/`, `scoping/`, `onboarding/`,
`skills/`, `recommended-skills.yaml`, or `pricing.yaml` …
```

### Task 38: Update `CONTRIBUTING.md`

**Files:**
- Modify: `CONTRIBUTING.md`

- [ ] **Step 1: Add a bootstrap-posture note**

Find the section that describes the source/runtime split (if present). Add a paragraph:

```markdown
### `skills/` — temporary bootstrap

`skills/readme-maintainer/` lives in-tree during Phase 1.2b so the
harness has a real skill to invoke before the external skills
ecosystem exists. This is a deliberate, scoped violation of spec §5.1
("tokenman ships zero skills"). It must be split out to a standalone
repo before Phase 3 opens dogfood runs against the library itself.
Do not add more skills here.
```

### Task 39: Update the project `CLAUDE.md` failure log if warranted

**Files:**
- Optional: `CLAUDE.md`

- [ ] **Step 1: Review the "Failure log" section**

If any failure happened during 1.2b-ii (e.g. the recorded-fixture shape needed a correction, or `git apply --index` on symlink-ful fixtures failed), add one bullet under the failure log. Otherwise skip.

### Task 40: Commit ii.9

- [ ] **Step 1: Commit**

```bash
git add .tokenman/CLAUDE.md CONTRIBUTING.md
# optionally CLAUDE.md if a failure-log bullet was added
git commit -m "$(cat <<'EOF'
docs: note skills/ forbidden path and bootstrap posture

.tokenman/CLAUDE.md adds skills/ to the list of source-zone paths
dogfood runs must not touch. CONTRIBUTING.md documents the bootstrap
posture and the commitment to split readme-maintainer out before
Phase 3 dogfood opens.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Finish Part II: push, review, merge

### Task 41: Final suite + imports check

- [ ] **Step 1: Full test run**

Run: `pytest -q`
Expected: all tests pass. `test_claude_skill_executor_live.py` shows SKIPPED (no TOKENMAN_LIVE).

- [ ] **Step 2: Imports check**

Run:
```bash
python3 -c "from harness.lib import ledger, runner, skill_executor, pr_opener, git_ops; \
from harness.lib.skill_executor import ClaudeSkillExecutor; \
from harness.lib.pr_opener import GhPROpener, PROpenerError; \
from harness.lib.git_ops import apply_diff_and_push, GitIdentity, GitOpsError; \
from harness.run import __main__; \
print('OK')"
```
Expected: `OK`.

- [ ] **Step 3: Dry-run CLI against the dev loop**

Run:
```bash
python -m harness.run --skill readme-maintainer --dry-run --repo tests/fixtures/tiny-python-repo
```
Expected: exits 0; prints a JSON ledger entry with `status=pr_opened`; `tests/fixtures/tiny-python-repo/.tokenman/ledger.jsonl` now has a line. Clean up:
```bash
rm -rf tests/fixtures/tiny-python-repo/.tokenman
```
(The fixture is per-CLAUDE.md pristine; the dry-run run dirtied it. For the real test, ii.6 uses a tmp copy.)

- [ ] **Step 4: Push branch**

Ask the user before pushing. If approved:
```bash
git push -u origin phase-1-2b-ii
```

- [ ] **Step 5: Open PR**

```bash
gh pr create --title "feat(harness): 1.2b-ii real skill integration" --body "$(cat <<'EOF'
## Summary
Swaps 1.2a's stub boundary classes for real ones, lands the first cataloged skill, adds a runner CLI, and produces a consumer-deployable workflow template.

- `git_ops` module for branch/apply/commit/push
- `ClaudeSkillExecutor` (copies repo to scratch, overlays skill, runs `claude -p`, diffs the result)
- `GhPROpener` (thin `gh pr create` wrapper; runner has already pushed the branch)
- `python -m harness.run` CLI with `--dry-run` local-iteration mode
- First skill `readme-maintainer` in-tree at `skills/readme-maintainer/` (temporary bootstrap — see `skills/README.md`)
- `recommended-skills.yaml` first entry
- Functional `tokenman.yml.template` (workflow_dispatch, uploads artifacts)
- `.tokenman/CLAUDE.md` adds `skills/` to forbidden paths
- Unattended framing at `harness/prompts/unattended_framing.v1.md`

Mock + recorded-replay tests in CI; one opt-in live test gated behind `TOKENMAN_LIVE=1`.

## Test plan
- [x] `pytest -q` green
- [x] `TOKENMAN_LIVE=1 pytest -m live` green locally against real `claude`
- [ ] Manual `workflow_dispatch` run against a throwaway repo — **PR URL**: <paste>, **artifact URL**: <paste>
- [ ] Reviewer: scan for TODOs, confirm the claude install step was resolved

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Paste the real smoke-run URLs in the PR body before asking for review.

### Task 42: After merge, clean up

- [ ] **Step 1: In main worktree**

```bash
cd ../tokenman
git checkout main
git pull --ff-only
git worktree remove ../tokenman-phase-1-2b-ii
git branch -D phase-1-2b-ii
```

- [ ] **Step 2: Confirm next-session handoff needs updating**

Edit `docs/next-session-prompt.md` for Phase 1.3 (scoping flow). That's a separate task, not part of 1.2b.

---

## Exit criteria checklist

- [ ] All 1.2b-i commits merged to `main`.
- [ ] All 1.2b-ii commits merged to `main`.
- [ ] `pytest -q` on `main` green.
- [ ] `TOKENMAN_LIVE=1 pytest -m live` green locally at least once.
- [ ] One manual `workflow_dispatch` smoke produced a real PR; URLs recorded in 1.2b-ii PR description.
- [ ] `python -c "from harness.lib import ledger, runner, skill_executor, pr_opener, git_ops; from harness.run import __main__; print('OK')"` succeeds.
- [ ] `.tokenman/PAUSE` still present.
- [ ] `.tokenman/CLAUDE.md` lists `skills/` as forbidden.
- [ ] `recommended-skills.yaml` has exactly one entry (`readme-maintainer`).
- [ ] Working tree clean.
