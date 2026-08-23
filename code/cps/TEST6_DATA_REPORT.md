# TEST 6 — RAPORT DANYCH (Etap A: zbiór odstępów między konfliktami)

**Protokół:** `TEST6_PROTOCOL.md` v1.0 (D-012) · **Rozstrzygnięcie:** `TASK_6A_RESOLUTION.md` / **D-013**
(scalanie w epizody) · **Zadanie:** `TASK_6.md` Etap A · **Data:** 2026-08-23
**Źródło:** `Inter-StateWarData_v4.0.csv` (sha256 `2535e30b…`) · **Builder:** `test6_build_intervals.py` v2.0
**Status:** **STOP (Krok 1, TASK_6A_RESOLUTION.md §6)** — zbiór przebudowany wg D-013, parametr
Weibulla nie liczony, kod testu nie pisany. Czeka na przegląd warstwy danych przed Etapem B.

---

## 0. Droga techniczna (bez zmian od Etapu A v1)

`lifelines` **nie jest dostępne** w środowisku. Nie instaluję go — w Etapie B
zaimplementuję **MLE Weibulla z cenzurowaniem prawostronnym ręcznie** (`scipy.optimize.minimize`
na log-wiarygodności: obserwacje pełne wnoszą log f(t), cenzurowane log S(t)).

## 1. Rozstrzygnięcie D-013 zastosowane — co się zmieniło

Konflikty tej samej diady, których przedziały trwania **nachodzą się lub stykają** (gap ≤ 0
na surowych danych), zostały scalone w **jeden epizod** (od najwcześniejszego początku do
najpóźniejszego końca w grupie, scalanie przechodnie). Odstęp liczony bez zmian: od końca
epizodu do początku następnego. **Próg ≥3 zastosowany do liczby epizodów** (D-013 §3), nie do
surowych wierszy — jednostką analizy jest czas oczekiwania, więc próg dotyczy jednostki, na
której się on liczy.

**Kontrola poprawności (D-013 §2):** po scaleniu żaden odstęp pełny nie jest niedodatni —
sprawdzone asercją w kodzie (`assert gap > 0`), zero naruszeń przy uruchomieniu. Gdyby się
pojawiło, kod miał się zatrzymać i zgłosić, nie łatać; nie było takiej potrzeby.

## 2. Tabela scaleń (§4.1) — 10 epizodów scalonych, 11 surowych „łuków" nachodzenia

| diada | epizod | lata | składowe konflikty |
|---|---|---|---|
| USA–Vietnam | 1965–1975 | 3 konflikty → 1 epizod | Vietnam War Phase 2 (1965–75); Second Laotian Phase 2 (1968–73); Communist Coalition (1970–71) |
| France–Bulgaria | 1939–1945 | 2→1 | II wś ×2 (zmiana strony) |
| Italy–Bulgaria | 1939–1945 | 2→1 | II wś ×2 (zmiana strony) |
| Bulgaria–Romania | 1939–1945 | 2→1 | II wś ×2 (zmiana strony) |
| Germany–USSR | 1914–1920 | 2→1 | I wś (1914–18); Latvian Liberation (1918–20) |
| USSR–Finland | 1939–1945 | 2→1 | Russo-Finnish (1939–40); II wś (1939–45) |
| USSR–China | 1900 | 2→1 | Boxer Rebellion; Sino-Russian (oba 1900) |
| USSR–Japan | 1939–1945 | 2→1 | Nomonhan (1939); II wś (1939–45) |
| China–Japan | 1937–1945 | 2→1 | III wojna chińsko-japońska (1937–41); II wś (1939–45) |
| Cambodia–Vietnam | 1965–1975 | 2→1 | Vietnam War Phase 2 (1965–75); Communist Coalition (1970–71) |

Suma „łuków" nachodzenia scalonych w tych 10 epizodach = 11 — dokładnie tyle, ile odstępów
niedodatnich zgłoszono w Etapie A v1 (§6 poprzedniej wersji tego raportu). Żaden przypadek nie
został pominięty. Pełna tabela epizodów (wszystkie 18×n, nie tylko scalone) jest w
`test6_episodes.csv`.

## 3. Diady wypadające poniżej progu po scaleniu (§4.2) — jawnie

Próg liczony na epizodach, nie na wierszach, więc diady o ≥3 surowych konfliktach mogą spaść
poniżej progu, jeśli scalenie zredukuje ich liczbę epizodów. **7 z 25 diad wypada:**

| diada | konflikty surowe | epizody po scaleniu |
|---|---|---|
| USA–Vietnam | 3 | **1** (wszystkie trzy scaliły się w jeden epizod) |
| France–Bulgaria | 3 | 2 |
| Germany–USSR | 3 | 2 |
| Italy–Bulgaria | 3 | 2 |
| USSR–Finland | 3 | 2 |
| USSR–China | 3 | 2 |
| Cambodia–Vietnam | 3 | 2 |

**Uwaga wobec wcześniejszej prognozy:** we wstępnej dyskusji nad rozstrzygnięciem D-013
spodziewano się wypadnięcia głównie trzech diad bułgarskich. W praktyce **Bulgaria–Romania
przechodzi próg** (miała 4 konflikty surowe, po scaleniu WWII-dubletu zostaje 3 epizody — wciąż
≥3), a wypadają za to USA–Vietnam, Germany–USSR, USSR–Finland, USSR–China i Cambodia–Vietnam,
które prognoza pominęła. Odnotowuję to jako korektę do wcześniejszego oczekiwania, nie jako
błąd w realizacji D-013 — próg jest stosowany identycznie do wszystkich 25 diad, wynik zależy
wyłącznie od tego, ile surowych konfliktów miała każda z nich przed scaleniem.

**25 diad wchodzących do budowy pozostaje niezmienione** (próg surowy ≥3, D-012) — zmienia się
wyłącznie to, które z nich przechodzą **drugi**, epizodowy próg D-013.

## 4. Nowe liczby kontrolne — obok liczb sprzed przebudowy

| wielkość | sprzed D-013 (Etap A v1) | **po D-013 (pierwszorzędny)** | wrażliwość (próg na wierszach, D-013 §4) |
|---|---|---|---|
| diady | 25 | **18** | 25 |
| odstępy pełne | 62 (51 „ok" + 11 niedodatnich) | **45** | 51 |
| odstępy cenzurowane | 25 | **18** | 25 |
| odstępy niedodatnie | 11 | **0** | 0 |

Wariant wrażliwości scala te same epizody, ale **nie usuwa** żadnej z 25 diad nawet jeśli
spadła poniżej progu epizodowego — pokazuje, czy rozstrzygnięcie progu (§3) samo w sobie
przesądza wynik. Plik: `test6_intervals_sensitivity.csv`.

## 5. CV pulowy po scaleniu — zestawienie z §0.2 i wersją sprzed D-013

| zbiór | n | CV |
|---|---|---|
| §0.2 protokołu (sprzed zamrożenia, bez modelu zerowego, bez cenzurowania) | — | 0,59–0,95 |
| Etap A v1 — tylko dodatnie, bez scalania (`flag=ok`) | 51 | 0,901 |
| Etap A v1 — wszystkie pełne łącznie z niedodatnimi | 62 | 1,181 |
| **Po D-013 — pierwszorzędny (18 diad, po scaleniu)** | **45** | **0,955** |
| Wariant wrażliwości (25 diad, po scaleniu, próg surowy) | 51 | 0,909 |

CV pierwszorzędne (0,955) leży **tuż powyżej** górnej granicy zakresu §0.2 (0,95) — różnica
jest niewielka i **§0.2 pozostaje punktem odniesienia dokumentacyjnym, nie celem do
odtworzenia** (D-013, konsekwencje uboczne): §0.2 najprawdopodobniej liczono po prostym
odrzuceniu nakładań, nie po scaleniu w epizody, więc bezpośrednie porównanie nie jest właściwą
miarą zgodności. Nie traktuję tej różnicy jako błędu ani jako potwierdzenia.

## 6. Odstępy według epok (po scaleniu, pierwszorzędny zbiór, wg roku końca epizodu poprzedniego)

| podział | przed | po |
|---|---|---|
| 1914 | 22 | 23 |
| 1945 | 31 | 14 |

## 7. Kolumna `flag` i status danych źródłowych

Nic z pierwotnego zbioru nie zostało skasowane: `test6_episodes.csv` zawiera pełną tabelę
scaleń (który surowy konflikt wszedł do którego epizodu), a pierwotny plik `test6_intervals.csv`
z Etapu A v1 (62+25 wierszy, kolumna `flag`, wszystkie 11 przypadków niedodatnich z opisem)
jest zachowany w historii commitów tej gałęzi. Scalanie zmienia **strukturę** zbioru
(z „konflikt" na „epizod" jako jednostkę), nie usuwa żadnego wiersza źródłowego.

## 8. Zakres — bez zmian (D-013 §5, „czego nie robimy")

Zbiór ogranicza się do `Inter-StateWarData_v4.0.csv` (Inter-State). Francja–Anglia i
Niemcy–Polska nie wchodzą — nie mają trzech wspólnych wojen **międzypaństwowych** COW, co jest
faktem o zbiorze danych, nie o historii tych par. Rozszerzenie na Extra-/Intra-State zmieniałoby
definicję diady i nie jest podejmowane teraz.

## 9. STOP (Krok 1, TASK_6A_RESOLUTION.md §6)

Zbiór przebudowany zgodnie z D-013; liczby kontrolne §4 podane obok siebie; tabela scaleń i
lista diad odrzuconych jawne. **Nie liczę Weibulla, nie piszę kodu testu.** Zgłaszam do
przeglądu warstwy danych — dopiero po akceptacji przechodzę do Etapu B (`test6_intervals.py` +
bliźniaczy `.md`, sześć punktów B1 z `TASK_6.md`, bez uruchamiania do czasu przeglądu kodu).

**Uwaga do Etapu B, zapisana już teraz:** przy 18 diadach i 45 odstępach pełnych + 18
cenzurowanych, estymacja dwuparametrowa (kształt + skala Weibulla) z cenzurowaniem będzie miała
**szeroki przedział ufności dla parametru kształtu**. Raport Etapu C poda przedział ufności
(profil wiarygodności albo bootstrap diadowy), nie samą wartość punktową i p.
