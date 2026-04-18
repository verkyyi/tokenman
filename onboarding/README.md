# onboarding/ — Guided first-run flow

**Source zone.** Contents here ship to consumers.

## Purpose
Implements the guided onboarding run described in `docs/spec.md` §6.4.
Runs all enabled skills back-to-back in one session with an elevated
budget, opens one PR per skill, writes
`.tokenman/onboarding-summary.md`. Exists to get a new consumer from
install to visible value in ~10 minutes.

## Status
Empty at Phase 0. Implemented in Phase 1.

## See also
- `docs/spec.md` §6.4 (guided onboarding run)
- `docs/spec.md` §12 Phase 1
