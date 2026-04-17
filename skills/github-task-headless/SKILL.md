---
name: github-task-headless
description: For Claude Code running HEADLESSLY via `claude -p` in GitHub Actions or similar CI. Use this skill in EVERY headless run that touches a GitHub issue — claim, do one bounded chunk of work, update progress, ask the human if blocked, resume on reply, close. There is no human watching this run; the GitHub issue is the ONLY channel. Trigger when the prompt references "this issue", "issue #NN", "the assigned task", or when the run originates from a GitHub Actions workflow with an issue context. Always check for human replies on awaiting-input issues at the start of every run before claiming new work. Do NOT use in interactive Claude Code sessions; that has its own skill (`github-task-interactive`).
---

# GitHub Task Protocol — Headless Mode

You are running via `claude -p` in CI. There is no human watching. The GitHub issue is the **only** channel between you and the human operator. Everything you say to them goes in the issue. Everything they say to you arrives as issue comments or 👍 reactions on your awaiting-input comments.

## Operating constraints

- **Single shot.** This run starts, does work, ends. No follow-up turns within the same run.
- **Bounded time.** Do one logical chunk. If the task is bigger, do as much as fits cleanly and hand off.
- **No interactive input.** If you need a human decision, exit with an awaiting-input comment.
- **Self-contained output.** Your run comment is read async, possibly hours later, possibly on a phone. Make it scannable.

## Run lifecycle

Every run follows this skeleton:

```
1. Run pre-flight (three sweeps): replies → orphans → queue
2. Identify the target issue (one of the sweeps surfaced it, or prompt named it)
3. Read its current state (body + last 5 comments + labels)
4. Do one bounded chunk of work
5. Write: update body (new state) + append run comment (what happened)
6. Decide ending state:
   - Completed → status:done, close, optionally PR with Fixes #NN
   - Blocked on human → status:awaiting-input + needs-input, exit
   - Blocked on external → status:blocked
   - More work to do → leave status:in-progress
7. Update heartbeat issue
```

## Identifying the target issue

The issue number arrives one of three ways:

- **GitHub event** (workflow triggered by issue activity): `${{ github.event.issue.number }}`
- **Pre-flight sweep** (see below) — sweeps 1 and 2 surface eligible work; sweep 3 claims new work
- **Explicit prompt**: "work on issue #42"

## Pre-flight: three sweeps before claiming new work

Each run starts with three sweeps in order. Stop at the first one that yields work to do; only fall through to claiming new work if all three return nothing.

### Sweep 1 — Detect human replies on awaiting-input issues

```bash
BOT_LOGIN="${BOT_LOGIN:-github-actions[bot]}"

gh issue list --label "needs-input" --state open --json number --jq '.[].number' \
| while read num; do
    last_author=$(gh api "repos/$GITHUB_REPOSITORY/issues/$num/comments" \
      --jq '.[-1].user.login')
    if [ "$last_author" != "$BOT_LOGIN" ]; then
      echo "Issue #$num: human replied — eligible to resume"
    fi
  done
```

When you resume an issue, the **first thing** in your new run comment must acknowledge the reply explicitly. Do not act silently.

### Sweep 2 — Detect orphaned in-progress issues

An interactive session may have crashed, the network may have dropped, the user may have closed their laptop and forgotten. Issues stuck at `status:in-progress` with no activity for >4h are orphan candidates.

```bash
stale_cutoff=$(date -u -d '4 hours ago' +%Y-%m-%dT%H:%M:%SZ)
gh issue list --label "status:in-progress" --state open \
  --json number,updatedAt \
  --jq ".[] | select(.updatedAt < \"$stale_cutoff\") | .number" \
| while read num; do
    # Don't re-ping if we already posted an activity check recently
    last_check=$(gh api "repos/$GITHUB_REPOSITORY/issues/$num/comments" \
      --jq "[.[] | select(.user.login == \"$BOT_LOGIN\") | select(.body | startswith(\"## ⏰ Activity check\"))] | last")
    [ "$last_check" != "null" ] && continue

    gh issue comment "$num" --body-file /tmp/activity-check.md
    gh issue edit "$num" \
      --add-label "status:awaiting-input,needs-input" \
      --remove-label "status:in-progress"
  done
```

Activity-check comment template:

```markdown
## ⏰ Activity check

This issue has been at `status:in-progress` with no updates for 4+ hours. If you're still actively working on it (interactive session paused), 👍 this comment within 24h and I'll leave it alone.

Otherwise, choose one:
- Reply "take over" — remove `do-not-pickup` and let me continue
- Reply "pause" — keep `do-not-pickup` and move to `status:blocked` until you signal otherwise
- Reply "done" / "abandon" — close

If no response in 24h, I'll assume orphan and reset to `status:todo` (without `do-not-pickup`) for the next eligible run.
```

A separate periodic job should sweep activity-check issues older than 24h with no human response and apply the default action (reset to `status:todo`, remove `do-not-pickup`).

### Sweep 3 — Pick the next eligible task

If the first two sweeps yielded nothing, claim new work from the queue:

```bash
recent_cutoff=$(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%SZ)

gh issue list --label "status:todo" --state open \
  --json number,labels,updatedAt \
  --jq "[.[]
    | select(.updatedAt < \"$recent_cutoff\")
    | select([.labels[].name] | contains([\"do-not-pickup\"]) | not)
    | .number] | first"
```

Three filters at once:

- `status:todo` — only claim work explicitly marked as available
- `do-not-pickup` excluded — never claim work the human is doing themselves
- Updated >10 min ago — avoid races with an active interactive session that just created the issue

If multiple eligible issues exist, prefer (in order): oldest `status:awaiting-input` with a fresh reply (sweep 1 already handled), then oldest `status:todo` (this sweep).

## Body template

Rewrite the body in full each run. Body = state, never log.

```markdown
## Goal
<stable one-liner>

## Acceptance criteria
- [ ] AC1
- [ ] AC2
- [x] AC3

## Plan
- [x] Step 1
- [ ] Step 2 — current
- [ ] Step 3

## Current state
<2–4 sentences: where I am, what's next>

## Blockers
<list, or "None">

## Links
- PR: #NN | Branch: feat/auth-123 | Related: #MM

---
_Status: 🟢 in-progress · Last run: 2026-04-17 15:12 UTC_
```

Apply:

```bash
gh issue edit "$NN" --body-file /tmp/body.md
```

## Run comment template

Exactly one per run. Self-contained. Scannable on a phone.

```markdown
## 🤖 Run 2026-04-17 15:12 UTC

**Did:** <what changed this run, with file paths and SHAs>
**State:** <progress N of M, current phase>
**Next:** <concrete next action for the next run>
```

Optional sections, only when relevant:

- `**Resumed from:**` <reference the human reply you're acting on>
- `**Surprises:**` <unexpected findings>
- `**PR:**` #NN

Post:

```bash
gh issue comment "$NN" --body-file /tmp/comment.md
```

If literally nothing changed this run (e.g. you found a blocker before doing any work), skip the run comment but bump the heartbeat. Don't post empty heartbeat-style comments to task issues.

## Asking the human for input

When you hit a decision you should not make alone — ambiguous spec, missing secret, architectural tradeoff, scope expansion — stop work and hand back cleanly.

```bash
gh issue edit "$NN" \
  --add-label "status:awaiting-input" --add-label "needs-input" \
  --remove-label "status:in-progress"

gh issue comment "$NN" --body-file /tmp/awaiting.md
```

Awaiting-input comment template:

```markdown
## 🛑 Awaiting input

@<owner> blocked on a decision I shouldn't make unilaterally.

**Question:** <one sentence>

**Context:** <2–3 sentences — why it matters, what I tried>

**Options:**
1. **<Option A>** — <tradeoff>. _My recommendation._
2. **<Option B>** — <tradeoff>.
3. **<Option C>** — <tradeoff>.

**To unblock:** reply with your pick (one word is fine), or 👍 this comment to accept the recommendation. I will not resume this task until you do.
```

**One open question per task at a time.** If you have three questions, bundle them numbered in one comment.

After posting, **exit the run.** Do not continue work on this issue.

## Detecting reply via reaction

A 👍 reaction on your awaiting-input comment means "accept the recommendation":

```bash
gh api "repos/$GITHUB_REPOSITORY/issues/comments/$COMMENT_ID/reactions" \
  --jq '.[] | select(.content == "+1") | .user.login'
```

To find the comment ID across runs without persistent state, scan recent bot comments for the awaiting-input header:

```bash
gh api "repos/$GITHUB_REPOSITORY/issues/$NN/comments" \
  --jq '[.[] | select(.user.login == "'"$BOT_LOGIN"'") | select(.body | startswith("## 🛑 Awaiting input"))] | last | .id'
```

## Completing a task

```bash
# Final run comment
gh issue comment "$NN" --body "✅ Done. PR #$PR_NUM merged. <one-sentence summary>."

# Mark done and close
gh issue edit "$NN" --add-label "status:done" --remove-label "status:in-progress"
gh issue close "$NN" --reason completed
```

If the task was abandoned (out of scope, superseded), close with `--reason "not planned"` and explain in the final comment.

## Heartbeat issue

Pin one long-lived issue titled "🫀 Agent heartbeat". Rewrite its body at the end of every run — this is the human's at-a-glance dashboard.

```markdown
## Last run
2026-04-17 15:12 UTC · 3 issues touched

## Open work
- 🟢 in-progress: 2
- 🟡 blocked: 1
- 🛑 awaiting-input: 1
- ⚪ todo: 4

## Currently blocked / waiting
- #42 — "Refactor auth" (awaiting reply, 2h)
- #51 — "Upgrade SDK" (blocked on upstream release)

## Recently updated
- #42 · #51 · #48
```

Don't close it. Don't post comments to it.

## GitHub Actions workflow snippet

A minimal scheduled invocation:

```yaml
name: agent-headless
on:
  schedule:
    - cron: "*/30 * * * *"
  issues:
    types: [labeled, unlabeled]
permissions:
  contents: write
  issues: write
  pull-requests: write
jobs:
  run:
    # Critical: skip when the bot is the actor — prevents self-trigger loops
    if: github.event.sender.login != 'github-actions[bot]'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          mode: headless
          prompt: |
            Use the github-task-headless skill.
            Run all three pre-flight sweeps in order: human replies on
            awaiting-input issues, orphan detection on stale in-progress
            issues, then claim from the queue if both yield nothing.
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          BOT_LOGIN: github-actions[bot]
```

The `if:` guard at the job level is essential — without it, every body or label edit the bot performs re-triggers the workflow and burns API budget in a loop.

## Label taxonomy (shared with interactive)

Exactly one `status:*` at a time:

- `status:todo` — claimed but not started; eligible for headless pickup
- `status:in-progress` — actively being worked on
- `status:blocked` — waiting on external dep
- `status:awaiting-input` — needs human decision (paired with `needs-input`)
- `status:in-review` — PR open, waiting on review/merge
- `status:done` — closed and complete

Modifiers (combine with the above):

- `do-not-pickup` — human is doing the work; never claim or take over even if `status:todo`
- `agent:<n>` — optional, e.g. `agent:headless`, `agent:interactive`

## Anti-patterns

- **Don't act on a needs-input reply silently.** Acknowledge in the new run comment first.
- **Don't ask >1 open question per task.** Bundle into one comment.
- **Don't post a run comment if nothing changed.** Bump the heartbeat instead.
- **Don't append to the body — rewrite it.** Body is state, comments are log.
- **Don't close an issue without `status:done`.** Filters and dashboards depend on the label.
- **Don't fork a new issue to "continue" work.** Same issue, new run comment.
- **Don't try to run multiple bounded chunks in one run.** One per run; the next scheduled run will pick up.
- **Don't use Projects v2 as a parallel state store.** Issue labels are canonical; a project board may mirror them as a read-only view.
