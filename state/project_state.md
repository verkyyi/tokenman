# Project State
Last updated: 2026-03-24T01:54:48Z
Updated by: evolve.yml

## Last Session
Action: evolve.yml SYNTHESIS — analyzed 107 research_log entries + 31 learned intents + 7 open issues. 4 convergent signals: context compression (3 sources → issue #78), self-learning (strengthens #72/#76), skill format alignment (strengthens #66/#68), source activity resumes (awesome-claude-code + deer-flow have new SHAs after 6-run stale period). No new human intents since 2026-03-22.

System health:
- Evolve: SEVERELY SATURATED (structural, 90% exceed max-turns=45, stable)
- Watcher: NORMALIZED (healthy, all under 30)
- Coder: HEALTHY — succeeded at 22:49
- Reviewer: HEALTHY — succeeded at 22:52
- Triage: HEALTHY — succeeded at 22:47 (re-triggered for #66, #67, #68)
- Weekly Analysis: HEALTHY — succeeded at 00:19
- Growth: HEALTHY — succeeded at 18:16
- Analyze: HEALTHY — succeeded at 00:24
- Feedback Learner: FAILING — script injection in workflow YAML (#72, likely-agent-fixable)
- Deploy: RECOVERING — no run since #65 fix (no site-content push since)
- All other workflows: healthy

## Current Priorities (ordered)
1. **[FIX]** Issue #72: Feedback Learner script injection — likely-agent-fixable, awaiting triage
2. **[PR]** PR #71: unified label registry — needs-review, 0 formal reviews (approaching 1h)
3. **[PR]** PR #55: fix reviewer.yml state reset — APPROVED 25h+, awaiting human merge (workflow YAML)
4. **[TRIAGE]** Issue #68: Adopt SKILL.md quality standard — triage re-triggered
5. **[TRIAGE]** Issue #67: Adopt hooks-based guardrail enforcement — triage re-triggered
6. **[TRIAGE]** Issue #66: Package harness patterns as installable skills — triage re-triggered
7. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
8. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28

## Open Items
1. Issue #72: [pipeline-fix] Feedback Learner script injection — likely-agent-fixable, awaiting triage
2. PR #71: [needs-review] unified label registry — 0 formal reviews, approaching 1h threshold
3. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 25h+, needs human merge
4. Issue #68: [evolve-finding] SKILL.md quality standard — triage re-triggered
5. Issue #67: [evolve-finding] hooks-based guardrail enforcement — triage re-triggered
6. Issue #66: [evolve-finding] package harness as installable skills — triage re-triggered
7. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
8. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 2 Key Metrics
- Commits: 300+ (advancing with state commits)
- Features shipped: 21
- Issues created: ~32 | Issues closed: ~30
- Workflow runs: ~200+ (evolve dominant)
- Research sources monitored: 10 active + 10 watch list
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: +1 star since v0.1.0 release (now flat at 2); discussion #49 has 0 engagement after 39h; distribution issues #22/#48 blocked on needs-human; no action taken — next action when features accumulate for v0.2.0

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- "Commit state changes via API" step now also commits untracked state files
- Evolve lightweight mode gate now deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (issue #53 closed, PR #55 APPROVED — awaiting human merge)
- PR #55 approved by reviewer — human merge needed for workflow YAML change (24h+ pending)
- analyze.yml stale branch bug fixed (issue #59 closed, fix deployed — Weekly Analysis succeeded at 18:16, fully confirmed)
- #63 and #64 fully processed: evolve→triage→coder→PR→reviewer→merge. Closed by watcher (GitHub auto-close missed).
- Evolve severely saturated — structural, stable (90% exceed max-turns)
- Watcher NORMALIZED — healthy (all under 30 turns)
- Feedback Learner FAILING — script injection in workflow YAML (#72 created, likely-agent-fixable added)
- PR #71 has reviewer comment but 0 formal reviews — potential silent failure, watch at next run
- Site content updated: hero headline now action-oriented, pac-man branding, broken logo removed, SSL/CNAME for tokenman.io
- README minor inaccuracy: says "10 external sources across rotating tiers" — actually 12 sources, all checked every run (no rotation). Not issueworthy given existing #38 coverage.
