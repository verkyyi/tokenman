# Tokenman - Current Spec

## Product sentence

Tokenman is a GitHub-native policy layer that makes coding-agent
maintenance runs safe to leave unattended.

## Current product boundary

The current target is intentionally narrow:

- GitHub Actions is the primary runtime
- GitHub web and mobile are the primary user interface
- local coding-agent sessions remain a setup and debugging path
- Phase 1 focuses on docs and `README.md` maintenance
- runs produce PRs only; there is no auto-merge path
- cost visibility is part of the product, so the ledger stays

Tokenman is not currently positioned as a broad autonomous maintenance
platform, a hosted service, or a custom execution framework.

## Target user

The best initial fit is maintainers who are already comfortable with:

- GitHub PR review
- coding-agent workflows such as Claude Code or Codex
- low-risk repo maintenance delegated to a scheduled system

That usually means solo developers, OSS maintainers, and small
AI-native teams.

## Interaction model

The primary user journey is GitHub-native:

- GitHub Actions runs scheduled or manually triggered jobs
- GitHub PRs are the review surface
- GitHub workflow summaries explain what happened on each run
- GitHub mobile and web are enough for routine operation

Local sessions still matter, but only as an operator path for setup,
scope editing, debugging, and one-off manual runs.

## Runtime model

The intended architecture is Actions-first and local-compatible.

GitHub Actions provides:

- scheduling
- workflow dispatch
- checked-out repo state
- run logs and summaries
- execution permissions

The coding agent provides:

- repo-specific reasoning
- file edits within allowed paths
- flexible implementation details

Tokenman provides:

- repo profiling
- scope drafting
- skill selection
- prompt assembly
- policy enforcement
- skip reasons
- cost accounting

## Responsibility split

Use this rule when deciding whether Tokenman should own behavior:

- If it is about how to edit the repo, prefer the coding agent.
- If it is about how to diff, commit, push, or open a PR, prefer `git`
  and `gh`.
- If it is about whether a run is allowed, what is in scope, what was
  skipped, and what it cost, keep it in Tokenman.

This means Tokenman should be a thin orchestration and policy layer, not
its own patch runtime.

## Ledger model

The ledger stays, but in a simpler form than earlier drafts.

- one append-only `ledger.jsonl`
- one record per run
- stored on a dedicated branch such as `tokenman-state`
- used for durable cost and outcome history

GitHub remains the UI for the current run. The ledger exists for
cross-run history and lightweight aggregation.

## Local compatibility

Actions-first does not mean Actions-only.

The same core pipeline should still be runnable from a local session
when needed:

- same runner
- same policy checks
- same scope logic
- same ledger model
- same `git` and `gh` integration

The local path is not the main product surface; it is the fastest way
to set up, debug, and recover from workflow issues without pushing every
experiment through CI.

## Out of scope for Phase 1

These are explicitly out of scope for the current release target:

- broad multi-skill maintenance positioning
- behavior-changing maintenance such as dependency upgrades or code cleanup
- adaptive scheduling and event-driven automation
- a hosted dashboard or GitHub Pages status surface
- a custom patch transport layer
- a generalized execution backend abstraction

## Canonical companion docs

- [`docs/phase-1-product-scope.md`](docs/phase-1-product-scope.md)
- [`docs/actions-first-refactor-plan.md`](docs/actions-first-refactor-plan.md)
- [`CONTRIBUTING.md`](../CONTRIBUTING.md)
