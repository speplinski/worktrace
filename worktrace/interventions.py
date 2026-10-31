"""Evidence interventions. Each operator edits the documents only; A* of every variant is recomputed
by the oracles. Operators that do not apply to an episode return None.

Families (e1_spec.md §6): remove_X, only_X, invert_X, add_Y (independent source), add_Y_remove_X (composed),
controls: null, placebo (re-id + reorder), sham (irrelevant document), copy (dependent duplicate of X).
"""
from __future__ import annotations

import datetime as dt
import random
import string

from .world import Episode, Source, iso, person_name

ARMS_FULL = ["factual", "remove_X", "only_X", "invert_X", "add_Y", "add_Y_remove_X", "null", "placebo", "sham", "copy"]


def _rng(e: Episode, salt: str) -> random.Random:
    return random.Random(f"{e.seed}:{e.cls}:{salt}")


def _sid(rng: random.Random) -> str:
    return "D-" + "".join(rng.choice(string.ascii_uppercase + string.digits) for _ in range(5))


def _X(e: Episode) -> Source | None:
    return e.source(e.decisive[0]) if e.decisive else None


def remove_X(e: Episode) -> Episode | None:
    x = _X(e)
    if x is None:
        return None
    v = e.clone("remove_X")
    v.sources = [s for s in v.sources if s.id != x.id]
    return v


def only_X(e: Episode) -> Episode | None:
    x = _X(e)
    if x is None:
        return None
    v = e.clone("only_X")
    keep = set(e.decisive) | {s.id for s in e.sources if s.role in ("register", "record")}
    v.sources = [s for s in v.sources if s.id in keep]
    return None if len(v.sources) == len(e.sources) else v


def invert_X(e: Episode) -> Episode | None:
    x = _X(e)
    if x is None:
        return None
    v = e.clone("invert_X")
    s = v.source(x.id)
    c = s.content
    today = dt.date.fromisoformat(e.decision_date)
    rng = _rng(e, "invert")
    if e.cls == "c3":
        if "transfer" in c:          # deed now names a different recipient -> reliable sources contradict
            c["transfer"]["to"] = person_name(rng)
        elif "shareholders" in c:    # excerpt now matches the register
            reg = next(t for t in v.sources if t.authority == "A_CBR")
            r = reg.content["beneficial_owners"][0]
            c["shareholders"] = [{"name": r["name"], "date_of_birth": r["date_of_birth"], "share_pct": 100,
                                  "holder_since": iso(dt.date.fromisoformat(reg.content["last_updated"]) - dt.timedelta(days=400))}]
        else:
            return None
    elif e.cls == "c5":
        if "filings" in c:
            rec = next(t for t in v.sources if "last_full_review" in t.content)
            last = dt.date.fromisoformat(rec.content["last_full_review"])
            post = [f for f in c["filings"] if f["change"] != "Annual accounts filed" and dt.date.fromisoformat(f["filed_on"]) > last]
            if post:
                for f in post:
                    f["filed_on"] = iso(last - dt.timedelta(days=rng.randint(5, 60)))
            else:
                c["filings"].append({"filed_on": iso(last + dt.timedelta(days=max(1, (today - last).days // 2))),
                                     "change": "Change of directors"})
        elif "last_full_review" in c:
            interval = 365 if c.get("risk_rating") == "higher-risk" else 1825
            last = dt.date.fromisoformat(c["last_full_review"])
            c["last_full_review"] = iso(today - dt.timedelta(days=60)) if (today - last).days > interval \
                else iso(today - dt.timedelta(days=interval + 40))
        elif s.kind.startswith("Business register excerpt"):
            age = (today - dt.date.fromisoformat(s.issue_date)).days
            s.issue_date = iso(today - dt.timedelta(days=5 if age > 30 else 45))
        else:
            return None
    elif e.cls == "c6":
        c["pep_match"] = not c.get("pep_match")
        c["pep_detail"] = "Former deputy minister, left office 7 months ago" if c["pep_match"] else None
    return v


def _independent_confirmation(e: Episode, rng: random.Random) -> Source | None:
    if e.cls == "c3":
        shr = next((s for s in e.sources if "shareholders" in s.content), None)
        cus = next((s for s in e.sources if "declared_beneficial_owners" in s.content), None)
        reg = next((s for s in e.sources if s.authority == "A_CBR"), None)
        if reg is None:
            return None
        if shr:
            o = shr.content["shareholders"][0]
            name, dob, since = o["name"], o["date_of_birth"], o["holder_since"]
        elif cus:
            o = cus.content["declared_beneficial_owners"][0]
            name, dob = o["name"], o["date_of_birth"]
            since = iso(dt.date.fromisoformat(reg.content["last_updated"]) + dt.timedelta(days=30))
        else:
            return None
        return Source(_sid(rng), "A_CRT", "Commercial court record of share transfer", since,
                      {"company": e.facts["company"], "transfer": {"from": "(previous holder)", "to": name, "to_date_of_birth": dob,
                                                                   "share_pct": 100, "effective_date": since}})
    if e.cls == "c5":
        fil = next((s for s in e.sources if "filings" in s.content), None)
        rec = next((s for s in e.sources if "last_full_review" in s.content), None)
        if not fil or not rec:
            return None
        last = dt.date.fromisoformat(rec.content["last_full_review"])
        post = [f for f in fil.content["filings"] if f["change"] != "Annual accounts filed" and dt.date.fromisoformat(f["filed_on"]) > last]
        if not post:
            return None
        return Source(_sid(rng), "A_CRT", "Court gazette notice of registered change", post[0]["filed_on"],
                      {"company": e.facts["company"], "notices": [dict(post[0])]})
    if e.cls == "c6":
        return Source(_sid(rng), "A_NOT", "Notarial certificate of incorporation", iso(dt.date.fromisoformat(e.decision_date) - dt.timedelta(days=900)),
                      {"company": e.facts["company"], "certifies": "Lawful incorporation and current legal existence"})
    return None


def add_Y(e: Episode) -> Episode | None:
    y = _independent_confirmation(e, _rng(e, "addY"))
    if y is None:
        return None
    v = e.clone("add_Y")
    v.sources.insert(_rng(e, "pos").randint(0, len(v.sources)), y)
    return v


def add_Y_remove_X(e: Episode) -> Episode | None:
    a = add_Y(e)
    x = _X(e)
    if a is None or x is None:
        return None
    a.variant, a.id = "add_Y_remove_X", f"{a.base_id}__add_Y_remove_X"
    # remove X and, for c3, the other non-independent tier-1 statement too (so Y must carry the decision)
    drop = {x.id}
    if e.cls == "c3":
        drop |= {s.id for s in e.sources if "shareholders" in s.content or "transfer" in s.content}
    a.sources = [s for s in a.sources if s.id not in drop]
    return a


def null(e: Episode) -> Episode:
    return e.clone("null")


def placebo(e: Episode) -> Episode:
    v = e.clone("placebo")
    rng = _rng(e, "placebo")
    mapping = {s.id: _sid(rng) for s in v.sources}
    for s in v.sources:
        s.id = mapping[s.id]
        if s.copy_of:
            s.copy_of = mapping.get(s.copy_of, s.copy_of)
    v.decisive = [mapping[d] for d in v.decisive if d in mapping]
    rng.shuffle(v.sources)
    return v


def sham(e: Episode) -> Episode:
    v = e.clone("sham")
    rng = _rng(e, "sham")
    v.sources.insert(rng.randint(0, len(v.sources)),
                     Source(_sid(rng), "A_CUS", "Utility bill for business premises", iso(dt.date.fromisoformat(e.decision_date) - dt.timedelta(days=12)),
                            {"company": e.facts["company"], "amount_due": f"{rng.randint(80, 900)}.00", "period": "previous month"},
                            role="irrelevant"))
    return v


def copy(e: Episode) -> Episode | None:
    x = _X(e)
    if x is None or e.cls == "c6":
        return None
    if e.cls == "c3" and not ({"shareholders", "transfer"} & set(x.content)):
        return None
    v = e.clone("copy")
    rng = _rng(e, "copy")
    dup = Source(_sid(rng), "A_VEN", f"Data-vendor reproduction: {x.kind}", x.issue_date, dict(x.content), copy_of=x.id)
    if e.cls == "c5" and x.kind.startswith("Business register excerpt"):
        dup.content["retrieved_on"] = e.decision_date
    v.sources.insert(rng.randint(0, len(v.sources)), dup)
    return v


OPERATORS = {"remove_X": remove_X, "only_X": only_X, "invert_X": invert_X, "add_Y": add_Y,
             "add_Y_remove_X": add_Y_remove_X, "null": null, "placebo": placebo, "sham": sham, "copy": copy}


def variants(e: Episode, arms: list[str]) -> list[Episode]:
    out = []
    for arm in arms:
        if arm == "factual":
            out.append(e)
            continue
        v = OPERATORS[arm](e)
        if v is not None:
            out.append(v)
    return out
