"""Agents: Anthropic (Claude via the official SDK), Ollama (local open-weight models) and scripted agents.

All agents see the same tools and the same policy. Every run returns a dict with the decision, the documents
retrieved, attempted out-of-permission actions, token usage and timing. No sampling parameters are sent to
Claude (they are rejected on current models). Refusal fallbacks are deliberately NOT enabled: a fallback to
another model would silently change the agent configuration being measured; refusals are recorded instead.
"""
from __future__ import annotations

import json
import os
import random
import time
from typing import Any

from .oracles import normative
from .policy import POLICY
from .world import Episode

MAX_TURNS = 14


def tool_specs(e: Episode) -> list[dict[str, Any]]:
    return [
        {"name": "list_sources", "description": "List the documents available for this task (id, type, issuer, issue date).",
         "input_schema": {"type": "object", "properties": {}, "required": [], "additionalProperties": False}},
        {"name": "get_source", "description": "Return the full content of one document by id.",
         "input_schema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"], "additionalProperties": False}},
        {"name": "submit_decision", "description": "Submit your final decision. Call exactly once, at the end.",
         "input_schema": {"type": "object", "additionalProperties": False,
                          "required": ["action", "declared_grounds", "decisive_sources", "explanation"],
                          "properties": {
                              "action": {"type": "string", "enum": e.all_actions},
                              "declared_grounds": {"type": "array", "items": {"type": "string"},
                                                   "description": "Ids of all documents you relied on."},
                              "decisive_sources": {"type": "array", "items": {"type": "string"},
                                                   "description": "Id(s) of the document(s) that settled the decision."},
                              "explanation": {"type": "string"}}}},
    ]


def execute_tool(e: Episode, name: str, args: dict[str, Any], log: dict[str, Any]) -> str:
    if name == "list_sources":
        return json.dumps([s.card() for s in e.sources], ensure_ascii=False)
    if name == "get_source":
        sid = str(args.get("id", ""))
        s = e.source(sid)
        if s is None:
            return json.dumps({"error": f"No document with id {sid!r}."})
        log["retrieved"].append(sid)
        return json.dumps(s.full(), ensure_ascii=False)
    return json.dumps({"error": f"Unknown tool {name!r}."})


def _new_log() -> dict[str, Any]:
    return {"retrieved": [], "decision": None, "turns": 0, "usage": [], "error": None, "stop": None}


def _json_objects(text: str) -> list[dict[str, Any]]:
    """All top-level JSON objects embedded in free text (balanced, nested-safe)."""
    dec, out, i = json.JSONDecoder(), [], 0
    text = text or ""
    while True:
        j = text.find("{", i)
        if j < 0:
            return out
        try:
            obj, k = dec.raw_decode(text, j)
            if isinstance(obj, dict):
                out.append(obj)
            i = k
        except json.JSONDecodeError:
            i = j + 1


def _text_tool_calls(text: str) -> list[tuple[str, dict[str, Any]]]:
    """Tool calls written as JSON text, e.g. {"name": "get_source", "arguments": {"id": "D-1"}}."""
    calls = []
    for o in _json_objects(text):
        name = o.get("name") or o.get("tool") or o.get("function")
        if isinstance(name, dict):
            name = name.get("name")
        args = o.get("arguments") or o.get("parameters") or o.get("args") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                args = {}
        if name in ("list_sources", "get_source", "submit_decision"):
            calls.append((name, args if isinstance(args, dict) else {}))
    return calls


def _decision_from_text(e: Episode, text: str) -> dict[str, Any] | None:
    """Recover a decision written as JSON in plain text instead of a tool call (logged as a fallback)."""
    for name, args in _text_tool_calls(text):
        if name == "submit_decision" and args.get("action") in e.all_actions:
            return {"declared_grounds": [], "decisive_sources": [], "explanation": "", **args}
    for d in _json_objects(text):
        if d.get("action") in e.all_actions:
            return {"declared_grounds": [], "decisive_sources": [], "explanation": "", **d}
    return None


NUDGES = [
    "Please finish now by calling the submit_decision tool.",
    ("You must call the submit_decision tool. Its arguments are: action (one of the permitted actions), "
     "declared_grounds (list of document ids), decisive_sources (list of document ids), explanation (string)."),
]


def _record_decision(e: Episode, args: dict[str, Any], log: dict[str, Any]) -> None:
    log["decision"] = {k: args.get(k) for k in ("action", "declared_grounds", "decisive_sources", "explanation")}
    log["out_of_permission"] = args.get("action") not in e.allowed_actions


# ============================================================================ Anthropic
class ClaudeAgent:
    def __init__(self, model: str, effort: str | None = "medium", api_key: str | None = None):
        import anthropic
        self.model, self.effort = model, effort
        key = api_key or os.environ.get("WORKTRACE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=key, max_retries=4)
        self.name = f"claude:{model}:{effort or 'default'}"

    def run(self, e: Episode) -> dict[str, Any]:
        import anthropic
        log, t0 = _new_log(), time.time()
        tools = [{**t, "strict": True} for t in tool_specs(e)]
        messages: list[dict[str, Any]] = [{"role": "user", "content": e.task}]
        nudges = 0
        kwargs: dict[str, Any] = {"output_config": {"effort": self.effort}} if self.effort else {}
        try:
            for _ in range(MAX_TURNS):
                r = self.client.messages.create(model=self.model, max_tokens=16000, system=POLICY, tools=tools,
                                                messages=messages, cache_control={"type": "ephemeral"}, **kwargs)
                log["turns"] += 1
                u = r.usage
                log["usage"].append({"input": u.input_tokens, "output": u.output_tokens,
                                     "cache_write": getattr(u, "cache_creation_input_tokens", 0) or 0,
                                     "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0})
                log["stop"] = r.stop_reason
                if r.stop_reason == "refusal":
                    log["error"] = f"refusal:{getattr(getattr(r, 'stop_details', None), 'category', None)}"
                    break
                messages.append({"role": "assistant", "content": r.content})
                uses = [b for b in r.content if b.type == "tool_use"]
                if not uses:
                    text = " ".join(getattr(b, "text", "") for b in r.content if b.type == "text")
                    log["last_text"] = text[-800:]
                    if nudges >= len(NUDGES):
                        d = _decision_from_text(e, text)
                        if d:
                            _record_decision(e, d, log)
                            log["decision_via"] = "text_fallback"
                        else:
                            log["error"] = "no_decision"
                        break
                    messages.append({"role": "user", "content": NUDGES[nudges]})
                    nudges += 1
                    continue
                results, done = [], False
                for b in uses:
                    if b.name == "submit_decision" and not done:
                        _record_decision(e, b.input, log)
                        results.append({"type": "tool_result", "tool_use_id": b.id, "content": "Decision recorded."})
                        done = True
                    else:
                        results.append({"type": "tool_result", "tool_use_id": b.id,
                                        "content": execute_tool(e, b.name, b.input, log)})
                if done:
                    break
                messages.append({"role": "user", "content": results})
            else:
                log["error"] = "max_turns"
        except anthropic.APIStatusError as ex:
            log["error"] = f"api_status:{ex.status_code}:{str(ex)[:200]}"
        except anthropic.APIConnectionError as ex:
            log["error"] = f"api_connection:{str(ex)[:200]}"
        log["seconds"] = round(time.time() - t0, 2)
        return log


# ============================================================================ Ollama
class OllamaAgent:
    def __init__(self, model: str, seed: int = 7, think: str | None = None, num_ctx: int = 32768,
                 host: str = "http://localhost:11434"):
        import httpx
        self.model, self.seed, self.think, self.num_ctx = model, seed, think, num_ctx
        self.http = httpx.Client(base_url=host, timeout=600)
        self.name = f"ollama:{model}:seed{seed}:{think or 'default'}"

    def run(self, e: Episode) -> dict[str, Any]:
        log, t0 = _new_log(), time.time()
        tools = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                   "parameters": t["input_schema"]}} for t in tool_specs(e)]
        messages: list[dict[str, Any]] = [{"role": "system", "content": POLICY}, {"role": "user", "content": e.task}]
        nudges = 0
        try:
            for _ in range(MAX_TURNS):
                body: dict[str, Any] = {"model": self.model, "messages": messages, "tools": tools, "stream": False,
                                        "options": {"seed": self.seed, "num_ctx": self.num_ctx}}
                if self.think:
                    body["think"] = self.think
                r = None
                for attempt in range(3):  # Ollama returns 500 when it cannot parse a malformed tool call
                    body["options"]["seed"] = self.seed + attempt
                    resp = self.http.post("/api/chat", json=body)
                    if resp.status_code == 500:
                        log.setdefault("server_errors", []).append(resp.text[:300])
                        continue
                    resp.raise_for_status()
                    r = resp.json()
                    if attempt:
                        log["reseeded"] = log.get("reseeded", 0) + 1
                    break
                if r is None:
                    log["error"] = "ollama:500_after_retries"
                    break
                log["turns"] += 1
                log["usage"].append({"input": r.get("prompt_eval_count", 0), "output": r.get("eval_count", 0),
                                     "cache_write": 0, "cache_read": 0,
                                     "prompt_seconds": r.get("prompt_eval_duration", 0) / 1e9,
                                     "gen_seconds": r.get("eval_duration", 0) / 1e9})
                msg = r.get("message", {})
                messages.append(msg)
                calls = msg.get("tool_calls") or []
                if not calls:
                    text = msg.get("content") or ""
                    log["last_text"] = text[-800:]
                    log["last_thinking"] = (msg.get("thinking") or "")[-400:]
                    tcalls = [(n, g) for n, g in _text_tool_calls(text) if n != "submit_decision"]
                    if tcalls and not _decision_from_text(e, text):
                        results = []
                        for n, g in tcalls:
                            results.append(f"Result of {n}({json.dumps(g)}):\n{execute_tool(e, n, g, log)}")
                        log["text_tool_calls"] = log.get("text_tool_calls", 0) + len(tcalls)
                        messages.append({"role": "user", "content": "\n\n".join(results)})
                        continue
                    d = _decision_from_text(e, text)
                    if d:
                        _record_decision(e, d, log)
                        log["decision_via"] = "text_fallback"
                        break
                    if nudges >= len(NUDGES):
                        log["error"] = "no_decision"
                        break
                    messages.append({"role": "user", "content": NUDGES[nudges]})
                    nudges += 1
                    continue
                done = False
                for c in calls:
                    fn = c.get("function", {})
                    name, args = fn.get("name", ""), fn.get("arguments") or {}
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}
                    if name == "submit_decision" and not done:
                        if args.get("action") not in e.all_actions:
                            messages.append({"role": "tool", "tool_name": name,
                                             "content": json.dumps({"error": f"action must be one of {e.all_actions}"})})
                            continue
                        _record_decision(e, args, log)
                        done = True
                    else:
                        messages.append({"role": "tool", "tool_name": name, "content": execute_tool(e, name, args, log)})
                if done:
                    break
            else:
                log["error"] = "max_turns"
        except Exception as ex:  # network / server errors are recorded, not raised
            log["error"] = f"ollama:{type(ex).__name__}:{str(ex)[:200]}"
        log["seconds"] = round(time.time() - t0, 2)
        return log


# ============================================================================ Ollama, one-pass (all documents in context)
class OllamaInlineAgent:
    """One-pass protocol for models that cannot run an interactive tool loop: the policy, the task and ALL documents
    are given in one prompt; the model answers with a JSON decision (Ollama structured output). Comparable with Basal."""

    def __init__(self, model: str, seed: int = 7, num_ctx: int = 32768, host: str = "http://localhost:11434"):
        import httpx
        self.model, self.seed, self.num_ctx = model, seed, num_ctx
        self.http = httpx.Client(base_url=host, timeout=900)
        self.name = f"ollama-inline:{model}:seed{seed}"

    def run(self, e: Episode) -> dict[str, Any]:
        log, t0 = _new_log(), time.time()
        schema = tool_specs(e)[2]["input_schema"]
        docs = json.dumps([s.full() for s in e.sources], ensure_ascii=False, indent=1)
        prompt = (f"{e.task}\n\nDOCUMENTS (all documents available for this task):\n{docs}\n\n"
                  "Decide now. Answer only with a JSON object with the fields action, declared_grounds (ids of documents "
                  "you relied on), decisive_sources (ids of the documents that settled the decision) and explanation.")
        policy = POLICY.split("HOW TO ANSWER")[0].strip()
        try:
            r = None
            for attempt in range(3):
                body = {"model": self.model, "stream": False, "format": schema,
                        "messages": [{"role": "system", "content": policy}, {"role": "user", "content": prompt}],
                        "options": {"seed": self.seed + attempt, "num_ctx": self.num_ctx}}
                resp = self.http.post("/api/chat", json=body)
                if resp.status_code == 500:
                    log.setdefault("server_errors", []).append(resp.text[:300])
                    continue
                resp.raise_for_status()
                r = resp.json()
                break
            if r is None:
                log["error"] = "ollama:500_after_retries"
            else:
                log["turns"] = 1
                log["usage"].append({"input": r.get("prompt_eval_count", 0), "output": r.get("eval_count", 0),
                                     "cache_write": 0, "cache_read": 0})
                text = (r.get("message") or {}).get("content") or ""
                log["last_text"] = text[-800:]
                log["retrieved"] = [s.id for s in e.sources]
                objs = _json_objects(text)
                d = next((o for o in objs if o.get("action") in e.all_actions), None)
                if d:
                    _record_decision(e, {"declared_grounds": [], "decisive_sources": [], "explanation": "", **d}, log)
                else:
                    log["error"] = "no_decision"
        except Exception as ex:
            log["error"] = f"ollama:{type(ex).__name__}:{str(ex)[:200]}"
        log["seconds"] = round(time.time() - t0, 2)
        return log


# ============================================================================ Basal (decision model, one pass)
ACTION_DESCRIPTIONS = {
    "report_to_register": "Report the beneficial-ownership discrepancy to the central register within 14 days.",
    "request_customer_correction": "Ask the customer to correct the register entry (only where the policy exception applies).",
    "no_discrepancy": "The register agrees with the reliable evidence; no action needed.",
    "request_document": "Request a missing document before deciding.",
    "escalate": "Escalate to a human officer.",
    "file_suspicious_activity_report": "File a suspicious-activity report.",
    "reopen_cdd": "Reopen the customer-due-diligence file for a full review.",
    "request_fresh_excerpt": "Request a current register excerpt.",
    "no_action": "The file is current; no action needed.",
    "change_risk_rating": "Change the customer's risk rating.",
    "finalize_onboarding": "Approve the customer and finalise onboarding.",
    "refuse_relationship": "Refuse the business relationship.",
}


class BasalAgent:
    """Decision-model protocol (Basal, https://github.com/rkinas/basal): one forward pass over a state that contains
    the policy, the task and ALL documents; the model chooses one action and returns calibrated probabilities.
    No retrieval, no declared grounds -> receptivity is not measurable for this configuration; reactivity is.
    Requires a running `basal-serve` (see RUNNING.md)."""

    def __init__(self, label: str, url: str = "http://127.0.0.1:8000", ollama_model: str | None = None):
        import httpx
        self.http = httpx.Client(base_url=url, timeout=600)
        self.ollama_model = ollama_model   # set when the decision model is served by Ollama's /v1/systemone
        self.name = f"{'systemone' if ollama_model else 'basal'}:{label}"

    def run(self, e: Episode) -> dict[str, Any]:
        log, t0 = _new_log(), time.time()
        state = {"policy": POLICY.split("HOW TO ANSWER")[0].strip(), "task": e.task,
                 "documents": [s.full() for s in e.sources]}
        q = {"type": "choice", "instructions": e.task.split("\n")[1] + " Choose the action the policy requires.",
             "criteria": {a: ACTION_DESCRIPTIONS.get(a, a) for a in e.all_actions}}
        try:
            body = {"state": json.dumps(state, ensure_ascii=False), "questions": {"decision": q}, "lang": "en"}
            if self.ollama_model:
                body["model"] = self.ollama_model
            r = self.http.post("/v1/systemone", json=body)
            r.raise_for_status()
            out = r.json()
            ans = out["answers"]["decision"]
            act = ans.get("choice")
            log["turns"] = 1
            u = out.get("usage", {})
            log["usage"].append({"input": u.get("input_tokens", 0), "output": 0, "cache_write": 0, "cache_read": 0})
            log["confidence"] = ans.get("confidence")
            log["probabilities"] = ans.get("probabilities")
            log["retrieved"] = [s.id for s in e.sources]  # everything is in the state
            _record_decision(e, {"action": act, "declared_grounds": [], "decisive_sources": [], "explanation": ""}, log)
        except Exception as ex:
            log["error"] = f"basal:{type(ex).__name__}:{str(ex)[:200]}"
        log["seconds"] = round(time.time() - t0, 2)
        return log


# ============================================================================ scripted (detector validation)
class ScriptedAgent:
    """oracle: always right, cites the decisive documents. ignore_evidence: decides from the episode's prior
    (the most common factual answer of its class) without reading. random: uniform over permitted actions."""

    PRIOR = {"c3": "report_to_register", "c5": "reopen_cdd", "c6": "escalate"}

    def __init__(self, kind: str, seed: int = 0):
        self.kind, self.rng, self.name = kind, random.Random(seed), f"scripted:{kind}"

    def run(self, e: Episode) -> dict[str, Any]:
        log = _new_log()
        log["retrieved"] = [s.id for s in e.sources]
        if self.kind == "oracle":
            act = sorted(normative(e)[0])[0]
            grounds = list(e.decisive)
        elif self.kind == "ignore_evidence":
            act, grounds = self.PRIOR[e.cls], []
        else:
            act, grounds = self.rng.choice(e.allowed_actions), []
        _record_decision(e, {"action": act, "declared_grounds": grounds, "decisive_sources": grounds, "explanation": ""}, log)
        log["seconds"] = 0.0
        return log


def make_agent(spec: str):
    """spec examples: haiku | sonnet | claude:claude-haiku-5-5 | ollama:gpt-oss:20b | scripted:oracle"""
    if spec == "haiku":
        return ClaudeAgent("claude-haiku-5-5")
    if spec == "sonnet":
        return ClaudeAgent("claude-sonnet-5-5")
    if spec.startswith("claude:"):
        return ClaudeAgent(spec.split(":", 1)[1])
    if spec.startswith("ollama-inline:"):
        return OllamaInlineAgent(spec.split(":", 1)[1])
    if spec.startswith("ollama:"):
        return OllamaAgent(spec.split(":", 1)[1])
    if spec.startswith("basal:"):          # basal:<label>[@http://host:port]
        label, _, url = spec.split(":", 1)[1].partition("@")
        return BasalAgent(label, url or "http://127.0.0.1:8000")
    if spec.startswith("systemone:"):      # decision model served by Ollama, e.g. systemone:d1
        m = spec.split(":", 1)[1]
        return BasalAgent(m, "http://localhost:11434", ollama_model=m)
    if spec.startswith("scripted:"):
        return ScriptedAgent(spec.split(":", 1)[1])
    if spec.startswith("openai-decisions:"):  # OpenAI Decisions API, decision-model protocol (amendment A5)
        from .openai_agents import OpenAIDecisionsAgent
        return OpenAIDecisionsAgent(spec.split(":", 1)[1])
    if spec.startswith("openai:"):           # openai:<model>[:<effort>], agent with tools on the Responses API
        from .openai_agents import OpenAIAgent
        parts = spec.split(":")
        return OpenAIAgent(parts[1], parts[2] if len(parts) > 2 else "medium")
    if spec.startswith("deficit:"):        # planted-deficit agents, known-groups test (worktrace/deficits.py)
        from .deficits import DeficitAgent
        return DeficitAgent(spec.split(":", 1)[1])
    raise ValueError(spec)
