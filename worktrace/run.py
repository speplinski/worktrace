"""Command-line runner. Resumable: every finished run is appended to a JSONL file and skipped next time.

Examples
  uv run python -m worktrace.run --agent scripted:oracle --classes c3,c5,c6 --n 5
  uv run python -m worktrace.run --agent haiku --n 17 --out runs/smoke_haiku.jsonl --workers 4
  uv run python -m worktrace.run --agent ollama:gpt-oss:20b --n 17 --out runs/smoke_gptoss20b.jsonl
  uv run python -m worktrace.score runs/smoke_haiku.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import datetime as _dtm

from . import __version__
from .agents import make_agent
from . import interrupt

START = _dtm.datetime.now()
from .classes import GENERATORS
from .interventions import ARMS_FULL, variants
from .oracles import normative

SEED_BASE = {"calibration": 100_000, "heldout": 200_000, "shifted": 300_000, "smoke": 900_000}


def load_dotenv(path: str = ".env") -> None:
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def build(classes: list[str], n: int, split: str, arms: list[str]):
    jobs = []
    for cls in classes:
        for i in range(n):
            e = GENERATORS[cls](SEED_BASE[split] + i, shift=(split == "shifted"))
            for v in variants(e, arms):
                astar, agree = normative(v)
                if not agree:
                    continue  # discarded: oracles disagree (logged by the generator tests)
                jobs.append((v, sorted(astar)))
    return jobs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True)
    ap.add_argument("--classes", default="c3,c5,c6")
    ap.add_argument("--n", type=int, default=17, help="base episodes per class")
    ap.add_argument("--split", default="smoke", choices=list(SEED_BASE))
    ap.add_argument("--arms", default=",".join(ARMS_FULL))
    ap.add_argument("--runs", type=int, default=1, help="repeated runs per (episode, arm)")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--out", default=None)
    ap.add_argument("--retry-errors", action="store_true", help="re-run runs that ended without a decision")
    ap.add_argument("--until", default=None, help="local time HH:MM after which no new runs start (night batches)")
    ap.add_argument("--max-usd", type=float, default=None, help="stop when the estimated spend reaches this")
    a = ap.parse_args(argv)
    load_dotenv()

    agent = make_agent(a.agent)
    out = Path(a.out or f"runs/{a.split}_{a.agent.replace(':', '_').replace('/', '_')}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            r = json.loads(line)
            key = (r["episode_id"], r["run"])
            if r.get("decision") and not r.get("error"):
                done.add(key)
            elif not a.retry_errors:
                done.add(key)
    jobs = [(v, astar, k) for v, astar in build(a.classes.split(","), a.n, a.split, a.arms.split(","))
            for k in range(a.runs) if (v.id, k) not in done]
    print(f"{agent.name}: {len(jobs)} runs to do ({len(done)} already in {out})", flush=True)

    from .score import cost_of  # local import keeps scoring optional
    prior = 0.0
    if out.exists():  # the spend cap is cumulative over resumed sessions
        prior = sum(cost_of(json.loads(l)) for l in out.read_text().splitlines() if l.strip())
    lock, spent, count = threading.Lock(), [prior], [0]

    interrupt.install()

    def work(job):
        v, astar, k = job
        if interrupt.STOP.is_set():
            return None
        if a.max_usd is not None and spent[0] >= a.max_usd:
            return None
        if a.until:
            import datetime as _dt
            hh, mm = map(int, a.until.split(":"))
            now = _dt.datetime.now()
            stop = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
            started = START
            if stop <= started:          # window crosses midnight
                stop += _dt.timedelta(days=1)
            if now >= stop:
                return None
        res = agent.run(v)
        rec = {"gen_version": __version__, "split": a.split, "agent": agent.name, "episode_id": v.id, "base_id": v.base_id or v.id, "cls": v.cls,
               "variant": v.variant, "run": k, "astar": astar, "decisive": v.decisive,
               "allowed": v.allowed_actions, "source_ids": [s.id for s in v.sources], **res}
        with lock:
            with out.open("a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            spent[0] += cost_of(rec)
            count[0] += 1
            if count[0] % 10 == 0 or count[0] == len(jobs):
                print(f"  {count[0]}/{len(jobs)} runs · est. ${spent[0]:.2f}", flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for f in as_completed(futs):
            f.result()
    if interrupt.STOP.is_set():
        print(f"Stopped by Ctrl+C after {count[0]} new runs (est. ${spent[0]:.2f}). Results so far: {out}")
        return 130
    if a.max_usd is not None and spent[0] >= a.max_usd:
        print(f"Stopped at the spend cap (${a.max_usd:.2f}). Re-run the same command to continue.")
    if a.until:
        print(f"Stopped or finished within the time window (until {a.until}). Re-run the same command to continue.")
    print(f"Done. Results: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
