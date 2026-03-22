#!/bin/bash
# Atomic state file update via GitHub API.
# Replaces git add/commit/push to avoid push conflicts between concurrent workflows.
# Usage: ./scripts/commit-state.sh <file_path> [commit_message]
# Requires: GH_TOKEN and GITHUB_REPOSITORY env vars (set by GitHub Actions)

set -euo pipefail

FILE_PATH="${1:?Usage: commit-state.sh <file_path> [commit_message]}"
COMMIT_MSG="${2:-state: update $(basename "$FILE_PATH" .md)}"
MAX_RETRIES=3

if [ ! -f "$FILE_PATH" ]; then
  echo "File not found: $FILE_PATH"
  exit 1
fi

for i in $(seq 1 $MAX_RETRIES); do
  # Get current SHA (file may not exist on remote yet)
  SHA=$(gh api "repos/$GITHUB_REPOSITORY/contents/$FILE_PATH" --jq '.sha' 2>/dev/null || echo "")

  # Encode local file content
  CONTENT=$(base64 -w0 "$FILE_PATH")

  # Build PUT request
  if [ -n "$SHA" ]; then
    RESULT=$(gh api "repos/$GITHUB_REPOSITORY/contents/$FILE_PATH" \
      -X PUT \
      -f message="$COMMIT_MSG" \
      -f content="$CONTENT" \
      -f sha="$SHA" 2>&1) || true
  else
    RESULT=$(gh api "repos/$GITHUB_REPOSITORY/contents/$FILE_PATH" \
      -X PUT \
      -f message="$COMMIT_MSG" \
      -f content="$CONTENT" 2>&1) || true
  fi

  # Check success
  if echo "$RESULT" | grep -q '"content"'; then
    echo "Updated $FILE_PATH"
    exit 0
  fi

  if [ "$i" -lt "$MAX_RETRIES" ]; then
    echo "Retry $i/$MAX_RETRIES for $FILE_PATH (SHA conflict or API error)"
    sleep 2
  fi
done

echo "Warning: Failed to update $FILE_PATH after $MAX_RETRIES retries"
exit 0  # Don't fail the workflow over state writes
