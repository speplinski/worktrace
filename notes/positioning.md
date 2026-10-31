# Mapa pozycjonowania — wersja 3 (po 3. rundzie lektury, 25.10.2026)

Synteza 27 notatek: runda 1 (`ledger.md` … `survey_traces_to_trust.md`), runda 2 (`r2_*.md`), runda 3 (`r3_*.md`). Wersje 1 i 2 są w historii gita. Tytuł: *Beyond Track Records: Decision-Structured Agency as a Basis for Delegating Autonomy to AI Agents*.

---

## 1. Werdykt

Nikt nie robi naraz: **autonomia per (konfiguracja agenta × klasa decyzji), przyznawana na podstawie interwencyjnie zmierzonego profilu tego, jak decyzje agenta zależą od dowodów, odwołalna na podstawie danych, porównana empirycznie z regułami opartymi na historii wyników, pewności, akceptacjach i ocenie śladu.**

Prawie każdy *element* osobno już istnieje. Paper stoi na **kombinacji**, na **rodzaju dowodu, na którym opiera się delegację**, oraz na **teście trafności predykcyjnej**. Tego nie robi nikt.

## 2. Ostateczny kształt wkładów

### W1. Konstrukt: decision-structured agency (DSA)
- **Definicja robocza:** właściwość pary (konfiguracja agenta, klasa decyzji): regularna *receptywność* i *reaktywność* decyzji na dowody rozstrzygające (Fischer i Ravizza, reasons-responsiveness; przez Meaningful Human Control), trzymanie się zakresu uprawnień, trafna eskalacja i poprawna rewizja po korekcie. Mierzona interwencjami na zewnętrznych dowodach, z prawdą z generatora o tym, który dowód rozstrzyga i jak wygląda nadmiarowość, ocenianymi względem podstaw zadeklarowanych przez agenta.
- **Nowe:** termin; połączenie wymiarów w jeden profil per klasa decyzji; pomiar interwencyjny z prawdą o strukturze dowodów; użycie do delegacji.
- **Nie nowe (cytować jako składowe):** behawioralny test reasons-responsiveness modelu fundamentowego, w tym zmiana faktów decyzji (CARE-Drive, 2602.15645; jednoetapowy, bez prawdy o dowodzie rozstrzygającym, bez eskalacji i delegacji); epistemic competence (SeekBench); epistemic agency (Reflection-Bench); judgment / kiedy pytać (HiL-Bench); progi eskalacji (Act or Escalate); restraint (Action Alignment, 2606.28739); epistemic honesty, verifiability (Trust Before Autonomy); boundary detection, escalation (Agent Reliability Profiles); paired act/abstain z prawdą z konstrukcji (AgentAbstain).
- **DSA jako pomiar wymagań** stawianych agentom przez DeepMind (Intelligent AI Delegation), którzy ich nie mierzą.

### W2. Reguła delegacji oparta na DSA
- Certyfikat per klasa: P(działanie nieuzasadnione | autonomiczne, c) ≤ α_c, łącznie dla wszystkich klas. Działanie nieuzasadnione = złe działanie albo dobre na złej podstawie, gdzie złą podstawę **wykrywają interwencje**, a nie sędzia LLM ani etykieta audytu.
- **Sztywny sufit uprawnień** (Earned Authority): autonomię poszerzamy tylko pod nim; podnieść go może tylko człowiek. Certyfikat wydaje niezależny ewaluator; jest związany z odciskiem konfiguracji agenta (model, prompt, narzędzia), wygasa i jest zawieszany przy każdej zmianie.
- **Klasy decyzji:** wymagania R_c (decydują o przenoszeniu profilu, tylko do klas o mniejszych wymaganiach) i parametry ryzyka K_c (stawka, odwracalność, zastrzeżenie prawne; ustalają α_c). Klasy zastrzeżone prawnie (AMLR art. 76(5)(b)) zawsze eskalują. Klasy oznaczone klasami działań Agent Reliability Profiles i osiami weryfikowalność / odwracalność / krytyczność (DeepMind).
- **Odebranie per klasa** istnieje już na podstawie danych o wynikach (Digital Apprentice jawnie, Minimal Oversight niejawnie; CSA tylko w zaplanowanych terminach). **Nasze:** odebranie wywołane nieudanymi testami interwencyjnymi, z histerezą, oraz ponowne testy we wszystkich klasach, które dzielą wymaganie, w którym nastąpiła porażka.
- **Opcje werdyktu:** proceed / proceed narrowed / escalate / refuse.
- **Statystyka cytowana, nie nasza:** Learn-then-Test, Clopper–Pearson + Bonferroni i łączenie rzadkich klas (Role-Stratified CRC), e-procesy (Podkopaev i Ramdas; CSA), plan CSP-1 (Dodge 1943) jako klasyczny precedens cyklu przyznanie–audyt–odebranie.
- **Formalnie cytowane:** ToolChain-CRC już dowodzi, że kalibracja na samym wyniku nie kontroluje złej podstawy. Nasze jest *jak* mierzymy podstawę (zależność interwencyjna, a nie etykieta dowodu). Te dwie miary rozjeżdżają się w obie strony.

### W3. Test trafności predykcyjnej (empiryczny rdzeń)
- **Kryterium niezależne od pomiaru DSA:** błędy wynikowe decyzji autonomicznych na odłożonych epizodach z przesunięciem dowodów, przy tym samym zakresie autonomii. Wstępnie zarejestrowane.
- **Baseline'y (ten sam silnik certyfikacji dla wszystkich):**
  - B-OO: czysta historia wyników per klasa
  - B-Shen: pewność + Clopper–Pearson (Shen 2026)
  - B-READY-conf i **B-READY-proc** (ta sama reguła, złą podstawę ocenia sędzia LLM; **kluczowa ablacja: sędzia vs interwencje**)
  - B-trace-judge: sędzia LLM ocenia „jasność i rzetelność” deklarowanych podstaw (propozycja DeepMind)
  - B-Hedwig (akceptacje), B-DigitalApprentice (odsetek poprawek), B-SovereignOS (audyty wyniku), B-MinimalOversight (skuteczność per klasa), B-ACP (liczniki historii)
  - B-TBA: pierwsza bramka Trust Before Autonomy (powtarzalność + wstrzymanie się przy usunięciu jedynego źródła). **Jeśli go nie pokonamy, wkład zawęża się do interwencji odpornych na nadmiarowość.**
  - **B-Pandey:** certyfikator kworum źródeł z odrębnych domen kontroli (2609.34245; testowany na syntetycznych płatnościach za faktury, dane sankcyjne tylko do rozkładów). Prawdopodobnie remis lub przegrana w klasach (i) i (iv), co rejestrujemy z góry; nasza przewaga oczekiwana w klasach (ii), (iii), (v).
- **Wyniki dodatkowe:** obciążenie recenzenta przy docelowej niezawodności, próg opłacalności dokładności recenzenta (jak w READY), krzywa ryzyko–zakres.
- **H1′:** nakładanie się trzech detektorów (wynik, audyt procedury w stylu CXBench/PAE, interwencje); główna wielkość: odsetek błędów podstawy przepuszczanych przez audyt procedury.
- **Trafność konstruktu:** agenci z celowo wbudowanymi deficytami; DSA warunkowane na tym, co agent rozwiązuje przy pełnej informacji (żeby DSA nie było zamaskowaną ogólną zdolnością); rozkład wariancji (agent / klasa / ziarno); ablacja klas: wymagania vs naiwne łączenie vs podobieństwo opisów.

### Rama, nie wkład
Pomost do teorii delegacji MAS: zaufanie Trust(X, Y, C, τ, g) per zadanie i kontekst, przenoszenie przez dopasowanie wymagań, aktualizacja tylko o porażki przypisane agentowi (Castelfranchi i Falcone), transfer kontroli (Scerri), appropriate reliance (Lee i See). DeepMind jako koncepcyjny poprzednik; my: pierwsza operacjonalizacja z testem.

## 3. Instrument pomiarowy: interwencje (cytować operatory)
- Operatory „usuń / tylko / odwróć / dodaj źródło” istnieją osobno: Pawar, Matton, Turpin, Atanasova, AgentAbstain, Liao, „Copies or Sources?”, GraphEcho, Pandey; przedeterminowanie: AUDITA (Halpern–Pearl, NESS).
- **Nasze:** złożenie (dodaj niezależne Y, potem usuń X), żeby dla pojedynczej decyzji odróżnić nadmiarowość od nieużycia; ocena względem deklarowanych podstaw; klasyfikacja każdej niezmienionej decyzji (nadmiarowość / znoszenie / brak reakcji); prawda o strukturze nadmiarowości z generatora.
- **Projekt:** wstępnie zarejestrowany katalog interwencji; kontrola semantycznej ważności i odsetka no-opów; ramiona placebo i pozorowane; kontrole kopia / wskaźnik / wypełnienie; „niezależne” = brak wspólnej instytucji kontrolnej (liczone per instytucja, nie per pochodzenie rekordu; Pandey, tab. 5); 3–5 przebiegów na epizod; porównania rozkładów, nie pojedynczych przebiegów; fałszywy graf podstaw (ta sama liczba, przepięte wskazania); audyt generatora pod kątem skrótów pozycyjnych i formatowych (CatchBench: F1 = 1,000 z samej kolejności deklaracji); sprawdzenie, czy agent nie odróżnia epizodów testowych od prawdziwych.

## 4. Domeny
- **Weryfikacja kontrahenta (AML, UE):** reguły z AMLR/EBA/FATF; flagowa interwencja z AMLR art. 24(2)(b). Odróżnić od CXBench (Reg E, procedura) i Pandey (sankcje, certyfikator wielodomenowy; baseline). Nigdy nie twierdzić zgodności z przepisami.
- **Auditable Design:** decyzje ocenne.

## 5. Nazewnictwo
- Unikać: „earned autonomy”, „graduated autonomy”, „readiness gates”, „certified autonomy”, „right for the right reasons”, „counterfactual replay”, „load-bearing”, „autonomy level”, „drift”, „ADAS”, „DNative”.
- Pisać: „agent-declared grounds” (nie „declared”, bo GRADE używa go inaczej); „evidence interventions”; „reliability allocation beneath a fixed ceiling” (nigdy „gwarancja bezpieczeństwa”).
- TRACE zawsze z arXiv:2607.12480.

## 6. Ryzyka
1. **DSA okaże się zamaskowaną ogólną zdolnością** (zdolności latentne często śledzą rozmiar modelu). Ochrona: deficyty wbudowane celowo, warunkowanie na rozwiązywalności, trafność rozróżniająca względem skuteczności.
2. **DSA nie różnicuje modeli** (struktura rozumowania bywa prawie identyczna między modelami). Wtedy H3 słabnie; raportować uczciwie.
3. **Przepaść generator → rzeczywistość:** gwarancje dotyczą tylko wygenerowanych epizodów. Napisać wprost.
4. **Tłok w domenie bankowej:** Pandey, CXBench, Agent Reliability Profiles (MLCommons, finanse), narzędzie płatnicze Solozobova.
5. **Szybko rosnąca literatura:** przed złożeniem sprawdzić ponownie: grupę Yue Zhao (USC), Solozobova, serię Fernandeza (P11), READY w wersji ICLR.

## 7. Do przeczytania przed pisaniem odpowiednich sekcji
- **Przed konspektem:** Minimal Oversight (2606.15563, „sensitivity-based intervention”, „masking”); Pandey i in. (2609.34245); CARE-Drive (2602.15645) w całości.
- **Przed sekcją DSA:** Rabanser i in. (2602.16666), HiL-Bench (2604.09408), Act or Escalate (2604.08588), Nautil (2610.03190); książka Fischera i Ravizzy (cytaty).
- **Przed sekcją o kosztach:** Zhou i in. CHI'26 (częstość potwierdzeń).
- **Uzupełniająco:** EDGE (2609.01360), FORTIS (2605.09163), Hu i in. (2605.30169), Griffiths 2005 (AAMAS), Lubars i Tan 2019, Lee i Tok 2025 (FAccT), Mao i in. 2023, Venanzi i in. IJCAI 2011, Soh i in. IJRR 2019, Burnett i in. AAMAS 2010.
- **Biblioteka:** Castelfranchi i Falcone 2010, §6.6.

## 8. Poprawki po rundzie 4 (Minimal Oversight, Pandey, CARE-Drive)

- **Zakres W2/W3:** tylko zwykłe, nieatakowane przesunięcia dowodów. Twierdzenie 1 Pandey i in.: przy możliwym fałszowaniu do k źródeł każda procedura musi eskalować, gdy dowody pasują do dwóch działań. Dla scenariusza ataku proponujemy łączenie naszej reguły z ich bramką.
- **Reguła maskowania (Azevedo) dla wszystkich baseline'ów:** oceniamy własną propozycję agenta sprzed korekty, także w epizodach eskalowanych.
- **Nowe do cytowania:** Pandey i in., „Local Allow, Global Deny” (2610.27620): zależność wyniku od informacji niedozwolonej da się wykryć tylko w parach przebiegów; Santoni de Sio i van den Hoven 2018 (tracking „demonstrably and verifiably”, „no matter how efficient”; przykład husky/śnieg = dobre działanie na złej podstawie; próg zależny od celu → α_c).
- **Receptywność / reaktywność:** CARE-Drive ich nie rozróżnia; to wnosimy my. Pomiar 2×2 per przebieg: czy agent rozpoznał zmianę, czy na nią zareagował.
