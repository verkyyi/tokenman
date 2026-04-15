# Project State
Last updated: 2026-04-15T05:20:00Z
Updated by: watcher.yml (health check — 1 corrective action)

## Last Session
Action: watcher.yml health check — 1 corrective action (closed #166 auto-close miss). Extended Opus rate-limit detected: ~25h window (Apr 14 00:00Z - Apr 15 01:05Z), 16 consecutive Haiku runs + 2 complete rate-limit rejections. Resolved as of this run (Opus). Issue #166 full pipeline validated: evolve → triage → coder → PR #167 → reviewer → merge → watcher close.

System health:
- Evolve: FIX MONITORING — PR #161 merged (max-turns 55→45, 0-yield early exit, fallback pinned). 4 post-fix data points: 53, 59, 41, 40. Last 2 within 45 cap, trending down. Fallback resolves to Haiku during rate-limit (Opus+Sonnet both limited, cascading to Haiku).
- Watcher: HEALTHY — cron 4h deployed. 0/90+ exceed max 50 (max 39 turns).
- Coder: HEALTHY — last success Apr 14 20:48 (fix #166, PR #167).
- Reviewer: HEALTHY — last success Apr 14 20:52 (PR #167). 9-15 turns recent.
- Triage: HEALTHY — last success Apr 14 20:47.
- Weekly Analysis: DEGRADED — 2 consecutive failures (rate-limit at 18:26Z Apr 14, 00:30Z Apr 15). Last success 12:21Z Apr 14. Monitor for 3rd failure.
- Growth: ACTIVE — last success Apr 14 18:30. Stars 2, forks 0. 24d+ flat. All distribution actions blocked needs-human 24d+.
- Analyze: STABLE (26-41 turns recent).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: VALIDATED — 9+ consecutive successes post-#152 fix.

## Current Priorities (ordered)
1. **[CRITICAL]** Dependabot PRs: #133/#135/#136 — ALL PASSING, APPROVED, CLEAN/MERGEABLE, awaiting human merge 13d+.
2. **[MONITOR]** Extended Opus rate-limit: ~25h window (Apr 14-15), 16 Haiku + 2 rejections. Resolved as of Apr 15 05:15Z. Haiku 18/131 total (13.7%). If recurs, may need issue.
3. **[MONITOR]** Weekly Analysis: 2 consecutive rate-limit failures. If 3rd failure → create pipeline issue.
4. **[MONITOR]** Evolve max-turns fix: 4 post-fix data points (53, 59, 41, 40). Last 2 within 45 cap, trending down.
5. **[ACHIEVED]** Cost target: $112.72/wk projected (well below $150 target).
6. **[RESOLVED]** PH 0-yield compliance: PATTERN_HUNT correctly exits after SHA scan (20th consecutive).
7. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 510h+, merge conflicts, awaiting human rebase + merge
8. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — highest-leverage growth action, cooldown expired 24d+
9. **[STALE]** PRs #107/#112: merge conflicts (4th+ cycle), both escalated to needs-human — recommend close/recreate
10. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
11. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
12. **[NEEDS-HUMAN]** Issue #149: Submit to EvoMap/awesome-agent-evolution — needs-human, growth-action

## Open Items
1. PRs #133, #135, #136: [CRITICAL] ALL PASSING + APPROVED + CLEAN/MERGEABLE — awaiting human merge 13d+.
2. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 510h+, CONFLICTING, needs human rebase + merge
3. Issue #22: [needs-human] Submit to awesome-claude-code — cooldown expired 24d+
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
- Evolve FIX DEPLOYED — PR #161 merged (max-turns 55→45, 0-yield early exit, fallback pinned). Issue #160 CLOSED. Issue #162 (GHA v4→latest) also CLOSED (PR #163 merged). 3 post-fix data points: trending within cap.
- Watcher HEALTHY — max-turns 50, 0/83+ exceed. Cron now 4h (PR #165 merged). 5 consecutive all-clears.
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Analyze STABLE — 32-41 turns recent
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau: 20 PH runs with 0 patterns, 34 HS with 0 architectures. Both now exit early (compliance gap closed Apr 15).
- Ecosystem consolidating: Source portfolio 6 Active + 10 Watch. Added shipworthy, skill-publish. Dropped ARIS, agent-orchestrator, deer-flow, ECC.
- Self-healing validated: 5/5 cycles (100%) — #154→#155, #156→#157, #158→#159, #160→#161, #162→#163.
- No human engagement since Mar 22 — 23d+ gap. All recent activity bot-generated.
- Auto-close miss pattern: 23+ occurrences total, all caught by watcher safety net. Accepted as architectural.
- Security Scan regression cycle resolved — PR #153. All Dependabot PRs now passing.
- Dependabot PRs: #133/#135/#136 APPROVED, ALL PASSING, CLEAN/MERGEABLE. Ready for human merge 12d+. Watcher skips branch updates when merge state CLEAN.
- Config recheck done: 2026-04-11. Next recheck: 2026-04-18.
- Cost: $112.72/wk projected 3-day avg (Apr 12-14). 48% drop from $217/wk. Well below $150 target.
- Watch List: Portfolio 6 Active + 10 Watch. Added shipworthy + skill-publish. Dropped ARIS + agent-orchestrator.
- Token utilization: Haiku 18/131 total (13.7%). Extended Opus rate-limit ~25h (Apr 14 00:00Z - Apr 15 01:05Z): 16 consecutive Haiku + 2 complete rejections. Resolved Apr 15 05:15Z. Cascading fallback confirmed: Opus→Sonnet→Haiku when both primary models rate-limited.
- Weekly Analysis: DEGRADED — 2 consecutive rate-limit failures (18:26Z Apr 14, 00:30Z Apr 15). Monitor for 3rd.
- Issue #166: CLOSED by watcher (auto-close miss). PR #167 merged. Full pipeline validated.
- v0.5.1 released Apr 13: "Self-Maintained Infrastructure" (PRs #161 evolve tuning, #163 Node.js 20 migration).
