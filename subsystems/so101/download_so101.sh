#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$ROOT_DIR/files"
DOWNLOAD_DIR="$(mktemp -d)"
trap 'rm -rf "$DOWNLOAD_DIR"' EXIT

mkdir -p "$TARGET_DIR"

SOURCE_URL="https://github.com/TheRobotStudio/SO-ARM100/archive/refs/heads/main.zip"
ZIP_PATH="$DOWNLOAD_DIR/so-arm100.zip"

echo "Downloading SO-ARM100 source archive..."
if command -v curl >/dev/null 2>&1; then
  curl -L --fail "$SOURCE_URL" -o "$ZIP_PATH"
elif command -v wget >/dev/null 2>&1; then
  wget -O "$ZIP_PATH" "$SOURCE_URL"
else
  echo "Error: curl or wget required to download upstream archive." >&2
  exit 1
fi

unzip -q "$ZIP_PATH" -d "$DOWNLOAD_DIR"

SRC_DIR="$(find "$DOWNLOAD_DIR" -maxdepth 2 -mindepth 1 -type d -name 'SO-ARM100-*' | head -n 1)"

if [ -z "$SRC_DIR" ]; then
  SRC_DIR="$(find "$DOWNLOAD_DIR" -maxdepth 2 -mindepth 1 -type d -name 'SO-ARM100*' | head -n 1)"
fi

if [ -z "$SRC_DIR" ]; then
  echo "Error: extracted source directory not found." >&2
  exit 1
fi

echo "Extracting model asset directories..."
for REL_PATH in STL STEP CAD; do
  if [ -d "$SRC_DIR/$REL_PATH" ]; then
    echo "Copying $REL_PATH..."
    cp -a "$SRC_DIR/$REL_PATH" "$TARGET_DIR/"
  fi
done

for ITEM in assets docs; do
  if [ -d "$SRC_DIR/$ITEM" ]; then
    echo "Copying $ITEM..."
    cp -a "$SRC_DIR/$ITEM" "$TARGET_DIR/"
  fi
done

echo "SO-101 assets downloaded to: $TARGET_DIR"
