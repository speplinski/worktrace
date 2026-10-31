"""Multiverse over the logged readings of the policy (exploratory). Every combination of:
  independence (R1/R2(b)): shown | not shown          -> exception (b) applies | report only
  annual accounts (R3):     not a change | change | both admissible
  missing excerpt (R3/R5):  request | optional (no_action) | evidence (request or escalate) | both (optional+evidence) | both (optional+request)
  contested deed inversion (A1 c3 invert_X, {escalate, request_document}): oracle | also report_to_register
= 2 x 3 x 5 x 2 = 60 answer keys. For each: H3 DSA vs track record (cells lower:higher:equal, sign-test p, GLMM beta and one-sided p),
DSA vs the two judge rules and B-TBA, theta, and what each rule certified with the shifted error in those classes.
Common core and all data. Writes multiverse.json and multiverse.md next to this file.
"""
import itertools, json, re, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, ".")
import numpy as np
from worktrace import analysis as A, glmm
from worktrace import answer_key as K
from worktrace.oracles import oracle_a
from worktrace.world import AUTHORITIES

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
A.JUDGE.update(A.load_judgments("runs/judge"))

def key_for(e, indep, annual, excerpt, deed):
    if e.cls == "c3":
        a = K.c3_answer(e, independence_shown=indep)
        if deed == "also report" and e.variant == "invert_X" and a == {"escalate", "request_document"}:
            kind = e.source(e.decisive[0]).kind if e.decisive else ""
            # A1 case: inverted notarial deed; identify via the base episode's decisive source kind
            if kind == "Notarial deed of share transfer" or _base_kind(e) == "Notarial deed of share transfer":
                a = a | {"report_to_register"}
        return a
    if e.cls == "c5":
        ann = {"not a change": [False], "change": [True], "both": [False, True]}[annual]
        mis = {"request": ["request"], "optional": ["optional"], "evidence": ["evidence"],
               "both (optional+evidence)": ["optional", "evidence"], "both (optional+request)": ["optional", "request"]}[excerpt]
        return {x for an in ann for m in mis for x in K.c5_answer(e, an, m)}
    return set(oracle_a(e))

_BK = {}
def _base_kind(e):
    b = e.base_id or e.id
    if b not in _BK:
        _BK[b] = A._decisive_kind(b)
    return _BK[b]

def act(r):
    d = r.get("decision"); return d.get("action") if isinstance(d, dict) else None

def h3(data):
    cells = {"track record": [0, 0, 0], "judged process": [0, 0, 0], "judged grounds": [0, 0, 0], "B-TBA": [0, 0, 0]}
    rows = []; grants = {"DSA": [0, 0, 0], "TR": [0, 0, 0]}; pooled = defaultdict(int)
    for cfg, recs in sorted(data.items()):
        cal = A.class_measures(recs, "calibration"); sh = A.shifted_error(recs)
        for c, v in cal.items():
            if v["j_n"]:
                for kk, n in v["cells"].items():
                    pooled[kk] += n
        if not cal or not sh or len(cal) < 3:
            continue
        for rule, key in (("DSA", "k_wt"), ("TR", "k_out")):
            g = A.certify(cal, key)
            for c in cal:
                if g[c]["grant"] and c in sh:
                    grants[rule][0] += 1; grants[rule][1] += sh[c][0]; grants[rule][2] += sh[c][1]
        for row in A.h3_rows(cfg, cal, sh):
            d = row["rules"]["DSA"]
            for base in cells:
                t = row["rules"].get(base)
                if not t or t["err"] is None or d["err"] is None or sorted(map(sorted, d["selections"])) == sorted(map(sorted, t["selections"])):
                    continue
                cells[base][0 if d["err"] < t["err"] - 1e-12 else 1 if d["err"] > t["err"] + 1e-12 else 2] += 1
            for rule in ("DSA", "track record"):
                sels = row["rules"][rule]["selections"]
                for sel in sels:
                    for c in sel:
                        e, n = sh.get(c, (0, 0)); rows.append((cfg, row["k"], rule, e, n, 1 / len(sels)))
    X, y, w, g = [], [], [], []
    for cfg, k, rule, e, n, wt in rows:
        for yy, cnt in ((1.0, e), (0.0, n - e)):
            if cnt:
                X.append([1.0, float(rule == "DSA"), float(k == 2)]); y.append(yy); w.append(wt * cnt); g.append(cfg)
    fit = glmm.fit(np.array(X), np.array(y), g, w=np.array(w), names=["intercept", "DSA", "k2"])
    f = pooled["ifail_jfail"] + pooled["ifail_jpass"]; p = pooled["ipass_jfail"] + pooled["ipass_jpass"]
    return {"cells": cells, "beta": fit["coef"]["DSA"]["est"], "se": fit["coef"]["DSA"]["se"], "p": fit["coef"]["DSA"]["p_lower"],
            "converged": fit["converged"], "sign_p": A.sign_test_p(cells["track record"][0], cells["track record"][1]),
            "grants": grants, "theta": pooled["ifail_jpass"] / f if f else None, "theta_n": f,
            "flag": pooled["ipass_jfail"] / p if p else None}

full = A.load("runs/pilot")
core = {k: [r for r in v if A.in_core(r)] for k, v in full.items()}
READINGS = list(itertools.product(["shown", "not shown"], ["not a change", "change", "both"],
                                  ["request", "optional", "evidence", "both (optional+evidence)", "both (optional+request)"],
                                  ["oracle", "also report"]))
def write_md(results, path):
    """Render the table the paper cites (paper/pilot/multiverse/multiverse.md) from the computed rows."""
    def cells(c, rule):
        x = c["cells"].get(rule); return f"{x[0]}:{x[1]}:{x[2]}" if x else "–"
    L = ["# H3 under every combination of the logged policy readings (exploratory)", "",
         "60 answer keys = independence (2) × annual accounts (3) × missing excerpt (5) × contested deed inversion (2). For each: DSA vs track "
         "record at matched coverage (cells where DSA has the lower : higher : equal shifted error), mixed-model β_DSA with one-sided p (H3 as "
         "registered), DSA vs the two judge-based rules and B-TBA (lower:higher:equal), θ (share of wrong-basis decisions the judge passes), and "
         "what each rule certified with the shifted errors in those classes. Common core and all data. Generated by `multiverse.py` from "
         "`runs/pilot` (final data, 14 configurations).", "",
         "| # | independence | annual accounts | missing excerpt | deed inversion | core: TR cells | core β (p) | core judged proc. | core judged grounds | core B-TBA | core θ | core DSA grants (err) | core TR grants (err) | all: TR cells | all β (p) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(results, 1):
        c, a = r["core"], r["all"]
        g = c["grants"]
        L.append(f"| {i} | {r['independence']} | {r['annual_accounts']} | {r['missing_excerpt']} | {r['deed_inversion']} | {cells(c, 'track record')} | "
                 f"{c['beta']:+.2f} ({c['p']:.3f}) | {cells(c, 'judged process')} | {cells(c, 'judged grounds')} | {cells(c, 'B-TBA')} | {100*c['theta']:.0f}% | "
                 f"{g['DSA'][0]} ({g['DSA'][1]}/{g['DSA'][2]}) | {g['TR'][0]} ({g['TR'][1]}/{g['TR'][2]}) | {cells(a, 'track record')} | {a['beta']:+.2f} ({a['p']:.3f}) |")
    L += ["", "Row 1 is the oracles' key (registered analysis). Row 27 (independence = shown, annual = both, excerpt = both (optional+evidence), deed = oracle) "
          "is the author's reviewed key after the withdrawal of the E02 verdict (A13, addendum of 2026-10-30). Row 3 (shown, not a change, optional, oracle) "
          "is the key closest to the legal texts (ambiguity log, legal check). Independence = not shown, annual = change, excerpt = optional, deed = oracle "
          "is the key built from the author's blind answers alone.", ""]
    path.write_text("\n".join(L))


if len(sys.argv) > 1 and sys.argv[1] == "--render":
    write_md(json.loads((Path(__file__).resolve().parent / "multiverse.json").read_text()), Path(__file__).resolve().parent / "multiverse.md")
    raise SystemExit(0)

results = []
for i, (indep, annual, excerpt, deed) in enumerate(READINGS):
    row = {"independence": indep, "annual_accounts": annual, "missing_excerpt": excerpt, "deed_inversion": deed}
    for name, data in (("core", core), ("all", full)):
        keyed = {k: [dict(r, astar=sorted(key_for(K.episode_of(r), indep == "shown", annual, excerpt, deed))) for r in v] for k, v in data.items()}
        row[name] = h3(keyed)
    results.append(row)
    c = row["core"]["cells"]["track record"]
    print(f"{i+1:2d}/60 indep={indep:9s} annual={annual:12s} excerpt={excerpt:24s} deed={deed:11s} | core {c[0]}:{c[1]}:{c[2]} beta={row['core']['beta']:+.2f} p={row['core']['p']:.2f} | all beta={row['all']['beta']:+.2f} p={row['all']['p']:.2f}", flush=True)
(OUT / "multiverse.json").write_text(json.dumps(results, indent=1))
write_md(results, OUT / "multiverse.md")
