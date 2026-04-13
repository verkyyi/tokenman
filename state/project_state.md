# Project State
Last updated: 2026-04-13T12:55:00Z
Updated by: watcher.yml

## Last Session
Action: watcher.yml health check — 2 corrective actions: closed #160 (PR #161 merged, auto-close miss #21), re-triggered triage for #162 (GITHUB_TOKEN-created, won't auto-trigger). Evolve fix (PR #161) partially effective: first post-fix run 53 turns on Haiku (down from 60-79, but exceeds new 45 cap). Haiku fallback persists despite --fallback-model claude-sonnet-4-6. Weekly Analysis 1 transient failure at 12:23Z. Coder failure at 09:17Z transient (succeeded 11:06Z).

System health:
- Evolve: FIX APPLIED, MONITORING — max-turns 55→45 merged (PR #161). First post-fix run: 53 turns on Haiku (improved from 60-79, but still exceeds 45 cap). Haiku fallback persists despite --fallback-model claude-sonnet-4-6 — likely platform-level. Need 2-3 more runs to assess.
- Watcher: HEALTHY but OVERWEIGHT — 0/87+ exceed max 50. Turns 19-39 recent. 54% of total cost. Candidate for frequency reduction (2h→4h).
- Coder: HEALTHY — last success Apr 13 11:06 (fix #160→PR #161). 31 turns.
- Reviewer: HEALTHY — last success Apr 13 11:10. 12 turns.
- Triage: HEALTHY — last success Apr 13 09:38.
- Weekly Analysis: MOSTLY HEALTHY — 1 transient failure at 12:23Z (exit code 1, 3.5 min), 8+ successes before. Not 3 consecutive.
- Growth: HEALTHY but FLAT — last success Apr 13 12:15. Stars 2, forks 0. 22d+ flat. No release candidate. All actions blocked needs-human.
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
- Evolve FIX APPLIED — max-turns 55→45 via PR #161 (merged Apr 13 11:12Z). First post-fix run: 53 turns on Haiku (PATTERN_HUNT, 0 issues). Improved from 60-79 pre-fix but still exceeds 45 cap. Haiku fallback persists despite --fallback-model claude-sonnet-4-6 — likely platform-level rate-limit behavior, not controllable via CLI flag. Issue #160 CLOSED.
- Watcher HEALTHY — max-turns 50, 0/87 exceed. Turns 19-36 recent. All recent runs Opus.
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
- Token utilization: evolve post-fix first run 53 turns on Haiku (down from 60-79, still exceeds 45 cap). Haiku fallback 5/155 (3.2%), latest 2 runs Haiku. Watcher 0/87+ exceed 50, turns 19-39 recent, all Opus. Issue #160 CLOSED (PR #161 merged). Issue #162 created (GHA Node.js 20 deprecation), triage re-triggered.
- Weekly Analysis: MOSTLY HEALTHY — 1 transient failure at Apr 13 12:23Z, 8+ successes before.
- Weekly analysis Apr 13 (deep): 415 commits (3 fix), 134 log entries. Cost $217→$138/wk (36% drop). Watcher 54% of spend — next optimization target (2h→4h cron). Research 0-yield floor (17 PH/30 HS). Self-healing: 3 cycles. 22d+ human gap. Profile 4/6 stalled. Proposed: watcher frequency reduction.
