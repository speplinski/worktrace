from collections import Counter

from worktrace.classes import GENERATORS
from worktrace.interventions import ARMS_FULL, variants
from worktrace.oracles import normative


def test_oracles_agree_and_variants_change_answers():
    disagree, astar, changed = Counter(), Counter(), Counter()
    for cls, gen in GENERATORS.items():
        for seed in range(1500):
            e = gen(seed)
            base, ok = normative(e)
            assert ok, (e.id, "factual")
            astar[(cls, tuple(sorted(base)))] += 1
            for v in variants(e, ARMS_FULL[1:]):
                a, ok = normative(v)
                if not ok:
                    disagree[(cls, v.variant)] += 1
                if a != base:
                    changed[(cls, v.variant)] += 1
    print("A* distribution:", dict(astar))
    print("variant changed A*:", dict(changed))
    assert not disagree, dict(disagree)


def test_controls_never_change_answer():
    for cls, gen in GENERATORS.items():
        for seed in range(500):
            e = gen(seed)
            base, _ = normative(e)
            for v in variants(e, ["null", "placebo", "sham"]):
                assert normative(v)[0] == base, (e.id, v.variant)


def test_shifted_split_oracles_agree():
    for cls, gen in GENERATORS.items():
        for seed in range(800):
            e = gen(seed, shift=True)
            assert normative(e)[1], e.id
            for v in variants(e, ARMS_FULL[1:]):
                assert normative(v)[1], (v.id, v.variant)
