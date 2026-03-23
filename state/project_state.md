# Project State
Last updated: 2026-03-23T00:00:00Z
Updated by: analyze.yml (weekly analysis run)

## Last Session
Action: analyze.yml — Week 3 strategic analysis. 358 commits (236 state, 122 feature/fix), 76 agent-log actions, 25+ features shipped. Key finding: evolve runs hitting diminishing returns (60%+ no-change runs). Reviewer Agent checkout conflict is top active bug (issue #53, PR #55). Evolve max-turns partially resolved (PR #54) but post-merge data inconclusive.

System health:
- Reviewer Agent: FAILURE — state file checkout conflict in README sync (issue #53, PR #55 open)
- Evolve: POST-MERGE MONITORING — max-turns raised to 45 (PR #54), 1/3 post-merge runs exceeding limit
- Weekly Analysis: HEALTHY (fixed by PR #52)
- Feedback Learner: RECOVERED (intermittent shell parsing bug, self-recovering)
- Watcher: HEALTHY (post-30 max-turns working, 1 run at 97%)
- Coder: HEALTHY (avg 90% of max-turns)
- All other workflows: healthy

## Current Priorities (ordered)
1. **[ISSUE]** Issue #53: Reviewer Agent README sync state file conflict — PR #55 open for fix
2. **[OPTIMIZE]** Evolve diminishing returns — 60%+ of runs find no source changes; needs smarter skip logic or reduced frequency
3. **[OPTIMIZE]** Evolve max-turns post-merge monitoring — 1/3 runs still exceeding 45, may need further increase
4. **[STALE]** Profile page FEATURE_STATUS — 4/6 sections unchecked despite landing redesign shipped; needs reconciliation
5. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
6. **[WAITING]** Issue #22: Submit to awesome-claude-code — 7-day cooldown expires ~March 28

## Open Items
1. Issue #53: [pipeline-fix] Reviewer Agent README sync checkout conflict — PR #55 open
2. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents — needs-human
3. Issue #22: [needs-human] Submit to awesome-claude-code — waiting until ~March 28

## Week 3 Key Metrics
- Commits: 358 (236 state, 122 feature/fix)
- Agent log actions: 76 (30 evolve, 15 watcher, 12 coder, 4 feedback-learner, 2 cli, 1 growth, 1 analyze, 1 discover)
- Features shipped: 25+
- Issues created: ~30 | Issues closed: ~25
- Research entries: 382 (12 sources + trending + OpenAI blog)
- Evolve no-change rate: ~60% of runs
- Stars: 1 | Forks: 0 | Adopters: 0

## Week-over-Week Delta
- Commits: 358 (up from 260 in Week 2, +38%)
- Features: 25+ (up from 21, +19%)
- Agent actions: 76 (up from 56, +36%)
- Key shift: Week 2 was feature-building; Week 3 was optimization and operational maturity (max-turns tuning, incremental evolve, token utilization, human-activity detection)

## Closed Items (recent)
- Issue #51: CLOSED — PR #54 merged (evolve+watcher max-turns fix)
- Issue #47: CLOSED — PR #52 merged (analyze.yml clean-tree fix)
- PRs #19, #20: CLOSED by owner (anti-sycophancy, agentic security — not merged)

## Critical Note for Next Agent
- All workflows gate on state/evolve_config.md — if deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve writes state/last_evolve_summary.md — next run uses it for incremental analysis
- "Commit state changes via API" step also commits untracked state files
- Incremental evolve (PR #46) merged — max-turns raised to 45 (PR #54)
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (issue #53, PR #55)
- Stale research sources: godagoo (Feb 3), humanlayer (Jan 7) — candidate for pruning
- OpenAI blog source persistently Cloudflare-blocked — needs replacement or removal
