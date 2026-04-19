# harness/ - Tokenman runtime source

**Source zone.** Contents here define the runtime that ships to
consumers.

## Purpose

The harness implements the internal action runtime:

- prepare the bounded docs-maintainer prompt
- invoke the coding agent with bounded context
- validate changed paths with `git`
- route valid runs to PR, issue, or no-op
- append cost and outcome history to the ledger

The harness should not grow into its own scheduler, patch-management
system, or broad execution framework.

## Contents

- `workflows/tokenman.yml.template` - installed into consumers at
  `.github/workflows/tokenman.yml`
- `lib/` - policy, orchestration, adapters, and ledger code

## See also

- [docs/spec.md](/Users/verkyyi/tokenman/docs/spec.md)
- [CONTRIBUTING.md](/Users/verkyyi/tokenman/CONTRIBUTING.md)
