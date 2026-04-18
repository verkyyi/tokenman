Continuing work on the tokenman library repo at /home/dev/projects/tokenman.

Context: Phase 1.2b is complete and merged. `main` at f510600 has a working
end-to-end harness loop (claude -p → git apply/commit/push → gh pr create)
plus the first cataloged skill and a consumer-deployable workflow template.
All 64 tests pass; the opt-in live test (`TOKENMAN_LIVE=1`) passes against
real claude in ~25s.

Phase 1 decomposition status:

  1.1  — ledger schema + status.sh v1                           (DONE, 68c2893)
  1.2a — harness plumbing (stub-driven, no claude -p, no gh)    (DONE, 8e042f5)
  1.2b — real-skill integration                                 (DONE, f510600)
  1.3  — scoping flow (tokenman scope → initial-scope.md)       (NEXT)
  1.4  — guided onboarding mode

Working tree is clean. `main` is in sync with `origin/main`. No open
branches. `.tokenman/PAUSE` is still committed; PAUSE stays on through
Phase 2 per spec §12.

## What Phase 1.2b delivered

- `harness/lib/git_ops.py` — `apply_diff_and_push` with rollback
- `harness/lib/skill_executor.py` — `ClaudeSkillExecutor` (copies repo →
  scratch, overlays skill at `.claude/skills/<name>/`, runs
  `claude -p --output-format json --append-system-prompt <framing>`,
  diffs after; excludes `.claude/.git/.tokenman` from copy and diff).
  Stub executor kept intact.
- `harness/lib/pr_opener.py` — `GhPROpener` (thin `gh pr create --json
  number -q .number`) and `PROpenerError`. Fake executor kept intact.
- `harness/lib/runner.py` — now calls `apply_diff_and_push` before
  `pr_opener.open`; new kwargs `base_branch="main"` and `git_identity`;
  error branch narrowed to `(GitOpsError, PROpenerError)`.
- `harness/lib/ledger.py` — `LedgerEntry`, `GeneratorBlock`,
  `EvaluatorBlock` TypedDicts.
- `harness/prompts/unattended_framing.v1.md` — versioned system-prompt
  framing. Bump = new file, new `prompt_version`.
- `harness/run/__main__.py` — `python -m harness.run --skill <name>
  [--repo .] [--ledger-path] [--runs-dir] [--claude-bin] [--base-branch]
  [--dry-run]`. `--dry-run` swaps in the `stub-readme` fixture + fake
  PR opener for local iteration.
- `harness/workflows/tokenman.yml.template` — consumer-deployable
  workflow (workflow_dispatch only, no schedule yet). One unresolved
  TODO: the `claude` CLI install step. Resolve during Phase 1.4
  onboarding work or leave until a real external consumer onboards.
- `skills/readme-maintainer/SKILL.md` — first in-tree skill. See
  `skills/README.md` for the bootstrap-posture explanation and the
  commitment to split it out to a sibling repo before Phase 3 dogfood
  opens.
- `recommended-skills.yaml` — first entry pointing at
  `./skills/readme-maintainer`.
- Tests: mock executor (4), replay against recorded fixture (1; fixture
  currently synthetic — flagged to refresh with a real capture), live
  smoke (1, gated by `TOKENMAN_LIVE=1`), git_ops (2), gh_pr_opener (4),
  CLI (2).

## Forward-facing cleanups surfaced during 1.2b (not blockers)

- The synthetic `tests/fixtures/claude-captures/readme-maintainer.json`
  should be refreshed with a real captured invocation. Simple: run the
  capture snippet in the Phase 1.2b plan (Task 25, Step 2) now that
  `skills/readme-maintainer/` exists and `claude` is available.
- The workflow template's `claude` install step still echoes TODO. Pick
  the install command (likely `npm i -g @anthropic-ai/claude-code`) and
  drop the `exit 1` once verified.
- Split `skills/readme-maintainer/` out to a standalone repo before
  Phase 3. Tracked in `skills/README.md`, catalog entry, and
  `.tokenman/CLAUDE.md` forbidden list.
- `GhPROpener` has not been exercised against real GitHub end-to-end.
  A manual `workflow_dispatch` run against a throwaway consumer repo
  is the validation step — can do before or during Phase 1.3.

## Phase 1.3 — scoping flow (next)

Per spec §6.3:

  tokenman scope

Produces `.tokenman/initial-scope.md` drafting:
  - Repo profile (language, size, test coverage, activity, deps)
  - Suggested skills (3–5 from the catalog, chosen from repo profile)
  - Skipped skills (with reasoning)
  - Suggested boundaries (file allowlists/denylists)
  - Suggested budget (% of subscription — see §7 summary)
  - Suggested schedule strategy
  - Expected PR volume

Phase 1.3 is a fresh brainstorming + design + plan cycle. Read these
first for context:

  - docs/spec.md §6.3 (scoping flow target behavior) and §5.1
    (catalog schema — scoping consumes it)
  - docs/superpowers/specs/2026-04-18-phase-1-2b-real-skill-integration-design.md
    (in particular "What's deliberately NOT in 1.2b" — 1.3's scope)
  - recommended-skills.yaml (only one entry today; 1.3 might add the
    "what's in the catalog?" question before scoping can recommend
    anything meaningful)
  - harness/lib/runner.py and harness/run/__main__.py (the scoping CLI
    will likely live alongside `harness/run` as another subcommand, or
    as its own `python -m harness.scope` module — open design question)

Entry ritual: start a fresh conversation, read this file, then invoke
the superpowers:brainstorming skill to scope Phase 1.3 before touching
code. Work in a worktree (branch `phase-1-3` off main).

Memory note: the `feedback_execution_style.md` entry captures a
preference from this project — default to inline execution once the
implementation plan is exhaustive; subagent-driven-development only
pays for tasks where independent review gate value is high. Phase 1.2b
switched mid-phase and finished in a fraction of the initial pace.
