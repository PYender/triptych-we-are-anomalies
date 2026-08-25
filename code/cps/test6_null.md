# TEST 6 — Krok B: modele zerowe N1/N2 (D-023/D-024/D-026)

**Realizuje:** `TEST6_PROTOCOL.md` §6 (dosłownie, cytowany paragraf poniżej) · **Kod:**
`test6_null.py` · **Status:** przegląd wykonany, wada §8 wykryta i rozstrzygnięta (D-026,
przed jakimkolwiek biegiem na danych rzeczywistych) — **NIEURUCHOMIONY** (`--run-real`
zablokowane, czeka na jawną autoryzację Kroku C).

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
(sprawdzone na 200 powtórzeniach, ziarno testowe różne od `20260822`). `p` z §6 testuje,
czy k̂_obs jest bardziej ekstremalny niż typowe k̂_sur (~0,92), **nie** czy różni się od
dokładnie 1,0.

**Rozbicie na dwa składniki (zlecone w przeglądzie D-026, wykonane).** Odchylenie od 1,0 ma
DWA źródła, działające w przeciwne strony — raport ma je podać osobno, nie jako jedną liczbę:

(a) **Mieszanka wykładniczych o różnych λ̂, dopasowana jednym wspólnym k, ciągnie k̂ w dół** —
diady mają bardzo różne λ̂ (od kilku do kilkudziesięciu lat oczekiwania), pulowanie takiej
heterogeniczności pod jednym k daje pozorny hazard malejący — ten sam mechanizm, dla którego
D-015 wprowadziło model kruchości F1. N1 poprawnie **dziedziczy** tę heterogeniczność (λ̂
liczone osobno per diada), więc jest nullem skalibrowanym na rzeczywistą strukturę
międzydiadyczną, nie na naiwny wspólny proces Poissona.

(b) **Sam estymator `fit_pooled` ma obciążenie w górę przy n=45 zdarzeniach** — zmierzone
istniejącym testem poprawności `test_censoring_bias` na realnej strukturze (18 grup,
`group_sizes_from('test6_intervals.csv')`), pod jednorodną prawdą k=1 (jedno wspólne λ dla
wszystkich diad, więc składnik (a) jest tu z konstrukcji zerowy — test izoluje czysto
obciążenie małej próby): 2000 powtórzeń, **średnie k̂ = 1,0249 (mediana 1,0153), obciążenie
≈ +2,5%**. Rząd wielkości zgodny ze zgłoszonymi w drugim przeglądzie ~3%.

Oba składniki mają trafić do raportu Kroku C osobno: (a) ciągnie w dół, (b) ciągnie w górę —
przypisanie całego odchylenia N1 (~0,92) jednemu mechanizmowi byłoby mylące.

**Czy surogaty N1 generują historie dłuższe niż diada mogła realnie mieć (zlecone w D-026,
wykonane).** `λ̂ = n/T` (T = realna ekspozycja całkowita diady, włącznie z `c`), więc
`E[Σt_sim] = n·(1/λ̂) = T`, a surogat dokłada do tego niezmienione `c` — stąd
`E[Σt_sim+c] = T+c > T` **systematycznie**, dla każdej diady z `c>0`. Sprawdzone bezpośrednio
(`n1_window_exceedance`, B=2000 na realnej strukturze 18 diad, ziarno eksploracyjne):
**75,4% surogatowych replik ma sumę przekraczającą realne okno diady** (zakres per-diada:
41%–98%, rośnie z udziałem `c/T`). **To nie jest zjawisko marginalne.** Jest to dodatkowe
źródło wariancji rozkładu zerowego N1 — surogaty generują historie dłuższe niż diada mogła
realnie mieć — co czyni test N1 **konserwatywnym** (trudniej odrzucić H0, niż gdyby surogaty
były ograniczone do realnego okna). Ma to być nazwane wprost w raporcie Kroku C.

## 2. N2 — implementacja, ZDEGENEROWANA względem k̂ pulowanego (D-026)

Pula wszystkich odstępów pełnych (n=45) i osobna pula wszystkich cenzurowanych (n=18)
tasowane niezależnie (`rng.permutation`), potem rozdzielane z powrotem do diad tak, by
każda diada zachowała swoją oryginalną liczbę odstępów pełnych i dokładnie jeden
cenzurowany. **Sprawdzone:** suma puli pełnych, suma puli cenzurowanych i liczebności
(45/18) identyczne przed i po permutacji — mechanika weryfikowalna wprost, nie tylko
przez wynik końcowy. Kod odtwarza §6 dosłownie i poprawnie.

**Ale (D-026, wykryte w przeglądzie, potwierdzone niezależnie przez Code): ta implementacja
jest algebraicznie zdegenerowana względem statystyki pierwszorzędnej.**
`negloglik_pooled(params, t, event)` sumuje po obserwacjach bez odniesienia do etykiety
diady — k̂ zależy wyłącznie od multizbioru par `(t, event)`. Permutacja N2 przenosi wartości
MIĘDZY diadami, ale nie zmienia tego multizbioru — k̂_sur ≡ k̂_obs dla KAŻDEJ permutacji, z
konstrukcji. Zweryfikowane na danych syntetycznych (5 permutacji): różnice rzędu 1e-8
(tolerancja optymalizatora, nie prawdziwa różnica).

**Poprawka do pierwotnego zgłoszenia (Code, po dodatkowej weryfikacji na danych realnych):**
teoretycznie `p_N2` powinno wynosić tożsamościowo 1,000 — ale **w praktyce, uruchamiając
literalnie kod i wzór §6, tak nie jest.** Na `test6_intervals.csv`, B=2000: `k_sur_sd ≈
7,7·10⁻⁹` (potwierdza degenerację — to szum optymalizatora, nie sygnał), ale wynikowe
`p` = **0,253** (ziarno protokołu `20260822`) i **0,266** (inne ziarno) — nie 1,000, nie 0,5,
tylko pozornie sensowna, w rzeczywistości przypadkowa liczba zależna od ziarna (deterministyczna
przy ustalonym ziarnie, powtórzone uruchomienie daje identyczny wynik — ale bez treści).
Przyczyna: porównanie `|k_sur−1| >= |k_obs−1|` z §6 rozstrzyga o remisie na poziomie szumu
numerycznego (permutacja zmienia kolejność sumowania tych samych wartości w
`np.sum(ll)`, co przy nieasocjatywności arytmetyki zmiennoprzecinkowej przesuwa optimum
Nelder-Mead o ~1e-8 w tę lub inną stronę) — **to JEST degeneracja, tylko widoczna na innym
poziomie precyzji niż idealna matematyczna tożsamość.** Ani 1,000, ani ta pozorna wartość
(0,253/0,266) nie są prawdziwym wynikiem; obie opisują to samo zjawisko. Reguła §8 (wymaga
P2<0,10) jest przez to **niespełnialna w sposób informacyjny w obecnym brzmieniu protokołu**
— cokolwiek P2 pokaże liczbowo, nie niesie treści o H6.1. Szczegóły, rozstrzygnięcie i
uzasadnienie w `CPS_DECISION_LOG.md` D-026 (zaktualizowane tą poprawką). `run_n2`/
`simulate_n2_once` **pozostają w kodzie** (nie usunięte — degeneracja ma być widoczna, nie
ukryta) i są oznaczone jako diagnostyka **poza regułą decyzyjną §8**, nie jako ścieżka do P2
wchodzącego do decyzji o H6.1.

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
- N1, 200 powtórzeń (ziarno testowe): średnie k̂_sur ≈ 0,92, opisane w §1, rozbite na dwa
  składniki (D-026).
- N2: suma i liczebność obu pul zachowane dokładnie po permutacji (sprawdzone bezpośrednio,
  nie przez wynik statystyki) — **ale degeneracja względem k̂ pulowanego wykryta niezależnie
  od tego sprawdzenia** (§2, D-026): zachowanie pul jest poprawne, problem jest o poziom
  wyżej (statystyka, nie mechanika permutacji).
- N1 przekroczenie realnego okna (`n1_window_exceedance`, D-026): 75,4% surogatowych replik
  przekracza realną ekspozycję diady, opisane w §1.

## 7. STOP

Kod gotowy do przeglądu — **przegląd wykonany, wykrył wadę protokołu (D-026), nie
implementacji.** Rozstrzygnięcie D-026: P1(N1) liczony i raportowany normalnie; P2(N2)
raportowany jako 1,000 z wyjaśnieniem tożsamości, poza regułą §8; reguła §8 raportowana jako
niespełnialna w obecnym brzmieniu; H6.1 pozostaje nierozstrzygnięta w ramach zamrożonego
protokołu. Dwie weryfikacje zlecone przed biegiem P1 (rozbicie obciążenia N1, przekroczenie
okna) wykonane, opisane w §1.

**Nadal NIEURUCHOMIONY na `test6_intervals.csv`** — D-026 odblokowuje dalszą pracę nad
diagnostyką i dokumentacją, nie sam bieg B=2000 na danych rzeczywistych. Krok C (rzeczywisty
bieg P1, raport z ujawnieniem wymaganym przez D-023 §5 i D-026, porównaniem z
`TEST6_REPORT.md`) czeka na jawną autoryzację przed `--run-real`.
