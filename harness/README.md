# harness/ - Tokenman runtime source

**Source zone.** Contents here define the runtime that ships to
consumers.

## Purpose

The harness should converge on a small Actions-first runtime:

- load repo profile and scope
- enforce policy before each run
- invoke the coding agent with bounded context
- inspect changed paths with `git`
- open or update a PR with `gh`
- append cost and outcome history to the ledger

The harness should not grow into its own scheduler, patch-management
system, or broad execution framework.

## Contents

- `workflows/tokenman.yml.template` - installed into consumers at
  `.github/workflows/tokenman.yml`
- `lib/` - policy, orchestration, adapters, and ledger code

## See also

- [docs/spec.md](/Users/verkyyi/tokenman/docs/spec.md)
- [docs/actions-first-refactor-plan.md](/Users/verkyyi/tokenman/docs/actions-first-refactor-plan.md)
- [CONTRIBUTING.md](/Users/verkyyi/tokenman/CONTRIBUTING.md)
