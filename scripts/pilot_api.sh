#!/usr/bin/env bash
# PILOT — Claude via API (light on the Mac; fine during the day). Stop/continue like the local script.
# Spend caps per model are hard limits checked during the run; total plan ~ $80 of the $100 credit (expires 11 Nov 2026).
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
test -f .env || { echo "Missing .env with WORKTRACE_API_KEY"; exit 1; }
ARMS_ALL="factual,remove_X,only_X,invert_X,add_Y,add_Y_remove_X,null,placebo,sham,copy"
mkdir -p runs/pilot
go () {  # $1 agent $2 tag $3 n_cal $4 n_held $5 n_shift $6 runs $7 cap_usd_per_split
  for split in calibration heldout shifted; do
    case $split in calibration) n=$3; arms=$ARMS_ALL;; heldout) n=$4; arms=$ARMS_ALL;; shifted) n=$5; arms=factual;; esac
    [ "$n" -eq 0 ] && continue
    $PY -m worktrace.run --agent "$1" --split $split --n $n --arms $arms --runs $6 --workers 4 \
      --retry-errors --max-usd $7 --out "runs/pilot/$2_$split.jsonl"
  done
}
go haiku                    haiku55   100 50 100 3 10     # ~ $13
go sonnet                   sonnet55   60 20  60 1 40     # ~ $46
go claude:claude-opus-5-5   opus55     15  0  15 1 20     # ~ $19
echo "API pilot done. Push:  git add runs && git commit -m 'Pilot API runs' && git pull --no-rebase --no-edit && git push"
