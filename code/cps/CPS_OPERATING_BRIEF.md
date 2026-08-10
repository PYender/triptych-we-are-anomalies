# CPS_OPERATING_BRIEF

**Instrukcja operacyjna dla sesji Claude Code — projekt CPS**
Wersja 1.1 · 10 sierpnia 2026 · język roboczy: polski

Ten plik odpowiada na pytanie **„co robić i skąd wziąć dane"**.
Na pytanie **„co wiemy i czego nie wolno"** odpowiada `CPS_CONTEXT_PACK.md`.
Na pytanie **„co już rozstrzygnięto i dlaczego"** — `CPS_DECISION_LOG.md`.
Na pytanie **„jakie jest dzisiejsze zadanie"** — `TESTn_PROTOCOL.md`.

Wklejaj wszystkie cztery, w tej kolejności, na początku sesji.

---

## 1. Punkt wyjścia

Poprzednia sesja (gałąź `claude/check-repo-access-73swA`, PR #3) została **zamknięta
i zmergowana**. Jej historia jest niedostępna, a to co z niej zostało w repozytorium
zawiera błędy wymienione w §5 context packu.

Nie zakładaj ciągłości. Nie odwołuj się do „poprzednich ustaleń" spoza tych trzech
plików. Jeżeli czegoś w nich nie ma — zapytaj, nie zrekonstruuj.

---

## 2. Dokumenty w repozytorium, którym nie wolno ufać bez erraty

Te pliki są na `main` i wyglądają jak stan wiedzy projektu. **Nie są.**

| Plik | Co jest w nim błędne |
|---|---|
| `Podsumowanie_walidacji_modelu_CPS_1.md` | tabela TEST 2 miesza dwa różne uruchomienia (χ² i T z runu AIC, p z runu AR-3); przypisuje Tryptykowi okno predykcji 2023–2027, podczas gdy Tryptyk mówi 2027–2030; pomija run `2026prelim_ar3`, którego wynik był gorszy; ekstrapoluje trend p(n) |
| `NOTE_2026_iran_prelim.md` | opiera się na zmyślonych punktach danych 2025–2026; kotwica „ostatni szczyt 1991" nie ma oparcia w serii; zapowiada p ≈ 0,05–0,08, a faktyczny wynik to 0,109 i nie został poprawiony |
| `epoch_folding_test_results_ar3.csv` | etykiety okien mówią „1816–2007" i „1918–2007" przy n = 209 i n = 107 — to są okna do 2024 (błąd etykiety w skrypcie) |
| `wars_extended_2026.csv` | zawiera zmyślone wartości `UCDP_EST` dla 2025 i 2026 — **kwarantanna** |
| `cps_extended_2024.csv` | duplikat `wars_extended_2024.csv` |

Osobno: w zamkniętej sesji padła teza, że **epoch-folding jest odporny na splice**,
bo „operuje na strukturze fazowej, nie amplitudzie". Jest fałszywa — statystyka sumuje
odchylenia średnich w koszach fazowych od średniej globalnej, więc trwały skok poziomu
podnosi χ² niezależnie od rytmu. Jeżeli natkniesz się na to twierdzenie w repo lub
odtworzysz je samodzielnie — jest błędne.

---

## 3. Skąd wziąć dane

### 3.1 Pliki źródłowe (są w repo, nie modyfikuj)

Ścieżki względem `code/cps/`.

| Plik | Lokalizacja | Zawiera |
|---|---|---|
| `wars_color.csv` | `code/cps/` | zagregowany blok COW 1816–2007, kolumna `wars` |
| `UcdpPrioConflict_v25_1.csv` | `data/ucdp/` | UCDP/PRIO ACD v25.1, poziom konflikt-rok |
| `BattleDeaths`, `NonState`, `OneSided`, `Dyadic` v25.1 | `data/ucdp/` | tylko rodzina testów 3, gdy protokół tego wymaga |
| `INTRA-STATE WARS v5.1.dta` | `data/cow/` | jeden z czterech zbiorów COW, **format Stata** |
| `INTRA-STATE_State_participant v5.1.dta` | `data/cow/` | poziom uczestnika |

### 3.1.1 Braki w warstwie źródłowej — stan na sierpień 2026

| Brak | Skutek |
|---|---|
| **Inter-State v4.0** (95 wojen, waga **1,0**) | seria COW nieodtwarzalna; to zbiór dominujący szczyty cyklu |
| **Extra-State v4.0** (163, waga 0,7) | j.w. |
| **Non-State v4.0** (62, waga 0,4) | j.w. |
| **`population.csv`** (OWID) | w `data/owid/` są tylko `population.metadata.json` i `readme.md`; warianty per capita nieodtwarzalne |

Wszystkie brakujące pliki to małe CSV — nic nie stoi na przeszkodzie, by je dodać.
Do czasu ich uzupełnienia blok COW w `wars_color.csv` jest **przyjmowany jako dany**
(kryterium D1 z Testu 0 niespełnione) i musi być tak opisany w rozdziale.

**Uwaga o formacie.** Pliki COW w repo są w `.dta`, a `load_warfile` w opublikowanym
skrypcie czyta CSV. Kanoniczne mają być CSV; `.dta` może leżeć obok. Nie przepisuj
loadera pod `.dta` bez uzgodnienia.

**Niewykorzystany zasób.** INTRA-STATE jest w wersji v5.1 (do 2014), pozostałe zbiory
kończą się na 2007, a skrypt ucina wszystko na `range(1816, 2008)` — lata 2008–2014
dla konfliktów wewnętrznych istnieją i nigdy nie były użyte. To daje test diagnozy
cenzurowania: jeżeli spadek serii do 1,6 w 2007 wynika z zamknięcia zbiorów v4.0,
to INTRA-STATE v5.1 nie powinien się w 2007 załamywać. Wynik przesądza, czy odcięcie
na 2003 jest konieczne.

Pozostałe pliki UCDP (`BattleDeaths`, `NonState`, `OneSided`, `Dyadic`) są w repo,
ale **nie wchodzą** do serii kanonicznej — służą wyłącznie testom replikacyjnym
z rodziny 3, i tylko gdy protokół tego wymaga.

### 3.2 Plik roboczy (wygeneruj sam, nie ufaj kopii)

`cps_canonical_v2.csv` jest **jedynym dopuszczalnym wejściem** do testów.
Powstaje ze skryptu `test0c_build_canonical.py`:

```bash
python test0c_build_canonical.py --data-dir <katalog-z-danymi> --out-dir out/
```

Wygeneruj go na starcie sesji, nawet jeśli plik już jest w repo, i **porównaj
wyjście kontrolne**. Jeżeli którakolwiek liczba się nie zgadza — zatrzymaj się
i zgłoś:

```
[W] skala=0.449 | D2 iloraz=1.35 PASS | D3 skok=+1.08 SD FAIL | 2007=3.8
[P] skala=0.710 | D2 iloraz=1.26 PASS | D3 skok=+0.23 SD PASS | 2007=11.5
warianty: ['A_COW_W', 'C_SPLICED_W', 'A_COW_P', 'C_SPLICED_P', 'B_UCDP']
```

Kontrola dodatkowa (`test0b_cow_rebuild.py`): replika reguły z v0.1 musi dać
`maks|Δ| = 0.000000` wobec `wars_color.csv`. To dowód, że łańcuch od plików
surowych do serii jest odtworzony wiernie, zanim nałożymy na niego korekty.

**Wycofane:** `cps_canonical_v1.csv` i `test0_data_layer.py` powstały przed
korektami F1–F3 i przed decyzją D-001. Zostają w repo jako zapis, nie jako wejście.

### 3.3 Polityka pochodzenia danych

Trzy poziomy, zależnie od rozmiaru i roli zasobu.

**Poziom 1 — w repozytorium.** Wszystko poniżej ~10 MB, co jest potrzebne do odtworzenia
serii: zbiory COW (CSV), UCDP v25.1, `population.csv`, tabele pośrednie.

**Poziom 2 — produkt pośredni w repo, źródło poza repo.** Google Books N-grams.
Do odtworzenia COLOR nie są potrzebne pliki `.gz` (116–433 MB każdy, 12 liter), tylko
tabela rocznych częstości 20 słów kluczowych plus globalny mianownik — ~192 wiersze,
kilkadziesiąt kB. Do repo trafia ta tabela oraz manifest źródeł (URL, stamp `20120701`,
sha256 każdego `.gz`).

**Poziom 3 — tylko dokumentacja.** GDELT Events (~6,4 GB). W modelu pełni rolę wyłącznie
diagnostyczną, a roczne agregaty (`gdelt_wars`, `gdelt_goldstein`) są już w `wars_color.csv`.
Do repo trafia skrypt agregujący i manifest, nic więcej.

Duże pliki, jeśli mają być publiczne, idą na **Zenodo** (DOI, wersjonowanie), nie do
gita. Nie commituj `.gz` ani plików GDELT **ani raz** — historia gita jest trwała,
a usunięcie wymaga przepisania historii, co przy `CITATION.cff` i publikacjach
odsyłających do konkretnych wersji jest kłopotliwe. Repo ma `.gitignore` na `*.gz`.

Konsekwencje, które trzeba mówić wprost zamiast obchodzić:

- rodzina testów 6 (rozszerzenie leksykonu COLOR) wymaga **liter `m` i `n`**, których
  nie ma w pobranym komplecie 12 liter (`a b c d e h i p r s t w`) — bez nich nie
  policzysz `missile` ani `nuclear`; `deterrence` i `containment` są osiągalne;
- do wszystkich pozostałych zaplanowanych testów wystarczają pliki z §3.1 — nie proś o `.gz`.

---

## 4. Checklista startu sesji

1. Przeczytaj `CPS_CONTEXT_PACK.md`, ten plik i protokół dnia. Potwierdź jednym zdaniem.
2. Wygeneruj `cps_canonical_v1.csv`; porównaj hashe i wyjście kontrolne z §3.2.
3. Sanity check serii: `A_COW` ma 188 wierszy (1816–2003), `B_UCDP` 79 (1946–2024),
   `C_SPLICED` 209. Kolumna `value_ma11t` istnieje i nie jest kopią `value_ma11c`.
4. Załóż gałąź `claude/cps-test-<n>`. Nie pracuj na `main`.
5. Dopiero teraz zacznij zadanie.

---

## 5. Pętla robocza jednego testu

```
protokół (dostajesz)  →  kod (.py + bliźniaczy .md)  →  przegląd autora  →
uruchomienie  →  wyniki (.csv + .pdf)  →  raport (.md)  →  PR
```

Zatrzymaj się po napisaniu kodu i **poczekaj na przegląd**, zanim uruchomisz.
Kod idzie do oceny jako plik `.md` z tą samą treścią, żeby dało się go czytać
i poprawiać niezależnie od wykonania.

Nie łącz dwóch testów w jednej sesji. Powód jest praktyczny: kompaktowanie kontekstu
zastępuje oryginał stratnym streszczeniem, a w tym projekcie streszczenia były już
źródłem błędów. Jedna sesja = jeden test = jeden PR.

---

## 6. Definicja ukończenia

Test jest skończony, gdy **wszystkie** poniższe są prawdziwe:

- [ ] wyniki pochodzą z serii dopuszczonej przez protokół — domyślnie `A_COW_W` (D-001); nie z `wars_extended_2026.csv`, nie z `cps_canonical_v1.csv`;
- [ ] każdy plik wyjściowy ma nagłówek `#` z wersją skryptu i sha256 wejść;
- [ ] ziarno losowe jest ustawione jawnie i zapisane w wyniku;
- [ ] raportowane są **wszystkie** uruchomione warianty, także te o gorszym wyniku;
- [ ] wskazany jest wariant pierwszorzędny, ustalony **przed** uruchomieniem;
- [ ] raport zawiera zdanie o tym, czy kryterium falsyfikacji z protokołu zostało spełnione;
- [ ] żadne twierdzenie w raporcie nie wykracza poza to, co mierzy statystyka.

---

## 7. Sytuacje wyjątkowe

**Wynik jest sprzeczny z hipotezą.** Zaraportuj go. Nie przeprojektowuj testu.
Nie tłumacz porażki „złym doborem narzędzia", chyba że potrafisz wskazać konkretną,
nazwaną własność metody, która to uzasadnia — i wtedy napisz to jako propozycję
nowego protokołu, nie jako korektę wyniku.

**Protokół okazuje się niewykonalny.** Zatrzymaj się i zgłoś. Nie improwizuj wariantu.

**Nie wiesz, jaką wartość parametru przyjąć.** Lista decyzji zastrzeżonych dla autora
jest w §8 context packu (rząd nulla, granice epok, wagi, kryterium falsyfikacji,
wybór testu pierwszorzędnego). Zapytaj.

**Brakuje pliku.** Sprawdź §3.3, zanim zapytasz — być może go po prostu nie ma
i nigdy nie będzie.

---

## 8. Konwencje repozytorium

- Repo: `github.com/PYender/triptych-we-are-anomalies`, katalog roboczy `code/cps/`.
- Gałąź: `claude/cps-test-<n>`, jeden PR na test.
- Commit zawiera: kod, bliźniaczy `.md`, wyniki `.csv`, wykres `.pdf`, raport `.md`.
- Wersja v0.1 Tryptyku jest **zamrożona jako archiwalna**. Poprawki wchodzą jako
  wersjonowana errata, nigdy jako cicha podmiana — repo ma `CITATION.cff` i publikacje
  na Zenodo, które odsyłają do konkretnej wersji.
- Nie usuwaj plików z listy w §2. Są zapisem błędów i mają wartość dokumentacyjną.
  Dodaj do każdego nagłówek odsyłający do erraty.
