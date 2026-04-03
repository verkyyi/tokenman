# Scaffold — Feature Status

## Core Harness
- [x] State management (project_state.md, agent_log.md)
- [x] Issue-driven event bus (triage → coder → reviewer)
- [x] Deploy pipeline (Astro build → GitHub Pages)
- [x] Manual dev channel (claude-task.yml)
- [x] Dynamic APP_NAME resolution across workflows
- [x] Self-evolution loop (evolve.yml)
- [x] Weekly improvement analysis (analyze.yml)
- [x] Project discovery (discover.yml)
- [x] Research log and external knowledge fetching
- [x] Repo profile page

## Codex Blog
- [x] content/codex collection registered in src/content.config.ts (Zod schema: title, date, description, tags)
- [x] Seed article: src/content/codex/harness-engineering-intro.md
- [x] /codex index page: src/pages/codex/index.astro (post listing)
- [x] /codex/[slug] page: src/pages/codex/[slug].astro (individual post renderer)
- [x] Codex section linked from index.astro

## Profile Page
- [x] Feedback link in Getting Started section (opens GitHub Issues new-issue page)
- [x] Mobile-friendly: fixed horizontal overflow on iOS Safari (closes #14)
- [x] Auto-redeploy on state/skills changes — deploy.yml path trigger includes state/** and skills/** (closes #29)

## Skills
- [x] harness.md
- [x] content.md
- [x] frontend.md
- [x] github-workflows.md
- [x] feedback-intake.md
- [x] seo.md
- [x] Skills updated for self-evolving architecture
- [x] adversarial-review.md — risk-scaled self-check protocol for evolve.yml Step 5
- [x] pre-merge gate — CI + risk-assessment + blocking-issue checks added to adversarial-review.md; referenced from harness.md reviewer guidance (closes #16)
- [x] structured findings table — Trigger/Why/Status/Findings table added to adversarial-review.md; machine-readable output for non-trivial reviews; pattern note for future skill files; referenced from harness.md (closes #5)
- [x] SKILL.md quality standard — all 8 skill files upgraded with allowed-tools frontmatter, "When NOT to Use", "Rationalizations to Reject", and anti-pattern examples (closes #68)
- [x] SKILL.md metadata added to all 8 skills (version, author, tags fields) (closes #66)
- [x] 4 standalone skill packages: adversarial-review, session-protocol, harness, feedback-intake
- [x] session-protocol extracted from CLAUDE.md into standalone skill
- [x] skills/README.md — catalog with installation instructions

## Watcher Improvements
- [x] Pipeline outcome health checks (responsibility #7) — triage comment detection, coder handoff detection, reviewer silent-failure detection; corrective action limit raised 3→5 (closes #23)

## Claude CLI Optimization (closes #26)
- [x] Tier 1 (coder, claude-task): claude-opus-4-6 + effort max + fallback sonnet + bypassPermissions; coder max-turns 30→40
- [x] Tier 2 (reviewer, evolve, triage): claude-sonnet-4-6 + effort high + fallback haiku + bypassPermissions; reviewer max-turns 15→30, triage 25→30
- [x] Tier 3 (watcher, growth, analyze, discover, feedback-learner): claude-haiku-4-5-20251001 + effort medium + bypassPermissions; analyze/discover 20→25, feedback-learner 10→25

## Token Utilization Feedback Loop (closes #28)
- [x] state/usage_log.md created (append-only, 7-day rolling window)
- [x] Phase 1 pilot: coder.yml, watcher.yml, evolve.yml instrumented with --output-format json + usage logging
- [x] Phase 2: watcher responsibility #8 — token utilization analysis (skips if <20 data lines; detects under/overutilization; creates max 1 optimization issue per run)
- [x] Phase 3 rollout: reviewer.yml, triage.yml, analyze.yml, claude-task.yml, discover.yml, feedback-learner.yml, growth.yml instrumented
- [x] Maintenance: 7-day rolling truncation via awk date comparison in each logging step
- [x] Workflows without existing state commit (reviewer, triage) given dedicated usage log commit step
- [x] feedback-learner commit step updated to include usage_log.md in both lesson/no-lesson paths

## README Auto-Sync (closes #38)
- [x] skills/readme-sync.md — documents sync protocol and auto-maintained sections
- [x] reviewer.yml post-merge step — deterministic shell sync of workflow count, table, and architecture section after structural changes
- [x] README.md inconsistencies fixed — "nine"/"ten" → "eleven", discover.yml added to table
- [x] Existing evolve.yml daily SEO check preserved as safety net (no changes needed)

## Hooks-Based Guardrail Enforcement (closes #67)
- [x] state/guardrail_policy.json — deny-rule policy (destructive rm, force push, secrets, workflow YAML, autonomy promotion)
- [x] .claude/hooks/guard.sh — PreToolUse hook script, fail-closed, reads policy and blocks matching tool calls
- [x] .claude/settings.json — PreToolUse hook registered alongside existing SessionEnd hook

## Script Testing (closes #139)
- [x] BATS-Core installed as npm dev dependency
- [x] tests/commit-state.bats — 7 tests (no-args, missing file, missing env, PUT with/without sha, retry logic, graceful failure)
- [x] tests/archive-research-log.bats — 7 tests (missing file, <=100 skip, >100 archive, create archive, header preservation, append mode)
- [x] tests/build-preamble.bats — 8 tests (no-tier, T1-T4 content, missing files, output-to-file)
- [x] npm run test:scripts script added to package.json

## Human-Pipeline Interaction (closes #33)
- [x] feedback-learner.yml: PR close-without-merge trigger + rejection handling (re-adds agent-ready, re-triggers coder)
- [x] feedback-learner.yml: merged PR close skipped (reviewer already handled)
- [x] coder.yml: issue comments included in coder prompt for re-trigger context
- [x] evolve.yml: Step 2f Human Intent Analysis (categorize human issues, track in learned_intents.md, create intent-driven issues)
- [x] README.md: "Interacting with the Pipeline" section documenting human interaction protocol
- [x] state/learned_intents.md: created as append-only placeholder for intent tracking
