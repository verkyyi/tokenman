#!/usr/bin/env bats

setup() {
  TEST_DIR="$(mktemp -d)"
  SCRIPT="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)/scripts/archive-research-log.sh"

  mkdir -p "$TEST_DIR/state"
  ORIG_DIR="$(pwd)"
  cd "$TEST_DIR"
}

teardown() {
  cd "$ORIG_DIR"
  rm -rf "$TEST_DIR"
}

create_research_log() {
  local num_entries="$1"
  cat > "$TEST_DIR/state/research_log.md" << 'HEADER'
# Research Log
# Format: ISO_TIMESTAMP | source | finding_summary | action_taken
# Example: 2026-03-20T10:00:00Z | github/anthropics | new release v2.0 | created issue #5
# ---
HEADER
  for i in $(seq 1 "$num_entries"); do
    echo "2026-03-20T10:00:00Z | source$i | finding $i | action $i" >> "$TEST_DIR/state/research_log.md"
  done
}

@test "skips gracefully when research_log.md does not exist" {
  run "$SCRIPT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"No research log found"* ]]
}

@test "skips when entry count <= 100" {
  create_research_log 50

  run "$SCRIPT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"no archiving needed"* ]]
}

@test "skips when entry count is exactly 100" {
  create_research_log 100

  run "$SCRIPT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"no archiving needed"* ]]
}

@test "archives correct number of entries when count > 100" {
  create_research_log 150

  run "$SCRIPT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"Archiving 50 entries"* ]]

  # Active file: 4 header lines + 100 kept entries = 104 lines
  local active_lines
  active_lines=$(wc -l < "$TEST_DIR/state/research_log.md")
  [ "$active_lines" -eq 104 ]

  # Archive file should exist with the archived entries
  [ -f "$TEST_DIR/state/research_log_archive.md" ]
  local archived_entries
  archived_entries=$(grep -c "^2026-" "$TEST_DIR/state/research_log_archive.md")
  [ "$archived_entries" -eq 50 ]
}

@test "creates archive file if it does not exist" {
  create_research_log 110
  [ ! -f "$TEST_DIR/state/research_log_archive.md" ]

  run "$SCRIPT"
  [ "$status" -eq 0 ]
  [ -f "$TEST_DIR/state/research_log_archive.md" ]
}

@test "preserves 4-line header in active file after archiving" {
  create_research_log 120

  run "$SCRIPT"
  [ "$status" -eq 0 ]

  # Verify header lines are intact
  local line1 line2 line3 line4
  line1=$(sed -n '1p' "$TEST_DIR/state/research_log.md")
  line2=$(sed -n '2p' "$TEST_DIR/state/research_log.md")
  line3=$(sed -n '3p' "$TEST_DIR/state/research_log.md")
  line4=$(sed -n '4p' "$TEST_DIR/state/research_log.md")
  [[ "$line1" == "# Research Log" ]]
  [[ "$line2" == *"Format:"* ]]
  [[ "$line3" == *"Example:"* ]]
  [[ "$line4" == "# ---" ]]
}

@test "appends to existing archive file (does not overwrite)" {
  # Pre-populate archive with old content
  cat > "$TEST_DIR/state/research_log_archive.md" << 'EOF'
# Research Log Archive
# Archived entries from state/research_log.md (rolling archive).
# This file is NOT read during session start — historical reference only.
# Format: ISO_TIMESTAMP | source | finding_summary | action_taken

2026-01-01T00:00:00Z | old-source | old finding | old action
EOF
  local initial_lines
  initial_lines=$(wc -l < "$TEST_DIR/state/research_log_archive.md")

  create_research_log 110
  run "$SCRIPT"
  [ "$status" -eq 0 ]

  # Archive should have grown
  local final_lines
  final_lines=$(wc -l < "$TEST_DIR/state/research_log_archive.md")
  [ "$final_lines" -gt "$initial_lines" ]

  # Old content must still be present
  grep -q "old-source" "$TEST_DIR/state/research_log_archive.md"
}
