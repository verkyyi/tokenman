# Project State
Last updated: 2026-03-23T08:07:42Z
Updated by: evolve.yml (self-evolution run)

## Last Session
Action: evolve.yml — self-evolution run. All 12 research sources unchanged since prior run (07:09Z). Trending +16 (3117 total). No new pipeline failures. Site content changes reviewed (hero copy, logo fix, SSL/CNAME) — all clean. Conditional steps skipped (hour 08). 0 issues created.

System health:
- Evolve: SEVERELY SATURATED (80% exceed max-turns=45) — lightweight gate deployed, workflows succeeding
- Watcher: OVERUTILIZED (71.4% exceed max-turns=30) — trending up from 66.7%
- Weekly Analysis: 1 FAILURE (06:26 stale branch) — issue #59 closed, fix deployed, awaiting next run
- Reviewer Agent: HEALTHY — succeeded at 06:06
- Feedback Learner: HEALTHY — succeeded at 07:38
- Coder: HEALTHY (avg 83%/40)
- Deploy: HEALTHY — succeeded at 07:50
- All other workflows: healthy

## Current Priorities (ordered)
1. **[PR]** PR #55: fix reviewer.yml state reset — APPROVED 8h+, awaiting human merge (workflow YAML)
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
- Stars: 1 | Forks: 0 | Adopters: 0

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
- PR #55 approved by reviewer — human merge needed for workflow YAML change (8h+ pending)
- analyze.yml stale branch bug fixed (issue #59 closed, fix deployed — awaiting next analyze run to confirm)
- Evolve severely saturated (80% exceed max-turns=45) — lightweight gate helps when sources unchanged but not when sources change; workflows still succeeding
- Watcher overutilized (71.4% exceed max-turns=30) — trending up, but completing work
- Feedback Learner healthy — succeeded 07:38, idle when no merged PRs (expected)
- Site content updated: hero headline now action-oriented, pac-man branding, broken logo removed, SSL/CNAME for tokenman.io
