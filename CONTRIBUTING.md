# Contributing to Tokenman

## Source zone vs runtime zone

Tokenman still uses a source-zone versus runtime-zone split. The repo
contains the harness source, while the runtime model remains the
reference shape for what a consumer repo will hold.

### Source zone - what tokenman is

These paths define the product and what ships to consumers:

- `harness/` - runtime code and workflow templates
- `docs/` - product and refactor docs
- `recommended-skills.yaml` - skill catalog metadata
- `tests/fixtures/` - synthetic consumer repos for harness testing

The catalog is the source of truth for skills. Do not add in-tree
product skills as a shortcut around the install flow.

Everything in `tests/fixtures/` should stay pristine.

### Runtime zone - what tokenman does

These paths describe the consumer runtime shape:

- `.tokenman/` - config, state, and runtime artifacts
- `.github/workflows/` - installed workflow entrypoints
- `.claude/skills/` - installed skills for a consumer repo
- `tokenman-state` - dedicated branch for append-only ledger history

The important rule is that runtime state should not distort the harness
design. Tokenman is being refactored toward an Actions-first runtime,
GitHub-native UI, and a smaller policy layer around `git`, `gh`, and
the coding agent.

## Current architecture direction

The current docs that define direction are:

- [`docs/spec.md`](docs/spec.md)
- [`docs/phase-1-product-scope.md`](docs/phase-1-product-scope.md)
- [`docs/actions-first-refactor-plan.md`](docs/actions-first-refactor-plan.md)

The short version:

- GitHub Actions is the primary runtime
- GitHub web and mobile are the primary UI
- local runs remain a setup and debugging path
- Phase 1 is docs-first and PR-only
- the ledger stays because cost is part of the product

Contributions should move the codebase toward that shape, not back
toward a larger custom runtime.

## Commit conventions

- Imperative, sentence case, no trailing period, under about 72 characters
- Use simple scopes when helpful: `docs: ...`, `fix: ...`, `feat: ...`,
  `test: ...`, `chore: ...`

## Running tests

Install dev dependencies and run pytest from the repo root:

```bash
pip install -e '.[dev]'
python -m pytest
```

## Code direction

Prefer simple ownership boundaries:

- Tokenman owns policy, scope, and ledger semantics
- the coding agent owns flexible repo edits
- `git` owns repo mechanics
- `gh` owns PR mechanics
- GitHub Actions owns scheduling and workflow runtime

Avoid adding new infrastructure when an existing tool already does the
job cleanly.
