Continuing work on the tokenman library repo at /home/dev/projects/tokenman.

Context: Phase 1.5 is complete and merged. `main` ships
`python -m harness.install` — fetches skills from
`recommended-skills.yaml` into `<consumer>/.claude/skills/` at a pinned
ref, writes `.tokenman-skill-lock` for drift detection, idempotent on
re-run. `readme-maintainer` extracted to
`github.com/verkyyi/readme-maintainer-skill` (v0.1.0). Consumer journey
is now `scope → install → onboard`; all three modules share
`harness/lib/catalog.py`.

Phase 1 decomposition status:

  1.1  — ledger schema + status.sh v1                           (DONE, 68c2893)
  1.2a — harness plumbing (stub-driven, no claude -p, no gh)    (DONE, 8e042f5)
  1.2b — real-skill integration                                 (DONE, f510600)
  1.3  — scoping flow (tokenman scope → initial-scope.md)       (DONE, 5267e12)
  1.4  — guided onboarding mode                                 (DONE, 5c85456)
  1.5  — skill install flow (catalog → .claude/skills/)         (DONE, phase-1-5 branch — merge pending)
  1.6  — TBD                                                    (NEXT)

Working tree is clean. `.tokenman/PAUSE` is still committed; PAUSE stays
on through Phase 2 per spec §12.

## What Phase 1.5 delivered

A real install flow, a catalog extraction, and the end of the in-tree
skill bootstrap. 13 commits on branch `phase-1-5`:

- `harness/lib/installer.py` — pure install logic: `install_skill(...)`
  resolves local or remote `source:` entries from the catalog, clones
  remote sources at a pinned tag/sha via `git_ops`, copies (or `path:`
  subdir-extracts) into `<repo>/.claude/skills/<name>/`, verifies
  `SKILL.md` parses, writes `.tokenman-skill-lock` (source, version,
  resolved sha, installed_at). Returns `InstallResult` (frozen
  dataclass: status ∈ {installed, unchanged, updated}, path, resolved
  sha). Idempotent: re-running with no drift returns `unchanged`;
  drift is detected via sha compare and refused without `--force`.
- `harness/lib/catalog.py` — shared catalog helpers extracted from
  the three CLI entrypoints: `load_catalog(path)`,
  `resolve_skill_dir(repo, name, catalog)`. Both `harness.scope`,
  `harness.onboard`, and `harness.run` now consume this module
  (eliminates the `_resolve_skill_dir` duplication flagged in the 1.4
  handoff).
- `harness/install/__main__.py` — `python -m harness.install
  [--repo .] [--catalog-path ...] [--skill NAME ...] [--force]
  [--dry-run]`. Exits 0 on success (prints one line per skill:
  `installed`, `unchanged`, `updated`), 2 on catalog/config errors,
  3 on remote-fetch failures, 4 on SKILL.md validation failures (with
  the resolved sha in the message for debuggability).
- `recommended-skills.yaml` — flipped the `readme-maintainer` entry
  from `./skills/readme-maintainer` (local) to
  `https://github.com/verkyyi/readme-maintainer-skill` at `v0.1.0`.
  In-tree `skills/readme-maintainer/` pruned; `skills/README.md`
  bootstrap note updated.
- `harness/scope/__main__.py` — scope's skill-md payload now reads
  from the consumer's `.claude/skills/<name>/SKILL.md` (populated by
  `harness.install`), so scope works for remote sources.
- `harness/run/__main__.py` — migrated onto `catalog.resolve_skill_dir`;
  no longer duplicates resolution logic.
- `tests/test_install_live.py` — opt-in (`TOKENMAN_LIVE=1`) live test
  that clones the real `readme-maintainer-skill` remote and verifies
  the lock file + idempotent re-run.
- README: Usage section now reflects the three-step consumer journey
  (scope → install → onboard) instead of the old two-step flow.

Test suite: 136 passed, 4 skipped (3 existing live-gated + 1 new
live-gated install test). With `TOKENMAN_LIVE=1` all pass.

## Forward-facing cleanups (still open)

Not blocking; candidates for a parallel cleanup pass before Phase 2.

- Refresh `tests/fixtures/claude-captures/readme-maintainer.json`
  with a real captured invocation (currently synthetic).
- Workflow template's `claude` install step still echoes TODO + has
  `exit 1`. Pick the install command (likely
  `npm i -g @anthropic-ai/claude-code`) and drop the `exit 1` once
  verified end-to-end.
- `GhPROpener` has not been exercised against real GitHub
  end-to-end. A manual `workflow_dispatch` run against a throwaway
  consumer repo is the validation step.

## Forward-facing notes from 1.5

- **Private-repo authentication.** `harness.install` shells out to
  `git clone` over public HTTPS. SSH URLs and `gh`-token auth for
  private catalog entries are not yet handled. Design: probably
  detect `git@…` / `ssh://…` and trust the user's ssh-agent, plus
  surface a `--token-env` for HTTPS with bearer tokens. Ties into
  whatever Phase 2 does for CI-side secrets.
- **Upgrade flow.** Today `--force` reinstalls at the pinned version.
  There's no `--upgrade` that fetches a newer tag than the lock. When
  the catalog bumps a skill's `version:`, consumers currently re-run
  install and it silently no-ops (the catalog version matches the
  lock version for an older checkout). Worth fixing before the
  catalog has multiple skills.
- **Parallel clones.** Install is sequential. Fine for 3–5 skills;
  revisit if the catalog grows past ~10. `concurrent.futures` would
  suffice — no async rewrite needed.
- **Pre-fetched SKILL.md in the catalog.** Today scope reads
  `skill_md` from the consumer's `.claude/skills/` (post-install).
  The prompt tolerates `null`, so a cold `scope`-then-`install` flow
  is ergonomic but means scope can't factor SKILL.md into its
  recommendation ordering before install runs. Option: cache SKILL.md
  text in `recommended-skills.yaml` (or a sibling manifest) so scope
  can see it without requiring install first. Purely ergonomic.

## Carryover from 1.4

- Per-skill errors do not abort the onboarding session; they're
  surfaced in `## What was skipped` with a pointer to
  `runs/<run_id>/executor.stderr`.
- `_seed_git_repo` test helper is duplicated across several test
  files. Plan deferred conftest.py extraction; do it the next time
  fixture shape changes.
- `_resolve_skill_dir` raising `SystemExit` was replaced by the
  `catalog.resolve_skill_dir` extraction in 1.5; this carry is
  closed.

## Phase 1.6 — next phase to be scoped

No formal 1.6 decomposition exists yet. Read spec §7 (budget and
scheduling) and §8 (observability) to pick the next slice. Likely
candidates:

- **Budget enforcement v1.** Today `OnboardingBudget` is an in-process
  stub with fixed ceilings. Spec §7 wants per-run accounting driven
  by real token counts off the claude JSON stream, persisted so
  subsequent runs see cumulative spend.
- **Scheduling + cadence.** The workflow template already supports
  `workflow_dispatch` and a `mode` input; spec §7 outlines a
  cron-driven cadence with rate-of-change caps. This is the first
  piece that makes tokenman "unattended" in the real sense.
- **Observability surfaces.** Spec §8 mentions `status.sh v2`, a
  per-consumer summary page, and machine-readable run artifacts.
  Small, tractable slice if budget/scheduling feels too big.

Entry ritual: start a fresh conversation, read this file, read
`docs/spec.md` §7 and §8, then invoke `superpowers:brainstorming` to
scope 1.6 before touching code. Work in a worktree (branch `phase-1-6`
off main).

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
