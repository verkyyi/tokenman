#!/usr/bin/env bats

setup() {
  TEST_DIR="$(mktemp -d)"
  SCRIPT="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)/scripts/build-preamble.sh"

  # Create a git repo so git rev-parse --show-toplevel works
  cd "$TEST_DIR"
  git init -q
  git config user.email "test@test.com"
  git config user.name "Test"

  # Create state files
  mkdir -p state

  cat > state/evolve_config.md << 'EOF'
## Repo Profile
Stack: Node.js, Astro, TypeScript

## Build
install: npm ci
build: npm run build

## Project
CLAUDE.md: ./CLAUDE.md
EOF

  cat > state/learned_rules.md << 'EOF'
## RULE test rule
This is a test learned rule.
EOF

  cat > state/project_state.md << 'EOF'
# Project State
Last updated: 2026-01-01
## Last Session
Test session content.
EOF

  cat > CLAUDE.md << 'EOF'
# Test CLAUDE.md
## Root constitution
Root CLAUDE content here.
EOF

  cat > state/agent_log.md << 'EOF'
2026-01-01T00:00:00Z | test | test log entry | done
EOF

  cat > state/research_sources.md << 'EOF'
## Active Sources
- source1: http://example.com
EOF

  cat > state/research_log.md << 'EOF'
# Research Log
2026-01-01 | source1 | test finding | test action
EOF

  cat > state/last_evolve_summary.md << 'EOF'
Last evolve summary test content.
EOF

  git add -A
  git commit -q -m "init"
}

teardown() {
  cd /
  rm -rf "$TEST_DIR"
}

@test "exits with error when no tier argument provided" {
  cd "$TEST_DIR"
  run "$SCRIPT"
  [ "$status" -ne 0 ]
}

@test "T1 output includes evolve_config and learned_rules" {
  cd "$TEST_DIR"
  run "$SCRIPT" 1
  [ "$status" -eq 0 ]
  [[ "$output" == *"## Evolve Config"* ]]
  [[ "$output" == *"Stack: Node.js"* ]]
  [[ "$output" == *"## Learned Rules"* ]]
  [[ "$output" == *"test learned rule"* ]]
}

@test "T1 does not include project_state" {
  cd "$TEST_DIR"
  run "$SCRIPT" 1
  [ "$status" -eq 0 ]
  [[ "$output" != *"## Current Project State"* ]]
}

@test "T2 includes T1 content plus project_state" {
  cd "$TEST_DIR"
  run "$SCRIPT" 2
  [ "$status" -eq 0 ]
  [[ "$output" == *"## Evolve Config"* ]]
  [[ "$output" == *"## Learned Rules"* ]]
  [[ "$output" == *"## Current Project State"* ]]
  [[ "$output" == *"Test session content"* ]]
}

@test "T3 includes T2 content plus CLAUDE.md and agent_log" {
  cd "$TEST_DIR"
  run "$SCRIPT" 3
  [ "$status" -eq 0 ]
  [[ "$output" == *"## Evolve Config"* ]]
  [[ "$output" == *"## Current Project State"* ]]
  [[ "$output" == *"## CLAUDE.md (root)"* ]]
  [[ "$output" == *"Root constitution"* ]]
  [[ "$output" == *"## Recent Agent Log"* ]]
  [[ "$output" == *"test log entry"* ]]
}

@test "T4 includes T3 content plus research_sources and research_log" {
  cd "$TEST_DIR"
  run "$SCRIPT" 4
  [ "$status" -eq 0 ]
  [[ "$output" == *"## Evolve Config"* ]]
  [[ "$output" == *"## Current Project State"* ]]
  [[ "$output" == *"## CLAUDE.md (root)"* ]]
  [[ "$output" == *"## Research Sources"* ]]
  [[ "$output" == *"source1"* ]]
  [[ "$output" == *"## Recent Research Log"* ]]
  [[ "$output" == *"## Previous Evolve Run Summary"* ]]
  [[ "$output" == *"Last evolve summary"* ]]
}

@test "handles missing state files gracefully with (not found)" {
  cd "$TEST_DIR"
  rm -f state/project_state.md state/learned_rules.md

  run "$SCRIPT" 2
  [ "$status" -eq 0 ]
  [[ "$output" == *"(not found)"* ]]
}

@test "output-to-file mode works correctly" {
  cd "$TEST_DIR"
  local outfile="$TEST_DIR/preamble-output.txt"

  run "$SCRIPT" 2 "$outfile"
  [ "$status" -eq 0 ]
  [ -f "$outfile" ]
  grep -q "## Evolve Config" "$outfile"
  grep -q "## Current Project State" "$outfile"
}
