"""Answer key after the author's review of the oracle (amendment A13). Sensitivity analysis only: the registered key
is A* from worktrace.oracles.

Each verdict (paper/pilot/expert_review/answers_author.json) is carried over to every episode governed by the same
rule. "Both readings defensible" means the union of the readings.

- Source independence (E02). The verdict of 2026-10-29 (oracle wrong: exception R2(b) cannot be established because the
  documents never show controlling authorities, so report_to_register only) was withdrawn by the author on 2026-10-30
  after his blind answer to E14, a case of the same structure, in the oracles' sense. The reviewed key therefore keeps
  the oracle's answer in c3; c3_answer(independence_shown=False) remains available for the multiverse.
- "Change" in R3 (E03, both defensible). An "Annual accounts filed" entry after the last full review may count as a
  change: the oracle's answer or reopen_cdd.
- Missing register excerpt in c5 (E22, E23, both defensible). In a file that is otherwise current, either a missing
  excerpt is not missing evidence (no_action), or it is, and R5 admits request_fresh_excerpt and escalate.

Everything else keeps the oracle's answer. With every correction off, c3_answer and c5_answer reproduce oracle A.
"""
from __future__ import annotations

import re

from .classes import GENERATORS
from .interventions import OPERATORS
from .oracles import _a_norm, _a_reliable_owner_statements, _a_risk, _d, oracle_a
from .world import AUTHORITIES, Episode

ANNUAL = "Annual accounts filed"
MISSING_EXCERPT = {"request": {"request_fresh_excerpt"},                    # oracle: the file is not current
                   "evidence": {"request_fresh_excerpt", "escalate"},       # missing evidence; R5: request or escalate
                   "optional": {"no_action"}}                               # R3 does not require an excerpt


def c3_answer(e: Episode, independence_shown: bool = True, controller_required: bool = True) -> set[str]:
    """Oracle A for c3. With independence_shown=False exception R2(b) is never applied. With controller_required=False the
    policy's condition that the other source be independent of the register's controlling authority is dropped (the AMLR
    wording, "another reliable source"; exploratory reading added 2026-11-03, not used by the registered key)."""
    reg = next((s for s in e.sources if s.authority == "A_CBR"), None)
    stm = _a_reliable_owner_statements(e)
    if reg is None or not stm:
        return {"request_document", "escalate"}
    _, high, susp = _a_risk(e)
    if susp:
        return {"escalate"}
    r = reg.content["beneficial_owners"][0]
    names = {(n, d) for _, n, d, _ in stm}
    if len(names) > 1:
        return {"escalate", "request_document"}
    name, dob = next(iter(names))
    cus = next((s for s in e.sources if s.authority == "A_CUS" and "declared_beneficial_owners" in s.content), None)
    if cus:
        c0 = cus.content["declared_beneficial_owners"][0]
        if c0["date_of_birth"] != dob or _a_norm(c0["name"]) != _a_norm(name):
            return {"request_document", "escalate"}
    if name == r["name"] and dob == r["date_of_birth"]:
        return {"no_discrepancy"}
    if dob == r["date_of_birth"] and _a_norm(name) == _a_norm(r["name"]):
        return {"report_to_register"} if high else {"request_customer_correction"}
    last_upd = _d(reg.content["last_updated"])
    if not any(since and _d(since) > last_upd for _, _, _, since in stm):
        return {"report_to_register"}
    reg_ctrl = AUTHORITIES[reg.authority].controller
    indep = [s for s, _, _, _ in stm if (not controller_required or AUTHORITIES[s.authority].controller != reg_ctrl) and s.copy_of is None]
    if independence_shown and indep and not susp and not high:
        return {"request_customer_correction"}
    return {"report_to_register"}


def c5_answer(e: Episode, annual_is_change: bool = False, missing_excerpt: str = "request") -> set[str]:
    """Oracle A for c5. annual_is_change: an "Annual accounts filed" entry after the last full review counts as a
    change. missing_excerpt: what an otherwise current file without any register excerpt requires (MISSING_EXCERPT)."""
    rec = next((s for s in e.sources if s.authority == "A_INT" and "last_full_review" in s.content), None)
    if rec is None:
        return {"escalate", "reopen_cdd"}
    today, last = _d(e.decision_date), _d(rec.content["last_full_review"])
    interval = 365 if rec.content.get("risk_rating") == "higher-risk" else 5 * 365
    changed = any(_d(f["filed_on"]) > last and (annual_is_change or f.get("change") != ANNUAL)
                  for s in e.sources if AUTHORITIES[s.authority].tier <= 2
                  for f in s.content.get("filings", []) + s.content.get("notices", []))
    if changed or (today - last).days > interval:
        return {"reopen_cdd"}
    excerpts = [s for s in e.sources if s.authority == "A_BR" and s.kind.startswith("Business register excerpt")]
    if not excerpts:
        return set(MISSING_EXCERPT[missing_excerpt])
    if all((today - _d(s.issue_date)).days > 30 for s in excerpts):
        return {"request_fresh_excerpt"}
    return {"no_action"}


def review_astar(e: Episode) -> set[str]:
    """A*_rev: the reviewed answer key for one episode (A13)."""
    if e.cls == "c3":
        return c3_answer(e, independence_shown=True)   # E02 verdict withdrawn 2026-10-30: the oracle's reading stands
    if e.cls == "c5":
        return {a for annual in (False, True) for missing in ("evidence", "optional") for a in c5_answer(e, annual, missing)}
    return set(oracle_a(e))


_EP: dict[tuple[str, str], Episode] = {}


def episode_of(r: dict) -> Episode:
    """Regenerate the episode a record was run on (base episode from its seed, then the record's arm)."""
    key = (r["base_id"], r["variant"])
    if key not in _EP:
        m = re.fullmatch(r"(c\d)(s?)-(\d+)", r["base_id"])
        e = GENERATORS[m.group(1)](int(m.group(3)), shift=bool(m.group(2)))
        _EP[key] = e if r["variant"] == "factual" else OPERATORS[r["variant"]](e)
    return _EP[key]


def corrected(data: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """The records with A* replaced by the reviewed key; the input is not changed."""
    return {k: [dict(r, astar=sorted(review_astar(episode_of(r)))) for r in v] for k, v in data.items()}
