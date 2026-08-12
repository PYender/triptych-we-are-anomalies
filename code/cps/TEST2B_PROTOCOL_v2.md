# TEST 2B — PROTOKÓŁ v2.0: natężenie zaburzeń a odchylenie od rytmu

**Rodzina 8, model 2** · **Wersja 2.0 — ZAMROŻONA**
**Data zamrożenia:** 11 sierpnia 2026, przed obliczeniem jakiejkolwiek statystyki testowej
**Zastępuje:** wersję 1.0 (okna zdarzeń) — powód zmiany w §0

---

## 0. Dlaczego v2.0 zastępuje v1.0

Wersja 1.0 dzieliła lata na „objęte oknem zaburzenia" i „pozostałe" i porównywała
średnie odchylenie w obu grupach. Po wygenerowaniu list z progów zewnętrznych
okazało się, że przy oknie L = 5 zdarzenia pokrywają **79%** okresu 1900–2007,
a przy L = 3 — **60%**. Reguła awaryjna z v1.0 §5 (skrócenie okna) nie ratuje
sytuacji, bo oba warianty przekraczają sufit 50%. Grupa odniesienia liczyłaby
23 lata na 108, więc porównanie grup nie mierzyłoby tego, co miało mierzyć.

**Zmiana dotyczy statystyki, nie danych.** Listy zdarzeń, progi i kryteria
pozostają bez zmian — nic nie jest usuwane ani zaostrzane po zobaczeniu wyników.
Zmienia się sposób, w jaki lista jest przekładana na zmienną objaśniającą:
z podziału zero-jedynkowego na **natężenie**.

Zmiana została podjęta po zobaczeniu pokrycia, ale **przed** policzeniem
jakiejkolwiek statystyki wiążącej odchylenia z zaburzeniami. Zgodnie z zakazem nr 10
fakt ten jest odnotowany, a v1.0 pozostaje w repozytorium jako zapis.

**Obserwacja uboczna, do rozdziału.** Sam fakt, że przy obiektywnych progach cztery
piąte XX wieku znajduje się w cieniu jakiegoś zdarzenia globalnego, jest wynikiem
merytorycznym: hipoteza tłumienia zakłada, że zaburzenia są wyjątkami. Nie są.

## 1. Hipoteza

**H8.2′** — Im większe natężenie zdarzeń zaburzających w danym roku i w latach
bezpośrednio poprzedzających, tym **niższa** aktywność wojenna względem regularnego
rytmu o okresie 32–40 lat.

Predykcja kierunkowa: współczynnik przy natężeniu **ujemny**.

**Test jest warunkowy** — zakłada rytm, którego Test 1 nie potwierdził, i pyta
wyłącznie o strukturę odchyleń od niego. Wynik pozytywny nie dowodzi istnienia cyklu.

## 2. Dane i konstrukcja odchylenia

Wejście: `cps_canonical_v2.csv`, wariant **`A_COW_W`**, kolumna `value` (surowa).

1. Detrending liniowy na całej serii 1816–2007 (jeden raz, nie w oknach — D-004).
2. Dopasowanie sinusoidy o **ustalonym okresie T = 35,1** (wartość z Tryptyku,
   s. 73). Estymowane wyłącznie amplituda i faza.
3. `d(t) = obserwacja(t) − przewidywanie cyklu(t)`.

Sinusoida jest **układem odniesienia, nie wynikiem** (zakaz nr 1). Do raportu
obowiązkowo: ta sama procedura daje 35,1 na serii sprzed korekt F1–F3 i **42,9**
na serii poprawionej (D-005). T = 35,1 przyjmujemy, by testować hipotezę
w jej oryginalnej postaci.

## 3. Zmienna objaśniająca: natężenie zaburzeń

```
S(t) = Σ_zdarzenia  w(t − rok_zdarzenia)
```
gdzie `w(k) = 1` dla `k ∈ {0, 1, 2, 3, 4}` i `0` w przeciwnym razie.

Czyli `S(t)` = liczba zdarzeń, których pięcioletni cień obejmuje rok *t*.
Przyjmuje wartości całkowite od 0 wzwyż; w latach o wielu nakładających się
zdarzeniach jest odpowiednio wyższa. To jest jedyna różnica wobec v1.0, gdzie
`S(t)` była binaryzowana do 0/1.

**Wszystkie zdarzenia mają wagę 1.** Ważenie „siłą" zdarzenia wprowadziłoby
swobodę niedającą się zadeklarować obiektywnie.

**Warianty zaniku, zadeklarowane z góry:** prostokątny `w(k) = 1` dla k ≤ 4
(podstawowy), oraz wykładniczy `w(k) = exp(−k/3)` dla k ≤ 9 (wrażliwość).

## 4. Listy zdarzeń — bez zmian wobec v1.0

Progi z v1.0 §2 obowiązują bez modyfikacji. Lista wynikowa: **39 zdarzeń**,
10 przed 1900 i 29 po 1900.

| kategoria | n | próg | źródło |
|---|---|---|---|
| trzęsienia ziemi | 13 | Mw ≥ 8,5 | USGS, *20 Largest Earthquakes since 1900* |
| pandemie | 12 | ≥ 3 kontynenty | **do weryfikacji źródłowej przez Code** |
| ENSO | 5 | Super El Niño | Webb i in. 2022, *Int. J. Climatol.* 42 |
| wulkany | 4 | VEI ≥ 6 | Smithsonian GVP, *Volcanoes of the World* |
| układy rozbrojeniowe | 3 | wielostronne, globalne | **do weryfikacji** |
| szoki naftowe | 2 | > 50% r/r | **do weryfikacji** |

**Zakaz redakcji obowiązuje.** Żadna pozycja nie może zostać usunięta ani dodana
po zobaczeniu wyników. Kategorie oznaczone „do weryfikacji" wymagają potwierdzenia
źródła; jeżeli dla którejś pozycji źródła nie ma, jest **usuwana przed liczeniem**
i fakt ten odnotowany — ale nie na podstawie tego, jak wpływa na wynik.

**Znane obciążenia, deklarowane przed uruchomieniem:**
- katalog trzęsień zaczyna się w 1900 — zero zdarzeń tej kategorii przed 1900;
- osiem z trzynastu trzęsień przypada na lata 1946–1965, czyli na powojenny spadek
  serii wojennej; to jest zbieżność, którą wariant S5 ma wykryć;
- ENSO przed 1950 to rekonstrukcja, nie pomiar CPC.

## 5. Model i statystyka

Regresja liniowa `d(t) = α + β·S(t) + ε(t)`.

**Statystyka testowa: β.** Hipoteza przewiduje **β < 0**. Test jednostronny.

Nie stosujemy błędów standardowych z regresji OLS — reszty są autoskorelowane,
więc byłyby zaniżone. Istotność wyłącznie z modelu zerowego (§6).

## 6. Model zerowy

**Wyczerpujące przesunięcie cykliczne.** Wektor `S(t)` przesuwany cyklicznie
o k = 1…n−1 lat względem `d(t)`; β liczone ponownie dla każdego przesunięcia.

Zachowuje autokorelację obu szeregów, rozkład wartości `S`, skupienia zdarzeń
i ich odstępy; niszczy wyłącznie wzajemne wyrównanie w czasie. Test **wyczerpujący**,
p dokładne, bez ziarna losowego.

```
p = (1 + #{β_przesunięte ≤ β_obs}) / n
```
Dla okresu 1900–2007 (n = 108) najmniejsze osiągalne p ≈ 0,0093.

## 7. Stratyfikacja i lista uruchomień

Podział na 1900 dotyczy **jakości katalogów, nie treści hipotezy** — nie mylić
z podziałem na 1914. Podokresy nie są łączone formalnie (metoda Fishera zakazana,
errata).

| ID | Wariant | Rola |
|---|---|---|
| **Q1** | 1900–2007, zanik prostokątny L=5, T=35,1, `A_COW_W` | **PIERWSZORZĘDNY — ORZEKA** |
| Q2 | 1816–1899 | opisowy (brak trzęsień w katalogu) |
| Q3 | 1816–2007 | opisowy |
| S1 | zanik wykładniczy exp(−k/3) | wrażliwość: kształt zaniku |
| S2 | T = 32 i T = 40 | wrażliwość: przyjęty okres |
| S3 | z wyłączeniem lat 1914–1918 i 1939–1945 | **obowiązkowy** — czy wynik nie jest funkcją dwóch wojen światowych |
| S4 | seria `A_COW_P` | hipoteza H2 |
| **S5** | każda kategoria osobno | **obowiązkowy** — czy wynik nie jest funkcją skupienia trzęsień 1946–1965 |
| S6 | `d(t)` wobec COLOR w tym samym modelu | drugi, niezależny pomiar tłumienia |
| T1 | udział wojen międzypaństwowych oraz relacja `A_COW_W` do `A_COW_P` przed i po 1945 | zdarzenie przekształcające (v1.0 §3a) |

Orzeka wyłącznie **Q1**.

## 8. Reguła decyzyjna i kryterium falsyfikacji

**Wynik pozytywny:** Q1 daje β < 0 **oraz** p < 0,05 **oraz** S3 nie odwraca znaku
**oraz** S5 pokazuje, że efekt nie pochodzi z jednej kategorii.

**Kryterium falsyfikacji — obowiązuje bezwarunkowo.** Jeżeli Q1 daje p ≥ 0,05
lub β ≥ 0, hipoteza tłumienia cyklu przez zdarzenia zewnętrzne **nie jest wsparta**.
Wówczas:

- nie wolno zmieniać progów, list ani kształtu zaniku;
- nie wolno przechodzić na kolejną, luźniejszą postać hipotezy;
- nie wolno tłumaczyć wyniku niedoskonałością metody bez wskazania **konkretnej,
  nazwanej własności** testu, która go dyskwalifikuje;
- rozdział zapisuje, że argument o tłumieniu został sprawdzony i nie znalazł
  potwierdzenia.

**To jest ostatnia postać modelu 2.** Wersja 1.0 upadła z powodu wykonalności,
nie wyniku. Jeżeli v2.0 upadnie z powodu wyniku, model 2 jest zamknięty.
Pozostają modele 1 (dryf fazy) i 3 (zmienna amplituda) z rodziny 8 — jako
odrębne hipotezy z własnymi protokołami, nie jako kolejne złagodzenie tej.

## 9. Ograniczenia deklarowane przed uruchomieniem

1. Test warunkowy — zakłada cykl, którego Test 1 nie wykazał.
2. T = 35,1 pochodzi z procedury dającej 42,9 na serii poprawionej (D-005).
3. Trzy pozycje z listy C9 Tryptyku są nietestowalne (v1.0 §3b): koszty wyczerpania
   (endogeniczne), współzależność handlowa (bez daty), Koncert Europy (przed serią).
4. Katalog trzęsień nie sięga przed 1900; ENSO przed 1950 to rekonstrukcja.
5. `S(t)` przyjmuje wartość dodatnią w 79% lat okresu 1900–2007 — zmienność
   objaśniająca pochodzi więc z *natężenia*, nie z kontrastu „zaburzenie / brak".

## 10. Produkty

`test2b_disturbance.py` + bliźniaczy `.md`; `test2b_events.csv` (z kolumną źródła
i statusem weryfikacji każdej pozycji); `test2b_results.csv`; `test2b_diagnostics.pdf`
(panel 1: seria z sinusoidą; panel 2: `d(t)` i `S(t)` na wspólnej osi czasu;
panel 3: rozkład β po wszystkich przesunięciach z wartością obserwowaną;
panel 4: β osobno dla każdej kategorii, wariant S5); `TEST2B_REPORT.md`.

Raport zawiera obowiązkowo: liczbę zdarzeń w rozbiciu na kategorie i podokresy,
rozkład wartości `S(t)`, zdanie o spełnieniu lub niespełnieniu kryterium z §8,
oraz zdanie o liczbie wariantów z przypomnieniem, że orzeka wyłącznie Q1.

## 11. Literatura

- Good, P. (2005). *Permutation, Parametric, and Bootstrap Tests of Hypotheses*, wyd. 3.
- Box, G.E.P. & Tiao, G.C. (1975). *Intervention Analysis with Applications to Economic and Environmental Problems*. JASA 70(349).
- Newhall, C.A. & Self, S. (1982). *The Volcanic Explosivity Index (VEI)*. J. Geophys. Res. 87(C2).
- Robock, A. (2000). *Volcanic Eruptions and Climate*. Rev. Geophys. 38(2).
- Webb, M.J. i in. (2022). *The Ensemble Oceanic Niño Index*. Int. J. Climatol. 42.
