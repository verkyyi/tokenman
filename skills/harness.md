---
name: harness
description: >
  Use when working on the Agentfolio harness itself: daemon workflows,
  state file management, event routing, approval gates, GitHub Actions
  YAML, or the overall harness architecture. Also use when the agent
  needs to understand how the system works before making changes.
---

# Agentfolio Harness

## Architecture
- Runtime: GitHub Actions (7 workflows)
- State: state/ folder — markdown files committed to repo
- Event bus: GitHub Issues with labels
- CMS: content/ folder — Astro content collections
- Deployment: GitHub Pages (Astro static build)

## State File Conventions

### state/project_state.md
Written at the end of EVERY workflow run. Read at the start.
Format must be consistent — Claude parses this.

Required sections:
- Last updated (ISO timestamp + workflow name)
- Last Session (action, done list, in-progress, next agent hint)
- Open Items (checkboxes with PR/issue numbers)
- Metrics Snapshot (updated by growth.yml weekly)

### state/agent_log.md
Append-only. Never edit existing lines. Format:
`TIMESTAMP | workflow_name | action description | outcome`

The Base.astro layout reads the last line of this file at BUILD TIME
to power the "last updated by agent" badge. Malformed lines will
break the badge. Always use the pipe-delimited format exactly.

### .commit-message
Written by Claude, read by the workflow's git commit step.
Keep it under 72 characters for the first line.
Use conventional commit format: type(scope): description

## Workflow Patterns

### Pattern A (Claude Code CLI)
Used for: onboard, coder, maintenance, growth, claude-task
```
claude -p "$(cat /tmp/prompt.txt)" \
  --allowedTools "bash,read,write,edit" \
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

## Approval Gates
See CLAUDE.md for the full list. Quick reference:
- AUTO: state files, broken links, dep patches, content sync
- auto-merge PR: lint fixes, content updates, SEO tweaks
- needs-review PR: visual changes, new sections, CLAUDE.md edits
- NEVER auto: delete content, modify workflows, publish externally

## Commit Protocol
1. Claude writes .commit-message file
2. Workflow runs: git add . && git commit -m "$(cat .commit-message)"
3. Claude never runs git commit directly

## Gotchas
- Never modify .github/workflows/ files from within a workflow run
- state/agent_log.md is append-only — never rewrite existing lines
- The agent badge reads the LAST valid pipe-delimited line in agent_log.md
- GITHUB_TOKEN has write access but cannot trigger other workflow runs
  (use repository_dispatch or workflow_dispatch for chaining)
- GitHub cron has ~15 min variance — don't rely on exact timing
- Lighthouse CI requires the Pages site to already be deployed
