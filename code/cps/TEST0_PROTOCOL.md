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

# TEST 0 — PROTOKÓŁ: warstwa danych i kalibracja złączenia COW↔UCDP

**Status:** zamrożony przed uruchomieniem kodu
**Wersja protokołu:** 1.0
**Kolejność obowiązkowa:** protokół → kod → uruchomienie → raport. Żadna decyzja
metodyczna nie może być podjęta po zobaczeniu wyników.

---

## 1. Cel

Test 0 nie testuje żadnej hipotezy merytorycznej. Ustala, **na jakiej serii wolno
liczyć cokolwiek innego**. Powód: w repozytorium współistnieje pięć nakładających się
plików serii, a współczynnik kalibracji złączenia COW→UCDP (0,5433) został wyznaczony
na oknie 1989–2006 i nie był sprawdzany poza nim.

Wszystkie dotychczasowe wyniki fazowe (w tym p = 0,087) pochodzą z serii sklejonej.
Jeśli sklejenie nie spełnia kryteriów poniżej, ta liczba nie może być raportowana
jako wynik dotyczący cyklu.

## 2. Dane wejściowe

| Plik | Rola | Uwaga |
|---|---|---|
| `wars_color.csv` | blok COW 1816–2007 (kolumna `wars`) | surowe pliki COW **nie są** w repo — blok przyjmowany jako dany, identyfikowany hashem |
| `UcdpPrioConflict_v25_1.csv` | blok UCDP 1946–2024 | odtwarzany od zera z pliku źródłowego |
| `wars_extended_2024.csv`, `cps_extended_2024.csv`, `wars_extended_2026.csv`, `ucdp_color.csv` | wyłącznie do weryfikacji zgodności | nie są wejściem do serii kanonicznej |

Hashe SHA-256 obu plików wejściowych zapisywane w nagłówku każdego pliku wyjściowego.

## 3. Reguła agregacji UCDP

Wagi odwzorowujące typologię COW, zgodnie z tym co zastosowano w `ucdp_adapter.py`:

| `type_of_conflict` | opis | waga |
|---|---|---|
| 2 | interstate | 1,0 |
| 3 | intrastate | 0,4 |
| 4 | internationalized intrastate | 0,7 |
| 1 | extrasystemic | pomijany |

`ucdp_raw(y)` = suma wag po wszystkich wierszach konflikt-rok w roku `y`.

Wagi są **odziedziczone, nie wybrane** — ich wrażliwość bada osobno rodzina testów 4,
nie Test 0.

## 4. Procedura

**Krok A — weryfikacja zgodności plików pochodnych.** Sprawdzenie, czy pliki serii
w repo są wzajemnie spójne i czy blok UCDP w `wars_extended_2024.csv` daje się
odtworzyć z pliku źródłowego przy jakiejś stałej skali.

**Krok B — diagnostyka cenzurowania ogona COW.** Dla okna wspólnego 1946–2007
porównanie przebiegu COW i UCDP w ostatnich latach serii COW. Miara: iloraz
średniej COW do średniej UCDP liczony w ruchomych oknach 10-letnich. Monotoniczny
spadek tego ilorazu w kierunku końca serii jest sygnaturą prawostronnego cenzurowania
(wojny trwające w momencie zamknięcia zbioru nie mają daty końca i wypadają z licznika).

**Krok C — stabilność skali kalibracyjnej.** Wyznaczenie skali `s = mean(COW)/mean(UCDP)`
na siedmiu oknach: 1946–2007, 1970–2007, 1989–2006, 1989–2007, 1997–2007, 1990–2000,
2000–2007. Dodatkowo regresja przez zero.

**Krok D — pomiar nieciągłości na złączeniu.** Dla każdej kandydującej skali:
różnica średniej z 10 lat przed złączeniem i 10 lat po nim, wyrażona w odchyleniach
standardowych serii COW.

**Krok E — budowa serii kanonicznych.**

## 5. Kryteria akceptacji (ustalone przed uruchomieniem)

**D1 — odtwarzalność.** Blok UCDP musi być odtwarzalny z pliku źródłowego regułą
z §3. Blok COW nie jest odtwarzalny (brak plików źródłowych w repo) — przyjmowany
jako dany i oznaczany jako ograniczenie.

**D2 — stabilność kalibracji.** Iloraz największej do najmniejszej skali z Kroku C
musi wynosić **< 1,5**. Powyżej tej wartości skala nie jest własnością danych, tylko
wybranego okna.

**D3 — ciągłość na złączeniu.** Nieciągłość z Kroku D musi wynosić **< 0,5 SD**
serii COW.

**Reguła decyzyjna.** Jeżeli D2 **lub** D3 nie jest spełnione, seria sklejona zostaje
odrzucona jako podstawa testów formalnych i może być używana wyłącznie jako ilustracja,
z jawną adnotacją. Testy formalne przechodzą wtedy na serie jednorodne.

## 6. Produkt: serie kanoniczne

Niezależnie od wyniku D2/D3 powstają trzy serie, każda z własnym przeznaczeniem:

| Wariant | Zakres | Przeznaczenie |
|---|---|---|
| **A — COW** | 1816 do roku odcięcia z Kroku B | jednorodna; podstawa testów spektralnych i fazowych |
| **B — UCDP** | 1946–2024 | jednorodna, niezależne kodowanie; replikacja |
| **C — sklejona** | A + przeskalowane B | wyłącznie ilustracja, o ile D2/D3 nie przejdą |

Dla każdej: seria surowa, wygładzenie centrowane MA(11) oraz **wygładzenie jednostronne
(trailing) MA(11)**. To drugie jest obowiązkowe wszędzie tam, gdzie test dotyczy
wyprzedzania w czasie — centrowana średnia wnosi do roku *t* informację z lat *t+1…t+5*
i unieważnia każdy test przyczynowości (błąd popełniony w sesji lutowej).

## 7. Czego Test 0 nie rozstrzyga

Nie orzeka o istnieniu cyklu, o okresie, o roli COLOR ani o wagach typów konfliktu.
Rozstrzyga wyłącznie, która seria jest dopuszczalnym wejściem do tych pytań.
