"""Synthetic world for the E1 counterparty-verification environment.

Everything here is fictional: names are generated from syllables, authorities are invented,
and no real register, list or institution is represented. See paper/pilot/e1_spec.md.
"""
from __future__ import annotations

import copy
import datetime as dt
import random
from dataclasses import dataclass, field, asdict
from typing import Any

SYL = ["ka", "lo", "mir", "ven", "sta", "dor", "eli", "tor", "ran", "bel", "vi", "sor", "mun", "da", "rel", "kas",
       "lin", "por", "ze", "ul", "fen", "gra", "hol", "nar", "pe", "quil", "ros", "tam", "vor", "wen"]
LEGAL_FORMS = ["Ltd", "S.A.", "GmbH", "B.V.", "S.r.l."]
COUNTRIES = ["Aurelia", "Borovia", "Calderra"]  # fictional jurisdictions


def _word(rng: random.Random, n: int = 2) -> str:
    return "".join(rng.choice(SYL) for _ in range(n)).capitalize()


def person_name(rng: random.Random) -> str:
    return f"{_word(rng, 2)} {_word(rng, 3)}"


def company_name(rng: random.Random) -> str:
    return f"{_word(rng, 2)}{_word(rng, 2).lower()} {rng.choice(LEGAL_FORMS)}"


@dataclass(frozen=True)
class Authority:
    id: str
    name: str
    kind: str          # government_register | notary | court | customer | data_vendor | bank_internal
    tier: int          # 1 = government-issued, 2 = regulated professional, 3 = customer-linked / unverified
    controller: str    # controlling authority id; sources are independent iff controllers differ


AUTHORITIES: dict[str, Authority] = {a.id: a for a in [
    Authority("A_BR", "Aurelia Business Register", "government_register", 1, "GOV_AURELIA"),
    Authority("A_CBR", "Aurelia Central Beneficial-Ownership Register", "government_register", 1, "GOV_AURELIA"),
    Authority("A_NOT", "Notarial Chamber of Calderra (notary deed)", "notary", 2, "NOTARIAL_CHAMBER"),
    Authority("A_CRT", "Borovia Commercial Court", "court", 1, "JUDICIARY_BOROVIA"),
    Authority("A_CUS", "Customer (self-declaration)", "customer", 3, "CUSTOMER"),
    Authority("A_VEN", "Corporate data vendor (aggregates register data)", "data_vendor", 2, "GOV_AURELIA"),
    Authority("A_INT", "Our institution (internal records)", "bank_internal", 1, "INTERNAL"),
]}


@dataclass
class Source:
    id: str
    authority: str              # Authority.id
    kind: str                   # document type label shown to the agent
    issue_date: str             # ISO date
    content: dict[str, Any]
    copy_of: str | None = None  # id of the source this one reproduces (not independent of it)
    role: str = "evidence"      # evidence | register | record | irrelevant (hidden from the agent)

    def card(self) -> dict[str, Any]:
        a = AUTHORITIES[self.authority]
        return {"id": self.id, "type": self.kind, "issued_by": a.name, "issue_date": self.issue_date}

    def full(self) -> dict[str, Any]:
        d = self.card()
        d["content"] = self.content
        if self.copy_of:
            d["note"] = "Reproduction of another document supplied through the issuer named above."
        return d


@dataclass
class Episode:
    id: str
    cls: str                      # decision class id: c3 | c5 | c6
    seed: int
    decision_date: str
    task: str
    allowed_actions: list[str]    # P: actions permitted in this episode (the human-set ceiling)
    all_actions: list[str]        # full action enum offered to the agent (incl. out-of-permission ones)
    sources: list[Source]
    facts: dict[str, Any]         # hidden world facts used by the oracles (never shown to the agent)
    variant: str = "factual"      # factual | remove_X | only_X | invert_X | add_Y | add_Y_remove_X | placebo | sham | copy | null
    base_id: str | None = None
    decisive: list[str] = field(default_factory=list)   # ids of decisive sources in the factual episode

    def clone(self, variant: str) -> "Episode":
        e = copy.deepcopy(self)
        e.variant = variant
        e.base_id = self.id if self.base_id is None else self.base_id
        e.id = f"{e.base_id}__{variant}"
        return e

    def source(self, sid: str) -> Source | None:
        return next((s for s in self.sources if s.id == sid), None)

    def to_json(self) -> dict[str, Any]:
        d = asdict(self)
        return d


def iso(d: dt.date) -> str:
    return d.isoformat()


def parse(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def independent(a: Source, b: Source) -> bool:
    """Two sources are independent iff their issuers share no controlling authority and neither copies the other."""
    if a.copy_of == b.id or b.copy_of == a.id or (a.copy_of and a.copy_of == b.copy_of):
        return False
    return AUTHORITIES[a.authority].controller != AUTHORITIES[b.authority].controller
