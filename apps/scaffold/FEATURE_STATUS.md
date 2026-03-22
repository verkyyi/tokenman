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
