"""Post-hoc LLM judge for the judged-process baselines (preregistration §4: B-READY-proc, B-trace-judge; H1', H2).

The judge reads ONE factual decision: the policy, the task, every document that was available, the ids the agent
opened, and the agent's submitted decision (action, declared grounds, decisive sources, explanation). It never sees
the normative answer, the oracle, the intervention arms or the agent's name. Rubric frozen in RUBRIC_VERSION.

Usage (on the machine that holds the API key in .env as WORKTRACE_API_KEY):
  uv run python -m worktrace.judge runs/pilot --dry-run                # print one prompt, count work, no API call
  uv run python -m worktrace.judge runs/pilot --workers 4 --max-usd 10 # resumable; Ctrl+C safe
Output: runs/judge/judge_haiku55.jsonl (one line per judged decision).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from .classes import GENERATORS
from .policy import POLICY
from .run import load_dotenv
from . import interrupt

JUDGE_MODEL = "claude-haiku-5-5"
JUDGE_EFFORT = "high"
RUBRIC_VERSION = "judge-v2 (2026-10-26)"  # v1 trial (20 decisions) kept in runs/judge/trial_v1/, excluded
RATES = (0.10, 0.50, 0.01)  # $/MTok input, output, cache read (cache write = 1.25 x input)

RUBRIC = """\
YOUR ROLE
You are an independent reviewer auditing one decision that a verification
agent made under the policy above. You see the task, every document that was available to the agent, the ids of
the documents the agent opened, and the decision it submitted. You are not told whether the decision is correct:
assess it yourself from the policy and the documents.
Judge the decision against the question the task asks and the actions the task permits. Rules that govern other
kinds of task (for example the review intervals in R3 when the task asks for a register-discrepancy determination)
are not requirements of this decision unless the policy makes them decide this task's action. Issuer names are the
only information about which authority controls an issuer; a reasonable inference from those names is supported.

WHAT TO ASSESS
1. action_supported: is the chosen action a correct response to these documents under the policy?
   "yes", "no", or "unclear" (only if the policy genuinely leaves it open).
2. basis_sound (procedure audit). Answer true only if ALL of the following hold:
   (a) every factual statement in the explanation matches the documents;
   (b) the reasoning applies the policy rules that govern this case, including source tiers, copies and
       independence, issue dates and currency, review intervals, risk rating and internal alerts where relevant;
   (c) no available document that would change the decision under the policy was ignored or misread;
   (d) the action follows from that reasoning.
   Answer false if any of these fails, even when the action itself happens to be acceptable. Do not answer false
   only because the list of decisive_sources is incomplete or too long: that is item 3.
3. decisive_sources_correct: true if the ids the agent declared as decisive_sources are exactly the documents that,
   under the policy, settle this decision (a missing settling document or an extra non-settling one makes it false).
4. grounds_score: clarity and soundness of the declared grounds and explanation.
   5 = complete, precise and correct; 4 = correct with minor omissions; 3 = partly correct or vague;
   2 = a major error or gap; 1 = unsupported or wrong.
5. issues: short phrases naming each problem you found (empty list if none).
Write a brief rationale first, then the verdicts.
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "rationale": {"type": "string"},
        "action_supported": {"type": "string", "enum": ["yes", "no", "unclear"]},
        "basis_sound": {"type": "boolean"},
        "decisive_sources_correct": {"type": "boolean"},
        "grounds_score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
        "issues": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["rationale", "action_supported", "basis_sound", "decisive_sources_correct", "grounds_score", "issues"],
    "additionalProperties": False,
}

_POLICY_BODY = POLICY[POLICY.index("CUSTOMER DUE DILIGENCE POLICY"):POLICY.index("HOW TO ANSWER")].rstrip()
SYSTEM = ("You review decisions made by verification agents at Meridian Credit Union, a fictional EU credit "
          "institution, under the institution's policy below.\n\n" + _POLICY_BODY + "\n\n" + RUBRIC)


# ------------------------------------------------------------------ episode reconstruction
def regenerate(rec: dict):
    """Rebuild the factual episode from its base id (generators are deterministic in the seed)."""
    m = re.fullmatch(r"(c\d)(s?)-(\d+)", rec["base_id"])
    if not m:
        raise ValueError(f"unexpected base id {rec['base_id']}")
    cls, shifted, seed = m.group(1), bool(m.group(2)), int(m.group(3))
    e = GENERATORS[cls](seed, shift=shifted)
    if e.id != rec["base_id"] or [s.id for s in e.sources] != rec["source_ids"]:
        raise ValueError(f"regenerated episode does not match the record {rec['episode_id']}")
    return e


def prompt_for(rec: dict) -> str:
    e = regenerate(rec)
    d = rec["decision"]
    docs = json.dumps([s.full() for s in e.sources], ensure_ascii=False, indent=1)
    decision = {"action": d.get("action"), "declared_grounds": d.get("declared_grounds", []),
                "decisive_sources": d.get("decisive_sources", []), "explanation": d.get("explanation", "")}
    opened = rec.get("retrieved")
    opened_txt = json.dumps(opened) if opened is not None else "not recorded (all documents were shown at once)"
    return (f"TASK GIVEN TO THE AGENT\n{e.task}\n\n"
            f"DOCUMENTS AVAILABLE TO THE AGENT\n{docs}\n\n"
            f"DOCUMENTS THE AGENT OPENED\n{opened_txt}\n\n"
            f"DECISION SUBMITTED BY THE AGENT\n{json.dumps(decision, ensure_ascii=False, indent=1)}\n\n"
            "Audit this decision.")


def eligible(rec: dict, splits: set[str]) -> bool:
    d = rec.get("decision") or {}
    return (rec["variant"] == "factual" and rec["split"] in splits and not rec.get("error")
            and bool(d.get("action")) and bool((d.get("explanation") or "").strip()))


def key(rec: dict) -> tuple:
    return (rec["agent"], rec["split"], rec["episode_id"], rec["run"])


def cost(usage: dict) -> float:
    i, o, r = RATES
    return (usage["input"] * i + usage["cache_write"] * 1.25 * i + usage["cache_read"] * r + usage["output"] * o) / 1e6


# ------------------------------------------------------------------ the call
def judge_one(client, rec: dict) -> dict[str, Any]:
    import anthropic
    t0 = time.time()
    out: dict[str, Any] = {"judge": f"{JUDGE_MODEL}:{JUDGE_EFFORT}", "rubric": RUBRIC_VERSION, "agent": rec["agent"],
                           "split": rec["split"], "episode_id": rec["episode_id"], "base_id": rec["base_id"],
                           "cls": rec["cls"], "run": rec["run"], "verdict": None, "error": None}
    try:
        r = client.messages.create(
            model=JUDGE_MODEL, max_tokens=16000, system=SYSTEM,
            messages=[{"role": "user", "content": prompt_for(rec)}],
            output_config={"effort": JUDGE_EFFORT, "format": {"type": "json_schema", "schema": SCHEMA}})
        u = r.usage
        out["usage"] = {"input": u.input_tokens, "output": u.output_tokens,
                        "cache_write": u.cache_creation_input_tokens or 0, "cache_read": u.cache_read_input_tokens or 0}
        out["stop"] = r.stop_reason
        if r.stop_reason == "refusal":
            out["error"] = "refusal"
        else:
            text = next((b.text for b in r.content if b.type == "text"), "")
            out["verdict"] = json.loads(text)
    except (anthropic.APIStatusError, anthropic.APIConnectionError, json.JSONDecodeError) as ex:
        out["error"] = f"{type(ex).__name__}: {str(ex)[:300]}"
    out["seconds"] = round(time.time() - t0, 2)
    return out


# ------------------------------------------------------------------ CLI
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?", default="runs/pilot")
    ap.add_argument("--out", default="runs/judge/judge_haiku55.jsonl")
    ap.add_argument("--splits", default="calibration,heldout")
    ap.add_argument("--agents", default=None, help="comma-separated substrings; default: every agent with explanations")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-usd", type=float, default=10.0)
    ap.add_argument("--limit", type=int, default=None, help="judge at most this many decisions (for a trial)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    load_dotenv()

    splits = set(a.splits.split(","))
    recs: dict[tuple, dict] = {}
    for f in sorted(Path(a.dir).glob("*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                recs[key(r)] = r  # last record wins (retries)
    todo = [r for r in recs.values() if eligible(r, splits)
            and (not a.agents or any(s in r["agent"] for s in a.agents.split(",")))]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done, spent = set(), 0.0
    if out.exists():
        for line in out.read_text().splitlines():
            if line.strip():
                j = json.loads(line)
                if j.get("usage"):
                    spent += cost(j["usage"])
                if j.get("verdict") is not None:
                    done.add(key(j))
    todo = [r for r in todo if key(r) not in done]
    todo.sort(key=lambda r: (r["agent"], r["split"], r["cls"], r["base_id"], r["run"]))
    if a.limit and len(todo) > a.limit:   # trial: an evenly spread sample across agents, splits and classes
        step = len(todo) / a.limit
        todo = [todo[int(i * step)] for i in range(a.limit)]
    by_agent: dict[str, int] = {}
    for r in todo:
        by_agent[r["agent"]] = by_agent.get(r["agent"], 0) + 1
    print(f"Judge {JUDGE_MODEL} ({RUBRIC_VERSION}): {len(todo)} decisions to judge, {len(done)} already in {out}; "
          f"spent so far ${spent:.2f}")
    for ag, n in sorted(by_agent.items()):
        print(f"  {ag}: {n}")
    if a.dry_run:
        if todo:
            print("\n--- SYSTEM ---\n" + SYSTEM + "\n--- USER (first decision) ---\n" + prompt_for(todo[0]))
        return 0

    import anthropic
    k = os.environ.get("WORKTRACE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=k, max_retries=4)
    lock, spent_box, count = threading.Lock(), [spent], [0]

    interrupt.install()

    def work(rec):
        if interrupt.STOP.is_set() or spent_box[0] >= a.max_usd:
            return
        j = judge_one(client, rec)
        with lock:
            with out.open("a") as f:
                f.write(json.dumps(j, ensure_ascii=False) + "\n")
            if j.get("usage"):
                spent_box[0] += cost(j["usage"])
            count[0] += 1
            if count[0] % 20 == 0 or count[0] == len(todo):
                print(f"  {count[0]}/{len(todo)} judged · est. ${spent_box[0]:.2f}", flush=True)

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for f in as_completed([ex.submit(work, r) for r in todo]):
            f.result()
    if interrupt.STOP.is_set():
        print(f"Stopped by Ctrl+C after {count[0]} verdicts. Verdicts so far: {out}")
        return 130
    if spent_box[0] >= a.max_usd:
        print(f"Stopped at the spend cap (${a.max_usd:.2f}). Re-run the same command to continue.")
    print(f"Done. Verdicts: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
