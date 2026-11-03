"""Two-way (configuration x episode) bootstrap for the delegation test (H3), DSA vs track record. Post hoc robustness
check added before submission (2026-11-03): shifted episodes are shared across configurations, rules and values of k,
so observations are crossed by configuration and episode; the configuration bootstrap of bootstrap_h3.py holds the
episode sample fixed. Here each resample draws configurations with replacement and, independently, base episodes with
replacement within each (split, class) stratum, the same episode draws applying to every drawn configuration (a cluster
bootstrap: an episode cluster is every record of that base episode, all configurations, runs and arms). In each resample
the whole chain is repeated: certification on the resampled calibration episodes, class selection at matched coverage
with the A7 tie weights, shifted outcome error on the resampled shifted episodes, and the registered mixed model.
Reported: β_DSA on the original data, bootstrap SE, 95% percentile interval, share of resamples with β ≥ 0 (descriptive),
one-sided p from a normal approximation with the bootstrap SE, and a recentred bootstrap p under H0: β = 0
(share of resamples with β* ≤ 2·β̂, i.e. β* − β̂ ≤ β̂). Usage:
  python paper/pilot/bootstrap_two_way.py [--B 1000] [--only core:registered] [--workers 4]
Run from the repository root. Writes paper/pilot/bootstrap_two_way.md and one .json per cell. Deterministic (seed per cell)."""
from __future__ import annotations
import argparse, json, math, random, sys, time
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from worktrace import analysis as A
from worktrace.answer_key import corrected
from bootstrap_h3 import rows_for, fit  # same chain and model as the configuration bootstrap

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPLITS = ("calibration", "shifted")


def strata(data):
    """(split, cls) -> sorted base ids present in any configuration."""
    s = defaultdict(set)
    for recs in data.values():
        for r in recs:
            if r["split"] in SPLITS:
                s[(r["split"], r["cls"])].add(r["base_id"])
    return {k: sorted(v) for k, v in s.items()}


def resample(data, strata_ids, rng):
    cfgs = sorted(data)
    draws = {k: [rng.choice(ids) for _ in ids] for k, ids in strata_ids.items()}
    # how many times each base id is drawn in its stratum
    mult = {k: defaultdict(int) for k in draws}
    for k, ds in draws.items():
        for b in ds:
            mult[k][b] += 1
    out = {}
    for i, c in enumerate(rng.choice(cfgs) for _ in cfgs):
        recs = []
        for r in data[c]:
            if r["split"] not in SPLITS:
                continue
            m = mult[(r["split"], r["cls"])].get(r["base_id"], 0)
            for j in range(m):
                recs.append(r if j == 0 else dict(r, run=r["run"] + 1000 * j))
        out[f"{c}#{i}"] = recs
    return out


_G = {}


def _init(data, strata_ids, key):
    """Pool initializer: the data are sent to each worker once (spawn-safe on macOS), not with every task."""
    _G.update(data=data, strata=strata_ids, key=key)
    A.SENSITIVITY["on"] = key == "A1"


def one(seed):
    data, strata_ids = _G["data"], _G["strata"]
    rng = random.Random(seed)
    try:
        rows = rows_for(resample(data, strata_ids, rng))
        est, se, p, conv = fit(rows)
        ok = conv and math.isfinite(est) and abs(est) < 20
        return est if ok else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=1000); ap.add_argument("--only", default=None)
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--render", action="store_true"); a = ap.parse_args()
    if a.render:
        return render()
    full = A.load(str(ROOT / "runs/pilot")); core = {k: [r for r in v if A.in_core(r)] for k, v in full.items()}
    for dname, data in (("core", core), ("all", full)):
        for key in ("registered", "A1", "reviewed"):
            name = f"{dname}:{key}"
            if a.only and name != a.only:
                continue
            d = corrected(data) if key == "reviewed" else data
            d = {k: [r for r in v if r["split"] in SPLITS] for k, v in d.items()}
            A.SENSITIVITY["on"] = key == "A1"
            est, se, p, conv = fit(rows_for(d))
            A.SENSITIVITY["on"] = False
            st = strata(d)
            seed0 = sum(ord(ch) for ch in name) * 1000003
            t0 = time.time()
            with Pool(a.workers, initializer=_init, initargs=(d, st, key)) as pool:
                res = pool.map(one, [seed0 + b for b in range(a.B)], chunksize=5)
            ests = [e for e in res if e is not None]; failed = len(res) - len(ests)
            bse = float(np.std(ests, ddof=1)); z = est / bse
            p_norm = 0.5 * math.erfc(-z / math.sqrt(2))                       # one-sided, H1: β < 0
            p_recentred = sum(1 for e in ests if e <= 2 * est) / len(ests)   # H0: β = 0, recentred (β* − β̂ ≤ β̂)
            share_ge0 = sum(1 for e in ests if e >= 0) / len(ests)
            cell = {"beta": est, "wald_se": se, "wald_p": p, "n_cfg": len(d), "strata": {f"{s}/{c}": len(v) for (s, c), v in st.items()},
                    "B": a.B, "fits": len(ests), "failed": failed, "boot_se": bse, "p_normal_boot_se": p_norm,
                    "p_recentred": p_recentred, "share_beta_ge_0": share_ge0,
                    "pct_2_5": float(np.percentile(ests, 2.5)), "pct_97_5": float(np.percentile(ests, 97.5)),
                    "seconds": round(time.time() - t0)}
            (HERE / f"bootstrap_two_way.{name.replace(':', '_')}.json").write_text(json.dumps(cell, indent=1))
            print(name, json.dumps(cell), flush=True)
    render()


def render():
    prev = {}
    for f in sorted(HERE.glob("bootstrap_two_way.*_*.json")):
        name = f.stem.split(".", 1)[1].replace("_", ":", 1); prev[name] = json.loads(f.read_text())
    if not prev:
        return
    L = ["# Two-way bootstrap (configurations × episodes) for the delegation test (DSA vs track record)", "",
         "Post hoc robustness check (added 2026-11-03, before submission). Generated by `paper/pilot/bootstrap_two_way.py` from `runs/pilot` (final data). "
         "Each resample draws configurations with replacement and, independently, base episodes with replacement within each (split, class) stratum, "
         "the same episode draws for every drawn configuration; certification, class selection (A7 tie weights), shifted error and the mixed model are "
         "repeated in every resample. β_DSA = estimate on the original data; Wald = the model's own SE and one-sided p; bootstrap SE = SD of the resampled "
         "estimates; p (normal) = one-sided normal p with the bootstrap SE; p (recentred) = share of resamples with β* ≤ 2β̂ (H0: β = 0); share ≥ 0 = share of "
         "resampled estimates with β_DSA ≥ 0 (descriptive); 95% percentile interval.", "",
         "| data | key | configurations | β_DSA | Wald SE (p) | bootstrap SE | p (normal) | p (recentred) | share ≥ 0 | 95% interval | fits (failed) | seconds |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    order = ["core:registered", "core:A1", "core:reviewed", "all:registered", "all:A1", "all:reviewed"]
    for name in [n for n in order if n in prev] + [n for n in prev if n not in order]:
        c = prev[name]; dn, key = name.split(":")
        L.append(f"| {dn} | {key} | {c['n_cfg']} | {c['beta']:+.3f} | {c['wald_se']:.3f} ({c['wald_p']:.3f}) | {c['boot_se']:.3f} | {c['p_normal_boot_se']:.3f} | "
                 f"{c['p_recentred']:.3f} | {c['share_beta_ge_0']:.3f} | [{c['pct_2_5']:+.2f}, {c['pct_97_5']:+.2f}] | {c['fits']} ({c['failed']}) | {c['seconds']} |")
    (HERE / "bootstrap_two_way.md").write_text("\n".join(L) + "\n"); print("written", HERE / "bootstrap_two_way.md")


if __name__ == "__main__":
    main()
