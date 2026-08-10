# TEST 1 — PROTOKÓŁ: czy okres 32–40 lat jest własnością danych

**Rodzina 1** (zwija zarzuty Z3, Z4 i Z14 z ADDENDA A Tryptyku, s. 142–143)
**Wersja protokołu:** 1.0 · **Status:** zamrożony przed uruchomieniem kodu
**Seria pierwszorzędna:** `A_COW_W` (decyzja D-001)

Kolejność obowiązkowa: protokół → kod → przegląd autora → uruchomienie → raport.
Żadna decyzja metodyczna nie zapada po zobaczeniu wyników. Jeżeli wynik podpowiada
inny test, powstaje **nowy** protokół z jawną adnotacją, że napisano go po obejrzeniu
poprzedniego.

---

## 1. Pytanie

Czy w serii konfliktów istnieje nadmiarowa moc w paśmie okresów **32–40 lat**,
większa niż daje proces autoregresyjny bez składowej okresowej?

To jest pytanie **poprzedzające** hipotezę H1. Test kontrastu epok (rodzina 2)
mierzy różnicę siły struktury fazowej między epokami przy *założonym* okresie;
jeżeli okres nie jest własnością danych, ta różnica dotyczy wielkości nieokreślonej.

Test **nie** rozstrzyga o kontraście epok, o przyczynie ewentualnego rytmu ani
o zdolności predykcyjnej.

## 2. Trzy zarzuty, na które odpowiada

| | Zarzut | Odpowiedź konstrukcyjna |
|---|---|---|
| **Z3** | wygładzanie 11-letnie tworzy sztuczny cykl | test **pierwszorzędny liczony na serii surowej**; wariant wygładzony tylko pomocniczo, z tym samym filtrem nałożonym na surogaty |
| **Z4** | sinusoida została wymuszona dopasowaniem | statystyką jest **udział mocy w paśmie**, nie R² dopasowania; `curve_fit` nie występuje w tym teście |
| **Z14** | cykl jest artefaktem kalendarza i filtrów | dwa niezależne modele zerowe: parametryczny AR(3) i nieparametryczny bootstrap blokowy |

Efekt Slutsky'ego–Yule'a (Slutsky 1937; Yule 1927) — filtr średniej ruchomej
nałożony na szum generuje pozorne oscylacje niskiej częstotliwości — jest tu głównym
zagrożeniem. Neutralizujemy go dwojako: przenosząc test na serię surową
i nakładając identyczny filtr na surogaty tam, gdzie wariant wygładzony występuje.

## 3. Dane

Wejście: `cps_canonical_v2.csv` (wygenerowany lokalnie ze skryptu
`test0c_build_canonical.py`, kontrola wyjścia wg §3.2 briefu).

| Wariant | Zakres | Rola w tym teście |
|---|---|---|
| `A_COW_W` | 1816–2007 | **pierwszorzędny** |
| `A_COW_P` | 1816–2007 | raportowany obok (hipoteza H2) |
| `B_UCDP` | 1946–2024 | replikacja na niezależnym kodowaniu |

Kolumny: `value` (surowa) do testów głównych, `value_ma11c` do wariantu pomocniczego.
`value_ma11t` w tym teście nie występuje — nie badamy tu wyprzedzania w czasie.
Serie `C_SPLICED_*` **nie są używane**.

## 4. Przygotowanie serii

1. **Detrending liniowy** (OLS na czasie), obowiązkowy dla wszystkich serii i dla
   każdego surogatu osobno. Uzasadnienie: liczba państw w systemie rośnie
   monotonicznie, więc seria ma składową sekularną, która przecieka do niskich
   częstotliwości i zawyża moc w badanym paśmie.
2. **Okno Hanna** przed transformatą, dla ograniczenia przecieku widmowego
   (Harris 1978; Percival & Walden 1993).
3. Bez centrowania poza detrendingiem, bez normalizacji wariancji — statystyka
   jest ilorazem, więc skala się skraca.

## 5. Statystyki testowe

**S1 — udział mocy w paśmie (pierwszorzędna).**

```
S1 = Σ PSD(f) dla f ∈ [1/40, 1/32]  ÷  Σ PSD(f) dla f ∈ [1/100, 1/4]
```

Periodogram bez uśredniania segmentowego (n ≈ 190 nie pozwala na Welcha bez utraty
rozdzielczości: Δf ≈ 1/190 ≈ 0,0053 1/rok, a szerokość pasma 32–40 lat to
0,0250–0,0313, czyli ok. 1,2 komórki). Mianownik ogranicza się do pasma 4–100 lat,
żeby wykluczyć składową zerową i nierozdzielczalne bardzo niskie częstotliwości.

**Uzupełnienie zerami ×4** przed transformatą. Bez niego pasmo zawiera dokładnie
dwie komórki Fouriera (okresy 38,4 i 32,0 roku), a hipotetyczne T = 35,1 wypada
dokładnie między nimi. Uzupełnienie zerami zagęszcza próbkowanie widma i usuwa
tę arbitralność; **nie zwiększa rozdzielczości** i nie może być tak przedstawiane.
Ten sam zabieg stosuje się do każdego surogatu.

**Deklaracja mocy testu, przed uruchomieniem.** Przy n = 192 pasmo 32–40 lat ma
szerokość 1,2 komórki rozdzielczej, a szereg mieści ok. 5,5 cyklu hipotetycznego
okresu (w epoce post-1914 — ok. 2,7). To jest reżim niskiej mocy: test wykryje
tylko składową o dużej amplitudzie i stabilnej fazie. **Wynik negatywny nie będzie
zatem dowodem nieistnienia cyklu, tylko stwierdzeniem, że przy tej długości szeregu
nie da się go odróżnić od procesu autoregresyjnego.** To rozróżnienie musi znaleźć
się w raporcie i w rozdziale; jego pominięcie byłoby nadinterpretacją w drugą stronę.

**S2 — χ² epoch-folding przy T = 35,1 (pomocnicza, dziedzina fazy).**
10 koszy fazowych, χ² = Σ nₖ(mₖ − m̄)² / s², zgodnie z Leahy i in. (1983)
oraz Schwarzenberg-Czerny (1989). Komplementarna wobec S1: wykrywa strukturę
niesinusoidalną, której periodogram nie widzi.

**S3 — skan χ² po T ∈ [28, 48] co 0,5 roku (wyłącznie opisowa).**
Raportowana jest pozycja maksimum, **bez wartości p**, chyba że policzy się
rozkład zerowy dla statystyki maksymalnej po całym skanie — i tylko wtedy p wolno podać.

## 6. Modele zerowe

**N1 — AR(3), rząd ustalony z góry (pierwszorzędny).**
Uzasadnienie teoretyczne, nie optymalizacyjne: dla rocznych szeregów
makrospołecznych zasada parsymonii Boxa–Jenkinsa wskazuje p ≤ 5; merytorycznie
trzy lata odpowiadają inercji zaangażowania w konflikt (typowa wojna trwa 1–4 lata,
więc rok *t* zależy od kilku poprzednich). Współczynniki estymowane metodą
Yule'a–Walkera na serii po detrendingu, surogaty generowane rekurencyjnie
z resztami losowanymi z rozkładu empirycznego (bootstrap parametryczny;
Davison & Hinkley 1997).

**Dlaczego nie AR wybrany przez AIC.** Na n ≈ 190 AIC wybiera AR(18–20), co zużywa
~10% stopni swobody i daje null, który sam jest quasi-okresowy — zespolone pierwiastki
wielomianu charakterystycznego potrafią odtworzyć oscylację o T ≈ 35. Model zerowy
zdolny naśladować hipotezę alternatywną nie ma mocy rozróżniającej. W sesji lutowej
udokumentowano skrajny przypadek: 61% surogatów AR(20) miało stabilniejszą fazę
niż dane rzeczywiste. Wariant AIC jest mimo to raportowany (§7, S2b) — zgodnie
z zakazem nr 3, nigdy nie podajemy tylko jednego rzędu.

**N2 — stacjonarny bootstrap blokowy (Politis & Romano 1994), średnia długość
bloku 10 lat, rozkład geometryczny.** Zachowuje zależność krótkozasięgową
i rozkład brzegowy, niszczy strukturę o okresie 32–40 lat. Model nieparametryczny,
więc niezależny od poprawności założenia AR. Wynik zgodny w N1 i N2 jest znacznie
mocniejszy niż w którymkolwiek osobno.

**Replikacje:** B = 2000 dla każdego wariantu, ziarno `20260810`. Błąd Monte Carlo
przy p ≈ 0,10 wynosi ok. ±0,007, co wystarcza do rozstrzygnięć przy α = 0,05.
Dla wariantu pierwszorzędnego dodatkowo B = 10000, jeżeli czas wykonania pozwala.

**Wartość p:** jednostronna, `p = (1 + #{S_sur ≥ S_obs}) / (B + 1)`.

## 7. Pre-rejestrowana lista uruchomień

Wykonywane są **wszystkie** poniższe. Raportowane są **wszystkie**, także te
o wyniku niekorzystnym. Żadne nie może zostać dodane po zobaczeniu rezultatów.

| ID | Seria | Filtr | Statystyka | Null | Rola |
|---|---|---|---|---|---|
| **P1** | `A_COW_W` 1816–2007 | surowa | S1 | AR(3) | **PIERWSZORZĘDNY** |
| **P2** | `A_COW_W` 1816–2007 | surowa | S1 | blok 10 | współpierwszorzędny |
| S1a | `A_COW_W` | MA(11) | S1 | AR(3) + ten sam MA(11) na surogatach | pomocniczy |
| S1b | `A_COW_W` | surowa | S1 | AR(p) wg AIC | wrażliwość na rząd |
| S1c | `A_COW_W` | surowa | S1 | AR(1) i AR(5) | wrażliwość na rząd |
| S1d | `A_COW_W` | surowa, bez detrendingu | S1 | AR(3) | wrażliwość na detrending |
| S1e | `A_COW_W` | surowa | S1, pasmo 30–42 | AR(3) | wrażliwość na granice pasma |
| S2a | `A_COW_W` | surowa | S2 (χ², T=35,1) | AR(3) | dziedzina fazy |
| S2b | `A_COW_W` | surowa | S2 | AR(p) wg AIC | porównanie z sesją lutową |
| S3 | `A_COW_W` | surowa | S3 (skan) | — | opisowy |
| E1 | `A_COW_W` 1914–2007 | surowa | S1, S2 | AR(3) | opis epoki 2 |
| E2 | `A_COW_W` 1816–1913 | surowa | S1, S2 | AR(3) | opis epoki 1 |
| R1 | `A_COW_P` 1816–2007 | surowa | S1, S2 | AR(3) | hipoteza H2 |
| R2 | `B_UCDP` 1946–2024 | surowa | S1, S2 | AR(3) | replikacja niezależna |

E1 i E2 mają charakter **opisowy** — formalne porównanie epok należy do rodziny 2
i wymaga własnego protokołu. Tutaj nie wolno wyciągać z nich wniosku o kontraście.

## 8. Reguła decyzyjna i kryterium falsyfikacji

**Wynik pozytywny** (okres jest własnością danych) wymaga łącznie:
- P1: p < 0,05, **oraz**
- P2: p < 0,10, **oraz**
- brak odwrócenia kierunku w S1c (żaden z wariantów AR(1)/AR(5) nie daje p > 0,50).

**Wynik negatywny — kryterium falsyfikacji.** Jeżeli P1 daje p ≥ 0,05 **lub**
P2 daje p ≥ 0,10, twierdzenie „okres 32–40 lat jest własnością danych"
**nie jest wsparte** i tak musi zostać zapisane w rozdziale.

Konsekwencja dla rodziny 2: przy wyniku negatywnym test kontrastu epok nadal się
odbywa, ale jest opisany jako **warunkowy** — bada różnicę siły struktury fazowej
przy okresie *przyjętym z hipotezy*, a nie *wykazanym w danych*. Ta różnica musi
być widoczna w tytule podrozdziału, nie w przypisie.

**Wynik niejednoznaczny** (P1 < 0,05, P2 ≥ 0,10 lub odwrotnie) raportowany jest
jako niejednoznaczny. Nie wolno wybrać korzystniejszego z dwóch nulli.

## 9. Kontrola wielokrotnego testowania

Testem pierwszorzędnym jest **wyłącznie P1**; P2 jest warunkiem potwierdzającym,
nie alternatywą. Pozostałe uruchomienia mają charakter opisowy i ich wartości p
nie służą do orzekania — służą do pokazania, jak wynik zależy od wyborów
technicznych. W raporcie ma się znaleźć zdanie wprost: *„liczba wykonanych
wariantów wynosi N; jedynym testem orzekającym jest P1"*.

Skan po T (S3) **nie generuje wartości p** przy statystyce maksymalnej bez własnego
rozkładu zerowego. Jeżeli Code chce podać p dla maksimum skanu, musi wygenerować
rozkład zerowy statystyki `max_T χ²(T)` po tym samym skanie — inaczej wartość jest
zawyżona wielokrotnym wyborem.

## 10. Produkty

| Plik | Zawartość |
|---|---|
| `test1_band_power.py` | kod |
| `test1_band_power.md` | ten sam kod jako dokument do niezależnej oceny |
| `test1_results.csv` | jeden wiersz na uruchomienie: ID, seria, filtr, statystyka, null, n, B, S_obs, percentyl 95 rozkładu zerowego, p, decyzja |
| `test1_diagnostics.pdf` | panel 1: serie surowe i po detrendingu; panel 2: periodogramy z zaznaczonym pasmem 32–40; panel 3: histogramy rozkładów zerowych dla P1 i P2 z zaznaczoną wartością obserwowaną; panel 4: skan S3 |
| `TEST1_REPORT.md` | raport wg §11 |

Każdy plik wyjściowy z nagłówkiem `#` zawierającym wersję skryptu, sha256 wejścia,
ziarno i liczbę replikacji.

## 11. Wymagana zawartość raportu

1. Tabela wszystkich uruchomień z §7, z wartościami p.
2. Jawne zdanie o tym, czy kryterium z §8 zostało spełnione.
3. Zdanie o liczbie wykonanych wariantów i o tym, że orzeka wyłącznie P1.
4. Porównanie z wynikami sesji lutowej (`spectral_significance_v2`: p_band 0,465
   i 0,550 przy nullu AR(18–20) na serii sprzed korekt F1–F3) — z zaznaczeniem,
   że seria i null są inne, więc liczby nie są bezpośrednio porównywalne.
5. Żadnego twierdzenia wykraczającego poza to, co mierzy statystyka.

## 12. Czego Code nie decyduje samodzielnie

Rząd i typ nulla, granice pasma, długość bloku, liczba koszy fazowych, wybór testu
pierwszorzędnego, granice epok, kryterium falsyfikacji. Wszystko to jest ustalone
powyżej. Przy wątpliwości — zatrzymaj się i zapytaj, nie improwizuj wariantu.

Jeżeli którykolwiek wariant okaże się niewykonalny technicznie, zgłoś to zamiast
podmieniać na zbliżony.

## 13. Literatura

- Slutsky, E. (1937). *The Summation of Random Causes as the Source of Cyclic Processes*. Econometrica 5(2).
- Yule, G.U. (1927). *On a Method of Investigating Periodicities in Disturbed Series*. Phil. Trans. R. Soc. A 226.
- Priestley, M.B. (1981). *Spectral Analysis and Time Series*.
- Percival, D.B. & Walden, A.T. (1993). *Spectral Analysis for Physical Applications*.
- Harris, F.J. (1978). *On the Use of Windows for Harmonic Analysis*. Proc. IEEE 66(1).
- Politis, D.N. & Romano, J.P. (1994). *The Stationary Bootstrap*. JASA 89(428).
- Davison, A.C. & Hinkley, D.V. (1997). *Bootstrap Methods and Their Application*.
- Leahy, D.A. i in. (1983). *On Searches for Pulsed Emission with Application to Four Globular Cluster X-ray Sources*. ApJ 266.
- Schwarzenberg-Czerny, A. (1989). *On the Advantage of Using Analysis of Variance for Period Search*. MNRAS 241.
- Box, G.E.P., Jenkins, G.M. & Reinsel, G.C. (2008). *Time Series Analysis: Forecasting and Control*, wyd. 4.
