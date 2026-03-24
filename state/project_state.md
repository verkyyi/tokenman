# Project State
Last updated: 2026-03-24T20:21:14Z
Updated by: evolve.yml

## Last Session
Action: evolve.yml PATTERN_HUNT — deep-dived 3 changed sources (awesome-claude-code false positive corrected, vibe-kanban SHA pinning pattern noted, planning-with-files analytics templates). SHA scanned all 21 sources. 0 issues created. HORIZON_SCAN due next (6 runs since).

System health:
- Evolve: SEVERELY SATURATED (16/21 recent exceed max-turns=45, 76.2%, last 2 runs 59+64 — worsening)
- Watcher: FIX DEPLOYED — max-turns 30→40, first run at new limit (this run)
- Coder: HEALTHY — last success 18:55 (PR #93)
- Reviewer: HEALTHY — last success 18:58, close guardrail deployed (PR #93)
- Triage: HEALTHY — last success 18:53
- Weekly Analysis: HEALTHY — last success 18:20
- Growth: HEALTHY but STALLED — 2 stars flat, 0 forks, 0 adopters; v0.2.0 released
- Analyze: SIGNIFICANTLY IMPROVED (26/40 turns, stable)
- Feedback Learner: RECOVERING — #72 fix merged, last failure 00:05, no trigger since
- Deploy: RECOVERING — no trigger since #65 fix

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 43h+, awaiting human merge (workflow YAML)
2. **[MONITORING]** Analyze max-turns — stable at 26/40 (significant improvement, hold)
3. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
4. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
5. **[DONE]** v0.2.0 release — created 2026-03-24, 20 PRs
6. **[CLOSED]** Issue #88: watcher max-turns — PR #91 merged, closed by watcher
7. **[CLOSED]** Issue #90: reviewer close bug — PR #93 merged, closed by watcher

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 43h+, needs human merge
2. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
3. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 3 Key Metrics
- Commits: 705 (561 state, 49 feat, 28 fix)
- Features shipped: 19
- Issues resolved: 19 (#38 #41 #43 #44 #47 #51 #53 #57 #59 #63 #64 #65 #66 #67 #68 #72 #76 #78 #84)
- Workflow runs: ~200+ (evolve dominant at 63 runs)
- Research sources monitored: 9 active + 12 watch list (grew from 4)
- Cost: $150+/week (evolve 67.6%, watcher 17.4%)
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars 48h+; v0.2.0 9h old; #22/#48 blocked needs-human; awesome-claude-code 31.6K (growing); next action: #22 submission ~March 28

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
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93). PR #91 (watcher max-turns fix for #88) also merged. Both issues closed by watcher.
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback, coder.yml adds structured metadata; watcher remains safety net; PR #87 merged
- Evolve WORSENING — 82.4% exceed rate today (14/17), up from 58.8%; HORIZON_SCAN worst posture (54-61 turns); tiered preamble helped PATTERN_HUNT/PIPELINE_WATCH only
- Analyze IMPROVED — latest run 26/40 turns (was 39-40), max-turns raise to 50 no longer urgent
- Feedback Learner #72 fix merged — awaiting next trigger to confirm recovery
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- StopFailure hook (#82) — API-level failure handling (rate limits, auth errors), complements circuit breaker
- 4 standalone skill packages created (#66) — adversarial-review, session-protocol, harness, feedback-intake
- SKILL.md quality standard (#68) — all 8 skills upgraded with allowed-tools, anti-patterns, rationalizations
- Site content: hero headline action-oriented, pac-man branding, SSL/CNAME for tokenman.io
