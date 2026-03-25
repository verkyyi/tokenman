# Project State
Last updated: 2026-03-25T19:00:00Z
Updated by: watcher.yml (health check)

## Last Session
Action: watcher.yml — 3 corrective actions: closed #109 (PR #111 merged, auto-close miss #18), removed agent-ready from #100 (has PR #105), re-triggered coder for #100 (PR #105 trivial .commit-message conflict from PR #111 merge race).

System health:
- Evolve: WORSENING — 4/10 (40%) recent runs exceed max-turns 55. BUT PR #111 merged reducing cron to every 3h. Should see improvement.
- Watcher: BORDERLINE — 2/4 post-fix exceed 50 (50%), small sample. PR #111 also reduces watcher to every 2h.
- Coder: RECOVERED — 2 consecutive successes after 4 failures. #108 fix working. PR #105 still has merge conflict.
- Reviewer: HEALTHY — last success 18:02. 8-22 turns.
- Triage: HEALTHY — last success 17:53.
- Weekly Analysis: HEALTHY — last success 18:20.
- Growth: HEALTHY — last success 18:19.
- Analyze: STABLE (26/40 turns)
- Feedback Learner: RECOVERING — #72 fix merged, no trigger since
- Deploy: RECOVERING — no trigger since #65 fix

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 70h+, awaiting human merge (workflow YAML)
2. **[CONFLICT]** PR #105: env scrub hardening — trivial .commit-message conflict, coder re-triggered (attempt #3)
3. **[BLOCKED]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, awaiting human merge (workflow YAML)
4. **[UPCOMING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
5. **[STALLED]** Profile page: 4/6 sections unchecked
6. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 70h+, needs human merge
2. Issue #100: [coder re-triggered] PR #105 has .commit-message merge conflict — coder attempt #3
3. Issue #103: [PR open] PR #107 APPROVED 2x, needs human merge (workflow YAML)
4. Issue #109: [CLOSED] PR #111 merged, frequency reduction active
5. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
6. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 3-4 Key Metrics
- Commits: 880+ (est. 75% state, 100+ feat/fix)
- Features shipped: 19
- Issues resolved: 27 (#38 #41 #43 #44 #47 #51 #53 #57 #59 #63 #64 #65 #66 #67 #68 #72 #76 #78 #84 #88 #90 #94 #96 #98 #99 #101 #108 #109)
- Agent log actions: 227
- Workflow runs: ~200+ (evolve dominant, frequency now reduced)
- Research sources monitored: 9 Active + 12 Watch List
- Cost: $514/week projected — PR #111 reduces evolve frequency to 3h, expected ~$314/week
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars; v0.2.0 released; #22 submission ~March 28; #48 blocked needs-human

## Weekly Analysis Recommendations
1. Merge PR #55 — only blocker requiring human action, recurring reviewer failures
2. Merge PR #107 — APPROVED 2x, reduces HORIZON_SCAN cost
3. Submit to awesome-claude-code (#22) ~Mar 28 when cooldown expires
4. Unblock profile page — 4/6 sections stalled
5. Monitor evolve trend post-frequency-reduction (PR #111)
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
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 70h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve WORSENING — max-turns 55, 4/10 exceed (40%). PR #111 reduces cron to 3h — monitor improvement.
- Watcher max-turns 50 (PR #106 merged). 2/4 post-fix exceed (50%, small sample). Frequency reduced to 2h (PR #111).
- Issue #100: PR #105 trivial .commit-message conflict. Coder re-triggered (attempt #3). If still failing next run, escalate to needs-human.
- Issue #103: PR #107 APPROVED 2x, needs human merge (workflow YAML). Similar to PR #55.
- Issue #108: CLOSED. Coder push-rejected loop FIXED. Branch creation fetches remote+rebases, push uses force-with-lease fallback.
- Issue #109: CLOSED. PR #111 merged — evolve cron reduced from */15 to every 3h, watcher from hourly to every 2h.
- Analyze IMPROVED — latest run 26/40 turns (was 39-40)
- Feedback Learner #72 fix merged — awaiting next trigger to confirm recovery
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- HORIZON_SCAN diminishing returns confirmed 6x — ecosystem consolidating
- Pattern adoption plateau: 10 consecutive PATTERN_HUNT runs with 0 issues each
- No human engagement since Mar 22 — all recent activity bot-generated
