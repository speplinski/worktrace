"""Leave-one-out robustness of the three theses (common core). Exploratory, not registered: run after every push.

  python -m worktrace.robustness > paper/pilot/robustness_loo.md
"""
from __future__ import annotations

import numpy as np
from collections import defaultdict
from worktrace import analysis as A, glmm

data = A.load("runs/pilot"); data = {k: [r for r in v if A.in_core(r)] for k, v in data.items()}
A.JUDGE.update(A.load_judgments())
ALL_INT = set(A.INTERVENTIONS)

def stats(cfgs, drop_arm=None, sens=False):
    A.SENSITIVITY["on"] = sens
    saved = set(A.INTERVENTIONS)
    if drop_arm:
        A.INTERVENTIONS.discard(drop_arm)
    rows, cells, pooled = [], defaultdict(lambda: [0, 0]), defaultdict(int)
    for cfg in cfgs:
        recs = data[cfg]
        if drop_arm:
            recs = [r for r in recs if r["variant"] != drop_arm]
        cal = A.class_measures(recs, "calibration"); sh = A.shifted_error(recs)
        if not cal:
            continue
        if A.judged(cal):   # pool only fully judged configurations, as report() does
            for c in cal.values():
                for k, v in c["cells"].items(): pooled[k] += v
        if not sh:
            continue
        for r in A.h3_rows(cfg, cal, sh):
            for rule in ("DSA", "track record"):
                sels = r["rules"][rule]["selections"]
                for sel in sels:
                    for c in sel:
                        e, n = sh.get(c, (0, 0)); rows.append((cfg, r["k"], rule, e, n, 1 / len(sels)))
            for base in ("track record", "judged process", "judged grounds"):
                if base in r["rules"] and r["rules"]["DSA"]["selections"] != r["rules"][base]["selections"]:
                    d, b = r["rules"]["DSA"]["err"], r["rules"][base]["err"]
                    if d is not None and b is not None:
                        cells[base][0] += d < b; cells[base][1] += d > b
    A.INTERVENTIONS.clear(); A.INTERVENTIONS.update(saved); A.SENSITIVITY["on"] = False
    X, y, w, g = [], [], [], []
    for cfg, k, rule, e, n, wt in rows:
        for yy, cnt in ((1.0, e), (0.0, n - e)):
            if cnt: X.append([1.0, float(rule == "DSA"), float(k == 2)]); y.append(yy); w.append(wt * cnt); g.append(cfg)
    p = None
    if len(set(g)) > 1:
        f = glmm.fit(np.array(X), np.array(y), g, w=np.array(w), names=["i", "DSA", "k2"]); p = f["coef"]["DSA"]["p_lower"]
    nf = pooled["ifail_jfail"] + pooled["ifail_jpass"]; npass = pooled["ipass_jfail"] + pooled["ipass_jpass"]
    theta = pooled["ifail_jpass"] / nf if nf else None
    fpr = pooled["ipass_jfail"] / npass if npass else None
    return p, dict(cells), theta, nf, fpr

cfgs = sorted(data)
def show(label, res):
    p, cells, th, nf, fpr = res
    c = "; ".join(f"vs {b}: {v[0]}:{v[1]}" for b, v in cells.items())
    print(f"- {label}: GLMM p={p if p is None else round(p,3)} | {c} | judge passes {th if th is None else round(100*th)}% of {nf} wrong-basis, flags {fpr if fpr is None else round(100*fpr)}% of good")
def main():
    print("# Leave-one-out robustness (exploratory, common core)\n")
    print("Each line removes one intervention type or one configuration and recomputes: the registered H3 mixed model "
          "(one-sided p, DSA vs track record), H3 cell counts DSA better:worse against each rule, and how many "
          "interventional basis failures the LLM procedure audit passes.\n")
    for sens in (False, True):
        print("\n## " + ("Without contested arms (A1)" if sens else "Primary") + "\n")
        show("all", stats(cfgs, sens=sens))
        for arm in sorted(ALL_INT):
            show(f"drop arm {arm}", stats(cfgs, drop_arm=arm, sens=sens))
        for c in cfgs:
            show(f"drop {c}", stats([x for x in cfgs if x != c], sens=sens))


if __name__ == "__main__":
    main()
