# TEST 6 — RAPORT DANYCH (Etap A: zbiór odstępów między konfliktami)

**Protokół:** `TEST6_PROTOCOL.md` v1.0 (D-012) · **Rozstrzygnięcia:** `TASK_6A_RESOLUTION.md` / **D-013**
(scalanie w epizody), `TASK_6A_ADDENDUM.md` / **D-014** (ekspozycja) · **Zadanie:** `TASK_6.md` Etap A
**Źródło wojen:** `Inter-StateWarData_v4.0.csv` (sha256 `2535e30b…`) · **Źródło członkostwa:**
`system2016.csv` (sha256 `280e10b4…`, potwierdzone bit-do-bitu z sumą podaną przez autora)
**Status:** **STOP przed Etapem B (Krok 1b, `TASK_6A_ADDENDUM.md` §6)** — builder v3.0 uruchomiony,
zbiór przeliczony na ekspozycję (D-014), zero naruszeń asercji. Krok 1 (D-013, §1–9) i Krok 1b
(D-014, §10–12) **wykonane**. Parametr Weibulla nadal nie liczony, kod testu nie pisany.

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
przesądza wynik. *(Ten wariant to dziś `test6_intervals_sensitivity_SB.csv` — patrz §11–12;
nazwa i zakres nie zmieniły się przy D-014, zmienił się tylko sposób liczenia czasu.)*

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

## 10. D-014 zastosowane — odstęp jako lata ekspozycji

`system2016.csv` dostarczony przez autora, potwierdzony bit-do-bitu (sha256 `280e10b4…`,
15 950 wierszy, kolumny `stateabb,ccode,year,version`, zakres 1816–2016, 217 kodów) —
zgodnie z sumą kontrolną podaną przed wgraniem. `find_input` trafia jednoznacznie w ten plik
(w repo nie ma pliku `states2016.csv` ani innego, z którym normalizacja nazwy mogłaby się
pomylić). Builder v3.0 uruchomiony bez naruszeń asercji: żaden odstęp **pełny** nie wyszedł
z ekspozycją zero.

**Kontrola poprawności implementacji, wykonana przed przyjęciem liczb do raportu:** dla 54
z 63 obserwacji zbioru pierwszorzędnego ekspozycja musi być dokładnie równa wartości
kalendarzowej (obserwacje, których żadna z przerw członkostwa nie dotyka). Wynik: **54/63
dokładnie zgodnych** — potwierdzone. Pozostałe 9 to dokładnie te z tabeli D-014:

| diada | typ | kalendarzowo | ekspozycja | przyczyna |
|---|---|---|---|---|
| Austria-Hungary–Italy | cenzurowany | 89 | **0** | ccode 300 opuszcza system w 1918 |
| France–Germany | cenzurowany | 62 | **18** | ccode 255 nieobecny 1945–1990 |
| Germany–Yugoslavia | pełny 1945→1999 | 54 | **10** | ccode 255 nieobecny 1945–1990 |
| Spain–Morocco | pełny 1910→1957 | 47 | **4** | ccode 600 nieobecny 1912–1956 |
| China–Japan | cenzurowany | 62 | 56 | ccode 740 nieobecny 1945–1952 |
| USSR–Japan | cenzurowany | 62 | 56 | ccode 740 nieobecny 1945–1952 |
| Greece–Turkey | cenzurowany | 85 | 83 | ccode 350 nieobecny 1941–1944 |
| Yugoslavia–Turkey | pełny 1918→1999 | 81 | 79 | ccode 345 nieobecny 1941–1944 |
| Syria–Israel | pełny 1949→1967 | 18 | 16 | ccode 652 nieobecny 1958–1961 |

**Sumy przed i po:** odstępy pełne 839 → **748** lat; cenzurowane 956 → **809** lat (zgodne
z D-014 co do roku). Austria-Hungary–Italy jest jedynym odstępem cenzurowanym o ekspozycji
zero w zbiorze pierwszorzędnym — dopuszczalne z definicji (D-014 §3: wnosi log S(0) = 0 do
wiarygodności; diada zostaje w zbiorze przez pozostałe odstępy pełne).

## 11. CV pulowy — trzy warianty (D-014 §4) obok §0.2

| wariant | próg | czas | n pełnych | CV |
|---|---|---|---|---|
| §0.2 protokołu (dokumentacyjny, bez modelu zerowego/cenzurowania) | — | — | — | 0,59–0,95 |
| **główny — orzeka** | epizodowy (D-013) | **ekspozycja (D-014)** | 45 | **0,983** |
| S-A (wrażliwość na D-014) | epizodowy | kalendarz | 45 | 0,955 |
| S-B (wrażliwość na D-013) | surowy (25 diad) | ekspozycja | 51 | 0,926 |

Ekspozycja podnosi CV względem kalendarza (0,955→0,983). **Poprawka do wcześniejszej wersji
tego zdania (`TASK_6B_BRIEF.md` §7):** korekta ekspozycji **niczego nie wydłuża** —
wyłącznie skraca (zawsze `ekspozycja ≤ kalendarz`). Wzrost CV bierze się stąd, że mianownik
(średnia) kurczy się szybciej niż licznik (odchylenie): średnia spada z 18,64 do 16,62
(−10,8%), odchylenie z 17,80 do 16,34 (−8,2%) — zweryfikowane bezpośrednio na danych.
Odpowiadają za to głównie dwa odstępy, które z wartości bliskich środkowi rozkładu stają się
jednymi z najkrótszych w zbiorze: Germany–Yugoslavia (54→10) i Spain–Morocco (47→4).
Różnica między wariantami jest mała (0,926–0,983); żaden nie odtwarza dokładnie §0.2, co jest
oczekiwane (§0.2 nie stosował ani scalania, ani ekspozycji) i nie jest tu traktowane jako
błąd ani potwierdzenie.

## 12. Dwa ograniczenia nazwane wprost (D-014, konsekwencje uboczne)

**Konsolidacja Europy po 1945 jest w tym zbiorze niemierzalna dla par niemieckich.** Po
korekcie France–Germany ma 18 lat ekspozycji od 1945, nie 62 — COW nie zna zjednoczonych
Niemiec 1945–1990 (RFN 260 i NRD 265 to inne kody, nieużyte przez ten builder, bo diady
budowane są na `Inter-StateWarData_v4.0.csv`, gdzie występuje wyłącznie ccode 255). Podział
epokowy 1945 (§6, niezmieniony przez ekspozycję: 31 przed / 14 po) **nie może** być czytany
jako świadectwo o powojennej konsolidacji — to ograniczenie danych, nie wynik.

**Kierunek obciążenia progu epizodowego (D-013) jest NIEUSTALONY — sprostowanie do
poprzedniej wersji tego paragrafu (D-017).** Siedem diad wypadających po scaleniu (§3) to
rzeczywiście pary o konfliktach najsilniej nachodzących się na siebie w zbiorze (USA–Vietnam:
trzy konflikty w dziesięć lat → jeden epizod → zero odstępów pełnych) — ten argument
strukturalny jest poprawny. Błędny był wniosek liczbowy: sześć odstępów pełnych, które
wariant S-B dokłada do zbioru głównego, wynosi **2, 19, 19, 21, 21 i 29 lat** — pięć z nich
leży blisko średniej zbioru głównego (16,6) i powyżej jego mediany (11), więc ich włączenie
**obniża** CV (0,983 → 0,926 w §11) — zbiór wygląda **bardziej** regularny, nie mniej.
USA–Vietnam, para faktycznie najsilniej zgrupowana, nie wnosi żadnego odstępu pełnego w
żadnym wariancie, więc nie jest tym, co S-B dokłada. Próg nie usuwa w rozpoznany sposób
świadectw przeciwko hipotezie H1 — usuwa parę bez odstępów w ogóle i dokłada pary o
odstępach zbliżonych do średniej. Wymóg raportowania **S-B na równi z wynikiem głównym w
Etapie C pozostaje w mocy**, ale z innym uzasadnieniem: nie dlatego, że S-B ujawnia ukryte
świadectwa przeciwne hipotezie, lecz dlatego, że próg widocznie przesuwa CV i wyboru między
wariantami nie wolno dokonywać po zobaczeniu wyniku. Pełne sprostowanie: `CPS_DECISION_LOG.md`
D-017.

## 13. STOP (Krok 1b, `TASK_6A_ADDENDUM.md` §6)

Trzy warianty zbudowane i przeliczone (`test6_intervals.csv` główny, `test6_intervals_sensitivity_SA.csv`,
`test6_intervals_sensitivity_SB.csv`), tabela scaleń (`test6_episodes.csv`) bez zmian od D-013.
Kontrola poprawności (54/63) potwierdzona przed przyjęciem liczb. **Nie liczę Weibulla, nie
piszę kodu testu.** Zgłaszam do przeglądu — dopiero po akceptacji przechodzę do Etapu B.

**Uwaga do Kroku 3, zapisana już teraz** (`TASK_6A_ADDENDUM.md` §6): przedział ufności dla
parametru kształtu Weibulla musi być bootstrapowany **na poziomie diady, nie odstępu** —
odstępy tej samej diady (np. Egypt–Israel, 4 wnoszone odstępy) nie są niezależnymi
obserwacjami; bootstrap po odstępach zaniżyłby przedział ok. dwukrotnie. Raport Etapu C podaje
przedział, nie samą wartość punktową i p, i raportuje główny wynik obok S-A i S-B (§12).
