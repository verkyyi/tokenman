"""Skill installer: fetch catalog entries into .claude/skills/<name>/.

See docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, Optional

__all__ = ["InstallResult", "install_skill"]

_REMOTE_SCHEMES = ("https://", "http://", "file://", "git://", "ssh://")


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

    if source.startswith(_REMOTE_SCHEMES):
        return _install_remote(
            skill_name=skill_name,
            catalog_entry=catalog_entry,
            target_dir=target_dir,
            force=force,
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


def _install_remote(
    *,
    skill_name: str,
    catalog_entry: dict,
    target_dir: Path,
    force: bool,
) -> InstallResult:
    source = catalog_entry["source"]
    version = catalog_entry.get("version")
    if not version:
        return InstallResult(
            skill_name=skill_name, status="errored",
            resolved_sha=None, exit_code=2,
            message="catalog entry has no 'version' field",
        )

    with tempfile.TemporaryDirectory(prefix="tokenman-install-") as tmp:
        tmpdir = Path(tmp)
        clone_dir = tmpdir / "clone"
        try:
            _git_clone(source, clone_dir)
            _git_checkout(clone_dir, version)
            resolved_sha = _git_rev_parse(clone_dir)
        except _GitError as exc:
            return InstallResult(
                skill_name=skill_name, status="errored",
                resolved_sha=None, exit_code=3,
                message=f"git: {exc}",
            )

        subpath = catalog_entry.get("path")
        if subpath:
            source_tree = clone_dir / subpath
            if not source_tree.is_dir():
                return InstallResult(
                    skill_name=skill_name, status="errored",
                    resolved_sha=resolved_sha, exit_code=4,
                    message=(
                        f"catalog path {subpath!r} not present in "
                        f"{source}@{version} (resolved {resolved_sha[:12]})"
                    ),
                )
        else:
            source_tree = clone_dir

        target_dir.parent.mkdir(parents=True, exist_ok=True)
        if target_dir.exists():
            existing = _read_existing_lock(target_dir)
            if existing is not None and existing.get("resolved_sha") == resolved_sha:
                return InstallResult(
                    skill_name=skill_name, status="unchanged",
                    resolved_sha=resolved_sha, exit_code=0,
                    message=f"{skill_name} already at {resolved_sha[:12]}",
                )
            if not force:
                return InstallResult(
                    skill_name=skill_name, status="errored",
                    resolved_sha=resolved_sha, exit_code=5,
                    message=(
                        f"{target_dir} exists but does not match "
                        f"{resolved_sha[:12]}; re-run with --force to overwrite"
                    ),
                )
            shutil.rmtree(target_dir)
        _copy_tree_minus_git(source_tree, target_dir)

        if not (target_dir / "SKILL.md").is_file():
            shutil.rmtree(target_dir, ignore_errors=True)
            return InstallResult(
                skill_name=skill_name, status="errored",
                resolved_sha=None, exit_code=4,
                message="SKILL.md missing after checkout",
            )

        _write_lock(
            target_dir=target_dir, source=source,
            version=version, resolved_sha=resolved_sha,
        )

    return InstallResult(
        skill_name=skill_name, status="installed",
        resolved_sha=resolved_sha, exit_code=0,
        message=f"installed {skill_name} at {version}",
    )


class _GitError(RuntimeError):
    pass


def _git_run(cmd: list[str], *, cwd: Optional[Path] = None) -> str:
    proc = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None,
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        raise _GitError(proc.stderr.strip() or proc.stdout.strip() or "unknown error")
    return proc.stdout.strip()


def _git_clone(source: str, dest: Path) -> None:
    _git_run(["git", "clone", "--quiet", source, str(dest)])


def _git_checkout(repo: Path, ref: str) -> None:
    _git_run(["git", "-C", str(repo), "checkout", "--quiet", ref])


def _git_rev_parse(repo: Path) -> str:
    return _git_run(["git", "-C", str(repo), "rev-parse", "HEAD"])


def _copy_tree_minus_git(src: Path, dst: Path) -> None:
    shutil.copytree(
        src, dst,
        ignore=shutil.ignore_patterns(".git"),
        symlinks=True,
    )


def _read_existing_lock(target_dir: Path) -> Optional[dict]:
    lock_path = target_dir / ".tokenman-skill-lock"
    if not lock_path.is_file():
        return None
    try:
        return json.loads(lock_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def _write_lock(
    *, target_dir: Path, source: str, version: str, resolved_sha: str,
) -> None:
    lock = {
        "source": source,
        "version": version,
        "resolved_sha": resolved_sha,
        "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    (target_dir / ".tokenman-skill-lock").write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n"
    )
