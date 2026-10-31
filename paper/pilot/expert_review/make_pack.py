"""Rater pack: the contested cases of the author's review, for other raters (amendment A13 follow-up).

  .venv/bin/python paper/pilot/expert_review/make_pack.py <fonts_dir>

One page of instructions, one warm-up case from outside the sample (c5-100019, the same the author trained on), then the
cases E02, E03, E22, E23, each on one A4 page; Polish and English. Writes pack_pl.pdf and pack_en.pdf next to this file.
No answers are included anywhere in the pack.
"""
from __future__ import annotations

import html
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.argv = [sys.argv[0]] + sys.argv[1:2]
spec = importlib.util.spec_from_file_location("ms", HERE / "make_sheets.py")
ms = importlib.util.module_from_spec(spec); spec.loader.exec_module(ms)
sys.path.insert(0, str(HERE.parents[2]))
from worktrace.classes import GENERATORS

CASES = ["E02", "E03", "E22", "E23"]
INTRO = {
    "pl": ("Przegląd klucza odpowiedzi", [
        "Dziękuję za pomoc. Masz przed sobą 5 spraw z fikcyjnego banku: jedną rozgrzewkową (PRZYKŁAD) i cztery właściwe. Każda sprawa to jedna "
        "strona: zadanie, dokumenty w aktach i zasady banku, które o niej decydują. Wszystko jest syntetyczne; nazwy firm, osób i krajów są wymyślone.",
        "O co chodzi. Testujemy agentów AI, którzy podejmują takie decyzje. Żeby ocenić agenta, potrzebny jest klucz odpowiedzi: co w danej sprawie "
        "nakazują zasady. Nasz klucz napisał program, a agenci dostali dokładnie te zasady i dokumenty, które widzisz. Chcemy sprawdzić dwie "
        "rzeczy: czy człowiek czytający te same zasady dochodzi do tej samej odpowiedzi, i czy te zasady rozchodzą się z praktyką. Nie oceniamy "
        "Ciebie; oceniamy klucz i zasady.",
        "Jak to zrobić. Czytaj tylko to, co jest na stronie. Nie dopowiadaj wiedzy z praktyki ani z przepisów spoza arkusza: jeśli zasady czegoś "
        "nie mówią, to tego nie ma. Na dole każdej strony zaznacz wszystkie działania, które zasady dopuszczają. Jeśli zasada mówi „X lub Y”, "
        "zaznacz oba. Jeśli uważasz, że zasady sprawy nie rozstrzygają, zaznacz to pole i mimo wszystko wskaż, co byś zrobił/a. Dopisz jedno "
        "zdanie, dlaczego, i swoją pewność. Ostatnia linia na stronie jest dla osób, które znają tę dziedzinę z praktyki: jeśli naprawdę "
        "zrobił(a)byś coś innego, niż wynika z zasad na stronie, napisz co.",
        "Zasady gry. Pracuj samodzielnie, bez narzędzi AI i bez konsultacji. Zacznij od PRZYKŁADU: nie ma w nim nic podchwytliwego, służy tylko "
        "oswojeniu się z formatem. Nie wracaj do poprzednich spraw po przejściu dalej. Jeśli coś w instrukcji jest "
        "niejasne, zapisz to na marginesie; to dla nas równie cenna informacja.",
        "Co z tym zrobimy. Twoje odpowiedzi trafią, zanonimizowane (inicjały), do dokumentacji badania, które zostanie opublikowane jako preprint. "
        "Porównamy je z kluczem i z odpowiedziami agentów. Chętnie pokażę Ci potem, jak wypadł klucz, agenci i inni oceniający."]),
    "en": ("Review of the answer key", [
        "Thank you for helping. You have 5 cases from a fictional bank in front of you: one warm-up (EXAMPLE) and four proper cases. Each case is "
        "one page: the task, the documents in the file and the bank's rules that govern it. Everything is synthetic; the names of companies, "
        "people and countries are invented.",
        "What this is about. We test AI agents that take decisions like these. To assess an agent you need an answer key: what the rules require "
        "in each case. Our key was written by a program, and the agents were given exactly the rules and documents you see. We want to know two "
        "things: whether a person reading the same rules reaches the same answer, and whether these rules part company with practice. We are "
        "not assessing you; we are assessing the key and the rules.",
        "How to do it. Read only what is on the page. Do not add knowledge from practice or from regulations outside the sheet: if the rules do "
        "not say it, it is not there. At the bottom of each page tick every action the rules allow. If a rule says “X or Y”, tick "
        "both. If you think the rules do not settle the case, tick that box and still say what you would do. Add one sentence on why, and your "
        "confidence.",
        "Ground rules. Work on your own, without AI tools and without consulting anyone. Start with the EXAMPLE: there is nothing tricky in it; "
        "it is only there to get used to the format. Do not go back to earlier cases once you have moved on. If anything "
        "in the instructions is unclear, write it in the margin; that is equally valuable information for us.",
        "What we will do with it. Your answers go, anonymised (initials), into the records of a study that will be published as a preprint. We "
        "will compare them with the key and with the agents' answers. I will gladly show you afterwards how the key, the agents and the other "
        "raters did."]),
}


def intro_page(lang: str) -> str:
    title, paras = INTRO[lang]
    body = "".join(f"<p class='ip'>{html.escape(p)}</p>" for p in paras)
    return f"<section class='page intro'><h1>{html.escape(title)}</h1>{body}<p class='ip sig'>Szymon P. Pepliński</p></section>"


PRACTICE = {"pl": "Jeśli w praktyce zrobił(a)byś coś innego niż wynika z zasad na tej stronie: co i dlaczego? (tylko jeśli znasz tę dziedzinę)",
            "en": "If in practice you would do something other than what the rules on this page say: what, and why? (only if you know this field)"}


def with_practice_line(h: str, lang: str) -> str:
    """One extra line under the answer block; nothing else changes on the sheet."""
    extra = f"<div class='why p2'>{html.escape(PRACTICE[lang])}<span class='line full'></span></div>"
    return h.replace("</section>", extra + "</section>")


def warmup(lang: str) -> str:
    e = GENERATORS["c5"](100019)
    it = {"n": 0, "cls": "c5", "task": e.task, "allowed": e.allowed_actions, "documents": [s.full() for s in e.sources]}
    h = with_practice_line(ms.page(it, lang), lang)
    return h.replace('<div class="code">Sprawa E00</div>', '<div class="code">PRZYKŁAD</div>').replace('<div class="code">Case E00</div>', '<div class="code">EXAMPLE</div>')


def build(lang: str) -> str:
    pages = [intro_page(lang), warmup(lang)]
    for code in CASES:
        it = ms.ITEMS[int(code[1:]) - 1]
        pages.append(with_practice_line(ms.page({**it, "n": int(code[1:])}, lang), lang))
    css = ms.CSS.replace('CSS = """', '') + (".intro{padding:22mm 24mm} .intro h1{font-size:16pt;margin:0 0 8mm} .ip{font-size:10.5pt;line-height:1.45;"
                                              "margin:0 0 4mm;text-align:justify} .sig{margin-top:10mm;color:#444} .why.p2{margin-top:1mm;font-size:8.4pt;color:#333}")
    return f"<!doctype html><html lang='{lang}'><head><meta charset='utf-8'><style>{ms.font_css()}{css}</style></head><body>{''.join(pages)}</body></html>"


def main() -> int:
    names = []
    for lang in ("pl", "en"):
        (HERE / f"pack_{lang}.html").write_text(build(lang)); names.append(f"pack_{lang}")
    js = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); await p.emulateMedia({ media: 'print' });
  for (const n of process.argv.slice(1)) {
    const f = process.env.DIR + '/' + n;
    await p.goto('file://' + f + '.html'); await p.waitForTimeout(400);
    const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => [i + 1, pg.scrollHeight - pg.clientHeight]).filter(x => x[1] > 1));
    if (over.length) console.log(n, 'OVERFLOW on pages', JSON.stringify(over));
    await p.pdf({ path: f + '.pdf', preferCSSPageSize: true, printBackground: true });
  }
  await b.close();
})();"""
    subprocess.run(["node", "-e", js, *names], check=True, env={**os.environ, "DIR": str(HERE)})
    for n in names:
        (HERE / f"{n}.html").unlink()
    return 0


if __name__ == "__main__":
    sys.exit(main())
