# TEST 7 — Etap B: kod estymacji P1 + symulacja odzysku + model zerowy N1 (rodzina 9b)

**Realizuje:** `TEST7_PROTOCOL.md` §5, §7, §8 (cytowane niżej, nie streszczane — reguła D-024)
· `TASK_7B_BRIEF.md` §2-§6 (D-029) · **Kod:** `test7_estimate.py` · **Estymator:**
`test6_weibull.py` po naprawie (pięć usterek + D-022), zweryfikowany w Kroku C Testu 6
(D-027) — **nie napisany od nowa** (brief §1). **Status: kod + symulacja + suita
poprawności gotowe do przeglądu. NIEURUCHOMIONY na `test7_intervals.csv` w sensie
decyzyjnym** — patrz §6 (ujawnienie) niżej.

---

## 0. Warunek wstępny odkryty i naprawiony: `test6_weibull.py` na tej gałęzi był NIEAKTUALNY

Zanim cokolwiek napisano: `claude/cps-test-7` miał wciąż **przedreperacyjną** kopię
`test6_weibull.py` — bez wielostartu, bez podłogi `θ̂` (D-022), bez wektoryzacji
`negloglik_frailty` potrzebnej wydajnościowo dla 120 grup. Budowanie Etapu B na tej kopii
powtórzyłoby dokładnie ten typ błędu, któremu ta cała procedura ma zapobiegać — użycie
nieprzejrzanego/przestarzałego kodu jako estymatora decyzyjnego.

**Naprawione przez zmergowanie `claude/cps-test-6` do `claude/cps-test-7`** (commit
`91cdee6`) — sprowadza naprawiony `test6_weibull.py`, `test6_null.py`, Krok C Testu 6 i
scala rozjechany `CPS_DECISION_LOG.md` obu gałęzi (D-019..D-029, w kolejności numerów,
bez utraty żadnego wpisu). To był dokładnie ten sam rodzaj rozjazdu międzygałęziowego,
który wcześniej rozwiązano przez `claude/cps-infra` (PR #14) — tym razem naprawiony przed
napisaniem kodu Etapu B, nie po.

## 1. Struktura modelu głównego — liczby przed/po (D-028)

Protokół §5 (cytat): „Model główny liczy się bez `t0` dla diad, które miały co najmniej
jeden epizod, i z pełnym cenzurowaniem dla diad bez epizodów." Wykonane w
`load_grouped(include_t0=False)`.

| | wszystkie diady w pliku | diady wnoszące ≥1 wiersz do modelu głównego |
|---|---|---|
| n | 120 | **106** |
| odstępy pełne | 43 | 43 (bez zmian — t0 nigdy nie jest pełny) |
| odstępy cenzurowane | 120 (62 `cenzurowany` + 58 `cenzurowany_bez_epizodow`) | **98** |

**Odkrycie wymagające jawnego odnotowania: 14 diad (120−106) wnoszą ZERO wierszy do modelu
głównego.** Mechanizm: diada o dokładnie jednym epizodzie, dla którego zadziałał Skutek A
(D-021 — okno domyka się na zdarzeniu, bez odstępu cenzurowanego po nim) ma tylko wiersz
`t0` (wykluczony z modelu głównego przez §5) i nic więcej — ani odstępu pełnego (potrzeba
≥2 epizodów), ani cenzurowanego (Skutek A go nie tworzy). To jest zgodne z protokołem
zastosowanym dosłownie, nie błąd, ale **efektywne N modelu głównego to 106, nie 120** — ma
być nazwane wprost w raporcie Etapu C, nie ukryte za samą liczbą 120 diad populacji.

Rozbicie diad z main-model rows: **98 ma dokładnie 1 obserwację cenzurowaną, 8 ma zero**
(wielo-epizodowe diady, u których Skutek A też zadziałał, ale mają wcześniejsze odstępy
pełne) — suma 98+8=106 zgadza się. Żadna diada nie ma więcej niż 1 (sprawdzone asercją w
`load_grouped`).

## 2. P1 — dopasowanie (brief §3, protokół §7)

> **P1** | Weibull z kruchością gamma | 120 diad, bez `t0` | **ORZEKA dla H9b.1**

`fit_p1(grouped)` zwraca oba dopasowania: `fit_frailty` (orzekający) i `fit_pooled`
(diagnostyka θ→0, brief §3 — „kosztuje zero, różnica P1 wobec pulowanego jest wprost miarą
heterogeniczności temp"). `ci_p1(...)` liczy **oba** przedziały (protokół §8: „Przedziały
ufności obowiązkowe, w dwóch postaciach: profil wiarygodności oraz bootstrap losujący całe
diady") dla obu dopasowań, reużywając `test6_weibull.profile_ci_k` /
`bootstrap_ci_k_pooled` / `bootstrap_ci_k_frailty` bez modyfikacji.

## 3. Symulacja odzysku parametrów na strukturze rzeczywistej (brief §4)

`group_specs_from` odczytuje **wyłącznie strukturę** (n_full, czy_ma_cenzurowany) per diada
— nigdy wartości `t` — z modelu głównego (106 grup). Różni się od
`test6_weibull.group_sizes_from`, które zakłada zawsze dokładnie 1 cenzurowany/diadę
(założenie fałszywe tutaj, patrz §1). `simulate_dataset_test7` generalizuje
`test6_weibull.simulate_dataset` na to 0/1-cenzurowanie, z cenzurowaniem
**administracyjnym** (niezależnym od czasu zdarzenia — usterka 4 przeglądu Testu 6:
cenzurowanie zależne od T zawyża k̂ o ok. 5 pkt proc.).

Trzy zestawy uruchomione (wyłącznie dane syntetyczne, struktura 106 grup / 43 zdarzenia /
98 cenzurowanych, zgodnie ze strukturą prawdziwego zbioru):

| zestaw | k praw. | θ praw. | k̂ pulowany | k̂ kruchość | θ̂ kruchość |
|---|---|---|---|---|---|
| k=1, θ=0 | 1,0 | 0,0 | 1,052 | 1,051 | **1e-10 (granica)** — poprawnie: brak kruchości wykryty |
| k=1,5, θ=0,3 | 1,5 | 0,3 | 1,339 | 1,696 | 1,692 — nie na granicy |
| k=0,7, θ=0,6 | 0,7 | 0,6 | 0,913 | 0,913 | **1e-10 (granica)** — kruchość NIE wykryta mimo θ prawdziwe=0,6 |

**Trzeci wiersz materializuje dokładnie to ostrzeżenie z brief §5** („Kruchość będzie słabo
identyfikowalna... spodziewaj się bardzo szerokiego przedziału dla θ"): przy silnej,
prawdziwej heterogeniczności (θ=0,6) ten pojedynczy przebieg **nie odróżnia jej od zera** —
θ̂ zapada się do granicy tak samo jak przy θ=0 (D-022, ta sama własność estymatora
udokumentowana dla Testu 6, teraz zademonstrowana na strukturze Testu 7). To nie jest błąd
kodu — to jest własność struktury (43 zdarzenia rozproszone po 106 grupach), zadeklarowana
przed biegiem, zgodnie z zasadą D-022/D-015.

`test_theta_zero_limit_test7`: log-wiarygodność pulowana vs kruchość(θ=1e-6) zgodne do
~4-5 miejsc po przecinku (różnica 9,7·10⁻⁵) — test zaliczony.

## 4. Model zerowy N1 — diagnostyczny, poza regułą §8 (D-029 pkt 2)

Zadeklarowane w D-029, **przed jakimkolwiek biegiem Testu 7**: doświadczenie z Kroku C Testu
6 (D-026/D-027) pokazało, że CI-only i model zerowy N1 mogą wskazać różne strony progu.
Reguła §8 Testu 7 (oparta wyłącznie na CI) **nie jest zmieniana** — zamrożona. Etap B ma
**dodatkowo** policzyć N1 na strukturze Testu 7 i podać `p` obok przedziałów, wyłącznie
diagnostycznie.

`run_n1_test7` przenosi mechanizm `test6_null.py` (λ̂=n/T per diada, surogaty
Exponential(1/λ̂), cenzurowanie stałe), generalizowany na 0/1-cenzurowanie (§1) — dla diady
bez obserwacji cenzurowanej surogat też jej nie dostaje. **Zabezpieczenie przed remisem
(D-026 §7) przeniesione również**: `tie_fraction`/`TIE_FRAC_STOP=0,01`, zatrzymuje bieg,
gdyby N1 Testu 7 okazał się zdegenerowany (nie powinien być — permutuje/losuje wewnątrz
struktury per-diady, nie między diadami — ale sprawdzane mechanicznie, nie zakładane).

**Sprawdzenie mechaniczne wykonane** (B=100, ziarno eksploracyjne, NIE ziarno protokołu,
NIE B=2000 — to nie jest bieg Etapu C): kod działa bez błędu, `frac_tie=0,0` (brak
degeneracji, zgodnie z oczekiwaniem — N1 nie ma mechanizmu N2). **Ujawnienie wymagane przez
zakaz nr 10:** to sprawdzenie z konieczności przelicza `fit_pooled` na realnych wartościach
`t` (żeby w ogóle sprawdzić, czy kod się nie wywraca) — tak samo jak mechaniczne
sprawdzenie N1 w Kroku B Testu 6 dotykało realnych `λ̂` per diada. Wynikowa wartość `k_obs`/
`p` **nie jest tu raportowana ani przez nikogo interpretowana** — była widoczna na ekranie
podczas weryfikacji kodu i nie jest chowana (zakaz nr 10 w drugą stronę), ale nie stanowi
wyniku Etapu C, który wymaga osobnego biegu przy ustalonym ziarnie protokołu i, jak Test 6,
osobnej autoryzacji.

## 5. Warianty wrażliwości — status (brief §3, protokół §7)

| id | status | powód |
|---|---|---|
| **S3** | **gotowy** — `load_grouped(include_t0=True)` | włącza `t0` jako pełny, zgodnie z definicją; 120 diad, 107 pełnych (43+64 t0), 98 cenzurowanych |
| S1 | **NIE zbudowany** | wymaga przebudowy sekwencji zdarzeń z wykluczeniem epizodów 1914–18/1939–45 — to zmienia sąsiadujące odstępy (nie tylko filtruje wiersze), czyli osobne zadanie budowy danych, analogiczne do Etapu A |
| S2 | **NIE zbudowany, dodatkowo: ZNALEZIONA NIEJEDNOZNACZNOŚĆ** | zob. §5b niżej |
| S4 | **NIE zbudowany** | wymaga całkowicie osobnej populacji z `td_rivalries.rda` (Thompson i Dreyer 2012) — nowy Etap A, nie wariant tego kodu |

**Zakres tej dostawy Etapu B ograniczony do P1 (główny) + S3** (obie na tej samej warstwie
danych już zbudowanej w Etapie A). S1/S2/S4 wymagają własnej budowy zbioru i nie są
częścią tego STOP-u — zgłaszam to wprost, zamiast rozmywać zakres.

## 5b. LUKA WYMAGAJĄCA DECYZJI — `positional=0` w S2 może być pusty

Sprawdzone strukturalnie w `tss_rivalries`: kolumna `positional` przyjmuje wyłącznie
wartości **1,0 albo brak (NaN)** — **nigdy dosłownie 0**. Warunek S2 „`spatial=1` i
`positional=0`" zastosowany dosłownie (`positional == 0`) dałby **zbiór pusty**. Możliwe
czytania: (a) `positional=0` oznacza „nieoznaczone jako pozycyjne", czyli `positional`
brakujące traktować jako 0 — wtedy S2 ma sens i sporą populację; (b) rzeczywiście nie ma w
tym źródle rywalizacji jednoznacznie NIE-pozycyjnych i S2 jest bezprzedmiotowy dla tej
wersji `tss_rivalries`. **Nie rozstrzygam tego sam** — to zmienia definicję wariantu, nie
technika. Zgłaszam do decyzji przed budową S2.

## 6. LUKA WYMAGAJĄCA DECYZJI — `ucieta=1` może wykluczać całe diady, nie tylko `t0`

`TEST7_PROTOCOL.md` §3 (cytat): „Diady te [18 rywalizacji lewostronnie uciętych] muszą być
oznaczone kolumną `ucięta = 1` **i wchodzić do wariantu S3, nie do modelu głównego**."
Kolumna `ucieta` w `test7_intervals.csv` jest ustawiana na **całej diadzie** (`ucieta_any`,
wszystkie jej wiersze), nie tylko na `t0`. Czytana dosłownie, ta reguła wyklucza z modelu
głównego **całe** te diady (nie tylko ich `t0`, które i tak jest zawsze wykluczone przez
regułę ogólną z §5) — łącznie **9 wierszy modelu głównego, 5 diad** (`France–Germany`,
`France–Austria-Hungary`, `USSR–Turkey`, `United Kingdom–France`, `United Kingdom–USSR`):

| diada | wiersze main-model | ekspozycja |
|---|---|---|
| United Kingdom–France | 1 cenzurowany_bez_epizodow | 88 |
| United Kingdom–USSR | 1 cenzurowany | 100 |
| France–Germany | 2 pełne + 1 cenzurowany | 43, 21, 0 |
| France–Austria-Hungary | 1 pełny | 55 |
| USSR–Turkey | 3 pełne | 24, 21, 36 |

Statystycznie wątpliwe jest wykluczanie **późniejszych** odstępów tej samej diady (np.
trzeciego odstępu USSR–Turkey, daleko od 1816) z powodu, że **pierwszy** odstęp diady był
lewostronnie ucięty — truncation dotyczy konkretnej obserwacji (t0), nie tożsamości diady.
Ale tekst protokołu, czytany dosłownie, mówi o **diadach**, nie o **odstępach**. **Nie
rozstrzygam tego sam** — kod (`load_grouped`) obecnie NIE implementuje żadnego wykluczenia
po `ucieta` (zachowuje literalne brzmienie ogólnej reguły §5: tylko `t0` wykluczone,
zawsze, dla wszystkich diad) — **to jest domyślne zachowanie kodu, nie decyzja o
interpretacji protokołu**, i wymaga potwierdzenia przed Etapem C: czy 9 wierszy/5 diad
zostają w modelu głównym, czy wychodzą z niego do S3.

## 7. Co ten kod NIE robi

Nie liczy `k_obs` P1 na `test7_intervals.csv` jako wynik — patrz §4, ujawnienie. Nie buduje
S1/S2/S4 (§5). Nie rozstrzyga luk z §5b/§6. `main()` blokuje `--run-real` (`SystemExit`).

## 8. STOP

Kod P1(główny)+S3, symulacja odzysku, model zerowy N1 diagnostyczny i suita poprawności
gotowe do przeglądu. Dwie luki wymagające decyzji autora (§5b, §6) zgłoszone, nie
rozstrzygnięte samodzielnie. S1/S2/S4 pozostają do osobnej budowy danych po ustaleniu §5b.
Bieg na danych rzeczywistych (Etap C) dopiero po przeglądzie kodu i, analogicznie do Testu 6
(D-027), po jawnej autoryzacji — nie automatycznie po samym przeglądzie.
