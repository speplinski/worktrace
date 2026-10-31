"""Judge-capability check (amendment A10): does a stronger judge from another developer discriminate basis failures
that the Haiku 5.5 judge does not? Same rubric (judge-v2), same prompt, same decisions.

  python -m worktrace.judge_check sample             # draw the stratified sample (deterministic), write it, no API calls
  python -m worktrace.judge_check run --limit 10     # trial
  python -m worktrace.judge_check run                # all sampled decisions (cap $6.5)
  python -m worktrace.judge_check analyse            # compare the two judges on the same decisions

Needs WORKTRACE_OPENAI_KEY in .env for `run`.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

from . import analysis as A
from . import interrupt
from .judge import RUBRIC_VERSION, SCHEMA, SYSTEM, prompt_for
from .run import load_dotenv

OUT = Path("runs/judge_check")
SAMPLE = OUT / "sample.json"
VERDICTS = OUT / "judge_gpt61sol.jsonl"
MODEL, EFFORT = "gpt-6.1-sol", "medium"
RATES = (2.00, 10.00, 0.10)   # gpt-6.1-sol, $/MTok input, output, cached input (developers.openai.com pricing, 2026-10-26)
CONFIGS = ["claude:claude-opus-5-5:medium", "claude:claude-sonnet-5-5:medium", "claude:claude-haiku-5-5:medium",
           "openai:gpt-6-luna:medium", "openai:gpt-6.1-terra:medium"]   # GPT-6.1 Sol itself excluded (self-judging)
PER_STRATUM, SEED = 20, 20261027


def _units_with_labels(key: str = "registered") -> list[dict]:
    """Basis labels under the registered key (default), without the contested arms ("A1") or under the reviewed key
    ("reviewed"; decisions that are no longer correct outcomes under that key are dropped)."""
    data, J = A.load("runs/pilot"), A.load_judgments()
    if key == "reviewed":
        from .answer_key import corrected
        data = corrected(data)
    rows = []
    for cfg in CONFIGS:
        for (cls, base, run), vs in A.units(data[cfg], "calibration").items():
            f = vs["factual"]
            if run != 0 or A._act(f) not in f["astar"]:
                continue
            j = J.get((f["agent"], "calibration", f["episode_id"], run))
            if j is None:
                continue
            ifail = any(A._act(v) not in v["astar"] for n, v in vs.items()
                        if n in A.INTERVENTIONS and not (key == "A1" and A.contested(v)))
            rows.append({"agent": cfg, "split": "calibration", "episode_id": f["episode_id"], "run": run, "cls": cls,
                         "basis_failure": ifail, "haiku_basis_sound": j["basis_sound"], "rec": f})
    return rows


def draw_sample() -> list[dict]:
    rng = random.Random(SEED)
    rows = _units_with_labels()
    picked = []
    for cfg in CONFIGS:
        for label in (True, False):
            pool = sorted((r for r in rows if r["agent"] == cfg and r["basis_failure"] == label), key=lambda r: r["episode_id"])
            picked += rng.sample(pool, min(PER_STRATUM, len(pool)))
    return picked


def cmd_sample() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    s = draw_sample()
    SAMPLE.write_text(json.dumps([{k: v for k, v in r.items() if k != "rec"} for r in s], indent=1))
    by = {}
    for r in s:
        by.setdefault(r["agent"], [0, 0])[0 if r["basis_failure"] else 1] += 1
    print(f"{len(s)} decisions -> {SAMPLE}")
    for a, (w, ok) in by.items():
        print(f"  {a}: basis failure {w}, right basis {ok}")
    return 0


def _post(http, body):
    for attempt in range(6):
        r = http.post("/responses", json=body)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 ** attempt); continue
        if r.status_code >= 400:
            raise RuntimeError(f"http_{r.status_code}:{r.text[:300]}")
        return r.json()
    raise RuntimeError("retries exhausted")


def cmd_run(limit: int | None, max_usd: float) -> int:
    import os, httpx
    load_dotenv()
    key = os.environ.get("WORKTRACE_OPENAI_KEY")
    if not key:
        print("Add WORKTRACE_OPENAI_KEY to .env"); return 1
    sample = json.loads(SAMPLE.read_text())
    recs = {(r["agent"], r["split"], r["episode_id"], r["run"]): r["rec"] for r in _units_with_labels()}
    done, spent = set(), 0.0
    if VERDICTS.exists():
        for line in VERDICTS.read_text().splitlines():
            j = json.loads(line)
            u = j.get("usage") or {}
            spent += (u.get("input", 0) * RATES[0] + u.get("cache_write", 0) * 1.25 * RATES[0] + u.get("cache_read", 0) * RATES[2] + u.get("output", 0) * RATES[1]) / 1e6
            if j.get("verdict"):
                done.add((j["agent"], j["split"], j["episode_id"], j["run"]))
    todo = [s for s in sample if (s["agent"], s["split"], s["episode_id"], s["run"]) not in done][: limit or None]
    print(f"Judge {MODEL} ({RUBRIC_VERSION}): {len(todo)} to judge, {len(done)} done, spent ${spent:.2f}")
    http = httpx.Client(base_url="https://api.openai.com/v1", timeout=600, headers={"Authorization": f"Bearer {key}"})
    interrupt.install()
    from .openai_agents import _usage
    for i, s in enumerate(todo, 1):
        if interrupt.STOP.is_set() or spent >= max_usd:
            break
        rec = recs[(s["agent"], s["split"], s["episode_id"], s["run"])]
        out: dict[str, Any] = {"judge": f"{MODEL}:{EFFORT}", "rubric": RUBRIC_VERSION, **{k: s[k] for k in ("agent", "split", "episode_id", "run")},
                               "verdict": None, "error": None}
        t0 = time.time()
        try:
            r = _post(http, {"model": MODEL, "instructions": SYSTEM, "input": prompt_for(rec), "reasoning": {"effort": EFFORT},
                             "text": {"format": {"type": "json_schema", "name": "verdict", "schema": SCHEMA, "strict": True}}})
            out["usage"] = _usage(r.get("usage") or {})
            text = "".join(c.get("text", "") for o in r.get("output", []) if o.get("type") == "message"
                           for c in o.get("content", []) if c.get("type") == "output_text")
            out["verdict"] = json.loads(text)
        except Exception as ex:
            out["error"] = f"{type(ex).__name__}: {str(ex)[:300]}"
        out["seconds"] = round(time.time() - t0, 2)
        u = out.get("usage") or {}
        spent += (u.get("input", 0) * RATES[0] + u.get("cache_write", 0) * 1.25 * RATES[0] + u.get("cache_read", 0) * RATES[2] + u.get("output", 0) * RATES[1]) / 1e6
        with VERDICTS.open("a") as f:
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
        if i % 10 == 0 or i == len(todo):
            print(f"  {i}/{len(todo)} judged · est. ${spent:.2f}", flush=True)
    if interrupt.STOP.is_set():
        print("Stopped by Ctrl+C. Re-run the same command to continue."); return 130
    print(f"Done. Verdicts: {VERDICTS}")
    return 0


def _j(rows, judge_key):
    w = [r for r in rows if r["basis_failure"]]; ok = [r for r in rows if not r["basis_failure"]]
    sens = sum(not r[judge_key] for r in w) / len(w) if w else float("nan")
    fpr = sum(not r[judge_key] for r in ok) / len(ok) if ok else float("nan")
    return sens - fpr, sens, fpr


def cmd_analyse(key: str = "registered") -> int:
    sample = json.loads(SAMPLE.read_text())
    if key != "registered":   # relabel the registered sample under another key; decisions no longer correct are dropped
        lab = {(r["agent"], r["split"], r["episode_id"], r["run"]): r["basis_failure"] for r in _units_with_labels(key)}
        kept = [dict(s, basis_failure=lab[k]) for s in sample if (k := (s["agent"], s["split"], s["episode_id"], s["run"])) in lab]
        print(f"Key {key}: {len(kept)} of {len(sample)} sampled decisions still correct outcomes; basis failures "
              f"{sum(r['basis_failure'] for r in kept)} (registered labels on the same decisions: "
              f"{sum(s['basis_failure'] for s in sample if (s['agent'], s['split'], s['episode_id'], s['run']) in lab)})")
        sample = kept
    sol = {}
    for line in VERDICTS.read_text().splitlines():
        j = json.loads(line)
        if j.get("verdict"):
            sol[(j["agent"], j["split"], j["episode_id"], j["run"])] = j["verdict"]["basis_sound"]
    rows = [{**s, "sol_basis_sound": sol[k]} for s in sample
            if (k := (s["agent"], s["split"], s["episode_id"], s["run"])) in sol]
    print(f"Decisions judged by both: {len(rows)} of {len(sample)}")

    def report(label, rs):
        jh, sh, fh = _j(rs, "haiku_basis_sound"); js, ss, fs = _j(rs, "sol_basis_sound")
        print(f"{label:28s} n={len(rs):3d} | Haiku J {jh:+.2f} (sens {sh:.2f}, FPR {fh:.2f}) | Sol J {js:+.2f} (sens {ss:.2f}, FPR {fs:.2f})")
    report("all", rows)
    report("Anthropic decisions", [r for r in rows if r["agent"].startswith("claude")])
    report("OpenAI decisions", [r for r in rows if r["agent"].startswith("openai")])
    rng = random.Random(1)
    w = [r for r in rows if r["basis_failure"]]; ok = [r for r in rows if not r["basis_failure"]]
    diffs = []
    for _ in range(4000):
        bs = [rng.choice(w) for _ in w] + [rng.choice(ok) for _ in ok]
        diffs.append(_j(bs, "sol_basis_sound")[0] - _j(bs, "haiku_basis_sound")[0])
    diffs.sort()
    js = _j(rows, "sol_basis_sound")[0]
    lo, hi = diffs[int(.025 * len(diffs))], diffs[int(.975 * len(diffs))]
    print(f"J(Sol) - J(Haiku) = {js - _j(rows, 'haiku_basis_sound')[0]:+.2f}, 95% bootstrap CI [{lo:+.2f}, {hi:+.2f}]")
    verdict = ("weak-judge account supported" if js >= 0.30 and lo > 0 else
               "convincing-explanations account supported" if js < 0.15 else "inconclusive")
    print(f"Pre-specified reading (A10): {verdict}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "run", "analyse"])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--max-usd", type=float, default=6.5)
    ap.add_argument("--key", default="registered", choices=["registered", "A1", "reviewed"])
    a = ap.parse_args(argv)
    if a.cmd == "sample":
        return cmd_sample()
    if a.cmd == "run":
        return cmd_run(a.limit, a.max_usd)
    return cmd_analyse(a.key)


if __name__ == "__main__":
    sys.exit(main())
