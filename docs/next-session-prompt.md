Continuing work on the tokenman library repo at /home/dev/projects/tokenman.

Context: Phase 1.4 is complete and merged. `main` at 5c85456 ships
`python -m harness.onboard` — orchestrator that loops every enabled
skill in one session through the existing `runner.run_skill` path,
opens one PR per skill via `GhPROpener`, and writes
`.tokenman/onboarding-summary.md` from a deterministic markdown
renderer. Workflow template gained a `mode` input
(`single | onboarding`, default `single` — backwards compatible).
Lightweight in-process budget stub: per_run_ceiling (default 30k) +
session_ceiling (default 3 × per_run × N_skills); session breaches
synthesize schema-valid `skipped_budget` ledger entries; per-skill
errors do not abort onboarding. All 102 tests pass + 3 opt-in skipped;
opt-in live test (`TOKENMAN_LIVE=1`) passes against real `claude -p`
in ~30s.

Phase 1 decomposition status:

  1.1  — ledger schema + status.sh v1                           (DONE, 68c2893)
  1.2a — harness plumbing (stub-driven, no claude -p, no gh)    (DONE, 8e042f5)
  1.2b — real-skill integration                                 (DONE, f510600)
  1.3  — scoping flow (tokenman scope → initial-scope.md)       (DONE, 5267e12)
  1.4  — guided onboarding mode                                 (DONE, 5c85456)
  1.5  — skill install flow (catalog → .claude/skills/)         (NEXT)

Working tree is clean. `main` is in sync with `origin/main`. No open
branches. `.tokenman/PAUSE` is still committed; PAUSE stays on through
Phase 2 per spec §12.

## What Phase 1.4 delivered

- `harness/lib/onboarder.py`:
  - `OnboardingBudget` (frozen dataclass: per_run_ceiling, session_ceiling).
  - `OnboardingResult` (frozen dataclass: entries, total_tokens,
    session_ceiling, started_at, finished_at, breached_ceiling).
  - `OnboardingError` exception for empty-skills guard.
  - `_synth_skipped_entry(*, skill_name, run_id, now)` — schema-valid
    skipped_budget ledger entry builder.
  - `run_onboarding(...)` — pre-flight worst-case check
    (`total_tokens + per_run_ceiling > session_ceiling`), iterates
    skills via `runner.run_skill`, continues past per-skill errors,
    synthesizes skipped_budget entries on session breach.
- `harness/lib/summary.py` — pure renderer: `build(*, result,
  repo_name, today=None) -> str`. Sections: title + token header,
  ## What ran, ## Pull requests opened, ## What was considered but
  not proposed, ## What was skipped, ## Next steps. Uses tightened
  `LedgerEntry` type hints throughout.
- `harness/onboard/__main__.py` — `python -m harness.onboard
  [--repo .] [--config-path ...] [--ledger-path ...] [--runs-dir ...]
  [--output-path ...] [--claude-bin claude] [--base-branch main]
  [--per-run-ceiling 30000] [--session-ceiling N] [--skill NAME ...]
  [--non-interactive] [--dry-run]`. Skill resolution: `--skill` flags
  override config; otherwise reads `tokenman.yaml`'s `skills:` list.
  No-skills hits exit 2 with a hint pointing at `harness.scope` /
  `--skill`. Dry-run substitutes StubSkillExecutor + FakePROpener and
  resolves every skill to the stub-readme fixture. Local helpers
  (`_tokenman_root`, `_load_catalog`, `_resolve_skill_dir`) duplicated
  from `harness.run.__main__` (deliberate — premature catalog.py
  extraction was rejected).
- `harness/workflows/tokenman.yml.template` — `mode` input
  (single|onboarding, default single, type=choice); `skill` flipped
  to required=false; run step `if/else` branches on
  `${{ inputs.mode }}`; artifact name now `tokenman-${{ inputs.mode
  }}-${{ github.run_id }}` for distinguishability. The Phase 1.2b
  `claude install` TODO + `exit 1` are intentionally preserved.
- Tests added (17 new, across 8 files):
  `test_onboarder.py` (5 — dataclass invariants, synth helper, happy
  path), `test_onboarder_budget.py` (1), `test_onboarder_continues_on_error.py`
  (1), `test_onboarder_empty_skills.py` (1), `test_summary.py` (6),
  `test_onboard_cli.py` (1), `test_onboard_cli_no_skills.py` (1),
  `test_workflow_template.py` (3), `test_onboard_live.py` (1,
  TOKENMAN_LIVE gated).
- Fixtures: `tests/fixtures/skills/stub-readme-second/` (mirrors
  stub-readme but with distinct summary lines so multi-skill loops
  can distinguish entries) and
  `tests/fixtures/onboarding-results/minimal.json` (canned
  OnboardingResult for `test_summary.py`).
- README gained one-line mention of `python -m harness.onboard`.

## Forward-facing cleanups (still open)

These were called out earlier and remain open — none block Phase 1.5,
but worth a parallel cleanup pass before Phase 2:

- Refresh `tests/fixtures/claude-captures/readme-maintainer.json`
  with a real captured invocation (currently synthetic).
- Workflow template's `claude` install step still echoes TODO + has
  `exit 1`. Pick the install command (likely
  `npm i -g @anthropic-ai/claude-code`) and drop the `exit 1` once
  verified end-to-end.
- Split `skills/readme-maintainer/` out to a standalone repo before
  Phase 3. Tracked in `skills/README.md`, catalog entry, and
  `.tokenman/CLAUDE.md` forbidden list. Phase 1.5 is a natural moment
  for this — extracting the skill exercises the very install flow
  Phase 1.5 is building.
- `GhPROpener` has not been exercised against real GitHub
  end-to-end. A manual `workflow_dispatch` run against a throwaway
  consumer repo is the validation step.

## Forward-facing notes from 1.4

- Onboarding currently assumes `.claude/skills/` is already populated,
  AND only resolves catalog entries whose `source:` is local (`./...`).
  Remote git-URL sources hit a hard exit 2 ("remote skill sources
  land in Phase 1.5"). That's exactly the gap Phase 1.5 closes.
- Per-skill errors do not abort the onboarding session; they're
  surfaced in `## What was skipped` with a pointer to
  `runs/<run_id>/executor.stderr`.
- `_seed_git_repo` test helper is duplicated across 5 test files.
  Plan deferred conftest.py extraction; do it the next time fixture
  shape changes.
- `_resolve_skill_dir` raises `SystemExit` (caught and converted to
  exit 2 in main()). Inherited from `harness.run.__main__`. Worth
  replacing with a domain exception (e.g. `SkillResolutionError`)
  during the next refactor pass.

## Phase 1.5 — skill install flow (next)

Per spec §6.2 ("/tokenman init") and §5.2 ("Skill installation"):

  /tokenman init   →   fetches skills from their pinned sources
                       into the consumer's .claude/skills/

What 1.5 needs to deliver:
  - Read `recommended-skills.yaml` and resolve any non-local
    `source:` entries (git URLs at minimum) by cloning/fetching
    into `.claude/skills/<skill-name>/` at the pinned `version:`
    (a tag or sha).
  - Update `harness.scope` and `harness.onboard` to drop their
    "local sources only" guard once install can populate
    `.claude/skills/`. Scope's payload should include `skill_md`
    text for installed remote skills the same way it does for
    local ones today.
  - Likely a new `python -m harness.install` CLI sibling to
    scope/onboard/run, plus `harness/lib/installer.py` for the
    pure logic.
  - A real consumer journey: `harness.scope` → `harness.install`
    → `harness.onboard`. README Usage should reflect that ordering.

Phase 1.5 is a fresh brainstorming + design + plan cycle. Read these
first:

  - docs/spec.md §5 (skills model — reference don't ship), §6.2
    (install), §6.3 (initial scoping), §6.4 (onboarding)
  - docs/superpowers/specs/2026-04-18-phase-1-4-onboarding-mode-design.md
    §2 (non-goals — explicitly defers install to 1.5)
  - recommended-skills.yaml (catalog format; readme-maintainer
    currently has a `./skills/readme-maintainer` source — extracting
    it to a remote repo is the natural first integration test for
    install)
  - skills/README.md (bootstrap posture explaining why
    skills/readme-maintainer is in-tree today)
  - harness/scope/__main__.py and harness/onboard/__main__.py — both
    have a `_resolve_skill_dir` that hard-rejects non-local sources;
    Phase 1.5 needs to update those paths

Open design questions for the brainstorm:
  - Where do remote skills land? `.claude/skills/<name>/` (per spec
    §3.4) or `~/.claude/skills/`? (Spec says the former; confirm.)
  - Pin format: tag, sha, semver range? `recommended-skills.yaml`
    currently uses `version: 0.1.0` for the in-tree skill — what
    does that look like for a real git remote?
  - Do we shell out to `git clone` or use a Python git library?
    (`git_ops.py` already shells out to git — consistent.)
  - Does install verify the SKILL.md exists and parses, or fail
    loudly if a remote source has drifted?
  - Idempotency: re-running install when `.claude/skills/<name>/`
    exists at the right version — no-op? Force-re-clone with `--force`?

Entry ritual: start a fresh conversation, read this file, then invoke
the superpowers:brainstorming skill to scope Phase 1.5 before touching
code. Work in a worktree (branch `phase-1-5` off main).

Memory notes:
  - `feedback_execution_style.md` — default to inline execution when
    the plan is exhaustive.
  - `feedback_decision_style.md` — during brainstorming, follow
    instinct and present decisions; skip A/B/C survey questions when
    one option is clearly better or precedent already settles it.
  - When running tests in a worktree, prefix with `PYTHONPATH=.` so
    pytest finds the worktree's modules instead of any installed
    package from the main checkout.
  - Reviewer subagents have, on at least one occasion, accidentally
    written and committed files to the main checkout instead of just
    reading the worktree. Brief them explicitly: "REVIEW ONLY. DO NOT
    WRITE OR COMMIT ANY FILES. Use only <worktree-path>."
