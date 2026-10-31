#!/usr/bin/env bash
# Known-groups test (paper/pilot/known_groups.md): scripted agents with planted deficits. No model, no cost, ~1 minute.
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
ARMS="factual,remove_X,only_X,invert_X,add_Y,add_Y_remove_X,placebo,sham,copy"
for kind in oracle memorised always_escalate copies_count order_cue; do
  for split in calibration heldout shifted; do
    case $split in calibration) n=60; arms=$ARMS;; heldout) n=30; arms=$ARMS;; shifted) n=60; arms=factual;; esac
    $PY -m worktrace.run --agent "deficit:$kind" --split $split --n $n --arms $arms \
      --out "runs/known_groups/${kind}_$split.jsonl" --workers 1 > /dev/null
  done
done
$PY -m worktrace.analysis runs/known_groups --judge-dir none --out paper/pilot/known_groups_results.md > /dev/null
echo "Results: paper/pilot/known_groups_results.md"
