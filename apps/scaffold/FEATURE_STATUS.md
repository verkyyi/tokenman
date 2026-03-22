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

## Watcher Improvements
- [x] Pipeline outcome health checks (responsibility #7) — triage comment detection, coder handoff detection, reviewer silent-failure detection; corrective action limit raised 3→5 (closes #23)

## Claude CLI Optimization (closes #26)
- [x] Tier 1 (coder, claude-task): claude-opus-4-6 + effort max + fallback sonnet + bypassPermissions; coder max-turns 30→40
- [x] Tier 2 (reviewer, evolve, triage): claude-sonnet-4-6 + effort high + fallback haiku + bypassPermissions; reviewer max-turns 15→30, triage 25→30
- [x] Tier 3 (watcher, growth, analyze, discover, feedback-learner): claude-haiku-4-5-20251001 + effort medium + bypassPermissions; analyze/discover 20→25, feedback-learner 10→25
