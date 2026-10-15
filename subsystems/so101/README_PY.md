SO-101 Python subsystem

This directory contains a small Python tool to download and prepare SO-101 (SO-ARM100)
model assets into the local subsystem workspace for further processing or usage.

Files added:
- main.py            : CLI tool to download and list assets
- requirements.txt   : Python dependencies

Quick start (Linux/macOS):

1. Create and activate a virtual environment (recommended):

   python3 -m venv .venv
   source .venv/bin/activate

2. Install dependencies:

   pip install -r subsystems/so101/requirements.txt

3. Download assets:

   python subsystems/so101/main.py download

4. List downloaded files:

   python subsystems/so101/main.py list

Notes:
- The script downloads the official SO-ARM100 main branch zip by default. To use a
  different upstream, pass `--url` to the download command.
- Downloaded model files will be placed under `subsystems/so101/files/` and that
  directory is ignored by Git to avoid committing large binaries.
