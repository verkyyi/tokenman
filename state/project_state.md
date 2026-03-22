# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-22T09:08:39Z
Updated by: evolve.yml (self-evolution run — tier 0, pipeline health, human intent analysis)

## Last Session
Action: evolve.yml — tier-0 research, pipeline health check, human intent analysis

Done:
- Researched all 3 core sources (claude-code, gstack, everything-claude-code) + 2 tier-0 sources (wshobson/agents, awesome-claude-code-subagents): all unchanged from previous runs
- Pipeline health: found 2 ACTIONABLE failures — Pipeline Watcher (23399465154) and Feedback Learner (23399326001) both fail with "Fallback model cannot be the same as the main model"; root cause: PR #27 (issue #26 fix) added --fallback-model=haiku when those workflows already use haiku as main model; created issue #36
- Human intent analysis (Step 2f): logged 10 human intents from last 7 days to learned_intents.md; FIX_PROCESS threshold met (3 issues: #35,#26,#23 — all pipeline reliability); issue #36 also serves this pattern
- Design evaluation: no issues found (Base.astro + index.astro look clean)

## Open Items (priority order)
1. Issue #36: [URGENT — pipeline broken] Watcher + feedback-learner fail due to --fallback-model==main model regression (PR #27)
2. Issue #35: [agent-ready — pipeline-fix] Avoid CLI/pipeline conflicts — detect human activity and prevent duplicated work
3. Issue #33: [agent-ready] Human intent learning, PR close handling, interaction guide (PR #34 merged but issue not auto-closed)
4. Issue #29: [agent-ready — bug] Profile page not synced with latest changes (PR #30 merged but issue not auto-closed)
5. Issue #28: [agent-ready] Token utilization feedback loop (PR #32 merged but issue not auto-closed)
6. Issue #26: [agent-ready] Optimize Claude CLI configuration (PR #27 merged but issue not auto-closed) — watcher failing so not auto-closing
7. Issue #31: [evolve-finding] Cache research source checksums (all sources unchanged for 3+ consecutive runs — this is timely)
8. Issue #8: [agent-ready — UNBLOCKED] Upgrade Node.js 20 actions before June 2026 deadline
9. PR #19: [needs-review] Anti-sycophancy guardrails for adversarial-review.md (closes #13)
10. PR #20: [needs-review] Agentic security patterns (closes #17)
11. Issue #22: [needs-review] Submit to hesreallyhim/awesome-claude-code (29k stars)
12. Issue #10: [needs-review] Last-updated badge user-friendly time
13. Issue #21: [feature] Add DeerFlow repo to external sources

## Critical Note for Next Agent
- Watcher.yml and feedback-learner.yml are BROKEN (issue #36) — they fail immediately with CLI error
- This means: issues resolved by merged PRs are NOT being auto-closed by watcher; stale agent-ready labels may accumulate
- Issues #33, #29, #28, #26 all have merged PRs but are NOT closed — watcher would normally catch this but is failing
- Issue #36 is the top priority fix; once merged, watcher will self-heal

## Research Saturation Note
All 5 research sources (3 core + 2 tier-0) have been unchanged for 3+ consecutive runs. Issue #31 (checksum caching) would reduce pointless API calls. Consider rotating to tier-1 or tier-2 next run.

## Metrics Snapshot
Period: 2026-03-15 to 2026-03-22 (first full week tracked)
- Total commits: 70+
- Stars: 1 | Forks: 0 | Adopters: 0
- Issues created this run: 1 (#36)
