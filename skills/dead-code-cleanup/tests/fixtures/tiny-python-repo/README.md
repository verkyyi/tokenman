# tiny-python-repo

Minimal Python project used as a test fixture for the `dead-code-cleanup`
skill.

## Layout

```
tiny-python-repo/
├── pyproject.toml         # minimal config; declares src/ as the package root
├── src/tinypkg/
│   ├── __init__.py
│   ├── app.py             # contains intentional dead imports + unreachable code
│   └── used.py            # clean helper, referenced by app.py
└── tests/
    └── test_app.py        # passes before AND after the skill runs
```

## Intentional dead code in `app.py`

| Line | Category | Expected skill action |
| --- | --- | --- |
| `import os` | whole-line unused import | remove |
| `import sys` | whole-line unused import | remove |
| `from typing import Any, List` | partial unused (`Any` used, `List` not) | KEEP (partial imports out of scope) |
| `print("never runs")` after `return` in `make_greeting` | unreachable statement | remove |
| block after `return items` in `legacy_process` | unreachable statements | remove |

## Running the fixture's own tests

```
cd tests/fixtures/tiny-python-repo
python -m pytest
```

All tests must pass both before and after `dead-code-cleanup` runs. If
any test fails after the skill runs, the skill violated its contract.
