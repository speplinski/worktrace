# Running the pilot (on your Mac)

One-time setup (Terminal):

```bash
brew install uv git                 # if missing
# Ollama app must be running (menu-bar icon); models used: gpt-oss:20b (and later gpt-oss:120b)
cd ~ && git clone https://github.com/speplinski/worktrace.git && cd worktrace
echo "WORKTRACE_API_KEY=sk-ant-api03-PASTE-YOUR-KEY" > .env     # never committed (.gitignore)
```

Smoke test (≈ 30–90 min; ≈ $1–3 of API credit; Mac must stay awake):

```bash
cd ~/worktrace && git pull
caffeinate -i bash scripts/smoke.sh
```

Every run is saved immediately; if anything stops, run the same command again and it resumes.
When it finishes, push the results (the last line of the script prints the command).

Useful single commands:

```bash
uv run python -m worktrace.run --agent haiku --n 17 --workers 4 --max-usd 5     # Claude Haiku 5.5
uv run python -m worktrace.run --agent ollama:gpt-oss:120b --n 5                 # larger local model
uv run python -m worktrace.score runs/<file>.jsonl                               # metrics, tokens, cost, speed
uv run --group dev pytest -q                                                     # generator / oracle tests
```

## Polish models

```bash
ollama pull SpeakLeash/bielik-11b-v3.0-instruct:Q8_0
bash scripts/ping_polish.sh          # Bielik 11B v3 and PLLuM 12B, 1 episode per class
```

## Basal (decision model, one pass; separate protocol)

Basal answers a typed choice question over a state in one forward pass and returns calibrated probabilities
(https://github.com/rkinas/basal, Apache-2.0). It runs behind its own server, `basal-serve` (MLX on Apple Silicon).
Install in a separate environment (per the Basal INSTALL guide, tag v2.4.1):

```bash
uv venv --python 3.12 --allow-existing ~/basal-mlx && source ~/basal-mlx/bin/activate
uv pip install "basal[mlx] @ https://github.com/rkinas/basal/archive/refs/tags/v2.4.1.tar.gz"
basal-serve --model Remek/basal-2.0-max-MLX-8bit --mode mlx --port 8000      # leave running in its own tab
```

Then, in the worktrace tab:

```bash
uv run python -m worktrace.run --agent "basal:basal-2.0-max@http://127.0.0.1:8000" --n 1 --out runs/ping_basal20max.jsonl
```

## LLM judge (judged-process baselines)

Claude Haiku 5.5 audits the factual decisions already collected (no new agent runs). Cost: about $0.001 per decision.

```bash
git pull --no-rebase --no-edit
bash scripts/judge.sh 20      # trial: 20 decisions, check that it works and what it costs
bash scripts/judge.sh         # everything not yet judged; resumable, cap $10
git add runs && git commit -m "Judge verdicts" && git pull --no-rebase --no-edit && git push
```

Run it again after the local models finish: it judges only the decisions that have no verdict yet.

## Pushing while a local run is still writing

Use `git pull --no-rebase --no-edit` (a merge), not `--rebase`. A rebase refuses to start while the running script
keeps changing `runs/pilot/*.jsonl`; a merge does not touch those files, because only the Mac ever writes them.

## API top-up (amendment A4)

Equalises Sonnet and Opus with the other models on the same episodes (~$39). Runs alongside the local models.

```bash
git pull --no-rebase --no-edit
bash scripts/pilot_api_topup.sh
git add runs && git commit -m "Pilot API top-up"; git pull --no-rebase --no-edit && git push
bash scripts/judge.sh          # then judge the new decisions (~$0.3) and push again
```
