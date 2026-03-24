# Project State
Last updated: 2026-03-24T02:20:00Z
Updated by: watcher.yml

## Last Session
Action: watcher.yml health check — 4 corrective actions: closed #66/#67/#68 (PRs merged, GitHub auto-close missed), re-triggered reviewer for PR #71 (open >2h, 0 reviews). #72 approaching 2h without triage (1h36m, likely-agent-fixable). #78 and #76 under 2h threshold.

System health:
- Evolve: SEVERELY SATURATED (structural, 9/10 last exceed max-turns=45, 90%, stable)
- Watcher: NORMALIZED (healthy, all under 30)
- Coder: HEALTHY — succeeded at 00:57
- Reviewer: HEALTHY — succeeded at 01:05 (re-triggered for PR #71)
- Triage: HEALTHY — succeeded at 00:55
- Weekly Analysis: HEALTHY — succeeded at 00:19
- Growth: HEALTHY — succeeded at 18:16
- Analyze: HEALTHY — succeeded at 00:24
- Feedback Learner: FAILING — script injection in workflow YAML (#72, likely-agent-fixable, awaiting triage)
- Deploy: RECOVERING — no run since #65 fix (no site-content push since)

## Current Priorities (ordered)
1. **[FIX]** Issue #72: Feedback Learner script injection — likely-agent-fixable, approaching 2h without triage
2. **[PR]** PR #71: unified label registry — needs-review, reviewer re-triggered by watcher
3. **[PR]** PR #55: fix reviewer.yml state reset — APPROVED 26h+, awaiting human merge (workflow YAML)
4. **[NEW]** Issue #78: State file compression — evolve-finding, <1h old, awaiting triage
5. **[NEW]** Issue #76: Circuit breaker pattern — evolve-finding, ~1h old, awaiting triage
6. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
7. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28

## Open Items
1. Issue #72: [pipeline-fix] Feedback Learner script injection — likely-agent-fixable, no triage comment (1h36m)
2. PR #71: [needs-review] unified label registry — reviewer re-triggered (0 reviews, >2h open)
3. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 26h+, needs human merge
4. Issue #78: [evolve-finding] state file compression — new, awaiting triage
5. Issue #76: [evolve-finding] circuit breaker pattern — new, awaiting triage
6. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
7. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28
8. Issue #66: CLOSED by watcher (PR #77 merged)
9. Issue #67: CLOSED by watcher (PR #73 merged)
10. Issue #68: CLOSED by watcher (PR #74 merged)

## Week 2 Key Metrics
- Commits: 300+ (advancing with state commits)
- Features shipped: 21
- Issues created: ~32 | Issues closed: ~30
- Workflow runs: ~200+ (evolve dominant)
- Research sources monitored: 10 active + 10 watch list
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: +1 star since v0.1.0 release (now flat at 2); discussion #49 has 0 engagement after 39h; distribution issues #22/#48 blocked on needs-human; no action taken — next action when features accumulate for v0.2.0

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- "Commit state changes via API" step now also commits untracked state files
- Evolve lightweight mode gate now deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (issue #53 closed, PR #55 APPROVED — awaiting human merge)
- PR #55 approved by reviewer — human merge needed for workflow YAML change (24h+ pending)
- analyze.yml stale branch bug fixed (issue #59 closed, fix deployed — Weekly Analysis succeeded at 18:16, fully confirmed)
- #63 and #64 fully processed: evolve→triage→coder→PR→reviewer→merge. Closed by watcher (GitHub auto-close missed).
- #66, #67, #68 fully processed: evolve→triage→coder→PR→reviewer→merge. Closed by watcher (GitHub auto-close missed again — recurring pattern).
- Evolve severely saturated — structural, stable (90% exceed max-turns)
- Watcher NORMALIZED — healthy (all under 30 turns)
- Feedback Learner FAILING — script injection in workflow YAML (#72 created, likely-agent-fixable added, approaching 2h without triage)
- PR #71 had 0 reviews after >2h — reviewer re-triggered by watcher
- Site content updated: hero headline now action-oriented, pac-man branding, broken logo removed, SSL/CNAME for tokenman.io
- README minor inaccuracy: says "10 external sources across rotating tiers" — actually 12 sources, all checked every run (no rotation). Not issueworthy given existing #38 coverage.
