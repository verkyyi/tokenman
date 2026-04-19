# Tokenman context for the tokenman library repo

## CRITICAL: this repo is the tokenman library itself.
## Dogfooding is SEVERELY restricted. Phase 3 README smoke test is active.

## Allowed paths (nothing else — and even these are gated by phase)
- docs/**/*.md                 # Phase 4+
- README.md                    # Phase 3 active (narrow README dogfood)
- CHANGELOG.md                 # Phase 4+ (if it ever exists)
- .tokenman/smoketest.md       # Phase 3 smoke test only

## FORBIDDEN paths (never touch, any phase)
- harness/                     # the runtime itself
- skills/                      # tombstone only; not part of the MVP surface
- .github/                     # the workflows
- .claude/skills/              # installed skills
- tests/fixtures/              # must remain pristine
- .tokenman/CLAUDE.md          # this file — human-edited only
- .tokenman/tokenman.yaml      # config — human-edited only
- LICENSE, .gitignore, .shellcheckrc

## FORBIDDEN operations
- Any change that could affect how the harness behaves
- Any change to version numbers
- Any change to package.json / pyproject.toml
- Direct commits to main
- Auto-merge

## If in doubt, abort. Open an issue instead of a PR.
