#!/usr/bin/env bash
# status.sh — human-readable summary of .tokenman/ledger.jsonl
#
# Usage:  bash scripts/status.sh [ledger-path]
# Default: .tokenman/ledger.jsonl
#
# Dependencies: jq, tac (standard on Linux), date.
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

LINES=$(wc -l < "$LEDGER" | tr -d ' ')

echo "== tokenman status =="
printf "ledger  : %s\n" "$LEDGER"
printf "entries : %s\n" "$LINES"
echo

echo "== last 10 runs (newest first) =="
printf "%-22s %-24s %-10s %-22s %12s\n" "timestamp" "skill" "status" "reason" "tokens"
printf "%-22s %-24s %-10s %-22s %12s\n" "----------------------" "------------------------" "----------" "----------------------" "------------"
tail -10 "$LEDGER" | tac | while read -r line; do
    [ -n "$line" ] || continue
    ts=$(     echo "$line" | jq -r '.ts')
    skill=$(  echo "$line" | jq -r '.skill')
    status=$( echo "$line" | jq -r '.status')
    reason=$( echo "$line" | jq -r '.reason // ""')
    tokens=$( echo "$line" | jq -r '(.input_tokens // 0) + (.output_tokens // 0)')
    printf "%-22s %-24s %-10s %-22s %12d\n" "$ts" "$skill" "$status" "$reason" "$tokens"
done
echo

CUTOFF=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)
echo "== 7-day totals (since $CUTOFF) =="
jq -sr --arg cutoff "$CUTOFF" '
    map(select(.ts >= $cutoff)) as $r
    | "runs=\($r | length)  prs_opened=\($r | map(select(.pr_number != null)) | length)  success=\($r | map(select(.status == "success")) | length)  skip=\($r | map(select(.status == "skip")) | length)  abort=\($r | map(select(.status == "abort")) | length)  tokens=\($r | map((.input_tokens // 0) + (.output_tokens // 0)) | add // 0)  lines_deleted=\($r | map(.lines_deleted // 0) | add // 0)"
' "$LEDGER"
echo

echo "== per-skill breakdown (all time) =="
jq -sr '
    group_by(.skill)
    | .[]
    | "- \(.[0].skill):  runs=\(length)  success=\(map(select(.status == "success")) | length)  skip=\(map(select(.status == "skip")) | length)  abort=\(map(select(.status == "abort")) | length)  prs=\(map(select(.pr_number != null)) | length)  tokens=\(map((.input_tokens // 0) + (.output_tokens // 0)) | add // 0)  lines_deleted=\(map(.lines_deleted // 0) | add // 0)"
' "$LEDGER"
