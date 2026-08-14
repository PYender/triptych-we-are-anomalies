# TEST 3 — RAPORT: analiza wielowariantowa decyzji przetwarzania

**Rodzina 4** (zarzuty Z8, Z9; realizuje zobowiązanie z D-001) · **Multiverse** (Steegen i in. 2016)
**Realizuje:** `TEST3_PROTOCOL.md` v1.0 · **Kod:** `test3_multiverse.py` · **Bieg:** 2026-08-14
**Wejście:** cztery zbiory COW + `population.csv`; serie budowane parametrycznie
(`test0c_build_canonical.py` v2.1). **Null:** AR(3), rząd z góry, B = 2000, ziarno 20260812.
**Siatka:** 192 kombinacje (2 poziomy × 4 wagi × 2 normalizacje × 2 wygładzania ×
2 detrendingi × 3 okresy). Kontrola interpolacji osobno.

Test **nie orzeka o istnieniu cyklu** — mierzy zależność wniosków od wyborów przetwarzania.

---

## 1. Wynik w jednym zdaniu

**Żadna z 192 specyfikacji nie daje istotnej mocy w paśmie (M1 p < 0,05).** Najmniejsze
osiągnięte `p_M1` w całej przestrzeni wynosi **0,11**. Odsetek specyfikacji wspierających
H1 (koniunkcja M1 p<0,05 ∧ M2>0, §6) wynosi **0%**. Reguła interpretacji §6 uruchomiona:
**„poniżej 5% — hipoteza nie broni się w przestrzeni specyfikacji; pojedyncze wyniki
wspierające byłyby oczekiwaną liczbą z 192 porównań"**. Tu nie ma nawet pojedynczych —
jest zero.

**Konsekwencja dla Testu 1.** Negatywny wynik Testu 1 **nie był specyficzny dla przyjętej
tam specyfikacji**. Brak istotności mocy w paśmie utrzymuje się na całej przestrzeni
dopuszczalnych wyborów, w tym w specyfikacji oryginalnej (jak opublikowano) i we wszystkich
wariantach wag, normalizacji, wygładzania, detrendingu i okresu.

## 2. Cztery odsetki wsparcia (§5.2)

H1 (D-002) jest **koniunkcją**: moc w paśmie **oraz** kontrast w kierunku przewidywanym.
Dlatego cztery odsetki, żeby było widać, który składnik zawodzi:

| miara | znaczenie | odsetek |
|---|---|---|
| M1 p < 0,05 | moc w paśmie obecna | **0,0%** (0/192) |
| M2 > 0 | kontrast w kierunku H1 (znak) | 77,6% (149/192) |
| **M1 p<0,05 ∧ M2>0** | **H1 jak sformułowana — orzeka §6** | **0,0%** |
| M1 p<0,05 ∧ M2 p<0,05 ∧ M2>0 | odczyt najostrzejszy | 0,0% |

**Żaden z tych odsetków nie jest wartością p** — kombinacje dzielą te same dane (§7.3
protokołu), więc odsetek wspierających nie jest prawdopodobieństwem czegokolwiek.

Zawodzi **składnik mocy w paśmie**, nie kierunek. Kontrast M2 > 0 wypada w 77,6%
specyfikacji (a M2 istotny i dodatni w 41/192 = 21%), ale **nigdy** nie towarzyszy mu
istotna moc w paśmie. Uwaga metodyczna: samo M2 > 0 przy braku efektu wypada ~50%
przypadków (rzut monetą), więc nie jest kryterium — ma sens wyłącznie w koniunkcji,
a koniunkcja jest pusta.

## 3. Specyfikacja oryginalna i pierwszorzędna (§5.1)

| specyfikacja | poziom · wagi · norm · wygł. · detr. · T | M1 | p_M1 | M2 | p_M2 |
|---|---|---|---|---|---|
| **oryginalna** (jak opublikowano) | P · inherited · raw · MA(11) · brak · 35,1 | 0,171 | 0,359 | +31,9 | 0,071 |
| **pierwszorzędna** (D-001+D-008+D-004) | W · equal · raw · brak · liniowy · 35,1 | 0,026 | 0,849 | −3,0 | 0,607 |

Uzasadnienie specyfikacji oryginalnej: wartość T = 35,1 pochodzi z dopasowania sinusoidy
do `wars_smooth` **bez detrendingu i bez normalizacji per capita** (mw-8 w kodzie v0.1);
detrending pojawiał się dopiero w periodogramie, czyli w odrębnej procedurze. Stąd
oryginalna specyfikacja ma wygładzanie MA(11), brak detrendingu, raw, poziom uczestnika.

Nawet specyfikacja **najkorzystniejsza dla tezy** (oryginalna: największy kontrast
M2 = +31,9, p_M2 = 0,071) **nie spełnia H1** — moc w paśmie nie jest istotna (p_M1 = 0,36).
Specyfikacja pierwszorzędna daje kontrast **ujemny** (epoka 1 > epoka 2) i moc nieistotną.

## 4. Rozbicie wariancji (§5.3 — udział sumy kwadratów, NIE test istotności)

Siatka jest zbalansowana (pełny czynnikowy), więc udziały SS są ortogonalne.

**M1 (moc w paśmie):**

| składnik | udział SS |
|---|---|
| poziom agregacji | 36,1% |
| wygładzanie | 21,0% |
| okres | 18,0% |
| poziom × wagi | 7,1% |
| poziom × norm | 2,9% |
| reszta (interakcje ≥2 rzędu) | 8,1% |

**M2 (kontrast epok):** poziom 32,9%, okres 14,7%, poziom×okres 7,0%, normalizacja 6,5%.

Największym źródłem zmienności wyniku jest **poziom agregacji** (W vs P), a nie zestaw
wag — wagi mają udział pomijalny (średnie M1: inherited 0,088, equal 0,085, steep 0,088,
flat 0,086). To bezpośrednia odpowiedź na zarzut Z8: **wybór wag nie steruje wnioskiem**;
steruje nim poziom agregacji (Z9 → D-001) i wygładzanie.

Kierunki (średnie M1 wg wymiaru): poziom P daje ~2,3× większy udział mocy niż W
(0,120 vs 0,053); wygładzanie MA(11) niemal podwaja go (0,112 vs 0,061) — to jest efekt
Slutsky'ego–Yule'a, przed którym ostrzegał Test 1; okres T = 32 daje więcej niż 35,1/40
(0,119 / 0,064 / 0,076). **Żadna z tych osi, ani ich złożenie, nie wypycha M1 do
istotności** — maksymalne M1 (0,28) nadal daje p_M1 = 0,11.

## 5. Wykres specyfikacji i rozkłady (§5.4, §5.1)

`test3_curve.pdf` (produkt główny): 192 wartości M1 uporządkowane rosnąco z macierzą
decyzji pod spodem — pokazuje, że rosnące M1 idzie w parze z poziomem P, wygładzaniem
i T = 32, ale próg istotności nie jest przekroczony na żadnym końcu.
`test3_diagnostics.pdf`: rozkłady M1 i M2 (ze specyfikacją oryginalną i pierwszorzędną),
rozbicie wariancji, kontrola interpolacji.

## 6. Hipoteza H2 wobec H1 (§Q3 protokołu)

Poziom uczestnika (`A_COW_P`, seria H2) zachowuje się **inaczej** niż poziom wojny
(H1): ma większy udział mocy (0,120 vs 0,053) i częściej dodatni kontrast. Ale różnica
jest ilościowa, nie jakościowa co do orzeczenia — również na poziomie P **żadna**
specyfikacja nie daje M1 p < 0,05. H2 wygląda „silniej" w opisie, lecz nie przekracza
progu istotności mocy w paśmie w żadnym wariancie.

## 7. Kontrola interpolacji ludności (zastępuje widmową kontrolę pc_1950)

Widmowa kontrola pc_1950 została **wycofana** przed uruchomieniem: przy n = 58 (1950–2007)
pasmo 32–40 lat jest węższe niż jedna komórka rozdzielcza (Δf ≈ 0,0172; ~0,38 komórki),
więc M1 mierzyłoby położenie prążka względem granic pasma, nie zawartość danych; M2 jest
tam i tak niedefiniowane (brak epoki 1). Zamiast liczyć widmo, pytamy wprost, czy
interpolacja deformuje wynik.

**Uprawnienie do przeniesienia pomiaru.** Normalizacja per capita jest **punktowa**
(wartość / ludność w tym samym roku), więc **względna deformacja serii per capita równa się
względnej deformacji mianownika**. To pozwala zmierzyć artefakt interpolacji tam, gdzie
mamy dane roczne (1950–2007), i odnieść go do okresu wcześniejszego.

**Własność tego zbioru, którą trzeba podać wprost:** węzły ludności biegną co dekadę od
1790 do 1940, a rok 1950 jest już pomiarem rocznym — więc **każdy rok z przedziału
1816–1949 leży między dwoma węzłami pomiarowymi** (np. 1941–1949 między 1940 a 1950).
**Ekstrapolacji przed 1950 nie ma w ogóle.** Bez tej informacji czytelnik nie ma jak
ocenić, który z dwóch poniższych wariantów jest właściwy.

Artefakt zmierzony na prawdzie 1950–2007 (decymacja do węzłów dekadowych → re-interpolacja
liniowa → różnica względem prawdy):

| wariant | średnia różnica | maksimum | uwaga |
|---|---|---|---|
| **zakotwiczony** (interpolacja między węzłami) | **0,22%** | **0,89%** (w środku dekady) | jedyny wierny odpowiednik pre-1950 |
| niezakotwiczony (ogon 2001–2007 ekstrapolowany) | 0,83% | 8,67% (przy 2007) | **błąd ekstrapolacji, którego w danych nie ma** |

Wariant zakotwiczony (**0,22% / 0,89%**) jest wielkością reprezentatywną. Wariant
niezakotwiczony (8,67%) pochodził z testu o niewłaściwej konstrukcji (wypełnienie ogona
płaską wartością z 2000 r. — struktura, której pre-1950 nie ma) i jest podany wyłącznie
dla jawności, poprawnie przypisany jako błąd ekstrapolacji.

**Reprezentatywność, nie ograniczenie górne.** Krzywizna logarytmu ludności na skali
dekadowej jest w obu okresach porównywalna: 2,58×10⁻² (1820–1940) wobec 2,02×10⁻²
(1950–2000), iloraz **0,78** (estymator: pierwiastek średniego kwadratu drugiej różnicy;
autor liczył średnią wartość bezwzględną i uzyskał 0,87 — kierunek ten sam). XIX wiek jest
*nieznacznie bardziej* zakrzywiony na skali dekadowej, więc błąd zmierzony na 1950–2007
jest **reprezentatywny** dla okresu wcześniejszego, a nie jego ograniczeniem górnym —
może być o kilkanaście procent zaniżony. Wniosek: interpolacja dekadowa deformuje serię
per capita o rząd **dziesiątych części procenta** średnio (<1% lokalnie), więc nie
wyjaśnia braku istotności; obciążenie z §2.1 pozostaje jawnie zadeklarowane dla okresu
sprzed 1950.

**Interakcja skali `pc_full × MA(11)`.** W kombinacjach per capita z wygładzaniem dwie
skale gładkości leżą blisko: sztuczna ~10-letnia gładkość mianownika (interpolacja
dekadowa do 1940) i okno MA(11). Mogą się nałożyć i wzmocnić gładkość w paśmie sąsiadującym
z badanym. Nie jest to błąd potoku (normalizacja jest przed filtrami, B2.4), lecz
obciążenie: udział mocy w tych kombinacjach należy czytać z tą świadomością. W praktyce
nie zmienia orzeczenia — również `pc_full × MA(11)` nie daje M1 p < 0,05.

## 8. Reguła interpretacji i granice wniosku

**Reguła §6 uruchomiona:** wynik < 5% (dokładnie 0%) → **hipoteza H1 nie broni się
w przestrzeni dopuszczalnych specyfikacji.** Decyzją rozdzielającą specyfikacje
„najbliższe wsparcia" od reszty jest przede wszystkim **poziom agregacji** i **wygładzanie**
— ale nawet ich najkorzystniejsze złożenie nie przekracza progu istotności.

Granice (§C2, obowiązkowe):
- Test **nie orzeka o istnieniu cyklu** — orzeka o wrażliwości wniosku na wybory.
- Odsetek wspierających **nie jest** prawdopodobieństwem czegokolwiek (kombinacje dzielą dane).
- Wynik **nie dotyczy** cyklu o dryfującej fazie — ta hipoteza wymaga innych narzędzi
  (D-009, rodzina 8 model 1) i nie jest przedmiotem tego testu.

## 9. Produkty

`test3_multiverse.py` + bliźniaczy `.md`; `test3_results.csv` (192 wiersze: wszystkie
wymiary + M1, M2, p_M1, p_M2, nagłówek `#` z wersją, ziarnem, B, sha buildera i kontrolą
interpolacji); `test3_curve.pdf` (wykres specyfikacji — produkt główny); `test3_diagnostics.pdf`
(rozkłady, rozbicie wariancji, kontrola interpolacji); `TEST3_REPORT.md`; `TEST3_BUILDER_REPORT.md`
(Etap A). Bieg reprodukowalny: ziarno 20260812, B = 2000, jedno ziarno na cały bieg.
