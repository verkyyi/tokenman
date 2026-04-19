# stub-readme-second

Second stub skill used by runner tests. Mirrors
`stub-readme` but emits a different output line so tests can
distinguish the two skills' ledger entries.

Reads `STUB_MODE` from env (`no_change` | `propose_diff` | `crash`),
defaulting to `no_change`. See `tests/fixtures/skills/stub-readme/`
for the original.
