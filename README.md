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

## Usage

Command-line tools shipped with the harness (run from a consumer repo
that has `tokenman` installed):

1. `python -m harness.scope --repo <path>` — draft `.tokenman/initial-scope.md` for a repo (spec §6.3). Interactive; use `--non-interactive` for automation, `--dry-run` to skip the live `claude -p` call.
2. `python -m harness.install --repo <path>` — fetch skills from `recommended-skills.yaml` into `<path>/.claude/skills/` (spec §5.2, §6.2). Pass `--skill NAME` (repeatable) to install a subset; `--force` to overwrite drifted installs.
3. `python -m harness.onboard --repo <path>` — run every enabled skill back-to-back, open a PR per skill, write `.tokenman/onboarding-summary.md` (spec §6.4).

Individual skill runs: `python -m harness.run --skill <name> --repo <path>` (spec §4).

## Repository structure

This repo is both the library (source of the harness) and its own
first paused-by-default consumer. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the source-zone versus
runtime-zone split.

## License

See [LICENSE](LICENSE).
