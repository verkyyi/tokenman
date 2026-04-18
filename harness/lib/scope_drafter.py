"""Orchestrate the single `claude -p` call that drafts initial-scope.md.

Responsibilities:
  1. Build the system prompt (from harness/prompts/scoping.v1.md) and
     user payload (JSON blob: repo profile + marketplace plugins +
     catalog + SKILL.md texts + user answers).
  2. Invoke the executor (Claude or Stub); parse its JSON response.
  3. Enforce the catalog allowlist by demoting non-catalog
     `recommended_skills` entries into `candidate_uncurated_plugins`.
  4. Retry once on invalid JSON; raise `ScopeDrafterError` otherwise.
"""
from __future__ import annotations

import json
import subprocess
from importlib.resources import files
from pathlib import Path
from typing import Optional, Protocol, TypedDict

from harness.lib.repo_profile import RepoProfile

_FRAMING_RESOURCE = files("harness.prompts") / "scoping.v1.md"


class ScopeDrafterError(Exception):
    """Raised when the LLM fails to produce a valid ScopeDraft."""


class ScopeExecutorError(Exception):
    """Raised by executors on transport failure."""


class RecommendedSkill(TypedDict):
    name: str
    reasoning: str
    default_cadence: str


class SkippedSkill(TypedDict):
    name: str
    reasoning: str


class CandidatePlugin(TypedDict):
    plugin: str
    marketplace: str
    reasoning: str


class Boundaries(TypedDict):
    allowed: list[str]
    forbidden: list[str]


class ScopeDraft(TypedDict):
    profile_prose: str
    recommended_skills: list[RecommendedSkill]
    skipped_skills: list[SkippedSkill]
    candidate_uncurated_plugins: list[CandidatePlugin]
    suggested_boundaries: Boundaries


class ScopeExecutor(Protocol):
    def run(self, *, system_prompt: str, user_payload: str) -> str: ...


class StubScopeExecutor:
    """Returns canned JSON strings. For unit tests and --dry-run."""

    def __init__(
        self,
        *,
        canned_result: Optional[str] = None,
        canned_sequence: Optional[list[str]] = None,
    ) -> None:
        if canned_sequence is not None:
            self._sequence = list(canned_sequence)
        elif canned_result is not None:
            self._sequence = [canned_result]
        else:
            raise ValueError("provide canned_result or canned_sequence")
        self.call_count = 0

    def run(self, *, system_prompt: str, user_payload: str) -> str:
        self.call_count += 1
        if not self._sequence:
            raise ScopeExecutorError("stub out of canned responses")
        return self._sequence.pop(0)


def _load_framing() -> str:
    return _FRAMING_RESOURCE.read_text(encoding="utf-8")


def _load_skill_md(
    *,
    catalog: dict[str, dict],
    catalog_root: Path,
    consumer_repo: Path,
) -> dict[str, Optional[str]]:
    """Load SKILL.md text for each catalog entry when available.

    - Local './…' source → read from <catalog_root>/<path>/SKILL.md.
    - Remote source, installed → read from
      <consumer_repo>/.claude/skills/<name>/SKILL.md.
    - Remote source, not yet installed → None (the scoping prompt
      tolerates null skill_md, falling back to the catalog entry's
      description).
    """
    out: dict[str, Optional[str]] = {}
    for name, entry in catalog.items():
        source = entry.get("source") if isinstance(entry, dict) else None
        if isinstance(source, str) and source.startswith("./"):
            skill_md = (catalog_root / source[2:] / "SKILL.md")
            try:
                out[name] = skill_md.read_text(encoding="utf-8")
            except OSError:
                out[name] = None
            continue
        if isinstance(source, str) and source.startswith(("https://", "http://")):
            installed = consumer_repo / ".claude" / "skills" / name / "SKILL.md"
            try:
                out[name] = installed.read_text(encoding="utf-8")
            except OSError:
                out[name] = None
            continue
        out[name] = None
    return out


def _build_payload(
    *,
    profile: RepoProfile,
    plugins: list[dict],
    user_answers: dict[str, str],
    catalog: dict[str, dict],
    skill_md: dict[str, Optional[str]],
) -> str:
    enriched_catalog = {}
    for name, entry in catalog.items():
        enriched_catalog[name] = {**entry, "skill_md": skill_md.get(name)}
    return json.dumps({
        "repo_profile": profile,
        "user_answers": user_answers,
        "catalog": enriched_catalog,
        "marketplace_plugins": plugins,
    }, separators=(",", ":"))


def _validate_draft(obj: object) -> ScopeDraft:
    if not isinstance(obj, dict):
        raise ScopeDrafterError("LLM output is not a JSON object")
    required = {
        "profile_prose", "recommended_skills", "skipped_skills",
        "candidate_uncurated_plugins", "suggested_boundaries",
    }
    missing = required - obj.keys()
    if missing:
        raise ScopeDrafterError(f"LLM output missing keys: {sorted(missing)}")
    bounds = obj["suggested_boundaries"]
    if not isinstance(bounds, dict) or "allowed" not in bounds or "forbidden" not in bounds:
        raise ScopeDrafterError("suggested_boundaries must have allowed/forbidden")
    return obj  # type: ignore[return-value]


def _enforce_allowlist(draft: ScopeDraft, catalog: dict[str, dict]) -> ScopeDraft:
    allowed_names = set(catalog.keys())
    kept: list[RecommendedSkill] = []
    demoted: list[CandidatePlugin] = list(draft["candidate_uncurated_plugins"])
    for skill in draft["recommended_skills"]:
        if skill["name"] in allowed_names:
            kept.append(skill)
        else:
            demoted.append(CandidatePlugin(
                plugin=skill["name"],
                marketplace="unknown",
                reasoning=skill["reasoning"],
            ))
    return ScopeDraft(
        profile_prose=draft["profile_prose"],
        recommended_skills=kept,
        skipped_skills=draft["skipped_skills"],
        candidate_uncurated_plugins=demoted,
        suggested_boundaries=draft["suggested_boundaries"],
    )


def draft(
    *,
    profile: RepoProfile,
    plugins: list[dict],
    user_answers: dict[str, str],
    catalog: dict[str, dict],
    executor: ScopeExecutor,
    consumer_repo: Path,
    catalog_root: Optional[Path] = None,
    prompt_version: str = "v1",
) -> ScopeDraft:
    if catalog_root is None:
        catalog_root = Path(__file__).resolve().parents[2]
    skill_md = _load_skill_md(
        catalog=catalog,
        catalog_root=catalog_root,
        consumer_repo=consumer_repo,
    )
    payload = _build_payload(
        profile=profile, plugins=plugins, user_answers=user_answers,
        catalog=catalog, skill_md=skill_md,
    )
    framing = _load_framing()

    raw = executor.run(system_prompt=framing, user_payload=payload)
    try:
        parsed = json.loads(raw)
        validated = _validate_draft(parsed)
    except (json.JSONDecodeError, ScopeDrafterError):
        retry_framing = (
            framing
            + "\n\nYour previous response was not valid JSON. "
            "Respond with JSON only, matching the schema."
        )
        raw = executor.run(system_prompt=retry_framing, user_payload=payload)
        try:
            parsed = json.loads(raw)
            validated = _validate_draft(parsed)
        except json.JSONDecodeError as exc:
            raise ScopeDrafterError(
                f"LLM output still not valid JSON after retry: {exc}. "
                f"Raw: {raw[:200]}"
            ) from exc

    return _enforce_allowlist(validated, catalog)


class ClaudeScopeExecutor:
    """Production executor: shells out to `claude -p` with JSON output."""

    def __init__(
        self,
        *,
        claude_bin: str = "claude",
        timeout_s: int = 180,
    ) -> None:
        self.claude_bin = claude_bin
        self.timeout_s = timeout_s

    def run(self, *, system_prompt: str, user_payload: str) -> str:
        argv = [
            self.claude_bin,
            "-p",
            "--output-format", "json",
            "--append-system-prompt", system_prompt,
        ]
        try:
            proc = subprocess.run(
                argv,
                input=user_payload,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
            )
        except subprocess.TimeoutExpired as exc:
            raise ScopeExecutorError(
                f"claude -p timed out after {self.timeout_s}s"
            ) from exc
        if proc.returncode != 0:
            raise ScopeExecutorError(
                f"claude -p exited {proc.returncode}: {proc.stderr.strip()}"
            )
        try:
            wrapper = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise ScopeExecutorError(
                f"claude -p stdout is not valid JSON: {exc}"
            ) from exc
        result = wrapper.get("result")
        if not isinstance(result, str):
            raise ScopeExecutorError(
                "claude -p JSON output missing string `result` field"
            )
        return result
