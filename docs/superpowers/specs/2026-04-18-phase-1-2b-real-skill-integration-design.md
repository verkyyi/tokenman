# Phase 1.2b Real-Skill Integration — Design

**Date:** 2026-04-18
**Status:** Approved via brainstorming, pending user review of this doc
**Parent spec:** `docs/spec.md` v0.2, §12 "Phase 1 — Wedge + guided onboarding"
**Sub-phase:** 1.2b of Phase 1's four-part decomposition
**Predecessor:** `docs/superpowers/specs/2026-04-18-phase-1-2a-harness-plumbing-design.md`

Phase 1 decomposition recap:
- 1.1 — ledger schema + `status.sh` v1 (DONE, 68c2893)
- 1.2a — harness plumbing (DONE, 8e042f5)
- **1.2 — linear harness workflow + first skill integration** (in progress)
  - **1.2b — real-skill integration** (this doc): `ClaudeSkillExecutor`,
    `GhPROpener`, first cataloged skill, functional
    `tokenman.yml.template`, runner CLI — split internally into a
    mechanical refactor branch (1.2b-i) and an integration branch
    (1.2b-ii).
- 1.3 — scoping flow (`tokenman scope`)
- 1.4 — guided onboarding mode

## Purpose

Swap 1.2a's stub boundary classes for real ones, land the first cataloged
skill, and produce a consumer-deployable workflow template. 1.2a froze
the orchestrator contract (`run_skill`, `SkillExecutor`, `PROpener`,
`ledger.append`) so 1.2b is a focused integration change — two new
concrete classes, a first skill, a CLI, a workflow, and a small
mechanical refactor cleaning up carry-overs the 1.2a reviewer flagged.

No runtime activity on the library repo yet: PAUSE stays on, 1.2b
exercises against `tests/fixtures/` and one throwaway consumer repo for
the live smoke. Full library dogfood is the Phase 3 gate per spec §12.

## Scope decisions (from brainstorming, 2026-04-18)

1. **First skill lives in-tree as a bootstrap.** `skills/readme-maintainer/`
   under a new source-zone `skills/` directory. Catalog entry uses
   `source: ./skills/readme-maintainer`. This is a deliberate, temporary
   violation of spec §5.1's "tokenman ships zero skills" — documented in
   `skills/README.md`, tracked as a follow-up, must be split to a
   sibling repo before Phase 3. Picked over a sibling repo today to
   keep iteration cost low during 1.2b's first-contact-with-real-claude
   phase; picked over "use a pre-existing community skill" because no
   vetted candidate exists yet.

2. **Diff production: copy + diff, not prompt-contract.**
   `ClaudeSkillExecutor` copies `repo_dir` into a scratch working copy,
   runs `claude -p` against the copy with its native Edit/Write tools,
   then runs `diff -ruN --exclude=.claude` between the original and the
   working copy. Skills edit files naturally; the diff is the executor's
   side effect. Original `repo_dir` stays read-only from the executor's
   point of view.

3. **Invocation shape: prompt points at the skill.** `claude -p` runs
   with `--append-system-prompt <harness-framing>` and a user prompt of
   `Invoke the <skill_name> skill. Edit files in place. When complete,
   stop.` Claude loads the skill via its Skill tool. Rejected
   alternatives: treating `SKILL.md` as a raw prompt template (defeats
   the skill ecosystem) and pure system-prompt injection (less explicit
   than a named invocation).

4. **Skill visibility: executor overlays into scratch.** The executor
   copies `skill_dir` into `scratch_dir/working/.claude/skills/<skill_name>/`
   before invoking claude, so Claude Code's Skill tool can find it.
   `.claude` is excluded from the diff so the overlay isn't proposed.
   When `/tokenman init` lands in 1.3, that fallback becomes redundant
   (skills will live permanently in `.claude/skills/`), but the
   executor's contract stays unchanged.

5. **Git work lives in the runner, not the PR opener.** After the
   executor produces `proposed.diff`, the runner calls a new
   `git_ops.apply_diff_and_push(...)`: create branch, apply, commit,
   push. Then `pr_opener.open(*, title, body, branch)` becomes a thin
   `gh pr create`. The `diff` argument is dropped from the `PROpener`
   Protocol.

6. **Testing: mocks for CI, recorded fixture for parsing, opt-in live
   smoke.** Normal CI uses `subprocess.run` mocks for both executor and
   PR opener. A recorded `claude -p --output-format json` capture at
   `tests/fixtures/claude-captures/readme-maintainer.json` drives a
   replay test that validates the parse path against real JSON shape.
   One `@pytest.mark.live` test runs the real executor against a
   fixture repo when `TOKENMAN_LIVE=1` is set.

7. **Workflow template: consumer-deployable.** Installs harness via
   `pip install git+https://github.com/verky/tokenman.git@main`;
   `workflow_dispatch` only (no schedule); no PAUSE / cooldown /
   budget / lock checks yet (Phase 2). Thin: most logic lives in
   `python -m harness.run`.

8. **CLI: `python -m harness.run`.** Module form, not a console script.
   Flags: `--skill`, `--repo`, `--ledger-path`, `--runs-dir`,
   `--claude-bin`, `--dry-run`. `--dry-run` swaps `FakePROpener` in —
   not a dry-run of claude itself; an escape hatch for local iteration
   against real claude.

9. **Two-branch phase split.** 1.2b-i is a pure mechanical refactor
   (carry-overs from the 1.2a review: `prompt_version` and `tokens` on
   `ExecutionResult`, artifact renames, `timeout_s` in constructor,
   drop `diff` from `PROpener`, add `LedgerEntry` TypedDict). Tests stay
   green. 1.2b-ii is purely additive (new classes, new skill, new CLI,
   new workflow). Reviewable in two clean surfaces.

## Architecture

1.2b does not change the module count in `harness/lib/`. It swaps the
concrete implementations behind the 1.2a Protocols, adds a CLI above
`run_skill`, and adds git work inside `run_skill`.

```
  .github/workflows/tokenman.yml    (consumer-deployable, workflow_dispatch)
            │  runs
            ▼
  python -m harness.run             (thin CLI; resolves skill via catalog)
            │  calls
            ▼
  harness.lib.runner.run_skill      (unchanged contract;
            │                        gains git branch/apply/push)
            │
  ┌─────────┼───────────────┬─────────────────────┐
  │         │               │                     │
  ▼         ▼               ▼                     ▼
ledger.py git_ops.py   skill_executor.py    pr_opener.py
append/   apply_diff_  SkillExecutor        PROpener Protocol
validate  and_push     Protocol             FakePROpener    (1.2a)
          (new)        StubSkillExecutor    GhPROpener      (1.2b-ii)
                       (1.2a)
                       ClaudeSkillExecutor  (1.2b-ii)
```

## 1.2b-i — mechanical refactor

Pure refactor branch. All existing tests stay green after each commit.

### Changes

1. **`ExecutionResult.prompt_version: str` added.** Runner reads
   `result.prompt_version` instead of hardcoding `"stub-v1"`.
   `StubSkillExecutor` returns `"stub-v1"`.
2. **`ExecutionResult.tokens: int = 0` added.** Runner reads
   `result.tokens` into `generator.tokens`. Stub returns `0`.
3. **Artifact renames.** `stub.stdout` → `executor.stdout`;
   `stub.stderr` → `executor.stderr`. Runner + tests updated together.
4. **`timeout_s` in executor constructor.**
   `StubSkillExecutor(timeout_s: int = 30)`. Wraps
   `subprocess.run(timeout=timeout_s)`. On timeout → synthesize
   `exit_code=-1` and a stderr note; runner surfaces as `status="error"`.
5. **Drop `diff` from `PROpener.open`.** New Protocol:
   `open(*, title, body, branch) -> int`. `FakePROpener` signature
   updated. Tests that previously inspected `diff` in the recorded
   call now read `runs/<id>/proposed.diff` from disk.
6. **`LedgerEntry` TypedDict** added to `harness/lib/ledger.py`; runner
   and tests annotate with it.

### Tests (1.2b-i)

- Existing runner tests: rename `stub.*` → `executor.*` assertions;
  add `prompt_version == "stub-v1"` and `tokens == 0` assertions on
  `generator`.
- New: `test_stub_timeout_surfaces_error` — `StubSkillExecutor(timeout_s=0.1)`
  against a 1s-sleep stub mode → `status="error"`, no ledger invariant
  violation.
- Existing `FakePROpener` tests: signature change (drop `diff` arg).

### Commits (branch `phase-1-2b-i`)

1. `refactor(harness): thread prompt_version and tokens through ExecutionResult`
2. `refactor(harness): rename stub.{stdout,stderr} to executor.{stdout,stderr}`
3. `refactor(harness): add timeout_s to executor constructor`
4. `refactor(harness): drop diff from PROpener Protocol; add LedgerEntry TypedDict`

Merge to `main` before starting 1.2b-ii.

## 1.2b-ii — integration

Purely additive branch. Lands new classes, the first cataloged skill,
the CLI, and the functional workflow template.

### 1.2b-ii.1 `harness/lib/git_ops.py` (~40 lines, new)

Factored out of `run_skill` for testability.

```python
@dataclass
class GitIdentity:
    name: str
    email: str

def apply_diff_and_push(
    repo_dir: Path,
    diff_text: str,
    branch: str,
    base: str,
    message: str,
    identity: GitIdentity,
    remote: str = "origin",
) -> None:
    """Create branch off base, git apply diff_text, commit, push.

    Raises GitOpsError with captured stderr on any step's failure.
    """
```

Steps: `git -C <repo> switch -c <branch> <base>` → `git apply` (feeds
`diff_text` via stdin) → `git add -A && commit` (identity via
`-c user.name=… -c user.email=…`) → `git push -u <remote> <branch>`.
Identity defaults to `GitIdentity("tokenman-bot", "tokenman@local")`;
overridable via `GIT_AUTHOR_*` / `GIT_COMMITTER_*` env if present.

### 1.2b-ii.2 `harness/lib/skill_executor.py` — add `ClaudeSkillExecutor`

```python
class ClaudeSkillExecutor:
    def __init__(
        self,
        claude_bin: str = "claude",
        timeout_s: int = 600,
        prompt_version: str = "harness-v1",
        extra_env: Optional[dict[str, str]] = None,
        framing_path: Optional[Path] = None,  # defaults to harness/prompts/unattended_framing.v1.md
    ) -> None: ...

    def execute(
        self,
        skill_dir: Path,
        repo_dir: Path,
        scratch_dir: Path,
    ) -> ExecutionResult: ...
```

`execute` steps:
1. `working = scratch_dir / "working"`;
   `shutil.copytree(repo_dir, working, ignore=shutil.ignore_patterns(".git", ".tokenman"))`.
   `.git` is excluded so claude doesn't reason about repo history inside
   the scratch copy; `.tokenman` is excluded so prior ledger/run state
   never leaks into a proposal.
2. `shutil.copytree(skill_dir, working / ".claude" / "skills" / skill_dir.name, dirs_exist_ok=True)`.
3. Build argv: `[claude_bin, "-p", "--output-format", "json",
   "--append-system-prompt", framing_text, user_prompt]` where
   `user_prompt = f"Invoke the {skill_dir.name} skill. Edit files in place. When complete, stop."`.
4. `subprocess.run(argv, cwd=working, env=os.environ | extra_env,
   capture_output=True, text=True, timeout=timeout_s, check=False)`.
5. Parse `proc.stdout` as JSON. Extract:
   - `tokens` = sum of `usage.input_tokens + usage.output_tokens +
     usage.cache_creation_input_tokens + usage.cache_read_input_tokens`
     (defensive — cache fields may be absent; default 0).
   - `summary` = final assistant text message; fallback to first
     non-empty stdout line if JSON parse fails.
6. Compute diff: `subprocess.run(["diff", "-ruN", "--exclude=.claude",
   "--exclude=.git", "--exclude=.tokenman", str(repo_dir), str(working)],
   capture_output=True, text=True)`. Write non-empty diff stdout to
   `scratch_dir / "proposed.diff"`. The three excludes mirror the copy:
   none of those paths are part of a legitimate proposal.
7. Write summary as `scratch_dir / "proposed.md"`.
8. Return `ExecutionResult(exit_code=proc.returncode, stdout=proc.stdout,
   stderr=proc.stderr, proposed_diff_path=<scratch/proposed.diff if
   non-empty else None>, proposed_md_path=<scratch/proposed.md>,
   summary=<summary>, prompt_version=self.prompt_version, tokens=<tokens>)`.

On `subprocess.TimeoutExpired`: synthesize an error ExecutionResult
with `exit_code=-1`, `stderr += "[executor] claude -p timed out"`.

### 1.2b-ii.3 `harness/prompts/unattended_framing.v1.md` (new)

Small, versioned. Bumping → new file (`v2.md`, ...); executor's
`prompt_version` tracks which one was loaded. Content covers:
- This is an unattended run; no questions, no interactive clarification
- Stay within the skill's scoped paths
- If the skill is inapplicable, stop with no edits
- Do not touch `.tokenman/`, `.github/`, `.claude/` (read-only if needed)

### 1.2b-ii.4 `harness/lib/pr_opener.py` — add `GhPROpener`

```python
class GhPROpener:
    def __init__(
        self,
        repo_dir: Path,
        base_branch: str = "main",
        gh_bin: str = "gh",
    ) -> None: ...

    def open(self, *, title: str, body: str, branch: str) -> int: ...
```

`open`: `subprocess.run([gh_bin, "pr", "create", "--title", title,
"--body", body, "--head", branch, "--base", self._base, "--json",
"number", "-q", ".number"], cwd=repo_dir, capture_output=True,
text=True, check=True)`. Returns `int(stdout.strip())`. On non-zero
exit → raises `PROpenerError` with stderr captured.

Assumes the branch already exists and is pushed (the runner guarantees
this via `git_ops.apply_diff_and_push`).

### 1.2b-ii.5 `runner.py` — git work wired in

In the `proposed.diff produced` branch of `run_skill`, before calling
`pr_opener.open`:

```python
branch = f"tokenman/{skill}/{run_id}"
try:
    git_ops.apply_diff_and_push(
        repo_dir=repo_dir,
        diff_text=diff_text,
        branch=branch,
        base=base_branch,   # injected; default "main"
        message=f"[tokenman] {skill}: {result.summary}",
        identity=git_identity,
    )
    pr = pr_opener.open(title=..., body=..., branch=branch)
    status = "pr_opened"
except (GitOpsError, PROpenerError) as exc:
    status = "error"; generator = None; pr = None
    append_to_executor_stderr(...)
```

`base_branch` and `git_identity` become new kwargs on `run_skill`
(optional; defaults).

### 1.2b-ii.6 `harness/run/__main__.py` — CLI

```
python -m harness.run \
  --skill readme-maintainer \
  [--repo .] \
  [--ledger-path <repo>/.tokenman/ledger.jsonl] \
  [--runs-dir   <repo>/.tokenman/runs] \
  [--claude-bin claude] \
  [--base-branch main] \
  [--dry-run]
```

Behavior:
- Resolve `skill_dir` from `recommended-skills.yaml`'s
  `<skill>.source`. If `source` starts with `./`, resolve relative to
  the library repo root (found via package metadata).
- Construct `ClaudeSkillExecutor(claude_bin=...)` unless `--dry-run`,
  in which case use `StubSkillExecutor` with a canned `propose_diff`
  stub for local-loop debugging.
- `--dry-run` also swaps `GhPROpener` for `FakePROpener` with a sink
  at `<runs-dir>/../dry-run-prs/`.
- Invoke `run_skill(...)`.
- Print the ledger entry (compact JSON) to stdout on success.
- Exit code: 0 if the ledger entry appended (any status); 1 if
  `run_skill` raised.

### 1.2b-ii.7 `skills/readme-maintainer/SKILL.md` (new)

Content:
- Name: `readme-maintainer`
- Description: "Keeps README aligned with actual repo contents."
- Version: `0.1.0`
- Scope: `README.md` only
- Shape: in-place edit, additive preferred
- Size limit: ~100 diff lines
- Deterministic-gate hints: touch only `README.md`; no new files
- Evaluator criteria: stays scoped, additive, consistent with repo style
- Typical token budget: 15 000
- Source: `./skills/readme-maintainer` (this repo, temporary — see
  `skills/README.md`)

### 1.2b-ii.8 `skills/README.md` (new)

Explains `skills/` as a 1.2b bootstrap posture, violating spec §5.1's
"ships zero skills" temporarily. Must be split to a sibling repo before
Phase 3 dogfood opens. Rationale lives here so future contributors
don't see it as precedent.

### 1.2b-ii.9 `recommended-skills.yaml` — first entry

```yaml
readme-maintainer:
  source: ./skills/readme-maintainer    # TEMPORARY: in-tree during 1.2b
  version: 0.1.0
  tier: starter
  blast_radius: low
  typical_tokens_per_run: 15000
  description: Keeps README aligned with actual repo contents.
  default_cadence: on-change
  evaluator_strictness: medium
```

A `# TODO(1.2b-split): extract to standalone repo` comment marks the
follow-up.

### 1.2b-ii.10 `harness/workflows/tokenman.yml.template`

Replaces the Phase 0 echo stub.

```yaml
# TEMPLATE — installed into consumer repos as
# .github/workflows/tokenman.yml.
#
# Phase 1.2b: workflow_dispatch only. No PAUSE/cooldown/budget/lock
# checks yet (Phase 2). No schedule yet.
#
# Requires: secrets.ANTHROPIC_API_KEY configured on the consumer repo.

name: tokenman
on:
  workflow_dispatch:
    inputs:
      skill:
        description: Skill to run
        required: true
        default: readme-maintainer
permissions:
  contents: write
  pull-requests: write
jobs:
  tokenman-run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install git+https://github.com/verky/tokenman.git@main
      - name: Install claude CLI
        run: |
          # TODO(1.2b-impl): resolve actual install command at
          # implementation time (npm global, pip, or other).
          echo "install claude here"
      - name: Configure git identity for bot commits
        run: |
          git config --global user.email "tokenman-bot@users.noreply.github.com"
          git config --global user.name  "tokenman-bot"
      - name: Run tokenman
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python -m harness.run --skill ${{ inputs.skill }} --repo .
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: tokenman-run-${{ github.run_id }}
          path: .tokenman/runs/
```

### 1.2b-ii.11 `.tokenman/CLAUDE.md` — forbid `skills/`

Append `skills/` to the existing forbidden-path list alongside
`harness/`, `scoping/`, `onboarding/`, `recommended-skills.yaml`,
`pricing.yaml`.

### 1.2b-ii.12 `CONTRIBUTING.md` — note bootstrap posture

Short paragraph near the source/runtime split section: `skills/` is a
temporary 1.2b bootstrap; future skills live in their own repos and
are pinned in `recommended-skills.yaml` by URL.

### Tests (1.2b-ii)

- `tests/test_claude_skill_executor_mock.py` — patch `subprocess.run`;
  call `execute` against a stub `skill_dir` + tmp `repo_dir` + scratch;
  assert argv/env/cwd shape; feed a synthetic JSON stdout; assert
  `ExecutionResult.tokens`, `summary`, `prompt_version` correct; assert
  diff computation path invoked with correct args.
- `tests/test_claude_skill_executor_replay.py` — load
  `tests/fixtures/claude-captures/readme-maintainer.json` (recorded
  once by hand during implementation); patch subprocess to return it;
  assert full `ExecutionResult` populated correctly from real-shape
  JSON.
- `tests/test_claude_skill_executor_live.py` — `@pytest.mark.live`,
  skipped unless `TOKENMAN_LIVE=1`. Runs real `ClaudeSkillExecutor`
  against `skills/readme-maintainer/` on a tmp copy of
  `tests/fixtures/tiny-python-repo/`. Asserts either a `proposed.diff`
  or a `no_change` outcome; no crash.
- `tests/test_gh_pr_opener.py` — patch `subprocess.run`; assert
  `gh pr create` argv shape; parse canned `123` stdout → `int`; assert
  `PROpenerError` on non-zero exit.
- `tests/test_git_ops.py` — seed a tmp bare repo as remote; seed a tmp
  worktree pointing at it; run `apply_diff_and_push` with a synthetic
  diff; assert branch exists locally and on the bare remote; assert
  commit message + author identity correct.
- `tests/test_runner_git_apply.py` — full `run_skill` with
  `StubSkillExecutor(STUB_MODE=propose_diff)` + `FakePROpener`. The
  test helper copies `tests/fixtures/tiny-python-repo/` to tmp, runs
  `git init && git add -A && git commit -m init` inside the copy, and
  configures a second tmp path as a `--bare` remote at `origin`.
  Asserts: branch created, commit present, branch pushed to bare
  remote, `FakePROpener.open` called with expected `branch=` kwarg.
  Neither fixture is modified in place.
- `tests/test_cli.py` — subprocess-invoke
  `python -m harness.run --skill readme-maintainer --dry-run --repo <tmp>`;
  `--dry-run` substitutes a canned-`propose_diff` stub executor and a
  `FakePROpener`, so this test never calls real `claude` or `gh`; assert
  exit 0; assert `.tokenman/ledger.jsonl` has one line; assert stdout
  ends with the ledger entry JSON.

### Manual smoke (PR-described, not automated)

One live `workflow_dispatch` run against a throwaway personal repo
(e.g. `verky/tokenman-smoke-test`). Expected: a PR is opened against
that repo's main; run artifacts uploaded and downloadable. PR link
and artifact URL captured in the 1.2b-ii PR description.

### Commits (branch `phase-1-2b-ii`)

1. `feat(harness): add git_ops module for branch/apply/push`
2. `feat(harness): wire git_ops into run_skill before PR open`
3. `feat(harness): add GhPROpener`
4. `feat(harness): add ClaudeSkillExecutor and unattended framing`
5. `test(harness): add recorded claude-output fixture and replay test`
6. `feat(harness): add python -m harness.run CLI`
7. `feat(skills): add in-tree readme-maintainer skill and catalog entry`
8. `feat(workflow): make tokenman.yml.template consumer-deployable`
9. `docs: note skills/ forbidden path and bootstrap posture`

Each commit trailer:

```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

## Files

### Additions (1.2b-ii)

- `harness/lib/git_ops.py`
- `harness/prompts/__init__.py`
- `harness/prompts/unattended_framing.v1.md`
- `harness/run/__init__.py`
- `harness/run/__main__.py`
- `skills/README.md`
- `skills/readme-maintainer/SKILL.md`
- `tests/fixtures/claude-captures/readme-maintainer.json`
- `tests/test_claude_skill_executor_mock.py`
- `tests/test_claude_skill_executor_replay.py`
- `tests/test_claude_skill_executor_live.py`
- `tests/test_gh_pr_opener.py`
- `tests/test_git_ops.py`
- `tests/test_runner_git_apply.py`
- `tests/test_cli.py`

### Modifications

- `harness/lib/skill_executor.py` — adds `ClaudeSkillExecutor` (1.2b-ii);
  `ExecutionResult` gains `prompt_version` + `tokens`; constructor gains
  `timeout_s` (1.2b-i).
- `harness/lib/pr_opener.py` — adds `GhPROpener` (1.2b-ii); Protocol
  loses `diff` (1.2b-i).
- `harness/lib/ledger.py` — adds `LedgerEntry` TypedDict (1.2b-i).
- `harness/lib/runner.py` — reads `result.prompt_version`/`result.tokens`;
  artifact renames; git work before PR open (1.2b-ii); new
  `base_branch` + `git_identity` kwargs.
- `harness/workflows/tokenman.yml.template` — functional (1.2b-ii).
- `recommended-skills.yaml` — first entry (1.2b-ii).
- `.tokenman/CLAUDE.md` — `skills/` added to forbidden paths (1.2b-ii).
- `CONTRIBUTING.md` — bootstrap-posture note (1.2b-ii).
- Tests under `tests/` — updated expectations (1.2b-i).

### Notably NOT modified

- `harness/lib/ledger.schema.json` — unchanged from 1.1.
- `harness/lib/ledger.py` `append`/`validate`/`last_run_id` — unchanged
  from 1.2a.
- `tests/fixtures/tiny-*-repo/` — unchanged, per project CLAUDE.md.
- `tests/fixtures/skills/stub-readme/` — unchanged, per project CLAUDE.md.
- `.tokenman/PAUSE` — still present. No automated runs against the
  library in 1.2b.

## Exit criteria

1. `pytest -q` green on `main` after both branches merged (live tests
   skipped when `TOKENMAN_LIVE` is unset).
2. `pytest -m live` passes locally against a real `claude` install on
   at least `skills/readme-maintainer/` + `tests/fixtures/tiny-python-repo/`.
3. One `workflow_dispatch` run executed against a throwaway consumer
   repo produced a real PR; PR URL and artifact URL captured in the
   1.2b-ii PR description.
4. `python -c "from harness.lib import ledger, runner, skill_executor,
   pr_opener, git_ops; from harness.run import __main__"` imports
   clean after `pip install -e '.[dev]'`.
5. `.tokenman/PAUSE` still present; no auto-runs against the library.
6. `.tokenman/CLAUDE.md` lists `skills/` alongside other forbidden
   source-zone paths.
7. `recommended-skills.yaml` has exactly one entry (`readme-maintainer`).
8. Working tree clean after all 1.2b-i + 1.2b-ii commits merged to main.

## What's deliberately NOT in 1.2b

- `/tokenman init` (Phase 1.3) — the scoping + install flow. 1.2b's
  `skills/` overlay inside the executor is the temporary substitute.
- Splitting `skills/readme-maintainer/` out to a sibling repo —
  follow-up after 1.2b, before Phase 3 dogfood opens.
- PAUSE check, cooldown, budget cap, open-PR lock — Phase 2 per spec
  §9 and §12.
- Evaluator stage, deterministic gate — Phase 3.
- Retention / GC of `.tokenman/runs/r-NNNN/` — Phase 2 per spec §8.2.
- Scheduled runs (cron / on-event triggers) — Phase 2. 1.2b workflow
  is `workflow_dispatch`-only.
- Multi-skill DAG invocation — Phase 4.
- Real library-repo dogfood — Phase 3 gate per spec §12.

## Open items

1. **Exact `claude` CLI install command** in the workflow — stubbed as
   a TODO in the template. Resolved during 1.2b-ii implementation
   (verified by the live smoke step).
2. **Exact claude -p JSON schema** — fields like `usage.*` and the
   final-message extraction path are assumed from documented behavior.
   Confirmed by the first real invocation during 1.2b-ii.4; any
   deviations captured in the recorded fixture and reflected in the
   parser.
3. **`GhPROpener` authentication in CI** — relies on
   `secrets.GITHUB_TOKEN` via `GH_TOKEN` env. Confirmed via the
   manual smoke. No design change expected; flagging so implementation
   doesn't forget.
4. **Token accounting for prompt caching** — `usage` includes cache
   hit/miss fields; we sum them defensively. If real output shows
   cache accounting materially skews `total_tokens`, revisit during
   1.2b-ii.5 (replay fixture lands there).

## Verification (after both branches merged)

```bash
# 1. Package installs
pip install -e '.[dev]' -q && echo OK

# 2. Tests pass (live skipped)
pytest -q

# 3. Live test passes locally (requires claude login + TOKENMAN_LIVE=1)
TOKENMAN_LIVE=1 pytest -q -m live

# 4. Imports work
python3 -c "from harness.lib import ledger, runner, skill_executor, pr_opener, git_ops; from harness.run import __main__; print('OK')"

# 5. Dry-run CLI against the stub
python -m harness.run --skill stub-readme --dry-run --repo tests/fixtures/tiny-python-repo

# 6. Manual workflow_dispatch smoke against a throwaway repo —
#    noted in the 1.2b-ii PR description with PR link.

# 7. Working tree clean
git status
```
