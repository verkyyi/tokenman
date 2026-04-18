"""`python -m harness.run` — runs one skill against a consumer repo.

Thin wrapper around harness.lib.runner.run_skill. Resolves skill_dir
from recommended-skills.yaml. --dry-run swaps ClaudeSkillExecutor for
the stub-readme fixture and GhPROpener for FakePROpener — useful for
local iteration or smoke testing without spending tokens or opening
real PRs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import yaml

from harness.lib import runner
from harness.lib.pr_opener import FakePROpener, GhPROpener
from harness.lib.skill_executor import ClaudeSkillExecutor, StubSkillExecutor


def _repo_root() -> Path:
    """Return the tokenman library repo root (where recommended-skills.yaml lives).

    The CLI is invoked from the consumer's repo, but the catalog lives in
    the tokenman library install. Walk up from this module's location to
    find recommended-skills.yaml.
    """
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / "recommended-skills.yaml").is_file():
            return candidate
    raise SystemExit(
        "recommended-skills.yaml not found; is tokenman installed correctly?"
    )


def _resolve_skill_dir(skill_name: str) -> Path:
    root = _repo_root()
    catalog_path = root / "recommended-skills.yaml"
    catalog = yaml.safe_load(catalog_path.read_text()) or {}
    entry = catalog.get(skill_name)
    if entry is None:
        raise SystemExit(f"skill {skill_name!r} not in recommended-skills.yaml")
    source = entry.get("source")
    if source is None:
        raise SystemExit(f"skill {skill_name!r} has no 'source' field")
    if source.startswith("./"):
        return (root / source[2:]).resolve()
    raise SystemExit(
        f"only local (./) sources are supported in 1.2b; got {source!r}"
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.run")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--ledger-path", default=None)
    parser.add_argument("--runs-dir", default=None)
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--base-branch", default="main")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    ledger_path = (
        Path(args.ledger_path) if args.ledger_path
        else repo / ".tokenman" / "ledger.jsonl"
    )
    runs_dir = (
        Path(args.runs_dir) if args.runs_dir
        else repo / ".tokenman" / "runs"
    )

    skill_dir = _resolve_skill_dir(args.skill)

    if args.dry_run:
        root = _repo_root()
        stub_skill = root / "tests" / "fixtures" / "skills" / "stub-readme"
        executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
        pr_opener = FakePROpener(sink_dir=runs_dir.parent / "dry-run-prs")
        effective_skill_dir = stub_skill
    else:
        executor = ClaudeSkillExecutor(claude_bin=args.claude_bin)
        pr_opener = GhPROpener(repo_dir=repo, base_branch=args.base_branch)
        effective_skill_dir = skill_dir

    entry = runner.run_skill(
        skill_dir=effective_skill_dir,
        repo_dir=repo,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name=args.skill,
        base_branch=args.base_branch,
    )
    print(json.dumps(entry, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
