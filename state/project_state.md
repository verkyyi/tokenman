# Project State
Last updated: 2026-03-22T19:09:16Z
Updated by: evolve.yml (self-evolution run)

## Last Session
Action: evolve.yml self-evolution — incremental research, all sources checked, 1 new finding (gstack v0.10.1.0)

System health:
- Weekly Analysis (analyze.yml): RESOLVED — succeeded at 18:07, issue #47 + PR #50 tracking fix
- Evolve: MONITORING post-incremental-merge (PR #46) — first post-merge run succeeded at 18:06, saturation data pending
- Watcher: borderline OVERUTILIZED (37.5% exceed 25, improving trend)
- Feedback Learner: RECOVERED (last fail 13:41, succeeded 17:29 x2)
- Coder: HEALTHY (0/2 exceed 40, avg 90%)
- All other workflows: healthy

## Current Priorities (ordered)
1. **[MONITOR]** Evolve max-turns saturation post-incremental-merge — if still >70% next week, raise to 40
2. **[PR-REVIEW]** PR #50 (analyze.yml clean-tree fix) — needs reviewer trigger
3. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day repo age cooldown expires ~March 28
4. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
5. **[STALLED]** Profile page FEATURE_STATUS: 4/6 sections unchecked (live stats, evolution timeline, capabilities, architecture) despite landing redesign shipping
6. **[CLEANUP]** Prune inactive research sources (godagoo 7+ weeks, humanlayer 2+ months inactive)

## Open Items
1. PR #50: fix(harness) guard analyze.yml PR step against clean tree — needs review
2. Issue #47: [pipeline-fix] Weekly Analysis clean-tree — PR #50 is the fix
3. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28
4. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs owner action
5. Evolve max-turns optimization (monitoring post-incremental-merge)
6. Profile page sections: live stats, evolution timeline, capabilities inventory, architecture diagram

## Week 2 Key Metrics
- Commits: 220+ (up from 64 at Week 1 midpoint)
- Features shipped: 21
- Issues created: ~25 | Issues closed: ~20
- Workflow runs: ~100+ (evolve dominant at ~20 runs)
- Research sources monitored: 12 + trending
- Stars: 1 | Forks: 0 | Adopters: 0

## Closed Items (recent)
- PRs #19 (anti-sycophancy) + #20 (agentic security): CLOSED by owner (not merged)
- Weekly Analysis 3x failure: RESOLVED (succeeded at 18:07)

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- "Commit state changes via API" step now also commits untracked state files
- Incremental evolve (PR #46) merged — should reduce max-turns saturation
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
