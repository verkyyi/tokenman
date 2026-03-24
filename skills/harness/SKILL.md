---
name: harness
version: 1.0.0
description: >
  Self-evolution loop architecture for AI agent harnesses. Covers
  daemon workflows, state management, event routing, approval gates,
  and the overall autonomous agent architecture pattern.
author: tokenman
tags: [architecture, self-evolution, automation, ci-cd, github-actions]
requires: []
preamble-tier: 2
---

# Self-Evolving Agent Harness

A pattern for building autonomous AI agent systems that improve themselves
over time. The harness coordinates multiple specialized workflows through
a shared state layer and event bus.

## Architecture

- **Runtime:** CI/CD platform (e.g., GitHub Actions)
- **State:** Version-controlled files (markdown committed to repo)
- **Event bus:** Issue tracker with labels for routing
- **Deployment:** Static site or equivalent output

## Core Workflows

A complete harness uses specialized workflows for each concern:

1. **Deploy** -- triggered on push to main; builds and publishes output
2. **Discover** -- manual dispatch; scans for new projects, generates config
3. **Triage** -- triggered on issue open/label; classifies and routes work
4. **Coder** -- triggered on agent-ready issues; implements features
5. **Reviewer** -- triggered on PR open/sync; reviews bot-authored PRs
6. **Evolve** -- scheduled (cron); self-improvement loop
7. **Analyze** -- scheduled (weekly); health metrics and trends
8. **Watcher** -- scheduled; monitors pipeline health, triggers corrections

## Self-Evolution Loop

The evolve workflow runs on a schedule:

1. **Research** -- fetch external changelogs, reference repos, ecosystem news;
   append findings to a research log
2. **Analyze** -- read activity logs, state files, failure log, workflow
   definitions, and skill files for patterns and gaps
3. **Act** -- auto-commit safe changes (state updates, wording fixes);
   propose structural changes via PR for human review
4. **Chain** -- if new projects are detected, trigger discovery workflow

**Constraint:** Maximum one structural PR per evolution run.

## Event Routing via Labels

Issues serve as the event bus. Labels control routing:

| Label | Effect |
|-------|--------|
| `agent-ready` | Triggers coder workflow |
| `feedback` | Triggers triage workflow |
| `needs-review` | Requires human approval before merge |
| `auto-merge` | Approved for automated merge |
| `needs-human` | Blocked until human action |

## Autonomy Tiers

Changes are classified by risk level, each with different approval gates:

**AUTO** -- commit directly, no PR needed:
- State file updates (logs, status trackers)
- Failure log entries
- Skill wording/clarity improvements (no behavioral changes)

**Auto-merge PR** -- open PR, auto-merge after review:
- Lint and type fixes
- Minor behavioral improvements (low risk)

**Needs-review PR** -- open PR, require human approval:
- Workflow/CI file changes
- Autonomy rule changes
- New skill files
- Changes inspired by external research

**NEVER auto-execute:**
- Deleting files or content
- Promoting the agent's own autonomy tier
- Modifying auth/secrets configuration
- More than one structural PR per evolution run

## State File Conventions

### Project State (read/write every run)
Written at end of every workflow run. Read at start.
Sections: last updated, last session summary, open items, metrics, critical notes.

### Activity Log (append-only)
Format: `TIMESTAMP | workflow_name | action description | outcome`
Never edit existing lines.

### Research Log (append-only)
Format: `ISO_TIMESTAMP | source | finding_summary | action_taken`
Prevents re-fetching sources already processed.

## Workflow Patterns

### Pattern A: CLI-based agent
The workflow invokes a CLI agent with full tool access:
```yaml
- run: |
    agent-cli -p "$(cat /tmp/prompt.txt)" \
      --allowed-tools "bash,read,write,edit" \
      --max-turns N
```
Agent can read APIs, write files, run commands. Cannot commit --
the workflow handles git operations.

### Pattern B: Action-based agent
Lighter weight, best for classification and API operations:
```yaml
- uses: agent-action@v1
  with:
    prompt: |
      [inline prompt]
```

## Failure Handling

If a step fails:
1. Write failure to activity log
2. Record failure in a persistent failure log (prevents repeat mistakes)
3. Open an issue labeled `agent-error`
4. Do NOT retry more than once automatically
5. Exit cleanly -- next run picks up from state

If a merged self-improvement causes a regression:
1. Log the regression in the failure log
2. Open a revert PR requiring human review

## Gotchas

- Never modify CI/workflow files from within a workflow run
- Activity logs are append-only -- never rewrite existing lines
- The standard CI token cannot trigger other workflow runs
  (use workflow dispatch for chaining)
- Scheduled CI has timing variance -- don't rely on exact execution times
- State commits should use an API-based approach to avoid push conflicts
