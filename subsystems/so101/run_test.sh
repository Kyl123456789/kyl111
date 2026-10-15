#!/usr/bin/env bash
# Simple test runner for the Python subsystem (runs inside repo root)
set -euo pipefail

python3 -m venv .venv_test
. .venv_test/bin/activate
pip install --upgrade pip
pip install -r subsystems/so101/requirements.txt
python subsystems/so101/main.py download --url https://github.com/TheRobotStudio/SO-ARM100/archive/refs/heads/main.zip
python subsystems/so101/main.py list

echo "Python subsystem test completed."
