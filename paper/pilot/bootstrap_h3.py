"""Configuration bootstrap for the delegation test (H3), DSA vs track record: the mixed model treats a shifted episode
that enters both rules and both k as independent, so its Wald standard error is optimistic (A12). Here configurations
are resampled with replacement (each draw a distinct group) and the model refitted. Usage:
  python paper/pilot/bootstrap_h3.py [--B 1000] [--only core:registered] [--workers 4] [--time]
Run from the repository root. Writes paper/pilot/bootstrap_h3.md and .json. Deterministic: the seed of each cell is the
CRC32 of its name (an earlier version used Python's hash(), which is randomised per process; corrected 2026-11-03)."""
from __future__ import annotations
import argparse, json, math, random, sys, time, zlib
from multiprocessing import Pool
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from worktrace import analysis as A, glmm
from worktrace.answer_key import corrected

HERE = Path(__file__).resolve().parent


def rows_for(data):
    rows = []
    for cfg, recs in sorted(data.items()):
        cal = A.class_measures(recs, "calibration"); sh = A.shifted_error(recs)
        if not cal or not sh or len(cal) < 3:
            continue
        for row in A.h3_rows(cfg, cal, sh):
            for rule in ("DSA", "track record"):
                sels = row["rules"][rule]["selections"]
                for sel in sels:
                    for c in sel:
                        e, n = sh.get(c, (0, 0)); rows.append((cfg, row["k"], rule, e, n, 1 / len(sels)))
    return rows


def fit(rows):
    X, y, w, g = [], [], [], []
    for cfg, k, rule, e, n, wt in rows:
        for yy, cnt in ((1.0, e), (0.0, n - e)):
            if cnt:
                X.append([1.0, float(rule == "DSA"), float(k == 2)]); y.append(yy); w.append(wt * cnt); g.append(cfg)
    f = glmm.fit(np.array(X), np.array(y), g, w=np.array(w), names=["intercept", "DSA", "k2"])
    c = f["coef"]["DSA"]
    return c["est"], c["se"], c["p_lower"], f["converged"]


_G = {}


def _init(by):
    _G["by"] = by


def _fit_sample(samp):
    by = _G["by"]
    rs = [(f"{c}#{i}",) + r[1:] for i, c in enumerate(samp) for r in by[c]]
    try:
        est, se, p, conv = fit(rs)
        return est if conv and math.isfinite(est) and abs(est) < 20 else None
    except Exception:
        return None


def bootstrap(rows, B, seed, workers=4):
    cfgs = sorted({r[0] for r in rows}); by = {c: [r for r in rows if r[0] == c] for c in cfgs}
    rng = random.Random(seed)
    samples = [[rng.choice(cfgs) for _ in cfgs] for _ in range(B)]   # all draws first, so the result is independent of the worker count
    with Pool(workers, initializer=_init, initargs=(by,)) as pool:
        res = pool.map(_fit_sample, samples, chunksize=5)
    ests = [e for e in res if e is not None]
    return ests, len(res) - len(ests)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=1000); ap.add_argument("--only", default=None)
    ap.add_argument("--time", action="store_true"); ap.add_argument("--render", action="store_true"); ap.add_argument("--workers", type=int, default=4); a = ap.parse_args()
    if a.render:
        return render()
    full = A.load(str(HERE.parents[1] / "runs/pilot")); core = {k: [r for r in v if A.in_core(r)] for k, v in full.items()}
    cells = {}
    for dname, data in (("core", core), ("all", full)):
        for key in ("registered", "A1", "reviewed"):
            name = f"{dname}:{key}"
            if a.only and name != a.only:
                continue
            A.SENSITIVITY["on"] = key == "A1"
            d = corrected(data) if key == "reviewed" else data
            rows = rows_for(d)
            A.SENSITIVITY["on"] = False
            t0 = time.time(); est, se, p, conv = fit(rows); dt = time.time() - t0
            if a.time:
                print(f"{name}: one fit {dt:.1f}s, β {est:+.3f} SE {se:.3f} p {p:.4f}"); continue
            ests, failed = bootstrap(rows, a.B, seed=zlib.crc32(name.encode()), workers=a.workers)
            bse = float(np.std(ests, ddof=1)) if len(ests) > 2 else float("nan")
            z = est / bse if bse else float("nan")
            p_norm = 0.5 * math.erfc(-z / math.sqrt(2)) if est < 0 else 1 - 0.5 * math.erfc(z / math.sqrt(2))  # one-sided, H1: β < 0
            p_norm = 0.5 * math.erfc(-z / math.sqrt(2))
            share_ge0 = sum(1 for e in ests if e >= 0) / len(ests) if ests else float("nan")
            lo, hi = (float(np.percentile(ests, 2.5)), float(np.percentile(ests, 97.5))) if ests else (float("nan"),) * 2
            cells[name] = {"beta": est, "wald_se": se, "wald_p": p, "n_cfg": len({r[0] for r in rows}), "B": a.B, "fits": len(ests), "failed": failed,
                           "boot_se": bse, "p_normal_boot_se": p_norm, "share_beta_ge_0": share_ge0, "pct_2_5": lo, "pct_97_5": hi}
            print(name, json.dumps(cells[name]), flush=True)
    if a.time:
        return
    for name, c in cells.items():
        (HERE / f"bootstrap_h3.{name.replace(':', '_')}.json").write_text(json.dumps(c, indent=1))
    render()


def render():
    prev = {}
    for f in sorted(HERE.glob("bootstrap_h3.*_*.json")):
        name = f.stem.split(".", 1)[1].replace("_", ":", 1); prev[name] = json.loads(f.read_text())
    if not prev:
        return
    B = next(iter(prev.values()))["B"]
    L = ["# Configuration bootstrap for the delegation test (DSA vs track record)", "",
         f"Generated by `paper/pilot/bootstrap_h3.py` from `runs/pilot` (final data). Configurations resampled with replacement, {B} resamples per cell, "
         "each resampled configuration a distinct group in the mixed model; seed per cell = CRC32 of the cell name. Wald = the model's own standard error and one-sided p (H1: β_DSA < 0); "
         "bootstrap SE = standard deviation of the resampled estimates; p (bootstrap SE) = one-sided normal p with the bootstrap SE; "
         "share ≥ 0 = share of resampled estimates with β_DSA ≥ 0 (a percentile-type one-sided p); 95% percentile interval of the resamples.", "",
         "| data | key | configurations | β_DSA | Wald SE | Wald p | bootstrap SE | p (bootstrap SE) | share ≥ 0 | 95% interval | fits (failed) |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    order = ["core:registered", "core:A1", "core:reviewed", "all:registered", "all:A1", "all:reviewed"]
    for name in [n for n in order if n in prev] + [n for n in prev if n not in order]:
        c = prev[name]; dn, key = name.split(":")
        L.append(f"| {dn} | {key} | {c['n_cfg']} | {c['beta']:+.3f} | {c['wald_se']:.3f} | {c['wald_p']:.3f} | {c['boot_se']:.3f} | {c['p_normal_boot_se']:.3f} | "
                 f"{c['share_beta_ge_0']:.3f} | [{c['pct_2_5']:+.2f}, {c['pct_97_5']:+.2f}] | {c['fits']} ({c['failed']}) |")
    (HERE / "bootstrap_h3.md").write_text("\n".join(L) + "\n"); print("written", HERE / "bootstrap_h3.md")


if __name__ == "__main__":
    main()
