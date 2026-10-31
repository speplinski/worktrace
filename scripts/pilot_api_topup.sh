#!/usr/bin/env bash
# Amendment A4: equalise the API models on the common core (same 60 calibration and 60 shifted base episodes per
# class as the local models; Sonnet held-out 20 -> 30). Resumes the existing files: only the missing runs are made.
# Light on the Mac (API, not GPU); can run alongside pilot_local.sh. Ctrl+C safe; run again to continue.
# Caps are cumulative per file (they include what the file already cost). Plan ~ $39.
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
test -f .env || { echo "Missing .env with WORKTRACE_API_KEY"; exit 1; }
ARMS_ALL="factual,remove_X,only_X,invert_X,add_Y,add_Y_remove_X,null,placebo,sham,copy"
R="$PY -m worktrace.run --runs 1 --workers 4 --retry-errors"
$R --agent sonnet                  --split heldout     --n 30 --arms $ARMS_ALL --max-usd 11 --out runs/pilot/sonnet55_heldout.jsonl   # +~$3
$R --agent claude:claude-opus-5-5  --split shifted     --n 60 --arms factual   --max-usd 7  --out runs/pilot/opus55_shifted.jsonl     # +~$5
$R --agent claude:claude-opus-5-5  --split calibration --n 60 --arms $ARMS_ALL --max-usd 44 --out runs/pilot/opus55_calibration.jsonl # +~$31
echo "Top-up done. Push:  git add runs && git commit -m 'Pilot API top-up'; git pull --no-rebase --no-edit && git push"
