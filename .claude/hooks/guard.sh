#!/bin/bash
# PreToolUse guardrail hook: deterministic enforcement of CLAUDE.md NEVER rules.
# Reads deny rules from state/guardrail_policy.json and checks tool name + arguments.
# Fail-closed: if policy file is missing or any error occurs, block the call.
set -euo pipefail

# Resolve repo root (script lives in .claude/hooks/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
POLICY_FILE="$REPO_ROOT/state/guardrail_policy.json"

# Read hook input from stdin (JSON with tool_name, tool_input, etc.)
INPUT=$(cat)

# Fail-closed: policy file must exist and be valid JSON
if [ ! -f "$POLICY_FILE" ]; then
  echo "BLOCKED: guardrail policy file missing at $POLICY_FILE" >&2
  exit 2
fi

if ! jq empty "$POLICY_FILE" 2>/dev/null; then
  echo "BLOCKED: guardrail policy file is not valid JSON" >&2
  exit 2
fi

# Extract tool name from hook input
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
if [ -z "$TOOL_NAME" ]; then
  # No tool name in input — allow (not a tool call we can check)
  exit 0
fi

# Extract tool input as a JSON object
TOOL_INPUT=$(echo "$INPUT" | jq -c '.tool_input // {}')

# Check each deny rule in the policy
RULE_COUNT=$(jq '.deny_rules | length' "$POLICY_FILE")

for ((i = 0; i < RULE_COUNT; i++)); do
  RULE_TOOL=$(jq -r ".deny_rules[$i].tool" "$POLICY_FILE")

  # Skip rules that don't match the current tool
  if [ "$RULE_TOOL" != "$TOOL_NAME" ]; then
    continue
  fi

  RULE_ID=$(jq -r ".deny_rules[$i].id" "$POLICY_FILE")
  RULE_DESC=$(jq -r ".deny_rules[$i].description" "$POLICY_FILE")
  ARG_FIELD=$(jq -r ".deny_rules[$i].arg_field" "$POLICY_FILE")

  # Extract the value of the argument field to check
  ARG_VALUE=$(echo "$TOOL_INPUT" | jq -r ".$ARG_FIELD // empty")
  if [ -z "$ARG_VALUE" ]; then
    continue
  fi

  # Check each pattern in the rule
  PATTERN_COUNT=$(jq ".deny_rules[$i].patterns | length" "$POLICY_FILE")
  for ((j = 0; j < PATTERN_COUNT; j++)); do
    PATTERN=$(jq -r ".deny_rules[$i].patterns[$j]" "$POLICY_FILE")

    if echo "$ARG_VALUE" | grep -qPi "$PATTERN"; then
      echo "BLOCKED by guardrail [$RULE_ID]: $RULE_DESC (pattern: $PATTERN)" >&2
      exit 2
    fi
  done
done

# All rules passed — allow the tool call
exit 0
