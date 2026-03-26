# Project State
Last updated: 2026-03-26T12:26:35Z
Updated by: evolve.yml (SYNTHESIS posture)

## Last Session
Action: evolve.yml SYNTHESIS — hour 12 SEO check found README/description outdated post-PR #111 (issue #113 created). 6 convergent signals analyzed. Cost $294/week validated. Pattern plateau 13th consecutive. Human disengagement 4+ days. Watch List decisions due Mar 30. SHA scan: 3 Active + 2 Watch List changes.

System health:
- Evolve: IMPROVING — post-frequency-reduction 6/6 under 55 limit. Turns: 37-52.
- Watcher: IMPROVING — post-frequency-reduction 10/10 under 50 limit. Turns: 25-45.
- Coder: RECOVERED — 4+ consecutive successes after 4 failures. #108 fix working.
- Reviewer: HEALTHY — 14-22 turns.
- Triage: HEALTHY.
- Weekly Analysis: HEALTHY.
- Growth: HEALTHY (17 turns).
- Analyze: STABLE (26-32 turns).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 90h+, awaiting human merge (workflow YAML)
2. **[NEEDS-HUMAN]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts, escalated to needs-human
3. **[NEEDS-HUMAN]** PR #112: env scrub hardening — APPROVED but merge conflicts (4th cycle), all workflow YAML, needs manual rebase + merge
4. **[UPCOMING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
5. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture)
6. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
7. **[MAINTENANCE]** Source portfolio rebalance — agents 18d+ stale (drop Apr 14), Watch List decisions due Mar 30

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 90h+, needs human merge
2. Issue #100: [needs-human] PR #112 APPROVED, merge conflicts (4th cycle), all workflow YAML — escalated
3. Issue #103: [needs-human] PR #107 APPROVED 2x, merge conflicts, escalated to needs-human (workflow YAML)
4. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
5. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week of Mar 19-26 Key Metrics
- Commits: 1072 (907 state, 165 feat/fix)
- Issues resolved: 9 (#88 #90 #94 #96 #98 #99 #101 #108 #109)
- Issues created: 9 (#94 #96 #98 #99 #100 #101 #103 #108 #109)
- Agent log actions: ~237
- Workflow runs: evolve ~80+, watcher ~70+, coder ~15, reviewer/triage/growth/analyze as expected
- Research entries: 142 (9 Active + 12 Watch List sources)
- Cost: ~$294/week post-PR #111 (69% reduction from ~$134/day to ~$42/day)
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars; v0.3.0 released Mar 26; #22 submission ~March 28 (awesome-cc 32.5K); #48 blocked needs-human
- Pattern adoption: 0 new patterns in 12 consecutive PATTERN_HUNT runs (plateau)
- Issue #113: README/description frequency claims outdated after PR #111

## Weekly Analysis Recommendations
1. Merge PR #55 — only blocker requiring human action, recurring reviewer state bugs
2. Merge PR #107 — APPROVED 2x, reduces HORIZON_SCAN cost (needs rebase first)
3. Rebase + merge PR #112 — APPROVED, env scrub hardening for all workflows
4. Submit to awesome-claude-code (#22) ~Mar 28 when cooldown expires
5. Drop wshobson/agents from Active sources — 18d+ stale, 0 pattern hits
6. Watch List bulk decisions after Mar 30 — OpenViking (31 obs, 0 patterns) strongest drop candidate
7. Reduce PATTERN_HUNT cadence — 11-run plateau, diminishing ROI
8. Unblock profile page — 4/6 sections stalled
9. Monitor cost trend — $294/week still 2x above $150 baseline target
10. Address root cause of evolve turn saturation — prompt depth, not just max-turns config

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 82h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve IMPROVING — max-turns 55, 0/6 post-reduction exceed (0%). PR #111 frequency reduction confirmed working.
- Watcher IMPROVING — max-turns 50 (PR #106), 0/10 post-reduction exceed (0%). Frequency reduced to 2h (PR #111). Turns: 25-45.
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Issue #108: CLOSED. Coder push-rejected loop FIXED.
- Issue #109: CLOSED. PR #111 merged — evolve cron reduced from */15 to every 3h, watcher from hourly to every 2h.
- Analyze STABLE — 26-42 turns
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- HORIZON_SCAN diminishing returns confirmed 6x — ecosystem consolidating
- Pattern adoption plateau: 11 consecutive PATTERN_HUNT runs with 0 issues each
- No human engagement since Mar 22 — all recent activity bot-generated
- PR #105 CLOSED (not merged) — superseded by PR #112
- claude-code v2.1.84: paths: glob frontmatter for skills — relevant to #66
