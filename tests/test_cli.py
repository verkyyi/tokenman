"""End-to-end test for the harness.run CLI (subprocess invocation)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import harness.run.__main__ as run_main


REPO_ROOT = Path(__file__).parent.parent
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def _seed_git_repo(repo: Path, remote: Path) -> None:
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name",  "seed"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "seed"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True)
    subprocess.run(["git", "-C", str(repo), "push", "-u", "origin", "main"], check=True, capture_output=True)


def test_cli_dry_run_produces_ledger_entry(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo)
    remote = tmp_path / "remote.git"
    _seed_git_repo(repo, remote)

    env = {**os.environ}
    proc = subprocess.run(
        [
            sys.executable, "-m", "harness.run",
            "--skill", "readme-maintainer",
            "--repo", str(repo),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(REPO_ROOT),
    )

    assert proc.returncode == 0, f"stderr: {proc.stderr}"

    ledger_path = repo / ".tokenman" / "ledger.jsonl"
    assert ledger_path.is_file(), "ledger file must be created"
    lines = [ln for ln in ledger_path.read_text().splitlines() if ln.strip()]
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["run_id"] == "r-0001"
    assert entry["skill"] == "readme-maintainer"
    assert entry["status"] in {"pr_opened", "no_change"}

    # stdout ends with the compact JSON entry
    last_stdout_line = [ln for ln in proc.stdout.splitlines() if ln.strip()][-1]
    assert json.loads(last_stdout_line) == entry


def test_cli_unknown_skill_exits_nonzero(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable, "-m", "harness.run",
            "--skill", "does-not-exist",
            "--repo", str(tmp_path),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert proc.returncode != 0
    assert "does-not-exist" in proc.stderr


def test_run_main_returns_nonzero_when_runner_reports_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(run_main.catalog, "tokenman_root", lambda: REPO_ROOT)
    monkeypatch.setattr(
        run_main.catalog,
        "load_catalog",
        lambda _root: {"readme-maintainer": {"source": "x", "version": "v"}},
    )
    monkeypatch.setattr(
        run_main.runner,
        "run_skill",
        lambda **_kwargs: {
            "run_id": "r-0001",
            "ts": "2026-04-18T00:00:00Z",
            "skill": "readme-maintainer",
            "status": "error",
            "pr": None,
            "issue": None,
            "generator": {
                "prompt_version": "harness-v1",
                "output_summary": "failed",
                "diff_lines": 0,
                "tokens": 0,
            },
            "evaluator": None,
            "duration_s": 0,
            "total_tokens": 0,
            "verdict": None,
            "verdict_note": None,
        },
    )

    code = run_main.main(
        ["--skill", "readme-maintainer", "--repo", str(tmp_path), "--dry-run"]
    )
    assert code == 1
