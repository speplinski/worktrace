#!/usr/bin/env bash
# OpenAI configurations (amendments A5, A6). Needs WORKTRACE_OPENAI_KEY in .env. API only; Ctrl+C safe, resumable.
#   bash scripts/pilot_openai.sh trial [luna|terra|sol ...]   # smoke episodes (excluded from analysis): setup + cost check
#   bash scripts/pilot_openai.sh full  [luna|terra|sol ...]   # 60/30/60 base episodes per class, shared seeds
# Without model names: luna (agent + Decisions API). Spend caps are cumulative per output file.
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
test -f .env || { echo "Missing .env"; exit 1; }
grep -q WORKTRACE_OPENAI_KEY .env || { echo "Add WORKTRACE_OPENAI_KEY=... to .env"; exit 1; }
ARMS_ALL="factual,remove_X,only_X,invert_X,add_Y,add_Y_remove_X,null,placebo,sham,copy"
R="$PY -m worktrace.run --runs 1 --workers 4 --retry-errors"
MODE="${1:-}"; shift || true
[ $# -eq 0 ] && set -- luna   # no arrays: macOS bash 3.2 + set -u

spec () { case $1 in luna) echo "gpt-6-luna gpt6luna 4 2 1";; terra) echo "gpt-6.1-terra gpt61terra 14 7 2";;
                     sol) echo "gpt-6.1-sol gpt61sol 28 14 4";; *) echo "unknown model $1" >&2; exit 1;; esac; }

for m in "$@"; do
  read -r id tag cap_cal cap_held cap_shift <<<"$(spec "$m")"
  case "$MODE" in
    trial)
      mkdir -p runs/trial
      $R --agent "openai:$id:medium" --split smoke --n 1 --arms $ARMS_ALL --max-usd 1 --out "runs/trial/openai_${tag}_smoke.jsonl"
      if [ "$m" = luna ]; then $R --agent openai-decisions:gpt-6-luna --split smoke --n 1 --arms $ARMS_ALL --max-usd 0.2 \
        --out runs/trial/openai_decisions_smoke.jsonl; fi
      $PY -m worktrace.score "runs/trial/openai_${tag}_smoke.jsonl" | head -40 ;;
    full)
      mkdir -p runs/pilot
      for split in calibration heldout shifted; do
        case $split in calibration) n=60; arms=$ARMS_ALL; cap=$cap_cal;; heldout) n=30; arms=$ARMS_ALL; cap=$cap_held;;
                       shifted) n=60; arms=factual; cap=$cap_shift;; esac
        $R --agent "openai:$id:medium" --split $split --n $n --arms $arms --max-usd $cap --out "runs/pilot/${tag}_$split.jsonl"
        if [ "$m" = luna ]; then $R --agent openai-decisions:gpt-6-luna --split $split --n $n --arms $arms --max-usd 1 \
          --out "runs/pilot/gpt6luna_decisions_$split.jsonl"; fi
      done ;;
    *) echo "Usage: bash scripts/pilot_openai.sh trial|full [luna|terra|sol ...]"; exit 1 ;;
  esac
done
echo "Push:  git add runs && git commit -m 'OpenAI runs'; git pull --no-rebase --no-edit && git push"
