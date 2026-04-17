---
name: github-task-interactive
description: For Claude Code running INTERACTIVELY in a terminal. Use this skill to decide WHETHER GitHub issue tracking is worth the overhead for the current session, and how to use issues as the async-visibility surface when it is. Trigger PROACTIVELY when the user says things like "ping me when done", "I'll be away", "let me know how it goes", "track this", or asks to start a multi-session/multi-day effort — those are signals to create an issue so the user can monitor from GitHub mobile. Also trigger when the user references an existing `#NN` issue or branch name encoding one (`fix/auth-123`). For trivial or exploratory work — typo fixes, single-file edits, debugging — DO NOT create an issue; just work in chat with TodoWrite. Do NOT use this skill in headless `claude -p` runs; that has its own skill (`github-task-headless`).
---

# GitHub Task Protocol — Interactive Mode

You are running inside Claude Code in the user's terminal. The user is present and you can talk to them in chat.

The first decision is **whether** to track this work in a GitHub issue at all. Most interactive sessions don't need one — the conversation in your terminal is already the source of truth. Issues earn their keep when the user might step away and want to check progress from somewhere else (typically GitHub mobile).

## When to create an issue (three tiers)

**Tier 1 — Auto-create silently. No question asked.**

User has explicitly signaled async intent. Phrases that trigger this:

- "ping me when done"
- "let me know how it goes"
- "I'm heading out" / "stepping away" / "be back later"
- "I'll check on this later"
- "track this" / "create an issue for this"
- "make sure I can see this from my phone"

Action: create the issue immediately with the AC template below, post the link in chat ("Tracking as #42 — you can monitor from GitHub mobile"), keep working.

If the user is going to do the work themselves and just wants visibility (e.g. "track this, I'll do it tomorrow morning"), add the `do-not-pickup` label so a headless agent doesn't take over while they're away.

**Tier 2 — Offer once.**

The work *might* outlive this session. Signals:

- Scope sounds multi-session ("build the auth system", "refactor the database layer")
- Stakeholders mentioned ("for Friday's demo", "the team needs to see")
- You estimate >1hr of work or >5 files touched

Action: ask one short question — "This looks like it'll take a while. Want me to create an issue so you can check on it from mobile?" If the user says no, drop it for the rest of the session.

**Tier 3 — Never.**

Trivial or exploratory work:

- Typo fixes, one-line bug fixes
- Debugging a single error
- Single-file edits
- Exploration / "what does this do?"
- Throwaway experiments

Action: just work in chat. Use TodoWrite for in-session steps. No issue.

**Existing issue:** if the user references `#NN` or you're on a branch encoding one, you're already in tracked mode — claim it (see "Working on a tracked issue" below).

## Acceptance Criteria template

When auto-creating in Tier 1, infer AC from the user's request. Use a flat checklist:

```
## Acceptance Criteria
- [ ] <happy path outcome>
- [ ] <happy path outcome>
- [ ] <error / edge case>
```

In Tier 1, **don't block on confirmation** — start working. Tell the user: "I inferred the AC — edit `#42` directly if I missed anything." They can adjust from mobile or in chat.

In Tier 2, present the inferred AC inline in chat for the user to ack or edit *before* you create the issue (they're right there, the round-trip is cheap).

Principles:

- Outcome-focused, not implementation
- Black-box testable from outside the code
- Cover the happy path first, one or two error/edge cases, anything non-functional only if obvious

## Roles (when an issue is in play)

| Surface | Role | Cadence |
|---------|------|---------|
| **Chat** with the user | Questions, decisions, reasoning | Real-time |
| **TodoWrite** tool | In-session step tracker | Per step |
| **Issue body** | Durable state: goal, AC, plan, current status | When material changes |
| **Issue comments** | Durable log: session summaries, decisions, handoffs | Once per session typically |
| **PR** with `Fixes #NN` | Closes the issue automatically on merge | At the end |

The most important rule: **don't talk to the user through the issue.** They are right here. Use chat. Reserve the issue for things that need to outlive this session — especially the things the user will read on mobile.

## Working on a tracked issue

Claim an existing issue:

```bash
gh issue edit NN --add-assignee @me \
  --add-label status:in-progress --remove-label status:todo
```

Linked branch (optional):

```bash
gh issue develop NN --checkout
```

Auto-create (Tier 1 or accepted Tier 2):

```bash
gh issue create -t "TITLE" -F /tmp/issue-body.md \
  -l "status:in-progress" -a @me
```

Body template for auto-creation:

```markdown
## Goal
<one stable sentence — your read of what the user asked for>

## Acceptance Criteria
- [ ] <inferred AC>
- [ ] <inferred AC>
- [ ] <error case>

## Notes
_Auto-created by Claude Code. Edit the AC if I got it wrong._

---
_Status: 🟢 in-progress · Last touched: 2026-04-17_
```

## During the session

Use **TodoWrite, not issue comments**, for in-session step tracking. The user sees TodoWrite live; the issue does not need that granularity.

Update the **issue body** when something material changes:

- An acceptance criterion is added or completed
- The plan changes shape
- A blocker emerges
- A non-goal becomes worth recording

Apply: write the body to a file, then:

```bash
gh issue edit NN --body-file /tmp/issue-NN.md
```

## Asking the user questions

You're interactive — **ask them in chat.** Do *not* post `awaiting-input` comments while the user is at the terminal; that protocol is for headless runs.

If a decision is worth remembering later (architectural tradeoff, scope call, vendor choice), summarize the resolved decision in **one** issue comment after the user answers — not the back-and-forth.

```bash
gh issue comment NN --body "Decision: chose Option B (in-house JWT) because <reason>."
```

## Ending a session

If an issue is in play, don't end with it in an inconsistent state.

### Case 1: Task complete

1. Open the PR with `Fixes #NN` in the body — issue auto-closes on merge.
2. Move the issue to review:

   ```bash
   gh issue edit NN --add-label status:in-review --remove-label status:in-progress
   ```
3. Post a final issue comment summarizing what shipped.

### Case 2: Stopping mid-task, will resume soon

1. Update the body: current state, what's next.
2. Post a "session end" comment: where I left off, what's next, any gotchas.
3. Leave `status:in-progress`.

### Case 3: Handing off (user checks from mobile, or async pickup)

1. Update the body thoroughly — the next reader has none of your session context.
2. Post a handoff comment with explicit "to resume: do X, Y, Z."
3. If a headless agent should pick it up, move back to `status:todo`. Otherwise leave `status:in-progress`.

### Case 4: Hit a blocker, user already left

This is the one case where you DO post an awaiting-input comment from interactive mode — because the user is now async.

1. Set labels:

   ```bash
   gh issue edit NN --add-label "status:awaiting-input,needs-input" --remove-label status:in-progress
   ```
2. Use the awaiting-input comment template from `github-task-headless`.

### Case 5: No issue was ever created

Just stop. No bookkeeping needed. If the work produced commits or files, summarize in chat.

## Label taxonomy (shared with headless)

Exactly one `status:*` at a time:

- `status:todo` — claimed but not started; eligible for headless pickup
- `status:in-progress` — actively being worked on
- `status:blocked` — waiting on external dep
- `status:awaiting-input` — needs human decision (paired with `needs-input`)
- `status:in-review` — PR open, waiting on review/merge
- `status:done` — closed and complete

Modifiers (combine with the above):

- `do-not-pickup` — human is doing the work; headless agent must not claim or take over even if `status:todo`
- `agent:<n>` — optional, e.g. `agent:interactive`, `agent:headless`

## Orphan detection (be aware)

If you set `status:in-progress` and the issue then sits with no updates for >4 hours, the headless agent may post an activity-check comment and move it to `status:awaiting-input`. This is the recovery path for crashed sessions. To respond:

- 👍 the activity-check comment within 24h to keep working as-is
- Reply "take over" to remove `do-not-pickup` and let headless continue
- Reply "pause" to keep `do-not-pickup` and move to `status:blocked`
- Reply "done" or "abandon" to close

If no response in 24h, headless resets to `status:todo` (clearing `do-not-pickup`) so the next eligible run picks it up.

## Quick reference

```bash
# Auto-create a tracked task
gh issue create -t "TITLE" -F /tmp/issue-body.md -l "status:in-progress" -a @me

# Auto-create where human will do the work (no headless pickup)
gh issue create -t "TITLE" -F /tmp/issue-body.md -l "status:in-progress,do-not-pickup" -a @me

# Claim existing
gh issue edit NN --add-assignee @me --add-label status:in-progress --remove-label status:todo

# Linked branch
gh issue develop NN --checkout

# Update body
gh issue edit NN --body-file /tmp/issue-NN.md

# Comment
gh issue comment NN --body-file /tmp/comment.md

# Move to review
gh issue edit NN --add-label status:in-review --remove-label status:in-progress

# PR with auto-close
gh pr create -t "feat(scope): summary (#NN)" -b "<body>. Fixes #NN."

# Hand off back to the queue
gh issue edit NN --add-label status:todo --remove-label status:in-progress
```

## Anti-patterns

- **Don't create an issue for Tier 3 work.** Typo fixes and one-file changes don't need tracking. Just do them in chat.
- **Don't ask "should I create an issue?" for clear Tier 1 signals.** Create it and tell the user you did.
- **Don't ask twice if the user said no in Tier 2.** Drop it for the session.
- **Don't comment for every TodoWrite step.** Use TodoWrite *for* per-step tracking.
- **Don't post `awaiting-input` while the user is in the chat.** Just ask them.
- **Don't leave `status:in-progress` set when you walk away** — pick `status:todo`, `status:awaiting-input`, or `status:in-review`.
- **Don't close an issue without confirming AC are checked or explicitly accepted.**
- **Don't duplicate TodoWrite content into the issue body.** Body = plan + state, TodoWrite = scratchpad.
- **Don't open a PR without `Fixes #NN`** when the PR completes the issue — manual closing is forgettable.
