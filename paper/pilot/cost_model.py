"""Rough cost model for the E1 pilot. Rates: claude-api skill model table (cached 2026-10-06);
verify on the official pricing page before spending. Cache write 1.25x (5-min TTL); batch -50% on all tokens."""
RATES = {  # $/MTok: input, output, cache_read
    "opus-5.5":   (4.00, 20.00, 0.20),
    "sonnet-5.5": (2.00, 10.00, 0.20),
}
CLASSES = 6
RUNS = 3          # repeated runs per (episode, arm)
ARMS = 7          # factual + 4 interventions (remove, only, invert, add-source/composed) + 2 controls (null/placebo, sham)
N_CAL, N_HELD, N_SHIFT = 100, 50, 100   # episodes per class
agent_runs = CLASSES * RUNS * (N_CAL * ARMS + N_HELD * ARMS + N_SHIFT * 1)
judge_calls = 2 * CLASSES * RUNS * (N_CAL + N_HELD + N_SHIFT)   # two LLM-judge baselines on factual runs

def run_cost(model, tok_in, tok_out, f_read, f_write, batch):
    i, o, r = RATES[model]
    fresh = 1 - f_read - f_write
    c = tok_in/1e6 * (fresh*i + f_write*1.25*i + f_read*r) + tok_out/1e6 * o
    return c * (0.5 if batch else 1.0)

print(f"agent runs per configuration: {agent_runs:,}; judge calls: {judge_calls:,}")
scen = {  # tokens in, tokens out (incl. thinking), cache-read share, cache-write share
    "lean (20k in / 1.5k out)":    (20_000, 1_500, 0.75, 0.08),
    "central (30k in / 2.5k out)": (30_000, 2_500, 0.70, 0.10),
    "heavy (60k in / 5k out)":     (60_000, 5_000, 0.65, 0.10),
}
for model in RATES:
    for name, (ti, to, fr, fw) in scen.items():
        for batch in (False, True):
            agent = agent_runs * run_cost(model, ti, to, fr, fw, batch)
            judge = judge_calls * run_cost("sonnet-5.5", 8_000, 600, 0.5, 0.1, batch)
            print(f"{model:10s} {name:28s} batch={str(batch):5s}  agent ${agent:>8,.0f}  + judges ${judge:>5,.0f}  = ${agent+judge:>8,.0f}")
