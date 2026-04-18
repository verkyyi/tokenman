# Phase 1.5 — Skill install flow

**Status:** Design (approved for planning)
**Date:** 2026-04-18
**Spec references:** docs/spec.md §5.2 (skill installation), §6.2 (`/tokenman init`), §3.4 (consumer layout)
**Supersedes:** none
**Follows:** Phase 1.4 (`docs/superpowers/specs/2026-04-18-phase-1-4-onboarding-mode-design.md`)

## 1. Goal

Ship the "fetch skills into the consumer's `.claude/skills/`" step of the install journey. After 1.5, a real consumer flow becomes:

```
python -m harness.scope       # writes .tokenman/initial-scope.md
python -m harness.install     # populates .claude/skills/ from recommended-skills.yaml
python -m harness.onboard     # runs every enabled skill once, opens PRs
```

The in-tree `skills/readme-maintainer/` is extracted to a standalone repo so install is exercised against a real remote, not only fixtures.

## 2. Non-goals

- Private-repo authentication. Catalog entries are public https URLs (or local `./` paths for tests / dogfood transition).
- `--upgrade` flow (fetching newer refs than pinned). Install is strictly "install the pinned version."
- Parallel clones. Sequential is fine for typical 3–5 skills.
- Auto-install from inside `scope` or `onboard`. Those continue to error loudly when a skill is missing; users re-run install explicitly.

## 3. User-visible surface

### 3.1 New CLI: `python -m harness.install`

```
python -m harness.install
  [--repo .]                # consumer repo (target of the install)
  [--config-path PATH]      # default: <repo>/.tokenman/tokenman.yaml
  [--skill NAME ...]        # repeatable; overrides config skills list
  [--force]                 # rm -rf drifted targets before reinstalling
  [--dry-run]               # no filesystem writes; print what would happen
  [--non-interactive]       # reserved; install has no prompts today
```

Behavior:
- Resolves the skill set the same way `onboard` does: `--skill` flags override `.tokenman/tokenman.yaml`'s `skills:` list. Empty set → exit 2 with a hint pointing at `harness.scope` / `--skill`.
- For each skill, delegates to `installer.install_skill(...)`.
- Prints one line per skill: `installed | unchanged | errored(<reason>)`.
- Per-skill errors do NOT abort the batch. All skills attempted.
- Exit 0 if every skill resolves to `installed` or `unchanged`; non-zero otherwise (code = max exit code seen).

### 3.2 Catalog schema changes

`recommended-skills.yaml` entries:

```yaml
readme-maintainer:
  source: https://github.com/verky/readme-maintainer-skill   # https URL or ./local-path
  version: v0.1.0                                            # tag or sha; documented "prefer tags"
  # path: skill/                                             # OPTIONAL — subdir holding SKILL.md
  tier: starter
  blast_radius: low
  typical_tokens_per_run: 15000
  description: Keeps README aligned with actual repo contents.
  default_cadence: on-change
  evaluator_strictness: medium
```

- `source:` accepts either a `./relative-path` (resolved against the tokenman library root) or an `https://…` git URL.
- `version:` accepts a tag (preferred — human-readable) or a full sha. No semver ranges.
- `path:` is new and optional; if present, only that subdir of the cloned repo is copied into `.claude/skills/<name>/`. Default: copy the whole tree (minus `.git/`).

No schema version bump — additive and backward compatible.

### 3.3 Installed layout

```
.claude/skills/
  readme-maintainer/
    SKILL.md
    … skill-authored files …
    .tokenman-skill-lock     # written by tokenman; committed alongside skill files
```

`.tokenman-skill-lock` contents:

```json
{
  "source": "https://github.com/verky/readme-maintainer-skill",
  "version": "v0.1.0",
  "resolved_sha": "abc123…",
  "installed_at": "2026-04-18T12:00:00Z"
}
```

The lock is committed to the consumer repo. `git diff` surfaces drift the same way it surfaces any other file change, keeping with the "files are the only medium" principle.

## 4. Architecture

### 4.1 New module: `harness/lib/installer.py` (pure logic)

```python
@dataclass(frozen=True)
class InstallResult:
    skill_name: str
    status: Literal["installed", "unchanged", "errored"]
    resolved_sha: str | None
    message: str                  # human-readable one-liner
    exit_code: int                # 0, 3, 4, 5 (see §6)

def install_skill(
    *,
    skill_name: str,
    catalog_entry: dict,
    target_dir: Path,
    tokenman_root: Path,          # for resolving ./local-path sources
    force: bool = False,
    now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    git_runner: GitRunner | None = None,   # injectable for tests
) -> InstallResult: ...
```

`GitRunner` is a thin wrapper (not a class hierarchy) around `subprocess.run(["git", …])` following the `harness/lib/git_ops.py` precedent. Default implementation shells out to `git`; tests inject a variant that runs against local bare repos / git bundles.

### 4.2 New CLI: `harness/install/__main__.py`

Glue only: argparse, config load, skill resolution, loop over `install_skill`, aggregate results, print summary, pick final exit code. Pattern mirrors `harness/onboard/__main__.py`.

### 4.3 Extract shared catalog helpers: `harness/lib/catalog.py`

`_tokenman_root`, `_load_catalog`, and `_resolve_skill_dir` are currently duplicated across `harness/scope/__main__.py` and `harness/onboard/__main__.py`. Phase 1.5 adds a third caller; extraction is earned.

New module API:

```python
def tokenman_root() -> Path: ...
def load_catalog(root: Path) -> dict[str, dict]: ...

class SkillResolutionError(Exception): ...

def resolve_skill_dir(
    *,
    skill_name: str,
    catalog: dict,
    tokenman_root: Path,
    consumer_repo: Path,
) -> Path:
    """
    Local source (./…)   → <tokenman_root>/<path>
    Remote source (http) → <consumer_repo>/.claude/skills/<skill_name>/
                           (raises SkillResolutionError if not yet installed)
    """
```

`scope/__main__.py` and `onboard/__main__.py` switch to these helpers and convert `SkillResolutionError` → exit 2 at the boundary. The `SystemExit`-based error path the handoff flagged as ugly is replaced in passing.

### 4.4 Updated guards in scope + onboard

- Drop the "remote skill sources land in Phase 1.5" exit-2.
- On `https://` source with no `.claude/skills/<name>/` present, error: `"skill '<name>' not installed; run 'python -m harness.install' first"`. Still exit 2.
- Local `./` sources keep current behavior.
- `harness/lib/scope_drafter.py::_load_skill_md` updated to handle remote sources. Scope runs *before* install in the consumer journey (§1), so at scope time `.claude/skills/` is typically empty for remote entries. Behavior:
  - Local `./` source → read from `<tokenman_root>/<path>/SKILL.md` (today's behavior, unchanged).
  - Remote source, `.claude/skills/<name>/SKILL.md` present → read from there (re-runs of scope after install pick it up).
  - Remote source, not yet installed → `skill_md = None`.
- The existing scoping prompt already tolerates null `skill_md` (`harness/prompts/scoping.v1.md` lines 65-67: "If a skill's `skill_md` is null or has no Scope section, fall back to the catalog description"). Degraded-mode scoping for un-installed remote skills is acceptable for 1.5; pre-fetching SKILL.md into the catalog is a §9 carry.

### 4.5 readme-maintainer extraction

Three commits on the `phase-1-5` branch:

1. **Extract.** Create new public repo `verky/readme-maintainer-skill`. Seed with the current contents of `skills/readme-maintainer/`. Tag `v0.1.0`. (Done outside the tokenman repo; the phase-1-5 branch doesn't carry that commit.)
2. **Flip catalog.** Edit `recommended-skills.yaml` → `source: https://github.com/verky/readme-maintainer-skill`, `version: v0.1.0`. Remove the TEMPORARY comment.
3. **Prune in-tree copy.** Delete `skills/readme-maintainer/` and `skills/README.md`'s bootstrap note. Drop the skill's path from `.tokenman/CLAUDE.md`'s forbidden list.

Commits 2 and 3 land on the `phase-1-5` branch. Commit 1 happens in the new repo and leaves only the tag as a trace.

## 5. Data flow — install one remote skill

```
1. Load catalog; look up entry by <skill_name>.
2. target = <consumer_repo>/.claude/skills/<skill_name>/
3. If source starts with "./":
     resolved = <tokenman_root>/<path>
     if resolved/SKILL.md missing:
         return status=errored, exit_code=4,
                message="local source has no SKILL.md at <path>"
     return status=unchanged, resolved_sha=None
     # Local sources are never materialized into .claude/skills/.
     # They're installed-in-place — scope/onboard/run reach into
     # <tokenman_root>/<path> directly. No lock file written.
4. Else (https source):
   a. tmpdir = mkdtemp
   b. git clone --quiet <source> <tmpdir>
   c. git -C <tmpdir> checkout --quiet <version>
   d. resolved_sha = git -C <tmpdir> rev-parse HEAD
   e. If target exists:
        try read <target>/.tokenman-skill-lock
        if lock.resolved_sha == resolved_sha → no-op, rm tmpdir,
                                              return status=unchanged
        else if not --force                 → return status=errored,
                                              exit_code=5,
                                              message="drifted; re-run with --force"
        else                                → rm -rf target
   f. If catalog entry has path:
        source_tree = tmpdir / <path>
      else:
        source_tree = tmpdir
   g. Copy source_tree → target, excluding any .git/ subtree.
   h. If target/SKILL.md does not exist:
        rm -rf target
        return status=errored, exit_code=4,
               message="SKILL.md missing after checkout"
   i. Write target/.tokenman-skill-lock (source, version, resolved_sha,
      installed_at=now().isoformat()+"Z").
   j. rm -rf tmpdir
   k. return status=installed, resolved_sha=...
```

## 6. Error handling (exit codes)

At the CLI level, the final exit code = max per-skill exit code. Per-skill codes:

| Code | Meaning                                             | Filesystem effect |
|------|-----------------------------------------------------|-------------------|
| 0    | installed or unchanged                              | target populated  |
| 2    | config error (unknown skill, missing source/version) before any skill ran | none |
| 3    | git clone/checkout failure, ref not found           | partial rolled back |
| 4    | verification error (SKILL.md missing post-checkout) | partial rolled back |
| 5    | drifted target, `--force` not passed                | target untouched  |

Per-skill errors do NOT abort the batch. All skills attempted; the summary line for each records its outcome.

## 7. Testing

### 7.1 Fixtures

- `tests/fixtures/remote-skills/fake-skill/` — plain source tree (SKILL.md + a one-line script). Checked into the repo as-is.
- `tests/conftest.py` helper `build_local_git_repo(source_tree, tag="v0.1.0") -> Path` — `git init --bare` in a tmpdir, populate, tag, return path. Used as the `source:` URL in test catalogs. No binary bundles checked in.

### 7.2 Unit tests — `tests/test_installer.py`

- Happy path (remote): `status=installed`, lock written, SKILL.md present.
- Happy path (local `./`): `status=unchanged`, no lock written, resolved in place.
- Re-install when lock matches: `status=unchanged`, no mutation.
- Drifted target without `--force`: `status=errored`, `exit_code=5`, target untouched.
- Drifted target with `--force`: `status=installed`, target rewritten, new lock.
- Bad ref (tag doesn't exist): `status=errored`, `exit_code=3`, partial cleaned.
- SKILL.md missing after checkout: `status=errored`, `exit_code=4`, partial cleaned.
- Optional `path:` subdir: copies only that subtree.

### 7.3 Unit tests — `tests/test_catalog.py`

New, covering the extracted `harness/lib/catalog.py`:
- `load_catalog` — happy path, non-mapping file raises.
- `resolve_skill_dir` — local source, remote installed, remote not installed (raises `SkillResolutionError`), unknown skill name (raises).

### 7.4 CLI smoke — `tests/test_install_cli.py`

- `python -m harness.install --skill fake-skill --repo <tmpdir>` against the local-bundle fixture. Verifies target + lock written; verifies summary line; verifies exit 0 on second run (`unchanged`).
- Empty skill set exits 2 with the standard hint.

### 7.5 Onboard / scope coverage

- `tests/test_onboard_errors_when_skill_not_installed.py` — catalog has a remote source; `.claude/skills/<name>/` absent → onboard exits 2 with "run install first" message.
- Existing scope/onboard tests updated: drop the "remote sources land in 1.5" exit-2 assertions; replace with the new install-first assertion where relevant.
- `test_workflow_template.py` — no changes expected; workflow install step is still a TODO (see §10).

### 7.6 Opt-in live test — `tests/test_install_live.py`

Gated on `TOKENMAN_LIVE=1`. Clones real `verky/readme-maintainer-skill` at tag `v0.1.0` into a tmpdir consumer; verifies install, lock, and idempotent re-run. Mirrors Phase 1.4's `test_onboard_live.py` pattern.

### 7.7 `_seed_git_repo` conftest extraction

Handoff flagged this as deferred until the next fixture-shape change. 1.5 introduces a new helper (`build_local_git_repo`) and reuses `_seed_git_repo` in install-adjacent tests. Extract both to `tests/conftest.py` as part of this phase rather than duplicating into a sixth file.

## 8. Ordering on the phase-1-5 branch

Suggested commit sequence (each green, each a reviewable unit):

1. `refactor(harness): extract harness/lib/catalog.py shared helpers` — scope and onboard switch to the shared module; no behavior change; `SkillResolutionError` replaces `SystemExit`.
2. `feat(install): add harness.lib.installer with remote + local support` — the pure module + its unit tests. No CLI yet.
3. `feat(install): add python -m harness.install CLI` — glue module + CLI tests + conftest helper.
4. `refactor(scope,onboard): drop 'remote sources land in 1.5' guard` — replace with "not installed; run install first" path; update tests.
5. `feat(catalog): flip readme-maintainer to remote source` — `recommended-skills.yaml` points at `github.com/verky/readme-maintainer-skill` v0.1.0. Live test begins passing.
6. `chore: prune in-tree skills/readme-maintainer/` — delete directory; update `skills/README.md`; drop forbidden-list entry in `.tokenman/CLAUDE.md`.
7. `test(install): add opt-in live install test` — gated on `TOKENMAN_LIVE=1`.
8. `docs: README + handoff refresh for Phase 1.5` — reflect the three-step consumer journey.

## 9. Forward-facing carries (still open after 1.5)

- Workflow template's `claude` install step still echoes TODO + `exit 1`. Decide command (likely `npm i -g @anthropic-ai/claude-code`) and drop `exit 1`. Not a 1.5 blocker.
- `tests/fixtures/claude-captures/readme-maintainer.json` is still synthetic. Refresh once live captures are easy.
- `GhPROpener` still hasn't been exercised against real GitHub end-to-end. Manual `workflow_dispatch` against a throwaway consumer repo is the validation step; carries into whichever phase first needs it.
- `--upgrade` flow, private-repo auth, and parallel clones are explicit non-goals (§2).
- **Pre-fetched SKILL.md in the catalog.** Scope runs before install, so for remote catalog entries it has no local SKILL.md to enrich the scoping prompt (§4.4). The prompt tolerates null skill_md, so scoping works but loses the per-skill Scope/Shape detail. A future phase should pre-fetch SKILL.md for each remote catalog entry into the tokenman library repo (e.g. `catalog-cache/<name>-<version>/SKILL.md`), keeping the catalog self-contained for scoping while install still fetches the full skill tree. Not 1.5.

## 10. Risks

- **Subtree copy edge cases.** Skill repos with unexpected file types (symlinks, large binaries) could surprise the copy step. Mitigation: use `shutil.copytree(..., symlinks=True)` and document that skill authors should keep repos lean. Acceptable risk for Phase 1.5 — we control the only remote skill today.
- **Lock drift from human edits.** A user editing files under `.claude/skills/<name>/` won't change `.tokenman-skill-lock`. Re-running install treats that as unchanged (sha matches), silently preserving the drift. Accepted: the skill's contents are in git; `git diff` is the source of truth. Not the installer's job to detect user edits.
- **Commit ordering tangles.** Commits 5 (flip catalog) and 6 (prune in-tree) must both land for the tokenman repo to be self-consistent. Mitigation: land them together in one push; CI on the `phase-1-5` branch runs once after both.
- **First-remote-skill failure mode.** If `verky/readme-maintainer-skill` is unreachable or the tag is missing when commit 5 lands, the live test and any consumer install break immediately. Mitigation: extract + tag the repo before commit 2 (even though the branch doesn't reference it until commit 5). Verify a dry-run `python -m harness.install --skill readme-maintainer` from a scratch checkout at commit 5 before merging.
