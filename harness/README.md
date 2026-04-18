# harness/ — Tokenman runtime source

**Source zone.** Contents here ship to consumers when `/tokenman init`
fetches the harness.

## Purpose
The tokenman runtime itself: workflow templates, generator/evaluator
drivers, deterministic gates, ledger append logic, PR opener. Not yet
implemented — Phase 0 scaffolds the directory and the workflow template
stub. Phase 1+ populates lib/ with actual code.

## Contents
- `workflows/tokenman.yml.template` — installed into
  consumers at `.github/workflows/tokenman.yml` by `/tokenman init`.

## See also
- `docs/spec.md` §3.2 (source vs runtime paths)
- `docs/spec.md` §4 (execution pipeline)
- `CONTRIBUTING.md` (source/runtime split)
