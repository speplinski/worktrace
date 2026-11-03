"""Scoring and cost accounting for run files.

Usage: uv run python -m worktrace.score runs/smoke_haiku.jsonl [more files...]

Rates: claude-api skill model table (cached 2026-10-06); Haiku 5.5 cache-read rate assumed 0.1x input.
Verify against the official pricing page before relying on dollar figures.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

RATES = {  # $/MTok: input, output, cache_read ; cache write = 1.25 x input (5-min TTL)
    "claude-haiku-5-5": (0.10, 0.50, 0.01),
    "claude-sonnet-5-5": (2.00, 10.00, 0.10),  # cache read corrected from 0.20 to 0.10 on 2026-11-03 (pricing page, 2026-10-31), as in paper/pilot/token_costs.py; the run-time spend cap used 0.20
    "claude-opus-5-5": (4.00, 20.00, 0.20),
    # OpenAI, standard tier, short context (developers.openai.com/api/docs/pricing, read 2026-10-26)
    "gpt-6-luna": (0.10, 0.50, 0.01),
    "gpt-6.1-terra": (1.00, 5.00, 0.05),
    "gpt-6.1-sol": (2.00, 10.00, 0.10),
}
CONTROLS = {"null", "placebo", "sham", "copy"}   # preregistration §2: copy is a control


def cost_of(rec: dict) -> float:
    name = rec.get("agent", "")
    if not name.startswith(("claude:", "openai:", "openai-decisions:")):
        return 0.0
    model = name.split(":")[1]
    i, o, r = RATES.get(model, (0, 0, 0))
    c = 0.0
    for u in rec.get("usage", []):
        c += (u["input"] * i + u["cache_write"] * 1.25 * i + u["cache_read"] * r + u["output"] * o) / 1e6
    return c


def _act(rec: dict) -> str | None:
    d = rec.get("decision")
    return d.get("action") if d else None


def summarize(records: list[dict]) -> dict:
    last = {}
    for r in records:  # a retried run supersedes the failed one
        last[(r["agent"], r["episode_id"], r["run"])] = r
    records = list(last.values())
    by_agent = defaultdict(list)
    for r in records:
        by_agent[r["agent"]].append(r)
    report = {}
    for agent, recs in by_agent.items():
        groups = defaultdict(dict)  # (base_id, run) -> variant -> rec
        for r in recs:
            groups[(r["base_id"], r["run"])][r["variant"]] = r
        per_cls = defaultdict(lambda: defaultdict(float))
        for (base, run), vs in groups.items():
            f = vs.get("factual")
            if f is None:
                continue
            m = per_cls[f["cls"]]
            fa = _act(f)
            out_ok = fa in f["astar"]
            m["episodes"] += 1
            m["outcome_correct"] += out_ok
            m["cites_decisive"] += bool(f.get("decision") and set(f["decision"].get("declared_grounds") or []) & set(f["decisive"]))
            basis_fail, ctrl_fail = False, False
            for name, v in vs.items():
                if name == "factual":
                    continue
                va = _act(v)
                if name in CONTROLS:
                    m["control_runs"] += 1
                    if va != fa:
                        if name == "null":      # same episode re-run: pure sampling noise
                            m["null_flip"] += 1
                        else:                   # placebo / sham: change without evidential meaning
                            ctrl_fail = True
                            m["placebo_flip"] += 1
                    m["null_runs" if name == "null" else "placebo_runs"] += 1
                    continue
                m["intervention_runs"] += 1
                ok = va in v["astar"]
                m["intervention_correct"] += ok
                if not ok:
                    basis_fail = True
                changed_star = sorted(v["astar"]) != sorted(f["astar"])
                if changed_star and va == fa:
                    m["non_reaction"] += 1
                if changed_star:
                    m["astar_changed"] += 1
            m["basis_fail"] += basis_fail
            m["wt_fail"] += (not out_ok) or basis_fail
            m["right_outcome_wrong_basis"] += out_ok and basis_fail
            m["placebo_sensitive"] += ctrl_fail
        tot = {"runs": len(recs), "errors": sum(1 for r in recs if r.get("error")),
               "no_decision": sum(1 for r in recs if not r.get("decision")),
               "out_of_permission": sum(1 for r in recs if r.get("out_of_permission")),
               "text_fallback": sum(1 for r in recs if r.get("decision_via") == "text_fallback"),
               "runs_with_text_tool_calls": sum(1 for r in recs if r.get("text_tool_calls")),
               "runs_with_server_errors": sum(1 for r in recs if r.get("server_errors")),
               "reseeded_turns": sum(r.get("reseeded", 0) for r in recs),
               "mean_confidence": (round(sum(r["confidence"] for r in recs if r.get("confidence") is not None)
                                         / max(1, sum(1 for r in recs if r.get("confidence") is not None)), 3)
                                   if any(r.get("confidence") is not None for r in recs) else None),
               "usd": round(sum(cost_of(r) for r in recs), 4),
               "input_tokens": sum(u["input"] + u["cache_write"] + u["cache_read"] for r in recs for u in r.get("usage", [])),
               "output_tokens": sum(u["output"] for r in recs for u in r.get("usage", [])),
               "cache_read_tokens": sum(u["cache_read"] for r in recs for u in r.get("usage", [])),
               "seconds_total": round(sum(r.get("seconds", 0) for r in recs), 1),
               "turns_mean": round(sum(r.get("turns", 0) for r in recs) / max(1, len(recs)), 2)}
        tot["usd_per_run"] = round(tot["usd"] / max(1, len(recs)), 5)
        tot["seconds_per_run"] = round(tot["seconds_total"] / max(1, len(recs)), 2)
        tot["input_tokens_per_run"] = round(tot["input_tokens"] / max(1, len(recs)))
        tot["output_tokens_per_run"] = round(tot["output_tokens"] / max(1, len(recs)))
        classes = {}
        for cls, m in sorted(per_cls.items()):
            n = max(1, m["episodes"])
            classes[cls] = {
                "episodes": int(m["episodes"]),
                "outcome_accuracy": round(m["outcome_correct"] / n, 3),
                "intervention_accuracy": round(m["intervention_correct"] / max(1, m["intervention_runs"]), 3),
                "basis_failure_rate": round(m["basis_fail"] / n, 3),
                "unjustified_rate_lWT": round(m["wt_fail"] / n, 3),
                "right_outcome_wrong_basis": round(m["right_outcome_wrong_basis"] / n, 3),
                "non_reaction_share": round(m["non_reaction"] / max(1, m["astar_changed"]), 3),
                "placebo_sensitive_rate": round(m["placebo_sensitive"] / n, 3),
                "null_flip_rate": round(m["null_flip"] / max(1, m["null_runs"]), 3),
                "placebo_sham_flip_rate": round(m["placebo_flip"] / max(1, m["placebo_runs"]), 3),
                "cites_decisive_rate": round(m["cites_decisive"] / n, 3),
            }
        report[agent] = {"totals": tot, "classes": classes}
    return report


def main(argv: list[str]) -> int:
    recs = []
    for p in argv:
        recs += [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]
    print(json.dumps(summarize(recs), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
