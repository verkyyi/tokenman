#!/usr/bin/env bash
# Install the runtime dependencies this skill needs on a fresh runner.
# Called by tokenman-run.yml before `claude -p` invokes the skill.
set -euo pipefail

echo "--- python3 before install ---"
python3 --version
python3 -m pip --version

echo "--- pip install pytest ruff ---"
python3 -m pip install --break-system-packages pytest ruff

echo "--- verify tools reachable ---"
python3 -m pytest --version
python3 -m ruff --version
which pytest  || echo "  (pytest binary not on PATH; python3 -m pytest still works)"
which ruff    || echo "  (ruff binary not on PATH; python3 -m ruff still works)"

# Make user-installed binaries visible to subsequent workflow steps
# (Claude's bash tool inherits the step's PATH). Without this, `pytest`
# on PATH is not found and the skill aborts with no-test-harness.
if [ -n "${GITHUB_PATH:-}" ]; then
    echo "$HOME/.local/bin" >> "$GITHUB_PATH"
    echo "--- appended $HOME/.local/bin to \$GITHUB_PATH ---"
fi
