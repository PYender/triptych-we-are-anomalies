# TEST 0C — RAPORT: seria kanoniczna v2 i poziom agregacji

**Skrypt:** `test0c_build_canonical.py` v2.0
**Wyjście:** `cps_canonical_v2.csv`, `test0c_calibration.csv`
**Warianty:** `A_COW_W`, `A_COW_P`, `B_UCDP`, `C_SPLICED_W`, `C_SPLICED_P`

`W` = poziom wojny (deduplikacja po `WarNum`) — zgodny z opisem zmiennej w rozdziale.
`P` = poziom uczestnika (zliczanie wierszy) — stan faktyczny w wersji v0.1.
Obie serie liczone z plików surowych z korektami F1–F3 z Testu 0B.

---

## 1. Kalibracja i kryteria

| | poziom W | poziom P |
|---|---|---|
| skala COW→UCDP (1989–2007) | 0,449 | 0,710 |
| D2 (stabilność skali, próg 1,5) | 1,35 **PASS** | 1,26 **PASS** |
| D3 (skok na złączeniu, próg 0,5 SD) | +1,08 SD **FAIL** | +0,23 SD **PASS** |
| wartość 2007 | 3,8 | 11,5 |

## 2. Korelacja z niezależnym zbiorem UCDP na oknie wspólnym

| okno | poziom W | poziom P |
|---|---|---|
| 1946–2007 | **0,734** | 0,235 |
| 1970–2007 | **0,647** | −0,209 |
| 1989–2006 | **0,880** | 0,174 |
| 1989–2007 | **0,882** | 0,185 |
| 1997–2007 | **0,801** | −0,054 |
| 2000–2007 | **0,768** | −0,009 |

Na poziomie wojny COW i UCDP mierzą wyraźnie to samo zjawisko. Na poziomie
uczestnika korelacja znika lub zmienia znak. To jest mocna przesłanka, że
**W jest właściwą operacjonalizacją**, jeśli zmienna ma znaczyć „liczba wojen".

## 3. Kontrast epok — wynik krytyczny

χ² przy T = 35,1, MA(11), wartości orientacyjne (bez bootstrapu):

| wariant | epoka 1 (1816–1913) | epoka 2 (1914–) | n₂ |
|---|---|---|---|
| **A_COW_W** | **14,53** | **6,97** | 94 |
| A_COW_P | 7,43 | 39,49 | 94 |
| C_SPLICED_W | 14,53 | 20,14 | 111 |
| C_SPLICED_P | 7,43 | 47,50 | 111 |
| B_UCDP | — | 7,84 | 79 |

Korelacja `A_COW_W` z `A_COW_P` wynosi 0,599 — to są dwie różne serie, nie warianty
tej samej.

### Co z tego wynika

**Kontrast epok odwraca się przy przejściu na poziom wojny.** Przy zliczaniu
uczestników epoka 2 jest ok. 5× silniejsza od epoki 1 (39,5 vs 7,4). Przy zliczaniu
wojen jest **słabsza** (7,0 vs 14,5).

**Seria wojno-poziomowa zgadza się z niezależnym UCDP.** χ² = 6,97 dla `A_COW_W`
i 7,84 dla `B_UCDP` — obie serie mówią to samo. Rozbieżność zgłoszona w Teście 0
(47,3 vs 7,8) była więc w znacznej części skutkiem porównywania uczestniko-lat
z wojno-latami, a nie realną niezgodnością zbiorów.

**Efekt jest zdominowany przez wojny wielostronne.** Na poziomie uczestnika I i II
wojna światowa wnoszą po kilkanaście–kilkadziesiąt wierszo-lat każda i stoją
w epoce 2 blisko siebie fazowo. To wystarcza, by wygenerować silny profil złożony
bez powtarzalnego rytmu.

## 4. Dwie możliwe odpowiedzi — decyzja merytoryczna, nie techniczna

**Odczyt A — wynik jest artefaktem agregacji.** Rozdział deklaruje pomiar liczby
wojen, mierzy uczestniko-lata, a przy pomiarze zgodnym z deklaracją efekt znika.
Wtedy teza o kontraście epok w obecnej postaci upada i trzeba ją wycofać.

**Odczyt B — zliczanie uczestników jest lepszą operacjonalizacją.** Liczba stron
konfliktu jest miarą *systemowego zaangażowania*, a więc dokładnie tego, co
hipoteza globalizacyjna przewiduje: po 1914 wojny wciągają wiele państw naraz.
Wojna dwudziestostronna nie jest dwudziestoma wojnami, ale też nie jest tym samym,
co wojna dwustronna. Wtedy jednak:

- zmienna musi zostać przemianowana i zdefiniowana wprost (np. „uczestniko-lata
  ważone typem konfliktu"), a nie opisywana jako „liczba wojen";
- wagi 1,0 / 0,7 / 0,4 wymagają ponownego uzasadnienia, bo działają na innej
  wielkości, niż zakładano;
- niezgodność z UCDP na poziomie uczestnika (r ≈ 0) przestaje być usterką,
  a staje się twierdzeniem wymagającym obrony;
- rodzina testów 4 przestaje być testem odporności i staje się **testem centralnym**.

Odczyt B jest obronialny, ale wymaga świadomej deklaracji **przed** testami, a nie
po zobaczeniu, który wariant daje mocniejszy wynik. To jest zakaz nr 10 z context packu
i obowiązuje również autora.

## 5. Rekomendacja

Zadeklarować **przed** uruchomieniem rodziny 1–3, która seria jest pierwszorzędna,
i uzasadnić to niezależnie od wyniku χ². Argument za `W`: zgodność z opisem zmiennej
i z niezależnym zbiorem. Argument za `P`: bezpośrednie mierzenie umiędzynarodowienia
konfliktu, czyli mechanizmu z hipotezy.

Niezależnie od wyboru **oba warianty muszą być raportowane** w rozdziale, razem
z tą tabelą. Zatajenie odwrócenia kontrastu byłoby najpoważniejszym możliwym
uchybieniem w całym projekcie.

## 6. Wpisy do erraty

- **[M]** kontrast epok, na którym opiera się teza, zależy od poziomu agregacji
  i odwraca się przy zliczaniu wojen zamiast uczestników;
- **[S]** rozbieżność COW vs UCDP zgłoszona w Teście 0 (47,3 vs 7,8) była w dużej
  części artefaktem porównywania różnych poziomów agregacji;
- **[M]** wagi typów konfliktu były kalibrowane na wielkości innej niż deklarowana.
