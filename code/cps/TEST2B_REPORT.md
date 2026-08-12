# TEST 2B — RAPORT: natężenie zaburzeń a odchylenie od rytmu

**Rodzina 8, model 2** · **Realizuje:** `TEST2B_PROTOCOL_v2.md` (zamrożony)
**Kod:** `test2b_disturbance.py` v1.0 · **Data biegu:** 2026-08-12
**Wejście:** `cps_canonical_v2.csv` (sha256 `145aed00…`), `test2b_events.csv`
(sha256 `555108fb…`, 34 zdarzenia po D-007)
**Null:** wyczerpujące przesunięcie cykliczne — p dokładne, bez ziarna losowego.

---

## 1. Wynik w jednym zdaniu

**Kryterium falsyfikacji z §8 zostało spełnione.** Test pierwszorzędny Q1 daje
β = −0,0598 przy **p = 0,6389** (wymagane p < 0,05). Hipoteza H8.2′ — że natężenie
zdarzeń zaburzających obniża aktywność wojenną względem rytmu 32–40 lat —
**nie jest wsparta**. Znak β jest wprawdzie ujemny (kierunek hipotezy), ale efekt
jest nieodróżnialny od zera: β_obs leży daleko powyżej 5. percentyla rozkładu
zerowego (−0,653).

Zgodnie z §8 protokołu **to jest ostatnia postać modelu 2**. Wersja 1.0 upadła
z powodu wykonalności (pokrycie), v2.0 upada z powodu **wyniku** — więc model 2
(cykl tłumiony przez zdarzenia zewnętrzne) zostaje **zamknięty**. Nie proponuje się
wersji 3.0. Pozostają modele 1 (dryf fazy) i 3 (zmienna amplituda) z rodziny 8 jako
odrębne hipotezy z własnymi protokołami — nie jako złagodzenie tej.

## 2. Tabela wszystkich uruchomień (§7)

β z regresji d(t) = α + β·S(t); p z rozkładu przesunięć (bez błędów standardowych
OLS — B1.5). Orzeka **wyłącznie Q1**.

| ID | podokres | n | zanik | T | β_obs | null p05 | **p** |
|---|---|---|---|---|---|---|---|
| **Q1** | 1900–2007 | 108 | rect | 35,1 | −0,0598 | −0,653 | **0,6389** |
| Q2 | 1816–1899 | 84 | rect | 35,1 | −0,8153 | −0,952 | 0,1429 |
| Q3 | 1816–2007 | 192 | rect | 35,1 | −0,3656 | −0,562 | 0,2500 |
| S1 | 1900–2007 | 108 | exp | 35,1 | −0,0507 | −0,970 | 0,6481 |
| S2_T32 | 1900–2007 | 108 | rect | 32,0 | −0,0867 | −0,574 | 0,6389 |
| S2_T40 | 1900–2007 | 108 | rect | 40,0 | +0,0871 | −0,755 | 0,6389 |
| **S3** | 1900–2007 | 96 | rect | 35,1 | −0,2334 | −0,672 | 0,4375 |
| S4 | 1900–2007 | 108 | rect | 35,1 | −0,0966 | −0,800 | 0,4537 |
| S5_earthquake | 1900–2007 | 108 | rect | 35,1 | −0,8726 | −0,934 | 0,0833 |
| S5_pandemic | 1900–2007 | 108 | rect | 35,1 | +0,8184 | −1,155 | 0,8056 |
| S5_enso | 1900–2007 | 108 | rect | 35,1 | +2,2102 | −2,316 | 0,9259 |
| S5_volcano | 1900–2007 | 108 | rect | 35,1 | +0,7775 | −2,313 | 0,5926 |
| S6 | — | — | — | — | — | — | zaślepka |
| T1 | — | — | — | — | — | — | zaślepka |

Wykonano **12 uruchomień liczbowych** (10 pozycji §7, z S2 i S5 rozwiniętymi na
6 wierszy) plus S6 i T1 jako zaślepki (§5). **Jedynym testem orzekającym jest Q1**;
pozostałe są opisowe i ich wartości p nie służą do orzekania.

## 3. Reguła decyzyjna i kryterium falsyfikacji (§8)

**Wynik pozytywny wymagał łącznie:** Q1 β < 0 **oraz** p < 0,05 **oraz** S3 nie
odwraca znaku **oraz** S5 pokazuje, że efekt nie pochodzi z jednej kategorii.

- **Q1: p = 0,6389 ≥ 0,05 → warunek pierwszorzędny NIESPEŁNIONY.** To samodzielnie
  przesądza wynik negatywny (§8, kryterium falsyfikacji obowiązuje bezwarunkowo).
- S3 (bez lat 1914–1918 i 1939–1945): β = −0,233, znak **zgodny** z Q1, ale również
  nieistotny (p = 0,44). Nie ratuje wyniku.
- S5 (ocena, nie próg — patrz §4): kierunek ujemny w Q1 pochodzi **wyłącznie
  z trzęsień ziemi**; trzy pozostałe kategorie mają β **dodatnie**.

Ponieważ Q1 nie spełnia progu, warunki S3 i S5 są bezprzedmiotowe dla orzeczenia —
opisujemy je poniżej, bo są wymagane w raporcie i wzmacniają diagnozę.

## 4. S5 — skąd bierze się (nieistotny) ujemny znak

Protokół żąda, by S5 pokazało, czy wynik nie jest funkcją jednej kategorii —
w szczególności skupienia **8 z 13 trzęsień ziemi w latach 1946–1965**, zbieżnego
z powojennym spadkiem serii wojennej (D-007, §4 protokołu). Rozkład β po kategoriach:

| kategoria | β | p |
|---|---|---|
| earthquake | **−0,873** | 0,083 |
| pandemic | +0,818 | 0,806 |
| enso | +2,210 | 0,926 |
| volcano | +0,778 | 0,593 |

Cały ujemny (kierunek hipotezy) sygnał w Q1 pochodzi z **jednej** kategorii —
trzęsień ziemi — i nawet ona osobno nie jest istotna (p = 0,083). Pozostałe trzy
kategorie wskazują **kierunek przeciwny** do hipotezy. Jest to dokładnie ta
zbieżność, przed którą ostrzegał protokół: gdyby Q1 wypadło istotnie, S5 i tak
zdyskwalifikowałoby wynik jako pochodzący z jednej kategorii i zbieżny czasowo
z powojennym spadkiem, a nie z tłumieniem przez zaburzenia. Nie orzekamy tego
progiem w kodzie (próg „≥2 kategorie" byłby arbitralny i niezadeklarowany) —
ocena jest tutaj, w raporcie.

## 5. Wrażliwości (opisowe)

- **Kształt zaniku (S1, exp):** β = −0,051, p = 0,648 — bez zmiany.
- **Przyjęty okres (S2):** T = 32 → β = −0,087 (p = 0,639); T = 40 → β = **+0,087**
  (p = 0,639). Znak β zmienia się z samym przyjętym okresem — potwierdza, że nie ma
  stabilnego związku natężenie–odchylenie.
- **Seria uczestnicza (S4, `A_COW_P`):** β = −0,097, p = 0,454 — również nieistotne.
- **Pełny szereg i epoka przedkatalogowa (Q3, Q2):** p = 0,250 i 0,143; opisowe,
  katalogi przed 1900 niepełne (§4 protokołu).

## 6. Uwagi metodyczne

- **Przesunięcie pozycyjne przy lukach (S3).** Q1 nie ma luk, więc test
  pierwszorzędny jest nietknięty. W S3 (usunięte lata wojen) `np.roll` przesuwa
  wektory **po pozycjach, nie po latach**, więc przesunięcie o k nie odpowiada
  dokładnie k latom; dla celu nulla — zniszczenie wyrównania przy zachowaniu
  struktury wewnętrznej obu wektorów — jest to bez znaczenia.
- **Efekt brzegowy:** `include_prewindow = True` (potwierdzone w przeglądzie).
  Jedyne zdarzenie sprzed okna zasilające S(t) w podokresie pierwszorzędnym to
  VI pandemia cholery (1899), rzucająca cień na 1900–1903; obcięcie do okna dałoby
  sztuczne zero natężenia w pierwszych latach.
- **Kalibracja nulla (przegląd autora).** Model zerowy trzyma nominalny poziom
  α = 0,05 przy autokorelacji reszt do φ = 0,9; błąd standardowy z OLS dałby przy
  φ = 0,8 aż 0,22 fałszywych odrzuceń — stąd zakaz B1.5, który kod respektuje.
- **S6 i T1 — zaślepki.** S6 (odchylenia vs COLOR) do wpięcia z
  `data/ngrams/ngram_color_rebuilt.csv` w kolejnym kroku; T1 (udział wojen
  międzypaństwowych i relacja `A_COW_W`:`A_COW_P` przed/po 1945) wymaga rozbicia
  serii COW na typy konfliktu — osobna praca. Zwracają jawny brak, nie wartość
  pozorną.

## 7. Produkty

`test2b_disturbance.py` + bliźniaczy `.md`; `test2b_events.csv` (34 + 5 removed);
`test2b_results.csv` (nagłówek `#` z wersją, T, liczbą zdarzeń, sha256 wejść);
`test2b_diagnostics.pdf` (panel 1: seria z sinusoidą; panel 2: d(t) i S(t) na
wspólnej osi; panel 3: rozkład β po przesunięciach dla Q1 z wartością obserwowaną;
panel 4: β osobno dla kategorii, S5); `TEST2B_REPORT.md`; `TEST2B_DATA_REPORT.md`
(Etap A).

## 8. Granice wniosku

Test jest **warunkowy** — zakłada rytm 32–40 lat, którego Test 1 nie potwierdził,
i pyta wyłącznie o strukturę odchyleń od niego. Wynik negatywny **nie dowodzi**, że
zaburzenia nie mają żadnego wpływu na aktywność wojenną — dowodzi, że **przy tej
liście, tym oknie i tej mierze natężenia nie ma systematycznego, wykrywalnego
tłumienia** rytmu przez zdarzenia zewnętrzne. Zgodnie z §0 protokołu wynik ten
**usuwa główny argument obronny** po Teście 1 (że test 1 nie wykrył cyklu, bo cykl
jest tłumiony): argument o tłumieniu został sprawdzony i nie znalazł potwierdzenia.
Wartość p **nie jest** prawdopodobieństwem hipotezy.
