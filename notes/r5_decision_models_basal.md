# R5 — „Decision models” (System One / Jev / JevBench) i Basal (Remigiusz Kinas)

*Odczyt 25.10.2026 przez agenta (README i dokumentacja rkinas/basal częściowo; Fabryka, Substack, DevStock jako źródła wtórne). Szczegóły i cytaty: raport agenta w historii sesji; poniżej to, co ważne dla paperu.*

## Dlaczego to ważne (nowy wątek related work — przeoczony w rundach 1–4)

Od września 2026 istnieje kategoria **„decision models” / „System One models”**: modele, które w jednym przebiegu wybierają opcję z listy i zwracają **skalibrowane prawdopodobieństwa**, z **certyfikowanymi progami odroczenia (deferral)** do człowieka. Ekosystem: TypeSafe AI **Jev** (15.09.2026, https://typesafe.ai/blog/introducing-system-one-models-and-jev), ranking **JevBench** (Benchmark Heaven, https://benchmarkheaven.com/jev-models; BETA; Intelligence + Calibration = Capability Score), konkurenci: H2O-Lightning-31B, kettei (Sqwish), OpenAI Decisions (gpt-6-luna), Microsoft-Decision-1, Liquid AI d1, Torchcast Decision, i polski **Basal**.

To jest dokładnie **delegacja oparta na pewności** — nasz baseline B-conf / B-Shen / B-READY-conf — wdrożona jako produkt:
- Basal: progi pewności per typ pytania certyfikowane jednostronnym **Clopper–Pearson 95%** dla 1% / 5% błędu wśród zaakceptowanych decyzji (CALIBRATION.md) — ta sama maszyneria co nasza; różnica: certyfikują **trafność wyniku**, nie podstawę decyzji.
- Ich własna dokumentacja wspiera naszą tezę: „The shipped file's certificate holds on our calibration data, not on this domain” (przykład: 1% → 8% błędu na obcej domenie); preprint arXiv:2610.19619 (do weryfikacji): Jev łamie podstawowe reguły prawdopodobieństwa w 54% odpowiedzi w grupie problemów.

**Pozycjonowanie:** „Decision models certify *how often* a confident choice is right; DSA asks *whether* the choice tracks the evidence that ought to settle it.” Dodać do §2.6 i do Tabeli 1.

## Basal — fakty (do weryfikacji przed cytowaniem)

- Rodzina modeli decyzyjnych PL/EN, Apache-2.0 (NOTICE, © 2026 Remigiusz Kinas; współautor raportu Bielik 11B v3).
- Wejście: `state` (tekst/JSON) + `questions` (typy: choice, noul (tak/nie), score, multi, act (z kosztami i `max_error` → `deferred`), tool (wybór narzędzia bez argumentów)). Wyjście: opcja + rozkład prawdopodobieństw + confidence; **bez tekstu, bez wieloturowości** (historia w `state`).
- Modele (HF `Remek/...`): basal-2.0-mini (1.5B, Bielik), **basal-2.0** (4.5B, Bielik; rekomendowany), **basal-2.0-max** (11B, Bielik-PL-11B-v3), basal-omni-pico (0.8B, Qwen3.5), basal-omni-1.0-mini (4B, Gemma 4 E4B), **basal-omni-1.0-max** (12B, Gemma 4), basal-omni-1.1-max, basal-omni-1.0-ultra (31B, Gemma 4). Wersje MLX i GGUF.
- Uruchomienie na Macu: `basal-serve` (pakiet z GitHuba, tag v2.4.1), tryb **MLX** zalecany; tryb Ollama ograniczony do 4096 tokenów i 20 opcji. Omni na Macu tylko tekst.
- Słabości (dokumentacja autora): „Exact arithmetic and thresholds are a weak spot of one-pass models” — istotne dla naszych klas c2 (udziały %) i c5 (daty).
- Brak „evidence head” w 2.0/omni (spany dowodów tylko w 1.5).
- Wyniki: JevBench 24.10.2026 — omni-1.0-ultra Capability 82.1 (2. wśród open-weight); Werdykt (benchmark autora): 2.0-max 0.784, omni-1.0-max 0.823, ultra 0.879. Źródła wtórne, liczby zmienne.

## Wnioski dla pilota

1. **Basal jako osobna konfiguracja „decision model”** (protokół jednoprzebiegowy: wszystkie dokumenty epizodu w `state`, pytanie `choice` z dozwolonymi akcjami + opcja „cannot be determined → escalate”). Interwencje na dowodach działają bez zmian. Dodatkowo daje **naturalny baseline pewności**: jego własna certyfikowana deferacja vs reguła DSA — bezpośredni test tezy „Beyond Track Records” na produkcie, który deleguje na podstawie pewności.
2. Uczciwość porównania: inny protokół (bez wyszukiwania dokumentów narzędziami) — raportować osobno, nie mieszać z agentami.
3. Kandydaci: basal-2.0-max (11B, linia Bielika) i basal-omni-1.0-max (12B, Gemma 4) przez MLX.

## Polskie modele agentowe

- **Bielik 11B v3.0 Instruct** (styczeń 2026): Ollama `SpeakLeash/bielik-11b-v3.0-instruct`, tag „tools” w Ollamie → do testu połączenia.
- **PLLuM**: brak wydania 2026 i brak udokumentowanego wywoływania narzędzi; najnowsze 250801 to modele bazowe. Lokalny `PRIHLOP/PLLuM:12b` (chat 2412) — test połączenia, prawdopodobnie odpada.

## Do przeczytania (runda 5)
- TypeSafe AI, Introducing System One models and Jev (15.09.2026)
- JevBench — metodologia (Benchmark Heaven)
- arXiv:2610.19619 (naruszenia reguł prawdopodobieństwa przez Jev) — zweryfikować
- rkinas/basal: docs/MCP.md, FORMAT2.md, TASKS.md, RESULTS.md
