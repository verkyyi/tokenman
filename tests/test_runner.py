"""Tests for harness.lib.runner."""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from harness.lib import ledger, runner
from harness.lib.pr_opener import FakePROpener, PROpenerError
from harness.lib.skill_executor import StubSkillExecutor


# --- helpers --------------------------------------------------------


def test_count_diff_lines_ignores_file_headers() -> None:
    diff = (
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1,2 +1,3 @@\n"
        " # Title\n"
        "+\n"
        "+new line\n"
        "-old line\n"
    )
    # '+++' and '---' headers are ignored; hunk header has no +/-; three
    # content lines have +/-: "+", "+new line", "-old line".
    assert runner._count_diff_lines(diff) == 3


def test_count_diff_lines_empty() -> None:
    assert runner._count_diff_lines("") == 0


def test_count_diff_lines_no_changes() -> None:
    diff = "--- a/x\n+++ b/x\n@@ -1,1 +1,1 @@\n only context\n"
    assert runner._count_diff_lines(diff) == 0


def test_format_run_id_pads_to_four() -> None:
    assert runner._format_run_id(1) == "r-0001"
    assert runner._format_run_id(42) == "r-0042"
    assert runner._format_run_id(9999) == "r-9999"


def test_iso_utc_seconds_precision_z_suffix() -> None:
    dt = datetime(2026, 4, 18, 12, 0, 0, tzinfo=timezone.utc)
    assert runner._iso_utc(dt) == "2026-04-18T12:00:00Z"


def test_iso_utc_converts_non_utc() -> None:
    from datetime import timedelta, timezone as tz
    dt = datetime(2026, 4, 18, 14, 0, 0, tzinfo=tz(timedelta(hours=2)))
    assert runner._iso_utc(dt) == "2026-04-18T12:00:00Z"


# --- run_skill integration -----------------------------------------


REPO_ROOT = Path(__file__).parent.parent
STUB_SKILL_DIR = REPO_ROOT / "tests" / "fixtures" / "skills" / "stub-readme"
TINY_PYTHON_REPO = REPO_ROOT / "tests" / "fixtures" / "tiny-python-repo"


def _prepare_repo_copy(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Return (repo_dir, ledger_path, runs_dir). Repo is a fresh copy of
    the fixture so fixture files stay pristine.
    """
    repo_dir = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo_dir)
    tokenman_dir = repo_dir / ".tokenman"
    tokenman_dir.mkdir(exist_ok=True)
    ledger_path = tokenman_dir / "ledger.jsonl"
    runs_dir = tokenman_dir / "runs"
    return repo_dir, ledger_path, runs_dir


def _prepare_repo_copy_with_remote(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """Return (repo_dir, ledger_path, runs_dir, remote_dir).

    repo_dir is a fresh copy of the fixture + `git init` + initial commit
    + origin pointing at remote_dir (a bare repo).
    """
    repo_dir = tmp_path / "repo"
    shutil.copytree(TINY_PYTHON_REPO, repo_dir)
    tokenman_dir = repo_dir / ".tokenman"
    tokenman_dir.mkdir(exist_ok=True)
    ledger_path = tokenman_dir / "ledger.jsonl"
    runs_dir = tokenman_dir / "runs"

    remote_dir = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote_dir)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.name",  "seed"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "commit", "-m", "seed"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "remote", "add", "origin", str(remote_dir)], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "push", "-u", "origin", "main"], check=True, capture_output=True)
    return repo_dir, ledger_path, runs_dir, remote_dir


def _fixed_now() -> datetime:
    return datetime(2026, 4, 18, 12, 0, 0, tzinfo=timezone.utc)


def test_run_skill_propose_diff_opens_pr(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir, remote_dir = _prepare_repo_copy_with_remote(tmp_path)
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
    pr_opener = FakePROpener(sink_dir=tmp_path / "prs", start=1000)

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name="stub-readme",
        now=_fixed_now,
    )

    # Returned entry
    assert entry["run_id"] == "r-0001"
    assert entry["status"] == "pr_opened"
    assert entry["pr"] == 1000
    # stub fixture diff has 2 content +/- lines (2x '+'), headers excluded.
    assert entry["generator"]["diff_lines"] == 2
    assert entry["generator"]["prompt_version"] == "stub-v1"
    assert entry["generator"]["tokens"] == 0
    assert entry["evaluator"] is None
    assert entry["total_tokens"] == 0

    # Ledger file
    lines = ledger_path.read_text().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == entry

    # Artifact dir
    art = runs_dir / "r-0001"
    assert (art / "proposed.diff").is_file()
    assert (art / "proposed.md").is_file()
    assert (art / "executor.stdout").is_file()
    assert (art / "executor.stderr").is_file()
    assert (art / "ledger.entry").is_file()
    assert json.loads((art / "ledger.entry").read_text()) == entry

    # PR opener invoked exactly once
    assert len(pr_opener.calls) == 1
    call = pr_opener.calls[0]
    assert call["branch"] == "tokenman/stub-readme/r-0001"
    diff_on_disk = (runs_dir / "r-0001" / "proposed.diff").read_text()
    assert "Stub-readme added this line" in diff_on_disk

    # Branch exists on origin (bare remote)
    ls = subprocess.run(
        ["git", "ls-remote", str(remote_dir), "refs/heads/tokenman/stub-readme/r-0001"],
        capture_output=True, text=True, check=True,
    )
    assert "tokenman/stub-readme/r-0001" in ls.stdout


def test_run_skill_no_change_skips_pr_opener(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    pr_opener = FakePROpener(sink_dir=tmp_path / "prs", start=1000)

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name="stub-readme",
        now=_fixed_now,
    )

    assert entry["status"] == "no_change"
    assert entry["pr"] is None
    assert entry["generator"]["diff_lines"] == 0
    assert entry["generator"]["prompt_version"] == "stub-v1"
    assert entry["generator"]["tokens"] == 0
    assert entry["total_tokens"] == 0
    assert pr_opener.calls == []

    art = runs_dir / "r-0001"
    assert not (art / "proposed.diff").exists()
    assert not (art / "proposed.md").exists()
    assert (art / "executor.stdout").is_file()
    assert (art / "executor.stderr").is_file()
    assert (art / "ledger.entry").is_file()


def test_run_skill_crash_records_error(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "crash"})
    pr_opener = FakePROpener()

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name="stub-readme",
        now=_fixed_now,
    )

    assert entry["status"] == "error"
    assert entry["generator"] is None
    assert entry["pr"] is None
    assert entry["total_tokens"] == 0
    assert pr_opener.calls == []

    art = runs_dir / "r-0001"
    assert (art / "executor.stdout").is_file()
    stderr_content = (art / "executor.stderr").read_text()
    assert "crashing on purpose" in stderr_content
    assert (art / "ledger.entry").is_file()

    # Ledger entry validates against the schema (sanity via re-parse).
    lines = ledger_path.read_text().splitlines()
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed == entry


def test_run_skill_allocates_r0001_on_empty_ledger(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)
    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    pr_opener = FakePROpener()

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        now=_fixed_now,
    )
    assert entry["run_id"] == "r-0001"


def test_run_skill_increments_from_existing_ledger(tmp_path: Path) -> None:
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)

    # Seed with r-0017 by hand-appending via ledger.append.
    seed = {
        "run_id": "r-0017",
        "ts": "2026-04-18T11:00:00Z",
        "skill": "stub-readme",
        "status": "no_change",
        "pr": None,
        "generator": {
            "prompt_version": "stub-v1",
            "output_summary": "seed",
            "diff_lines": 0,
            "tokens": 0,
        },
        "evaluator": None,
        "duration_s": 0,
        "total_tokens": 0,
        "verdict": None,
        "verdict_note": None,
    }
    ledger.append(ledger_path, seed)

    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    pr_opener = FakePROpener()
    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        now=_fixed_now,
    )
    assert entry["run_id"] == "r-0018"
    assert ledger.last_run_id(ledger_path) == 18


def test_run_skill_leaves_no_ledger_entry_on_append_failure(tmp_path: Path) -> None:
    """If ledger.append raises (here: ts monotonicity), the runner
    propagates the exception, the ledger file is unchanged, and the
    per-run ledger.entry file is absent (but subprocess artifacts
    still exist because the skill ran).
    """
    repo_dir, ledger_path, runs_dir = _prepare_repo_copy(tmp_path)

    # Seed ledger with a future-dated entry so our fixed now() goes
    # backward and trips invariant 5.
    future = {
        "run_id": "r-0001",
        "ts": "2099-01-01T00:00:00Z",
        "skill": "stub-readme",
        "status": "no_change",
        "pr": None,
        "generator": {
            "prompt_version": "stub-v1",
            "output_summary": "seed",
            "diff_lines": 0,
            "tokens": 0,
        },
        "evaluator": None,
        "duration_s": 0,
        "total_tokens": 0,
        "verdict": None,
        "verdict_note": None,
    }
    ledger.append(ledger_path, future)
    before = ledger_path.read_text()

    executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
    pr_opener = FakePROpener()
    with pytest.raises(ledger.LedgerInvariantError, match="ts"):
        runner.run_skill(
            skill_dir=STUB_SKILL_DIR,
            repo_dir=repo_dir,
            ledger_path=ledger_path,
            runs_dir=runs_dir,
            executor=executor,
            pr_opener=pr_opener,
            now=_fixed_now,  # 2026 — before 2099
        )

    # Ledger unchanged
    assert ledger_path.read_text() == before

    # Artifacts present (subprocess did run), but per-run ledger.entry absent.
    art = runs_dir / "r-0002"
    assert (art / "executor.stdout").is_file()
    assert (art / "executor.stderr").is_file()
    assert not (art / "ledger.entry").exists()


def test_run_skill_records_error_when_pr_opener_raises(tmp_path: Path) -> None:
    """If pr_opener.open() raises, the runner converts the run to an
    error outcome rather than crashing: status=error, generator=None,
    pr=None, stderr captures the traceback, ledger has exactly one entry.
    """
    repo_dir, ledger_path, runs_dir, _remote_dir = _prepare_repo_copy_with_remote(tmp_path)

    class BrokenPROpener:
        def open(self, *, title, body, branch):
            raise PROpenerError("boom")

    executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
    pr_opener = BrokenPROpener()

    entry = runner.run_skill(
        skill_dir=STUB_SKILL_DIR,
        repo_dir=repo_dir,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name="stub-readme",
        now=_fixed_now,
    )

    assert entry["status"] == "error"
    assert entry["generator"] is None
    assert entry["pr"] is None
    assert entry["total_tokens"] == 0

    # Single ledger line, matches the returned entry.
    lines = ledger_path.read_text().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == entry

    # Artifacts: proposed.diff was copied (subprocess succeeded before PR
    # opener ran), stderr captures the failure message and traceback.
    art = runs_dir / "r-0001"
    assert (art / "proposed.diff").is_file()
    stderr_content = (art / "executor.stderr").read_text()
    assert "git/pr_opener failed: boom" in stderr_content
    assert "PROpenerError" in stderr_content
