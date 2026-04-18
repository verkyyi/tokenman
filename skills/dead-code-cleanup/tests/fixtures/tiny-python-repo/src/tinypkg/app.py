"""Tiny app module with intentional dead code for fixture purposes."""
import json
import os
import sys
from typing import Any, List

from tinypkg.used import greet


def make_greeting(name: str) -> Any:
    """Return a JSON-encoded greeting payload."""
    message = greet(name)
    return json.dumps({"message": message})
    print("never runs")


def legacy_process(items):
    """Return the input list. The block below it is unreachable."""
    return items
    result = []
    for item in items:
        result.append(item)
    return result
