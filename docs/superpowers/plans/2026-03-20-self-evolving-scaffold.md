# Self-Evolving Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform Agentfolio from a personal portfolio scaffold into a self-evolving, general-purpose harness whose first project is itself.

**Architecture:** Incremental transform — strip portfolio-specific content and pages, generalize workflows with dynamic APP_NAME resolution, add `apps/scaffold/` for self-referential evolution rules, add `apps/profile/` for repo profile page, introduce `evolve.yml` and `analyze.yml` workflows, create `state/research_log.md` for external knowledge tracking.

**Tech Stack:** Astro 4.5, Tailwind CSS 3.4, GitHub Actions, Claude Code CLI, TypeScript, Zod

**Spec:** `docs/superpowers/specs/2026-03-20-self-evolving-scaffold-design.md`

---

## File Structure

### Files to create
- `apps/scaffold/CLAUDE.md` — self-evolution rules
- `apps/scaffold/FEATURE_STATUS.md` — scaffold improvement tracker
- `apps/profile/CLAUDE.md` — profile page content rules
- `apps/profile/FEATURE_STATUS.md` — profile feature tracker
- `state/research_log.md` — external research findings (append-only)
- `.github/workflows/discover.yml` — project discovery workflow (replaces onboard.yml)
- `.github/workflows/evolve.yml` — self-evolution workflow (replaces maintenance.yml)
- `.github/workflows/analyze.yml` — weekly improvement analysis (replaces growth.yml)
- `src/pages/index.astro` — repo profile page (replaces portfolio index)

### Files to modify
- `CLAUDE.md` — update harness architecture, autonomy rules, workflow list
- `README.md` — rewrite for self-evolving scaffold
- `src/content.config.ts` — new collection schemas for repo profile data
- `src/layouts/Base.astro` — update for repo profile (remove portfolio-specific markup)
- `.github/workflows/deploy.yml` — remove portfolio copy steps, remove hardcoded APP_NAME
- `.github/workflows/triage.yml` — replace hardcoded `apps/portfolio/CLAUDE.md` with dynamic resolution
- `.github/workflows/reviewer.yml` — replace hardcoded `apps/portfolio/CLAUDE.md` with dynamic resolution
- `.github/workflows/coder.yml` — dynamic APP_NAME resolution
- `.github/workflows/claude-task.yml` — dynamic APP_NAME resolution with input
- `skills/harness.md` — update for self-evolution architecture
- `skills/content.md` — generalize from portfolio to project content
- `skills/frontend.md` — generalize for scaffold profile page
- `skills/github-workflows.md` — reflect new workflow names and APP_NAME strategy
- `skills/seo.md` — refocus from personal SEO to repo discoverability
- `tailwind.config.mjs` — strip portfolio-specific config if unused
- `astro.config.mjs` — update site URL handling

### Files to delete
- `content/profile.json`
- `content/projects/example.md`
- `content/projects/` (directory)
- `content/posts/` (directory, currently empty)
- `content/llms.txt`
- `apps/portfolio/CLAUDE.md`
- `apps/portfolio/FEATURE_STATUS.md`
- `apps/portfolio/growth_goals.md`
- `plugin/SKILL.md`
- `plugin/install.mjs`
- `plugin/package.json`
- `docs/onboarding.md`
- `state/drafts/` (directory, if exists — used by old growth.yml)
- `src/pages/projects/[slug].astro`
- `src/pages/api/profile.json.ts`
- `.github/workflows/onboard.yml`
- `.github/workflows/maintenance.yml`
- `.github/workflows/growth.yml`

---

## Task 1: Strip portfolio content and plugin

Remove all portfolio-specific content files and the plugin directory. This is the clean slate for everything that follows.

**Files:**
- Delete: `content/profile.json`, `content/projects/example.md`, `content/llms.txt`
- Delete: `apps/portfolio/CLAUDE.md`, `apps/portfolio/FEATURE_STATUS.md`, `apps/portfolio/growth_goals.md`
- Delete: `plugin/SKILL.md`, `plugin/install.mjs`, `plugin/package.json`
- Delete: `docs/onboarding.md`

- [ ] **Step 1: Delete portfolio content files and empty directories**

```bash
rm content/profile.json content/projects/example.md content/llms.txt
rmdir content/projects
rmdir content/posts 2>/dev/null || true
rmdir state/drafts 2>/dev/null || true
```

- [ ] **Step 2: Delete apps/portfolio/ directory**

```bash
rm -r apps/portfolio
```

- [ ] **Step 3: Delete plugin/ directory**

```bash
rm -r plugin
```

- [ ] **Step 4: Delete portfolio onboarding doc**

```bash
rm docs/onboarding.md
```

- [ ] **Step 5: Verify no broken references to deleted files**

```bash
grep -r "profile\.json\|llms\.txt\|example\.md\|growth_goals\|apps/portfolio\|plugin/" --include="*.ts" --include="*.astro" --include="*.mjs" --include="*.md" --include="*.yml" . | grep -v ".git/" | grep -v "specs/" | grep -v "plans/"
```

Expected: hits in workflow YAMLs, skills, README, CLAUDE.md, src/ files (all fixed in later tasks).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: strip portfolio content, plugin, and onboarding doc"
```

---

## Task 2: Create apps/scaffold/ and apps/profile/

Set up the two new project directories with their CLAUDE.md constitutions and FEATURE_STATUS files.

**Files:**
- Create: `apps/scaffold/CLAUDE.md`
- Create: `apps/scaffold/FEATURE_STATUS.md`
- Create: `apps/profile/CLAUDE.md`
- Create: `apps/profile/FEATURE_STATUS.md`

- [ ] **Step 1: Create apps/scaffold/CLAUDE.md**

```markdown
# Scaffold — Self-Evolution Constitution
# Rules for how the harness improves itself.
# Root harness rules live in the root CLAUDE.md.

## This Project
The scaffold's first project is itself. The agent analyzes its own
workflows, skills, and failure log to propose improvements.
This file governs HOW the agent evolves the harness.

Owner: autonomous (reviewed by human)
Scope: all files in repo root (.github/, skills/, state/, CLAUDE.md)

## Self-Evolution Rules

ANALYZE — what the agent examines:
- CLAUDE.md failure log for repeated patterns
- Workflow run history for inefficiencies
- Skill files for gaps or outdated guidance
- External research (Anthropic blog, GitHub changelog, reference repos)
- state/agent_log.md for action patterns

PROPOSE — how improvements are suggested:
- One structural PR per evolve.yml run maximum
- Each PR must cite the failure or inefficiency that triggered it
- Research-inspired changes always need human review

FORBIDDEN — the agent must never:
- Promote its own autonomy (move needs-review to auto-commit)
- Modify workflow YAML without human review
- Chain multiple structural changes in one run
- Delete skill files or state files

## Autonomy Overrides
# These override root CLAUDE.md defaults for scaffold self-evolution.

failure_log_entries: auto
skill_wording_clarity: auto
skill_behavioral_changes: auto-merge
workflow_yaml_changes: needs-review
claude_md_autonomy_rules: needs-review
new_skill_files: needs-review

## Failure Log
# Add a line every time the agent makes a mistake evolving itself.
# Format: # DATE: what went wrong → what rule prevents it now
```

- [ ] **Step 2: Create apps/scaffold/FEATURE_STATUS.md**

```markdown
# Scaffold — Feature Status

## Core Harness
- [x] State management (project_state.md, agent_log.md)
- [x] Issue-driven event bus (triage → coder → reviewer)
- [x] Deploy pipeline (Astro build → GitHub Pages)
- [x] Manual dev channel (claude-task.yml)
- [ ] Dynamic APP_NAME resolution across workflows
- [ ] Self-evolution loop (evolve.yml)
- [ ] Weekly improvement analysis (analyze.yml)
- [ ] Project discovery (discover.yml)
- [ ] Research log and external knowledge fetching
- [ ] Repo profile page

## Skills
- [x] harness.md
- [x] content.md
- [x] frontend.md
- [x] github-workflows.md
- [x] feedback-intake.md
- [x] seo.md
- [ ] Skills updated for self-evolving architecture
```

- [ ] **Step 3: Create apps/profile/CLAUDE.md**

```markdown
# Profile — Repo Profile Page Constitution
# Rules for the scaffold's public-facing profile page.
# Root harness rules live in the root CLAUDE.md.

## This Project
A live dashboard of the scaffold's own activity and capabilities.
Replaces the personal portfolio. Built with Astro, served from GitHub Pages.

Owner: autonomous (layout changes reviewed by human)
Scope: src/pages/index.astro, src/layouts/Base.astro, content/

## Content Sources
The profile page reads these files at BUILD TIME (no runtime fetches):
- state/agent_log.md → activity feed, commit stats
- state/research_log.md → recent research findings
- skills/*.md → capabilities inventory
- CLAUDE.md failure log → "mistakes it won't make again"

## Content Rules

AUTO — agent updates without asking:
- Stat regeneration from agent_log.md
- Activity feed updates
- Capabilities list sync from skills/

NEEDS APPROVAL (PR with label: needs-review):
- Layout or structural changes to index.astro
- New sections added to the profile
- Hero tagline or copy changes
- Styling changes

NEVER auto-execute:
- Removing sections from the profile
- Changing the repo name or identity
- Adding external tracking or analytics

## Deploy
build: npm run build
output: dist/
pages: GitHub Pages via deploy.yml

## Failure Log
# Format: # DATE: what went wrong → what rule prevents it now
```

- [ ] **Step 4: Create apps/profile/FEATURE_STATUS.md**

```markdown
# Profile — Feature Status

## Page Sections
- [ ] Hero (repo name, tagline, description)
- [ ] Live stats (agent commits, improvements, failures fixed)
- [ ] Evolution timeline (recent agent activity)
- [ ] Capabilities inventory (from skills/)
- [ ] Architecture diagram
- [ ] Getting started guide

## Infrastructure
- [ ] Content schemas for repo profile data
- [ ] Build-time data extraction from state files
- [ ] Auto-refresh via evolve.yml → deploy.yml pipeline
```

- [ ] **Step 5: Commit**

```bash
git add apps/scaffold/ apps/profile/
git commit -m "feat: add apps/scaffold/ and apps/profile/ constitutions"
```

---

## Task 3: Create state/research_log.md

Initialize the new state file for external research tracking.

**Files:**
- Create: `state/research_log.md`

- [ ] **Step 1: Create state/research_log.md**

```markdown
# Research Log
# Append-only. Written by evolve.yml during research phase.
# Format: ISO_TIMESTAMP | source | finding_summary | action_taken
# Example: 2026-03-20T03:00:00Z | anthropic-blog | Claude Code 1.5 adds native hooks | no action — noted for future reference
```

- [ ] **Step 2: Commit**

```bash
git add state/research_log.md
git commit -m "feat: add state/research_log.md for external knowledge tracking"
```

---

## Task 4: Update root CLAUDE.md

Rewrite the harness constitution to reflect the self-evolving architecture, new workflow names, and updated autonomy rules.

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Rewrite CLAUDE.md**

Replace the entire contents with:

```markdown
# Agentfolio — Scaffold Constitution
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
1. Issue/PR-triggered (triage, coder, reviewer): read from issue/PR
   label (e.g., project:profile, project:scaffold). Default: scaffold.
2. Cron-triggered (evolve, analyze): iterate all apps/*/ folders,
   or target scaffold for self-evolution tasks.
3. Manual dispatch (claude-task, discover): accept APP_NAME as input.

## Session Protocol

ON START (every workflow run):
1. Read state/project_state.md — what happened last
2. Read apps/${APP_NAME}/CLAUDE.md — project-specific rules
3. Read apps/${APP_NAME}/FEATURE_STATUS.md — what's done and pending
4. Check current event: issue body, PR diff, workflow input

ON STOP (every workflow run):
1. Write session summary to state/project_state.md
2. Update state/agent_log.md (append one line)
3. Update apps/${APP_NAME}/FEATURE_STATUS.md if anything changed
4. Commit all state/ changes with message: "state: [summary]"

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
- ANTHROPIC_API_KEY: in secrets, use for claude -p
- APP_NAME: resolved dynamically per workflow (see APP_NAME Resolution)
- Workflows run on ubuntu-latest runners
- Full outbound internet access in runners

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
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "feat(harness): rewrite constitution for self-evolving scaffold"
```

---

## Task 5: Update config files and deploy.yml (before page rewrite)

Update astro.config.mjs, deploy.yml, tailwind.config.mjs, package.json, and .gitignore BEFORE rewriting pages, so that intermediate builds don't break due to deleted content files.

**Files:**
- Modify: `.github/workflows/deploy.yml`
- Modify: `astro.config.mjs`
- Modify: `tailwind.config.mjs`
- Modify: `package.json`
- Modify: `.gitignore`

- [ ] **Step 1: Read current files**

```bash
cat .github/workflows/deploy.yml
cat astro.config.mjs
cat tailwind.config.mjs
cat package.json
cat .gitignore
```

- [ ] **Step 2: Update deploy.yml — remove portfolio-specific lines**

Remove from deploy.yml:
- The `env: APP_NAME: portfolio` on the "Build Astro site" step (around line 35-36)
- The step that copies `content/llms.txt` to `dist/llms.txt` (around line 50)
- The step that copies `content/profile.json` to `dist/api/profile.json` (around line 57)

Keep everything else (checkout, Node setup, npm install, Astro build, Pages deploy).

- [ ] **Step 3: Update astro.config.mjs**

Remove the portfolio-specific site URL logic that reads `content/profile.json`. Use a simple static site URL or environment variable instead. Keep Tailwind and Sitemap integrations. Ensure static output mode.

- [ ] **Step 4: Update tailwind.config.mjs**

Review and strip any portfolio-specific typography or badge classes that are no longer used. Keep base config.

- [ ] **Step 5: Update package.json**

Update the `name` field to `agentfolio` (not portfolio). Update `description`. Remove any portfolio-specific scripts if present.

- [ ] **Step 6: Add ephemeral workflow files to .gitignore**

Add these lines to `.gitignore`:

```
# Ephemeral workflow communication files
.proposed-change.md
.trigger-discovery.txt
```

- [ ] **Step 7: Verify deploy.yml has no portfolio references**

```bash
grep -n "portfolio\|profile\.json\|llms\.txt" .github/workflows/deploy.yml
```

Expected: no output.

- [ ] **Step 8: Commit**

```bash
git add .github/workflows/deploy.yml astro.config.mjs tailwind.config.mjs package.json .gitignore
git commit -m "chore: update configs, deploy.yml, and .gitignore for scaffold"
```

---

## Task 6: Update triage.yml and reviewer.yml

Replace hardcoded `apps/portfolio/CLAUDE.md` references with dynamic APP_NAME resolution via issue/PR labels.

**Files:**
- Modify: `.github/workflows/triage.yml`
- Modify: `.github/workflows/reviewer.yml`

- [ ] **Step 1: Read current triage.yml**

```bash
cat .github/workflows/triage.yml
```

- [ ] **Step 2: Update triage.yml**

Replace the hardcoded `apps/portfolio/CLAUDE.md` reference in the prompt with dynamic resolution. Add a step before the Claude action that extracts APP_NAME from issue labels:

```yaml
- name: Resolve APP_NAME
  id: resolve-app
  run: |
    APP_NAME=$(gh issue view ${{ github.event.issue.number }} --json labels -q '.labels[].name' | grep '^project:' | sed 's/project://' | head -1)
    echo "app_name=${APP_NAME:-scaffold}" >> "$GITHUB_OUTPUT"
  env:
    GH_TOKEN: ${{ github.token }}
```

Then update the prompt to reference `apps/${{ steps.resolve-app.outputs.app_name }}/CLAUDE.md`.

- [ ] **Step 3: Read current reviewer.yml**

```bash
cat .github/workflows/reviewer.yml
```

- [ ] **Step 4: Update reviewer.yml**

Same pattern — extract APP_NAME from PR labels:

```yaml
- name: Resolve APP_NAME
  id: resolve-app
  run: |
    APP_NAME=$(gh pr view ${{ github.event.pull_request.number }} --json labels -q '.labels[].name' | grep '^project:' | sed 's/project://' | head -1)
    echo "app_name=${APP_NAME:-scaffold}" >> "$GITHUB_OUTPUT"
  env:
    GH_TOKEN: ${{ github.token }}
```

Update the prompt to reference `apps/${{ steps.resolve-app.outputs.app_name }}/CLAUDE.md`.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/triage.yml .github/workflows/reviewer.yml
git commit -m "feat(workflow): dynamic APP_NAME resolution in triage and reviewer"
```

---

## Task 7: Update coder.yml and claude-task.yml

Replace hardcoded APP_NAME with dynamic resolution.

**Files:**
- Modify: `.github/workflows/coder.yml`
- Modify: `.github/workflows/claude-task.yml`

- [ ] **Step 1: Read current coder.yml**

```bash
cat .github/workflows/coder.yml
```

- [ ] **Step 2: Update coder.yml**

Replace `env: APP_NAME: portfolio` with dynamic resolution from issue labels (same pattern as triage.yml). Update all `${APP_NAME}` references in the prompt-building step to use the resolved value.

- [ ] **Step 3: Read current claude-task.yml**

```bash
cat .github/workflows/claude-task.yml
```

- [ ] **Step 4: Update claude-task.yml**

Add `app_name` as a workflow_dispatch input with default `scaffold`:

```yaml
inputs:
  app_name:
    description: 'Target project (folder name in apps/)'
    required: false
    default: 'scaffold'
```

Replace `env: APP_NAME: portfolio` with `env: APP_NAME: ${{ github.event.inputs.app_name }}`.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/coder.yml .github/workflows/claude-task.yml
git commit -m "feat(workflow): dynamic APP_NAME in coder and claude-task"
```

---

## Task 8: Create discover.yml (replaces onboard.yml)

Write the project discovery workflow and delete the old onboard.yml.

**Files:**
- Create: `.github/workflows/discover.yml`
- Delete: `.github/workflows/onboard.yml`

- [ ] **Step 1: Read current onboard.yml for reference**

```bash
cat .github/workflows/onboard.yml
```

- [ ] **Step 2: Create discover.yml**

```yaml
name: Discover Project

on:
  workflow_dispatch:
    inputs:
      app_name:
        description: 'Folder name in apps/ to discover (or "all" to scan for new projects)'
        required: false
        default: 'all'

permissions:
  contents: write
  pull-requests: write

jobs:
  discover:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Build discovery prompt
        run: |
          cat > /tmp/prompt.txt << 'PROMPT'
          You are the project discovery agent for Agentfolio.

          ## Your Task
          Scan the apps/ directory for projects that need setup.

          If app_name is "all": find every folder in apps/ that does NOT
          have a CLAUDE.md file and discover each one.

          If app_name is specific: discover that one project.

          ## Discovery Process
          For each project folder:
          1. SCAN — list all files, check for package.json, Dockerfile,
             config files, source code extensions, directory structure
          2. INFER — determine: language, framework, build tool, test runner,
             deploy mechanism
          3. GENERATE — create two files:
             - apps/<name>/CLAUDE.md with:
               - Project description (inferred from README, package.json, or code)
               - Stack details
               - Build/test/deploy commands (from config files)
               - Autonomy overrides (conservative: everything starts needs-review)
               - Empty failure log
             - apps/<name>/FEATURE_STATUS.md with:
               - Feature inventory based on what you found

          ## Rules
          - Do NOT modify the project's own code
          - Do NOT create per-project workflows
          - Do NOT assume any specific framework — infer everything
          - If apps/<name>/CLAUDE.md already exists, skip that project
          - Write files directly, do not open a PR (the workflow handles git)

          ## Context
          $(cat CLAUDE.md)

          ## Target
          App name: ${{ github.event.inputs.app_name }}
          PROMPT

      - name: Run Claude Code
        run: |
          claude -p "$(cat /tmp/prompt.txt)" \
            --allowedTools "bash,read,write,edit,glob,grep" \
            --max-turns 20
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Check for changes
        id: changes
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            echo "has_changes=true" >> "$GITHUB_OUTPUT"
          else
            echo "has_changes=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Update state (on main, before any branch checkout)
        run: |
          CHANGED=$(git status --porcelain | wc -l)
          echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | discover | scanned apps/ for new projects | ${CHANGED} files changed" >> state/agent_log.md
          git add state/
          git commit -m "state: discovery scan completed" || true
          git push || true

      - name: Create PR with discovered projects
        if: steps.changes.outputs.has_changes == 'true'
        run: |
          BRANCH="discover/$(date +%Y%m%d-%H%M%S)"
          git checkout -b "$BRANCH"
          git add apps/
          git commit -m "feat: discover new projects in apps/"
          git push -u origin "$BRANCH"
          gh pr create \
            --title "Discover: new project configurations" \
            --body "Auto-generated project constitutions from discover.yml. Review the generated CLAUDE.md files before merging." \
            --label "needs-review"
        env:
          GH_TOKEN: ${{ github.token }}
```

- [ ] **Step 3: Delete onboard.yml**

```bash
rm .github/workflows/onboard.yml
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/discover.yml .github/workflows/onboard.yml
git commit -m "feat(workflow): add discover.yml, remove onboard.yml"
```

---

## Task 9: Create evolve.yml (replaces maintenance.yml)

Write the self-evolution workflow and delete maintenance.yml.

**Files:**
- Create: `.github/workflows/evolve.yml`
- Delete: `.github/workflows/maintenance.yml`

- [ ] **Step 1: Read current maintenance.yml for reference**

```bash
cat .github/workflows/maintenance.yml
```

- [ ] **Step 2: Create evolve.yml**

```yaml
name: Self-Evolve

on:
  schedule:
    - cron: '0 3 * * *'  # Daily 3am UTC
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write
  issues: write

env:
  APP_NAME: scaffold

jobs:
  evolve:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 50

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Build evolution prompt
        run: |
          cat > /tmp/prompt.txt << 'PROMPT'
          You are the self-evolution agent for Agentfolio.

          ## Your Task
          Analyze the scaffold and propose improvements. You have two phases:

          ### Phase 1: Research
          Fetch external knowledge to inform improvements:
          - Check reference repos for new commits/releases:
            - https://api.github.com/repos/godagoo/claude-code-always-on/commits?per_page=5
            - https://api.github.com/repos/humanlayer/humanlayer/commits?per_page=5
          - Check GitHub Actions changelog:
            - https://api.github.com/repos/actions/runner/releases?per_page=3
          - Log all findings to state/research_log.md (append only)
          - Format: ISO_TIMESTAMP | source | finding_summary | action_taken

          ### Phase 2: Analyze
          Read and analyze:
          - state/agent_log.md — recent actions and patterns
          - state/project_state.md — current state
          - CLAUDE.md failure log — repeated failures
          - .github/workflows/*.yml — workflow efficiency
          - skills/*.md — skill coverage gaps
          - Recent git log (last 20 commits) — what changed

          Look for:
          - Repeated failures that need new rules
          - Workflow inefficiencies that need patches
          - Missing skills that need drafting
          - New apps/ folders without CLAUDE.md (trigger discovery)

          ### Phase 3: Act
          Based on findings:
          - AUTO-COMMIT: failure log entries, state updates, skill wording fixes
          - Write improvements to files directly for auto-commit items
          - For structural changes (workflow YAML, CLAUDE.md rules, new skills):
            write a file at .proposed-change.md describing the change and why
          - Maximum ONE structural change proposal per run

          ### Rules
          - You CANNOT promote your own autonomy
          - You CANNOT modify workflow YAML directly (propose only)
          - Each proposal must cite the failure or research that triggered it
          - If you find a new apps/ folder without CLAUDE.md, note it in
            .trigger-discovery.txt with the folder name (workflow handles dispatch)

          ## Context
          $(cat CLAUDE.md)
          $(cat apps/scaffold/CLAUDE.md)

          ## Current State
          $(cat state/project_state.md)

          ## Recent Agent Log (last 20 lines)
          $(tail -20 state/agent_log.md)

          ## Failure Log
          $(grep "^# [0-9]" CLAUDE.md | tail -20)
          PROMPT

      - name: Run Claude Code
        run: |
          claude -p "$(cat /tmp/prompt.txt)" \
            --allowedTools "bash,read,write,edit,glob,grep" \
            --max-turns 30
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Auto-commit safe changes
        run: |
          git add state/ CLAUDE.md skills/
          git diff --cached --quiet || git commit -m "state: evolve.yml — $(date -u +%Y-%m-%d)"
          git push || true

      - name: Trigger discovery if needed
        if: hashFiles('.trigger-discovery.txt') != ''
        run: |
          APP=$(cat .trigger-discovery.txt)
          gh workflow run discover.yml -f app_name="$APP"
          rm .trigger-discovery.txt
        env:
          GH_TOKEN: ${{ github.token }}

      - name: Create structural PR if proposed
        if: hashFiles('.proposed-change.md') != ''
        run: |
          BRANCH="evolve/$(date +%Y%m%d-%H%M%S)"
          git checkout -b "$BRANCH"
          # Apply proposed changes (agent wrote them to files)
          git add -A
          TITLE=$(head -1 .proposed-change.md | sed 's/^# //')
          BODY=$(cat .proposed-change.md)
          rm .proposed-change.md
          git commit -m "feat(harness): $TITLE"
          git push -u origin "$BRANCH"
          gh pr create \
            --title "$TITLE" \
            --body "$BODY" \
            --label "needs-review"
        env:
          GH_TOKEN: ${{ github.token }}
```

- [ ] **Step 3: Delete maintenance.yml**

```bash
rm .github/workflows/maintenance.yml
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/evolve.yml .github/workflows/maintenance.yml
git commit -m "feat(workflow): add evolve.yml self-evolution loop, remove maintenance.yml"
```

---

## Task 10: Create analyze.yml (replaces growth.yml)

Write the weekly improvement analysis workflow and delete growth.yml.

**Files:**
- Create: `.github/workflows/analyze.yml`
- Delete: `.github/workflows/growth.yml`

- [ ] **Step 1: Read current growth.yml for reference**

```bash
cat .github/workflows/growth.yml
```

- [ ] **Step 2: Create analyze.yml**

```yaml
name: Weekly Analysis

on:
  schedule:
    - cron: '0 6 * * 1'  # Monday 6am UTC
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

env:
  APP_NAME: scaffold

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Build analysis prompt
        run: |
          cat > /tmp/prompt.txt << 'PROMPT'
          You are the weekly analysis agent for Agentfolio.

          ## Your Task
          Produce a strategic analysis of the scaffold's past week.

          ### What to analyze
          1. Read state/agent_log.md entries from the past 7 days
          2. Read state/research_log.md entries from the past 7 days
          3. Review git log from the past 7 days
          4. Check apps/scaffold/FEATURE_STATUS.md — what progressed?
          5. Check apps/profile/FEATURE_STATUS.md — what progressed?

          ### What to look for
          - Recurring failures or patterns in agent_log
          - Workflow bottlenecks (PRs that took multiple review rounds)
          - Skills used vs. available — any gaps?
          - Research findings that haven't been acted on yet
          - FEATURE_STATUS items that are stalled

          ### Output
          Append a weekly summary to state/agent_log.md with:
          - Format: ISO_TIMESTAMP | analyze | weekly-summary | [key findings]
          - Include: actions completed, failures encountered, recommendations

          Update state/project_state.md with current priorities.

          If clear improvements are identified, write them to
          .proposed-change.md (same format as evolve.yml — one per run max).

          ## Context
          $(cat CLAUDE.md)
          $(cat apps/scaffold/CLAUDE.md)

          ## Current State
          $(cat state/project_state.md)
          PROMPT

      - name: Run Claude Code
        run: |
          claude -p "$(cat /tmp/prompt.txt)" \
            --allowedTools "bash,read,write,edit,glob,grep" \
            --max-turns 20
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Commit state updates
        run: |
          git add state/
          git diff --cached --quiet || git commit -m "state: weekly analysis — $(date -u +%Y-%m-%d)"
          git push || true

      - name: Create improvement PR if proposed
        if: hashFiles('.proposed-change.md') != ''
        run: |
          BRANCH="analyze/$(date +%Y%m%d)"
          git checkout -b "$BRANCH"
          git add -A
          TITLE=$(head -1 .proposed-change.md | sed 's/^# //')
          BODY=$(cat .proposed-change.md)
          rm .proposed-change.md
          git commit -m "feat(harness): $TITLE"
          git push -u origin "$BRANCH"
          gh pr create \
            --title "$TITLE" \
            --body "$BODY" \
            --label "needs-review"
        env:
          GH_TOKEN: ${{ github.token }}
```

- [ ] **Step 3: Delete growth.yml**

```bash
rm .github/workflows/growth.yml
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/analyze.yml .github/workflows/growth.yml
git commit -m "feat(workflow): add analyze.yml weekly analysis, remove growth.yml"
```

---

## Task 11: Rewrite content schemas and profile page

Replace portfolio content schemas with repo profile data schemas. Replace portfolio index with repo profile page.

**Files:**
- Modify: `src/content.config.ts`
- Modify: `src/pages/index.astro`
- Modify: `src/layouts/Base.astro`
- Delete: `src/pages/projects/[slug].astro`
- Delete: `src/pages/api/profile.json.ts`

- [ ] **Step 1: Read current files**

```bash
cat src/content.config.ts
cat src/pages/index.astro
cat src/layouts/Base.astro
cat src/pages/projects/\[slug\].astro
cat src/pages/api/profile.json.ts
```

- [ ] **Step 2: Rewrite src/content.config.ts**

The profile page reads state files and skill files directly via `fs.readFileSync` at build time (Astro runs in Node). Skill files have no YAML frontmatter, so Astro content collections won't work for them. Replace with an empty/minimal config:

```typescript
// Content collections are not used for the repo profile page.
// State and skill files are read directly via fs at build time.
// This file is kept for future content collection use by discovered projects.
export const collections = {};
```

- [ ] **Step 3: Delete portfolio page templates**

```bash
rm src/pages/projects/\[slug\].astro
rm src/pages/api/profile.json.ts
rmdir src/pages/projects src/pages/api
```

- [ ] **Step 4: Rewrite src/layouts/Base.astro**

Update the layout to remove portfolio-specific markup (JSON-LD for Person, portfolio OG tags). Keep the HTML shell, agent badge logic, and basic meta tags. Update title and description for the scaffold.

Key changes:
- Title: "Agentfolio — Self-Evolving Scaffold"
- Description: repo description instead of personal bio
- Remove JSON-LD Person schema
- Keep agent badge logic (reads state/agent_log.md at build time)
- Update OG tags for repo profile

- [ ] **Step 5: Rewrite src/pages/index.astro**

Replace portfolio page with repo profile page. The page should:

1. Import and use Base layout
2. Read `state/agent_log.md` via `fs.readFileSync` at build time, parse pipe-delimited entries
3. Read skill files from `skills/` directory via `fs.readdirSync` + `fs.readFileSync` (no content collections — skill files lack frontmatter)
4. Read CLAUDE.md failure log entries via `fs.readFileSync` and parse lines starting with `# 20` (date-prefixed entries)
5. Render sections:
   - **Hero**: "Agentfolio" title, tagline, brief description
   - **Stats**: count of agent log entries, unique workflows, failure log entries
   - **Recent Activity**: last 10 agent log entries as a timeline
   - **Capabilities**: list skills with descriptions
   - **Failure Log**: "mistakes it won't make again" section
   - **Getting Started**: fork instructions

Use Tailwind for styling. Keep it minimal and clean.

- [ ] **Step 6: Verify build works**

```bash
npm install && npm run build
```

Expected: successful build with `dist/index.html` generated.

- [ ] **Step 7: Commit**

```bash
git add src/ content/
git commit -m "feat: replace portfolio with repo profile page"
```

---

## Task 12: Update skills files

Generalize all skill files from portfolio-specific to scaffold-general.

**Files:**
- Modify: `skills/harness.md`
- Modify: `skills/content.md`
- Modify: `skills/frontend.md`
- Modify: `skills/github-workflows.md`
- Modify: `skills/seo.md`
- Keep: `skills/feedback-intake.md` (already generic)

- [ ] **Step 1: Read all skill files**

```bash
for f in skills/*.md; do echo "=== $f ==="; cat "$f"; done
```

- [ ] **Step 2: Update skills/harness.md**

Key changes:
- Update workflow list (8 workflows with new names)
- Add self-evolution loop description
- Add APP_NAME resolution strategy
- Update state file list (add research_log.md)
- Update autonomy gates to match new CLAUDE.md

- [ ] **Step 3: Update skills/content.md**

Key changes:
- Remove references to profile.json, llms.txt, portfolio project cards
- Generalize to "project content management"
- Describe how content/ serves the repo profile page
- Update collection schemas reference

- [ ] **Step 4: Update skills/frontend.md**

Key changes:
- Remove portfolio page structure references
- Describe the repo profile page structure
- Keep Astro + Tailwind patterns (still relevant)
- Update build commands if changed

- [ ] **Step 5: Update skills/github-workflows.md**

Key changes:
- Update workflow names (onboard→discover, maintenance→evolve, growth→analyze)
- Add APP_NAME dynamic resolution documentation
- Add `gh workflow run` chaining pattern for discover.yml
- Update trigger documentation

- [ ] **Step 6: Update skills/seo.md**

Key changes:
- Remove personal SEO focus (JSON-LD Person, personal OG tags)
- Refocus on repo discoverability (GitHub SEO, README optimization)
- Keep robots.txt and sitemap guidance
- Update structured data for SoftwareApplication or Project schema

- [ ] **Step 7: Commit**

```bash
git add skills/
git commit -m "feat: generalize skill files for self-evolving scaffold"
```

---

## Task 13: Rewrite README.md

Replace portfolio README with scaffold README.

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite README.md**

```markdown
# Agentfolio

**A self-evolving scaffold for autonomous web projects.**
The repo is the system. The scaffold's first project is itself.

---

## What it is

Agentfolio is a harness of GitHub Actions workflows that make any web project
agent-powered. The agent triages feedback, fixes bugs, discovers new projects,
and evolves its own workflows and skills over time.

No server. No daemon. No database. GitHub IS the infrastructure.

---

## How it works

```
Push to main         → deploy.yml    → Astro build    → Pages live
Feedback issue       → triage.yml   → classify       → labels
agent-ready label    → coder.yml    → implement fix  → PR
Agent PR opened      → reviewer.yml → review         → merge/flag
Daily 3am UTC        → evolve.yml   → self-evolution → improvements
Monday 6am UTC       → analyze.yml  → weekly review  → priorities
New app folder       → discover.yml → infer stack    → generate rules
Your instruction     → claude-task  → Claude acts    → commit
```

---

## The eight workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `deploy.yml` | push to main | Astro build → GitHub Pages |
| `discover.yml` | manual / evolve trigger | Scans apps/, infers stack, generates CLAUDE.md |
| `triage.yml` | feedback issue opened | Classifies bug/ux/positive, labels |
| `coder.yml` | agent-ready label added | Implements fix, opens PR |
| `reviewer.yml` | agent PR opened | Reviews diff, approves or flags |
| `evolve.yml` | daily 3am UTC | Analyzes failures + research, proposes improvements |
| `analyze.yml` | weekly Monday 6am UTC | Strategic analysis, identifies patterns |
| `claude-task.yml` | manual (anytime) | Your dev channel — type any instruction |

---

## Self-evolution

The scaffold improves itself daily:

1. **Research** — checks reference repos and changelogs for new patterns
2. **Analyze** — reads its own failure log and action history
3. **Act** — auto-commits safe fixes, opens PRs for structural changes
4. **Learn** — every mistake becomes a rule that prevents recurrence

The agent cannot promote its own autonomy. Structural changes always need
human review. The git log is the audit trail.

---

## Quick start

1. Fork this repo
2. Settings → Secrets → Add `ANTHROPIC_API_KEY`
3. Settings → Pages → Source: GitHub Actions
4. Drop your project in `apps/your-project/`
5. Run the "Discover Project" workflow
6. The scaffold generates rules for your project and starts maintaining it

---

## Adding a project

Create a folder in `apps/` with your code. Run `discover.yml`. The agent will:
- Scan your files and infer the stack
- Generate `apps/your-project/CLAUDE.md` with tailored rules
- Generate `apps/your-project/FEATURE_STATUS.md`
- Open a PR for your review

Or create `apps/your-project/CLAUDE.md` manually — see `apps/scaffold/CLAUDE.md`
for the format.

---

## Philosophy

> The model is the agent. The code is the harness.

Every agent mistake becomes a line in the failure log. The constitution grows
with the project. The git log is the audit trail. The Issues tab is the event
bus. The Actions tab is the dashboard.

---

## References

Built on patterns from:
- [godagoo/claude-code-always-on](https://godagoo.github.io/claude-code-always-on/)
- [mitchellh.com — harness engineering](https://mitchellh.com/writing/my-ai-adoption-journey)
- [Anthropic — Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [humanlayer/12-factor-agents](https://github.com/humanlayer/humanlayer)

---

## License

MIT — fork it, adapt it, build on it.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: rewrite README for self-evolving scaffold"
```

---

## Task 14: Write scaffold onboarding doc

Replace the deleted portfolio onboarding guide with a scaffold-focused one.

**Files:**
- Create: `docs/onboarding.md`

- [ ] **Step 1: Create docs/onboarding.md**

Write a scaffold-focused onboarding guide covering:
- Prerequisites (GitHub account, Anthropic API key)
- Fork and configure (secrets, Pages settings)
- How the scaffold works (brief workflow overview)
- Adding your first project to `apps/`
- Running `discover.yml` to generate rules
- Customizing `apps/your-project/CLAUDE.md`
- Understanding the self-evolution loop

Keep it concise — the README covers the high-level overview, this is the step-by-step walkthrough.

- [ ] **Step 2: Commit**

```bash
git add docs/onboarding.md
git commit -m "docs: add scaffold-focused onboarding guide"
```

---

## Task 15: Update issue templates

Update the feedback issue template to be project-generic instead of portfolio-specific.

**Files:**
- Modify: `.github/ISSUE_TEMPLATE/feedback.yml`
- Keep: `.github/ISSUE_TEMPLATE/config.yml`

- [ ] **Step 1: Read current feedback template**

```bash
cat .github/ISSUE_TEMPLATE/feedback.yml
```

- [ ] **Step 2: Update feedback.yml**

Remove any portfolio-specific wording. Make the template generic:
- Update title/description to reference "this project" instead of "portfolio"
- Add a project dropdown field if there are multiple apps
- Keep the feedback categories (bug, UX, positive, other)

- [ ] **Step 3: Commit**

```bash
git add .github/ISSUE_TEMPLATE/
git commit -m "chore: generalize feedback issue template"
```

---

## Task 16: Final verification and FEATURE_STATUS update

Run full build, verify no broken references, update feature status.

**Files:**
- Modify: `apps/scaffold/FEATURE_STATUS.md`
- Modify: `apps/profile/FEATURE_STATUS.md`

- [ ] **Step 1: Verify no remaining portfolio references**

```bash
grep -rn "portfolio" --include="*.yml" --include="*.ts" --include="*.astro" --include="*.mjs" --include="*.json" . | grep -v ".git/" | grep -v node_modules | grep -v "specs/" | grep -v "plans/"
```

Expected: no output (or only in CLAUDE.md failure log historical entries).

- [ ] **Step 2: Run full build**

```bash
npm install && npm run build
```

Expected: clean build.

- [ ] **Step 3: Update apps/scaffold/FEATURE_STATUS.md**

Mark completed items:
- [x] Dynamic APP_NAME resolution across workflows
- [x] Self-evolution loop (evolve.yml)
- [x] Weekly improvement analysis (analyze.yml)
- [x] Project discovery (discover.yml)
- [x] Research log and external knowledge fetching
- [x] Skills updated for self-evolving architecture

- [ ] **Step 4: Update apps/profile/FEATURE_STATUS.md**

Mark completed items:
- [x] Hero (repo name, tagline, description)
- [x] Content schemas for repo profile data
- Mark remaining items as still pending (stats, timeline, etc. will be iteratively improved by the scaffold itself)

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "feat: complete self-evolving scaffold transformation"
```

- [ ] **Step 6: Push**

```bash
git push
```
