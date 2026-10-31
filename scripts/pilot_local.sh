#!/usr/bin/env bash
# PILOT — local models (Mac GPU). Safe to stop at any time with Ctrl+C; run the same command again to continue.
# Optional: stop starting new runs at a given time, e.g.  bash scripts/pilot_local.sh 07:30
# Design (preregistration.md): classes c3,c5,c6; calibration 60, held-out 30, shifted 60 base episodes per class;
# 1 seeded run per arm; no null arm (identical under a fixed seed). No --retry-errors: with a fixed seed a failed run
# (timeout, no decision) fails again identically; it counts as an error, as registered (§7).
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
UNTIL=${1:-}
ARMS="factual,remove_X,only_X,invert_X,add_Y,add_Y_remove_X,placebo,sham,copy"
EXTRA=(); [ -n "$UNTIL" ] && EXTRA=(--until "$UNTIL")

run () {  # $1 agent spec, $2 file tag
  for split in calibration heldout shifted; do
    case $split in calibration) n=60; arms=$ARMS;; heldout) n=30; arms=$ARMS;; shifted) n=60; arms=factual;; esac
    $PY -m worktrace.run --agent "$1" --split $split --n $n --arms $arms \
      --out "runs/pilot/$2_$split.jsonl" ${EXTRA[@]+"${EXTRA[@]}"}
  done
}
mkdir -p runs/pilot
# priority order: fast / most informative first
run "systemone:d1"                                              d1
run "ollama:gpt-oss:120b"                                       gptoss120b
run "ollama:mistral-small3.2:24b"                               mistralsmall32
run "ollama-inline:SpeakLeash/bielik-11b-v3.0-instruct:Q8_0"    bielik11b_inline
run "ollama:gemma4:26b"                                         gemma4_26b
run "ollama:qwen3.8:27b"                                        qwen38_27b
# gpt-oss 20B dropped by amendment A9 (same family as gpt-oss 120B; scale is covered by the Claude and GPT-6 series):
# run "ollama:gpt-oss:20b"                                        gptoss20b
echo "All local models done. Push:  git add runs && git commit -m 'Pilot local runs' && git pull --no-rebase --no-edit && git push"
