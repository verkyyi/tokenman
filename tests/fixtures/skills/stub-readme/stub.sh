#!/usr/bin/env bash
# Stub skill entrypoint. Reads STUB_MODE env var, edits the repo
# checkout passed as $2, and may write proposed.md into the scratch dir
# passed as $1. See SKILL.md in this directory.
set -euo pipefail

if [ "$#" -lt 2 ]; then
    echo "stub-readme: missing scratch-dir/repo-dir args" >&2
    exit 64
fi

SCRATCH="$1"
REPO="$2"
MODE="${STUB_MODE:-no_change}"

case "$MODE" in
  no_change)
    echo "stub-readme: no changes needed"
    ;;
  propose_diff)
    cat > "$SCRATCH/proposed.md" <<'MD'
Proposed adding a blank line and a sentence under the README heading.
MD
    printf '\nStub-readme added this line.\n' >> "$REPO/README.md"
    echo "stub-readme: proposed 1 diff"
    ;;
  crash)
    echo "stub-readme: crashing on purpose" >&2
    exit 2
    ;;
  *)
    echo "stub-readme: unknown STUB_MODE ${MODE@Q}" >&2
    exit 3
    ;;
esac
