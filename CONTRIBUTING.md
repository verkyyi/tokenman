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
- `skills/` — **temporary** bootstrap for Phase 1.2b; see below
- `recommended-skills.yaml` — curated catalog
- `pricing.yaml` — budget calibration data
- `docs/` — documentation
- `tests/fixtures/` — synthetic consumer repos for harness testing

### `skills/` — temporary bootstrap

`skills/readme-maintainer/` lives in-tree during Phase 1.2b so the
harness has a real skill to invoke before the external skills
ecosystem exists. This is a deliberate, scoped violation of spec §5.1
("tokenman ships zero skills"). It must be split out to a standalone
repo before Phase 3 opens dogfood runs against the library itself.
Do not add more skills here. See `skills/README.md` for the full
rationale and exit plan.

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

## Running tests

Install dev dependencies and run pytest from the repo root:

```bash
pip install -e '.[dev]'
pytest
```

The canonical ledger schema lives at `harness/lib/ledger.schema.json`;
test fixtures at `tests/ledgers/*.jsonl`. The test suite validates every
fixture entry against the schema, so schema drift fails fast.

## Harness runtime modules

The Python harness lives under `harness/lib/`:

- `harness/lib/ledger.schema.json` — canonical ledger shape (from Phase 1.1).
- `harness/lib/ledger.py` — `validate()`, `append()`, `last_run_id()`. Enforces the conditional invariants the JSON Schema cannot express.
- `harness/lib/skill_executor.py` — `ExecutionResult`, `SkillExecutor` Protocol, `StubSkillExecutor` (tests only), `ClaudeSkillExecutor` (Phase 1.2b-ii, `claude -p` backed).
- `harness/lib/pr_opener.py` — `PROpener` Protocol + `PROpenerError`, `FakePROpener` (tests only), `GhPROpener` (Phase 1.2b-ii, `gh pr create` backed).
- `harness/lib/git_ops.py` — `apply_diff_and_push` (branch/apply/commit/push, Phase 1.2b-ii).
- `harness/lib/runner.py` — `run_skill`, the orchestrator.
- `harness/run/__main__.py` — `python -m harness.run` CLI (Phase 1.2b-ii).
- `harness/prompts/unattended_framing.v1.md` — versioned system-prompt framing for the unattended-claude invocation (Phase 1.2b-ii).

Tests for each module live at `tests/test_<module>.py`. The stub skill used by executor + runner integration tests lives at `tests/fixtures/skills/stub-readme/`.

Run `pytest` from the repo root after `pip install -e '.[dev]'`.

## Status

Phase 1.2b-ii is the current milestone: real-skill integration. The
runner now calls `claude -p` via `ClaudeSkillExecutor`, opens PRs via
`GhPROpener`, and exposes a `python -m harness.run` CLI consumed by a
consumer-deployable workflow template. `.tokenman/PAUSE` remains on
through Phase 2. See `docs/spec.md` §12 for the full phased roadmap.
