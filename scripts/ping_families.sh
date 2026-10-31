#!/usr/bin/env bash
# Other model families. Pull first:
#   ollama pull qwen3.8:27b ; ollama pull mistral-small3.2:24b ; ollama pull d1
# (gemma4:26b and gpt-oss:120b already installed). 1 episode per class, all arms.
set -uo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
for m in "qwen3.8:27b" "mistral-small3.2:24b" "gemma4:26b" "gpt-oss:120b"; do
  f="runs/ping_agent_$(echo "$m" | tr ':/.' '___').jsonl"
  echo "== $m (agent with tools) =="
  $PY -m worktrace.run --agent "ollama:$m" --n 1 --retry-errors --out "$f"
done
echo "== Liquid AI d1 (decision model via Ollama /v1/systemone) =="
$PY -m worktrace.run --agent "systemone:d1" --n 1 --retry-errors --out runs/ping_decision_d1.jsonl
$PY -m worktrace.score runs/ping_agent_*.jsonl runs/ping_decision_d1.jsonl | grep -E '"(ollama:|systemone:|runs|errors|no_decision|text_fallback|runs_with_text_tool_calls|runs_with_server_errors|seconds_per_run|outcome_accuracy|intervention_accuracy)'
