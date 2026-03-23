# Evolve Research Postures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the evolve.yml step-by-step checklist prompt with a posture-based self-directing research system that restores pattern extraction and adds source exploration.

**Architecture:** The evolve workflow's Claude prompt is replaced entirely. A new `state/research_sources.md` file gives Claude ownership of its source inventory. The prompt defines 4 research postures (PATTERN HUNT, PIPELINE WATCH, HORIZON SCAN, SYNTHESIS) that Claude rotates through. The YAML workflow structure outside the prompt is minimally changed (only the prompt heredoc and the usage logging step).

**Tech Stack:** GitHub Actions YAML, Claude Code CLI, bash, GitHub API

**Spec:** `docs/superpowers/specs/2026-03-23-evolve-research-postures-design.md`

**Prerequisites:** Create the feature branch before starting any tasks:
```bash
git checkout -b feat/evolve-research-postures
```

---

### Task 1: Create seed research_sources.md

**Files:**
- Create: `state/research_sources.md`

This is the Claude-managed source inventory, seeded from the current evolve_config.md Research Sources list with purpose annotations added per the spec's Initial Seed table.

- [ ] **Step 1: Create state/research_sources.md**

```markdown
# Research Sources
# Managed by evolve.yml. Claude adds, prunes, and annotates freely.
# Seeded from evolve_config.md on first run.
# Last updated: 2026-03-23T00:00:00Z

## Active Sources

### anthropics/claude-code
- **Why:** The runtime we build on — releases, breaking changes, new hooks, CLI flags
- **Look for:** CHANGELOG entries, new hook types, permission changes, SDK updates
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Protected source — never drop. Check CHANGELOG and releases, not just commits.

### garrytan/gstack
- **Why:** Harness engineering patterns — skills, slash commands, review protocols, agent orchestration
- **Look for:** New skill files, workflow patterns, agent guardrails, PR review techniques, structured output formats
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 5
- **Notes:** Most productive source so far. v0.9.7-v0.11.3 yielded adversarial review, structured tables, anti-sycophancy, pre-merge gate, security patterns.

### affaan-m/everything-claude-code
- **Why:** Community harness patterns, skill collections, optimization techniques
- **Look for:** New skills, CLAUDE.md patterns, workflow architectures, instinct files
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 1
- **Notes:** Large community repo — watch for novel patterns emerging from contributors.

### hesreallyhim/awesome-claude-code
- **Why:** Curated ecosystem catalog — discover new tools, libraries, and patterns
- **Look for:** New entries in Orchestrators/Tools/Skills sections, trending repos referenced
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Good source for HORIZON SCAN cross-references.

### bytedance/deer-flow
- **Why:** Multi-agent orchestration patterns from a major tech company
- **Look for:** Agent coordination, state management, tool orchestration, LLM provider patterns
- **Added:** 2026-03-21 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Active development. Enterprise-scale patterns may not be directly applicable but inform design.

### wshobson/agents
- **Why:** Agent framework patterns — autonomous agent architectures
- **Look for:** Retry patterns, memory management, tool selection, agent lifecycle
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Monitor for novel agent architecture ideas.

### VoltAgent/awesome-claude-code-subagents
- **Why:** Subagent patterns and skill registry — how others structure agent delegation
- **Look for:** New subagent types, skill file formats, delegation patterns
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Community-curated list of subagent implementations.

### actions/runner
- **Why:** CI/CD runtime we depend on — deprecation notices, new features, security fixes
- **Look for:** Node.js version deprecation timelines, runner image changes, new action features
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Check releases, not just commits. Dependency bumps are usually noise.

### withastro/astro
- **Why:** Web framework we use — security fixes, breaking changes, new features
- **Look for:** Security advisories, breaking changes in minor/major releases, new content collection features
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Only actionable for security fixes or features that affect our site build.

### verkyyi/tokenman
- **Why:** Self-reference — track forks, adopters, and how the scaffold is used
- **Look for:** New forks, adopter modifications, issues filed by users
- **Added:** 2026-03-20 (seed) | **Last deep:** never | **Pattern hits:** 0
- **Notes:** Used during HORIZON SCAN for adoption tracking.

## Watch List
<!-- Sources under evaluation. Promoted to Active or Dropped after 3+ observations over 7+ days. -->

## Dropped Sources
<!-- Removed sources with reason. Kept for history so we don't re-discover them. -->

### godagoo/claude-code-always-on
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-02-03 (7+ weeks), no new patterns found

### humanlayer/humanlayer
- **Dropped:** 2026-03-23 | **Reason:** Inactive since 2026-01-07 (11+ weeks), no relevant patterns
```

- [ ] **Step 2: Verify the file exists and has correct structure**

Run: `head -5 state/research_sources.md && grep -c "^### " state/research_sources.md`
Expected: Header lines visible, 12 source headings (10 Active + 2 Dropped)

- [ ] **Step 3: Commit**

```bash
git add state/research_sources.md
git commit -m "feat(state): seed research_sources.md from evolve_config.md

Claude-managed source inventory with per-source purpose annotations,
'Look for' hints, and pattern hit stats. Replaces the static source
list in evolve_config.md.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Write the new evolve.yml prompt

**Files:**
- Modify: `.github/workflows/evolve.yml:36-445` (the entire "Build evolution prompt" step)

This is the core change. Replace the ~400-line step-by-step prompt with the posture-based prompt. The prompt is structured as: Identity → Always-Do → Posture Selection → 4 Posture Playbooks → Source Management → Issue Creation → Logging → Hard Rules. Context injection at the bottom stays similar but adds research_sources.md and recent research_log.

- [ ] **Step 1: Replace the "Build evolution prompt" step**

Replace `.github/workflows/evolve.yml` lines 36-445 (the entire `name: Build evolution prompt` step and its `run:` block) with:

```yaml
      - name: Build evolution prompt
        run: |
          cat > /tmp/prompt.txt << 'PROMPT'
          You are a self-directing research agent for this project. Your mission:
          find patterns, tools, and practices in the broader ecosystem that can
          make this harness better — then turn the best findings into actionable issues.

          You are NOT a checklist executor. You are a researcher with judgment.
          Each run, you choose a research posture, go deep on what matters,
          and skip what doesn't. Quality of insight beats breadth of coverage.

          You MUST execute bash commands to fetch data, write files, and make changes.
          Do NOT just reason about what to do — actually do it.

          ## ALWAYS: Quick Health Glance (every run, before posture)

          Run this first, regardless of which posture you pick:

          ```bash
          TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
          FAILED=$(gh run list --status failure --limit 5 --json databaseId,workflowName,createdAt \
            -q '.[] | "\(.databaseId) | \(.workflowName) | \(.createdAt)"')
          ```

          If there are 3+ NEW failures (not listed in the Previous Evolve Run Summary),
          you MUST pick PIPELINE_WATCH as your posture. Otherwise, note them for the
          next PIPELINE_WATCH run and proceed with your chosen posture.

          ## Posture Selection

          Read the posture history and "Runs since each" counters from the
          Previous Evolve Run Summary below.

          Pick ONE posture for this run:
          1. If any posture hasn't run in 8+ runs → MUST pick it (staleness override)
          2. If 3+ new pipeline failures (from health glance above) → MUST pick PIPELINE_WATCH
          3. Otherwise, pick what's most valuable right now:
             - Many sources have new SHAs since last scan → PATTERN_HUNT
             - research_log has 5+ unresolved findings from recent runs → SYNTHESIS
             - Watch List is empty or stale → HORIZON_SCAN
             - Usage costs trending up or recent failures → PIPELINE_WATCH
          4. Suggested cadence per 8-run window: PATTERN_HUNT ×3, PIPELINE_WATCH ×2,
             HORIZON_SCAN ×2, SYNTHESIS ×1

          If no posture history exists (first run), or the Previous Evolve Run
          Summary does not contain a "Posture:" field (transition from old format):
          pick PATTERN_HUNT. Set all "runs since" counters to 8.

          Log your choice and one-line reasoning before executing.

          ## Posture: PATTERN HUNT
          Mindset: "What can we adopt?"

          1. From your Research Sources (Active section), pick 3-4 to deep-dive.
             Prioritize:
             - Sources with recent changes (SHA differs from last summary)
             - Sources with high pattern-hit rate (see "Pattern hits" in research_sources.md)
             - Sources not deep-dived in 5+ runs (see "Last deep" timestamp)
          2. For each, fetch recent commits AND read the actual changes:
               COMMITS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                 "https://api.github.com/repos/OWNER/REPO/commits?per_page=5" | head -c 2000)
             For any interesting commit, read the diff or PR description:
               DETAIL=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                 "https://api.github.com/repos/OWNER/REPO/commits/SHA" | head -c 3000)
          3. For each change, ask: "What pattern is this? Could our harness adopt it?"
             - If yes: log the pattern in research_log.md with: source, pattern name,
               what it does, how it could apply to our harness
             - If no: one sentence why not, move on
          4. Update each deep-dived source's "Last deep" timestamp and "Pattern hits"
             count in state/research_sources.md
          5. Quick SHA scan of remaining Active sources — note any changes for next run
             but don't deep-dive them

          Issue creation: create issues for patterns with a clear adoption path.
          Title: "[evolve] Adopt X pattern from Y"

          ## Posture: PIPELINE WATCH
          Mindset: "Is anything broken or degrading?"

          1. Full failure analysis:
               FAILED=$(gh run list --status failure --limit 10 \
                 --json databaseId,workflowName,createdAt,conclusion \
                 -q '.[] | "\(.databaseId) | \(.workflowName) | \(.createdAt)"')
          2. For each failed run:
             - Get details: `gh run view <id> --log-failed 2>&1 | tail -30`
             - Categorize: ALREADY-FIXED (same workflow succeeded more recently) /
               TRANSIENT (network, rate limit, runner) / ACTIONABLE (code bug, config error)
             - For ACTIONABLE: check if issue exists
               (`gh issue list --state open --label pipeline-fix --json title -q '.[].title'`),
               create if not:
               `gh issue create --title "[pipeline] Brief description" --body "..." --label "pipeline-fix,project:$(echo $GITHUB_REPOSITORY | cut -d/ -f2)"`
          3. Check state/usage_log.md for cost trends or token saturation patterns
          4. Quick SHA scan of all Active sources (note changes, don't deep-dive)

          Append health summary to research_log.md:
          TIMESTAMP | pipeline-health | X failed, Y actionable, Z issues created | details

          Issue creation: pipeline-fix issues only.

          ## Posture: HORIZON SCAN
          Mindset: "What's new out there?"

          1. Search for new repos in the problem space:
               # Trending: claude code agent repos, pushed recently
               TRENDING=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                 "https://api.github.com/search/repositories?q=claude+code+agent+pushed:>$(date -u -d '7 days ago' +%Y-%m-%d)&sort=stars&per_page=15" \
                 | head -c 4000)
               # Also search: self-evolving, agent harness, claude skills
          2. Check cross-references from Active sources: what do they depend on?
             Who forks them? What related repos appear in their READMEs?
          3. For each interesting find:
             - Check against Active, Watch List, and Dropped sections in research_sources.md
             - If new: add to Watch List with initial assessment
          4. Review existing Watch List sources:
             - Fetch recent commits for each
             - If 3+ observations over 7+ days AND active + relevant → promote to Active
             - If 3+ observations AND stale/irrelevant → move to Dropped with reason
          5. Review Active sources for staleness:
             - No commits in 4+ weeks → candidate for Dropped (except protected sources)
             - 5+ deep-dives with 0 pattern hits → candidate for Dropped
          6. Check own repo forks/adopters:
               FORKS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                 "https://api.github.com/repos/$GITHUB_REPOSITORY/forks?sort=newest&per_page=10" \
                 | head -c 2000)

          Issue creation: rare — only if a discovered repo has an immediately adoptable
          pattern. Mostly this posture feeds the Watch List for future PATTERN HUNTs.

          ## Posture: SYNTHESIS
          Mindset: "What patterns have emerged across runs?"

          1. Read state/research_log.md entries from the last 7 days
          2. Read the posture history from the Previous Evolve Run Summary
          3. Look for convergent signals:
             - Same pattern noted in 2+ sources across different runs
             - A Watch List source that keeps showing activity
             - A finding noted in an earlier run that now has more supporting evidence
             - Human issues + research findings pointing in the same direction
          4. Execute time-gated steps that are due:
             - Hour 06 UTC (check with `date -u +%H`): growth metrics and adoption tracking
               ```bash
               REPO_STATS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                 "https://api.github.com/repos/$GITHUB_REPOSITORY")
               STARS=$(echo "$REPO_STATS" | grep -o '"stargazers_count":[0-9]*' | cut -d: -f2)
               FORKS_COUNT=$(echo "$REPO_STATS" | grep -o '"forks_count":[0-9]*' | cut -d: -f2)
               TRAFFIC=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                 "https://api.github.com/repos/$GITHUB_REPOSITORY/traffic/views")
               ```
               Write metrics to state/growth_metrics.md. Log to research_log.md.
               Also check for adopters/forks and update state/adopters.md.
             - Hour 12 UTC: SEO & discoverability
               Check README.md accuracy, repo topics, meta tags, robots.txt.
               Only change what's genuinely out of date.
             - Every 7 days (check "Last recheck" in evolve_config.md): config re-check
               Scan for new dependency files, frameworks, deploy configs.
               If significant change: create issue. If not: update recheck date.
             - Scaffold version check:
               ```bash
               LATEST=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                 "https://api.github.com/repos/verkyyi/tokenman/releases/latest" \
                 | grep -o '"tag_name":"[^"]*"' | cut -d'"' -f4)
               ```
               If new version available and no existing issue: create upgrade issue.
          5. Human intent analysis:
             Read state/learned_intents.md. Query recent human issues:
             ```bash
             SINCE=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)
             HUMAN_ISSUES=$(gh issue list --state all --json number,title,author,labels,createdAt \
               --jq "[.[] | select(.author.login != \"github-actions[bot]\" and .createdAt >= \"$SINCE\")]")
             ```
             Categorize intents (EXPAND_SOURCES, IMPROVE_QUALITY, ADD_CAPABILITY,
             FIX_PROCESS, GROW_REACH). Append to state/learned_intents.md.
          6. Create issues backed by accumulated evidence from steps 1-5.

          Issue creation: multi-run observations become issues. Higher confidence
          because backed by accumulated evidence, not a single SHA change.

          ## Source Management

          You fully own state/research_sources.md. Rules:
          - Add freely: any repo discovered during HORIZON SCAN or cross-references
          - New additions go to Watch List first (3+ observations over 7+ days before promotion)
          - Promote Watch → Active when: consistent activity + relevant patterns found
          - Drop when: 4+ weeks inactive, OR 5+ deep-dives with 0 pattern hits
          - Never drop: anthropics/claude-code (runtime dependency)
          - Target: 8-15 Active sources, 5-10 Watch List
          - Always record a reason when promoting or dropping
          - Non-GitHub sources (blogs, docs) use URL as heading with a "Fetch:" field
          - Drop unreachable non-GitHub sources after 3 consecutive failed fetches
          - If research_sources.md doesn't exist, seed it from the Research Sources
            section of the Evolve Config below

          ## Issue Creation

          Before creating any issue:
          1. Dedup: `gh issue list --state all --limit 100 --json title,labels \
               -q '[.[] | select(.labels[].name == "evolve-finding" or .labels[].name == "pipeline-fix")] | .[].title'`
          2. If a similar issue already exists, skip

          Issue framing:
          - Title: "[evolve] Adopt X pattern from Y" or "[pipeline] Fix X"
          - Body MUST include: ## Source, ## Pattern, ## Proposed Change, ## Evidence
          - Labels: evolve-finding (research), pipeline-fix (pipeline),
            intent-driven (human intent) + project:$(echo $GITHUB_REPOSITORY | cut -d/ -f2)
          - Save issue number: `echo "$ISSUE_NUM" >> .new_issues.txt`

          Maximum 3 issues per run (any type). Quality over quantity.

          ## Logging (REQUIRED — every run, every posture)

          1. Append to state/agent_log.md (one structured line):
             TIMESTAMP | evolve.yml | POSTURE_NAME | deep:N scan:N issues:N findings:N | narrative summary

          2. Append to state/research_log.md (one line per finding):
             TIMESTAMP | source-name | finding summary | action taken

          3. Write state/last_evolve_summary.md (overwrite):
             ```
             # Last Evolve Summary
             Timestamp: YYYY-MM-DDTHH:MM:SSZ
             Main HEAD: <sha from git rev-parse HEAD>
             Posture: POSTURE_NAME (reason for choice)
             Posture history: [last 8 postures as array]
             Runs since each:
               PATTERN_HUNT: N
               PIPELINE_WATCH: N
               HORIZON_SCAN: N
               SYNTHESIS: N
             Open issues: #N, #M, ...

             ## Source Digests
             source/name: <latest sha> | last-deep: ISO_TIMESTAMP | one-line summary

             ## Findings This Run
             - finding 1
             - finding 2 (or "No findings this run")
             N issues created.
             ```

          4. Update state/research_sources.md with any changes
             (new Watch List entries, updated stats, promotions, drops)

          5. Write brief session summary to state/project_state.md

          ## Rules
          - You CANNOT promote your own autonomy
          - You CANNOT modify workflow YAML directly
          - You MUST check for duplicates before creating issues
          - You MUST log every run to agent_log.md with the structured format above
          - You MUST update last_evolve_summary.md every run (even if nothing changed)
          - You MUST cycle through all 4 postures within every 8 runs
          - Maximum THREE issues per run — quality over quantity
          - When reading research sources, look for ADOPTABLE PATTERNS,
            not just version bumps. Ask "What can we learn?" not "What changed?"

          ## Previous Evolve Run Summary
          $(cat state/last_evolve_summary.md 2>/dev/null || echo "No previous run summary available — this is the first posture-based run. Pick PATTERN_HUNT. Set all counters to 8.")

          ## Research Sources (Claude-managed — you own this file)
          $(cat state/research_sources.md 2>/dev/null || echo "No sources file — seed from evolve_config.md Research Sources section.")

          ## Context
          $(cat $(grep '^CLAUDE.md:' state/evolve_config.md | cut -d' ' -f2) 2>/dev/null || cat CLAUDE.md)

          ## Current State
          $(cat state/project_state.md)

          ## Recent Agent Log (last 20 lines)
          $(tail -20 state/agent_log.md)

          ## Recent Research Log (last 15 lines)
          $(tail -15 state/research_log.md)

          ## Failure Log
          $(grep "^# [0-9]" CLAUDE.md | tail -20)

          ## Learned Rules (from human feedback — MUST follow these)
          $(cat state/learned_rules.md)

          ## Evolve Config (project settings)
          $(cat state/evolve_config.md)
          PROMPT
```

- [ ] **Step 2: Verify YAML syntax**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/evolve.yml'))" && echo "YAML valid"`
Expected: "YAML valid"

- [ ] **Step 3: Verify heredoc closes properly**

Run: `grep -c "^          PROMPT" .github/workflows/evolve.yml`
Expected: 1 (exactly one PROMPT delimiter closing the heredoc)

- [ ] **Step 4: Verify prompt size is reasonable**

Run: `sed -n '/cat > \/tmp\/prompt.txt/,/^          PROMPT$/p' .github/workflows/evolve.yml | wc -l`
Expected: ~250-300 lines (down from ~410, more focused)

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/evolve.yml
git commit -m "feat(evolve): replace step-by-step prompt with posture-based research

Replace the ~400-line sequential checklist (Steps 1-5, 2a-2h) with a
posture-based self-directing research system. 4 postures rotate:
PATTERN HUNT (deep-dive sources for adoptable patterns),
PIPELINE WATCH (failure analysis), HORIZON SCAN (discover new repos),
SYNTHESIS (cross-run pattern detection + time-gated checks).

Key changes:
- Identity: 'researcher with judgment' not 'checklist executor'
- Sources: Claude reads/manages research_sources.md, not config
- Depth: PATTERN HUNT reads actual diffs, not just SHAs
- Exploration: HORIZON SCAN discovers new repos via trending/cross-refs
- Evidence: SYNTHESIS creates issues from multi-run observations
- Logging: structured posture/deep/scan/issues/findings per run

Removes: Incremental Analysis Rules, Lightweight Mode Gate,
'iterate ALL sources every run', 'IMPORTANT CONFIG RULES' block.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Update usage logging to extract posture

**Files:**
- Modify: `.github/workflows/evolve.yml` — the "Log usage metrics" step (find by step name, not line number — lines shift after Task 2)

Add posture and issue count extraction from last_evolve_summary.md to the usage log line.

- [ ] **Step 1: Add posture/issues extraction to the usage logging step**

In the "Log usage metrics" step, after the existing `COST=...` line and before the `mkdir -p state` line, add:

```bash
          # Extract posture and issues from evolve summary
          POSTURE=$(grep -oP 'Posture: \K\w+' state/last_evolve_summary.md 2>/dev/null || echo "unknown")
          ISSUES_CREATED=$(grep -oP '(\d+) issues created' state/last_evolve_summary.md 2>/dev/null | grep -oP '\d+' || echo "0")
```

Then update the `echo` line that writes to usage_log.md from:
```bash
          echo "${TIMESTAMP} | evolve | model:${MODEL} | in:${INPUT} | out:${OUTPUT} | turns:${TURNS} | cost:${COST}" >> state/usage_log.md
```
to:
```bash
          echo "${TIMESTAMP} | evolve | model:${MODEL} | in:${INPUT} | out:${OUTPUT} | turns:${TURNS} | cost:${COST} | posture:${POSTURE} | issues:${ISSUES_CREATED}" >> state/usage_log.md
```

- [ ] **Step 2: Verify YAML still valid**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/evolve.yml'))" && echo "YAML valid"`
Expected: "YAML valid"

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/evolve.yml
git commit -m "feat(evolve): add posture and issues to usage_log.md

Extract posture name and issue count from last_evolve_summary.md
after Claude runs. Appends posture:X and issues:N fields to the
usage log line for efficiency tracking.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Clean up evolve_config.md

**Files:**
- Modify: `state/evolve_config.md` (remove Research Sources and Search Queries sections)

Claude now owns sources via research_sources.md. The config keeps build, stack, workflow fit, and user answers.

- [ ] **Step 1: Remove the Research Sources and Search Queries sections**

Remove the `## Research Sources` section (lines listing the 12 repos) and the `## Search Queries` section from `state/evolve_config.md`. Keep everything else: header, Repo Profile, Build, Workflow Fit, User Answers, Project.

The file should look like:

```markdown
# Evolve Config
# Generated by onboarding CLI session. Human edits welcome.
# Delete this file to re-trigger onboarding.
# Version: 1
# Last recheck: 2026-03-22

## Repo Profile
Stack: Node.js, Astro, TypeScript
Purpose: Self-evolving scaffold template — the repo IS the system
Maturity: Active (100+ commits)

## Build
install: npm ci
build: npm run build
test: npm run build
e2e-setup: npx playwright install --with-deps chromium
e2e: npx playwright test
deploy: GitHub Pages via GitHub Actions

## Workflow Fit
evolve: HIGH
triage: HIGH
coder: HIGH
reviewer: HIGH
watcher: HIGH
deploy: HIGH
growth: HIGH
feedback-learner: HIGH
analyze: HIGH
discover: SKIP — single-project
claude-task: HIGH

## User Answers
Deploy: GitHub Pages via deploy.yml
Tests: npm run build (Astro build validates) + Playwright E2E
Public: Yes — open-source template
Bypass permissions confirmed: Yes

## Project
CLAUDE.md: ./CLAUDE.md
```

- [ ] **Step 2: Verify config still has required fields**

Run: `grep -c "^## " state/evolve_config.md`
Expected: 5 sections (Repo Profile, Build, Workflow Fit, User Answers, Project)

Run: `grep "CLAUDE.md:" state/evolve_config.md`
Expected: `CLAUDE.md: ./CLAUDE.md` (prompt reads this to find CLAUDE.md path)

- [ ] **Step 3: Commit**

```bash
git add state/evolve_config.md
git commit -m "chore(config): move Research Sources to research_sources.md

Source list is now Claude-managed in state/research_sources.md with
per-source purpose annotations and stats. Config retains build,
stack, workflow fit, and user answers.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Create the PR

**Files:** None (all changes already committed)

This is a workflow YAML change, so per CLAUDE.md autonomy rules it requires a `needs-review` PR.

- [ ] **Step 1: Create a feature branch and push**

```bash
git checkout -b feat/evolve-research-postures
git push -u origin feat/evolve-research-postures
```

Note: If already on a branch, skip checkout. If commits are already on the branch, just push.

- [ ] **Step 2: Create the PR**

```bash
gh pr create --title "feat(evolve): posture-based self-directing research" --body "$(cat <<'EOF'
## Summary

- Replace the ~400-line step-by-step evolve prompt with a posture-based self-directing research system
- Add `state/research_sources.md` — Claude-managed source inventory with purpose annotations, pattern hit stats, and Watch/Dropped lists
- 4 research postures rotate every run: **PATTERN HUNT** (deep-dive for adoptable patterns), **PIPELINE WATCH** (failure analysis), **HORIZON SCAN** (discover new repos), **SYNTHESIS** (cross-run pattern detection + time-gated checks)
- Structured logging: `posture | deep:N scan:N issues:N findings:N` in agent_log, posture/issues in usage_log
- Move Research Sources from evolve_config.md to research_sources.md (Claude owns it now)

## Why

After the config-driven refactor, evolve dropped from 53% research issue creation rate (8 issues in 15 runs) to 0% (0 issues in 23+ runs). The agent became a mechanical SHA checker. This redesign restores research depth via PATTERN HUNT, adds source exploration via HORIZON SCAN, and improves issue quality via SYNTHESIS (multi-run evidence).

## Test plan

- [ ] First run auto-detects no posture history, picks PATTERN_HUNT, initializes counters
- [ ] PATTERN_HUNT reads actual commit diffs (not just SHAs) and looks for adoptable patterns
- [ ] Posture rotation visible in last_evolve_summary.md after 8+ runs
- [ ] HORIZON_SCAN adds sources to Watch List within 24h
- [ ] Pipeline health detection still works (PIPELINE_WATCH)
- [ ] usage_log.md lines include posture:X and issues:N fields
- [ ] No regression in state file commits or triage triggers

## Spec

`docs/superpowers/specs/2026-03-23-evolve-research-postures-design.md`

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" --label "needs-review"
```

- [ ] **Step 3: Verify PR was created**

Run: `gh pr view --json url,state -q '.url'`
Expected: PR URL displayed

---

### Task 6: Post-merge monitoring checklist

**Files:** None — this is observation-only after the PR merges

After the PR is merged, monitor the first 8 evolve runs (about 2 hours at 15-min intervals) to validate the success criteria from the spec.

- [ ] **Step 1: Check first run picked PATTERN_HUNT**

Run (after ~15 min): `head -10 state/last_evolve_summary.md`
Expected: `Posture: PATTERN_HUNT` with counters initialized

- [ ] **Step 2: Check posture rotation after 8 runs (~2 hours)**

Run: `grep "Posture history" state/last_evolve_summary.md`
Expected: All 4 posture types appear in the array

- [ ] **Step 3: Check research_sources.md is being updated**

Run: `grep "Last deep:" state/research_sources.md | head -5`
Expected: Some sources have updated "Last deep" timestamps

- [ ] **Step 4: Check structured logging is working**

Run: `tail -5 state/agent_log.md`
Expected: Lines contain `deep:N scan:N issues:N findings:N` format

Run: `tail -3 state/usage_log.md | grep evolve`
Expected: Lines contain `posture:X | issues:N` fields

- [ ] **Step 5: Check Watch List populated (after first HORIZON_SCAN)**

Run: `sed -n '/^## Watch List/,/^## /p' state/research_sources.md`
Expected: At least one source under Watch List

- [ ] **Step 6: Verify issue creation resumed (after 24h)**

Run: `gh issue list --state all --label evolve-finding --json createdAt,title -q '.[] | select(.createdAt > "MERGE_DATE") | .title'`
Expected: At least 1 new evolve-finding issue
