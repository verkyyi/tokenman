# Project State
Last updated: 2026-04-12T14:50:06Z
Updated by: watcher.yml

## Last Session
Action: watcher.yml health check — 7th consecutive all clear, 0 corrective actions. 0 failures in last 6h. Dependabot PRs #133/#135/#136 CLEAN+MERGEABLE (no branch update needed, awaiting human merge 10d+). All workflows HEALTHY. Token utilization HEALTHY (162 data lines, all Opus).

System health:
- Evolve: HEALTHY — turns 34-60, max 55. 5/28 (17.9%) exceed rate (below 30% threshold). Latest 12:09 Apr 12.
- Watcher: HEALTHY — 0/90+ exceed max 50. Turns 19-39 recent. All Opus, 3/162 Haiku (1.9%).
- Coder: HEALTHY — last success Apr 8 20:51.
- Reviewer: HEALTHY — last success Apr 8 20:53. 12 turns.
- Triage: HEALTHY — last success Apr 12 09:20.
- Weekly Analysis: HEALTHY — 7+ consecutive successes since transient failure Apr 11 00:24Z. Latest 12:12 Apr 12.
- Growth: HEALTHY — last success Apr 12 09:17.
- Analyze: STABLE (27-39 turns recent).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: VALIDATED — 9+ consecutive successes post-#152 fix.

## Current Priorities (ordered)
1. **[READY]** Dependabot PRs: #133/#135/#136 — ALL PASSING, APPROVED, branches updated, awaiting human merge. #1 watcher overhead source (80+ branch updates).
2. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 474h+, merge conflicts, awaiting human rebase + merge (workflow YAML)
3. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — 36.9K stars, highest-leverage growth action, cooldown expired 20d+
4. **[STALE]** PRs #107/#112: merge conflicts (4th+ cycle), both escalated to needs-human — recommend close/recreate
5. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
6. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture) — no progress this week
7. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
8. **[NEEDS-HUMAN]** Issue #149: Submit to EvoMap/awesome-agent-evolution — needs-human, growth-action
9. **[MONITOR]** Research cadence: 17 PH 0-pattern, 29 HS 0-architecture — structural plateau confirmed, consider reduction

## Open Items
1. PRs #133, #135, #136: [ready] ALL PASSING + APPROVED + CLEAN/MERGEABLE — awaiting human merge (10d+). Watcher spent 88+ corrective actions on branch updates.
2. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 474h+, CONFLICTING, needs human rebase + merge
3. Issue #22: [needs-human] Submit to awesome-claude-code — 36.9K stars, cooldown expired 20d+
4. Issue #103: [stale] PR #107 APPROVED 2x, merge conflicts (4th cycle) — recommend close/recreate
5. Issue #100: [stale] PR #112 APPROVED, merge conflicts (4th cycle) — recommend close/recreate
6. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
7. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
8. Issue #149: [needs-human] Submit to EvoMap/awesome-agent-evolution

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED 474h+ — CONFLICTING, needs human rebase + merge)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve HEALTHY — max-turns 55, 5/28 (17.9%) exceed. Latest 60 turns (HORIZON_SCAN, single occurrence). Cron 6h confirmed.
- Watcher HEALTHY — max-turns 50, 0/90+ exceed. Turns 19-39 recent. Haiku fallbacks fully resolved — last 64+ runs Opus (3/162 total, 1.9%).
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Analyze STABLE — 26-39 turns recent
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau: 17 PH runs with 0 patterns (continuing multi-week drought). CI/CLI structural gap permanent. Security sources exhausted.
- Ecosystem consolidating: backporcher is first true architectural peer (10 stars, parallel agent dispatcher). Source portfolio: 6 Active + 10 Watch (dropped ARIS + orchestrator, added shipworthy).
- Task-level learnings pattern: convergent signal across 3+ sources (#150 created, #151 merged). Extends feedback-learner concept to agent task outcomes.
- No human engagement since Mar 22 — 20d+ gap. All recent activity bot-generated.
- Auto-close miss pattern: 20 occurrences total, all caught by watcher safety net. Accepted as architectural.
- Security Scan regression cycle: #137→#141→#145→#152 (4 cascading issues over 3 days), resolved by PR #153. All Dependabot PRs now passing.
- Dependabot PRs: #133/#135/#136 APPROVED, ALL PASSING, CLEAN/MERGEABLE. Ready for human merge. Skipping branch updates when merge state is CLEAN to reduce churn.
- Config recheck done: 2026-04-11. Next recheck: 2026-04-18.
- Cost: $138/wk 3-day avg (Apr 10-12, down from $155). Watcher 54%, evolve 22%, analyze 22%. Evolve 6h cadence savings confirmed.
- Watch List: Portfolio 6 Active + 10 Watch. Dropped ARIS + agent-orchestrator this cycle. Added shipworthy.
- Token utilization: evolve 5/28 exceed 55 (17.9%). Watcher 0/90+ exceed 50, turns 19-39 recent. All Opus, 3/162 Haiku (1.9%). HEALTHY.
- Weekly Analysis: HEALTHY. Transient failure Apr 11 00:24Z followed by 7 consecutive successes. Latest 12:12 Apr 12.
- Weekly analysis Apr 11: 474 commits, 122 log entries, 6 issues created+fixed, v0.5.0 released, research structural plateau (16 PH/29 HS consecutive 0-yield). 20d+ human gap.
