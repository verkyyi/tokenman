---
name: feedback-intake
description: >
  Use when the developer says "user reported", "got feedback that",
  "someone said", pastes feedback text, or asks Claude to log feedback.
  Also activates on /feedback command. Parses any feedback format into
  a structured GitHub Issue that triggers the triage workflow.
allowed-tools:
  - Bash
---

# Feedback Intake Skill

## Purpose
Convert any unstructured feedback (verbal description, pasted text,
email excerpt, Slack message) into a properly structured GitHub Issue
that the triage workflow can classify and action.

## When NOT to Use
- When the input is already a structured GitHub issue — it's already in the pipeline
- When the developer wants to fix a bug directly without logging — still create the issue, but don't use this skill for the fix
- When the input is an agent internal error — use `agent-error` label directly, not the feedback pipeline
- When triaging or routing existing issues — that's the triage workflow's job, not feedback intake

## Rationalizations to Reject
- "I'll fix this bug directly instead of filing an issue" — always create the issue first; triage handles routing
- "Multiple feedback items can go in one issue to save time" — one issue per feedback item for proper triage and tracking
- "I can add the agent-ready label myself to speed things up" — triage agent decides routing and labeling
- "This feedback is too minor to log" — all feedback gets logged; let triage decide priority

## Trigger Phrases
- "user reported..."
- "got feedback that..."
- "someone said the [section] is..."
- "can you log this: ..."
- "a visitor mentioned..."
- "/feedback [text]"

## What to Extract
From any feedback input, identify:
1. **Type**: bug | ux-suggestion | positive | question
2. **Location**: which page or section (if mentioned)
3. **Description**: what the person actually experienced
4. **Browser/device**: if mentioned

## GitHub Issue Format
Always create the issue using gh CLI:

```bash
gh issue create \
  --title "[feedback] [brief description]" \
  --label "feedback" \
  --body "**Type:** [bug|suggestion|positive|question]
**Section:** [page or section, or 'unspecified']
**Browser/Device:** [if known, else 'not specified']

**Description:**
[the actual feedback, in the visitor's words if possible]

---
*Logged via feedback-intake skill*" \
  --repo OWNER/REPO
```

## Examples

Input: "someone said the projects section doesn't load on mobile"
Output issue:
```
Title: [feedback] Projects section not loading on mobile
Labels: feedback
Body:
  Type: bug
  Section: Projects section
  Browser/Device: mobile (unspecified)
  Description: Projects section doesn't load on mobile devices.
```

Input: "user said they loved the design, very clean"
Output issue:
```
Title: [feedback] Positive feedback on design
Labels: feedback
Body:
  Type: positive
  Section: general
  Description: User expressed that the design is clean and appealing.
```

## After Creating the Issue
1. Tell the developer: "Logged as Issue #N. Triage workflow will
   classify and action it within the next workflow run."
2. Do NOT try to fix the issue yourself — triage workflow handles routing
3. Do NOT close the issue — triage workflow handles lifecycle

## Batch Intake
If the developer gives multiple feedback items at once, create one
issue per item. Do not bundle multiple distinct pieces of feedback
into a single issue — it makes triage and tracking harder.

## Gotchas
- Always add the 'feedback' label — this triggers triage.yml
- Title must start with "[feedback]" for the triage workflow filter
- Do not add agent-ready label yourself — triage agent decides that
- If the feedback is already a bug you know how to fix:
  still create the issue. Don't skip the triage workflow.
