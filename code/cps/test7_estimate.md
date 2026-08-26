# TEST 7 — Etap B: kod estymacji P1 + symulacja odzysku + model zerowy N1 (rodzina 9b)

**Realizuje:** `TEST7_PROTOCOL.md` §5, §7, §8 (cytowane niżej, nie streszczane — reguła D-024)
· `TASK_7B_BRIEF.md` §2-§6 (D-029) · **Kod:** `test7_estimate.py` · **Estymator:**
`test6_weibull.py` po naprawie (pięć usterek + D-022), zweryfikowany w Kroku C Testu 6
(D-027) — **nie napisany od nowa** (brief §1). **Status: po przeglądzie
`PRZEGLAD_test7_estimate.md` — 4 punkty blokujące naprawione (§1b niżej), plus jedno NOWE,
poważniejsze odkrycie (§3b) wykryte przy okazji naprawy. NIEURUCHOMIONY na
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

## 3. Symulacja odzysku parametrów na strukturze rzeczywistej (brief §4)

`group_specs_from` odczytuje **wyłącznie strukturę** (n_full, czy_ma_cenzurowany) per diada
— nigdy wartości `t` — z modelu głównego (101 grup, po §1b). Różni się od
`test6_weibull.group_sizes_from`, które zakłada zawsze dokładnie 1 cenzurowany/diadę
(założenie fałszywe tutaj, patrz §1). `simulate_dataset_test7` generalizuje
`test6_weibull.simulate_dataset` na to 0/1-cenzurowanie, z cenzurowaniem
**administracyjnym** (niezależnym od czasu zdarzenia — usterka 4 przeglądu Testu 6:
cenzurowanie zależne od T zawyża k̂ o ok. 5 pkt proc.).

**Struktura jest ekstremalnie rzadka: tylko 11 ze 101 grup ma ≥2 zdarzenia pełne** (82 grupy
mają 0, 8 mają 1). Tylko te 11 grup niosą jakąkolwiek informację o heterogeniczności — to
mniej korzystne niż w Teście 6 (gdzie żadna grupa nie miała zera zdarzeń) i gorsze, niż
przewidywał brief §5 („kilkanaście grup niosących informację" — trafne co do liczby, ale
patrz §3b, konsekwencja jest poważniejsza niż „szeroki przedział").

Trzy zestawy uruchomione (wyłącznie dane syntetyczne, struktura 101 grup / 37 zdarzeń /
95 cenzurowanych, zgodnie ze strukturą prawdziwego zbioru po §1b):

| zestaw | k praw. | θ praw. | k̂ pulowany | k̂ kruchość | θ̂ kruchość |
|---|---|---|---|---|---|
| k=1, θ=0 | 1,0 | 0,0 | 0,946 | 1,051 | **1,302 — nie na granicy** |
| k=1,5, θ=0,3 | 1,5 | 0,3 | 1,229 | 1,442 | 1,482 — nie na granicy |
| k=0,7, θ=0,6 | 0,7 | 0,6 | 0,777 | 0,804 | 0,343 — nie na granicy |

`test_theta_zero_limit_test7`: log-wiarygodność pulowana vs kruchość(θ=1e-9) zgodne do
2,7·10⁻⁵ — test zaliczony (θ=1e-6 użyte pierwotnie zbiegało wolniej na tej strukturze,
sprawdzone bezpośrednio: różnica maleje gładko z θ, 0,35→4·10⁻⁶ między logθ=−6 a −20 —
wolniejsze tempo zbieżności, nie błąd; zamieniono na θ=1e-9).

## 3b. ODKRYCIE NOWE, POWAŻNIEJSZE niż brief §5 przewidywał — θ̂ nie zapada się, tylko rozjeżdża w GÓRĘ, spuriously

Zlecony przez przegląd pomiar procentowy (§3c niżej) ujawnił coś innego niż D-022 dla Testu
6: na tej strukturze (11/101 grup informujących) `θ̂` **nie zapada się do granicy** —
zapada się w 0–1,7% biegów na 60, w zależności od θ prawdziwego (patrz tabela §3c). Zamiast
tego **mediana θ̂ wynosi 1,4–1,6 NIEZALEŻNIE od θ prawdziwego, włącznie z θ_prawdziwe=0**:

**Zweryfikowane, że to nie jest awaria wielostartu.** Dla repliki syntetycznej z θ_prawdziwe=0:
wszystkie 4 punkty startowe zbiegły do tego samego θ̂≈1,60 (`converged_same=True`,
`k_by_start` identyczne do 6 miejsca), z log-wiarygodnością **−189,13**, WYRAŹNIE wyższą
(lepszą) niż na granicy θ=1e-10 (log-wiarygodność −192,14, identyczna z modelem pulowanym).
**To jest prawdziwe, dobrze zidentyfikowane maksimum wiarygodności — nie błąd optymalizacji
ani przypadek startu.**

**Interpretacja.** Przy tak małej liczbie grup niosących informację (11/101), gamma-kruchość
MLE ma tendencję do znajdowania **pozornej heterogeniczności** nawet, gdy jej prawdziwie nie
ma — przypadkowa zmienność w tym, jak nieliczne wielo-zdarzeniowe grupy rozkładają odstępy,
zostaje wchłonięta przez `θ̂` jako rzekoma kruchość, bo model ma na to miejsce (mało grup
kontrolnych, żeby to obalić). To jest **poważniejszy problem niż ten, o który pytał brief
§5** („szeroki przedział, spodziewaj się"): to nie jest kwestia szerokości przedziału wokół
prawdziwej wartości — **punktowe θ̂ jest systematycznie przesunięte w górę, niezależnie od
prawdy, i jest to dobrze zidentyfikowany (nie graniczny) wynik**, więc nie ma prostego
sygnału ostrzegawczego typu „θ̂ na granicy" do wyłapania go automatycznie.

**Konsekwencja dla P1 (orzekający, protokół §7).** Statystyka orzekająca dla H9b.1 to `k̂`
z modelu z kruchością, nie samo `θ̂` — ale `k̂` z kruchością jest liczone **łącznie** z
oszacowaniem `θ̂`, więc spuriously podwyższone `θ̂` wpływa też na `k̂` (patrz tabela §3: przy
θ_prawdziwe=0, k̂_kruchość=1,051 vs k̂_pulowany=0,946 — kruchość i pulowany DAJĄ RÓŻNE
odpowiedzi nawet, gdy prawdziwej kruchości nie ma, bo model kruchości "zużywa" część
zmienności na spurious θ̂ zamiast na k). **Nie naprawiam tego teraz — zgłaszam jako
ustalenie do oceny przed Etapem C**, analogicznie do D-022 dla Testu 6, ale gorsze: tam
zgodność P1/F1 była czasem niediagnostyczna (granica), tutaj F1 (orzekający) może dawać
systematycznie inny wynik niż intuicja o „braku kruchości" sugerowałaby.

## 3c. Zapadanie się/rozjazd θ̂ — pomiar procentowy (naprawiony brak nr 1 z przeglądu)

`test_frailty_boundary_collapse_test7` (60 powtórzeń na θ, jak D-022 dla Testu 6, ale na
`simulate_dataset_test7`/`group_specs` — 0/1-cenzurowanie, nie zawsze-1-cenzurowany):

| θ prawdziwe | % na granicy (60 biegów) | mediana θ̂ |
|---|---|---|
| 0,0 | 0,0% | **1,588** |
| 0,3 | 1,7% | **1,647** |
| 0,6 | 0,0% | **1,488** |
| 1,0 | 0,0% | **1,426** |

Zgodne z §3b: procent na granicy jest NISKI (przeciwieństwo Testu 6, gdzie przy θ=0 granica
wychodziła w 60% biegów) — ale mediana θ̂ jest **oderwana od prawdy** w każdym wierszu.
Niski odsetek granicy TUTAJ nie oznacza dobrej identyfikowalności — oznacza, że estymator
konsekwentnie ląduje w innym, spuriously-podwyższonym miejscu zamiast na granicy.

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

## 4b. Realizm cenzurowania w symulacji — uwaga niebolkująca z przeglądu, sprawdzona

Cenzurowanie administracyjne `c = Exponential(scale=lam)` ma poprawny ODSETEK (zgodny z
konstrukcją grupy), ale jego ROZKŁAD nie musi przypominać realnego, gdzie czas cenzurowany
to pozostała ekspozycja, a dla diad bez epizodów — całe okno. `censoring_realism_check`
porównuje medianę: **w realnych danych stosunek mediany cenzurowanej do mediany pełnej
wynosi 2,25** (18 wobec 8 lat) — obserwacje cenzurowane są typowo znacznie DŁUŻSZE niż
odstępy pełne. **W symulacji (k=1,λ=20,θ=0) stosunek wynosi 0,90** — w symulacji
cenzurowanie jest, jeśli już, odrobinę KRÓTSZE niż zdarzenia, nie dłuższe. **Symulacja
odzysku nie odtwarza tej asymetrii** — informacyjność (długość) obserwacji cenzurowanych
względem pełnych jest w symulacji zaniżona względem rzeczywistości, więc wyniki symulacji
odzysku (§3, §3b, §3c) mogą NIE przewidywać dokładnie zachowania na realnym zbiorze w tym
wymiarze — mają być czytane jako orientacyjne co do rzędu wielkości/kierunku problemu, nie
jako precyzyjna kalibracja. Nie naprawiane teraz (zmiana rozkładu symulowanego cenzurowania
wymagałaby decyzji o modelu tego rozkładu, wykraczającej poza ten Etap B).

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
naprawia rozjazdu θ̂ opisanego w §3b (opisujemy, nie łatamy, zgodnie z zasadą D-022/D-026).
Nie zmienia rozkładu cenzurowania symulacji (§4b). `main()` blokuje `--run-real`
(`SystemExit`).

## 8. STOP

Cztery punkty blokujące z `PRZEGLAD_test7_estimate.md` naprawione: §1b (naruszenie
protokołu — ucieta), §3c (pomiar procentowy zapadania/rozjazdu θ̂), §4 (N1 liczony obiema
statystykami), §2 (frac_theta_boundary surfaced w bootstrapie). Uwagi niebolkujące
uwzględnione: §4b (realizm cenzurowania), §6 (ograniczenie diad typu Troi).

**Odkrycie nowe, wykryte przy naprawie, ważniejsze niż punkt zlecony (§3b):** na strukturze
Testu 7 (11/101 grup informujących o kruchości) `θ̂` nie zapada się do granicy jak w Teście
6 — zamiast tego ląduje w dobrze zidentyfikowanym, ale spuriously podwyższonym miejscu
(mediana 1,4–1,6) NIEZALEŻNIE od prawdy, włącznie z brakiem prawdziwej kruchości. To nie
jest naprawione ani rozstrzygnięte samodzielnie — zgłaszam do oceny przed Etapem C, bo
wpływa bezpośrednio na wiarygodność `k̂` orzekającego (kruchość), nie tylko na `θ̂` samo
w sobie.

Kod P1(główny, po §1b)+S3, symulacja odzysku, model zerowy N1 (obie statystyki), suita
poprawności (rozszerzona o §3c/§4b) gotowe do ponownego przeglądu. Bieg na danych
rzeczywistych (Etap C) dopiero po nim i, analogicznie do Testu 6 (D-027), po jawnej
autoryzacji — nie automatycznie po samym przeglądzie.
