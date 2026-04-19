# Tokenman

Tokenman is a harness that makes `claude -p` safe to run unattended on a repo.
See `docs/spec.md` for the full scoping draft.

## For interactive Claude Code sessions

- **Direction & architecture**: `docs/spec.md` (authoritative)
- **Contributor workflow & source/runtime split**: `CONTRIBUTING.md`
- **Dogfooding boundaries (runtime zone)**: `.tokenman/CLAUDE.md` — strict

## Commit conventions
Imperative, sentence case, no period, <72 chars.
- feat(action|harness|ledger|dogfood): …
- fix(…): …
- docs: …
- chore: …
- test: …

## What NOT to do in this repo
- Do not modify files in `harness/` from a dogfood run. The paranoid
  `.tokenman/CLAUDE.md` forbids this.
- Do not modify `tests/fixtures/` — harness tests must be able to reset them.
- Do not widen dogfood scope beyond the current README-only gate without
  updating `.tokenman/CLAUDE.md` and `.tokenman/tokenman.yaml` together.
- Do not call the Anthropic API directly — action runs go through the official
  Claude Code Action.

## Failure log
(fresh — no entries)
