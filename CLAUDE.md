# Agentfolio — Scaffold Constitution
# Harness rules only. No project-specific knowledge lives here.
# Project context: read apps/${APP_NAME}/CLAUDE.md

## What this scaffold is
An always-evolving web project harness powered by Claude Code.
The repo IS the system. State lives in state/. Events live in
GitHub Issues. Every agent action is a commit.

## Harness Architecture
Runtime:     GitHub Actions (7 workflows)
State:       state/ folder (committed markdown files)
Event bus:   GitHub Issues with labels
CMS:         content/ folder (Astro content collections)
Memory:      state/project_state.md (read/write every run)
Deployment:  GitHub Pages (Astro static build)

## Session Protocol

ON START (every workflow run):
1. Read state/project_state.md — what happened last
2. Read apps/${APP_NAME}/CLAUDE.md — project-specific rules
3. Read apps/${APP_NAME}/FEATURE_STATUS.md — what's failing
4. Check current event: issue body, PR diff, workflow input

ON STOP (every workflow run):
1. Write session summary to state/project_state.md
2. Update state/agent_log.md (append one line)
3. Update apps/${APP_NAME}/FEATURE_STATUS.md if anything changed
4. Commit all state/ changes with message: "state: [summary]"

## Autonomy Rules (scaffold defaults — app CLAUDE.md may override)

AUTO — commit directly, no PR needed:
- State file updates (project_state.md, agent_log.md)
- Broken link patches
- Dependency security patches (non-breaking)
- Regenerated sitemap.xml, llms.txt, robots.txt
- New blog posts synced from RSS
- GitHub API content sync (project descriptions, stars)

PR — open a pull request, label: auto-merge:
- Lint and type fixes
- Content updates to existing project cards
- SEO meta tag improvements
- Lighthouse score improvements (markup/config only)

PR — open a pull request, label: needs-review:
- New profile sections added
- Visual/layout changes
- Skills list modifications
- Any change to apps/${APP_NAME}/CLAUDE.md
- Schema or config file changes

NEVER auto-execute:
- Deleting content or files
- Changing auth configuration
- Modifying workflow YAML files
- Publishing to external platforms (drafts only)

## GitHub Actions Context
- GITHUB_TOKEN: always available, use for API calls
- ANTHROPIC_API_KEY: in secrets, use for claude -p
- APP_NAME env var: set in each workflow, points to apps/ subfolder
- Workflows run on ubuntu-latest runners
- Full outbound internet access in runners

## Tool Usage in Workflows
Preferred order for file operations:
1. GitHub API (for GitHub data — richest, most structured)
2. curl (for external HTTP — RSS, npm stats, etc.)
3. Standard unix tools (grep, jq, sed — for parsing)

## Commit Message Convention
feat(content): add new project card for [repo]
fix(seo): update structured data after profile change
state: session summary — [what was done]
chore(deps): patch [package] security vulnerability
content(sync): refresh [n] project descriptions from GitHub API

## Failure Handling
If a step fails:
1. Write failure to state/agent_log.md
2. Open a GitHub Issue labeled: agent-error
3. Do NOT retry more than once automatically
4. Exit cleanly — next run will pick up from state

## FAILURE LOG
# Each line = a past mistake, now prevented.
# Add here. Never remove. Date every entry.
# (Empty on fresh scaffold — grows with your project)
