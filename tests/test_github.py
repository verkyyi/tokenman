"""Unit tests for harness.github."""
from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from harness import github


def test_open_pull_request_builds_expected_argv(tmp_path: Path) -> None:
    with patch("harness.github.subprocess.run") as mocked:
        mocked.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="https://github.com/acme/repo/pull/4242\n",
            stderr="",
        )
        pr = github.open_pull_request(
            repo_dir=tmp_path,
            title="[tokenman] docs-maintainer: add section",
            body="Proposed change.",
            branch="tokenman/docs-maintainer/r-0001",
            base_branch="main",
        )

    assert pr == 4242
    args, kwargs = mocked.call_args
    cmd = args[0]
    assert cmd[0] == "gh"
    assert cmd[1:3] == ["pr", "create"]
    assert "--draft" in cmd
    assert "--title" in cmd and "[tokenman] docs-maintainer: add section" in cmd
    assert "--body" in cmd and "Proposed change." in cmd
    assert "--head" in cmd and "tokenman/docs-maintainer/r-0001" in cmd
    assert "--base" in cmd and "main" in cmd
    assert kwargs["cwd"] == str(tmp_path)


def test_open_pull_request_raises_on_nonzero_exit(tmp_path: Path) -> None:
    with patch("harness.github.subprocess.run") as mocked:
        mocked.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="HTTP 422: Validation Failed",
        )
        with pytest.raises(github.GitHubError) as exc:
            github.open_pull_request(repo_dir=tmp_path, title="t", body="b", branch="br")
        assert "422" in str(exc.value)


def test_open_pull_request_parses_number_from_url_with_trailing_whitespace(
    tmp_path: Path,
) -> None:
    with patch("harness.github.subprocess.run") as mocked:
        mocked.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="https://github.com/acme/repo/pull/17 \n\n",
            stderr="",
        )
        assert (
            github.open_pull_request(repo_dir=tmp_path, title="t", body="b", branch="br")
            == 17
        )


def test_open_issue_builds_expected_argv(tmp_path: Path) -> None:
    with patch("harness.github.subprocess.run") as mocked:
        mocked.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="https://github.com/acme/repo/issues/88\n",
            stderr="",
        )
        issue = github.open_issue(repo_dir=tmp_path, title="review needed", body="details")

    assert issue == 88
    args, kwargs = mocked.call_args
    cmd = args[0]
    assert cmd[0] == "gh"
    assert cmd[1:3] == ["issue", "create"]
    assert "--title" in cmd and "review needed" in cmd
    assert "--body" in cmd and "details" in cmd
    assert kwargs["cwd"] == str(tmp_path)


def test_open_issue_raises_on_unexpected_stdout(tmp_path: Path) -> None:
    with patch("harness.github.subprocess.run") as mocked:
        mocked.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="created ok but no url\n",
            stderr="",
        )
        with pytest.raises(github.GitHubError):
            github.open_issue(repo_dir=tmp_path, title="t", body="b")
