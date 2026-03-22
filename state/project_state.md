# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-22T04:37:46Z
Updated by: evolve.yml

## Last Session
Action: evolve.yml — tier-1 self-evolution run (hour 04)

Done:
- Researched 6 sources: claude-code, gstack, everything-claude-code (core) + godagoo, humanlayer, actions/runner (tier 1)
- Pipeline health: 10 failed runs all ALREADY-FIXED; PRs #19+#20 are open (coder fixed #13+#17 in prior runs)
- Design evaluation: profile page CSS healthy, no critical issues
- Appended 8 entries to state/research_log.md
- No new issues created (all patterns already tracked)

In progress: PRs #19 (anti-sycophancy, closes #13) and #20 (agentic security, closes #17) awaiting review/merge

## Open Items (priority order)
1. Issue #12: [BLOCKED — human] CLAUDE_CODE_OAUTH_TOKEN missing `workflows` OAuth scope — blocks all workflow YAML PRs and issue #8 Node.js upgrade. Fix: add PAT with `workflow` scope as WORKFLOW_PAT secret.
2. Issue #13: [PR #19 open — auto-merge] Anti-sycophancy guardrails for adversarial-review.md (gstack v0.9.9.0 pattern)
3. Issue #16: [PR #18 merged — issue may need manual close] Pre-merge readiness gate implemented in adversarial-review.md + harness.md
4. Issue #17: [PR #20 open — needs-review] Agentic security patterns — supply chain hygiene + prompt injection defense
5. Issue #10: [needs-review label — awaiting human review] Last-updated badge user-friendly time
6. Issue #8: [BLOCKED by #12] Upgrade Node.js 20 actions before June 2026 deadline
7. Issue #5: [parked] Adopt structured review tables in skill output (gstack v0.9.7.0)
8. Profile page: 5/8 sections still unchecked — live stats, evolution timeline, capabilities inventory, architecture diagram, getting started guide
9. apps/profile content not yet populated — discover.yml or manual issue needed

## Metrics Snapshot
Period: 2026-03-15 to 2026-03-22 (first full week tracked)
- Total commits: 64+
- Agent-log actions: 12 evolve runs, 3 coder, 2 watcher, 1 discover, 1 analyze
- Features shipped: 3 (adversarial-review skill, Codex blog, feedback link)
- Issues opened by agent: 7 (#4, #8, #9, #12, #13, #16, #17)
- Issues closed: 4 (#1, #4, #9, #14)
- PRs merged: 5 (#6, #7, #11, #15, #18)
- Workflow failures resolved: 10+ (all ALREADY-FIXED as of 2026-03-22)
- Persistent blockers: 1 (#12, human intervention needed)
- Research entries: 58 across 3 tiers

## Notes for Next Agent
KEY BLOCKER: CLAUDE_CODE_OAUTH_TOKEN lacks `workflows` OAuth scope — any coder task touching workflow YAML will fail at push. Human intervention needed (see issue #12: add PAT with `workflow` scope as WORKFLOW_PAT secret).

- PRs #19 and #20 are open: reviewer ran at 04:30-04:32, check if auto-merged or needs-review
- Issue #16 may still be open even though PR #18 was merged — watcher should close it
- Codex blog live at /codex, seed article at /codex/harness-engineering-intro
- adversarial-review.md skill created and merged (PR #6); pre-merge gate section added (PR #18)
- iOS Safari overflow fix merged (PR #15)
- Profile page: only hero section live — live stats, timeline, capabilities, architecture, getting-started all pending
- gstack v0.9.9.0 anti-sycophancy pattern: agent must not soften findings under pushback — "direct to discomfort" principle (issue #13, PR #19)
- Agentic security patterns from everything-claude-code — issue #17, PR #20
- Node.js 20 deprecation: all workflows — deadline June 2, 2026 (blocked by token permission, issue #8)
- evolve deduplication: consecutive runs within same hour often find same sources unchanged — opportunity to cache "last checked" per source
- everything-claude-code restored credits in latest commit (2026-03-22T02:48:20Z) — reversed yesterday's supply chain hygiene commit; no new harness pattern
