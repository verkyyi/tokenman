# Tokenman

Tokenman is a harness that makes `claude -p` safe to run unattended on a repo.
See `docs/spec.md` for the full scoping draft.

## For interactive Claude Code sessions

- **Direction & architecture**: `docs/spec.md` (authoritative)
- **Contributor workflow & source/runtime split**: `CONTRIBUTING.md`
- **Dogfooding boundaries (runtime zone)**: `.tokenman/CLAUDE.md` — strict

## Commit conventions
Imperative, sentence case, no period, <72 chars.
- feat(harness|scoping|onboarding|catalog|dogfood): …
- fix(harness|…): …
- docs: …
- chore: …
- test: …

## What NOT to do in this repo
- Do not modify files in `harness/`, `scoping/`, `onboarding/`,
  `recommended-skills.yaml`, or `pricing.yaml` from a dogfood run. The
  paranoid `.tokenman/CLAUDE.md` forbids this.
- Do not remove `.tokenman/PAUSE` until the Phase 3 gate (spec §12).
- Do not call the Anthropic API directly — all execution goes through `claude -p`.

## Failure log
(fresh — no entries)
