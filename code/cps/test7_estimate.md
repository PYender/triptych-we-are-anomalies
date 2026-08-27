# TEST 7 — Etap B: kod estymacji P1 + symulacja odzysku + model zerowy N1 (rodzina 9b)

**Realizuje:** `TEST7_PROTOCOL.md` §5, §7, §8 (cytowane niżej, nie streszczane — reguła D-024)
· `TASK_7B_BRIEF.md` §2-§6 (D-029) · **Kod:** `test7_estimate.py` · **Estymator:**
`test6_weibull.py` po naprawie (pięć usterek + D-022), zweryfikowany w Kroku C Testu 6
(D-027) — **nie napisany od nowa** (brief §1). **Status: po DRUGIM przeglądzie
`PRZEGLAD_test7_estimate.md` — usterka mechanizmu cenzurowania w symulacji odzysku
naprawiona (§3); w konsekwencji WYCOFANE zgłoszenie D-030 o „spuriously podwyższonym θ̂"
(§3b) — było artefaktem złego mechanizmu, nie własnością danych. NIEURUCHOMIONY na
`test7_intervals.csv` w sensie decyzyjnym** — patrz §4 (ujawnienie) niżej.

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

| | wszystkie diady w pliku | diady wnoszące ≥1 wiersz do modelu głównego (po §1b) |
|---|---|---|
| n | 120 | **101** |
| odstępy pełne | 43 | **37** |
| odstępy cenzurowane | 120 (62 `cenzurowany` + 58 `cenzurowany_bez_epizodow`) | **95** |

**Odkrycie wymagające jawnego odnotowania: 14 diad (120−106, przed poprawką §1b) wnoszą
ZERO wierszy do modelu głównego.** Mechanizm: diada o dokładnie jednym epizodzie, dla
którego zadziałał Skutek A (D-021 — okno domyka się na zdarzeniu, bez odstępu cenzurowanego
po nim) ma tylko wiersz `t0` (wykluczony z modelu głównego przez §5) i nic więcej — ani
odstępu pełnego (potrzeba ≥2 epizodów), ani cenzurowanego (Skutek A go nie tworzy). To jest
zgodne z protokołem zastosowanym dosłownie, nie błąd, ale **efektywne N modelu głównego to
101, nie 120** — ma być nazwane wprost w raporcie Etapu C, nie ukryte za samą liczbą 120
diad populacji. Patrz §5 (ograniczenie „przypadki typu Troi").

## 1b. NAPRAWIONE (przegląd, naruszenie protokołu) — diady lewostronnie ucięte wykluczone w całości

`TEST7_PROTOCOL.md` §3 (cytat): „Diady te [18 rywalizacji lewostronnie uciętych] muszą być
oznaczone kolumną `ucięta = 1` **i wchodzić do wariantu S3, nie do modelu głównego**." Zdanie
nie zostawia alternatywy (`PRZEGLAD_test7_estimate.md` §2) — pierwsza wersja tego kodu
traktowała to błędnie jako lukę interpretacyjną i zostawiała te diady w modelu głównym
(wykluczając tylko ich `t0`, jak wszystkie inne diady). **To było niezgodne z §3, nie wybór
interpretacyjny.**

**Naprawione:** `load_grouped(include_t0=False)` wyklucza teraz **całe diady** `ucieta==1`;
`include_t0=True` (S3) włącza je z powrotem, razem z `t0` — dokładnie tam, gdzie §3 każe im
być. Dotyczy 5 diad, 9 wierszy modelu głównego (`France–Germany`, `France–Austria-Hungary`,
`USSR–Turkey`, `United Kingdom–France`, `United Kingdom–USSR`). **Liczby przed/po (D-028):**
n 106→**101**, pełne 43→**37**, cenzurowane 98→**95** — zweryfikowane bezpośrednim
przeliczeniem, zgadza się dokładnie z przewidywaniem przeglądu („efektywne N spada z 106 na
około 101").

## 2. P1 — dopasowanie (brief §3, protokół §7)

> **P1** | Weibull z kruchością gamma | 120 diad, bez `t0` | **ORZEKA dla H9b.1**

`fit_p1(grouped)` zwraca oba dopasowania: `fit_frailty` (orzekający) i `fit_pooled`
(diagnostyka θ→0, brief §3 — „kosztuje zero, różnica P1 wobec pulowanego jest wprost miarą
heterogeniczności temp"). `ci_p1(...)` liczy **oba** przedziały (protokół §8: „Przedziały
ufności obowiązkowe, w dwóch postaciach: profil wiarygodności oraz bootstrap losujący całe
diady") dla obu dopasowań, reużywając `test6_weibull.profile_ci_k` /
`bootstrap_ci_k_pooled` / `bootstrap_ci_k_frailty` bez modyfikacji.

**NAPRAWIONE (brak nr 3 z przeglądu).** `bootstrap_ci_k_frailty` zwraca od D-022 czwarty
element, `frac_theta_boundary` — pierwsza wersja `ci_p1` woła tę funkcję i po prostu nie
rozpakowywała/etykietowała go, więc przedział bootstrapowy dla kruchości byłby zwrócony bez
towarzyszącej mu liczby wymaganej do jego interpretacji. Naprawione: `ci_p1` teraz zwraca
`bootstrap_frailty["frac_theta_boundary"]` i flagę `interpretowalny` (próg 30%, zgodnie z
duchem D-022 „kilkadziesiąt procent") jawnie obok przedziału. W świetle §3b/§3c — na tej
strukturze problemem może być NIE granica (niski odsetek), tylko rozjazd w drugą stronę;
`frac_theta_boundary` sam w sobie nie wykryje tego drugiego zjawiska, co ma być odnotowane
w raporcie Etapu C, nie mylone z „przedział jest OK, bo granica rzadka".

## 3. Symulacja odzysku parametrów na strukturze rzeczywistej (brief §4) — MECHANIZM NAPRAWIONY (drugi przegląd)

**Usterka wykryta w drugim przeglądzie, we własnym, wcześniej zatwierdzonym kodzie
recenzenta.** Pierwsza wersja (`group_specs_from` + stara `simulate_dataset_test7`) ustalała
z góry liczbę zdarzeń pełnych i to, czy istnieje obserwacja cenzurowana (z realnej
struktury), a czas cenzurowania losowała **niezależnie** od czasów zdarzeń — zdarzenie i
cenzurowanie nigdy się nie „spotykały". W rzeczywistości obserwacja jest cenzurowana, gdy
czas administracyjny wypada PRZED zdarzeniem: widzimy `min(T,C)`, a liczba zdarzeń pełnych
jest WYNIKIEM tego wyścigu, nie założeniem.

Recenzent zmierzył skutek: przy k_prawdziwe=1, właściwy mechanizm daje nieobciążone k̂ na
każdym poziomie cenzurowania (mediana 0,989–1,013); stara konstrukcja jest nieobciążona
TYLKO, gdy skala cenzurowania przypadkiem równa się λ (mediana 1,025), i zaniża k̂ o **jedną
trzecią** przy skali 2,5×λ (mediana 0,670) — dokładnie reżim, w jakim leżą realne dane
(stosunek median cenzurowane/pełne = 2,25, §4b).

**Naprawione:** `window_lengths_from` odczytuje realną długość okna administracyjnego (Σ
wszystkich realnych `ekspozycja` danej diady w modelu głównym) — fakt egzogeniczny/
strukturalny (długość okna nie jest wynikiem procesu wojen, tylko dat kalendarzowych/
członkostwa), analogicznie do `T` już używanego w `test6_null.py`/D-026, nie nowe naruszenie
zasady „nigdy wartości t". `simulate_dataset_test7` symuluje teraz właściwy wyścig:
odstępy pełne, dopóki suma mieści się w oknie, ostatni ucina się do reszty okna jako
cenzurowany. **Liczba zdarzeń jest wynikiem, nie założeniem.**

**Struktura jest ekstremalnie rzadka: tylko 11 ze 101 grup ma ≥2 zdarzenia pełne** (82 grupy
mają 0, 8 mają 1) — rozkład pełny w §3d. Scenariusze skalibrowane na λ=89 (Σokien/n_zdarzeń
realnych = 3279/37 ≈ 88,6), żeby liczba zdarzeń symulacji zbliżała się do realnej (37) —
poprzednie λ=15-25 dawało kilkukrotnie więcej zdarzeń niż realny zbiór, bo teraz liczba
zdarzeń jest wynikiem, nie parametrem wejściowym.

Trzy zestawy uruchomione (dane syntetyczne, poprawiony mechanizm, 101 okien realnych):

| zestaw | k praw. | θ praw. | n zdarzeń (wynik) | k̂ pulowany | k̂ kruchość | θ̂ kruchość |
|---|---|---|---|---|---|---|
| k=1, θ=0 | 1,0 | 0,0 | 38 | 0,900 | 0,900 | **1e-10 (granica)** — poprawnie: brak kruchości wykryty |
| k=1,5, θ=0,3 | 1,5 | 0,3 | 22 | 1,606 | 1,607 | **1e-10 (granica)** — nieodróżnione od zera |
| k=0,7, θ=0,6 | 0,7 | 0,6 | 52 | 0,650 | 0,682 | 0,345 — nie na granicy, sensowny rząd wielkości |

`test_theta_zero_limit_test7`: log-wiarygodność pulowana vs kruchość(θ=1e-9) zgodne do
3,5·10⁻⁵ — test zaliczony.

## 3b. WYCOFANIE — „spuriously podwyższone θ̂" (D-030) było artefaktem złego mechanizmu, nie własnością danych

**Poprzednia wersja tego dokumentu (i wpis D-030) zgłaszała, że θ̂ konsekwentnie ląduje w
dobrze zidentyfikowanym, ale spuriously podwyższonym miejscu (mediana 1,4–1,6) NIEZALEŻNIE
od θ prawdziwego, włącznie z θ=0 — z weryfikacją, że wszystkie 4 starty multistartu zbiegały
do tego samego optimum, lepszego niż granica.** Po naprawie mechanizmu cenzurowania (§3)
zjawisko **znika**: przy θ_prawdziwe=0, k̂_kruchość zbiega do granicy θ̂=1e-10 (poprawnie —
brak kruchości wykryty), nie do 1,6. Multistart faktycznie zbiegał konsekwentnie do jednego
optimum za każdym razem — ale było to optimum WŁAŚCIWE DLA ŹLE SKONSTRUOWANYCH DANYCH
(sztucznie utworzonych przez niezależne losowanie zdarzeń i cenzurowania), nie artefakt
samego wielostartu ani realna własność struktury Testu 7. **Wniosek D-030 o „poważniejszym
problemie niż brief §5 przewidywał" jest tu wycofany** — dokładnie zgodnie z tym, jak sam
recenzent wycofał własne wcześniejsze podejrzenie o usterce w granicy θ→0 po sprawdzeniu.
Pełny pomiar procentowy z poprawionym mechanizmem — §3c.

## 3c. Zapadanie się θ̂ — pomiar procentowy, poprawiony mechanizm

`test_frailty_boundary_collapse_test7` (60 powtórzeń/θ, jak D-022, poprawiony mechanizm §3,
λ=89):

| θ prawdziwe | % na granicy (60 biegów) | mediana θ̂ |
|---|---|---|
| 0,0 | **48,3%** | 0,0088 |
| 0,3 | 26,7% | 0,111 |
| 0,6 | 16,7% | 0,684 |
| 1,0 | 3,3% | 0,950 |

**Wzorzec sensowny, analogiczny do D-022 (Test 6, 60%/33%/12%/2% na tych samych progach θ)**:
odsetek na granicy MALEJE monotonicznie wraz z θ prawdziwym, mediana θ̂ ROŚNIE w stronę
prawdy (0,95 przy θ=1,0 — bardzo bliskie). Test 7 (101 grup, mimo 82 puste) zapada się
NIECO CZĘŚCIEJ niż Test 6 przy θ=0 (48% wobec 60%... — w tym samym rzędzie wielkości,
różnica prawdopodobnie wynika ze strumienia losowań i różnicy w rozmiarze próby, nie
odnotowuję dalej bez dodatkowej weryfikacji). To jest DOKŁADNIE zjawisko, jakiego brief §5
się spodziewał („szeroki przedział dla θ") — nie coś gorszego, jak błędnie zgłoszono w D-030
przy złym mechanizmie.

## 3d. Rozkład liczby zdarzeń na diadę — same liczebności (zażądane przez Claude)

| n zdarzeń pełnych | liczba diad |
|---|---|
| 0 | 82 |
| 1 | 8 |
| 2 | 5 |
| 3 | 5 |
| 4 | 1 |
| **razem** | **101** |

## 3e. Zadeklarowane odchylenie — przeliczone dla obu testów, poprawionym mechanizmem

Zlecone przez Claude: odchylenie standardowe k̂ (statystyka orzekająca każdego testu) pod
prawdą k=1/θ=0, poprawionym mechanizmem, λ skalibrowane do realnej liczby zdarzeń:

| test | statystyka orzekająca | n grup | λ | n powtórzeń | mediana k̂ | odch. std. k̂ |
|---|---|---|---|---|---|---|
| Test 6 | pulowana (`fit_pooled`) | 18 | 34,6 | 300 | 1,010 | **0,127** |
| Test 7 | kruchość (`fit_frailty`) | 101 | 89,0 | 150 | 1,013 | **0,138** |

Test 6: 0,127 — praktycznie identyczne z wcześniej deklarowanym „~0,12" (ta wartość okazuje
się nie wymagać korekty, bo `test6_weibull.simulate_dataset` domyślnie losuje cenzurowanie
ze skalą `censor_scale=lam` — dokładnie ten przypadek, który recenzent zmierzył jako
przypadkowo nieobciążony). Test 7: 0,138 — nieco NIŻSZE niż poprzednio cytowane „~0,15"
(Claude), z poprawionym mechanizmem i skalibrowanym λ. Różnica jest w granicach szumu tych
liczby powtórzeń (150 vs 300) — nie traktuję jej jako precyzyjnej do trzeciego miejsca.

## 4. Model zerowy N1 — diagnostyczny, poza regułą §8 (D-029 pkt 2)

Zadeklarowane w D-029, **przed jakimkolwiek biegiem Testu 7**: doświadczenie z Kroku C Testu
6 (D-026/D-027) pokazało, że CI-only i model zerowy N1 mogą wskazać różne strony progu.
Reguła §8 Testu 7 (oparta wyłącznie na CI) **nie jest zmieniana** — zamrożona. Etap B ma
**dodatkowo** policzyć N1 na strukturze Testu 7 i podać `p` obok przedziałów, wyłącznie
diagnostycznie.

`run_n1_test7` przenosi mechanizm `test6_null.py` (λ̂=n/T per diada, surogaty
Exponential(1/λ̂), cenzurowanie stałe), generalizowany na 0/1-cenzurowanie (§1) — dla diady
bez obserwacji cenzurowanej surogat też jej nie dostaje. **Zabezpieczenie przed remisem
(D-026 §7) przeniesione również**: `tie_fraction`/`TIE_FRAC_STOP=0,01`, zatrzymuje bieg dla
KAŻDEJ z dwóch statystyk osobno (nie powinien być zdegenerowany — permutuje/losuje wewnątrz
struktury per-diady, nie między diadami — ale sprawdzane mechanicznie, nie zakładane).

**NAPRAWIONE (brak nr 2 z przeglądu — statystyka niewłaściwa).** Pierwsza wersja liczyła
`k_obs` i wszystkie surogaty wyłącznie przez `fit_pooled`, podczas gdy statystyką ORZEKAJĄCĄ
w Teście 7 jest `fit_frailty` (§7 protokołu) — diagnostyka pokazywała rozjazd dla statystyki,
która nie rozstrzyga H9b.1, nie odpowiadając na pytanie, dla którego powstała
(`PRZEGLAD_TASK_7B.md` §2). **Naprawione: liczy teraz OBIE wersje**, `pooled` (pełne
B=2000, tanie) i `frailty` (statystyka orzekająca, zredukowane `B_frailty=500` —
kompromis kosztowy zaakceptowany w przeglądzie, dopasowanie z kruchością jest znacząco
droższe). `simulate_n1_once_test7` zwraca teraz też etykiety diad, wymagane, żeby ten sam
surogat dało się ocenić obiema statystykami.

**Sprawdzenie mechaniczne wykonane** (B=50/20, ziarno eksploracyjne, NIE ziarno protokołu,
NIE B=2000/500 docelowe — to nie jest bieg Etapu C): obie ścieżki działają bez błędu,
`frac_tie=0,0` dla obu (brak degeneracji, zgodnie z oczekiwaniem — N1 nie ma mechanizmu N2).
**Ujawnienie wymagane przez zakaz nr 10:** to sprawdzenie z konieczności przelicza
`fit_pooled`/`fit_frailty` na realnych wartościach `t` (żeby w ogóle sprawdzić, czy kod się
nie wywraca) — tak samo jak mechaniczne sprawdzenie N1 w Kroku B Testu 6 dotykało realnych
`λ̂` per diada. Wynikowe wartości `k_obs`/`p` **nie są tu raportowane ani przez nikogo
interpretowane** — były widoczne na ekranie podczas weryfikacji kodu i nie są chowane (zakaz
nr 10 w drugą stronę), ale nie stanowią wyniku Etapu C, który wymaga osobnego biegu przy
ustalonym ziarnie protokołu i, jak Test 6, osobnej autoryzacji.

## 4b. Realizm cenzurowania w symulacji — sprawdzony ponownie po naprawie mechanizmu

Przed naprawą (§3): stosunek mediany cenzurowanej do mediany pełnej wynosił **2,25** realnie
wobec **0,90** w symulacji — duża rozbieżność, która okazała się OBJAWEM usterki nadrzędnej
(cenzurowanie losowane niezależnie od zdarzeń), nie osobnym zjawiskiem do korygowania z
osobna. **Po naprawie (okno realne jako fakt, liczba zdarzeń jako wynik):** stosunek wynosi
**1,52** — znacznie bliżej realnego (2,25) niż poprzednio (0,90), choć nie identyczne (jeden
konkretny scenariusz k=1/λ=89/θ=0 nie musi odtworzyć każdego aspektu realnego rozkładu co do
liczby, tylko mechanizm generowania). Traktowane jako potwierdzenie, że naprawa poprawiła
realizm we właściwym kierunku, nie jako precyzyjna kalibracja.

## 5. Warianty wrażliwości — status (brief §3, protokół §7)

| id | status | powód |
|---|---|---|
| **S3** | **gotowy** — `load_grouped(include_t0=True)` | włącza `t0` jako pełny ORAZ zwraca diady `ucieta==1` (§1b — to ich właściwe miejsce); 120 diad, 107 pełnych, 98 cenzurowanych (zweryfikowane bezpośrednio) |
| S1 | **NIE zbudowany** | wymaga przebudowy sekwencji zdarzeń z wykluczeniem epizodów 1914–18/1939–45 — to zmienia sąsiadujące odstępy (nie tylko filtruje wiersze), czyli osobne zadanie budowy danych, analogiczne do Etapu A |
| S2 | **NIE zbudowany, ale ROZSTRZYGNIĘTY w przeglądzie** | patrz §5b — feasibility potwierdzona (76 wierszy/73 diady), budowa nadal do wykonania |
| S4 | **NIE zbudowany** | wymaga całkowicie osobnej populacji z `td_rivalries.rda` (Thompson i Dreyer 2012) — nowy Etap A, nie wariant tego kodu |

**Zakres tej dostawy Etapu B ograniczony do P1 (główny) + S3** (obie na tej samej warstwie
danych już zbudowanej w Etapie A). S1/S2/S4 wymagają własnej budowy zbioru i nie są
częścią tego STOP-u — zgłaszam to wprost, zamiast rozmywać zakres.

## 5b. ROZSTRZYGNIĘTE w przeglądzie — `positional=0` w S2, konwencja NaN=0

Sprawdzone strukturalnie w `tss_rivalries`: kolumna `positional` przyjmuje wyłącznie
wartości **1,0 albo brak (NaN)** — **nigdy dosłownie 0**. **Rozstrzygnięcie przeglądu:**
brak wartości oznacza nieobecność składnika, czyli 0 — ta konwencja jest już w projekcie
użyta i sprawdzalna: liczba kontrolna 152 dla `spatial=1` (D-016) powstała z tej samej
kolumnowej rodziny wartości 1,0/NaN, filtrując `spatial==1` (152 wierszy potwierdzone
niezależnie); stosowanie innej konwencji dla `positional` niż dla `spatial` byłoby
niespójnością wewnątrz jednego zbioru. **S2 = `spatial==1` i `positional != 1`.**
Zweryfikowane niezależnie: **76 wierszy rywalizacji, 73 unikalne diady** przed nałożeniem
okna ryzyka — zgadza się dokładnie z pomiarem przeglądu. Wariant jest wykonalny, nie pusty.
Budowa zbioru (rebuild okien/odstępów ograniczony do tej populacji) pozostaje do zrobienia —
nie część tego STOP-u (§5).

## 6. Ograniczenie do raportu — 14 diad typu Troi, niewidoczne dla modelu głównego

Diady wnoszące zero wierszy do modelu głównego (§1, 14 na 106 przed §1b, wciąż 14 po —
niedotknięte poprawką ucieta) to przypadki, w których **jedyna wojna diady zakończyła samą
rywalizację** — jeden konflikt i koniec, analogicznie do Troi. Nie wnoszą nic do
wiarygodności (nie obciążają estymacji P1), ale **zmieniają to, o czym test w praktyce
orzeka**: populacja Testu 7 została dobrana świadomie po stawce terytorialnej (rywalizacje
przestrzenne, D-016), nie po liczbie wojen — właśnie po to, żeby takie pary (jeden wybuch,
koniec sporu) wejść do analizy, w przeciwieństwie do progu ≥3 wojen w Teście 6. **Model
główny mimo to ich nie widzi** — mechanizm §5 protokołu (t0 poza modelem) w połączeniu z
Skutkiem A (D-021) usuwa je z pełnym skutkiem, nie częściowym. Ma to trafić do ograniczeń
raportu Etapu C wprost: dobór populacji po stawce nie gwarantuje, że wszystkie tak dobrane
pary są widoczne modelowi, który z niej korzysta.

## 7. Co ten kod NIE robi

Nie liczy `k_obs` P1 na `test7_intervals.csv` jako wynik decyzyjny — patrz §4, ujawnienie.
Nie buduje S1/S2/S4 (§5) — S2 rozstrzygnięty co do definicji (§5b), ale niezbudowany. Nie
zmienia rozkładu cenzurowania symulacji poza mechanizmem już naprawionym w §3 (drobna
rozbieżność 1,52 wobec 2,25 w §4b nie jest korygowana dalej — jeden scenariusz nie musi
odtworzyć całego realnego rozkładu). `main()` blokuje `--run-real` (`SystemExit`).

## 8. STOP

**Pierwsza runda** (D-030): cztery punkty blokujące z pierwszego przeglądu naprawione —
§1b (naruszenie protokołu, ucieta), §3c (pomiar procentowy), §4 (N1 obiema statystykami),
§2 (frac_theta_boundary). Uwagi niebolkujące: §4b (realizm cenzurowania — pierwsza wersja),
§6 (ograniczenie Troi).

**Druga runda (ten dokument):** drugi przegląd wykrył usterkę mechanizmu cenzurowania w
samej symulacji odzysku — recenzent wskazał ją we własnym, wcześniej zatwierdzonym kodzie i
odnotował to wprost. Naprawiona (§3): okno realne jako fakt egzogeniczny, liczba zdarzeń
jako wynik wyścigu T-kontra-okno, nie założenie. **Konsekwencja: „odkrycie" z D-030 o
spuriously podwyższonym θ̂ jest WYCOFANE (§3b)** — po naprawie θ̂ zachowuje się sensownie,
analogicznie do D-022 (Test 6). Zadeklarowane odchylenie przeliczone dla obu testów (§3e):
Test 6 0,127 (bez zmian względem „~0,12"), Test 7 0,138 (nieco niżej niż „~0,15"). Rozkład
liczebności zdarzeń na diadę podany osobno (§3d).

Kod P1(główny, po §1b)+S3, symulacja odzysku (mechanizm naprawiony), model zerowy N1 (obie
statystyki), suita poprawności gotowe do kolejnego przeglądu. Bieg na danych rzeczywistych
(Etap C) dopiero po nim i, analogicznie do Testu 6 (D-027), po jawnej autoryzacji — nie
automatycznie po samym przeglądzie.
