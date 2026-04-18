# Tokenman - Phase 1 Product Scope

## Product boundary

Phase 1 proves that Tokenman can safely generate mergeable docs-maintenance
PRs for Claude Code users, with clear cost visibility and minimal operator
anxiety.

- User: maintainers already comfortable with GitHub PR review and Claude Code
- Job: keep `README.md` and repo-facing docs current without manual follow-up
- Repo scope: docs-only
- Execution model: one skill at a time, one open PR per skill, GitHub Actions
  fixed schedule or manual trigger only
- Interaction model: GitHub web and mobile are the default UI; local
  coding-agent sessions are for setup and debugging
- Trust model: PR-only, no auto-merge, pause file, explicit path boundaries,
  append-only ledger on a dedicated state branch

This keeps the spirit of `docs/spec.md`, but narrows the promise to the part
most likely to earn trust first.

## Keep in Phase 1

- Install flow that writes `.tokenman/`, workflow file, and skill files into
  the repo
- Initial scoping flow, but limited to repo profile, recommended docs skill(s),
  and allowed/forbidden paths
- Guided onboarding run, capped to 1-2 docs-focused PRs rather than "all
  enabled skills"
- One starter skill from `recommended-skills.yaml`: `readme-maintainer`
- Fixed schedule and manual runs only
- Basic observability: `ledger.jsonl`, per-run artifacts, and GitHub workflow
  summaries
- Core guardrails: `PAUSE`, open-PR lock, scope check, size cap, and
  review-bandwidth gate if it is cheap to implement
- PR labels and branch naming conventions

## Defer out of Phase 1

- Budget calibration via subscription detection and `pricing.yaml`
- Multi-skill onboarding beyond docs / README
- Dependency bumps, dead-code cleanup, or other behavior-affecting maintenance
- Generator/evaluator split if it materially slows delivery
- Adaptive scheduling, event-driven runs, cooldown optimization, and token
  allocation presets
- Learning loop, `learned.md`, and preference inference from PR outcomes
- DAG / parallel execution
- External catalog breadth as a product message
- Broader dogfood expansion rules as user-facing roadmap

## Concrete Phase 1 roadmap

### 1. Install and scope

- `/tokenman init` creates the runtime files and installs the single starter
  skill
- `tokenman scope` produces a reviewable docs-only scope file
- User edits boundaries before the first run

### 2. Onboarding proof

- One onboarding command runs the starter skill once
- Output is at most 1-2 reviewable PRs plus a short onboarding summary
- The summary answers: what changed, what was skipped, and what it cost

### 3. Scheduled docs maintenance

- Fixed weekly run or manual trigger
- One open PR per skill, docs-only boundaries, pause respected
- If no useful change is found, the ledger records `no_change` cleanly

### 4. Trust and observability polish

- Status script shows last runs, PR outcomes, and token usage
- Artifact retention is simple and conservative
- README and demo focus on safe unattended docs upkeep, not general autonomous
  repo maintenance

## Phase 1 exit criteria

- User installs in under 5 minutes
- First docs PR appears within 10 minutes
- At least one Phase 1 user merges a PR without needing to deeply inspect the
  harness
- Ledger and status output answer "what did it do and what did it cost?" in
  under 30 seconds
- The product can show repeated low-risk value before adding a second skill
