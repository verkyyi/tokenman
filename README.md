# Tokenman

Open-source toolset (skills + workflows) that installs into any repo to
enable async AI maintenance via PRs. This repo is the **library** — source
of truth for distributable skills and workflows. Consumer repos install
copies.

> **Scaffolding stub.** The full README — with install steps, library-vs-consumer
> explanation, ledger usage, and the "this repo does not run tokenman on
> itself" notice — is authored in Step 5 of the setup plan.

## Repo layout (library role)

```
.tokenman/tokenman.yaml   # declares role: library
skills/                   # source of truth for distributable skills
workflows/                # source of truth for distributable workflows
CLAUDE.md                 # harness rules for Claude Code sessions
```

## Current skill

- `dead-code-cleanup` (Python) — subtractive-only cleanup of provably unused imports and unreachable code.

## License

MIT — see [LICENSE](./LICENSE).
