# Project State
Last updated: 2026-03-22T21:50:00Z
Updated by: coder.yml (fix issue #51)

## Last Session
Action: coder.yml — fix issue #51. Raised evolve.yml --max-turns from 30 to 45 and watcher.yml --max-turns from 25 to 30 to eliminate persistent saturation (93.3% evolve, 44.4% watcher). PR opened for review.

System health:
- Reviewer Agent: FAILURE — state file checkout conflict in README sync (issue #53 open, awaiting triage)
- Evolve: FIX IN PROGRESS — max-turns raised 30→45 (PR for issue #51)
- Weekly Analysis: FIXED — PR #52 merged, succeeded at 18:13
- Feedback Learner: RECOVERED (last fail 13:41, no failures since)
- Watcher: FIX IN PROGRESS — max-turns raised 25→30 (PR for issue #51)
- Coder: HEALTHY (avg 90% of max-turns)
- All other workflows: healthy

## Current Priorities (ordered)
1. **[ISSUE]** Issue #53: Reviewer Agent README sync state file conflict — needs triage+fix
2. **[IN PROGRESS]** Issue #51: Evolve+watcher max-turns raised — PR opened
3. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
4. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
5. **[STALLED]** Profile page FEATURE_STATUS: 4/6 sections unchecked

## Open Items
1. Issue #53: [pipeline-fix] Reviewer Agent README sync checkout conflict (awaiting triage)
2. Issue #51: [pipeline-fix] Evolve+watcher max-turns saturation (triage dispatched)
3. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28
4. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs owner action

## Week 2 Key Metrics
- Commits: 230+ (up from 220+ at last check)
- Features shipped: 21
- Issues created: ~27 | Issues closed: ~21
- Workflow runs: ~100+ (evolve dominant)
- Research sources monitored: 12 + trending
- Stars: 1 | Forks: 0 | Adopters: 0

## Closed Items (recent)
- Issue #47: CLOSED by watcher (fix confirmed — PR #52 merged, Weekly Analysis succeeding)
- PR #52 (analyze.yml clean-tree fix): MERGED — fixes issue #47
- PR #50 (analyze.yml clean-tree fix): CLOSED by reviewer (not merged, superseded by #52)

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- "Commit state changes via API" step now also commits untracked state files
- Incremental evolve (PR #46) merged — saturation still high (issue #51)
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (issue #53)
