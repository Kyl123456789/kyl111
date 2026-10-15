#!/usr/bin/env bash
# Convenience runner for the SO-101 Python subsystem.
# Usage: ./run_so101.sh download|list [--url URL]
set -euo pipefail

# If a venv exists in .venv, prefer using it; otherwise fall back to system python
if [ -f .venv/bin/activate ]; then
  . .venv/bin/activate
fi

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 download|list [--url URL]"
  exit 2
fi

CMD="$1"
shift || true

python -m subsystems.so101 "$CMD" "$@"
