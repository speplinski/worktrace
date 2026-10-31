"""Construct validity (CV1, CV2; preregistration §6) and two exploratory tables asked for by the reviews.

CV1: is l_basis among correct outcomes reducible to outcome accuracy? Across (configuration, class) cells of the
     calibration split: Pearson and Spearman correlation between l_out and l_basis|correct, and the share of the
     variance of l_basis|correct that a linear regression on l_out leaves unexplained (1 - R^2). Also across
     configurations (classes pooled).
CV2: variance decomposition of the unit-level basis loss into configuration, class, their interaction and the
     within-cell residual (ANOVA sums of squares over calibration units). The seed (run) component is estimated from
     the one configuration with repeated runs (Claude Haiku 5.5, three runs per episode): share of the within-episode
     variance across runs.
Certified sets: what each rule certified and the shifted outcome error of those classes, pooled.
H3 on c3 and c5 only: the matched-coverage comparison with c6 removed (k = 1), DSA vs track record.

Three keys: registered A*, contested arms excluded (A1), reviewed key (A13). Common core and all data. Exploratory
except CV1 and CV2, which were pre-registered as secondary hypotheses. Usage: python paper/pilot/construct_validity.py
(from the repository root); writes construct_validity.md next to this file.
"""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, ".")
import numpy as np
from worktrace import analysis as A
from worktrace import answer_key as K

OUT = Path(__file__).resolve().parent / "construct_validity.md"
A.JUDGE.update(A.load_judgments("runs/judge"))


def unit_losses(recs, split="calibration"):
    """Per unit (class, base, run): (l_out, l_basis) under the current SENSITIVITY setting."""
    out = {}
    for (cls, base, run), vs in A.units(recs, split).items():
        f = vs.get("factual")
        if f is None:
            continue
        fa = A._act(f)
        lout = fa not in f["astar"]
        lbasis = False
        for name, v in vs.items():
            if name == "factual" or name in A.CONTROLS:
                continue
            if A.SENSITIVITY["on"] and A.contested(v):
                continue
            lbasis |= A._act(v) not in v["astar"]
        out[(cls, base, run)] = (int(lout), int(lbasis))
    return out


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3 or x.std() == 0 or y.std() == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    from scipy.stats import rankdata
    if len(x) < 3:
        return None
    return pearson(rankdata(x), rankdata(y))


def cv1(data):
    cells = []   # (cfg, cls, l_out, l_basis_given_correct, n_correct)
    for cfg, recs in sorted(data.items()):
        ul = unit_losses(recs)
        by = defaultdict(list)
        for (cls, _, _), v in ul.items():
            by[cls].append(v)
        if len(by) < 3:          # partial configuration (a run in progress): not comparable, as in the H3 analyses
            continue
        for cls, vs in by.items():
            n = len(vs); lout = sum(o for o, _ in vs) / n
            corr = [b for o, b in vs if not o]
            if corr:
                cells.append((cfg, cls, lout, sum(corr) / len(corr), len(corr)))
    x = [c[2] for c in cells]; y = [c[3] for c in cells]
    r = pearson(x, y); rho = spearman(x, y)
    unexpl = None
    if r is not None:
        unexpl = 1 - r * r
    # across configurations, classes pooled (weighted by units)
    cfgs = defaultdict(lambda: [0, 0, 0, 0])
    complete = {c[0] for c in cells}
    for cfg, recs in sorted(data.items()):
        if cfg not in complete:
            continue
        for (cls, _, _), (o, b) in unit_losses(recs).items():
            cfgs[cfg][0] += 1; cfgs[cfg][1] += o
            if not o:
                cfgs[cfg][2] += 1; cfgs[cfg][3] += b
    xc = [v[1] / v[0] for v in cfgs.values() if v[2]]; yc = [v[3] / v[2] for v in cfgs.values() if v[2]]
    rc = pearson(xc, yc); rhoc = spearman(xc, yc)
    return {"cells": cells, "r": r, "rho": rho, "unexplained": unexpl, "n_cells": len(cells),
            "r_cfg": rc, "rho_cfg": rhoc, "unexplained_cfg": (1 - rc * rc) if rc is not None else None, "n_cfg": len(xc)}


def cv2(data):
    """Two-way ANOVA decomposition (configuration x class, unbalanced, sequential sums of squares) of the unit-level
    basis loss. Reported as shares of the total sum of squares."""
    rows = []
    for cfg, recs in sorted(data.items()):
        ul = unit_losses(recs)
        if len({cls for cls, _, _ in ul}) < 3:
            continue
        for (cls, _, _), (o, b) in ul.items():
            rows.append((cfg, cls, b))
    if not rows:
        return None
    y = np.array([r[2] for r in rows], float)
    cfgs = sorted({r[0] for r in rows}); clss = sorted({r[1] for r in rows})
    gm = y.mean(); sst = float(((y - gm) ** 2).sum())
    cfg_mean = {c: np.mean([r[2] for r in rows if r[0] == c]) for c in cfgs}
    cls_mean = {c: np.mean([r[2] for r in rows if r[1] == c]) for c in clss}
    cell_mean = {}
    for c1 in cfgs:
        for c2 in clss:
            v = [r[2] for r in rows if r[0] == c1 and r[1] == c2]
            if v:
                cell_mean[(c1, c2)] = np.mean(v)
    ss_cfg = float(sum((cfg_mean[r[0]] - gm) ** 2 for r in rows))
    ss_cls = float(sum((cls_mean[r[1]] - gm) ** 2 for r in rows))
    ss_cell = float(sum((cell_mean[(r[0], r[1])] - gm) ** 2 for r in rows))
    ss_int = max(0.0, ss_cell - ss_cfg - ss_cls)
    ss_res = float(sum((r[2] - cell_mean[(r[0], r[1])]) ** 2 for r in rows))
    return {"n": len(rows), "cfg": ss_cfg / sst, "cls": ss_cls / sst, "int": ss_int / sst, "res": ss_res / sst,
            "n_cfg": len(cfgs)}


def seed_component(recs):
    """Haiku: share of the variance of the unit-level basis loss that lies between runs of the same base episode."""
    ul = unit_losses(recs)
    by = defaultdict(list)
    for (cls, base, run), (_, b) in ul.items():
        by[(cls, base)].append(b)
    multi = {k: v for k, v in by.items() if len(v) > 1}
    if not multi:
        return None
    y = np.array([b for v in multi.values() for b in v], float)
    sst = float(((y - y.mean()) ** 2).sum())
    ss_within = float(sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in multi.values()))
    return {"episodes": len(multi), "units": len(y), "within_share": (ss_within / sst) if sst else None,
            "disagree_share": sum(1 for v in multi.values() if len(set(v)) > 1) / len(multi)}


def certified_sets(data):
    """Grants per rule with the shifted outcome error of the granted classes, pooled over configurations."""
    tot = {"DSA": [0, 0, 0], "track record": [0, 0, 0]}
    per = []
    for cfg, recs in sorted(data.items()):
        cal = A.class_measures(recs, "calibration"); sh = A.shifted_error(recs)
        if len(cal) < 3 or not sh:
            continue
        g = {"DSA": A.certify(cal, "k_wt"), "track record": A.certify(cal, "k_out")}
        line = {"cfg": cfg}
        for rule in tot:
            cs = sorted(c for c in cal if g[rule][c]["grant"] and c in sh)
            e = sum(sh[c][0] for c in cs); n = sum(sh[c][1] for c in cs)
            tot[rule][0] += len(cs); tot[rule][1] += e; tot[rule][2] += n
            line[rule] = (cs, e, n)
        per.append(line)
    return tot, per


def h3_no_c6(data):
    """DSA vs track record at k = 1 with c6 removed from both rules' rankings."""
    cells = [0, 0, 0]; rows = []
    for cfg, recs in sorted(data.items()):
        cal = {c: m for c, m in A.class_measures(recs, "calibration").items() if c != "c6"}
        sh = A.shifted_error(recs)
        if len(cal) < 2 or not sh:
            continue
        for row in A.h3_rows(cfg, cal, sh):
            d = row["rules"]["DSA"]; t = row["rules"]["track record"]
            if d["err"] is None or t["err"] is None or sorted(map(sorted, d["selections"])) == sorted(map(sorted, t["selections"])):
                continue
            cells[0 if d["err"] < t["err"] - 1e-12 else 1 if d["err"] > t["err"] + 1e-12 else 2] += 1
            rows.append((cfg, d["classes"], d["err"], t["classes"], t["err"]))
    return cells, rows


def keyed(data, key):
    if key == "reviewed":
        return {k: [dict(r, astar=sorted(K.review_astar(K.episode_of(r)))) for r in v] for k, v in data.items()}
    return data


def fmt(x, d=2):
    return "–" if x is None else f"{x:.{d}f}"


def main():
    full = A.load("runs/pilot")
    core = {k: [r for r in v if A.in_core(r)] for k, v in full.items()}
    haiku = next(k for k in full if "haiku" in k)
    lines = ["# Construct validity (CV1, CV2) and two exploratory tables",
             "",
             "Generated by `paper/pilot/construct_validity.py`. CV1 and CV2 are the pre-registered secondary hypotheses "
             "(preregistration §6); the certified-set tally and the H3 comparison without c6 are exploratory (asked for by the "
             "reviews of 2026-10-29). Calibration units as in the results files (A8: units missing any arm are dropped). "
             "Three keys: registered A\\*, contested arms excluded (A1), reviewed key (A13). Deficit agents excluded.",
             ""]
    for key in ("registered", "A1", "reviewed"):
        A.SENSITIVITY["on"] = key == "A1"
        for name, data in (("common core", core), ("all data", full)):
            d = keyed(data, key)
            c1 = cv1(d); c2 = cv2(d); cs, per = certified_sets(d); nc6, rows = h3_no_c6(d)
            lines.append(f"## Key: {key}; {name}")
            lines.append("")
            lines.append(f"**CV1.** Across {c1['n_cells']} (configuration, class) cells: Pearson r(ℓ_out, ℓ_basis | correct) = {fmt(c1['r'])}, "
                         f"Spearman ρ = {fmt(c1['rho'])}; share of the variance of ℓ_basis | correct not explained by ℓ_out: {fmt(c1['unexplained'])}. "
                         f"Across {c1['n_cfg']} configurations (classes pooled): r = {fmt(c1['r_cfg'])}, ρ = {fmt(c1['rho_cfg'])}, unexplained {fmt(c1['unexplained_cfg'])}.")
            lines.append("")
            lines.append("| configuration | class | ℓ_out | ℓ_basis among correct outcomes | n correct |")
            lines.append("|---|---|---|---|---|")
            for cfg, cls, lo, lb, n in c1["cells"]:
                lines.append(f"| {cfg} | {cls} | {100*lo:.1f}% | {100*lb:.1f}% | {n} |")
            lines.append("")
            if c2:
                lines.append(f"**CV2.** Unit-level basis loss, {c2['n']} calibration units, {c2['n_cfg']} configurations: share of the total sum of squares "
                             f"between configurations {100*c2['cfg']:.1f}%, between classes {100*c2['cls']:.1f}%, configuration × class {100*c2['int']:.1f}%, "
                             f"within cells {100*c2['res']:.1f}%.")
            if name == "all data":
                sc = seed_component(d[haiku])
                if sc:
                    lines.append(f"Seed (run) component, Claude Haiku 5.5 only ({sc['episodes']} base episodes × runs, {sc['units']} units): "
                                 f"{100*sc['within_share']:.1f}% of the variance of the basis loss lies between runs of the same episode; "
                                 f"runs disagree on the basis loss in {100*sc['disagree_share']:.1f}% of episodes.")
            lines.append("")
            lines.append(f"**Certified sets.** DSA: {cs['DSA'][0]} class grants, shifted outcome error {cs['DSA'][1]}/{cs['DSA'][2]}"
                         f"{' (' + format(100*cs['DSA'][1]/cs['DSA'][2], '.1f') + '%)' if cs['DSA'][2] else ''}; "
                         f"track record: {cs['track record'][0]} grants, {cs['track record'][1]}/{cs['track record'][2]}"
                         f"{' (' + format(100*cs['track record'][1]/cs['track record'][2], '.1f') + '%)' if cs['track record'][2] else ''}.")
            lines.append("")
            lines.append("| configuration | DSA grants (shifted errors / n) | track-record grants (shifted errors / n) |")
            lines.append("|---|---|---|")
            for ln in per:
                a, b = ln["DSA"], ln["track record"]
                lines.append(f"| {ln['cfg']} | {', '.join(a[0]) or '–'} ({a[1]}/{a[2]}) | {', '.join(b[0]) or '–'} ({b[1]}/{b[2]}) |")
            lines.append("")
            lines.append(f"**H3 without c6** (c3 and c5 only, k = 1): cells where the rules differ: {sum(nc6)}; DSA lower in {nc6[0]}, higher in {nc6[1]}, equal {nc6[2]}.")
            for cfg, dc, de, tc, te in rows:
                lines.append(f"- {cfg}: DSA {dc} → {100*de:.1f}%, track record {tc} → {100*te:.1f}%")
            lines.append("")
    A.SENSITIVITY["on"] = False
    OUT.write_text("\n".join(lines) + "\n")
    print(OUT)


if __name__ == "__main__":
    main()
