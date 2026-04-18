#!/usr/bin/env bash
# Install the runtime dependencies this skill needs on a fresh runner.
# Called by tokenman-run.yml before `claude -p` invokes the skill.
set -euo pipefail

python3 -m pip install --break-system-packages --quiet pytest ruff
