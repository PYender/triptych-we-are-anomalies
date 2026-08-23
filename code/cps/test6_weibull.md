# TEST 6 — Etap B: kod estymacji Weibulla (rodzina 9)

**Realizuje:** `TASK_6B_BRIEF.md` (D-015) na zbiorach z Kroku 1b (D-012–D-014).
**Kod:** `test6_weibull.py` · **Status:** kod do przeglądu, **NIEURUCHOMIONY na danych
rzeczywistych** — jedyne biegi w tym dokumencie są na danych **syntetycznych** (testy
poprawności, brief §3).

---

## 1. Cztery dopasowania (brief §1) — nie więcej

| id | funkcja | zbiór (plik) | rola |
|---|---|---|---|
| **P1** | `fit_pooled` | `test6_intervals.csv` (18 diad, ekspozycja) | **ORZEKA** dla H9 |
| F1 | `fit_frailty` | `test6_intervals.csv` — **wyłącznie** ten zbiór | drugorzędny (D-015 B) |
| S-A | `fit_pooled` | `test6_intervals_sensitivity_SA.csv` (epizodowy×kalendarz) | wrażliwość na D-014 |
| S-B | `fit_pooled` | `test6_intervals_sensitivity_SB.csv` (próg surowy×ekspozycja) | wrażliwość na D-013 |

Kruchość (F1) liczona tylko na zbiorze głównym — brief §1 zabrania krzyżowania modelu
z wariantami wrażliwości. Kod nie ma parametru, który by na to pozwalał (`fit_frailty`
przyjmuje jeden `t,event,diad` naraz, wywoływane jawnie tylko dla P1 w Kroku 3).

## 2. Wiarygodność pulowana (P1, S-A, S-B)

```
h(t) = (k/λ)·(t/λ)^(k−1)      H(t) = (t/λ)^k
pełna:       log f(t) = log(k/λ) + (k−1)·log(t/λ) − H(t)
cenzurowana: log S(t) = −H(t)
```

Optymalizacja po `(log k, log λ)` (Nelder-Mead), żeby `k,λ>0` bez ograniczeń w optymalizatorze.
`log(t/λ)` liczone tylko dla obserwacji **pełnych** (`t_safe = t gdzie t>0, inaczej 1.0`) —
cenzurowana obserwacja o ekspozycji zero (Austria-Hungary–Italy, D-014 §3) nigdy nie wchodzi
w tę gałąź; wnosi wyłącznie `−H(0) = 0` do sumy, zgodnie ze specyfikacją brief §2.

## 3. Wiarygodność z kruchością gamma (F1, D-015 B)

Wzór z brief §3, kruchość gamma o średniej 1 i wariancji θ, dzielona w obrębie diady:

```
log L_i = Σ_{j:pełne} log h(t_ij) + D_i·log θ + lgamma(1/θ+D_i) − lgamma(1/θ)
        − (1/θ+D_i)·log(1+θ·H_i)
```

`H_i` sumuje hazard skumulowany po **wszystkich** obserwacjach diady *i* (pełnych i
cenzurowanej), `D_i` liczy tylko pełne. Optymalizacja po `(log k, log λ, log θ)`.

**Poprawka numeryczna wykryta podczas testowania (nie w danych, w kodzie):** przy
przeszukiwaniu przez optymalizator `log θ` może zejść poniżej ok. −745, gdzie
`exp(log θ)` dopełnia się do dokładnego zera w float64 — dalej `1/θ→inf`, `log θ→−inf`,
`gammaln(inf)` daje `nan`. Zastosowano podłogę `θ = max(exp(log θ), 1e-10)`; nie zmienia to
optimum (granica θ→0 jest i tak testowana osobno, §5.1 niżej), tylko chroni minimalizator
przed `nan` w trakcie przeszukiwania. Zweryfikowano ponownie z `warnings.simplefilter("error")`
— brak ostrzeżeń po poprawce.

## 4. Przedziały ufności (brief §4) — obowiązkowe w obu postaciach

- **Profil wiarygodności dla k** (`profile_ci_k`): siatka `log k`, przy każdym punkcie
  optymalizacja pozostałych parametrów, granice na progu `χ²₁(0,95)=3,841` (test ilorazu
  wiarygodności, dwustronny z konstrukcji — nie ma założenia o kierunku).
- **Bootstrap na poziomie diady** (`bootstrap_ci_k_pooled`, `bootstrap_ci_k_frailty`):
  losowanie ze zwracaniem **całych diad**, nie odstępów. Dla F1 każda wylosowana kopia
  diady dostaje **własną etykietę grupy** (`{diada}__{numer_powtórzenia}`) — bez tego
  powtórzone losowanie tej samej diady scaliłoby jej obserwacje w jedną większą grupę
  z jednym wspólnym losowaniem kruchości, co zaniżyłoby wariancję bootstrapu.

Obie metody uruchomione (smoke test na danych syntetycznych, nie w tym pliku jako oficjalny
wynik) i działają bez błędów po poprawce z §3.

## 5. Testy poprawności (brief §3, obowiązkowe przed biegiem na danych rzeczywistych)

### 5.1 Granica θ→0

Dane syntetyczne (k=1,3, λ=20, θ=0, struktura 18/45/18 z `test6_intervals.csv`), θ ustawione
na `1e-6` w modelu z kruchością:

| wielkość | wartość |
|---|---|
| log-wiarygodność pulowana | −179,433186 |
| log-wiarygodność z kruchością (θ=1e-6) | −179,433188 |
| różnica bezwzględna | **2,8·10⁻⁶** |

Zgodność do ~6 miejsc po przecinku, jak wymaga brief §3.1. **Test zaliczony.**

### 5.2 Odzysk parametrów — trzy zestawy, struktura identyczna z Etapem A (18 grup, 45
zdarzeń pełnych, 18 cenzurowanych; rozkład wielkości grup: 1×4, 7×3, 10×2)

| zestaw | k prawdziwe | λ prawdziwe | θ prawdziwe | k̂ pulowany | k̂ kruchość | θ̂ kruchość |
|---|---|---|---|---|---|---|
| k=1, θ=0 (bez pamięci, bez kruchości) | 1,0 | 20,0 | 0,0 | 1,163 | 1,163 | **1,1·10⁻⁷** |
| k=1,5, θ=0,3 (rosnący hazard, kruchość umiarkowana) | 1,5 | 15,0 | 0,3 | 1,329 | 1,430 | 0,165 |
| k=0,7, θ=0,6 (malejący hazard/grupowanie, kruchość silna) | 0,7 | 25,0 | 0,6 | 0,505 | 0,641 | 0,391 |

**Odczyt, zgodny z ostrzeżeniem brief §3 („spodziewaj się płaskiej powierzchni"):** to
pojedyncze losowanie na zestaw, nie badanie kalibracji — przy 45 zdarzeniach w 18 grupach
szum jest duży. Mimo to widać systematyczny, sensowny wzorzec: (a) przy braku kruchości
(zestaw 1) model z kruchością poprawnie **odzyskuje θ≈0** zamiast fałszywie wykrywać
heterogeniczność; (b) przy silnej kruchości (zestaw 3) model pulowany **systematycznie myli
się mocniej** niż model z kruchością (k̂=0,505 wobec prawdziwego 0,7, błąd 28%, kontra
k̂=0,641, błąd 8%) — dokładnie ten mechanizm, dla którego F1 istnieje jako wariant
drugorzędny. Żadna z trzech estymacji nie jest „dokładna" i nie ma być — to demonstracja, że
estymator działa w prawidłowym reżimie, nie kalibracja pokrycia przedziału ufności (do tego
służy bootstrap na danych rzeczywistych w Kroku 3, którego wynik pokaże realną szerokość
niezależnie od tego, co powiedzą dane).

## 6. Założenia D-015 A — w kodzie i tutaj

1. **Zegar zatrzymany, nie wyzerowany.** `dlugosc_odstepu` w plikach wejściowych to już suma
   lat ekspozycji (policzona w Etapie A, D-014); model traktuje ją jako jeden ciągły czas
   oczekiwania. Kod nie odróżnia obserwacji z przerwaną ekspozycją od innych — to jest
   właśnie treść założenia, nie coś do zaimplementowania osobno.
2. **Dyskretyzacja.** Odstępy w pełnych latach (liczby całkowite), model ciągły. Nie
   koryguję (bez losowego rozmycia wewnątrz roku) — zgodnie z brief §5.2, przyjęte jako
   ograniczenie do odnotowania w raporcie Etapu C, nie do naprawienia w kodzie.

## 7. Czego ten kod NIE robi (brief §6)

- Nie dodaje piątego wariantu.
- Nie wybiera między P1 a F1 — obie funkcje istnieją, wybór interpretacji różnicy jest
  regułą deklarowaną w D-015 (przed biegiem), **ale tekst czterech przypadków czytania tej
  różnicy nie został przekazany w `TASK_6B_BRIEF.md`** (patrz D-015, „zastrzeżenie do
  uzupełnienia") — potrzebny przed Krokiem 3, nie przed napisaniem tego kodu.
- Nie uruchamia niczego na `test6_intervals*.csv` poza odczytem **samej struktury grup**
  (`group_sizes_from`) do testu odzysku parametrów — nigdy odczytem wartości `t`/`event`.
  `main()` blokuje jawnie próbę biegu na danych rzeczywistych (`--run-real` podnosi
  `SystemExit` z odwołaniem do brief §6/§8).

## 8. STOP (Krok 2, `TASK_6B_BRIEF.md` §8)

Kod i testy poprawności gotowe do przeglądu. Po akceptacji — Krok 3: bieg P1/F1/S-A/S-B na
`test6_intervals*.csv`, wyniki commitowane przed raportem, raport podaje przedziały (profil +
bootstrap diadowy), nie same wartości punktowe, i zestawia P1 z F1, S-A, S-B oraz z Testem 7
(gdy dostępny), z kierunkiem obciążenia progu epizodowego nazwanym jako nieustalony (D-017)
przy S-B.
