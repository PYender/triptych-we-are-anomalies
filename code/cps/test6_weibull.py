#!/usr/bin/env python3
"""
TEST 6 — Etap B: estymacja Weibulla z cenzurowaniem (rodzina 9).
Realizuje TASK_6.md Etap B / TASK_6B_BRIEF.md. D-012..D-015.

Cztery dopasowania (brief §1), nie więcej: P1 (Weibull pulowany, zbiór główny — ORZEKA),
F1 (Weibull z kruchością gamma dzieloną w obrębie diady, wariant drugorzędny, WYŁĄCZNIE
zbiór główny), S-A (pulowany, epizodowy×kalendarz), S-B (pulowany, próg surowy×ekspozycja).

D-015 A — założenia, nazwane tu i w raporcie:
  1. Zegar zatrzymany, nie wyzerowany: odstęp o przerwanej ekspozycji = SUMA lat ekspozycji;
     model liczy hazard od tej sumy, jakby proces nie przestawał płynąć. Dotyczy obserwacji
     dotkniętych przez D-014 (ekspozycja < kalendarz).
  2. Dyskretyzacja: odstępy w pełnych latach, model ciągły — dla odstępów minimalnych (1 rok)
     różnica nie jest zaniedbywalna; przyjęte jako założenie, nie korygowane.

Cenzurowany odstęp o ekspozycji zero (Austria-Hungary–Italy, D-014 §3) wnosi log S(0) = 0,
tj. nic — NIE jest usuwany z pętli; log(t/lam) liczony tylko dla obserwacji pełnych (t>0
zagwarantowane asercją w builderze), więc nie ma dzielenia/log(0).

NIE URUCHAMIANE na danych rzeczywistych w tym etapie (Krok 2, TASK_6B_BRIEF.md §8). Jedyne
uruchomienia w tym pliku to testy poprawności na danych SYNTETYCZNYCH (§3 brief):
  1. granica θ→0 (kruchość → pulowany)
  2. odzysk parametrów (trzy zestawy, w tym k=1 i θ=0), na strukturze 18 grup / 45 zdarzeń /
     18 cenzurowanych identycznej z Etapem A.
Wyniki tych testów są częścią produktu — patrz test6_weibull.md i sekcja main() poniżej
(uruchamiana jawnie z linii poleceń, nigdy automatycznie na test6_intervals.csv).
"""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gammaln
from scipy.stats import chi2

RNG_SEED = 20260823


# ============================ dane ============================
def load_variant(path: str):
    """Zwraca (t, event, diad): t=dlugosc_odstepu (lata ekspozycji lub kalendarzowe wg
    wariantu pliku), event=1 pełny/0 cenzurowany, diad=etykieta grupy."""
    df = pd.read_csv(path, comment="#")
    t = df["dlugosc_odstepu"].to_numpy(float)
    event = 1 - df["cenzurowany"].to_numpy(int)
    diad = df["diada"].to_numpy()
    return t, event, diad


# ============================ P1/S-A/S-B: Weibull pulowany ============================
def negloglik_pooled(params: np.ndarray, t: np.ndarray, event: np.ndarray) -> float:
    logk, loglam = params
    k, lam = np.exp(logk), np.exp(loglam)
    H = (t / lam) ** k
    t_safe = np.where(t > 0, t, 1.0)                 # log(t/lam) tylko sensowny dla t>0;
    logf = np.log(k / lam) + (k - 1.0) * np.log(t_safe / lam) - H
    ll = np.where(event == 1, logf, -H)              # cenzurowany: log S(t) = -H(t); t=0 -> 0
    return -float(np.sum(ll))


def fit_pooled(t, event, x0=(0.0, 3.0)):
    res = minimize(negloglik_pooled, x0=np.array(x0, dtype=float), args=(t, event),
                   method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-11, maxiter=8000))
    logk, loglam = res.x
    return dict(k=float(np.exp(logk)), lam=float(np.exp(loglam)), loglik=-float(res.fun),
               logk=float(logk), loglam=float(loglam), res=res)


# ============================ F1: Weibull + kruchość gamma (D-015 B) ============================
def negloglik_frailty(params: np.ndarray, t: np.ndarray, event: np.ndarray,
                      group_idx: np.ndarray, n_groups: int) -> float:
    logk, loglam, logtheta = params
    # theta floor: exp(logtheta) może dojść do 0.0 w float64 (logtheta < ~-745), gdy
    # optymalizator eksploruje granicę theta->0; bez tego 1/theta -> inf, log(theta) -> -inf,
    # gammaln(inf) daje nan. Floor nie zmienia optimum (theta->0 to i tak granica testowana
    # osobno testem theta_zero_limit), tylko chroni minimalizator przed nan podczas przeszukiwania.
    k, lam, theta = np.exp(logk), np.exp(loglam), max(np.exp(logtheta), 1e-10)
    H = (t / lam) ** k
    t_safe = np.where(t > 0, t, 1.0)
    logh = np.log(k / lam) + (k - 1.0) * np.log(t_safe / lam)     # log h(t), użyty tylko gdzie event==1
    total = 0.0
    for g in range(n_groups):
        m = group_idx == g
        ev = event[m] == 1
        D = int(ev.sum())
        Hi = float(H[m].sum())
        sum_logh = float(logh[m][ev].sum())
        total += (sum_logh + D * np.log(theta) + gammaln(1.0 / theta + D) - gammaln(1.0 / theta)
                 - (1.0 / theta + D) * np.log1p(theta * Hi))
    return -total


def fit_frailty(t, event, diad, x0=(0.0, 3.0, -2.0)):
    groups, group_idx = np.unique(diad, return_inverse=True)
    n_groups = len(groups)
    res = minimize(negloglik_frailty, x0=np.array(x0, dtype=float),
                   args=(t, event, group_idx, n_groups),
                   method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-11, maxiter=12000))
    logk, loglam, logtheta = res.x
    return dict(k=float(np.exp(logk)), lam=float(np.exp(loglam)), theta=float(np.exp(logtheta)),
               loglik=-float(res.fun), logk=float(logk), loglam=float(loglam),
               logtheta=float(logtheta), res=res)


# ============================ przedziały ufności (brief §4) ============================
def profile_ci_k(negloglik_full, args, k_hat: float, rest0: np.ndarray, loglik_max: float,
                 level: float = 0.95, n_grid: int = 81,
                 k_lo_mult: float = 0.1, k_hi_mult: float = 10.0):
    """Profil wiarygodności dla k: dla siatki log k, optymalizuje pozostałe parametry
    (`rest`), zwraca (lo, hi) na progu χ²_1 przy `level`."""
    thresh = chi2.ppf(level, df=1)
    grid = np.linspace(np.log(k_hat * k_lo_mult), np.log(k_hat * k_hi_mult), n_grid)
    lr = np.empty(n_grid)
    rest = np.array(rest0, dtype=float)
    for i, lk in enumerate(grid):
        def obj(r, lk=lk):
            return negloglik_full(np.concatenate(([lk], r)), *args)
        res = minimize(obj, x0=rest, method="Nelder-Mead",
                       options=dict(xatol=1e-9, fatol=1e-11, maxiter=3000))
        rest = res.x
        lr[i] = 2.0 * (loglik_max - (-res.fun))
    k_grid = np.exp(grid)
    idx_hat = int(np.argmin(np.abs(k_grid - k_hat)))
    lo = _interp_crossing(k_grid, lr, thresh, idx_hat, -1)
    hi = _interp_crossing(k_grid, lr, thresh, idx_hat, +1)
    return lo, hi, k_grid, lr


def _interp_crossing(k_grid, lr, thresh, idx_hat, direction):
    i = idx_hat
    n = len(k_grid)
    while 0 <= i + direction < n:
        j = i + direction
        if lr[j] >= thresh:
            k0, k1 = k_grid[i], k_grid[j]
            l0, l1 = lr[i], lr[j]
            frac = (thresh - l0) / (l1 - l0) if l1 != l0 else 0.0
            return float(k0 + frac * (k1 - k0))
        i = j
    return float(k_grid[0] if direction < 0 else k_grid[-1])   # siatka nie sięga granicy


def bootstrap_ci_k_pooled(t, event, diad, B=2000, seed=RNG_SEED, level=0.95, x0=(0.0, 3.0)):
    """Bootstrap CAŁYCH DIAD (nie odstępów) — brief §4."""
    groups = np.unique(diad)
    idx_by_group = {g: np.where(diad == g)[0] for g in groups}
    rng = np.random.default_rng(seed)
    ks = np.empty(B)
    for b in range(B):
        sampled = rng.choice(groups, size=len(groups), replace=True)
        idx = np.concatenate([idx_by_group[g] for g in sampled])
        fit = fit_pooled(t[idx], event[idx], x0=x0)
        ks[b] = fit["k"]
    lo, hi = np.percentile(ks, [(1 - level) / 2 * 100, (1 + level) / 2 * 100])
    return float(lo), float(hi), ks


def bootstrap_ci_k_frailty(t, event, diad, B=2000, seed=RNG_SEED, level=0.95,
                           x0=(0.0, 3.0, -2.0)):
    """Bootstrap diadowy dla F1 — każda kopia wylosowanej diady dostaje WŁASNĄ etykietę
    grupy (nie jest scalana z innymi kopiami tej samej diady w jedną super-grupę)."""
    groups = np.unique(diad)
    idx_by_group = {g: np.where(diad == g)[0] for g in groups}
    rng = np.random.default_rng(seed)
    ks = np.empty(B)
    for b in range(B):
        sampled = rng.choice(groups, size=len(groups), replace=True)
        idx_parts, lab_parts = [], []
        for rep, g in enumerate(sampled):
            ix = idx_by_group[g]
            idx_parts.append(ix)
            lab_parts.append(np.full(len(ix), f"{g}__{rep}"))
        idx = np.concatenate(idx_parts)
        lab = np.concatenate(lab_parts)
        fit = fit_frailty(t[idx], event[idx], lab, x0=x0)
        ks[b] = fit["k"]
    lo, hi = np.percentile(ks, [(1 - level) / 2 * 100, (1 + level) / 2 * 100])
    return float(lo), float(hi), ks


# ============================ dane syntetyczne (testy poprawności §3) ============================
def group_sizes_from(path="test6_intervals.csv"):
    """Struktura zbioru głównego: liczba zdarzeń pełnych per diada (1 cenzurowany na diadę
    zawsze doliczany osobno) — do testu odzysku parametrów na tej samej strukturze."""
    df = pd.read_csv(path, comment="#")
    return df[df["cenzurowany"] == 0].groupby("diada").size().to_numpy()


def simulate_dataset(k, lam, theta, n_full_per_group, rng):
    """Symuluje zbiór o STRUKTURZE zadanej przez n_full_per_group (liczba zdarzeń pełnych
    na grupę; każda grupa ma dodatkowo dokładnie 1 obserwację cenzurowaną). Kruchość
    gamma(1/theta, theta) o średniej 1 (theta=0 -> bez kruchości, u=1 dla wszystkich)."""
    ts, ev, gid = [], [], []
    for g, n_full in enumerate(n_full_per_group):
        u = 1.0 if theta <= 0 else rng.gamma(shape=1.0 / theta, scale=theta)
        for _ in range(int(n_full)):
            e = rng.exponential(1.0)                 # H(T)=u*(T/lam)^k = E ~ Exp(1)
            T = lam * (e / u) ** (1.0 / k)
            ts.append(T); ev.append(1); gid.append(g)
        # jedna obserwacja cenzurowana: prawdziwy czas T_true, obserwacja = frakcja < T_true
        e = rng.exponential(1.0)
        T_true = lam * (e / u) ** (1.0 / k)
        frac = rng.uniform(0.05, 0.95)
        ts.append(T_true * frac); ev.append(0); gid.append(g)
    return np.array(ts), np.array(ev), np.array([f"G{g}" for g in gid])


# ============================ testy poprawności (§3 brief) ============================
def test_theta_zero_limit(n_full_per_group, k_true=1.3, lam_true=20.0):
    rng = np.random.default_rng(RNG_SEED)
    t, event, diad = simulate_dataset(k_true, lam_true, 0.0, n_full_per_group, rng)
    groups, gidx = np.unique(diad, return_inverse=True)
    logk, loglam = np.log(k_true), np.log(lam_true)
    ll_pooled = -negloglik_pooled(np.array([logk, loglam]), t, event)
    for logtheta in (np.log(1e-6),):
        ll_frailty = -negloglik_frailty(np.array([logk, loglam, logtheta]), t, event, gidx, len(groups))
    diff = abs(ll_pooled - ll_frailty)
    return dict(loglik_pooled=ll_pooled, loglik_frailty_theta1e6=ll_frailty,
               abs_diff=diff, ok=diff < 1e-4)


def test_parameter_recovery(n_full_per_group, k_true, lam_true, theta_true, label):
    rng = np.random.default_rng(RNG_SEED)
    t, event, diad = simulate_dataset(k_true, lam_true, theta_true, n_full_per_group, rng)
    fit_p = fit_pooled(t, event)
    result = dict(label=label, k_true=k_true, lam_true=lam_true, theta_true=theta_true,
                 n_events=int(event.sum()), n_censored=int((1 - event).sum()),
                 n_groups=len(n_full_per_group),
                 pooled_k_hat=fit_p["k"], pooled_lam_hat=fit_p["lam"])
    if theta_true > 0:
        fit_f = fit_frailty(t, event, diad)
        result.update(frailty_k_hat=fit_f["k"], frailty_lam_hat=fit_f["lam"],
                      frailty_theta_hat=fit_f["theta"])
    else:
        fit_f = fit_frailty(t, event, diad, x0=(fit_p["logk"], fit_p["loglam"], np.log(1e-4)))
        result.update(frailty_k_hat=fit_f["k"], frailty_lam_hat=fit_f["lam"],
                      frailty_theta_hat=fit_f["theta"])
    return result


def run_correctness_suite(intervals_csv="test6_intervals.csv"):
    n_full_per_group = group_sizes_from(intervals_csv)
    out = {}
    out["theta_zero_limit"] = test_theta_zero_limit(n_full_per_group)
    out["recovery"] = [
        test_parameter_recovery(n_full_per_group, k_true=1.0, lam_true=20.0, theta_true=0.0,
                                label="k=1 (bez pamieci), theta=0 (bez kruchosci)"),
        test_parameter_recovery(n_full_per_group, k_true=1.5, lam_true=15.0, theta_true=0.3,
                                label="k=1.5 (rosnacy hazard), theta=0.3 (kruchosc umiarkowana)"),
        test_parameter_recovery(n_full_per_group, k_true=0.7, lam_true=25.0, theta_true=0.6,
                                label="k=0.7 (malejacy hazard/grupowanie), theta=0.6 (kruchosc silna)"),
    ]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intervals", default="test6_intervals.csv",
                    help="tylko do odczytu STRUKTURY (liczba zdarzeń/grupa) dla testów syntetycznych")
    ap.add_argument("--run-real", action="store_true",
                    help="ZABLOKOWANE w Etapie B — patrz TASK_6B_BRIEF.md §6/§8")
    a = ap.parse_args()
    if a.run_real:
        raise SystemExit("Etap B: uruchamianie na danych rzeczywistych jest zablokowane do Kroku 3 "
                         "(TASK_6B_BRIEF.md §6, §8). Usuń --run-real dopiero po przeglądzie kodu.")
    import json
    print(json.dumps(run_correctness_suite(a.intervals), indent=2, default=float))


if __name__ == "__main__":
    main()
