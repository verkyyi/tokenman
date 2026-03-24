---
name: harness
version: 1.0.0
description: >
  Use when working on the Tokenman harness itself: daemon workflows,
  state file management, event routing, approval gates, GitHub Actions
  YAML, or the overall harness architecture. Also use when the agent
  needs to understand how the system works before making changes.
author: tokenman
tags: [architecture, self-evolution, automation, ci-cd, github-actions]
---

# Tokenman Harness

## Architecture
- Runtime: GitHub Actions (8 workflows)
- State: state/ folder — markdown files committed to repo
- Event bus: GitHub Issues with labels
- CMS: content/ folder — Astro content collections
- Deployment: GitHub Pages (Astro static build)

## When NOT to Use
- When working only on frontend/Astro files (src/) — use the `frontend` skill instead
- When writing or updating content collection entries in content/ — use the `content` skill
- When debugging SEO, meta tags, or structured data — use the `seo` skill
- When the task is a pure GitHub API operation with no harness context — use `github-workflows` skill
- When making simple state file appends that don't require understanding the architecture

## Rationalizations to Reject
- "I'll just modify the workflow YAML directly in this run" — workflow YAML changes always need a PR
- "State file format doesn't matter much" — malformed agent_log.md breaks the activity badge on the site
- "I can skip reading project_state.md this time" — session protocol requires reading state on start, every time
- "One more structural change won't hurt" — max one structural PR per evolve.yml run, no exceptions

## Anti-Patterns

**Bad — editing workflow YAML inside a workflow run:**
During a coder.yml run, the agent edits `.github/workflows/coder.yml` directly and commits.
This bypasses the PR review gate and can cause self-triggering loops.

**Good — opening a PR for workflow changes:**
The agent creates a branch, commits the workflow YAML change, and opens a `needs-review` PR.
The reviewer workflow validates the change before merge.

**Bad — rewriting agent_log.md:**
The agent rewrites existing lines in `state/agent_log.md` to "clean up" formatting.
This destroys the append-only audit trail and may break downstream consumers.

**Good — append-only state writes:**
The agent appends a new pipe-delimited line to `state/agent_log.md` without touching existing entries.

## Workflows
1. **deploy.yml** — triggered on push to main; builds and publishes Pages site
2. **discover.yml** — manual dispatch; scans apps/ for new projects, generates CLAUDE.md
3. **triage.yml** — triggered on issue open/label; classifies feedback and routes
4. **coder.yml** — triggered on agent-ready issues; implements features via Claude Code
5. **reviewer.yml** — triggered on PR open/sync; reviews bot-authored PRs
6. **evolve.yml** — daily cron; self-improvement loop (research → analyze → propose)
7. **analyze.yml** — weekly cron; traffic, stars, and repo health metrics
8. **claude-task.yml** — manual dispatch; runs arbitrary Claude Code tasks

## Self-Evolution Loop
evolve.yml runs daily:
1. **Research** — fetch external changelogs, reference repos; append to state/research_log.md
2. **Analyze** — read agent_log.md, project_state.md, failure log, workflow YAML, skills/
3. **Act** — AUTO-COMMIT safe changes (state, failure log entries, skill wording);
   write .proposed-change.md for structural changes (workflow YAML, new skills, rule changes)
4. **Chain** — if new apps/ folder found without CLAUDE.md, write .trigger-discovery.txt;
   workflow dispatches discover.yml with `gh workflow run discover.yml -f app_name="$APP"`

Maximum one structural PR per evolve.yml run.

## APP_NAME Resolution
Workflows determine which project they operate on:
1. **Issue/PR-triggered** (triage, coder, reviewer): read from issue/PR label
   (e.g., `project:profile`, `project:scaffold`). Default: scaffold.
2. **Cron-triggered** (evolve, analyze): iterate all apps/*/ folders,
   or target scaffold for self-evolution tasks.
3. **Manual dispatch** (claude-task, discover): accept APP_NAME as workflow input.

Project-specific rules live in apps/${APP_NAME}/CLAUDE.md.

## State File Conventions

### state/project_state.md
Written at the end of EVERY workflow run. Read at the start.
Format must be consistent — Claude parses this.

Required sections:
- Last updated (ISO timestamp + workflow name)
- Last Session (action, done list, in-progress, next agent hint)
- Open Items (checkboxes with PR/issue numbers)
- Metrics Snapshot (updated by analyze.yml weekly)

### state/agent_log.md
Append-only. Never edit existing lines. Format:
`TIMESTAMP | workflow_name | action description | outcome`

The repo profile page reads the last line of this file at BUILD TIME
to power the "last updated by agent" badge. Malformed lines will
break the badge. Always use the pipe-delimited format exactly.

### state/research_log.md
Append-only. Written by evolve.yml during the Research phase.
Format: `ISO_TIMESTAMP | source | finding_summary | action_taken`

Never rewrite existing entries. Used by the evolution agent to avoid
re-fetching sources it has already processed.

### .commit-message
Written by Claude, read by the workflow's git commit step.
Keep it under 72 characters for the first line.
Use conventional commit format: type(scope): description

## Workflow Patterns

### Pattern A (Claude Code CLI)
Used for: discover, coder, evolve, analyze, claude-task
```
claude -p "$(cat /tmp/prompt.txt)" \
  --allowedTools "bash,read,write,edit,glob,grep" \
  --max-turns [N]
```
Claude has full bash access. Can read GitHub API responses,
write files, run npm commands.
CANNOT commit — workflow YAML does git operations.

### Pattern C (Official Action)
Used for: triage, reviewer
```yaml
uses: anthropics/claude-code-action@v1
with:
  prompt: |
    [inline prompt]
```
Lighter weight. Best for classification and GitHub API operations.
Uses gh CLI for Issue/PR operations.

## Reviewer Workflow — Pre-Merge Gate
Before the reviewer agent issues any merge recommendation, it MUST run the
Pre-Merge Gate defined in `skills/adversarial-review.md`. The gate blocks merge
if CI is failing, if a high-risk file (`.github/workflows/`, `CLAUDE.md`
autonomy rules) was changed without an explicit one-sentence risk assessment,
or if any open blocking issue is linked to the PR.

After the gate, append a findings table (Trigger | Why | Status | Findings) for
non-trivial reviews. All review skill files follow this pattern — see
`skills/adversarial-review.md` § Findings Table.

## Autonomy Gates
See CLAUDE.md for the full list. Quick reference:
- AUTO: state files, failure log entries, skill wording improvements, FEATURE_STATUS
- auto-merge PR: lint fixes, minor behavioral skill improvements
- needs-review PR: workflow YAML changes, CLAUDE.md rule changes, new skill files,
  any change from external research, profile page layout changes,
  discovery-generated CLAUDE.md for new projects
- NEVER auto: delete files/content, promote own autonomy tier,
  modify auth/secrets, more than one structural PR per evolve.yml run

## Commit Protocol
1. Claude writes .commit-message file
2. Workflow runs: git add . && git commit -m "$(cat .commit-message)"
3. Claude never runs git commit directly

## Gotchas
- Never modify .github/workflows/ files from within a workflow run
- state/agent_log.md is append-only — never rewrite existing lines
- state/research_log.md is append-only — never rewrite existing lines
- The agent badge reads the LAST valid pipe-delimited line in agent_log.md
- GITHUB_TOKEN has write access but cannot trigger other workflow runs
  (use gh workflow run for chaining — evolve.yml → discover.yml)
- GitHub cron has ~15 min variance — don't rely on exact timing
- Lighthouse CI requires the Pages site to already be deployed
