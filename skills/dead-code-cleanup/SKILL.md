---
name: dead-code-cleanup
version: 0.1.0
origin: local
---

# dead-code-cleanup

Remove **provably unused imports** and **unreachable code** from a Python
codebase. Subtractive diffs only. Tests must pass before and after.

This skill runs as a supervised, test-gated cleanup pass inside a GitHub
Actions workflow (typically `tokenman-run.yml`) via `claude -p` — not as
an interactive refactor.

## When to activate

When tokenman is asked to clean up dead code in a Python project. The
`tokenman-run` workflow invokes this skill on its configured cadence.

## Scope — what this skill DOES

1. **Whole-line unused imports.** An `import X` or `from X import A` line
   where the imported name is not referenced anywhere in the file and is
   not exported via `__all__`.
2. **Unreachable statements.** Statements whose in-order predecessor at
   the same nesting level is an unconditional `return`, `raise`,
   `continue`, or `break`.

Both must be detectable by static analysis. If an analyser does not flag
it, leave it alone.

## Non-goals — what this skill DOES NOT do

- **No refactoring.** No rename, reorder, extract, inline, or move.
- **No logic changes.** No operator flips, condition tweaks,
  default-value changes, or any runtime behavior change.
- **No partial-line import edits.** If a `from X import A, B` line has
  some used and some unused names, LEAVE it. The skill only removes
  whole-line imports whose every imported name is unused.
- **No test changes.** Do not modify anything under `tests/`,
  `test_*.py`, or `*_test.py`. A symbol referenced by a test is used.
- **No reformatting.** No reindent, no line-ending changes, no blank-line
  adjustments in files that have no dead-code changes.
- **No dependency edits.** No changes to `pyproject.toml`, `setup.cfg`,
  `setup.py`, `requirements*.txt`, or lock files.
- **No new files.** Only delete lines from existing files.
- **No comment cleanup.** If removing dead code orphans a comment, the
  comment stays.

## Procedure

1. **Identify source dirs.** Source dirs = the Python packages declared
   in `pyproject.toml` / `setup.cfg`. Fallback: every top-level directory
   containing `__init__.py`, plus `src/` if it exists. Tests are NOT
   source dirs. Record the source-dir allowlist; every removal must be
   inside it.
2. **Baseline tests.** Run `python3 -m pytest` (or the project's
   configured test command). Prefer `python3 -m pytest` over `pytest`
   directly — it works even when the binary is not on PATH (common
   in user installs). If any test fails, ABORT with
   reason `baseline-failed`. If `python3 -m pytest` itself cannot run
   (no pytest installed), ABORT with reason `no-test-harness`.
3. **Find unused imports.** Use a well-known analyser:
   `python3 -m ruff check --select F401 --output-format=json`,
   `python3 -m pyflakes`, or a direct AST walk. Filter to whole-line
   unused imports only. (Prefer the `python3 -m` form over bare
   binaries for the same PATH-reachability reason as above.)
4. **Find unreachable code.** Walk each source file's AST. For every
   block, flag statements that follow an unconditional terminator
   (`Return`, `Raise`, `Continue`, `Break`) at the same indentation
   level.
5. **Apply removals, one file at a time.** Delete target lines exactly.
   Do not reflow, reindent, or insert anything. Do not combine changes
   across files into one hunk.
6. **Verify.**
   - Tests pass. Re-run the suite. For any file whose change breaks a
     test, `git checkout` that file and drop it from the diff. Keep the
     rest.
   - `git diff --numstat` shows `0` insertions overall.
   - Total deletions ≤ 100 lines. If above, truncate to the
     smallest-impact subset that fits.
   - `git diff --name-only` lists only paths inside the source-dir
     allowlist.
7. **Open the PR.**
   - Branch: `tokenman/dead-code-cleanup-<YYYYMMDD-HHMMSS>`.
   - Base: `main`.
   - Title: `tokenman: dead-code-cleanup — N imports, M unreachable`.
   - Label: `tokenman:dead-code-cleanup`.
   - Body: a short per-file list of what was removed and which category.

## Abort conditions

Stop immediately, emit a `status: abort` ledger entry. No commits, no PR.

| Reason | Trigger |
| --- | --- |
| `baseline-failed` | Tests fail before any change. |
| `nothing-to-do` | Analyser returns zero findings. |
| `scope-violation` | A planned or applied change touches a path outside the source-dir allowlist. |
| `diff-has-insertions` | Final diff has any line insertion. |
| `diff-too-large` | Deletions exceed 100 lines after truncation attempt. |
| `tests-broken-by-change` | Every proposed change, applied one at a time, breaks tests — nothing is safe to ship. |
| `no-test-harness` | Project has no tests, or `pytest` (or equivalent) cannot run. |

## Output

On success: a PR on `main` labeled `tokenman:dead-code-cleanup`. Diff is
all deletions, under 100 lines. All tests pass.

On abort: no commits, no PR. The `tokenman-run` workflow records the
reason in `.tokenman/ledger.jsonl`.

## Testing this skill

The fixture at `tests/fixtures/tiny-python-repo/` is a minimal Python
project with intentional dead imports and unreachable statements plus a
passing test suite. A correct skill run against it deletes:

- `import os` and `import sys` in `src/tinypkg/app.py` (both unused).
- The `print("never runs")` statement after `return` in `make_greeting`.
- The unreachable block after `return items` in `legacy_process`.

`from typing import Any, List` stays: `Any` is used, and partial imports
are out of scope.
