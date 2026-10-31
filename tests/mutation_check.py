"""Mutation check (run by hand): inject known kinds of bugs into worktrace/analysis.py one at a time and confirm the
test suite fails. Restores the file afterwards. Usage: .venv/bin/python tests/mutation_check.py
Expected survivors are equivalent mutants (no behavioural difference on possible data): "<" vs "<=" at alpha,
shifted arms (the shifted split has only the factual arm), H3 classes vs selections (both sorted sets)."""
import shutil, subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]; F = REPO / "worktrace/analysis.py"
orig = F.read_text()
MUTANTS = {
 "copy counted as intervention (A8 bug)": ('            elif name == "copy":\n                m["copy_n"] += 1', '            elif name == "copy":\n                lbasis |= va not in v["astar"]\n                m["copy_n"] += 1'),
 "ties broken by class name (A7 bug)": ('return [tuple(sorted(chosen + list(comb))) for comb in combinations(group, k - len(chosen))]', 'return [tuple(sorted(chosen + group[:k - len(chosen)]))]'),
 "incomplete units kept (A8 bug)": ('if set(vs) == expected_arms(key[1], arms_used):', 'if True:'),
 "contested = old proxy (A12 bug)": ('return _decisive_kind(r["base_id"]).startswith("Business register excerpt")', 'return "request_fresh_excerpt" in r["astar"]'),
 "non-reaction ignores factual correctness (A12 bug)": ('if not lout and fa not in v["astar"]:', 'if fa not in v["astar"]:'),
 "retry replaces no_decision (A12 bug)": ('if old is not None and old.get("error") in AGENT_FAILURES:', 'if False:'),
 "certification uses < instead of <=": ('res[cls] = {"ub": ub, "grant": ub <= alpha}', 'res[cls] = {"ub": ub, "grant": ub < alpha}'),
 "Bonferroni missing": ('ub = _betainc_upper(m[key], m["n"], delta / C)', 'ub = _betainc_upper(m[key], m["n"], delta)'),
 "CP bound two-sided by mistake": ('return float(beta.ppf(1 - delta, k + 1, n - k))', 'return float(beta.ppf(1 - delta / 2, k + 1, n - k))'),
 "l_WT = l_basis only": ('m["l_wt"] += lout or lbasis', 'm["l_wt"] += lbasis'),
 "control flips counted in l_basis": ('                if EXPLORATORY["controls_in_basis"]:\n                    lbasis |= va not in v["astar"]\n            elif name in CONTROLS:', '                lbasis |= va not in v["astar"]\n            elif name in CONTROLS:'),
 "H3 compares ordered lists not sets (old bug)": ('if r["rules"]["DSA"]["selections"] != r["rules"][base]["selections"]', 'if r["rules"]["DSA"]["classes"] != r["rules"][base]["classes"]'),
 "shifted error counts all arms": ('if r["split"] == "shifted" and r["variant"] == "factual":\n            e[r["cls"]][0]', 'if r["split"] == "shifted":\n            e[r["cls"]][0]'),
 "B-TBA uses max -> min": ('out["B-TBA"] = {c: max(v) for c, v in tba.items()}', 'out["B-TBA"] = {c: min(v) for c, v in tba.items()}'),
 "sensitivity skip ignored": ('if SENSITIVITY["on"] and contested(v):\n                continue', 'if False:\n                continue'),
 "core filter off by one": ('seed - SEED_BASE[r["split"]] < CORE[r["split"]]', 'seed - SEED_BASE[r["split"]] <= CORE[r["split"]]'),
}
res = {}
try:
    for name, (a, b) in MUTANTS.items():
        if orig.count(a) != 1:
            res[name] = f"NOT APPLIED (pattern count {orig.count(a)})"; continue
        F.write_text(orig.replace(a, b))
        r = subprocess.run([str(REPO / ".venv/bin/python"), "-m", "pytest", "-q", "-x", str(REPO / "tests")], cwd=REPO,
                           capture_output=True, text=True)
        res[name] = "CAUGHT" if r.returncode != 0 else "survived"
finally:
    F.write_text(orig)
for k, v in res.items(): print(f"{v:30s} {k}")
