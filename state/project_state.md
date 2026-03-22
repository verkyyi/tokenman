# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-22T07:40:00Z
Updated by: coder.yml (issue #23)

## Last Session
Action: coder.yml — fix issue #23 (watcher outcome health checks)

Done:
- Added responsibility #7 to watcher.yml prompt: pipeline stage outcome checks
  - Triage: re-trigger if issue >2h has no "Triaged by agentfolio triage agent" comment
  - Coder handoff: re-trigger triage if coder attempted but left issue with no label/PR
  - Reviewer: detect silent failures (0 reviews after run), re-trigger; escalate to needs-human on repeat failure
- Raised corrective actions limit 3→5 to accommodate additional checks
- Opened PR for issue #23 (needs-review — workflow YAML change)

In progress: PRs #19 (anti-sycophancy, closes #13), #20 (agentic security, closes #17), and new PR for #23 (watcher outcome checks) — all awaiting human review

## Open Items (priority order)
1. Issue #12: [BLOCKED — human] CLAUDE_CODE_OAUTH_TOKEN missing `workflows` OAuth scope — blocks all workflow YAML PRs and issue #8 Node.js upgrade. Fix: add PAT with `workflow` scope as WORKFLOW_PAT secret.
2. Issue #22: [agent-ready] Submit to hesreallyhim/awesome-claude-code (29k stars) — first growth action (from growth.yml)
3. PR #19: [awaiting human review] Anti-sycophancy guardrails for adversarial-review.md (gstack v0.9.9.0 pattern, closes #13)
4. PR #20: [awaiting human review] Agentic security patterns — supply chain hygiene + prompt injection defense (closes #17)
5. PR for #23: [awaiting human review] Watcher outcome health checks — triage/coder/reviewer stage verification
6. Issue #10: [needs-review label — awaiting human review] Last-updated badge user-friendly time
7. Issue #8: [BLOCKED by #12] Upgrade Node.js 20 actions before June 2026 deadline
8. Issue #5: [parked] Adopt structured review tables in skill output (gstack v0.9.7.0)
9. Profile page: 5/8 sections still unchecked — live stats, evolution timeline, capabilities inventory, architecture diagram, getting started guide
10. apps/profile content not yet populated — discover.yml or manual issue needed

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
KEY BLOCKER: CLAUDE_CODE_OAUTH_TOKEN lacks `workflows` OAuth scope — any coder task touching workflow YAML will fail at push. Human intervention needed (see issue #12: add PAT with `workflow` scope as WORKFLOW_PAT secret). Issue #21 (add DeerFlow to evolve.yml) is blocked by #12 — `agent-ready` label removed by watcher to stop retry loop.

- PRs #19 (closes #13) and #20 (closes #17) are open and awaiting human review — reviewer already ran for both
- Issue #22 is open and agent-ready — growth strategy: submit to awesome-claude-code listing
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
