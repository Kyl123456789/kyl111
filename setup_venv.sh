#!/usr/bin/env bash
set -euo pipefail

# setup_venv.sh
# Create and activate a Python virtual environment in .venv and install deps.

VENV_DIR=.venv
PYTHON=${PYTHON:-python3}

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python not found: $PYTHON" >&2
  exit 1
fi

$PYTHON -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install -U pip
pip install -r requirements.txt

echo "Virtual environment created at $VENV_DIR and dependencies installed.\nActivate with: source $VENV_DIR/bin/activate"
