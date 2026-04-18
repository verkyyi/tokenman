# Phase 1.3 — Scoping flow design

**Phase:** 1.3
**Date:** 2026-04-18
**Status:** draft — pre-implementation
**Implements:** spec.md §6.3 (initial scoping)
**Supersedes:** none

---

## 1. Goal

Deliver `python -m harness.scope` — a CLI that inspects a consumer repo,
queries the Claude Code plugin marketplace(s), asks the user a few
interactive questions, calls `claude -p` once, and emits
`.tokenman/initial-scope.md` — the artifact that seeds the user's
initial `tokenman.yaml`.

This is the **minimum viable** implementation of spec §6.3. Budget,
schedule strategy, and expected PR volume are explicitly deferred to
Phase 2 (see §7 below).

## 2. Non-goals

- Budget section in `initial-scope.md` — Phase 2 (spec §7).
- Schedule-strategy section — Phase 2.
- Expected-PR-volume estimation — needs ledger history, Phase 4.
- Installing skills from the scope file — separate flow, Phase 1.4.
- Writing `.tokenman/tokenman.yaml` — the user does that manually in
  Phase 1, using the scope file as reference.
- Any changes to `harness/run`, `harness/lib/runner.py`, or the
  execution pipeline — Phase 1.3 is discovery-only.
- Library-side dogfood — scoping is exercised via fixtures (spec §10.4).

## 3. User journey

```
$ cd my-repo
$ python -m harness.scope
[inspecting repo...]
[loading 2 marketplaces, 147 plugins total]

A few questions:

  1. What's this repo for? (one line)
     > a CLI tool for managing todo lists

  2. What's your main maintenance concern?
     [a] keeping docs honest  [b] dep freshness
     [c] dead code cleanup    [d] other
     > a

  3. Paths off-limits? (comma-separated globs, blank to skip)
     > migrations/**, scripts/legacy/**

  4. Anything else the scoping agent should know?
     >

[calling claude -p...]

=== Draft .tokenman/initial-scope.md ===
<rendered markdown preview>
========================================

Accept this draft? [a]ccept / [e]dit in $EDITOR / [x] abort
> a

Wrote .tokenman/initial-scope.md
```

## 4. Architecture

### 4.1 Module layout

```
harness/
├── scope/
│   ├── __init__.py
│   └── __main__.py               # CLI entry point
├── lib/
│   ├── repo_profile.py           # deterministic repo inspection
│   ├── marketplace.py            # read marketplace.json manifests
│   └── scope_drafter.py          # orchestrates claude -p, allowlist enforcement
└── prompts/
    └── scoping.v1.md             # versioned system-prompt framing
```

Matches the `harness/run/` + `harness/lib/{git_ops,pr_opener,…}.py`
pattern established in Phase 1.2b. Prompt framing is versioned with a
`.v1` suffix per the Phase 1.2b precedent (`unattended_framing.v1.md`);
a bump = new file + `prompt_version` bump in the output metadata.

### 4.2 Data flow

```
  [CLI argv]
      │
      ▼
  repo_profile.inspect(repo_dir) ──► RepoProfile
      │
      ▼
  marketplace.list_plugins(refresh?) ──► list[Plugin]
      │
      ▼
  _ask_interactive_questions() ──► dict[str, str]
      │
      ▼
  scope_drafter.draft(
      profile, plugins, user_answers,
      catalog = recommended-skills.yaml,
      executor = ClaudeScopeExecutor | StubScopeExecutor,
  ) ──► ScopeDraft (typed)
      │
      ▼
  _enforce_allowlist(draft, catalog) ──► ScopeDraft'
      │
      ▼
  _render_markdown(draft') ──► str
      │
      ▼
  [show preview, accept/edit/abort]
      │
      ▼
  write .tokenman/initial-scope.md
```

## 5. Component details

### 5.1 `harness/lib/repo_profile.py`

**Purpose:** deterministically summarise a repo. No LLM, no network.

**Entry point:**
```python
def inspect(repo_dir: Path) -> RepoProfile:
    ...
```

**`RepoProfile` TypedDict:**
```python
class RepoProfile(TypedDict):
    languages: dict[str, int]       # {"python": 42, "yaml": 8}
    total_files: int
    total_bytes: int
    tests_present: bool
    ci_present: bool
    readme_present: bool
    deps_files: list[str]           # ["pyproject.toml", "package.json"]
    recent_commits_30d: int
```

**Detection rules (deliberately simple):**
- `languages`: count of tracked files per extension, mapped to a
  canonical language via a small hardcoded table (`py`→`python`,
  `ts`→`typescript`, etc.). Unknown extensions go to `"other"`.
- `total_files`, `total_bytes`: from `git ls-files -z` output.
- `tests_present`: any of `tests/`, `test/`, `__tests__/`, or files
  matching `test_*.py`, `*_test.go`, `*.spec.ts`, `*.test.js`.
- `ci_present`: `.github/workflows/` or `.circleci/config.yml` or
  `.gitlab-ci.yml` exists.
- `readme_present`: any `README*` at repo root.
- `deps_files`: presence check for
  `pyproject.toml`, `requirements.txt`, `package.json`,
  `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, `build.gradle`.
- `recent_commits_30d`: `git rev-list --count --since='30 days ago' HEAD`.

**Failure modes:**
- Not a git repo → `RepoProfileError("<path> is not a git repository")`.
- Empty repo (no commits) → `recent_commits_30d = 0`, continue.

### 5.2 `harness/lib/marketplace.py`

**Purpose:** enumerate plugins across configured marketplaces.

**Entry points:**
```python
def list_plugins(refresh: bool = False) -> list[Plugin]:
    ...

def marketplace_root() -> Path:
    # ~/.claude/plugins/marketplaces/
    ...
```

**`Plugin` TypedDict:**
```python
class Plugin(TypedDict):
    name: str
    description: str
    category: Optional[str]
    homepage: Optional[str]
    marketplace: str     # provenance — which marketplace it came from
```

**Behavior:**
- `marketplace_root()` = `Path.home() / ".claude" / "plugins" / "marketplaces"`.
- `list_plugins(refresh=True)` first runs
  `subprocess.run(["claude", "plugins", "marketplace", "update"])`
  (best-effort; non-zero exit is logged but not fatal — read stale cache).
- Globs `marketplace_root() / "*/.claude-plugin/marketplace.json"`,
  parses each, flattens the `plugins[]` array, decorates each entry
  with `marketplace=<dir-name>`.
- If root is missing or no manifests found, returns `[]` with a
  warning printed to stderr. Scope generation continues with empty
  registry (see §5.4, §5.6).

**Failure modes:**
- Malformed `marketplace.json` → log warning, skip that manifest,
  continue with the rest.

### 5.3 `harness/lib/scope_drafter.py`

**Purpose:** call `claude -p`, parse the response, enforce the catalog
allowlist.

**Entry point:**
```python
def draft(
    *,
    profile: RepoProfile,
    plugins: list[Plugin],
    user_answers: dict[str, str],
    catalog: dict[str, dict],    # parsed recommended-skills.yaml
    executor: ScopeExecutor,     # protocol, see below
    prompt_version: str = "v1",
) -> ScopeDraft:
    ...
```

**`ScopeExecutor` protocol:**
```python
class ScopeExecutor(Protocol):
    def run(self, *, system_prompt: str, user_payload: str) -> str:
        """Returns the raw JSON string from claude -p's `result` field.

        Raises ScopeExecutorError on transport failure (timeout,
        non-zero exit from claude, stdout not valid JSON wrapper).
        """
```

Two implementations:
- `ClaudeScopeExecutor` — shells out to `claude -p
  --output-format json --append-system-prompt <framing>`, reads
  stdin for the payload, extracts `.result` via `json.loads`.
- `StubScopeExecutor(canned_result: str)` — returns `canned_result`
  verbatim. For unit tests and `--dry-run`.

**`ScopeDraft` TypedDict (matches the JSON schema the LLM must emit):**
```python
class RecommendedSkill(TypedDict):
    name: str
    reasoning: str
    default_cadence: str

class SkippedSkill(TypedDict):
    name: str
    reasoning: str

class CandidatePlugin(TypedDict):
    plugin: str
    marketplace: str
    reasoning: str

class Boundaries(TypedDict):
    allowed: list[str]
    forbidden: list[str]

class ScopeDraft(TypedDict):
    profile_prose: str
    recommended_skills: list[RecommendedSkill]
    skipped_skills: list[SkippedSkill]
    candidate_uncurated_plugins: list[CandidatePlugin]
    suggested_boundaries: Boundaries
```

**System-prompt framing** (`harness/prompts/scoping.v1.md`) — tells the
LLM:
- Role: "You are drafting an initial-scope.md for tokenman".
- Hard rules:
  - Any skill you recommend MUST appear in `<catalog>`.
  - If a plugin looks interesting but isn't in the catalog, put it in
    `candidate_uncurated_plugins` and explain why.
  - Boundaries default from each recommended skill's `SKILL.md` scope
    fields. If a skill's scope isn't declared, propose conservative
    defaults (README and top-level docs only).
- Response format: JSON matching `ScopeDraft` schema, no prose outside
  the JSON.

**Allowlist enforcement (`_enforce_allowlist`):**
After parsing the LLM's JSON, for each `recommended_skills[i]`, if
`i.name not in catalog`, move it to `candidate_uncurated_plugins` with
a synthetic `marketplace="unknown"` and `reasoning` = original
reasoning. This is the backstop; the prompt also states the rule.

**Retry policy:**
If `executor.run()` returns invalid JSON (doesn't parse, or doesn't
match schema), retry **once** with an appended system-prompt line:
"Your previous response was not valid JSON. Respond with JSON only,
matching the schema." If the second attempt also fails, raise
`ScopeDrafterError` and surface the raw output.

**Failure modes:**
- `ScopeExecutorError` propagated.
- `ScopeDrafterError` on post-retry JSON failure.

### 5.4 `harness/scope/__main__.py`

**CLI:**
```
python -m harness.scope [--repo .] [--refresh] [--claude-bin claude]
                       [--output-path .tokenman/initial-scope.md]
                       [--non-interactive] [--dry-run]
```

**Flags:**
- `--repo` — target repo directory (default `.`).
- `--refresh` — refresh marketplace caches before reading.
- `--claude-bin` — binary to invoke (default `claude`).
- `--output-path` — where to write; default
  `<repo>/.tokenman/initial-scope.md`.
- `--non-interactive` — skip the 4 user prompts, use empty answers.
  For tests and automation.
- `--dry-run` — substitute `StubScopeExecutor` returning a canned
  JSON fixture. No `claude` invocation. Useful for local iteration.

**Output behavior:**
- Interactive `accept / edit / abort`:
  - `accept` (default): write `output-path`, exit 0.
  - `edit`: open `$EDITOR` (fallback `vi`) on a tempfile
    preloaded with the rendered markdown; on save, write to
    `output-path`, exit 0. On abort-edit (empty save), same as
    `abort`.
  - `abort`: no file written, exit 1.
- `--non-interactive` implies `accept` automatically.

### 5.5 Rendering — `_render_markdown(draft) -> str`

Fixed template, string-formatted from a `ScopeDraft`. Sections in
fixed order:

```markdown
# Tokenman — Initial scope for <repo name>

_Generated by `python -m harness.scope` on <date>._
_Prompt version: <version>._

## Repo profile

<profile_prose>

**Facts:**
- Languages: <language mix>
- Files: <N>  Size: <M KB>
- Tests: <yes/no>  CI: <yes/no>  README: <yes/no>
- Dependency files: <list or "none">
- Commits in last 30 days: <N>

## Recommended skills

For each recommended_skills[i]:
- **<name>** — <reasoning>
  _Default cadence:_ <default_cadence>

(If empty: "No skills from the curated catalog match this repo yet.")

## Skills considered but skipped

(list from skipped_skills; empty → "None.")

## Candidates for catalog

The scoping pass found plugins that looked relevant but aren't in
`recommended-skills.yaml`. Tokenman will **not** install these. If you
want to use one, open a PR against `verky/tokenman` adding it to the
catalog.

(list from candidate_uncurated_plugins; empty → "None.")

## Suggested boundaries

### Allowed paths
(list; empty → "None declared — skills operate under their own SKILL.md scopes.")

### Forbidden paths
(list; empty → "None.")

## What's not here yet

Budget and schedule strategy are declared by the user in
`.tokenman/tokenman.yaml`; automated suggestion lands with Phase 2
(spec §7). Expected PR volume estimation lands with Phase 4 once the
ledger has history to draw on. This scope file is the seed for that
eventual configuration.
```

### 5.6 Empty-registry behavior

If `marketplace.list_plugins()` returns `[]`:
- Still proceed with the LLM call — the catalog is enough on its own
  for `recommended_skills` and `skipped_skills`.
- `candidate_uncurated_plugins` will be `[]` (nothing to discover).
- Add a one-line note in the rendered markdown under the "Candidates
  for catalog" header: "_No marketplaces configured. Run `claude
  plugins marketplace add <source>` to enable discovery._"

## 6. Prompt contract

`harness/prompts/scoping.v1.md` is the system prompt. The user payload
(passed on stdin to `claude -p`) is a single JSON document:

```json
{
  "repo_profile": { ... },
  "user_answers": {
    "purpose": "...",
    "concern": "...",
    "off_limits": "...",
    "other": "..."
  },
  "catalog": { ... },     // parsed recommended-skills.yaml
  "marketplace_plugins": [ ... ]
}
```

The prompt must make these rules explicit:
1. Output valid JSON matching the `ScopeDraft` schema.
2. Only recommend skills whose `name` is a key in `catalog`.
3. Uncurated plugins go in `candidate_uncurated_plugins`, not
   `recommended_skills`.
4. Boundaries derived from each recommended skill's `SKILL.md` Scope
   section (included in the payload — see §6.1); conservative
   README-only defaults if not declared.
5. No prose outside the JSON document.

### 6.1 SKILL.md inclusion in payload

For each catalog entry whose `source` is a local path (`./...`),
`scope_drafter` reads that skill's `SKILL.md` from disk and attaches
its full text in the payload under `catalog[<name>].skill_md`.
Non-local sources (git URLs) are skipped in Phase 1.3 — their
`skill_md` field is `null` and the LLM must fall back to conservative
defaults for boundaries. Fetching remote SKILL.md files lands with
Phase 1.4's install flow.

## 7. Deferred sections

Spec §6.3 lists sections that are **not** produced by Phase 1.3:
- **Suggested budget** — Phase 2 introduces `pricing.yaml` and
  subscription-tier calibration.
- **Suggested schedule strategy** — Phase 2 introduces `adaptive`.
  Through Phase 1, consumers default to fixed weekly and the library
  stays `manual` until Phase 3 (spec §7, §12).
- **Expected PR volume** — needs ledger history; Phase 4.

The "What's not here yet" section of the rendered markdown documents
these deferrals explicitly so users understand the gap.

## 8. Error handling

| Failure | Response |
|---|---|
| Not a git repo | Hard error before any LLM call; exit 2. |
| `recommended-skills.yaml` missing | Hard error; exit 2. |
| No marketplaces configured | Proceed with empty registry, note in output. |
| `marketplace.json` malformed | Skip that manifest, warn, continue. |
| `claude -p` exits non-zero | Exit 3, print stderr, no file written. |
| `claude -p` output not JSON | Retry once; if still fails, exit 3. |
| `ScopeDraft` schema mismatch | Same as invalid JSON — retry once. |
| User picks `abort` | Exit 1, no file written. |
| `$EDITOR` exits with saved-empty file | Treat as abort. |

## 9. Testing strategy

Following the Phase 1.2b split between fast CI tests and opt-in live
tests.

### 9.1 Unit tests (fast, always run)

- `test_repo_profile.py` — create a tiny `git init`-ed tmpdir with
  known files, assert each field of `RepoProfile`. Covers:
  happy path, empty repo, missing README, polyglot repo.
- `test_marketplace.py` — build a fake `marketplaces/` tree with two
  manifests (one well-formed, one malformed), assert flattening and
  malformed-skipped behavior.
- `test_scope_drafter.py`:
  - Happy path with `StubScopeExecutor` returning valid JSON; assert
    `ScopeDraft` fields.
  - Allowlist enforcement: stub returns `recommended_skills` with a
    name not in catalog; assert it's demoted to
    `candidate_uncurated_plugins`.
  - Retry on invalid JSON: stub returns `"not json"` once, valid JSON
    the second time; assert success with one retry.
  - Retry exhaustion: stub returns invalid JSON twice;
    assert `ScopeDrafterError`.

### 9.2 CLI integration test

- `test_scope_cli.py` — invoke `python -m harness.scope --dry-run
  --non-interactive --repo <fixture>` and assert the rendered
  markdown contains the expected section headers and at least one
  recommended skill.

### 9.3 Live test (opt-in)

- `test_scope_live.py` — gated by `TOKENMAN_LIVE=1`. Invokes real
  `claude -p` against `tests/fixtures/tiny-python-repo/` with
  `--non-interactive`. Asserts output parses, contains README section,
  and finishes in <60s. Same harness as
  `test_real_skill_integration.py` from 1.2b.

### 9.4 Fixtures

- `tests/fixtures/tiny-python-repo/` — **already exists** from earlier
  phases. Reused by `test_repo_profile.py`. If any field ends up
  needing content the existing fixture doesn't provide, extend the
  fixture rather than spawning a new one.
- `tests/fixtures/fake-marketplaces/` — **new.** Two marketplace
  manifests (one well-formed with 3 plugins, one malformed JSON).
- `tests/fixtures/scope-captures/minimal.json` — **new.** Canned LLM
  response for `--dry-run`.

## 10. Open questions resolved by this design

- **Module placement:** `python -m harness.scope`, sibling to
  `harness.run`. Rejected: adding a subcommand to
  `harness.run` would entangle discovery with execution.
- **LLM-assisted vs fully deterministic:** LLM-assisted (one call).
  Rejected: rules-engine approach, because the prose (why this skill,
  why not this one) is the product; and the catalog will grow.
- **Interactive vs one-shot:** Interactive (4 prompts). Rejected:
  pure one-shot; the repo-purpose signal from the user meaningfully
  shapes recommendations and is cheap to ask.
- **Registry model:** discovery from local marketplace manifests,
  allowlist from `recommended-skills.yaml`. Rejected: registry
  replaces the catalog (loses §5.1 pinning guarantees); Claude-Code
  plugins map 1:1 to skills (they don't — a plugin may contain 0..n
  skills, which is why the output names them "plugins" not "skills"
  under "Candidates for catalog").

## 11. Implementation sketch — file inventory

New files:
- `harness/scope/__init__.py`
- `harness/scope/__main__.py`
- `harness/lib/repo_profile.py`
- `harness/lib/marketplace.py`
- `harness/lib/scope_drafter.py`
- `harness/prompts/scoping.v1.md`
- `tests/test_repo_profile.py`
- `tests/test_marketplace.py`
- `tests/test_scope_drafter.py`
- `tests/test_scope_cli.py`
- `tests/test_scope_live.py`
- `tests/fixtures/fake-marketplaces/<name>/.claude-plugin/marketplace.json` (×2)
- `tests/fixtures/scope-captures/minimal.json`

Reused files:
- `tests/fixtures/tiny-python-repo/` — already exists; used as-is
  by `test_repo_profile.py` and the live test.

Modified files:
- `README.md` — one-line mention under "Usage" that `python -m
  harness.scope` exists.
- `CONTRIBUTING.md` — note about the scoping flow if the project
  section warrants it.

Not touched:
- `harness/lib/runner.py`, `harness/run/__main__.py` — unchanged.
- `recommended-skills.yaml` — unchanged.
- `.tokenman/` runtime state — unchanged (PAUSE stays).

## 12. Success criteria

- `python -m harness.scope --dry-run --non-interactive --repo
  tests/fixtures/tiny-python-repo` exits 0 and writes a markdown
  file with all expected sections.
- Live test passes against a real `claude -p` in <60s.
- Recommending a skill not in `recommended-skills.yaml` is impossible
  by construction (the allowlist backstop demotes it).
- Unit tests ≤2s total; full non-live suite still under the budget
  established by 1.2b.
