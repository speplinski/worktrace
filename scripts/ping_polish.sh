#!/usr/bin/env bash
# Polish models. Bielik 11B v3 cannot run an interactive tool loop (it simulates the whole trajectory with invented
# document ids), so Polish models run in the ONE-PASS protocol (all documents in context, JSON answer),
# the same protocol as Basal (a decision fine-tune of Bielik 11B v3). 1 episode per class, all arms.
set -uo pipefail
cd "$(dirname "$0")/.."
uv sync -q   # make sure the environment is current, then call its Python directly (clean Ctrl+C)
PY=.venv/bin/python
echo "== Bielik 11B v3.0 (one-pass) =="
$PY -m worktrace.run --agent "ollama-inline:SpeakLeash/bielik-11b-v3.0-instruct:Q8_0" --n 1 --retry-errors --out runs/ping_inline_bielik11b_v3.jsonl
echo "== PLLuM 12B chat (one-pass) =="
$PY -m worktrace.run --agent "ollama-inline:PRIHLOP/PLLuM:12b" --n 1 --retry-errors --out runs/ping_inline_pllum12b.jsonl
echo "== gpt-oss:20b (one-pass, for protocol comparison) =="
$PY -m worktrace.run --agent "ollama-inline:gpt-oss:20b" --n 1 --retry-errors --out runs/ping_inline_gptoss20b.jsonl
$PY -m worktrace.score runs/ping_inline_*.jsonl | grep -E '"(ollama-inline:|runs|errors|no_decision|seconds_per_run|outcome_accuracy|intervention_accuracy)'
