#!/usr/bin/env bash
# Next Anthropic credit cycle (after 11 Nov 2026): Opus 5.5 held-out 30 base episodes per class, completing 60/30/60.
# About $21. Ctrl+C safe; resumable. Covered by amendment A4 (common core), which planned Opus without held-out
# only for budget reasons in the first cycle.
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
test -f .env || { echo "Missing .env with WORKTRACE_API_KEY"; exit 1; }
ARMS_ALL="factual,remove_X,only_X,invert_X,add_Y,add_Y_remove_X,null,placebo,sham,copy"
$PY -m worktrace.run --agent claude:claude-opus-5-5 --split heldout --n 30 --arms $ARMS_ALL --runs 1 \
  --workers 4 --retry-errors --max-usd 24 --out runs/pilot/opus55_heldout.jsonl
echo "Done. Push, then run: bash scripts/judge.sh"
