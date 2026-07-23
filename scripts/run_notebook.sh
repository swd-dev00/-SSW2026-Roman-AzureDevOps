#!/usr/bin/env bash
set -euo pipefail

NOTEBOOK="/workspace/notebooks/SSW2026_Merged_Advanced_DarkLens_SED_Fitting.ipynb"
OUTPUT_DIR="/workspace/executed"
OUTPUT_NAME="SSW2026_Merged_Advanced_DarkLens_SED_Fitting_executed.ipynb"

mkdir -p "$OUTPUT_DIR"

jupyter nbconvert \
  --to notebook \
  --execute "$NOTEBOOK" \
  --output "$OUTPUT_NAME" \
  --output-dir "$OUTPUT_DIR" \
  --ExecutePreprocessor.timeout=-1 \
  --ExecutePreprocessor.kernel_name=python3
