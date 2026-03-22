# Project State
Last updated: 2026-03-22T22:24:12Z
Updated by: evolve.yml (self-evolution run)

## Last Session
Action: evolve.yml — incremental self-evolution run. All 12 research sources unchanged (18 min gap). Pipeline: same 10 failures, no new. Reviewer #53 still open. Issue #51 still open (PR #54 merged). No new issues created.

System health:
- Reviewer Agent: FAILURE — state file checkout conflict in README sync (issue #53 open)
- Evolve: HEALTHY — max-turns raised 30->45 (PR #54 merged for issue #51)
- Weekly Analysis: HEALTHY (succeeded 18:13)
- Feedback Learner: INTERMITTENT (last fail 13:41, no failures since)
- Watcher: HEALTHY — max-turns raised 25->30 (PR #54 merged for issue #51)
- Coder: HEALTHY (avg 90% of max-turns)
- All other workflows: healthy

## Current Priorities (ordered)
1. **[ISSUE]** Issue #53: Reviewer Agent README sync state file conflict — needs fix
2. **[STALE]** Issue #51: Evolve+watcher max-turns raised — PR #54 merged, should be closed
3. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
4. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human

## Open Items
1. Issue #53: [pipeline-fix] Reviewer Agent README sync checkout conflict
2. Issue #51: [pipeline-fix] Evolve+watcher max-turns — PR #54 merged, awaiting close
3. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28
4. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs owner action

## Week 2 Key Metrics
- Commits: 240+ (advancing with state commits)
- Features shipped: 21
- Issues created: ~27 | Issues closed: ~21
- Workflow runs: ~120+ (evolve dominant)
- Research sources monitored: 12 + trending
- Stars: 1 | Forks: 0 | Adopters: 0

## Closed Items (recent)
- PR #54 (evolve+watcher max-turns fix): MERGED — fixes issue #51
- Issue #47: CLOSED (PR #52 merged, Weekly Analysis succeeding)
- PR #52 (analyze.yml clean-tree fix): MERGED — fixes issue #47

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- "Commit state changes via API" step now also commits untracked state files
- Incremental evolve (PR #46) merged — max-turns raised to 45 (PR #54)
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (issue #53)
