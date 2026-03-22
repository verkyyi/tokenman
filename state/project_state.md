# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-22T08:10:00Z
Updated by: coder.yml (fix issue #28)

## Last Session
Action: coder.yml — fix issue #28 (token utilization feedback loop)

Done:
- Created state/usage_log.md (append-only, 7-day rolling window)
- Phase 1 pilot: instrumented coder.yml, watcher.yml, evolve.yml with --output-format json > /tmp/claude_output.json + usage logging step
- Phase 2: added watcher responsibility #8 (token utilization analysis) — skips if <20 data lines; detects under/overutilization signals; creates max 1 optimization issue per run
- Phase 3 rollout: instrumented all 7 remaining workflows (reviewer, triage, analyze, claude-task, discover, feedback-learner, growth)
- Added dedicated usage log commit steps for reviewer.yml and triage.yml (had no state commit)
- Updated feedback-learner.yml to commit usage_log.md in both lesson/no-lesson paths
- Each logging step includes 7-day rolling truncation via awk date comparison
- JSON field extraction: model from modelUsage keys, total input tokens (input + cache_creation + cache_read), output_tokens, num_turns, total_cost_usd; all with "unknown" fallbacks
- Build passing (exit 0); FEATURE_STATUS updated
- Opened PR for issue #28 (needs-review)

In progress: PRs #19 (reviewer re-triggered) and #20 (reviewer re-triggered); issue #8 coder queued

## Open Items (priority order)
1. Issue #8: [agent-ready — UNBLOCKED] Upgrade Node.js 20 actions before June 2026 deadline (WORKFLOW_PAT now available via #12 fix)
2. PR #19: [reviewer re-triggered] Anti-sycophancy guardrails for adversarial-review.md (gstack v0.9.9.0 pattern, closes #13)
3. PR #20: [reviewer re-triggered] Agentic security patterns — supply chain hygiene + prompt injection defense (closes #17)
4. Issue #22: [needs-review] Submit to hesreallyhim/awesome-claude-code (29k stars) — first growth action
5. Issue #10: [needs-review — awaiting human] Last-updated badge user-friendly time
6. Issue #5: [PR opened — auto-merge] Structured findings table added to adversarial-review.md (closes #5)
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
