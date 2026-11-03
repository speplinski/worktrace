"""Token accounting for the paper's cost table (paper/pilot/token_costs.py): the OpenAI Responses API reports reasoning
tokens inside output_tokens (output_tokens_details.reasoning_tokens is a subset), so the `reasoning` field kept in the
run records must not be added to `output` a second time. Regression test for the double count corrected on 2026-11-03."""
import importlib.util, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location("token_costs", ROOT / "paper/pilot/token_costs.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def test_reasoning_tokens_are_not_added_twice():
    tc = _load()
    rec = {"usage": [{"input": 3, "cache_read": 1120, "cache_write": 0, "output": 14, "reasoning": 0},
                     {"input": 3, "cache_read": 1240, "cache_write": 260, "output": 274, "reasoning": 116}]}
    i, o, cr, cw = tc.tokens(rec)
    assert (i, o, cr, cw) == (6, 288, 2360, 260)   # output = 14 + 274; the 116 reasoning tokens are already inside 274


def test_records_without_reasoning_field_are_unchanged():
    tc = _load()
    rec = {"usage": [{"input": 4, "output": 27, "cache_write": 2175, "cache_read": 0}, {"input": 2, "output": 104, "cache_write": 169, "cache_read": 2175}]}
    assert tc.tokens(rec) == (6, 131, 2175, 2344)
