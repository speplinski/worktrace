#!/usr/bin/env bash
# PILOT — Basal 2.0-max (needs `basal-serve --model Remek/basal-2.0-max-MLX-8bit --mode mlx --port 8000` in another tab).
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
ARMS="factual,remove_X,only_X,invert_X,add_Y,add_Y_remove_X,placebo,sham,copy"
mkdir -p runs/pilot
for split in calibration heldout shifted; do
  case $split in calibration) n=60; arms=$ARMS;; heldout) n=30; arms=$ARMS;; shifted) n=60; arms=factual;; esac
  $PY -m worktrace.run --agent "basal:basal-2.0-max@http://127.0.0.1:8000" --split $split --n $n --arms $arms \
    --retry-errors --out "runs/pilot/basal20max_$split.jsonl"
done
