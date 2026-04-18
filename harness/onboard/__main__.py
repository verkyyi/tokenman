"""`python -m harness.onboard` — runs all enabled skills back-to-back
in one session, opens a PR per skill, writes
.tokenman/onboarding-summary.md.

See docs/superpowers/specs/2026-04-18-phase-1-4-onboarding-mode-design.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml

from harness.lib import onboarder, summary
from harness.lib.onboarder import OnboardingBudget, OnboardingError
from harness.lib.pr_opener import FakePROpener, GhPROpener
from harness.lib.skill_executor import ClaudeSkillExecutor, StubSkillExecutor


_DEFAULT_PER_RUN = 30_000


def _tokenman_root() -> Path:
    """Find the tokenman library repo root (holds recommended-skills.yaml)."""
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / "recommended-skills.yaml").is_file():
            return candidate
    raise SystemExit("recommended-skills.yaml not found; is tokenman installed?")


def _load_catalog(root: Path) -> dict[str, dict]:
    data = yaml.safe_load((root / "recommended-skills.yaml").read_text()) or {}
    if not isinstance(data, dict):
        raise SystemExit("recommended-skills.yaml must be a mapping")
    return data


def _resolve_skill_dir(skill_name: str, catalog: dict, root: Path) -> Path:
    entry = catalog.get(skill_name)
    if entry is None:
        raise SystemExit(
            f"skill {skill_name!r} not in recommended-skills.yaml"
        )
    source = entry.get("source")
    if source is None:
        raise SystemExit(f"skill {skill_name!r} has no 'source' field")
    if source.startswith("./"):
        return (root / source[2:]).resolve()
    raise SystemExit(
        f"remote skill sources land in Phase 1.5; got {source!r}"
    )


def _enabled_skills_from_config(config_path: Path) -> list[str]:
    if not config_path.is_file():
        return []
    data = yaml.safe_load(config_path.read_text()) or {}
    skills = data.get("skills") or []
    if not isinstance(skills, list):
        return []
    return [s for s in skills if isinstance(s, str)]


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m harness.onboard")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--config-path", default=None,
                        help="default: <repo>/.tokenman/tokenman.yaml")
    parser.add_argument("--ledger-path", default=None,
                        help="default: <repo>/.tokenman/ledger.jsonl")
    parser.add_argument("--runs-dir", default=None,
                        help="default: <repo>/.tokenman/runs")
    parser.add_argument("--output-path", default=None,
                        help="default: <repo>/.tokenman/onboarding-summary.md")
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--base-branch", default="main")
    parser.add_argument("--per-run-ceiling", type=int, default=_DEFAULT_PER_RUN)
    parser.add_argument("--session-ceiling", type=int, default=None,
                        help="default: 3 × per_run_ceiling × N_skills")
    parser.add_argument("--skill", action="append", default=[],
                        help="repeatable; overrides config skills list")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="use stub executor + fake PR opener; "
                             "every skill resolves to the stub-readme fixture")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    config_path = (
        Path(args.config_path).resolve() if args.config_path
        else repo / ".tokenman" / "tokenman.yaml"
    )
    ledger_path = (
        Path(args.ledger_path).resolve() if args.ledger_path
        else repo / ".tokenman" / "ledger.jsonl"
    )
    runs_dir = (
        Path(args.runs_dir).resolve() if args.runs_dir
        else repo / ".tokenman" / "runs"
    )
    output_path = (
        Path(args.output_path).resolve() if args.output_path
        else repo / ".tokenman" / "onboarding-summary.md"
    )

    # Resolve skills.
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

    root = _tokenman_root()
    catalog = _load_catalog(root)

    if args.dry_run:
        # Every skill resolves to the same stub fixture; substitute fakes.
        stub_dir = root / "tests" / "fixtures" / "skills" / "stub-readme"
        skills = [(name, stub_dir) for name in skill_names]
        executor = StubSkillExecutor(extra_env={"STUB_MODE": "no_change"})
        pr_opener = FakePROpener(sink_dir=runs_dir.parent / "dry-run-prs")
    else:
        try:
            skills = [
                (name, _resolve_skill_dir(name, catalog, root))
                for name in skill_names
            ]
        except SystemExit as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        executor = ClaudeSkillExecutor(claude_bin=args.claude_bin)
        pr_opener = GhPROpener(repo_dir=repo, base_branch=args.base_branch)

    session_ceiling = (
        args.session_ceiling
        if args.session_ceiling is not None
        else 3 * args.per_run_ceiling * len(skills)
    )
    budget = OnboardingBudget(
        per_run_ceiling=args.per_run_ceiling,
        session_ceiling=session_ceiling,
    )

    try:
        result = onboarder.run_onboarding(
            skills=skills,
            repo_dir=repo,
            ledger_path=ledger_path,
            runs_dir=runs_dir,
            executor=executor,
            pr_opener=pr_opener,
            budget=budget,
            base_branch=args.base_branch,
        )
    except OnboardingError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    rendered = summary.build(result=result, repo_name=repo.name)

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered)
    except OSError as exc:
        print(f"error: failed to write {output_path}: {exc}", file=sys.stderr)
        return 4

    print(f"wrote {output_path}")
    print(
        f"total tokens: {result.total_tokens:,} "
        f"({100 * result.total_tokens / max(result.session_ceiling, 1):.1f}% "
        "of session ceiling)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
