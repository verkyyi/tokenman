"""Shared catalog helpers: root lookup, load, resolve skill path.

Replaces three copies previously duplicated in scope/__main__.py and
onboard/__main__.py. Will grow a third caller (install/__main__.py) in
Phase 1.5.
"""
from __future__ import annotations

from pathlib import Path

import yaml


class SkillResolutionError(Exception):
    """Catalog / skill-resolution error. CLIs convert to exit 2."""


def tokenman_root() -> Path:
    """Find the tokenman library repo root (holds recommended-skills.yaml)."""
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / "recommended-skills.yaml").is_file():
            return candidate
    raise SkillResolutionError(
        "recommended-skills.yaml not found; is tokenman installed?"
    )


def load_catalog(root: Path) -> dict[str, dict]:
    data = yaml.safe_load((root / "recommended-skills.yaml").read_text()) or {}
    if not isinstance(data, dict):
        raise SkillResolutionError("recommended-skills.yaml must be a mapping")
    return data


def resolve_skill_dir(
    *,
    skill_name: str,
    catalog: dict,
    tokenman_root: Path,
    consumer_repo: Path,
) -> Path:
    """Return the on-disk path a runner should pass to the executor.

    - Local source ('./…')   -> <tokenman_root>/<path>.
    - Remote source ('https:…') -> <consumer_repo>/.claude/skills/<name>/
      if present; otherwise raises SkillResolutionError("not installed; …").
    """
    entry = catalog.get(skill_name)
    if entry is None:
        raise SkillResolutionError(
            f"skill {skill_name!r} not in recommended-skills.yaml"
        )
    source = entry.get("source")
    if source is None:
        raise SkillResolutionError(
            f"skill {skill_name!r} has no 'source' field"
        )
    if source.startswith("./"):
        return (tokenman_root / source[2:]).resolve()
    if source.startswith(("https://", "http://")):
        installed = (consumer_repo / ".claude" / "skills" / skill_name).resolve()
        if (installed / "SKILL.md").is_file():
            return installed
        raise SkillResolutionError(
            f"skill {skill_name!r} not installed; "
            "run `python -m harness.install` first"
        )
    raise SkillResolutionError(
        f"skill {skill_name!r} has unsupported source scheme: {source!r}"
    )
