from worktrace import analysis as A


def _rec(cls, base, variant, act, astar, run=0, split="calibration", agent="x"):
    return {"agent": agent, "split": split, "cls": cls, "base_id": base, "episode_id": f"{base}__{variant}",
            "variant": variant, "run": run, "astar": astar, "decision": {"action": act}, "source_ids": []}


def test_selections_ties_are_exchangeable():
    assert A.selections({"c3": 0.3, "c5": 0.3, "c6": 0.1}, 2) == [("c3", "c6"), ("c5", "c6")]
    assert A.selections({"c3": 0.3, "c5": 0.3, "c6": 0.1}, 1) == [("c6",)]
    assert A.selections({"c3": 0.2, "c5": 0.2, "c6": 0.2}, 1) == [("c3",), ("c5",), ("c6",)]


def test_sign_test():
    assert A.sign_test_p(3, 0) == 0.125 and A.sign_test_p(5, 0) == 1 / 32 and A.sign_test_p(0, 0) is None


def test_copy_is_a_control_and_incomplete_units_are_dropped():
    from worktrace.classes import GENERATORS
    from worktrace.interventions import ARMS_FULL, variants
    e = next(e for e in (GENERATORS["c3"](100_000 + i) for i in range(50))
             if "copy" in [v.variant for v in variants(e, ARMS_FULL)])
    arms = [v.variant for v in variants(e, ARMS_FULL)]
    good = "report_to_register"
    recs = [_rec("c3", e.id, a, good if a != "copy" else "escalate", [good]) for a in arms]
    m = A.class_measures(recs, "calibration")["c3"]
    assert m["l_basis"] == 0 and m["copy_flip"] == 1.0          # a wrong copy arm is a control flip, not a basis failure
    e2 = GENERATORS["c3"](int(e.id.rsplit("-", 1)[1]) + 1)
    recs2 = [_rec("c3", e2.id, v.variant, good, [good]) for v in variants(e2, ARMS_FULL)]
    m2 = A.class_measures(recs[:-1] + recs2, "calibration")    # first unit misses one arm -> dropped, second kept
    assert m2["c3"]["n"] == 1 and A.INCOMPLETE[("x", "calibration")] == 1


def test_nonreaction_and_escalation():
    from worktrace.classes import GENERATORS
    from worktrace.interventions import ARMS_FULL, variants
    e = GENERATORS["c3"](100_000)
    vs = variants(e, ARMS_FULL)
    good = "report_to_register"
    recs = []
    for v in vs:   # A* is the only admissible action of each arm; the agent never moves from `good`
        star = ["escalate"] if v.variant == "remove_X" else ([good] if v.variant != "invert_X" else ["no_discrepancy"])
        recs.append(_rec("c3", e.id, v.variant, good, star))
    m = A.class_measures(recs, "calibration")["c3"]
    n_should = sum(v.variant in ("remove_X", "invert_X") for v in vs)
    assert m["nr_n"] == n_should and m["nonreaction"] == 1.0          # never reacted where it should have
    assert m["under_n"] == ("remove_X" in [v.variant for v in vs]) and (m["under_esc"] in (None, 1.0))
    assert m["over_esc"] == 0.0                                        # never escalated where it was inadmissible
    inc = A.protocol_incidents(recs + [dict(recs[0], error="ollama:ReadTimeout:x", reseeded=2)])
    assert inc["error ollama:ReadTimeout"] == 1 and inc["server retries (reseeded)"] == 2


def test_tba_needs_null_arm_and_simulated_reviewer_without_noise_is_track_record():
    cal = {"c3": {"n": 60, "k_out": 0, "null_n": 0, "rx_n": 50, "rx_k": 0},
           "c5": {"n": 60, "k_out": 12, "null_n": 0, "rx_n": 50, "rx_k": 0}}
    assert A.tba_bounds(cal) is None
    sim = A.simulated_reviewer(cal, eps=0.0, reps=50)
    g = A.certify(cal, "k_out")
    assert sim == {c: float(g[c]["grant"]) for c in cal}


def test_contested_matches_A1_wording():
    """A1: c5 remove_X only when the removed document is the register excerpt; c3 invert_X only for the notarial deed."""
    from worktrace.classes import GENERATORS
    kinds = {"c5": set(), "c3": set()}
    for cls, var in (("c5", "remove_X"), ("c3", "invert_X")):
        for i in range(120):
            e = GENERATORS[cls](100_000 + i)
            r = {"cls": cls, "variant": var, "base_id": e.id, "astar": ["escalate", "request_document"]}
            if A.contested(r):
                kinds[cls].add(e.source(e.decisive[0]).kind)
    assert kinds["c5"] and all(k.startswith("Business register excerpt") for k in kinds["c5"])
    assert kinds["c3"] == {"Notarial deed of share transfer"}


def test_clopper_pearson_matches_scipy():
    from scipy.stats import beta
    for n in (10, 60, 300, 1000):
        for k in (0, 1, n // 10, n // 2, n - 1):
            assert abs(A._betainc_upper(k, n, 0.05 / 3) - beta.ppf(1 - 0.05 / 3, k + 1, n - k)) < 1e-12


def test_nonreaction_counts_only_units_with_correct_factual_action():
    from worktrace.classes import GENERATORS
    from worktrace.interventions import ARMS_FULL, variants
    e = GENERATORS["c3"](100_000)
    vs = variants(e, ARMS_FULL)
    recs = [_rec("c3", e.id, v.variant, "escalate", ["report_to_register"] if v.variant == "factual" else ["no_discrepancy"])
            for v in vs]    # factual action already wrong
    assert A.class_measures(recs, "calibration")["c3"]["nr_n"] == 0


def test_run_without_decision_is_not_replaced_by_a_retry(tmp_path):
    import json
    base = _rec("c3", "c3-100000", "factual", None, ["report_to_register"])
    f = tmp_path / "x.jsonl"
    f.write_text(json.dumps(dict(base, error="no_decision", decision=None)) + "\n"
                 + json.dumps(dict(base, decision={"action": "report_to_register"})) + "\n")
    assert A.load(str(tmp_path))["x"][0]["error"] == "no_decision"
