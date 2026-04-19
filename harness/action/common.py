"""Shared helpers for the Tokenman GitHub Action flow."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def env_default(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in {None, ""} else default


def tokenman_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_prompt_template() -> str:
    return (tokenman_root() / "prompt.md").read_text(encoding="utf-8")


def git_lines(repo_dir: Path, *args: str) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(repo_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def recent_changed_files(repo_dir: Path) -> list[str]:
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    payload_path = os.environ.get("GITHUB_EVENT_PATH")
    payload: dict = {}
    if payload_path and Path(payload_path).is_file():
        try:
            payload = json.loads(Path(payload_path).read_text())
        except json.JSONDecodeError:
            payload = {}

    if event_name == "push":
        before = payload.get("before")
        after = payload.get("after") or os.environ.get("GITHUB_SHA")
        if before and after and set(before) != {"0"}:
            return git_lines(repo_dir, "diff", "--name-only", f"{before}..{after}")

    if event_name in {"pull_request", "pull_request_target"}:
        pr = payload.get("pull_request") or {}
        base = ((pr.get("base") or {}).get("sha"))
        head = ((pr.get("head") or {}).get("sha"))
        if base and head:
            return git_lines(repo_dir, "diff", "--name-only", f"{base}..{head}")

    changed = git_lines(repo_dir, "diff", "--name-only", "HEAD~1..HEAD")
    if changed:
        return changed
    return git_lines(repo_dir, "show", "--pretty=", "--name-only", "HEAD")


def markdown_list(items: list[str], *, empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- `{item}`" for item in items)


def render_prompt(
    *,
    job_type: str,
    event_name: str,
    ref_name: str,
    read_paths: list[str],
    write_paths: list[str],
    recent_changes: list[str],
) -> str:
    template = load_prompt_template()
    replacements = {
        "{{JOB_TYPE}}": job_type,
        "{{EVENT_NAME}}": event_name or "unknown",
        "{{REF_NAME}}": ref_name or "unknown",
        "{{READ_PATHS}}": markdown_list(
            read_paths, empty="No read paths were provided."
        ),
        "{{WRITE_PATHS}}": markdown_list(
            write_paths, empty="No write paths were provided."
        ),
        "{{RECENT_CHANGES}}": markdown_list(
            recent_changes, empty="No recent code changes were detected."
        ),
    }
    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def context_summary(
    *,
    event_name: str,
    ref_name: str,
    read_paths: list[str],
    write_paths: list[str],
    recent_changes: list[str],
) -> str:
    lines = [
        f"- GitHub event: `{event_name or 'unknown'}`",
        f"- Base ref: `{ref_name or 'unknown'}`",
        "- Read scope:",
        markdown_list(read_paths, empty="No read paths were provided."),
        "- Write scope:",
        markdown_list(write_paths, empty="No write paths were provided."),
        "- Recent code changes in read scope:",
        markdown_list(recent_changes, empty="No recent code changes were detected."),
    ]
    return "\n".join(lines)


def base_branch(repo_dir: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    env_branch = env_default("GITHUB_BASE_REF") or env_default("GITHUB_REF_NAME")
    if env_branch:
        return env_branch
    current = git_lines(repo_dir, "branch", "--show-current")
    return current[0] if current else "main"


def require(name: str, value: str | None) -> str:
    if value:
        return value
    raise SystemExit(f"missing required input: {name}")


def write_multiline_output(name: str, value: str) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    delimiter = f"TOKENMAN_{name.upper()}_EOF"
    with Path(output_path).open("a", encoding="utf-8") as handle:
        handle.write(f"{name}<<{delimiter}\n")
        handle.write(value)
        if not value.endswith("\n"):
            handle.write("\n")
        handle.write(f"{delimiter}\n")
