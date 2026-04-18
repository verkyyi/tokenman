# scoping/ — Discovery and scope-proposal logic

**Source zone.** Contents here ship to consumers.

## Purpose
Implements the scope-proposal flow described in `docs/spec.md` §6.3.
Given a fresh consumer repo, detects language/size/test-coverage/activity
and proposes an initial scope (skills, boundaries, budget, schedule).
Output: `.tokenman/initial-scope.md` in the consumer repo.

## Status
Empty at Phase 0. Implemented in Phase 1.

## See also
- `docs/spec.md` §6.3 (initial scoping)
- `docs/spec.md` §12 Phase 1 (wedge + guided onboarding)
