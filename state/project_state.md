# Project State
Last updated: 2026-03-31T15:34:17Z
Updated by: evolve.yml (SYNTHESIS)

## Last Session
Action: evolve.yml SYNTHESIS — system at structural equilibrium. Pattern plateau 24th, ecosystem consolidation 16th, human disengaged 10d+, pipeline 52h+ failure-free. 4/7 Active + 1/7 Watch SHAs changed (churn, no patterns). 0 issues created.

System health:
- Evolve: HEALTHY — 0/10 recent exceed 55 (0%). Turns: 27-54. Note: 54-turn PW run at 12:32 (98% of max) — single outlier.
- Watcher: HEALTHY — 0/15 recent exceed 50 (0%). Turns: 26-35.
- Coder: HEALTHY — last success Mar 29 14:49. 12 turns.
- Reviewer: HEALTHY — last success Mar 29 14:52. 11 turns.
- Triage: HEALTHY — last success Mar 31 09:27.
- Weekly Analysis: HEALTHY — last success Mar 31 12:19.
- Growth: HEALTHY (24 turns).
- Analyze: STABLE (25-33 turns).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 230h+, awaiting human merge (workflow YAML)
2. **[NEEDS-HUMAN]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts, escalated to needs-human
3. **[NEEDS-HUMAN]** PR #112: env scrub hardening — APPROVED but merge conflicts (4th cycle), all workflow YAML, needs manual rebase + merge
4. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — 7-day cooldown EXPIRED 3+ days, highest-leverage growth action
5. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture)
6. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
7. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
8. **[DONE]** Source portfolio rebalance — completed Mar 27 SYNTHESIS. Citadel promoted, gstack demoted, 5 dropped.

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 230h+, needs human merge
2. Issue #100: [needs-human] PR #112 APPROVED, merge conflicts (4th cycle), all workflow YAML — escalated
3. Issue #103: [needs-human] PR #107 APPROVED 2x, merge conflicts, escalated to needs-human (workflow YAML)
4. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
5. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
6. Issue #22: [needs-human] Submit to awesome-claude-code — cooldown EXPIRED 3+ days

## Week of Mar 24-31 Key Metrics
- Commits: 707 (690 state, 17 feat/fix)
- Issues resolved: 5 (#113, #116, #120, #122, #125)
- Issues created: 3 (#122, #124, #125)
- Agent log actions: ~107 (down from ~237 prev week — frequency reduction working)
- Workflow runs: evolve ~56, watcher ~84, growth ~7, analyze ~7, coder ~3, reviewer ~3, triage ~5
- Research entries: 137 across 14 Active + 7 Watch List sources
- Cost: ~$205/week ($29.30/day avg), down 26% from $273 prev week, 78% below pre-PR #111 peak
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars for 10d+; v0.3.0 120h old; #22 cooldown EXPIRED day 3+ (awesome-cc 34.7K accelerating); #48 blocked needs-human; bottleneck is 100% human engagement 10d+
- Pattern adoption: 0 new patterns in 24 consecutive PATTERN_HUNT runs (structural plateau — CI/CLI gap)
- Ecosystem consolidation: 16th consecutive HORIZON_SCAN with no new architectures
- Auto-close misses: 6 total (#113, #116, #120, #122, #125), all caught by watcher — architectural, handled

## Weekly Analysis Recommendations
1. Merge PR #55 — only blocker requiring human action, recurring reviewer state bugs, approved 226h+
2. Rebase + merge PR #107 — APPROVED 2x, reduces HORIZON_SCAN cost (needs rebase)
3. Rebase + merge PR #112 — APPROVED, env scrub hardening for all workflows (needs rebase)
4. Submit to awesome-claude-code (#22) — highest-leverage growth action, cooldown expired 3+ days
5. Reduce PATTERN_HUNT cadence — 23 consecutive plateaus, structural CI/CLI gap, diminishing ROI
6. Unblock profile page — 4/6 sections stalled, no progress this week
7. Monitor cost trend — $205/week, approaching $150 baseline target at current trajectory
8. Consider dropping discover workflow — SKIP in config, single-project repo
9. Address human disengagement — 10d+ no human activity, all 6 open items blocked on human action, growth 100% bottlenecked

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 226h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve HEALTHY — max-turns 55, 0/10 post-reduction exceed (0%). Turns: 27-54. Note: 54-turn PW outlier at 12:32.
- Watcher HEALTHY — max-turns 50, 0/15 exceed (0%). Turns: 26-35. Frequency 2h (PR #111).
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Analyze STABLE — 28-33 turns
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau confirmed structural: CI-cron harness vs CLI/interactive sources. 24 consecutive 0-issue PH runs.
- Ecosystem consolidating: 16 consecutive HS with 0 new architectures. Source portfolio stable at 7 Active + 7 Watch.
- No human engagement since Mar 22 — all recent activity bot-generated. 10d+ gap.
- Auto-close miss pattern: 6 occurrences, all caught by watcher safety net. Root cause: bot-to-bot merge race condition. Accepted as architectural.
- claude-code v2.1.88 latest: PermissionDenied hook, StructuredOutput fix, prompt cache fix, nested CLAUDE.md re-injection. Low CI impact.
- Cost trajectory: $205/week, down 78% from $134/day peak. Approaching $150/week target.
