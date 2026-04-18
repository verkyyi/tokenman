# Tokenman — Library

Open-source toolset (skills + workflows) that installs into any repo to
enable async AI maintenance via PRs. This repo is the **library** — source
of truth for distributable skills and workflows. Consumer repos install
copies.

## Role

`role: library` (declared in `.tokenman/tokenman.yaml`).

- NOT a hosted product, NOT a CLI wrapper, NOT self-evolving.
- **Dogfooding is OFF.** Tokenman does not run on itself.
- Distribution: Claude Code CLI users. Manual copy for now; no installer yet.

## Safety model

- **PRs only.** Tokenman workflows never commit directly — they open PRs; humans merge.
- **Execution: `claude -p`** (headless Claude Code inside GitHub Actions). Never the Anthropic API directly.
- Every skill's `SKILL.md` has frontmatter: `name`, `version`, `origin: local`.

## Directory contract

| Path | Meaning |
| --- | --- |
| `/skills/` | **Source of truth** for distributable skills. |
| `/workflows/` | **Source of truth** for distributable workflows. |
| `/.tokenman/tokenman.yaml` | Declares this repo's role. |
| `.claude/skills/` | Consumer runtime path. **Must stay empty in this repo.** |
| `.github/workflows/` | Consumer runtime path. **Must stay empty in this repo.** |

Consumers copy `/skills/<name>/` → `.claude/skills/<name>/` and `/workflows/<name>.yml` → `.github/workflows/<name>.yml`.

## Current library surface

- **`dead-code-cleanup`** (Python, v0.1.0) — removes provably unused imports and unreachable code. Subtractive diffs only; tests must pass; diff under 100 lines.

**Legacy skills** still present in `/skills/` (kept pending decision): `adversarial-review/`, `harness/`, `session-protocol/`, `feedback-intake/`, `github-roadmap-planning/`, `github-task-headless/`, `github-task-interactive/`, plus loose `.md` files (`content.md`, `frontend.md`, `seo.md`, `github-workflows.md`, `readme-sync.md`, `adversarial-review.md`, `harness.md`, `feedback-intake.md`). These are NOT part of the current library surface.

## Commit conventions

Imperative, sentence case, no trailing period, under ~72 chars.

- `feat(skill): …` / `feat(workflow): …`
- `fix(skill|workflow): …`
- `docs: …`
- `chore: …`

## What NOT to do in this repo

- Do NOT create `.claude/skills/` or `.github/workflows/` here with distributable content.
- Do NOT add new skills to the library surface without explicit scope approval.
- Do NOT wire tokenman workflows to run on this repo.
- Do NOT call the Anthropic API directly — all execution goes through `claude -p`.

## Failure log

> One line per past mistake. Add, never remove. Date every entry.

_(fresh — no entries yet)_
