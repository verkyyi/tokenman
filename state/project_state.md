# Project State
Last updated: 2026-04-02T00:41:00Z
Updated by: evolve.yml

## Last Session
Action: evolve.yml — PATTERN_HUNT. Deep-dived claude-code v2.1.90 (perf+security, auto on upgrade), Citadel runtime-agnostic stack (multi-runtime abstraction, N/A for bash/markdown), everything-cc (CI cleanup, N/A). SHA scan: Active 4/7 changed, Watch 2/8 changed. Pattern plateau 28th PH. 0 issues created.

System health:
- Evolve: HEALTHY — 0/10 recent exceed 55 (0%). Turns: 31-49.
- Watcher: HEALTHY — 0/10 recent exceed 50 (0%). Turns: 25-40.
- Coder: HEALTHY — last success Apr 1 07:05. 23 turns.
- Reviewer: HEALTHY — last success Apr 1 07:08. 15 turns.
- Triage: HEALTHY — last success Apr 1 18:20.
- Weekly Analysis: HEALTHY — last success Apr 1 18:18.
- Growth: HEALTHY (29 turns).
- Analyze: STABLE (21-31 turns).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 264h+, awaiting human merge (workflow YAML)
2. **[NEEDS-HUMAN]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts, escalated to needs-human
3. **[NEEDS-HUMAN]** PR #112: env scrub hardening — APPROVED but merge conflicts (4th cycle), all workflow YAML, needs manual rebase + merge
4. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — 7-day cooldown EXPIRED 3+ days, highest-leverage growth action
5. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture)
6. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
7. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
8. **[DONE]** Source portfolio rebalance — completed Mar 27 SYNTHESIS. Citadel promoted, gstack demoted, 5 dropped.

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 264h+, needs human merge
2. Issue #100: [needs-human] PR #112 APPROVED, merge conflicts (4th cycle), all workflow YAML — escalated
3. Issue #103: [needs-human] PR #107 APPROVED 2x, merge conflicts, escalated to needs-human (workflow YAML)
4. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
5. Issue #127: [DONE] Adopt runner-guard CI/CD security scanning — PR #128 merged Apr 1 07:09, auto-closed by watcher
6. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
7. Issue #22: [needs-human] Submit to awesome-claude-code — cooldown EXPIRED 3+ days

## Week of Mar 24-31 Key Metrics
- Commits: 707 (690 state, 17 feat/fix)
- Issues resolved: 5 (#113, #116, #120, #122, #125)
- Issues created: 3 (#122, #124, #125)
- Agent log actions: ~107 (down from ~237 prev week — frequency reduction working)
- Workflow runs: evolve ~56, watcher ~84, growth ~7, analyze ~7, coder ~3, reviewer ~3, triage ~5
- Research entries: 137 across 14 Active + 7 Watch List sources
- Cost: ~$205/week ($29.30/day avg), down 26% from $273 prev week, 78% below pre-PR #111 peak
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: flat at 2 stars for 11d+; v0.4.0 released Apr 1 09:28 (9h old, too early to measure); #22 cooldown EXPIRED day 4+ (awesome-cc 35.4K accelerating +169/9h); #48 blocked needs-human; discussion #49 0 engagement 11d; bottleneck is 100% human engagement 10d+
- Pattern adoption: 1 new pattern in last 27 PATTERN_HUNT runs (runner-guard #127 broke 26-run plateau)
- Ecosystem consolidation: 17th consecutive HORIZON_SCAN with no new architectures
- Auto-close misses: 7 total (#113, #116, #120, #122, #125, #127), all caught by watcher — architectural, handled

## SYNTHESIS Cross-Run Observations (Apr 1)
1. **Security = productive research vein**: runner-guard broke 26-run PH plateau. claude-code v2.1.83-89 security releases are the most CI-relevant changes. #127 runner-guard DONE (full pipeline chain in 3h). #100 env scrub still needs-human. Future PH should weight security-focused sources.
2. **Human bottleneck critical**: 10d+ since Mar 22. 6 needs-human items, 3 PRs merge-conflicted. Growth 100% bottlenecked. All automated optimization paths exhausted.
3. **Research ROI declining**: 17 HS consolidation, 26 PH plateau (broken once). Valuable finds from niche/specialized sources, not volume. Consider further cadence reduction.

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 264h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve HEALTHY — max-turns 55, 0/10 exceed (0%). Turns: 31-49.
- Watcher HEALTHY — max-turns 50, 0/10 exceed (0%). Turns: 25-40. Frequency 2h (PR #111).
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Analyze STABLE — 28-33 turns
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau: 1 issue in 27 PH runs (runner-guard #127). CI/CLI structural gap still real.
- Ecosystem consolidating: 17 consecutive HS with 0 new architectures. Source portfolio stable at 7 Active + 8 Watch.
- No human engagement since Mar 22 — all recent activity bot-generated. 10d+ gap.
- Auto-close miss pattern: 7 occurrences (#113, #116, #120, #122, #125, #127), all caught by watcher safety net. Root cause: bot-to-bot merge race condition. Accepted as architectural.
- claude-code v2.1.89 latest: defer permission, autocompact thrash fix, TaskCreated hook, file_path absolute fix, memory leak fix. Major stability release.
- Cost trajectory: $205/week, down 78% from $134/day peak. Approaching $150/week target.
