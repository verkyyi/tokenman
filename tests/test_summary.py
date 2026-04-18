"""Unit tests for harness.lib.summary.build."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from harness.lib.onboarder import OnboardingResult
from harness.lib.summary import build


REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "onboarding-results" / "minimal.json"


def _load_result() -> OnboardingResult:
    raw = json.loads(FIXTURE.read_text())
    return OnboardingResult(
        entries=raw["entries"],
        total_tokens=raw["total_tokens"],
        session_ceiling=raw["session_ceiling"],
        started_at=datetime.fromisoformat(
            raw["started_at"].replace("Z", "+00:00")
        ).astimezone(timezone.utc),
        finished_at=datetime.fromisoformat(
            raw["finished_at"].replace("Z", "+00:00")
        ).astimezone(timezone.utc),
        breached_ceiling=raw["breached_ceiling"],
    )


def test_build_contains_all_expected_section_headers() -> None:
    result = _load_result()
    md = build(result=result, repo_name="my-repo")

    assert "# Tokenman — Onboarding summary for my-repo" in md
    assert "## What ran" in md
    assert "## Pull requests opened" in md
    assert "## What was considered but not proposed" in md
    assert "## What was skipped" in md
    assert "## Next steps" in md


def test_build_lists_each_skill_in_what_ran() -> None:
    result = _load_result()
    md = build(result=result, repo_name="my-repo")
    assert "**readme-maintainer**" in md
    assert "**dep-bump-safe**" in md


def test_build_links_pr_opened_to_pr_number() -> None:
    result = _load_result()
    md = build(result=result, repo_name="my-repo")
    assert "PR #42" in md or "#42" in md


def test_build_lists_no_change_in_considered_section() -> None:
    result = _load_result()
    md = build(result=result, repo_name="my-repo")
    considered = md.split("## What was considered but not proposed", 1)[1]
    considered = considered.split("## What was skipped", 1)[0]
    assert "dep-bump-safe" in considered
    assert "All dependencies already at latest" in considered


def test_build_what_was_skipped_says_nothing_when_empty() -> None:
    result = _load_result()
    md = build(result=result, repo_name="my-repo")
    skipped = md.split("## What was skipped", 1)[1]
    skipped = skipped.split("## Next steps", 1)[0]
    assert "Nothing was skipped." in skipped


def test_build_total_tokens_and_utilization_in_header() -> None:
    result = _load_result()
    md = build(result=result, repo_name="my-repo")
    assert "Total tokens: 22,300" in md
    assert "Session ceiling: 180,000" in md
    # 22300 / 180000 ≈ 12.4% — render rounded to one decimal or whole %.
    assert "12" in md
