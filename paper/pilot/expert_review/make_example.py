"""Warm-up example sheet (PRZYKLAD) for the rater pack. Usage: python make_example.py [fonts-dir]; writes example_pl.html/.pdf next to this file."""
import importlib.util, json, subprocess, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.argv = ["x", sys.argv[1] if len(sys.argv) > 1 else str(HERE / "fonts")]
spec = importlib.util.spec_from_file_location("ms", "" + str(__import__("pathlib").Path(__file__).resolve().parent / "make_sheets.py") + "")
ms = importlib.util.module_from_spec(spec); spec.loader.exec_module(ms)
sys.path.insert(0, str(ROOT))
from worktrace.classes import GENERATORS
e = GENERATORS["c5"](100019)
it = {"n": 0, "cls": "c5", "task": e.task, "allowed": e.allowed_actions, "documents": [s.full() for s in e.sources]}
h = ms.page(it, "pl")
h = h.replace('<div class="code">Sprawa E00</div>', '<div class="code">PRZYKŁAD</div>')
h = h.replace("<div class='opt'><span class='box'></span><div><code>reopen_cdd</code>", "<div class='opt'><span class='box tick'>✓</span><div><code>reopen_cdd</code>")
h = h.replace("<span class='c'><span class='box sm'></span>pewny/a</span>", "<span class='c'><span class='box sm tick'>✓</span>pewny/a</span>")
h = h.replace('<div class="why">Dlaczego (krótko):<span class="line full"></span></div>',
  '<div class="why">Dlaczego (krótko): <span class="hand">Klient ma podwyższone ryzyko, więc pełny przegląd musi być co najmniej raz w roku (R3). '
  'Ostatni był 2026-10-23, a decyzja zapada 2028-01-08, czyli ponad rok później, więc trzeba otworzyć akta ponownie. '
  'Odpis z 2027-12-29 jest aktualny (10 dni przed decyzją), a wpis z 2026-05-03 jest sprzed ostatniego przeglądu, więc żadne inne działanie nie jest potrzebne.</span></div>')
css = ms.CSS.replace('CSS = """', '') + ".tick{font:700 12pt sans-serif;color:#1a4fa0;text-align:center;line-height:4.4mm} .box.sm.tick{font-size:10pt;line-height:3.4mm} .hand{font-style:italic;color:#1a4fa0}"
doc = f"<!doctype html><html lang='pl'><head><meta charset='utf-8'><style>{ms.font_css()}{css}</style></head><body>{h}</body></html>"
out = str(HERE / "example_pl")
open(out + ".html", "w").write(doc)
js = """const { chromium } = require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.emulateMedia({media:'print'});
await p.goto('file://'+process.argv[1]+'.html');await p.waitForTimeout(400);
const o=await p.evaluate(()=>{const pg=document.querySelector('.page');return pg.scrollHeight-pg.clientHeight});console.log('overflow',o);
await p.pdf({path:process.argv[1]+'.pdf',preferCSSPageSize:true,printBackground:true});await b.close()})();"""
subprocess.run(["node", "-e", js, out], check=True)
