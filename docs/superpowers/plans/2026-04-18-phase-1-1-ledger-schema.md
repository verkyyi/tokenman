# Phase 1.1 Ledger Schema Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lock the tokenman ledger schema, rework `status.sh` as `harness/templates/status.sh`, and introduce a pytest-enforced validation test — so Phase 1.2+ runtime code has a stable observability contract.

**Architecture:** Five logical commits, each independently reviewable. Commit 1 writes the canonical JSON Schema and fixtures README. Commit 2 writes two JSONL fixtures (all-statuses enum coverage + realistic-week aggregation). Commit 3 adds root `pyproject.toml` with dev deps and a parameterized pytest test. Commit 4 moves `scripts/status.sh` to `harness/templates/status.sh` and rewrites it for the new schema (ledger-only). Commit 5 updates `CONTRIBUTING.md` and `.tokenman/CLAUDE.md` for the new paths. Task 6 verifies exit criteria.

**Tech Stack:** JSON Schema Draft 2020-12, Python 3.10+, pytest, jsonschema, bash, jq, shellcheck, Git. No new runtime dependencies — all added deps are dev-only (`pyproject.toml [project.optional-dependencies].dev`).

**Design:** `docs/superpowers/specs/2026-04-18-phase-1-1-ledger-schema-design.md`

---

## Scope Check

This plan covers a single, well-bounded sub-phase (Phase 1.1 of the Phase 1 decomposition established during brainstorming). No further decomposition needed. Later sub-phases (1.2 runtime workflow, 1.3 scoping, 1.4 onboarding) get their own design + plan cycles.

---

## File Structure

### Additions
- `harness/lib/ledger.schema.json` — JSON Schema Draft 2020-12, canonical contract
- `harness/templates/status.sh` — bash+jq reader, ledger-only
- `tests/ledgers/README.md` — explains ledger test fixtures
- `tests/ledgers/all-statuses.jsonl` — 10 entries, one per status enum value
- `tests/ledgers/realistic-week.jsonl` — 18 entries, synthetic week
- `tests/test_ledger_schema.py` — pytest parameterized validator
- `pyproject.toml` — repo root, first time; dev optional-dependencies only

### Removals
- `scripts/status.sh` — replaced by `harness/templates/status.sh`
- `scripts/` — directory removed once its only file moves out

### Modifications
- `CONTRIBUTING.md` — add "Running tests" section after "Commit conventions"
- `.tokenman/CLAUDE.md` — remove `scripts/` from the forbidden paths line

### Unchanged
- `docs/spec.md`, `docs/superpowers/specs/*`, `docs/superpowers/plans/2026-04-18-phase-0-*`
- `harness/README.md`, `harness/workflows/tokenman.yml.template`
- `scoping/README.md`, `onboarding/README.md`
- `recommended-skills.yaml`, `pricing.yaml`
- `tests/fixtures/**`
- `README.md`, `CLAUDE.md`, `LICENSE`, `.shellcheckrc`, `.gitignore`
- `.tokenman/PAUSE`, `.tokenman/tokenman.yaml`
- `.github/workflows/.gitkeep`, `.claude/skills/.gitkeep`

---

## Commit-Message Convention

Per `CLAUDE.md`: imperative, sentence case, no period, <72 chars. Scope prefixes: `feat(harness|scoping|onboarding|catalog|dogfood): …`, `chore: …`, `test: …`, `docs: …`.

Each commit includes the Claude trailer:
```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

Work happens in `/home/dev/projects/tokenman`. All `git` commands use `-C /home/dev/projects/tokenman` to avoid `cd`.

---

## Tasks

### Task 1: Lock ledger schema + fixtures README

**Files:**
- Create: `/home/dev/projects/tokenman/harness/lib/ledger.schema.json`
- Create: `/home/dev/projects/tokenman/tests/ledgers/README.md`

**Rationale:** Establish the canonical schema contract for `.tokenman/ledger.jsonl` entries per `docs/spec.md` §8.1, and the directory where schema-test fixtures live. Nothing else in the commit depends on code or tests yet — just files and a README.

- [ ] **Step 1: Create `harness/lib/` directory**

Run:
```bash
mkdir -p /home/dev/projects/tokenman/harness/lib
```

Expected: no output, exit 0.

- [ ] **Step 2: Write `harness/lib/ledger.schema.json`**

Write file `/home/dev/projects/tokenman/harness/lib/ledger.schema.json` with content:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/verky/tokenman/harness/lib/ledger.schema.json",
  "title": "Tokenman ledger entry",
  "description": "One line in .tokenman/ledger.jsonl. See docs/spec.md §8.1.",
  "type": "object",
  "required": ["run_id", "ts", "skill", "status", "duration_s", "total_tokens"],
  "additionalProperties": false,
  "properties": {
    "run_id": {
      "type": "string",
      "pattern": "^r-[0-9]{4}$",
      "description": "Four-digit zero-padded run ID, monotonic per repo from r-0001."
    },
    "ts": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$",
      "description": "ISO 8601 UTC, Z suffix, second precision."
    },
    "skill": {
      "type": "string",
      "minLength": 1,
      "description": "Skill name this run exercised."
    },
    "status": {
      "type": "string",
      "enum": [
        "pr_opened",
        "no_change",
        "skipped_lock",
        "skipped_cooldown",
        "skipped_budget",
        "skipped_pause",
        "skipped_review_bandwidth",
        "aborted_gate",
        "aborted_evaluator",
        "error"
      ]
    },
    "pr": {
      "oneOf": [
        { "type": "null" },
        { "type": "integer", "minimum": 1 }
      ],
      "description": "PR number; non-null only when status == 'pr_opened'. Invariant enforced by append utility (Phase 1.2)."
    },
    "generator": {
      "description": "Populated whenever the generator ran; null for skip statuses and pre-generator errors.",
      "oneOf": [
        { "type": "null" },
        {
          "type": "object",
          "required": ["prompt_version", "output_summary", "diff_lines", "tokens"],
          "additionalProperties": false,
          "properties": {
            "prompt_version": { "type": "string", "minLength": 1 },
            "output_summary": { "type": "string" },
            "diff_lines":     { "type": "integer", "minimum": 0 },
            "tokens":         { "type": "integer", "minimum": 0 }
          }
        }
      ]
    },
    "evaluator": {
      "description": "Always null in Phase 1; populated Phase 3+ when generator/evaluator split is live.",
      "oneOf": [
        { "type": "null" },
        {
          "type": "object",
          "required": ["prompt_version", "verdict", "reason", "tokens"],
          "additionalProperties": false,
          "properties": {
            "prompt_version": { "type": "string", "minLength": 1 },
            "verdict":        { "type": "string", "enum": ["approve", "reject"] },
            "reason":         { "type": "string" },
            "tokens":         { "type": "integer", "minimum": 0 }
          }
        }
      ]
    },
    "duration_s":   { "type": "integer", "minimum": 0 },
    "total_tokens": { "type": "integer", "minimum": 0 },
    "verdict": {
      "oneOf": [
        { "type": "null" },
        { "type": "string", "enum": ["merged_good", "closed_bad", "stale", "ignored"] }
      ],
      "description": "Null on write; filled in by user at weekly review."
    },
    "verdict_note": {
      "oneOf": [
        { "type": "null" },
        { "type": "string" }
      ]
    }
  },
  "$comment": "Conditional invariants (documented, not schema-enforced here): (1) pr is non-null iff status == 'pr_opened'. (2) generator is non-null for statuses where the generator ran (pr_opened, no_change, aborted_gate, aborted_evaluator, and generator-phase errors); null for skipped_* statuses. (3) total_tokens = (generator.tokens or 0) + (evaluator.tokens or 0). These invariants are enforced by the append-validate utility in Phase 1.2."
}
```

- [ ] **Step 3: Verify the schema file parses as valid JSON**

Run:
```bash
python3 -c "import json; json.load(open('/home/dev/projects/tokenman/harness/lib/ledger.schema.json')); print('OK')"
```

Expected: `OK` printed on stdout. Any traceback is a failure — fix the JSON syntax before proceeding.

- [ ] **Step 4: Verify the schema file parses as a valid JSON Schema Draft 2020-12**

Run:
```bash
python3 -c "
import json
import jsonschema
schema = json.load(open('/home/dev/projects/tokenman/harness/lib/ledger.schema.json'))
jsonschema.Draft202012Validator.check_schema(schema)
print('OK')
"
```

Expected: `OK`. If `jsonschema` is not installed yet (`ModuleNotFoundError`), install it first with `python3 -m pip install 'jsonschema>=4.21' -q` and retry. (Task 3 adds it as a proper dev dep; this check just validates the schema format at commit time.)

Any `jsonschema.exceptions.SchemaError` is a failure — fix the schema before proceeding.

- [ ] **Step 5: Create `tests/ledgers/` directory**

Run:
```bash
mkdir -p /home/dev/projects/tokenman/tests/ledgers
```

Expected: no output, exit 0.

- [ ] **Step 6: Write `tests/ledgers/README.md`**

Write file `/home/dev/projects/tokenman/tests/ledgers/README.md` with content:

```markdown
# Ledger test fixtures

JSONL files used by `tests/test_ledger_schema.py` to validate the ledger
schema (`harness/lib/ledger.schema.json`) and by `harness/templates/status.sh`
as realistic input. Distinct from `tests/fixtures/` which hosts synthetic
consumer repos.

## Fixtures

- `all-statuses.jsonl` — one entry per `status` enum value (10 entries).
  Schema-coverage fixture. Some entries are forward-looking (Phase 2/3
  statuses like `skipped_budget`, `aborted_evaluator`) but valid under
  the schema today.
- `realistic-week.jsonl` — a synthetic week of runs across 2–3 skills
  (~18 entries). Aggregation fixture; exercises the per-skill breakdown
  and last-N-runs sections of `status.sh`.

## Updating fixtures

If you change the schema, run `pytest` at the repo root. If fixture
entries no longer validate, either fix the entries or revert the schema
change — schema drift should require an explicit update path, not happen
by accident.
```

- [ ] **Step 7: Verify both files exist**

Run:
```bash
ls /home/dev/projects/tokenman/harness/lib/ledger.schema.json /home/dev/projects/tokenman/tests/ledgers/README.md
```

Expected: both paths print. No "No such file" messages.

- [ ] **Step 8: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add harness/lib tests/ledgers/README.md
git -C /home/dev/projects/tokenman status --short
```

Expected: `A  harness/lib/ledger.schema.json` and `A  tests/ledgers/README.md`.

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
feat(harness): lock ledger schema v1

Canonical JSON Schema Draft 2020-12 contract for .tokenman/ledger.jsonl
entries, covering spec §8.1. Locks the full Phase 3 shape now
(generator + evaluator sub-objects), with Phase 1 runs writing
evaluator: null. Conditional invariants (e.g., pr non-null iff status
== pr_opened) are documented in the schema's $comment; enforcement
ships with the append utility in Phase 1.2.

Also scaffolds tests/ledgers/ where the test fixtures for this schema
will land in the next commit.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds. `git -C /home/dev/projects/tokenman log --oneline -1` shows `feat(harness): lock ledger schema v1`.

---

### Task 2: Add ledger schema fixtures

**Files:**
- Create: `/home/dev/projects/tokenman/tests/ledgers/all-statuses.jsonl`
- Create: `/home/dev/projects/tokenman/tests/ledgers/realistic-week.jsonl`

**Rationale:** Two fixture ledgers that exercise the schema. `all-statuses.jsonl` has one entry per status enum value (10 total). `realistic-week.jsonl` has 18 entries across three skills spanning 2026-04-11 through 2026-04-17. The first validates schema coverage; the second exercises `status.sh` aggregation in Task 4.

- [ ] **Step 1: Write `tests/ledgers/all-statuses.jsonl`**

Write file `/home/dev/projects/tokenman/tests/ledgers/all-statuses.jsonl` with these exact 10 lines (one JSON object per line, no trailing newline beyond the file's final newline):

```
{"run_id":"r-0001","ts":"2026-04-11T09:00:00Z","skill":"readme-maintainer","status":"pr_opened","pr":128,"generator":{"prompt_version":"v1","output_summary":"Added Installation section with quick-start command.","diff_lines":22,"tokens":15000},"evaluator":null,"duration_s":35,"total_tokens":15000,"verdict":null,"verdict_note":null}
{"run_id":"r-0002","ts":"2026-04-11T15:00:00Z","skill":"readme-maintainer","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"README already aligned with repo contents.","diff_lines":0,"tokens":8500},"evaluator":null,"duration_s":18,"total_tokens":8500,"verdict":null,"verdict_note":null}
{"run_id":"r-0003","ts":"2026-04-12T08:00:00Z","skill":"readme-maintainer","status":"skipped_lock","pr":null,"generator":null,"evaluator":null,"duration_s":1,"total_tokens":0,"verdict":null,"verdict_note":null}
{"run_id":"r-0004","ts":"2026-04-12T14:00:00Z","skill":"dead-code-cleanup","status":"skipped_cooldown","pr":null,"generator":null,"evaluator":null,"duration_s":1,"total_tokens":0,"verdict":null,"verdict_note":null}
{"run_id":"r-0005","ts":"2026-04-13T09:00:00Z","skill":"dead-code-cleanup","status":"skipped_budget","pr":null,"generator":null,"evaluator":null,"duration_s":1,"total_tokens":0,"verdict":null,"verdict_note":null}
{"run_id":"r-0006","ts":"2026-04-13T11:00:00Z","skill":"dep-bump-safe","status":"skipped_pause","pr":null,"generator":null,"evaluator":null,"duration_s":0,"total_tokens":0,"verdict":null,"verdict_note":null}
{"run_id":"r-0007","ts":"2026-04-13T18:00:00Z","skill":"dep-bump-safe","status":"skipped_review_bandwidth","pr":null,"generator":null,"evaluator":null,"duration_s":1,"total_tokens":0,"verdict":null,"verdict_note":null}
{"run_id":"r-0008","ts":"2026-04-14T10:00:00Z","skill":"readme-maintainer","status":"aborted_gate","pr":null,"generator":{"prompt_version":"v1","output_summary":"Proposed touching harness/README.md — outside allowed paths.","diff_lines":5,"tokens":11200},"evaluator":null,"duration_s":12,"total_tokens":11200,"verdict":null,"verdict_note":null}
{"run_id":"r-0009","ts":"2026-04-14T16:00:00Z","skill":"readme-maintainer","status":"aborted_evaluator","pr":null,"generator":{"prompt_version":"v1","output_summary":"Rewrote Installation section heavily.","diff_lines":48,"tokens":11000},"evaluator":{"prompt_version":"v1","verdict":"reject","reason":"Diff size exceeds skill limit; changes too opinionated.","tokens":3300},"duration_s":28,"total_tokens":14300,"verdict":null,"verdict_note":null}
{"run_id":"r-0010","ts":"2026-04-15T10:00:00Z","skill":"dead-code-cleanup","status":"error","pr":null,"generator":{"prompt_version":"v1","output_summary":"Attempted to run ruff; crashed partway.","diff_lines":0,"tokens":9400},"evaluator":null,"duration_s":20,"total_tokens":9400,"verdict":null,"verdict_note":null}
```

- [ ] **Step 2: Verify `all-statuses.jsonl` is valid JSONL and has 10 lines**

Run:
```bash
python3 -c "
import json
path = '/home/dev/projects/tokenman/tests/ledgers/all-statuses.jsonl'
lines = [l for l in open(path).read().splitlines() if l.strip()]
assert len(lines) == 10, f'expected 10 entries, got {len(lines)}'
statuses = set()
for i, line in enumerate(lines, 1):
    entry = json.loads(line)
    statuses.add(entry['status'])
expected = {'pr_opened','no_change','skipped_lock','skipped_cooldown','skipped_budget','skipped_pause','skipped_review_bandwidth','aborted_gate','aborted_evaluator','error'}
assert statuses == expected, f'missing={expected-statuses}, extra={statuses-expected}'
print('OK')
"
```

Expected: `OK`. Any assertion failure indicates a fixture mistake.

- [ ] **Step 3: Verify every `all-statuses.jsonl` entry validates against the schema**

Run:
```bash
python3 -c "
import json, jsonschema
schema = json.load(open('/home/dev/projects/tokenman/harness/lib/ledger.schema.json'))
v = jsonschema.Draft202012Validator(schema)
path = '/home/dev/projects/tokenman/tests/ledgers/all-statuses.jsonl'
for i, line in enumerate(open(path).read().splitlines(), 1):
    if not line.strip(): continue
    entry = json.loads(line)
    errs = list(v.iter_errors(entry))
    assert not errs, f'line {i}: {[e.message for e in errs]}'
print('OK')
"
```

Expected: `OK`. If any entry fails validation, either fix the entry or the schema — the entry should be the culprit since the schema was locked in Task 1.

- [ ] **Step 4: Write `tests/ledgers/realistic-week.jsonl`**

Write file `/home/dev/projects/tokenman/tests/ledgers/realistic-week.jsonl` with these exact 18 lines:

```
{"run_id":"r-0001","ts":"2026-04-11T02:00:00Z","skill":"readme-maintainer","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"README already describes current repo layout.","diff_lines":0,"tokens":18000},"evaluator":null,"duration_s":32,"total_tokens":18000,"verdict":null,"verdict_note":null}
{"run_id":"r-0002","ts":"2026-04-11T10:00:00Z","skill":"dead-code-cleanup","status":"pr_opened","pr":126,"generator":{"prompt_version":"v1","output_summary":"Removed unused helper in src/utils/legacy.py.","diff_lines":14,"tokens":15000},"evaluator":null,"duration_s":34,"total_tokens":15000,"verdict":null,"verdict_note":null}
{"run_id":"r-0003","ts":"2026-04-11T18:00:00Z","skill":"dep-bump-safe","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"No patch-level bumps available.","diff_lines":0,"tokens":4500},"evaluator":null,"duration_s":11,"total_tokens":4500,"verdict":null,"verdict_note":null}
{"run_id":"r-0004","ts":"2026-04-12T09:00:00Z","skill":"readme-maintainer","status":"pr_opened","pr":128,"generator":{"prompt_version":"v1","output_summary":"Added Contributing pointer and updated badges.","diff_lines":12,"tokens":22000},"evaluator":null,"duration_s":41,"total_tokens":22000,"verdict":null,"verdict_note":null}
{"run_id":"r-0005","ts":"2026-04-12T15:00:00Z","skill":"dead-code-cleanup","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"No dead code found after ripgrep sweep.","diff_lines":0,"tokens":9000},"evaluator":null,"duration_s":22,"total_tokens":9000,"verdict":null,"verdict_note":null}
{"run_id":"r-0006","ts":"2026-04-13T08:00:00Z","skill":"dep-bump-safe","status":"pr_opened","pr":129,"generator":{"prompt_version":"v1","output_summary":"Bumped requests 2.32.1 → 2.32.3 (patch).","diff_lines":3,"tokens":7500},"evaluator":null,"duration_s":15,"total_tokens":7500,"verdict":null,"verdict_note":null}
{"run_id":"r-0007","ts":"2026-04-13T14:00:00Z","skill":"readme-maintainer","status":"skipped_lock","pr":null,"generator":null,"evaluator":null,"duration_s":1,"total_tokens":0,"verdict":null,"verdict_note":null}
{"run_id":"r-0008","ts":"2026-04-14T06:00:00Z","skill":"dead-code-cleanup","status":"error","pr":null,"generator":{"prompt_version":"v1","output_summary":"Proposed deletion of unused helper module.","diff_lines":17,"tokens":7100},"evaluator":null,"duration_s":15,"total_tokens":7100,"verdict":null,"verdict_note":null}
{"run_id":"r-0009","ts":"2026-04-14T12:00:00Z","skill":"readme-maintainer","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"README unchanged; no new sections warranted.","diff_lines":0,"tokens":16000},"evaluator":null,"duration_s":28,"total_tokens":16000,"verdict":null,"verdict_note":null}
{"run_id":"r-0010","ts":"2026-04-14T18:00:00Z","skill":"dep-bump-safe","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"All deps already at latest patch.","diff_lines":0,"tokens":4000},"evaluator":null,"duration_s":10,"total_tokens":4000,"verdict":null,"verdict_note":null}
{"run_id":"r-0011","ts":"2026-04-15T10:00:00Z","skill":"dead-code-cleanup","status":"pr_opened","pr":132,"generator":{"prompt_version":"v1","output_summary":"Removed three unused imports in src/core.","diff_lines":8,"tokens":12000},"evaluator":null,"duration_s":24,"total_tokens":12000,"verdict":null,"verdict_note":null}
{"run_id":"r-0012","ts":"2026-04-15T16:00:00Z","skill":"readme-maintainer","status":"pr_opened","pr":135,"generator":{"prompt_version":"v1","output_summary":"Replaced obsolete CLI example with current syntax.","diff_lines":18,"tokens":20000},"evaluator":null,"duration_s":38,"total_tokens":20000,"verdict":null,"verdict_note":null}
{"run_id":"r-0013","ts":"2026-04-16T08:00:00Z","skill":"dep-bump-safe","status":"skipped_pause","pr":null,"generator":null,"evaluator":null,"duration_s":0,"total_tokens":0,"verdict":null,"verdict_note":null}
{"run_id":"r-0014","ts":"2026-04-16T12:00:00Z","skill":"dead-code-cleanup","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"No dead code detected this cycle.","diff_lines":0,"tokens":8000},"evaluator":null,"duration_s":19,"total_tokens":8000,"verdict":null,"verdict_note":null}
{"run_id":"r-0015","ts":"2026-04-16T18:00:00Z","skill":"readme-maintainer","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"README reflects current CLI and install steps.","diff_lines":0,"tokens":16200},"evaluator":null,"duration_s":30,"total_tokens":16200,"verdict":null,"verdict_note":null}
{"run_id":"r-0016","ts":"2026-04-17T09:00:00Z","skill":"dead-code-cleanup","status":"skipped_cooldown","pr":null,"generator":null,"evaluator":null,"duration_s":1,"total_tokens":0,"verdict":null,"verdict_note":null}
{"run_id":"r-0017","ts":"2026-04-17T14:00:00Z","skill":"dead-code-cleanup","status":"no_change","pr":null,"generator":{"prompt_version":"v1","output_summary":"No dead code found after full scan.","diff_lines":0,"tokens":7000},"evaluator":null,"duration_s":22,"total_tokens":7000,"verdict":null,"verdict_note":null}
{"run_id":"r-0018","ts":"2026-04-17T18:00:00Z","skill":"readme-maintainer","status":"pr_opened","pr":141,"generator":{"prompt_version":"v1","output_summary":"Added a Usage section with three examples.","diff_lines":22,"tokens":18000},"evaluator":null,"duration_s":38,"total_tokens":18000,"verdict":null,"verdict_note":null}
```

- [ ] **Step 5: Verify `realistic-week.jsonl` has exactly 18 lines and correct distribution**

Run:
```bash
python3 -c "
import json
from collections import Counter
path = '/home/dev/projects/tokenman/tests/ledgers/realistic-week.jsonl'
lines = [l for l in open(path).read().splitlines() if l.strip()]
assert len(lines) == 18, f'expected 18 entries, got {len(lines)}'

entries = [json.loads(l) for l in lines]
by_status = Counter(e['status'] for e in entries)
by_skill  = Counter(e['skill']  for e in entries)

assert by_status == Counter({'no_change':8, 'pr_opened':6, 'skipped_lock':1, 'skipped_cooldown':1, 'skipped_pause':1, 'error':1}), f'status counts wrong: {by_status}'
assert by_skill == Counter({'readme-maintainer':7, 'dead-code-cleanup':7, 'dep-bump-safe':4}), f'skill counts wrong: {by_skill}'

# Token totals per skill
from collections import defaultdict
tok = defaultdict(int)
for e in entries:
    tok[e['skill']] += e['total_tokens']
assert tok['readme-maintainer'] == 110200, f'readme tokens: {tok[\"readme-maintainer\"]}'
assert tok['dead-code-cleanup'] == 58100,  f'dead-code tokens: {tok[\"dead-code-cleanup\"]}'
assert tok['dep-bump-safe'] == 16000,      f'dep-bump tokens: {tok[\"dep-bump-safe\"]}'
assert sum(tok.values()) == 184300, f'grand total: {sum(tok.values())}'

# Timestamps in range
for e in entries:
    assert '2026-04-11' <= e['ts'][:10] <= '2026-04-17', f'ts out of range: {e[\"ts\"]}'

print('OK')
"
```

Expected: `OK`. Any assertion failure indicates a fixture error — fix the specific offending line before proceeding.

- [ ] **Step 6: Verify every `realistic-week.jsonl` entry validates against the schema**

Run:
```bash
python3 -c "
import json, jsonschema
schema = json.load(open('/home/dev/projects/tokenman/harness/lib/ledger.schema.json'))
v = jsonschema.Draft202012Validator(schema)
path = '/home/dev/projects/tokenman/tests/ledgers/realistic-week.jsonl'
for i, line in enumerate(open(path).read().splitlines(), 1):
    if not line.strip(): continue
    entry = json.loads(line)
    errs = list(v.iter_errors(entry))
    assert not errs, f'line {i}: {[e.message for e in errs]}'
print('OK')
"
```

Expected: `OK`.

- [ ] **Step 7: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add tests/ledgers/all-statuses.jsonl tests/ledgers/realistic-week.jsonl
git -C /home/dev/projects/tokenman status --short
```

Expected: two `A` lines for the two new JSONL files.

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
test: add ledger schema fixtures

Two JSONL fixtures under tests/ledgers/:

- all-statuses.jsonl — 10 entries, one per 'status' enum value, for
  schema-coverage tests. Some entries (skipped_budget,
  aborted_evaluator, skipped_review_bandwidth) are forward-looking for
  Phase 2/3 but valid under the locked schema today.
- realistic-week.jsonl — 18 entries across three skills
  (readme-maintainer, dead-code-cleanup, dep-bump-safe) spanning
  2026-04-11 through 2026-04-17. Used by status.sh aggregation tests
  in a later commit.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 3: Add pyproject and ledger schema validation test

**Files:**
- Create: `/home/dev/projects/tokenman/pyproject.toml`
- Create: `/home/dev/projects/tokenman/tests/test_ledger_schema.py`

**Rationale:** Locks the schema via executable test — "schema locked" should mean CI fails on drift, not just documentation. Introduces a root `pyproject.toml` with dev-only optional-dependencies and a parameterized pytest test.

- [ ] **Step 1: Write `pyproject.toml`**

Write file `/home/dev/projects/tokenman/pyproject.toml` with content:

```toml
[project]
name = "tokenman-dev"
version = "0.0.0"
description = "Dev tooling for the tokenman library repo (not a published package)"
requires-python = ">=3.10"

[project.optional-dependencies]
dev = [
  "pytest>=8",
  "jsonschema>=4.21",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Write `tests/test_ledger_schema.py`**

Write file `/home/dev/projects/tokenman/tests/test_ledger_schema.py` with content:

```python
"""Validate every ledger fixture entry against harness/lib/ledger.schema.json."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "harness" / "lib" / "ledger.schema.json"
LEDGERS_DIR = REPO_ROOT / "tests" / "ledgers"


@pytest.fixture(scope="module")
def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


@pytest.fixture(scope="module")
def validator(schema: dict) -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(schema)


@pytest.mark.parametrize(
    "ledger_path",
    sorted(LEDGERS_DIR.glob("*.jsonl")),
    ids=lambda p: p.name,
)
def test_every_entry_validates(
    validator: jsonschema.Draft202012Validator,
    ledger_path: Path,
) -> None:
    """Each line in every *.jsonl fixture must validate against the schema."""
    for lineno, line in enumerate(ledger_path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        entry = json.loads(line)
        errors = sorted(validator.iter_errors(entry), key=lambda e: e.path)
        if errors:
            msgs = "\n".join(f"  - {e.message} at {list(e.path)}" for e in errors)
            pytest.fail(f"{ledger_path.name}:{lineno}\n{msgs}")


def test_all_statuses_fixture_covers_enum(schema: dict) -> None:
    """all-statuses.jsonl must have exactly one entry per status enum value."""
    all_statuses_path = LEDGERS_DIR / "all-statuses.jsonl"
    entries = [
        json.loads(line)
        for line in all_statuses_path.read_text().splitlines()
        if line.strip()
    ]
    expected = set(schema["properties"]["status"]["enum"])
    actual = {e["status"] for e in entries}
    assert actual == expected, (
        f"missing: {expected - actual}, extra: {actual - expected}"
    )
```

- [ ] **Step 3: Install dev dependencies**

Run:
```bash
python3 -m pip install -e '/home/dev/projects/tokenman[dev]' -q
```

Expected: no errors. If `pip` is missing, install Python first or use `python3 -m ensurepip --upgrade`.

- [ ] **Step 4: Run pytest and verify 3 tests pass**

Run:
```bash
cd /home/dev/projects/tokenman && python3 -m pytest -v
```

Expected output contains (exact count, all passing):

```
tests/test_ledger_schema.py::test_every_entry_validates[all-statuses.jsonl] PASSED
tests/test_ledger_schema.py::test_every_entry_validates[realistic-week.jsonl] PASSED
tests/test_ledger_schema.py::test_all_statuses_fixture_covers_enum PASSED

============================== 3 passed in ... ==============================
```

Exit code 0. If any test fails, diagnose: a validation failure points to either a fixture bug (from Task 2) or a schema bug (from Task 1). Fix the offender before proceeding.

- [ ] **Step 5: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add pyproject.toml tests/test_ledger_schema.py
git -C /home/dev/projects/tokenman status --short
```

Expected: two `A` lines.

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
chore: add pyproject and ledger schema validation test

Introduces pyproject.toml at the repo root (first time) with dev-only
optional-dependencies (pytest, jsonschema). Not a published package;
contributors install with 'pip install -e ".[dev]"' and run 'pytest'.

The new test at tests/test_ledger_schema.py validates every fixture
entry under tests/ledgers/ against harness/lib/ledger.schema.json and
additionally asserts that all-statuses.jsonl covers every value of
the status enum. Three tests total, all passing.

This is what makes "ledger schema locked" mean something: CI fails on
drift between schema and fixtures.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 4: Move status.sh to harness/templates and rewrite for new schema

**Files:**
- Create: `/home/dev/projects/tokenman/harness/templates/status.sh`
- Delete: `/home/dev/projects/tokenman/scripts/status.sh`
- Delete: `/home/dev/projects/tokenman/scripts/` (empty after removing status.sh)

**Rationale:** Moves the reader to the canonical source-zone location (`harness/templates/`, mirroring `harness/workflows/`) and rewrites it for the new ledger schema. The old script at `scripts/status.sh` used a different shape (`input_tokens`/`output_tokens`/`pr_number`/`lines_deleted`) that no longer matches the ledger. The rewrite is ledger-only: no GitHub API, no config read, no cap %. Renders all-time summary, per-skill breakdown, and the last 10 runs.

- [ ] **Step 1: Create `harness/templates/` directory**

Run:
```bash
mkdir -p /home/dev/projects/tokenman/harness/templates
```

Expected: no output, exit 0.

- [ ] **Step 2: Write `harness/templates/status.sh`**

Write file `/home/dev/projects/tokenman/harness/templates/status.sh` with content:

```bash
#!/usr/bin/env bash
# status.sh — human-readable summary of .tokenman/ledger.jsonl (v1)
#
# Phase 1.1 of docs/spec.md §12. Ledger-only reader — no GitHub API,
# no config read, no cap %. /tokenman init copies this file into a
# consumer's .tokenman/status.sh at install time.
#
# Usage:  bash status.sh [ledger-path]
# Default ledger-path: .tokenman/ledger.jsonl
#
# Dependencies: jq, standard POSIX tools.
set -euo pipefail

LEDGER="${1:-.tokenman/ledger.jsonl}"

if [ ! -f "$LEDGER" ]; then
    echo "No ledger at $LEDGER (no tokenman runs yet)."
    exit 0
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "status.sh requires jq. Install it first: apt install jq / brew install jq."
    exit 1
fi

LINES=$(grep -c . "$LEDGER" 2>/dev/null || true)
LINES="${LINES:-0}"

if [ "$LINES" -eq 0 ]; then
    echo "Ledger $LEDGER is empty (no tokenman runs yet)."
    exit 0
fi

echo "Tokenman status"
echo
printf "Ledger:  %s  (%s entries)\n" "$LEDGER" "$LINES"
echo

# --- Summary (all time) ------------------------------------------------
# jq computes counts + sums; bash printf handles alignment.
# -s slurps all JSONL entries into one array; -r emits raw (no JSON-string
# quoting) so @tsv produces a literal tab-separated line.
counts=$(jq -sr '[
    length,
    (map(select(.status == "pr_opened"))                | length),
    (map(select(.status == "no_change"))                | length),
    (map(select(.status | startswith("skipped_")))      | length),
    (map(select(.status | startswith("aborted_")))      | length),
    (map(select(.status == "error"))                    | length),
    (map(.total_tokens) | add // 0),
    (map(select(.status == "skipped_lock"))             | length),
    (map(select(.status == "skipped_cooldown"))         | length),
    (map(select(.status == "skipped_budget"))           | length),
    (map(select(.status == "skipped_pause"))            | length),
    (map(select(.status == "skipped_review_bandwidth")) | length)
] | @tsv' "$LEDGER")

read -r total prs nochg skipped aborted errors tokens sk_lock sk_cd sk_bd sk_ps sk_rb <<< "$counts"

avg=0
if [ "$total" -gt 0 ]; then
    avg=$(( tokens / total ))
fi

echo "Summary (all time):"
printf "  Runs:          %3d\n" "$total"
printf "  PRs opened:    %3d\n" "$prs"
printf "  No-change:     %3d\n" "$nochg"
printf "  Skipped:       %3d  (lock: %d, cooldown: %d, budget: %d, pause: %d, review-bandwidth: %d)\n" \
    "$skipped" "$sk_lock" "$sk_cd" "$sk_bd" "$sk_ps" "$sk_rb"
printf "  Aborted:       %3d\n" "$aborted"
printf "  Errors:        %3d\n" "$errors"
printf "  Tokens:   %8d  (avg %d/run)\n" "$tokens" "$avg"
echo

# --- Top skills (all time) ---------------------------------------------
echo "Top skills (all time):"
jq -sr '
    group_by(.skill)
    | map({
        skill: .[0].skill,
        tokens: (map(.total_tokens) | add // 0),
        runs:   length,
        prs:    (map(select(.status == "pr_opened")) | length)
      })
    | sort_by(-.tokens)
    | .[]
    | [.skill, .tokens, .runs, .prs]
    | @tsv
' "$LEDGER" | while IFS=$'\t' read -r skill tokens runs prs; do
    printf "  %-20s  %7d tok   %d runs  %d PRs\n" "$skill" "$tokens" "$runs" "$prs"
done
echo

# --- Last 10 runs (newest first) ---------------------------------------
echo "Last 10 runs (newest first):"
jq -sr '
    sort_by(.ts)
    | reverse
    | .[0:10]
    | .[]
    | [.run_id, .ts, .skill, .status, .total_tokens]
    | @tsv
' "$LEDGER" | while IFS=$'\t' read -r run_id ts skill status tokens; do
    printf "  %s  %s  %-20s  %-17s %6d\n" "$run_id" "$ts" "$skill" "$status" "$tokens"
done
```

- [ ] **Step 3: Make the script executable**

Run:
```bash
chmod +x /home/dev/projects/tokenman/harness/templates/status.sh
```

Expected: no output, exit 0.

- [ ] **Step 4: Verify the script passes shellcheck**

Run:
```bash
shellcheck /home/dev/projects/tokenman/harness/templates/status.sh
```

Expected: no output, exit 0. Any warning (e.g., SC2086 about unquoted vars) must be fixed before proceeding — the repo has a `.shellcheckrc` that suppresses accepted lint items; real issues must be addressed.

- [ ] **Step 5: Run against `realistic-week.jsonl` and verify output**

Run:
```bash
cd /home/dev/projects/tokenman && bash harness/templates/status.sh tests/ledgers/realistic-week.jsonl
```

Expected output (character-for-character):

```
Tokenman status

Ledger:  tests/ledgers/realistic-week.jsonl  (18 entries)

Summary (all time):
  Runs:           18
  PRs opened:      6
  No-change:       8
  Skipped:         3  (lock: 1, cooldown: 1, budget: 0, pause: 1, review-bandwidth: 0)
  Aborted:         0
  Errors:          1
  Tokens:     184300  (avg 10238/run)

Top skills (all time):
  readme-maintainer      110200 tok   7 runs  3 PRs
  dead-code-cleanup       58100 tok   7 runs  2 PRs
  dep-bump-safe           16000 tok   4 runs  1 PRs

Last 10 runs (newest first):
  r-0018  2026-04-17T18:00:00Z  readme-maintainer     pr_opened          18000
  r-0017  2026-04-17T14:00:00Z  dead-code-cleanup     no_change           7000
  r-0016  2026-04-17T09:00:00Z  dead-code-cleanup     skipped_cooldown       0
  r-0015  2026-04-16T18:00:00Z  readme-maintainer     no_change          16200
  r-0014  2026-04-16T12:00:00Z  dead-code-cleanup     no_change           8000
  r-0013  2026-04-16T08:00:00Z  dep-bump-safe         skipped_pause          0
  r-0012  2026-04-15T16:00:00Z  readme-maintainer     pr_opened          20000
  r-0011  2026-04-15T10:00:00Z  dead-code-cleanup     pr_opened          12000
  r-0010  2026-04-14T18:00:00Z  dep-bump-safe         no_change           4000
  r-0009  2026-04-14T12:00:00Z  readme-maintainer     no_change          16000
```

Exit code 0. If the output differs:
- The KEY semantic checks are: (a) 18 entries; (b) 6 PRs opened / 8 no-change / 3 skipped / 0 aborted / 1 error; (c) 184300 total tokens and 10238 avg; (d) per-skill tokens 110200/58100/16000; (e) exactly 10 last-runs rows, newest first starting with r-0018. Minor whitespace drift (a single-space difference here or there due to printf field widths) is acceptable if the semantic checks pass. Any difference in the numeric values is a bug in `status.sh` — fix and re-run.

- [ ] **Step 6: Run against `all-statuses.jsonl` and verify it renders without error**

Run:
```bash
cd /home/dev/projects/tokenman && bash harness/templates/status.sh tests/ledgers/all-statuses.jsonl
```

Expected:
- Exit code 0.
- Output starts with `Tokenman status`, shows 10 entries in the header, and includes "Top skills (all time):" plus "Last 10 runs (newest first):" sections.
- Summary shows: 1 pr_opened, 1 no_change, 5 skipped (lock/cooldown/budget/pause/review-bandwidth each 1), 2 aborted (aborted_gate + aborted_evaluator), 1 error.

- [ ] **Step 7: Run against a nonexistent path and verify benign behavior**

Run:
```bash
bash /home/dev/projects/tokenman/harness/templates/status.sh /tmp/nonexistent-ledger.jsonl
```

Expected:
- Exit code 0.
- Stdout: `No ledger at /tmp/nonexistent-ledger.jsonl (no tokenman runs yet).`

Then with an empty file:
```bash
: > /tmp/empty-ledger.jsonl && bash /home/dev/projects/tokenman/harness/templates/status.sh /tmp/empty-ledger.jsonl; rm -f /tmp/empty-ledger.jsonl
```

Expected:
- Exit code 0.
- Stdout: `Ledger /tmp/empty-ledger.jsonl is empty (no tokenman runs yet).`

- [ ] **Step 8: Remove the old `scripts/status.sh` and the `scripts/` directory**

Run:
```bash
git -C /home/dev/projects/tokenman rm scripts/status.sh
rmdir /home/dev/projects/tokenman/scripts
```

Expected:
- First command prints `rm 'scripts/status.sh'`.
- Second command succeeds silently (directory was empty after removing the tracked file).

- [ ] **Step 9: Verify `scripts/` is gone**

Run:
```bash
test ! -e /home/dev/projects/tokenman/scripts && echo OK
```

Expected: `OK`.

- [ ] **Step 10: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add harness/templates/status.sh
git -C /home/dev/projects/tokenman status --short
```

Expected:
```
A  harness/templates/status.sh
D  scripts/status.sh
```

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
feat(harness): move status.sh to harness/templates and rewrite

Moves the reader from scripts/status.sh to its canonical source-zone
location at harness/templates/status.sh, mirroring the pattern used by
harness/workflows/tokenman.yml.template. /tokenman init will later
copy this file into consumers as .tokenman/status.sh.

Rewritten for the new ledger schema (spec §8.1): reads total_tokens
directly instead of input_tokens/output_tokens, uses pr instead of
pr_number, groups skipped-run reasons off the status enum rather than
a freeform 'reason' field. Ledger-only — no GitHub API call for PR
state, no config read for cap %. Those are separate concerns for a
later sub-phase or script.

Removes the scripts/ directory (was dev-tooling limbo per
docs/superpowers/specs/2026-04-18-phase-0-scaffolding-design.md).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 5: Update CONTRIBUTING and runtime CLAUDE.md for 1.1 paths

**Files:**
- Modify: `/home/dev/projects/tokenman/CONTRIBUTING.md`
- Modify: `/home/dev/projects/tokenman/.tokenman/CLAUDE.md`

**Rationale:** Document the new test workflow (pytest + jsonschema) in `CONTRIBUTING.md`, and remove `scripts/` from the runtime-zone CLAUDE.md's forbidden list since the directory no longer exists. `.tokenman/CLAUDE.md` is human-edited (dogfood can't write to it); safe to edit directly while PAUSE is on.

- [ ] **Step 1: Update `.tokenman/CLAUDE.md` — remove `scripts/` from forbidden list**

The current file has the line:
```
- LICENSE, .gitignore, .shellcheckrc, scripts/
```

Edit it to:
```
- LICENSE, .gitignore, .shellcheckrc
```

Use the `Edit` tool with:
- `old_string`: `- LICENSE, .gitignore, .shellcheckrc, scripts/`
- `new_string`: `- LICENSE, .gitignore, .shellcheckrc`

- [ ] **Step 2: Verify the runtime CLAUDE.md no longer mentions `scripts/`**

Run:
```bash
grep -F 'scripts/' /home/dev/projects/tokenman/.tokenman/CLAUDE.md && echo "FAIL: still mentions scripts/" || echo "OK: scripts/ not mentioned"
```

Expected: `OK: scripts/ not mentioned`.

- [ ] **Step 3: Insert "Running tests" section into `CONTRIBUTING.md`**

Use the `Edit` tool. The anchor (the text that appears only once in the
file) is the existing `## Phase 0 status` heading plus the paragraph that
follows it. Replace the whole block (heading + current paragraph) with the
new "Running tests" section followed by an updated "Status" section.

`old_string`:

    ## Phase 0 status

    The harness is not implemented yet. Phase 0 establishes scaffolding
    and contracts. See `docs/spec.md` §12 for the full phased roadmap.

`new_string`:

    ## Running tests

    Install dev dependencies and run pytest from the repo root:

    ```bash
    pip install -e '.[dev]'
    pytest
    ```

    The canonical ledger schema lives at `harness/lib/ledger.schema.json`;
    test fixtures at `tests/ledgers/*.jsonl`. The test suite validates every
    fixture entry against the schema, so schema drift fails fast.

    ## Status

    Phase 0 scaffolding is in place. Phase 1.1 has locked the ledger
    schema and reworked `status.sh`. The harness runner is not
    implemented yet — Phase 1.2 covers that. See `docs/spec.md` §12 for
    the full phased roadmap.

(The Edit tool takes these as literal text — no escaping of backticks
or leading indentation tricks are needed. The leading 4-space indent
shown in this plan is a Markdown block-quote artifact; feed the actual
text to `Edit` starting from column 0.)

- [ ] **Step 4: Verify `CONTRIBUTING.md` has the new section and updated status**

Run:
```bash
grep -q '^## Running tests$'     /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q '^## Status$'            /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q 'pip install -e'         /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q 'pytest'                 /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q 'ledger.schema.json'     /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q 'Phase 1.1 has locked'   /home/dev/projects/tokenman/CONTRIBUTING.md && \
! grep -q '^## Phase 0 status$'  /home/dev/projects/tokenman/CONTRIBUTING.md && \
echo OK
```

Expected: `OK`. Any missing grep is a failure.

Also verify the top-level heading ordering:

```bash
grep -E '^## ' /home/dev/projects/tokenman/CONTRIBUTING.md
```

Expected, in order:
```
## Source zone vs runtime zone
## Commit conventions
## Running tests
## Status
```

(Plus `### Source zone …`, `### Runtime zone …`, `### Why the separation matters` inside the first section — those are unchanged.)

- [ ] **Step 5: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add CONTRIBUTING.md .tokenman/CLAUDE.md
git -C /home/dev/projects/tokenman status --short
```

Expected:
```
M CONTRIBUTING.md
M .tokenman/CLAUDE.md
```

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
docs: update CONTRIBUTING and runtime CLAUDE.md for 1.1 paths

CONTRIBUTING.md gets a 'Running tests' section documenting the
pytest + jsonschema workflow introduced in the previous commit,
pointing at harness/lib/ledger.schema.json and tests/ledgers/.
The stale 'Phase 0 status' heading is renamed to 'Status' and
rewritten to reflect Phase 1.1 completion.

.tokenman/CLAUDE.md drops 'scripts/' from the forbidden-paths list
since the directory no longer exists (status.sh moved to
harness/templates/). The rest of the paranoid list is unchanged:
harness/ still covers harness/lib/ and harness/templates/, so the
script's new home is still implicitly off-limits to dogfood runs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 6: Verify Phase 1.1 exit criteria (no commit)

**Rationale:** Confirms each exit criterion from the design doc (§Exit criteria) holds after all five commits. No code changes, no commit — this task produces a pass/fail verdict.

- [ ] **Step 1: Criterion 1 — Schema valid JSON Schema Draft 2020-12**

Run:
```bash
python3 -c "
import json, jsonschema
schema = json.load(open('/home/dev/projects/tokenman/harness/lib/ledger.schema.json'))
jsonschema.Draft202012Validator.check_schema(schema)
print('criterion 1: PASS')
"
```

Expected: `criterion 1: PASS`.

- [ ] **Step 2: Criterion 2 — Enum coverage fixture**

Run:
```bash
python3 -c "
import json
entries = [json.loads(l) for l in open('/home/dev/projects/tokenman/tests/ledgers/all-statuses.jsonl').read().splitlines() if l.strip()]
assert len(entries) == 10, f'expected 10, got {len(entries)}'
expected = {'pr_opened','no_change','skipped_lock','skipped_cooldown','skipped_budget','skipped_pause','skipped_review_bandwidth','aborted_gate','aborted_evaluator','error'}
actual = {e['status'] for e in entries}
assert actual == expected, f'missing={expected-actual}, extra={actual-expected}'
print('criterion 2: PASS')
"
```

Expected: `criterion 2: PASS`.

- [ ] **Step 3: Criterion 3 — Realistic-week fixture shape**

Run:
```bash
python3 -c "
import json
from collections import Counter
entries = [json.loads(l) for l in open('/home/dev/projects/tokenman/tests/ledgers/realistic-week.jsonl').read().splitlines() if l.strip()]
assert len(entries) == 18, f'expected 18, got {len(entries)}'
for e in entries:
    assert '2026-04-11' <= e['ts'][:10] <= '2026-04-17', f'ts out of range: {e[\"ts\"]}'
by_status = Counter(e['status'] for e in entries)
assert by_status == Counter({'no_change':8, 'pr_opened':6, 'skipped_lock':1, 'skipped_cooldown':1, 'skipped_pause':1, 'error':1})
print('criterion 3: PASS')
"
```

Expected: `criterion 3: PASS`.

- [ ] **Step 4: Criterion 4 — pytest passes**

Run:
```bash
cd /home/dev/projects/tokenman && python3 -m pytest -q
```

Expected: exit code 0, output shows `3 passed`.

- [ ] **Step 5: Criterion 5 — `status.sh` renders three ways**

Run:
```bash
bash /home/dev/projects/tokenman/harness/templates/status.sh /home/dev/projects/tokenman/tests/ledgers/realistic-week.jsonl >/dev/null && \
bash /home/dev/projects/tokenman/harness/templates/status.sh /home/dev/projects/tokenman/tests/ledgers/all-statuses.jsonl   >/dev/null && \
OUT=$(bash /home/dev/projects/tokenman/harness/templates/status.sh /tmp/nonexistent-ledger.jsonl) && \
echo "$OUT" | grep -q 'No ledger at /tmp/nonexistent-ledger.jsonl' && \
echo "criterion 5: PASS"
```

Expected: `criterion 5: PASS`.

- [ ] **Step 6: Criterion 6 — shellcheck clean**

Run:
```bash
shellcheck /home/dev/projects/tokenman/harness/templates/status.sh && echo "criterion 6: PASS"
```

Expected: `criterion 6: PASS`.

- [ ] **Step 7: Criterion 7 — `scripts/` gone**

Run:
```bash
test ! -e /home/dev/projects/tokenman/scripts && echo "criterion 7: PASS"
```

Expected: `criterion 7: PASS`.

- [ ] **Step 8: Criterion 8 — Runtime CLAUDE.md no longer mentions `scripts/`**

Run:
```bash
if grep -F 'scripts/' /home/dev/projects/tokenman/.tokenman/CLAUDE.md >/dev/null; then
  echo "criterion 8: FAIL"
else
  grep -q 'harness/' /home/dev/projects/tokenman/.tokenman/CLAUDE.md && echo "criterion 8: PASS"
fi
```

Expected: `criterion 8: PASS`.

- [ ] **Step 9: Criterion 9 — CONTRIBUTING.md documents pytest**

Run:
```bash
grep -q 'pip install -e' /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q 'pytest'          /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q 'ledger.schema.json' /home/dev/projects/tokenman/CONTRIBUTING.md && \
echo "criterion 9: PASS"
```

Expected: `criterion 9: PASS`.

- [ ] **Step 10: Criterion 10 — Working tree clean after 5 commits**

Run:
```bash
git -C /home/dev/projects/tokenman status
```

Expected: `nothing to commit, working tree clean`.

Then verify the five commit messages:

```bash
git -C /home/dev/projects/tokenman log --oneline -5
```

Expected: five lines, in reverse chronological order:
```
<hash> docs: update CONTRIBUTING and runtime CLAUDE.md for 1.1 paths
<hash> feat(harness): move status.sh to harness/templates and rewrite
<hash> chore: add pyproject and ledger schema validation test
<hash> test: add ledger schema fixtures
<hash> feat(harness): lock ledger schema v1
```

- [ ] **Step 11: Final summary**

If all ten criteria pass: **Phase 1.1 is complete.** Report to the user:
- Five commits added.
- Schema is locked, fixtures exist, test suite enforces the contract.
- `status.sh` relocated and rewritten.
- Ready to proceed to Phase 1.2 (linear harness workflow + first skill integration).

---

## Self-Review Notes

Self-review performed after plan was written:

**1. Spec coverage.** All ten exit criteria in the design doc are exercised by Task 6; each of the five commit slots in the design doc's "Order of commits" maps to Tasks 1–5 respectively. The design's six scope decisions are all reflected in the task content (schema shape, Phase 3 posture, ledger-only `status.sh`, `harness/templates/` location, fixture distribution, pytest enforcement).

**2. Placeholder scan.** No TBD/TODO/fill-in phrases in task steps. Every code block contains complete content; every shell command has an expected result.

**3. Type consistency.** Schema field names (`run_id`, `ts`, `skill`, `status`, `pr`, `generator`, `evaluator`, `duration_s`, `total_tokens`, `verdict`, `verdict_note`) are used identically in the schema (Task 1), fixtures (Task 2), test (Task 3), and `status.sh` jq queries (Task 4). Per-skill token totals in `realistic-week.jsonl` (Task 2) match the expected output in Task 4 Step 5 (readme 110200, dead-code 58100, dep-bump 16000; grand total 184300; avg 10239).

**4. Edge cases.** `status.sh` handles: missing ledger path (Task 4 Step 7), empty ledger file (Task 4 Step 7 second case), `jq` not installed (handled in-script), zero-division when LINES=0 (handled via `if $total > 0 then … else 0 end` in the avg computation).

**5. Forward references.** Task 1's fixtures README (`tests/ledgers/README.md`) references `all-statuses.jsonl` and `realistic-week.jsonl` before they exist in Task 2; and `harness/templates/status.sh` before it exists in Task 4. These are prose forward references, not runtime broken states — the test suite doesn't run until Task 3 anyway.

**6. Schema-enforcement dependency cycle.** Task 1 Step 4 installs `jsonschema` ad-hoc to verify the schema; Task 3 installs it formally via `pyproject.toml`. This is a deliberate asymmetry: we want to check the schema file is well-formed at Task 1 commit time, before the pyproject scaffolding arrives. The ad-hoc install is a diagnostic, not a commitment.
