# Phase 0 Scaffolding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the tokenman repo from its legacy "ships skills" shape into the library-plus-paused-dogfood layout specified in `docs/spec.md` §3.3. Delete legacy, scaffold source and runtime zones with contract-level stubs, install paranoid boundaries, add fixture skeletons, rewrite repo docs.

**Architecture:** Seven tasks, six of which produce one logical commit each. Task 7 is a no-commit verification pass. No runtime code is written — only directory structure, schema stubs, documentation, and fixture skeletons. The design this plan implements is `docs/superpowers/specs/2026-04-18-phase-0-scaffolding-design.md`.

**Tech Stack:** Git, Bash, YAML, Markdown, Python (fixture file content), TypeScript (fixture file content). No runtime dependencies added.

---

## Scope Check

This plan covers a single, well-bounded subsystem (Phase 0 scaffolding). No decomposition needed.

---

## File Structure

### Deletions (Task 1)
- `/skills/` entire tree
- `/workflows/tokenman-run.yml`
- `/workflows/` (auto-removed after its only file is deleted)

### Rewrites
- `/README.md` — Task 6
- `/CLAUDE.md` — Task 6
- `/.tokenman/tokenman.yaml` — Task 4

### New files by zone

**Source zone (Tasks 2 and 3):**
- `/harness/README.md`
- `/harness/workflows/tokenman.yml.template`
- `/scoping/README.md`
- `/onboarding/README.md`
- `/recommended-skills.yaml`
- `/pricing.yaml`

**Runtime zone (Task 4):**
- `/.tokenman/PAUSE`
- `/.tokenman/CLAUDE.md` (paranoid boundaries)
- `/.github/workflows/.gitkeep`
- `/.claude/skills/.gitkeep`

**Fixtures (Task 5):**
- `/tests/fixtures/README.md`
- `/tests/fixtures/tiny-python-repo/README.md`
- `/tests/fixtures/tiny-python-repo/pyproject.toml`
- `/tests/fixtures/tiny-python-repo/src/tiny_python_repo/__init__.py`
- `/tests/fixtures/tiny-python-repo/tests/test_smoke.py`
- `/tests/fixtures/tiny-python-repo/.tokenman/tokenman.yaml`
- `/tests/fixtures/tiny-python-repo/.github/workflows/.gitkeep`
- `/tests/fixtures/tiny-python-repo/.claude/skills/.gitkeep`
- `/tests/fixtures/tiny-typescript-repo/README.md`
- `/tests/fixtures/tiny-typescript-repo/package.json`
- `/tests/fixtures/tiny-typescript-repo/tsconfig.json`
- `/tests/fixtures/tiny-typescript-repo/src/index.ts`
- `/tests/fixtures/tiny-typescript-repo/tests/smoke.test.ts`
- `/tests/fixtures/tiny-typescript-repo/.tokenman/tokenman.yaml`
- `/tests/fixtures/tiny-typescript-repo/.github/workflows/.gitkeep`
- `/tests/fixtures/tiny-typescript-repo/.claude/skills/.gitkeep`

**Contributor doc (Task 6):**
- `/CONTRIBUTING.md`

### Kept unchanged
- `/LICENSE`, `/.shellcheckrc`, `/.gitignore`
- `/docs/spec.md`
- `/docs/superpowers/specs/2026-04-18-phase-0-scaffolding-design.md`
- `/scripts/status.sh` (deferred rework to Phase 1)

---

## Commit-Message Convention

All commits on Phase 0 use the convention documented in the root `CLAUDE.md` being written in Task 6:
- Imperative, sentence case, no trailing period, <72 chars
- `feat(harness|scoping|onboarding|catalog|dogfood): …`, `chore: …`, `test: …`, `docs: …`

Each commit includes the Claude trailer:
```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

The work happens in **`/home/dev/projects/tokenman`** — all absolute paths below assume that directory. All `git` commands use `-C /home/dev/projects/tokenman` to avoid `cd`.

---

## Tasks

### Task 1: Remove legacy skills and workflows

**Files:**
- Delete: `/home/dev/projects/tokenman/skills/` (entire tree)
- Delete: `/home/dev/projects/tokenman/workflows/tokenman-run.yml`

**Rationale:** Per `docs/spec.md` §5.1 tokenman ships zero skills; the current `/skills/` tree (9 subdirs including `dead-code-cleanup` and seven legacy skills, plus 7 loose `.md` files) contradicts the new direction. `/workflows/tokenman-run.yml` is the old monolithic workflow being replaced by `harness/workflows/tokenman.yml.template` in Task 2. Git history preserves everything.

- [ ] **Step 1: Verify current legacy state before deletion**

Run:
```bash
ls /home/dev/projects/tokenman/skills && ls /home/dev/projects/tokenman/workflows
```

Expected: lists the legacy skill directories and `tokenman-run.yml`. If either directory is missing, STOP and investigate — someone else may have already moved them.

- [ ] **Step 2: Stage-and-delete /skills/ with git rm**

Run:
```bash
git -C /home/dev/projects/tokenman rm -rf skills
```

Expected: git prints `rm 'skills/...'` for each tracked file. The working tree directory is removed.

- [ ] **Step 3: Stage-and-delete /workflows/ with git rm**

Run:
```bash
git -C /home/dev/projects/tokenman rm -rf workflows
```

Expected: git prints `rm 'workflows/tokenman-run.yml'`. Directory removed.

- [ ] **Step 4: Verify deletions**

Run:
```bash
test ! -e /home/dev/projects/tokenman/skills && test ! -e /home/dev/projects/tokenman/workflows && echo OK
```

Expected: `OK` printed on stdout. Any other output is a failure.

- [ ] **Step 5: Verify staged deletions with git status**

Run:
```bash
git -C /home/dev/projects/tokenman status --short
```

Expected: every line starts with `D ` (uppercase D = staged deletion). No untracked or modified files.

- [ ] **Step 6: Commit**

Run:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
chore: remove legacy skills and workflows

Per docs/spec.md §5.1 tokenman ships zero skills. The /skills/ surface
(dead-code-cleanup plus seven legacy skills) and the monolithic
workflows/tokenman-run.yml are retired. Git history preserves everything;
dead-code-cleanup can be promoted to its own repo later if it earns a
catalog entry.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds. Running `git -C /home/dev/projects/tokenman log --oneline -1` shows `chore: remove legacy skills and workflows`.

---

### Task 2: Scaffold source zone directories

**Files:**
- Create: `/home/dev/projects/tokenman/harness/README.md`
- Create: `/home/dev/projects/tokenman/harness/workflows/tokenman.yml.template`
- Create: `/home/dev/projects/tokenman/scoping/README.md`
- Create: `/home/dev/projects/tokenman/onboarding/README.md`

**Rationale:** Scaffold the three source-zone directories (`harness/`, `scoping/`, `onboarding/`) from `docs/spec.md` §3.2. Each gets a README documenting its purpose and pointing to the relevant spec section. The harness directory also gets the workflow template — a no-op stub that Phase 1 will populate.

- [ ] **Step 1: Create `harness/README.md`**

Write file `/home/dev/projects/tokenman/harness/README.md` with content:

```markdown
# harness/ — Tokenman runtime source

**Source zone.** Contents here ship to consumers when `/tokenman init`
fetches the harness.

## Purpose
The tokenman runtime itself: workflow templates, generator/evaluator
drivers, deterministic gates, ledger append logic, PR opener. Not yet
implemented — Phase 0 scaffolds the directory and the workflow template
stub. Phase 1+ populates lib/ with actual code.

## Contents
- `workflows/tokenman.yml.template` — installed into
  consumers at `.github/workflows/tokenman.yml` by `/tokenman init`.

## See also
- `docs/spec.md` §3.2 (source vs runtime paths)
- `docs/spec.md` §4 (execution pipeline)
- `CONTRIBUTING.md` (source/runtime split)
```

- [ ] **Step 2: Create `harness/workflows/tokenman.yml.template`**

Write file `/home/dev/projects/tokenman/harness/workflows/tokenman.yml.template` with content:

```yaml
# TEMPLATE — installed into consumer repos at /tokenman init as
# .github/workflows/tokenman.yml. This file in the library repo never runs;
# the installed copy on a consumer does.
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

- [ ] **Step 3: Create `scoping/README.md`**

Write file `/home/dev/projects/tokenman/scoping/README.md` with content:

```markdown
# scoping/ — Discovery and scope-proposal logic

**Source zone.** Contents here ship to consumers.

## Purpose
Implements the scope-proposal flow described in `docs/spec.md` §6.3.
Given a fresh consumer repo, detects language/size/test-coverage/activity
and proposes an initial scope (skills, boundaries, budget, schedule).
Output: `.tokenman/initial-scope.md` in the consumer repo.

## Status
Empty at Phase 0. Implemented in Phase 1.

## See also
- `docs/spec.md` §6.3 (initial scoping)
- `docs/spec.md` §12 Phase 1 (wedge + guided onboarding)
```

- [ ] **Step 4: Create `onboarding/README.md`**

Write file `/home/dev/projects/tokenman/onboarding/README.md` with content:

```markdown
# onboarding/ — Guided first-run flow

**Source zone.** Contents here ship to consumers.

## Purpose
Implements the guided onboarding run described in `docs/spec.md` §6.4.
Runs all enabled skills back-to-back in one session with an elevated
budget, opens one PR per skill, writes
`.tokenman/onboarding-summary.md`. Exists to get a new consumer from
install to visible value in ~10 minutes.

## Status
Empty at Phase 0. Implemented in Phase 1.

## See also
- `docs/spec.md` §6.4 (guided onboarding run)
- `docs/spec.md` §12 Phase 1
```

- [ ] **Step 5: Verify files were created correctly**

Run:
```bash
ls /home/dev/projects/tokenman/harness/README.md /home/dev/projects/tokenman/harness/workflows/tokenman.yml.template /home/dev/projects/tokenman/scoping/README.md /home/dev/projects/tokenman/onboarding/README.md
```

Expected: all four paths print on stdout, none raise "No such file".

- [ ] **Step 6: Verify YAML template is syntactically valid**

Run:
```bash
python3 -c "import yaml; yaml.safe_load(open('/home/dev/projects/tokenman/harness/workflows/tokenman.yml.template'))"
```

Expected: no output, exit code 0. Any traceback is a failure.

- [ ] **Step 7: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add harness scoping onboarding
git -C /home/dev/projects/tokenman status --short
```

Expected: all four new files show `A ` (uppercase A = added).

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
feat(harness): scaffold source zone

Create the three source-zone directories (harness/, scoping/,
onboarding/) with README stubs. Install a no-op tokenman.yml.template
in harness/workflows/. No runtime logic yet — Phase 1 populates.

Per docs/spec.md §3.2 these files ship to consumers at /tokenman init;
the library's own runtime copies live under .github/workflows/ and are
added in a later commit (still empty at Phase 0).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 3: Add catalog and pricing stubs

**Files:**
- Create: `/home/dev/projects/tokenman/recommended-skills.yaml`
- Create: `/home/dev/projects/tokenman/pricing.yaml`

**Rationale:** Two top-level source-zone files: the curated skills catalog and the pricing-calibration data. Both are stubs at Phase 0 — schema comments only, no entries or values. Phase 1 adds the first catalog entry (`readme-maintainer`); Phase 2 wires pricing.

- [ ] **Step 1: Create `recommended-skills.yaml`**

Write file `/home/dev/projects/tokenman/recommended-skills.yaml` with content:

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

- [ ] **Step 2: Create `pricing.yaml`**

Write file `/home/dev/projects/tokenman/pricing.yaml` with content:

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

- [ ] **Step 3: Verify both files are syntactically valid YAML**

Run:
```bash
python3 -c "
import yaml
for f in ['/home/dev/projects/tokenman/recommended-skills.yaml', '/home/dev/projects/tokenman/pricing.yaml']:
    result = yaml.safe_load(open(f))
    print(f, '->', repr(result))
"
```

Expected:
```
/home/dev/projects/tokenman/recommended-skills.yaml -> None
/home/dev/projects/tokenman/pricing.yaml -> None
```

Both parse to `None` because they are comment-only. Any traceback or non-`None` value is a failure.

- [ ] **Step 4: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add recommended-skills.yaml pricing.yaml
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
feat(catalog): add recommended-skills.yaml and pricing.yaml stubs

Both top-level source-zone files scaffolded as schema-only stubs. No
entries or values — Phase 1 populates recommended-skills.yaml with its
first entry (readme-maintainer); Phase 2 wires pricing.yaml into the
budget-calibration flow.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 4: Initialize paused runtime zone

**Files:**
- Rewrite: `/home/dev/projects/tokenman/.tokenman/tokenman.yaml`
- Create: `/home/dev/projects/tokenman/.tokenman/PAUSE`
- Create: `/home/dev/projects/tokenman/.tokenman/CLAUDE.md`
- Create: `/home/dev/projects/tokenman/.github/workflows/.gitkeep`
- Create: `/home/dev/projects/tokenman/.claude/skills/.gitkeep`

**Rationale:** Populate the runtime zone described in `docs/spec.md` §3.3 with paranoid boundaries and a paused configuration. The existing `.tokenman/tokenman.yaml` uses the old `role: library` / `produces:` schema that has no meaning in the new direction; it's replaced with the runtime-config schema (schedule / budget / skills / retention / dogfood). `.tokenman/PAUSE` halts any future run. `.tokenman/CLAUDE.md` documents the paranoid allow/forbid path lists for when dogfood unpauses at Phase 3. `.gitkeep` files ensure the empty directories are tracked (git does not track empty dirs).

- [ ] **Step 1: Read the current `.tokenman/tokenman.yaml` before rewriting**

This verifies the old schema is what we expect (defense against unexpected drift).

Run:
```bash
cat /home/dev/projects/tokenman/.tokenman/tokenman.yaml
```

Expected: the file shows `role: library` and `produces: [dead-code-cleanup]`. If it doesn't, STOP and investigate.

- [ ] **Step 2: Rewrite `.tokenman/tokenman.yaml`**

Replace the file contents entirely with:

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

- [ ] **Step 3: Create `.tokenman/PAUSE`**

Write file `/home/dev/projects/tokenman/.tokenman/PAUSE` with content:

```
# This file halts all tokenman runs on this repo.
# Removed at Phase 3 gate per docs/spec.md §12. Do not delete without
# reading the phased roadmap.
```

- [ ] **Step 4: Create `.tokenman/CLAUDE.md` (paranoid boundaries)**

Write file `/home/dev/projects/tokenman/.tokenman/CLAUDE.md` with content:

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

- [ ] **Step 5: Create `.github/workflows/.gitkeep`**

Write file `/home/dev/projects/tokenman/.github/workflows/.gitkeep` as an empty file.

Run:
```bash
mkdir -p /home/dev/projects/tokenman/.github/workflows && : > /home/dev/projects/tokenman/.github/workflows/.gitkeep
```

Expected: no output, exit 0. The `:` command is a shell no-op; `> path` truncates/creates the file.

- [ ] **Step 6: Create `.claude/skills/.gitkeep`**

Run:
```bash
mkdir -p /home/dev/projects/tokenman/.claude/skills && : > /home/dev/projects/tokenman/.claude/skills/.gitkeep
```

Expected: no output, exit 0.

- [ ] **Step 7: Verify new `.tokenman/tokenman.yaml` is valid YAML with expected shape**

Run:
```bash
python3 -c "
import yaml
d = yaml.safe_load(open('/home/dev/projects/tokenman/.tokenman/tokenman.yaml'))
assert d['schedule']['strategy'] == 'manual', d['schedule']
assert d['budget']['per_run_tokens'] == 0, d['budget']
assert d['skills'] == [], d['skills']
assert d['dogfood']['phase'] == 0, d['dogfood']
assert d['dogfood']['pause_committed'] is True, d['dogfood']
print('OK')
"
```

Expected: `OK` printed. Any `AssertionError` or traceback is a failure.

- [ ] **Step 8: Verify all runtime-zone files exist**

Run:
```bash
ls /home/dev/projects/tokenman/.tokenman/tokenman.yaml /home/dev/projects/tokenman/.tokenman/PAUSE /home/dev/projects/tokenman/.tokenman/CLAUDE.md /home/dev/projects/tokenman/.github/workflows/.gitkeep /home/dev/projects/tokenman/.claude/skills/.gitkeep
```

Expected: all five paths print on stdout, none raise "No such file".

- [ ] **Step 9: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add .tokenman .github .claude
git -C /home/dev/projects/tokenman status --short
```

Expected: `M .tokenman/tokenman.yaml` plus four `A ` lines for the new files.

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
feat(dogfood): initialize paused runtime zone

Rewrite .tokenman/tokenman.yaml to the new schema (schedule / budget /
skills / retention / dogfood) with schedule.strategy: manual and all
budgets at 0. Add .tokenman/PAUSE to halt any run attempt. Add paranoid
.tokenman/CLAUDE.md documenting allowed and forbidden paths for when
dogfood unpauses at Phase 3. Track .github/workflows/ and .claude/skills/
as empty directories via .gitkeep.

Per docs/spec.md §10 the library-specific dogfood runs under much
stricter caps and path restrictions than normal consumers.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 5: Add fixture skeleton repos

**Files:**
- Create 8 files under `/home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/`
- Create 8 files under `/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/`
- Create `/home/dev/projects/tokenman/tests/fixtures/README.md`

**Rationale:** Fixtures simulate external consumer repos for later harness testing (`docs/spec.md` §10.4). Phase 0 establishes the shape — two skeleton fixtures with minimal source code, a test file, consumer-shape `.tokenman/tokenman.yaml`, and empty `.github/workflows/` + `.claude/skills/`. Nothing runs against them yet.

- [ ] **Step 1: Create `tests/fixtures/README.md`**

Write file `/home/dev/projects/tokenman/tests/fixtures/README.md` with content:

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

- [ ] **Step 2: Create `tiny-python-repo/README.md`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/README.md` with content:

```markdown
# tiny-python-repo

Fixture for tokenman harness testing. Simulates a minimal Python consumer repo.
```

- [ ] **Step 3: Create `tiny-python-repo/pyproject.toml`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/pyproject.toml` with content:

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "tiny-python-repo"
version = "0.1.0"
description = "Fixture consumer for tokenman harness testing"
requires-python = ">=3.10"
```

- [ ] **Step 4: Create `tiny-python-repo/src/tiny_python_repo/__init__.py`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/src/tiny_python_repo/__init__.py` with content:

```python
import json  # intentionally unused — representative of dead-code targets


def greet(name: str) -> str:
    return f"hello, {name}"
```

- [ ] **Step 5: Create `tiny-python-repo/tests/test_smoke.py`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/tests/test_smoke.py` with content:

```python
def test_smoke() -> None:
    assert True
```

- [ ] **Step 6: Create `tiny-python-repo/.tokenman/tokenman.yaml` (consumer shape)**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/.tokenman/tokenman.yaml` with content:

```yaml
# Consumer-shape tokenman config for the tiny-python-repo fixture.
# Contrast with ../../../.tokenman/tokenman.yaml (library shape) — no dogfood:
# field, normal placeholder budgets, consumer-default retention.

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

- [ ] **Step 7: Create tiny-python-repo .gitkeep files**

Run:
```bash
mkdir -p /home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/.github/workflows
mkdir -p /home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/.claude/skills
: > /home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/.github/workflows/.gitkeep
: > /home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/.claude/skills/.gitkeep
```

Expected: no output, exit 0.

- [ ] **Step 8: Create `tiny-typescript-repo/README.md`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/README.md` with content:

```markdown
# tiny-typescript-repo

Fixture for tokenman harness testing. Simulates a minimal TypeScript consumer repo.
```

- [ ] **Step 9: Create `tiny-typescript-repo/package.json`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/package.json` with content:

```json
{
  "name": "tiny-typescript-repo",
  "version": "0.1.0",
  "description": "Fixture consumer for tokenman harness testing",
  "type": "module",
  "scripts": {
    "test": "node --test tests/"
  }
}
```

- [ ] **Step 10: Create `tiny-typescript-repo/tsconfig.json`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/tsconfig.json` with content:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "node",
    "strict": true,
    "outDir": "dist"
  },
  "include": ["src/**/*"]
}
```

- [ ] **Step 11: Create `tiny-typescript-repo/src/index.ts`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/src/index.ts` with content:

```typescript
export function greet(name: string): string {
  return `hello, ${name}`;
}
```

- [ ] **Step 12: Create `tiny-typescript-repo/tests/smoke.test.ts`**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/tests/smoke.test.ts` with content:

```typescript
import { test } from 'node:test';
import assert from 'node:assert';

test('smoke', () => {
  assert.ok(true);
});
```

- [ ] **Step 13: Create `tiny-typescript-repo/.tokenman/tokenman.yaml` (consumer shape)**

Write file `/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/.tokenman/tokenman.yaml` with content:

```yaml
# Consumer-shape tokenman config for the tiny-typescript-repo fixture.
# Contrast with ../../../.tokenman/tokenman.yaml (library shape) — no dogfood:
# field, normal placeholder budgets, consumer-default retention.

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

- [ ] **Step 14: Create tiny-typescript-repo .gitkeep files**

Run:
```bash
mkdir -p /home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/.github/workflows
mkdir -p /home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/.claude/skills
: > /home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/.github/workflows/.gitkeep
: > /home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/.claude/skills/.gitkeep
```

Expected: no output, exit 0.

- [ ] **Step 15: Verify both consumer-shape YAML files parse**

Run:
```bash
python3 -c "
import yaml
for p in [
    '/home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/.tokenman/tokenman.yaml',
    '/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/.tokenman/tokenman.yaml',
]:
    d = yaml.safe_load(open(p))
    assert d['schedule']['strategy'] == 'fixed'
    assert d['retention']['artifacts_days'] == 30
    assert 'dogfood' not in d, f'consumer config must not have dogfood field in {p}'
print('OK')
"
```

Expected: `OK`. Any assertion failure indicates schema drift.

- [ ] **Step 16: Verify both package/project files parse**

Run:
```bash
python3 -c "
import json, sys
j = json.load(open('/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/package.json'))
assert j['name'] == 'tiny-typescript-repo'
j2 = json.load(open('/home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/tsconfig.json'))
assert 'compilerOptions' in j2
print('OK')
"
```

Expected: `OK`.

- [ ] **Step 17: Verify Python fixture imports cleanly**

Run:
```bash
python3 -c "
import sys
sys.path.insert(0, '/home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/src')
from tiny_python_repo import greet
assert greet('world') == 'hello, world'
print('OK')
"
```

Expected: `OK`.

- [ ] **Step 18: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add tests
git -C /home/dev/projects/tokenman status --short
```

Expected: ~17 `A ` lines (one per new file).

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
test: add fixture skeleton repos

Two fixture consumers (tiny-python-repo, tiny-typescript-repo) for
later harness testing (docs/spec.md §10.4). Both are skeletons:
minimal source, one smoke test, consumer-shape .tokenman/tokenman.yaml,
empty .github/workflows/ and .claude/skills/.

No harness runs against them yet — Phase 1 wires them in when the
generator/evaluator pipeline exists.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 6: Rewrite repo-level docs

**Files:**
- Rewrite: `/home/dev/projects/tokenman/README.md`
- Rewrite: `/home/dev/projects/tokenman/CLAUDE.md`
- Create: `/home/dev/projects/tokenman/CONTRIBUTING.md`

**Rationale:** The repo-root documentation currently describes the old direction. `README.md` is the public face; `CLAUDE.md` is for interactive Claude Code sessions; `CONTRIBUTING.md` is for human contributors. Each targets a distinct audience.

- [ ] **Step 1: Rewrite `README.md`**

Replace the contents of `/home/dev/projects/tokenman/README.md` entirely with:

```markdown
# Tokenman

**Tokenman is the runtime that makes `claude -p` safe to run unattended on your repo.**

It lets any repo install a background maintenance agent that proposes
changes via PRs on a schedule, within a budget the user controls, without
requiring supervision.

## Status

Pre-release. Phase 0 scaffolding is in place; nothing runs yet. See
[`docs/spec.md`](docs/spec.md) for the full scoping draft and phased
roadmap.

## What tokenman ships

- A harness (scheduled workflows, guardrails, observability)
- A scoping and onboarding flow
- A curated catalog of recommended community skills (references, not copies)
- Documentation and conventions

## What tokenman does not ship

- Its own skills
- Hosted infrastructure
- Cloud accounts or dashboards

## Repository structure

This repo is both the library (source of the harness) and its own
first paused-by-default consumer. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the source-zone versus
runtime-zone split.

## License

See [LICENSE](LICENSE).
```

- [ ] **Step 2: Rewrite `CLAUDE.md`**

Replace the contents of `/home/dev/projects/tokenman/CLAUDE.md` entirely with:

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
- feat(harness|scoping|onboarding|catalog|dogfood): …
- fix(harness|…): …
- docs: …
- chore: …
- test: …

## What NOT to do in this repo
- Do not modify files in `harness/`, `scoping/`, `onboarding/`,
  `recommended-skills.yaml`, or `pricing.yaml` from a dogfood run. The
  paranoid `.tokenman/CLAUDE.md` forbids this.
- Do not remove `.tokenman/PAUSE` until the Phase 3 gate (spec §12).
- Do not call the Anthropic API directly — all execution goes through `claude -p`.

## Failure log
(fresh — no entries)
```

- [ ] **Step 3: Create `CONTRIBUTING.md`**

Write file `/home/dev/projects/tokenman/CONTRIBUTING.md` with content:

```markdown
# Contributing to Tokenman

## Source zone vs runtime zone

Tokenman lives in a single repository that plays two roles at once: it is
both the library (source of the harness) and its own first consumer. To
keep these from entangling, the repo is split into two zones.

### Source zone — what tokenman *is*

These paths contain the code and assets that ship to consumers when a
user runs `/tokenman init` in their repo:

- `harness/` — runtime code and workflow templates
- `scoping/` — discovery and scope-proposal logic
- `onboarding/` — guided first-run flow
- `recommended-skills.yaml` — curated catalog
- `pricing.yaml` — budget calibration data
- `docs/` — documentation
- `tests/fixtures/` — synthetic consumer repos for harness testing

Edits to source-zone files are the main library-development work.
Everything in `tests/fixtures/` stays pristine — harness tests reset it.

### Runtime zone — what tokenman *does on this repo*

These paths contain the library's own paused dogfood state:

- `.tokenman/` — config, state, ledger, artifacts
- `.github/workflows/` — actual workflows that run on this repo
- `.claude/skills/` — skills installed for this repo's dogfooding

The library's runtime zone is the canonical example of what a consumer's
runtime zone looks like — structurally identical, just with stricter
caps and a `dogfood:` field in `tokenman.yaml`.

### Why the separation matters

Updates to `harness/workflows/tokenman.yml.template` (source) do NOT
automatically update `.github/workflows/tokenman.yml` (runtime). The
runtime copy is a deliberate install step. This preserves the ability
to ship library changes without immediately dogfooding them.

## Commit conventions

- Imperative, sentence case, no trailing period, under ~72 characters
- Use scope prefixes: `feat(harness|scoping|onboarding|catalog|dogfood): …`,
  `fix(…): …`, `docs: …`, `chore: …`, `test: …`
- PRs opened by the harness itself (once dogfood unpauses at Phase 3)
  use the `[tokenman]` prefix per `docs/spec.md` §10.6, enabling clean
  filtering of human versus harness history:

  ```
  git log --grep='\[tokenman\]' --invert-grep    # human commits only
  git log --grep='\[tokenman\]'                  # dogfood commits only
  ```

## Phase 0 status

The harness is not implemented yet. Phase 0 establishes scaffolding
and contracts. See `docs/spec.md` §12 for the full phased roadmap.
```

- [ ] **Step 4: Verify the three doc files exist and look right**

Run:
```bash
wc -l /home/dev/projects/tokenman/README.md /home/dev/projects/tokenman/CLAUDE.md /home/dev/projects/tokenman/CONTRIBUTING.md
```

Expected: three line-count lines. Each should be between 20 and 80 lines (sanity bounds on length).

- [ ] **Step 5: Verify docs link correctly to existing files**

Run:
```bash
grep -o 'docs/spec.md\|CONTRIBUTING.md\|LICENSE\|.tokenman/CLAUDE.md' /home/dev/projects/tokenman/README.md /home/dev/projects/tokenman/CLAUDE.md /home/dev/projects/tokenman/CONTRIBUTING.md | sort -u
```

Expected: lists the referenced paths. Then confirm each target exists:

```bash
test -f /home/dev/projects/tokenman/docs/spec.md && test -f /home/dev/projects/tokenman/CONTRIBUTING.md && test -f /home/dev/projects/tokenman/LICENSE && test -f /home/dev/projects/tokenman/.tokenman/CLAUDE.md && echo OK
```

Expected: `OK`.

- [ ] **Step 6: Stage and commit**

Run:
```bash
git -C /home/dev/projects/tokenman add README.md CLAUDE.md CONTRIBUTING.md
git -C /home/dev/projects/tokenman status --short
```

Expected: `M README.md`, `M CLAUDE.md`, `A CONTRIBUTING.md`.

Then:
```bash
git -C /home/dev/projects/tokenman commit -m "$(cat <<'EOF'
docs: rewrite README, CLAUDE.md, add CONTRIBUTING

README.md becomes a one-screen overview pointing at docs/spec.md. Root
CLAUDE.md becomes a router for interactive sessions pointing at the
three content docs (spec.md, CONTRIBUTING.md, .tokenman/CLAUDE.md).
CONTRIBUTING.md is new and explains the source/runtime split from
docs/spec.md §3.2.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit succeeds.

---

### Task 7: Verify Phase 0 exit criteria (no commit)

**Rationale:** Confirm each of the exit criteria from the design doc §Exit criteria holds after all six commits. No code changes, no commit — this task produces a pass/fail verdict on Phase 0 completion.

- [ ] **Step 1: Criterion 1 — Legacy cleared**

Run:
```bash
test ! -e /home/dev/projects/tokenman/skills && test ! -e /home/dev/projects/tokenman/workflows && echo "criterion 1: PASS"
```

Expected: `criterion 1: PASS`.

- [ ] **Step 2: Criterion 2 — Source zone populated**

Run:
```bash
test -f /home/dev/projects/tokenman/harness/README.md && \
test -f /home/dev/projects/tokenman/harness/workflows/tokenman.yml.template && \
test -f /home/dev/projects/tokenman/scoping/README.md && \
test -f /home/dev/projects/tokenman/onboarding/README.md && \
test -f /home/dev/projects/tokenman/recommended-skills.yaml && \
test -f /home/dev/projects/tokenman/pricing.yaml && \
echo "criterion 2: PASS"
```

Expected: `criterion 2: PASS`.

- [ ] **Step 3: Criterion 3 — Runtime zone populated and paused**

Run:
```bash
test -f /home/dev/projects/tokenman/.tokenman/PAUSE && \
test -f /home/dev/projects/tokenman/.tokenman/CLAUDE.md && \
test -f /home/dev/projects/tokenman/.github/workflows/.gitkeep && \
test -f /home/dev/projects/tokenman/.claude/skills/.gitkeep && \
grep -q 'strategy: manual' /home/dev/projects/tokenman/.tokenman/tokenman.yaml && \
grep -q 'per_run_tokens: 0' /home/dev/projects/tokenman/.tokenman/tokenman.yaml && \
echo "criterion 3: PASS"
```

Expected: `criterion 3: PASS`.

- [ ] **Step 4: Criterion 4 — Documentation rewritten**

Run:
```bash
test -f /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q 'docs/spec.md' /home/dev/projects/tokenman/README.md && \
grep -q 'docs/spec.md' /home/dev/projects/tokenman/CLAUDE.md && \
grep -q 'Source zone' /home/dev/projects/tokenman/CONTRIBUTING.md && \
grep -q 'Runtime zone' /home/dev/projects/tokenman/CONTRIBUTING.md && \
echo "criterion 4: PASS"
```

Expected: `criterion 4: PASS`.

- [ ] **Step 5: Criterion 5 — Fixture skeletons in place**

Run:
```bash
test -d /home/dev/projects/tokenman/tests/fixtures/tiny-python-repo && \
test -d /home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo && \
test -f /home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/pyproject.toml && \
test -f /home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/package.json && \
test -f /home/dev/projects/tokenman/tests/fixtures/tiny-python-repo/.tokenman/tokenman.yaml && \
test -f /home/dev/projects/tokenman/tests/fixtures/tiny-typescript-repo/.tokenman/tokenman.yaml && \
echo "criterion 5: PASS"
```

Expected: `criterion 5: PASS`.

- [ ] **Step 6: Criterion 6 — Nothing runs**

Run:
```bash
test -f /home/dev/projects/tokenman/.tokenman/PAUSE && \
grep -q 'strategy: manual' /home/dev/projects/tokenman/.tokenman/tokenman.yaml && \
[ "$(find /home/dev/projects/tokenman/.github/workflows -type f ! -name '.gitkeep' | wc -l)" = "0" ] && \
echo "criterion 6: PASS"
```

Expected: `criterion 6: PASS`. The `find` subcommand confirms no workflow file besides `.gitkeep` is present.

- [ ] **Step 7: Criterion 7 — Committed in logical chunks**

Run:
```bash
git -C /home/dev/projects/tokenman log --oneline HEAD~6..HEAD
```

Expected: six lines, one per Phase 0 commit, in this order:
```
<hash> docs: rewrite README, CLAUDE.md, add CONTRIBUTING
<hash> test: add fixture skeleton repos
<hash> feat(dogfood): initialize paused runtime zone
<hash> feat(catalog): add recommended-skills.yaml and pricing.yaml stubs
<hash> feat(harness): scaffold source zone
<hash> chore: remove legacy skills and workflows
```

(Exact order may vary if tasks were reordered; what matters is that all six commits are present.)

- [ ] **Step 8: Working tree clean**

Run:
```bash
git -C /home/dev/projects/tokenman status
```

Expected: `nothing to commit, working tree clean`.

- [ ] **Step 9: Sanity — `scripts/status.sh` still works**

Run:
```bash
bash /home/dev/projects/tokenman/scripts/status.sh
```

Expected: `No ledger at .tokenman/ledger.jsonl (no tokenman runs yet).` — a benign no-op message.

- [ ] **Step 10: Final tree sanity**

Run:
```bash
find /home/dev/projects/tokenman -maxdepth 2 -not -path '*/.git*' -not -path '*/node_modules*' | sort
```

Expected: tree matches the "Tree after Phase 0" diagram in
`docs/superpowers/specs/2026-04-18-phase-0-scaffolding-design.md`.
Report any unexpected files or missing expected files.

If all ten steps pass: **Phase 0 is complete.** Proceed to Phase 1 design when ready.

---

## Self-Review Notes

Self-review completed after plan was written:

**1. Spec coverage** — all seven exit criteria in the design doc are exercised
by Task 7; each of the six commit slots in the design doc's "Order of
operations" maps to Tasks 1–6 respectively.

**2. Placeholder scan** — no TBD/TODO/fill-in phrases. The one literal
"TBD" appears inside the `pricing.yaml` file content, which is intentional
(the schema itself is deferred to Phase 2 per the design).

**3. Type consistency** — `.tokenman/tokenman.yaml` schema fields
(`schedule.strategy`, `budget.per_run_tokens`, `skills`, `retention`,
`dogfood`) are referenced identically across Tasks 4 and 5 and Task 7
verification.

**4. Ambiguity** — fixture `smoke.test.ts` uses `node:test` explicitly
(not `tsx` or another runner), and the `assert.ok(true)` body avoids
transpilation questions at Phase 0.
