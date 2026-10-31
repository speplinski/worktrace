import json
from types import SimpleNamespace

from worktrace import judge
from worktrace.classes import GENERATORS


def _rec(cls="c3", seed=100000, shift=False):
    e = GENERATORS[cls](seed, shift=shift)
    return {"agent": "claude:test", "split": "calibration", "episode_id": e.id, "base_id": e.id, "cls": cls,
            "variant": "factual", "run": 0, "source_ids": [s.id for s in e.sources], "retrieved": None,
            "decision": {"action": "escalate", "declared_grounds": [], "decisive_sources": [], "explanation": "x"}}


def test_regenerate_matches_all_classes_and_shift():
    for cls in ("c3", "c5", "c6"):
        for shift, base in ((False, 100000), (True, 300000)):
            for i in range(30):
                r = _rec(cls, base + i, shift)
                assert judge.regenerate(r).id == r["base_id"]


def test_prompt_hides_ground_truth():
    r = _rec()
    r["astar"], r["decisive"] = ["report_to_register"], ["D-XXXXX"]
    p = judge.prompt_for(r) + judge.SYSTEM
    assert "astar" not in p and "D-XXXXX" not in p and "claude:test" not in p
    assert "intervention" not in p.lower() and "oracle" not in p.lower()


def test_judge_one_parses_structured_output():
    verdict = {"rationale": "ok", "action_supported": "yes", "basis_sound": True, "decisive_sources_correct": False,
               "grounds_score": 4, "issues": []}
    usage = SimpleNamespace(input_tokens=10, output_tokens=5, cache_creation_input_tokens=0, cache_read_input_tokens=0)
    resp = SimpleNamespace(usage=usage, stop_reason="end_turn",
                           content=[SimpleNamespace(type="thinking"), SimpleNamespace(type="text", text=json.dumps(verdict))])
    calls = []
    client = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: calls.append(kw) or resp))
    out = judge.judge_one(client, _rec())
    assert out["verdict"] == verdict and out["error"] is None
    kw = calls[0]
    assert kw["model"] == "claude-haiku-5-5" and "temperature" not in kw
    assert kw["output_config"]["format"]["schema"] == judge.SCHEMA


def test_only_factual_with_explanation_is_eligible():
    r = _rec()
    assert judge.eligible(r, {"calibration"})
    assert not judge.eligible({**r, "variant": "remove_X"}, {"calibration"})
    assert not judge.eligible({**r, "split": "shifted"}, {"calibration"})
    assert not judge.eligible({**r, "decision": {"action": "escalate"}}, {"calibration"})
