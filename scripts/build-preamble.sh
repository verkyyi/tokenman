#!/usr/bin/env bash
# build-preamble.sh — Tiered context assembly for workflow prompts
# Usage: ./scripts/build-preamble.sh <tier> [output_file]
#   tier: 1-4 (see skills/README.md for tier definitions)
#   output_file: optional, defaults to stdout
#
# Tiers:
#   T1 (minimal):  learned_rules + evolve_config
#   T2 (standard): T1 + autonomy rules (CLAUDE.md) + project_state
#   T3 (extended): T2 + full CLAUDE.md + project CLAUDE.md + agent_log
#   T4 (full):     T3 + research_sources + research_log + last_evolve_summary

set -euo pipefail

TIER="${1:?Usage: build-preamble.sh <tier> [output_file]}"
OUTPUT="${2:-/dev/stdout}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ".")"

# Resolve project CLAUDE.md path from evolve_config
PROJECT_CLAUDE=""
if [ -f "$REPO_ROOT/state/evolve_config.md" ]; then
  PROJECT_CLAUDE=$(grep '^CLAUDE.md:' "$REPO_ROOT/state/evolve_config.md" | cut -d' ' -f2 || true)
fi

{
  # --- T1: Minimal (learned_rules + evolve_config) ---
  echo "## Evolve Config"
  cat "$REPO_ROOT/state/evolve_config.md" 2>/dev/null || echo "(not found)"
  echo ""
  echo "Use the Build section for install/build/test commands. Do NOT assume npm."
  echo "Read CLAUDE.md from the path in the Project section of the config."
  echo ""
  echo "## Learned Rules (from human feedback — MUST follow these)"
  cat "$REPO_ROOT/state/learned_rules.md" 2>/dev/null || echo "(not found)"
  echo ""

  if [ "$TIER" -ge 2 ]; then
    # --- T2: Standard (T1 + project_state) ---
    echo "## Current Project State"
    cat "$REPO_ROOT/state/project_state.md" 2>/dev/null || echo "(not found)"
    echo ""
  fi

  if [ "$TIER" -ge 3 ]; then
    # --- T3: Extended (T2 + full CLAUDE.md + project CLAUDE.md + agent_log) ---
    echo "## CLAUDE.md (root)"
    cat "$REPO_ROOT/CLAUDE.md" 2>/dev/null || echo "(not found)"
    echo ""
    if [ -n "$PROJECT_CLAUDE" ] && [ -f "$REPO_ROOT/$PROJECT_CLAUDE" ]; then
      echo "## Project CLAUDE.md"
      cat "$REPO_ROOT/$PROJECT_CLAUDE" 2>/dev/null || echo "(not found)"
      echo ""
    fi
    echo "## Recent Agent Log (last 30 lines)"
    tail -30 "$REPO_ROOT/state/agent_log.md" 2>/dev/null || echo "(not found)"
    echo ""
  fi

  if [ "$TIER" -ge 4 ]; then
    # --- T4: Full (T3 + research_sources + research_log + last_evolve_summary) ---
    echo "## Research Sources"
    cat "$REPO_ROOT/state/research_sources.md" 2>/dev/null || echo "(not found)"
    echo ""
    echo "## Recent Research Log (last 15 lines)"
    tail -15 "$REPO_ROOT/state/research_log.md" 2>/dev/null || echo "(not found)"
    echo ""
    echo "## Previous Evolve Run Summary"
    cat "$REPO_ROOT/state/last_evolve_summary.md" 2>/dev/null || echo "(not found)"
    echo ""
    echo "## Failure Log"
    grep "^# [0-9]" "$REPO_ROOT/CLAUDE.md" 2>/dev/null | tail -20 || echo "(none)"
    echo ""
  fi
} > "$OUTPUT"
