"""Smoke test for harness/workflows/tokenman.yml.template.

Loads the template as YAML and asserts the Phase 1.4 mode input is
present and the run step branches on it.
"""
from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = REPO_ROOT / "harness" / "workflows" / "tokenman.yml.template"


def _load_template() -> dict:
    return yaml.safe_load(TEMPLATE.read_text())


def test_workflow_has_mode_input_with_single_and_onboarding_choices() -> None:
    doc = _load_template()
    # PyYAML may parse the `on` key as boolean True — the workflow YAML
    # uses bare `on:`. Handle both.
    on_block = doc.get("on") or doc.get(True)
    assert on_block is not None, "workflow_dispatch block missing"
    inputs = on_block["workflow_dispatch"]["inputs"]
    assert "mode" in inputs
    mode = inputs["mode"]
    assert mode["type"] == "choice"
    assert set(mode["options"]) == {"single", "onboarding"}
    assert mode["default"] == "single"


def test_workflow_skill_input_is_optional_now() -> None:
    doc = _load_template()
    on_block = doc.get("on") or doc.get(True)
    inputs = on_block["workflow_dispatch"]["inputs"]
    assert "skill" in inputs
    assert inputs["skill"].get("required") is False


def test_workflow_run_step_branches_on_mode() -> None:
    raw = TEMPLATE.read_text()
    assert 'if [ "${{ inputs.mode }}" = "onboarding" ]' in raw
    assert "python -m harness.onboard" in raw
    assert "python -m harness.run" in raw
    assert "--runtime-mode actions" in raw
