"""Replays a recorded `claude -p --output-format json` stdout through
ClaudeSkillExecutor._parse_json_output. Guards the parser against
JSON-shape drift without spending real tokens.
"""
from __future__ import annotations

import json
from pathlib import Path

from harness.lib.skill_executor import ClaudeSkillExecutor


CAPTURE_PATH = (
    Path(__file__).parent / "fixtures" / "claude-captures" / "readme-maintainer.json"
)


def test_parse_real_or_synthetic_capture() -> None:
    raw = CAPTURE_PATH.read_text()
    summary, tokens = ClaudeSkillExecutor._parse_json_output(raw, exit_code=0)

    # The capture is either synthetic (see Task 25 Step 2) or real, but in
    # either case the following invariants must hold.
    assert isinstance(summary, str) and summary.strip(), "summary must be non-empty string"
    assert tokens > 0, "tokens must be positive for a real/synthetic capture"

    # The usage block should have been consumable.
    doc = json.loads(raw)
    usage = doc.get("usage", {})
    expected = (
        int(usage.get("input_tokens", 0))
        + int(usage.get("output_tokens", 0))
        + int(usage.get("cache_creation_input_tokens", 0))
        + int(usage.get("cache_read_input_tokens", 0))
    )
    assert tokens == expected
