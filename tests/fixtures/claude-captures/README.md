# `claude -p --output-format json` captures

Each file is a recorded `stdout` from a real (or synthetic) invocation.
Used by `tests/test_claude_skill_executor_replay.py` to validate the
parser against real JSON shape without re-spending tokens.

`readme-maintainer.json` is currently **synthetic** — refresh it with
a real capture once `skills/readme-maintainer/` (ii.7) lands and
`claude` is available locally. Capture snippet lives in
`docs/superpowers/plans/2026-04-18-phase-1-2b-real-skill-integration.md`
Task 25 Step 2.
