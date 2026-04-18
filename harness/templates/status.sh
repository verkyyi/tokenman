#!/usr/bin/env bash
# status.sh — human-readable summary of .tokenman/ledger.jsonl (v1)
#
# Phase 1.1 of docs/spec.md §12. Ledger-only reader — no GitHub API,
# no config read, no cap %. /tokenman init copies this file into a
# consumer's .tokenman/status.sh at install time.
#
# Usage:  bash status.sh [ledger-path]
# Default ledger-path: .tokenman/ledger.jsonl
#
# Dependencies: jq, standard POSIX tools.
set -euo pipefail

LEDGER="${1:-.tokenman/ledger.jsonl}"

if [ ! -f "$LEDGER" ]; then
    echo "No ledger at $LEDGER (no tokenman runs yet)."
    exit 0
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "status.sh requires jq. Install it first: apt install jq / brew install jq."
    exit 1
fi

LINES=$(grep -cv '^[[:space:]]*$' "$LEDGER" 2>/dev/null || true)
LINES="${LINES:-0}"

if [ "$LINES" -eq 0 ]; then
    echo "Ledger $LEDGER is empty (no tokenman runs yet)."
    exit 0
fi

echo "Tokenman status"
echo
printf "Ledger:  %s  (%s entries)\n" "$LEDGER" "$LINES"
echo

# --- Summary (all time) ------------------------------------------------
# jq computes counts + sums; bash printf handles alignment.
# -s slurps all JSONL entries into one array; -r emits raw (no JSON-string
# quoting) so @tsv produces a literal tab-separated line.
counts=$(jq -sr '[
    length,
    (map(select(.status == "pr_opened"))                | length),
    (map(select(.status == "no_change"))                | length),
    (map(select(.status | startswith("skipped_")))      | length),
    (map(select(.status | startswith("aborted_")))      | length),
    (map(select(.status == "error"))                    | length),
    (map(.total_tokens) | add // 0),
    (map(select(.status == "skipped_lock"))             | length),
    (map(select(.status == "skipped_cooldown"))         | length),
    (map(select(.status == "skipped_budget"))           | length),
    (map(select(.status == "skipped_pause"))            | length),
    (map(select(.status == "skipped_review_bandwidth")) | length)
] | @tsv' "$LEDGER")

read -r total prs nochg skipped aborted errors tokens sk_lock sk_cd sk_bd sk_ps sk_rb <<< "$counts"

avg=0
if [ "$total" -gt 0 ]; then
    avg=$(( tokens / total ))
fi

echo "Summary (all time):"
printf "  Runs:          %3d\n" "$total"
printf "  PRs opened:    %3d\n" "$prs"
printf "  No-change:     %3d\n" "$nochg"
printf "  Skipped:       %3d  (lock: %d, cooldown: %d, budget: %d, pause: %d, review-bandwidth: %d)\n" \
    "$skipped" "$sk_lock" "$sk_cd" "$sk_bd" "$sk_ps" "$sk_rb"
printf "  Aborted:       %3d\n" "$aborted"
printf "  Errors:        %3d\n" "$errors"
printf "  Tokens:   %8d  (avg %d/run)\n" "$tokens" "$avg"
echo

# --- Top skills (all time) ---------------------------------------------
echo "Top skills (all time):"
jq -sr '
    group_by(.skill)
    | map({
        skill: .[0].skill,
        tokens: (map(.total_tokens) | add // 0),
        runs:   length,
        prs:    (map(select(.status == "pr_opened")) | length)
      })
    | sort_by(-.tokens)
    | .[]
    | [.skill, .tokens, .runs, .prs]
    | @tsv
' "$LEDGER" | while IFS=$'\t' read -r skill tokens runs prs; do
    printf "  %-20s  %7d tok   %d runs  %d PRs\n" "$skill" "$tokens" "$runs" "$prs"
done
echo

# --- Last 10 runs (newest first) ---------------------------------------
echo "Last 10 runs (newest first):"
jq -sr '
    sort_by(.ts)
    | reverse
    | .[0:10]
    | .[]
    | [.run_id, .ts, .skill, .status, .total_tokens]
    | @tsv
' "$LEDGER" | while IFS=$'\t' read -r run_id ts skill status tokens; do
    printf "  %s  %s  %-20s  %-17s %6d\n" "$run_id" "$ts" "$skill" "$status" "$tokens"
done
