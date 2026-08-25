# TEST 6 — Krok B: modele zerowe N1/N2 (D-023/D-024)

**Realizuje:** `TEST6_PROTOCOL.md` §6 (dosłownie, cytowany paragraf poniżej) · **Kod:**
`test6_null.py` · **Status:** do przeglądu, **NIEURUCHOMIONY** (`--run-real` zablokowane).

---

## 0. Cytat protokołu (reguła dodana w D-024 — briefy cytują, nie streszczają)

> **N1 — parametryczny.** Proces Poissona o intensywności estymowanej z danych, osobno dla
> każdej diady, z tą samą strukturą cenzurowania i tą samą liczbą zdarzeń.
> B = 2000 symulacji, ziarno 20260822.
>
> **N2 — permutacyjny.** Odstępy przetasowane między diadami z zachowaniem liczebności.
> Niszczy strukturę wewnątrz diady, zachowuje rozkład brzegowy puli.
>
> Wynik zgodny w obu modelach jest znacznie mocniejszy niż w którymkolwiek osobno.
>
> `p = (1 + #{|k_sur − 1| ≥ |k_obs − 1|}) / (B + 1)`

## 1. N1 — implementacja

Dla diady o zdarzeniach pełnych `t_1..t_n` i jednej obserwacji cenzurowanej `c`:
`λ̂ = n / (Σt_i + c)` (standardowy MLE wykładniczy z cenzurowaniem, per diada). Surogat:
`n` świeżych rysowań `Exponential(1/λ̂)` jako odstępy pełne; **`c` pozostaje niezmienione**
— to jest „ta sama struktura cenzurowania": okno administracyjne (kiedy zbiór się kończy)
jest faktem obserwowanym, nie częścią procesu generującego dane pod H0. Liczba zdarzeń
(`n` pełnych + 1 cenzurowany) identyczna z danymi obserwowanymi z konstrukcji.

**Właściwość odkryta przy sprawdzaniu (nie usterka, do udokumentowania przed biegiem):**
średnie k̂ surogatów N1 na strukturze zbioru głównego (18 diad) wynosi **~0,92, nie 1,0**
(sprawdzone na 200 powtórzeniach, ziarno testowe różne od `20260822`). Przyczyna: diady
mają bardzo różne λ̂ (od kilku do kilkudziesięciu lat oczekiwania), a **pulowanie danych
z wielu wykładniczych o różnych szybkościach, dopasowane jednym wspólnym k, daje pozorny
hazard malejący** — ten sam mechanizm, dla którego D-015 wprowadziło model kruchości F1.
N1 poprawnie **dziedziczy** tę heterogeniczność (bo λ̂ liczone osobno per diada), więc jest
nullem **skalibrowanym na rzeczywistą strukturę międzydiadyczną**, nie na naiwny wspólny
proces Poissona — to jest właściwość zamierzona, nie błąd, ale musi być nazwana w raporcie:
`p` z §6 testuje, czy k̂_obs jest bardziej ekstremalny niż typowe k̂_sur (~0,92), **nie**
czy różni się od dokładnie 1,0.

## 2. N2 — implementacja

Pula wszystkich odstępów pełnych (n=45) i osobna pula wszystkich cenzurowanych (n=18)
tasowane niezależnie (`rng.permutation`), potem rozdzielane z powrotem do diad tak, by
każda diada zachowała swoją oryginalną liczbę odstępów pełnych i dokładnie jeden
cenzurowany. **Sprawdzone:** suma puli pełnych, suma puli cenzurowanych i liczebności
(45/18) identyczne przed i po permutacji — mechanika weryfikowalna wprost, nie tylko
przez wynik końcowy.

## 3. Statystyka i wartość p

`k̂` liczone `test6_weibull.fit_pooled` — ten sam, naprawiony estymator (pięć poprawek +
D-022), identycznie na danych obserwowanych i na każdym surogacie. `p` wg wzoru §6,
dwustronna z konstrukcji (`|k̂−1|`, nie kierunkowa).

## 4. Ziarno — celowo inne niż w `test6_weibull.py`

`SEED_PROTOCOL = 20260822`, zgodnie z §6 protokołu — **inne** niż `RNG_SEED = 20260823`
używane w `test6_weibull.py` do testów poprawności syntetycznych. Rozdzielenie jest
celowe: ziarno protokołu jest zamrożone od 22 sierpnia i nie wolno go zmieniać; ziarno
testów poprawności jest wewnętrzną sprawą implementacji.

## 5. Czego ten kod NIE robi

Nie liczy `k_obs` żadnego wariantu poza odczytem struktury do sprawdzeń mechanicznych
(sumy, liczebności — nie sam wynik testu). Nie uruchamia B=2000 na `test6_intervals.csv`.
`main()` blokuje `--run-real` z `SystemExit`, analogicznie do blokady w `test6_weibull.py`
sprzed D-022.

Nie implementuje jeszcze S1/S3/S4/S7/S8 (wymagają osobnych zbiorów danych — D-024 §S1/S7/S8
rozstrzyga *zasady*, budowa tych zbiorów to osobny krok). `run_n1`/`run_n2` przyjmują
dowolną ścieżkę do pliku o formacie `test6_intervals*.csv` (kolumny `diada`,
`dlugosc_odstepu`, `cenzurowany`), więc są gotowe do użycia na tych zbiorach, gdy powstaną.

## 6. Sprawdzenia mechaniczne wykonane (nie jest to bieg B=2000 na realnym k_obs)

- `load_grouped`/`flatten`: 18 diad, 45 pełnych, 18 cenzurowanych — zgodne z metadanymi pliku.
- N1, 200 powtórzeń (ziarno testowe): średnie k̂_sur ≈ 0,92, opisane w §1.
- N2: suma i liczebność obu pul zachowane dokładnie po permutacji (sprawdzone bezpośrednio,
  nie przez wynik statystyki).

## 7. STOP

Kod gotowy do przeglądu. Po akceptacji: bieg B=2000 na `test6_intervals.csv` (P1=N1, P2=N2),
sprawdzenie reguły §8 w trzech warunkach naraz, raport Kroku C z ujawnieniem wymaganym
przez D-023 (bieg wykonywany ze znajomością wyniku z analizy niezgodnej,
`TEST6_REPORT.md`) i porównaniem obu metod jako samodzielnym wynikiem.
