# TEST 4 — RAPORT: odporność kontrastu epok na obserwacje odstające

**Rodzina 2, kontrola H2** · **Realizuje:** `TEST4_PROTOCOL.md` v1.0 (D-010)
**Kod:** `test4_robustness.py` (zatwierdzony w przeglądzie przed biegiem) · **Bieg:** 2026-08-14
**Wejście:** `cps_canonical_v2.csv` (sha256 `145aed00…`), warianty `A_COW_P` (pierwszorzędny)
i `A_COW_W` (porównawczy), kolumna `value`. **Null:** AR(3), rząd z góry, B = 2000, ziarno 20260814.

Test dotyczy **wyłącznie H2** (umiędzynarodowienie), nie H1 i nie istnienia cyklu.

---

## 1. Wynik w jednym zdaniu

**Kryterium §6 spełnione — wynik POZYTYWNY.** Kontrast epok w serii uczestniczej
`A_COW_P` przy usunięciu 5 najwyższych lat epoki 2 daje **M2 = 24,91, p = 0,0085**
(warunek 1: M2 > 0 i p < 0,05 — spełniony), a spadek M2 między k = 0 a k = 5 wynosi
**−0,54** (M2 wręcz rośnie) wobec oczekiwanego z losowego usuwania **1,63 ± 3,07**
(warunek 2: w paśmie S4 — spełniony). To **pierwszy pozytywny wynik w całym projekcie**.

Kontrast **nie jest funkcją kilku lat skrajnych**: usuwanie kolejnych najwyższych lat
epoki 2 nie znosi go, lecz go umacnia (k = 10: M2 = 30,23, p = 0,0020). Odpowiedź na
pytanie „ile obserwacji trzeba usunąć, żeby wynik zniknął" brzmi: **nie znika nawet
po dziesięciu** (protokół §4: „kontrast jest własnością rozkładu").

**Czego ten wynik NIE mówi** (§7, §B2):
- nie dotyczy H1 ani istnienia cyklu — Test 3 wykazał brak mocy w paśmie w **0/192**
  kombinacjach, także tam, gdzie kontrast był najsilniejszy;
- kontrast epok **nie jest dowodem okresowości**;
- T = 35,1 jest **przyjęty, nie zmierzony** (D-005).

## 2. Krzywa P1 — M2(k) i p(k) z pasmem odniesienia S4

`A_COW_P`, T = 35,1, R3 (usuwanie k najwyższych lat epoki 2, faza liczona z numeru roku).
Pasmo S4 = usuwanie k **losowych** lat, 500 powtórzeń, osobny strumień losowy.

| k | n | M2 | p | S4 mean | S4 sd |
|---|---|---|---|---|---|
| 0 | 94 | 24,37 | 0,0190 | 24,37 | — |
| 1 | 93 | 23,82 | 0,0195 | 24,01 | 0,62 |
| 2 | 92 | 23,78 | 0,0170 | 23,72 | 0,97 |
| 3 | 91 | 23,03 | 0,0180 | 23,41 | 1,15 |
| 4 | 90 | 23,46 | 0,0150 | 23,11 | 1,35 |
| **5** | 89 | **24,91** | **0,0085** | 22,74 | 1,54 |
| 6 | 88 | 25,89 | 0,0075 | 22,57 | 1,56 |
| 7 | 87 | 27,32 | 0,0035 | 22,16 | 1,69 |
| 8 | 86 | 25,51 | 0,0055 | 21,77 | 1,90 |
| 9 | 85 | 27,66 | 0,0025 | 21,55 | 1,83 |
| 10 | 84 | 30,23 | 0,0020 | 21,05 | 2,11 |

**Interpretacja.** Usuwanie *najwyższych* lat trzyma M2 na poziomie 23–30 i obniża p,
podczas gdy usuwanie *losowych* lat systematycznie obniża M2 (24,4 → 21,1). Znaczy to,
że najwyższe lata **nie są** nośnikiem kontrastu — gdyby były, ich usunięcie zbijałoby
M2 mocniej niż losowe. Jest odwrotnie: kontrast leży w **rozkładzie**, nie w ogonie.

## 3. Lista k najwyższych lat epoki 2 (obie serie, obie listy)

R3 usuwa najwyższe lata serii **po detrendingu** (na niej liczone jest M2). Podajemy też
listę **surową** (opis historyczny, D-010). Listy się różnią, bo `A_COW_P` ma **dodatni
trend** (rozpad systemu kolonialnego → więcej stron), więc detrending globalny ściąga
późne szczyty mocniej niż wczesne — 1970/1971/1973 spadają w rankingu, a 1919/1920 rosną.

**`A_COW_P`, 5 najwyższych epoki 2:**
- po detrendingu (usuwane przez R3): 1991 (12,95), 1918 (12,89), 1941 (12,81), 1919 (11,94), 1920 (11,90)
- surowe (D-010): 1991 (25,9), 1941 (23,4), 1970 (23,4), 1971 (23,0), 1918 (22,4)

**`A_COW_W`, 5 najwyższych epoki 2:**
- po detrendingu: 1920 (7,60), 1992 (6,24), 1991 (5,85), 1919 (4,61), 1978 (4,36)
- surowe: 1920 (13,5), 1992 (13,3), 1991 (12,9), 1978 (11,2), 1987 (11,1)

Maksimum serii uczestniczej to **1991** (koalicja Zatoki Perskiej), nie wojna światowa.

## 4. Warianty potwierdzające

| ID | wariant | seria | M2 (k=0 / k=5) | p | wniosek |
|---|---|---|---|---|---|
| **P1** | R3 | `A_COW_P` | 24,37 / **24,91** | **0,0085** (k=5) | **ORZEKA — pozytywny** |
| S1 | R2 winsoryzacja 95. pct | `A_COW_P` | 22,20 | 0,033 | robustny bez luk |
| S1 | R2 winsoryzacja 90. pct | `A_COW_P` | 22,96 | 0,027 | robustny bez luk |
| S2 | R3, T = 32 | `A_COW_P` | 27,79 / 27,31 | 0,009 (k=0) | kontrast najsilniejszy przy T = 32 |
| S2 | R3, T = 40 | `A_COW_P` | 10,03 | 0,202 | **kontrola negatywna** — brak kontrastu, zgodnie z Testem 3 |

Winsoryzacja (ograniczenie skrajnych bez usuwania) daje kontrast istotny przy obu
progach. Wariant T = 40 zachowuje się jak zaprojektowana kontrola negatywna
(nieistotny na każdym k) — cokolwiek jest w danych, siedzi w paśmie krótszym niż 35 lat,
spójnie z Testem 3 (kontrast przy T = 32, brak przy T = 40).

## 5. P2 — wyłączenie lat wojen światowych (rozbrojenie zarzutu, D-010)

Usunięcie 12 lat (1914–1918, 1939–1945) z epoki 2: **M2 = 14,65, p = 0,096**.

Zarzut z D-002 („kontrast to artefakt dwóch wojen światowych") był **nietrafny** i został
wycofany (D-010): maksimum serii uczestniczej wypada na 1991, a nie na wojnę światową,
i kontrast przeżywa usuwanie najwyższych lat (P1). Wynik P2 wymaga jednak **uczciwego
zapisania w obie strony**: po wyłączeniu bloku wojennego kontrast **nie znika** (M2
pozostaje dodatni, tego samego rzędu, 14,65), ale jego istotność **spada do p = 0,096**.
Znaczy to, że lata wojenne *współtworzą* kontrast — ale nie *dominują* go, bo (a) usuwanie
5–10 najwyższych lat (w tym części lat wojennych) go nie znosi, lecz umacnia (P1), oraz
(b) P2 usuwa 12 konkretnych lat kalendarzowych, w tym cztery lata I wojny i lata II wojny,
które nie są najwyższe — czyli tnie próbę mocniej i w innym miejscu niż R3. Orzeka
wyłącznie P1; P2 jest wariantem publicznym, nie rozstrzygającym.

## 6. S3 — porównanie z serią wojno-poziomową `A_COW_W`

Na poziomie wojny kontrastu **nie ma**: R3 daje M2 ujemne na każdym k (−2,5 przy k=0,
p = 0,58), R1 M2 = 3,17 (p = 0,38), winsoryzacja M2 ujemne. Potwierdza to wynik Testu 3:
efekt jest **własnością serii uczestniczej**, nie wojno-poziomowej — te serie mierzą różne
wielkości (D-001). Kontrast dotyczy **zaangażowania stron**, nie liczby wojen.

## 7. S5 — kontrola detrendingu wewnątrz epoki (obok, poza §6)

Pytanie z przeglądu: czy kontrast `A_COW_P` nie jest artefaktem trendu wewnątrz epoki 2
(epoch-folding nie jest odporny na trend — zakaz nr 4). Odpowiedź liczbowa:

| seria | detrending globalny (P1/S3) | detrending w epoce (S5) |
|---|---|---|
| `A_COW_P` | M2 = 24,37 (k=0), p = 0,019 | M2 = 23,04 (k=0), p = 0,028 — **robustny** |
| `A_COW_W` | M2 = −2,54 (k=0) | M2 = +3,73 (k=0) → znak **odwraca się** |

Dla serii pierwszorzędnej detrending wewnątrz epoki zmienia M2 o < 6% i nie rusza
istotności (23,0 wobec 24,4) — **kontrast nie jest artefaktem trendu**; nachylenie
resztowe epoki 2 w `A_COW_P` jest znikome (−0,0077/rok). Dla `A_COW_W` znak kontrastu
**zależy od zakresu detrendingu** (globalny −2,5, w epoce +3,7) — bezpośrednia ilustracja
D-004 (+0,0404/rok, χ² rośnie o 43% przy detrendingu w oknie). To wzmacnia wybór z §2:
P1 używa detrendingu globalnego, niezmiennego.

**Uwaga metodyczna (świadomy wybór).** Baza modelu zerowego AR(3) jest we wszystkich
wariantach dopasowywana do serii detrendowanej **globalnie** (stacjonarnej), także w S5 —
AR(3) na serii z trendem byłby źle uwarunkowany, a obserwacja i surogat i tak przechodzą
tę samą ścieżkę detrendingu epokowego. Zatwierdzone w przeglądzie.

## 8. Reguła §6, liczba wariantów, granice

**Oba warunki §6 spełnione** dla P1: M2 > 0 i p < 0,05 przy k = 5 (M2 = 24,91, p = 0,0085)
**oraz** spadek M2 (k=0→k=5) w paśmie S4 (−0,54 wobec 1,63 ± 3,07). Twierdzenie
**„kontrast epok jest własnością rozkładu, nie kilku lat"** jest **wsparte**.

Wykonano P1, P2, S1 (×2 progi), S2 (×2 okresy), S3 (R1/R2/R3), S4 (pasmo), S5 (2 serie) —
**orzeka wyłącznie P1**; pozostałe są potwierdzające lub opisowe.

Granice (§7, §B2): wynik dotyczy **wyłącznie H2**. Kontrast epok nie jest dowodem cyklu
(Test 3: 0/192 mocy w paśmie). T = 35,1 przyjęte (D-005). Epoka 2 ma 94 lata (~2,7 cyklu) —
test odporności nie naprawia ograniczenia długości szeregu. Serie `A_COW_P` i `A_COW_W`
mierzą różne wielkości (korelacja 0,60); wynik dla P nie przenosi się na W.

**Co ten wynik znaczy dla rozdziału.** Twierdzenie z żywym poparciem brzmi: *po 1914
konflikty angażują naraz więcej stron, w sposób wykazujący większą koncentrację fazową
w paśmie ~28–36 lat niż wcześniej* — i ta różnica jest własnością rozkładu, nie kilku lat
skrajnych. To jest H2, nie H1: nie „liczba wojen pulsuje w rytmie 35 lat" (obalone
w Teście 3), lecz strukturalna różnica w umiędzynarodowieniu konfliktów między epokami.

## 9. Produkty

`test4_robustness.py` + bliźniaczy `.md`; `test4_results.csv` (jeden wiersz na uruchomienie:
id, seria, wariant, T, k, n, M2, p, pasmo S4; nagłówek `#` z wersją, ziarnem, B, sha,
werdyktem P1, obiema listami lat); `test4_curves.pdf` (panel 1: M2(k)+p(k) dla P1 z pasmem
S4; panel 2: `A_COW_W`; panel 3: epoka 2 z zaznaczonymi najwyższymi latami; panel 4:
winsoryzacja); `TEST4_REPORT.md`. Bieg reprodukowalny: ziarno 20260814, B = 2000,
surogaty i S4 na osobnych strumieniach losowych.
