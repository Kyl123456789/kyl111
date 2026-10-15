#!/usr/bin/env bash
set -euo pipefail

# run.sh — example run helper
# Usage: bash run.sh "Some input text"

INPUT_TEXT=${1:-"Hello SO101"}
INPUT_FILE=examples_input.txt
OUTPUT_FILE=out.jsonl

mkdir -p examples
printf "%s\n" "$INPUT_TEXT" > "$INPUT_FILE"

python run_so101.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"

echo "Wrote output to $OUTPUT_FILE"
