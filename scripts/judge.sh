#!/usr/bin/env bash
# Post-hoc LLM judge (Claude Haiku 5.5) for the judged-process baselines. Needs WORKTRACE_API_KEY in .env.
# Safe to stop with Ctrl+C; run the same command again to continue. Re-run after new local results arrive.
#   bash scripts/judge.sh          # judge everything not yet judged (cap $10)
#   bash scripts/judge.sh 20       # trial: judge only 20 decisions
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
if [ -n "${1:-}" ]; then
  $PY -m worktrace.judge runs/pilot --workers 4 --max-usd 10 --limit "$1"
else
  $PY -m worktrace.judge runs/pilot --workers 4 --max-usd 10
fi
echo "Push:  git add runs && git commit -m 'Judge verdicts' && git pull --no-rebase --no-edit && git push"
