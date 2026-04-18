# Phase 1.4 — Guided onboarding mode design

**Phase:** 1.4
**Date:** 2026-04-18
**Status:** draft — pre-implementation
**Implements:** spec.md §6.4 (guided onboarding run)
**Supersedes:** none

---

## 1. Goal

Deliver `python -m harness.onboard` and a `mode=onboarding` workflow input
that runs every enabled skill back-to-back in a single session, opens one
labeled PR per skill, and writes `.tokenman/onboarding-summary.md` —
the artifact that demonstrates value to a fresh consumer within minutes
of install.

This is the **minimum viable** implementation of spec §6.4. Real budget
calibration, evaluator stage, and adaptive scheduling are explicitly
deferred to Phase 2/3.

## 2. Non-goals

- **Skill install flow** (fetching from remote `source:` URLs in the
  catalog). Catalog has only `readme-maintainer` with a local `./` source —
  onboarding reuses what's already on disk. Remote install lands when the
  catalog actually grows. Tracked as Phase 1.5 candidate.
- **Real budget enforcement.** Phase 2 wires `pricing.yaml` and
  subscription tiers. Onboarding gets two in-process token ceilings
  (per-run flag, session ceiling) so a runaway can't burn down the world,
  but no `pricing.yaml` read.
- **Evaluator stage.** Phase 3.
- **Adaptive scheduling, cooldowns, review-bandwidth gating, PAUSE
  enforcement.** Phase 2.
- **Library dogfood.** Onboarding is exercised against
  `tests/fixtures/tiny-python-repo/` only. PAUSE on the library stays
  through Phase 2 per spec §12. Phase 1.4 PAUSE status: ON.
- **Modifying `harness.run` semantics.** Single-skill execution is
  unchanged.
- **Writing `.tokenman/tokenman.yaml`.** The user authors this manually
  in Phase 1, seeded by Phase 1.3's `initial-scope.md`.

## 3. User journey

```
$ cd my-repo
$ python -m harness.onboard
[loading config from .tokenman/tokenman.yaml]
[2 skills enabled: readme-maintainer, dep-bump-safe]
[session ceiling: 180,000 tokens (3× 30,000 × 2)]

[1/2] readme-maintainer ... pr_opened (#42, 14,200 tok)
[2/2] dep-bump-safe     ... no_change (8,100 tok)

Wrote .tokenman/onboarding-summary.md
Total: 22,300 tokens (12% of session ceiling)
```

Or via the workflow:

```
gh workflow run tokenman.yml -f mode=onboarding
```

## 4. Architecture

### 4.1 Module layout

```
harness/
├── onboard/
│   ├── __init__.py
│   └── __main__.py             # CLI entry point
└── lib/
    ├── onboarder.py            # orchestrator: skills loop, budget tracking
    └── summary.py              # markdown renderer for onboarding-summary.md
```

Mirrors the established `harness/scope/` + `harness/lib/scope_drafter.py`
and `harness/run/` + `harness/lib/runner.py` patterns. Splitting
`onboarder.py` from `summary.py` (rather than inlining the renderer like
`harness.scope` does) reflects that the summary is meaningfully more
complex than scope's renderer — it groups by `status`, links PRs, and
surfaces "considered but skipped" entries — so unit-testing it against
canned `OnboardingResult` fixtures is cleaner with a separate module.

### 4.2 Data flow

```
  [CLI argv]
      │
      ▼
  load tokenman.yaml ──► enabled_skills (list[str])
      │
      ▼
  resolve each via recommended-skills.yaml ──► [(name, skill_dir)]
      │
      ▼
  onboarder.run_onboarding(
      skills=…, repo_dir=…, ledger_path=…, runs_dir=…,
      executor=ClaudeSkillExecutor | StubSkillExecutor,
      pr_opener=GhPROpener | FakePROpener,
      budget=OnboardingBudget(per_run_ceiling, session_ceiling),
  )
      │
      │  for each skill:
      │      runner.run_skill(...) ──► LedgerEntry
      │      accumulate tokens
      │      if session_ceiling exceeded → break + synthesize
      │          skipped_budget entries for the rest
      │
      ▼
  OnboardingResult (entries, totals, started_at, finished_at)
      │
      ▼
  summary.build(result, repo_name, session_ceiling) ──► str
      │
      ▼
  write .tokenman/onboarding-summary.md
```

## 5. Component details

### 5.1 `harness/lib/onboarder.py`

**Purpose:** orchestrate a single onboarding session. No I/O beyond what
`runner.run_skill` already does (ledger, artifacts).

**Entry point:**

```python
def run_onboarding(
    *,
    skills: list[tuple[str, Path]],   # [(skill_name, skill_dir)]
    repo_dir: Path,
    ledger_path: Path,
    runs_dir: Path,
    executor: SkillExecutor,
    pr_opener: PROpener,
    budget: OnboardingBudget,
    base_branch: str = "main",
    git_identity: GitIdentity | None = None,
    now: Callable[[], datetime] | None = None,
) -> OnboardingResult:
    ...
```

**`OnboardingBudget` dataclass:**

```python
@dataclass(frozen=True)
class OnboardingBudget:
    per_run_ceiling: int       # default 30_000; advisory in 1.4 (post-hoc flag)
    session_ceiling: int       # default 3 × per_run × len(skills)
```

**`OnboardingResult` dataclass:**

```python
@dataclass(frozen=True)
class OnboardingResult:
    entries: list[LedgerEntry]   # one per attempted skill, in order
    total_tokens: int
    session_ceiling: int
    started_at: datetime
    finished_at: datetime
    breached_ceiling: bool       # True if any skill was skipped_budget
```

**Behavior:**

- For each `(name, skill_dir)`:
  - **Pre-flight check (worst-case bound):** if `total_tokens +
    per_run_ceiling > session_ceiling`, do **not** invoke
    `runner.run_skill`. We use `per_run_ceiling` as a pessimistic upper
    bound because we don't know skill N's actual usage in advance;
    pre-flighting on the ceiling means we never *start* a skill that
    could push us over. Synthesize a `skipped_budget` ledger entry (via
    `_synth_skipped_entry` — see below) and append it via
    `ledger.append`. Continue the loop so every enabled skill shows up
    in the summary.
  - Otherwise, call `runner.run_skill(skill_dir=skill_dir, …)`. The
    runner persists the ledger entry itself. Add `entry["total_tokens"]`
    to the running total.
- `runner.run_skill` already returns `status="error"` on its own
  failures (executor non-zero, gitops/PR-opener failure). The onboarder
  treats `error` like any other terminal status: surface it in the
  summary, **continue with the next skill**.
- After the loop, build and return `OnboardingResult`.

**`_synth_skipped_entry(skill_name, run_id, now)`:**

Builds a ledger entry matching the `ledger.schema.json` shape with
`status="skipped_budget"`, `pr=null`, `generator=null`, `evaluator=null`,
`duration_s=0`, `total_tokens=0`. Run ID is allocated via
`ledger.last_run_id + 1`, same as `runner.run_skill` does — this means
the skipped entry **does** consume a run number, which is intentional
(every onboarding decision is auditable in the ledger).

**Failure modes:**
- Empty `skills` list → `OnboardingError("no skills to onboard")`.
  Caller (CLI) is responsible for checking config first; this is a
  belt-and-suspenders guard.

### 5.2 `harness/lib/summary.py`

**Entry point:**

```python
def build(
    *,
    result: OnboardingResult,
    repo_name: str,
    today: datetime | None = None,
) -> str:
    ...
```

Renders deterministic markdown. Sections in fixed order:

```markdown
# Tokenman — Onboarding summary for <repo_name>

_Generated by `python -m harness.onboard` on <date> in <duration>s._
_Total tokens: <N>  Session ceiling: <M>  Utilization: <P>%_

## What ran

- **<skill-1>** — <status> (<tokens> tok) → PR #<N> | no_change | skipped_budget | error
- **<skill-2>** — …

## Pull requests opened

- **#<N>**: <skill> — <output_summary>
- (or "None — every enabled skill produced no_change or was skipped.")

## What was considered but not proposed

For each entry with status=`no_change`:
- **<skill>** — <generator.output_summary>

(empty → "Every enabled skill proposed a change.")

## What was skipped

For each entry with status in {`skipped_budget`, `error`}:
- **<skill>** — <reason>
  - `skipped_budget`: "session token ceiling reached before this skill ran"
  - `error`: "executor or PR-opener failed; see runs/<run_id>/executor.stderr"

(empty → "Nothing was skipped.")

## Next steps

- Review the PRs above at your pace.
- Edit `.tokenman/CLAUDE.md` to teach the harness boundaries.
- Edit `.tokenman/tokenman.yaml` to add/remove skills or adjust schedule.
- Re-run onboarding any time: `gh workflow run tokenman.yml -f mode=onboarding`
```

### 5.3 `harness/onboard/__main__.py`

**CLI:**

```
python -m harness.onboard
    [--repo .]
    [--config-path .tokenman/tokenman.yaml]
    [--claude-bin claude]
    [--ledger-path .tokenman/ledger.jsonl]
    [--runs-dir .tokenman/runs]
    [--per-run-ceiling 30000]
    [--session-ceiling <auto>]
    [--skill SKILL]                 # repeatable; overrides config
    [--base-branch main]
    [--non-interactive]
    [--dry-run]
    [--output-path .tokenman/onboarding-summary.md]
```

**Flags:**

- `--repo`, `--config-path`, `--ledger-path`, `--runs-dir`,
  `--claude-bin`, `--base-branch`, `--output-path` — mirror
  `harness.run` and `harness.scope` shapes.
- `--per-run-ceiling`, `--session-ceiling` — onboarding budget knobs.
  If `--session-ceiling` is omitted, computed as
  `3 × per_run_ceiling × len(enabled_skills)` (the "3× elevated budget"
  from spec §6.4).
- `--skill SKILL` (repeatable) — skip config read, use the given skills
  directly. Lets onboarding be invoked against a fixture that has no
  `tokenman.yaml`, and lets a user dry-run onboarding before the config
  exists.
- `--non-interactive` — currently a no-op (onboarding has no prompts in
  1.4); kept for shape-parity with `harness.scope` and to leave room for
  future "confirm before opening N PRs" dialog.
- `--dry-run` — substitute `StubSkillExecutor` + `FakePROpener` and
  resolve every skill to `tests/fixtures/skills/stub-readme/`. No
  `claude` invocation, no real PRs.

**Skill resolution:**

1. If `--skill` is provided one or more times, use those names.
2. Else read `<config-path>`, take `skills:` (list of strings).
3. For each name, look up `recommended-skills.yaml`; resolve `source:`
   the same way `harness.run` does (only `./` local sources supported in
   1.4 — same Phase 1.5 deferral as install).

**Output behavior:**

- Always writes `<output-path>` (default `<repo>/.tokenman/onboarding-summary.md`).
- Exit codes:
  - `0` — onboarding ran (even if some skills errored or were skipped).
  - `2` — config error: missing config + no `--skill`, no skills enabled,
    skill name not in catalog.
  - `4` — summary file write failed (filesystem error). Ledger entries
    already persisted by `runner` are unaffected.

### 5.4 Workflow template — `harness/workflows/tokenman.yml.template`

Add a `mode` input and branch the run step on it:

```yaml
on:
  workflow_dispatch:
    inputs:
      mode:
        description: single (one skill) or onboarding (all enabled)
        required: true
        default: single
        type: choice
        options: [single, onboarding]
      skill:
        description: Skill to run (required when mode=single)
        required: false
        default: readme-maintainer
```

Run step:

```yaml
- name: Run tokenman
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    GH_TOKEN:          ${{ secrets.GITHUB_TOKEN }}
  run: |
    if [ "${{ inputs.mode }}" = "onboarding" ]; then
      python -m harness.onboard --repo .
    else
      python -m harness.run --skill "${{ inputs.skill }}" --repo .
    fi
```

The artifact-upload step changes from `name: tokenman-run-…` to
`name: tokenman-${{ inputs.mode }}-${{ github.run_id }}` so onboarding
artifacts are distinguishable in the Actions UI.

The `claude install` TODO from Phase 1.2b stays as-is — Phase 1.4 does
not block on resolving it (it remains `exit 1` until a separate cleanup
pass).

## 6. Budget — minimal Phase 1.4 stub

Two ceilings, both in tokens, both with safe defaults:

- `per_run_ceiling = 30_000` (default). Used by the onboarder's
  pre-flight check as a worst-case upper bound on skill N's token spend
  — we never *start* a skill that could push the session past
  `session_ceiling`. The executor itself does **not** enforce a mid-run
  limit in 1.4; a skill that exceeds `per_run_ceiling` mid-run is
  recorded honestly in the ledger and counted against the session
  total. Mid-run enforcement is Phase 2.
- `session_ceiling = 3 × per_run_ceiling × len(enabled_skills)`. The
  "3× normal weekly cap" from spec §6.4. Computed once at start, checked
  between skills (not mid-run).

Both overridable via CLI flags for fixture testing. Phase 2 replaces this
with real `pricing.yaml`-driven budgets and pre-run enforcement.

The handoff from Phase 1.3 explicitly called out "Phase 1.4 will need a
lightweight budget stub even though enforcement lands Phase 2" — this
section is that stub. It does not pretend to be more.

## 7. Error handling

| Failure | Response |
|---|---|
| `tokenman.yaml` missing AND no `--skill` flags | Exit 2 with message pointing to `harness.scope`. |
| `tokenman.yaml` present but `skills: []` AND no `--skill` flags | Exit 2 with same message. |
| Skill name not in `recommended-skills.yaml` | Exit 2 before any run starts; fail loud — config drift is a bug. |
| Skill `source:` is non-local (git URL) | Exit 2 with message: "remote skill sources land in Phase 1.5". |
| Single skill returns `status=error` from `runner.run_skill` | Logged in summary, **continue** with next skill. Onboarding shouldn't abort because one skill flaked. |
| Session ceiling breached | Remaining skills get synthetic `skipped_budget` ledger entries; exit 0. |
| Summary file write fails | Exit 4. Ledger entries already persisted by `runner` are unaffected; rerunning is safe (the next run gets a fresh `run_id` block). |

## 8. Testing strategy

Following the 1.2b/1.3 split: fast unit tests + opt-in live test.

### 8.1 Unit tests

- `test_onboarder.py` — happy path with `StubSkillExecutor` +
  `FakePROpener` + 2 fake skill dirs. Assert two ledger entries
  appended in order, `OnboardingResult.total_tokens` equals sum, both
  PRs opened.
- `test_onboarder_budget.py` — set `session_ceiling` low enough to
  break after one skill. Assert second skill gets `skipped_budget`
  ledger entry (synthesized, not from `runner.run_skill`), assert
  `breached_ceiling=True`.
- `test_onboarder_continues_on_error.py` — three skills, second one
  uses an executor that returns `status=error`. Assert third skill
  still ran, all three entries present.
- `test_onboarder_empty_skills.py` — empty `skills` list raises
  `OnboardingError`.
- `test_summary.py` — feed canned `OnboardingResult` to `summary.build`,
  assert section headers present, PR list correctly formatted, "What
  was skipped" populated only when applicable.

### 8.2 CLI integration tests

- `test_onboard_cli.py` — invoke `python -m harness.onboard --dry-run
  --non-interactive --repo <fixture> --skill stub-skill-a --skill
  stub-skill-b`. Assert exit 0, summary file contains both skill names
  and the "Pull requests opened" section.
- `test_onboard_cli_no_skills.py` — invoke against a fixture with no
  config and no `--skill` flags; assert exit 2 with the expected
  diagnostic.

### 8.3 Workflow-template smoke

- `test_workflow_template.py` — load
  `harness/workflows/tokenman.yml.template` as YAML, assert `mode`
  input exists with the documented choices, assert the run step
  contains both `harness.onboard` and `harness.run` invocations. Same
  shape as any existing template tests; if none exist, this file is
  the first.

### 8.4 Live test (opt-in)

- `test_onboard_live.py` — gated by `TOKENMAN_LIVE=1`. Real `claude -p`
  against `tests/fixtures/tiny-python-repo/`, single skill
  (`readme-maintainer`), with `--non-interactive`. Asserts summary file
  written, ledger contains one entry, run completes in <90s. Same
  envelope as `test_scope_live.py`.

### 8.5 Fixtures

- `tests/fixtures/skills/stub-readme/` — already exists, reused as
  skill #1.
- `tests/fixtures/skills/stub-readme-second/` — **new.** Minimal
  SKILL.md + `run.sh` that produces a different no-op (or a tiny
  additive diff against a fixture file the existing stub doesn't
  touch). Lets the onboarder loop over >1 skill.
- `tests/fixtures/scope-captures/` and other 1.3 fixtures — untouched.
- `tests/fixtures/onboarding-results/minimal.json` — **new.** Canned
  `OnboardingResult` for `test_summary.py`.

## 9. Open questions resolved by this design

- **Module placement:** `python -m harness.onboard` as a sibling to
  `harness.run` and `harness.scope`. Rejected: `harness.run --mode
  onboarding`, because it entangles single-skill execution (the
  Phase 1-2 path) with multi-skill orchestration in one module.
- **Where the budget lives:** in-process `OnboardingBudget` dataclass
  passed to the orchestrator, with sensible defaults. Rejected: reading
  `pricing.yaml` (premature — that's Phase 2), and reading
  `tokenman.yaml`'s `budget:` section (it's all zeros in Phase 0-2 per
  spec §10.5; reading it would just disable onboarding entirely).
- **What happens when one skill errors:** continue with the next.
  Rejected: abort the session, because that would conflate one skill's
  flake with onboarding-wide failure and hide what other skills would
  have done.
- **Where skipped-budget entries come from:** synthesized by the
  onboarder and appended to the ledger. Rejected: leaving them out of
  the ledger (loses auditability), and threading skip logic into
  `runner.run_skill` (couples the runner to onboarding-specific
  concerns).

## 10. Implementation sketch — file inventory

**New:**
- `harness/onboard/__init__.py`
- `harness/onboard/__main__.py`
- `harness/lib/onboarder.py`
- `harness/lib/summary.py`
- `tests/test_onboarder.py`
- `tests/test_onboarder_budget.py`
- `tests/test_onboarder_continues_on_error.py`
- `tests/test_onboarder_empty_skills.py`
- `tests/test_summary.py`
- `tests/test_onboard_cli.py`
- `tests/test_onboard_cli_no_skills.py`
- `tests/test_workflow_template.py`
- `tests/test_onboard_live.py`
- `tests/fixtures/skills/stub-readme-second/SKILL.md`
- `tests/fixtures/skills/stub-readme-second/run.sh`
- `tests/fixtures/onboarding-results/minimal.json`

**Modified:**
- `harness/workflows/tokenman.yml.template` — add `mode` input + branch.
- `README.md` — Usage section gains a one-liner for `python -m
  harness.onboard`.

**Untouched:**
- `harness/lib/runner.py`, `harness/run/__main__.py` — single-skill path
  unchanged.
- `harness/lib/scope_drafter.py`, `harness/scope/__main__.py` — scoping
  unchanged.
- `recommended-skills.yaml` — catalog stays as-is. Onboarding will, in
  practice, run one skill until the catalog grows; the loop and budget
  logic are written to absorb future catalog growth without refactor.
- `pricing.yaml` — does not exist yet; Phase 2 introduces it.
- `.tokenman/PAUSE`, `.tokenman/tokenman.yaml`, `.tokenman/CLAUDE.md` —
  library stays paused. Phase 1.4 PAUSE status: ON.

## 11. Success criteria

- `python -m harness.onboard --dry-run --non-interactive --repo
  tests/fixtures/tiny-python-repo --skill stub-skill-a --skill
  stub-skill-b` exits 0, writes a summary file with all expected
  sections, lists every requested skill.
- A skill returning `status=error` does not stop subsequent skills.
- Session-ceiling breach is observable in the summary, not silent.
- Live test passes against real `claude -p` in <90s.
- Workflow template change is backwards-compatible: `mode` defaults to
  `single`, and `mode=single` runs exactly the existing
  `harness.run --skill` path.
- Library PAUSE remains ON; no dogfood execution at any point during
  Phase 1.4.

## 12. Phase 1.5 candidates surfaced by this design

Not in scope, but called out so they don't get lost:

- **Skill install flow.** Onboarding assumes `.claude/skills/` is
  already populated (or that catalog `source:` is local). A consumer
  workflow that does `tokenman scope` → `tokenman install` →
  `tokenman onboard` is the natural next user journey.
- **Pre-run "confirm N PRs?" dialog.** `--non-interactive` is reserved
  for it. Phase 1.4 doesn't need it because dry-run + fixtures cover
  development; a real consumer running onboarding for the first time
  may want one.
- **Summary linking back to ledger entries.** Currently the summary
  references `runs/<run_id>/executor.stderr` for errors. When the
  ledger gets a query interface, summary entries could deep-link.
