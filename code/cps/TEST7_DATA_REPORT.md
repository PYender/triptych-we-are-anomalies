# TEST 7 — RAPORT DANYCH (Etap A: okna ryzyka i czasy oczekiwania, rodzina 9b)

**Protokół:** `TEST7_PROTOCOL.md` v1.0 (D-016) · **Sprostowanie liczby kontrolnej:** D-020 ·
**Przeliczenie Etapu A:** D-021 (reguła zdarzeń), D-025 (wykluczenie 1 odstępu) · **Zadanie:**
`TASK_7A_BRIEF.md` · **Data budowy:** 2026-08-24 · **Data przeliczenia:** 2026-08-25
**Źródła:** `tss_rivalries.rda` (sha256 `7d4aabe8…`, commit `fe150a26` peacesciencer,
2026-07-01 — sprzed D-016, brak ryzyka dryfu zbioru), `Inter-StateWarData_v4.0.csv`
(sha256 `2535e30b…`), `system2016.csv` (sha256 `280e10b4…`) · **Builder:** `test7_build_windows.py` v1.2
**Status:** **STOP** — zbiór okien ryzyka i czasów przeliczony po D-021/D-025 i
udokumentowany (§5, §6, §9). Żadna statystyka czasów oczekiwania nie policzona (§6 brief).
Etap B nadal zablokowany, patrz §8.

---

## 1. Liczby kontrolne (§2 brief) — zgodne, z jednym sprostowanym wyjątkiem

| sprawdzenie | oczekiwane | uzyskane |
|---|---|---|
| `tss_rivalries` | 264 wiersze, 12 kolumn | **264, 12** ✓ |
| `td_rivalries` | 197 wierszy, 10 kolumn | **197, 10** ✓ |
| wiersze ze `spatial=1` | 152 | **152** ✓ |
| unikalnych diad ze `spatial=1` | 141 | **141** ✓ |
| rywalizacje (wiersze) rozpoczęte przed 1816 | 18 | **18** ✓ |
| diady z niepustym oknem ryzyka | ~~129~~ **120** (sprostowanie D-020) | **120** |

Jedyna rozbieżność (129 vs 120) była błędem liczby kontrolnej w D-016, nie błędem
implementacji — sprostowana w **D-020**: pierwotne 129 policzono z pominięciem warunku
członkostwa w systemie państw (`system2016.csv`), którego wzór §3 protokołu wymaga wprost.
Wzór §3 pozostaje bez zmian. Pozostałe pięć sprawdzeń zgodne co do cyfry przed jakąkolwiek
korektą.

## 2. Rozbicie 21 diad odrzuconych (D-020)

| grupa | n | przyczyna |
|---|---|---|
| **A** | 9 | okres rywalizacji całkowicie przed 1816 |
| **B** | 3 | okres rywalizacji całkowicie po 2007 |
| **C** | 9 | brak wspólnych lat członkostwa obu stron w części okresu mieszczącej się w [1816,2007] |

**Grupa A** (rywalizacje historyczne zakończone przed początkiem zbioru COW): United
Kingdom–Spain (1568–1667), Netherlands–Spain (1579–1648), France–Spain (1494–1700),
Spain–Portugal (1494–1580), Spain–Austria (1701–1793), Spain–Turkey (1494–1585),
Austria-Hungary–Turkey (1494–1700), ccode 324–Turkey (1494–1717 — ccode 324 nieobecny
w `system2016.csv` w ogóle, jednostka polityczna wygasła przed powstaniem współczesnego
systemu państw), USSR–Sweden (1697–1721, era wojny północnej).

**Grupa B** (rywalizacje zaczynające się po zamknięciu `Inter-StateWarData_v4.0.csv`):
trzy pary z okresami rywalizacji startującymi 2008 lub później.

**Grupa C** — przykład wart odnotowania: **Niemcy–Austria (rywalizacja 1740–1870)** odpada,
bo COW koduje Austro-Węgry jako ccode `300` do 1918, a Austrię jako ccode `305` dopiero od
1919 — w przedziale [1816,1870] (część okresu mieszcząca się w zbiorze COW) nie ma roku,
w którym ccode `305` istnieje w `system2016.csv`. **To jest ograniczenie konwencji kodowania
COW, nie twierdzenie historyczne** o nieistnieniu Austrii jako podmiotu w tym okresie —
zgodnie z zasadą przyjętą już w D-012 dla ciągłości państw. Pozostałe osiem przypadków grupy C
mają analogiczną przyczynę — data wejścia współczesnego kodu ccode do `system2016.csv`
(zwykle rok niepodległości/uznania międzynarodowego) wypada później niż koniec nakładającej
się z [1816,2007] części historycznej rywalizacji:

| diada | okres(y) rywalizacji | wejście strony późniejszej |
|---|---|---|
| Nicaragua–Costa Rica | 1842–1858 | obie 1900/1920 |
| United Kingdom–Myanmar | 1816–1826 | Myanmar 1948 (niepodległość) |
| France–Vietnam | 1858–1884 | Wietnam 1954 (Genewa) |
| USSR–Iran | 1816–1828 | Iran 1855 |
| Ethiopia–Egypt | 1868–1882, 2011–2020 | Ethiopia 1898; drugi okres całkowicie po 2007 (jak grupa B) |
| Turkey–Egypt | 1828–1841 | Egipt 1855 |
| Yemen–Oman | 1967–1982 | Jemen (zjednoczony) 1990 |
| Thailand–Vietnam | 1816–1884 | Tajlandia 1887; Wietnam 1954 |

Pełna lista 21 diad z okresami i przyczyną: `test7_build_windows.py` wypisuje ją przy
uruchomieniu (`diady odrzucone (puste okno)`); commit builda zawiera jej zapis w logu.

## 3. Kontrola implementacji (§4 brief) — ekspozycja vs czas kalendarzowy

| wielkość | wartość |
|---|---|
| wiersze zbioru (`test7_intervals.csv`) | 225 |
| ekspozycja = kalendarz | **213 / 225** |
| rozbieżne | 12 |

Wszystkie 12 rozbieżności wyjaśnione co do sztuki — dwie przyczyny, obie zgodne z projektem
(D-014, §3.1 brief):

**Przerwa w członkostwie** (jak w Teście 6): France–Germany (cenzurowany 1945–1955: ekspozycja
**0** — cały przedział mieści się w luce Niemiec 1945–1990), Italy–Ethiopia (7→3, okupacja
włoska 1936–1941), Syria–Israel (18→16, luka Syrii 1958–1961 — ten sam mechanizm co w
Teście 6/D-014), i pięć mniejszych przypadków (1–24 lat różnicy).

**Przerwa między okresami rywalizacji** (nowe wobec Testu 6, §3.1 brief) — dwa duże
przypadki, sprawdzone bezpośrednio w `test7_windows.csv`:
- **China–Japan** (cenzurowany 1945–2007: kalendarz 62, ekspozycja **12**): diada ma dwa
  osobne okresy rywalizacji, 1873–1945 i 1996–2020 (okno przycięte do 2007). Lata 1945–1996
  (51 lat) nie należą do żadnego okresu — poprawnie wyłączone z ekspozycji, nie są czasem
  ryzyka.
- **Iran–Afghanistan** (cenzurowany_bez_epizodow 1919–2001: kalendarz 82, ekspozycja **24**):
  analogicznie, okresy 1816–1937 i 1996–2001 z 59-letnią przerwą między nimi.

Żadna z 12 rozbieżności nie jest błędem — obie kategorie są mechanizmem zamierzonym.

## 4. Kontrola nazw — w obie strony (§5 brief, §2 protokołu)

| para | w zbiorze `spatial=1` | z niepustym oknem |
|---|---|---|
| USA–Wietnam | **nie** | — |
| USA–ZSRR | **nie** (rywalizacja istnieje, ale `spatial=0` — zgodnie z D-016) | — |
| Niemcy–Polska | tak | tak |
| Francja–Anglia | tak | tak |
| Niemcy–Francja | tak | tak |
| Rosja–Turcja | tak | tak |

Wszystkie sześć zgodne z oczekiwaniami D-016 co do statusu.

**18 diad zbioru głównego Testu 6 wobec filtru rywalizacji przestrzennej:** **16 z 18** ma
`spatial=1` **i wszystkie 16 mają niepuste okno** — zgodne z D-016 („16 ma składnik
przestrzenny"). Dwie diady Testu 6 poza zbiorem rywalizacji: Germany–Yugoslavia i
Guatemala–El Salvador (żadna nie figuruje w `tss_rivalries` w ogóle, nie tylko poza
`spatial=1`).

## 5. Epizody częściowo w oknie — 4 przypadki — ROZSTRZYGNIĘTE (D-021, D-025)

Pierwotnie zgłoszone jako nierozstrzygnięte (§3.3 brief), poniższe cztery przypadki
epizodu „częściowo w oknie" zostały rozstrzygnięte regułą **D-021** (zdarzenie liczy się,
gdy jego **początek** mieści się w oknie ryzyka; okno domyka się na zdarzeniu, jeśli ono
samo wykracza poza koniec okna — Skutek A; okno już trwające w chwili otwarcia przesuwa
początek okna na koniec tego epizodu — Skutek B):

| diada | epizod | mechanizm | skutek |
|---|---|---|---|
| France–Italy | II wś (1939–1945) | Skutek A | zdarzenie liczone, okno domyka się na 1939 (starcie wojny), bez odstępu cenzurowanego po nim |
| Germany–Poland | II wś (1939–1945) | Skutek A | zdarzenie liczone, okno domyka się na 1939 |
| Italy–Ethiopia | II wś (1939–1945) | Skutek A | zdarzenie liczone, okno domyka się na 1939 — **ale odstęp Podbój Etiopii(1936)→II wś(1939) ma ekspozycję 0 i wykluczony osobną decyzją, D-025 (§7 niżej)** |
| Cambodia–Vietnam | Wojna wietnamska + Communist Coalition (1965–1975) | Skutek B | epizod już trwał przy otwarciu okna → początek okna przesunięty z 1970 na 1975 (koniec epizodu) |

Żadna z reguł nie została wymyślona post-hoc pod te cztery przypadki — D-021 jest ogólną
zasadą zastosowaną jednolicie do wszystkich 120 diad; te cztery są po prostu przypadkami,
w których miała nietrywialny skutek.

## 6. Struktura zbioru głównego — po D-021 i D-025, liczby nowe obok dotychczasowych

| typ wiersza | dotychczas (przed D-021) | **nowe (po D-021+D-025)** | opis |
|---|---|---|---|
| `t0` | 62 | **64** | otwarcie okna → pierwszy epizod — **poza modelem głównym** (§5 protokołu) |
| `pelny` | 43 | **43** | odstęp między kolejnymi epizodami |
| `cenzurowany` | 62 | **42** | ostatni epizod → domknięcie okna |
| `cenzurowany_bez_epizodow` | 58 | **56** | diada bez żadnego epizodu w oknie — **cały okres jest jedną obserwacją cenzurowaną** |
| **razem** | **225** | **205** | 120 diad (bez zmian — D-021/D-025 nie zmieniają zbioru diad, tylko sekwencję zdarzeń w środku) |

Kierunek zmian zgodny z mechanizmem D-021: trzy diady (France–Italy, Germany–Poland,
Italy–Ethiopia) zyskują zdarzenie via Skutek A, co zamienia ich `cenzurowany`
(i w niektórych przypadkach `cenzurowany_bez_epizodow`) na `t0` — stąd `t0` rośnie, a
`cenzurowany`/`cenzurowany_bez_epizodow` maleją; Skutek A jednocześnie **nie dodaje** odstępu
cenzurowanego po zdarzeniu domykającym okno (bo nie wiadomo, kiedy trwająca wojna się
skończy), co dodatkowo obniża `cenzurowany`. `pelny` pozostaje 43 przypadkowo — D-021 dodaje
jeden potencjalny odstęp pełny (Italy–Ethiopia, Podbój Etiopii→II wś), ale ten jeden odstęp ma
ekspozycję 0 i jest wykluczony przez D-025 (§7 niżej), więc liczba odstępów pełnych
**wchodzących do modelu** nie zmienia się mimo zmiany w budowie sekwencji zdarzeń.

**56 diad bez epizodów po D-021** (dotychczas 58) — brief §3.4 podkreślał, że to sedno testu
(„około siedemdziesięciu par... jeżeli wypadną ze zbioru, coś poszło źle"). 56/120 = 47%,
nadal zgodne rzędem wielkości z ok. 70/141 = 50% w D-016 (liczonym na całej populacji 141,
przed odrzuceniem 21 diad z pustym oknem). Nie zniknęły — są obecne i stanowią prawie
połowę zbioru.

## 7. D-025 — wykluczenie jednego odstępu (Italy–Ethiopia)

Odstęp pełny Italy–Ethiopia między epizodem „Podbój Etiopii" (1935–36) a II wś (1939–1945)
ma **ekspozycję 0** — cały ten okres (1936–1939) przypada na aneksję włoską, gdy Etiopia jako
podmiot jest **całkowicie nieobecna** w `system2016.csv` (nie istnieje wtedy jako oddzielne
państwo systemu). To ten sam mechanizm nieciągłości członkostwa co Austria-Hungary/Austria w
Teście 6 (D-014 §3), tylko bardziej skrajny (całkowita nieobecność, nie tylko przerwa).

**Rozstrzygnięcie:** ten JEDEN odstęp wykluczony z analizy — nie cała diada Italy–Ethiopia
(odstęp `t0`, 1898→1935, zostaje). **Uzasadnienie (po korekcie w przeglądzie): to nie jest
wyjątek, tylko D-013 zastosowane w czasie ekspozycji.** D-013 nakazuje scalać epizody
stykające się lub nakładające się w czasie. Między tymi dwoma epizodami nie ma **ani
jednego roku ekspozycji** — w zegarze, którym faktycznie mierzymy odstępy (suma lat
ekspozycji, nie kalendarz), one się stykają, więc D-013 zastosowane poprawnie każe je
scalić, a nie liczyć jako dwa zdarzenia oddzielone odstępem. Scalenie i wykluczenie dają
identyczny wynik liczbowy (zero wniesionych obserwacji z tego przejścia), więc decyzja
operacyjna zostaje, ale przestaje wymagać osobnej licencji — jest konsekwencją reguły już
obowiązującej. Analogia do Polski walczącej z zaborcami, nieistniejącej formalnie jako
podmiot, ilustruje *dlaczego* zerowa ekspozycja znaczy zerowy dystans, ale nie jest już
samodzielną podstawą decyzji.

**Kierunek obciążenia:** usunięcie odstępu o zerowej długości usuwa masę z **dolnego
końca** rozkładu, co podnosi oszacowane k̂ w stronę 1 (w stronę modelu zerowego) —
**działa przeciw hipotezie H9b, nie na jej korzyść**.

Implementacja: `test7_build_windows.py` zbiera każdy odstęp o ekspozycji ≤0 do osobnej listy
`wykluczenia` zamiast zatrzymywać bieg asercją; `main()` **sprawdza jawnie**, że jedyny
wykluczony przypadek to Italy–Ethiopia — jakikolwiek NOWY, nieautoryzowany przypadek
ekspozycji≤0 nadal zatrzymuje bieg do decyzji (`AssertionError`), zgodnie z zasadą, że D-025
autoryzuje wyłącznie ten jeden, sprawdzony przypadek, nie ogólną regułę „pomijaj zero-ekspozycji
po cichu". Lista wykluczeń zapisana w `test7_excluded_intervals.csv` (1 wiersz), liczba
w metadanych obu plików wynikowych (`odstepy_wykluczone_D025`).

## 8. Zasięg Skutku A (D-021) — własność strukturalna zbioru, nie margines

Przeliczenie ujawniło coś wymagającego wyjaśnienia arytmetycznego: obserwacje cenzurowane
spadły ze 120 (62 `cenzurowany` + 58 `cenzurowany_bez_epizodow`, po jednej na diadę) do
98 (42 + 56) — **22 diady straciły ogon cenzurowany w całości**, mimo że D-021 explicite
zgłaszało tylko 4 przypadki (§5). Zweryfikowano bezpośrednim przeliczeniem: Skutek A
(okno domyka się na zdarzeniu, bez odstępu cenzurowanego po nim) uruchamia się wszędzie
tam, gdzie ostatni kwalifikujący epizod diady kończy się w chwili domknięcia okna ryzyka
lub później (`ostatni_epizod.koniec >= koniec_okna`) — **niezależnie od tego, czy przypadek
był wcześniej zgłoszony**. Dokładnie **22 z 64 diad z epizodami** spełniają ten warunek:

United States of America–Japan, Brazil–Paraguay, Paraguay–Argentina, United Kingdom–Germany,
United Kingdom–China, United Kingdom–Japan, France–Austria-Hungary, France–Italy,
France–China, France–Thailand, Germany–Poland, Germany–USSR, Austria-Hungary–Italy,
Austria-Hungary–Yugoslavia, Austria-Hungary–USSR, Hungary–Yugoslavia, Italy–Ethiopia,
Yugoslavia–Turkey, Bulgaria–Romania, USSR–Turkey, USSR–Japan, Uganda–Tanzania.

W większości przypadków (I i II wś) to konwencja kodowania Thompsona, która kończy okres
rywalizacji razem z wojną, która ją rozstrzyga; kilka przypadków niezwiązanych ze światowymi
wojnami (Lopez War 1870, Boxer Rebellion 1900, Franco-Thai 1941, Uganda-Tanzania 1979)
pokazuje, że mechanizm jest ogólny, nie ograniczony do konfliktów światowych.

**To zachowanie kodu jest poprawne** — D-021 to jedna reguła zastosowana jednolicie do
wszystkich 120 diad, nie cztery reguły punktowe pod cztery zgłoszone przypadki. Ale przy
22/64 = 34% diad z epizodami zdarzenie i domknięcie okna są **z definicji równoczesne** —
to nie są niezależne obserwacje czasu oczekiwania w tym samym sensie co pozostałe 42, gdzie
okno domyka się niezależnie od tego, kiedy skończyła się ostatnia wojna. Przy 4 przypadkach
(§5) to była uwaga na marginesie; przy 22 jest to **fakt o strukturze danych**, z którym
Etap B musi się liczyć od początku — możliwy wpływ na sposób traktowania obserwacji
`cenzurowany` kontra diad, które go nie mają, nie rozstrzygany tutaj, tylko udokumentowany
przed Etapem B, nie dopiero w Etapie C.

## 9. Co pozostaje poza tą turą

Zgodnie z `TASK_7A_BRIEF.md` §0: żadnych kolumn dla H9b.2 (straty, czas trwania,
status mocarstwowy) — nie budowane nawet „na zapas". COW NMC i ICOW nie dostarczone,
model H9b.2 odłożony.

## 10. STOP

Zbiór zbudowany: `test7_windows.csv` (120 diad, okna po D-021 — Cambodia–Vietnam z oknem
przesuniętym 1970→1975), `test7_intervals.csv` (**205** wierszy obserwacji, po D-021+D-025 —
patrz §6, §7), `test7_excluded_intervals.csv` (1 wiersz, Italy–Ethiopia, D-025). Liczby
kontrolne §1 zgodne po sprostowaniu D-020; kontrola §4 (213/225, sprzed D-021/D-025) w pełni
wyjaśniona; kontrola nazw §5 zgodna z D-016. Cztery epizody częściowe pierwotnie zgłoszone
w §5 (starej wersji) są teraz rozstrzygnięte regułą D-021, z jednym dodatkowym wykluczeniem
D-025 (§7). Zweryfikowano też i udokumentowano zasięg Skutku A poza cztery zgłoszone
przypadki — 22/64 diad z epizodami mają zdarzenie i domknięcie okna równoczesne z definicji
(§8), własność strukturalna zbioru, nie margines. **Nie liczę żadnej statystyki czasów
oczekiwania — ani CV, ani mediany, ani
parametru kształtu.** Etap B (dopasowanie estymatora) pozostaje zablokowany niezależnie od
tego przeliczenia — czeka na (a) przegląd `TASK_7B_BRIEF.md` przez autora pod kątem tego
samego typu podmiany metodologii, jaka wykryto w Teście 6 (D-023), oraz (b) zamknięty,
zgodny z protokołem bieg Kroku C Testu 6, dowodzący wspólnego estymatora na realnych danych.
