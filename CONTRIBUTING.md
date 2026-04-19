# Contributing to Tokenman

## Source zone vs runtime zone

Tokenman is now a narrow GitHub Action product. The repo contains the
action contract plus the internal Python modules that implement prompt
preparation, validation, routing, and ledger writes.

### Source zone - what tokenman is

These paths define the product and what ships to consumers:

- `action.yml` - GitHub Action contract
- `entrypoint.sh` - thin shell preflight
- `prompt.md` - fixed docs-maintainer framing
- `harness/` - internal action/runtime implementation
- `docs/` - current product docs
- `tests/` - action and runtime validation

### Runtime zone - what tokenman does

These paths describe the consumer runtime shape:

- checked-out repo contents under GitHub Actions
- `.tokenman/` - run state and artifacts for the current invocation
- `.github/workflows/` - consumer workflow entrypoints
- `tokenman-state` - dedicated branch for append-only ledger history

The important rule is that runtime state should not distort the harness
design. Tokenman is a GitHub-native policy layer around the official
Claude Code Action, plus `git`/`gh` for repository mechanics.

## Current architecture direction

The current docs that define direction are:

- [`docs/spec.md`](docs/spec.md)
- [`README.md`](README.md)

The short version:

- GitHub Actions is the primary runtime
- GitHub web and mobile are the primary UI
- the MVP is one job: `docs_maintainer`
- the trust boundary is explicit `read_paths` / `write_paths`
- outcomes are pull request, issue, or no-op
- the ledger stays because cost is part of the product

Contributions should move the codebase toward that shape, not back
toward a larger local runtime or skill platform.

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

- Tokenman owns policy, prompt shaping, validation, and ledger semantics
- the coding agent owns flexible repo edits
- `git` owns repo mechanics
- `gh` owns PR mechanics
- GitHub Actions owns scheduling and workflow runtime

Avoid adding new infrastructure when an existing tool already does the
job cleanly.
