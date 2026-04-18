"""Unit tests for harness.lib.pr_opener.GhPROpener."""
from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from harness.lib.pr_opener import GhPROpener, PROpenerError


def test_gh_pr_opener_builds_expected_argv(tmp_path: Path) -> None:
    opener = GhPROpener(repo_dir=tmp_path, base_branch="main", gh_bin="gh")

    with patch("harness.lib.pr_opener.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="https://github.com/acme/repo/pull/4242\n",
            stderr="",
        )
        pr = opener.open(
            title="[tokenman] readme-maintainer: add section",
            body="Proposed change.",
            branch="tokenman/readme-maintainer/r-0001",
        )

    assert pr == 4242
    args, kwargs = m.call_args
    cmd = args[0]
    assert cmd[0] == "gh"
    assert cmd[1:3] == ["pr", "create"]
    assert "--draft" in cmd
    assert "--title" in cmd and "[tokenman] readme-maintainer: add section" in cmd
    assert "--body" in cmd and "Proposed change." in cmd
    assert "--head" in cmd and "tokenman/readme-maintainer/r-0001" in cmd
    assert "--base" in cmd and "main" in cmd
    assert kwargs["cwd"] == str(tmp_path)


def test_gh_pr_opener_raises_on_nonzero_exit(tmp_path: Path) -> None:
    opener = GhPROpener(repo_dir=tmp_path)

    with patch("harness.lib.pr_opener.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="HTTP 422: Validation Failed",
        )
        with pytest.raises(PROpenerError) as exc:
            opener.open(title="t", body="b", branch="br")
        assert "422" in str(exc.value)


def test_gh_pr_opener_parses_number_from_url_with_trailing_whitespace(
    tmp_path: Path,
) -> None:
    opener = GhPROpener(repo_dir=tmp_path)
    with patch("harness.lib.pr_opener.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="https://github.com/acme/repo/pull/17 \n\n",
            stderr="",
        )
        assert opener.open(title="t", body="b", branch="br") == 17


def test_gh_pr_opener_raises_on_unexpected_stdout(tmp_path: Path) -> None:
    opener = GhPROpener(repo_dir=tmp_path)
    with patch("harness.lib.pr_opener.subprocess.run") as m:
        m.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="created ok but no url\n",
            stderr="",
        )
        with pytest.raises(PROpenerError):
            opener.open(title="t", body="b", branch="br")
