# TEST 6 — Etap B: kod estymacji Weibulla (rodzina 9)

**Realizuje:** `TASK_6B_BRIEF.md` (D-015) na zbiorach z Kroku 1b (D-012–D-014).
**Kod:** `test6_weibull.py` · **Status:** pięć usterek naprawionych i zaakceptowanych
(`PRZEGLAD_test6_weibull.md`); warunek D-022 wykonany (§8–9) — **Krok 3 odblokowany**,
kod dotąd NIEURUCHOMIONY na `test6_intervals*.csv`. Estymator jest
wspólny z Testem 7 (`TASK_7B_BRIEF.md` §1) — poprawki obsługują oba tory naraz.

---

## 0. Odpowiedź na przegląd — pięć usterek, pięć poprawek

Przegląd (2026-08-24) potwierdził poprawność wzoru na wiarygodność brzegową i podłogi na θ,
ale znalazł pięć usterek, wszystkie w kodzie wspólnym. Poniżej każda, z poprawką i wynikiem
ponownego testu.

### 0.1 KRYTYCZNA — `_interp_crossing` zwracał brzeg siatki jako granicę przedziału

Gdy profil nie osiągał progu χ²₁ w zakresie siatki, funkcja milcząco zwracała `k_grid[0]`
albo `k_grid[-1]` — liczbę nieodróżnialną od prawdziwej granicy. **Poprawka:** zwraca teraz
`(nan, False)` gdy próg nie jest osiągnięty; `profile_ci_k` zwraca też flagi
`lo_bounded`/`hi_bounded`. **Test negatywny (odtworzenie przypadku z przeglądu):** siatka
zawężona do `(0,9k, 1,1k)` — maksymalne LR na siatce **0,762** (poniżej progu 3,841) →
`lo=nan, hi=nan, lo_bounded=False, hi_bounded=False`. Wcześniej zwróciłoby to fikcyjny
przedział `(1,0023, 1,2250)`.

### 0.2 POWAŻNA — brak wielu punktów startowych

`fit_pooled` i `fit_frailty` przyjmują teraz `x0_list` (domyślnie 2 punkty dla pulowanego,
4 dla kruchości — `DEFAULT_X0_POOLED`, `DEFAULT_X0_FRAILTY`), wybierają najwyższą
wiarygodność i zwracają `converged_same` (czy wszystkie starty zbiegły do wspólnego optimum
w tolerancji względnej 10⁻³) oraz `k_by_start`. **Wynik na zestawie odzysku k=1/θ=0:**
wszystkie 5 startów (4 domyślne + rozgrzany z dopasowania pulowanego) zbiega do
k̂∈[1,01944; 1,01958] — `converged_same=True`. Poprzednia usterka (domyślny start lądujący
na θ→0 fałszywie zgłaszany jako sukces, gdy inne starty dawały Δloglik=0,057 lepiej) nie
występuje już przy pełnym wielostarcie.

### 0.3 zgłaszane θ bez podłogi

`fit_frailty` zwracał `exp(logtheta)` surowe (np. `1,1·10⁻¹⁵`), podczas gdy wiarygodność
liczono z podłogą `1e-10` — liczby których model nigdy nie użył. **Poprawka:** zwracane θ ma
tę samą podłogę; dodano `theta_at_boundary` (True, gdy surowe θ ≤ 1e-10). Na zestawie k=1/θ=0:
`frailty_theta_hat=1e-10, theta_at_boundary=True` — czytelne jako „granica numeryczna”, nie
jako wynik.

### 0.4 cenzurowanie informacyjne w `simulate_dataset`

Poprzednia wersja: czas cenzurowania = ułamek (0,05–0,95) świeżo wylosowanego czasu zdarzenia
tej samej grupy — czyli **zależny od T**, mimo że w danych rzeczywistych cenzurowanie jest
administracyjne (domknięcie okna w 2007, niezależne od tego, jak długo para by czekała).
Przegląd zmierzył obciążenie: średnie k̂ na 400 powtórzeniach 1,084 zamiast 1,029 (+5,5 pkt
proc., w stronę k>1, czyli w stronę hipotezy).

**Poprawka:** czas cenzurowania `C ~ Exp(λ)`, losowany niezależnie od kruchości `u` i od
zdarzeń grupy. **Ponowny pomiar, ten sam protokół co w przeglądzie (400 powtórzeń, k=1,
θ=0, statystyka pulowana):**

| schemat cenzurowania | średnie k̂ | mediana | odchylenie | obciążenie |
|---|---|---|---|---|
| `T_true·U` (poprzedni, błędny) | 1,084 (przegląd) | 1,079 | 0,126 | +8,4% |
| `C~Exp(λ)` administracyjne (poprawiony) | **1,0301** | 1,0177 | 0,1249 | **+3,0%** |

Zgodne co do rzędu wielkości z własnym pomiarem przeglądu dla schematu administracyjnego
(1,0293) — różnica trzeciego miejsca po przecinku wynika z innego ziarna/kolejności losowań.

### 0.5 profil wiarygodności nie zbiegał dla modelu kruchości

`profile_ci_k` startował od lewej krawędzi siatki i przesuwał punkt startowy w prawo —
dla modelu kruchości wewnętrzna optymalizacja utykała w gorszym optimum niż `fit_frailty`,
zaniżając profil (LR w k̂ = 0,50 zamiast ~0 w przykładzie z przeglądu).

**Poprawka:** profil zakotwiczony w k̂ — liczony NAJPIERW w punkcie k̂ (z kilku startów
wokół `rest_hat`), potem rozszerzany na zewnątrz w obie strony z rozgrzanym startem
(poprzedni punkt siatki + `rest_hat` jako alternatywa). Zwraca `anchor_lr` i `anchor_ok`
(próg 10⁻²). **Test na syntetycznym zestawie (k=1,4, λ=18, θ=0,3):**

| model | LR w k̂ (powinno ≈0) | anchor_ok | przedział 95% |
|---|---|---|---|
| pulowany | 0,0 | True | (1,0068; 1,5968) |
| kruchość | −0,00036 | True | (1,0067; 1,5968) |

Oba profile poprawnie osiągają zero w punkcie oszacowania; oba przedziały w pełni
ograniczone (`bounded=True` po obu stronach).

## 1. Cztery dopasowania (brief §1) — bez zmian co do liczby

| id | funkcja | zbiór (plik) | rola |
|---|---|---|---|
| **P1** | `fit_pooled` | `test6_intervals.csv` (18 diad, ekspozycja) | **ORZEKA** dla H9 |
| F1 | `fit_frailty` | `test6_intervals.csv` — **wyłącznie** ten zbiór | drugorzędny (D-015 B) |
| S-A | `fit_pooled` | `test6_intervals_sensitivity_SA.csv` (epizodowy×kalendarz) | wrażliwość na D-014 |
| S-B | `fit_pooled` | `test6_intervals_sensitivity_SB.csv` (próg surowy×ekspozycja) | wrażliwość na D-013 |

Kruchość (F1) liczona tylko na zbiorze głównym. Estymator jest teraz też podstawą Testu 7
(`TASK_7B_BRIEF.md` §1–2), gdzie role P1/F1 są ODWRÓCONE — tam orzeka model z kruchością,
tu pulowany (D-015 B, uzasadnienie przy różnej wielkości populacji).

## 2. Wiarygodność pulowana (P1, S-A, S-B) — bez zmian

```
h(t) = (k/λ)·(t/λ)^(k−1)      H(t) = (t/λ)^k
pełna:       log f(t) = log(k/λ) + (k−1)·log(t/λ) − H(t)
cenzurowana: log S(t) = −H(t)
```

## 3. Wiarygodność z kruchością gamma (F1, D-015 B) — wzór bez zmian, θ z podłogą wszędzie

```
log L_i = Σ_{j:pełne} log h(t_ij) + D_i·log θ + lgamma(1/θ+D_i) − lgamma(1/θ)
        − (1/θ+D_i)·log(1+θ·H_i)
```

Podłoga `θ = max(exp(log θ), 1e-10)` stosowana identycznie wewnątrz wiarygodności i w
zwracanej wartości (0.3).

## 4. Przedziały ufności (brief §4)

- **Profil wiarygodności dla k** (`profile_ci_k`): zakotwiczony w k̂, rozszerzany na zewnątrz
  (0.5); granica nieosiągnięta w siatce → `nan` (0.1), nigdy brzeg siatki.
- **Bootstrap na poziomie diady**: jak dotąd (każda kopia diady własną etykietą grupy dla F1),
  jeden punkt startowy na replikę — wielostart jest tam, gdzie się liczy najbardziej, czyli
  w punktowym oszacowaniu na pełnych danych; B replik × wielostart byłoby nieproporcjonalnie
  kosztowne.

## 5. Testy poprawności (brief §3) — zaktualizowane po poprawkach

### 5.1 Granica θ→0 — bez zmian, wciąż zaliczony

Różnica log-wiarygodności pulowanej i z kruchością (θ=1e-6): **1,23·10⁻⁵**.

### 5.2 Odzysk parametrów — trzy zestawy, struktura 18/45/18, po poprawkach 0.2–0.4

| zestaw | k praw. | λ praw. | θ praw. | k̂ pulowany | k̂ kruchość | θ̂ kruchość | zgodność startów |
|---|---|---|---|---|---|---|---|
| k=1, θ=0 | 1,0 | 20,0 | 0,0 | 1,019 | 1,020 | 1e-10 (granica) | oba modele: tak |
| k=1,5, θ=0,3 | 1,5 | 15,0 | 0,3 | 1,361 | 1,361 | 1e-10 (granica) | oba modele: tak |
| k=0,7, θ=0,6 | 0,7 | 25,0 | 0,6 | 0,605 | 0,626 | 0,067 | oba modele: tak |

Wszystkie pięć startów zgadza się do ~10⁻⁵–10⁻⁸ we wszystkich sześciu dopasowaniach
(3 zestawy × 2 modele) — usterka 0.2 nie występuje po poprawce. Liczby punktowe różnią się
od wersji sprzed poprawek (inny schemat cenzurowania → inne dane syntetyczne przy tym samym
ziarnie), nie są bezpośrednio porównywalne z poprzednią tabelą.

Odczyt bez zmian względem poprzedniej wersji: przy 45 zdarzeniach w 18 grupach żadna
estymacja nie jest „dokładna” i nie ma być — demonstracja reżimu, nie kalibracja pokrycia.

### 5.3 Obciążenie cenzurowania (nowy test, weryfikuje poprawkę 0.4)

400 powtórzeń, k=1, θ=0, statystyka pulowana: średnie k̂=1,0301 (obciążenie +3,0%),
mediana 1,0177, odchylenie 0,1249. Tabela porównawcza w §0.4.

### 5.4 Zakotwiczenie profilu wiarygodności (nowy test, weryfikuje poprawkę 0.5)

k=1,4, λ=18, θ=0,3: LR w k̂ ≈ 0 dla obu modeli (0,0 i −0,00036), oba przedziały w pełni
ograniczone. Tabela w §0.5.

## 6. Założenia D-015 A — w kodzie i tutaj (bez zmian)

1. **Zegar zatrzymany, nie wyzerowany.** `dlugosc_odstepu` to już suma lat ekspozycji.
2. **Dyskretyzacja.** Odstępy w pełnych latach, model ciągły — przyjęte jako ograniczenie,
   nie korygowane.

## 7. Czego ten kod NIE robi (brief §6)

- Nie dodaje piątego wariantu.
- Nie wybiera między P1 a F1 — tekst czterech przypadków czytania różnicy nadal nie został
  przekazany (D-015, „zastrzeżenie do uzupełnienia”) — potrzebny przed Krokiem 3 Testu 6
  i przed Etapem C Testu 7.
- Nie uruchamia niczego na `test6_intervals*.csv` poza odczytem struktury grup
  (`group_sizes_from`) do testów syntetycznych. `main()` blokuje `--run-real`.

## 8. D-022 — zapadanie się θ̂ do granicy (dodatek do suity, warunek Kroku 3, nie przegląd kodu)

Drugi przegląd zaakceptował pięć poprawek bez zastrzeżeń do kodu i znalazł własność
estymatora: θ̂ zapada się do granicy numerycznej **także gdy heterogeniczność naprawdę
istnieje** — przy 18–120 grupach nie zawsze da się ją wykryć. Pełne uzasadnienie i
konsekwencja dla reguły decyzyjnej D-015 B: `CPS_DECISION_LOG.md` D-022.

**`test_frailty_boundary_collapse`** (nowa, na stałe w `run_correctness_suite`): k=1,2,
60 powtórzeń, θ prawdziwe ∈ {0; 0,3; 0,6; 1,0}, na strukturze Testu 6 i Testu 7 naraz:

| θ prawdziwe | Test 6 (18 grup): % granica / mediana θ̂ | Test 7 (120 grup, 58 bez zdarzeń): % granica / mediana θ̂ |
|---|---|---|
| 0,0 | 60,0% / 1e-10 | 26,7% / 6,0·10⁻⁸ |
| 0,3 | 33,3% / 0,0050 | 18,3% / 0,0428 |
| 0,6 | 11,7% / 0,231 | 6,7% / 0,268 |
| 1,0 | 1,7% / 0,454 | 0,0% / 0,643 |

Zgodne co do rzędu wielkości z pomiarem przeglądu na strukturze Testu 6 (35%/0,0003;
17%/0,20; 0%/0,42 — różnice z innego strumienia losowań). Test 7, mimo 58 diad bez
zdarzeń, identyfikuje θ nieco lepiej niż Test 6 na każdym poziomie (więcej grup przeważa
nad brakiem zdarzeń w części z nich).

**Konsekwencja dla raportu Etapu C (obu testów):** zgodność P1/F1 czytana jako „brak
świadectwa rytmu" (D-015 B, przypadek pierwszy) **tylko gdy θ̂ nie leży na granicy**. Przy
θ̂ na granicy wynik jest nierozstrzygający co do heterogeniczności, raportowany osobno od
wyniku dla k.

**`bootstrap_ci_k_frailty`** zwraca teraz też `frac_theta_boundary` — jeśli przekracza
kilkadziesiąt procent replik, przedział bootstrapowy dla kruchości nie jest interpretowalny
i ma być tak opisany, nie podany jako goła liczba.

**Poprawki wydajnościowe wymuszone tą symulacją** (bez zmiany wyniku, zweryfikowane
identycznością z poprzednią wersją przed zamianą): `negloglik_frailty` zwektoryzowany
(`np.bincount` zamiast pętli Python po grupach — konieczne dla 120 grup Testu 7);
`group_sizes_from` poprawiony, by grupować po wszystkich wierszach, nie tylko pełnych —
inaczej 58 diad Testu 7 bez zdarzeń znikało po cichu ze struktury syntetycznej.

## 9. STOP — Krok 3 odblokowany

Warunek Kroku 3 (D-022, dodatek do suity) wykonany — bez ponownego przeglądu kodu, zgodnie
z decyzją autora. Wszystkie testy poprawności (θ→0, odzysk ×3, obciążenie cenzurowania,
zakotwiczenie profilu, zapadanie θ̂ ×2 struktury) zaliczone. **Krok 3 Testu 6 może się
rozpocząć.** Etap B Testu 7 na tym samym estymatorze — po Kroku 3 Testu 6, zgodnie z
`TASK_7B_BRIEF.md` §1 (kolejność prac).
