"""Convert the Markdown drafts (paper/draft/*.md) into LaTeX sections and compile the PDF.

Usage: python3 paper/latex/build.py            # writes paper/latex/sections/*.tex and builds paper/latex/main.pdf
       python3 paper/latex/build.py --arxiv    # also packs paper/latex/arxiv_submission.tar.gz for arXiv
Needs pandoc and a TeX distribution with acmart. Edit the Markdown, never the generated .tex files.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRAFT = HERE.parent / "draft"
OUT = HERE / "sections"

# Parenthetical form used in the drafts -> BibTeX key (paper/references.bib). Narrative forms are derived below.
CITES = {
    "Castelfranchi & Falcone, 1998": "castelfranchi1998delegation", "Castelfranchi & Falcone, 2000": "castelfranchi2000trust",
    "Falcone & Castelfranchi, 2008": "falcone2008generalizing", "Falcone & Castelfranchi, 2010": "falcone2010transitivity",
    "Venanzi et al., 2011": "venanzi2011facing", "Burnett et al., 2010": "burnett2010bootstrapping",
    "Soh et al., 2020": "soh2020multitask", "Scerri et al., 2002": "scerri2002adjustable", "Lee & See, 2004": "lee2004trust",
    "Fischer & Ravizza, 1998": "fischer1998responsibility", "Santoni de Sio & van den Hoven, 2018": "santonidesio2018mhc",
    "Mecacci & Santoni de Sio, 2020": "mecacci2020mhc", "Veluwenkamp, 2022": "veluwenkamp2022reasons",
    "Turpin et al., 2023": "turpin2023unfaithful", "Lanham et al., 2023": "lanham2023measuring",
    "Atanasova et al., 2023": "atanasova2023faithfulness", "Matton et al., 2025": "matton2025walk",
    "Gao et al., 2026a": "gao2026graphoftrace", "Gao et al., 2026b": "gao2026copies",
    "Wang et al., 2026a": "wang2026survey", "Wang et al., 2026b": "wang2026graphecho",
    "Pandey et al., 2026a": "pandey2026certified", "Pandey et al., 2026b": "pandey2026local", "W3C, 2013": "w3c2013provo",
    "Clopper & Pearson, 1934": "clopper1934confidence", "Dodge, 1943": "dodge1943sampling",
    "El-Yaniv & Wiener, 2010": "elyaniv2010foundations", "Geifman & El-Yaniv, 2017": "geifman2017selective",
    "Angelopoulos et al., 2025": "angelopoulos2025ltt", "Waudby-Smith & Ramdas, 2024": "waudbysmith2024betting",
    "Podkopaev & Ramdas, 2022": "podkopaev2022tracking", "Madras et al., 2018": "madras2018predict",
    "Mozannar & Sontag, 2020": "mozannar2020consistent", "FSB, 2026": "fsb2026sound", "Rusu, 2026": "rusu2026fca",
    "Needham et al., 2025": "needham2025evaluated", "Shao et al., 2025": "shao2025seekbench",
    "Khanzadeh, 2026": "khanzadeh2026ariadne", "Tomašev et al., 2026": "tomasev2026delegation",
    "Suryana et al., 2026": "suryana2026caredrive", "Cao et al., 2026": "cao2026pae", "Cao, 2026": "cao2026loopholes", "Yuan et al., 2026": "yuan2026sovereign",
    "Fernandez, 2026": "fernandez2026acp", "Nian et al., 2026": "nian2026auditable", "Trinh et al., 2026": "trinh2026hilbench",
    "Ríos-García et al., 2026": "riosgarcia2026scientists", "Solozobov, 2026": "solozobov2026demm",
    "Sahoo et al., 2026": "sahoo2026agentlens", "Khosravi & Huo, 2026": "khosravi2026csa",
    "Weber & Taneja, 2026": "weber2026apprentice", "Azevedo, 2026": "azevedo2026minimal",
    "Opoku & Banahene, 2026": "opoku2026toolchain",
    "European Parliament and Council, 2024": "eu2024amlr",
    "Knight & Leveson, 1986": "knight1986independence", "Barr et al., 2015": "barr2015oracle", "Segura et al., 2016": "segura2016metamorphic",
    "Steegen et al., 2016": "steegen2016multiverse", "Ribeiro et al., 2020": "ribeiro2020checklist", "Gardner et al., 2020": "gardner2020contrast",
    "Kaushik et al., 2020": "kaushik2020cad", "McCoy et al., 2019": "mccoy2019right", "Geirhos et al., 2020": "geirhos2020shortcut",
    "Northcutt et al., 2021": "northcutt2021label", "Plank, 2022": "plank2022variation", "Jacobs & Wallach, 2021": "jacobs2021measurement",
    "Merigoux et al., 2021": "merigoux2021catala", "European Banking Authority, 2021": "eba2021riskfactors", "Financial Action Task Force, 2026": "fatf2026recommendations", "Flynt, 2026": "flynt2026groundeval", "Li & Zhao, 2026": "li2026actionalignment",
    "Liu et al., 2026": "liu2026agentabstain", "Chang & Chang, 2026": "chang2026trace", "Liao, 2026": "liao2026provenance",
    "Zhang & Zhang, 2026": "zhang2026earned", "Rahman et al., 2026": "rahman2026rolestratified", "Shen, 2026": "shen2026provable",
    "Kim et al., 2026": "kim2026ledger", "Du & Chen, 2026": "du2026audita", "Chatrath et al., 2026": "chatrath2026ready",
    "Pang et al., 2026": "pang2026dnative", "Pawar et al., 2026": "pawar2026necessary", "Mahale, 2026": "mahale2026causal",
    "Bi et al., 2026": "bi2026nautil", "Hsu et al., 2026": "hsu2026arp", "Angelidis et al., 2026": "angelidis2026tba",
    "Yu et al., 2026": "yu2026cxbench", "Jevons, 1865": "jevons1865coal", "Kinas, 2026": "kinas2026basal", "Microsoft, 2026": "microsoft2026agentssdk", "GitHub, 2026": "github2026copilotsdk", "Liquid AI, 2026": "liquid2026d1", "Shukla et al., 2026": "shukla2026hedwig", "DosSantos DiSorbo & Ju, 2026": "dossantos2026escalate",
}


def narrative(p: str) -> str:
    """'Gao et al., 2026a' -> 'Gao et al. (2026a)'; 'A & B, 2000' -> 'A and B (2000)'."""
    names, year = p.rsplit(", ", 1)
    return f"{names.replace(' & ', ' and ')} ({year})"


def convert_citations(md: str) -> tuple[str, set[str]]:
    used: set[str] = set()
    md = md.replace("Castelfranchi & Falcone, 1998; 2000", "@@castelfranchi1998delegation,castelfranchi2000trust@@")
    used |= {"castelfranchi1998delegation", "castelfranchi2000trust"} if "@@castelfranchi1998" in md else set()
    for p, k in sorted(CITES.items(), key=lambda x: -len(x[0])):
        n = narrative(p)
        if n in md:
            md = md.replace(n, f"##{k}##"); used.add(k)
        if p in md:
            md = re.sub(re.escape(p) + r"(?![0-9a-z])", f"@@{k}@@", md); used.add(k)
    # placeholder tokens survive pandoc as plain text; turned into \citet / \citealp after conversion
    return md, used


def clean(md: str) -> str:
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = re.sub(r"\n---\n+## References.*", "\n", md, flags=re.S)       # per-section key lists
    md = re.sub(r"\n## References used.*", "\n", md, flags=re.S)
    md = re.sub(r"^\*(Draft v\d|Final data).*?\*\s*$", "", md, flags=re.M)           # draft banner
    md = re.sub(r"^# (\d+\.?\s+)?", "# ", md, flags=re.M)               # drop manual section numbers
    md = re.sub(r"^## \d+\.\d+\s+", "## ", md, flags=re.M)
    md = re.sub(r"^\*\*\d+\.\d+\s+", "**", md, flags=re.M)              # run-in paragraph headings
    # table titles ("## Table 1 — X" or "**Table 3.** X") become captions of the next table
    md = re.sub(r"^## Table \d+\s*[—-]\s*(.*)$", r"QQCAPQQ\1QQENDQQ", md, flags=re.M)
    md = re.sub(r"^\*\*Table \d+\.\*\*\s*(.*)$", r"QQCAPQQ\1QQENDQQ", md, flags=re.M)
    return md


def content_widths(tex_t: str) -> str:
    """pandoc gives wrapped columns equal widths (25% each for four columns). Re-weight each p{} column by the
    average amount of text in its data cells, so a narrow '#' column does not take a quarter of the page."""
    n = tex_t.count("\\real{")
    if n < 2 or "\\midrule\\noalign{}" not in tex_t:
        return tex_t
    # longtable puts the foot (\\bottomrule) before the data rows, so drop it rather than split on it
    data = tex_t.split("\\midrule\\noalign{}", 1)[1].replace("\\bottomrule\\noalign{}", "")
    lens = [[] for _ in range(n)]
    for row in data.split("\\\\"):
        cells = re.split(r"(?<!\\)&", row)
        if len(cells) != n:
            continue
        for i, c in enumerate(cells):
            plain = re.sub(r"\\[a-zA-Z]+\*?|[{}$]", "", c).strip()
            lens[i].append(len(plain))
    if not all(lens):
        return tex_t
    w = [max(4.0, sum(l) / len(l)) for l in lens]
    w = [x / sum(w) for x in w]
    it = iter(w)
    return re.sub(r"\\real\{[0-9.]+\}", lambda _: "\\real{%.4f}" % next(it), tex_t)


def tables_twocolumn(tex: str) -> str:
    """pandoc emits longtable, which acmart's two-column layout rejects: turn each into table*/tabular."""
    def repl(m):
        body = m.group(2)
        body = re.sub(r"\\caption\{.*?\}\\tabularnewline\n", "", body, flags=re.S)
        body = re.sub(r"\\end(first)?head\n|\\endlastfoot\n|\\endfoot\n", "", body)
        # keep only the first header block (pandoc repeats it for continuation pages)
        parts = body.split("\\midrule\\noalign{}")
        if len(parts) > 2:
            body = parts[0] + "\\midrule\\noalign{}" + parts[-1]
        body = body.replace("\\bottomrule\\noalign{}", "")
        tex_t = (m.group(1) + body).replace("\\columnwidth", "\\textwidth")
        return ("\\begin{table*}\n\\small\n\\begin{tabular}" + content_widths(tex_t) + "\\bottomrule\n\\end{tabular}\n\\end{table*}")
    return re.sub(r"\\begin\{longtable\}\[\]((?:\{[^\n]*\}))(.*?)\\end\{longtable\}", repl, tex, flags=re.S)


def attach_table_notes(tex: str) -> str:
    """A 'Notes to Table N.' paragraph and the footnotes that follow a table float move inside the float, so that
    they are typeset under the table instead of wherever the text around the float lands."""
    m = re.search(r"\\end\{tabular\}\n\\end\{table\*\}\n\n(Notes to Table \d+\..*?)\n\n(?=\\begin\{center\}\\rule)", tex, flags=re.S)
    if not m:
        return tex
    notes = m.group(1).replace("\n\n", "\\par ")
    block = "\\end{tabular}\n\\vspace{3pt}\\par\\begingroup\\footnotesize " + notes + "\\par\\endgroup\n\\end{table*}\n\n"
    return tex[:m.start()] + block + tex[m.end():]


def build_section(md_path: Path) -> set[str]:
    md, used = convert_citations(clean(md_path.read_text()))
    tex = subprocess.run(["pandoc", "-f", "markdown+tex_math_dollars-auto_identifiers", "-t", "latex",
                          "--top-level-division=section", "--columns=120"],
                         input=md, capture_output=True, text=True, check=True).stdout
    tex = re.sub(r"\\#\\#([a-z0-9]+)\\#\\#", r"\\citet{\1}", tex)
    tex = re.sub(r"@@([a-z0-9,]+)@@", r"\\citealp{\1}", tex)
    tex = tables_twocolumn(tex)
    # move each caption marker into the next table* float
    def cap(m):
        return m.group(2).replace("\\begin{table*}\n", "\\begin{table*}\n\\caption{" + m.group(1).strip() + "}\n", 1)
    tex = re.sub(r"QQCAPQQ(.*?)QQENDQQ\n*(.*?\\begin\{table\*\}\n)", cap, tex, flags=re.S)
    tex = attach_table_notes(tex)
    tex = tex.replace("\\tightlist\n", "").replace("\\mathbb{1}", "\\mathds{1}")
    # markdown "---" separators mark working sections in the drafts; they are not rules in print
    tex = tex.replace("\\begin{center}\\rule{0.5\\linewidth}{0.5pt}\\end{center}\n", "")
    (OUT / (md_path.stem + ".tex")).write_text(f"% GENERATED from paper/draft/{md_path.name} by build.py — do not edit\n" + tex)
    return used


def statements() -> None:
    fm = (DRAFT / "00_front_matter.md").read_text()
    keep = [l for l in fm.splitlines() if l.startswith("**Statement") or l.startswith("**Code") or l.startswith("**Use of AI")]
    md = "\n\n".join(re.sub(r"\*\*(.+?)\*\*", r"**\1**", l) for l in keep)
    tex = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex"], input=md, capture_output=True, text=True, check=True).stdout
    (OUT / "00_statements.tex").write_text("% GENERATED from paper/draft/00_front_matter.md — do not edit\n" + tex)
    ab = next((l for l in fm.splitlines() if l.startswith("**Abstract:**")), "").replace("**Abstract:**", "", 1).strip()
    ab_tex = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex"], input=ab, capture_output=True, text=True,
                            check=True).stdout if ab else "TODO: abstract.\n"
    (OUT / "00_abstract.tex").write_text("% GENERATED from paper/draft/00_front_matter.md — do not edit\n" + ab_tex)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    used: set[str] = set()
    for f in sorted(DRAFT.glob("[01][0-9]_*.md")):
        if f.name.startswith("00_"):
            continue
        used |= build_section(f)
    statements()
    keys = set(re.findall(r"^@\w+\{([^,]+),", (HERE.parent / "references.bib").read_text(), re.M))
    missing = sorted(used - keys)
    if missing:
        print("Citation keys missing from references.bib:", missing)
        return 1
    r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                       cwd=HERE, capture_output=True, text=True, errors="replace")
    log = (HERE / "main.log").read_text(errors="ignore") if (HERE / "main.log").exists() else ""
    undefined = sorted(set(re.findall(r"Citation `([^']+)' .*undefined", log)))
    pages = re.search(r"Output written on main.pdf \((\d+) pages", log)
    print(f"latexmk exit {r.returncode}; pages: {pages.group(1) if pages else '?'}; undefined citations: {undefined or 'none'}")
    if r.returncode != 0:
        print(r.stdout[-3000:])
    elif "--arxiv" in sys.argv:
        arxiv_bundle()
    return r.returncode


def arxiv_bundle() -> None:
    """Pack what arXiv needs: main.tex, unicode.tex, sections/*.tex and main.bbl (arXiv uses the .bbl, not the .bib).
    acmart and the fonts are part of TeX Live on arXiv. Test-compiles the bundle without BibTeX first."""
    import shutil, tarfile, tempfile
    files = ["main.tex", "unicode.tex", "main.bbl"] + [f"sections/{p.name}" for p in sorted(OUT.glob("*.tex"))]
    with tempfile.TemporaryDirectory() as tmp:
        for f in files:
            (Path(tmp) / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(HERE / f, Path(tmp) / f)
        for _ in range(2):
            t = subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], cwd=tmp,
                               capture_output=True, text=True, errors="replace")
        log = (Path(tmp) / "main.log").read_text(errors="ignore")
        bad = re.findall(r"Citation `([^']+)' .*undefined", log)
        print(f"arXiv bundle test compile: exit {t.returncode}; undefined citations: {sorted(set(bad)) or 'none'}")
    out = HERE / "arxiv_submission.tar.gz"
    with tarfile.open(out, "w:gz") as tar:
        for f in files:
            tar.add(HERE / f, arcname=f)
    print(f"arXiv bundle: {out} ({len(files)} files)")


if __name__ == "__main__":
    sys.exit(main())
