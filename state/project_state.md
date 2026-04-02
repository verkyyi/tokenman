# Project State
Last updated: 2026-04-02T16:55:00Z
Updated by: watcher.yml

## Last Session
Action: watcher.yml — health check. 2 corrective actions: re-triggered triage for #137 (>2h old, no triage comment); triggered reviewer for #136 (Dependabot deploy-pages bump, >4h old, 0 reviews). PR #134 merged (upload-pages-artifact v3→v4). PR #133 reviewed+approved but needs human merge (workflows permission). PR #135 reviewed with concerns (checkout v6 may not exist). Watcher first breach of 50-turn threshold (52 turns at 14:57, 1/10). 5 needs-human held. No needs-human unblocked by recent closes.

System health:
- Evolve: MONITOR — 1/10 recent exceed 55 (10%). Turns: 31-65.
- Watcher: MONITOR — 1/10 recent exceed 50 (52 turns at 14:57, first breach). Turns: 26-52.
- Coder: HEALTHY — last success Apr 2 12:54. 19 turns.
- Reviewer: HEALTHY — last success Apr 2 14:54. 10-19 turns.
- Triage: HEALTHY — last success Apr 2 12:53.
- Weekly Analysis: HEALTHY — last success Apr 2 12:18.
- Growth: HEALTHY (37 turns).
- Analyze: STABLE (21-27 turns).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: BROKEN — runner-guard checksum verification failure on all branches (#137).

## Current Priorities (ordered)
1. **[NEW]** Issue #137: runner-guard checksum failure — blocks all PR security scans (pipeline-fix, likely-agent-fixable)
2. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 278h+, awaiting human merge (workflow YAML)
3. **[NEEDS-HUMAN]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts, escalated to needs-human
4. **[NEEDS-HUMAN]** PR #112: env scrub hardening — APPROVED but merge conflicts (4th cycle), all workflow YAML, needs manual rebase + merge
5. **[IN-REVIEW]** PRs #133, #135, #136: Dependabot GHA bumps — #134 merged; #133 approved, needs human merge; #135 reviewed with concerns; #136 reviewer triggered
6. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — 7-day cooldown EXPIRED 3+ days, highest-leverage growth action
7. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture)
8. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
9. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions

## Open Items
1. Issue #137: [new] runner-guard checksum failure — blocks all PR security scans, pipeline-fix, likely-agent-fixable
2. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 278h+, needs human merge
3. Issue #100: [needs-human] PR #112 APPROVED, merge conflicts (4th cycle), all workflow YAML — escalated
4. Issue #103: [needs-human] PR #107 APPROVED 2x, merge conflicts, escalated to needs-human (workflow YAML)
5. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
6. PRs #133, #135, #136: [in-review] Dependabot GHA bumps — #134 merged; #133 approved needs human merge; #135 flagged concerns; #136 reviewer triggered
7. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
8. Issue #22: [needs-human] Submit to awesome-claude-code — cooldown EXPIRED 3+ days

## Week of Mar 24-31 Key Metrics
- Commits: 707 (690 state, 17 feat/fix)
- Issues resolved: 5 (#113, #116, #120, #122, #125)
- Issues created: 3 (#122, #124, #125)
- Agent log actions: ~107 (down from ~237 prev week — frequency reduction working)
- Workflow runs: evolve ~56, watcher ~84, growth ~7, analyze ~7, coder ~3, reviewer ~3, triage ~5
- Research entries: 137 across 14 Active + 7 Watch List sources
- Cost: ~$205/week ($29.30/day avg), down 26% from $273 prev week, 78% below pre-PR #111 peak
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars for 12d+; v0.4.0 24h old (1 ShellCheck fix since — no release candidate); #22 cooldown EXPIRED day 5+ (awesome-cc 35.7K accelerating +243/15h); #48 blocked needs-human; discussion #49 0 engagement 11.6d; bottleneck is 100% human engagement 11d+
- Pattern adoption: 2 patterns in last 31 PATTERN_HUNT runs (#127, #131). Security-adjacent patterns only productive vein.
- Ecosystem consolidation: 19th consecutive HORIZON_SCAN with no new architectures
- Auto-close misses: 9 total (#113, #116, #120, #122, #125, #127, #129, #131), all caught by watcher — architectural, handled

## SYNTHESIS Cross-Run Observations (Apr 2)
1. **Security = only productive research vein** (5th confirmation): 3/4 most recent issues (#127, #129, #131) security-adjacent. Small niche repos (runner-guard 6 stars, claude-agent-dispatch 2 stars) dramatically outperform large popular repos. Pattern yield inversely correlated with repo popularity.
2. **Source portfolio rebalanced**: Demoted everything-cc (13+ consecutive 0-pattern) and deer-flow (19+ consecutive 0-pattern) from Active to Watch. Active: 6, Watch: 11. High-churn repos with wrong stack produce noise, not signal.
3. **Human bottleneck critical**: 11d+ since Mar 22. 6 needs-human items. Growth 100% bottlenecked. All automated optimization paths exhausted.
4. **Research ROI declining**: 19 HS consolidation, 31 PH runs with only 2 patterns. Valuable finds exclusively from niche/specialized/architecturally-similar sources.

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 268h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve MONITOR — max-turns 55, 1/10 exceed (10%). Turns: 31-65. Latest HS spike from claude-agent-dispatch deep-dive.
- Watcher MONITOR — max-turns 50, 1/10 exceed (52 turns at 14:57, first breach). Turns: 26-52. Frequency 2h (PR #111).
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Analyze STABLE — 28-33 turns
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau partially broken: 2 issues in 31 PH runs (#127, #131). CI/CLI structural gap still real. Security sources = highest yield.
- Ecosystem consolidating: 19 consecutive HS with 0 new architectures. Source portfolio rebalanced: 6 Active + 11 Watch (demoted everything-cc, deer-flow).
- No human engagement since Mar 22 — all recent activity bot-generated. 10d+ gap.
- Auto-close miss pattern: 9 occurrences (#113, #116, #120, #122, #125, #127, #129, #131), all caught by watcher safety net. Root cause: bot-to-bot merge race condition. Accepted as architectural.
- Security Scan BROKEN: runner-guard v2.5.2 checksum verification failure on all branches. Issue #137 created (pipeline-fix, likely-agent-fixable). Blocks all PR security checks.
- Dependabot PRs: #133 (setup-node v4→v6, approved, needs human merge), #134 (upload-pages-artifact v3→v4, MERGED), #135 (checkout v4→v6, reviewed with concerns), #136 (deploy-pages v4→v5, reviewer triggered).
- claude-code v2.1.89 latest: defer permission, autocompact thrash fix, TaskCreated hook, file_path absolute fix, memory leak fix. Major stability release.
- Cost trajectory: $205/week, down 78% from $134/day peak. Approaching $150/week target.
