# Phase 1.2a Harness Plumbing — Design

**Date:** 2026-04-18
**Status:** Approved via brainstorming, pending user review of this doc
**Parent spec:** `docs/spec.md` v0.2, §12 "Phase 1 — Wedge + guided onboarding"
**Sub-phase:** 1.2a of Phase 1's four-part decomposition

Phase 1 decomposition recap:
- 1.1 — ledger schema + `status.sh` v1 (DONE, merged at 68c2893)
- **1.2 — linear harness workflow + first skill integration** (in progress)
  - **1.2a — harness plumbing** (this doc): append utility, runner, stub
    skill, fixture wiring. No `claude -p`, no real PR opens, workflow
    template stays a stub.
  - 1.2b — real-skill integration: `ClaudeSkillExecutor`, `GhPROpener`,
    catalog entry, functional `tokenman.yml.template`, runner CLI.
- 1.3 — scoping flow (`tokenman scope`)
- 1.4 — guided onboarding mode

## Purpose

Build and test the end-to-end runner pipeline against a deterministic
stub skill, so that 1.2b's swap to `claude -p` + `gh pr create` changes
only the two boundary classes and nothing in the orchestrator. 1.2a's
output is working Python harness code covered by integration tests — no
workflow changes, no external calls, no runtime activity on the library
repo (PAUSE still on through Phase 2 per spec §12).

Why split 1.2 at all: "linear workflow + first skill integration" bundles
plumbing, claude invocation, PR opening, catalog curation, and workflow
yaml — any single one is a reasonable sub-phase. Locking the plumbing
contract first means 1.2b is a focused integration change, not a mixed
plumbing-plus-integration change.

## Scope decisions (from brainstorming, 2026-04-18)

1. **Split 1.2 into 1.2a (plumbing) + 1.2b (integration).** 1.2a proves
   the end-to-end loop against a deterministic stub. 1.2b replaces the
   stub with a real skill and wires the workflow template.

2. **Language: Python.** Matches 1.1's `pyproject.toml` + `pytest` +
   `jsonschema`. Conditional invariants (pr non-null iff
   `status == "pr_opened"`; `total_tokens = generator.tokens +
   evaluator.tokens`; generator null for skip statuses) are painful in
   bash+jq — they were explicitly deferred from 1.1 for this reason.
   Runner logic (subprocess management, stdout/stderr capture,
   timeouts) is ergonomic in Python. `ubuntu-latest` runners ship
   Python 3 by default, so no consumer-side install cost. `status.sh`
   stays bash — reading a ledger is a jq-shaped problem.

3. **PR opener is mocked in 1.2a.** Factor out a `PROpener` protocol.
   `FakePROpener` returns an incrementing integer and persists the
   would-be PR's arguments to disk for test inspection. `GhPROpener`
   lands in 1.2b. The interface split is design we'll need regardless;
   writing the fake is cheap; the full happy path (run → proposal →
   ledger entry with `pr_opened`) becomes testable in 1.2a.

4. **Stub skill is a subprocess.** `StubSkillExecutor` invokes
   `stub.sh` as a subprocess, matching the real-world subprocess
   boundary `claude -p` will use. Avoids "the stub was fine in-process
   but the real executor has a contract mismatch" bugs.

5. **Stub skill location: `tests/fixtures/skills/`.** Separate from
   `tests/fixtures/tiny-*-repo/`. Repo fixtures stay pristine
   "consumer-shaped" trees; skill fixtures are "what the harness
   exercises". One stub skill runs against any repo fixture.

6. **Stub supports three modes:** `no_change`, `propose_diff`, `crash`.
   Selected by `STUB_MODE` env var. Covers the three runner outcomes
   1.2a has to exercise (no_change, pr_opened, error).

7. **`run_id` allocated from ledger.** Read the last non-blank line,
   parse its `run_id`, increment. Empty/missing ledger → `r-0001`.
   Correct under spec §4.1 serialization; avoids a second source of
   truth drifting against the ledger.

8. **No runner CLI in 1.2a.** Tests invoke the runner as a Python
   function. 1.2b adds a CLI once the workflow template needs an
   entrypoint — CLI design is cleaner with a known caller.

## Architecture

Four Python modules in `harness/lib/`, each behind a narrow interface so
1.2b swaps implementations without touching the orchestrator.

```
    tests / (future 1.2b CLI)
            │  calls
            ▼
    ┌───────────────────┐
    │  runner.py        │  orchestrates one run
    │  run_skill(...)   │
    └─────────┬─────────┘
              │
      ┌───────┼────────────────────────────┐
      │       │                            │
      ▼       ▼                            ▼
  ledger.py  skill_executor.py         pr_opener.py
  append(),  SkillExecutor Protocol    PROpener Protocol
  validate() StubSkillExecutor (1.2a)  FakePROpener (1.2a)
             ClaudeSkillExecutor(1.2b) GhPROpener (1.2b)
```

- **`ledger.py`** — schema-aware append + validation. Enforces
  conditional invariants the JSON Schema cannot express.
- **`runner.py`** — the orchestrator. One public function, `run_skill`,
  implementing the data flow in the next section. Dependencies
  (`SkillExecutor`, `PROpener`, `now`) are injected.
- **`skill_executor.py`** — the subprocess boundary. `StubSkillExecutor`
  in 1.2a; `ClaudeSkillExecutor` in Phase 3+.
- **`pr_opener.py`** — the PR-opening boundary. `FakePROpener` in 1.2a;
  `GhPROpener` in 1.2b.

**Package structure.** `harness/__init__.py` and `harness/lib/__init__.py`
are added, and `pyproject.toml` grows a `[tool.setuptools.packages.find]`
stanza selecting `harness*`. After `pip install -e '.[dev]'`, tests do
`from harness.lib import ledger, runner, skill_executor, pr_opener`.

## Data flow: one run

Single invocation of `run_skill`, happy path:

```
1. Test constructs:
     skill_dir   = tests/fixtures/skills/stub-readme/
     repo_dir    = <tmp copy of tests/fixtures/tiny-python-repo/>
     ledger_path = repo_dir / ".tokenman" / "ledger.jsonl"
     runs_dir    = repo_dir / ".tokenman" / "runs"
     executor    = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
     pr_opener   = FakePROpener(sink_dir=<tmp>)
     now         = lambda: datetime(2026,4,18,12,0,0,tzinfo=UTC)

2. runner.run_skill(...) — single entry point:

   2a. Allocate run_id.
       - ledger.last_run_id(ledger_path) → int | None
       - None → "r-0001"; otherwise increment with zero-padding.

   2b. Start monotonic clock.

   2c. Create artifact dir: runs_dir / run_id /

   2d. Create scratch dir (tempfile.TemporaryDirectory).

   2e. executor.execute(skill_dir, repo_dir, scratch_dir) →
       ExecutionResult(exit_code, stdout, stderr,
                       proposed_diff_path, proposed_md_path, summary).

   2f. Persist subprocess output.
       - stub.stdout and stub.stderr always written into the artifact
         dir (empty file if capture was empty).
       - If the scratch dir contains proposed.diff / proposed.md, copy
         them into the artifact dir.

   2g. Decide status and populate fields.
       - exit_code != 0                      → status="error",
                                               generator=None, pr=None.
       - no proposed.diff produced           → status="no_change",
                                               generator={prompt_version:
                                                 "stub-v1", output_summary:
                                                 executor.summary,
                                                 diff_lines:0, tokens:0},
                                               pr=None.
       - proposed.diff produced              → diff_lines = count of
                                               lines starting with '+'
                                               or '-' excluding file-
                                               header lines ('+++', '---'
                                               with a space or tab after);
                                               call pr_opener.open(title,
                                                 body, branch, diff) →
                                               status="pr_opened",
                                               generator={…, diff_lines},
                                               pr=<int>.

   2h. Stop clock. duration_s = int(elapsed).

   2i. Build ledger entry (dict conforming to LedgerEntry TypedDict):
       run_id, ts (now() → ISO 8601 UTC seconds), skill (from
       skill_name kwarg, default skill_dir.name), status, pr,
       generator, evaluator=None, duration_s,
       total_tokens = (generator["tokens"] if generator else 0),
       verdict=None, verdict_note=None.

   2j. ledger.append(ledger_path, entry):
       - jsonschema validates structure.
       - Conditional invariants validate (listed below).
       - On success: open("a"), write compact JSON + "\n", flush.

   2k. Copy the appended line into runs/<run_id>/ledger.entry
       (written only after successful append; a failed append leaves
        artifacts but no per-run ledger copy, mirroring
        ledger.jsonl's "failed runs have no line").

   2l. Return the entry dict.
```

**Error paths:**

- Stub non-zero exit → `status="error"`, `generator=None`, `pr=None`.
  Ledger entry still written. Artifacts include `stub.stderr` so the
  failure is diagnosable.
- `ledger.append` raises `LedgerInvariantError` → runner lets it
  propagate; the failure is a test-caller problem, not a run outcome.
  `ledger.jsonl` and `ledger.entry` both unchanged.
- `pr_opener.open` raises → runner catches, records `status="error"`,
  leaves the proposed diff in the artifact dir. A failed PR-open is a
  run outcome, not a runner crash.

## Invariants enforced by `ledger.append`

The schema from 1.1 (`harness/lib/ledger.schema.json`) captures shape.
`ledger.append` additionally enforces:

1. **PR ↔ status:** `pr` non-null iff `status == "pr_opened"`.
2. **Generator null-ness by status:**
   - `status` starts with `skipped_` → `generator` must be null.
   - `status == "error"` → `generator` may be null (pre-generator
     failure) *or* populated (generator produced output then erred
     downstream); both valid.
   - All other statuses → `generator` must be populated.
3. **Token sum:**
   `total_tokens == (generator["tokens"] if generator else 0) +
   (evaluator["tokens"] if evaluator else 0)`.
4. **`run_id` monotonicity:** the integer portion of `run_id` must be
   strictly greater than the last non-blank line's `run_id`.
5. **`ts` monotonicity:** the new entry's `ts` ≥ the last entry's `ts`
   (lexicographic compare is valid for ISO 8601 UTC Z-suffix).

Any violation raises `LedgerInvariantError` *before* the line is
written. File state is unchanged on failure.

These invariants live in `ledger.append`, not in a `jsonschema` keyword
extension, because (2) is conditional on a different field (`status`),
and (3)–(5) depend on prior state or on cross-field arithmetic the
JSON Schema Draft 2020-12 vocabulary can't naturally express.

## Files

### Additions

1. **`harness/__init__.py`** — empty
2. **`harness/lib/__init__.py`** — empty
3. **`harness/lib/ledger.py`** (~100 lines)
   - `LedgerEntry` — TypedDict mirroring the schema
   - `LedgerInvariantError(ValueError)`
   - `_load_schema() -> dict` — reads and caches `ledger.schema.json`
   - `validate(entry) -> None` — schema check then conditional invariants
   - `append(ledger_path: Path, entry: LedgerEntry) -> None`
   - `last_run_id(ledger_path: Path) -> int | None` — scans last non-blank
     line, parses `r-NNNN`, returns the integer; returns None if file is
     missing or empty.
4. **`harness/lib/pr_opener.py`** (~40 lines)
   - `class PROpener(Protocol)` — `open(*, title, body, branch, diff) -> int`
   - `class FakePROpener` — monotonic counter (defaults to 1000 so fake
     PR numbers are visually distinct from run_ids). Optional `sink_dir`
     persists each would-be PR's arguments as `pr-<n>.json` for test
     inspection.
5. **`harness/lib/skill_executor.py`** (~60 lines)
   - `@dataclass ExecutionResult(exit_code, stdout, stderr,
     proposed_diff_path: Path | None, proposed_md_path: Path | None,
     summary: str)`
   - `class SkillExecutor(Protocol)` — `execute(skill_dir, repo_dir,
     scratch_dir) -> ExecutionResult`
   - `class StubSkillExecutor(extra_env: dict | None = None)` — runs
     `skill_dir / "stub.sh"` via `subprocess.run(..., cwd=repo_dir,
     env=os.environ | extra_env)`, captures stdout/stderr. Summary =
     first non-empty stdout line, or `"stub-readme: <mode>"` fallback.
6. **`harness/lib/runner.py`** (~120 lines)
   - `run_skill(*, skill_dir, repo_dir, ledger_path, runs_dir,
     executor, pr_opener, skill_name: str | None = None,
     now: Callable[[], datetime] | None = None) -> LedgerEntry`
   - Implements the data flow above. `now` is injectable to keep
     timestamps deterministic in tests.
7. **`tests/fixtures/skills/README.md`** — explains the directory's
   purpose (stub skills, not real ones; separate from `tests/fixtures/`
   repos) and how to add a new stub.
8. **`tests/fixtures/skills/stub-readme/SKILL.md`** — documentation
   only: states that this is a stub, lists the three modes and the
   `STUB_MODE` env var, explicitly notes the runner does not parse it
   in 1.2a.
9. **`tests/fixtures/skills/stub-readme/stub.sh`** (~30 lines, bash) —
   reads `STUB_MODE`, writes canned output into `$1`:
   - `no_change` → prints a summary line; writes nothing.
   - `propose_diff` → prints a summary line; writes a small canned diff
     and a `proposed.md`.
   - `crash` → prints a stderr line; `exit 2`.
   - unknown mode → `exit 3`. Must pass `shellcheck`.
10. **`tests/test_ledger_append.py`** — unit tests for `ledger.append`
    and each invariant.
11. **`tests/test_runner.py`** — integration tests. Each constructs a
    tmp-copied fixture repo, a `FakePROpener` with a test-local `sink_dir`,
    a `StubSkillExecutor` pointing at `stub-readme`, and a fixed `now`.

### Modifications

12. **`pyproject.toml`** — add:
    ```toml
    [tool.setuptools.packages.find]
    where = ["."]
    include = ["harness*"]
    ```
    Dev deps (`pytest`, `jsonschema`) from 1.1 already cover runtime
    needs; no new deps.
13. **`CONTRIBUTING.md`** — add a short note that runtime harness code
    lives under `harness/lib/` and its tests live at `tests/test_*.py`
    alongside the 1.1 schema test.

### Notably NOT modified

- **`.tokenman/CLAUDE.md`** — still forbids `harness/`. Nothing to
  change. PAUSE stays on.
- **`harness/workflows/tokenman.yml.template`** — stays a Phase 0 stub.
  Functional workflow = 1.2b.
- **`harness/lib/ledger.schema.json`** — unchanged. The Python code is
  the schema's first real consumer; the schema itself is already final
  from 1.1.
- **`recommended-skills.yaml`** — still empty. Real catalog entry =
  1.2b.
- **`tests/fixtures/tiny-*-repo/`** — unchanged per `CLAUDE.md`.
- **`tests/test_ledger_schema.py`** — unchanged from 1.1.

## Testing plan

Total after 1.2a: ~18 tests (3 existing schema tests + ~9 ledger.append
tests + ~6 runner integration tests). Runtime a few seconds.

### `tests/test_ledger_append.py`

Unit tests, no subprocess, no fixture repo.

- `test_append_to_missing_ledger_creates_file` — r-0001 entry, parent
  dir exists, ledger.jsonl created with exactly one valid line.
- `test_append_appends_without_clobber` — seed with
  `tests/ledgers/realistic-week.jsonl` copied to tmp; append r-0019;
  last line is new, prior 18 intact.
- `test_schema_violation_rejected` — entry missing `run_id` raises
  `LedgerInvariantError`; file unchanged.
- `test_invariant_pr_requires_pr_opened` — `status="no_change"` with
  `pr=42` raises; `status="pr_opened"` with `pr=None` raises.
- `test_invariant_generator_null_on_skipped` — `status="skipped_cooldown"`
  with non-null generator raises.
- `test_invariant_total_tokens_sum` — generator.tokens=100,
  evaluator=None, total_tokens=99 raises; total_tokens=100 passes.
- `test_invariant_run_id_monotonic` — seeded ledger ending at r-0005;
  append r-0004 raises; append r-0005 raises; append r-0006 passes.
- `test_invariant_ts_monotonic` — same shape for timestamps.
- `test_last_run_id_empty_and_missing` — missing file → None; empty
  file → None; single-entry → that entry's int.

### `tests/test_runner.py`

Integration tests. Each copies `tests/fixtures/tiny-python-repo/` to a
tmp directory so the original fixture stays pristine.

- `test_propose_diff_opens_pr` — STUB_MODE=propose_diff → return value
  has `status="pr_opened"`, `pr` equals FakePROpener's first issued
  number, `generator.diff_lines > 0`; ledger has exactly one line;
  `runs/r-0001/` contains `proposed.diff`, `proposed.md`, `stub.stdout`,
  `stub.stderr`, `ledger.entry`.
- `test_no_change_skips_pr_opener` — STUB_MODE=no_change →
  `status="no_change"`, `pr=None`, `generator.diff_lines=0`,
  `FakePROpener.open` never called, no `proposed.diff` in artifact dir,
  `ledger.entry` present.
- `test_crash_records_error` — STUB_MODE=crash → `status="error"`,
  `generator=None`, `pr=None`, `stub.stderr` contains "crashing on
  purpose", ledger entry validates, FakePROpener never called.
- `test_run_id_allocation_empty_ledger` — r-0001.
- `test_run_id_allocation_existing_ledger` — seed with r-0017, next
  run → r-0018.
- `test_ledger_entry_persisted_only_on_successful_append` — inject a
  `now` that duplicates the seeded last entry's ts; assert the append
  raises, `ledger.jsonl` unchanged, `runs/<id>/ledger.entry` absent,
  but `stub.stdout` / `stub.stderr` present (subprocess did run).

### Manual check

Run `status.sh` from 1.1 against a ledger produced by `test_runner.py`
and confirm it renders cleanly. Not automated; single ad-hoc command,
noted in the PR description.

## Exit criteria

1. `pytest` from repo root exits 0 with ~18 tests passing.
2. `harness.lib.{ledger,runner,skill_executor,pr_opener}` importable
   after `pip install -e '.[dev]'`.
3. `ledger.append` writes only when the entry passes schema *and* all
   five invariants; otherwise raises `LedgerInvariantError` and leaves
   the file unchanged.
4. `run_skill` against `stub-readme` produces correct ledger entries
   for all three modes (`no_change`, `propose_diff`, `crash`) and
   leaves `runs/r-NNNN/` populated per the artifact list in the data
   flow.
5. `shellcheck tests/fixtures/skills/stub-readme/stub.sh` passes.
6. `status.sh` from 1.1 renders cleanly against a ledger produced by
   the new runner (ad-hoc, not automated).
7. `.tokenman/PAUSE` still present. No changes to
   `harness/workflows/tokenman.yml.template` or `.github/workflows/`.
   Dogfood paused.
8. Working tree clean after the four commits.

## What's deliberately NOT in 1.2a

- `ClaudeSkillExecutor` and any `claude -p` invocation (1.2b)
- `GhPROpener` and any real PR creation (1.2b)
- Functional `tokenman.yml.template` (1.2b)
- Runner CLI (`python -m harness.run`) — deferred to 1.2b when the
  workflow template needs an entrypoint
- Catalog entry in `recommended-skills.yaml` — real skill curation
  lands with 1.2b
- Parsing `SKILL.md` for name / scope / shape / size / gate hints —
  stub has a `SKILL.md` for documentation only; the runner does not
  read it in 1.2a. Parsing is deferred until a skill contract need
  materializes (probably Phase 3 when the deterministic gate consumes
  `scope` and `shape`).
- Trigger-check stage (PAUSE check, cooldown, budget caps, open-PR
  lock, review-bandwidth gate) — all Phase 2.
- Deterministic gate (scope / shape / size / forbidden-pattern /
  file-type checks between generator and evaluator) — Phase 3.
- Evaluator stage — Phase 3.
- Retention / GC of `runs/r-NNNN/` dirs — Phase 2 per spec §8.2.
- Locking for concurrent runners — not needed under spec §4.1
  serialization. A lockfile can be added if concurrent runs ever
  become a real requirement.

## Order of commits

Four commits, independently reviewable. Each earlier commit leaves the
working tree in a passing state; the runner tests land with the runner.

1. **`feat(harness): add ledger append utility with invariant enforcement`**
   — `harness/__init__.py`, `harness/lib/__init__.py`,
   `harness/lib/ledger.py`, `pyproject.toml` packages stanza,
   `tests/test_ledger_append.py`. ~9 new ledger tests pass; the 1.1
   schema test continues to pass.

2. **`feat(harness): add skill executor and PR opener abstractions`**
   — `harness/lib/skill_executor.py`, `harness/lib/pr_opener.py`,
   `tests/fixtures/skills/README.md`,
   `tests/fixtures/skills/stub-readme/SKILL.md`,
   `tests/fixtures/skills/stub-readme/stub.sh`. Small focused tests
   for `StubSkillExecutor` end-to-end against the stub (all three
   modes) and for `FakePROpener` counter behavior. No runner yet.

3. **`feat(harness): add runner that orchestrates a single-skill run`**
   — `harness/lib/runner.py`, `tests/test_runner.py`. Integration
   tests land here.

4. **`docs: note harness-lib modules in CONTRIBUTING`** — doc-only.

Each commit uses the trailer:

```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

## Open items

None blocking 1.2a execution. Forward-looking for 1.2b:

1. **`ClaudeSkillExecutor` contract.** Does it invoke `claude -p`
   directly, or through `claude-code-sdk` / similar? Decide with
   1.2b's first real skill integration; the `SkillExecutor` Protocol
   is deliberately minimal so either works.
2. **Runner CLI shape.** `python -m harness.run --skill NAME
   --repo PATH`? Or a `tokenman-run` console script? Decide when the
   workflow template needs it.
3. **Single-skill vs multi-skill invocation.** 1.2a's `run_skill` runs
   one skill. Onboarding mode (1.4) and Phase 4's parallel DAG both
   need a multi-skill orchestrator. That wrapper lives above
   `run_skill`; 1.2a's contract doesn't need to change.
4. **`FakePROpener.sink_dir` discoverability.** For the eventual
   offline-development-loop story (harness dev on fixtures without
   GitHub), having a `FakePROpener` that persists rich PR metadata may
   be useful beyond testing. Not a 1.2a concern.

## Verification (after all four commits)

```bash
# 1. Package installs
pip install -e '.[dev]' -q && echo OK

# 2. Tests pass
pytest -q

# 3. Shellcheck on the stub
shellcheck tests/fixtures/skills/stub-readme/stub.sh && echo OK

# 4. Imports work
python3 -c "from harness.lib import ledger, runner, skill_executor, pr_opener; print('OK')"

# 5. status.sh still renders against a tmp ledger we produce ad hoc
#    (manual step — documented in PR description)

# 6. Working tree clean
git status
```
