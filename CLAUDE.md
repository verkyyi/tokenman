# Tokenman — Scaffold Constitution
# Harness rules only. No project-specific knowledge lives here.
# Project context: read apps/${APP_NAME}/CLAUDE.md

## What this scaffold is
A self-evolving web project harness powered by Claude Code.
The repo IS the system. State lives in state/. Events live in
GitHub Issues. Every agent action is a commit. The scaffold's
first project is itself — it improves its own workflows, skills,
and rules over time.

## Harness Architecture
Runtime:     GitHub Actions (8 workflows)
State:       state/ folder (committed markdown files)
Event bus:   GitHub Issues with labels
CMS:         content/ folder (Astro content collections)
Memory:      state/project_state.md (read/write every run)
Research:    state/research_log.md (append-only, external findings)
Deployment:  GitHub Pages (Astro static build)

## APP_NAME Resolution
Workflows determine which project they operate on:
1. Issue/PR-triggered (triage, coder, reviewer): read from issue/PR metadata. Default: scaffold.
2. Cron-triggered (evolve, analyze): iterate all apps/*/ folders,
   or target scaffold for self-evolution tasks.
3. Manual dispatch (claude-task, discover): accept APP_NAME as input.

## Session Protocol

ON START (every workflow run AND every CLI session):
1. Read state/project_state.md — what happened last
2. Read apps/${APP_NAME}/CLAUDE.md — project-specific rules
3. Read apps/${APP_NAME}/FEATURE_STATUS.md — what's done and pending
4. Check current event: issue body, PR diff, workflow input

ON STOP (every workflow run AND every CLI session):
1. Write session summary to state/project_state.md
2. Update state/agent_log.md (append one line)
3. Update apps/${APP_NAME}/FEATURE_STATUS.md if anything changed
4. Commit all state/ changes with message: "state: [summary]"

CLI SESSION CLOSE (enforced by SessionEnd hook):
When the user ends a CLI session (exits, /clear, closes terminal):
- The SessionEnd hook auto-commits any uncommitted state/ changes
- To ensure a useful summary exists, Claude MUST update state files
  BEFORE the session ends — do not wait to be asked
- When you detect the conversation is wrapping up (user says "done",
  "thanks", "that's all", asks to commit, or context is being compressed),
  proactively update state/project_state.md and state/agent_log.md

## Autonomy Rules (scaffold defaults — app CLAUDE.md may override)

AUTO — commit directly, no PR needed:
- State file updates (project_state.md, agent_log.md, research_log.md)
- Failure log entries in CLAUDE.md
- Skill file wording/clarity improvements (no behavioral changes)
- FEATURE_STATUS updates

PR — open a pull request, label: auto-merge:
- Lint and type fixes
- Minor skill improvements (behavioral, low-risk)

PR — open a pull request, label: needs-review:
- Workflow YAML changes (always)
- CLAUDE.md autonomy rule changes
- New skill files
- Any change inspired by external research
- Profile page layout/copy changes
- Discovery-generated CLAUDE.md for new projects

NEVER auto-execute:
- Deleting files or content
- Promoting its own autonomy tier
- Modifying auth/secrets configuration
- More than one structural PR per evolve.yml run
  (structural = workflow YAML, CLAUDE.md autonomy rules, new skill files)

## GitHub Actions Context
- GITHUB_TOKEN: always available, use for API calls
- CLAUDE_CODE_OAUTH_TOKEN: in secrets, use for claude -p and claude-code-action
- APP_NAME: resolved dynamically per workflow (see APP_NAME Resolution)
- Workflows run on ubuntu-latest runners
- Full outbound internet access in runners
- --bare flag (claude-code v2.1.81): NOT adopted. All 10 workflows use
  CLAUDE_CODE_OAUTH_TOKEN (OAuth), but --bare disables OAuth and requires
  ANTHROPIC_API_KEY. The startup savings are marginal vs total agent runtime.
  Revisit only if ANTHROPIC_API_KEY is provisioned for other reasons. (#63)

## Tool Usage in Workflows
Preferred order for file operations:
1. GitHub API (for GitHub data — richest, most structured)
2. curl (for external HTTP — RSS, blogs, changelogs)
3. Standard unix tools (grep, jq, sed — for parsing)

## Commit Message Convention
feat(content): add new content for [topic]
feat(harness): add [workflow/skill/capability]
fix(workflow): fix [issue] in [workflow]
state: session summary — [what was done]
chore(deps): patch [package] security vulnerability
research: [source] — [finding summary]

## Failure Handling
If a step fails:
1. Write failure to state/agent_log.md
2. Add failure to CLAUDE.md failure log (below)
3. Open a GitHub Issue labeled: agent-error
4. Do NOT retry more than once automatically
5. Exit cleanly — next run will pick up from state

If a merged self-improvement causes a regression:
1. Log the regression in the failure log
2. Open a revert PR (needs-review)

## FAILURE LOG
# Each line = a past mistake, now prevented.
# Add here. Never remove. Date every entry.
# (Empty on fresh scaffold — grows with your project)
