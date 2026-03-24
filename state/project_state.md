# Project State
Last updated: 2026-03-24T13:37:08Z
Updated by: evolve.yml (PIPELINE_WATCH)

## Last Session
Action: evolve.yml PIPELINE_WATCH — pipeline 100% success (last 30 runs). 10 failures analyzed: all ALREADY-FIXED/FIXED-UNTESTED. Cost: evolve $1.91/run avg ($36.24/19 runs today), HORIZON_SCAN most expensive ($2.23/run). Watcher rising to $1.18/run. 3 SHA changes queued (deer-flow, astro, OpenViking). 0 issues created.

System health:
- Evolve: SEVERELY SATURATED (14/18 recent exceed max-turns=45, 77.8% — HORIZON_SCAN worst at 54-61 turns; per-run cost $1.33-$2.42)
- Watcher: WORSENING (4/8 recent exceed 30, 50% — #88 created to raise limit to 40)
- Coder: HEALTHY — last succeeded at 09:54
- Reviewer: HEALTHY — 6+ consecutive successes since last failure at 02:23
- Triage: HEALTHY — succeeded at 09:52
- Weekly Analysis: HEALTHY — succeeded at 12:16
- Growth: HEALTHY but STALLED — 2 stars flat, 0 forks, 0 adopters; v0.2.0 released
- Analyze: SIGNIFICANTLY IMPROVED (26/40 turns, was 36-40 — max-turns raise may no longer be needed)
- Feedback Learner: RECOVERING — #72 fix merged, 1 failure since (00:05), no trigger since
- Deploy: RECOVERING — no trigger since #65 fix

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 36h+, awaiting human merge (workflow YAML)
2. **[PR OPEN]** Issue #88: Raise watcher.yml max-turns 30→40 — PR opened
3. **[MONITORING]** Analyze max-turns — was 36-40/40, latest run 26/40 (significant improvement, hold off on raise)
4. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
5. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
6. **[DONE]** v0.2.0 release — created 2026-03-24, 20 PRs

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 36h+, needs human merge
2. Issue #88: [pipeline-fix] Watcher max-turns 30→40 — PR opened, awaiting merge
3. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
4. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

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
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 36h+)
- Watcher max-turns raised 30→40 — PR opened for #88, 42.9% of runs were exceeding 30
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback, coder.yml adds structured metadata; watcher remains safety net; PR #87 merged
- Evolve MIXED — 60% exceed rate (6/10), HORIZON_SCAN worst posture (avg 57 turns); tiered preamble helped PATTERN_HUNT/SYNTHESIS but not HORIZON_SCAN
- Analyze IMPROVED — latest run 26/40 turns (was 39-40), max-turns raise to 50 no longer urgent
- Feedback Learner #72 fix merged — awaiting next trigger to confirm recovery
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- StopFailure hook (#82) — API-level failure handling (rate limits, auth errors), complements circuit breaker
- 4 standalone skill packages created (#66) — adversarial-review, session-protocol, harness, feedback-intake
- SKILL.md quality standard (#68) — all 8 skills upgraded with allowed-tools, anti-patterns, rationalizations
- Site content: hero headline action-oriented, pac-man branding, SSL/CNAME for tokenman.io
