"""`python -m harness.install` — populates .claude/skills/ from the catalog.

See docs/superpowers/specs/2026-04-18-phase-1-5-skill-install-design.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml

from harness.lib import catalog, installer


def _enabled_skills_from_config(config_path: Path) -> list[str]:
    if not config_path.is_file():
        return []
    data = yaml.safe_load(config_path.read_text()) or {}
    skills = data.get("skills") or []
    if not isinstance(skills, list):
        return []
    return [s for s in skills if isinstance(s, str)]


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.install")
    parser.add_argument("--repo", default=".",
                        help="consumer repo (install target)")
    parser.add_argument("--config-path", default=None,
                        help="default: <repo>/.tokenman/tokenman.yaml")
    parser.add_argument("--catalog-path", default=None,
                        help="override tokenman library's recommended-skills.yaml "
                             "(defaults to the one in the tokenman library root)")
    parser.add_argument("--skill", action="append", default=[],
                        help="repeatable; overrides config skills list")
    parser.add_argument("--force", action="store_true",
                        help="rm -rf drifted targets before reinstalling")
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would happen; no filesystem writes")
    parser.add_argument("--non-interactive", action="store_true",
                        help="reserved; install has no prompts today")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    config_path = (
        Path(args.config_path).resolve() if args.config_path
        else repo / ".tokenman" / "tokenman.yaml"
    )

    if args.catalog_path:
        catalog_path = Path(args.catalog_path).resolve()
        root = catalog_path.parent
    else:
        try:
            root = catalog.tokenman_root()
        except catalog.SkillResolutionError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    try:
        catalog_data = catalog.load_catalog(root)
    except catalog.SkillResolutionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.skill:
        skill_names = list(args.skill)
    else:
        skill_names = _enabled_skills_from_config(config_path)

    if not skill_names:
        print(
            "error: no skills enabled. Add skills to "
            f"{config_path} or pass --skill NAME (repeatable). "
            "Run `python -m harness.scope` first to draft a config.",
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        for name in skill_names:
            entry = catalog_data.get(name)
            src = entry.get("source") if entry else "<unknown>"
            ver = entry.get("version") if entry else "<unknown>"
            print(f"[dry-run] would install {name} from {src} @ {ver}")
        return 0

    final_exit = 0
    for name in skill_names:
        entry = catalog_data.get(name)
        if entry is None:
            print(f"{name}: errored(skill not in catalog)")
            final_exit = max(final_exit, 2)
            continue

        target = repo / ".claude" / "skills" / name
        result = installer.install_skill(
            skill_name=name,
            catalog_entry=entry,
            target_dir=target,
            tokenman_root=root,
            force=args.force,
        )

        print(f"{result.skill_name}: {result.status}({result.message})")
        final_exit = max(final_exit, result.exit_code)

    return final_exit


if __name__ == "__main__":
    sys.exit(main())
