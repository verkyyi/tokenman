# Project State
Last updated: 2026-03-24T05:10:00Z
Updated by: watcher.yml

## Last Session
Action: watcher.yml health check — 1 corrective action (closed #78, PR #81 merged, auto-close missed). All workflows healthy. Feedback Learner RECOVERING (#72 fix merged). Deploy RECOVERING (no trigger since fix). Evolve still severely saturated (structural).

System health:
- Evolve: SEVERELY SATURATED (structural, stable — 87.5% exceed max-turns, haiku fallback at 04:43)
- Watcher: NORMALIZED (healthy)
- Coder: HEALTHY — succeeded at 04:23
- Reviewer: HEALTHY — succeeded at 04:29
- Triage: HEALTHY — succeeded at 04:21
- Weekly Analysis: HEALTHY — succeeded at 00:19
- Growth: HEALTHY — succeeded at 18:16
- Analyze: HEALTHY — succeeded at 00:24 (NEAR-LIMIT: 39/40 turns)
- Feedback Learner: RECOVERING — #72 fix merged at 03:35, no run since (awaiting next trigger)
- Deploy: RECOVERING — no run since #65 fix (no site-content push since)

## Current Priorities (ordered)
1. **[PR]** PR #55: fix reviewer.yml state reset — APPROVED 29h+, awaiting human merge (workflow YAML)
2. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
3. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 29h+, needs human merge
2. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
3. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 2 Key Metrics
- Commits: 300+ (advancing with state commits)
- Features shipped: 21
- Issues created: ~32 | Issues closed: ~30
- Workflow runs: ~200+ (evolve dominant)
- Research sources monitored: 10 active + 10 watch list
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: +1 star since v0.1.0 release (now flat at 2); discussion #49 0 engagement; distribution issues #22/#48 blocked on needs-human; no action taken — next action when features accumulate for v0.2.0

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- "Commit state changes via API" step now also commits untracked state files
- Evolve lightweight mode gate now deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (issue #53 closed, PR #55 APPROVED — awaiting human merge 29h+)
- analyze.yml stale branch bug fixed (issue #59 closed, fix deployed — confirmed working)
- GitHub auto-close continues to miss: #63, #64, #66, #67, #68, #78 all closed manually by watcher
- Evolve severely saturated — structural, stable (87.5% exceed max-turns, haiku fallback recurring)
- Feedback Learner #72 fix merged at 03:35 — awaiting next trigger to confirm recovery
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Site content updated: hero headline now action-oriented, pac-man branding, broken logo removed, SSL/CNAME for tokenman.io
