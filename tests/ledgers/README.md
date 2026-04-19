# Ledger test fixtures

JSONL files used by `tests/test_ledger_schema.py` to validate the ledger
schema (`harness/ledger.schema.json`) as realistic input.

## Fixtures

- `all-statuses.jsonl` — one entry per `status` enum value (10 entries).
  Schema-coverage fixture. Some entries are forward-looking (Phase 2/3
  statuses like `skipped_budget`, `aborted_evaluator`) but valid under
  the schema today.
- `realistic-week.jsonl` — a synthetic week of runs across 2–3 skills
  (~18 entries). Aggregation fixture for ledger summaries.

## Updating fixtures

If you change the schema, run `pytest` at the repo root. If fixture
entries no longer validate, either fix the entries or revert the schema
change — schema drift should require an explicit update path, not happen
by accident.
