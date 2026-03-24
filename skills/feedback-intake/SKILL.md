---
name: feedback-intake
version: 1.0.0
description: >
  Converts unstructured user feedback (verbal, pasted text, emails)
  into structured issue tracker entries that trigger triage workflows.
  Handles batch intake, type classification, and routing.
author: tokenman
tags: [feedback, triage, issue-tracking, user-input]
requires: []
---

# Feedback Intake Skill

## Purpose

Convert any unstructured feedback (verbal description, pasted text,
email excerpt, chat message) into a properly structured issue that
a triage workflow can classify and action.

## Trigger Phrases

Activate this skill when the user says:
- "user reported..."
- "got feedback that..."
- "someone said the [section] is..."
- "can you log this: ..."
- "a visitor mentioned..."
- "/feedback [text]"

## What to Extract

From any feedback input, identify:
1. **Type**: bug | ux-suggestion | positive | question
2. **Location**: which page, section, or feature (if mentioned)
3. **Description**: what the person actually experienced
4. **Browser/device**: if mentioned

## Issue Format

Create a structured issue using your project's issue tracker CLI:

```
Title: [feedback] [brief description]
Labels: feedback

Body:
  Type: [bug|suggestion|positive|question]
  Section: [page or section, or 'unspecified']
  Browser/Device: [if known, else 'not specified']

  Description:
  [the actual feedback, in the visitor's words if possible]

  ---
  Logged via feedback-intake skill
```

## Examples

**Input:** "someone said the projects section doesn't load on mobile"

**Output issue:**
```
Title: [feedback] Projects section not loading on mobile
Labels: feedback
Body:
  Type: bug
  Section: Projects section
  Browser/Device: mobile (unspecified)
  Description: Projects section doesn't load on mobile devices.
```

**Input:** "user said they loved the design, very clean"

**Output issue:**
```
Title: [feedback] Positive feedback on design
Labels: feedback
Body:
  Type: positive
  Section: general
  Description: User expressed that the design is clean and appealing.
```

## After Creating the Issue

1. Tell the user: "Logged as Issue #N. Triage workflow will classify
   and action it within the next run."
2. Do NOT try to fix the issue yourself -- triage handles routing
3. Do NOT close the issue -- triage handles lifecycle

## Batch Intake

If the user gives multiple feedback items at once, create one issue
per item. Do not bundle multiple distinct pieces of feedback into a
single issue -- it makes triage and tracking harder.

## Rules

- Always add the `feedback` label -- this triggers the triage workflow
- Title must start with `[feedback]` for the triage workflow filter
- Do not add routing labels yourself -- the triage agent decides that
- If the feedback is already a bug you know how to fix:
  still create the issue. Don't skip the triage workflow.
