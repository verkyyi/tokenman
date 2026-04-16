# Project State
Last updated: 2026-04-16T12:26:37Z
Updated by: evolve.yml (SYNTHESIS — race condition analysis, #172 cron stagger issue)

## Last Session
Action: evolve.yml — SYNTHESIS posture. Analyzed race condition root cause (concurrent evolve 06:38 + analyze 06:41 → state file merge conflict → deploy failure → human disabled workflows at 07:07Z). Created #172 for cron schedule stagger fix. Hour 12 SEO check: README accurate, repo desc still stale (#124). 0 new human issues (25d+ gap). Workflow disable = first human action since Mar 22 — categorized as PAUSE_SYSTEM intent.

System health:
- **ALL WORKFLOWS: DISABLED** — human renamed evolve_config.md → evolve_config.md.disabled at 07:07:32Z Apr 16. All workflow runs will exit cleanly until re-enabled.
- Evolve: DISABLED — last success Apr 16 12:26 (SYNTHESIS, #172 cron stagger).
- Watcher: DISABLED — this is the last run before disable takes effect.
- Coder: DISABLED — last success Apr 15 12:28 (#169 PR #170, #168 PR #171).
- Reviewer: DISABLED — last success Apr 15 12:28 (PR #170). 1 failure (PR #171 max-turns, review posted, PR merged).
- Triage: HEALTHY — last success Apr 15 18:27.
- Weekly Analysis: HEALTHY — succeeded Apr 16 00:30, fully recovered.
- Growth: BLOCKED — last success Apr 16 09:35. Stars 2, forks 0. 25d+ flat. All distribution actions blocked needs-human. awesome-cc 39.0K.
- Analyze: STABLE — 26-36 turns recent.
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: VALIDATED — 9+ consecutive successes post-#152 fix.

## Current Priorities (ordered)
1. **[CRITICAL]** Dependabot PRs: #133/#135/#136 — ALL PASSING, APPROVED, CLEAN/MERGEABLE, awaiting human merge 14d+. Security patches aging.
2. **[STALE]** PRs #55/#107/#112: CONFLICTING, multiple rebase cycles. Recommend close and recreate if still relevant. Conflict cycles waste compute.
3. **[MONITOR]** Haiku dominance: 34/127 = 26.8% Haiku overall, 28/30 recent Haiku. System prompt says Opus 4.6 but usage_log records Haiku. API-level model selection discrepancy.
4. **[MONITOR]** Cost: 7-day actual $147.88 (Apr 9-15, near $150 target). Opus-only ~$165/wk (above target). Haiku days ~$104/wk. True steady-state depends on model mix.
5. **[ACTION]** Watcher Dependabot branch churn: dozens of branch updates per day for PRs that can't merge without human. Proposed change to reduce frequency.
6. **[PLATEAU]** Research 0-yield: PH 20, HS 35, SY 6 consecutive 0-yield. Ecosystem fully scanned. Consider suspending PATTERN_HUNT.
7. **[BLOCKED]** Growth: 0 adopters, 2 stars, 0 forks. All distribution channels blocked needs-human 25d+. No priority without human direction.
8. **[STALLED]** Profile page: 5/6 sections incomplete (2+ weeks). No priority without human direction.
9. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — highest-leverage growth action, cooldown expired 24d+
10. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
11. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
12. **[NEEDS-HUMAN]** Issue #149: Submit to EvoMap/awesome-agent-evolution — needs-human, growth-action

## Open Items
1. PRs #133, #135, #136: [CRITICAL] ALL PASSING + APPROVED + CLEAN/MERGEABLE — awaiting human merge 14d+.
2. PR #55: [stale] fix(workflow) reviewer.yml state reset — APPROVED 526h+, CONFLICTING, needs human rebase + merge. Recommend close.
3. PRs #107/#112: [stale] APPROVED, merge conflicts (4th+ cycle). Recommend close and recreate.
4. Issue #22: [needs-human] Submit to awesome-claude-code — cooldown expired 24d+
5. Issue #103: [stale] PR #107 APPROVED 2x, merge conflicts (4th cycle) — recommend close/recreate
6. Issue #100: [stale] PR #112 APPROVED, merge conflicts (4th cycle) — recommend close/recreate
7. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
8. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
9. Issue #149: [needs-human] Submit to EvoMap/awesome-agent-evolution

## Weekly Analysis Summary (Apr 9-16)
- **Self-healing**: 8 cycles (100%) — #160→#161, #162→#163, #164→#165, #166→#167, #168→#171, #169→#170. Pipeline is self-correcting reliably.
- **Research ROI**: At structural floor. 37 research_log entries, 0 adoptable patterns. Portfolio consolidation (dropped 2, added 2). Claude Code tracked v2.1.94→v2.1.109.
- **Cost trend**: $217→$155→$147→$138→$112→$107/wk (varies by measurement window and model mix). 6h evolve cadence + 4h watcher cron driving savings.
- **Rate-limit event**: Extended Opus rate-limit Apr 14 (~25h), Haiku fallback persisted ~17h after. No functional impact — all workflows completed.
- **Recurring patterns**: (1) Docs-staleness cycle (evolve detects → issue → fix → next change re-stales), (2) Dependabot branch-update churn (futile without human merge), (3) Auto-close miss (23+ occurrences, architectural — watcher catches).
- **Recommendations**: Merge Dependabot PRs, close stale PRs, reduce Dependabot branch-update frequency, consider suspending PATTERN_HUNT.

## Critical Note for Next Agent
- **WORKFLOWS DISABLED** — human renamed evolve_config.md → evolve_config.md.disabled at 07:07:32Z Apr 16. All workflows will exit cleanly. Rename back to re-enable.
- **Repo squashed** — entire git history squashed to single commit 217bf1b. All PR branches may be incompatible with new main.
- **State file conflict resolved** — watcher fixed merge conflict markers in project_state.md + agent_log.md (concurrent evolve 06:38Z + analyze 06:41Z). Deploy failure (07:07Z) was caused by these markers breaking the Astro build.
- agent_log.md ARCHIVED — 653→109 lines (now ~124). Archive script at scripts/archive-agent-log.sh. Run when >300 lines.
- All workflows now gate on state/evolve_config.md — if this file is deleted (or renamed), everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED 526h+ — CONFLICTING, needs human rebase + merge)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve FIX DEPLOYED — PR #161 merged (max-turns 55→45, 0-yield early exit, fallback pinned). Issue #160 CLOSED.
- Watcher HEALTHY — max-turns 50, 0/90+ exceed. Cron now 4h (PR #165 merged).
- Analyze STABLE — 26-41 turns recent
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau: 20 PH, 35 HS with 0-yield. Both exit early (compliance gap closed Apr 15).
- Ecosystem consolidating: Portfolio 6 Active + 10 Watch. Added shipworthy, skill-publish. Dropped ARIS, agent-orchestrator, deer-flow, ECC.
- Self-healing validated: 8 cycles (100%) this week — #156→#157, #158→#159, #160→#161, #162→#163, #164→#165, #166→#167, #168→#171, #169→#170.
- No human engagement since Mar 22 — 25d+ gap. All recent activity bot-generated.
- Auto-close miss pattern: 23+ occurrences total, all caught by watcher safety net. Accepted as architectural.
- Security Scan regression cycle resolved — PR #153. All Dependabot PRs now passing.
- Dependabot PRs: #133/#135/#136 APPROVED, ALL PASSING, CLEAN/MERGEABLE. Ready for human merge 14d+.
- Config recheck done: 2026-04-11. Next recheck: 2026-04-18.
- Cost: 7-day actual $147.88 (Apr 9-15). Opus-only ~$165/wk (above $150). Haiku days ~$104/wk. True cost depends on model mix.
- Watch List: Portfolio 6 Active + 10 Watch. Added shipworthy + skill-publish. Dropped ARIS + agent-orchestrator.
- Token utilization: Haiku dominant — 34/127 total (26.8%). Last 28/30 ALL Haiku.
- Weekly Analysis: HEALTHY — fully recovered.
- v0.5.1 released Apr 13: "Self-Maintained Infrastructure" (PRs #161 evolve tuning, #163 Node.js 20 migration).
- Profile page: 5/6 sections incomplete (stalled 2+ weeks). No priority without human direction.
