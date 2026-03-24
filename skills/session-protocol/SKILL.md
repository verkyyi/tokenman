---
name: session-protocol
version: 1.0.0
description: >
  Start/stop state management protocol for AI agent sessions.
  Ensures every agent run reads prior context on start and writes
  a summary on stop, preventing context loss across runs.
author: tokenman
tags: [state-management, session, context, persistence]
requires: []
preamble-tier: 2
---

# Session Protocol

A pattern for maintaining persistent state across AI agent sessions,
whether triggered by CI/CD workflows, CLI interactions, or automated
schedules. Every session reads prior context on start and writes a
summary on stop.

## Overview

Agent sessions are stateless by default -- each run starts fresh with
no memory of previous work. This protocol solves that by defining
explicit read/write checkpoints that persist context in state files.

## ON START (every session)

At the beginning of every agent session:

1. **Read project state** -- Load the last session summary to understand
   what happened previously, what's in progress, and what to do next.
   - Recommended file: `state/project_state.md` (or equivalent)

2. **Read project rules** -- Load any project-specific configuration,
   conventions, or constraints the agent must follow.
   - Recommended file: project-level `CLAUDE.md` or equivalent config

3. **Read feature status** -- Understand what's done and what's pending.
   - Recommended file: `FEATURE_STATUS.md` (or equivalent tracker)

4. **Check current event** -- Understand what triggered this session:
   issue body, PR diff, workflow input, user message, etc.

## ON STOP (every session)

At the end of every agent session:

1. **Write session summary** -- Record what was done, what's in progress,
   and hints for the next session.
   - Update: `state/project_state.md` (or equivalent)
   - Include: action taken, items completed, items remaining, next steps

2. **Append to activity log** -- Add a single-line entry to an append-only
   log for auditability.
   - Format: `TIMESTAMP | session_source | action | outcome`
   - File: `state/agent_log.md` (or equivalent)

3. **Update feature tracker** -- Mark completed items, add new discoveries.
   - Update: `FEATURE_STATUS.md` (or equivalent)

4. **Commit state changes** -- Ensure all state file updates are persisted
   (via git commit, API call, or equivalent).

## Interactive Session Close

For CLI/interactive sessions (as opposed to CI-triggered runs):

- The agent should proactively update state files when it detects the
  conversation is wrapping up (user says "done", "thanks", "that's all",
  or context is being compressed).
- A session-end hook can auto-commit uncommitted state changes as a
  safety net.

## State File Conventions

### Project State (read/write)
The primary state file. Written at end of every session, read at start.
Required sections:
- **Last updated** -- ISO timestamp + session source
- **Last Session** -- action summary, completed items, in-progress items
- **Open Items** -- checkboxes with issue/PR/task references
- **Critical Notes** -- important context for the next agent

### Activity Log (append-only)
Never edit existing lines. Format:
```
TIMESTAMP | session_source | action description | outcome
```

### Feature Status (read/write)
Checkbox-based tracker:
```markdown
## Feature Area
- [x] Completed item
- [ ] Pending item
```

## Integration Patterns

### CI/CD Workflow Integration
```yaml
# Start: read state
- name: Read project state
  run: cat state/project_state.md

# ... agent work ...

# Stop: commit state
- name: Commit state changes
  run: |
    git add state/
    git commit -m "state: session summary"
```

### CLI Session Integration
Configure a session-end hook that auto-commits state changes:
```bash
# On session close, commit any dirty state files
git add state/ && git commit -m "state: CLI session close"
```

## Benefits

- **Context continuity** -- agents pick up where the last session left off
- **Auditability** -- every action is logged with timestamp and source
- **Coordination** -- multiple agents/workflows share state without conflicts
- **Resilience** -- if a session crashes, the next run recovers from state

## Gotchas

- State files should use a consistent, machine-parseable format
- The activity log is append-only -- never rewrite existing lines
- Commit state changes atomically (all state files in one commit)
- If multiple agents run concurrently, use a commit script that handles
  merge conflicts (e.g., GitHub API-based commits instead of git push)
