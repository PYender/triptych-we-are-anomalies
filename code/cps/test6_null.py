#!/usr/bin/env python3
"""
TEST 6 — Krok B (D-023/D-024): modele zerowe N1/N2 zgodnie z TEST6_PROTOCOL.md §6.

N1 — parametryczny. Proces Poissona o intensywności estymowanej z danych, OSOBNO dla
każdej diady, z tą samą strukturą cenzurowania i tą samą liczbą zdarzeń: dla diady
o n zdarzeniach pełnych (t_1..t_n) i jednej obserwacji cenzurowanej (c), λ̂ = n / (Σt_i + c)
(standardowy MLE wykładniczy z cenzurowaniem). Surogat: n świeżych rysowań
Exponential(1/λ̂), CENZUROWANA WARTOŚĆ POZOSTAJE c (struktura okna administracyjnego jest
faktem, nie częścią modelu zerowego) — liczba zdarzeń i typ cenzurowania niezmienione,
zmieniają się tylko wylosowane długości odstępów pełnych.

N2 — permutacyjny. Odstępy przetasowane MIĘDZY diadami z zachowaniem liczebności: pula
wartości pełnych (n=45) tasowana i rozdzielana z powrotem do diad zachowując, ile pełnych
wnosi każda diada; analogicznie pula cenzurowanych (n=18, jedna na diadę). Niszczy
strukturę WEWNĄTRZ diady (kolejność/wielkość odstępów danej pary), zachowuje rozkład
brzegowy całej puli.

Statystyka i wartość p (§6): p = (1 + #{|k̂_sur − 1| ≥ |k̂_obs − 1|}) / (B + 1), k̂ liczone
naprawionym `test6_weibull.fit_pooled` (pięć poprawek + D-022) identycznie na danych
obserwowanych i na każdym surogacie.

B=2000, ziarno 20260822 (§6 — inny niż RNG_SEED=20260823 używany w test6_weibull.py dla
testów poprawności; ten skrypt ma WŁASNE, protokołem narzucone ziarno).

D-026: N2 zdegenerowany względem k̂ pulowanego, poza regułą decyzyjną §8 (diagnostyka).
D-026 §7: kontrola remisów (`tie_fraction`) wbudowana w run_n1/run_n2, zatrzymuje bieg,
jeśli surogaty remisują z obserwacją ponad próg — zabezpieczenie przed pomyleniem szumu
numerycznego z wynikiem (dokładnie to, co przeoczono przy pierwszym zgłoszeniu P2=1,000).

Krok C AUTORYZOWANY (2026-08-25, po D-026) — `--run-real` odblokowane.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import numpy as np
import pandas as pd

import test6_weibull as w

SEED_PROTOCOL = 20260822        # §6 — ziarno przypisane WYŁĄCZNIE modelom zerowym N1/N2
B_NULL = 2000

# D-026 §7 (reguła ogólna po korekcie Claude): każdy model zerowy oparty na symulacji, w
# którym surogat może remisować z obserwacją, wymaga jawnego wykrywania remisów — inaczej
# nierówność nieostra z §6 jest poprawna tylko w arytmetyce dokładnej; w zmiennoprzecinkowej
# remis rozstrzyga się na szumie i daje pozornie sensowną, w rzeczywistości bezwartościową
# liczbę (patrz N2, p=0,253/0,266). TIE_TOL=1e-6 — tolerancja rozpoznania remisu;
# TIE_FRAC_STOP — próg odsetka remisów, powyżej którego bieg ma się zatrzymać (nie tylko
# ostrzec) jako degenerację, a nie liczyć p dalej.
TIE_TOL = 1e-6
TIE_FRAC_STOP = 0.01


def tie_fraction(k_sur: np.ndarray, kobs: float, tol: float = TIE_TOL) -> float:
    """Odsetek surogatów remisujących z obserwacją (|k_sur-k_obs|<tol) — D-026 §7. Pod
    prawdziwie ciągłym, niezdegenerowanym rozkładem zerowym oczekiwana wartość to praktycznie
    zero (prawdopodobieństwo trafienia w przedział szerokości 2*tol jest znikome); wartość
    istotnie większa od zera jest sygnałem degeneracji typu N2, nie zbiegiem okoliczności."""
    return float(np.mean(np.abs(k_sur - kobs) < tol))


def load_grouped(path: str):
    """Zwraca listę (diad, t_full: np.ndarray, c_cens: float) — jedna pozycja na diadę,
    z zachowaniem struktury pliku (może mieć 0 zdarzeń pełnych, wtedy t_full puste)."""
    df = pd.read_csv(path, comment="#")
    out = []
    for d, g in df.groupby("diada"):
        t_full = g.loc[g.cenzurowany == 0, "dlugosc_odstepu"].to_numpy(float)
        c_rows = g.loc[g.cenzurowany == 1, "dlugosc_odstepu"].to_numpy(float)
        assert len(c_rows) == 1, f"diada {d}: oczekiwano dokładnie 1 obserwacji cenzurowanej, jest {len(c_rows)}"
        out.append((d, t_full, float(c_rows[0])))
    return out


def flatten(grouped):
    """(diady, t, event) z listy (diad, t_full, c) — do fit_pooled."""
    diads, t, event = [], [], []
    for d, t_full, c in grouped:
        for x in t_full:
            diads.append(d); t.append(x); event.append(1)
        diads.append(d); t.append(c); event.append(0)
    return np.array(diads), np.array(t, float), np.array(event, int)


def k_obs(path: str) -> tuple[float, list]:
    grouped = load_grouped(path)
    diads, t, event = flatten(grouped)
    fit = w.fit_pooled(t, event)
    return fit["k"], grouped


# ============================ N1 — parametryczny (Poisson per diada) ============================
def simulate_n1_once(grouped, rng) -> float:
    diads_sim, t_sim, event_sim = [], [], []
    for d, t_full, c in grouped:
        n = len(t_full)
        total_exposure = float(t_full.sum() + c)         # ekspozycja obserwowana, struktura stała
        lam_hat = n / total_exposure if total_exposure > 0 else 0.0
        if n > 0 and lam_hat > 0:
            new_full = rng.exponential(1.0 / lam_hat, size=n)
        else:
            new_full = np.array([])
        for x in new_full:
            diads_sim.append(d); t_sim.append(x); event_sim.append(1)
        diads_sim.append(d); t_sim.append(c); event_sim.append(0)     # cenzurowanie: struktura stała
    return np.array(t_sim, float), np.array(event_sim, int)


def run_n1(path: str, B: int = B_NULL, seed: int = SEED_PROTOCOL):
    kobs, grouped = k_obs(path)
    rng = np.random.default_rng(seed)
    k_sur = np.empty(B)
    for b in range(B):
        t_sim, event_sim = simulate_n1_once(grouped, rng)
        k_sur[b] = w.fit_pooled(t_sim, event_sim)["k"]
    frac_tie = tie_fraction(k_sur, kobs)
    if frac_tie > TIE_FRAC_STOP:
        raise AssertionError(
            f"D-026 §7: {frac_tie:.1%} surogatów N1 remisuje z obserwacją "
            f"(|k_sur-k_obs|<{TIE_TOL}) — próg {TIE_FRAC_STOP:.0%} przekroczony, oznaka "
            "degeneracji analogicznej do N2. Zatrzymuję bieg zamiast zwracać p bez treści.")
    p = (1 + int(np.sum(np.abs(k_sur - 1.0) >= np.abs(kobs - 1.0)))) / (B + 1)
    return dict(model="N1", k_obs=kobs, p=p, B=B, seed=seed,
               k_sur_mean=float(k_sur.mean()), k_sur_median=float(np.median(k_sur)),
               k_sur_sd=float(k_sur.std(ddof=1)), frac_tie=frac_tie)


# ============================ N2 — permutacyjny (między diadami) ============================
# D-026: N2 jest ZDEGENEROWANY względem k̂ pulowanego. `negloglik_pooled(params, t, event)`
# sumuje po obserwacjach bez odniesienia do etykiety diady — k̂ zależy wyłącznie od
# multizbioru par (t, event). Permutacja N2 przenosi wartości MIĘDZY diadami, ale nie
# zmienia tego multizbioru: k̂_sur == k̂_obs dla KAŻDEJ permutacji, z konstrukcji, niezależnie
# od danych. Konsekwencja: p_N2 = (1+B)/(B+1) ≡ 1,000 zawsze — nie wynik, tożsamość algebraiczna.
# §8 wymaga P2<0,10 razem z dwoma innymi warunkami; skoro P2≡1, §8 jest niespełnialne w
# obecnym brzmieniu protokołu. Kod poniżej ODTWARZA §6 dosłownie i poprawnie — wada leży w
# niespójności protokołu (§6 kontra §5/§7), nie w tej implementacji. `run_n2` pozostaje do
# diagnostyki (np. na modelu kruchości F1, gdzie permutacja NIE jest zdegenerowana, bo θ
# zależy od grupowania wewnątrz diady) — NIE wchodzi do reguły decyzyjnej §8 dla P1.
def simulate_n2_once(grouped, rng) -> tuple[np.ndarray, np.ndarray]:
    full_pool = np.concatenate([t_full for _, t_full, _ in grouped]) if any(len(t_full) for _, t_full, _ in grouped) else np.array([])
    cens_pool = np.array([c for _, _, c in grouped], float)
    full_perm = rng.permutation(full_pool)
    cens_perm = rng.permutation(cens_pool)
    t_sim, event_sim = [], []
    i = 0
    for _, t_full, _ in grouped:
        n = len(t_full)
        for x in full_perm[i:i + n]:
            t_sim.append(x); event_sim.append(1)
        i += n
    for c in cens_perm:
        t_sim.append(c); event_sim.append(0)
    return np.array(t_sim, float), np.array(event_sim, int)


def run_n2(path: str, B: int = B_NULL, seed: int = SEED_PROTOCOL):
    """D-026: DIAGNOSTYKA, poza regułą decyzyjną §8 — zdegenerowany względem k̂ pulowanego
    (patrz komentarz nad `simulate_n2_once`). MATEMATYCZNIE k̂_sur ≡ k̂_obs dla każdej permutacji
    (ten sam multizbiór par (t,event)), więc TEORETYCZNIE p powinno wynosić tożsamościowo
    (1+B)/(B+1)=1,000. W PRAKTYCE, na tym kodzie (Nelder-Mead, tolerancja ~1e-8), k̂_sur różni
    się od k̂_obs o szum numeryczny (kolejność sumowania zmienia się przy permutacji, stąd
    inny wynik optymalizacji w granicach tolerancji) — `p` liczone dosłownie ze wzoru §6
    wychodzi jako WARTOŚĆ POZORNIE SENSOWNA, ale w rzeczywistości przypadkowa i zależna od
    ziarna (sprawdzone: 0,253 i 0,266 dla dwóch różnych ziarn na tych samych danych realnych,
    identyczne p przy identycznym ziarnie — deterministyczne, ale bez treści). Ani 1,000, ani
    ta pozorna wartość nie są prawdziwym wynikiem — obie są artefaktem tej samej degeneracji,
    tylko widocznym na innym poziomie precyzji. Funkcja zostaje ze względu na przejrzystość
    (pokazuje degenerację wprost, nie ukrywa jej usuwając kod) i jako baza pod ewentualną
    diagnostykę F1 (niewykonaną tutaj)."""
    kobs, grouped = k_obs(path)
    rng = np.random.default_rng(seed)
    k_sur = np.empty(B)
    for b in range(B):
        t_sim, event_sim = simulate_n2_once(grouped, rng)
        k_sur[b] = w.fit_pooled(t_sim, event_sim)["k"]
    frac_tie = tie_fraction(k_sur, kobs)          # oczekiwane WYSOKIE (degeneracja znana, D-026)
    p = (1 + int(np.sum(np.abs(k_sur - 1.0) >= np.abs(kobs - 1.0)))) / (B + 1)
    return dict(model="N2", k_obs=kobs, p=p, B=B, seed=seed,
               k_sur_mean=float(k_sur.mean()), k_sur_median=float(np.median(k_sur)),
               k_sur_sd=float(k_sur.std(ddof=1)), frac_tie=frac_tie,
               poza_regula_decyzyjna_S8=True,
               uwaga_D026="zdegenerowany wzgledem k-hat pulowanego (k_sur_sd rzedu 1e-8 = "
                          "szum optymalizatora, nie sygnal); 'p' policzone doslownie ze wzoru "
                          "SS6 jest artefaktem szumu numerycznego przy dokladnej remisie, NIE "
                          "wartoscia 1.000 w praktyce ani wynikiem empirycznym - nie raportowac "
                          "jako liczby, tylko jako opisane zjawisko")


# ============================ D-026: diagnostyki zlecone przed biegiem P1 ============================
def n1_window_exceedance(grouped, B: int = B_NULL, seed: int = SEED_PROTOCOL):
    """Frakcja replik N1, w których Σt_sim + c przekracza realną długość okna diady (T =
    Σt_full_real + c). Nadmiar jest DOKŁADNY, nie tylko „systematyczny" (D-026 §7, Claude):
    λ̂ = n/T, więc oczekiwana długość pojedynczego losowanego odstępu = T/n, a suma n odstępów
    ma w oczekiwaniu E[Σt_sim] = n·(T/n) = T. Po dołożeniu NIEZMIENIONEGO c surogat ma
    oczekiwany czas całkowity E[Σt_sim+c] = T+c, wobec obserwowanego T — nadmiar w oczekiwaniu
    równa się DOKŁADNIE c, nie w przybliżeniu. Stąd struktura n1_window_exceedance ~75% w
    całym zbiorze: to własność konstrukcji N1 w dosłownym brzmieniu §6, nie efekt uboczny
    parametrów. Konsekwencja dla odczytu wyniku (asymetryczna, nie tylko „konserwatywny"):
    niska wartość P1 jest wiarygodna z nadwyżką (rozkład zerowy jest już rozdęty, więc trudniej
    o nią przez przypadek), wysoka wartość P1 jest częściowo przypisywalna KONSTRUKCJI modelu
    zerowego, nie danym. Nie naprawiane (D-026 §7: opisujemy, nie łatamy protokół po fakcie)."""
    rng = np.random.default_rng(seed)
    per_diad, total_exceed, total_reps = [], 0, 0
    for d, t_full, c in grouped:
        tot_real = float(t_full.sum() + c)
        n_full = len(t_full)
        lam_hat = n_full / tot_real if tot_real > 0 else 0.0
        exceed = 0
        for _ in range(B):
            sim_full_sum = rng.exponential(1.0 / lam_hat, size=n_full).sum() if (n_full > 0 and lam_hat > 0) else 0.0
            if sim_full_sum + c > tot_real:
                exceed += 1
        per_diad.append(dict(diada=d, n=n_full, c=c, tot_real=tot_real, frac_exceed=exceed / B))
        total_exceed += exceed; total_reps += B
    return dict(overall_frac_exceed=total_exceed / total_reps, per_diad=per_diad, B=B, seed=seed)


def test_tie_detector_discriminates(n_reps=300, seed=13):
    """D-026 §7: sprawdza, że `tie_fraction`/próg TIE_FRAC_STOP faktycznie rozróżniają
    zdegenerowany przypadek (N2, znany) od niezdegenerowanego (surogat losowany niezależnie
    od obserwacji, np. czysty szum) — nie tylko istnieją w kodzie, ale robią to, co mają."""
    rng = np.random.default_rng(seed)
    kobs = 0.85
    k_sur_degenerate = np.full(n_reps, kobs) + rng.normal(0, 1e-8, n_reps)   # jak N2
    k_sur_healthy = rng.normal(1.0, 0.15, n_reps)                            # jak N1 zdrowy
    frac_degenerate = tie_fraction(k_sur_degenerate, kobs)
    frac_healthy = tie_fraction(k_sur_healthy, kobs)
    return dict(frac_degenerate=frac_degenerate, frac_healthy=frac_healthy,
               degenerate_flagged=frac_degenerate > TIE_FRAC_STOP,
               healthy_not_flagged=frac_healthy <= TIE_FRAC_STOP)


def run_null_correctness_suite(intervals_csv: str = "test6_intervals.csv"):
    """Suita mechaniczna Kroku B/C — do uruchomienia przed KAŻDYM biegiem P1/P2 na danych
    rzeczywistych, obok `test6_weibull.run_correctness_suite`. Nie liczy p decyzyjnego."""
    grouped = load_grouped(intervals_csv)
    out = {}
    out["n1_window_exceedance"] = n1_window_exceedance(grouped, B=500, seed=1)
    out["tie_detector_discriminates"] = test_tie_detector_discriminates()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", default="test6_intervals.csv")
    ap.add_argument("--run-real", action="store_true",
                    help="Krok C (D-026): autoryzowany przez autora, patrz CPS_DECISION_LOG.md")
    a = ap.parse_args()
    if a.run_real:
        suite = run_null_correctness_suite(a.main)
        print(json.dumps(suite, ensure_ascii=False, indent=2, default=str))
        p1 = run_n1(a.main)
        print(json.dumps(p1, ensure_ascii=False, indent=2))
        p2 = run_n2(a.main)
        print(json.dumps(p2, ensure_ascii=False, indent=2))
        return
    print("Krok B: kod gotowy. Użyj --run-real, żeby policzyć P1(N1)/P2(N2) na danych rzeczywistych.")


if __name__ == "__main__":
    main()
