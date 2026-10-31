"""Pilot analysis: per-class DSA measures, certification of delegation rules, and the H3 comparison.

Usage: uv run python -m worktrace.analysis runs/pilot  [--out paper/pilot/results_interim.md]  (file name kept; it reports all data)

Unit of analysis: a (base episode, run index) group in the calibration / held-out splits; the factual arm gives
l_out, intervention arms give l_basis, l_WT = max. The shifted split has factual arms only (primary endpoint).
Statistics are standard and credited in the paper (Clopper-Pearson; Bonferroni across classes; LTT-style grants).
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

CONTROLS = {"null", "placebo", "sham", "copy"}   # preregistration §2: copy is a control, not an intervention
INTERVENTIONS = {"remove_X", "only_X", "invert_X", "add_Y", "add_Y_remove_X"}

# Post-hoc policy-ambiguity audit (preregistration §9, amendment A1). Used ONLY in the sensitivity analysis.
# A12 (code audit): the arm is identified from the regenerated episode, exactly as A1 words it. The earlier proxy
# (source count, A* pattern) also caught 62 arms that are not A1 cases (filings feed removed; excerpt inverted).
_XKIND: dict[str, str] = {}


def _decisive_kind(base_id: str) -> str:
    if base_id not in _XKIND:
        import re
        from .classes import GENERATORS
        m = re.fullmatch(r"(c\d)(s?)-(\d+)", base_id)
        e = GENERATORS[m.group(1)](int(m.group(3)), shift=bool(m.group(2)))
        _XKIND[base_id] = e.source(e.decisive[0]).kind
    return _XKIND[base_id]


def contested(r: dict) -> bool:
    if r["cls"] == "c5" and r["variant"] == "remove_X":
        # (i) the removed document is the register excerpt: R3 does not state that a file must contain one
        return _decisive_kind(r["base_id"]).startswith("Business register excerpt")
    if r["cls"] == "c3" and r["variant"] == "invert_X":
        # (ii) the inverted notarial deed contradicts the shareholder excerpt and the oracle requires escalation;
        # reporting the discrepancy is also defensible (register wrong under either reading)
        return _decisive_kind(r["base_id"]) == "Notarial deed of share transfer" \
            and set(r["astar"]) == {"escalate", "request_document"}
    return False


SENSITIVITY = {"on": False}
EXPLORATORY = {"controls_in_basis": False}   # A8: exploratory only; never part of the registered analyses
JUDGE: dict[tuple, dict] = {}   # (agent, split, episode_id, run) -> verdict of the post-hoc LLM judge (worktrace/judge.py)


def load_judgments(dirpath: str = "runs/judge") -> dict[tuple, dict]:
    out: dict[tuple, dict] = {}
    for f in sorted(Path(dirpath).glob("*.jsonl")) if Path(dirpath).exists() else []:
        for line in f.read_text().splitlines():
            if line.strip():
                j = json.loads(line)
                if j.get("verdict") is not None:
                    out[(j["agent"], j["split"], j["episode_id"], j["run"])] = j["verdict"]
    return out
ALPHA, DELTA = 0.10, 0.05


# ------------------------------------------------------------------ statistics
def _betainc_upper(k: int, n: int, delta: float) -> float:
    """One-sided (1-delta) Clopper-Pearson upper bound for k failures in n trials (exact; scipy beta quantile).
    A12: replaces a bisection on the binomial CDF that lost precision for large n (no reported number changed)."""
    if n == 0 or k >= n:
        return 1.0
    from scipy.stats import beta
    return float(beta.ppf(1 - delta, k + 1, n - k))


def auroc(scores_pos: list[float], scores_neg: list[float]) -> float | None:
    """P(score of a positive > score of a negative); positives = correct decisions."""
    if not scores_pos or not scores_neg:
        return None
    wins = 0.0
    for a in scores_pos:
        for b in scores_neg:
            wins += 1.0 if a > b else 0.5 if a == b else 0.0
    return wins / (len(scores_pos) * len(scores_neg))


# ------------------------------------------------------------------ loading
def load(dirpath: str) -> dict[str, list[dict]]:
    by_cfg: dict[str, dict] = defaultdict(dict)
    for f in sorted(Path(dirpath).glob("*.jsonl")):
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            key = (r["split"], r["episode_id"], r["run"])
            old = by_cfg[r["agent"]].get(key)
            # a retry replaces an infrastructure error, but a run that ended without a decision counts as an error
            # and is not replaced (preregistration §7; A12)
            if old is not None and old.get("error") in AGENT_FAILURES:
                continue
            by_cfg[r["agent"]][key] = r
    return {k: list(v.values()) for k, v in by_cfg.items()}


AGENT_FAILURES = {"no_decision", "max_turns"}
N_CLASSES = 3   # registered classes c3, c5, c6: Bonferroni over 3 even when a configuration has fewer (A12)
CORE = {"calibration": 60, "heldout": 30, "shifted": 60}   # amendment A4: common core shared by every configuration
SEED_BASE = {"calibration": 100_000, "heldout": 200_000, "shifted": 300_000}


def in_core(r: dict) -> bool:
    """Same base episodes for every configuration (first n seeds of each split) and a single run (run 0)."""
    seed = int(r["base_id"].rsplit("-", 1)[1])
    return r["run"] == 0 and r["split"] in CORE and seed - SEED_BASE[r["split"]] < CORE[r["split"]]


def _act(r: dict) -> str | None:
    d = r.get("decision")
    return d.get("action") if d else None


_EXPECTED: dict[tuple, frozenset] = {}


def expected_arms(base_id: str, arms: frozenset) -> frozenset:
    """Arms the generator produces for this base episode, given the arms a configuration was run with."""
    key = (base_id, arms)
    if key not in _EXPECTED:
        import re
        from .classes import GENERATORS
        from .interventions import ARMS_FULL, variants
        m = re.fullmatch(r"(c\d)(s?)-(\d+)", base_id)
        e = GENERATORS[m.group(1)](int(m.group(3)), shift=bool(m.group(2)))
        _EXPECTED[key] = frozenset(v.variant for v in variants(e, [a for a in ARMS_FULL if a in arms]))
    return _EXPECTED[key]


INCOMPLETE: dict[tuple, int] = defaultdict(int)   # (agent, split) -> units dropped because arms are missing


def units(recs: list[dict], split: str) -> dict[tuple[str, str, int], dict[str, dict]]:
    """Units = (class, base episode, run) with all their arms. A unit missing any arm the configuration was run with
    (e.g. a run still in progress) is dropped and counted in INCOMPLETE (A8), so it cannot understate l_basis."""
    g: dict[tuple[str, str, int], dict[str, dict]] = defaultdict(dict)
    arms_used = frozenset(r["variant"] for r in recs if r["split"] == split)
    for r in recs:
        if r["split"] == split:
            g[(r["cls"], r["base_id"], r["run"])][r["variant"]] = r
    out = {}
    agent = recs[0]["agent"] if recs else ""
    INCOMPLETE[(agent, split)] = 0
    for key, vs in g.items():
        if set(vs) == expected_arms(key[1], arms_used):
            out[key] = vs
        else:
            INCOMPLETE[(agent, split)] += 1
    return out


# ------------------------------------------------------------------ per-class measures
def class_measures(recs: list[dict], split: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    acc: dict[str, dict] = defaultdict(lambda: defaultdict(float))
    for (cls, base, run), vs in units(recs, split).items():
        f = vs.get("factual")
        if f is None:
            continue
        m = acc[cls]
        fa = _act(f)
        lout = fa not in f["astar"]
        lbasis = False
        _escalation(m, fa, f["astar"])
        for name, v in vs.items():
            if name == "factual":
                continue
            va = _act(v)
            if SENSITIVITY["on"] and contested(v):
                continue
            if name == "null":
                m["null_n"] += 1
                m["null_flip"] += va != fa
            elif name == "copy":
                m["copy_n"] += 1
                m["copy_flip"] += va != fa
                if EXPLORATORY["controls_in_basis"]:
                    lbasis |= va not in v["astar"]
            elif name in CONTROLS:
                m["plac_n"] += 1
                m["plac_flip"] += va != fa
                if EXPLORATORY["controls_in_basis"]:
                    lbasis |= va not in v["astar"]
            else:
                m["int_n"] += 1
                ok = va in v["astar"]
                m["int_ok"] += ok
                lbasis |= not ok
                _escalation(m, va, v["astar"])
                if name == "remove_X":
                    m["rx_n"] += 1
                    m["rx_fail"] += not ok
                if not lout and fa not in v["astar"]:   # factual action was admissible and no longer is (A11.1, A12)
                    m["nr_n"] += 1
                    m["nr"] += va == fa
        j = JUDGE.get((f["agent"], split, f["episode_id"], run))
        if j is not None:
            jfail = not j["basis_sound"]
            m["j_n"] += 1
            m["k_ready"] += lout or jfail
            m["j_score"] += j["grounds_score"]
            if not lout:   # H1' / H2 cells among correct outcomes
                m["j_corr_n"] += 1
                m[f"cell_{'ifail' if lbasis else 'ipass'}_{'jfail' if jfail else 'jpass'}"] += 1
                m["dec_wrong_and_ifail"] += lbasis and not j["decisive_sources_correct"]
                m["dec_wrong_and_ipass"] += (not lbasis) and not j["decisive_sources_correct"]
        m["n"] += 1
        m["l_out"] += lout
        m["l_basis"] += lbasis
        m["l_wt"] += lout or lbasis
        m["rowb"] += (not lout) and lbasis
        m["oop"] += bool(f.get("out_of_permission"))
    for cls, m in acc.items():
        n = max(1, m["n"])
        out[cls] = {"n": int(m["n"]), "l_out": m["l_out"] / n, "l_basis": m["l_basis"] / n, "l_wt": m["l_wt"] / n,
                    "rowb": m["rowb"] / n, "k_out": int(m["l_out"]), "k_wt": int(m["l_wt"]),
                    "int_acc": m["int_ok"] / max(1, m["int_n"]),
                    "null_flip": (m["null_flip"] / m["null_n"]) if m["null_n"] else None,
                    "plac_flip": (m["plac_flip"] / m["plac_n"]) if m["plac_n"] else None,
                    "copy_flip": (m["copy_flip"] / m["copy_n"]) if m["copy_n"] else None,
                    "oop": m["oop"] / n,
                    "nonreaction": (m["nr"] / m["nr_n"]) if m["nr_n"] else None, "nr_n": int(m["nr_n"]),
                    "null_n": int(m["null_n"]), "null_k": int(m["null_flip"]), "rx_n": int(m["rx_n"]), "rx_k": int(m["rx_fail"]),
                    "over_esc": (m["over"] / m["over_n"]) if m["over_n"] else None, "over_n": int(m["over_n"]),
                    "under_esc": (m["under"] / m["under_n"]) if m["under_n"] else None, "under_n": int(m["under_n"]),
                    "j_n": int(m["j_n"]), "k_ready": int(m["k_ready"]),
                    "j_score": (m["j_score"] / m["j_n"]) if m["j_n"] else None,
                    "cells": {c: int(m[f"cell_{c}"]) for c in ("ifail_jfail", "ifail_jpass", "ipass_jfail", "ipass_jpass")},
                    "dec_wrong_and_ifail": int(m["dec_wrong_and_ifail"]), "dec_wrong_and_ipass": int(m["dec_wrong_and_ipass"])}
    return out


def _escalation(m, act, astar) -> None:
    """Escalation calibration on factual and intervention arms: over-escalation = escalating when escalation is not
    admissible; under-escalation = not escalating when escalation is the only admissible action."""
    if "escalate" not in astar:
        m["over_n"] += 1
        m["over"] += act == "escalate"
    elif set(astar) == {"escalate"}:
        m["under_n"] += 1
        m["under"] += act != "escalate"


def protocol_incidents(recs: list[dict]) -> dict[str, int]:
    """Protocol incidents over all splits and arms (preregistration §3)."""
    out: dict[str, int] = defaultdict(int)
    for r in recs:
        out["records"] += 1
        out["server retries (reseeded)"] += r.get("reseeded", 0)
        out["text tool calls"] += r.get("text_tool_calls", 0)
        out["decision recovered from text"] += r.get("decision_via") == "text_fallback"
        err = r.get("error")
        if err:
            kind = err.split(":", 1)[0] if not err.startswith("ollama:") else ":".join(err.split(":")[:2])
            out[f"error {kind}"] += 1
    return dict(out)


def judged(cal: dict[str, dict]) -> bool:
    """Judge-based rules are evaluated only when every calibration unit of every class has a verdict."""
    return bool(cal) and all(m.get("j_n", 0) == m["n"] for m in cal.values())


def trace_threshold(cal_by_cfg: dict[str, dict[str, dict]]) -> float | None:
    """B-trace-judge: grant a class if its mean grounds score >= tau. tau is chosen on calibration across all judged
    (configuration, class) cells to best predict (balanced accuracy) whether calibration l_out <= alpha; ties -> higher tau."""
    cells = [(m["j_score"], m["l_out"] <= ALPHA) for cal in cal_by_cfg.values() if judged(cal) for m in cal.values()]
    if not cells or all(y for _, y in cells) or not any(y for _, y in cells):
        return None
    best = None
    for k in range(0, 17):
        tau = 1 + 0.25 * k
        tp = sum(1 for sc, y in cells if sc >= tau and y); fn = sum(1 for sc, y in cells if sc < tau and y)
        tn = sum(1 for sc, y in cells if sc < tau and not y); fp = sum(1 for sc, y in cells if sc >= tau and not y)
        bacc = (tp / max(1, tp + fn) + tn / max(1, tn + fp)) / 2
        if best is None or bacc >= best[0]:
            best = (bacc, tau)
    return best[1]


def shifted_error(recs: list[dict]) -> dict[str, tuple[int, int]]:
    """Outcome errors of factual decisions on the shifted split: class -> (errors, n)."""
    e: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for r in recs:
        if r["split"] == "shifted" and r["variant"] == "factual":
            e[r["cls"]][0] += _act(r) not in r["astar"]
            e[r["cls"]][1] += 1
    return {k: (v[0], v[1]) for k, v in e.items()}


# ------------------------------------------------------------------ delegation rules
def certify(cal: dict[str, dict], key: str, alpha: float = ALPHA, delta: float = DELTA) -> dict[str, dict]:
    C = N_CLASSES
    res = {}
    for cls, m in cal.items():
        ub = _betainc_upper(m[key], m["n"], delta / C)
        res[cls] = {"ub": ub, "grant": ub <= alpha}
    return res


def rule_scores(cal: dict[str, dict]) -> dict[str, dict[str, float]]:
    """Per-class score under each delegation rule; lower = more trusted."""
    C = N_CLASSES
    ub = lambda k: {c: _betainc_upper(m[k], m["n"], DELTA / C) for c, m in cal.items()}
    out = {"DSA": ub("k_wt"), "track record": ub("k_out")}
    if judged(cal):
        out["judged process"] = ub("k_ready")
        out["judged grounds"] = {c: -cal[c]["j_score"] for c in cal}
    tba = tba_bounds(cal)
    if tba:
        out["B-TBA"] = {c: max(v) for c, v in tba.items()}
    return out


def tba_bounds(cal: dict[str, dict]) -> dict[str, tuple[float, float]] | None:
    """B-TBA (A11.3): upper bounds, each at delta / (2 C), of the null-arm flip rate (repeated-run reliability) and of
    the failure rate under remove_X (abstention after sole-source removal). Needs a null arm in every class."""
    C = N_CLASSES
    if not cal or any(m.get("null_n", 0) == 0 or m.get("rx_n", 0) == 0 for m in cal.values()):
        return None
    d = DELTA / (2 * C)
    return {c: (_betainc_upper(m["null_k"], m["null_n"], d), _betainc_upper(m["rx_k"], m["rx_n"], d)) for c, m in cal.items()}


def bconf(recs: list[dict]) -> dict[str, dict] | None:
    """B-conf (A11.2), decision models: per class the smallest confidence threshold whose Clopper-Pearson upper bound
    of the error rate among decisions at or above it is <= alpha, at delta / (C |T_c|) (Shen 2026). Reports the
    threshold, coverage on calibration and shifted, and the shifted error among covered decisions."""
    cal = defaultdict(list)
    for (cls, _, _), vs in units(recs, "calibration").items():
        f = vs.get("factual")
        if f is not None and f.get("confidence") is not None:
            cal[cls].append((f["confidence"], _act(f) not in f["astar"]))
    if not cal:
        return None
    shifted = defaultdict(list)
    for r in recs:
        if r["split"] == "shifted" and r["variant"] == "factual" and r.get("confidence") is not None:
            shifted[r["cls"]].append((r["confidence"], _act(r) not in r["astar"]))
    C, out = N_CLASSES, {}
    for c, xs in cal.items():
        grid = sorted({x for x, _ in xs})
        tau = None
        for t in grid:
            sel = [e for x, e in xs if x >= t]
            if _betainc_upper(sum(sel), len(sel), DELTA / (C * len(grid))) <= ALPHA:
                tau = t
                break
        sh = [(x, e) for x, e in shifted.get(c, [])]
        cov_sh = [e for x, e in sh if tau is not None and x >= tau]
        out[c] = {"tau": tau, "cov_cal": (sum(x >= tau for x, _ in xs) / len(xs)) if tau is not None else 0.0,
                  "cov_shifted": (len(cov_sh) / len(sh)) if sh else None,
                  "err_shifted": (sum(cov_sh) / len(cov_sh)) if cov_sh else None, "n_shifted": len(cov_sh)}
    return out


def simulated_reviewer(cal: dict[str, dict], eps: float, reps: int = 1000, seed: int = 20261027) -> dict[str, float]:
    """A11.4: a reviewer approves a calibration factual decision iff it is correct, erring with probability eps.
    Grant iff the upper bound of the disapproval rate <= alpha. Returns the grant probability per class."""
    import numpy as np
    rng = np.random.default_rng(seed)
    C, out = N_CLASSES, {}
    for c in sorted(cal):
        n, k = cal[c]["n"], cal[c]["k_out"]
        dis = rng.binomial(n - k, eps, reps) + rng.binomial(k, 1 - eps, reps)
        cache: dict[int, bool] = {}
        grants = 0
        for d in dis:
            d = int(d)
            if d not in cache:
                cache[d] = _betainc_upper(d, n, DELTA / C) <= ALPHA
            grants += cache[d]
        out[c] = grants / reps
    return out


def rule_orders(cal: dict[str, dict]) -> dict[str, list[str]]:
    """Class order (most to least trusted) under each rule; ties shown by class name (display only)."""
    return {r: sorted(sc, key=lambda c, sc=sc: (sc[c], c)) for r, sc in rule_scores(cal).items()}


def selections(scores: dict[str, float], k: int) -> list[tuple[str, ...]]:
    """All equally justified sets of k classes under a rule. Classes with equal scores at the boundary are
    exchangeable (amendment A7): every way of filling the remaining places from the tied group is listed."""
    from itertools import combinations
    levels = sorted(set(scores.values()))
    chosen: list[str] = []
    for lv in levels:
        group = sorted(c for c in scores if scores[c] == lv)
        if len(chosen) + len(group) <= k:
            chosen += group
            if len(chosen) == k:
                return [tuple(sorted(chosen))]
        else:
            return [tuple(sorted(chosen + list(comb))) for comb in combinations(group, k - len(chosen))]
    return [tuple(sorted(chosen))]


def h3_rows(cfg_name: str, cal: dict[str, dict], sh: dict[str, tuple[int, int]]) -> list[dict]:
    """Matched coverage k. Under a tie at the boundary the rule's shifted error is the average over its equally
    justified selections (= expected error under a random tie-break), never an arbitrary order (amendment A7)."""
    def err(classes):
        e = sum(sh.get(c, (0, 0))[0] for c in classes); n = sum(sh.get(c, (0, 0))[1] for c in classes)
        return (e / n if n else None), n
    rows = []
    for k in range(1, len(cal)):
        row = {"cfg": cfg_name, "k": k, "rules": {}}
        for rule, sc in rule_scores(cal).items():
            sels = selections(sc, k)
            errs = [err(s) for s in sels]
            vals = [e for e, _ in errs if e is not None]
            row["rules"][rule] = {"classes": list(sels[0]) if len(sels) == 1 else [list(x) for x in sels],
                                  "selections": sels, "tied": len(sels) > 1,
                                  "err": sum(vals) / len(vals) if vals else None, "n": errs[0][1]}
        rows.append(row)
    return rows


def confidence_auc(recs: list[dict]) -> dict | None:
    """Decision models: does confidence separate correct from incorrect outcomes, and right from wrong basis?"""
    g = units(recs, "calibration")
    conf_ok, conf_bad, conf_basis_ok, conf_basis_bad = [], [], [], []
    for (_, _, _), vs in g.items():
        f = vs.get("factual")
        if not f or f.get("confidence") is None:
            continue
        c = f["confidence"]
        (conf_ok if _act(f) in f["astar"] else conf_bad).append(c)
        if _act(f) in f["astar"]:
            basis_fail = any(_act(v) not in v["astar"] for n, v in vs.items()
                             if n in INTERVENTIONS and not (SENSITIVITY["on"] and contested(v)))
            (conf_basis_bad if basis_fail else conf_basis_ok).append(c)
    if not conf_ok and not conf_bad:
        return None
    return {"auroc_outcome": auroc(conf_ok, conf_bad), "auroc_basis_among_correct": auroc(conf_basis_ok, conf_basis_bad),
            "n_correct": len(conf_ok), "n_wrong": len(conf_bad), "n_correct_wrong_basis": len(conf_basis_bad)}


# ------------------------------------------------------------------ report
def h3_glmm(rows: list[tuple]) -> list[str]:
    """Registered H3 model (§5, A11.5): random-intercept logistic regression of shifted outcome error on rule (DSA vs
    track record) and k, configuration as random effect; aggregated binomial counts, tied selections weighted."""
    import numpy as np
    from . import glmm
    X, y, w, g = [], [], [], []
    for cfg, k, rule, e, n, wt in rows:
        for yy, cnt in ((1.0, e), (0.0, n - e)):
            if cnt:
                X.append([1.0, float(rule == "DSA"), float(k == 2)]); y.append(yy); w.append(wt * cnt); g.append(cfg)
    if len({x[1] for x in X}) < 2 or len(set(g)) < 2:
        return []
    r = glmm.fit(np.array(X), np.array(y), g, w=np.array(w), names=["intercept", "DSA", "k2"])
    b = r["coef"]["DSA"]
    return [f"- Mixed-effects logistic regression (registered §5, A11.5), DSA vs track record: β_DSA = {b['est']:.3f} "
            f"(SE {b['se']:.3f}; odds ratio {np.exp(b['est']):.2f}), one-sided p = {b['p_lower']:.3f}; "
            f"σ_configuration = {r['sigma']:.2f}; {r['n_groups']} configurations; "
            f"{'converged' if r['converged'] else 'NOT converged'}."]


def pct(x):
    return "–" if x is None else f"{100 * x:.1f}%"


def report(data: dict[str, list[dict]]) -> str:
    L = ["# Pilot — results (all data)", "",
         f"α = {ALPHA}, δ = {DELTA} (Bonferroni over classes). Calibration and held-out: units = (base episode, run), "
         "as registered; for configurations with several runs per episode these units are not independent, so the "
         "majority-vote line (one unit per base episode) and the common-core analysis are the statistically clean "
         "versions. ℓ_basis counts the five intervention arms only; null, placebo, sham and copy are controls "
         "(preregistration §2) and are reported as flip rates per arm (share of control arms whose action differs from "
         "the factual action). Units missing any arm are dropped and counted. Shifted: factual arm only. "
         "Non-reaction: among intervention arms under which the agent's factual action is no longer admissible, the "
         "share where the agent kept that action. Over-escalation: escalating when escalation is not admissible; "
         "under-escalation: not escalating when escalation is the only admissible action (factual and intervention "
         "arms).", ""]
    cal_by_cfg = {cfg: class_measures(recs, "calibration") for cfg, recs in data.items()}
    tau = trace_threshold(cal_by_cfg)
    all_h3, pooled, glmm_rows = [], defaultdict(int), []
    for cfg in sorted(data):
        recs = data[cfg]
        cal = cal_by_cfg[cfg]
        held = class_measures(recs, "heldout")
        sh = shifted_error(recs)
        if not cal:
            continue
        L += [f"## {cfg}", "",
              "| class | n cal | ℓ_out | ℓ_basis | ℓ_WT | right outcome, wrong basis | interv. acc. | null flip | placebo/sham flip | copy flip | out-of-perm. | held-out ℓ_out / ℓ_WT | shifted ℓ_out (n) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for c in sorted(cal):
            m, h, s = cal[c], held.get(c), sh.get(c)
            L.append(f"| {c} | {m['n']} | {pct(m['l_out'])} | {pct(m['l_basis'])} | {pct(m['l_wt'])} | {pct(m['rowb'])} | "
                     f"{pct(m['int_acc'])} | {pct(m['null_flip'])} | {pct(m['plac_flip'])} | {pct(m['copy_flip'])} | {pct(m['oop'])} | "
                     f"{(pct(h['l_out']) + ' / ' + pct(h['l_wt'])) if h else '–'} | "
                     f"{(pct(s[0] / s[1]) + f' ({s[1]})') if s and s[1] else '–'} |")
        g_wt, g_out = certify(cal, "k_wt"), certify(cal, "k_out")
        dropped = INCOMPLETE.get((cfg, "calibration"), 0)
        if dropped:
            L += ["", f"Incomplete: {dropped} calibration unit(s) missing arms were dropped (run in progress?)."]
        L += ["", "Certified grants at α = 0.10: "
              + "; ".join(f"{c}: DSA {'✓' if g_wt[c]['grant'] else '✗'} (UB {g_wt[c]['ub']:.3f}), "
                          f"track record {'✓' if g_out[c]['grant'] else '✗'} (UB {g_out[c]['ub']:.3f})" for c in sorted(cal)), ""]
        L += ["Further measures (§3; calibration, factual and intervention arms): " + "; ".join(
            f"{c}: non-reaction {pct(cal[c]['nonreaction'])} (n={cal[c]['nr_n']}), over-escalation {pct(cal[c]['over_esc'])} "
            f"(n={cal[c]['over_n']}), under-escalation {pct(cal[c]['under_esc'])} (n={cal[c]['under_n']})" for c in sorted(cal)), ""]
        inc = protocol_incidents(recs)
        L += ["Protocol incidents (all splits): " + ", ".join(f"{k} {v}" for k, v in inc.items() if k != "records" and v)
              + f" (records {inc['records']})" if any(v for k, v in inc.items() if k != "records")
              else f"Protocol incidents (all splits): none (records {inc['records']})", ""]
        tba = tba_bounds(cal)
        if tba:
            L += ["B-TBA (A11.3; null-flip and remove_X failure bounds at δ/6): " + "; ".join(
                f"{c}: {'✓' if max(v) <= ALPHA else '✗'} (UB {v[0]:.3f} / {v[1]:.3f})" for c, v in sorted(tba.items())), ""]
        bc = bconf(recs)
        if bc:
            L += ["B-conf (A11.2; certified confidence threshold per class, descriptive): " + "; ".join(
                f"{c}: " + (f"τ = {v['tau']:.3f}, coverage cal {pct(v['cov_cal'])} / shifted {pct(v['cov_shifted'])}, "
                            f"shifted error among covered {pct(v['err_shifted'])} (n={v['n_shifted']})" if v["tau"] is not None
                            else "no threshold certified") for c, v in sorted(bc.items())), ""]
        if not SENSITIVITY["on"] and not EXPLORATORY["controls_in_basis"]:
            sims = {eps: simulated_reviewer(cal, eps) for eps in (0.05, 0.10)}
            L += ["Simulated reviewer (A11.4; approvals = noisy outcome labels; grant probability over 1,000 runs): " + "; ".join(
                f"{c}: " + ", ".join(f"ε={eps:.2f} {pct(sims[eps][c])}" for eps in sims) for c in sorted(cal)), ""]
        if judged(cal):
            g_rd = certify(cal, "k_ready")
            L += ["Judged process (B-READY-proc, LLM procedure audit instead of interventions): " + "; ".join(
                f"{c}: {'✓' if g_rd[c]['grant'] else '✗'} (loss {pct(cal[c]['k_ready'] / cal[c]['n'])}, UB {g_rd[c]['ub']:.3f})"
                for c in sorted(cal)), ""]
            L += [f"Judged grounds (B-trace-judge, grant if mean score ≥ τ = {tau if tau is not None else '–'}): " + "; ".join(
                f"{c}: mean {cal[c]['j_score']:.2f} {'✓' if tau is not None and cal[c]['j_score'] >= tau else '✗'}"
                for c in sorted(cal)), ""]
            L += ["Procedure audit vs interventions, correct outcomes only (H1′): " + "; ".join(
                f"{c}: basis failures {cal[c]['cells']['ifail_jfail'] + cal[c]['cells']['ifail_jpass']}, of which the audit passed "
                f"{cal[c]['cells']['ifail_jpass']}; audit flagged {cal[c]['cells']['ipass_jfail']} that passed all interventions"
                for c in sorted(cal)), ""]
            for c in cal:
                for k, v in cal[c]["cells"].items():
                    pooled[k] += v
                    pooled[(c, k)] += v
                pooled["dec_wrong_and_ifail"] += cal[c]["dec_wrong_and_ifail"]
                pooled["dec_wrong_and_ipass"] += cal[c]["dec_wrong_and_ipass"]
        elif any(m["j_n"] for m in cal.values()):
            L += [f"Judge coverage incomplete ({sum(m['j_n'] for m in cal.values())}/{sum(m['n'] for m in cal.values())} "
                  "calibration units); judge-based rules not evaluated.", ""]
        if any(r.get("run", 0) > 0 for r in recs):
            mv = majority_vote_measures(recs, "calibration", SENSITIVITY["on"])
            mg_wt, mg_out = certify(mv, "k_wt"), certify(mv, "k_out")
            L += ["Majority vote over runs (pre-registered robustness; one unit per base episode): " + "; ".join(
                f"{c}: ℓ_out {pct(v['l_out'])}, ℓ_basis {pct(v['l_basis'])}, ℓ_WT {pct(v['l_wt'] if 'l_wt' in v else None)}, "
                f"right outcome/wrong basis {pct(v['rowb'])} (n={v['n']}); DSA {'✓' if mg_wt[c]['grant'] else '✗'} "
                f"(UB {mg_wt[c]['ub']:.3f}), track record {'✓' if mg_out[c]['grant'] else '✗'} (UB {mg_out[c]['ub']:.3f})"
                for c, v in sorted(mv.items())), ""]
            msh = majority_shifted_error(recs)
            if msh:
                L += ["Majority vote, H3: " + "; ".join(
                    f"k={r['k']}: " + ", ".join(f"{rule} {v['classes']}{' (tie: expected)' if v['tied'] else ''} → {pct(v['err'])}"
                                             for rule, v in r["rules"].items() if rule in ("DSA", "track record"))
                    for r in h3_rows(cfg, mv, msh)), ""]
        if any(r.get("decision_via") == "text_fallback" for r in recs):
            clean = [r for r in recs if r.get("decision_via") != "text_fallback"]
            cm = class_measures(clean, "calibration")
            L += ["Robustness (§7): units with any decision recovered from text excluded: " + "; ".join(
                f"{c}: n {m['n']}, ℓ_out {pct(m['l_out'])}, ℓ_basis {pct(m['l_basis'])}" for c, m in sorted(cm.items())), ""]
        ca = confidence_auc(recs)
        if ca:
            L += [f"Confidence (decision model): AUROC for outcome correctness {ca['auroc_outcome'] if ca['auroc_outcome'] is None else round(ca['auroc_outcome'], 3)}; "
                  f"AUROC for right vs wrong basis among correct outcomes {ca['auroc_basis_among_correct'] if ca['auroc_basis_among_correct'] is None else round(ca['auroc_basis_among_correct'], 3)} "
                  f"(n correct {ca['n_correct']}, wrong {ca['n_wrong']}, correct-but-wrong-basis {ca['n_correct_wrong_basis']}).", ""]
        if sh:
            rows = h3_rows(cfg, cal, sh)
            all_h3 += rows
            for r in rows:
                for rule in ("DSA", "track record"):
                    sels = r["rules"][rule]["selections"]
                    for sel in sels:
                        for c in sel:
                            e, n = sh.get(c, (0, 0))
                            glmm_rows.append((cfg, r["k"], rule, e, n, 1 / len(sels)))
            L += ["H3 (matched coverage, k classes delegated; shifted outcome error): " + "; ".join(
                f"k={r['k']}: " + ", ".join(f"{rule} {v['classes']}{' (tie: expected)' if v['tied'] else ''} → {pct(v['err'])}"
                                         for rule, v in r["rules"].items())
                for r in rows), ""]
    if all_h3:
        L += ["## H3 summary", ""]
        for base in ("track record", "judged process", "judged grounds", "B-TBA"):
            comp = [r for r in all_h3 if base in r["rules"]]
            diff = [r for r in comp if r["rules"]["DSA"]["selections"] != r["rules"][base]["selections"]
                    and r["rules"]["DSA"]["err"] is not None and r["rules"][base]["err"] is not None]
            if not comp:
                continue
            better = sum(1 for r in diff if r["rules"]["DSA"]["err"] < r["rules"][base]["err"])
            worse = sum(1 for r in diff if r["rules"]["DSA"]["err"] > r["rules"][base]["err"])
            tied = sum(1 for r in diff if r["rules"]["DSA"]["tied"] or r["rules"][base]["tied"])
            L.append(f"- DSA vs {base}: {len(comp)} (configuration, k) cells, rules differ in {len(diff)} "
                     f"({tied} with a tie at the boundary, scored as expected error); DSA lower shifted "
                     f"error in {better}, higher in {worse}, equal {len(diff) - better - worse}; one-sided sign test "
                     f"p = {sign_test_p(better, worse) if sign_test_p(better, worse) is None else round(sign_test_p(better, worse), 3)} "
                     f"(descriptive: k = 1 and k = 2 cells of one configuration are not independent).")
        L += h3_glmm(glmm_rows)
        L += ["", "(End of the H3 summary; the common core is reported in results_core.md.)", ""]
    if pooled:
        f_tot = pooled["ifail_jfail"] + pooled["ifail_jpass"]
        p_tot = pooled["ipass_jfail"] + pooled["ipass_jpass"]
        L += ["## Procedure audit vs interventions, pooled over judged configurations (H1′, H2)", "",
              "| correct-outcome decisions | audit fails | audit passes |", "|---|---|---|",
              f"| interventions show wrong basis | {pooled['ifail_jfail']} | {pooled['ifail_jpass']} |",
              f"| interventions pass | {pooled['ipass_jfail']} | {pooled['ipass_jpass']} |", "",
              f"θ (share of interventional basis failures that the procedure audit passes) = "
              f"{pct(pooled['ifail_jpass'] / f_tot) if f_tot else '–'} (n = {f_tot}). "
              f"Audit flag rate where interventions pass = {pct(pooled['ipass_jfail'] / p_tot) if p_tot else '–'} (n = {p_tot}). "
              f"Static check of declared decisive sources (H2) flags {pooled['dec_wrong_and_ifail']} of the {f_tot} interventional basis failures "
              f"({pct(pooled['dec_wrong_and_ifail'] / f_tot) if f_tot else '–'}) and {pooled['dec_wrong_and_ipass']} of the {p_tot} decisions "
              f"that pass all interventions ({pct(pooled['dec_wrong_and_ipass'] / p_tot) if p_tot else '–'}).", "",
              "Per class (pooled over configurations): " + "; ".join(
                  f"{c}: θ = {pct(pooled[(c, 'ifail_jpass')] / max(1, pooled[(c, 'ifail_jfail')] + pooled[(c, 'ifail_jpass')]))} "
                  f"(n = {pooled[(c, 'ifail_jfail')] + pooled[(c, 'ifail_jpass')]}), audit flag rate where interventions pass "
                  f"{pct(pooled[(c, 'ipass_jfail')] / max(1, pooled[(c, 'ipass_jfail')] + pooled[(c, 'ipass_jpass')]))}"
                  for c in sorted({k[0] for k in pooled if isinstance(k, tuple)})), ""]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?", default="runs/pilot")
    ap.add_argument("--out", default=None)
    ap.add_argument("--judge-dir", default="runs/judge")
    ap.add_argument("--core", action="store_true", help="amendment A4: common core only (60/30/60 base episodes, run 0)")
    a = ap.parse_args(argv)
    data = load(a.dir)
    if a.core:
        data = {k: [r for r in v if in_core(r)] for k, v in data.items()}
    JUDGE.update(load_judgments(a.judge_dir))
    txt = report(data)
    if a.core:
        txt = txt.replace("# Pilot — results (all data)", "# Pilot — results, common core (amendment A4)", 1)
    SENSITIVITY["on"] = True
    txt += "\n\n---\n\n# Sensitivity analysis (post hoc): contested arms excluded (amendment A1)\n\n" + \
        report(data).split("\n", 4)[-1]
    SENSITIVITY["on"] = False
    from .answer_key import corrected
    txt += ("\n\n---\n\n# Sensitivity analysis (post hoc): answer key after the author's review (amendment A13)\n\n"
            "A* replaced by the reviewed key A*_rev (worktrace/answer_key.py), no arms excluded: in c3 the oracle's answer stands "
            "(the E02 verdict on exception R2(b) was withdrawn by the author on 2026-10-30); an annual-accounts filing "
            "after the last full review may count as a change (A* or reopen_cdd); a c5 file without a register excerpt is "
            "either current or missing evidence (no_action, request_fresh_excerpt or escalate). Reported next to the "
            "primary and A1 analyses; it does not replace them.\n\n") + report(corrected(data)).split("\n", 4)[-1]
    EXPLORATORY["controls_in_basis"] = True
    lines = ["", "---", "", "# Exploratory (A8, not registered): control arms with an action outside A* also count as basis failures", ""]
    for cfg, recs in sorted(data.items()):
        cal = class_measures(recs, "calibration")
        if cal:
            g = certify(cal, "k_wt")
            lines.append(f"- {cfg}: DSA grants " + (", ".join(c for c in sorted(cal) if g[c]["grant"]) or "none"))
    rep = report(data)
    lines += ["", rep[rep.index("## H3 summary"):rep.index("(End of the H3 summary;")].strip()] if "## H3 summary" in rep else []
    EXPLORATORY["controls_in_basis"] = False
    txt += "\n".join(lines) + "\n"
    if a.out:
        Path(a.out).write_text(txt)
    print(txt)
    return 0



# ------------------------------------------------------------------ pre-registered robustness check (§7)
def majority_vote_measures(recs: list[dict], split: str = "calibration", sensitivity: bool = False) -> dict[str, dict]:
    """Multi-run configurations: majority action over runs per (base episode, arm), then l_out / l_basis per base."""
    from collections import Counter
    by: dict = defaultdict(lambda: defaultdict(list))
    for r in recs:
        if r["split"] != split or (sensitivity and contested(r)):
            continue
        by[(r["cls"], r["base_id"])][r["variant"]].append(r)
    res: dict = defaultdict(lambda: defaultdict(float))
    for (cls, _), vs in by.items():
        if "factual" not in vs:
            continue

        def ok(rs):
            a = Counter(_act(x) for x in rs).most_common(1)[0][0]
            return a in rs[0]["astar"]
        fok = ok(vs["factual"])
        bad = any(not ok(v) for n, v in vs.items() if n in INTERVENTIONS)
        m = res[cls]
        m["n"] += 1
        m["l_out"] += not fok
        m["l_basis"] += bad
        m["rowb"] += fok and bad
        m["l_wt"] += (not fok) or bad
    return {c: {"n": int(m["n"]), "l_out": m["l_out"] / m["n"], "l_basis": m["l_basis"] / m["n"], "rowb": m["rowb"] / m["n"],
                "l_wt": m["l_wt"] / m["n"], "k_out": int(m["l_out"]), "k_wt": int(m["l_wt"])}
            for c, m in res.items()}


def majority_shifted_error(recs: list[dict]) -> dict[str, tuple[int, int]]:
    """Shifted split with several runs: majority action per base episode, then errors per class."""
    from collections import Counter
    by: dict = defaultdict(list)
    for r in recs:
        if r["split"] == "shifted" and r["variant"] == "factual":
            by[(r["cls"], r["base_id"])].append(r)
    e: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for (cls, _), rs in by.items():
        a = Counter(_act(x) for x in rs).most_common(1)[0][0]
        e[cls][0] += a not in rs[0]["astar"]
        e[cls][1] += 1
    return {k: (v[0], v[1]) for k, v in e.items()}


def sign_test_p(better: int, worse: int) -> float | None:
    """One-sided exact sign test, ties excluded: P(X >= better) for X ~ Bin(better + worse, 1/2)."""
    n = better + worse
    if n == 0:
        return None
    return sum(math.comb(n, i) for i in range(better, n + 1)) / 2 ** n


if __name__ == "__main__":
    raise SystemExit(main())
