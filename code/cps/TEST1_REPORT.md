# TEST 1 — RAPORT: czy okres 32–40 lat jest własnością danych

**Rodzina 1** (zarzuty Z3, Z4, Z14 z ADDENDA A Tryptyku)
**Realizuje:** `TEST1_PROTOCOL.md` v1.0 · **Kod:** `test1_band_power.py` v1.0
**Seria pierwszorzędna:** `A_COW_W` 1816–2007 (decyzja D-001)
**Data biegu:** 2026-08-11 · **Ziarno:** 20260810 · **B:** 2000 (P1 dodatkowo 10000)
**Wejście:** `cps_canonical_v2.csv`, sha256 `145aed0053af0d79…` (wygenerowany lokalnie z `test0c_build_canonical.py`; wyjście kontrolne zgodne z briefem §3.2)

Kod przeszedł przegląd autora przed uruchomieniem. Zgłoszona w przeglądzie
rozbieżność z §10 (brak panelu 3 — rozkłady zerowe P1/P2 — oraz niepełny panel 1
i brak kolumny `decyzja`) została usunięta przez autora przed biegiem; skrypt
realizuje §10 w całości. Żadna statystyka testowa ani reguła decyzyjna nie uległy
zmianie względem wersji recenzowanej.

---

## 1. Wynik w jednym zdaniu

**Kryterium pozytywne z §8 nie zostało spełnione.** Test pierwszorzędny P1 daje
p = 0,9555 (przy p < 0,05 wymaganym), a współpierwszorzędny P2 daje p = 0,9405
(przy p < 0,10 wymaganym). Twierdzenie „okres 32–40 lat jest własnością danych"
**nie jest wsparte** przez ten test.

Zgodnie z pre-rejestrowaną **deklaracją mocy** (protokół §5), przy n = 192
i szerokości pasma ≈ 1,2 komórki rozdzielczej jest to reżim niskiej mocy. Wynik
negatywny **nie jest dowodem nieistnienia cyklu** — jest stwierdzeniem, że przy tej
długości szeregu **nadmiarowej mocy w paśmie 32–40 lat nie da się odróżnić od
procesu autoregresyjnego**. To rozróżnienie jest wiążące dla rozdziału i nie wolno
go pominąć w żadną stronę.

## 2. Tabela wszystkich uruchomień (§7 protokołu)

Wszystkie 18 uruchomień z pre-rejestrowanej listy, B = 2000, ziarno 20260810.
Orzeka **wyłącznie P1**; P2 potwierdza; pozostałe są opisowe (§9).

| ID | Seria / okno | Filtr | Stat. | Null | n | S_obs | null p95 | **p** | Rola |
|---|---|---|---|---|---|---|---|---|---|
| **P1** | A_COW_W 1816–2007 | surowa | S1 32–40 | AR(3) | 192 | 0,009616 | 0,183523 | **0,9555** | PIERWSZORZĘDNY |
| **P2** | A_COW_W 1816–2007 | surowa | S1 32–40 | blok~geom(śr.10) | 192 | 0,009616 | 0,159944 | **0,9405** | współpierwszorzędny |
| S1a | A_COW_W 1816–2007 | MA(11) | S1 32–40 | AR(3)+MA(11) | 192 | 0,027406 | 0,349462 | 0,9370 | pomocniczy |
| S1b | A_COW_W 1816–2007 | surowa | S1 32–40 | AR(1) [AIC] | 192 | 0,009616 | 0,171657 | 0,9465 | wrażliwość: rząd |
| S1c1 | A_COW_W 1816–2007 | surowa | S1 32–40 | AR(1) | 192 | 0,009616 | 0,180361 | 0,9545 | wrażliwość: rząd |
| S1c5 | A_COW_W 1816–2007 | surowa | S1 32–40 | AR(5) | 192 | 0,009616 | 0,194466 | 0,9535 | wrażliwość: rząd |
| S1d | A_COW_W 1816–2007 | surowa, bez detrend. | S1 32–40 | AR(3) | 192 | 0,009677 | 0,210203 | 0,9770 | wrażliwość: detrending |
| S1e | A_COW_W 1816–2007 | surowa | S1 **30–42** | AR(3) | 192 | 0,023584 | 0,238609 | 0,9265 | wrażliwość: pasmo |
| S2a | A_COW_W 1816–2007 | surowa | S2 (χ², T=35,1) | AR(3) | 192 | 19,4538 | 38,3472 | 0,4408 | dziedzina fazy |
| S2b | A_COW_W 1816–2007 | surowa | S2 | AR(1) [AIC] | 192 | 19,4538 | 39,2834 | 0,4613 | porównanie z sesją lutową |
| E1_S1 | A_COW_W 1914–2007 | surowa | S1 32–40 | AR(3) | 94 | 0,019096 | 0,111616 | 0,6952 | opis epoki 2 |
| E1_S2 | A_COW_W 1914–2007 | surowa | S2 | AR(3) | 94 | 25,7703 | 35,9489 | 0,2704 | opis epoki 2 |
| E2_S1 | A_COW_W 1816–1913 | surowa | S1 32–40 | AR(3) | 98 | 0,113040 | 0,196314 | 0,2774 | opis epoki 1 |
| E2_S2 | A_COW_W 1816–1913 | surowa | S2 | AR(3) | 98 | 22,0447 | 33,3165 | 0,2774 | opis epoki 1 |
| R1_S1 | A_COW_P 1816–2007 | surowa | S1 32–40 | AR(3) | 192 | 0,092406 | 0,181182 | 0,2699 | hipoteza H2 |
| R1_S2 | A_COW_P 1816–2007 | surowa | S2 | AR(3) | 192 | 31,4884 | 36,9353 | 0,1019 | hipoteza H2 |
| R2_S1 | B_UCDP 1946–2024 | surowa | S1 32–40 | AR(3) | 79 | 0,199295 | 0,219325 | 0,0965 | replikacja |
| R2_S2 | B_UCDP 1946–2024 | surowa | S2 | AR(3) | 79 | 26,8868 | 42,2663 | 0,3118 | replikacja |

**Skan S3 (opisowy, bez p, §5/§9):** maksimum χ² przy T = 40,5 lat, χ² = 21,11.
Pozycja podana wyłącznie opisowo — bez rozkładu zerowego statystyki maksymalnej
nie wolno przypisać jej wartości p (§9).

**Wariant pierwszorzędny przy B = 10000** (dodatkowy, protokół §6): P1 daje
**p = 0,9584** (S_obs = 0,009616, null p95 = 0,191402). Zgodny z biegiem B = 2000
(0,9555); zwiększenie liczby replikacji nie zmienia rozstrzygnięcia.

## 3. Reguła decyzyjna i kryterium falsyfikacji (§8)

- P1: p = 0,9555 — próg p < 0,05 **NIESPEŁNIONY**.
- P2: p = 0,9405 — próg p < 0,10 **NIESPEŁNIONY**.
- S1c: AR(1) p = 0,9545, AR(5) p = 0,9535 — brak odwrócenia (oba > 0,50, ale
  warunek pozytywny wymaga p ≤ 0,50, więc i tak nie jest spełniony).

Ponieważ P1 daje p ≥ 0,05 **i** P2 daje p ≥ 0,10, spełnione jest **kryterium
falsyfikacji z §8**: twierdzenie „okres 32–40 lat jest własnością danych"
nie jest wsparte i tak musi zostać zapisane w rozdziale.

**Konsekwencja dla rodziny 2 (§8, ostatni akapit).** Test kontrastu epok nadal
się odbywa, ale jest **warunkowy**: bada różnicę siły struktury fazowej przy
okresie *przyjętym z hipotezy*, a nie *wykazanym w danych*. To musi być widoczne
w tytule podrozdziału, nie w przypisie.

## 4. Liczba wariantów i test orzekający (§9)

Liczba wykonanych uruchomień w pre-rejestrowanej liście wynosi **18** (plus
opisowy skan S3 i dodatkowy bieg P1 przy B = 10000). **Jedynym testem orzekającym
jest P1**; P2 jest warunkiem potwierdzającym, nie alternatywą. Wartości p
pozostałych uruchomień służą wyłącznie pokazaniu, jak wynik zależy od wyborów
technicznych — nie do orzekania. Nie wybrano korzystniejszego z dwóch nulli
(P1 i P2 dają zgodny wynik negatywny).

## 5. Porównanie z sesją lutową (§11.4)

Sesja lutowa (`spectral_significance_v2.py`) raportowała `p_band` = 0,465
(1816–2007) i 0,550 (1918–2007) przy nullu **AR(18–20)** dobranym przez AIC,
na serii **sprzed korekt F1–F3**. Obecny P1 daje p = 0,9555 przy nullu **AR(3)
ustalonym z góry** na serii kanonicznej v2.

**Liczby nie są bezpośrednio porównywalne**: różnią się (a) seria (przed vs po
F1–F3), (b) rząd i sposób doboru nulla (AIC AR(18–20) vs AR(3) pre-rejestrowany),
(c) normalizacja statystyki. Kierunek różnicy (obecne p wyraźnie wyższe) jest
spójny z diagnozą przekrojową z context packu §4.1: null AR wysokiego rzędu jest
sam quasi-okresowy i zaniża p, bo potrafi naśladować hipotezę alternatywną. AR(3)
jest nullem o większej mocy rozróżniającej i to on jest pierwszorzędny — nie
odwrotnie. Żadnego wniosku o „poprawie" ani „pogorszeniu" wyniku między sesjami
nie wolno stąd wyciągać; to inne testy na innych danych.

## 6. Dwa ustalenia towarzyszące (do protokołu rodziny 2)

### 6.1 Zakres detrendingu przesądza znak kontrastu epok — ustalenie wiążące

Statystyka S2 (χ² epoch-folding, T = 35,1, faza od pierwszego roku okna) na
`A_COW_W`, dla epoki 2 (1914–2007) i epoki 1 (1816–1913), zależy jakościowo od
tego, na jakim zakresie wykonano detrending liniowy:

| Zakres detrendingu | χ² epoka 2 | χ² epoka 1 | Znak kontrastu |
|---|---|---|---|
| bez detrendingu | 14,73 | 22,23 | epoka 1 > epoka 2 (przeciwny do hipotezy) |
| **detrending w oknie** (ten kod, E1/E2) | **25,77** | **22,04** | epoka 2 > epoka 1 (zgodny z hipotezą) |
| detrending na całej serii | 18,00 | 20,54 | epoka 1 > epoka 2 (przeciwny do hipotezy) |

χ² epoki 2 waha się od 14,7 do 25,8 **wyłącznie** od tej decyzji, a **znak kontrastu
się odwraca**: tylko detrending w oknie stawia epokę 2 wyżej. Ponieważ w Teście 1
E1/E2 mają charakter wyłącznie opisowy (§7), **nie wyciągamy z tego żadnego wniosku
o kontraście epok**. Ustalenie jest jednak wiążące dla rodziny 2: **zakres
detrendingu musi być zadeklarowany w protokole rodziny 2 przed policzeniem
jakiejkolwiek statystyki** — inaczej znak rdzeniowego wyniku tezy zależy od wyboru
podjętego po zobaczeniu danych (zakaz nr 10). Zapisane również w `CPS_DECISION_LOG.md`
(D-004).

Uwaga porządkowa: liczby te nie są porównywalne z χ² z sesji lutowej (14,53 / 6,97
w context packu §2), które używały fazy `rok mod T` od roku 0; przy tej konwencji
detrending w oknie daje 11,25 / 15,03, a na serii MA(11) — 6,97 / 14,53 (odtworzenie
liczb lutowych). Konwencja fazy jest drugą osią nieporównywalności.

### 6.2 Rząd AR wybrany przez AIC — domknięcie wątku lutowego

AIC (pmax = 20) na `A_COW_W` 1816–2007 po detrendingu wybiera **AR(1)**. Na tej
samej serii po wygładzeniu MA(11) wybiera **AR(13)**, z płaskim minimum w okolicy
rzędów 17–18. Potwierdza to, że rząd **18–20 z sesji lutowej był artefaktem
wygładzania**, a nie własnością danych: wygładzanie 11-letnie wprowadza
długozasięgową autokorelację, którą AIC „wypełnia" wysokim rzędem AR. Na serii
surowej właściwy null jest niski (AR(1) wg AIC, AR(3) wg parsymonii Boxa–Jenkinsa),
co jest zgodne z uzasadnieniem doboru nulla w protokole §6. Warianty S1b/S2b w tym
teście uruchamiają AIC na serii po detrendingu (surowej) i również dają niski rząd
(AR(1)) — patrz tabela §2.

## 7. Produkty

| Plik | Zawartość |
|---|---|
| `test1_band_power.py` | kod (v1.0), zrealizowany protokół v1.0 |
| `test1_band_power.md` | bliźniaczy dokument, kod bajt-w-bajt zgodny z `.py` |
| `test1_results.csv` | 18 wierszy, nagłówek `#` z wersją, ziarnem, B, sha256 wejścia |
| `test1_diagnostics.pdf` | 4 panele §10: (1) serie surowe i po detrendingu; (2) periodogram z pasmem 32–40; (3) rozkłady zerowe P1/P2 z wartością obserwowaną i 95. percentylem; (4) skan S3 |
| `TEST1_REPORT.md` | ten raport |

## 8. Granice wniosku (§11.5)

Test mierzy **udział mocy w paśmie 32–40 lat względem pasma 4–100 lat** i porównuje
go z dwoma modelami zerowymi. Nie mierzy i nie orzeka o: kontraście epok
(rodzina 2), przyczynie ewentualnego rytmu, zdolności predykcyjnej, ani o hipotezie
H2 (seria `A_COW_P` raportowana obok jako opis, nie jako test H2 — R1). Wartość p
**nie jest** prawdopodobieństwem hipotezy. Wynik R2 na `B_UCDP` (p = 0,0965 dla S1)
jest opisowy i nie zmienia rozstrzygnięcia P1; pozostaje otwartym problemem z
context packu §4.3, nie jego rozwiązaniem.
