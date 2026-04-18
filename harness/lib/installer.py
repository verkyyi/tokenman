"""Skill installer: fetch catalog entries into .claude/skills/<name>/.

See docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

__all__ = ["InstallResult", "install_skill"]


@dataclass(frozen=True)
class InstallResult:
    skill_name: str
    status: Literal["installed", "unchanged", "errored"]
    resolved_sha: Optional[str]
    message: str
    exit_code: int


def install_skill(
    *,
    skill_name: str,
    catalog_entry: dict,
    target_dir: Path,
    tokenman_root: Path,
    force: bool = False,
) -> InstallResult:
    source = catalog_entry.get("source")
    if source is None:
        return InstallResult(
            skill_name=skill_name, status="errored",
            resolved_sha=None, exit_code=2,
            message="catalog entry has no 'source' field",
        )

    if source.startswith("./"):
        return _install_local(
            skill_name=skill_name,
            local_path=(tokenman_root / source[2:]).resolve(),
        )

    return InstallResult(
        skill_name=skill_name, status="errored",
        resolved_sha=None, exit_code=2,
        message=f"unsupported source scheme: {source!r}",
    )


def _install_local(*, skill_name: str, local_path: Path) -> InstallResult:
    if not (local_path / "SKILL.md").is_file():
        return InstallResult(
            skill_name=skill_name, status="errored",
            resolved_sha=None, exit_code=4,
            message=f"local source has no SKILL.md at {local_path}",
        )
    return InstallResult(
        skill_name=skill_name, status="unchanged",
        resolved_sha=None, exit_code=0,
        message=f"local source resolved in place at {local_path}",
    )
