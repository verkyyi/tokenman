#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_ACTION_PATH:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

if ! command -v gh >/dev/null 2>&1; then
    echo "Tokenman requires the GitHub CLI (gh) on the runner." >&2
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Tokenman requires python3 on the runner." >&2
    exit 1
fi
