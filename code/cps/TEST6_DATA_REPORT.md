# TEST 6 — RAPORT DANYCH (Etap A: zbiór odstępów między konfliktami)

**Protokół:** `TEST6_PROTOCOL.md` v1.0 (D-012) · **Rozstrzygnięcia:** `TASK_6A_RESOLUTION.md` / **D-013**
(scalanie w epizody), `TASK_6A_ADDENDUM.md` / **D-014** (ekspozycja) · **Zadanie:** `TASK_6.md` Etap A
**Źródło wojen:** `Inter-StateWarData_v4.0.csv` (sha256 `2535e30b…`)
**Status:** 🛑 **ZABLOKOWANE przed Krokiem 1b** — brak pliku `system2016.csv` w repo, patrz §10.
Krok 1 (D-013, sekcje 1–9 poniżej) **przyjęty i niezmieniony**; opisuje ostatni działający build
(builder v2.0, odstępy kalendarzowe). Builder v3.0 (D-014, ekspozycja) jest napisany i czeka
na przegląd kodu, ale **NIEURUCHOMIONY** — CSV-y na tej gałęzi to wciąż wyjście v2.0.

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

## 9. Krok 1 — przyjęty (TASK_6A_RESOLUTION.md §6)

Zbiór przebudowany zgodnie z D-013; liczby kontrolne §4 podane obok siebie; tabela scaleń i
lista diad odrzuconych jawne. Ten krok jest **zaakceptowany** (`TASK_6A_ADDENDUM.md` §0)
niezależnie zweryfikowany co do cyfry (epizody, diady, odstępy, CV). **Aktualnym punktem
zatrzymania jest §10 poniżej**, nie ten paragraf.

## 10. STOP — Krok 1b zablokowany: brak `system2016.csv` (D-014)

**D-014** rozstrzyga, że odstęp liczony jest jako **liczba lat ekspozycji** — lat, w których
oba kody ccode diady są członkami systemu państw COW wg `system2016.csv` (COW State System
Membership v2016) — a nie jako różnica dat kalendarzowych. Dziewięć z 63 obserwacji jest
dotkniętych (wszystkie z ogona rozkładu, m.in. Austria-Hungary–Italy: 89 lat kalendarzowych →
**0** lat ekspozycji, bo ccode 300 opuszcza system w 1918; France–Germany: 62 → 18, bo ccode
255 nieobecny 1945–1990). Pełne uzasadnienie i tabela w `CPS_DECISION_LOG.md` D-014.

**Blokada.** Pliku `system2016.csv` **nie ma w repozytorium** (sprawdzone: `data/cow/`, cała
reszta `data/`). Próba pobrania go z dystrybucji COW (correlatesofwar.org) kończy się błędem
sieciowym na poziomie proxy tego środowiska (`CONNECT tunnel failed, response 403`) — to ten
sam rodzaj blokady egress, na którą trafiliśmy przy katalogach zewnętrznych w Teście 2B. Nie
próbuję obejść tej blokady ani zgadywać zawartości pliku.

**Kod jest gotowy, nieuruchomiony.** `test6_build_intervals.py` v3.0 implementuje D-014
(funkcje `load_membership`, `exposure`) zgodnie z `TASK_6A_ADDENDUM.md` §3: wczytuje
`ccode`,`year` z `system2016.csv`, liczy ekspozycję jako lata w przedziale (t0, t1] obecne dla
obu stron, buduje **trzy warianty naraz** (główny: próg epizodowy × ekspozycja; S-A: próg
epizodowy × kalendarz; S-B: próg surowy × ekspozycja — zgodnie z §4 addendum, bez krzyżowania
w cztery komórki). Asercja zatrzymuje bieg, jeśli jakikolwiek odstęp **pełny** wyjdzie z
ekspozycją zero (§3.3); odstęp **cenzurowany** o ekspozycji zero jest dopuszczalny. Sprawdzone
składniowo (`py_compile`), **nie uruchomione** — brak danych wejściowych. CSV-y na tej gałęzi
(`test6_intervals.csv`, `test6_episodes.csv`, `test6_intervals_sensitivity.csv`) są wciąż
wyjściem **v2.0** (kalendarzowym) i zostaną zastąpione wyjściem v3.0 (plus nowe pliki
`test6_intervals_sensitivity_SA.csv`, `_SB.csv`) po dostarczeniu pliku i uruchomieniu builda.

**Potrzebne od autora:** plik `system2016.csv` (COW State System Membership v2016; kolumny co
najmniej `ccode`, `year`) — w dowolnym miejscu pod `code/cps/data/` (np. `data/cow/`),
`find_input` znajdzie go niezależnie od dokładnej ścieżki. Po dostarczeniu: uruchamiam builder
v3.0, aktualizuję ten raport wg `TASK_6A_ADDENDUM.md` §5, i **dopiero wtedy** zgłaszam Krok 1b
do przeglądu przed Etapem B.

**Uwaga do Kroku 3, zapisana już teraz** (`TASK_6A_ADDENDUM.md` §6): przedział ufności dla
parametru kształtu Weibulla musi być bootstrapowany **na poziomie diady, nie odstępu** —
odstępy tej samej diady (np. Egypt–Israel, 4 wnoszone odstępy) nie są niezależnymi
obserwacjami; bootstrap po odstępach zaniżyłby przedział ok. dwukrotnie.
