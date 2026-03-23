#!/bin/sh
set -e

# Ensure uv uses copy mode to avoid hardlink warnings when cache and target are on different filesystems
if [ -z "$UV_LINK_MODE" ]; then
  export UV_LINK_MODE=copy
fi

# Work in the workspace directory (mount your project to /app so PWD == /app)
cd "$PWD" || true

# If a pyproject.toml exists, optionally compile it to requirements.txt using uv before syncing
if [ -f "pyproject.toml" ]; then
  if command -v uv >/dev/null 2>&1; then
    echo "Detected pyproject.toml — optionally compiling to requirements.txt with uv (for reproducible pins)"
    uv pip compile pyproject.toml -o requirements.txt || echo "'uv pip compile' failed, continuing"
  else
    echo "uv not found; cannot compile pyproject.toml to requirements.txt"
  fi
fi

# Always run uv sync: uv will create/update the project .venv directly (requirements.txt is optional)
if command -v uv >/dev/null 2>&1; then
  echo "Running: uv sync (copy mode) — this will create or update $PWD/.venv; uv operates on the venv itself"
  uv sync --link-mode=copy || echo "'uv sync' failed, continuing to shell"
else
  echo "uv not found; skipping sync. Please ensure uv is installed in the image."
fi

# Exec fish login shell for interactive development
exec /usr/bin/fish -l
