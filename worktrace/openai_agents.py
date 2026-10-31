"""OpenAI configurations (amendment A5): an agent with tools on the Responses API, and the Decisions API as a
decision model. Plain HTTPS (httpx), no extra dependency. Key: WORKTRACE_OPENAI_KEY in .env (never committed).

Same policy, same tools, same episode text as the Claude agent. No sampling parameters (GPT-6 reasoning models
reject temperature when reasoning effort is not "none"); reasoning effort "medium", as for Claude.
Request/response shapes follow developers.openai.com/api/docs/guides/function-calling and .../guides/decisions
(read 2026-10-26).
"""
from __future__ import annotations

import json
import os
import time
from typing import Any

from .agents import (ACTION_DESCRIPTIONS, MAX_TURNS, NUDGES, _decision_from_text, _new_log, _record_decision,
                     execute_tool, tool_specs)
from .policy import POLICY
from .world import Episode

BASE = "https://api.openai.com/v1"


class _Client:
    def __init__(self):
        import httpx
        key = os.environ.get("WORKTRACE_OPENAI_KEY")
        if not key:
            raise RuntimeError("WORKTRACE_OPENAI_KEY is not set (add it to .env)")
        self.http = httpx.Client(base_url=BASE, timeout=600, headers={"Authorization": f"Bearer {key}"})

    def post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        """POST with retries on rate limits, server errors and connection errors (exponential backoff)."""
        import httpx
        delay = 2.0
        for attempt in range(6):
            try:
                r = self.http.post(path, json=body)
            except httpx.TransportError:
                if attempt == 5:
                    raise
                time.sleep(delay); delay *= 2
                continue
            if r.status_code == 429 or r.status_code >= 500:
                if attempt == 5:
                    r.raise_for_status()
                time.sleep(float(r.headers.get("retry-after", delay))); delay *= 2
                continue
            if r.status_code >= 400:
                raise RuntimeError(f"http_{r.status_code}:{r.text[:300]}")
            return r.json()
        raise RuntimeError("unreachable")


def _usage(u: dict[str, Any]) -> dict[str, int]:
    det = u.get("input_tokens_details") or {}
    cached, written = det.get("cached_tokens", 0) or 0, det.get("cache_write_tokens", 0) or 0
    return {"input": max(0, u.get("input_tokens", 0) - cached - written), "cache_read": cached, "cache_write": written,
            "output": u.get("output_tokens", 0),
            "reasoning": (u.get("output_tokens_details") or {}).get("reasoning_tokens", 0)}


class OpenAIAgent:
    """Agent with tools on the Responses API; the running input list is sent back each turn, including reasoning
    items, as the function-calling guide requires for reasoning models."""

    def __init__(self, model: str, effort: str = "medium"):
        self.model, self.effort, self.client = model, effort, _Client()
        self.name = f"openai:{model}:{effort}"

    def run(self, e: Episode) -> dict[str, Any]:
        log, t0 = _new_log(), time.time()
        tools = [{"type": "function", "name": t["name"], "description": t["description"],
                  "parameters": t["input_schema"], "strict": True} for t in tool_specs(e)]
        items: list[dict[str, Any]] = [{"role": "user", "content": e.task}]
        nudges = 0
        try:
            for _ in range(MAX_TURNS):
                r = self.client.post("/responses", {"model": self.model, "instructions": POLICY, "input": items,
                                                    "tools": tools, "reasoning": {"effort": self.effort}})
                log["turns"] += 1
                log["usage"].append(_usage(r.get("usage") or {}))
                log["stop"] = r.get("status")
                out = r.get("output") or []
                if any(c.get("type") == "refusal" for o in out if o.get("type") == "message" for c in o.get("content", [])):
                    log["error"] = "refusal"
                    break
                items += out
                calls = [o for o in out if o.get("type") == "function_call"]
                if not calls:
                    text = " ".join(c.get("text", "") for o in out if o.get("type") == "message"
                                    for c in o.get("content", []) if c.get("type") == "output_text")
                    log["last_text"] = text[-800:]
                    if nudges >= len(NUDGES):
                        d = _decision_from_text(e, text)
                        if d:
                            _record_decision(e, d, log)
                            log["decision_via"] = "text_fallback"
                        else:
                            log["error"] = "no_decision"
                        break
                    items.append({"role": "user", "content": NUDGES[nudges]})
                    nudges += 1
                    continue
                done = False
                for c in calls:
                    try:
                        args = json.loads(c.get("arguments") or "{}")
                    except json.JSONDecodeError:
                        args = {}
                    if c.get("name") == "submit_decision" and not done:
                        _record_decision(e, args, log)
                        result, done = "Decision recorded.", True
                    else:
                        result = execute_tool(e, c.get("name", ""), args, log)
                    items.append({"type": "function_call_output", "call_id": c["call_id"], "output": result})
                if done:
                    break
            else:
                log["error"] = "max_turns"
        except Exception as ex:  # recorded, never silently replaced by another configuration
            log["error"] = f"openai:{type(ex).__name__}:{str(ex)[:300]}"
        log["seconds"] = round(time.time() - t0, 2)
        return log


class OpenAIDecisionsAgent:
    """Decision-model protocol on the Decisions API (POST /v1/decisions; gpt-6-luna is the only supported model).
    Same information as Basal and d1: policy, task and all documents in one request; one choice question over the
    same action list and descriptions; returns the chosen action, per-option probabilities and a confidence."""

    def __init__(self, model: str = "gpt-6-luna"):
        self.model, self.client = model, _Client()
        self.name = f"openai-decisions:{model}"

    def run(self, e: Episode) -> dict[str, Any]:
        log, t0 = _new_log(), time.time()
        docs = json.dumps([s.full() for s in e.sources], ensure_ascii=False, indent=1)
        body = {"model": self.model,
                "input": [{"role": "developer", "content": [{"type": "input_text", "text": POLICY.split("HOW TO ANSWER")[0].strip()}]},
                          {"role": "user", "content": [{"type": "input_text", "text": f"{e.task}\n\nDOCUMENTS:\n{docs}"}]}],
                "questions": [{"name": "decision", "type": "choice",
                               "instructions": e.task.split("\n")[1] + " Choose the action the policy requires.",
                               "choices": [{"value": a, "description": ACTION_DESCRIPTIONS.get(a, a)} for a in e.all_actions]}]}
        try:
            r = self.client.post("/decisions", body)
            ans = next((a for a in r.get("answers", []) if a.get("name") == "decision"), {})
            log["turns"] = 1
            u = _usage(r.get("usage") or {})
            u["output"] = 0  # output tokens are not charged on this endpoint
            log["usage"].append(u)
            if ans.get("type") == "refusal":
                log["error"] = "refusal"
            else:
                log["confidence"] = ans.get("confidence")
                log["probabilities"] = ans.get("probabilities")
                log["retrieved"] = [s.id for s in e.sources]
                _record_decision(e, {"action": ans.get("choice"), "declared_grounds": [], "decisive_sources": [],
                                     "explanation": ""}, log)
        except Exception as ex:
            log["error"] = f"openai-decisions:{type(ex).__name__}:{str(ex)[:300]}"
        log["seconds"] = round(time.time() - t0, 2)
        return log
