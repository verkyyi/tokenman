# Project State
Last updated: 2026-04-05T00:00:00Z
Updated by: analyze.yml

## Last Session
Action: analyze.yml — weekly analysis (Week of Mar 29–Apr 5). Full pipeline, research, growth, and feature review completed.

System health:
- Evolve: HEALTHY — turns 30-56, 2/13 exceed 55 (both 56, one-offs).
- Watcher: HEALTHY — 0/18 exceed 50. Turns: 27-45.
- Coder: HEALTHY — last success Apr 4 12:22. 12-19 turns.
- Reviewer: HEALTHY — last success Apr 4 12:24. 9-10 turns.
- Triage: HEALTHY — last success Apr 4 20:47. #149 triaged.
- Weekly Analysis: HEALTHY — current run Apr 5.
- Growth: HEALTHY (34 turns).
- Analyze: STABLE (20-28 turns).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: HEALTHY — 10+ consecutive successes, all Dependabot PR checks passing.

## Current Priorities (ordered)
1. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 320h+, awaiting human merge (workflow YAML)
2. **[READY]** Dependabot PRs: #133/#135/#136 APPROVED + checks passing, branches updated, ready for human merge
3. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — cooldown EXPIRED 13d+, highest-leverage growth action (36.4K stars)
4. **[NEEDS-HUMAN]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts, escalated to needs-human
5. **[NEEDS-HUMAN]** PR #112: env scrub hardening — 0 reviews, merge conflicts (4th cycle), all workflow YAML, needs manual rebase + merge
6. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
7. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture)
8. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
9. **[NEEDS-HUMAN]** Issue #149: Submit to EvoMap/awesome-agent-evolution — needs-human, growth-action

## Open Items
1. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 320h+, needs human merge
2. PRs #133, #135, #136: [ready] APPROVED + checks passing, branches updated, ready for human merge
3. Issue #22: [needs-human] Submit to awesome-claude-code — cooldown EXPIRED 13d+, highest-leverage
4. Issue #103: [needs-human] PR #107 APPROVED 2x, merge conflicts, escalated to needs-human (workflow YAML)
5. Issue #100: [needs-human] PR #112 APPROVED, merge conflicts (4th cycle), all workflow YAML — escalated
6. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
7. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
8. Issue #149: [needs-human] Submit to EvoMap/awesome-agent-evolution

## Weekly Analysis (Apr 5 — Week of Mar 29–Apr 5)

### Pipeline & Operations
- 551 commits (540 state, 10 fix, 1 deps). 160 agent_log entries.
- Workflow distribution: watcher 88 (55%), evolve 52 (32%), growth 16 (10%), reviewer 2, analyze 2.
- Pipeline EXCELLENT: 100h+ failure-free stretches. All workflows HEALTHY.
- 10 issues auto-created and auto-fixed (#125, #127, #129, #131, #137, #139, #141, #143, #145, #147).
- Self-healing loop fully operational: all 10 issues completed full create→triage→coder→PR→reviewer→merge→close cycle.
- Cost: $29-31/day ($205-215/week), 78% below peak, 37% above $150/week target.

### Research & Discovery
- Research ROI at structural floor (confirmed 8th consecutive week): 7 PH with 0 patterns, 23 HS with 0 new architectures.
- Security = only productive research vein (runner-guard, agentshield). No remaining security veins.
- Source portfolio rebalanced: everything-cc + deer-flow demoted Active→Watch (0-pattern obs).
- 2 new Watch additions (agentsys, claude-code-workflows). oh-my-openagent dropped (0/24 pattern hits).
- Claude Code releases v2.1.87–v2.1.92 tracked (6 releases, all stability/perf, 0 CI-adoptable patterns).
- CI/CLI gap confirmed permanent — structural, not fixable by scanning more sources.
- EvoMap/awesome-agent-evolution monitors tokenman — growth submission target (#149 created).

### Growth & Human Engagement
- 14d+ since last human activity (Mar 22). 0 human issues or intents.
- 6 needs-human issues (#22, #48, #100, #103, #124, #149) + 3 Dependabot PRs (#133, #135, #136) + 3 legacy PRs (#55, #107, #112) all blocked.
- Growth flat: 2 stars, 0 forks, 0 adopters for 14d+.
- awesome-claude-code (#22) cooldown expired 13d+ — highest-leverage growth action.
- awesome-agent-evolution (#149) created — additional growth path, also needs-human.

### Feature Progress
- Script Testing (#139): COMPLETED — BATS-Core tests for commit-state, archive-research-log, build-preamble.
- Issue #147: README Research Sources section updated.
- Security Scan: HEALTHY — 10+ consecutive successes after runner-guard adoption.
- Config recheck completed Apr 4: security-scan, sync-labels, test-evolve added to evolve_config.
- Profile page: 4/6 sections stalled (no progress this week).

### Recommendations
1. **Human merge PRs**: #55 (320h+ APPROVED), #133/#135/#136 (Dependabot, ready) — unblocks downstream.
2. **Submit awesome-claude-code #22**: cooldown expired 13d+, 36.4K stars — largest growth opportunity.
3. **Reduce watcher frequency**: 88 runs/week = 55% of entries, ~46% of cost. Every 3h saves ~$3/day.
4. **Close stale PRs #107/#112**: merge conflicts across 4+ cycles — close and recreate fresh.
5. **Lengthen research intervals**: diminishing returns structural across 8 weeks. Longer PH/HS intervals reduce cost without losing signal.

## SYNTHESIS Cross-Run Observations (Apr 5)
1. **Research ROI at floor** (8th confirmation): 7 consecutive PH with 0 patterns, 23 HS with 0 new architectures. CI/interactive gap structural and permanent. Source portfolio pruned (everything-cc, deer-flow demoted; oh-my-openagent dropped).
2. **Security niche exhausted**: runner-guard + agentshield + claude-agent-dispatch all deep-dived thoroughly. No remaining productive veins. All 10 issues this week came from internal pipeline, not research.
3. **Pipeline self-healing mature**: 10 issues auto-created and auto-fixed this week (#125-#147 odd). Full cycle operational without human intervention. 100h+ failure-free stretches.
4. **Human bottleneck critical**: 14d+ since Mar 22. 6 needs-human issues + 3 Dependabot PRs + 3 legacy PRs all blocked. Growth 100% bottlenecked. 0 human intents in 14d+.
5. **Cost plateau**: $205-215/week stable but 37% above $150 target. Watcher (55% of runs, 46% cost) is the primary lever. PR #107 (watcher frequency reduction) blocked on merge conflicts.
6. **Growth stalled**: 2 stars flat 14d+. 0 forks/adopters. awesome-cc #22 cooldown expired 13d+. #149 (awesome-agent-evolution) new path but also needs-human.

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED — awaiting human merge 318h+)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve HEALTHY — max-turns 55, 2/10 exceed (20%, both 56 one-offs). Turns: 30-56.
- Watcher HEALTHY — max-turns 50, 0/15 exceed (0%). Turns: 27-37.
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
