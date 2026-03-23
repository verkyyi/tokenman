# Unified Label Registry

**Date:** 2026-03-23
**Status:** Approved

## Problem

Labels are created in one place (evolve.yml) but referenced across 8+ workflows. Many labels used in workflow prompts were never formally created — they either came from GitHub defaults or manual creation. There is no single place to see what labels exist, what they mean, or who uses them. Adding `project:*` scope labels added complexity for a single-project repo.

## Design

### 1. Registry file: `.github/labels.yml`

A flat YAML list defining every label the project uses. This is the single source of truth.

```yaml
# .github/labels.yml — single source of truth for all GitHub labels
# Synced by .github/workflows/sync-labels.yml

- name: agent-ready
  color: "0e8a16"
  description: Ready for coder agent
```

Each entry has `name`, `color`, and `description`. Comments group labels by category for readability.

### 2. Workflow: `.github/workflows/sync-labels.yml`

**Triggers:**
- `push` to `main` when `.github/labels.yml` changes
- `schedule` — weekly (catches manual drift)
- `workflow_dispatch` — manual trigger with optional `prune` input

**Logic:**
1. Parse `.github/labels.yml` with `yq` (installed via `snap install yq` or binary download — not pre-installed on ubuntu-latest)
2. For each entry: `gh label create "$name" --color "$color" --description "$desc" --force`
3. **Prune step** (opt-in, defaults to `false`): list all GitHub labels, diff against registry, delete labels not in the file
4. No Claude/AI — pure shell, fast, deterministic, idempotent

**Prune safety:** The `prune` input defaults to `false`. Must be explicitly set to `true` via workflow dispatch. Push and schedule triggers never prune.

### 3. Migration

**Remove from evolve.yml:**
- Delete the "Ensure labels exist" step (lines 448-460) that currently runs `gh label create` for 8 labels

**Remove `project:*` references from workflow prompts:**
- evolve.yml line ~126 (PIPELINE WATCH posture): remove `project:$(echo $GITHUB_REPOSITORY | cut -d/ -f2)` from `--label` in prompt
- evolve.yml line ~239 (Issue Creation section): remove `project:$(echo $GITHUB_REPOSITORY | cut -d/ -f2)` from prompt
- watcher.yml lines ~176-177, ~204: remove `project:<reponame>` from issue creation instructions in prompt
- growth.yml line ~146: remove `project:<reponame>` from label instructions in prompt
- triage.yml lines ~59, ~64: remove project label instructions from prompt
- feedback-learner.yml line ~119: remove project label instruction from prompt
- feedback-learner.yml line ~275: remove `project:$(gh repo view --json name -q .name)` from `--label` flag

**Update CLAUDE.md:**
- Remove `project:*` label pattern from APP_NAME Resolution section (line ~24)

**No changes needed to:**
- Workflows that only `--add-label` or `--label` without `project:*` (coder, reviewer, analyze, claude-task, discover) — these stay as-is

### 4. Label inventory

**Pipeline status:**
| Name | Color | Description |
|------|-------|-------------|
| `agent-ready` | `0e8a16` | Ready for coder agent |
| `needs-human` | `d93f0b` | Requires human action (external platform, secrets, permissions) |
| `needs-review` | `fbca04` | Needs human review |
| `likely-agent-fixable` | `0e8a16` | Watcher determined this pipeline issue can be fixed by the coder agent |
| `human-wip` | `d93f0b` | Human is actively working on this issue |

**Pipeline origin:**
| Name | Color | Description |
|------|-------|-------------|
| `evolve-finding` | `7057ff` | Issue created by evolve.yml |
| `pipeline-fix` | `d73a4a` | Pipeline failure to fix |
| `adopter-insight` | `1d76db` | Pattern found from adopter usage |
| `intent-driven` | `5319e7` | Issue driven by human intent analysis |

**Issue type:**
| Name | Color | Description |
|------|-------|-------------|
| `bug` | `d73a4a` | Something isn't working |
| `feature` | `a2eeef` | New feature request |
| `question` | `d876e3` | Further information is requested |
| `ux-request` | `e4e669` | UX improvement suggestion |
| `growth-action` | `0075ca` | Growth and distribution action |
| `positive` | `0e8a16` | Positive feedback |
| `spam` | `e4e669` | Spam or irrelevant |

**Workflow meta:**
| Name | Color | Description |
|------|-------|-------------|
| `auto-merge` | `0e8a16` | PR approved for automatic merge |
| `agent-error` | `d73a4a` | Issue created by agent failure handling |
| `feedback` | `1d76db` | User feedback (also hardcoded in `.github/ISSUE_TEMPLATE/feedback.yml`) |

**Total: 19 labels.**

GitHub default labels not in this list (`documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `wontfix`, `triaged`) will be pruned when prune is enabled. Until then they remain unused.

## Non-goals

- Dynamic label generation (e.g., `project:*` per-repo labels) — removed, single project
- Third-party sync actions (e.g., `EndBug/label-sync`) — shell script is simpler and has no dependencies
- Label permissions/CODEOWNERS — not needed at current scale
