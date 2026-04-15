#!/usr/bin/env bash
# archive-agent-log.sh — Rolling archive for agent_log.md
# Moves entries beyond the last 100 to agent_log_archive.md.
# Preserves append-only contract: data is moved, never deleted.
# Modeled on scripts/archive-research-log.sh (PR #78).

set -euo pipefail

AGENT_LOG="state/agent_log.md"
ARCHIVE="state/agent_log_archive.md"
HEADER_LINES=9  # 5 comment lines + blank + ## Log + blank + HTML comment
KEEP=100        # entries to keep in active file

if [ ! -f "$AGENT_LOG" ]; then
  echo "No agent log found, skipping archive."
  exit 0
fi

TOTAL_LINES=$(wc -l < "$AGENT_LOG")
ENTRY_LINES=$((TOTAL_LINES - HEADER_LINES))

if [ "$ENTRY_LINES" -le "$KEEP" ]; then
  echo "Agent log has $ENTRY_LINES entries (<= $KEEP), no archiving needed."
  exit 0
fi

ARCHIVE_COUNT=$((ENTRY_LINES - KEEP))
echo "Archiving $ARCHIVE_COUNT entries (keeping last $KEEP of $ENTRY_LINES)."

# Extract header
head -n "$HEADER_LINES" "$AGENT_LOG" > /tmp/agent_header.txt

# Extract entries to archive (lines after header, up to ARCHIVE_COUNT)
ARCHIVE_START=$((HEADER_LINES + 1))
ARCHIVE_END=$((HEADER_LINES + ARCHIVE_COUNT))

# Initialize archive file if it doesn't exist
if [ ! -f "$ARCHIVE" ]; then
  cat > "$ARCHIVE" << 'EOF'
# Agent Log Archive
# Archived entries from state/agent_log.md (rolling archive).
# This file is NOT read during session start — historical reference only.
# Format: ISO_DATETIME | workflow | action | outcome

EOF
fi

# Append archived entries
sed -n "${ARCHIVE_START},${ARCHIVE_END}p" "$AGENT_LOG" >> "$ARCHIVE"

# Rebuild active file: header + kept entries
KEEP_START=$((ARCHIVE_END + 1))
cat /tmp/agent_header.txt > /tmp/agent_new.txt
sed -n "${KEEP_START},\$p" "$AGENT_LOG" >> /tmp/agent_new.txt

mv /tmp/agent_new.txt "$AGENT_LOG"
rm -f /tmp/agent_header.txt

echo "Archived $ARCHIVE_COUNT entries. Active file now has $KEEP entries."
