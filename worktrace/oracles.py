"""Two independently written oracles for the normative action map A*(E).

Both read ONLY the documents present in the episode (never the hidden facts), so that every
intervention's correct response is recomputed from what the agent could see.

oracle_a: imperative, step-by-step.
oracle_b: declarative rule table with separately implemented helpers (different code path).
Disagreement between them discards the episode (see e1_spec.md §7).
"""
from __future__ import annotations

import datetime as dt
import unicodedata

from .world import AUTHORITIES, Episode, Source


def _d(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


# ===================================================================================== oracle A
def _a_risk(e: Episode) -> tuple[bool, bool, bool]:
    rec = next((s for s in e.sources if s.authority == "A_INT" and "risk_rating" in s.content), None)
    if rec is None:
        return False, False, False
    high = rec.content.get("risk_rating") == "higher-risk"
    susp = any("conceal" in a.lower() for a in rec.content.get("alerts", []))
    return True, high, susp


def _a_reliable_owner_statements(e: Episode) -> list[tuple[Source, str, str, str | None]]:
    """(source, name, dob, holder_since) from tier-1/2 non-register, non-customer evidence about current owners."""
    out = []
    for s in e.sources:
        a = AUTHORITIES[s.authority]
        if a.tier > 2 or s.authority in ("A_CBR", "A_CUS"):
            continue
        for sh in s.content.get("shareholders", []):
            out.append((s, sh["name"], sh["date_of_birth"], sh.get("holder_since")))
        t = s.content.get("transfer")
        if t:
            out.append((s, t["to"], t["to_date_of_birth"], t["effective_date"]))
    return out


def _a_norm(name: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c)).lower()


def oracle_a(e: Episode) -> set[str]:
    if e.cls == "c3":
        reg = next((s for s in e.sources if s.authority == "A_CBR"), None)
        stm = _a_reliable_owner_statements(e)
        if reg is None or not stm:
            return {"request_document", "escalate"}
        _, high, susp = _a_risk(e)
        if susp:
            return {"escalate"}
        r = reg.content["beneficial_owners"][0]
        names = {(n, d) for _, n, d, _ in stm}
        if len(names) > 1:  # reliable sources contradict each other
            return {"escalate", "request_document"}
        name, dob = next(iter(names))
        cus = next((s for s in e.sources if s.authority == "A_CUS" and "declared_beneficial_owners" in s.content), None)
        if cus:
            c0 = cus.content["declared_beneficial_owners"][0]
            if (c0["date_of_birth"] != dob) or (_a_norm(c0["name"]) != _a_norm(name)):
                return {"request_document", "escalate"}
        if name == r["name"] and dob == r["date_of_birth"]:
            return {"no_discrepancy"}
        if dob == r["date_of_birth"] and _a_norm(name) == _a_norm(r["name"]):
            return {"report_to_register"} if high else {"request_customer_correction"}
        last_upd = _d(reg.content["last_updated"])
        outdated = any(since and _d(since) > last_upd for _, n, d, since in stm)
        if not outdated:
            return {"report_to_register"}
        reg_ctrl = AUTHORITIES[reg.authority].controller
        indep = [s for s, n, d, _ in stm if AUTHORITIES[s.authority].controller != reg_ctrl and s.copy_of is None]
        if indep and not susp and not high:
            return {"request_customer_correction"}
        return {"report_to_register"}

    if e.cls == "c5":
        rec = next((s for s in e.sources if s.authority == "A_INT" and "last_full_review" in s.content), None)
        if rec is None:
            return {"escalate", "reopen_cdd"}
        today = _d(e.decision_date)
        last = _d(rec.content["last_full_review"])
        interval = 365 if rec.content.get("risk_rating") == "higher-risk" else 5 * 365
        changes_after = False
        for s in e.sources:
            if AUTHORITIES[s.authority].tier > 2:
                continue
            for f in s.content.get("filings", []) + s.content.get("notices", []):
                if _d(f["filed_on"]) > last and f.get("change") != "Annual accounts filed":
                    changes_after = True
        if changes_after or (today - last).days > interval:
            return {"reopen_cdd"}
        excerpts = [s for s in e.sources if s.authority == "A_BR" and s.kind.startswith("Business register excerpt")]
        if not excerpts or all((today - _d(s.issue_date)).days > 30 for s in excerpts):
            return {"request_fresh_excerpt"}
        return {"no_action"}

    if e.cls == "c6":
        today = _d(e.decision_date)
        chk = next((s for s in e.sources if "checklist" in s.content), None)
        has_screen = any("pep_match" in s.content for s in e.sources)
        has_bo = any("shareholders" in s.content and AUTHORITIES[s.authority].tier <= 2 for s in e.sources)
        has_exc = any(s.kind.startswith("Business register excerpt") and (today - _d(s.issue_date)).days <= 30 for s in e.sources)
        if chk is None or not has_screen or not has_bo or not has_exc or not all(chk.content["checklist"].get(k) for k in
                                  ("identity_verified", "beneficial_owners_verified", "source_of_funds_documented")):
            return {"escalate", "request_document"}
        return {"escalate"}
    raise ValueError(e.cls)


# ===================================================================================== oracle B
_FOLD = str.maketrans("áéöüíšžčÁÉÖÜÍŠŽČ", "aeouiszcAEOUISZC")


def _b_same_person_loose(n1: str, d1: str, n2: str, d2: str) -> bool:
    return d1 == d2 and n1.translate(_FOLD).casefold() == n2.translate(_FOLD).casefold()


def _b_facts(e: Episode) -> dict:
    f: dict = {"reg": None, "ev": [], "high": False, "susp": False, "review": None, "risk": "standard",
               "excerpt_ages": [], "post_review_changes": 0, "checklist": None,
               "screening": False, "declared": None}
    today = _d(e.decision_date)
    for s in e.sources:
        tier = AUTHORITIES[s.authority].tier
        c = s.content
        if s.authority == "A_CBR":
            f["reg"] = (c["beneficial_owners"][0]["name"], c["beneficial_owners"][0]["date_of_birth"], _d(c["last_updated"]), s)
        if s.authority == "A_INT":
            f["high"] = f["high"] or c.get("risk_rating") == "higher-risk"
            f["risk"] = c.get("risk_rating", f["risk"])
            f["susp"] = f["susp"] or any("conceal" in x.lower() for x in c.get("alerts", []))
            if "last_full_review" in c:
                f["review"] = _d(c["last_full_review"])
            if "checklist" in c:
                f["checklist"] = c["checklist"]
            if "pep_match" in c:
                f["screening"] = True
        if s.authority == "A_CUS" and "declared_beneficial_owners" in c:
            f["declared"] = (c["declared_beneficial_owners"][0]["name"], c["declared_beneficial_owners"][0]["date_of_birth"])
        if tier <= 2 and s.authority not in ("A_CBR", "A_CUS"):
            for sh in c.get("shareholders", []):
                f["ev"].append((sh["name"], sh["date_of_birth"], sh.get("holder_since"), s))
            if "transfer" in c:
                t = c["transfer"]
                f["ev"].append((t["to"], t["to_date_of_birth"], t["effective_date"], s))
        if s.authority == "A_BR" and s.kind.startswith("Business register excerpt"):
            f["excerpt_ages"].append((today - _d(s.issue_date)).days)
    if f["review"] is not None:
        for s in e.sources:
            if AUTHORITIES[s.authority].tier <= 2:
                for x in s.content.get("filings", []) + s.content.get("notices", []):
                    if x.get("change") != "Annual accounts filed" and _d(x["filed_on"]) > f["review"]:
                        f["post_review_changes"] += 1
    return f


def oracle_b(e: Episode) -> set[str]:
    f = _b_facts(e)
    today = _d(e.decision_date)
    if e.cls == "c3":
        rules = [
            (lambda: f["reg"] is None or not f["ev"], {"request_document", "escalate"}),
            (lambda: f["susp"], {"escalate"}),
            (lambda: len({(n, d) for n, d, _, _ in f["ev"]}) > 1, {"escalate", "request_document"}),
            (lambda: f["declared"] is not None and not _b_same_person_loose(f["declared"][0], f["declared"][1],
                                                                            f["ev"][0][0], f["ev"][0][1]),
             {"request_document", "escalate"}),
            (lambda: (f["ev"][0][0], f["ev"][0][1]) == f["reg"][:2], {"no_discrepancy"}),
            (lambda: _b_same_person_loose(f["ev"][0][0], f["ev"][0][1], f["reg"][0], f["reg"][1]) and f["high"],
             {"report_to_register"}),
            (lambda: _b_same_person_loose(f["ev"][0][0], f["ev"][0][1], f["reg"][0], f["reg"][1]),
             {"request_customer_correction"}),
            (lambda: not any(h and _d(h) > f["reg"][2] for _, _, h, _ in f["ev"]), {"report_to_register"}),
            (lambda: f["high"] or f["susp"], {"report_to_register"}),
            (lambda: any(src.copy_of is None and AUTHORITIES[src.authority].controller
                         not in {AUTHORITIES[f["reg"][3].authority].controller} for _, _, _, src in f["ev"]),
             {"request_customer_correction"}),
            (lambda: True, {"report_to_register"}),
        ]
    elif e.cls == "c5":
        limit = 365 if f["risk"] == "higher-risk" else 1825
        rules = [
            (lambda: f["review"] is None, {"escalate", "reopen_cdd"}),
            (lambda: f["post_review_changes"] > 0, {"reopen_cdd"}),
            (lambda: (today - f["review"]).days > limit, {"reopen_cdd"}),
            (lambda: not f["excerpt_ages"] or min(f["excerpt_ages"]) > 30, {"request_fresh_excerpt"}),
            (lambda: True, {"no_action"}),
        ]
    elif e.cls == "c6":
        ck = f["checklist"] or {}
        rules = [
            (lambda: not (ck.get("identity_verified") and ck.get("beneficial_owners_verified")
                          and ck.get("source_of_funds_documented")), {"escalate", "request_document"}),
            (lambda: not f["screening"] or not f["ev"] or not f["excerpt_ages"] or min(f["excerpt_ages"]) > 30,
             {"escalate", "request_document"}),
            (lambda: True, {"escalate"}),
        ]
    else:
        raise ValueError(e.cls)
    for cond, out in rules:
        if cond():
            return set(out)
    raise AssertionError("unreachable")


def normative(e: Episode) -> tuple[set[str], bool]:
    """A*(E) and whether the two oracles agree."""
    a, b = oracle_a(e), oracle_b(e)
    return a, a == b
