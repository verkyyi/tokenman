# Tokenman MVP Spec

## Summary

Tokenman is a thin control layer that runs inside GitHub Actions and
wraps the official Claude Code Action to make recurring engineering work
more scoped, repeatable, auditable, and safe.

The MVP is intentionally narrow:

- one job: `docs_maintainer`
- one runtime: GitHub Actions
- one trust boundary: explicit `read_paths` and `write_paths`
- three outcomes: pull request, issue, or no-op

Claude provides the coding intelligence. Tokenman provides the job
shape, prompt shaping, scope enforcement, output routing, and guardrails.

## Product goal

Enable maintainers to assign a recurring docs-maintenance responsibility
to Claude inside GitHub while ensuring the work stays inside a declared
boundary.

Initial promise:

> Automatically maintain docs for a defined part of the repo, using
> Claude, with strict path boundaries and predictable outputs.

## Non-goals

The MVP is not:

- a general-purpose coding agent
- a multi-agent orchestration platform
- a custom runtime outside GitHub Actions
- a full policy engine
- a replacement for Claude Code Action

It also does not support:

- arbitrary code-maintenance jobs
- autonomous production-code edits outside the declared write scope
- multiple job types at launch

## Core concept

Claude is the execution engine that:

- reads context
- reasons about repo changes
- edits files
- returns a structured result

Tokenman is the harness that:

- decides when Claude runs
- shapes Claude's task into a fixed job
- enforces read/write boundaries
- validates the resulting diff
- routes the result into PR, issue, or no-op

## MVP job

### `docs_maintainer`

Responsibility:

- keep documentation aligned with recent code changes for a declared repo area

Allowed behavior:

- inspect recent code changes
- inspect in-scope documentation targets
- update docs within allowed write paths
- open a PR when confidence is high
- open an issue when confidence is low
- no-op when no relevant drift is found

Disallowed behavior:

- changing production code
- changing files outside declared write scope
- broad repo rewrites
- changing workflows or config files unless explicitly allowed

## Runtime model

GitHub Actions is the only runtime in the MVP.

That gives Tokenman:

- native triggers
- native permissions
- native logs
- native repo context
- native review surfaces through PRs and issues

Tokenman should feel GitHub-native, not like a separate platform.

## Integration model

Users install Tokenman through a workflow file that:

- checks out the repo
- invokes Tokenman
- passes scope settings
- uses GitHub event triggers

Internal execution flow:

1. Tokenman receives workflow inputs.
2. Tokenman gathers repo and event context.
3. Tokenman builds a constrained prompt.
4. Tokenman invokes the official Claude Code Action.
5. Tokenman validates resulting changes.
6. Tokenman routes the result into PR, issue, or no-op.

## Inputs

Required:

- `github_token`
- `read_paths`
- `write_paths`

Optional:

- `job_type` default `docs_maintainer`
- `on_high_confidence` default `pull_request`
- `on_low_confidence` default `issue`

Example:

```yaml
with:
  github_token: ${{ secrets.GITHUB_TOKEN }}
  read_paths: |
    services/payments/**
    openapi/payments.yaml
  write_paths: |
    docs/payments/**
  on_high_confidence: pull_request
  on_low_confidence: issue
```

## Scope model

Scope is the core control mechanism.

- Read scope: files Claude may inspect as context
- Write scope: files Claude may modify

Enforcement rule:

- any changed file outside declared `write_paths` causes the run to fail safe

Failure-safe behavior:

- reject the change set
- do not open a PR
- open an issue when configured to explain the violation

## Prompt model

Tokenman does not expose raw prompt-writing as the main UX. It generates
a structured prompt around the fixed job.

The generated prompt must include:

- job identity: docs maintainer
- recent repo changes
- read scope
- write scope
- allowed and disallowed actions
- expected output modes

Prompt principles:

- narrow
- surgical
- deterministic
- role-based, not open-ended

## Output model

Tokenman supports exactly three outcomes:

### Pull request

Used when:

- relevant doc drift exists
- edits stay in scope
- confidence is high enough

### Issue

Used when:

- likely doc drift exists
- confidence is too low for direct edits
- scope was violated
- validation failed

### No-op

Used when:

- no doc-relevant change is detected
- or docs already appear aligned

## Validation rules

Required validations:

- all modified files are inside `write_paths`
- no source-code files were changed for docs-only jobs
- the repo has an actual diff before PR creation

Failure handling:

- do not create PR
- create issue or no-op with the failure reason
- include a run summary in GitHub Actions output

## GitHub artifacts

### PR behavior

When opening a PR, Tokenman should:

- create a branch
- commit only the in-scope changes
- open a PR with a short structured summary

### Issue behavior

When opening an issue, Tokenman should summarize:

- what changed in code
- why docs may be stale
- why no PR was created

### No-op behavior

No-op runs should still emit a clear workflow summary and ledger entry.

## Repo shape

The user-facing MVP shape is:

```text
tokenman/
├─ action.yml
├─ entrypoint.sh
├─ prompt.md
└─ README.md
```

The `harness/` package remains as internal implementation code for the
action runtime.

## Success criteria

The MVP succeeds if a maintainer can:

1. install Tokenman in a repo with one workflow file
2. define allowed read and write paths
3. trigger a run on code changes
4. get a docs PR when confidence is high
5. trust that Tokenman will not silently modify out-of-scope files

The product success signal is:

> I can let this maintain docs in this lane without worrying it will
> wander across the repo.
