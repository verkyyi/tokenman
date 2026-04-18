# Tokenman

**Tokenman is a GitHub-native policy layer that makes coding-agent
maintenance runs safe to leave unattended.**

The product target is narrow on purpose: GitHub Actions runs a coding
agent on a schedule or manual dispatch, Tokenman enforces scope and
guardrails, and the result is a reviewable PR plus durable cost history.

## Current direction

Tokenman is pre-release and currently being refactored toward an
Actions-first, docs-first Phase 1:

- GitHub Actions is the primary runtime
- GitHub web and mobile are the primary user interface
- local coding-agent sessions remain a setup and debugging path
- the initial product scope is docs and `README.md` maintenance only
- the ledger stays because cost visibility is part of the product

## What Tokenman owns

- repo profiling and scope drafting
- skill selection and prompt assembly
- policy checks such as pause, allowed paths, and one-open-PR lock
- append-only cost and outcome history

## What Tokenman does not try to own

- repo mechanics that `git` already handles
- PR mechanics that `gh` already handles
- a hosted control plane or dashboard
- a broad autonomous maintenance platform in Phase 1

## Current CLI path

The current consumer flow in the harness is:

1. `python -m harness.scope --repo <path>` - draft
   `.tokenman/initial-scope.md` for a repo
2. `python -m harness.install --repo <path>` - fetch curated skills from
   `recommended-skills.yaml` into `<path>/.claude/skills/`
3. `python -m harness.onboard --repo <path>` - run enabled skills
   back-to-back and open reviewable PRs

Individual skill runs remain available through
`python -m harness.run --skill <name> --repo <path>`.

## Document map

- [`docs/spec.md`](docs/spec.md) - current product and architecture spec
- [`docs/phase-1-product-scope.md`](docs/phase-1-product-scope.md) -
  narrowed product boundary for the first release
- [`docs/actions-first-refactor-plan.md`](docs/actions-first-refactor-plan.md) -
  module-level refactor target
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - contributor guidance for the
  current architecture

## Repository structure

This repo contains the harness source and the docs that define the
current product direction. The working model is still a source zone
versus runtime zone split; contributor guidance lives in
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

See [LICENSE](LICENSE).
