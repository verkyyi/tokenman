"""Unit tests for harness.lib.scope_drafter."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness.lib import scope_drafter

REPO_ROOT = Path(__file__).resolve().parent.parent
CANNED = REPO_ROOT / "tests" / "fixtures" / "scope-captures" / "minimal.json"


def _profile():
    from harness.lib.repo_profile import RepoProfile
    return RepoProfile(
        languages={"python": 3}, total_files=4, total_bytes=500,
        tests_present=True, ci_present=False, readme_present=True,
        deps_files=["pyproject.toml"], recent_commits_30d=2,
    )


def _catalog() -> dict[str, dict]:
    return {
        "readme-maintainer": {
            "source": "./skills/readme-maintainer",
            "version": "0.1.0",
            "tier": "starter",
        }
    }


def _plugins() -> list[dict]:
    return [
        {"name": "readme-sync", "description": "x", "category": None,
         "homepage": None, "marketplace": "one"},
    ]


def _answers() -> dict[str, str]:
    return {"purpose": "cli tool", "concern": "a", "off_limits": "",
            "other": ""}


def test_draft_happy_path() -> None:
    executor = scope_drafter.StubScopeExecutor(canned_result=CANNED.read_text())
    draft = scope_drafter.draft(
        profile=_profile(),
        plugins=_plugins(),
        user_answers=_answers(),
        catalog=_catalog(),
        executor=executor,
    )
    assert draft["recommended_skills"][0]["name"] == "readme-maintainer"
    assert draft["suggested_boundaries"]["allowed"] == ["README.md"]


def test_draft_demotes_non_catalog_skill() -> None:
    rogue = json.loads(CANNED.read_text())
    rogue["recommended_skills"].append({
        "name": "not-in-catalog",
        "reasoning": "invented",
        "default_cadence": "weekly",
    })
    executor = scope_drafter.StubScopeExecutor(canned_result=json.dumps(rogue))
    draft = scope_drafter.draft(
        profile=_profile(),
        plugins=_plugins(),
        user_answers=_answers(),
        catalog=_catalog(),
        executor=executor,
    )
    names = [s["name"] for s in draft["recommended_skills"]]
    assert "not-in-catalog" not in names
    demoted = [p["plugin"] for p in draft["candidate_uncurated_plugins"]]
    assert "not-in-catalog" in demoted


def test_draft_retries_once_on_invalid_json() -> None:
    executor = scope_drafter.StubScopeExecutor(
        canned_sequence=["not json", CANNED.read_text()]
    )
    draft = scope_drafter.draft(
        profile=_profile(),
        plugins=_plugins(),
        user_answers=_answers(),
        catalog=_catalog(),
        executor=executor,
    )
    assert draft["recommended_skills"][0]["name"] == "readme-maintainer"
    assert executor.call_count == 2


def test_draft_raises_after_retry_exhaustion() -> None:
    executor = scope_drafter.StubScopeExecutor(
        canned_sequence=["not json", "still not json"]
    )
    with pytest.raises(scope_drafter.ScopeDrafterError):
        scope_drafter.draft(
            profile=_profile(),
            plugins=_plugins(),
            user_answers=_answers(),
            catalog=_catalog(),
            executor=executor,
        )


def test_draft_includes_skill_md_in_payload_for_local_catalog_entries(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills" / "readme-maintainer"
    skills_root.mkdir(parents=True)
    (skills_root / "SKILL.md").write_text("SCOPE: README.md only.\n")
    catalog = {
        "readme-maintainer": {
            "source": "./skills/readme-maintainer",
            "version": "0.1.0",
        }
    }

    captured: dict[str, str] = {}

    class CapturingExecutor:
        call_count = 0
        def run(self, *, system_prompt: str, user_payload: str) -> str:
            self.call_count += 1
            captured["payload"] = user_payload
            return CANNED.read_text()

    scope_drafter.draft(
        profile=_profile(),
        plugins=_plugins(),
        user_answers=_answers(),
        catalog=catalog,
        executor=CapturingExecutor(),
        catalog_root=tmp_path,
    )
    assert "SCOPE: README.md only." in captured["payload"]
