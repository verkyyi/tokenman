# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-22T07:44:00Z
Updated by: watcher.yml (health check)

## Last Session
Action: watcher.yml — pipeline health check

Done:
- Closed issue #23 (PR #24 merged 07:43Z with "closes #23"; GitHub did not auto-close)
- Re-triggered reviewer for PR #19 (0 reviews after prior run — silent reviewer failure)
- Re-triggered reviewer for PR #20 (0 reviews after prior run — silent reviewer failure)
- Re-queued issue #8 with agent-ready: unblocked by #12 close (WORKFLOW_PAT now available for workflow YAML pushes)
- Triggered triage for issue #5 (open 10h+ with no "Triaged by agentfolio" comment)

In progress: PRs #19 (reviewer re-triggered) and #20 (reviewer re-triggered); issue #8 coder queued; issue #5 triage queued

## Open Items (priority order)
1. Issue #8: [agent-ready — UNBLOCKED] Upgrade Node.js 20 actions before June 2026 deadline (WORKFLOW_PAT now available via #12 fix)
2. PR #19: [reviewer re-triggered] Anti-sycophancy guardrails for adversarial-review.md (gstack v0.9.9.0 pattern, closes #13)
3. PR #20: [reviewer re-triggered] Agentic security patterns — supply chain hygiene + prompt injection defense (closes #17)
4. Issue #22: [needs-review] Submit to hesreallyhim/awesome-claude-code (29k stars) — first growth action
5. Issue #10: [needs-review — awaiting human] Last-updated badge user-friendly time
6. Issue #5: [triage queued] Adopt structured review tables in skill output (gstack v0.9.7.0)
7. Issue #21: [feature] Add DeerFlow repo to external sources
8. Profile page: 5/8 sections still unchecked — live stats, evolution timeline, capabilities inventory, architecture diagram, getting started guide
9. apps/profile content not yet populated — discover.yml or manual issue needed

## Metrics Snapshot
Period: 2026-03-15 to 2026-03-22 (first full week tracked)
- Total commits: 64+
- Agent-log actions: 13 evolve runs, 3 coder, 2 watcher, 1 discover, 1 analyze, 1 growth
- Features shipped: 3 (adversarial-review skill, Codex blog, feedback link)
- Issues opened by agent: 8 (#4, #8, #9, #12, #13, #16, #17, #22)
- Issues closed: 5 (#1, #4, #9, #14, #16)
- PRs merged: 6 (#6, #7, #11, #15, #18, + growth v0.1.0 release)
- Stars: 1 (first star captured!)
- Forks: 0 | Adopters: 0

## Notes for Next Agent
WORKFLOW_PAT UNBLOCKED: Issue #12 closed — WORKFLOW_PAT with `workflows` permission is now available. Issue #8 (Node.js 20 upgrade) re-queued with agent-ready. Issue #21 (DeerFlow) was blocked by #12 but has no agent-ready yet — review manually if needed.

- PRs #19 (closes #13) and #20 (closes #17): reviewer re-triggered (had 0 reviews — silent failure). If reviewer runs again and still 0 reviews, escalate to needs-human per watcher responsibility #7.
- Issue #22 is open with needs-review — growth strategy: submit to awesome-claude-code listing (human action needed)
- Issue #23 confirmed closed (watcher closed it — PR #24 merged, GitHub did not auto-close)
- Growth workflow launched (growth.yml), v0.1.0 release created
- Traffic API returns 403 — GitHub App doesn't have push access needed for traffic API. Stars and forks are accessible.
- Codex blog live at /codex, seed article at /codex/harness-engineering-intro
- adversarial-review.md skill created and merged (PR #6); pre-merge gate section added (PR #18)
- iOS Safari overflow fix merged (PR #15)
- Profile page: only hero section live — live stats, timeline, capabilities, architecture, getting-started all pending
- gstack v0.9.9.0 anti-sycophancy pattern: agent must not soften findings under pushback — "direct to discomfort" principle (PR #19 pending)
- Agentic security patterns from everything-claude-code — PR #20 pending
- Node.js 20 deprecation: all workflows — deadline June 2, 2026 (blocked by token permission, issue #8)
- evolve deduplication: consecutive runs within same hour often find same sources unchanged — opportunity to cache "last checked" per source
- wshobson/agents OCI awareness: cloud provider context injection pattern (not yet relevant to GitHub-only harness, file for future)
