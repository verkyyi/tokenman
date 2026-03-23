# Project State
Last updated: 2026-03-23T22:47:00Z
Updated by: watcher.yml (health check)

## Last Session
Action: coder.yml — implement cross-model outside voice for reviewer agent (issue #64). Added Outside Voice protocol to skills/adversarial-review.md, secondary Sonnet subagent step to reviewer.yml (with tier-based skip for state-only PRs), tension detection and PR commenting, review log persistence to state/review_log.md. Build passes. Opened PR for issue #64.

System health:
- Evolve: SEVERELY SATURATED (structural, stable, 90% exceed max-turns=45)
- Watcher: NORMALIZED (healthy, 10% exceed 30)
- Weekly Analysis: HEALTHY — succeeded at 18:16
- Reviewer Agent: HEALTHY — succeeded at 06:06
- Feedback Learner: HEALTHY/IDLE — succeeded at 07:38
- Coder: HEALTHY (33/40 avg, 83%)
- Deploy: RECOVERING — 2 failures at 20:29+20:44 (#65 fix deployed, no run since ~2h)
- Growth: HEALTHY — succeeded at 18:16
- Analyze: HEALTHY — succeeded at 18:23
- All other workflows: healthy

## Current Priorities (ordered)
1. **[PR]** PR #55: fix reviewer.yml state reset — APPROVED 21h+, awaiting human merge (workflow YAML)
2. **[NEW]** Issue #68: Adopt SKILL.md quality standard — awaiting triage
3. **[NEW]** Issue #67: Adopt hooks-based guardrail enforcement — awaiting triage
4. **[NEW]** Issue #66: Package harness patterns as installable skills — awaiting triage
5. **[NEW]** Issue #64: Adopt cross-model outside voice for reviewer — triage re-triggered by watcher
6. **[NEW]** Issue #63: Investigate --bare flag for workflows — triage re-triggered by watcher
4. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
5. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28

## Open Items
1. PR #55: fix(workflow) reviewer.yml state reset — APPROVED 23h+, needs human merge
2. Issue #68: [evolve-finding] SKILL.md quality standard — awaiting triage
3. Issue #67: [evolve-finding] hooks-based guardrail enforcement — awaiting triage
4. Issue #66: [evolve-finding] package harness as installable skills — awaiting triage
5. Issue #64: [evolve-finding] cross-model outside voice — triage re-triggered
6. Issue #63: [evolve-finding] --bare flag for workflows — triage re-triggered
7. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
8. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 2 Key Metrics
- Commits: 300+ (advancing with state commits)
- Features shipped: 21
- Issues created: ~32 | Issues closed: ~30
- Workflow runs: ~200+ (evolve dominant)
- Research sources monitored: 12 + trending
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
- PR #55 approved by reviewer — human merge needed for workflow YAML change (20h+ pending)
- analyze.yml stale branch bug fixed (issue #59 closed, fix deployed — Weekly Analysis succeeded at 18:16, fully confirmed)
- Evolve severely saturated — structural, stable
- Watcher NORMALIZED — healthy
- Feedback Learner healthy — succeeded 07:38, idle when no merged PRs (expected)
- Site content updated: hero headline now action-oriented, pac-man branding, broken logo removed, SSL/CNAME for tokenman.io
- README minor inaccuracy: says "10 external sources across rotating tiers" — actually 12 sources, all checked every run (no rotation). Not issueworthy given existing #38 coverage.
