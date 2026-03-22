# Incremental Evolve — Lightweight Staleness Awareness

Closes #44.

## Problem

Each evolve.yml run starts with zero memory of the previous run. The agent re-fetches all 12+ research sources, re-reads the full git log, re-explores the repo structure, and re-analyzes every step — even when nothing has changed since an hour ago. Usage data shows runs averaging 30-43 turns and 600K-950K input tokens, with many consecutive runs finding "all unchanged from prior run."

The goal is not cost reduction (users run on subscriptions) but efficiency: fewer wasted turns, faster runs, and more focused analysis on what actually changed.

## Design

A single new state file (`state/last_evolve_summary.md`) written at the end of each run and injected into the next run's prompt. The LLM uses this to skip unchanged steps. No bash conditionals — the prompt builder stays simple.

### last_evolve_summary.md Format

Written by the agent at the end of Step 4 (Update project state):

```markdown
# Last Evolve Summary
Timestamp: 2026-03-22T14:11:04Z
Mode: HUMAN_ACTIVE=false
Main HEAD: abc1234
Open issues: #22, #43, #44

## Research Source Digests
anthropics/claude-code: def5678 | v1.2.3 released with hooks improvement
garrytan/gstack: ghi9012 | v0.9.9.0, no changes
...

## Steps Executed
Step 1: Research — 12 sources checked, 1 new finding (deer-flow gateway fix)
Step 2: Analyze — no new patterns in agent_log
Step 2a: Pipeline — 10 failures, all ALREADY-FIXED
Step 2b: Design — minor spacing fix applied
Step 2c: Growth — skipped (not hour 06)
...

## Findings Summary
No actionable findings. 0 issues created.
```

### Prompt Changes

Two additions to the prompt builder step:

**1. Inject the summary** (alongside existing `$(cat ...)` blocks at lines 402-417):

```
## Previous Evolve Run Summary
$(cat state/last_evolve_summary.md 2>/dev/null || echo "No previous run summary available — perform full analysis.")
```

**2. Add incremental analysis instructions** (after the existing HUMANFLAG block, before the step definitions):

```
## Incremental Analysis Rules
Read the Previous Evolve Run Summary above.
- If the summary is missing or older than 24 hours: perform a full analysis of all steps.
- If the summary is recent (< 24 hours): for each step, compare what you find against the summary.
  - Research sources: if a source's latest commit SHA matches the summary, state "unchanged since last run" and move on. Only log sources that have new commits.
  - Pipeline health: if no new failed runs since the summary timestamp, state "no new failures" and move on.
  - Design evaluation: if no new commits touching site files since the summary, skip.
  - Other steps: use your judgment — if the data matches the summary, skip the detailed analysis.
- Always execute Step 3 (logging) and Step 4 (state update).
- Always write an updated last_evolve_summary.md at the end of the run, even if nothing changed.
- If the previous summary shows HUMAN_ACTIVE=true and the current run is HUMAN_ACTIVE=false, treat steps that were skipped due to HUMAN_ACTIVE mode as needing full analysis (the previous run's skip was policy-driven, not data-driven).
- When skipping a step, use one sentence. Do not re-analyze data you've already confirmed is unchanged.
```

**3. Add summary write instruction** (at the end of Step 4):

```
Also write state/last_evolve_summary.md with: timestamp, HUMAN_ACTIVE mode,
main HEAD SHA, open issues list, per-source latest commit SHA and one-line summary,
which steps were executed vs skipped, and a findings summary.
Use the format shown in the Previous Evolve Run Summary section above.
```

### Expected Behavior

| Scenario | Before | After |
|----------|--------|-------|
| Nothing changed since last run | 30-43 turns, 600K-950K tokens | ~10-15 turns — confirms each source unchanged, logs, updates state |
| One research source has a new commit | Same as above | ~15-20 turns — full analysis on that source, skips others |
| Summary missing or stale (>24h) | Same as above | Full run (same as current behavior) |
| New workflow failures detected | Same as above | Full pipeline analysis, skips unchanged research |

### State File Lifecycle

- Written by the evolve agent at end of each run (Step 4)
- Committed via `scripts/commit-state.sh` (existing atomic state write path)
- Read by the prompt builder via `$(cat ...)` shell expansion
- No special cleanup needed — overwritten each run

### Edge Cases

**First run (new untracked file):** The "Commit state changes via API" step (line 464-473) uses `git diff --name-only state/` which only lists tracked, modified files. A brand new `state/last_evolve_summary.md` won't appear. Fix: add `git ls-files --others --exclude-standard state/` to also pick up untracked state files in the commit loop.

**Cancellation (cancel-in-progress):** If a run is cancelled before committing the summary, it's lost. The next run sees the older summary (or none) and falls back to a fuller analysis. This is correct behavior — no special handling needed.

**HUMAN_ACTIVE runs:** The agent always writes the summary, including the `Mode: HUMAN_ACTIVE=true/false` field. When the next run reads a summary from a HUMAN_ACTIVE run, the incremental rules account for this: if the previous run was HUMAN_ACTIVE (meaning Steps 2b and 5 were skipped, and no issues were created), the next non-HUMAN_ACTIVE run must NOT skip those steps based on the previous summary. The prompt instruction should state: "If the previous summary shows HUMAN_ACTIVE=true and the current run is HUMAN_ACTIVE=false, treat steps that were skipped due to HUMAN_ACTIVE as needing full analysis."

**Open issues field:** This lists all open repo issues (from `gh issue list`), not just evolve-finding issues. The agent already runs `gh issue list` in its analysis, so this adds no extra API call — it just records the result for the next run to compare against.

**Timestamp parsing:** The summary uses UTC with Z suffix (`2026-03-22T14:11:04Z`). The 24-hour staleness check depends on the LLM correctly computing the delta. This is reliable for UTC timestamps but has no bash-level enforcement, consistent with the "no bash conditionals" design constraint.

## Affected Files

| File | Change |
|------|--------|
| `.github/workflows/evolve.yml` | Add `$(cat state/last_evolve_summary.md)` to context injection block (line ~416). Add incremental analysis instructions to prompt (after line ~61). Add summary write instruction to Step 4 (after line ~368). |
| `.github/workflows/evolve.yml` | Fix "Commit state changes via API" step (line ~467) to also commit untracked state files. |
| `state/last_evolve_summary.md` | New file — created by agent on first run after this change |

## What This Does NOT Do

- Does not add bash conditional logic to the prompt builder
- Does not change the prompt structure (same steps, same order)
- Does not affect other workflows (watcher, coder, etc.) — though the same pattern could be applied later
- Does not guarantee exact turn/token targets — the LLM decides what to skip based on the summary
- Does not remove any analysis capability — everything still runs when changes are detected
