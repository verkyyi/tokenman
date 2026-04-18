"""Smoke test for harness/workflows/tokenman.yml.template."""
from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = REPO_ROOT / "harness" / "workflows" / "tokenman.yml.template"


def _load_template() -> dict:
    return yaml.safe_load(TEMPLATE.read_text())


def test_workflow_has_mode_input_with_single_and_onboarding_choices() -> None:
    doc = _load_template()
    on_block = doc.get("on") or doc.get(True)
    assert on_block is not None, "workflow_dispatch block missing"
    inputs = on_block["workflow_dispatch"]["inputs"]
    assert "mode" in inputs
    mode = inputs["mode"]
    assert mode["type"] == "choice"
    assert set(mode["options"]) == {"single", "onboarding"}
    assert mode["default"] == "single"
    assert on_block["schedule"] == [{"cron": "17 9 * * 1"}]


def test_workflow_skill_input_is_optional_now() -> None:
    doc = _load_template()
    on_block = doc.get("on") or doc.get(True)
    inputs = on_block["workflow_dispatch"]["inputs"]
    assert "skill" in inputs
    assert inputs["skill"].get("required") is False


def test_workflow_run_step_branches_on_mode() -> None:
    raw = TEMPLATE.read_text()
    assert 'if [ "${{ inputs.mode }}" = "onboarding" ]' in raw
    assert "python -m harness.install --repo ." in raw
    assert "python -m harness.onboard" in raw
    assert "python -m harness.run" in raw
    assert "--runtime-mode actions" in raw
    assert "npm install -g @anthropic-ai/claude-code" in raw
    assert "exit 1" not in raw


def test_workflow_has_actions_first_concurrency() -> None:
    doc = _load_template()
    concurrency = doc["concurrency"]
    assert concurrency["group"] == "tokenman"
    assert concurrency["cancel-in-progress"] is False
