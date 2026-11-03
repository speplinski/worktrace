"""Compute selected rows of the multiverse (for cross-checking between machines). Usage:
  python paper/pilot/multiverse/rows.py 63 78 85       # row numbers as in multiverse.md
  python paper/pilot/multiverse/rows.py --random 3     # three rows drawn with a fixed seed from the added block 61-90"""
import importlib.util, random, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("mv", HERE / "multiverse.py"); argv = sys.argv; sys.argv = ["mv"]
mv = importlib.util.module_from_spec(spec); spec.loader.exec_module(mv); sys.argv = argv
A, K = mv.A, mv.K
if "--random" in sys.argv:
    rows = sorted(random.Random(20261103).sample(range(61, 91), int(sys.argv[sys.argv.index("--random") + 1])))
else:
    rows = [int(x) for x in sys.argv[1:] if x.isdigit()]
full = A.load(str(HERE.parents[2] / "runs/pilot")); core = {k: [r for r in v if A.in_core(r)] for k, v in full.items()}
for i in rows:
    indep, annual, excerpt, deed = mv.READINGS[i - 1]
    out = []
    for name, data in (("core", core), ("all", full)):
        keyed = {k: [dict(r, astar=sorted(mv.key_for(K.episode_of(r), indep, annual, excerpt, deed))) for r in v] for k, v in data.items()}
        h = mv.h3(keyed); c = h["cells"]["track record"]
        out.append(f"{name} {c[0]}:{c[1]}:{c[2]} beta={h['beta']:+.4f} p={h['p']:.4f} theta={100*h['theta']:.1f}%")
    print(f"row {i:2d} | {indep} | {annual} | {excerpt} | {deed} | " + " | ".join(out), flush=True)
