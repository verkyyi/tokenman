# Contributing to Tokenman

## Source zone vs runtime zone

Tokenman lives in a single repository that plays two roles at once: it is
both the library (source of the harness) and its own first paused-by-default
consumer. To keep these from entangling, the repo is split into two zones.

### Source zone — what tokenman *is*

These paths contain the code and assets that ship to consumers when a
user runs `/tokenman init` in their repo:

- `harness/` — runtime code and workflow templates
- `scoping/` — discovery and scope-proposal logic
- `onboarding/` — guided first-run flow
- `recommended-skills.yaml` — curated catalog
- `pricing.yaml` — budget calibration data
- `docs/` — documentation
- `tests/fixtures/` — synthetic consumer repos for harness testing

Edits to source-zone files are the main library-development work.
Everything in `tests/fixtures/` stays pristine — harness tests reset it.

### Runtime zone — what tokenman *does on this repo*

These paths contain the library's own paused dogfood state:

- `.tokenman/` — config, state, ledger, artifacts
- `.github/workflows/` — actual workflows that run on this repo
- `.claude/skills/` — skills installed for this repo's dogfooding

The library's runtime zone is the canonical example of what a consumer's
runtime zone looks like — structurally identical, just with stricter
caps and a `dogfood:` field in `tokenman.yaml`.

### Why the separation matters

Updates to `harness/workflows/tokenman.yml.template` (source) do NOT
automatically update `.github/workflows/tokenman.yml` (runtime, once
installed). The runtime copy is a deliberate install step. At Phase 0
the runtime workflow file does not exist yet — it is installed when
dogfood unpauses at Phase 3. This preserves the ability to ship library
changes without immediately dogfooding them.

## Commit conventions

- Imperative, sentence case, no trailing period, under ~72 characters
- Use scope prefixes: `feat(harness|scoping|onboarding|catalog|dogfood): …`,
  `fix(…): …`, `docs: …`, `chore: …`, `test: …`
- PRs opened by the harness itself (once dogfood unpauses at Phase 3)
  use the `[tokenman]` prefix per `docs/spec.md` §10.6, enabling clean
  filtering of human versus harness history:

  ```
  git log --grep='\[tokenman\]' --invert-grep    # human commits only
  git log --grep='\[tokenman\]'                  # dogfood commits only
  ```

## Phase 0 status

The harness is not implemented yet. Phase 0 establishes scaffolding
and contracts. See `docs/spec.md` §12 for the full phased roadmap.
