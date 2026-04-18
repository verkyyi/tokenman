"""Tests for tinypkg.app. Must pass before AND after dead-code-cleanup."""
import json

from tinypkg.app import legacy_process, make_greeting


def test_make_greeting_returns_json_with_name():
    payload = json.loads(make_greeting("World"))
    assert payload == {"message": "Hello, World!"}


def test_legacy_process_returns_input():
    assert legacy_process([1, 2, 3]) == [1, 2, 3]
