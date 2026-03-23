#!/bin/bash
# Evolve Workflow Smoke Test
# Run after merging any evolve.yml changes to validate the posture system.
# Usage: ./tests/evolve-smoke-test.sh [run_id]
#   If run_id is provided, checks that specific run.
#   If omitted, triggers a new run and waits for it.
#
# What it checks:
#   1. Run completes successfully
#   2. Posture was selected and logged
#   3. Structured log format is correct (deep:N scan:N issues:N findings:N)
#   4. last_evolve_summary.md has posture history and counters
#   5. research_sources.md was updated (Last deep / Pattern hits)
#   6. usage_log.md has posture:X and issues:N fields
#   7. No regression in state file commits

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

check() {
  local desc="$1"
  local result="$2"
  if [ "$result" = "pass" ]; then
    echo -e "  ${GREEN}PASS${NC} $desc"
    PASS=$((PASS + 1))
  elif [ "$result" = "warn" ]; then
    echo -e "  ${YELLOW}WARN${NC} $desc"
    WARN=$((WARN + 1))
  else
    echo -e "  ${RED}FAIL${NC} $desc"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Evolve Smoke Test ==="
echo ""

# Step 0: Get or trigger run
RUN_ID="${1:-}"
if [ -z "$RUN_ID" ]; then
  echo "Triggering evolve workflow..."
  gh workflow run evolve.yml
  sleep 5
  RUN_ID=$(gh run list --workflow=evolve.yml --limit 1 --json databaseId -q '.[0].databaseId')
  echo "Run ID: $RUN_ID"
  echo "Waiting for completion (timeout 10 min)..."
  gh run watch "$RUN_ID" --exit-status 2>&1 | tail -3 || true
fi

# Step 1: Check run status
echo ""
echo "--- Run Status ---"
CONCLUSION=$(gh run view "$RUN_ID" --json conclusion -q '.conclusion')
if [ "$CONCLUSION" = "success" ]; then
  check "Run completed successfully" "pass"
else
  check "Run completed successfully (got: $CONCLUSION)" "fail"
fi

# Pull latest state
git pull --quiet 2>/dev/null || true

# Step 2: Check posture selection
echo ""
echo "--- Posture Selection ---"
if [ -f state/last_evolve_summary.md ]; then
  POSTURE=$(grep -oP 'Posture: \K\w+' state/last_evolve_summary.md 2>/dev/null || echo "")
  if [ -n "$POSTURE" ]; then
    check "Posture selected: $POSTURE" "pass"
  else
    check "Posture field present in last_evolve_summary.md" "fail"
  fi

  HISTORY=$(grep "Posture history:" state/last_evolve_summary.md 2>/dev/null || echo "")
  if [ -n "$HISTORY" ]; then
    check "Posture history present: $HISTORY" "pass"
  else
    check "Posture history field present" "fail"
  fi

  COUNTERS=$(grep -c "PATTERN_HUNT\|PIPELINE_WATCH\|HORIZON_SCAN\|SYNTHESIS" state/last_evolve_summary.md 2>/dev/null || echo "0")
  if [ "$COUNTERS" -ge 4 ]; then
    check "All 4 posture counters present" "pass"
  else
    check "All 4 posture counters present (found $COUNTERS)" "fail"
  fi
else
  check "last_evolve_summary.md exists" "fail"
fi

# Step 3: Check structured agent log
echo ""
echo "--- Structured Logging ---"
LAST_LOG=$(tail -1 state/agent_log.md)
if echo "$LAST_LOG" | grep -qP 'deep:\d+ scan:\d+ issues:\d+ findings:\d+'; then
  check "Agent log has structured format (deep/scan/issues/findings)" "pass"
else
  # Might be from a different workflow — check last evolve entry
  LAST_EVOLVE_LOG=$(grep "evolve.yml" state/agent_log.md | tail -1)
  if echo "$LAST_EVOLVE_LOG" | grep -qP 'deep:\d+ scan:\d+ issues:\d+ findings:\d+'; then
    check "Agent log has structured format (deep/scan/issues/findings)" "pass"
  else
    check "Agent log has structured format" "fail"
    echo "    Last evolve log: $LAST_EVOLVE_LOG"
  fi
fi

POSTURE_IN_LOG=$(grep "evolve.yml" state/agent_log.md | tail -1 | grep -oP 'PATTERN_HUNT|PIPELINE_WATCH|HORIZON_SCAN|SYNTHESIS' || echo "")
if [ -n "$POSTURE_IN_LOG" ]; then
  check "Agent log has posture name: $POSTURE_IN_LOG" "pass"
else
  check "Agent log has posture name" "fail"
fi

# Step 4: Check research_sources.md updated
echo ""
echo "--- Research Sources ---"
if [ -f state/research_sources.md ]; then
  ACTIVE_COUNT=$(sed -n '/^## Active Sources/,/^## /p' state/research_sources.md | grep -c "^### " 2>/dev/null || echo "0")
  if [ "$ACTIVE_COUNT" -ge 8 ] && [ "$ACTIVE_COUNT" -le 15 ]; then
    check "Active sources in range (8-15): $ACTIVE_COUNT" "pass"
  else
    check "Active sources in range 8-15 (got $ACTIVE_COUNT)" "warn"
  fi

  DEEP_DIVED=$(grep "Last deep:" state/research_sources.md | grep -v "never" | wc -l 2>/dev/null || echo "0")
  if [ "$DEEP_DIVED" -gt 0 ]; then
    check "Some sources have been deep-dived: $DEEP_DIVED" "pass"
  else
    check "At least one source has been deep-dived" "warn"
  fi

  DROPPED_COUNT=$(sed -n '/^## Dropped Sources/,$ p' state/research_sources.md | grep -c "^### " 2>/dev/null || echo "0")
  check "Dropped sources tracked: $DROPPED_COUNT" "pass"
else
  check "research_sources.md exists" "fail"
fi

# Step 5: Check usage log
echo ""
echo "--- Usage Log ---"
LAST_EVOLVE_USAGE=$(grep "| evolve |" state/usage_log.md | tail -1)
if echo "$LAST_EVOLVE_USAGE" | grep -q "posture:"; then
  USAGE_POSTURE=$(echo "$LAST_EVOLVE_USAGE" | grep -oP 'posture:\K\w+' || echo "")
  if [ "$USAGE_POSTURE" != "unknown" ] && [ -n "$USAGE_POSTURE" ]; then
    check "Usage log has posture: $USAGE_POSTURE" "pass"
  else
    check "Usage log posture is 'unknown' — snapshot step may not be working" "warn"
  fi

  if echo "$LAST_EVOLVE_USAGE" | grep -q "issues:"; then
    check "Usage log has issues field" "pass"
  else
    check "Usage log has issues field" "fail"
  fi
else
  check "Usage log has posture field" "fail"
fi

# Step 6: Check research log
echo ""
echo "--- Research Log ---"
RECENT_RESEARCH=$(tail -20 state/research_log.md | grep -c "$(date -u +%Y-%m-%d)" 2>/dev/null || echo "0")
if [ "$RECENT_RESEARCH" -gt 0 ]; then
  check "Research log has entries from today: $RECENT_RESEARCH" "pass"
else
  check "Research log has entries from today" "warn"
fi

# Step 7: Check state files committed
echo ""
echo "--- State Commits ---"
LAST_STATE_COMMIT=$(git log --oneline -5 | grep "state: evolve" | head -1)
if [ -n "$LAST_STATE_COMMIT" ]; then
  check "State commit found: $LAST_STATE_COMMIT" "pass"
else
  check "Recent state commit from evolve" "warn"
fi

# Summary
echo ""
echo "=== Results ==="
echo -e "${GREEN}PASS: $PASS${NC}  ${YELLOW}WARN: $WARN${NC}  ${RED}FAIL: $FAIL${NC}"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo "Some checks failed. Review the output above."
  exit 1
elif [ "$WARN" -gt 0 ]; then
  echo "All critical checks passed. Warnings may resolve after more runs."
  exit 0
else
  echo "All checks passed."
  exit 0
fi
