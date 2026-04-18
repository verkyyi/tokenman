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

# Make pytest / ruff reachable system-wide. Belt + suspenders:
# - Append $HOME/.local/bin to $GITHUB_PATH (visible to subsequent steps)
# - Symlink the binaries into /usr/local/bin (on PATH for every shell,
#   including any subshells claude-code may spawn that don't inherit
#   PATH from the Actions env).
if [ -n "${GITHUB_PATH:-}" ]; then
    echo "$HOME/.local/bin" >> "$GITHUB_PATH"
    echo "--- appended $HOME/.local/bin to \$GITHUB_PATH ---"
fi
if command -v sudo >/dev/null 2>&1; then
    for bin in pytest ruff; do
        src="$HOME/.local/bin/$bin"
        [ -x "$src" ] && sudo ln -sf "$src" "/usr/local/bin/$bin"
    done
    echo "--- symlinked pytest/ruff into /usr/local/bin ---"
    ls -l /usr/local/bin/pytest /usr/local/bin/ruff
fi
