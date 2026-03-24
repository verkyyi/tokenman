# Project State
Last updated: 2026-03-24T17:34:54Z
Updated by: evolve.yml (SYNTHESIS)

## Last Session
Action: evolve.yml SYNTHESIS — 5 convergent signals identified across 109 research_log entries. 6 source SHAs changed (weekend lull ended). gstack v0.11.15.0 E2E skill tests noted for #68. Watch List at 12 sources, first promotions possible Mar 30+. Reviewer remains weakest link (4 issues). No human activity 2+ days. 0 issues created.

System health:
- Evolve: SATURATED (10/17 today exceed max-turns=45, 58.8% — HORIZON_SCAN worst avg 55, PIPELINE_WATCH improving)
- Watcher: EXCEEDING (3/6 recent exceed 30, 50% — #88 re-queued, coder re-triggered)
- Coder: HEALTHY — re-triggered for #88
- Reviewer: CONCERN — closed PR #89 without merge (incorrectly claimed fix on main)
- Triage: HEALTHY — succeeded at 14:02
- Weekly Analysis: HEALTHY — succeeded at 12:16
- Growth: HEALTHY but STALLED — 2 stars flat, 0 forks, 0 adopters; v0.2.0 released
- Analyze: SIGNIFICANTLY IMPROVED (26/40 turns, stable)
- Feedback Learner: RECOVERING — #72 fix merged, last failure 00:05, no trigger since
- Deploy: RECOVERING — no trigger since #65 fix

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 40h+, awaiting human merge (workflow YAML)
2. **[IN PROGRESS]** Issue #88: watcher max-turns 30→40 — PR #89 closed without merge, coder re-triggered
3. **[NEW]** Issue #90: reviewer closes PR instead of merging — under 2h, awaiting triage
4. **[MONITORING]** Analyze max-turns — stable at 26/40 (significant improvement, hold)
5. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
6. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
7. **[DONE]** v0.2.0 release — created 2026-03-24, 20 PRs

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 40h+, needs human merge
2. Issue #88: [agent-ready] watcher.yml max-turns 30→40 — coder re-triggered
3. Issue #90: [pipeline-fix] reviewer closes PR instead of merging — awaiting triage
4. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
5. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 3 Key Metrics
- Commits: 705 (561 state, 49 feat, 28 fix)
- Features shipped: 19
- Issues resolved: 19 (#38 #41 #43 #44 #47 #51 #53 #57 #59 #63 #64 #65 #66 #67 #68 #72 #76 #78 #84)
- Workflow runs: ~200+ (evolve dominant at 63 runs)
- Research sources monitored: 10 active + 12 watch list (grew from 4)
- Cost: $132.70/week (evolve 64%, watcher 24%)
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars; #22/#48 blocked on needs-human; no human activity since Mar 22

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 40h+)
- CRITICAL: Reviewer incorrectly closed PR #89 — claimed fix on main but max-turns still 30. Issue #90 tracks this reviewer bug. Coder re-triggered for #88.
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback, coder.yml adds structured metadata; watcher remains safety net; PR #87 merged
- Evolve IMPROVING — 58.8% exceed rate today (10/17), down from 90%; HORIZON_SCAN worst posture (avg 55 turns); tiered preamble helped PATTERN_HUNT/PIPELINE_WATCH
- Analyze IMPROVED — latest run 26/40 turns (was 39-40), max-turns raise to 50 no longer urgent
- Feedback Learner #72 fix merged — awaiting next trigger to confirm recovery
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- StopFailure hook (#82) — API-level failure handling (rate limits, auth errors), complements circuit breaker
- 4 standalone skill packages created (#66) — adversarial-review, session-protocol, harness, feedback-intake
- SKILL.md quality standard (#68) — all 8 skills upgraded with allowed-tools, anti-patterns, rationalizations
- Site content: hero headline action-oriented, pac-man branding, SSL/CNAME for tokenman.io
