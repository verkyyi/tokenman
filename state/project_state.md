# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-21T22:42:00Z
Updated by: coder.yml

## Last Session
Action: coder.yml — fix issue #9 (feedback entry point on public website)
Done:
- Added "Submit Feedback →" link to Getting Started section in src/pages/index.astro
- Link points to https://github.com/verkyyi/agentfolio/issues/new (new tab, noopener noreferrer)
- Styled as .cta-link — matches existing cosmic design system
- Build passing (npm run build)
- Opened PR for issue #9

In progress: none

Next agent: Reviewer for PR (issue #9)

## Open Items
- Issue #8: [pipeline] Upgrade Node.js 20 actions before June 2026 deadline
- Issue open: [evolve] Adopt structured review tables in skill output (gstack v0.9.7.0 pattern)
- Issue open: [evolve] Add adversarial self-review step to evolve.yml agent output
- apps/profile content not yet populated — discover.yml or manual issue needed

## Metrics Snapshot
(empty — analyze.yml will populate after first weekly run)

## Notes for Next Agent
The scaffold is healthy. No regressions or failures logged.
- Codex blog live at /codex, seed article at /codex/harness-engineering-intro
- adversarial-review.md skill created and merged (PR #6)
- Codex blog added and merged (PR #7)
- gstack v0.9.8.0 pre-merge readiness gate pattern noted — potential future skill
- Node.js 20 deprecation: all workflows using actions/checkout@v4 and actions/deploy-pages@v4 — deadline June 2, 2026
