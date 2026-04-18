"""Live test for `python -m harness.scope`. Gated by TOKENMAN_LIVE=1."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


pytestmark = pytest.mark.skipif(
    os.environ.get("TOKENMAN_LIVE") != "1",
    reason="set TOKENMAN_LIVE=1 to run live claude -p scoping test",
)


def test_scope_live_against_tiny_repo(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "seed"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "seed"],
        check=True, capture_output=True,
    )

    out_path = tmp_path / "initial-scope.md"
    proc = subprocess.run(
        [sys.executable, "-m", "harness.scope",
         "--repo", str(repo),
         "--output-path", str(out_path),
         "--non-interactive"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=180,
    )
    assert proc.returncode == 0, f"stderr: {proc.stderr}\nstdout: {proc.stdout}"
    content = out_path.read_text()
    assert "# Tokenman — Initial scope for" in content
    assert "## Recommended skills" in content
    assert "## Suggested boundaries" in content
