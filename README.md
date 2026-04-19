# Tokenman

Tokenman is a thin control layer for Claude inside GitHub Actions.

The MVP is intentionally narrow:

- one job: `docs_maintainer`
- one runtime: GitHub Actions
- one trust boundary: explicit `read_paths` and `write_paths`
- three outcomes: pull request, issue, or no-op

Claude does the reasoning and editing. Tokenman supplies the fixed job,
prompt shaping, scope enforcement, output routing, run artifacts, and
append-only history.

## MVP contract

The public surface is the GitHub Action at [action.yml](action.yml).
It accepts:

- `github_token`
- `read_paths`
- `write_paths`
- `job_type` default `docs_maintainer`
- `on_high_confidence` default `pull_request`
- `on_low_confidence` default `issue`

Tokenman runs Claude against the checked-out repo, validates the diff,
and then:

- opens a PR when the edit is in-scope
- opens an issue when the run is blocked or confidence is low
- records a no-op when nothing useful changed

## Example

```yaml
name: Tokenman Docs Maintainer

on:
  push:
    branches:
      - main
    paths:
      - "services/payments/**"
      - "openapi/payments.yaml"
  workflow_dispatch:

jobs:
  docs-maintainer:
    runs-on: ubuntu-latest

    permissions:
      contents: write
      pull-requests: write
      issues: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Tokenman
        uses: your-org/tokenman@v1
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
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

`ANTHROPIC_API_KEY` is shown above because Tokenman wraps the official
Claude Code Action, which needs model authentication for automation
runs. You can also provide `CLAUDE_CODE_OAUTH_TOKEN` instead.

## Repo shape

The MVP user-facing files are:

- `action.yml`
- `entrypoint.sh`
- `prompt.md`
- `README.md`

The `harness/` package remains as internal implementation code for the
action runtime, ledger, and local debugging path.

## License

See [LICENSE](LICENSE).
