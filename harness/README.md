# harness/ - Tokenman action runtime

**Source zone.** Contents here define the runtime that ships to
consumers.

## Purpose

The harness is the internal implementation behind the public Action:

- prepare the bounded docs-maintainer prompt
- wrap the official Claude Code Action
- validate changed paths with `git`
- route valid runs to PR, issue, or no-op
- append cost and outcome history to the ledger

It should stay flat and action-specific, not grow into a framework.

## Contents

- `prepare.py` - pre-Claude prompt/state preparation
- `finalize.py` - post-Claude validation and routing
- `docs.py` - docs-maintainer-only validation and PR/issue body helpers
- `scope.py` - read/write path parsing and enforcement
- `git.py` - git branch/diff/commit helpers
- `github.py` - `gh` helpers for PR and issue creation
- `ledger.py` and `ledger.schema.json` - append-only run history
- `workflow.yml.template` - example consumer workflow

## See also

- [docs/spec.md](/Users/verkyyi/tokenman/docs/spec.md)
- [CONTRIBUTING.md](/Users/verkyyi/tokenman/CONTRIBUTING.md)
