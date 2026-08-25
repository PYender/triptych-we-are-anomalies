# TEST 6 — Krok C: wynik rzeczywisty P1(N1)/P2(N2), zgodny z §6–§8 protokołu

**Realizuje:** `TEST6_PROTOCOL.md` §6–§8 · **Poprzedza:** D-015 (Etap B), D-022 (θ̂ na
granicy), D-023 (wykrycie podmiany silnika statystycznego), D-024 (Krok A — mapowanie
S1–S8), D-026 (wada §8: N2 zdegenerowany), D-027 (autoryzacja Kroku C) · **Kod:**
`test6_null.py`, `test6_weibull.py` · **Dane:** `test6_intervals.csv` (18 diad, 45 odstępów
pełnych, 18 cenzurowanych) · **Status: bieg zamknięty. H6.1 NIEROZSTRZYGNIĘTA w ramach
zamrożonego protokołu** (nie „wsparta", nie „obalona") — z przyczyn opisanych w §4 niżej.

---

## 0. Ujawnienie wymagane przez zakaz nr 10 (D-023, w obie strony)

Ten bieg wykonano **ze znajomością dwóch wcześniejszych wyników**, obu — zgodnie z zakazem
nr 10 — ujawnionych tutaj wprost, a nie przemilczanych:

1. **Wynik metodologicznie niezgodny** (`TEST6_REPORT.md`, D-023): profil
   wiarygodności/bootstrap diadowy na tych samych danych dał k̂=0,7780, CI profilu
   (0,6029–0,9791), CI bootstrap (0,6471–0,9649) — oba wykluczają 1.
2. **Wada protokołu D-026**: N2 zdegenerowany względem k̂ pulowanego, wykryta **analitycznie,
   przed jakimkolwiek biegiem na danych rzeczywistych** — degeneracja jest własnością
   algebraiczną (`negloglik_pooled` nie używa etykiety diady), niezależną od tego, co
   pokazują dane, więc jej wykrycie nie mogło zostać zainspirowane wynikiem.

Metodologia N1/N2 (§6) NIE została zmieniona po zapoznaniu się z żadnym z tych dwóch faktów —
kod i ziarno (`SEED_PROTOCOL=20260822`) były zamrożone w Kroku B (D-024), przed tym biegiem.

## 1. P1 (N1) — wynik

| wielkość | wartość |
|---|---|
| k̂_obs (pulowany, `fit_pooled`) | **0,7780** |
| B | 2000 |
| ziarno | 20260822 (protokół, §6) |
| p = (1+#{&#124;k_sur−1&#124;≥&#124;k_obs−1&#124;})/(B+1) | **0,068** |
| k̂_sur średnie | 0,9147 |
| k̂_sur mediana | 0,9111 |
| k̂_sur odch. std | 0,0981 |
| frac_tie (zabezpieczenie D-026 §7) | 0,0 — brak degeneracji, bieg wiarygodny |

k̂_obs identyczne z analizą niezgodną (§0) — to ten sam estymator na tych samych danych,
zgodność punktowa jest oczekiwana z konstrukcji, nie jest niezależnym potwierdzeniem.

## 2. P2 (N2) — zdegenerowany, NIE liczba (D-026)

`frac_tie = 1,0` — potwierdza degenerację. `p` policzone dosłownie ze wzoru §6 na tym biegu
wynosi 0,253 (ta sama wartość, którą zmierzono w przeglądzie D-026, ziarno identyczne).
**Ta liczba nie jest raportowana jako wynik.** P2 nie niesie żadnej treści o danych — ani
w teorii (gdzie wynosiłoby tożsamościowo 1,000), ani w praktyce tego kodu (gdzie wychodzi
0,253, artefakt szumu numerycznego przy dokładnej remisie). Zjawisko opisane w D-026/D-026 §7,
nie liczba.

## 3. Reguła decyzyjna §8 — niespełnialna w sposób informacyjny

§8 protokołu wymaga trzech warunków naraz, w tym P2<0,10. Skoro P2 nie niesie treści (§2),
**żaden wynik P1 nie może uczynić reguły §8 spełnioną w sposób informacyjny** — nie dlatego,
że dane są niejednoznaczne, tylko dlatego, że jeden z trzech wymaganych warunków jest
strukturalnie niesprawdzalny. To ustalono w D-026 przed tym biegiem, niezależnie od tego,
co pokazałoby P1.

**H6.1 pozostaje NIEROZSTRZYGNIĘTA w ramach zamrożonego protokołu.** Nie „wsparta częściowo",
nie „obalona" — protokół w obecnym brzmieniu nie ma dla niej osiągalnego wyniku pozytywnego
(D-026), niezależnie od jakości czy kierunku danych.

## 4. Co P1 samo w sobie pokazuje (opisowo, poza regułą §8)

Poza regułą decyzyjną: P1 daje p=0,068, kierunek zgodny z hipotezą (k̂_obs=0,778<1, hazard
malejący/regeneracja słabnąca z kolejną wojną), i jest zgodny jakościowo (ten sam kierunek,
nie ta sama metoda) z analizą niezgodną z §0. To jest opis, nie rozstrzygnięcie — reguła §8
wymagała trzech warunków naraz, nie samego P1.

## 5. Rozbicie odchylenia N1 od 1,0 (zlecone w D-026, wykonane w Kroku B)

Średnie k̂_sur=0,9147 (nie 1,0) ma DWA źródła działające w przeciwne strony:

- **Mieszanka wykładniczych o różnych λ̂ per diada** pod jednym wspólnym k ciągnie k̂ w dół
  (mechanizm D-015/F1).
- **Obciążenie małej próby samego estymatora** (`fit_pooled`, n=45 zdarzeń) ciągnie k̂ w
  górę: zmierzone `test_censoring_bias` pod jednorodną prawdą k=1 na realnej strukturze —
  **+2,5%** (2000 powtórzeń, średnie k̂=1,0249, mediana 1,0153).

Przypisanie całego odchylenia (0,9147 vs 1,0) jednemu mechanizmowi byłoby mylące — oba
składniki działają, w przeciwnych kierunkach.

## 6. Przekroczenie okna N1 — własność konstrukcji, nie efekt uboczny (D-026 §7)

**75,5%** surogatowych replik N1 (B=500 diagnostyczne na 18 diadach, ziarno eksploracyjne) ma
Σt_sim+c przekraczające realną ekspozycję diady (zakres per-diada: 43%–97%, rośnie z udziałem
cenzurowania `c/T`). Nadmiar w oczekiwaniu równa się **dokładnie `c`**: `λ̂=n/T` implikuje
`E[Σt_sim]=T`, a dołożenie niezmienionego `c` daje `E[Σt_sim+c]=T+c`, systematycznie ponad
realne `T`.

**Konsekwencja dla odczytu P1=0,068, asymetryczna:** rozkład zerowy N1 ma zawyżoną wariancję
(surogaty generują historie dłuższe niż diada mogła realnie mieć) — to czyni test
**konserwatywnym**. Niska wartość P1 (jak tutaj, 0,068) jest więc **wiarygodna z nadwyżką**:
trudniej o nią przez przypadek, skoro null jest już rozdęty. Odwrotnie, gdyby P1 wyszło
wysokie, byłoby to **częściowo przypisywalne samej konstrukcji modelu zerowego, nie danym**.
Ta asymetria działa na korzyść wiarygodności tego konkretnego wyniku P1, ale nie zmienia
statusu H6.1 ustalonego w §3 — §8 wymaga P2, nie samego P1.

## 7. Porównanie metod jako samodzielny wynik (D-023 §5, zrealizowane)

| | analiza niezgodna (`TEST6_REPORT.md`, D-023) | Krok C (ten dokument, §6–§8) |
|---|---|---|
| metoda | profil wiarygodności + bootstrap diadowy | symulacyjny test p, model zerowy N1 (proces Poissona per diada) |
| k̂ | 0,7780 | 0,7780 (ta sama estymacja punktowa) |
| miara niepewności | CI profilu (0,603–0,979), CI bootstrap (0,647–0,965) — oba wykluczają 1 | p=0,068 względem nullu skalibrowanego na strukturę międzydiadyczną (k̂_sur≈0,91, nie 1,0) |
| reguła decyzyjna | brak (diagnostyka, D-023) | §8 protokołu — niespełnialna (P2 zdegenerowany, D-026) |
| status wobec H6.1 | żaden — dokument sam się tak opisuje | nierozstrzygnięta w ramach zamrożonego protokołu |

Obie metody wskazują w tym samym kierunku (k̂<1, przedziały/p spójne z odrzuceniem modelu bez
pamięci), ale z innej struktury wnioskowania — **zgodność kierunku dwóch różnych metod jest
odrębną obserwacją**, nie dowodem, że którakolwiek z osobna wystarczyłaby jako rozstrzygnięcie
przewidziane przez protokół. Żadna z dwóch nie zastępuje drugiej ani reguły §8.

## 8. Co pozostaje poza tym Krokiem C

- **S1–S8** (warianty wrażliwości): zmapowane merytorycznie w Kroku A
  (`TASK_6C_S1S8_MAPPING.md`, D-024), ale ich zbiory danych (poza głównym) NIE zostały
  zbudowane — ten Krok C liczy wyłącznie zbiór główny (P1/P2). Budowa S1–S8 to osobny krok,
  nieautoryzowany tym biegiem.
- **H6.2** (kontrast epokowy, S5/S6): protokół nie ma dla niej reguły decyzyjnej w §8
  (D-024) — nie dopisana teraz, pozostaje nierozstrzygnięta z innego powodu niż H6.1 (brak
  kryterium, nie wada kryterium).
- **N2 dla modelu kruchości F1** (dozwolone D-026 jako diagnostyka poza §8): niewykonane
  w tym Kroku.

## 9. Status końcowy

**H6.1: NIEROZSTRZYGNIĘTA w ramach zamrożonego `TEST6_PROTOCOL.md`.** Reguła §8 nie może
zostać spełniona w sposób informacyjny (D-026). P1 samodzielnie opisuje kierunek zgodny z
hipotezą (§4), konserwatywnie obciążony w stronę trudniejszego odrzucenia (§6), zgodny
jakościowo z niezależną, metodologicznie odmienną analizą (§7) — ale żadna z tych obserwacji
nie jest tym, co protokół pre-rejestrował jako rozstrzygnięcie. Test 6 zamknięty w tej
postaci, w jakiej dało się go uczciwie zamknąć.
