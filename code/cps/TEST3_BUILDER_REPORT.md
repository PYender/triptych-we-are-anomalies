# TEST 3 — RAPORT BUILDERA (Etap A: parametryzacja `test0c_build_canonical.py`)

**Protokół:** `TEST3_PROTOCOL.md` v1.0 · **Zadanie:** `TASK_3.md` Etap A · **Data:** 2026-08-12
**Skrypt:** `test0c_build_canonical.py` **v2.1** (było v2.0)
**Status:** **STOP** — kod testu nie napisany, żadna statystyka nie liczona.

---

## 1. Co zmieniono

Dodano dwa parametry multiwersum (D-008), oba z wartościami domyślnymi
odtwarzającymi zachowanie v2.0. Logika budowania serii **nie została przepisana** —
parametry są doszyte (zgodnie z preferowaną formą z §A2):

- `--weights {inherited,equal,steep,flat}` (domyślnie `inherited`) — zestaw wag
  kategorii COW (Inter/Extra/Non/Intra), §3.2 protokołu / A3.
- `--normalization {raw,pc_full,pc_1950}` (domyślnie `raw`) — normalizacja per capita,
  §3.3 / A4. `pc_1950` to kontrola poza siatką główną (dane roczne, 1950–2007).

Korekty F1–F3 obowiązują we **wszystkich** wariantach — to poprawki błędów, nie
wymiar multiwersum. Nowe funkcje importowalne (`build_cow(dd, level, weights)`,
`world_population(dd)`, `apply_normalization(s, mode, dd)`) — Etap C wykorzysta je
zamiast powielać logikę.

## 2. Dowód regresji (warunek nienaruszalności, §A2)

Bieg domyślny po modyfikacji:

```
python test0c_build_canonical.py --data-dir data --out-dir <tmp>
[W] skala=0.449 | D2 iloraz=1.35 PASS | D3 skok=+1.08 SD FAIL | 2007=3.8
[P] skala=0.710 | D2 iloraz=1.26 PASS | D3 skok=+0.23 SD PASS | 2007=11.5
```

Linia kontrolna **identyczna** z briefem §3.2. ✅

**Dane serii — bit w bit identyczne.** sha256 wierszy danych (plik bez linii
nagłówka `#`, którą wszyscy konsumenci pomijają przez `comment="#"`):

| | sha256 (dane, 16 zn.) |
|---|---|
| nowy build (domyślny) | `77c1159084954826` |
| `cps_canonical_v2.csv` na `main` | `77c1159084954826` |

Identyczne. Wszystkie serie (`A_COW_W/P`, `B_UCDP`, `C_SPLICED_*`, wszystkie kolumny
`value/ma11c/ma11t`) są niezmienione — wyniki Testów 1 i 2B stoją nienaruszone.

### 2.1 Rozbieżność do rozstrzygnięcia: pełny sha pliku ≠ 145aed00 (tylko nagłówek)

Pełny sha256 pliku wynosi `7c24783b…`, a **nie** `145aed00…` z §A2. Różnica jest
**wyłącznie w linii nagłówka `#`** i wynika z dwóch rzeczy, obu wymaganych/proweniencyjnych:

- bump wersji `"script": v2.0 → v2.1` (wymagany w §A5);
- dwa klucze proweniencji: `"weights": "inherited"`, `"normalization": "raw"`.

Nagłówek jest czytany przez **żadnego** konsumenta (Test 1, Test 2B i builder używają
`pd.read_csv(..., comment="#")`), więc merytoryczny niezmiennik „domyślne zachowanie
nienaruszone" jest spełniony — dane są identyczne. Ale §A2 żąda pełnej identyczności
pliku i mówi „jakakolwiek różnica = zatrzymanie i zgłoszenie", więc **zgłaszam** i nie
rozstrzygam sam. Tu §A2 (pełny sha) i §A5 (wersja v2.1 w nagłówku) są w sprzeczności.

**Rozstrzygnięte (autor).** Zaakceptowano zmianę nagłówka: kryterium regresji to
**suma kontrolna wierszy danych po pominięciu nagłówka** plus zgodność linii
kontrolnej — oba spełnione. Nagłówek `#` niesie proweniencję i ma się zmieniać wraz
ze skryptem. Bez zmiany kodu.

## 3. Normalizacja i interpolacja (deklaracja, §A4 / §2.1)

Ludność: `population.csv`, `Entity == "World"`, kolumna `Population (historical)`,
**interpolowana liniowo** na serii natywnej (z punktami sprzed 1816) i wycięta do
1816–2007. Diagnostyka pokrycia (pełny rozkład, zaakceptowany przez autora):

| podokres | lata | pomiary | interpolowane | udział interpolacji |
|---|---|---|---|---|
| 1816–1949 | 134 | 13 | 121 | **90,3%** |
| 1950–2007 | 58 | 58 | 0 | 0% |
| całość 1816–2007 | 192 | 71 | 121 | **63,0%** |

Pomiary dekadowe do 1940, roczne od 1950. Punkty 1800 i 1810 istnieją w danych, więc
lata **1816–1819 są INTERPOLOWANE** (między 1810 a 1820: 1050,95 → 1065,62 mln), nie
ekstrapolowane — **w oknie 1816–2007 nie ma ekstrapolacji** (sprostowanie wcześniejszej
uwagi buildera; potwierdzone przez autora).

**Korekta liczby w §2.1 protokołu (zaakceptowana).** Protokół podawał „~79%"
interpolacji przed 1950; poprawna wartość to **90,3%** (121/134 lat 1816–1949) —
poprzednia liczba była błędem rachunkowym (błędna podstawa dzielenia). Liczba pomiarów
(71) i pustych lat (121 na 192) była poprawna. Korekta jest **niekorzystna**:
wzmacnia ostrzeżenie o wariancie per capita (więcej interpolacji, nie mniej), i tak
należy ją zapisać. Nie zmienia planu — per capita wchodzi do siatki (D-A).

## 4. Tabela kontrolna — 12 kombinacji wag × normalizacji, oba poziomy

Wartości surowe w jednostkach naturalnych; per capita w „na osobę" (×10⁻⁹).
**M1 i M2 są niezmiennicze względem skali** (ilorazy mocy / wariancji), więc mała
wartość bezwzględna per capita nie wpływa na statystyki testu.

| poziom | wagi | norm | n | średnia | odch. std | rok 2007 |
|---|---|---|---|---|---|---|
| W | inherited | raw | 192 | 5,765 | 2,494 | 3,80 |
| W | inherited | pc_full | 192 | 2,89e−9 | 1,60e−9 | 5,62e−10 |
| W | inherited | pc_1950 | 58 | 1,76e−9 | 4,96e−10 | 5,62e−10 |
| W | equal | raw | 192 | 10,90 | 5,221 | 8,00 |
| W | equal | pc_full | 192 | 5,36e−9 | 2,97e−9 | 1,18e−9 |
| W | equal | pc_1950 | 58 | 3,48e−9 | 8,70e−10 | 1,18e−9 |
| W | steep | raw | 192 | 4,163 | 1,864 | 2,50 |
| W | steep | pc_full | 192 | 2,09e−9 | 1,19e−9 | 3,70e−10 |
| W | steep | pc_1950 | 58 | 1,26e−9 | 4,09e−10 | 3,70e−10 |
| W | flat | raw | 192 | 7,947 | 3,793 | 5,60 |
| W | flat | pc_full | 192 | 3,90e−9 | 2,16e−9 | 8,29e−10 |
| W | flat | pc_1950 | 58 | 2,53e−9 | 6,52e−10 | 8,29e−10 |
| P | inherited | raw | 192 | 9,203 | 5,594 | 11,50 |
| P | inherited | pc_full | 192 | 4,35e−9 | 2,74e−9 | 1,70e−9 |
| P | inherited | pc_1950 | 58 | 3,06e−9 | 1,66e−9 | 1,70e−9 |
| P | equal | raw | 192 | 14,55 | 7,387 | 19,00 |
| P | equal | pc_full | 192 | 6,89e−9 | 3,66e−9 | 2,81e−9 |
| P | equal | pc_1950 | 58 | 4,86e−9 | 1,65e−9 | 2,81e−9 |
| P | steep | raw | 192 | 7,460 | 5,314 | 8,00 |
| P | steep | pc_full | 192 | 3,50e−9 | 2,55e−9 | 1,18e−9 |
| P | steep | pc_1950 | 58 | 2,50e−9 | 1,67e−9 | 1,18e−9 |
| P | flat | raw | 192 | 11,39 | 6,306 | 13,30 |
| P | flat | pc_full | 192 | 5,36e−9 | 3,07e−9 | 1,97e−9 |
| P | flat | pc_1950 | 58 | 3,83e−9 | 1,64e−9 | 1,97e−9 |

Kontrole spójności: `W/inherited/raw` daje 2007 = 3,80 i średnią 5,765 (zgodne z linią
kontrolną); `P/inherited/raw` daje 2007 = 11,50. Wagi `equal` (wszystkie 1,0) podnoszą
poziom, `steep` obniżają — zgodnie z konstrukcją. `pc_1950` ma n = 58 (1950–2007).

## 5. Uwaga (propozycja, nie wykonanie — §A2)

Nie wydzielałem funkcji budującej do osobnego modułu (§A2 zabrania robić to samemu).
Gdyby Etap C miał wołać builder 192+ razy, czystsze byłoby zaimportowanie
`build_cow`/`apply_normalization` (już importowalne) niż 192 uruchomienia CLI.
To jest propozycja do akceptacji, nie zmiana wykonana.

## 6. Status

Etap A **zaakceptowany** przez autora. Rozstrzygnięcia: (1) nagłówek — kryterium to
suma kontrolna wierszy danych (spełnione); (2) interpolacja pre-1950 = 90,3% (korekta
§2.1 przyjęta); (3) import funkcji buildera w Etapie C — zgoda, pod warunkiem braku
efektów ubocznych przy imporcie (spełnione: `main()` pod `__main__`, brak zapisu/wypisu
na poziomie modułu). Przechodzę do Etapu B (kod testu do przeglądu, bez uruchamiania).
