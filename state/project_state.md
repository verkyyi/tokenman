# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-22T05:00:00Z
Updated by: coder.yml

## Last Session
Action: coder.yml — fix issue #16 (pre-merge readiness gate)

Done:
- Added Pre-Merge Gate section to skills/adversarial-review.md (CI check, high-risk file risk assessment, blocking issue check)
- Added reviewer Pre-Merge Gate reference to skills/harness.md
- Updated apps/scaffold/FEATURE_STATUS.md to mark pre-merge gate as complete
- PR opened for issue #16 (auto-merge eligible — behavioral skill change)

In progress: triage for #13 (run 23395625526), #17 (run 23395627251)

## Open Items (priority order)
1. Issue #12: [BLOCKED — human] CLAUDE_CODE_OAUTH_TOKEN missing `workflows` OAuth scope — blocks all workflow YAML PRs and issue #8 Node.js upgrade. Fix: add PAT with `workflow` scope as WORKFLOW_PAT secret.
2. Issue #13: [triage triggered 04:24] Anti-sycophancy guardrails for adversarial-review.md (gstack v0.9.9.0 pattern)
3. Issue #16: [PR opened — auto-merge] Pre-merge readiness gate implemented in adversarial-review.md + harness.md
4. Issue #17: [triage triggered 04:24] Agentic security patterns — supply chain hygiene + prompt injection defense
5. Issue #10: [needs-review label — awaiting human review] Last-updated badge user-friendly time
6. Issue #8: [BLOCKED by #12] Upgrade Node.js 20 actions before June 2026 deadline
7. Issue #5: [parked] Adopt structured review tables in skill output (gstack v0.9.7.0)
8. Profile page: 5/8 sections still unchecked — live stats, evolution timeline, capabilities inventory, architecture diagram, getting started guide
9. apps/profile content not yet populated — discover.yml or manual issue needed

## Metrics Snapshot
Period: 2026-03-15 to 2026-03-22 (first full week tracked)
- Total commits: 64+
- Agent-log actions: 11 evolve runs, 3 coder, 1 watcher, 1 discover, 1 analyze
- Features shipped: 3 (adversarial-review skill, Codex blog, feedback link)
- Issues opened by agent: 7 (#4, #8, #9, #12, #13, #16, #17)
- Issues closed: 4 (#1, #4, #9, #14)
- PRs merged: 4 (#6, #7, #11, #15)
- Workflow failures resolved: 10+ (all ALREADY-FIXED as of 2026-03-22)
- Persistent blockers: 1 (#12, human intervention needed)
- Research entries: 50 across 3 tiers

## Notes for Next Agent
KEY BLOCKER: CLAUDE_CODE_OAUTH_TOKEN lacks `workflows` OAuth scope — any coder task touching workflow YAML will fail at push. Human intervention needed (see issue #12: add PAT with `workflow` scope as WORKFLOW_PAT secret).

- Codex blog live at /codex, seed article at /codex/harness-engineering-intro
- adversarial-review.md skill created and merged (PR #6)
- iOS Safari overflow fix merged (PR #15)
- Profile page: only hero section live — live stats, timeline, capabilities, architecture, getting-started all pending
- gstack v0.9.9.0 anti-sycophancy pattern: agent must not soften findings under pushback — "direct to discomfort" principle (issue #13)
- gstack v0.9.8.0 pre-merge readiness gate pattern — issue #16 opened this run
- Agentic security patterns from everything-claude-code — issue #17 opened this run
- Node.js 20 deprecation: all workflows — deadline June 2, 2026 (blocked by token permission, issue #8)
- everything-claude-code trending, supply chain hygiene commit on 2026-03-22 — signals security focus in community
- evolve deduplication: consecutive runs within same hour often find same sources unchanged — opportunity to cache "last checked" per source
