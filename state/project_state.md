# Project State
Last updated: 2026-03-25T15:41:21Z
Updated by: evolve.yml (PIPELINE_WATCH)

## Last Session
Action: evolve.yml PIPELINE_WATCH — 10 failures analyzed (6 already-fixed, 1 transient, 3 actionable tracked by #108). Coder at 4 consecutive failures (push-rejected on fix/issue-100). Cost ~$75/day (slight improvement). SHA scan: 20/21 sources unchanged, astro changed. 0 issues created.

System health:
- Evolve: IMPROVING — 2/10 (20%) post-fix exceed max-turns 55. Cost concern: $29/day at 16 runs/day.
- Watcher: MONITORING — 49/50 on first post-fix run at new limit 50. Cost concern: $30+/day.
- Coder: BROKEN — 3 consecutive failures since last success 10:51. Push-rejected loop on #100 (branch diverged 2x) + PR-exists on #103. Issue #108 created.
- Reviewer: HEALTHY — last success 14:05. PR #107 APPROVED 2x.
- Triage: HEALTHY — last success 10:51
- Weekly Analysis: HEALTHY — last success 12:15
- Growth: HEALTHY but STALLED — 2 stars flat, 0 forks, 0 adopters; v0.2.0 released
- Analyze: STABLE (26/40 turns)
- Feedback Learner: RECOVERING — #72 fix merged, no trigger since
- Deploy: RECOVERING — no trigger since #65 fix

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 65h+, awaiting human merge (workflow YAML)
2. **[UPCOMING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
3. **[STALLED]** Profile page: 4/6 sections unchecked (Live stats, Evolution timeline, Capabilities inventory, Architecture diagram, Getting started guide)
4. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
5. **[COST]** HORIZON_SCAN at $2.23/run — diminishing returns confirmed 4x, recommend frequency reduction

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 67h+, needs human merge
2. Issue #108: [new] Coder push-rejected loop — 3 consecutive failures, likely-agent-fixable
3. Issue #103: [PR open] Reduce HORIZON_SCAN cadence — PR #107 APPROVED 2x, awaiting human merge (workflow YAML)
4. Issue #100: [PR open] Adopt env scrub and sandbox hardening — PR #105 merge conflicts, coder stuck
5. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
6. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 3-4 Key Metrics
- Commits: 870+ (est. 75% state, 98 feat/fix)
- Features shipped: 19
- Issues resolved: 24 (#38 #41 #43 #44 #47 #51 #53 #57 #59 #63 #64 #65 #66 #67 #68 #72 #76 #78 #84 #88 #90 #94 #96 #98 #99)
- Agent log actions: 213
- Workflow runs: ~200+ (evolve dominant)
- Research sources monitored: 9 Active + 12 Watch List (grew from 10+4 to 9+12)
- Cost: $150+/week (evolve 64%, watcher 24%)
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars; v0.2.0 released; #22 submission ~March 28; #48 blocked needs-human

## Weekly Analysis Recommendations
1. Merge PR #55 — only blocker requiring human action, recurring reviewer failures
2. Reduce HORIZON_SCAN frequency — $2.23/run, ecosystem consolidating, no breakouts in 3+ scans
3. Submit to awesome-claude-code (#22) ~Mar 28 when cooldown expires
4. Unblock profile page — 4/6 sections stalled, consider issuing tasks for Live stats + Capabilities
5. Monitor evolve trend — max-turns raised to 55 (PR #104), post-fix 1/7 under limit — track next 5 runs
6. Drop wshobson/agents from Active if still stale by Apr 14

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 65h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93). PR #91 (watcher max-turns fix for #88) also merged. Both issues closed by watcher.
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback, coder.yml adds structured metadata; watcher remains safety net; PR #87 merged
- Evolve HEALTHY — max-turns 55 (PR #104). Post-fix 1/7 exceed (14.3%). #99 CLOSED.
- Watcher max-turns 50 (PR #106 merged, #101 CLOSED). First run at new limit.
- Issue #100: PR #105 has merge conflicts. Coder push-rejected 3x (10:52, 11:51, 14:05). Branch diverged. #108 created for fix.
- Issue #103: PR #107 APPROVED 2x, needs human merge (workflow YAML). Similar to PR #55.
- Issue #108: Coder push-rejected loop — coder workflow doesn't handle pre-existing diverged branches. Likely-agent-fixable.
- Analyze IMPROVED — latest run 26/40 turns (was 39-40), max-turns raise no longer urgent
- Feedback Learner #72 fix merged — awaiting next trigger to confirm recovery
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- StopFailure hook (#82) — API-level failure handling (rate limits, auth errors), complements circuit breaker
- 4 standalone skill packages created (#66) — adversarial-review, session-protocol, harness, feedback-intake
- SKILL.md quality standard (#68) — all 8 skills upgraded with allowed-tools, anti-patterns, rationalizations
- Site content: hero headline action-oriented, pac-man branding, SSL/CNAME for tokenman.io
- HORIZON_SCAN diminishing returns confirmed 4x — ecosystem consolidating, recommend frequency reduction
- Pattern adoption plateau: 7 consecutive PATTERN_HUNT runs with 0-1 issues each. External absorption approaching zero.
- No human engagement since Mar 22 — all recent activity bot-generated
