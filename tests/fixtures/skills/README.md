# Skill test fixtures

Stub skills used by `tests/test_skill_executor.py` and
`tests/test_runner.py` to exercise the harness runner without invoking
`claude -p`. These are deliberately minimal — a fake SKILL.md plus a
bash entrypoint (`stub.sh`) that writes canned files based on the
`STUB_MODE` env var.

Not to be confused with `tests/fixtures/tiny-*-repo/`, which hosts
synthetic *consumer* repositories for harness integration tests.

## Adding a new stub

Each stub lives under `tests/fixtures/skills/<name>/` and must contain:

- `SKILL.md` — human-readable notes; the runner does not parse it.
- `stub.sh` — executable bash entrypoint that takes one argument
  (a scratch directory) and writes `proposed.diff` / `proposed.md` into
  it, or exits non-zero.

All stub scripts must pass `shellcheck`.
