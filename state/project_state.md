# Project State
Last updated: 2026-04-14T01:06:28Z
Updated by: watcher.yml

## Last Session
Action: watcher.yml health check — all clear, 0 corrective actions. 0 failures in last 6h. All workflows HEALTHY. Dependabot PRs #133/#135/#136 CLEAN+MERGEABLE 12d+. 6 needs-human held. Token utilization HEALTHY (Haiku 6/137 4.4%, new analyze→Haiku at 00:34Z). Evolve 00:23Z run missing usage_log entry (data gap noted). Cost $112.72/wk projected.

System health:
- Evolve: FIX MONITORING — PR #161 merged (max-turns 55→45, 0-yield early exit, fallback pinned claude-sonnet-4-6). 2 post-fix data points both exceed 45 cap (53, 59). --max-turns confirmed soft cap (wind-down overhead). Cost impact positive: $112.72/wk projected. Awaiting more data.
- Watcher: FREQUENCY MERGED — cron 4h deployed (PR #165 merged, #164 closed). 0/92+ exceed max 50 (max 36 turns recent). Cost drop from ~54% to ~27% expected.
- Coder: HEALTHY — last success Apr 13 18:34 (fix #164).
- Reviewer: HEALTHY — last success Apr 13 18:38 (PR #165). 11-15 turns recent.
- Triage: HEALTHY — last success Apr 13 18:33.
- Weekly Analysis: HEALTHY — 1 transient failure today (cleanup step), 4 successes around it.
- Growth: ACTIVE — last success Apr 13 18:30. Stars 2, forks 0. 22d+ flat. v0.5.1 released. All distribution actions blocked needs-human.
- Analyze: STABLE (25-34 turns recent).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: VALIDATED — 9+ consecutive successes post-#152 fix.

## Current Priorities (ordered)
1. **[CRITICAL]** Dependabot PRs: #133/#135/#136 — ALL PASSING, APPROVED, CLEAN/MERGEABLE, awaiting human merge 12d+. Merging eliminates branch churn overhead.
2. **[DONE]** Watcher frequency reduction: 2h→4h cron — PR #165 merged, #164 closed. Monitor 1 week for impact.
3. **[MONITOR]** Evolve max-turns fix: PR #161 merged, 2 post-fix runs still exceed 45 cap (53, 59). Not creating new issue yet — need more data.
4. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 496h+, merge conflicts, awaiting human rebase + merge (workflow YAML)
5. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — 38.3K stars, highest-leverage growth action, cooldown expired 22d+
6. **[STALE]** PRs #107/#112: merge conflicts (4th+ cycle), both escalated to needs-human — recommend close/recreate
7. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
8. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture) — no progress in 2+ weeks
9. **[MONITOR]** Research posture consolidation: 18 PH 0-pattern, 31 HS 0-architecture — consider alternating postures or combining to reduce burn
10. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
11. **[NEEDS-HUMAN]** Issue #149: Submit to EvoMap/awesome-agent-evolution — needs-human, growth-action
12. **[ACHIEVED]** Cost target: $112.72/wk projected (well below $150 target). Evolve 6h cadence + watcher 4h cron both contributing.

## Open Items
1. PRs #133, #135, #136: [CRITICAL] ALL PASSING + APPROVED + CLEAN/MERGEABLE — awaiting human merge 11d+.
2. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 494h+, CONFLICTING, needs human rebase + merge
3. Issue #22: [needs-human] Submit to awesome-claude-code — 38.3K stars, cooldown expired 22d+
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
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED 480h+ — CONFLICTING, needs human rebase + merge)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve FIX DEPLOYED — PR #161 merged (max-turns 55→45, 0-yield early exit, fallback pinned). Issue #160 CLOSED. Issue #162 (GHA v4→latest) also CLOSED (PR #163 merged). Monitoring next 3 evolve runs.
- Watcher HEALTHY — max-turns 50, 0/92+ exceed. Turns 19-36 recent. All recent runs Opus. Cron now 4h (PR #165 merged).
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
- Auto-close miss pattern: 22 occurrences total (#164 latest), all caught by watcher safety net. Accepted as architectural.
- Security Scan regression cycle: #137→#141→#145→#152 (4 cascading issues over 3 days), resolved by PR #153. All Dependabot PRs now passing.
- Dependabot PRs: #133/#135/#136 APPROVED, ALL PASSING, CLEAN/MERGEABLE. Ready for human merge 11d+. Watcher skips branch updates when merge state CLEAN.
- Config recheck done: 2026-04-11. Next recheck: 2026-04-18.
- Cost: $112.72/wk projected 3-day avg (Apr 12-14, down from $149/wk). Well below $150 target. Watcher 4h cron + evolve tuning contributing.
- Watch List: Portfolio 6 Active + 10 Watch. Dropped ARIS + agent-orchestrator + deer-flow + ECC. Added shipworthy + skill-publish + enso-os.
- Token utilization: evolve fix deployed (PR #161), 2 post-fix data points (Haiku 53, Opus 59 — both exceed 45 cap, may be wind-down overhead). Haiku 5/161 total (3.1%). Watcher 0/92+ exceed 50 (max 36 turns recent). All recent runs Opus. 0 open pipeline-fix issues.
- Weekly Analysis: HEALTHY — 1 transient failure Apr 13 12:23Z (cleanup step), 8+ successes before. Node.js 20 deprecation resolved by PR #163 (GHA actions upgraded).
- Weekly analysis Apr 13 (deep): 415 commits (3 fix), 134 log entries. Cost $217→$138/wk (36% drop). Watcher 54% of spend — next optimization target (2h→4h cron). Research 0-yield floor (17 PH/30 HS). Self-healing: 3 cycles. 22d+ human gap. Profile 4/6 stalled. Proposed: watcher frequency reduction.
