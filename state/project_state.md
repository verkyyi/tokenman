# Project State
# This file is written by every workflow run at exit.
# Read at start of every workflow run.
# Committed to repo — git history is the full audit trail.

Last updated: 2026-03-22T12:15:00Z
Updated by: coder.yml (issue #38)

## Last Session
Action: coder.yml — implement README auto-sync (issue #38)

Done:
- Created skills/readme-sync.md — documents the sync protocol (auto-maintained sections, triggers, rules)
- Added post-merge README sync step to reviewer.yml — deterministic shell script that updates workflow count (heading + architecture), adds missing table rows, removes rows for deleted workflows; only runs when structural files changed in merged PR
- Fixed README.md inconsistencies: heading "ten" → "eleven", architecture "nine" → "eleven", added discover.yml to workflow table
- Build passes after changes
- Opened PR for issue #38

## Open Items (priority order)
1. Issue #38: README auto-sync — PR opened, awaiting review
2. Issue #22: [needs-human] Submit to awesome-claude-code — repo must be 7 days old; human will resubmit after cooldown
3. Triage comment format mismatch: watcher's detection pattern doesn't match actual triage output; causes unnecessary re-triggers

## Deferred
- Evolve history gap: evolve doesn't read research_log.md or check closed issues for deduplication

## Critical Note for Next Agent
- Workflow YAML changed (reviewer.yml) — PR requires needs-review label per autonomy rules
- The post-merge sync step in reviewer.yml is safe from infinite loops: README.md is not in deploy.yml path triggers, and reviewer only triggers on PR events
- WORKFLOW_PAT secret is configured — coder can push workflow YAML changes
- Issue #22 has been triaged (2 duplicate triage comments); do NOT re-trigger triage again

## Metrics Snapshot
Period: 2026-03-15 to 2026-03-22
- Total commits: 75+
- Stars: 1 | Forks: 0 | Adopters: 0
