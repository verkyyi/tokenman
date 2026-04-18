# Phase 1.1 Ledger Schema & Status Script v1 — Design

**Date:** 2026-04-18
**Status:** Approved via brainstorming, pending user review of this doc
**Parent spec:** `docs/spec.md` v0.2, §12 "Phase 1 — Wedge + guided onboarding"
**Sub-phase:** 1.1 of 4
- 1.1 — ledger schema + `status.sh` v1 (this doc)
- 1.2 — linear harness workflow + first skill integration (next)
- 1.3 — scoping flow (`tokenman scope`)
- 1.4 — guided onboarding mode

## Purpose

Lock the ledger schema (`docs/spec.md` §8.1) and rework `status.sh` for the
new schema. Produces the observability contract that Phase 1.2+ runtime
code writes against. No runtime logic in this sub-phase — only a schema
file, example fixtures, a reader script, and a pytest-based enforcement
test. Exit state: the schema is authoritative and machine-verified,
`status.sh` renders the new shape, and fixtures document every `status`
enum value.

Phase 1 as specified in `docs/spec.md` §12 bundles six workstreams
(ledger, harness workflow, skill integration, scoping, onboarding,
consumer schedule defaults); 1.1 is the narrowest foundational piece —
locking an observability shape that everything downstream relies on.

## Scope decisions (from brainstorming, 2026-04-18)

1. **Phase 1.1 scope** — schema file + `status.sh` v1 rewrite + example
   ledger fixtures. The append-validate utility belongs with the harness
   runner (Phase 1.2); a schema without executable validation is still a
   draft, so example fixtures + a pytest validator carry that load.

2. **Phase 3 fields today** — lock the full Phase 3 schema now. Phase 1
   runs write `evaluator: null`. Adding fields later would count as a
   breaking change for parsers; keeping `evaluator: null` in Phase 1 costs
   nothing and makes the schema honest about the target pipeline.

3. **`status.sh` v1 scope** — strictly ledger-only. No GitHub API, no
   config read, no cap %. PR-state resolution (`merged/closed/pending`
   from the spec §8.3 example) is a separate script or Phase 2 feature.
   A ledger reader should work on any clone with zero auth.

4. **Location** — `status.sh` moves to `harness/templates/status.sh`,
   mirroring `harness/workflows/tokenman.yml.template`. Explicit naming
   makes the source/runtime relationship self-documenting. `/tokenman
   init` will later copy it to `.tokenman/status.sh` in consumers.
   `scripts/` directory is deleted (was dev-tooling limbo at Phase 0).

5. **Fixture coverage** — one entry per `status` value (10 entries,
   forward-looking where necessary) + one curated "realistic week" ledger
   (exactly 18 entries) that exercises aggregation. The first tests schema
   coverage; the second tests `status.sh` rendering.

6. **Enforcement** — introduce `pyproject.toml` at repo root with dev
   deps (`pytest`, `jsonschema`) and a parameterized test that validates
   every fixture entry against the schema. "Locked schema" means CI fails
   on drift — enforcement, not documentation.

## Before / after directory layout

### Additions
- `harness/lib/ledger.schema.json` — JSON Schema Draft 2020-12
- `harness/templates/status.sh` — bash+jq reader, new schema
- `tests/ledgers/README.md` — explains ledger test fixtures
- `tests/ledgers/all-statuses.jsonl` — 10 entries, one per status
- `tests/ledgers/realistic-week.jsonl` — 18 entries, synthetic week
- `tests/test_ledger_schema.py` — pytest schema validator
- `pyproject.toml` — root; dev optional-dependencies

### Removals
- `scripts/status.sh` — moved to `harness/templates/status.sh`
- `scripts/` — directory deleted

### Rewrites (human edits; dogfood is paused through Phase 2)
- `CONTRIBUTING.md` — document new paths + `pytest` run command
- `.tokenman/CLAUDE.md` — drop `scripts/` from forbidden list

### Tree after Phase 1.1

```
tokenman/
├── README.md
├── CLAUDE.md
├── CONTRIBUTING.md                      # updated
├── LICENSE, .shellcheckrc, .gitignore
├── pyproject.toml                       # NEW
│
├── docs/
│   ├── spec.md
│   └── superpowers/
│       └── specs/
│           ├── 2026-04-18-phase-0-scaffolding-design.md
│           └── 2026-04-18-phase-1-1-ledger-schema-design.md   # this file
│
├── harness/
│   ├── README.md
│   ├── lib/                             # NEW — canonical schema lives here
│   │   └── ledger.schema.json           # NEW
│   ├── templates/                       # NEW — install-time assets
│   │   └── status.sh                    # NEW (moved from scripts/, rewritten)
│   └── workflows/
│       └── tokenman.yml.template
│
├── scoping/
│   └── README.md
│
├── onboarding/
│   └── README.md
│
├── recommended-skills.yaml
├── pricing.yaml
│
├── tests/
│   ├── fixtures/                        # fake consumer repos (existing)
│   │   ├── README.md
│   │   ├── tiny-python-repo/
│   │   └── tiny-typescript-repo/
│   ├── ledgers/                         # NEW — ledger JSON fixtures
│   │   ├── README.md                    # NEW
│   │   ├── all-statuses.jsonl           # NEW
│   │   └── realistic-week.jsonl         # NEW
│   └── test_ledger_schema.py            # NEW
│
├── .tokenman/                           # runtime zone, still paused
│   ├── PAUSE
│   ├── tokenman.yaml
│   └── CLAUDE.md                        # updated (scripts/ removed from list)
│
├── .github/
│   └── workflows/
│       └── .gitkeep
│
└── .claude/
    └── skills/
        └── .gitkeep
```

No `scripts/` directory.

Note: `harness/lib/` and `harness/templates/` are introduced here as two
source-zone subdirectories. `lib/` holds the canonical contracts (schema,
later the append utility, the PR opener, etc.); `templates/` holds assets
that `/tokenman init` copies verbatim into consumer repos. Workflow
templates that already live at `harness/workflows/*.template` stay there —
workflows are a distinct category, the more specific directory name
wins.

## File contents

### `harness/lib/ledger.schema.json`

JSON Schema Draft 2020-12. One object per line in `.tokenman/ledger.jsonl`.
Schema shape mirrors `docs/spec.md` §8.1 with structural validation only;
conditional invariants (e.g., "pr non-null iff status == pr_opened") are
documented in `$comment` and enforced by the append utility in 1.2.

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

### `tests/ledgers/README.md`

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
  (~18 entries). Aggregation fixture; exercises the per-skill breakdown,
  7-day totals, and last-N-runs sections of `status.sh`.

## Updating fixtures
If you change the schema, run `pytest` at the repo root. If fixture
entries no longer validate, either fix the entries or revert the schema
change — schema drift should require an explicit update path, not happen
by accident.
```

### `tests/ledgers/all-statuses.jsonl`

Exactly 10 one-line entries (one per `status` value), covering the
schema-coverage matrix:

| run_id | status | generator | evaluator | pr |
|---|---|---|---|---|
| r-0001 | pr_opened | populated | null | 128 |
| r-0002 | no_change | populated | null | null |
| r-0003 | skipped_lock | null | null | null |
| r-0004 | skipped_cooldown | null | null | null |
| r-0005 | skipped_budget | null | null | null |
| r-0006 | skipped_pause | null | null | null |
| r-0007 | skipped_review_bandwidth | null | null | null |
| r-0008 | aborted_gate | populated | null | null |
| r-0009 | aborted_evaluator | populated | populated (verdict: reject) | null |
| r-0010 | error | populated | null | null |

Timestamps sequential, `skill` values varied across 2–3 skill names,
token counts realistic (low thousands for generator runs, 0 for skips).

### `tests/ledgers/realistic-week.jsonl`

Exactly 18 entries across three skills (`readme-maintainer`,
`dead-code-cleanup`, `dep-bump-safe`). Distribution:

- 8 × `no_change`
- 6 × `pr_opened` (3 readme, 2 dead-code, 1 dep-bump; varying PR numbers)
- 3 × `skipped_*` (one each of `skipped_lock`, `skipped_cooldown`, `skipped_pause`)
- 1 × `error`
- 0 × `aborted_*` (rare in a "realistic" week)

Per-skill run totals: readme-maintainer 7, dead-code-cleanup 7,
dep-bump-safe 4 (sum = 18). Per-skill token totals: 110,200 + 58,100 +
16,000 = 184,300 (so `avg = 10,239/run` in the rendered output below).

Run IDs monotonic `r-0001`…`r-0018`. Timestamps span
`2026-04-11T00:00:00Z` through `2026-04-17T23:59:59Z` (seven full
calendar days, ending the day before the fixture was authored).

### `harness/templates/status.sh`

Bash+jq. Ledger-only. Reads exactly one argument: the ledger path
(default `.tokenman/ledger.jsonl`). Handles: missing file (benign
message, exit 0), empty file (benign message, exit 0), one-entry ledger,
many-entry ledger.

Output (against `tests/ledgers/realistic-week.jsonl`):

```
Tokenman status

Ledger:  tests/ledgers/realistic-week.jsonl  (18 entries)

Summary (all time):
  Runs:          18
  PRs opened:     6
  No-change:      8
  Skipped:        3  (lock: 1, cooldown: 1, pause: 1)
  Aborted:        0
  Errors:         1
  Tokens:   184,300  (avg 10,239/run)

Top skills (all time):
  readme-maintainer   110,200 tok   7 runs  3 PRs
  dead-code-cleanup    58,100 tok   7 runs  2 PRs
  dep-bump-safe        16,000 tok   4 runs  1 PR

Last 10 runs (newest first):
  r-0018  2026-04-17T18:00Z  readme-maintainer   pr_opened       18,400
  r-0017  2026-04-17T10:00Z  dead-code-cleanup   no_change        5,100
  ...
```

**Window framing.** Spec §8.3 uses a "last 7 days" framing, but that
requires either real-time date math (drifts against static fixtures) or a
`--since` flag (scope creep). Phase 1.1 renders all-time totals; Phase 2
adds windowed views alongside cap % once budget enforcement needs them.

Implementation shape (pseudocode):

```bash
#!/usr/bin/env bash
# status.sh — human-readable summary of .tokenman/ledger.jsonl (v1)
# Phase 1.1 of docs/spec.md §12. Ledger-only; no GitHub API.
#
# Usage:  bash harness/templates/status.sh [ledger-path]
# Default: .tokenman/ledger.jsonl
#
# Dependencies: jq, standard POSIX tools.
set -euo pipefail

LEDGER="${1:-.tokenman/ledger.jsonl}"

# 1. Missing / empty ledger → benign message, exit 0.
# 2. Header: path + entry count.
# 3. All-time summary: group by status, count, sum tokens.
# 4. Top skills (all time): per-skill tokens, runs, PRs opened.
# 5. Last 10 runs (newest first): timestamp, skill, status, total_tokens.
```

Must pass `shellcheck` (the repo has `.shellcheckrc`). No behavior
changes from the existing script beyond schema alignment and cap-%
removal.

### `pyproject.toml`

Repo-root file (first time).

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

Not a published package. Contributors install with:

```bash
pip install -e '.[dev]'
pytest
```

The `pytest` invocation picks up `tests/test_ledger_schema.py` and any
future library-side tests. Fixture-repo tests inside
`tests/fixtures/tiny-python-repo/` are not discovered (they live under a
deeper pyproject).

### `tests/test_ledger_schema.py`

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
    assert actual == expected, f"missing: {expected - actual}, extra: {actual - expected}"
```

Three tests total: two from the parametrized group (one per fixture
file), one enum-coverage assertion on `all-statuses.jsonl`.

### `CONTRIBUTING.md` diff

Add a "Running tests" section pointing at the new pytest workflow, plus
brief notes that ledger test data lives at `tests/ledgers/` and the
canonical schema at `harness/lib/ledger.schema.json`. Keep the
source/runtime split explanation intact.

### `.tokenman/CLAUDE.md` diff

Remove `scripts/` from the forbidden-paths list (the directory no longer
exists). Leave the rest of the paranoid list intact: `harness/`,
`scoping/`, `onboarding/`, `recommended-skills.yaml`, `pricing.yaml`,
`.github/`, `.claude/skills/`, `tests/fixtures/`, `.tokenman/CLAUDE.md`,
`.tokenman/tokenman.yaml`, `LICENSE`, `.gitignore`, `.shellcheckrc`.

Note: `tests/ledgers/` is **not** added to the forbidden list. It is
test data, not fixture consumer repos — harness runs still don't write
to it directly, and the broader `.tokenman/CLAUDE.md` posture ("if in
doubt, abort") covers accidental edits. This keeps the forbidden list
tight and intentional.

## Exit criteria

1. **Schema valid.** `harness/lib/ledger.schema.json` parses as valid
   JSON Schema Draft 2020-12 (verified via `jsonschema` library load).
2. **Enum coverage fixture.** `tests/ledgers/all-statuses.jsonl` has
   exactly 10 entries, one per `status` value. Verified by
   `test_all_statuses_fixture_covers_enum`.
3. **Realistic-week fixture.** `tests/ledgers/realistic-week.jsonl` has
   exactly 18 entries with timestamps `2026-04-11T00:00:00Z` through
   `2026-04-17T23:59:59Z`. Per-skill and per-status breakdown matches
   the "realistic-week" distribution above.
4. **Tests pass.** After `pip install -e '.[dev]'`, `pytest` from repo
   root exits 0 with 3 tests passing.
5. **`status.sh` renders.**
   - `bash harness/templates/status.sh tests/ledgers/realistic-week.jsonl`
     prints the expected shape (header, all-time summary, top skills,
     last 10 runs) and exits 0.
   - `bash harness/templates/status.sh tests/ledgers/all-statuses.jsonl`
     renders without error and exits 0.
   - `bash harness/templates/status.sh /tmp/nonexistent.jsonl` prints a
     benign "no ledger" message and exits 0.
6. **Shellcheck.** `shellcheck harness/templates/status.sh` passes.
7. **`scripts/` gone.** Directory and file both absent from working tree.
8. **Runtime CLAUDE.md updated.** `scripts/` no longer in the forbidden
   paths list. `harness/` still forbidden (covers `harness/lib/` and
   `harness/templates/`).
9. **CONTRIBUTING updated.** Documents `pip install -e '.[dev]'` +
   `pytest` workflow and points at schema + fixtures paths.
10. **Working tree clean** after the 5 commits (see next section).

## Order of commits

Five commits, independently reviewable:

1. `feat(harness): lock ledger schema v1` — add
   `harness/lib/ledger.schema.json` and `tests/ledgers/README.md`.
2. `test: add ledger schema fixtures` — add
   `tests/ledgers/all-statuses.jsonl` and
   `tests/ledgers/realistic-week.jsonl`.
3. `chore: add pyproject and ledger schema validation test` — add root
   `pyproject.toml` and `tests/test_ledger_schema.py`.
4. `feat(harness): move status.sh to harness/templates and rewrite for new schema` —
   move file, rewrite for new schema, delete `scripts/`.
5. `docs: update CONTRIBUTING and runtime CLAUDE.md for 1.1 paths` —
   document pytest workflow, remove `scripts/` from `.tokenman/CLAUDE.md`
   forbidden list.

Each commit uses the trailer:

```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

Each is self-contained — earlier commits don't leave the working tree in a
broken state (e.g., commit 2 adds fixtures but commit 3 is what imports
them into the test; commit 1's fixtures README promises files that arrive
in commit 2, which is a forward reference in prose, not a runtime broken
state).

## What's deliberately NOT in Phase 1.1

- **Append-validate utility** — ships with 1.2's harness runner.
- **Conditional invariants enforcement** — documented in the schema's
  `$comment`; enforced by the append utility in 1.2.
- **PR-state resolution via `gh pr view`** — separate script or Phase 2.
- **Cap % / budget awareness in `status.sh`** — requires config read;
  belongs with budget enforcement in Phase 2.
- **`/tokenman init` copying `status.sh` into consumers** — Phase 1.2 or
  later.
- **Fixture consumer-repo runs** — Phase 1.2 wires the harness to
  actually run against the existing `tests/fixtures/tiny-*-repo/`.

## Open items

None blocking Phase 1.1 execution. Forward-looking questions that may
surface when Phase 1.2 starts:

1. Should the append utility live at `harness/lib/ledger.py` (Python) or
   `harness/lib/append-ledger.sh` (bash)? Depends on the harness glue
   language, which is a Phase 1.2 decision.
2. Should `harness/templates/status.sh` be copied into consumers by
   `/tokenman init` (file copy) or symlinked (not portable) or re-
   generated from the library (coupling)? Straight file copy is the
   default; confirm when `/tokenman init` is implemented.

## Verification (after all five commits)

```bash
# 1. Schema parses
python3 -c "import json; json.load(open('harness/lib/ledger.schema.json'))" && echo OK

# 2. Tests pass
pip install -e '.[dev]' -q && pytest -q

# 3. status.sh renders without error
bash harness/templates/status.sh tests/ledgers/realistic-week.jsonl >/dev/null && echo OK
bash harness/templates/status.sh tests/ledgers/all-statuses.jsonl >/dev/null && echo OK
bash harness/templates/status.sh /tmp/no-such-ledger.jsonl            && echo OK

# 4. shellcheck passes
shellcheck harness/templates/status.sh && echo OK

# 5. scripts/ gone
test ! -e scripts && echo OK

# 6. working tree clean
git status
```
