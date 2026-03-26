# Project State
Last updated: 2026-03-26T05:20:00Z
Updated by: watcher.yml

## Last Session
Action: watcher.yml health check — all clear. 0 corrective actions. All workflows HEALTHY. Post-frequency-reduction trend continues: evolve 3/3 under 55, watcher 6/6 under 50 (turns trending down: 42→45→28→25). 4 issues correctly held at needs-human (#103, #100, #48, #22). 3 PRs awaiting human merge (#55 82h+, #107 18h+, #112 10h+). No broken chains, stuck runs, or repeated failures.

System health:
- Evolve: IMPROVING — 2/10 (20%) exceed max-turns 55. Post-frequency-reduction: 3/3 under limit.
- Watcher: IMPROVING — 1/7 (14%) exceed 50. Post-frequency-reduction: 6/6 under limit. Turns trending down.
- Coder: RECOVERED — 4 consecutive successes after 4 failures. #108 fix working.
- Reviewer: HEALTHY — last success 19:14. 14-22 turns.
- Triage: HEALTHY — last success 17:53.
- Weekly Analysis: HEALTHY — last success 00:24 Mar 26.
- Growth: HEALTHY — last success 18:19.
- Analyze: STABLE (26/40 turns on latest run 00:28 Mar 26)
- Feedback Learner: RECOVERED — last success 19:14 (5 turns). #72 fix confirmed working.
- Deploy: RECOVERING — no trigger since #65 fix

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 82h+, awaiting human merge (workflow YAML)
2. **[NEEDS-HUMAN]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts 18h+, escalated to needs-human (workflow YAML)
3. **[NEEDS-HUMAN]** Issue #103 / PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts 18h+, workflow YAML, escalated to needs-human
4. **[NEEDS-HUMAN]** Issue #100 / PR #112: env scrub hardening — APPROVED but merge conflicts (4th cycle), all workflow YAML, needs manual rebase + merge
5. **[UPCOMING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28
6. **[STALLED]** Profile page: 4/6 sections unchecked
7. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 82h+, needs human merge
2. Issue #100: [needs-human] PR #112 APPROVED, merge conflicts (4th cycle), all workflow YAML — escalated
3. Issue #103: [needs-human] PR #107 APPROVED 2x, merge conflicts 8h+, escalated to needs-human (workflow YAML)
4. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
5. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 3-4 Key Metrics
- Commits: 890+ (est. 75% state, 100+ feat/fix)
- Features shipped: 19
- Issues resolved: 27 (#38 #41 #43 #44 #47 #51 #53 #57 #59 #63 #64 #65 #66 #67 #68 #72 #76 #78 #84 #88 #90 #94 #96 #98 #99 #101 #108 #109)
- Agent log actions: 232
- Workflow runs: ~220+ (evolve dominant, frequency now reduced)
- Research sources monitored: 9 Active + 12 Watch List
- Cost: ~$294/week measured post-PR #111 (69% reduction from ~$134/day pre-merge to ~$42/day)
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars; v0.2.0 released; #22 submission ~March 28; #48 blocked needs-human

## Weekly Analysis Recommendations
1. Merge PR #55 — only blocker requiring human action, recurring reviewer failures
2. Merge PR #107 — APPROVED 2x, reduces HORIZON_SCAN cost (needs rebase first)
3. Rebase + merge PR #112 — APPROVED, env scrub hardening for all workflows
4. Submit to awesome-claude-code (#22) ~Mar 28 when cooldown expires
5. Unblock profile page — 4/6 sections stalled
6. Monitor evolve trend post-frequency-reduction (PR #111)
7. Drop wshobson/agents from Active if still stale by Apr 14

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 72h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve IMPROVING — max-turns 55, 2/10 exceed (20%, down from 30%). PR #111 frequency reduction confirmed working. Post-reduction runs 3/3 under limit.
- Watcher IMPROVING — max-turns 50 (PR #106), 1/7 exceed (14%, down from 22%). Frequency reduced to 2h (PR #111). Post-reduction 6/6 under limit. Turns trending down.
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Modifies all 10 workflow YAML files. Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts 8h+. Same pattern as #100 — workflow YAML, manual rebase + merge required.
- Issue #108: CLOSED. Coder push-rejected loop FIXED.
- Issue #109: CLOSED. PR #111 merged — evolve cron reduced from */15 to every 3h, watcher from hourly to every 2h.
- Analyze STABLE — latest run 42/40 turns (minor variance)
- Feedback Learner RECOVERED — 5 turns on 19:14 run, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- HORIZON_SCAN diminishing returns confirmed 6x — ecosystem consolidating
- Pattern adoption plateau: 10 consecutive PATTERN_HUNT runs with 0 issues each
- No human engagement since Mar 22 — all recent activity bot-generated
- PR #105 CLOSED (not merged) — superseded by PR #112
