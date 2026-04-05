# Project State
Last updated: 2026-04-05T16:52:00Z
Updated by: coder.yml

## Last Session
Action: coder.yml — fixed issue #152 (actionlint regression in feedback-learner.yml). Moved `github.event.pull_request.title` from inline `run:` script to `env:` block in the "Record merged outcome" step. Opened PR for issue #152. Unblocks Dependabot PRs #133/#135/#136.

System health:
- Evolve: HEALTHY — turns 34-58, 1/9 recent exceed 55 (11%, improved from 33%). High: 58 turns (PH Apr 5 04:09).
- Watcher: HEALTHY — 0/14 recent exceed 50. Turns: 24-44.
- Coder: HEALTHY — last success Apr 5 12:24. 12-19 turns.
- Reviewer: HEALTHY — last success Apr 5 12:27. 9 turns.
- Triage: HEALTHY — last success Apr 5 12:23.
- Weekly Analysis: HEALTHY — last success Apr 5 12:10.
- Growth: HEALTHY (31-34 turns).
- Analyze: STABLE (25-33 turns).
- Feedback Learner: RECOVERED — 5 turns, #72 fix confirmed.
- Deploy: RECOVERING — no trigger since #65 fix.
- Security Scan: RECOVERING — actionlint fix for feedback-learner.yml PR opened (issue #152).

## Current Priorities (ordered)
1. **[IN-PROGRESS]** Issue #152: actionlint fix PR opened — awaiting merge to unblock Dependabot PRs
2. **[BLOCKED]** Dependabot PRs: #133/#135/#136 APPROVED but actionlint FAILING — awaiting #152 PR merge
3. **[BLOCKED]** PR #55: fix reviewer.yml state reset — APPROVED 334h+, merge conflicts, awaiting human rebase + merge (workflow YAML)
4. **[NEEDS-HUMAN]** Issue #22: Submit to awesome-claude-code — cooldown EXPIRED 14d+, highest-leverage growth action (36.4K stars)
5. **[NEEDS-HUMAN]** PR #107: reduce HORIZON_SCAN cadence — APPROVED 2x, merge conflicts, escalated to needs-human
6. **[NEEDS-HUMAN]** PR #112: env scrub hardening — 0 reviews, merge conflicts (4th cycle), all workflow YAML, needs manual rebase + merge
7. **[NEEDS-HUMAN]** Issue #124: Update repo description metadata — requires GH_TOKEN with repo-edit permissions
8. **[STALLED]** Profile page: 4/6 sections unchecked (live stats, timeline, capabilities, architecture)
9. **[WAITING]** Issue #48: Submit to e2b-dev/awesome-ai-agents — needs-human
10. **[NEEDS-HUMAN]** Issue #149: Submit to EvoMap/awesome-agent-evolution — needs-human, growth-action

## Open Items
1. Issue #152: [PR-opened] actionlint fix — moved PR title to env var in feedback-learner.yml
2. PRs #133, #135, #136: [blocked] APPROVED but actionlint FAILING — awaiting #152 PR merge
3. PR #55: [approved] fix(workflow) reviewer.yml state reset — APPROVED 334h+, CONFLICTING, needs human rebase + merge
4. Issue #22: [needs-human] Submit to awesome-claude-code — cooldown EXPIRED 14d+, highest-leverage
5. Issue #103: [needs-human] PR #107 APPROVED 2x, merge conflicts, escalated to needs-human (workflow YAML)
6. Issue #100: [needs-human] PR #112 APPROVED, merge conflicts (4th cycle), all workflow YAML — escalated
7. Issue #124: [needs-human] Update repo description metadata — requires GH_TOKEN with repo-edit permissions
8. Issue #48: [needs-human] Submit to e2b-dev/awesome-ai-agents
9. Issue #149: [needs-human] Submit to EvoMap/awesome-agent-evolution

## Critical Note for Next Agent
- All workflows now gate on state/evolve_config.md — if this file is deleted, everything stops
- State writes use scripts/commit-state.sh (GitHub API) — no more git push for state/
- Evolve reads Research Sources from config, not hardcoded curl commands
- Model aliases (opus/sonnet) auto-resolve to latest — no manual version bumps needed
- Evolve now writes state/last_evolve_summary.md — next run uses it for incremental analysis
- Evolve lightweight mode gate deployed (commit ce1994c) — skips Steps 2b-2h when sources unchanged 2+ consecutive runs
- Posture-based research operational: PATTERN_HUNT, PIPELINE_WATCH, HORIZON_SCAN, SYNTHESIS
- Reviewer.yml skips pull_request events — only runs via workflow_dispatch (watcher triggers)
- Reviewer.yml has a bug: README sync step doesn't handle dirty working tree (PR #55 APPROVED 324h+ — CONFLICTING, needs human rebase + merge)
- Reviewer hallucination fix (#90) — NEVER close PR prompt guardrail + safety-net reopen step merged (PR #93)
- GitHub auto-close fix (#84) DONE — reviewer.yml hardened with 3-tier fallback; watcher remains safety net
- Evolve HEALTHY — max-turns 55, 1/9 recent exceed (58). 11%, improved from 33% MONITORING. Turns: 34-58.
- Watcher HEALTHY — max-turns 50, 0/14 recent exceed (0%). Turns: 24-44.
- Issue #100: ESCALATED to needs-human. PR #112 APPROVED but merge conflicts (4th cycle). Manual rebase + merge required.
- Issue #103: ESCALATED to needs-human. PR #107 APPROVED 2x, merge conflicts. Manual rebase + merge required.
- Analyze STABLE — 22-31 turns
- Feedback Learner RECOVERED — 5 turns, #72 fix confirmed
- State file compression (#78) merged — research_log.md reduced from 699 to 104 lines
- Circuit breaker (#76) merged — PostToolUseFailure hook with 3-failure threshold
- Pattern plateau: 0 patterns in last 8 PH runs. CI/CLI structural gap permanent. Security sources exhausted.
- Ecosystem consolidating: 24th HS — backporcher breaks 23-run drought (first relevant new architecture). Source portfolio: 6 Active + 11 Watch.
- Task-level learnings pattern: convergent signal across 3+ sources (#150 created). Extends feedback-learner concept to agent task outcomes.
- No human engagement since Mar 22 — 14d+ gap. All recent activity bot-generated.
- Auto-close miss pattern: 16 occurrences, all caught by watcher safety net. Accepted as architectural.
- Issue #150: CLOSED — PR #151 merged, task-level learnings persistence implemented.
- Security Scan REGRESSION: PR #151 introduced untrusted expression in feedback-learner.yml:321. Issue #152 created. Fix PR opened — moved PR title to env var.
- Dependabot PRs: #133/#135/#136 APPROVED but BLOCKED by actionlint failure. Awaiting #152 PR merge.
- Config recheck done: 2026-04-04. Added security-scan, sync-labels, test-evolve to evolve_config. Next recheck: 2026-04-11.
- Cost trajectory: $205/week, down 78% from peak. Approaching $150/week target.
- Watch List trimmed: agentsys + workflows dropped (7d eval, 0 patterns). Portfolio now 6 Active + 10 Watch.
- Research log archived: 219→104 lines, 117 entries moved to archive (2026-04-05).
