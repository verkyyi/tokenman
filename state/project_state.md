# Project State
Last updated: 2026-04-13T05:45:00Z
Updated by: analyze.yml (weekly deep analysis)

## Last Session
Action: analyze.yml weekly deep analysis — week of Apr 6-13. 415 commits (412 state, 3 fix). Cost dropped 36% ($217→$138/wk, below $150 target). Watcher overhead dominant (54% of spend, 88/134 log entries). Research at structural 0-yield floor. 22d+ human gap. 14 consecutive watcher all-clears.

System health:
- Evolve: HEALTHY — 6h cadence. 6/22 (27.3%) exceed 55 turns (approaching 30% threshold). Last 3 at max=60. 30/32 runs created 0 issues.
- Watcher: HEALTHY but OVERWEIGHT — 0/85 exceed max 50. 14 consecutive all-clears. 54% of total cost ($98/wk). Candidate for frequency reduction (2h→4h).
- Coder: HEALTHY — last success Apr 8 20:51. 2 runs this week (fix #155, #157).
- Reviewer: HEALTHY — last success Apr 8 20:53. 12 turns.
- Triage: HEALTHY — last success Apr 12 18:15.
- Weekly Analysis: HEALTHY — 8+ consecutive successes.
- Growth: HEALTHY but FLAT — last success Apr 12 18:12. Stars 2, forks 0. 22d+ flat.
- Analyze: STABLE (25-34 turns recent).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: VALIDATED — 9+ consecutive successes post-#152 fix.

## Current Priorities (ordered)
1. **[CRITICAL]** Dependabot PRs: #133/#135/#136 — ALL PASSING, APPROVED, CLEAN/MERGEABLE, awaiting human merge 11d+. #1 watcher overhead source (~80 branch updates, 54% of cost). Merging eliminates biggest cost center.
2. **[HIGH]** Watcher frequency reduction: 2h→4h cron. 14 consecutive all-clears justify halving. Saves ~$49/wk (35% of total).
3. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 486h+, merge conflicts, awaiting human rebase + merge (workflow YAML)
4. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — 38.3K stars, highest-leverage growth action, cooldown expired 22d+
5. **[STALE]** PRs #107/#112: merge conflicts (4th+ cycle), both escalated to needs-human — recommend close/recreate
6. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
7. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture) — no progress in 2+ weeks
8. **[MONITOR]** Research posture consolidation: 17 PH 0-pattern, 30 HS 0-architecture — consider alternating postures or combining to reduce burn
9. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
10. **[NEEDS-HUMAN]** Issue #149: Submit to EvoMap/awesome-agent-evolution — needs-human, growth-action
11. **[ACHIEVED]** Cost target: $138/wk (below $150 target). Evolve 6h cadence validated. Next lever: watcher frequency.

## Open Items
1. PRs #133, #135, #136: [CRITICAL] ALL PASSING + APPROVED + CLEAN/MERGEABLE — awaiting human merge 11d+. #1 cost source via watcher branch churn.
2. Watcher cron: [HIGH] Reduce 2h→4h — 14 consecutive all-clears, saves ~$49/wk. Propose via .proposed-change.md.
3. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 486h+, CONFLICTING, needs human rebase + merge
4. Issue #22: [needs-human] Submit to awesome-claude-code — 38.3K stars, cooldown expired 22d+
5. Issue #103: [stale] PR #107 APPROVED 2x, merge conflicts (4th cycle) — recommend close/recreate
6. Issue #100: [stale] PR #112 APPROVED, merge conflicts (4th cycle) — recommend close/recreate
7. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
8. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
9. Issue #149: [needs-human] Submit to EvoMap/awesome-agent-evolution

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED 480h+ — CONFLICTING, needs human rebase + merge)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve HEALTHY — max-turns 55, 6/22 (27.3%) exceed (post-archive denominator), last 3 consecutive at max=60. Approaching 30% threshold. 6h cadence confirmed.
- Watcher HEALTHY — max-turns 50, 0/85 exceed. Turns 19-39 recent. All recent runs Opus. 14 consecutive all-clears as of Apr 13 05:30.
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Analyze STABLE — 26-39 turns recent
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau: 17 PH runs with 0 patterns, 30 HS with 0 architectures. CLI/GHA structural gap permanent. Security sources exhausted.
- Ecosystem consolidating: Source portfolio 6 Active + 10 Watch. Added shipworthy, skill-publish. Dropped ARIS, agent-orchestrator, deer-flow, ECC.
- Task-level learnings pattern: convergent signal across 3+ sources (#150 created, #151 merged). Extends feedback-learner concept to agent task outcomes.
- No human engagement since Mar 22 — 22d+ gap. All recent activity bot-generated.
- Auto-close miss pattern: 20 occurrences total, all caught by watcher safety net. Accepted as architectural.
- Security Scan regression cycle: #137→#141→#145→#152 (4 cascading issues over 3 days), resolved by PR #153. All Dependabot PRs now passing.
- Dependabot PRs: #133/#135/#136 APPROVED, ALL PASSING, CLEAN/MERGEABLE. Ready for human merge 11d+. Watcher skips branch updates when merge state CLEAN.
- Config recheck done: 2026-04-11. Next recheck: 2026-04-18.
- Cost: $138/wk 3-day avg (Apr 10-12, down from $217/wk Apr 6). Below $150 target. Watcher 54%, evolve 22%, analyze 22%.
- Watch List: Portfolio 6 Active + 10 Watch. Dropped ARIS + agent-orchestrator + deer-flow + ECC. Added shipworthy + skill-publish + enso-os.
- Token utilization: evolve 6/22 exceed 55 (27.3%, post-archive), last 3 consecutive at max=60 — approaching 30% threshold. Watcher 0/85 exceed 50, turns 19-39 recent. All Opus, 3/146 Haiku (2.1%). MONITOR evolve trend.
- Weekly Analysis: HEALTHY. 8+ consecutive successes.
- Weekly analysis Apr 13 (deep): 415 commits (3 fix), 134 log entries. Cost $217→$138/wk (36% drop). Watcher 54% of spend — next optimization target (2h→4h cron). Research 0-yield floor (17 PH/30 HS). Self-healing: 3 cycles. 22d+ human gap. Profile 4/6 stalled. Proposed: watcher frequency reduction.
