# TEST 2B — RAPORT DANYCH (Etap A: weryfikacja listy zdarzeń)

**Protokół nadrzędny:** `TEST2B_PROTOCOL_v2.md` (zamrożony 11.08.2026)
**Zadanie:** `TASK_2B.md`, Etap A · **Data:** 2026-08-12
**Wejście:** `test2b_events_draft.csv` (39 pozycji) · **Wyjście:** `test2b_events.csv`
**Status:** zakończony **STOP** przed Etapem B — β nie liczone, kod testu nie pisany.

---

## 0. Warunek brzegowy tej sesji: brak dostępu do katalogów

Polityka egress środowiska blokuje (403 na bramce) **wszystkie sześć** domen
źródłowych: `volcano.si.edu`, `earthquake.usgs.gov`, `www.cpc.ncep.noaa.gov`,
`rmets.onlinelibrary.wiley.com` (Webb 2022), `www.bp.com`, `www.who.int`.
Sprawdzone `curl`-em i narzędziem WebFetch — oba zwracają blokadę.

Zgodnie z dyrektywą autora: **dane z pliku przyjęte jako dane**, z adnotacją
o niemożności bezpośredniej weryfikacji; **lista nie została zredagowana z pamięci**.
W konsekwencji `verification_status` wszystkich 39 pozycji = `source_cited_unverified`.
Żadna pozycja nie została w tej sesji usunięta ani dodana. Weryfikacja, którą dało
się wykonać bez sieci — kontrole **strukturalne, spójnościowe i definicyjne** — jest
opisana niżej; weryfikacja **źródłowa** (A1 przepisanie, A2 potwierdzenie źródeł)
pozostaje otwarta i wymaga albo odblokowania egress, albo podrzucenia surowych
katalogów do repo.

---

## 1. Liczba zdarzeń — kategorie i podokresy

Łącznie **39** zdarzeń. Zgodne z deklaracją protokołu §4 (39; 10 przed 1900, 29 po).

| kategoria | n | 1816–1899 | 1900–2007 |
|---|---|---|---|
| earthquake | 13 | 0 | 13 |
| pandemic | 12 | 7 | 5 |
| enso | 5 | 2 | 3 |
| volcano | 4 | 1 | 3 |
| treaty | 3 | 0 | 3 |
| energy | 2 | 0 | 2 |
| **razem** | **39** | **10** | **29** |

**Asymetria katalogów (deklarowana w protokole §4):** trzęsienia ziemi (0 przed
1900), traktaty i szoki naftowe (0 przed 1900) występują wyłącznie w podokresie
pierwszorzędnym. Potwierdza to obciążenie, które warianty S3/S5 mają kontrolować.
**8 z 13 trzęsień** przypada na lata 1946–1965 (1946, 1950, 1952, 1957, 1960, 1963,
1964, 1965) — dokładnie powojenny spadek serii wojennej; to jest zbieżność, dla
której S5 (każda kategoria osobno) jest w §8 warunkiem koniecznym pozytywnego Q1.

## 2. Rozkład natężenia S(t) — zanik prostokątny L = 5

`S(t) = Σ w(t − rok_zdarzenia)`, `w(k)=1` dla k∈{0,1,2,3,4}. Liczone ze wszystkich
39 zdarzeń (cień pięcioletni). Statystyka testowa **nie jest** tu liczona — S(t) jest
wyłącznie własnością listy.

| podokres | n lat | min | max | średnia | odch. std | pokrycie S>0 |
|---|---|---|---|---|---|---|
| 1816–1899 | 84 | 0 | 2 | 0,548 | 0,666 | 45,2% |
| **1900–2007** | 108 | 0 | 4 | 1,352 | 1,071 | **78,7%** |
| 1816–2007 | 192 | 0 | 4 | 1,000 | 0,997 | 64,1% |

Liczebność wartości S(t), podokres pierwszorzędny **1900–2007**:
`0:23 · 1:45 · 2:24 · 3:11 · 4:5`. Podokres 1816–1899: `0:46 · 1:30 · 2:8`.

**Pokrycie 78,7% przy L = 5 (60,2% przy L = 3)** odtwarza liczby z §0 protokołu
(79% / 60%) i potwierdza, że listy pozostały nietknięte oraz że zmienność
objaśniająca w v2.0 pochodzi z **natężenia**, nie z kontrastu „zaburzenie / brak" —
grupa „poza cieniem" ma tylko 23 lata na 108.

**Nakładania.** 48 lat pełnego szeregu leży w cieniu >1 zdarzenia (S>1). Dwa lata
mają po dwa zdarzenia startujące w tym samym roku: **1957** (EART_1957 Aleuty +
PAND_1957 grypa azjatycka) i **1972** (ENSO_1972 + TREA_1972 SALT I).

## 3. Kontrole wykonane offline (bez dostępu do źródeł)

- **Zgodność progowa wartości podanych w pliku:** wszystkie `earthquake` mają
  Mw ≥ 8,5; wszystkie `volcano` VEI = 6 (≥6); lata wszystkich pozycji mieszczą się
  w 1816–2007. Tambora (1815) słusznie nieobecna — reguła „rok wybuchu", nie rok
  skutku klimatycznego.
- **Rekoncyliacja liczności:** 13/12/5/4/3/2 = 39, zgodnie z tabelą §4 protokołu.
- **Reguła „rok początku":** lata pandemii cholery (1817, 1829, 1846, 1863, 1881,
  1899, 1961) odpowiadają konwencjonalnym latom **początku** kolejnych pandemii,
  nie kulminacji — zgodnie z regułą. (Uwaga: dla III pandemii spotyka się też datę
  1852; plik używa 1846 — patrz §4.)

## 4. Pozycje wątpliwe (zostają w liście; zastrzeżenie opisane)

Zgodnie z A4 — spełniają lub deklarują spełnienie progu, ale budzą zastrzeżenie.
**Żadnej nie usuwam** (zakaz redakcji + brak dostępu do źródła rozstrzygającego).

1. **PAND_1817 (I pandemia cholery)** — próg „≥3 kontynenty" wątpliwy. W konsensusie
   historyczno-epidemiologicznym I pandemia opisywana jest głównie jako **azjatycka**
   (dotarła do Bliskiego Wschodu i wschodniego wybrzeża Afryki, bez Europy i obu
   Ameryk). Pozostałe pandemie cholery (II–VII) zwykle spełniają próg wyraźniej.
2. **TREA_1972 (SALT I)** — układ **dwustronny** USA–ZSRR. Kryterium v1.0 §2 wymaga
   traktatu **wielostronnego** o zasięgu globalnym. Kwalifikacja wątpliwa na wprost.
3. **TREA_1975 (Akt Końcowy KBWE / Helsinki)** — **nie jest traktatem**, lecz
   deklaracją polityczną; nie ma „wejścia w życie", na którym reguła §2/A2 opiera rok.
   Kwalifikacja jako „układ rozbrojeniowy, wielostronny, globalny" wątpliwa.
4. **Kategoria earthquake — niespójność źródła z progiem.** Źródło („USGS, *20
   Largest Earthquakes since 1900*") jest listą **rankingową** (20 największych),
   podczas gdy próg protokołu jest **progowy** (Mw ≥ 8,5). Przy granicy oba kryteria
   mogą się rozjeżdżać (zdarzenie 8,5 poza pierwszą 20 wypadłoby z listy rankingowej;
   pozycja rankingowa o Mw < 8,5 wypadłaby z progu). Nierozstrzygalne bez pełnego
   katalogu USGS/ISC-GEM.
5. **ENSO przed 1950 (1877, 1888)** — rekonstrukcja, nie pomiar CPC; inna miara.
   Największa asymetria jakości danych między epokami (deklarowana w §4 protokołu).

## 5. Kryterium w obie strony — kategoria „treaty" wymaga decyzji autora

Zadanie A2 nakazuje sprawdzić, czy „wielostronny o zasięgu globalnym" **nie obejmuje
pozycji spoza listy** — i jeśli obejmuje, **dodać je**. Tego **nie da się rozstrzygnąć
w tej sesji** i nie wolno rozstrzygać z pamięci:

- Kandydaci **nazwani wprost w zadaniu** (A2): **LTBT** (Układ o zakazie prób
  w trzech środowiskach, wejście w życie 1963) i **NPT** (wejście w życie 1970) —
  na pierwszy rzut oka spełniają „wielostronny, globalny". Ich dodanie wymaga
  potwierdzenia (a) roku **wejścia w życie** i (b) spełnienia kryterium — ze źródła,
  które jest niedostępny (egress). **Nie dodaję ich z pamięci.**
- Problem jest szerszy: kategoria „traktaty" **nie ma wyczerpującego katalogu
  zewnętrznego z progiem** (w odróżnieniu od GVP/USGS/ONI). Kryterium „wielostronny,
  globalny" bez zamkniętej listy może objąć wiele pozycji (np. Protokół genewski,
  BWC 1975, CWC 1997, Układ o przestrzeni kosmicznej 1967, Układ o dnie morskim
  1972…), co istotnie zmieniłoby zarówno liczbę zdarzeń, jak i S(t) w podokresie
  pierwszorzędnym. To najsłabiej zdefiniowana z sześciu kategorii i najbardziej
  narażona na problem „kryterium działa w obie strony".

**Decyzja zastrzeżona dla autora (§2 zadania):** albo (i) odblokować egress /
podrzucić katalog traktatów i pozwolić dokończyć weryfikację i kompletację listy
w obie strony, albo (ii) zadeklarować **zamkniętą, wyczerpującą** definicję/listę
traktatów kwalifikujących się do progu. Do tego czasu trzy pozycje `treaty`
pozostają jak w szkicu, ze statusem `source_cited_unverified` i zastrzeżeniami z §4.

## 6. Co pozostaje otwarte (blokada egress)

- **A1 (earthquake/volcano/enso):** przepisanie wartości nie zweryfikowane wobec
  USGS/GVP/Webb — domeny zablokowane. Dane przyjęte z pliku.
- **A2 (pandemic/energy/treaty):** weryfikacja źródłowa niewykonana. Dla `energy`
  deklaracja „ceny nominalne vs realne" zapada w Etapie B, przed liczeniem (rekomendacja
  do potwierdzenia: nominalne — skok 1973 i 1979 przekracza 50% r/r w ujęciu
  nominalnym w sposób bezsporny; wymaga potwierdzenia wobec BP/EI).
- **Efekt brzegowy (do rozstrzygnięcia w Etapie B):** jedyne zdarzenie sprzed 1900
  rzucające cień na podokres pierwszorzędny to VI pandemia cholery (1899) →
  S(1900..1903) zyskuje po +1. Konwencja, czy zdarzenia sprzed okna zasilają S(t)
  w oknie, jest decyzją Etapu B (jeden z punktów, na których test się psuje).

## 7. Podsumowanie i STOP

Wykonano weryfikację **strukturalną, spójnościową i definicyjną** listy 39 zdarzeń
oraz obowiązkową diagnostykę A4 (liczności, rozkład S(t), nakładania). Weryfikacja
**źródłowa** pozostaje otwarta z powodu blokady egress; zgodnie z dyrektywą autora
dane przyjęto z pliku, listy nie redagowano z pamięci. Zgłoszono pięć pozycji
wątpliwych i jedną decyzję zastrzeżoną dla autora (kompletność kategorii `treaty`
w obie strony).

**STOP — Etap B nie rozpoczęty.** β nie liczone, kod testu nie pisany. Lista i ten
raport idą do przeglądu autora. Po przeglądzie i rozstrzygnięciu kwestii `treaty`
(oraz — jeśli możliwe — weryfikacji źródłowej) rozpocznę Etap B na tej samej gałęzi
i w tym samym PR.
