# SO-101 subsystem

This directory contains the tooling to fetch the official SO-101 / SO-ARM100 source assets into the repo-local workspace.

## Structure

- `download_so101.sh` downloads the official repository and extracts the asset directories
- `files/` stores the downloaded content locally (ignored by Git)

## Quick start

```bash
chmod +x subsystems/so101/download_so101.sh
./subsystems/so101/download_so101.sh
```

## What it downloads

The script fetches the official upstream project and copies the STL / STEP / CAD related asset folders if present.

## Upstream source

- https://github.com/TheRobotStudio/SO-ARM100

## Notes

- The downloaded model files are intentionally kept out of Git to avoid large binary diffs.
- You can inspect the extracted files under `subsystems/so101/files/`.
