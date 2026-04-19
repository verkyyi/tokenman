"""Smoke test for the public workflow template."""
from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = REPO_ROOT / "harness" / "workflows" / "tokenman.yml.template"


def _load_template() -> dict:
    return yaml.safe_load(TEMPLATE.read_text())


def test_workflow_has_push_and_manual_triggers() -> None:
    doc = _load_template()
    on_block = doc.get("on") or doc.get(True)
    assert on_block is not None
    assert "push" in on_block
    assert "workflow_dispatch" in on_block
    assert on_block["push"]["branches"] == ["main"]
    assert "services/payments/**" in on_block["push"]["paths"]
    assert "openapi/payments.yaml" in on_block["push"]["paths"]


def test_workflow_uses_public_action_surface() -> None:
    raw = TEMPLATE.read_text()
    assert "uses: your-org/tokenman@v1" in raw
    assert "github_token: ${{ secrets.GITHUB_TOKEN }}" in raw
    assert "read_paths:" in raw
    assert "write_paths:" in raw
    assert "on_high_confidence: pull_request" in raw
    assert "on_low_confidence: issue" in raw


def test_workflow_requests_issue_permissions() -> None:
    doc = _load_template()
    permissions = doc["jobs"]["docs-maintainer"]["permissions"]
    assert permissions["contents"] == "write"
    assert permissions["pull-requests"] == "write"
    assert permissions["issues"] == "write"
