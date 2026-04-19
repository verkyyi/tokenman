"""Tests for the public action manifest."""
from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
ACTION = REPO_ROOT / "action.yml"


def _load_action() -> dict:
    return yaml.safe_load(ACTION.read_text())


def test_action_requires_scope_inputs() -> None:
    doc = _load_action()
    inputs = doc["inputs"]
    assert inputs["github_token"]["required"] is True
    assert inputs["read_paths"]["required"] is True
    assert inputs["write_paths"]["required"] is True


def test_action_defaults_match_mvp_spec() -> None:
    doc = _load_action()
    inputs = doc["inputs"]
    assert inputs["job_type"]["default"] == "docs_maintainer"
    assert inputs["on_high_confidence"]["default"] == "pull_request"
    assert inputs["on_low_confidence"]["default"] == "issue"


def test_action_exports_routing_outputs() -> None:
    doc = _load_action()
    outputs = doc["outputs"]
    assert set(outputs) >= {"outcome", "status", "run_id", "pr_number", "issue_number"}


def test_action_uploads_run_artifacts() -> None:
    raw = ACTION.read_text()
    assert "actions/upload-artifact@v4" in raw
    assert ".tokenman/runs/" in raw


def test_action_wraps_official_claude_code_action() -> None:
    raw = ACTION.read_text()
    assert "uses: anthropics/claude-code-action@v1" in raw
    assert "structured_output" in raw
    assert "Tokenman preflight" in raw
