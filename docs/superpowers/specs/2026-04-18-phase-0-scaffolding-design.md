# Phase 0 Scaffolding — Design

**Date:** 2026-04-18
**Status:** Approved via brainstorming, pending user review of this doc
**Parent spec:** `docs/spec.md` v0.2, §12 "Phase 0 — Foundation"

## Purpose

Scaffold the tokenman repo for the Option B single-repo dogfood structure
described in `docs/spec.md`. Phase 0 establishes layout and contracts only —
no runnable harness code. Exit state: repo tree clean, contracts written,
dogfood PAUSE committed, nothing runs.

## Scope decisions (from brainstorming, 2026-04-18)

1. **Legacy disposition** — delete entirely. The current `/skills/` tree
   (including `dead-code-cleanup` and seven legacy skills) and
   `/workflows/tokenman-run.yml` contradict the new direction (spec §5.1:
   tokenman ships zero skills). Git history preserves everything. If
   `dead-code-cleanup` earns a catalog spot later, it gets promoted to its
   own repo.

2. **Scaffolding depth** — contract-level. Directories get READMEs; schema
   files (`recommended-skills.yaml`, `pricing.yaml`, `.tokenman/tokenman.yaml`)
   are written with their shapes documented but empty of real content. A stub
   workflow template exists but exits immediately. No working runtime logic.

3. **Fixture shape** — skeleton with placeholder source files. Each fixture
   is structured like a real consumer repo (has `.tokenman/`,
   `.github/workflows/`, `.claude/skills/`) but contains only enough code
   that a later `readme-maintainer` run would have something to propose.

4. **Two `tokenman.yaml` shapes** — library and consumer divergence. The
   library's runtime zone config has stricter caps and a `dogfood.phase`
   field (spec §10.5); the consumer shape doesn't. Honest structural
   divergence is preferred over hiding state elsewhere.

## Before / after directory layout

### Deletions
- `/skills/` entire tree (all subdirs + 7 loose `.md` files)
- `/workflows/tokenman-run.yml`
- `/workflows/` (empty after removal)

### Kept as-is
- `/LICENSE`, `/.shellcheckrc`, `/.gitignore` — unchanged
- `/docs/spec.md` — already written
- `/scripts/status.sh` — deferred rework to Phase 1 when ledger schema locks;
  harmless at Phase 0 because no ledger exists

### Rewrites
- `/README.md` — currently 7.8k describing old direction; becomes brief
  overview + pointer to spec
- `/CLAUDE.md` — currently says "dogfooding is OFF" and lists legacy
  skills; becomes a router for interactive sessions pointing at the three
  content docs
- `/.tokenman/tokenman.yaml` — currently `role: library, produces:`; becomes
  the new runtime-config schema, paused and zero-budget

### Tree after Phase 0

```
tokenman/
├── README.md                          # rewritten — brief + pointer to spec
├── CLAUDE.md                          # rewritten — router
├── CONTRIBUTING.md                    # NEW — source/runtime split
├── LICENSE, .shellcheckrc, .gitignore # kept
│
├── docs/
│   ├── spec.md                        # exists
│   └── superpowers/
│       └── specs/
│           └── 2026-04-18-phase-0-scaffolding-design.md  # this file
│
├── harness/
│   ├── README.md                      # NEW
│   └── workflows/
│       └── tokenman.yml.template      # NEW — stub, exits immediately
│
├── scoping/
│   └── README.md                      # NEW
│
├── onboarding/
│   └── README.md                      # NEW
│
├── recommended-skills.yaml            # NEW — empty catalog, schema in comments
├── pricing.yaml                       # NEW — TODO placeholder, shape documented
│
├── tests/
│   └── fixtures/
│       ├── README.md                  # NEW
│       ├── tiny-python-repo/          # skeleton consumer (see below)
│       └── tiny-typescript-repo/      # skeleton consumer (see below)
│
├── scripts/
│   └── status.sh                      # kept, deferred rework
│
├── .tokenman/                         # runtime zone
│   ├── PAUSE                          # NEW — committed
│   ├── tokenman.yaml                  # rewritten — new schema, paused
│   └── CLAUDE.md                      # NEW — paranoid boundaries
│
├── .github/
│   └── workflows/
│       └── .gitkeep                   # empty dir tracked
│
└── .claude/
    └── skills/
        └── .gitkeep                   # empty dir tracked
```

### Note: deviation from spec §10.1

Spec §10.1 says "the workflow file exists but will not execute while
PAUSE is present." Phase 0 takes a safer approach: no workflow file is
installed yet. The directory `.github/workflows/` exists (tracked via
`.gitkeep`) but contains no workflow. `.github/workflows/tokenman.yml`
is installed at the Phase 3 gate alongside PAUSE removal. The PAUSE
file still sits in the runtime zone at Phase 0 as a leading indicator
of the paused posture and to catch accidental workflow installation
before Phase 3.

## File contents

### `.tokenman/CLAUDE.md` (paranoid boundaries)

Adapted from spec §10.2 for this repo's actual layout:

```markdown
# Tokenman context for the tokenman library repo

## CRITICAL: this repo is the tokenman library itself.
## Dogfooding is SEVERELY restricted. PAUSE is ON through Phase 2.

## Allowed paths (nothing else — and even these are gated by phase)
- docs/**/*.md                 # Phase 4+
- README.md                    # Phase 3+ (narrow README dogfood)
- CHANGELOG.md                 # Phase 4+ (if it ever exists)
- .tokenman/smoketest.md       # Phase 3 smoke test only

## FORBIDDEN paths (never touch, any phase)
- harness/                     # the runtime itself
- scoping/                     # the scoping logic itself
- onboarding/                  # the onboarding logic itself
- recommended-skills.yaml      # the catalog
- pricing.yaml                 # budget calibration
- .github/                     # the workflows
- .claude/skills/              # installed skills
- tests/fixtures/              # must remain pristine
- .tokenman/CLAUDE.md          # this file — human-edited only
- .tokenman/tokenman.yaml      # config — human-edited only
- LICENSE, .gitignore, .shellcheckrc, scripts/

## FORBIDDEN operations
- Any change that could affect how the harness behaves
- Any change to version numbers
- Any change to package.json / pyproject.toml (if ever added)
- Direct commits to main
- Auto-merge

## If in doubt, abort. Open an issue instead of a PR.
```

### `.tokenman/tokenman.yaml` (new runtime schema)

```yaml
# Tokenman runtime config for the LIBRARY REPO'S own dogfood.
# Consumers have identical structure but different values.
# See docs/spec.md §3.4 for the consumer equivalent.

schedule:
  strategy: manual             # no cron trigger until Phase 3
  min_interval: 48h
  max_interval: 14d
  pause_at: 95%

budget:
  # Library-specific cap: ~20% of normal-consumer default (see spec §7.2).
  # Zero until Phase 3; raised to real values when dogfood starts.
  per_run_tokens: 0
  per_skill_weekly_tokens: 0
  global_weekly_tokens: 0

skills:
  # No skills enabled in Phase 0-2.
  # Phase 3 will add readme-maintainer for smoke test → narrow README scope.
  []

retention:
  artifacts_days: 14           # stricter than consumer default (30)

dogfood:
  phase: 0                     # human-edited as phases advance
  pause_committed: true        # presence of .tokenman/PAUSE
```

### `.tokenman/PAUSE`

```
# This file halts all tokenman runs on this repo.
# Removed at Phase 3 gate per docs/spec.md §12. Do not delete without
# reading the phased roadmap.
```

### `recommended-skills.yaml`

```yaml
# Curated catalog of community-authored skills.
# Tokenman ships ZERO skills (spec §5.1) — entries below are references only.
#
# Schema per entry (spec §5.1):
#   <skill-name>:
#     source: <git url or path>
#     version: <semver or tag>
#     tier: starter | common | advanced
#     blast_radius: low | medium | high
#     typical_tokens_per_run: <int>
#     description: <one line>
#     default_cadence: <e.g. weekly, on-change>
#     evaluator_strictness: low | medium | high
#
# Empty at Phase 0. First entry added in Phase 1 (readme-maintainer).
```

### `pricing.yaml`

```yaml
# Claude pricing, pulled at consumer-repo init to calibrate budget suggestions.
# Schema and values TBD; wired in Phase 2.
#
# Expected shape:
#   plans:
#     pro:       { monthly_usd: ..., approx_tokens: ... }
#     team:      { ... }
#   allocations:
#     conservative: 0.05
#     recommended:  0.10
#     aggressive:   0.20
```

### `harness/workflows/tokenman.yml.template`

```yaml
# TEMPLATE — installed into consumer repos at /tokenman init as
# .github/workflows/tokenman.yml. This file never runs; the installed copy does.
#
# Phase 0: stub. Phase 1 adds trigger-check + generator steps.

name: tokenman
on:
  workflow_dispatch:
    inputs:
      mode:
        description: run mode (scheduled | onboarding | smoke)
        default: scheduled

jobs:
  tokenman-run:
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo "tokenman.yml.template — Phase 0 stub. Not yet implemented."
          exit 0
```

### Root `/CLAUDE.md` (router, rewritten)

```markdown
# Tokenman

Tokenman is a harness that makes `claude -p` safe to run unattended on a repo.
See `docs/spec.md` for the full scoping draft.

## For interactive Claude Code sessions

- **Direction & architecture**: `docs/spec.md` (authoritative)
- **Contributor workflow & source/runtime split**: `CONTRIBUTING.md`
- **Dogfooding boundaries (runtime zone)**: `.tokenman/CLAUDE.md` — strict

## Commit conventions
Imperative, sentence case, no period, <72 chars.
- feat(harness|scoping|onboarding): …
- fix(harness|…): …
- docs: …
- chore: …

## What NOT to do in this repo
- Do not modify files in `harness/`, `scoping/`, `onboarding/`,
  `recommended-skills.yaml`, or `pricing.yaml` from a dogfood run. The
  paranoid `.tokenman/CLAUDE.md` forbids this.
- Do not remove `.tokenman/PAUSE` until the Phase 3 gate (spec §12).
- Do not call the Anthropic API directly — all execution goes through `claude -p`.

## Failure log
(fresh — no entries)
```

### Root `/README.md` (brief, rewritten)

One-screen overview following spec §1:
- What tokenman is (the product sentence)
- What it ships / does not ship
- Status: "Phase 0 scaffolding in place; nothing runs yet"
- Pointers to `docs/spec.md` and `CONTRIBUTING.md`

### `/CONTRIBUTING.md` (new)

Explains source/runtime split from spec §3.2:
- Source zone files ship to consumers; runtime zone files are local dogfood state
- How to contribute to each zone
- Why the separation matters
- `[tokenman]` commit prefix convention for dogfood PRs (spec §10.6)
- Where to look for what

### `harness/README.md`, `scoping/README.md`, `onboarding/README.md`

Each ~10 lines: zone purpose + "this directory is source zone — its contents ship to consumers" + link to relevant spec section.

## Fixture design

### `tests/fixtures/README.md`

```markdown
# Fixture consumer repos

These directories simulate external consumer repos for harness testing.
Treat them as pristine: never edit from a dogfood run (forbidden in
.tokenman/CLAUDE.md). Harness tests reset them as part of their setup.

## Phase 0 status
Skeleton only — no harness runs against them yet.

## Fixtures
- tiny-python-repo/      — minimal Python project
- tiny-typescript-repo/  — minimal TypeScript project
```

### `tests/fixtures/tiny-python-repo/`

```
tiny-python-repo/
├── README.md                     # 2-3 lines: "fixture for harness testing"
├── pyproject.toml                # package name, version 0.1.0, no deps
├── src/
│   └── tiny_python_repo/
│       └── __init__.py           # one trivial function + one unused import
├── tests/
│   └── test_smoke.py             # one passing test
├── .tokenman/
│   └── tokenman.yaml             # consumer-shape config
├── .github/
│   └── workflows/
│       └── .gitkeep              # empty; filled by harness tests
└── .claude/
    └── skills/
        └── .gitkeep              # empty; filled by harness tests
```

### `tests/fixtures/tiny-typescript-repo/`

```
tiny-typescript-repo/
├── README.md
├── package.json                  # name, version 0.1.0, no runtime deps
├── tsconfig.json
├── src/
│   └── index.ts                  # one exported function
├── tests/
│   └── smoke.test.ts             # one passing test (node --test)
├── .tokenman/
│   └── tokenman.yaml             # consumer-shape config
├── .github/
│   └── workflows/
│       └── .gitkeep              # empty
└── .claude/
    └── skills/
        └── .gitkeep              # empty
```

### Consumer-shape `tokenman.yaml` for fixtures

Contrast with the library-shape above — no `dogfood:` field, normal
budget values (placeholder), consumer-default retention:

```yaml
schedule:
  strategy: fixed
  min_interval: 48h

budget:
  per_run_tokens: 30000
  per_skill_weekly_tokens: 100000
  global_weekly_tokens: 250000

skills: []

retention:
  artifacts_days: 30
```

## Exit criteria

Phase 0 is done when all of these hold:

1. **Legacy cleared.** No `/skills/`, no `/workflows/tokenman-run.yml`.
   Working tree matches the tree above.
2. **Source zone populated with contract-level stubs.** `harness/`,
   `scoping/`, `onboarding/` each have a README; `recommended-skills.yaml`
   and `pricing.yaml` exist with schema comments;
   `harness/workflows/tokenman.yml.template` is a no-op stub.
3. **Runtime zone populated and paused.** `.tokenman/PAUSE` committed;
   `.tokenman/tokenman.yaml` on new schema with `schedule.strategy: manual`
   and all budgets zeroed; `.tokenman/CLAUDE.md` paranoid-bounded;
   `.github/workflows/` and `.claude/skills/` exist as empty directories
   tracked via `.gitkeep` files.
4. **Documentation rewritten.** Root `README.md`, root `CLAUDE.md`, and new
   `CONTRIBUTING.md` point at `docs/spec.md` as source of truth and explain
   the source/runtime split.
5. **Fixture skeletons in place.** `tests/fixtures/tiny-python-repo/` and
   `tiny-typescript-repo/` with the shape above, each in consumer shape.
6. **Nothing runs.** Verifiable by: `.tokenman/PAUSE` present +
   `.tokenman/tokenman.yaml` has `schedule.strategy: manual` +
   `.github/workflows/` empty + no cron triggers in any committed workflow.
7. **Committed in logical chunks** so the transition is reviewable in git
   history.

## Order of operations

Six commits, each independently reviewable:

1. `chore: remove legacy skills and workflows`
   - Delete `/skills/`, `/workflows/`
2. `feat(harness): scaffold source zone`
   - Add `harness/`, `scoping/`, `onboarding/` with READMEs
   - Add `harness/workflows/tokenman.yml.template` stub
3. `feat(catalog): add recommended-skills.yaml and pricing.yaml stubs`
4. `feat(dogfood): initialize paused runtime zone`
   - Rewrite `.tokenman/tokenman.yaml` to new schema
   - Add `.tokenman/PAUSE`
   - Add paranoid `.tokenman/CLAUDE.md`
   - Create `.github/workflows/.gitkeep` and `.claude/skills/.gitkeep`
     (git does not track empty directories otherwise)
5. `test: add fixture skeleton repos`
   - Add `tests/fixtures/` with both fixtures and fixture README
6. `docs: rewrite README, CLAUDE.md, add CONTRIBUTING`
   - Rewrite root `/README.md` and `/CLAUDE.md`
   - Add `/CONTRIBUTING.md`

## What's deliberately NOT in Phase 0

- Working workflow logic (Phase 1)
- Scoping or onboarding implementation (Phase 1)
- Budget enforcement (Phase 2)
- Generator/evaluator split (Phase 3)
- Live dogfood of any kind (Phase 3+)
- Ledger schema lock-in (Phase 1)
- Rework of `scripts/status.sh` (Phase 1, after ledger schema locks)
- `CHANGELOG.md` (Phase 5 when first external user exists)

## Open items

None blocking Phase 0 execution. Deferred concerns tracked by the phase
they belong to, above.

## Verification (after all commits)

- `ls /home/dev/projects/tokenman/skills 2>&1 | grep -q "No such"` — legacy gone
- `test -f /home/dev/projects/tokenman/.tokenman/PAUSE` — PAUSE present
- `grep "strategy: manual" /home/dev/projects/tokenman/.tokenman/tokenman.yaml` — schedule confirmed manual
- `find /home/dev/projects/tokenman/.github/workflows -type f` — empty (or just .gitkeep)
- `bash /home/dev/projects/tokenman/scripts/status.sh` — prints "No ledger at ..." (harmless)
- Directory tree matches the "after" tree above
