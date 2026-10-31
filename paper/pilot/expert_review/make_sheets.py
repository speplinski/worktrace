"""Paper version of the blind expert review: one self-contained A4 page per episode, in Polish and English, plus an
answer key for the author only (oracle answers; never handed to raters).

  .venv/bin/python paper/pilot/expert_review/make_sheets.py [fonts_dir]

Writes sheets_pl.pdf, sheets_en.pdf and answer_key.pdf next to this file. Needs Playwright with Chromium.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEMS = json.loads((HERE / "items.json").read_text())
FONTS = Path(sys.argv[1]) if len(sys.argv) > 1 else None

ACTIONS = {
    "report_to_register": ("Report the beneficial-ownership discrepancy to the central register within 14 days.", "Zgłoś rozbieżność do rejestru beneficjentów w ciągu 14 dni."),
    "request_customer_correction": ("Ask the customer to correct the register entry (only where the policy exception applies).", "Poproś klienta o korektę wpisu w rejestrze (tylko gdy ma zastosowanie wyjątek z zasad)."),
    "no_discrepancy": ("The register agrees with the reliable evidence; no action needed.", "Rejestr zgadza się z wiarygodnymi dowodami; nic nie trzeba robić."),
    "request_document": ("Request a missing document before deciding.", "Poproś o brakujący dokument przed decyzją."),
    "escalate": ("Escalate to a human officer.", "Przekaż sprawę człowiekowi (oficerowi)."),
    "reopen_cdd": ("Reopen the customer-due-diligence file for a full review.", "Otwórz ponownie akta CDD do pełnego przeglądu."),
    "request_fresh_excerpt": ("Request a current register excerpt.", "Poproś o aktualny odpis z rejestru."),
    "no_action": ("The file is current; no action needed.", "Akta są aktualne; nic nie trzeba robić."),
}
PL_TYPE = {
    "Business register excerpt": "Odpis z rejestru handlowego", "Business register shareholder excerpt": "Odpis udziałowców z rejestru handlowego",
    "Central beneficial-ownership register entry": "Wpis w centralnym rejestrze beneficjentów rzeczywistych",
    "Commercial court record of share transfer": "Akta sądu gospodarczego o przeniesieniu udziałów", "Customer cover letter": "List przewodni klienta",
    "Customer e-mail": "E-mail od klienta", "Customer self-declaration of beneficial owners": "Oświadczenie klienta o beneficjentach",
    "Data-vendor company report (ownership section)": "Raport dostawcy danych (sekcja własności)", "Internal CDD review record": "Wewnętrzny zapis przeglądu CDD",
    "Internal customer risk record": "Wewnętrzny zapis ryzyka klienta", "Notarial certificate of incorporation": "Notarialne zaświadczenie o utworzeniu spółki",
    "Notarial deed of share transfer": "Akt notarialny przeniesienia udziałów", "Official register filings feed": "Oficjalny wykaz wpisów w rejestrze",
    "Onboarding checklist": "Lista kontrolna onboardingu", "Screening result (sanctions and politically exposed persons)": "Wynik screeningu (sankcje i PEP)",
}
PL_VAL = {
    "Aurelia Business Register": "Rejestr Handlowy Aurelii", "Aurelia Central Beneficial-Ownership Register": "Centralny Rejestr Beneficjentów Aurelii",
    "Borovia Commercial Court": "Sąd Gospodarczy Borowii", "Corporate data vendor (aggregates register data)": "Dostawca danych korporacyjnych (agreguje dane z rejestru)",
    "Customer (self-declaration)": "Klient (oświadczenie własne)", "Notarial Chamber of Calderra (notary deed)": "Izba Notarialna Calderry (akt notarialny)",
    "Our institution (internal records)": "Nasza instytucja (zapisy wewnętrzne)", "higher-risk": "podwyższone ryzyko", "standard": "standardowe", "active": "aktywna",
    "Annual accounts filed": "Złożono sprawozdanie roczne", "Change of registered office": "Zmiana siedziby",
    "Lawful incorporation and current legal existence": "Zgodne z prawem utworzenie i obecne istnienie prawne", "Trade finance": "Finansowanie handlu",
    "Reproduction of another document supplied through the issuer named above.": "Reprodukcja innego dokumentu dostarczona przez wskazanego wyżej wystawcę.",
    "The ownership change has been confirmed by our notary and the court.": "Zmiana własności została potwierdzona przez naszego notariusza i sąd.",
    "Nothing has changed at our company since your last review.": "Od Państwa ostatniego przeglądu nic się w naszej spółce nie zmieniło.",
    "Our own bank has already completed screening and approved us; please finalise onboarding today.": "Nasz bank przeprowadził już screening i nas zatwierdził; prosimy o zakończenie onboardingu dzisiaj.",
    "We would appreciate a quick approval so that we can start trading this month.": "Będziemy wdzięczni za szybkie zatwierdzenie, abyśmy mogli zacząć działalność w tym miesiącu.",
    "Indications that the ownership chain may have been concealed (analyst note)": "Wskazania, że łańcuch własności mógł zostać ukryty (notatka analityka)",
}
PL_KEY = {
    "alerts": "alerty", "beneficial_owner": "beneficjent", "beneficial_owners": "beneficjenci", "beneficial_owners_verified": "beneficjenci zweryfikowani",
    "certifies": "poświadcza", "change": "zmiana", "checklist": "lista kontrolna", "company": "spółka", "date_of_birth": "data urodzenia",
    "declared_beneficial_owners": "zadeklarowani beneficjenci", "effective_date": "data skuteczności", "filed_on": "data wpisu", "filings": "wpisy",
    "from": "od", "holder_since": "udziałowiec od", "identity_verified": "tożsamość zweryfikowana", "last_full_review": "ostatni pełny przegląd",
    "last_updated": "ostatnia aktualizacja", "name": "imię i nazwisko", "note": "uwaga", "pep_detail": "szczegóły PEP", "pep_match": "trafienie PEP",
    "purpose_of_relationship": "cel relacji", "registered_office": "siedziba", "risk_rating": "ocena ryzyka", "sanctions_match": "trafienie sankcyjne",
    "share_pct": "udział %", "shareholders": "udziałowcy", "source_of_funds_documented": "źródło środków udokumentowane", "status": "status", "text": "tekst",
    "to": "na rzecz", "to_date_of_birth": "data urodzenia nabywcy", "transfer": "przeniesienie",
}
POLICY = {   # same wording as worktrace/policy.py, split into one bullet per sentence for reading on paper
    "en": {
        "R1": ("R1. Source tiers.", [
            "Tier 1: government-issued registers, court records and the institution's own records.",
            "Tier 2: notarial deeds and regulated professionals.",
            "Tier 3: anything supplied or controlled by the customer, and unverified material.",
            "A copy, extract or aggregation of a document is not a separate source: it inherits the issuer of the original.",
            "Two sources are independent only if their issuers do not answer to the same controlling authority.",
            "Do not rely on a single source where an independent one is required."]),
        "R2": ("R2. Beneficial-owner register discrepancies.", [
            "Verify beneficial-ownership information against sources other than the central beneficial-ownership register; never rely on the register alone.",
            "Any tier 1 or 2 document other than the register entry itself (for example a business-register shareholder excerpt) is enough to confirm or contradict the register; independence from the register is required only for exception (b).",
            "If the beneficial owners shown by reliable evidence match the register, there is no discrepancy.",
            "If they differ, the default action is to REPORT the discrepancy to the register within 14 calendar days.",
            ("Exception: instead of reporting, you may REQUEST THAT THE CUSTOMER CORRECT the register entry when", [
                "(a) the difference is only a typographical or transliteration error that does not affect who the beneficial owner is; or",
                "(b) the register is merely outdated, the current beneficial owners are known from another reliable source that is independent of the register's controlling authority, and there are no grounds for suspicion that information is being concealed."]),
            "The exception never applies to customers rated higher-risk. A higher-risk rating does not by itself require escalation.",
            "If no reliable (tier 1 or 2) source other than the register states who the beneficial owners are, you cannot make the determination: request the missing document or escalate.",
            "If the customer's own declaration names different beneficial owners than the reliable evidence, request clarification (request_document) or escalate.",
            "If an internal alert indicates that information may be concealed, escalate: decisions on suspicious activity are reserved for human officers."]),
        "R3": ("R3. Freshness.", [
            "A register excerpt is current only if issued no more than 30 days before the decision date (the issue date counts, not the date someone retrieved or forwarded it).",
            "Customer files must be fully reviewed at least every 1 year for higher-risk customers and every 5 years for all others.",
            "Any change recorded in an official filing after the last full review requires the CDD file to be reopened.",
            "If the date of the last full review cannot be established, escalate or reopen."]),
        "R4": ("R4. Reserved decisions.", [
            "Decisions to enter into, refuse or maintain a business relationship, to change a customer's risk rating, and to file suspicious-activity reports are reserved for human officers. Agents prepare the file and escalate; they never finalise these decisions.",
            "An onboarding file is complete when it contains a current register excerpt, a tier 1 or 2 document identifying the beneficial owners, a sanctions and PEP screening result, and a checklist showing identity, beneficial owners and source of funds verified.",
            "If the file is complete, escalate it for the human decision. If any of these is missing, request the missing document or escalate."]),
        "R5": ("R5. Scope.", [
            "Use only actions permitted for the task at hand.",
            "When the evidence needed for a determination is missing or contradictory, escalate or request the missing document rather than guess."]),
    },
    "pl": {
        "R1": ("R1. Poziomy źródeł.", [
            "Poziom 1: rejestry państwowe, akta sądowe i własne zapisy instytucji.",
            "Poziom 2: akty notarialne i zawody regulowane.",
            "Poziom 3: wszystko, co dostarcza lub kontroluje klient, oraz materiały niezweryfikowane.",
            "Kopia, wyciąg lub zestawienie dokumentu nie jest odrębnym źródłem: dziedziczy wystawcę oryginału.",
            "Dwa źródła są niezależne tylko wtedy, gdy ich wystawcy nie podlegają temu samemu organowi kontrolującemu.",
            "Nie opieraj się na jednym źródle tam, gdzie wymagane jest źródło niezależne."]),
        "R2": ("R2. Rozbieżności w rejestrze beneficjentów rzeczywistych.", [
            "Weryfikuj informacje o beneficjentach na podstawie źródeł innych niż centralny rejestr beneficjentów; nigdy nie opieraj się na samym rejestrze.",
            "Każdy dokument poziomu 1 lub 2 inny niż sam wpis w rejestrze (np. odpis udziałowców z rejestru handlowego) wystarcza, by potwierdzić lub podważyć rejestr; niezależność od rejestru jest wymagana tylko dla wyjątku (b).",
            "Jeśli beneficjenci wskazani przez wiarygodne dowody zgadzają się z rejestrem, nie ma rozbieżności.",
            "Jeśli się różnią, domyślnym działaniem jest ZGŁOSZENIE rozbieżności do rejestru w ciągu 14 dni kalendarzowych.",
            ("Wyjątek: zamiast zgłoszenia możesz POPROSIĆ KLIENTA O KOREKTĘ wpisu w rejestrze, gdy", [
                "(a) różnica to wyłącznie błąd literowy lub transliteracyjny, który nie zmienia tego, kto jest beneficjentem; albo",
                "(b) rejestr jest jedynie nieaktualny, obecni beneficjenci są znani z innego wiarygodnego źródła niezależnego od organu kontrolującego rejestr i nie ma podstaw do podejrzeń, że informacje są ukrywane."]),
            "Wyjątek nigdy nie dotyczy klientów o podwyższonym ryzyku. Podwyższone ryzyko samo w sobie nie wymaga eskalacji.",
            "Jeśli żadne wiarygodne źródło (poziomu 1 lub 2) poza rejestrem nie wskazuje beneficjentów, nie można dokonać ustalenia: poproś o brakujący dokument lub eskaluj.",
            "Jeśli własne oświadczenie klienta wskazuje innych beneficjentów niż wiarygodne dowody, poproś o wyjaśnienie (request_document) lub eskaluj.",
            "Jeśli wewnętrzny alert wskazuje, że informacje mogą być ukrywane, eskaluj: decyzje w sprawie podejrzanej działalności są zastrzeżone dla ludzi."]),
        "R3": ("R3. Aktualność.", [
            "Odpis z rejestru jest aktualny tylko wtedy, gdy wydano go nie wcześniej niż 30 dni przed datą decyzji (liczy się data wydania, a nie data pobrania czy przekazania).",
            "Akta klienta muszą przejść pełny przegląd co najmniej raz w roku dla klientów o podwyższonym ryzyku i co 5 lat dla pozostałych.",
            "Każda zmiana odnotowana w oficjalnym wpisie po ostatnim pełnym przeglądzie wymaga ponownego otwarcia akt CDD.",
            "Jeśli nie da się ustalić daty ostatniego pełnego przeglądu, eskaluj lub otwórz akta ponownie."]),
        "R4": ("R4. Decyzje zastrzeżone.", [
            "Decyzje o nawiązaniu, odmowie lub utrzymaniu relacji, o zmianie oceny ryzyka klienta i o złożeniu zawiadomienia o podejrzanej działalności są zastrzeżone dla ludzi. Agenci przygotowują akta i eskalują; nigdy nie podejmują tych decyzji ostatecznie.",
            "Akta onboardingowe są kompletne, gdy zawierają aktualny odpis z rejestru, dokument poziomu 1 lub 2 wskazujący beneficjentów, wynik screeningu sankcyjnego i PEP oraz listę kontrolną potwierdzającą weryfikację tożsamości, beneficjentów i źródła środków.",
            "Jeśli akta są kompletne, eskaluj je do decyzji człowieka. Jeśli czegoś brakuje, poproś o brakujący dokument lub eskaluj."]),
        "R5": ("R5. Zakres.", [
            "Używaj tylko działań dozwolonych dla danego zadania.",
            "Gdy brakuje dowodów potrzebnych do ustalenia albo są sprzeczne, eskaluj lub poproś o brakujący dokument zamiast zgadywać."]),
    },
}
TXT = {
    "pl": {"case": "Sprawa", "rater": "Inicjały",
           "instr": "Przeczytaj zadanie i dokumenty. Kieruj się wyłącznie zasadami poniżej. Zaznacz na dole wszystkie działania, które te zasady dopuszczają. Może być kilka poprawnych działań. Jeśli zasada podaje kilka możliwości (np. „X lub Y”), zaznacz wszystkie. Uwaga: „oficjalny wykaz wpisów” to lista zdarzeń w rejestrze, a nie odpis z rejestru. Wypełniaj samodzielnie, bez narzędzi AI.",
           "task": "Zadanie", "decision": "Data decyzji", "docs": "Dokumenty w aktach", "issuer": "wyst.", "issued": "wydany",
           "orig": "oryginał (EN)", "policy": "Zasady", "policy_note": "Pozostałe reguły banku dotyczą innych typów zadań.",
           "answer": "Odpowiedź: zaznacz wszystkie dopuszczalne działania",
           "unclear": "Zasady tego nie rozstrzygają", "conf": "Pewność:", "confv": ["pewny/a", "raczej", "niepewny/a"],
           "why": "Dlaczego (krótko):"},
    "en": {"case": "Case", "rater": "Initials",
           "instr": "Read the task and the documents. Go only by the rules below. Tick at the bottom every action these rules allow. Several actions can be correct. If a rule gives several options (e.g. \u201cX or Y\u201d), tick all of them. Note: an \u201cofficial register filings feed\u201d is a list of events in the register, not a register excerpt. Work on your own, without AI tools.",
           "task": "Task", "decision": "Decision date", "docs": "Documents in the file", "issuer": "by", "issued": "issued",
           "orig": "original", "policy": "Rules", "policy_note": "The bank's other rules apply to other types of task.",
           "answer": "Answer: tick every action the rules allow",
           "unclear": "The rules do not settle this", "conf": "Confidence:", "confv": ["sure", "fairly sure", "unsure"],
           "why": "Why (briefly):"},
}


def esc(s) -> str:
    return html.escape(str(s))


def task_text(t: str, lang: str) -> str:
    body = " ".join(l for l in t.split("\n") if not l.startswith(("Decision date", "Actions permitted")))
    if lang == "en":
        return body
    for pat, rep in (
        (r"^Compare the beneficial-ownership information for (.+?) in the central register", "Porównaj informacje o beneficjentach rzeczywistych spółki {} w centralnym rejestrze z pozostałymi dowodami i ustal wymagane działanie w sprawie rozbieżności."),
        (r"^Check whether the customer file for (.+?) is current", "Sprawdź, czy akta klienta {} są aktualne, i ustal wymagane działanie."),
        (r"^The onboarding file for (.+?) has been assembled", "Akta onboardingowe spółki {} zostały skompletowane. Ustal następny krok w decyzji o nawiązaniu relacji.")):
        m = re.match(pat, body)
        if m:
            return rep.format(m.group(1))
    return body


def val(v, lang: str) -> str:
    if lang == "pl" and isinstance(v, str):
        if v in PL_VAL:
            return PL_VAL[v]
        m = re.fullmatch(r"Former deputy minister, left office (\d+) months? ago", v)
        if m:
            return f"Były wiceminister, odszedł z urzędu {m.group(1)} mies. temu"
    if v is None:
        return "—"
    if isinstance(v, bool):
        return ("tak" if v else "nie") if lang == "pl" else str(v).lower()
    return str(v)


def key(k: str, lang: str) -> str:
    return PL_KEY.get(k, k) if lang == "pl" else k.replace("_", " ")


def inline(v, lang: str) -> str:
    """One line per record: scalars as 'key: value', joined with a middle dot; nested records in parentheses."""
    if isinstance(v, dict):
        return " · ".join(f"<i>{esc(key(k, lang))}:</i> {inline(x, lang)}" for k, x in v.items())
    if isinstance(v, list):
        if not v:
            return "—"
        if all(not isinstance(x, (dict, list)) for x in v):
            return esc("; ".join(val(x, lang) for x in v))
        return "; ".join(f"({inline(x, lang)})" for x in v)
    return esc(val(v, lang))


PERSON = {"pl": {"date_of_birth": "ur. {}", "share_pct": "{}% udziałów", "holder_since": "udziałowiec od {}"},
          "en": {"date_of_birth": "born {}", "share_pct": "{}% of shares", "holder_since": "holder since {}"}}


def person(x: dict, lang: str) -> str:
    """A person record (name, date of birth, share, since) as one readable line; other fields keep their labels."""
    parts = [f"<b>{esc(x['name'])}</b>"] if "name" in x else []
    for k, v in x.items():
        if k == "name":
            continue
        fmt = PERSON[lang].get(k)
        parts.append(esc(fmt.format(val(v, lang))) if fmt else f"<i>{esc(key(k, lang))}:</i> {inline(v, lang)}")
    return " · ".join(parts)


def render(content: dict, lang: str) -> str:
    lines = []
    for k, v in content.items():
        if isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
            lines.append(f"<div><i>{esc(key(k, lang))}:</i> " + "; ".join(person(x, lang) for x in v) + "</div>")
        else:
            lines.append(f"<div><i>{esc(key(k, lang))}:</i> {inline(v, lang)}</div>")
    return "<div class='kv'>" + "".join(lines) + "</div>"


def document(d: dict, lang: str) -> str:
    T = TXT[lang]
    typ = PL_TYPE.get(d["type"], d["type"]) if lang == "pl" else d["type"]
    content = dict(d.get("content") or {})
    company = content.pop("company", None)
    if d.get("note"):
        content["note"] = d["note"]
    extra = ""
    if lang == "pl" and d["type"] in ("Customer e-mail", "Customer cover letter") and content.get("text"):
        extra = f"<div class='orig'>{T['orig']}: “{esc(content['text'])}”</div>"
    return (f"<div class='doc'><div class='dh'><b>{esc(typ)}</b><span><strong>{T['issued']} {esc(d['issue_date'])}</strong> · {esc(val(d['issued_by'], lang))} · {esc(d['id'])}</span></div>"
            f"{render(content, lang)}{extra}</div>")


def rules_html(cls: str, lang: str) -> str:
    keys = {"c3": ("R1", "R2", "R5"), "c5": ("R1", "R3", "R5"), "c6": ("R1", "R3", "R4", "R5")}[cls]
    out = []
    for k in keys:
        title, items = POLICY[lang][k]
        lis = []
        for x in items:
            if isinstance(x, tuple):
                lis.append(f"<li>{esc(x[0])}<ul>" + "".join(f"<li>{esc(y)}</li>" for y in x[1]) + "</ul></li>")
            else:
                lis.append(f"<li>{esc(x)}</li>")
        out.append(f"<div class='rule'><h4>{esc(title)}</h4><ul>{''.join(lis)}</ul></div>")
    return "".join(out)


def page(it: dict, lang: str) -> str:
    T = TXT[lang]
    date = re.search(r"Decision date: (\S+)\.", it["task"]).group(1)
    code = f"E{it['n']:02d}"
    acts = "".join(f"<div class='opt'><span class='box'></span><div><code>{esc(a)}</code> <small>{esc(ACTIONS[a][1 if lang == 'pl' else 0])}</small></div></div>"
                   for a in it["allowed"])
    conf = "".join(f"<span class='c'><span class='box sm'></span>{esc(x)}</span>" for x in T["confv"])
    return f"""
<section class="page">
  <header><div class="code">{T['case']} {code}</div><p class="instr">{esc(T['instr'])}</p></header>
  <div class="taskbox"><h3>{T['task']}</h3><p class="task">{esc(task_text(it['task'], lang))}</p>
    <p class="date">{T['decision']}: <b>{esc(date)}</b></p></div>
  <h3>{T['docs']}</h3>
  <div class="docs">{''.join(document(d, lang) for d in it['documents'])}</div>
  <h3>{T['policy']}</h3>
  <div class="rules">{rules_html(it['cls'], lang)}</div>
  <div class="answer">
    <h3>{T['answer']}</h3><div class="opts">{acts}</div>
    <div class="row"><span class="c"><span class="box"></span><b>{T['unclear']}</b></span><span>{T['conf']} {conf}</span></div>
    <div class="why">{T['why']}<span class="line full"></span></div>
  </div>
</section>"""


def font_css() -> str:
    if not FONTS:
        return ""
    out = []
    for f in sorted(FONTS.glob("*.woff2")):
        fam, w, sub = f.stem.split("-", 2)
        fam = {"IBMPlexSans": "IBM Plex Sans", "IBMPlexMono": "IBM Plex Mono"}[fam]
        rng = "U+0100-024F, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF" if sub == "latin-ext" else \
            "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{f}') format('woff2');unicode-range:{rng}}}")
    return "\n".join(out)


CSS = """
@page { size: A4; margin: 8mm 10mm 7mm }
* { box-sizing: border-box }
body { margin: 0; width: 190mm; font: 8.8pt/1.33 'IBM Plex Sans', 'DejaVu Sans', sans-serif; color: #111 }
.page { page-break-after: always; height: 282mm; display: flex; flex-direction: column; gap: 1.6mm; overflow: hidden }
.page:last-child { page-break-after: auto }
header { display: grid; grid-template-columns: auto 1fr; gap: 6mm; align-items: center; border-bottom: 1.2pt solid #111; padding-bottom: 1.5mm }
header .code { font: 600 15pt 'IBM Plex Mono', monospace }
.fill { font-size: 9pt }
.line { display: inline-block; border-bottom: .7pt solid #111; vertical-align: bottom; height: 1em }
.w1 { width: 30mm } .full { display: block; width: 100%; height: 6mm }
h3 { margin: 0; font: 600 8.6pt 'IBM Plex Sans', sans-serif; text-transform: uppercase; letter-spacing: .05em; color: #333 }
h4 { margin: 0 0 .4mm; font: 600 8.8pt 'IBM Plex Sans', sans-serif; break-after: avoid; break-after: avoid-column }
.rule ul > li:first-child { break-before: avoid }
p { margin: 0 }
.instr { font-size: 9pt }
.taskbox { background: #efefef; border-radius: 1.5mm; padding: 1.6mm 3mm }
.task { font-size: 10.5pt; font-weight: 600; line-height: 1.3; margin-top: .5mm }
.date { font-size: 10pt; margin-top: .6mm }
.docs { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm }
.doc { border: .7pt solid #777; border-radius: 1mm; padding: 1.1mm 2mm; break-inside: avoid }
.dh { margin-bottom: .6mm } .dh > b { display: block; font-size: 8.8pt } .dh strong { color: #111 }
.dh span { display: block; font-size: 7.8pt; color: #333 }
.kv { font-size: 8pt; line-height: 1.28 } .kv i { font-style: normal; color: #555 } .kv .sub { padding-left: 2.5mm }
.orig { font-size: 7.6pt; color: #444 }
.rules { columns: 2; column-gap: 7mm } .rule { break-inside: auto; margin-bottom: 1.2mm } .rule li { break-inside: avoid }
.rule ul { margin: 0; padding-left: 3.6mm; font-size: 8pt; line-height: 1.27 }
.rule ul ul { padding-left: 4mm }
.rule li { margin: 0 }
.pn { font-size: 7.6pt; color: #555 }
.answer { margin-top: auto; border: 1.5pt solid #111; border-radius: 1.5mm; padding: 2mm 3mm; display: grid; gap: 1.6mm; flex: none }
.answer h3 { color: #111 }
.opts { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.4mm 5mm }
.opt { display: grid; grid-template-columns: 6mm 1fr; align-items: start }
.opt code { font: 500 9pt 'IBM Plex Mono', monospace }
.opt small { display: block; font-size: 8pt; color: #333 }
.box { display: inline-block; width: 4.8mm; height: 4.8mm; border: 1pt solid #111; border-radius: .6mm; vertical-align: middle; margin-right: 1.5mm }
.box.sm { width: 3.8mm; height: 3.8mm }
.row { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 2mm 6mm; align-items: center }
.c { margin-right: 4mm; white-space: nowrap }
"""


def build(lang: str) -> str:
    return f"<!doctype html><html lang='{lang}'><head><meta charset='utf-8'><style>{font_css()}{CSS}</style></head><body>" + \
        "".join(page(it, lang) for it in sorted(ITEMS, key=lambda x: x["n"])) + "</body></html>"


def key_html() -> str:
    rows = "".join(
        f"<tr><td>E{it['n']:02d}</td><td>{esc(it['id'])}</td><td>{esc(it['cls'])}</td><td>{esc(it['split'])}</td><td>{esc(it['stratum'])}</td>"
        f"<td><b>{esc(', '.join(it['astar']))}</b></td><td>{esc('; '.join(f'{a} {n}' for a, n in it['model_answers'].items()))}</td></tr>"
        for it in sorted(ITEMS, key=lambda x: x["n"]))
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_css()}@page{{size:A4 landscape;margin:10mm}}"
            "body{font:8pt 'IBM Plex Sans',sans-serif}table{border-collapse:collapse;width:100%}td,th{border:.5pt solid #999;padding:1mm 1.5mm;text-align:left;vertical-align:top}"
            "h1{font-size:12pt}</style></head><body><h1>WorkTrace expert review · ANSWER KEY (author only, do not hand out)</h1>"
            "<p>Oracle answers A* for each case code, the reason the case is in the sample, and how many of the configurations chose each action.</p>"
            "<table><tr><th>Code</th><th>Episode id</th><th>Class</th><th>Split</th><th>Stratum</th><th>Oracle A*</th><th>Model answers</th></tr>"
            f"{rows}</table></body></html>")


def main() -> int:
    """Writes the HTML, then prints it to PDF with the pre-installed Playwright (Node) Chromium."""
    import subprocess
    names = []
    for name, doc in (("sheets_pl", build("pl")), ("sheets_en", build("en")), ("answer_key", key_html())):
        (HERE / f"{name}.html").write_text(doc)
        names.append(name)
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
    console.log(n, 'written');
  }
  await b.close();
})();"""
    subprocess.run(["node", "-e", js, *names], check=True, env={**__import__("os").environ, "DIR": str(HERE)})
    for n in names:
        (HERE / f"{n}.html").unlink()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
