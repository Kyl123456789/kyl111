#!/usr/bin/env python3
"""
SO-101 Model Fetcher and Manager

This script downloads the upstream SO-ARM100 repository zip archive, extracts it,
and copies relevant model asset folders (STL/STEP/CAD/assets/docs) into the
local subsystem `files/` directory.

Usage:
  python main.py download    # download and extract assets
  python main.py list        # list files in the local files/ directory

The script is intentionally dependency-light (requests + tqdm). See requirements.txt.
"""

from __future__ import annotations
import argparse
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    import requests
except Exception:  # pragma: no cover - helpful error message
    print("Missing dependency 'requests'. Install with: pip install -r requirements.txt")
    raise

try:
    from tqdm import tqdm
except Exception:  # pragma: no cover
    print("Missing dependency 'tqdm'. Install with: pip install -r requirements.txt")
    raise


ROOT = Path(__file__).resolve().parent
FILES_DIR = ROOT / "files"
DEFAULT_URL = "https://github.com/TheRobotStudio/SO-ARM100/archive/refs/heads/main.zip"


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(dest, "wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc="Downloading") as pbar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))


def extract_and_copy(zip_path: Path, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        members = z.namelist()
        # Find top-level extracted dir that likely contains SO-ARM100
        top_dirs = sorted({m.split("/")[0] for m in members if "/" in m})
        candidate = None
        for d in top_dirs:
            if "SO-ARM100" in d or "SO-ARM" in d or "SO-ARM100".lower() in d.lower():
                candidate = d
                break
        if candidate is None and top_dirs:
            candidate = top_dirs[0]

        # Extract to temp dir then copy specific folders
        with tempfile.TemporaryDirectory() as tmpd:
            z.extractall(tmpd)
            src_root = Path(tmpd) / candidate
            if not src_root.exists():
                raise RuntimeError(f"Could not find extracted source directory under {candidate}")

            copied_any = False
            for rel in ("STL", "STEP", "CAD", "assets", "docs"):
                src = src_root / rel
                if src.exists() and src.is_dir():
                    dst = target_dir / rel
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    print(f"Copied {rel} -> {dst}")
                    copied_any = True

            if not copied_any:
                # As a fallback, copy all files under src_root that look like models (*.stl, *.step, *.stp)
                patterns = ["**/*.stl", "**/*.STL", "**/*.step", "**/*.stp", "**/*.STEP", "**/*.STP"]
                found = False
                for pat in patterns:
                    for p in src_root.glob(pat):
                        relp = p.relative_to(src_root)
                        dstp = target_dir / relp
                        dstp.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(p, dstp)
                        print(f"Copied model: {relp}")
                        found = True
                if not found:
                    print("Warning: no model directories or model files were found in the upstream archive.")


def list_local_files(target_dir: Path) -> None:
    if not target_dir.exists():
        print(f"Local files directory does not exist: {target_dir}")
        return
    for root, dirs, files in os.walk(target_dir):
        level = Path(root).relative_to(target_dir).parts
        indent = "  " * len(level)
        print(f"{indent}{Path(root).name}/")
        for f in files:
            print(f"{indent}  {f}")


def cmd_download(args: argparse.Namespace) -> int:
    url = args.url or DEFAULT_URL
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "so-arm100.zip"
        print(f"Downloading from: {url}")
        try:
            download_file(url, zip_path)
        except Exception as e:
            print(f"Download failed: {e}")
            return 2
        try:
            extract_and_copy(zip_path, FILES_DIR)
        except Exception as e:
            print(f"Extract/copy failed: {e}")
            return 3
    print(f"Done. Assets available under: {FILES_DIR}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    list_local_files(FILES_DIR)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="so101-manager")
    sub = parser.add_subparsers(dest="cmd")
    p_download = sub.add_parser("download", help="Download and extract SO-ARM100 assets")
    p_download.add_argument("--url", help="Upstream zip URL to download (defaults to official repo)")
    p_list = sub.add_parser("list", help="List files in local files/ directory")

    args = parser.parse_args(argv)
    if args.cmd == "download":
        return cmd_download(args)
    elif args.cmd == "list":
        return cmd_list(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
