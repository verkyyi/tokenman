# stub-readme

Stub skill used by the tokenman harness test suite. Does **not** invoke
Claude. The runner in Phase 1.2a does not parse this file — it is
documentation only.

## Modes

Selected via the `STUB_MODE` env var passed by `StubSkillExecutor`:

| Mode | Effect |
|---|---|
| `no_change` (default) | Print a summary, write nothing. |
| `propose_diff` | Print a summary, write canned `proposed.diff` + `proposed.md`. |
| `crash` | Print to stderr, exit 2. |

Any other `STUB_MODE` value exits 3.
