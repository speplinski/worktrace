"""Sample for the author's blind expert review of the normative answers A* (oracle labels).

Per class (c3, c5, c6), 10 episodes from the common core (run 0), chosen deterministically:
  5 intervention or factual arms where the most configurations disagree with the oracle (most likely label errors),
  2 contested arms of A1 (c3, c5; for c6, two more high-disagreement arms),
  2 shifted factual episodes with the most outcome errors across configurations,
  1 arm where every configuration agrees with the oracle (control).
Ties are broken by a seeded shuffle. Writes paper/pilot/expert_review/items.json.

  python -m worktrace.expert_sample
"""
from __future__ import annotations

import json
import random
import re
from collections import defaultdict
from pathlib import Path

from . import analysis as A
from .classes import GENERATORS
from .interventions import variants

SEED = 20261028
OUT = Path("paper/pilot/expert_review/items.json")


def episode(base_id: str, variant: str):
    m = re.fullmatch(r"(c\d)(s?)-(\d+)", base_id)
    e = GENERATORS[m.group(1)](int(m.group(3)), shift=bool(m.group(2)))
    return e if variant == "factual" else variants(e, [variant])[0]


def main() -> int:
    data = A.load("runs/pilot")
    cfgs = [c for c in data if not c.startswith("deficit:")]
    arms = defaultdict(lambda: {"answers": {}, "rec": None})
    for cfg in cfgs:
        for r in data[cfg]:
            if not A.in_core(r) or r["variant"] in A.CONTROLS:
                continue
            a = arms[(r["split"], r["episode_id"])]
            a["answers"][cfg] = A._act(r)
            a["rec"] = r
    rng = random.Random(SEED)
    pool = list(arms.items())
    rng.shuffle(pool)
    items = []
    for cls in ("c3", "c5", "c6"):
        def dis(v):
            ans = [x for x in v["answers"].values()]
            return sum(x not in v["rec"]["astar"] for x in ans) / len(ans)
        mine = [(k, v) for k, v in pool if v["rec"]["cls"] == cls and len(v["answers"]) >= 8]
        used: set[str] = set()

        def take(cands, n, stratum):
            got = 0
            for k, v in cands:
                b = v["rec"]["base_id"]
                if got == n or b in used:
                    continue
                used.add(b)
                items.append((stratum, k, v))
                got += 1

        nonshift = [(k, v) for k, v in mine if k[0] != "shifted"]
        contested = [(k, v) for k, v in nonshift if A.contested(v["rec"])]
        hard = sorted([(k, v) for k, v in nonshift if not A.contested(v["rec"])], key=lambda kv: -dis(kv[1]))
        shifted = sorted([(k, v) for k, v in mine if k[0] == "shifted"], key=lambda kv: -dis(kv[1]))
        easy = [(k, v) for k, v in nonshift if dis(v) == 0 and not A.contested(v["rec"])]
        take(hard, 5 if contested else 7, "most disagreement with the oracle")
        take(contested, 2, "contested (A1)")
        take(shifted, 2, "shifted split, most outcome errors")
        take(easy, 1, "all configurations agree (control)")
    out = []
    for stratum, (split, eid), v in items:
        r = v["rec"]
        e = episode(r["base_id"], r["variant"])
        assert [s.id for s in e.sources] == r["source_ids"], eid
        counts: dict[str, int] = defaultdict(int)
        for x in v["answers"].values():
            counts[x or "(no decision)"] += 1
        out.append({"id": eid if split != "shifted" else eid, "split": split, "cls": r["cls"], "variant": r["variant"],
                    "stratum": stratum, "contested": A.contested(r), "task": e.task, "allowed": e.allowed_actions,
                    "documents": [s.full() for s in e.sources], "astar": sorted(r["astar"]),
                    "model_answers": dict(sorted(counts.items(), key=lambda kv: -kv[1])), "n_models": len(v["answers"])})
    rng.shuffle(out)
    for i, it in enumerate(out, 1):
        it["n"] = i
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    by = defaultdict(int)
    for it in out:
        by[(it["cls"], it["stratum"])] += 1
    for k, n in sorted(by.items()):
        print(k, n)
    print(len(out), "items ->", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
