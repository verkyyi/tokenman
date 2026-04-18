"""onboard exits 2 when a remote catalog skill isn't installed yet."""
from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path


def test_onboard_errors_without_install(tmp_path):
    consumer = tmp_path / "consumer"
    (consumer / ".tokenman").mkdir(parents=True)
    (consumer / ".tokenman" / "tokenman.yaml").write_text(
        textwrap.dedent("""
            skills:
              - readme-maintainer
        """).lstrip()
    )

    env_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable, "-m", "harness.onboard",
            "--repo", str(consumer),
        ],
        cwd=str(consumer),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
    )

    assert result.returncode == 2, result.stderr
    combined = result.stdout + result.stderr
    assert "not installed" in combined
    assert "python -m harness.install" in combined
