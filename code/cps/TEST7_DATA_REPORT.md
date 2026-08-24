# TEST 7 — RAPORT DANYCH (Etap A: okna ryzyka i czasy oczekiwania, rodzina 9b)

**Protokół:** `TEST7_PROTOCOL.md` v1.0 (D-016) · **Sprostowanie liczby kontrolnej:** D-020 ·
**Zadanie:** `TASK_7A_BRIEF.md` · **Data:** 2026-08-24
**Źródła:** `tss_rivalries.rda` (sha256 `7d4aabe8…`, commit `fe150a26` peacesciencer,
2026-07-01 — sprzed D-016, brak ryzyka dryfu zbioru), `Inter-StateWarData_v4.0.csv`
(sha256 `2535e30b…`), `system2016.csv` (sha256 `280e10b4…`) · **Builder:** `test7_build_windows.py` v1.0
**Status:** **STOP** — zbiór okien ryzyka i czasów zbudowany i udokumentowany. Żadna
statystyka czasów oczekiwania nie policzona (§6 brief). Czeka na przegląd przed Etapem B.

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

## 5. Epizody częściowo w oknie — 4 przypadki, zgłoszone (§3.3 brief)

Epizod uznany za „częściowo w oknie", gdy jego początek lub koniec mieści się w oknie
diady, ale nie oba naraz — **wykluczony** z sekwencji zdarzeń (nie obcięty po cichu),
wypisany osobno w `test7_partial_episodes.csv`:

| diada | epizod | okno diady | strona przecięta |
|---|---|---|---|
| France–Italy | II wś (1939–1945) | [1881,1940] | koniec okna (1940) wypada w trakcie wojny |
| Germany–Poland | II wś (1939–1945) | [1918,1939] | koniec okna dokładnie na starcie wojny |
| Italy–Ethiopia | II wś (1939–1945) | [1898,1943] | koniec okna (1943) wypada w trakcie wojny |
| Cambodia–Vietnam | Wojna wietnamska + Communist Coalition (1965–1975) | [1970,1983] | początek okna (1970) wypada w trakcie konfliktu |

Trzy z czterech to II wś kończąca akurat rywalizację (koniec okresu rywalizacji ≈ koniec
wojny, konwencja kodowania Thompsona kończy rywalizację wraz z wojną, która ją rozstrzyga).
**Nie rozstrzygam, jak je policzyć** (wliczyć częściowo, wykluczyć całkowicie, przyciąć do
granicy okna) — zgłaszam do decyzji przed Etapem B, zgodnie z §3.3 brief.

## 6. Struktura zbioru głównego

| typ wiersza | n | opis |
|---|---|---|
| `t0` | 62 | otwarcie okna → pierwszy epizod — **poza modelem głównym** (§5 protokołu) |
| `pelny` | 43 | odstęp między kolejnymi epizodami |
| `cenzurowany` | 62 | ostatni epizod → domknięcie okna |
| `cenzurowany_bez_epizodow` | 58 | diada bez żadnego epizodu w oknie — **cały okres jest jedną obserwacją cenzurowaną** |
| **razem** | **225** | 120 diad |

**58 diad bez epizodów** — brief §3.4 podkreślał, że to sedno testu („około siedemdziesięciu
par... jeżeli wypadną ze zbioru, coś poszło źle"). 58 jest niżej niż orientacyjne ~70 z D-016
(które liczyło na całej populacji 141, przed odrzuceniem 21 diad z pustym oknem) — proporcja
się zgadza: 58/120 = 48%, wobec ok. 70/141 = 50% w D-016. Nie zniknęły — są obecne i
stanowią prawie połowę zbioru.

## 7. Co pozostaje poza tą turą

Zgodnie z `TASK_7A_BRIEF.md` §0: żadnych kolumn dla H9b.2 (straty, czas trwania,
status mocarstwowy) — nie budowane nawet „na zapas". COW NMC i ICOW nie dostarczone,
model H9b.2 odłożony.

## 8. STOP

Zbiór zbudowany: `test7_windows.csv` (125 okresów ryzyka dla 120 diad — 5 diad ma dwa
ważne okresy, w tym China–Japan i Iran–Afghanistan z §3), `test7_intervals.csv` (225 wierszy
obserwacji), `test7_partial_episodes.csv` (4 przypadki do rozstrzygnięcia). Liczby kontrolne §1 zgodne po sprostowaniu D-020; kontrola §4 (213/225)
w pełni wyjaśniona; kontrola nazw §5 zgodna z D-016. **Nie liczę żadnej statystyki czasów
oczekiwania — ani CV, ani mediany, ani parametru kształtu.** Czekam na przegląd i na
rozstrzygnięcie w sprawie czterech epizodów częściowych (§5 tego raportu) przed Etapem B.
