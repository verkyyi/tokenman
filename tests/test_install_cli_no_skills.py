"""`python -m harness.install` with no enabled skills exits 2 with a hint."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_no_skills_exits_2(tmp_path):
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    # No --skill flag, no tokenman.yaml.

    env_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "harness.install", "--repo", str(consumer)],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 2
    assert "no skills" in result.stderr.lower()
    assert "harness.scope" in result.stderr or "--skill" in result.stderr
