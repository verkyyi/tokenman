# Actions-First Refactor Plan

This plan assumes the typical runtime is GitHub Actions, the primary user interface is GitHub itself (mobile and web), and the ledger remains part of the product because cost visibility is a core requirement. The ledger should be simplified to an append-only state file stored in GitHub, not treated as a local runtime subsystem. Local coding-agent sessions remain supported as a setup and debugging path, but not as the primary product surface.

## Product boundary

Tokenman should behave like a policy and trust layer around existing tools, not like a standalone automation runtime.

GitHub Actions should provide:

- scheduling
- manual dispatch
- checked-out repo state
- workflow logs and reruns
- execution permissions
- workflow summary output

The coding agent should provide:

- repo-specific reasoning
- file edits within allowed paths
- flexible implementation for maintenance tasks

Tokenman should provide:

- repo understanding
- scope selection
- skill selection
- policy enforcement
- skip reasons
- cost accounting

Local sessions should still be able to run the same core pipeline for:

- setup
- debugging
- manual recovery

## Core modules to keep

### `repo_profile.py`

Keep this module. It is product logic that turns a raw repository into structured signals for scope drafting and skill selection.

### `scope_drafter.py`

Keep this module, but narrow its responsibility to the Phase 1 product:

- docs-safe skill selection
- allowed paths
- exclusions
- cadence

It should not carry broader long-term platform ambitions into the first user experience.

### `runner.py`

Keep this module as the single-run coordinator. It should own workflow policy for one invocation:

- paused or not
- open PR lock
- cadence check
- budget guardrails
- allowed skill check

### `ledger.py`

Keep this module, but simplify it aggressively. GitHub Actions logs and step summaries are useful for the current run, but they are not a durable cost and outcome record across runs. Ledger remains justified because cost is part of the product promise.

The recommended design is:

- one append-only `ledger.jsonl`
- stored on a dedicated branch such as `tokenman-state`
- one JSON record per run
- no writes to the main working branch

The ledger should capture only stable product data such as:

- timestamp
- workflow run id
- run attempt
- skill
- outcome
- skip reason
- changed paths
- PR URL
- token counts
- estimated cost

GitHub should remain the UI for the current run. The ledger should exist only for durable history and lightweight aggregation.

## Modules to merge

### `onboarder.py` into `runner.py`

Onboarding should become a run mode, not a separate subsystem. In an Actions-first design, onboarding is just a special workflow dispatch with tighter limits and clearer summaries.

### `summary.py` into the runner output path

Summary generation should be part of the main run pipeline so the system emits one consistent output model for:

- GitHub step summaries
- PR body text
- ledger metadata

## Modules to shrink heavily

### `skill_executor.py`

Reduce this module to:

- prompt assembly
- coding agent invocation
- artifact capture
- token and result extraction

It should not own a patch transport layer or behave like a second execution runtime.

### `git_ops.py`

Reduce this module to a thin wrapper around standard `git` operations:

- inspect changed files with `git diff --name-only`
- reject out-of-scope paths
- `git add`
- `git commit`
- `git push`

The custom patch-generation and patch-application workflow should be removed.

### `pr_opener.py`

Reduce this module to a thin `gh` wrapper for:

- creating or updating a draft PR
- capturing PR number and URL
- applying labels and body text if needed

It should not own more PR protocol logic than necessary.

## Things to cut now

Cut these directly because they duplicate existing tools or infrastructure:

- custom patch generation and apply flow
- any scheduler logic beyond "should this workflow run now?"
- any abstraction for multiple execution backends before a second backend exists
- any separate status surface beyond GitHub workflow summaries, PRs, and the ledger
- any GitHub Pages status idea
- any attempt to use Actions logs, summaries, or artifacts as the long-term ledger

## Target architecture

The simplified runtime should be:

1. GitHub Actions triggers from `schedule` or `workflow_dispatch`.
2. The runner loads repo profile and scope.
3. The runner checks policy:
   - pause file
   - open PR lock
   - cadence
   - skill allowlist
   - budget guardrails
4. The skill executor builds the prompt and invokes the coding agent against the checked-out repo.
5. The git adapter inspects changed paths.
6. The runner rejects out-of-scope edits.
7. If there is no valid change, the runner writes a `no_change` ledger entry and exits cleanly.
8. If there is a valid change, `git` stages, commits, and pushes it.
9. `gh` opens or updates a draft PR.
10. The runner appends the final record to `ledger.jsonl` on the dedicated state branch with outcome, cost, changed paths, skip reason, and PR URL.

The same pipeline should remain runnable from a local session with
stdout summaries instead of GitHub workflow summaries.

## Practical implementation rule

Use this rule to decide whether code should exist:

- If it is about how to edit the repo, prefer the coding agent.
- If it is about how to store, diff, commit, push, or open a PR, prefer `git` and `gh`.
- If it is about when a run is allowed, what is in scope, what was skipped, and what it cost, keep it in Tokenman.
- If it is about durable run history, keep the data model in Tokenman but use GitHub as the storage layer.

## Refactor sequence

When this work starts, the safest order is:

1. Remove custom patch transport and make the agent edit the checkout directly.
2. Collapse onboarding into the runner as a mode.
3. Shrink `git_ops.py` to thin `git` wrappers and path-scope enforcement.
4. Shrink `pr_opener.py` to thin `gh` integration.
5. Simplify `ledger.py` to append normalized run records to `ledger.jsonl` on the dedicated state branch.
6. Merge summary generation into the runner output path.
7. Trim config and docs so the product surface matches the simplified runtime.

## Desired end state

The codebase should converge on a small number of responsibilities:

- GitHub Actions provides the runtime
- the coding agent provides flexible repo-specific edits
- `git` and `gh` provide repository mechanics
- Tokenman provides policy, trust, and cost accountability
- the ledger is a tiny append-only history file stored on a dedicated GitHub branch

That is the implementation that best matches the current product positioning.
