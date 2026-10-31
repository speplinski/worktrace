#!/usr/bin/env bash
# WorkTrace smoke test. Run from the repository root:  bash scripts/smoke.sh
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
test -f .env || { echo "Missing .env with WORKTRACE_API_KEY=... (see README)"; exit 1; }

echo "== 1/4 Local model connectivity (gpt-oss:20b, 1 episode per class) =="
$PY -m worktrace.run --agent ollama:gpt-oss:20b --n 1 --retry-errors --out runs/smoke_ping_gptoss20b.jsonl

echo "== 2/4 Claude Haiku 5.5: 17 episodes per class x all arms (~460 runs, est. \$1-3, hard cap \$5) =="
$PY -m worktrace.run --agent haiku --n 17 --workers 4 --max-usd 5 --retry-errors --out runs/smoke_haiku.jsonl

echo "== 3/4 Local gpt-oss:20b: 5 episodes per class x all arms (~135 runs; measures speed) =="
$PY -m worktrace.run --agent ollama:gpt-oss:20b --n 5 --retry-errors --out runs/smoke_gptoss20b.jsonl

echo "== 4/4 Scoring =="
$PY -m worktrace.score runs/smoke_haiku.jsonl runs/smoke_gptoss20b.jsonl > runs/smoke_summary.json
cat runs/smoke_summary.json
echo
echo "Done. Now run:  git add runs/smoke_*.jsonl runs/smoke_summary.json && git commit -m 'Smoke test results' && git push"
