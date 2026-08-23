# TEST 5 — RAPORT: skan po okresach ze statystyką maksymalną

**Rodzina 1 rozszerzona** · **Realizuje:** `TEST5_PROTOCOL.md` v1.0 (D-011)
**Kod:** `test5_periodscan.py` (zatwierdzony w przeglądzie przed biegiem) · **Bieg:** 2026-08-22
**Wejście:** `cps_canonical_v2.csv` (sha256 `145aed00…`), kolumna `value`.
**Skan:** T ∈ [8, 60] lat, krok 0,5 — **105 punktów**. **Null:** AR(3), rząd z góry,
B = 2000, ziarno 20260815, **rozkład zerowy = rozkład maksimów po skanie** (§5).

Test pyta o istnienie **jakiegokolwiek** okresu w 8–60 lat; nie zakłada 32–40 ani 18 lat.

---

## 1. Wynik w jednym zdaniu

**Kryterium falsyfikacji §7 spełnione — wynik NEGATYWNY.** Test pierwszorzędny P1
(A_COW_W, moc w paśmie) daje **p = 0,0725 ≥ 0,05** wobec rozkładu maksimów; test
współpierwszorzędny P2 (χ²) daje **p = 0,6152 ≥ 0,10**. Twierdzenie *„w szeregu istnieje
jakikolwiek okres wyróżniający się ponad przypadek w zakresie 8–60 lat"* **nie jest
wsparte**.

Trzeci warunek §7 również zawodzi (i jest tu najbardziej pouczający): rozkład `Targmax`
surogatów jest **silnie skupiony na krótkich okresach** — 72,4% surogatów osiąga maksimum
w paśmie 8–12 lat, 59,3% dokładnie przy dolnej granicy T = 8. Maksimum danych wypada
**również przy T = 8**, czyli dokładnie tam, gdzie piętrzą się maksima samego szumu AR(3).
Pozycja maksimum w danych nie jest zatem informacją — jest tym, czego oczekujemy od
procesu bez składowej okresowej.

## 2. Tabela uruchomień (§6)

`Wmax` i `Targmax` po skanie; p wobec **rozkładu maksimów** surogatów. Orzeka wyłącznie P1.

| ID | seria | okno | stat. | Wmax | Targmax [lata] | null max p95 | **p** | rola |
|---|---|---|---|---|---|---|---|---|
| **P1** | A_COW_W | 1816–2007 | W1 | 0,5226 | 8,0 | 0,5446 | **0,0725** | ORZEKA |
| **P2** | A_COW_W | 1816–2007 | W2 | 43,62 | 59,5 | 66,38 | **0,6152** | potwierdza |
| S1 | A_COW_P | 1816–2007 | W1 | 0,2766 | 28,0 | 0,5610 | 0,9340 | H2 |
| S1 | A_COW_P | 1816–2007 | W2 | 58,44 | 53,0 | 62,11 | 0,0760 | H2 |
| S2 | A_COW_W | 1914–2007 | W1 | 0,4561 | 8,0 | 0,7280 | 0,6027 | epoka 2 |
| S2 | A_COW_W | 1914–2007 | W2 | 29,80 | 35,5 | 51,72 | 0,9750 | epoka 2 |
| S3 | A_COW_P | 1914–2007 | W1 | 0,3008 | 12,5 | 0,6685 | 0,9035 | epoka 2, H2 |
| S3 | A_COW_P | 1914–2007 | W2 | 36,30 | 51,0 | 50,88 | 0,6522 | epoka 2, H2 |
| S4 | B_UCDP | 1946–2024 | W1 | 0,2839 | 49,0 | 0,5493 | 0,6657 | replikacja |
| S4 | B_UCDP | 1946–2024 | W2 | 56,03 | 52,0 | 62,13 | 0,2069 | replikacja |
| S5 | A_COW_W | 1816–2007, MA(11) | W1 | 0,2581 | 51,0 | 0,5182 | 0,6742 | wpływ MA(11) |

Żadne uruchomienie **orzekające** nie osiąga p < 0,05. Jedyna wartość p < 0,10 w całej
tabeli to opisowe **S1/W2** (A_COW_P, χ², p = 0,076 przy T = 53) — nie orzeka i nie może
być tak czytana; przy statystyce maksymalnej i jednym opisowym wariancie z sześciu jedna
wartość ~0,08 jest oczekiwana. Pełne krzywe W(T) (105 punktów na wariant) są w
`test5_scan.csv`.

## 3. Rozkład `Targmax` surogatów (kontrola §5/§7)

Dla P1 (W1), rozkład okresu, przy którym surogaty osiągają maksimum:

| pasmo | udział surogatów |
|---|---|
| 8–12 lat | **72,4%** |
| 12–20 lat | 14,5% |
| 20–32 lat | 10,8% |
| 32–45 lat | 2,1% |
| 45–60 lat | 0,2% |

Mediana `Targmax` surogatów = 8,0 lat; 59,3% przy samej dolnej granicy. Rozkład jest
skrajnie niejednorodny. **Sprostowanie (przegląd niezależny, 2026-08-23):** poprzednia
wersja tego akapitu tłumaczyła skupienie tym, że „AR(3) ma najwięcej mocy przy krótkich
okresach" — to jest **odwrotność** rzeczywistego kształtu widma. AR(3) dopasowane do tej
serii ma φ₁ ≈ 0,67 (silnie dodatnie); to szum czerwony, którego moc **rośnie** z okresem
(zweryfikowane numerycznie: średnia PSD surogatów rośnie monotonicznie od T=8 do T=60).
**Prawdziwa przyczyna jest geometryczna, nie widmowa:** W1(T) to udział mocy w paśmie
o STAŁEJ szerokości okresowej T±4 lat wobec mianownika stałego (4–100 lat); szerokość tego
pasma **w częstotliwości** maleje jak ~1/T² wraz z T — przy T=8 pasmo ma szerokość
częstotliwościową ~0,167/rok, przy T=35 ~0,0066/rok, czyli **25-krotnie węziej**. Nawet
przy widmie rosnącym z okresem ten efekt geometryczny dominuje: zweryfikowano, że średnie
W1(T) surogatów **maleje** monotonicznie z T (0,343 przy T=8 → 0,038 przy T=60), mimo że
surowa moc PSD rośnie w tym samym zakresie. **Konsekwencja interpretacyjna (bez zmian):**
fakt, że maksimum danych też wypada przy T = 8, nie niesie informacji o okresowości — to
artefakt konstrukcji statystyki W1 (szerokość pasma zależna od T), nie własność danych ani
kształtu widma AR. Ten sam mechanizm jest powodem, dla którego korekta na statystykę
maksymalną jest konieczna (problem Daviesa): bez niej maksimum z szerokiego skanu
wyglądałoby na istotne.

## 4. Reguła decyzyjna §7 — wszystkie trzy warunki

- P1: p = 0,0725 ≥ 0,05 → **niespełniony**.
- P2: p = 0,6152 ≥ 0,10 → **niespełniony**.
- Rozkład `Targmax` surogatów **skupiony** w wąskim podzakresie (8–12 lat) zawierającym
  `Targmax` danych → warunek kontrolny **niespełniony**.

Wynik jest negatywny każdym z trzech kryteriów niezależnie.

**Uwaga o P1 i P2.** Obie statystyki policzono na **wspólnych realizacjach** surogatów
A_COW_W (jeden zestaw AR(3) na konfigurację). Są więc **skorelowane** — zgodność ich
wyniku negatywnego nie jest dwoma niezależnymi potwierdzeniami, lecz jednym; wspólne
realizacje czynią natomiast porównanie W1 z W2 uczciwszym niż osobne losowania. Kolejność
losowania (jeden strumień rng) jest zapisana w nagłówku `test5_results.csv` (`run_order`)
dla odtwarzalności.

## 5. Dlaczego ten wynik negatywny jest mocniejszy niż Testu 1 (§8)

Deklaracja mocy sprzed uruchomienia — komórki rozdzielcze i liczba cykli w szeregu
192-letnim:

| pasmo | cykli (n = 192) | komórek rozdzielczych |
|---|---|---|
| 8–12 lat | 24,0–16,0 | 8,00 |
| 12–20 lat | 16,0–9,6 | 6,40 |
| 20–32 lat | 9,6–6,0 | 3,60 |
| 32–45 lat *(pasmo Testów 1/3/4)* | 6,0–4,3 | 1,73 |
| 45–60 lat | 4,3–3,2 | 1,07 |

Testy 1, 3 i 4 działały w najgorszym miejscu zakresu (1,73 komórki, ~4–6 powtórzeń), gdzie
wynik negatywny można było tłumaczyć krótkością szeregu. Test 5 przeskanował także pasma
o **wysokiej mocy** (12–20 lat: 6,40 komórki, 10–16 powtórzeń) — i **tam również nie
znalazł sygnału**. Brak okresowości w paśmie krótkookresowym **nie da się usprawiedliwić
długością szeregu**, więc wynik negatywny Testu 5 jest **znacznie mocniejszy** niż Testu 1.

## 6. Porównanie z Testami 1 i 3

Testy 1 (p = 0,956) i 3 (0/192 specyfikacji) badały wyłącznie pasmo 32–40 lat i były
negatywne. Test 5 rozszerza to na cały zakres 8–60 lat z poprawną korektą na
wielokrotność i **potwierdza oraz wzmacnia** tamten wynik: nie tylko okres z Tryptyku,
lecz **żaden** okres w 8–60 lat nie wyróżnia się ponad proces autoregresyjny. Intuicja
autora o ~18 latach nie wyróżnia się w skanie (okolice 12–20 lat nie dają istotnego
maksimum; por. §3) — co jest oczekiwane, bo liczba 18 pochodziła z danych, które już
wykorzystaliśmy (D-011), i nie była hipotezą prerejestrowaną.

## 7. Granice wniosku (§9, §B2)

- **Test nie dotyczy cyklu o dryfującej fazie** (D-009) — skan zakłada stały okres w oknie;
  wariant z dryfem wymaga innych narzędzi i osobnego protokołu.
- **W1(T) nie jest porównywalne między okresami bez zastrzeżenia z §3:** szerokość pasma
  T±4 w częstotliwości maleje jak ~1/T², więc W1 ma wbudowaną tendencję do wyższych wartości
  przy krótkim T niezależnie od kształtu widma. Statystyka maksymalna i rozkład Targmax
  surogatów (§3) są na to odporne z konstrukcji — porównanie surogat-do-surogat jest uczciwe —
  ale odczyt W1(T) danych „na oko" (np. z Panelu 1) bez odniesienia do pasma 95. percentyla
  surogatów przy tym samym T byłby mylący.
- **Żaden okres nie jest tu „potwierdzony ani obalony" indywidualnie** — test orzeka
  o istnieniu *jakiejkolwiek* okresowości, nie o 18, 35 ani żadnej konkretnej liczbie.
- Gdyby wynik był pozytywny, wskazany okres byłby **kandydatem**, nie hipotezą potwierdzoną,
  wymagającym danych niezależnych (§9.2). Wynik jest negatywny, więc jedyna dopuszczalna
  kontynuacja (§7) — test wskazanego okresu na danych wstrzymanych — **nie ma zastosowania**:
  skan nie wskazał kandydata ponad przypadek. Nie wolno wyjmować pojedynczego okresu ze
  skanu do osobnego testu na tych samych danych.

## 8. Produkty

`test5_periodscan.py` + bliźniaczy `.md`; `test5_results.csv` (11 wierszy: id, seria, okno,
filtr, statystyka, n, Wmax, Targmax, percentyl 95 rozkładu maksimów, p, decyzja; nagłówek
`#` z wersją, ziarnem, B, siatką, `run_order`, sha); `test5_scan.csv` (pełne krzywe W(T),
105 wierszy na wariant, z per-T 95. percentylem surogatów); `test5_scan.pdf` (panel 1:
W1(T) dla P1 z pasmem 95. percentyla; panel 2: W2(T) dla P2; panel 3: histogram `Targmax`
surogatów z pozycją danych; panel 4: porównanie serii i okien); `TEST5_REPORT.md`.
Bieg reprodukowalny: ziarno 20260815, B = 2000, jeden strumień rng w kolejności `run_order`.
