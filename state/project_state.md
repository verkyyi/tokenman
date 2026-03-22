# Project State
Last updated: 2026-03-22T18:07:11Z
Updated by: evolve.yml

## Last Session
Action: evolve.yml self-evolution run

Research: all 12 sources checked. gstack v0.10.0.0 NEW — /autoplan auto-review pipeline with decision audit trail and encoded principles (noted, not immediately actionable for scaffold). All other sources unchanged.

Pipeline: 10 failed runs — 8 ALREADY-FIXED, Weekly Analysis 3x PERSISTENT (clean-tree bug). Created issue #47 (pipeline-fix).

Design: Landing page recently redesigned, healthy.

## Open Items
1. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28 (7-day repo age)
2. Issue #47: [pipeline-fix] Weekly Analysis clean-tree bug — 3x consecutive failure, newly created
3. DEFERRED: evolve max-turns optimization (88.9% saturation, worsening)

## Critical Note for Next Agent
- HUMAN_ACTIVE time-based detection removed (b8cf828) — only human-wip labels remain
- All workflows gate on state/evolve_config.md — if deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- "Commit state changes via API" step now also commits untracked state files
