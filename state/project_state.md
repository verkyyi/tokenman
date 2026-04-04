# Project State
Last updated: 2026-04-04T18:20:00Z
Updated by: growth.yml

## Last Session
Action: growth.yml — growth strategy run. 1 action: created issue #149 (EvoMap/awesome-agent-evolution submission). Stars flat at 2 for 14d+. New target discovered by evolve horizon scan — they already monitor tokenman but haven't listed it in curated README. v0.4.0 81h old, 1 non-state commit since (not release-worthy). awesome-cc 36.4K accelerating. All growth actions blocked on human engagement.

System health:
- Evolve: HEALTHY — 2/9 exceed 55 (PH+HS both 56). Turns: 30-56. Monitoring trend.
- Watcher: HEALTHY — 0/13 exceed 50. Turns: 27-37.
- Coder: HEALTHY — last success Apr 4 12:22. 12-19 turns.
- Reviewer: HEALTHY — last success Apr 4 12:24. 9 turns.
- Triage: HEALTHY — last success Apr 4 12:21.
- Weekly Analysis: HEALTHY — last success Apr 4 12:10.
- Growth: HEALTHY (33-34 turns).
- Analyze: STABLE (20-31 turns).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: HEALTHY — 10+ consecutive successes, all Dependabot PR checks passing.

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 316h+, awaiting human merge (workflow YAML)
2. **[READY]** Dependabot PRs: #133/#135/#136 APPROVED + checks passing, CLEAN+MERGEABLE, branches updated, ready for human merge
3. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — 7-day cooldown EXPIRED 7+ days, highest-leverage growth action (36.2K stars, accelerating)
4. **[NEEDS-HUMAN]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts, escalated to needs-human
5. **[NEEDS-HUMAN]** PR #112: env scrub hardening — 0 reviews, merge conflicts (4th cycle), all workflow YAML, needs manual rebase + merge
6. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
7. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture)
8. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
9. **[NEW]** Issue #149: Submit to EvoMap/awesome-agent-evolution — niche (21★), perfect category fit, they already monitor us

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 316h+, needs human merge
2. PRs #133, #135, #136: [ready] APPROVED + checks passing, CLEAN+MERGEABLE, ready for human merge
3. Issue #22: [needs-human] Submit to awesome-claude-code — cooldown EXPIRED 7+ days, highest-leverage
4. Issue #103: [needs-human] PR #107 APPROVED 2x, merge conflicts, escalated to needs-human (workflow YAML)
5. Issue #100: [needs-human] PR #112 APPROVED, merge conflicts (4th cycle), all workflow YAML — escalated
6. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
7. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
8. Issue #149: [needs-review] Submit to EvoMap/awesome-agent-evolution — niche but perfect category fit, they already monitor us

## Weekly Analysis (Apr 4 — Week of Mar 28–Apr 4)

### Pipeline & Operations
- 543 commits (9 fix, 534 state). 163 agent_log entries.
- Workflow distribution: watcher 91 (56%), evolve 53 (32%), growth 16 (10%), reviewer 2, analyze 1.
- Pipeline EXCELLENT: 100h+ failure-free stretches. All workflows HEALTHY.
- 9 issues auto-created and auto-fixed (#125, #127, #129, #131, #137, #139, #141, #143, #145).
- Self-healing loop confirmed: watcher detects → triage → coder → PR → reviewer → merge → close.
- Cost: $29-31/day ($205/week), 78% below peak. Approaching $150/week target.

### Research & Discovery
- Security = only productive research vein. Broke 26-PH plateau via runner-guard (#127).
- Research ROI at structural floor: 6 consecutive PH with 0 patterns, 21+ HS with 0 new architectures.
- Source portfolio rebalanced: everything-cc + deer-flow demoted to Watch (0-pattern obs). New Watch: runner-guard, agentshield, agentsys, claude-code-workflows, ARIS.
- CI/CLI gap confirmed permanent — all major repos produce interactive-session patterns, not CI-harness patterns.

### Growth & Human Engagement
- 14d+ since last human activity (Mar 22). 0 human issues or intents.
- 5 needs-human issues (#22, #48, #100, #103, #124) + 3 Dependabot PRs (#133, #135, #136) + 3 legacy PRs (#55, #107, #112) all blocked.
- Growth flat: 2 stars, 0 forks, 0 adopters for 14d+.
- awesome-claude-code (#22) cooldown expired 6d+ — highest-leverage growth action remaining.

### Feature Progress
- Script Testing (#139): COMPLETED — BATS-Core tests for commit-state, archive-research-log, build-preamble.
- Security Scan: HEALTHY — 10+ consecutive successes after runner-guard adoption.
- Config recheck completed Apr 4: security-scan, sync-labels, test-evolve added to evolve_config.

### Recommendations
1. **Human merge PRs**: #55 (306h+ APPROVED), #133/#135/#136 (Dependabot, ready) — unblocks downstream.
2. **Submit awesome-claude-code #22**: cooldown expired, 36.2K stars accelerating — largest growth opportunity.
3. **Consider watcher frequency reduction**: 91 runs/week = 45% of cost. Reducing to every 3h saves ~$3/day.
4. **Evolve research cadence review**: Diminishing returns confirmed structural. Longer intervals between PH/HS would reduce cost without losing signal.
5. **Close stale PRs**: #107 and #112 have merge conflicts across 4 cycles — consider closing and recreating fresh.

## SYNTHESIS Cross-Run Observations (Apr 4)
1. **Research ROI at floor** (7th confirmation): 6 consecutive PH with 0 patterns across 12+ deep-dives. CI/interactive gap confirmed structural. 21 consecutive HS with 0 new architectures. System reliably observes but yields near-zero actionable patterns.
2. **Security niche exhausted**: Last 3 productive issues (#127, #129, #131) were security-adjacent from small niche repos. Both source repos (runner-guard, claude-agent-dispatch) have been deep-dived thoroughly. No remaining veins.
3. **Pipeline self-healing confirmed**: #137, #141, #143, #145 all created→fixed→closed within hours. Full cycle: watcher detects → creates issue → triage → coder → PR → reviewer → merge → watcher closes.
4. **Human bottleneck critical**: 14d+ since Mar 22. 5 needs-human items + 6 PRs blocked. Growth 100% bottlenecked. 0 human intents in 14d.
5. **Growth stalled**: 2 stars flat 14d+. 0 forks/adopters. All automated paths exhausted. awesome-cc 36.2K accelerating — opportunity cost growing daily.

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 314h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve HEALTHY — max-turns 55, 1/10 exceed (10%, latest PH 56 one-off). Turns: 30-56.
- Watcher HEALTHY — max-turns 50, 0/12 exceed (0%). Turns: 27-45.
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Analyze STABLE — 22-31 turns
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau: 0 patterns in last 6 PH runs. CI/CLI structural gap permanent. Security sources exhausted.
- Ecosystem consolidating: 22 consecutive HS with 0 new architectures. Source portfolio: 6 Active + 12 Watch.
- No human engagement since Mar 22 — 13d+ gap. All recent activity bot-generated.
- Auto-close miss pattern: 15 occurrences, all caught by watcher safety net. Accepted as architectural.
- Security Scan HEALTHY: #141/#143/#145 all fixed. 10+ consecutive successes. All 3 Dependabot PRs passing checks.
- Dependabot PRs: #133/#135/#136 APPROVED + checks passing, CLEAN+MERGEABLE, ready for human merge.
- Config recheck done: 2026-04-04. Added security-scan, sync-labels, test-evolve to evolve_config. Next recheck: 2026-04-11.
- Cost trajectory: $205/week, down 78% from peak. Approaching $150/week target.
