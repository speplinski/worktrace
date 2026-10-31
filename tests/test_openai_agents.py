import json

from worktrace import openai_agents as oa
from worktrace.classes import GENERATORS


class FakeClient:
    """Replays a scripted Responses-API conversation: list sources, open one, submit a decision."""
    def __init__(self, e):
        self.e, self.calls = e, []

    def post(self, path, body):
        self.calls.append((path, json.loads(json.dumps(body))))  # snapshot: the agent keeps appending
        n = len(self.calls)
        usage = {"input_tokens": 3000, "input_tokens_details": {"cached_tokens": 2000, "cache_write_tokens": 0},
                 "output_tokens": 500, "output_tokens_details": {"reasoning_tokens": 400}}
        if path == "/decisions":
            return {"answers": [{"type": "choice", "name": "decision", "choice": "escalate", "confidence": 0.8,
                                 "probabilities": [{"value": "escalate", "probability": 0.9}]}], "usage": usage}
        sid = self.e.sources[0].id
        steps = [
            [{"type": "reasoning", "id": "rs_1", "summary": []},
             {"type": "function_call", "call_id": "c1", "name": "list_sources", "arguments": "{}"}],
            [{"type": "function_call", "call_id": "c2", "name": "get_source", "arguments": json.dumps({"id": sid})}],
            [{"type": "function_call", "call_id": "c3", "name": "submit_decision", "arguments": json.dumps(
                {"action": "escalate", "declared_grounds": [sid], "decisive_sources": [sid], "explanation": "x"})}],
        ]
        return {"status": "completed", "output": steps[n - 1], "usage": usage}


def _agent(cls, e, *a):
    ag = cls.__new__(cls)
    if cls is oa.OpenAIAgent:
        ag.model, ag.effort, ag.name = "gpt-6-luna", "medium", "openai:gpt-6-luna:medium"
    else:
        ag.model, ag.name = "gpt-6-luna", "openai-decisions:gpt-6-luna"
    ag.client = FakeClient(e)
    return ag


def test_agent_tool_loop_records_decision_and_sends_items_back():
    e = GENERATORS["c3"](100_000)
    ag = _agent(oa.OpenAIAgent, e)
    log = ag.run(e)
    assert log["error"] is None and log["decision"]["action"] == "escalate" and log["turns"] == 3
    assert log["retrieved"] == [e.sources[0].id]
    last_input = ag.client.calls[-1][1]["input"]
    assert any(i.get("type") == "reasoning" for i in last_input)                # reasoning items passed back
    assert [i["call_id"] for i in last_input if i.get("type") == "function_call_output"] == ["c1", "c2"]
    body = ag.client.calls[0][1]
    assert body["reasoning"] == {"effort": "medium"} and "temperature" not in body
    assert all(t["strict"] for t in body["tools"])
    assert log["usage"][0] == {"input": 1000, "cache_read": 2000, "cache_write": 0, "output": 500, "reasoning": 400}


def test_decisions_agent_maps_choice_and_confidence():
    e = GENERATORS["c6"](100_000)
    ag = _agent(oa.OpenAIDecisionsAgent, e)
    log = ag.run(e)
    assert log["decision"]["action"] == "escalate" and log["confidence"] == 0.8
    q = ag.client.calls[0][1]["questions"][0]
    assert q["type"] == "choice" and {c["value"] for c in q["choices"]} == set(e.all_actions)
