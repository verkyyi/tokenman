# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-22T08:28:00Z
Updated by: coder.yml (fix issue #33 — human intent learning, PR close handling, interaction guide)

## Last Session
Action: coder.yml — implemented issue #33 (human intent learning, PR close handling, interaction guide)

Done:
- feedback-learner.yml: added `pull_request: [closed]` trigger + rejection handling (re-adds agent-ready to linked issue, posts rejection context, re-triggers coder via existing RETRIGGER_CODER action); merged PRs skipped via job if condition
- coder.yml: added issue comments fetch (`gh issue view --json comments`) to "Build coder prompt" step so re-triggered coders see rejection context
- evolve.yml: added Step 2f Human Intent Analysis between 2e and 3 (query human-created issues, categorize intent, append to state/learned_intents.md, create max 1 intent-driven issue when 2+ issues share a category); max issues per run raised 2→3 (research + intent); added intent-driven label to Ensure labels step
- README.md: added "Interacting with the Pipeline" section documenting comment-on-issue, close-PR-without-merge, not-planned, permanent rules, agent-ready label, claude-task
- state/learned_intents.md: created as empty placeholder with header
- Build passing (exit 0)

In progress: PR for issue #33 (needs-review — workflow YAML changes)

## Open Items (priority order)
1. Issue #33: [PR opened — needs-review] Human intent learning, PR close handling, interaction guide
2. Issue #8: [agent-ready — UNBLOCKED] Upgrade Node.js 20 actions before June 2026 deadline
3. PR #19: [reviewer re-triggered] Anti-sycophancy guardrails for adversarial-review.md (closes #13)
4. PR #20: [reviewer re-triggered] Agentic security patterns — supply chain hygiene + prompt injection defense (closes #17)
5. Issue #22: [needs-review] Submit to hesreallyhim/awesome-claude-code (29k stars)
6. Issue #10: [needs-review — awaiting human] Last-updated badge user-friendly time
7. Issue #21: [feature] Add DeerFlow repo to external sources
8. Profile page: 5/8 sections still unchecked

## Metrics Snapshot
Period: 2026-03-15 to 2026-03-22 (first full week tracked)
- Total commits: 65+
- Stars: 1 | Forks: 0 | Adopters: 0

## Notes for Next Agent
- PR for issue #33 modifies 3 workflow YAML files — must use WORKFLOW_PAT for push and labeled needs-review per autonomy rules
- feedback-learner.yml permissions changed from issues:read to issues:write (needed for label manipulation and commenting)
- evolve max issues raised from 2 to 3 (2 research + 1 intent)
- state/learned_intents.md auto-covered by evolve.yml git add state/
- PRs #19 and #20 still awaiting human review
