Continuing work on the tokenman library repo at /home/dev/projects/tokenman.

Context: Phase 1.2a (harness plumbing — ledger append utility, runner,
skill_executor / pr_opener Protocols, stub-readme fixture) is complete
and merged to main at 8e042f5 (fast-forward, six commits from the
phase-1-2a branch plus two earlier docs commits for the 1.2a
design + plan).

Phase 1 decomposition (set during 1.1 brainstorming, then further split
during 1.2a brainstorming):

  1.1  — ledger schema + status.sh v1                          (DONE, 68c2893)
  1.2a — harness plumbing (stub-driven, no claude -p, no gh)   (DONE, 8e042f5)
  1.2b — real-skill integration                                (NEXT)
  1.3  — scoping flow (tokenman scope → initial-scope.md)
  1.4  — guided onboarding mode

Important: main is 8 commits ahead of origin/main (6 from 1.2a + 2 docs).
Not pushed. Ask the user before pushing — they haven't authorized it yet.

Start Phase 1.2b. Read these first for context:

  - docs/superpowers/specs/2026-04-18-phase-1-2a-harness-plumbing-design.md
    (especially "What's deliberately NOT in 1.2a" and "Open items" —
    those are 1.2b scope)
  - harness/lib/{runner,skill_executor,pr_opener,ledger}.py
    (the contracts 1.2b slots into)
  - tests/fixtures/skills/stub-readme/ (the stub that ClaudeSkillExecutor
    replaces)
  - harness/workflows/tokenman.yml.template (still a Phase 0 echo stub;
    1.2b makes it functional)
  - recommended-skills.yaml (still empty; 1.2b adds the first entry)

Phase 1.2b scope, in rough priority order:

  1. ClaudeSkillExecutor — real claude -p invocation satisfying the
     SkillExecutor Protocol from 1.2a. Subprocess-based, same interface,
     swap-in at the runner's call site.
  2. GhPROpener — real `gh pr create` satisfying the PROpener Protocol.
  3. A real first skill (readme-maintainer is the spec's named example)
     pinned in recommended-skills.yaml with version, tier, blast_radius,
     token budget.
  4. Functional tokenman.yml.template — replaces the Phase 0 echo stub
     with a workflow that installs deps, runs the runner against the
     consumer's repo, and uploads artifacts.
  5. Runner CLI — `python -m harness.run --skill <name> --repo <path>`
     or similar, invokable from the workflow.

Forward-facing concerns the 1.2a final reviewer flagged (not blockers,
but worth designing for in the 1.2b kickoff):

  - `prompt_version` is currently hardcoded to "stub-v1" in runner.py.
    Better pattern: add `prompt_version: str` to ExecutionResult so
    StubSkillExecutor and ClaudeSkillExecutor each own their own value.
    Runner stops caring. ~4-line runner change.
  - Artifact filenames `stub.stdout` / `stub.stderr` encode "stub" into
    the generic runner. Rename to `executor.stdout` / `executor.stderr`
    (or `skill.stdout` / `skill.stderr`) when ClaudeSkillExecutor lands.
  - Decide where `timeout_s` belongs when ClaudeSkillExecutor arrives.
    Recommendation: constructor, not Protocol. Keeps the runner
    generic. claude -p can run minutes; current subprocess.run has no
    timeout.
  - LedgerEntry TypedDict was mentioned in the 1.2a design but never
    landed — run_skill returns a plain dict. Add the TypedDict if
    editor ergonomics in harness/lib/ become noticeable as the surface
    grows.

Dogfood is still paused (.tokenman/PAUSE present, per spec §12 phased
plan). PAUSE stays committed through Phase 2. 1.2b still runs against
tests/fixtures/, not against the library itself.

Then invoke brainstorming to scope Phase 1.2b before touching code.
Work in a worktree (branch phase-1-2b off main).
