> **WYCOFANE — patrz `TEST0B_REPORT.md` i `CPS_DECISION_LOG.md` (D-003).**
>
> Ten dokument jest zachowany jako zapis ścieżki rozumowania. Jego dwa główne
> ustalenia zostały obalone przez Test 0B:
>
> - diagnoza „prawostronnego cenzurowania zbioru COW" była błędna — faktyczną
>   przyczyną deformacji końcówki serii jest niepoprawna obsługa kodu `-7`
>   (wojna trwająca) w kodzie agregującym, a nie brak danych;
> - wynikające z niej odcięcie serii na 2003 zostało cofnięte (D-003) — seria
>   biegnie do 2007;
> - kryterium D2 (stabilność kalibracji) nie przechodziło na serii sprzed korekt
>   F1–F3; na serii poprawionej przechodzi, więc odrzucenie serii sklejonej
>   również jest nieaktualne.
>
> Obowiązującą warstwą danych jest `cps_canonical_v2.csv` (Test 0C).

---

# TEST 0 — RAPORT: warstwa danych i kalibracja złączenia COW↔UCDP

**Protokół:** `TEST0_PROTOCOL.md` v1.0 (zamrożony przed uruchomieniem)
**Skrypt:** `test0_data_layer.py` v1.0
**Wejście:** `wars_color.csv` (sha256 `86f2ec64b8c1…`), `UcdpPrioConflict_v25_1.csv` (sha256 `356fd8ed…`)
**Wyjście:** `cps_canonical_v1.csv`, `test0_calibration.csv`, `test0_censoring.csv`, `test0_diagnostics.pdf`

---

## Krok A — zgodność plików w repozytorium

`wars_extended_2024.csv` i `cps_extended_2024.csv` są **identyczne** co do wartości
(różnią się wyłącznie nazwą kolumny `wars` / `wars_raw`) — jeden z nich jest zbędny.
Blok COW w obu zgadza się co do jednej dziesiętnej z kolumną `wars` w `wars_color.csv`.
Blok UCDP odtwarza się z pliku źródłowego regułą wag {2:1,0; 3:0,4; 4:0,7} przy stałym
mnożniku **0,5433** — czyli kalibracja z `ucdp_adapter.py` jest w pełni odtworzona.

**Kryterium D1 — spełnione dla UCDP.** Nie jest spełnione dla COW: surowe pliki COW
(`Inter-`, `Extra-`, `Non-`, `INTRA-StateWarData`) **nie znajdują się w repozytorium**,
więc blok 1816–2007 przyjmowany jest jako dany. To ograniczenie musi być wymienione
w rozdziale: dziś nikt z zewnątrz nie odtworzy tej serii od zera.

Uwaga uboczna: `wars_smooth` w `wars_color.csv` i w `wars_extended_2024.csv` **różni się
do 1,93 jednostki** dla tych samych lat, bo wygładzenie liczono na seriach różnej długości.
Cytowanie „wars_smooth" bez wskazania pliku jest więc niejednoznaczne.

## Krok B — ogon serii COW jest cenzurowany

Iloraz średnich COW/UCDP w oknach 10-letnich spada nieprzerwanie przez **cztery ostatnie
lata** serii COW. Wartości surowe mówią same za siebie:

| rok | 2003 | 2004 | 2005 | 2006 | 2007 |
|---|---|---|---|---|---|
| COW | 8,3 | 5,6 | 4,9 | 3,5 | **1,6** |
| UCDP ważone | 15,3 | 14,4 | 14,7 | 14,7 | 15,2 |

UCDP w tych samych latach jest płaskie. Spadek COW do 1,6 nie jest zjawiskiem
historycznym, tylko **prawostronnym cenzurowaniem**: wojny trwające w momencie zamknięcia
zbioru nie mają daty końca, więc warunek `Start ≤ rok ≤ End` przestaje je wyłapywać.

**Konsekwencja dla dotychczasowych wyników.** Ten sztuczny dołek leży bezpośrednio przed
blokiem UCDP. Tworzy fałszywe „V" na złączeniu, które (1) zawyża amplitudę rzekomego
wzrostu po 2008 i (2) zniekształca każdą skalę kalibracyjną liczoną na oknie sięgającym
2007. **Rok odcięcia: 2003.**

## Krok C — kalibracja nie jest własnością danych

| okno | skala | corr |
|---|---|---|
| 1946–2007 | 0,811 | 0,18 |
| 1970–2007 | 0,673 | 0,05 |
| 1989–2006 | **0,543** *(użyta w repo)* | 0,73 |
| 1989–2007 | 0,524 | 0,75 |
| 1997–2007 | 0,463 | 0,73 |
| 1990–2000 | 0,587 | 0,66 |
| 2000–2007 | 0,401 | 0,75 |
| regresja przez 0, 1989–2003 | 0,590 | 0,65 |

Iloraz skrajnych skal: **2,02**, przy progu 1,5.

**Kryterium D2 — NIESPEŁNIONE.** Wartość 0,543 nie jest cechą relacji COW↔UCDP, tylko
wyborem okna. Przy oknie o osiem lat krótszym seria po 2008 byłaby o **26% niższa**.

## Krok D — nieciągłość po odcięciu ogona znika

Przy skali wyznaczonej na oknie 1989–2003 (**0,578**) skok na złączeniu wynosi
**+0,03 jednostki = +0,01 SD** — **kryterium D3 spełnione**.

To ważne i pozytywne odkrycie: rażąca nieciągłość mierzona wcześniej (COW 2007 = 1,60 →
UCDP 2008 = 9,73, skok ~1,5×) była w **przeważającej części efektem cenzurowanego ogona
COW**, a nie samej kalibracji. Po usunięciu lat 2004–2007 obie serie schodzą się poziomem.

## Decyzja

Ponieważ **D2 nie jest spełnione**, seria sklejona zostaje **odrzucona jako podstawa
testów formalnych** i może występować wyłącznie jako ilustracja, z adnotacją o zależności
od okna kalibracji. Testy formalne przechodzą na serie jednorodne.

## Produkt: `cps_canonical_v1.csv`

| Wariant | Zakres | n | Rola |
|---|---|---|---|
| **A_COW** | 1816–2003 | 188 | jednorodna; podstawa testów spektralnych i fazowych |
| **B_UCDP** | 1946–2024 | 79 | jednorodna, niezależne kodowanie; replikacja |
| **C_SPLICED** | 1816–2024 | 209 | wyłącznie ilustracja (D2 FAIL) |

Każdy wariant ma trzy kolumny wartości: `value` (surowa), `value_ma11c` (centrowana MA-11)
i `value_ma11t` (**jednostronna** MA-11). Ta trzecia jest obowiązkowa w każdym teście
dotyczącym wyprzedzania w czasie — centrowana średnia wnosi do roku *t* informację z lat
*t+1…t+5* i unieważnia testy przyczynowości.

## Co to zmienia dla dotychczasowych liczb

Orientacyjnie (sama statystyka χ², bez bootstrapu — pełne p wymaga uruchomienia
`cross_epoch_phase_test.py` na nowych seriach):

| seria, epoka 2 od 1914 | n | χ² |
|---|---|---|
| z repo, sklejona starą skalą (1914–2024) | 111 | 51,9 |
| **A_COW (1914–2003)** | 90 | 47,3 |
| **C_SPLICED nową skalą (1914–2024)** | 111 | 55,6 |
| **B_UCDP (1946–2024), niezależna** | 79 | **7,8** |

Dwie rzeczy wymagają uwagi przy projektowaniu Testu 1:

1. Sygnał fazowy w epoce 2 **nie znika** po oczyszczeniu danych — na samej serii COW
   1914–2003 χ² wynosi 47,3, czyli praktycznie tyle, co na serii sklejonej. Podstawa
   twierdzenia o kontraście epok jest więc nienaruszona.
2. Seria UCDP jako niezależna replikacja daje χ² = **7,8**, czyli tyle co epoka
   przedglobalizacyjna. To wymaga wyjaśnienia w Teście 1: przy n = 79 mamy tam
   ~2,2 cyklu i UCDP mierzy w większości konflikty wewnątrzpaństwowe, więc nie jest to
   ta sama wielkość — ale nie wolno tego przemilczeć. Dziś to najsłabszy punkt tezy.

## Wnioski porządkowe do erraty

- **[S]** `wars_extended_2024.csv` i `cps_extended_2024.csv` — duplikat, jeden do usunięcia.
- **[M]** skala 0,543 raportowana jako wielkość zmierzona; jest wielkością wybraną.
- **[M]** ostatnie cztery lata serii COW są cenzurowane i były używane we wszystkich testach.
- **[S]** `wars_smooth` oznacza dwie różne rzeczy w dwóch plikach.
- **[M]** brak surowych plików COW w repo uniemożliwia niezależne odtworzenie serii bazowej.
