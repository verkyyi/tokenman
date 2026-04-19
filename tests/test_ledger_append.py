"""Tests for harness.lib.ledger — schema validation, invariants, append."""
from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path

import pytest

from harness.lib import ledger


# A known-valid Phase 1 entry used as the base for variant tests below.
VALID_PR_OPENED: dict = {
    "run_id": "r-0001",
    "ts": "2026-04-18T12:00:00Z",
    "skill": "stub-readme",
    "status": "pr_opened",
    "pr": 1000,
    "issue": None,
    "generator": {
        "prompt_version": "stub-v1",
        "output_summary": "proposed 1 diff",
        "diff_lines": 3,
        "tokens": 0,
    },
    "evaluator": None,
    "duration_s": 0,
    "total_tokens": 0,
    "verdict": None,
    "verdict_note": None,
}


def test_validate_accepts_canonical_entry() -> None:
    ledger.validate(copy.deepcopy(VALID_PR_OPENED))


def test_validate_rejects_entry_missing_required_field() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    del bad["run_id"]
    with pytest.raises(ledger.LedgerInvariantError):
        ledger.validate(bad)


def test_validate_rejects_bad_run_id_pattern() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["run_id"] = "r-1"
    with pytest.raises(ledger.LedgerInvariantError):
        ledger.validate(bad)


def test_last_run_id_missing_file(tmp_path: Path) -> None:
    assert ledger.last_run_id(tmp_path / "nope.jsonl") is None


def test_last_run_id_empty_file(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    p.write_text("")
    assert ledger.last_run_id(p) is None


def test_last_run_id_blank_lines_only(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    p.write_text("\n\n   \n")
    assert ledger.last_run_id(p) is None


def test_last_run_id_returns_integer_portion(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    entry = copy.deepcopy(VALID_PR_OPENED)
    entry["run_id"] = "r-0042"
    p.write_text(json.dumps(entry) + "\n")
    assert ledger.last_run_id(p) == 42


def test_last_run_id_uses_last_non_blank_line(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    e1 = copy.deepcopy(VALID_PR_OPENED)
    e1["run_id"] = "r-0001"
    e2 = copy.deepcopy(VALID_PR_OPENED)
    e2["run_id"] = "r-0002"
    e2["ts"] = "2026-04-18T12:00:01Z"
    e2["pr"] = 1001
    p.write_text(json.dumps(e1) + "\n" + json.dumps(e2) + "\n\n")
    assert ledger.last_run_id(p) == 2


def test_append_to_missing_ledger_creates_file(tmp_path: Path) -> None:
    p = tmp_path / "sub" / "ledger.jsonl"
    entry = copy.deepcopy(VALID_PR_OPENED)
    ledger.append(p, entry)
    assert p.is_file()
    lines = p.read_text().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == entry


def test_append_appends_without_clobber(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    e1 = copy.deepcopy(VALID_PR_OPENED)
    e1["run_id"] = "r-0001"
    e2 = copy.deepcopy(VALID_PR_OPENED)
    e2["run_id"] = "r-0002"
    e2["ts"] = "2026-04-18T12:00:01Z"
    e2["pr"] = 1001
    ledger.append(p, e1)
    ledger.append(p, e2)
    lines = p.read_text().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["run_id"] == "r-0001"
    assert json.loads(lines[1])["run_id"] == "r-0002"


def test_append_leaves_file_unchanged_on_validation_failure(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    e1 = copy.deepcopy(VALID_PR_OPENED)
    ledger.append(p, e1)
    before = p.read_text()
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["run_id"] = "not-a-run-id"
    with pytest.raises(ledger.LedgerInvariantError):
        ledger.append(p, bad)
    assert p.read_text() == before


def test_invariant_pr_non_null_without_pr_opened_rejected() -> None:
    # Use status='error' so the generator null-ness invariant (Task 6) does
    # not also fire; this test isolates invariant 1.
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "error"
    bad["pr"] = 42
    with pytest.raises(ledger.LedgerInvariantError, match="pr"):
        ledger.validate(bad)


def test_invariant_issue_non_null_without_issue_opened_rejected() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["issue"] = 42
    with pytest.raises(ledger.LedgerInvariantError, match="issue"):
        ledger.validate(bad)


def test_invariant_issue_opened_requires_issue_number() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "issue_opened"
    bad["pr"] = None
    bad["issue"] = None
    with pytest.raises(ledger.LedgerInvariantError, match="issue"):
        ledger.validate(bad)


def test_invariant_issue_opened_accepts_issue_number() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "issue_opened"
    ok["pr"] = None
    ok["issue"] = 77
    ledger.validate(ok)


def test_invariant_pr_null_with_pr_opened_rejected() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["pr"] = None
    with pytest.raises(ledger.LedgerInvariantError, match="pr"):
        ledger.validate(bad)


def test_invariant_generator_must_be_null_on_skipped_status() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "skipped_cooldown"
    bad["pr"] = None
    # generator still populated → violation
    with pytest.raises(ledger.LedgerInvariantError, match="generator"):
        ledger.validate(bad)


def test_invariant_generator_must_be_populated_on_no_change() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["status"] = "no_change"
    bad["pr"] = None
    bad["generator"] = None
    with pytest.raises(ledger.LedgerInvariantError, match="generator"):
        ledger.validate(bad)


def test_invariant_generator_null_on_error_accepted() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "error"
    ok["pr"] = None
    ok["issue"] = None
    ok["generator"] = None
    ok["total_tokens"] = 0
    ledger.validate(ok)  # must not raise


def test_invariant_generator_populated_on_error_accepted() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "error"
    ok["pr"] = None
    ok["issue"] = None
    # generator stays populated; total_tokens already matches 0
    ledger.validate(ok)  # must not raise


def test_invariant_generator_null_on_skipped_without_pr_accepted() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "skipped_pause"
    ok["pr"] = None
    ok["issue"] = None
    ok["generator"] = None
    ok["total_tokens"] = 0
    ledger.validate(ok)  # must not raise


def test_invariant_total_tokens_mismatch_rejected() -> None:
    bad = copy.deepcopy(VALID_PR_OPENED)
    bad["generator"]["tokens"] = 100
    bad["total_tokens"] = 99  # off-by-one
    with pytest.raises(ledger.LedgerInvariantError, match="total_tokens"):
        ledger.validate(bad)


def test_invariant_total_tokens_match_accepted() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["generator"]["tokens"] = 100
    ok["total_tokens"] = 100
    ledger.validate(ok)


def test_invariant_total_tokens_sums_generator_and_evaluator() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["generator"]["tokens"] = 100
    ok["evaluator"] = {
        "prompt_version": "v1",
        "verdict": "approve",
        "reason": "fine",
        "tokens": 25,
    }
    ok["total_tokens"] = 125
    ledger.validate(ok)


def test_invariant_total_tokens_zero_when_both_null() -> None:
    ok = copy.deepcopy(VALID_PR_OPENED)
    ok["status"] = "skipped_pause"
    ok["pr"] = None
    ok["issue"] = None
    ok["generator"] = None
    ok["evaluator"] = None
    ok["total_tokens"] = 0
    ledger.validate(ok)


def _seeded_ledger(tmp_path: Path, last_run_id: str, last_ts: str) -> Path:
    p = tmp_path / "ledger.jsonl"
    entry = copy.deepcopy(VALID_PR_OPENED)
    entry["run_id"] = last_run_id
    entry["ts"] = last_ts
    ledger.append(p, entry)
    return p


def test_invariant_run_id_must_strictly_increase(tmp_path: Path) -> None:
    p = _seeded_ledger(tmp_path, "r-0005", "2026-04-18T12:00:00Z")

    same = copy.deepcopy(VALID_PR_OPENED)
    same["run_id"] = "r-0005"
    same["ts"] = "2026-04-18T12:00:05Z"
    same["pr"] = 1001
    with pytest.raises(ledger.LedgerInvariantError, match="run_id"):
        ledger.append(p, same)

    older = copy.deepcopy(VALID_PR_OPENED)
    older["run_id"] = "r-0004"
    older["ts"] = "2026-04-18T12:00:05Z"
    older["pr"] = 1002
    with pytest.raises(ledger.LedgerInvariantError, match="run_id"):
        ledger.append(p, older)


def test_invariant_run_id_increment_accepted(tmp_path: Path) -> None:
    p = _seeded_ledger(tmp_path, "r-0005", "2026-04-18T12:00:00Z")
    nxt = copy.deepcopy(VALID_PR_OPENED)
    nxt["run_id"] = "r-0006"
    nxt["ts"] = "2026-04-18T12:00:05Z"
    nxt["pr"] = 1001
    ledger.append(p, nxt)
    assert ledger.last_run_id(p) == 6


def test_invariant_ts_must_not_go_backward(tmp_path: Path) -> None:
    p = _seeded_ledger(tmp_path, "r-0005", "2026-04-18T12:00:00Z")
    backward = copy.deepcopy(VALID_PR_OPENED)
    backward["run_id"] = "r-0006"
    backward["ts"] = "2026-04-18T11:59:59Z"
    backward["pr"] = 1001
    with pytest.raises(ledger.LedgerInvariantError, match="ts"):
        ledger.append(p, backward)


def test_invariant_ts_equal_to_previous_accepted(tmp_path: Path) -> None:
    # ts monotonicity is non-strict: equality is allowed.
    p = _seeded_ledger(tmp_path, "r-0005", "2026-04-18T12:00:00Z")
    same_ts = copy.deepcopy(VALID_PR_OPENED)
    same_ts["run_id"] = "r-0006"
    same_ts["ts"] = "2026-04-18T12:00:00Z"
    same_ts["pr"] = 1001
    ledger.append(p, same_ts)


def _seed_git_repo_with_remote(repo: Path, remote: Path) -> None:
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "seed@local"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "seed"], check=True)
    (repo / "README.md").write_text("seed\n")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", "seed"],
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(remote)], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "push", "-u", "origin", "main"],
        check=True,
        capture_output=True,
    )


def test_state_branch_store_appends_and_reads_last_run_id(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    remote = tmp_path / "remote.git"
    _seed_git_repo_with_remote(repo, remote)

    store = ledger.StateBranchLedgerStore(repo_dir=repo)
    assert ledger.last_run_id(store) is None

    e1 = copy.deepcopy(VALID_PR_OPENED)
    ledger.append(store, e1)
    assert ledger.last_run_id(store) == 1

    e2 = copy.deepcopy(VALID_PR_OPENED)
    e2["run_id"] = "r-0002"
    e2["ts"] = "2026-04-18T12:00:01Z"
    e2["pr"] = 1001
    ledger.append(store, e2)
    assert ledger.last_run_id(store) == 2

    subprocess.run(
        ["git", "-C", str(repo), "fetch", "origin", "tokenman-state:refs/heads/tokenman-state"],
        check=True,
        capture_output=True,
    )
    raw = subprocess.check_output(
        ["git", "-C", str(repo), "show", "tokenman-state:ledger.jsonl"],
        text=True,
    )
    lines = [json.loads(line) for line in raw.splitlines() if line.strip()]
    assert [line["run_id"] for line in lines] == ["r-0001", "r-0002"]
