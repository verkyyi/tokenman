"""Smoke tests for `python -m harness.install`."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def _run_cli(*, cwd: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    env_root = Path(__file__).resolve().parents[1]
    return subprocess.run(
        [sys.executable, "-m", "harness.install", *args],
        cwd=str(cwd),
        env={**os.environ, "PYTHONPATH": str(env_root)},
        capture_output=True, text=True, check=False,
    )


def test_cli_installs_and_is_idempotent(tmp_path, build_local_git_repo, fake_skill_source):
    remote = build_local_git_repo(fake_skill_source)
    catalog_path = tmp_path / "lib" / "recommended-skills.yaml"
    _write(
        catalog_path,
        textwrap.dedent(f"""
            fake-skill:
              source: file://{remote}
              version: v0.1.0
        """).lstrip(),
    )
    consumer = tmp_path / "consumer"
    consumer.mkdir()

    first = _run_cli(
        cwd=consumer,
        args=[
            "--repo", str(consumer),
            "--catalog-path", str(catalog_path),
            "--skill", "fake-skill",
        ],
    )
    assert first.returncode == 0, first.stderr
    assert "installed" in first.stdout
    target = consumer / ".claude" / "skills" / "fake-skill"
    assert (target / "SKILL.md").is_file()
    lock = json.loads((target / ".tokenman-skill-lock").read_text())
    assert lock["version"] == "v0.1.0"

    second = _run_cli(
        cwd=consumer,
        args=[
            "--repo", str(consumer),
            "--catalog-path", str(catalog_path),
            "--skill", "fake-skill",
        ],
    )
    assert second.returncode == 0, second.stderr
    assert "unchanged" in second.stdout
