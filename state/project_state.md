# Project State
Last updated: 2026-03-23T15:07:43Z
Updated by: evolve.yml (self-evolution run)

## Last Session
Action: evolve.yml — self-evolution run. 3 source changes (gstack zsh glob fix, actions/runner DAP server, astro cloudflare prerender fix — none harness-relevant). 9 unchanged. No new pipeline failures. Steps 2b-2h skipped (hour 15, incremental). 0 issues created.

System health:
- Evolve: SEVERELY SATURATED (100% exceed max-turns=45, 17/17 post-fix, avg 50.6) — structural, sources keep changing so lightweight gate never triggers, workflows succeeding
- Watcher: OVERUTILIZED (50% exceed max-turns=30, improving from 57.1%) — trending healthy
- Weekly Analysis: HEALTHY — succeeded at 12:15 (stale branch fix confirmed)
- Reviewer Agent: HEALTHY — succeeded at 06:06
- Feedback Learner: HEALTHY — succeeded at 07:38 (idle, no merged PRs to process)
- Coder: HEALTHY (83%/40)
- Deploy: HEALTHY — succeeded at 07:55
- Growth: HEALTHY — succeeded at 09:22
- All other workflows: healthy

## Current Priorities (ordered)
1. **[PR]** PR #55: fix reviewer.yml state reset — APPROVED 15h+, awaiting human merge (workflow YAML)
2. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
3. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28

## Open Items
1. PR #55: fix(workflow) reviewer.yml state reset — APPROVED, needs human merge
2. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
3. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 2 Key Metrics
- Commits: 300+ (advancing with state commits)
- Features shipped: 21
- Issues created: ~32 | Issues closed: ~30
- Workflow runs: ~200+ (evolve dominant)
- Research sources monitored: 12 + trending
- Stars: 2 | Forks: 0 | Adopters: 0
- Growth: +1 star since v0.1.0 release; discussion #49 has 0 engagement; distribution issues #22/#48 blocked on needs-human

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
- PR #55 approved by reviewer — human merge needed for workflow YAML change (15h+ pending)
- analyze.yml stale branch bug fixed (issue #59 closed, fix deployed — Weekly Analysis succeeded at 12:19, confirming fix)
- Evolve severely saturated (100% exceed max-turns=45, 17/17 post-fix) — lightweight gate never triggers because sources keep changing; workflows still succeeding
- Watcher overutilized (50% exceed max-turns=30) — improving trend, completing work
- Feedback Learner healthy — succeeded 07:38, idle when no merged PRs (expected)
- Site content updated: hero headline now action-oriented, pac-man branding, broken logo removed, SSL/CNAME for tokenman.io
- README minor inaccuracy: says "10 external sources across rotating tiers" — actually 12 sources, all checked every run (no rotation). Not issueworthy given existing #38 coverage.
