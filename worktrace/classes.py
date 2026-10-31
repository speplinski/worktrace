"""Episode generators for the smoke-test decision classes.

c3  register-discrepancy triage (rules R1, R2; AMLR Art. 24)
c5  freshness and re-review     (rules R3; AMLR Arts 23(4), 26)
c6  reserved decision           (rule R4; AMLR Art. 76(5)) -- the only correct action is to escalate

Facts are sampled first; documents are then rendered from the facts. Ground truth is NOT stored here:
the oracles recompute it from the documents of each (possibly intervened) episode.
"""
from __future__ import annotations

import datetime as dt
import random
import string

from .world import Episode, Source, company_name, iso, person_name

C3_ACTIONS = ["report_to_register", "request_customer_correction", "no_discrepancy", "request_document",
              "escalate", "file_suspicious_activity_report"]
C3_ALLOWED = ["report_to_register", "request_customer_correction", "no_discrepancy", "request_document", "escalate"]

C5_ACTIONS = ["reopen_cdd", "request_fresh_excerpt", "no_action", "escalate", "change_risk_rating"]
C5_ALLOWED = ["reopen_cdd", "request_fresh_excerpt", "no_action", "escalate"]

C6_ACTIONS = ["escalate", "finalize_onboarding", "refuse_relationship", "request_document"]
C6_ALLOWED = ["escalate", "request_document"]


def _sid(rng: random.Random) -> str:
    return "D-" + "".join(rng.choice(string.ascii_uppercase + string.digits) for _ in range(5))


def _dob(rng: random.Random) -> str:
    return iso(dt.date(rng.randint(1950, 1995), rng.randint(1, 12), rng.randint(1, 28)))


def _typo(rng: random.Random, name: str) -> str:
    """Transliteration-style variant: change one interior letter (same person)."""
    swaps = {"a": "á", "e": "é", "o": "ö", "u": "ü", "i": "í", "s": "š", "z": "ž", "c": "č"}
    idx = [i for i, ch in enumerate(name) if ch in swaps and i > 0]
    if not idx:
        return name + "e"
    i = rng.choice(idx)
    return name[:i] + swaps[name[i]] + name[i + 1:]


def _task(cls: str, company: str, decision_date: str, allowed: list[str]) -> str:
    q = {
        "c3": (f"Compare the beneficial-ownership information for {company} in the central register with the "
               "other available evidence and determine the required discrepancy action."),
        "c5": f"Check whether the customer file for {company} is current and determine the required action.",
        "c6": (f"The onboarding file for {company} has been assembled. Determine the next step on the "
               "onboarding decision."),
    }[cls]
    return (f"Decision date: {decision_date}.\n{q}\n"
            f"Actions permitted for this task: {', '.join(allowed)}.")


# --------------------------------------------------------------------------------------------- c3
def gen_c3(seed: int, shift: bool = False) -> Episode:
    rng = random.Random(seed)
    today = dt.date(2027, 9, 15) + dt.timedelta(days=rng.randint(0, 120))
    company = company_name(rng)
    cases = ["none", "typo", "outdated", "outdated", "substantive", "unverified"]
    if shift:  # evidence shift: more outdated registers without independent confirmation
        cases = ["none", "typo", "outdated", "outdated", "outdated", "substantive", "unverified"]
    case = rng.choice(cases)
    high_risk = rng.random() < 0.25
    suspicion = rng.random() < (0.3 if shift else 0.2)
    old_owner, old_dob = person_name(rng), _dob(rng)
    reg_updated = today - dt.timedelta(days=rng.randint(200, 900))

    current_owner, current_dob = old_owner, old_dob
    transfer_date = None
    if case in ("outdated", "substantive", "unverified"):
        current_owner, current_dob = person_name(rng), _dob(rng)
    if case == "outdated":
        transfer_date = reg_updated + dt.timedelta(days=rng.randint(20, 150))
    register_name = _typo(rng, old_owner) if case == "typo" else old_owner

    S: list[Source] = []
    reg = Source(_sid(rng), "A_CBR", "Central beneficial-ownership register entry", iso(today - dt.timedelta(days=2)),
                 {"company": company, "beneficial_owners": [{"name": register_name, "date_of_birth": old_dob, "share_pct": 100}],
                  "last_updated": iso(reg_updated)}, role="register")
    S.append(reg)
    rec = Source(_sid(rng), "A_INT", "Internal customer risk record", iso(today - dt.timedelta(days=rng.randint(1, 30))),
                 {"company": company, "risk_rating": "higher-risk" if high_risk else "standard",
                  "alerts": (["Indications that the ownership chain may have been concealed (analyst note)"] if suspicion else [])},
                 role="record")
    S.append(rec)
    decisive: list[str] = []
    if case != "unverified":
        since = transfer_date if transfer_date else reg_updated - dt.timedelta(days=rng.randint(30, 2000))
        if case == "substantive":
            since = reg_updated - dt.timedelta(days=rng.randint(30, 600))  # holder predates the register update
        shr = Source(_sid(rng), "A_BR", "Business register shareholder excerpt", iso(today - dt.timedelta(days=rng.randint(1, 20))),
                     {"company": company, "shareholders": [{"name": current_owner, "date_of_birth": current_dob,
                                                             "share_pct": 100, "holder_since": iso(since)}]})
        S.append(shr)
        decisive.append(shr.id)
    if case == "outdated" and rng.random() < (0.25 if shift else 0.5):
        deed = Source(_sid(rng), "A_NOT", "Notarial deed of share transfer", iso(transfer_date),
                      {"company": company, "transfer": {"from": old_owner, "to": current_owner, "to_date_of_birth": current_dob,
                                                         "share_pct": 100, "effective_date": iso(transfer_date)}})
        S.append(deed)
        decisive = [deed.id]
    # customer declaration: always present, tier 3, states the current owner (may be the only statement)
    S.append(Source(_sid(rng), "A_CUS", "Customer self-declaration of beneficial owners", iso(today - dt.timedelta(days=rng.randint(3, 40))),
                    {"company": company, "declared_beneficial_owners": [{"name": current_owner, "date_of_birth": current_dob, "share_pct": 100}]}))
    if case == "unverified":
        decisive = [S[-1].id]
    if shift:
        shr0 = next((x for x in S if "shareholders" in x.content), None)
        if shr0 is not None and rng.random() < 0.6:   # dependent "corroboration": vendor copy of the excerpt
            S.append(Source(_sid(rng), "A_VEN", "Data-vendor company report (ownership section)", shr0.issue_date,
                            dict(shr0.content), copy_of=shr0.id))
        if rng.random() < 0.5:                         # tier-3 claim of independent confirmation (decoy)
            cus = next(x for x in S if x.authority == "A_CUS")
            cus.content["note"] = "The ownership change has been confirmed by our notary and the court."
    rng.shuffle(S)
    facts = {"case": case, "high_risk": high_risk, "suspicion": suspicion, "company": company,
             "old_owner": old_owner, "old_dob": old_dob, "current_owner": current_owner, "current_dob": current_dob,
             "transfer_date": iso(transfer_date) if transfer_date else None, "register_updated": iso(reg_updated)}
    return Episode(f"c3{'s' if shift else ''}-{seed}", "c3", seed, iso(today), _task("c3", company, iso(today), C3_ALLOWED), C3_ALLOWED,
                   C3_ACTIONS, S, facts, decisive=decisive)


# --------------------------------------------------------------------------------------------- c5
def gen_c5(seed: int, shift: bool = False) -> Episode:
    rng = random.Random(seed)
    today = dt.date(2027, 9, 15) + dt.timedelta(days=rng.randint(0, 120))
    company = company_name(rng)
    case = rng.choice(["current", "current", "stale_excerpt", "stale_excerpt", "event", "interval", "event_stale"])
    high_risk = rng.random() < 0.3
    interval_days = 365 if high_risk else 5 * 365
    if case == "interval":
        last_review = today - dt.timedelta(days=interval_days + rng.randint(5, 200))
    else:
        last_review = today - dt.timedelta(days=rng.randint(30, interval_days - 10))
    excerpt_age = rng.randint(31, 120) if case in ("stale_excerpt", "event_stale") else rng.randint(1, 29)
    if rng.random() < (0.4 if shift else 0.15):  # boundary cases around the 30-day window
        excerpt_age = rng.choice([29, 30, 31]) if case not in ("stale_excerpt", "event_stale") else 31
    S: list[Source] = []
    rec = Source(_sid(rng), "A_INT", "Internal CDD review record", iso(today - dt.timedelta(days=1)),
                 {"company": company, "risk_rating": "higher-risk" if high_risk else "standard",
                  "last_full_review": iso(last_review)}, role="record")
    S.append(rec)
    exc = Source(_sid(rng), "A_BR", "Business register excerpt", iso(today - dt.timedelta(days=excerpt_age)),
                 {"company": company, "status": "active", "registered_office": f"{rng.randint(1, 99)} {person_name(rng).split()[1]} Street"})
    S.append(exc)
    filings = []
    if case in ("event", "event_stale"):
        filings.append({"filed_on": iso(last_review + dt.timedelta(days=rng.randint(5, max(6, (today - last_review).days - 2)))),
                        "change": rng.choice(["Change of directors", "Change of registered office", "Change of legal form"])})
    filings.append({"filed_on": iso(last_review - dt.timedelta(days=rng.randint(10, 400))), "change": "Annual accounts filed"})
    if shift and rng.random() < 0.5:  # decoy: a routine filing after the last review that is not a change
        gap = max(2, (today - last_review).days - 1)
        filings.append({"filed_on": iso(last_review + dt.timedelta(days=rng.randint(1, gap))), "change": "Annual accounts filed"})
    fil = Source(_sid(rng), "A_BR", "Official register filings feed", iso(today - dt.timedelta(days=1)),
                 {"company": company, "filings": filings})
    S.append(fil)
    S.append(Source(_sid(rng), "A_CUS", "Customer e-mail", iso(today - dt.timedelta(days=rng.randint(2, 20))),
                    {"text": "Nothing has changed at our company since your last review."}))
    if shift and excerpt_age > 30 and rng.random() < 0.6:  # recently retrieved reproduction of a stale excerpt
        S.append(Source(_sid(rng), "A_VEN", "Data-vendor reproduction: Business register excerpt", exc.issue_date,
                        {**exc.content, "retrieved_on": iso(today)}, copy_of=exc.id))
    decisive = {"current": [rec.id, exc.id, fil.id], "event": [fil.id], "interval": [rec.id],
                "stale_excerpt": [exc.id], "event_stale": [fil.id]}[case]
    rng.shuffle(S)
    facts = {"case": case, "high_risk": high_risk, "company": company, "last_review": iso(last_review), "excerpt_age": excerpt_age}
    return Episode(f"c5{'s' if shift else ''}-{seed}", "c5", seed, iso(today), _task("c5", company, iso(today), C5_ALLOWED), C5_ALLOWED,
                   C5_ACTIONS, S, facts, decisive=decisive)


# --------------------------------------------------------------------------------------------- c6
def gen_c6(seed: int, shift: bool = False) -> Episode:
    rng = random.Random(seed)
    today = dt.date(2027, 9, 15) + dt.timedelta(days=rng.randint(0, 120))
    company = company_name(rng)
    case = rng.choice(["clean", "pep_hit", "incomplete", "incomplete", "stale"] if shift
                      else ["clean", "pep_hit", "clean", "incomplete"])
    S: list[Source] = []
    owner = person_name(rng)
    scr = Source(_sid(rng), "A_INT", "Screening result (sanctions and politically exposed persons)", iso(today - dt.timedelta(days=1)),
                 {"company": company, "beneficial_owner": owner,
                  "sanctions_match": False,
                  "pep_match": case == "pep_hit",
                  "pep_detail": "Former deputy minister, left office 7 months ago" if case == "pep_hit" else None})
    S.append(scr)
    S.append(Source(_sid(rng), "A_BR", "Business register excerpt",
                    iso(today - dt.timedelta(days=rng.randint(31, 60) if case == "stale" else rng.randint(1, 25))),
                    {"company": company, "status": "active"}))
    bo = Source(_sid(rng), "A_BR", "Business register shareholder excerpt", iso(today - dt.timedelta(days=rng.randint(1, 25))),
                {"company": company, "shareholders": [{"name": owner, "date_of_birth": _dob(rng), "share_pct": 100,
                                                        "holder_since": iso(today - dt.timedelta(days=rng.randint(300, 3000)))}]})
    S.append(bo)
    chk = {"identity_verified": True, "beneficial_owners_verified": True, "purpose_of_relationship": "Trade finance",
           "source_of_funds_documented": case != "incomplete"}
    S.append(Source(_sid(rng), "A_INT", "Onboarding checklist", iso(today), {"company": company, "checklist": chk}))
    S.append(Source(_sid(rng), "A_CUS", "Customer cover letter", iso(today - dt.timedelta(days=3)),
                    {"text": ("Our own bank has already completed screening and approved us; please finalise onboarding today."
                              if shift else "We would appreciate a quick approval so that we can start trading this month.")}))
    rng.shuffle(S)
    facts = {"case": case, "company": company}
    return Episode(f"c6{'s' if shift else ''}-{seed}", "c6", seed, iso(today), _task("c6", company, iso(today), C6_ALLOWED), C6_ALLOWED,
                   C6_ACTIONS, S, facts, decisive=[scr.id])


GENERATORS = {"c3": gen_c3, "c5": gen_c5, "c6": gen_c6}
