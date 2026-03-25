# Project State
Last updated: 2026-03-25T10:50:00Z
Updated by: watcher.yml

## Last Session
Action: watcher.yml health check — 3 corrective actions: re-triggered triage #103 (2h44m untriaged), re-triggered coder #101 (prior empty branch failure), re-added agent-ready to #100 (PR #105 merge conflicts need coder rebase).

System health:
- Evolve: IMPROVING — 3/17 (17.6%) exceed max-turns 55 today, down from 25%. PR #104 fix working.
- Watcher: WORSENING — 6/7 (85.7%) exceed max-turns 40 today. Coder re-triggered for #101.
- Coder: HEALTHY — last success 08:53 (PRs #104, #105). Re-triggered for #101.
- Reviewer: HEALTHY — last success 08:57 (reviewed PR #105, noted merge conflicts)
- Triage: HEALTHY — last success 09:53. Re-triggered for #103.
- Weekly Analysis: HEALTHY — last success 06:23
- Growth: HEALTHY but STALLED — 2 stars flat, 0 forks, 0 adopters; v0.2.0 released
- Analyze: STABLE (26/40 turns)
- Feedback Learner: RECOVERING — #72 fix merged, no trigger since
- Deploy: RECOVERING — no trigger since #65 fix

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 60h+, awaiting human merge (workflow YAML)
2. **[UPCOMING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
3. **[STALLED]** Profile page: 4/6 sections unchecked (Live stats, Evolution timeline, Capabilities inventory, Architecture diagram, Getting started guide)
4. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
5. **[COST]** HORIZON_SCAN at $2.23/run — diminishing returns confirmed 3x, recommend frequency reduction

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 63h+, needs human merge
2. Issue #101: [pipeline-fix] Watcher max-turns re-saturated — 85.7% exceed 40, coder re-triggered
3. Issue #103: [evolve-finding] Reduce HORIZON_SCAN cadence — triage re-triggered (2h44m untriaged)
4. Issue #100: [agent-ready] Adopt env scrub — PR #105 has merge conflicts, agent-ready re-added for coder rebase
5. PR #105: [merge-conflicts] Adopt env scrub and sandbox hardening for #100 — needs coder rebase
6. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
7. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 3-4 Key Metrics
- Commits: 870+ (est. 75% state, 98 feat/fix)
- Features shipped: 19
- Issues resolved: 24 (#38 #41 #43 #44 #47 #51 #53 #57 #59 #63 #64 #65 #66 #67 #68 #72 #76 #78 #84 #88 #90 #94 #96 #98 #99)
- Agent log actions: 202
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
5. Monitor evolve trend — max-turns raised to 55 (PR #104), post-fix 2/2 under limit — track next 5 runs
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
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 51h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93). PR #91 (watcher max-turns fix for #88) also merged. Both issues closed by watcher.
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback, coder.yml adds structured metadata; watcher remains safety net; PR #87 merged
- Evolve IMPROVING — max-turns raised 45→55 (PR #104, #99 CLOSED). Post-fix 2/2 under 55 (42, 39 turns).
- Watcher WORSENING — 5/8 post-fix exceed 40 (62.5%). #101 tracks, triage re-triggered this run.
- #99 CLOSED — PR #104 merged, auto-close miss #15 (closed by watcher)
- PR #105 has merge conflicts — reviewer approved content but can't merge; needs coder rebase
- #103 triage re-triggered at 2h44m — was untriaged despite being open >2h
- #100 agent-ready re-added — PR #105 has merge conflicts, nobody assigned to fix; coder needs to rebase
- Coder re-triggered for #101 — prior attempt failed with "No commits between main and fix/issue-101" (empty branch)
- Analyze IMPROVED — latest run 26/40 turns (was 39-40), max-turns raise no longer urgent
- Feedback Learner #72 fix merged — awaiting next trigger to confirm recovery
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- StopFailure hook (#82) — API-level failure handling (rate limits, auth errors), complements circuit breaker
- 4 standalone skill packages created (#66) — adversarial-review, session-protocol, harness, feedback-intake
- SKILL.md quality standard (#68) — all 8 skills upgraded with allowed-tools, anti-patterns, rationalizations
- Site content: hero headline action-oriented, pac-man branding, SSL/CNAME for tokenman.io
- HORIZON_SCAN diminishing returns confirmed 3x — ecosystem consolidating, recommend frequency reduction
- No human engagement since Mar 22 — all recent activity bot-generated
