# Tokenman — Specification

**Version:** 0.2 (draft)
**Author:** Lee (Verky Yi)
**Status:** Scoping draft — pre-implementation
**Changelog:** v0.2 — switched from split-repo (Option A) to single-repo dogfood (Option B); added paused-by-default discipline, source/runtime separation, and phased PAUSE-removal plan.

---

## 1. What tokenman is

Tokenman is a **harness that makes `claude -p` safe to run unattended on a repo**. It lets any repo install a background maintenance agent that proposes changes via PRs on a schedule, within a budget the user controls, without requiring the user to supervise.

Tokenman is **not** a skills library, not a hosted service, not a CLI wrapper, not a framework. It is a runtime plus a curated catalog of community skills.

**Product sentence:**
> Tokenman is the runtime that makes `claude -p` safe to run unattended on your repo.

**What tokenman ships:**
- A harness (scheduled workflows, guardrails, observability)
- A scoping and onboarding flow
- A curated catalog of recommended skills (references, not copies)
- Documentation and conventions

**What tokenman does not ship:**
- Its own skills
- Hosted infrastructure
- Cloud accounts or dashboards
- A terminal/CLI product (separate side project, out of scope)

**Tokenman dogfoods itself.** The tokenman library repo is also its own first consumer, under strict scope and phased trust (see §3 and §12).

---

## 2. Core principle

**The harness and the interactive session share the repo as their only medium.**

Every piece of state tokenman holds is a file in the repo. Every instruction the user gives is a file edit. Every output is a PR, an issue, or a file. No side channels, no external databases, no proprietary interfaces.

Consequences:
- Uninstall = `rm -rf .tokenman/ .github/workflows/tokenman.yml .claude/skills/`
- Fork a tokenman-enabled repo → the fork has tokenman
- Interactive Claude Code sessions can read, understand, and modify tokenman state with no special integration
- Git history is tokenman's audit log
- The only principled exception is secrets (GitHub Actions secrets, referenced by name in the repo)

---

## 3. Architecture overview

### 3.1 One repo, two roles

Tokenman lives in a single repository (`github.com/verky/tokenman`) that serves as both:

- **The library** — source of the harness, scoping logic, onboarding flow, and skills catalog
- **Its own first consumer** — tokenman is dogfooded against the library itself, under strict scope and phased trust

Dogfooding is the default posture, but it is **paused by default** and opens up incrementally by phase. The discipline that makes this safe is the strict separation between source paths and runtime paths described in §3.2, plus the phased PAUSE-removal schedule in §12.

External consumers still install tokenman into their own repos in the usual way — nothing about the single-repo structure affects the consumer experience.

### 3.2 Source vs runtime paths

The repo has two structurally distinct zones:

**Source zone** (what tokenman *is*):
```
harness/                     # runtime code, workflow templates
scoping/                     # discovery and scope-proposal logic
onboarding/                  # guided first-run flow
recommended-skills.yaml      # curated catalog
docs/                        # documentation
tests/fixtures/              # synthetic consumer repos for harness testing
```

**Runtime zone** (what tokenman *does on this repo*):
```
.tokenman/                   # config, state, ledger, artifacts — for dogfooding
.github/workflows/           # actual workflows that run on this repo
.claude/skills/              # skills installed for this repo's own dogfooding
```

Files in the source zone are what gets shipped to external consumers. Files in the runtime zone are local operational state from dogfooding. The two zones are never conflated: the workflow that ships to consumers lives at `harness/workflows/tokenman.yml.template`; the workflow that runs on *this* repo lives at `.github/workflows/tokenman.yml`. Updates to the template do not automatically update the runtime copy — that's a deliberate install step.

### 3.3 Repo file layout (library + dogfood)

```
tokenman/
├── README.md                          # explains library-is-also-consumer structure
├── CONTRIBUTING.md                    # explains the source/runtime split for contributors
├── harness/
│   ├── workflows/
│   │   └── tokenman.yml.template      # SOURCE — what gets installed into consumers
│   ├── lib/                           # runtime logic (generator/evaluator drivers, etc.)
│   └── README.md
├── scoping/
│   └── ...                            # SOURCE — discovery + scope-proposal
├── onboarding/
│   └── ...                            # SOURCE — guided first-run flow
├── recommended-skills.yaml            # SOURCE — curated catalog
├── pricing.yaml                       # SOURCE — budget calibration data
├── docs/
│   └── ...
├── tests/
│   └── fixtures/                      # fake consumer repos for harness testing
│       ├── tiny-python-repo/
│       └── tiny-typescript-repo/
├── .tokenman/                         # RUNTIME — dogfooding state on THIS repo
│   ├── PAUSE                          # committed as present in Phase 0-2 (see §12)
│   ├── tokenman.yaml                  # config; schedule.strategy: manual until Phase 3
│   ├── CLAUDE.md                      # paranoid boundaries for self-application
│   ├── learned.md                     # appears Phase 4+
│   ├── ledger.jsonl                   # appears when first run happens
│   └── runs/                          # appears when first run happens
├── .github/
│   └── workflows/
│       └── tokenman.yml               # RUNTIME — gated by PAUSE
└── .claude/
    └── skills/                        # RUNTIME — empty in Phase 0-2; populated later
```

### 3.4 Consumer repo file layout (external users)

When an external user installs tokenman, their repo gets:

```
.tokenman/
  tokenman.yaml              # config: enabled skills, budget, schedule
  CLAUDE.md                  # user-authored guidance for the agent
  learned.md                 # harness-authored preference inferences (Phase 4+)
  initial-scope.md           # committed artifact of the init scoping decision
  PAUSE                      # optional kill-switch (presence = paused)
  ledger.jsonl               # append-only run log
  runs/
    r-NNNN/
      proposed.diff
      proposed.md
      deterministic.log
      evaluator.json
      ledger.entry
.claude/
  skills/                    # installed skills (fetched from catalog)
.github/
  workflows/
    tokenman.yml             # the scheduled workflow
```

Identical structure to the library's runtime zone. This is not a coincidence — it's the product of the source/runtime separation. The library's runtime zone is the canonical example of what a consumer looks like.

---

## 4. The execution pipeline

Each tokenman run is a DAG of stages. In Phase 1 it's linear; by Phase 4 it's parallelized across skills.

### 4.1 Stage diagram (single run)

```
1. Trigger check (cheap, deterministic)
   ├─ budget check — current cycle usage vs cap
   ├─ cooldown check — minimum interval since last run of this skill
   ├─ PAUSE check — does .tokenman/PAUSE exist?
   ├─ review-bandwidth check — unresolved tokenman PRs under threshold?
   └─ open-PR lock — is there already an open PR for this skill?

2. Generator (LLM, permissive)
   ├─ reads: SKILL.md, .tokenman/CLAUDE.md, .tokenman/learned.md, recent ledger
   ├─ task: propose one scoped change (or empty diff with explanation)
   └─ writes: .tokenman/runs/r-NNNN/proposed.diff + proposed.md

3. Deterministic gate (code, free)
   ├─ scope — touches only permitted files
   ├─ shape — matches skill's expected diff pattern
   ├─ size — within skill's size limit
   ├─ forbidden patterns — no disallowed content
   └─ file-type allowlist — correct extensions modified

4. Evaluator (LLM, strict, adversarial)
   ├─ reads: proposed.diff, SKILL.md criteria, CLAUDE.md boundaries
   ├─ does NOT read: generator's rationale (fresh eyes)
   ├─ task: find reasons to reject; approve only if no defensible rejection
   └─ writes: evaluator.json { verdict, reason }

5. PR opener (serialized)
   ├─ opens PR against branch `tokenman/<skill>/r-NNNN`
   ├─ labels with `tokenman:<skill>`, never auto-merges
   ├─ appends ledger entry with all run metadata
   └─ updates learned.md proposals if applicable
```

### 4.2 Cost shape

- Trigger check: free
- Generator: 10-30k tokens per run (depends on skill)
- Deterministic gate: free
- Evaluator: 2-5k tokens per run
- PR opener: minimal (GitHub API)

Bad runs die at stages 1 or 3, costing nothing or only the generator. Approved runs cost generator + evaluator. Weekly average per skill: ~15-25k tokens on mature tuning.

---

## 5. Skills model

### 5.1 Reference, don't ship

Tokenman ships **zero skills**. It ships a **curated catalog** of community skills, pinned by version and source. Each entry:

```yaml
# recommended-skills.yaml
readme-maintainer:
  source: github.com/someone-else/claude-readme-skill
  version: v1.2.0
  tier: starter                 # starter | common | advanced
  blast_radius: low             # low | medium | high
  typical_tokens_per_run: 15000
  description: Keeps README aligned with actual repo contents.
  default_cadence: on-change
  evaluator_strictness: medium
```

The library maintainer's editorial job: evaluate skills, pin known-good versions, drop misbehaving skills, add new ones as the ecosystem grows.

### 5.2 Skill installation

`/tokenman init` fetches skills from their pinned sources into the consumer's `.claude/skills/`. The user's tokenman install is a combination of the harness (from `verky/tokenman`) and skills (from wherever they live).

### 5.3 Skill contract

For a skill to work under tokenman's harness, its `SKILL.md` must specify:

- Name, version, origin
- Scope — which files/paths it operates on
- Shape — expected diff pattern (additive, subtractive, in-place, etc.)
- Size limit — maximum diff size
- Deterministic gate hints — any skill-specific checks
- Evaluator criteria — what the evaluator should check for
- Typical token budget — upper bound for one run

Skills that don't conform are not included in the catalog.

---

## 6. The user journey

### 6.1 Discovery

User encounters tokenman via Claude Code community, a friend, or a post. Lands on `github.com/verky/tokenman`. README explains what tokenman is in one screen, shows a short demo, links to install. Crucially, the README also shows tokenman's own commit history as evidence — the library has been dogfooding tokenman for weeks/months, so the user can see real PRs opened by real runs.

### 6.2 Install

```bash
# In the user's repo:
/tokenman init
```

Effects:
- Writes `.tokenman/tokenman.yaml` (seeded with detected facts)
- Writes `.tokenman/CLAUDE.md` (with TODO placeholders)
- Writes `.github/workflows/tokenman.yml`
- Fetches initial recommended skills into `.claude/skills/`
- Everything visible in `git status` before commit

### 6.3 Initial scoping

After install, tokenman runs a **discovery and scoping pass**:

```
tokenman scope
```

Output: `.tokenman/initial-scope.md` — a draft scope proposal presenting:
- Repo profile (language, size, test coverage, activity, deps)
- Suggested skills (3-5 from the catalog, chosen based on repo profile)
- Skipped skills (with reasoning)
- Suggested boundaries (file allowlists/denylists)
- Suggested budget (percentage of user's Claude subscription)
- Suggested schedule strategy (fixed/adaptive/event-driven)
- Expected PR volume

User reviews, edits, and confirms. The scope becomes the initial `tokenman.yaml` content.

### 6.4 Guided onboarding run

Triggered on install (with consent) or manually:

```bash
gh workflow run tokenman.yml -f mode=onboarding
```

In onboarding mode:
- Runs all enabled skills back-to-back in one session
- Uses an elevated budget (3× normal weekly cap, still hard-capped)
- Opens one labeled PR per skill
- Writes `.tokenman/onboarding-summary.md` with:
  - What the harness observed
  - What each skill proposed (linked to PRs)
  - What was considered but not proposed (self-restraint)
  - What the user can do next
  - Cost and budget utilization

User ends up with 2-4 reviewable PRs within ~10 minutes of install.

### 6.5 Settling in

Weekly/monthly runs begin on schedule. User reviews PRs at their pace. Ledger accumulates. Customization via `.tokenman/CLAUDE.md` edits.

### 6.6 Ongoing teaching

From Phase 4 onward, tokenman observes PR outcomes and writes preference inferences to `.tokenman/learned.md`. The user reviews and approves each inferred preference. Approved preferences feed back into generator and evaluator prompts on subsequent runs.

---

## 7. Budget and scheduling

### 7.1 Budget calibration during init

Tokenman detects (or asks about) the user's Claude subscription and billing cycle. It suggests a percentage allocation:

- **5% — Conservative** — 1-2 PRs/week, minimal cost
- **10% — Recommended (default)** — 2-4 PRs/week, balanced
- **20% — Aggressive** — 4-8 PRs/week, proactive maintenance
- **Custom** — user-specified percentage

Suggestions translate to concrete token budgets (per-run, weekly, monthly) displayed alongside the percentage.

`pricing.yaml` in the library repo is pulled at init time, ensuring budget suggestions reflect current Claude pricing.

### 7.2 Budget enforcement

Three-layer cap hierarchy:

| Cap | Enforced at | Action on breach |
|---|---|---|
| Per-run | Before generator starts | Skip run, log `skipped_run_cap` |
| Per-skill weekly | Before generator starts | Skip run, log `skipped_skill_cap` |
| Global weekly/monthly | Before generator starts | Skip run, log `skipped_global_cap` |

Caps are re-checked before each stage; any stage that would exceed a cap fails the whole run gracefully.

**Library repo has stricter caps.** The library's own `.tokenman/tokenman.yaml` sets budgets at roughly 20% of a normal consumer's default. The library is not a typical consumer and should not spend like one.

### 7.3 Schedule strategies

Declared in `tokenman.yaml`:

```yaml
schedule:
  strategy: adaptive          # fixed | adaptive | event-driven | manual
  target_utilization: 80%     # adaptive: aim for this fraction of budget
  min_interval: 48h
  max_interval: 14d
  pause_at: 95%               # throttle hard at this fraction of budget
```

**Fixed** — runs on defined cadence (e.g., weekly Sunday midnight). Simple, predictable.

**Adaptive** — self-tunes based on ledger history:
- Low utilization → run more often
- High utilization → run less often
- Repeated no-ops → back off
- Recent activity spike → accelerate

**Event-driven** — triggers on repo events (PR merged, commits to main) rather than schedule. Most responsive to real work.

**Manual** — never runs on a schedule; only via `workflow_dispatch`. This is the library repo's default until Phase 3.

Init recommends a strategy based on repo activity detected during discovery.

---

## 8. Observability

### 8.1 The ledger

`.tokenman/ledger.jsonl` — append-only, one line per run, always written:

```json
{
  "run_id": "r-0087",
  "ts": "2026-05-03T10:30Z",
  "skill": "readme-maintainer",
  "status": "pr_opened",
  "pr": 128,
  "generator": {
    "prompt_version": "v3",
    "output_summary": "proposed adding a 'Usage' section",
    "diff_lines": 34,
    "tokens": 14200
  },
  "evaluator": {
    "prompt_version": "v1",
    "verdict": "approve",
    "reason": "scope appropriate, additive, consistent with repo style",
    "tokens": 3100
  },
  "duration_s": 42,
  "total_tokens": 17300,
  "verdict": null,
  "verdict_note": null
}
```

`status` is a fixed enum: `pr_opened | no_change | skipped_lock | skipped_cooldown | skipped_budget | skipped_pause | skipped_review_bandwidth | aborted_gate | aborted_evaluator | error`.

`verdict` is null on write. User fills it in during weekly review: `merged_good | closed_bad | stale | ignored`.

### 8.2 Per-run artifacts

`.tokenman/runs/r-NNNN/` holds the proposed diff, generator reasoning, evaluator verdict, and intermediate logs. Retention: full artifacts for 30 days (configurable), ledger summary forever.

Garbage collection runs as part of the workflow, deleting old artifact directories and pruning merged branches. The library repo uses an accelerated retention (14 days for artifacts) to contain dogfood noise.

### 8.3 The status script

`harness/templates/status.sh` (library dev copy; installed as `.tokenman/status.sh` in consumer repos) reads the ledger and prints:

```
Tokenman status — last 7 days

Runs:       23
PRs opened:  8  (3 merged, 2 closed, 3 pending)
No-change runs: 11
Skipped:  4  (2 cooldown, 1 lock, 1 budget)

Tokens: 287,450  (avg 12,500/run, 57% of weekly cap)
Top consumers:
  readme-maintainer    180,100
  dead-code-cleanup     87,250
  dep-bump-safe         20,100

Last 5 runs:
  r-0042  05-03 10:30  readme-maintainer  pr_opened     17,300 tok
  r-0041  05-02 10:30  readme-maintainer  no_change      8,200 tok
  r-0040  05-01 10:30  dead-code-cleanup  skipped_lock       0 tok
  ...
```

Designed for `cat`, `jq`, and quick human skim. No dashboard until file-based observability genuinely breaks down.

### 8.4 Self-inspectability

Interactive Claude Code sessions can reconstruct full tokenman history from files alone. A user asking "why did tokenman reject this change two weeks ago?" gets a correct answer because the diff, verdict, and reason all live in the repo.

### 8.5 Filtering dogfood noise in library git history

The library repo's git log interleaves human contributions and tokenman-opened PRs. Contributors who want to see only human history use:

```bash
git log --grep='\[tokenman\]' --invert-grep
```

All tokenman-opened PRs on the library repo have commit messages prefixed `[tokenman]` by convention. CONTRIBUTING.md documents this for new contributors.

---

## 9. Safety model

### 9.1 Action types

- **PR opens** — the only mechanism by which tokenman proposes changes
- **Issue opens** — for observations the harness wants to surface but not act on
- **File writes in `.tokenman/`** — ledger, artifacts, learned preferences
- **No direct commits to main** — ever
- **No auto-merge** — ever
- **No branch deletion outside its own** — tokenman only manages `tokenman/*` branches

### 9.2 Guardrails (enforced in this order)

1. PAUSE file respected — presence of `.tokenman/PAUSE` halts all runs
2. Budget caps enforced — per-run, per-skill, per-cycle
3. Cooldown — minimum interval between runs of the same skill
4. Open-PR lock — one open PR per skill at a time
5. Review-bandwidth gate — skip scheduled runs if unresolved tokenman PRs exceed threshold
6. Scope check — proposed changes must stay within declared boundaries
7. Size cap — diffs exceeding skill limits are rejected
8. Evaluator gate — LLM evaluator can reject any proposal
9. Stale PR auto-close — tokenman PRs open >14 days are closed with a comment

### 9.3 Human coexistence

When human and harness edit the same file:

- Harness PRs are always against fresh branches (`tokenman/<skill>/r-NNNN`)
- CLAUDE.md can declare "hot paths" — files recently modified on main that the harness should skip
- Harness yields to human activity (timid-by-default)
- Merge conflicts on tokenman PRs are the human's choice to resolve or close

### 9.4 Teaching and steering

All harness steering happens via file edits:

- **Teach** — append to `.tokenman/CLAUDE.md`
- **Pause** — create `.tokenman/PAUSE`
- **Steer** — edit `.tokenman/tokenman.yaml` (skills list, budgets, schedule)
- **Skip run** — delete scheduled workflow trigger
- **Force run** — `workflow_dispatch`

All of these are achievable in an interactive Claude Code session with no special tooling.

---

## 10. Dogfooding disciplines (library-specific)

Because tokenman lives in the same repo as the library, dogfooding requires disciplines beyond what a typical consumer needs. These are non-optional.

### 10.1 Paused by default

The library repo's `.tokenman/PAUSE` file is committed at repo creation. The workflow file exists but will not execute while PAUSE is present. PAUSE is only removed at the phase gates defined in §12.

### 10.2 Paranoid CLAUDE.md

The library's `.tokenman/CLAUDE.md` is the strictest in existence. It is heavy on forbidden paths and light on permitted paths. Example:

```markdown
# Tokenman context for the tokenman library repo

## CRITICAL: this repo is the tokenman library itself.
## Dogfooding is SEVERELY restricted.

## Allowed paths (nothing else)
- docs/**/*.md
- README.md
- CHANGELOG.md

## FORBIDDEN paths (never touch)
- harness/           — the runtime itself
- scoping/           — the scoping logic itself
- onboarding/        — the onboarding logic itself
- recommended-skills.yaml  — the catalog
- pricing.yaml       — budget calibration data
- .github/           — the workflows
- .claude/skills/    — installed skills
- tests/fixtures/    — must remain pristine

## FORBIDDEN operations
- Any change that could affect how the harness behaves
- Any change to version numbers
- Any change to package.json / pyproject.toml

## If in doubt, abort.
```

The rule: **tokenman on the library can only do things that, if wrong, embarrass us but don't break us.** README typos, doc clarifications, example updates — yes. Anything that affects the harness's own behavior — never.

### 10.3 Smoke test before real work

When PAUSE is first removed on the library (Phase 3), the first workflow run is a no-op smoke test:

- Reads the config
- Checks trigger gates
- Writes a single ledger entry saying "smoke test passed"
- Opens a PR that adds a line to a `.tokenman/smoketest.md` file

No creative output. No source code touched. Just proof that the harness machinery works on the real thing. The smoke test runs for a week before any real skill executes on the library.

### 10.4 Development loop uses fixtures, not the library

Iterating on the harness (fixing bugs, tuning prompts, testing new guardrails) uses `tests/fixtures/*`, not the live library. The library's own scheduled runs use the current committed harness; they are a validation layer, not a development environment.

Rule of thumb: if tempted to trigger a manual run on the library to test a change, trigger it on a fixture instead.

### 10.5 Stricter retention and caps

The library's own `.tokenman/tokenman.yaml`:

- Budget cap at ~20% of a normal consumer's default
- Artifact retention: 14 days (vs 30 for normal consumers)
- Schedule: `manual` until Phase 3; `adaptive` with conservative params thereafter

### 10.6 `[tokenman]` commit prefix

All commits tokenman opens on the library repo have messages prefixed `[tokenman]`. This enables clean filtering of human vs harness history (§8.5).

---

## 11. Learning loop (Phase 4+)

### 11.1 Signal sources (ranked by reliability)

| Signal | Reliability |
|---|---|
| PR merged as-is | High |
| PR merged with edits | Medium-high |
| PR closed with substantive comment | High |
| Line-level review comments | High |
| Labels added (`wontfix`, `needs-rework`) | High |
| PR merged with edits (unexplained) | Medium |
| PR closed silently | Medium-low |
| PR stale >14 days | Low |

### 11.2 Learning mechanism

After each run, the harness observes PR outcomes via GitHub API. When patterns emerge across ≥N runs (threshold configurable, default 5), the harness proposes a learning:

```markdown
# learned.md

## Proposed learnings (pending user approval)

### readme-maintainer
- Observation: 3 of last 5 merged PRs had emojis removed in commit edits
- Proposed preference: "do not use emojis in headings"
- Evidence: r-0087 (commit 3a2b), r-0094 (commit f8e1), r-0101 (commit 2d4c)
- [Approve] [Reject] [Edit]

## Approved preferences (active)

### readme-maintainer  
- (2026-04-12) No emojis in headings — 5 consecutive merged PRs support this
```

Approved preferences are injected into the generator and evaluator prompts on subsequent runs. Rejected preferences are recorded (so they don't re-propose identically). Learnings are repo-scoped — never leaked across consumers.

### 11.3 Risks and mitigations

- **Overfitting to quirks** — learnings live in the consumer repo only
- **Bad signal from silent closures** — weight explicit feedback much higher
- **Noise amplification** — threshold prevents one-off events from becoming preferences
- **Opaque behavior change** — every learning is user-approved before activation

---

## 12. Phased roadmap

Each phase has a defined library-PAUSE status. The dogfood opens up incrementally as the harness earns trust.

### Phase 0 — Foundation (week 1)
- Repo scaffolding with both source zone (`harness/`, `scoping/`, `onboarding/`, `recommended-skills.yaml`) and runtime zone (`.tokenman/`, `.github/workflows/`, `.claude/skills/`)
- `.tokenman/PAUSE` committed at creation
- Paranoid `.tokenman/CLAUDE.md` written
- CONTRIBUTING.md explains source/runtime split
- Fixture repos under `tests/fixtures/` for harness testing
- Nothing runs on the library repo

**Library PAUSE status:** ON (committed).

**Exit:** repo tree clean, contracts written, nothing runs yet.

### Phase 1 — Wedge + guided onboarding (weeks 2-4)
- Integrate first recommended skill (`readme-maintainer` from community) — validated against fixtures, not the library
- Initial scoping flow implemented (`tokenman scope` produces `initial-scope.md`)
- Guided onboarding mode with elevated budget, summary file, PR-per-skill
- Basic linear workflow
- Ledger schema locked, status script v1
- Fixed weekly schedule as default for consumers

**Library PAUSE status:** ON.

**Exit:** can install tokenman into a consumer repo (fixture or external), run scoping, trigger onboarding, see 1-2 meaningful PRs within 10 minutes.

### Phase 2 — Trust and observability (week 5)
- Budget calibration in init (subscription detection, percentage suggestion)
- Adaptive scheduling (uses ledger data to self-tune)
- PAUSE file, per-run cap, weekly cap enforced
- Review-bandwidth gating
- Stale PR auto-close
- Weekly retro-verdict review habit documented

**Library PAUSE status:** ON.

**Exit:** "what did tokenman do and what did it cost?" answerable in <10 seconds on consumer repos; harness self-regulates within budget.

### Phase 3 — Evaluator and artifacts + first dogfood (weeks 6-8)
- Generator/evaluator split
- Deterministic gate (scope, shape, size, pattern checks)
- Per-run artifact directories
- Rejection-reason feedback loop into prompt tuning
- **Library PAUSE removed for smoke test only** (§10.3) — one week of no-op runs
- After clean smoke-test week: narrow dogfood on library README only, with `readme-maintainer`, budget capped at 20% of normal

**Library PAUSE status:** OFF (smoke test first, then narrow README scope).

**Exit:** measurable drop in bad-PR rate on fixtures; library has survived one week of smoke tests plus several narrow dogfood runs without incident.

### Phase 4 — Multi-skill, learning, and wider dogfood (weeks 9-11)
- Second and third recommended skills integrated
- DAG-based parallel workflow
- Learning loop: PR outcome observation, `learned.md`, user-approved preferences
- Harness proven skill-agnostic (no special cases)
- **Library dogfood widens** to include `docs/` and `CHANGELOG.md` but not harness source
- Additional skills on library repo run only if they explicitly stay within allowed paths

**Library PAUSE status:** OFF, scope widened to docs.

**Exit:** 3+ skills running in parallel on fixtures; first learnings approved; library repo safely dogfooding broader docs scope.

### Phase 5 — Distribution polish (weeks 12-14)
- `/tokenman init` as polished Claude Code slash command
- Versioned skills catalog with semver pinning
- Install docs with expected-cost grounding drawn from library's own ledger
- First external user onboarded end-to-end
- Subscription-aware budget UX fully wired

**Library PAUSE status:** OFF, scope unchanged from Phase 4.

**Exit:** at least one external user installs, runs, and merges a tokenman PR; library's own commit history is usable as a public demo.

### Phase 6+ — Demand-driven
Only built if users ask:
- `/tokenman teach` formalized as file-edit shortcut
- Third-party skills catalog (community submissions)
- More recommended skills added as the ecosystem grows
- Dashboard or web UI (only if JSONL breaks down)
- GitHub App wrapper (if install friction blocks adoption)

**Library PAUSE status:** OFF, with permanent prohibition on scoping tokenman onto `harness/`, `scoping/`, `onboarding/`, `recommended-skills.yaml`, `pricing.yaml`, `.github/`, `.claude/skills/`, or `tests/fixtures/`. Those changes require human judgment and do not ever get delegated to the harness.

---

## 13. What stays out of scope permanently

- Hosted runners or SaaS tier
- Paid plans — tokenman is free and open source
- Terminal.tokenman.io as a primary product (remains side project)
- Multi-repo orchestration (one repo at a time)
- Framework ambitions (tokenman is a specific tool, not a general platform)
- Shipping our own skills (permanent editorial discipline)
- Auto-merge capability
- Direct commits to main
- Tokenman touching its own harness source (permanent, enforced by library CLAUDE.md)

---

## 14. Open questions

These are unresolved and should be answered before the relevant phase:

1. **Subscription detection mechanism** — does Claude CLI expose subscription tier in a way tokenman can read, or is it a user prompt? (Phase 2)
2. **Skills catalog governance** — how are new skills vetted for inclusion? What's the removal criterion? (Phase 4+)
3. **Learning loop threshold defaults** — how many consistent signals before a learning is proposed? (Phase 4, will require tuning)
4. **Library dogfood scope expansion criteria** — what evidence is needed before widening scope in each phase? (Phase 3 and 4 — probably "N clean weeks of current scope")
5. **First external user acquisition channel** — Claude Code community? Chinese dev community? HN Show? (Phase 5)

---

## 15. Success criteria

Tokenman is a success if:

- A user can install it in under 5 minutes
- First meaningful PR appears within 10 minutes of install
- The ledger and status script together answer "what did it do and what did it cost?" in under 30 seconds
- Weekly operating cost is predictable and within the user's chosen budget
- At least 50% of scheduled runs produce useful output (either a merged PR or a correctly-skipped run)
- Users who install it still have it installed 60 days later
- The library repo grows more skills in its catalog over time without growing the harness
- The library's own dogfood history is demonstrable as public evidence by Phase 5

Tokenman is a failure if:

- Users uninstall within a week
- Ledger or PAUSE mechanisms are insufficient to build trust
- Users cannot explain what tokenman does after using it for a month
- The harness becomes coupled to specific skills (skill changes require harness changes)
- We drift into shipping skills instead of curating them
- The library dogfood causes token waste or corrupts the harness source (this would require rolling back dogfood scope, not abandoning Option B)

---

## 16. Glossary

- **Harness** — the tokenman runtime itself: workflows, guardrails, observability, scoping, onboarding
- **Skill** — an external, community-authored piece of maintenance capability, referenced by tokenman's catalog
- **Library repo** — `github.com/verky/tokenman`, source of the harness and also its own first consumer
- **Consumer repo** — any repo with tokenman installed; the library repo is its own consumer
- **Source zone** — `harness/`, `scoping/`, `onboarding/`, `recommended-skills.yaml`, `pricing.yaml`, `docs/`, `tests/fixtures/` — what tokenman *is*
- **Runtime zone** — `.tokenman/`, `.github/workflows/`, `.claude/skills/` — what tokenman *does on this repo*
- **Dogfood** — tokenman running on the tokenman library repo itself, under strict phased scope
- **Ledger** — `.tokenman/ledger.jsonl`, the append-only run log
- **Scope** — the declared boundaries of what tokenman may touch in a consumer repo
- **Run** — a single invocation of one skill through the full pipeline
- **Cycle** — a budget period (usually aligned with Claude subscription billing cycle)
- **Generator / Evaluator** — the two LLM stages of a Phase 3+ run
- **Deterministic gate** — the code-based checks between generator and evaluator
- **Learning** — an inferred preference the harness proposes based on PR outcomes
- **Onboarding mode** — the elevated-budget first-run that demonstrates value immediately
- **Smoke test** — the no-op first run after PAUSE removal on the library, to verify machinery without risk

---

*End of spec. Version 0.2 — Option B dogfood structure with phased PAUSE-removal. Expect further refinements as Phase 0 begins.*
