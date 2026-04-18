# Tokenman

Open-source toolset — skills + workflows — that installs into any repo
to enable **async AI maintenance via pull requests**. Claude Code
(`claude -p` inside GitHub Actions) runs small, well-scoped skills on a
weekly schedule; each run opens a PR you review and merge. PRs only,
never direct commits. No hosted backend.

> **This repo is the library.** The skills and workflows here are the
> source of truth. You don't run tokenman on this repo — you install
> tokenman into your own repo.

## Library vs consumer repo

Tokenman splits into two roles, declared in `.tokenman/tokenman.yaml`:

| Role | What it is | Declared by |
| --- | --- | --- |
| `library` | Source of truth for distributable skills + workflows. Does NOT run tokenman on itself. | `role: library` |
| `consumer` | Any repo that has tokenman installed. Runs the workflows on a cron. | `role: consumer` |

Because consumer repos run the workflows from `.github/workflows/` and
Claude Code looks for skills in `.claude/skills/`, the **library** repo
keeps those runtime paths deliberately empty. Library distributables
live in `/skills/` and `/workflows/`. Consumer installs copy across:

```
library  (this repo)                   consumer  (your repo)
├── skills/<name>/SKILL.md          →  .claude/skills/<name>/SKILL.md
├── workflows/<name>.yml            →  .github/workflows/<name>.yml
└── .tokenman/tokenman.yaml            .tokenman/tokenman.yaml
   (role: library)                     (role: consumer)
```

This separation is why you won't find a
`.github/workflows/tokenman-run.yml` in this repo. If you did,
tokenman would run on itself, which it doesn't.

## Current library surface

| Skill | Language | What it does |
| --- | --- | --- |
| `dead-code-cleanup` | Python | Removes provably unused imports and unreachable code. Subtractive diffs only, tests must pass before and after, under 100 lines per PR. |

More skills will land as they prove their value. Start small.

> Legacy skills (`adversarial-review`, `harness`, `session-protocol`,
> `feedback-intake`, `github-roadmap-planning`, `github-task-*`, plus
> loose `.md` files) are still present in `/skills/` from an earlier
> incarnation of this repo. They are **not** part of the current
> library surface and have not been re-validated against tokenman's
> `name` / `version` / `origin: local` frontmatter contract.

## Install into a consumer repo

v0.1.0 has no installer — you copy the files manually. From the root of
your consumer repo:

```bash
# 1. Clone the library somewhere convenient
git clone https://github.com/verkyyi/tokenman.git /tmp/tokenman

# 2. Copy the skill(s) you want
mkdir -p .claude/skills
cp -r /tmp/tokenman/skills/dead-code-cleanup .claude/skills/

# 3. Copy the workflow
mkdir -p .github/workflows
cp /tmp/tokenman/workflows/tokenman-run.yml .github/workflows/

# 4. Declare your repo's role
mkdir -p .tokenman
cat > .tokenman/tokenman.yaml <<'EOF'
role: consumer
installed:
  - dead-code-cleanup
EOF

# 5. (Optional) Add the status script
mkdir -p scripts
cp /tmp/tokenman/scripts/status.sh scripts/
chmod +x scripts/status.sh

# 6. Commit and push
git add .claude/skills/dead-code-cleanup \
        .github/workflows/tokenman-run.yml \
        .tokenman/tokenman.yaml \
        scripts/status.sh
git commit -m "Install tokenman dead-code-cleanup"
git push
```

Then in your repo's GitHub settings:

1. **Secrets → Actions → New repository secret**: add
   `CLAUDE_CODE_OAUTH_TOKEN` (from
   [console.anthropic.com](https://console.anthropic.com) →
   Claude Code → OAuth token).
2. **Actions → General → Workflow permissions**: enable "Read and
   write permissions" and "Allow GitHub Actions to create and approve
   pull requests".
3. If `main` is protected: add a bypass rule so tokenman's
   `GITHUB_TOKEN` can push ledger entries. Tokenman writes
   `.tokenman/ledger.jsonl` directly to main — that's the one
   exception to the PRs-only rule, because the ledger is bookkeeping,
   not code.

The workflow runs on its schedule (weekly, Monday 12:00 UTC by
default). You can also trigger it manually from the Actions tab, with
a `dry_run` option if you want the skill to verify without opening a
PR.

## Reading the ledger

Every run appends one JSON line to `.tokenman/ledger.jsonl`:

```json
{"run_id":"42-1","ts":"2026-04-22T12:00:17Z","skill":"dead-code-cleanup","status":"success","reason":"","pr_number":17,"files_changed":2,"lines_deleted":7,"input_tokens":12345,"output_tokens":678,"duration_s":42}
```

| Field | Meaning |
| --- | --- |
| `run_id` | `<github.run_id>-<attempt>` — traces back to the Actions run. |
| `ts` | ISO 8601 UTC timestamp, run start. |
| `skill` | Skill name. |
| `status` | `success`, `skip`, `abort`, `dry-run`, or `error`. |
| `reason` | Short string; populated for skip/abort (e.g. `cooldown`, `pr-already-open`, `nothing-to-do`, `baseline-failed`). |
| `pr_number` | Number of the PR opened, or `null`. |
| `files_changed` | Count of files touched. |
| `lines_deleted` | Count of lines removed (subtractive diff only, per skill contract). |
| `input_tokens` / `output_tokens` | Claude API token counts for the run. |
| `duration_s` | Wall-clock seconds the skill took. |

### Quick status

If you copied `scripts/status.sh`, run it from the consumer repo root:

```
$ bash scripts/status.sh
== tokenman status ==
ledger  : .tokenman/ledger.jsonl
entries : 14

== last 10 runs (newest first) ==
timestamp              skill                    status     reason                       tokens
---------------------- ------------------------ ---------- ---------------------- ------------
2026-04-22T12:00:17Z   dead-code-cleanup        success                                  13023
2026-04-15T12:00:05Z   dead-code-cleanup        skip       pr-already-open                   0
...

== 7-day totals (since 2026-04-15T12:00:00Z) ==
runs=2  prs_opened=1  success=1  skip=1  abort=0  tokens=13023  lines_deleted=7

== per-skill breakdown (all time) ==
- dead-code-cleanup:  runs=14  success=6  skip=5  abort=3  prs=6  tokens=87340  lines_deleted=42
```

### Direct jq queries

```bash
# PRs opened in the last 30 days
jq -c 'select(.pr_number != null and
              .ts >= (now - 30*86400 | strftime("%Y-%m-%dT%H:%M:%SZ")))' \
  .tokenman/ledger.jsonl

# Total tokens consumed, all time, for a given skill
jq -s 'map(select(.skill == "dead-code-cleanup"))
       | map(.input_tokens + .output_tokens) | add' \
  .tokenman/ledger.jsonl

# All abort reasons
jq -r 'select(.status == "abort") | "\(.ts)  \(.reason)"' \
  .tokenman/ledger.jsonl
```

## This repo does not run tokenman on itself

Tokenman v0.1.0 is a library, not a self-evolving system. The library
repo deliberately has no `.github/workflows/tokenman-run.yml` and
declares `role: library`. If that ever changes, it will be a
deliberate, reviewed decision documented here.

## Tuning

All tunable limits live in the `env:` block at the top of
`.github/workflows/tokenman-run.yml` in the consumer repo:

| Env var | Default | Effect |
| --- | --- | --- |
| `TOKENMAN_PR_MAX_AGE_DAYS` | `14` | Auto-close tokenman PRs older than this with a comment. |
| `TOKENMAN_RUN_COOLDOWN_HOURS` | `24` | Minimum time between successful runs of a skill. |
| `TOKENMAN_TOKEN_BUDGET_7D` | `0` | Rolling 7-day token cap. `0` means count only, no enforcement. |

The cron schedule (`'0 12 * * 1'` — Monday 12:00 UTC) is in the
`on.schedule` block of the same workflow; edit there.

## Status

**v0.1.0.** Single skill (`dead-code-cleanup`, Python). No installer.
PR-only maintenance diffs (ledger is the one direct-to-main exception).
Manual library-to-consumer copy. Breaking changes are likely as the
ergonomics shake out.

## License

MIT — see [LICENSE](./LICENSE).
