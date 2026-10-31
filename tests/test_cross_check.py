"""Cross-check on the real pilot data: an independent reference implementation (adapted from the independent code
audit, A12) recomputes the core quantities from the raw records without calling worktrace.analysis, and compares.

Covers: loading with the §7 rule, completeness of units, the common core (A4), l_out and l_WT with and without the
contested arms of A1, shifted outcome errors, certification grants (scipy Clopper-Pearson, Bonferroni over 3 classes)
and the H3 cell counts DSA vs track record with exchangeable ties (A7), exact fractions.
"""
import json
import re
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import pytest
from scipy.stats import beta

from worktrace import analysis as A
from worktrace.classes import GENERATORS
from worktrace.interventions import ARMS_FULL, variants

RUNS = Path(__file__).resolve().parents[1] / "runs" / "pilot"
INTERV = {"remove_X", "only_X", "invert_X", "add_Y", "add_Y_remove_X"}
ALPHA, DELTA, NCLS = 0.10, 0.05, 3

pytestmark = pytest.mark.skipif(not RUNS.exists(), reason="pilot data not present")


def ref_load():
    d = defaultdict(dict)
    for f in sorted(RUNS.glob("*.jsonl")):
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            key = (r["split"], r["episode_id"], r["run"])
            prev = d[r["agent"]].get(key)
            if prev is not None and prev.get("error") in ("no_decision", "max_turns"):
                continue          # §7: a run without a decision stays an error
            d[r["agent"]][key] = r
    return {a: list(v.values()) for a, v in d.items()}


def act(r):
    d = r.get("decision")
    return d.get("action") if isinstance(d, dict) else None


def in_core(r):
    base = {"calibration": 100000, "heldout": 200000, "shifted": 300000}[r["split"]]
    lim = {"calibration": 60, "heldout": 30, "shifted": 60}[r["split"]]
    return r["run"] == 0 and int(r["base_id"].rsplit("-", 1)[1]) - base < lim


_EP = {}


def episode(base_id):
    if base_id not in _EP:
        m = re.fullmatch(r"(c\d)(s?)-(\d+)", base_id)
        _EP[base_id] = GENERATORS[m.group(1)](int(m.group(3)), shift=bool(m.group(2)))
    return _EP[base_id]


def ref_contested(r):
    """A1 as worded: c5 remove_X of the register excerpt; c3 invert_X of the notarial deed with A* {escalate, request_document}."""
    e = episode(r["base_id"])
    kind = e.source(e.decisive[0]).kind
    if r["cls"] == "c5" and r["variant"] == "remove_X":
        return kind.startswith("Business register excerpt")
    if r["cls"] == "c3" and r["variant"] == "invert_X":
        return kind == "Notarial deed of share transfer" and sorted(r["astar"]) == ["escalate", "request_document"]
    return False


def ref_cal(recs, sens):
    g = defaultdict(dict)
    for r in recs:
        if r["split"] == "calibration":
            g[(r["cls"], r["base_id"], r["run"])][r["variant"]] = r
    arms = {r["variant"] for r in recs if r["split"] == "calibration"}
    out = defaultdict(lambda: [0, 0, 0])      # n, k_out, k_wt
    for (c, b, run), vs in g.items():
        exp = {v.variant for v in variants(episode(b), [a for a in ARMS_FULL if a in arms])}
        if set(vs) != exp:
            continue
        lout = act(vs["factual"]) not in vs["factual"]["astar"]
        lb = any(act(v) not in v["astar"] for n, v in vs.items() if n in INTERV and not (sens and ref_contested(v)))
        o = out[c]
        o[0] += 1
        o[1] += lout
        o[2] += lout or lb
    return dict(out)


def ref_shifted(recs):
    out = defaultdict(lambda: [0, 0])
    for r in recs:
        if r["split"] == "shifted" and r["variant"] == "factual":
            out[r["cls"]][0] += act(r) not in r["astar"]
            out[r["cls"]][1] += 1
    return dict(out)


def ub(k, n):
    return 1.0 if n == 0 or k >= n else float(beta.ppf(1 - DELTA / NCLS, k + 1, n - k))


def ref_selections(scores, k):
    cl = sorted(scores)
    return sorted(s for s in combinations(cl, k)
                  if not [c for c in cl if c not in s] or max(scores[c] for c in s) <= min(scores[c] for c in cl if c not in s))


@pytest.fixture(scope="module")
def data():
    return ref_load(), A.load(str(RUNS))


@pytest.mark.parametrize("core", [False, True])
@pytest.mark.parametrize("sens", [False, True])
def test_reference_matches_analysis(data, core, sens):
    ref_all, ana_all = data
    assert set(ref_all) == set(ana_all)
    A.SENSITIVITY["on"] = sens
    h3 = [0, 0, 0]       # DSA lower, higher, equal among cells where the selections differ
    h3_ana = [0, 0, 0]
    try:
        for cfg in sorted(ref_all):
            ref = [r for r in ref_all[cfg] if in_core(r)] if core else ref_all[cfg]
            ana = [r for r in ana_all[cfg] if A.in_core(r)] if core else ana_all[cfg]
            rc, ac = ref_cal(ref, sens), A.class_measures(ana, "calibration")
            assert set(rc) == set(ac), cfg
            for c in rc:
                assert tuple(rc[c]) == (ac[c]["n"], ac[c]["k_out"], ac[c]["k_wt"]), (cfg, c)
                ga, go = A.certify(ac, "k_wt"), A.certify(ac, "k_out")
                assert ga[c]["grant"] == (ub(rc[c][2], rc[c][0]) <= ALPHA), (cfg, c, "DSA grant")
                assert go[c]["grant"] == (ub(rc[c][1], rc[c][0]) <= ALPHA), (cfg, c, "track-record grant")
            rs, as_ = ref_shifted(ref), A.shifted_error(ana)
            assert {c: tuple(v) for c, v in rs.items()} == as_, cfg
            if not rs or not rc:
                continue
            sc = {"DSA": {c: ub(v[2], v[0]) for c, v in rc.items()}, "TR": {c: ub(v[1], v[0]) for c, v in rc.items()}}
            for k in range(1, len(rc)):
                sel = {r: ref_selections(s, k) for r, s in sc.items()}
                err = {r: sum(Fraction(sum(rs[c][0] for c in x), sum(rs[c][1] for c in x)) for x in sel[r]) / len(sel[r])
                       for r in sel}
                if sel["DSA"] != sel["TR"]:
                    h3[0 if err["DSA"] < err["TR"] else 1 if err["DSA"] > err["TR"] else 2] += 1
            for row in A.h3_rows(cfg, ac, as_):
                d, t = row["rules"]["DSA"], row["rules"]["track record"]
                if sorted(d["selections"]) != sorted(t["selections"]):
                    h3_ana[0 if d["err"] < t["err"] - 1e-12 else 1 if d["err"] > t["err"] + 1e-12 else 2] += 1
    finally:
        A.SENSITIVITY["on"] = False
    assert h3 == h3_ana


def ref_tba(recs, sens):
    """Reference B-TBA (A11.3): null-arm flips and remove_X failures per class, bounds at delta / (2 * 3), score = max."""
    g = defaultdict(dict)
    for r in recs:
        if r["split"] == "calibration":
            g[(r["cls"], r["base_id"], r["run"])][r["variant"]] = r
    arms = {r["variant"] for r in recs if r["split"] == "calibration"}
    cnt = defaultdict(lambda: [0, 0, 0, 0])     # null n, null flips, remove_X n, remove_X failures
    for (c, b, run), vs in g.items():
        if set(vs) != {v.variant for v in variants(episode(b), [a for a in ARMS_FULL if a in arms])}:
            continue
        fa = act(vs["factual"])
        if "null" in vs and not (sens and ref_contested(vs["null"])):
            cnt[c][0] += 1
            cnt[c][1] += act(vs["null"]) != fa
        if "remove_X" in vs and not (sens and ref_contested(vs["remove_X"])):
            cnt[c][2] += 1
            cnt[c][3] += act(vs["remove_X"]) not in vs["remove_X"]["astar"]
    if not cnt or any(v[0] == 0 or v[2] == 0 for v in cnt.values()):
        return None
    d = DELTA / (2 * NCLS)
    b = lambda k, n: 1.0 if k >= n else float(beta.ppf(1 - d, k + 1, n - k))
    return {c: max(b(v[1], v[0]), b(v[3], v[2])) for c, v in cnt.items()}


@pytest.mark.parametrize("sens", [False, True])
def test_btba_and_report_summary_match_reference(data, sens):
    ref_all, ana_all = data
    A.SENSITIVITY["on"] = sens
    try:
        for cfg in sorted(ref_all):
            ref = [r for r in ref_all[cfg] if in_core(r)]
            ana = [r for r in ana_all[cfg] if A.in_core(r)]
            ac = A.class_measures(ana, "calibration")
            rt, at = ref_tba(ref, sens), A.tba_bounds(ac)
            assert (rt is None) == (at is None), cfg
            if rt:
                assert {c: round(v, 9) for c, v in rt.items()} == {c: round(max(v), 9) for c, v in at.items()}, cfg
                assert {c: round(v, 9) for c, v in rt.items()} == {c: round(v, 9) for c, v in A.rule_scores(ac)["B-TBA"].items()}, cfg
        # the H3 summary line printed by report() must agree with an independent count over the same cells
        core = {k: [r for r in v if A.in_core(r)] for k, v in ana_all.items()}
        rep = A.report(core)
        line = next(l for l in rep.splitlines() if l.startswith("- DSA vs track record:"))
        got = tuple(int(x) for x in re.search(r"lower shifted error in (\d+), higher in (\d+), equal (\d+)", line).groups())
        lo = hi = eq = 0
        for cfg in sorted(ref_all):
            ref = [r for r in ref_all[cfg] if in_core(r)]
            rc, rs = ref_cal(ref, sens), ref_shifted(ref)
            if not rc or not rs:
                continue
            sc = {"DSA": {c: ub(v[2], v[0]) for c, v in rc.items()}, "TR": {c: ub(v[1], v[0]) for c, v in rc.items()}}
            for k in range(1, len(rc)):
                sel = {r: ref_selections(s, k) for r, s in sc.items()}
                if sel["DSA"] == sel["TR"]:
                    continue
                err = {r: sum(Fraction(sum(rs[c][0] for c in x), sum(rs[c][1] for c in x)) for x in sel[r]) / len(sel[r])
                       for r in sel}
                lo += err["DSA"] < err["TR"]; hi += err["DSA"] > err["TR"]; eq += err["DSA"] == err["TR"]
        assert got == (lo, hi, eq)
    finally:
        A.SENSITIVITY["on"] = False
