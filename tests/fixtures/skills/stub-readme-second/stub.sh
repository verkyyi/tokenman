#!/usr/bin/env bash
# Second stub skill entrypoint. Mirrors stub-readme/stub.sh but with a
# distinct summary so multi-skill tests can tell the two apart.
set -euo pipefail

if [ "$#" -lt 2 ]; then
    echo "stub-readme-second: missing scratch-dir/repo-dir args" >&2
    exit 64
fi

SCRATCH="$1"
REPO="$2"
MODE="${STUB_MODE:-no_change}"

case "$MODE" in
  no_change)
    echo "stub-readme-second: nothing to change"
    ;;
  propose_diff)
    cat > "$SCRATCH/proposed.md" <<'MD'
Proposed adding a different sentence under the README heading.
MD
    printf '\nStub-readme-second added a different sentence.\n' >> "$REPO/README.md"
    echo "stub-readme-second: proposed 1 diff"
    ;;
  crash)
    echo "stub-readme-second: crashing on purpose" >&2
    exit 2
    ;;
  *)
    echo "stub-readme-second: unknown STUB_MODE ${MODE@Q}" >&2
    exit 3
    ;;
esac
