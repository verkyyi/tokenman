"""Read Claude-Code plugin marketplace manifests.

Reads local caches at ~/.claude/plugins/marketplaces/<name>/.claude-plugin/
marketplace.json. Malformed manifests are skipped with a warning; missing
cache root returns an empty list.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, TypedDict


class Plugin(TypedDict):
    name: str
    description: str
    category: Optional[str]
    homepage: Optional[str]
    marketplace: str


def marketplace_root() -> Path:
    return Path.home() / ".claude" / "plugins" / "marketplaces"


def list_plugins(*, root: Optional[Path] = None, refresh: bool = False) -> list[Plugin]:
    if refresh:
        subprocess.run(
            ["claude", "plugins", "marketplace", "update"],
            capture_output=True,
            text=True,
        )

    base = root if root is not None else marketplace_root()
    if not base.exists():
        return []

    plugins: list[Plugin] = []
    for manifest_path in sorted(base.glob("*/.claude-plugin/marketplace.json")):
        marketplace_name = manifest_path.parent.parent.name
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(
                f"warning: skipping malformed marketplace {marketplace_name!r}: {exc}",
                file=sys.stderr,
            )
            continue

        for entry in data.get("plugins", []):
            if not isinstance(entry, dict) or "name" not in entry:
                continue
            plugins.append(Plugin(
                name=str(entry["name"]),
                description=str(entry.get("description", "")),
                category=entry.get("category"),
                homepage=entry.get("homepage"),
                marketplace=marketplace_name,
            ))
    return plugins
