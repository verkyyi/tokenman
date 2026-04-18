"""`python -m harness.run` — runs one skill against a consumer repo.

Thin wrapper around harness.lib.runner.run_skill. Resolves skill_dir
from recommended-skills.yaml via harness.lib.catalog. --dry-run swaps
ClaudeSkillExecutor for the stub-readme fixture and GhPROpener for
FakePROpener — useful for local iteration or smoke testing without
spending tokens or opening real PRs.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

from harness.lib import catalog, runner
from harness.lib.pr_opener import FakePROpener, GhPROpener
from harness.lib.skill_executor import ClaudeSkillExecutor, StubSkillExecutor


def _default_runtime_mode() -> str:
    return "actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local_debug"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.run")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--ledger-path", default=None)
    parser.add_argument("--runs-dir", default=None)
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--base-branch", default="main")
    parser.add_argument(
        "--runtime-mode",
        choices=["actions", "local_debug"],
        default=_default_runtime_mode(),
    )
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

    try:
        root = catalog.tokenman_root()
        catalog_data = catalog.load_catalog(root)
    except catalog.SkillResolutionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        # Dry-run uses the stub fixture, so the skill needn't be installed;
        # but still fail fast on unknown skill names so typos surface.
        if args.skill not in catalog_data:
            print(
                f"error: skill {args.skill!r} not in recommended-skills.yaml",
                file=sys.stderr,
            )
            return 2
        stub_skill = root / "tests" / "fixtures" / "skills" / "stub-readme"
        executor = StubSkillExecutor(extra_env={"STUB_MODE": "propose_diff"})
        pr_opener = FakePROpener(sink_dir=runs_dir.parent / "dry-run-prs")
        effective_skill_dir = stub_skill
    else:
        try:
            effective_skill_dir = catalog.resolve_skill_dir(
                skill_name=args.skill, catalog=catalog_data,
                tokenman_root=root, consumer_repo=repo,
            )
        except catalog.SkillResolutionError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        executor = ClaudeSkillExecutor(claude_bin=args.claude_bin)
        pr_opener = GhPROpener(repo_dir=repo, base_branch=args.base_branch)

    entry = runner.run_skill(
        skill_dir=effective_skill_dir,
        repo_dir=repo,
        ledger_path=ledger_path,
        runs_dir=runs_dir,
        executor=executor,
        pr_opener=pr_opener,
        skill_name=args.skill,
        base_branch=args.base_branch,
        runtime_mode=args.runtime_mode,
    )
    print(json.dumps(entry, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
