#!/usr/bin/env bash
# Stub skill entrypoint. Reads STUB_MODE env var, writes canned output
# into the scratch dir passed as $1. See SKILL.md in this directory.
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "stub-readme: missing scratch-dir arg" >&2
    exit 64
fi

SCRATCH="$1"
MODE="${STUB_MODE:-no_change}"

case "$MODE" in
  no_change)
    echo "stub-readme: no changes needed"
    ;;
  propose_diff)
    cat > "$SCRATCH/proposed.diff" <<'DIFF'
--- a/README.md
+++ b/README.md
@@ -1,3 +1,5 @@
 # tiny-python-repo

 Fixture for tokenman harness testing. Simulates a minimal Python consumer repo.
+
+Stub-readme added this line.
DIFF
    cat > "$SCRATCH/proposed.md" <<'MD'
Proposed adding a blank line and a sentence under the README heading.
MD
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
