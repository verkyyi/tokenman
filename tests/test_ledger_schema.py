"""Validate every ledger fixture entry against harness/ledger.schema.json."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "harness" / "ledger.schema.json"
LEDGERS_DIR = REPO_ROOT / "tests" / "ledgers"


@pytest.fixture(scope="module")
def schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


@pytest.fixture(scope="module")
def validator(schema: dict) -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(schema)


@pytest.mark.parametrize(
    "ledger_path",
    sorted(LEDGERS_DIR.glob("*.jsonl")),
    ids=lambda p: p.name,
)
def test_every_entry_validates(
    validator: jsonschema.Draft202012Validator,
    ledger_path: Path,
) -> None:
    """Each line in every *.jsonl fixture must validate against the schema."""
    for lineno, line in enumerate(ledger_path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        entry = json.loads(line)
        errors = sorted(validator.iter_errors(entry), key=lambda e: e.path)
        if errors:
            msgs = "\n".join(f"  - {e.message} at {list(e.path)}" for e in errors)
            pytest.fail(f"{ledger_path.name}:{lineno}\n{msgs}")


def test_all_statuses_fixture_covers_enum(schema: dict) -> None:
    """all-statuses.jsonl must have exactly one entry per status enum value."""
    from collections import Counter

    all_statuses_path = LEDGERS_DIR / "all-statuses.jsonl"
    entries = [
        json.loads(line)
        for line in all_statuses_path.read_text().splitlines()
        if line.strip()
    ]
    expected = set(schema["properties"]["status"]["enum"])
    actual_counts = Counter(e["status"] for e in entries)
    actual = set(actual_counts)
    assert actual == expected, (
        f"missing: {expected - actual}, extra: {actual - expected}"
    )
    duplicates = [s for s, c in actual_counts.items() if c > 1]
    assert not duplicates, f"duplicate statuses: {duplicates}"
