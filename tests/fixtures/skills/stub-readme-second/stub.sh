#!/usr/bin/env bash
# Second stub skill entrypoint. Mirrors stub-readme/stub.sh but with a
# distinct summary so multi-skill tests can tell the two apart.
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "stub-readme-second: missing scratch-dir arg" >&2
    exit 64
fi

SCRATCH="$1"
MODE="${STUB_MODE:-no_change}"

case "$MODE" in
  no_change)
    echo "stub-readme-second: nothing to change"
    ;;
  propose_diff)
    cat > "$SCRATCH/proposed.diff" <<'DIFF'
--- a/README.md
+++ b/README.md
@@ -1,3 +1,5 @@
 # tiny-python-repo

 Fixture for tokenman harness testing. Simulates a minimal Python consumer repo.
+
+Stub-readme-second added a different sentence.
DIFF
    cat > "$SCRATCH/proposed.md" <<'MD'
Proposed adding a different sentence under the README heading.
MD
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
