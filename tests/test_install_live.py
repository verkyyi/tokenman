"""Opt-in live test — clones the real readme-maintainer repo.

Enable with TOKENMAN_LIVE=1. Skipped by default to keep the default
test run hermetic.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


pytestmark = pytest.mark.live


def test_install_readme_maintainer_live(tmp_path):
    consumer = tmp_path / "consumer"
    consumer.mkdir()

    env_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable, "-m", "harness.install",
            "--repo", str(consumer),
            "--skill", "readme-maintainer",
        ],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr

    target = consumer / ".claude" / "skills" / "readme-maintainer"
    assert (target / "SKILL.md").is_file()
    lock = json.loads((target / ".tokenman-skill-lock").read_text())
    assert lock["version"] == "v0.1.0"
    assert lock["source"] == "https://github.com/verkyyi/readme-maintainer-skill"

    # Idempotent re-run.
    second = subprocess.run(
        [
            sys.executable, "-m", "harness.install",
            "--repo", str(consumer),
            "--skill", "readme-maintainer",
        ],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
        timeout=60,
    )
    assert second.returncode == 0, second.stderr
    assert "unchanged" in second.stdout
