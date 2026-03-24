---
name: readme-sync
version: 1.0.0
description: >
  Use when README.md needs to reflect current repo structure.
  Covers workflow count, workflow table, and architecture section.
  Referenced by reviewer.yml post-merge step and evolve.yml Step 2e.
author: tokenman
tags: [readme, documentation, sync, automation]
---

# README Sync

## Purpose
Keep README.md consistent with the actual repo structure. Prevent
drift between workflow count, table, architecture section, and reality.

## When NOT to Use
- When README content is already accurate — don't rewrite for style preferences alone
- When the change is to workflow behavior (not structure) — only sync on structural additions/removals
- When manually crafting README marketing copy or narrative sections
- When the README change is purely cosmetic (badge color, link format) with no structural drift

## Rationalizations to Reject
- "The README could use a full rewrite" — surgical changes only; preserve human-written descriptions
- "I'll update the README while I'm fixing this other thing" — only sync when structure actually changed
- "The style of the auto-inserted row doesn't match perfectly" — the daily evolve check refines descriptions; don't block on style
- "I should reorder the workflow table rows" — preserve existing order; only add/remove rows

## Anti-Patterns

**Bad — full table rewrite for style consistency:**
The agent rewrites all 8 rows of the workflow table to normalize description length,
destroying human-written descriptions that were accurate and well-phrased.

**Good — surgical row addition:**
A new workflow file was added. The agent inserts one new row with basic info
extracted from the YAML, leaving all existing rows untouched.

## Auto-maintained sections
These README sections are kept in sync automatically:

1. **Workflow heading** — "## The N workflows" must match .github/workflows/*.yml count
2. **Workflow table** — every workflow file must have a row; deleted workflows must be removed
3. **Architecture tree** — "# The N autonomous workflows" comment must match actual count

## Sync triggers
- **Post-merge (reviewer.yml)** — deterministic shell sync after any merged PR that changes workflow, skill, or app structure files
- **Daily (evolve.yml Step 2e)** — full Claude-assisted review of README quality and accuracy at 12 UTC

## How the post-merge sync works
The reviewer.yml post-merge step:
1. Detects if merged PR changed `.github/workflows/`, `skills/`, or `apps/` paths
2. Counts actual workflow files, updates heading and architecture count
3. Adds missing workflows to the table with basic info extracted from the YAML
4. Removes table rows for deleted workflow files
5. Only commits if README content actually changed

## Table row format
```
| `name.yml` | Trigger description | What it does |
```

Trigger is extracted from the workflow's `on:` section. The daily evolve
check refines auto-inserted descriptions to match the existing style.

## Rules
- Only update if content is genuinely out of date
- Preserve existing human-written descriptions
- Surgical changes only — no full rewrites
- The daily evolve check refines descriptions; post-merge handles structure
