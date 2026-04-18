Continuing work on the tokenman library repo at /home/dev/projects/tokenman.

Context: Phase 1.3 is complete and merged. `main` at 5267e12 ships
`python -m harness.scope` — deterministic repo profile + Claude-Code
plugin marketplace discovery + one `claude -p` call + allowlist
backstop + interactive accept/edit, producing
`.tokenman/initial-scope.md`. All 83 tests pass (64 prior + 19 new);
opt-in live test (`TOKENMAN_LIVE=1`) passes against real `claude -p`
in ~20s.

Phase 1 decomposition status:

  1.1  — ledger schema + status.sh v1                           (DONE, 68c2893)
  1.2a — harness plumbing (stub-driven, no claude -p, no gh)    (DONE, 8e042f5)
  1.2b — real-skill integration                                 (DONE, f510600)
  1.3  — scoping flow (tokenman scope → initial-scope.md)       (DONE, 5267e12)
  1.4  — guided onboarding mode                                 (NEXT)

Working tree is clean. `main` is in sync with `origin/main`. No open
branches. `.tokenman/PAUSE` is still committed; PAUSE stays on through
Phase 2 per spec §12.

## What Phase 1.3 delivered

- `harness/lib/repo_profile.py` — `inspect(repo_dir) -> RepoProfile`
  (languages via extension tally, size, tests/CI/README presence,
  dep files, 30-day commit count). Rejects non-git dirs.
- `harness/lib/marketplace.py` — `list_plugins(refresh=False)` reads
  `~/.claude/plugins/marketplaces/*/.claude-plugin/marketplace.json`,
  skips malformed manifests, returns empty list if root missing.
- `harness/lib/scope_drafter.py`:
  - `ScopeDraft`, `RecommendedSkill`, `SkippedSkill`,
    `CandidatePlugin`, `Boundaries` TypedDicts.
  - `ScopeExecutor` Protocol + `StubScopeExecutor` + `ClaudeScopeExecutor`.
  - `draft(...)` — builds payload (inclusive of each local catalog
    entry's SKILL.md text), calls executor, validates schema, retries
    once on invalid JSON, enforces allowlist by demoting non-catalog
    `recommended_skills` to `candidate_uncurated_plugins`.
- `harness/prompts/scoping.v1.md` — versioned system-prompt framing.
- `harness/scope/__main__.py` — `python -m harness.scope
  [--repo .] [--refresh] [--claude-bin claude] [--output-path ...]
  [--non-interactive] [--dry-run]`. Interactive flow asks 4 questions,
  calls claude -p (or stub in dry-run), shows rendered preview,
  prompts accept/edit/abort.
- Tests: `test_repo_profile.py` (4), `test_marketplace.py` (3),
  `test_scope_drafter.py` (7), `test_scope_cli.py` (5),
  `test_scope_live.py` (1, TOKENMAN_LIVE gated).
- Fixtures added: `tests/fixtures/fake-marketplaces/{one,two}/`
  (one well-formed, one malformed) and
  `tests/fixtures/scope-captures/minimal.json`.
- README gained a Usage section mentioning both
  `python -m harness.scope` and `python -m harness.run`.

## Forward-facing cleanups surfaced during 1.2b (still open)

- Refresh `tests/fixtures/claude-captures/readme-maintainer.json`
  with a real captured invocation (currently synthetic).
- Workflow template's `claude` install step still echoes TODO.
  Pick the install command (likely `npm i -g @anthropic-ai/claude-code`)
  and drop the `exit 1` once verified.
- Split `skills/readme-maintainer/` out to a standalone repo before
  Phase 3. Tracked in `skills/README.md`, catalog entry, and
  `.tokenman/CLAUDE.md` forbidden list.
- `GhPROpener` has not been exercised against real GitHub end-to-end.
  A manual `workflow_dispatch` run against a throwaway consumer repo
  is the validation step.

## Forward-facing notes from 1.3

- Scoping currently only reads SKILL.md for catalog entries with
  local (`./`) sources. Remote (git URL) sources get
  `skill_md: null` and the LLM falls back to conservative boundary
  defaults. Remote fetching lands with Phase 1.4's install flow.
- `ClaudeScopeExecutor.run` timeout default is 180s, same shape as
  `ClaudeSkillExecutor`. Live test finishes in ~20s on the tiny
  fixture.

## Phase 1.4 — guided onboarding mode (next)

Per spec §6.4:

  gh workflow run tokenman.yml -f mode=onboarding

In onboarding mode:
  - Runs all enabled skills back-to-back in one session
  - Uses an elevated budget (3× normal weekly cap, still hard-capped)
  - Opens one labeled PR per skill
  - Writes `.tokenman/onboarding-summary.md` with observations, what
    each skill proposed (linked to PRs), what was considered but
    self-restrained, next steps, cost/budget utilization

Phase 1.4 is a fresh brainstorming + design + plan cycle. Read these
first:

  - docs/spec.md §6.4 (onboarding mode), §6.2 (install), §7 (budget
    — Phase 1.4 will need a lightweight budget stub even though
    enforcement lands Phase 2)
  - docs/superpowers/specs/2026-04-18-phase-1-3-scoping-flow-design.md
    (the scoping output is 1.4's input)
  - harness/workflows/tokenman.yml.template (onboarding mode is a
    new dispatch input the template will grow)
  - harness/run/__main__.py + harness/scope/__main__.py (1.4 may
    introduce `harness/onboard` as a sibling, or may extend
    `harness.run` with a `--mode onboarding` flag — open design
    question)

Entry ritual: start a fresh conversation, read this file, then invoke
the superpowers:brainstorming skill to scope Phase 1.4 before touching
code. Work in a worktree (branch `phase-1-4` off main).

Memory notes:
  - `feedback_execution_style.md` — default to inline execution when
    the plan is exhaustive. Phase 1.3 executed inline end-to-end in a
    single session; subagent dispatch would have been wasteful.
  - When running tests in a worktree, prefix with `PYTHONPATH=.` so
    pytest finds the worktree's modules instead of the installed
    package from the main checkout.
