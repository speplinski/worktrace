from worktrace import world
from worktrace.classes import GENERATORS
from worktrace.deficits import DeficitAgent
from worktrace.interventions import ARMS_FULL, variants
from worktrace.oracles import normative


def test_oracle_deficit_agent_is_always_admissible():
    a = DeficitAgent("oracle")
    for cls in ("c3", "c5", "c6"):
        for i in range(20):
            for v in variants(GENERATORS[cls](100_000 + i), ARMS_FULL):
                assert a.decide(v) in normative(v)[0]


def test_copies_count_restores_authority_table():
    before = {k: a.controller for k, a in world.AUTHORITIES.items()}
    a = DeficitAgent("copies_count")
    for i in range(10):
        a.decide(GENERATORS["c3"](100_000 + i))
    assert {k: a.controller for k, a in world.AUTHORITIES.items()} == before


def test_memorised_replays_calibration_only():
    a = DeficitAgent("memorised")
    e = GENERATORS["c5"](200_001)          # held-out seed: falls back to the prior
    assert a.decide(e) == "reopen_cdd"
