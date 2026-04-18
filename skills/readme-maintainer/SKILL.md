---
name: readme-maintainer
description: Keep the repo's README.md aligned with the actual contents of the repo.
---

# readme-maintainer

**Version:** 0.1.0
**Source:** tokenman library, `skills/readme-maintainer/` (temporary — see `skills/README.md`)

## Scope

Operates on `README.md` only. Does not read or modify other files.

## Shape

In-place edit. Prefer additive changes (new sections) over rewrites. If
the README already describes the repo accurately, stop without edits.

## Size limit

Diff must be ≤ ~100 lines. If a bigger change is warranted, stop and
surface the observation in your final message instead of making the
edit.

## Deterministic gate hints

- Only `README.md` should appear in the diff.
- No new files.
- No deletions of entire top-level sections without an explicit reason.

## Evaluator criteria (medium strictness)

- Changes stay scoped to `README.md`.
- Additions are factually grounded in other repo contents (do not
  invent features).
- Tone is consistent with the existing README.

## Typical token budget

~15 000 tokens per run (generator + evaluator combined).

## Instructions

When invoked:

1. Read `README.md`.
2. Read the repo structure (top-level files and directories) to
   compare what's documented against what's present.
3. If the README omits something significant (e.g. missing `Usage`,
   `Install`, or `Development` section that the repo clearly supports),
   propose an addition.
4. If the README is already aligned with the repo, stop without edits
   and say so in your final message.
5. Stay within the size limit. If you think a bigger change is needed,
   summarize the finding instead of making it.
