"""Scripted agents with planted deficits for the known-groups validity test (paper/pilot/known_groups.md).

Deterministic, no model. Spec for make_agent: deficit:<kind>, kind in oracle | memorised | always_escalate |
copies_count | order_cue. Run single-threaded (copies_count patches the authority table while it decides).
"""
from __future__ import annotations

import contextlib
import copy
import dataclasses
import re
from typing import Any

from . import world
from .classes import GENERATORS
from .oracles import normative
from .world import Episode

PRIOR = {"c3": "report_to_register", "c5": "reopen_cdd", "c6": "escalate"}
CALIBRATION_SEEDS = range(100_000, 200_000)


def _answer(e: Episode) -> str:
    return sorted(normative(e)[0])[0]


@contextlib.contextmanager
def _everyone_independent():
    """Every issuer answers to its own authority (no shared control)."""
    saved = dict(world.AUTHORITIES)
    try:
        for k, a in saved.items():
            world.AUTHORITIES[k] = dataclasses.replace(a, controller=f"OWN_{k}")
        yield
    finally:
        world.AUTHORITIES.clear()
        world.AUTHORITIES.update(saved)


class DeficitAgent:
    KINDS = ("oracle", "memorised", "always_escalate", "copies_count", "order_cue")

    def __init__(self, kind: str):
        if kind not in self.KINDS:
            raise ValueError(f"unknown deficit {kind}")
        self.kind, self.name = kind, f"deficit:{kind}"

    def decide(self, e: Episode) -> str:
        if self.kind == "oracle":
            return _answer(e)
        if self.kind == "always_escalate":
            return "escalate"
        if self.kind == "memorised":
            m = re.fullmatch(r"(c\d)(s?)-(\d+)", e.base_id or e.id)
            seed = int(m.group(3))
            if seed in CALIBRATION_SEEDS:   # seen during calibration: replay the stored factual answer
                return _answer(GENERATORS[m.group(1)](seed, shift=bool(m.group(2))))
            return PRIOR[e.cls]
        if self.kind == "copies_count":
            v = copy.deepcopy(e)
            for s in v.sources:
                s.copy_of = None
            with _everyone_independent():
                return _answer(v)
        if self.kind == "order_cue":
            return _answer(e) if ord(e.sources[0].id[-1]) % 2 == 0 else PRIOR[e.cls]
        raise AssertionError

    def run(self, e: Episode) -> dict[str, Any]:
        act = self.decide(e)
        grounds = list(e.decisive)
        return {"retrieved": [s.id for s in e.sources], "turns": 0, "usage": [], "error": None, "stop": "scripted",
                "out_of_permission": act not in e.allowed_actions, "seconds": 0.0,
                "decision": {"action": act, "declared_grounds": grounds, "decisive_sources": grounds, "explanation": ""}}
