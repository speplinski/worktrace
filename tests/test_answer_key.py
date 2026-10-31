"""Reviewed answer key (A13, as revised on 2026-10-30): with the corrections off it is the oracle; with them on it gives
the author's verdicts on the reviewed cases and changes only what the verdicts cover."""
import json
from pathlib import Path

import pytest

from worktrace import answer_key as K
from worktrace.classes import GENERATORS
from worktrace.interventions import ARMS_FULL, variants
from worktrace.oracles import normative, oracle_a

ROOT = Path(__file__).resolve().parents[1]
ITEMS = json.loads((ROOT / "paper" / "pilot" / "expert_review" / "items.json").read_text())
RUNS = ROOT / "runs" / "pilot"


def _episodes(n=60):
    for cls in ("c3", "c5"):
        for base, shift in ((100_000, False), (200_000, False), (300_000, True)):
            for i in range(n):
                yield from variants(GENERATORS[cls](base + i, shift=shift), ARMS_FULL)


def test_corrections_off_reproduce_the_oracle():
    for e in _episodes():
        off = K.c3_answer(e) if e.cls == "c3" else K.c5_answer(e)
        assert off == oracle_a(e), e.id


def _item(code):
    it = ITEMS[int(code[1:]) - 1]
    base, _, variant = it["id"].partition("__")
    e = K.episode_of({"base_id": base, "variant": variant or "factual"})
    assert e.id == it["id"]
    return e, it


def test_reviewed_cases_give_the_authors_verdicts():
    want = {"E03": {"reopen_cdd", "no_action"},
            "E22": {"no_action", "request_fresh_excerpt", "escalate"},
            "E23": {"no_action", "request_fresh_excerpt", "escalate"}}
    for code, astar in want.items():
        e, it = _item(code)
        assert set(it["astar"]) != astar, code          # the disputed cases differ from the oracle
        assert K.review_astar(e) == astar, code


def test_cases_judged_right_keep_the_oracle_answer():
    for code in ("E01", "E02", "E04", "E05", "E10", "E11", "E12", "E28"):   # E02: verdict withdrawn 2026-10-30
        e, it = _item(code)
        assert K.review_astar(e) == set(it["astar"]) == set(normative(e)[0]), code


def test_only_the_reviewed_rules_change_the_key():
    for e in _episodes(40):
        old, new = oracle_a(e), K.review_astar(e)
        if old == new:
            continue
        # only c5 changes (both readings admissible: a strict superset of the oracle's answer); c3 keeps the oracle
        assert e.cls == "c5" and new > old, e.id


@pytest.mark.skipif(not RUNS.exists(), reason="pilot data not present")
def test_changed_variants_in_the_common_core():
    from worktrace import analysis as A
    data = A.load(str(RUNS))
    changed = {}
    for recs in data.values():
        for r in recs:
            if A.in_core(r) and K.review_astar(K.episode_of(r)) != set(r["astar"]):
                changed[(r["split"], r["episode_id"])] = r["cls"]
    assert len(changed) == 44
    assert sum(c == "c3" for c in changed.values()) == 0
    assert sum(c == "c5" for c in changed.values()) == 44
