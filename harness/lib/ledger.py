"""Ledger append utility — validates entries against the schema and the
conditional invariants the schema cannot express, then appends JSONL lines.
See docs/spec.md §8.1 and
docs/superpowers/specs/2026-04-18-phase-1-2a-harness-plumbing-design.md.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

import jsonschema


_SCHEMA_PATH = Path(__file__).parent / "ledger.schema.json"


class LedgerInvariantError(ValueError):
    """Raised when a ledger entry violates schema or conditional invariants."""


@lru_cache(maxsize=1)
def _load_schema() -> dict:
    return json.loads(_SCHEMA_PATH.read_text())


@lru_cache(maxsize=1)
def _schema_validator() -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(_load_schema())


def validate(entry: dict, *, previous: Optional[dict] = None) -> None:
    """Validate entry against the JSON schema and conditional invariants.

    Raises LedgerInvariantError if any check fails. Checks:
      1. JSON Schema (harness/lib/ledger.schema.json).
      2. pr is non-null iff status == "pr_opened".
      3. generator is null on skipped_* statuses; populated on
         pr_opened / no_change / aborted_*; either allowed on error.
      4. total_tokens == generator.tokens + evaluator.tokens (counting
         absent blocks as 0).
      5. When `previous` is supplied: run_id strictly greater than
         previous['run_id']; ts >= previous['ts'] (non-strict).
    """
    errors = list(_schema_validator().iter_errors(entry))
    if errors:
        msgs = "; ".join(f"{list(e.path)}: {e.message}" for e in errors)
        raise LedgerInvariantError(f"schema: {msgs}")

    status = entry["status"]
    pr = entry.get("pr")
    if status == "pr_opened" and pr is None:
        raise LedgerInvariantError("pr must be non-null when status == 'pr_opened'")
    if status != "pr_opened" and pr is not None:
        raise LedgerInvariantError(
            f"pr must be null when status == {status!r} (got {pr!r})"
        )

    gen = entry.get("generator")
    if status.startswith("skipped_"):
        if gen is not None:
            raise LedgerInvariantError(
                f"generator must be null when status == {status!r}"
            )
    elif status == "error":
        # Either null (pre-generator failure) or populated (generator ran
        # then a later stage erred) is acceptable.
        pass
    else:
        # pr_opened, no_change, aborted_gate, aborted_evaluator
        if gen is None:
            raise LedgerInvariantError(
                f"generator must be populated when status == {status!r}"
            )

    gen_tokens = gen["tokens"] if gen else 0
    ev = entry.get("evaluator")
    ev_tokens = ev["tokens"] if ev else 0
    expected = gen_tokens + ev_tokens
    if entry["total_tokens"] != expected:
        raise LedgerInvariantError(
            f"total_tokens ({entry['total_tokens']}) != "
            f"generator.tokens ({gen_tokens}) + evaluator.tokens ({ev_tokens})"
        )

    if previous is not None:
        prev_run_n = int(previous["run_id"].split("-")[1])
        new_run_n = int(entry["run_id"].split("-")[1])
        if new_run_n <= prev_run_n:
            raise LedgerInvariantError(
                f"run_id {entry['run_id']!r} not strictly greater than "
                f"previous {previous['run_id']!r}"
            )
        if entry["ts"] < previous["ts"]:
            raise LedgerInvariantError(
                f"ts {entry['ts']!r} is before previous ts {previous['ts']!r}"
            )


def _last_entry(ledger_path: Path) -> Optional[dict]:
    """Return the last non-blank JSON line as a dict, or None."""
    if not ledger_path.is_file():
        return None
    lines = [ln for ln in ledger_path.read_text().splitlines() if ln.strip()]
    if not lines:
        return None
    return json.loads(lines[-1])


def last_run_id(ledger_path: Path) -> Optional[int]:
    """Return the integer portion of the last entry's run_id, or None if the
    ledger is missing / empty / all-blank.
    """
    last = _last_entry(ledger_path)
    if last is None:
        return None
    return int(last["run_id"].split("-")[1])


def append(ledger_path: Path, entry: dict) -> None:
    """Validate then append entry as a compact JSON line.

    Creates parent directories and the file if missing. On validation
    failure the file is left unchanged.
    """
    previous = _last_entry(ledger_path)
    validate(entry, previous=previous)

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, separators=(",", ":"))
    with ledger_path.open("a") as f:
        f.write(line + "\n")
        f.flush()
