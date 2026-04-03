#!/usr/bin/env bats

setup() {
  TEST_DIR="$(mktemp -d)"
  SCRIPT="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)/scripts/commit-state.sh"

  echo "test content" > "$TEST_DIR/test-file.md"

  MOCK_BIN="$TEST_DIR/mock-bin"
  mkdir -p "$MOCK_BIN"
  PATH="$MOCK_BIN:$PATH"

  export GITHUB_REPOSITORY="owner/repo"
  export GH_TOKEN="fake-token"

  # Mock git to do nothing
  cat > "$MOCK_BIN/git" << 'EOF'
#!/bin/bash
exit 0
EOF
  chmod +x "$MOCK_BIN/git"

  # Mock sleep to avoid waiting during retries
  cat > "$MOCK_BIN/sleep" << 'EOF'
#!/bin/bash
exit 0
EOF
  chmod +x "$MOCK_BIN/sleep"
}

teardown() {
  rm -rf "$TEST_DIR"
}

@test "exits with error when no arguments provided" {
  run "$SCRIPT"
  [ "$status" -ne 0 ]
}

@test "exits with error when file does not exist" {
  run "$SCRIPT" "$TEST_DIR/nonexistent.md"
  [ "$status" -eq 1 ]
  [[ "$output" == *"File not found"* ]]
}

@test "handles missing GITHUB_REPOSITORY env var" {
  unset GITHUB_REPOSITORY
  run "$SCRIPT" "$TEST_DIR/test-file.md"
  # set -u causes failure on unbound variable
  [ "$status" -ne 0 ]
}

@test "PUT with sha for existing file" {
  cat > "$MOCK_BIN/gh" << 'EOF'
#!/bin/bash
if [[ "$*" == *"--jq"* ]]; then
  echo "existingsha456"
elif [[ "$*" == *"-X"*"PUT"* ]]; then
  if [[ "$*" == *"sha=existingsha456"* ]]; then
    echo '{"content": {"name": "test-file.md"}}'
  else
    echo '{"message": "sha mismatch"}' >&2
    exit 1
  fi
fi
EOF
  chmod +x "$MOCK_BIN/gh"

  run "$SCRIPT" "$TEST_DIR/test-file.md"
  [ "$status" -eq 0 ]
  [[ "$output" == *"Updated"* ]]
}

@test "PUT without sha for new file" {
  cat > "$MOCK_BIN/gh" << 'EOF'
#!/bin/bash
if [[ "$*" == *"--jq"* ]]; then
  exit 1
elif [[ "$*" == *"-X"*"PUT"* ]]; then
  if [[ "$*" == *"sha="* ]]; then
    echo '{"message": "should not have sha"}' >&2
    exit 1
  fi
  echo '{"content": {"name": "test-file.md"}}'
fi
EOF
  chmod +x "$MOCK_BIN/gh"

  run "$SCRIPT" "$TEST_DIR/test-file.md"
  [ "$status" -eq 0 ]
  [[ "$output" == *"Updated"* ]]
}

@test "retries on failure then succeeds" {
  export GH_CALL_COUNTER="$TEST_DIR/gh-put-counter"
  echo "0" > "$GH_CALL_COUNTER"

  cat > "$MOCK_BIN/gh" << 'EOF'
#!/bin/bash
if [[ "$*" == *"--jq"* ]]; then
  echo "sha789"
elif [[ "$*" == *"-X"*"PUT"* ]]; then
  COUNT=$(cat "$GH_CALL_COUNTER")
  COUNT=$((COUNT + 1))
  echo "$COUNT" > "$GH_CALL_COUNTER"
  if [ "$COUNT" -le 1 ]; then
    echo '{"message": "conflict"}'
  else
    echo '{"content": {"name": "test-file.md"}}'
  fi
fi
EOF
  chmod +x "$MOCK_BIN/gh"

  run "$SCRIPT" "$TEST_DIR/test-file.md"
  [ "$status" -eq 0 ]
  [[ "$output" == *"Retry"* ]]
  [[ "$output" == *"Updated"* ]]
}

@test "exits 0 even after max retries (graceful failure)" {
  cat > "$MOCK_BIN/gh" << 'EOF'
#!/bin/bash
if [[ "$*" == *"--jq"* ]]; then
  echo "sha000"
elif [[ "$*" == *"-X"*"PUT"* ]]; then
  echo '{"message": "always failing"}'
fi
EOF
  chmod +x "$MOCK_BIN/gh"

  run "$SCRIPT" "$TEST_DIR/test-file.md"
  [ "$status" -eq 0 ]
  [[ "$output" == *"Warning: Failed to update"* ]]
}
