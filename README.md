# Tokenman

**Tokenman is the runtime that makes `claude -p` safe to run unattended on your repo.**

It lets any repo install a background maintenance agent that proposes
changes via PRs on a schedule, within a budget the user controls, without
requiring supervision.

## Status

Pre-release. Phase 0 scaffolding is in place; nothing runs yet. See
[`docs/spec.md`](docs/spec.md) for the full scoping draft and phased
roadmap.

## What tokenman ships

- A harness (scheduled workflows, guardrails, observability)
- A scoping and onboarding flow
- A curated catalog of recommended community skills (references, not copies)
- Documentation and conventions

## What tokenman does not ship

- Its own skills
- Hosted infrastructure
- Cloud accounts or dashboards

## Repository structure

This repo is both the library (source of the harness) and its own
first paused-by-default consumer. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the source-zone versus
runtime-zone split.

## License

See [LICENSE](LICENSE).
