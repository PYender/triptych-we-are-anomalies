# TEST 2B — RAPORT DANYCH (Etap A: weryfikacja listy zdarzeń)

**Protokół nadrzędny:** `TEST2B_PROTOCOL_v2.md` (zamrożony 11.08.2026)
**Zadanie:** `TASK_2B.md`, Etap A · **Data:** 2026-08-12
**Wejście:** `test2b_events_draft.csv` (39 pozycji) · **Wyjście:** `test2b_events.csv`
**Rozstrzygnięcie autora:** D-007 (wyłączenie kategorii endogenicznych)
**Status:** zakończony **STOP** — β nie liczone, kod testu w Etapie B do przeglądu.

---

## 0. Warunek brzegowy tej sesji: brak dostępu do katalogów

Polityka egress środowiska blokuje (403 na bramce) **wszystkie sześć** domen
źródłowych: `volcano.si.edu`, `earthquake.usgs.gov`, `www.cpc.ncep.noaa.gov`,
`rmets.onlinelibrary.wiley.com` (Webb 2022), `www.bp.com`, `www.who.int`.
Sprawdzone `curl`-em i narzędziem WebFetch — oba zwracają blokadę.

Decyzja autora: **egress nie jest otwierany**; weryfikacja źródłowa pozostaje
niewykonana, a ograniczenie jest opisane. Dane przyjęto z pliku jako dane;
**listy nie redagowano z pamięci**. `verification_status` = `source_cited_unverified`
dla wszystkich 34 pozycji listy finalnej. Weryfikacja wykonana bez sieci —
**strukturalna, spójnościowa i definicyjna** — jest opisana niżej.

## 1. Rozstrzygnięcie D-007 — wyłączenie kategorii endogenicznych

Przegląd listy w Etapie A wykazał, że dwie kategorie szkicu naruszają kryterium
„zewnętrzności wobec dynamiki konfliktu", zadeklarowane w v1.0 §3b (na jego podstawie
odrzucono wcześniej „koszty wyczerpania po wielkich wojnach"):

- **`treaty` (3)** — traktaty rozbrojeniowe zawierane są w okresach **odprężenia**,
  jako skutek opadającego napięcia; wyjaśnianie spadku konfliktowości traktatami
  odwraca kierunek zależności.
- **`energy` (2)** — szoki naftowe w tym oknie są **następstwem konfliktów**
  (1973: embargo OPEC po wojnie Jom Kipur; 1979: rewolucja irańska).

Pięć wierszy dostaje `verification_status = removed` z notatką odsyłającą do D-007;
**wiersze pozostają w pliku** (zakaz kasowania). Nie dodano LTBT, NPT ani żadnego
innego kandydata — problem „kryterium w obie strony" znika wraz z całą kategorią
`treaty`, która jako jedyna nie miała wyczerpującego katalogu zewnętrznego.

**Lista finalna: 34 zdarzenia** — trzęsienia 13, pandemie 12, ENSO 5, wulkany 4.

## 2. Liczba zdarzeń — kategorie i podokresy (lista finalna, 34)

| kategoria | n | 1816–1899 | 1900–2007 |
|---|---|---|---|
| earthquake | 13 | 0 | 13 |
| pandemic | 12 | 7 | 5 |
| enso | 5 | 2 | 3 |
| volcano | 4 | 1 | 3 |
| **razem** | **34** | **10** | **24** |

*(usunięte D-007, poza listą: treaty 3, energy 2 — wszystkie 1900–2007.)*

**Asymetria katalogów.** Trzęsienia ziemi występują wyłącznie po 1900 (0 przed).
**8 z 13 trzęsień** przypada na lata 1946–1965 (1946, 1950, 1952, 1957, 1960, 1963,
1964, 1965) — dokładnie powojenny spadek serii wojennej; zbieżność, dla której S5
(każda kategoria osobno) jest w §8 warunkiem koniecznym pozytywnego Q1.

## 3. Rozkład natężenia S(t) — zanik prostokątny L = 5

`S(t) = Σ w(t − rok_zdarzenia)`, `w(k)=1` dla k∈{0,1,2,3,4}, ze wszystkich 34 zdarzeń.
Statystyka testowa **nie jest** tu liczona — S(t) jest własnością listy.

| podokres | n lat | min | max | średnia | odch. std | pokrycie S>0 |
|---|---|---|---|---|---|---|
| 1816–1899 | 84 | 0 | 2 | 0,548 | 0,666 | 45,2% |
| **1900–2007** | 108 | 0 | 4 | **1,120** | **0,934** | **75,0%** |
| 1816–2007 | 192 | 0 | 4 | 0,870 | 0,874 | 62,0% |

Liczebność wartości S(t), **1900–2007**: `0:27 · 1:52 · 2:21 · 3:5 · 4:3`.
Podokres 1816–1899: `0:46 · 1:30 · 2:8`.

**Skutek D-007 na podokres pierwszorzędny:** pokrycie 78,7% → **75,0%** (L=5),
średnia 1,352 → **1,120**, odchylenie 1,071 → **0,934**. Przy L=3 pokrycie 60,2% →
54,6%. Zmienność objaśniająca zachowana; grupa „poza cieniem" rośnie z 23 do 27 lat
na 108.

**Nakładania.** 37 lat pełnego szeregu w cieniu >1 zdarzenia. Po usunięciu `treaty`
pozostaje **jeden** rok z dwoma zdarzeniami startującymi razem: **1957**
(EART_1957 Aleuty + PAND_1957 grypa azjatycka). (Rok 1972 stracił zbieg, bo
SALT I odpadł.)

## 4. Kontrole wykonane offline

- **Zgodność progowa:** wszystkie `earthquake` Mw ≥ 8,5; wszystkie `volcano` VEI = 6;
  lata w zakresie 1816–2007. Tambora (1815) słusznie nieobecna (reguła „rok wybuchu").
- **Rekoncyliacja liczności:** 13/12/5/4 = 34.
- **Reguła „rok początku":** lata pandemii cholery odpowiadają latom **początku**
  kolejnych pandemii, nie kulminacji.
- **Kategoria earthquake — niespójność źródła bez skutku (rozstrzygnięte).** Źródło
  („USGS, *20 Largest Earthquakes since 1900*") jest listą **rankingową**, nie
  zapytaniem progowym; schodzi jednak do **Mw 8,4**, czyli poniżej progu 8,5, więc
  **wszystkie** zdarzenia Mw ≥ 8,5 od 1900 są w niej zawarte — dla naszego progu lista
  jest **kompletna**. Zarzut formalnie słuszny, bez skutku dla listy.

## 5. Pozycje wątpliwe (zostają w liście; zastrzeżenie opisane)

1. **PAND_1817 (I pandemia cholery)** — zastrzeżenie zgłoszone w Etapie A: pandemia
   bywa opisywana głównie jako azjatycka. **Rozstrzygnięcie autora (D-007 przegląd):
   pozostaje** — udokumentowane rozprzestrzenienie Indie → Azja Płd.-Wsch. → Bliski
   Wschód → wschodnia Afryka daje trzy kontynenty. Zastrzeżenie zachowane tutaj
   zgodnie z wymogiem A4.
2. **ENSO przed 1950 (1877, 1888)** — rekonstrukcja, nie pomiar CPC; inna miara.
   Największa asymetria jakości danych między epokami (deklarowana w §4 protokołu).

*(Pozycje `treaty`/`energy` nie są „wątpliwe" — zostały rozstrzygnięte jako `removed`
w D-007, §1.)*

## 6. Co pozostaje otwarte

- **Weryfikacja źródłowa** (A1 przepisanie wobec USGS/GVP/Webb; A2 potwierdzenie
  pandemii): **niewykonana** — egress zablokowany, decyzją autora nieotwierany.
  Dane przyjęte z pliku ze statusem `source_cited_unverified`.
- **Efekt brzegowy (Etap B).** Jedyne zdarzenie sprzed 1900 rzucające cień na
  podokres pierwszorzędny to VI pandemia cholery (1899) → S(1900..1903) +1.
  Konwencja, czy zdarzenia sprzed okna zasilają S(t) w oknie, jest decyzją Etapu B
  (jeden z punktów B1, na których test się psuje).

## 7. Podsumowanie i STOP

Lista finalna liczy **34 zdarzenia** w czterech bezspornie zewnętrznych kategoriach
(D-007). Wykonano weryfikację strukturalną, spójnościową i definicyjną oraz
obowiązkową diagnostykę A4 (liczności, rozkład S(t), nakładania). Weryfikacja
źródłowa pozostaje otwarta (egress); dane przyjęto z pliku, listy nie redagowano
z pamięci. Zarzut wobec kategorii earthquake rozstrzygnięto (lista kompletna dla
progu). Jedna pozycja pozostaje wątpliwa z zachowanym zastrzeżeniem (PAND_1817).

Etap A zamknięty. Kod Etapu B (`test2b_disturbance.py` + bliźniaczy `.md`) jest
przygotowany **do przeglądu, bez uruchomienia** — patrz osobny plik. β nie liczone.
