# Self-Evolving Scaffold — Design Spec

**Date:** 2026-03-20
**Status:** Approved
**Approach:** Incremental Transform (from portfolio scaffold to self-evolving harness)

---

## Overview

Transform Agentfolio from a personal portfolio scaffold into a general-purpose, self-evolving harness. The scaffold's first project is itself — it uses its own workflows to improve its own workflows, its own CLAUDE.md to refine its own CLAUDE.md. A repo profile page replaces the portfolio as the public face.

### Core Principles

- **The repo IS the system.** No servers, no databases. GitHub is the infrastructure.
- **Self-referential, not duplicative.** `apps/scaffold/` contains rules about how to evolve the harness, not a copy of it.
- **Reactive + proactive.** The scaffold fixes its own failures AND adopts external best practices.
- **Tiered autonomy.** Safe changes auto-commit; structural changes need human review.

---

## 1. Architecture

### What stays (root level)

```
.github/workflows/       # The engine — all workflows live here
state/                   # agent_log.md, project_state.md
skills/                  # Harness skills (generalized)
CLAUDE.md                # Root constitution
```

### What changes

```
apps/scaffold/           # Self-referential project (rules for evolving the harness)
  CLAUDE.md              # "How to improve yourself" rules
  FEATURE_STATUS.md      # Scaffold improvement tracker

apps/profile/            # Repo's public profile page
  CLAUDE.md              # Content/display rules for the profile
  FEATURE_STATUS.md      # Profile feature tracker

state/research_log.md    # New — external research findings (append-only)

src/                     # Minimal static site for repo profile (replaces portfolio)
content/                 # Repo-focused content (not personal portfolio)
src/content.config.ts    # Rewritten — new collection schemas for repo profile data
```

### What gets removed

- `content/profile.json` — personal portfolio data
- `content/projects/example.md` — portfolio project cards
- `content/llms.txt` — personal AI-readable profile
- `apps/portfolio/` — entire folder (including `CLAUDE.md`, `FEATURE_STATUS.md`, `growth_goals.md`)
- `plugin/` — entire folder (premature)
- Portfolio-specific page templates in `src/pages/` (`index.astro`, `projects/[slug].astro`, `api/profile.json.ts`)
- `docs/onboarding.md` — portfolio-centric setup guide (replace with scaffold-focused onboarding)

### What gets updated

- `README.md` — rewrite to describe the self-evolving scaffold, not a portfolio tool. Remove plugin references, update workflow table, update quick-start guide.
- `deploy.yml` — remove portfolio-specific copy steps (`content/llms.txt` to `dist/`, `content/profile.json` to `dist/api/`). Remove `APP_NAME: portfolio`.

### Workflow mapping

All workflows that currently hardcode `APP_NAME: portfolio` must be updated. Workflows become multi-project aware: they read `APP_NAME` from the triggering event context (issue label, PR label, or workflow input) and fall back to `scaffold` as the default.

| Current | Becomes | Changes needed |
|---|---|---|
| `deploy.yml` | `deploy.yml` | Remove portfolio copy steps, remove hardcoded `APP_NAME` |
| `onboard.yml` | `discover.yml` | Rewrite — scans `apps/*/`, infers stack, generates rules |
| `triage.yml` | `triage.yml` | Update `APP_NAME` to dynamic resolution |
| `coder.yml` | `coder.yml` | Update `APP_NAME` to dynamic resolution |
| `reviewer.yml` | `reviewer.yml` | Update `APP_NAME` to dynamic resolution |
| `maintenance.yml` | `evolve.yml` | Rewrite — self-evolution loop with research phase |
| `growth.yml` | `analyze.yml` | Rewrite — weekly improvement analysis |
| `claude-task.yml` | `claude-task.yml` | Update `APP_NAME` to accept input, default `scaffold` |

### APP_NAME resolution strategy

Workflows determine which project they're operating on:
1. **Issue/PR-triggered** (`triage.yml`, `coder.yml`, `reviewer.yml`): read from issue/PR label (e.g., `project:profile`, `project:scaffold`). Default to `scaffold` if no label.
2. **Cron-triggered** (`evolve.yml`, `analyze.yml`): iterate over all `apps/*/` folders, or target `scaffold` for self-evolution tasks.
3. **Manual dispatch** (`claude-task.yml`, `discover.yml`): accept `APP_NAME` as workflow input.

### Self-referential loop (no duplication)

The harness (root level) is the single source of truth for workflows, state, and the constitution. `apps/scaffold/` does not duplicate the harness — it is a lens on it, containing rules about how to evolve the harness. The actual workflows, skills, and state files remain in their canonical locations.

```
Agent runs evolve.yml
  -> reads root CLAUDE.md (harness rules)
  -> reads apps/scaffold/CLAUDE.md (self-improvement rules)
  -> analyzes its OWN workflows, skills, failure log
  -> proposes improvements via PR (governed by autonomy tiers)
  -> reviewer.yml reviews the PR
  -> human approves structural changes, safe ones auto-merge
```

---

## 2. Project Discovery (`discover.yml`)

When a new folder appears in `apps/`, the agent autonomously figures out what it is and sets it up.

### Trigger

Manual dispatch with `APP_NAME` input, or chained from `evolve.yml` via `gh workflow run discover.yml -f app_name=<name>` when it detects a new `apps/*/` folder without a `CLAUDE.md`.

### Discovery flow

1. **Scan** the folder — file extensions, package.json, Dockerfile, config files, directory structure
2. **Infer** the stack — language, framework, build tool, test runner
3. **Generate** `apps/<name>/CLAUDE.md` — autonomy rules tailored to what was found
4. **Generate** `apps/<name>/FEATURE_STATUS.md` — initial feature inventory
5. **Open** a `needs-review` PR with the generated files

### Generated CLAUDE.md contains

- Project description (inferred)
- Stack details
- Build/test/deploy commands (discovered from config files)
- Content rules (if applicable)
- Autonomy overrides (conservative defaults — everything starts as `needs-review`)

### What discovery does NOT do

- Modify the project's own code
- Create per-project workflows (shared workflows handle all projects)
- Assume any specific framework

Discovery heuristics live in skill files and improve over time via `evolve.yml`.

---

## 3. Self-Evolution Loop (`evolve.yml`)

The core differentiator — the scaffold improving itself.

### Trigger

Daily cron at 3:00 UTC (same schedule as current maintenance.yml).

### The loop

1. **Read state** — `state/agent_log.md`, failure log in `CLAUDE.md`, recent git history
2. **Research** — fetch external knowledge (incremental rollout):
   - **Phase 1 (initial)**: GitHub API — check reference repos from README.md for new commits/releases. Check GitHub Actions changelog via API.
   - **Phase 2 (later)**: RSS feeds from Anthropic engineering blog and GitHub blog. Parse with standard tools (curl + jq for JSON feeds, curl + grep for Atom/RSS).
   - **Phase 3 (aspirational)**: Broader web research. Mechanism TBD based on what Phase 1-2 teach us.
   - Summarize findings relevant to the harness
3. **Analyze** — informed by both internal failures AND external trends:
   - Repeated failures -> propose a new rule in CLAUDE.md failure log
   - Workflow inefficiencies -> propose workflow changes
   - Missing skills -> draft a new skill file
   - Undiscovered projects -> trigger discovery via `gh workflow run discover.yml`
4. **Act** — based on autonomy tiers:
   - **Auto-commit**: failure log entries, state updates, skill wording/clarity, FEATURE_STATUS updates
   - **PR (auto-merge)**: minor skill improvements (behavioral, low-risk)
   - **PR (needs-review)**: workflow YAML changes, CLAUDE.md rule changes, new skills, research-inspired changes
5. **Log** — append actions to `state/agent_log.md`, research findings to `state/research_log.md`

### Safety rails

- The agent cannot promote its own autonomy (e.g., move `needs-review` to `auto-commit`)
- Workflow YAML changes always require human review
- Max one structural PR per run — prevents cascading self-modifications. "Structural" = any change to workflow YAML, CLAUDE.md autonomy rules, or new skill files.
- Each self-improvement PR must state what failure or inefficiency triggered it
- All research-inspired changes require human review
- If a merged self-improvement causes a regression in a subsequent run, the failure is logged and a revert PR is opened (needs-review)

### Example cycle

```
Day 1:  coder.yml fails because it doesn't handle monorepo test paths
Day 1:  Failure logged in CLAUDE.md failure log (auto-commit)
Day 2:  evolve.yml reads failure log, proposes coder.yml patch (needs-review PR)
Day 2:  Human approves -> merged
Day 3:  evolve.yml verifies the fix worked, updates FEATURE_STATUS (auto-commit)
```

---

## 4. Improvement Analysis (`analyze.yml`)

Weekly strategic analysis — complements the daily tactical `evolve.yml`.

### Trigger

Weekly cron, Monday 6:00 UTC (same schedule as current growth.yml).

### What it does

1. **Review the week** — read `state/agent_log.md` and `state/research_log.md` entries from the past 7 days
2. **Identify patterns** — recurring failures, workflow bottlenecks, skills used vs. available, PRs that needed multiple review rounds
3. **Assess skill gaps** — are there categories of work the agent struggles with that a new skill file could address?
4. **Produce a weekly summary** — append to `state/agent_log.md` with findings and recommended priorities
5. **Optionally act** — if clear improvements are identified, open a needs-review PR (same autonomy rules as evolve.yml)

### How it differs from evolve.yml

| | `evolve.yml` | `analyze.yml` |
|---|---|---|
| Frequency | Daily | Weekly |
| Focus | Tactical — fix specific failures, apply specific research | Strategic — identify trends, prioritize improvements |
| Research | Fetches external sources | Reads internal state only |
| Output | State updates + PRs | Summary + optional PRs |

---

## 5. Research Log (`state/research_log.md`)

New state file for tracking external knowledge. Created as part of initial implementation.

### Format

Append-only, like `agent_log.md`. Pipe-delimited.

```
ISO_TIMESTAMP | source | finding_summary | action_taken
```

### Each entry records

- Date
- Sources checked
- Key findings
- Action taken (or "no action — noted for future reference")

### Autonomy

- Writing to `research_log.md`: auto-commit (always)
- Acting on research findings: needs-review PR (always)

---

## 6. Repo Profile Page

The scaffold's public face — a live dashboard of its own activity.

### What it displays

- **Hero**: Repo name, tagline, what the scaffold does
- **Live stats**: Total agent commits, self-improvements made, failures caught and fixed (from `state/agent_log.md` at build time)
- **Evolution timeline**: Recent agent activity — what it changed and why
- **Capabilities**: Current skills inventory (read from `skills/` directory)
- **Architecture diagram**: How the harness works
- **Getting started**: How to fork and use the scaffold

### Content source (no new CMS)

- `state/agent_log.md` -> activity feed, stats
- `state/research_log.md` -> "what the scaffold learned recently"
- `skills/*.md` -> capabilities list
- `CLAUDE.md` failure log -> "mistakes it won't make again"

### How it stays fresh

`evolve.yml` updates state files -> triggers `deploy.yml` -> profile page rebuilds with latest data. No manual content management needed.

### Stack

Astro (already present). Single page. Minimal styling. `src/content.config.ts` rewritten with new collection schemas appropriate for repo profile data (replacing portfolio `projects` and `posts` collections).

### New page templates

- `src/pages/index.astro` — single repo profile page (replaces portfolio index)
- Remove `src/pages/projects/[slug].astro` and `src/pages/api/profile.json.ts`

### `apps/profile/CLAUDE.md` rules

- Auto-commit: stat regeneration, activity feed updates
- Needs-review: layout changes, new sections, copy changes to hero/tagline

---

## 7. State Management

### State files

| File | Purpose | Access |
|---|---|---|
| `state/project_state.md` | Session state, read at start / written at end of every run | Read/write |
| `state/agent_log.md` | Append-only action history | Append only |
| `state/research_log.md` | External research findings from evolve.yml | Append only |

### Per-project state

Lives in `apps/*/FEATURE_STATUS.md`, not in `state/`. Keeps project-specific tracking close to project rules. `state/` stays harness-level.

### State read order (every workflow)

1. `state/project_state.md` — what happened last
2. `CLAUDE.md` — harness rules
3. `apps/<relevant>/CLAUDE.md` — project rules
4. `apps/<relevant>/FEATURE_STATUS.md` — project status

---

## 8. Autonomy Rules

### AUTO — commit directly

- State file updates (`project_state.md`, `agent_log.md`, `research_log.md`)
- Failure log entries in `CLAUDE.md`
- Skill file wording/clarity improvements (no behavioral changes)
- FEATURE_STATUS updates
- Profile page stat regeneration

### PR — auto-merge

- Lint and type fixes
- Minor skill improvements (behavioral, but low-risk)

### PR — needs-review

- Workflow YAML changes (always)
- CLAUDE.md autonomy rule changes
- New skill files
- Any change inspired by external research
- Profile page layout/copy changes
- Discovery-generated CLAUDE.md for new projects

### NEVER auto-execute

- Deleting files or content
- Promoting its own autonomy tier
- Modifying auth/secrets configuration
- More than one structural PR per evolve.yml run (structural = workflow YAML, CLAUDE.md autonomy rules, new skill files)

---

## 9. Migration Scope

Files and docs that need updating as part of the transformation, beyond the architecture changes above:

| File | Action |
|---|---|
| `README.md` | Rewrite — describe self-evolving scaffold, remove portfolio/plugin references |
| `docs/onboarding.md` | Rewrite — scaffold-focused setup guide |
| `src/content.config.ts` | Rewrite — new collection schemas for repo profile |
| `tailwind.config.mjs` | Review — strip portfolio-specific typography/badge config if unused |
| `skills/content.md` | Rewrite — generalize from portfolio content to project content management |
| `skills/frontend.md` | Update — generalize from portfolio Astro pages to scaffold profile page |
| `skills/seo.md` | Update — refocus from personal SEO to repo discoverability |
| `skills/feedback-intake.md` | Keep — already generic |
| `skills/github-workflows.md` | Update — reflect new workflow names and APP_NAME strategy |
| `skills/harness.md` | Update — reflect self-evolution architecture |
| `public/robots.txt` | Keep — already generic |
| `.gitignore` | Keep — already generic |
