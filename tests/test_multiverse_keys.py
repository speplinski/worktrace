"""The exploratory multiverse (paper/pilot/multiverse/multiverse.py) enumerates 90 combinations of four logged policy
readings. The paper states that all 90 give distinct answer keys, i.e. differ in the admissible set of at least one
episode. This test fixes that count from the episodes of the pilot (calibration, held-out and shifted splits)."""
import hashlib, importlib.util, itertools, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_multiverse():
    spec = importlib.util.spec_from_file_location("multiverse", ROOT / "paper/pilot/multiverse/multiverse.py")
    mod = importlib.util.module_from_spec(spec)
    sys.argv = ["multiverse"]  # the module reads argv for its output directory
    spec.loader.exec_module(mod)
    return mod


def test_ninety_readings_give_ninety_distinct_keys():
    mv = _load_multiverse()
    A, K = mv.A, mv.K
    full = A.load(str(ROOT / "runs/pilot"))
    episodes = {}
    for recs in full.values():
        for r in recs:
            if r["episode_id"] not in episodes:
                episodes[r["episode_id"]] = K.episode_of(r)
    ids = sorted(episodes)
    assert len(ids) > 1000
    seen = {}
    for indep, annual, excerpt, deed in mv.READINGS:
        h = hashlib.sha1("|".join(",".join(sorted(mv.key_for(episodes[i], indep, annual, excerpt, deed))) for i in ids).encode()).hexdigest()
        seen.setdefault(h, []).append((indep, annual, excerpt, deed))
    assert len(mv.READINGS) == 90
    assert len(seen) == 90, f"{len(seen)} distinct keys; coinciding readings: {[v for v in seen.values() if len(v) > 1]}"
    text = (ROOT / "paper/pilot/multiverse/multiverse.md").read_text()
    assert "90 answer keys" in text and "All 90 keys differ" in text
