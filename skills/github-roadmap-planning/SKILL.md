---
name: github-roadmap-planning
description: Use this skill when the user wants to plan, organize, sequence, or review work that spans multiple issues — anything bigger than a single task. Triggers include "plan v1", "create a roadmap", "what's the roadmap", "break down [feature/epic]", "what should ship next", "review milestones", "we're slipping on X", "reorganize the backlog", "close out v0.3", "what's left in this milestone". Operates one layer above the github-task-interactive skill — this one groups issues into milestones (releases or themes) with goals, due dates, and success criteria. Pairs with github-task-interactive, which handles per-issue mechanics. Do NOT use for single-task tracking (use github-task-interactive), pure brainstorming with no commitment, or status questions about one specific issue.
---

# GitHub Roadmap Planning

## Purpose

Group GitHub Issues into Milestones that represent **shippable units of work** with goals, success criteria, and target dates. Use Milestones as the planning surface so the user can see "what ships next, by when, and what's left" at a glance — without leaving GitHub.

This skill plans *across* issues. It does **not** replace `github-task-interactive`, which handles individual issue lifecycles. When this skill creates issues during a milestone breakdown, it follows that skill's per-issue conventions (acceptance criteria checkboxes, status labels, etc.).

---

## When to use

### Tier 1 — act immediately, no confirmation

Trigger phrases (match deterministically):

- "plan v1" / "plan v0.2" / "plan the next release"
- "create a roadmap" / "roadmap for X"
- "create a milestone for X"
- "what's the roadmap" / "show the roadmap"
- "break down [feature]" / "break this down into issues"
- "what's left in v0.X" / "where are we on v1"
- "close out v0.X" / "ship v0.X"
- "move issue #N to next milestone"

### Tier 2 — surface the option, then act on confirmation

Implicit signals — ask one short question, then proceed:

- User describes a multi-week scope ("I want to ship the triage loop") → "Want to create a milestone for this so we can track the breakdown?"
- User mentions a target date ("by end of June") → "Create a milestone with that due date?"
- User lists 5+ tasks together → "Should these go under a single milestone?"
- User says "we have too many open issues" → "Want to organize them into milestones?"

### Tier 3 — do not use this skill

- Single task, no time horizon → use `github-task-interactive`
- Pure brainstorming, no decision being made → just discuss
- Status check on one issue → query directly
- The repo has fewer than 3 open issues total → milestones are overkill

---

## Core model

| Concept | Maps to | Holds |
|---------|---------|-------|
| Milestone | A release or theme | Goal, success criteria, due date, set of issues |
| Issue | A single shippable change | Per-task state (handled by `github-task-interactive`) |
| Label `roadmap:current` / `roadmap:next` / `roadmap:later` | Optional planning hint on issues not yet milestoned | Pre-commit triage |

**A milestone exists when:**

- It has a clear goal (1 sentence)
- It has 3-5 observable success criteria
- It has at least 3 issues attached (otherwise it's a wish, not a plan)
- It has a target date (rough — weeks, not days)

---

## Naming

- **Version-style** (`v0.1`, `v0.2`, `v1.0`) for product releases. Use semver discipline: `v0.x` for pre-stable; `v1.0` is the first commitment to API/UX stability. Don't skip numbers.
- **Theme-style** (`MCP Migration`, `Self-serve Onboarding`, `Triage Quality`) for cross-cutting work that doesn't ship as a versioned release.
- Avoid pure date-style (`2026-Q3`) — calendars slip and the title becomes a lie. Themes age better.
- Pick **one mode per repo**. Don't mix `v0.3` and `Q3 Performance` in the same product.

---

## Conventions

### Milestone description format

```markdown
**Goal:** [one sentence — what shipping this unlocks for users]

**Success criteria:**
- [ ] [observable outcome 1]
- [ ] [observable outcome 2]
- [ ] [observable outcome 3]

**Out of scope:** [what we explicitly are not doing this milestone]

**Linked issues:** [auto-populated by GitHub]
```

### Active milestone count

At most **3 open milestones** at a time:

1. The one **in flight** (where most issues live and active work happens)
2. The **next** one (shape only — title + goal + a few seed issues)
3. A **`backlog`** milestone for triage (optional)

More than 3 open milestones = the roadmap is fictional.

### Issue → milestone assignment rules

- Assign **at issue creation time** via `--milestone`. Reassigning mid-flight is a planning miss; if it happens, drop a comment explaining why.
- An issue belongs in the current milestone **only if** not shipping it would mean the milestone goal isn't met.
- Nice-to-haves go in the next milestone or `backlog` — never the current one.

### Due dates

- Milestones longer than 4 weeks are usually too big — split them.
- Add ~30% slack to honest estimates. A "2-week" milestone gets a 3-week `due_on`.
- Don't update `due_on` silently when slipping. Either replan (Case 4) or accept the slip in a comment.

---

## Workflows

### Case 1 — Creating a new roadmap

When user says "plan v1" or "create a roadmap":

1. **Clarify the destination** — one question only: "What does done look like for this product/release?"
2. **Propose 3-5 milestones** in sequence as a compact table (title, one-line goal, rough date). Don't create anything yet.
3. **Get a yes/no on the shape.** If the user wants edits, iterate inline.
4. **Create only milestone #1 in full** (with success criteria + 5-10 issues). Create milestones #2-3 as **shape only** (title + goal + due date, no issues yet). Don't create milestones beyond #3.
5. **Confirm before creating issues** — show the proposed issue list inline (titles + one-line scope each) and wait for approval.

```bash
# Create milestone
gh api repos/OWNER/REPO/milestones \
  -f title="v0.1 — MCP-native MVP" \
  -f description="$(cat <<'EOF'
**Goal:** Ship the email triage loop end-to-end so a single user can receive, classify, and act on inbound mail via MCP only.

**Success criteria:**
- [ ] Inbound email reaches the LLM triage within 30s
- [ ] 3-tier classification labels apply correctly on test corpus
- [ ] User can reply via chatbot and the message lands in recipient's inbox
- [ ] No traditional UI required for the full loop

**Out of scope:** multi-user, persistent agent profiles, self-serve onboarding
EOF
)" \
  -f due_on="2026-05-01T00:00:00Z"

# Capture the milestone number from the response, then create issues attached to it
gh issue create \
  --title "Wire AgentMail webhook to triage Lambda" \
  --body "..." \
  --milestone "v0.1 — MCP-native MVP"
```

### Case 2 — Breaking down a milestone into issues

When the user has a milestone (existing or just-created) and wants to flesh it out:

1. **Read the milestone description** and any existing issues attached.
2. **Propose 5-10 issues** that cover the goal. Each issue must be:
   - Independently shippable in 1-3 days
   - Have clear acceptance criteria
   - Not overlap with other issues in the milestone
3. **Show the proposed list inline** — titles + one-line scope each. No bodies yet.
4. **On approval**, create with `--milestone` flag set at creation time. Use `github-task-interactive` issue body conventions (AC checkboxes, status labels) for each.

### Case 3 — Roadmap review / status check

When user asks "what's the roadmap" or "where are we on v1":

```bash
# All open milestones with progress counts
gh api "repos/OWNER/REPO/milestones?state=open" \
  | jq -r '.[] | "\(.title) | due \(.due_on // "—") | \(.closed_issues)/\(.open_issues + .closed_issues) closed"'

# Issues in a specific milestone, by state
gh api "repos/OWNER/REPO/issues?milestone=N&state=all&per_page=100" \
  | jq -r 'group_by(.state) | .[] | "\(.[0].state): \(length)"'

# Open issues grouped by status label
gh api "repos/OWNER/REPO/issues?milestone=N&state=open&per_page=100" \
  | jq -r '.[] | "#\(.number) [\(.labels | map(select(.name | startswith("status:"))) | .[0].name // "—")] \(.title)"'
```

Present as a compact table:

| Milestone | Due | Progress | Days left | Status |
|-----------|-----|----------|-----------|--------|
| v0.1 — MVP | 2026-05-01 | 7/12 | 14 | on track |
| v0.2 — Multi-user | 2026-06-15 | 0/0 | 59 | shape only |

**Slip detector:** flag any milestone where `(open_issues × 1 day) > days_remaining`. Surface the slip with a concrete suggestion (push date, cut scope, or parallelize).

### Case 4 — Replanning (a milestone is slipping)

Triggered when slip detector fires, or user says "we're behind on X":

1. **Show the data first** — open issues, blocked issues, awaiting-input issues (use status labels from `github-task-interactive`).
2. **Offer three concrete moves**, ranked by cost to the user:
   - **Push date** — extend `due_on` by N days (cheapest, most honest if estimate was wrong)
   - **Cut scope** — move specific issues to next milestone or `backlog` (preserves date, signals priority)
   - **Add parallelism** — flag issues that could be split or paralleled (only if more hands are actually available)
3. **Don't move anything without explicit approval.** Show the exact `gh api` PATCH commands you'd run.
4. **After approval, batch-update** and drop a comment on the milestone explaining the change ("v0.1 due_on pushed from 2026-05-01 → 2026-05-14 because triage Lambda took longer than estimated").

```bash
# Push due date
gh api --method PATCH repos/OWNER/REPO/milestones/N \
  -f due_on="2026-05-14T00:00:00Z"

# Move issue to a different milestone
gh api --method PATCH repos/OWNER/REPO/issues/ISSUE_N \
  -F milestone=NEXT_MILESTONE_NUMBER

# Remove milestone entirely (sends issue back to no-milestone)
gh api --method PATCH repos/OWNER/REPO/issues/ISSUE_N \
  -F milestone=null
```

### Case 5 — Closing out a milestone

When work is complete or user says "ship v0.1" / "close out v0.1":

1. **Verify cleanliness** — check for any open issues. If found, ask: close them, move to next milestone, or block the close?
2. **Verify success criteria** — read the milestone description's success criteria checkboxes. If any are unchecked, surface them and ask whether they're actually met or being deferred.
3. **Close the milestone:**

   ```bash
   gh api --method PATCH repos/OWNER/REPO/milestones/N -f state=closed
   ```
4. **Generate a release-notes summary** from closed issues:

   ```bash
   gh api "repos/OWNER/REPO/issues?milestone=N&state=closed&per_page=100" \
     | jq -r '.[] | "- #\(.number) \(.title)"'
   ```

   Present this as a markdown block the user can paste into a release announcement, CHANGELOG.md, or a tweet.
5. **Suggest creating the next milestone** if not already shaped.

### Case 6 — Backlog triage (issues without a milestone)

When user says "triage the backlog" or "where do these issues belong":

1. **List unmilestoned open issues:**

   ```bash
   gh api "repos/OWNER/REPO/issues?milestone=none&state=open&per_page=100" \
     | jq -r '.[] | "#\(.number) [\(.labels | map(.name) | join(","))] \(.title)"'
   ```
2. **Propose an assignment for each** — "v0.1", "v0.2", `backlog`, or "close as out-of-scope". Show as a table.
3. **Confirm in batch** (one approval covers all moves), then apply.

---

## Pairing with `github-task-interactive`

| Layer | Skill | Owns |
|-------|-------|------|
| Roadmap | `github-roadmap-planning` (this) | Milestones, sequencing, due dates, scope decisions |
| Issue | `github-task-interactive` | Per-issue body, AC checkboxes, status labels, comments, completion |

When this skill creates issues during Case 1 or Case 2, it produces issue bodies in the format `github-task-interactive` expects so that downstream per-issue work composes cleanly.

When `github-task-interactive` closes an issue, this skill's status views (Case 3) automatically reflect the change — no extra wiring needed.

---

## Anti-patterns

- **Don't create empty milestones.** A milestone with no issues is a wish. Either populate it in the same session or hold off creating it.
- **Don't shape milestones beyond #3.** Future milestones can be discussed but shouldn't exist as GitHub objects yet — premature milestones become noise that has to be cleaned up later.
- **Don't use `due_on` as a hard commitment without slack.** Add ~30%. If the estimate was wrong, push the date in Case 4 with an explanatory comment — don't pretend the original date was fine.
- **Don't close a milestone while issues remain open silently.** Always force the explicit decision: close, move, or block.
- **Don't reassign an issue's milestone mid-flight without commenting** on the issue explaining the move. It erases planning history.
- **Don't number versioned milestones non-sequentially** (v0.2 → v0.5 with nothing in between). It looks like missing releases.
- **Don't mix versioned and themed milestones in the same repo.** Pick one mode and stick with it.
- **Don't keep more than 3 milestones open.** If there are more, the roadmap isn't real — close the oldest, merge overlapping ones, or move issues to `backlog`.
- **Don't re-do per-issue mechanics here.** Acceptance criteria, status labels, comments, completion → defer to `github-task-interactive`. This skill stops at the issue boundary.
- **Don't create a milestone the user didn't ask for.** Tier 1 phrases are explicit; Tier 2 is a question, not an action.
