#!/usr/bin/env python3
"""
TEST 12 (rodzina 10, UCDP) — Etap 2, symulacja mocy/kalibracji z SS8 protokolu.

Cztery pomiary, wszystkie na strukturze rzeczywistej (74 pary, 221 zdarzen pelnych, 25%
cenzurowania) mechanizmem min(T,C) (D-031), NIGDY na realnych wartosciach t:

1. Odchylenie k-hat pod prawda k=1 (test7_estimate.declared_deviation, reuzyte bez zmian).
2. Faktyczny poziom istotnosci PELNEJ reguly SS5 (N1 p<0.05 ORAZ profil wyklucza 1) pod
   prawda zerowa - zgodnie z ustaleniem D-053, nominalne 0.05 nie obowiazuje dla koniunkcji.
3. Pokrycie OBU przedzialow (profil i bootstrap) na poziomie par, pod prawda k=1, D-045-style.
4. NAJWAZNIEJSZY: obciazenie k-hat wynikajace z zaokraglenia odstepow do pelnych lat, na
   rozkladzie o medianie dwoch lat.

Mechanizm dyskretyzacji (pomiar 4) - wyprowadzenie: jesli epizod konczy sie w czasie ciaglym
t1 = E + phi (E=rok calkowity, phi~U(0,1) faza w roku), a nastepny epizod zaczyna sie w
czasie ciaglym t1+T (T~Weibull(k,lambda) ciagle), to obserwowana calkowita przerwa w latach
(wariant A) wynosi floor(phi+T) - 1. Warunek T+phi>=1 (inaczej nie bylby to osobny epizod z
przynajmniej jednym pelnym rokiem przerwy, sprzeczne z definicja epizodu SS2 protokolu) -
losowania z T+phi<1 odrzucane (rejection sampling), nie ucinane.
"""
from __future__ import annotations
import json, time
import numpy as np
import pandas as pd

import test6_weibull as w
import test6_null as n0
import test7_estimate as e

SEED = w.RNG_SEED
SEED_N1 = 20260822


def load_structure(path="test12_intervals_prog3.csv"):
    df = pd.read_csv(path, comment="#")
    windows = df.groupby("dyad_id")["dlugosc"].sum().tolist()
    n_full = int((df.cenzurowany == 0).sum())
    n_cens = int((df.cenzurowany == 1).sum())
    return windows, n_full, n_cens


# ============================ pomiar 1: odchylenie ============================
def measure_deviation(windows, n_full, n_reps=2000):
    lam_true = sum(windows) / n_full
    res = e.declared_deviation(windows, "pooled", k_true=1.0, lam_true=lam_true, n_reps=n_reps, seed=SEED)
    return res, lam_true


# ============================ pomiar 2+3: kalibracja pelnej reguly + pokrycie ============================
def one_calib_rep(windows, lam_true, rng, B_n1=300, B_boot=300):
    t, event, gid = e.simulate_dataset_test7(1.0, lam_true, 0.0, windows, rng)
    fit = w.fit_pooled(t, event)
    prof = w.profile_ci_k(w.negloglik_pooled, (t, event), fit["k"], [fit["loglam"]], fit["loglik"])
    lo_p, hi_p = prof["lo"], prof["hi"]
    profil_wyklucza_1 = bool((not np.isnan(lo_p)) and (not np.isnan(hi_p)) and not (lo_p <= 1.0 <= hi_p))
    profil_pokrywa_1 = bool((not np.isnan(lo_p)) and (not np.isnan(hi_p)) and lo_p <= 1.0 <= hi_p)

    lo_b, hi_b, _ = w.bootstrap_ci_k_pooled(t, event, gid, B=B_boot, seed=int(rng.integers(0, 2**31 - 1)))
    bootstrap_pokrywa_1 = bool(lo_b <= 1.0 <= hi_b)

    grouped = []
    for g in range(len(windows)):
        mask = gid == g
        t_full = t[mask & (event == 1)]
        c_rows = t[mask & (event == 0)]
        c = float(c_rows[0]) if len(c_rows) else None
        grouped.append((g, t_full, c))
    rngn = np.random.default_rng(int(rng.integers(0, 2**31 - 1)))
    k_sur = np.empty(B_n1)
    for b in range(B_n1):
        t_sim, ev_sim = n0.simulate_n1_once(grouped, rngn)
        k_sur[b] = w.fit_pooled(t_sim, ev_sim)["k"]
    p_n1 = (1 + int(np.sum(np.abs(k_sur - 1.0) >= np.abs(fit["k"] - 1.0)))) / (B_n1 + 1)

    pelna_regula_odrzuca = bool(p_n1 < 0.05 and profil_wyklucza_1)
    return dict(k=fit["k"], p_n1=p_n1, profil_pokrywa_1=profil_pokrywa_1,
               bootstrap_pokrywa_1=bootstrap_pokrywa_1, pelna_regula_odrzuca=pelna_regula_odrzuca)


def measure_calibration(windows, lam_true, n_outer=150, B_n1=300, B_boot=300, seed=SEED):
    rng = np.random.default_rng(seed)
    recs = [one_calib_rep(windows, lam_true, rng, B_n1, B_boot) for _ in range(n_outer)]
    n = len(recs)
    pokrycie_profil = float(np.mean([r["profil_pokrywa_1"] for r in recs]))
    pokrycie_bootstrap = float(np.mean([r["bootstrap_pokrywa_1"] for r in recs]))
    poziom_pelnej_reguly = float(np.mean([r["pelna_regula_odrzuca"] for r in recs]))
    return dict(n_outer=n, B_n1=B_n1, B_boot=B_boot,
               pokrycie_profil=pokrycie_profil, pokrycie_bootstrap=pokrycie_bootstrap,
               faktyczny_poziom_pelnej_reguly=poziom_pelnej_reguly,
               faktyczny_poziom_95CI=(
                   max(0.0, poziom_pelnej_reguly - 1.96 * np.sqrt(poziom_pelnej_reguly * (1 - poziom_pelnej_reguly) / n)),
                   min(1.0, poziom_pelnej_reguly + 1.96 * np.sqrt(poziom_pelnej_reguly * (1 - poziom_pelnej_reguly) / n)),
               ))


# ============================ pomiar 4: obciazenie z zaokraglenia ============================
def discretize_gap(T, rng):
    while True:
        phi = rng.uniform(0.0, 1.0)
        val = phi + T
        if val >= 1.0:
            return float(np.floor(val)) - 1.0


def simulate_rounded_dataset(k, lam, windows, rng):
    """Jak simulate_dataset_test7, ale kazdy PELNY odstep przechodzi przez dyskretyzacje
    rok-po-roku (funkcja discretize_gap) - okna same w sobie sa juz calkowitoliczbowe
    (rzeczywiste dane), wiec wyscig min(T,C) toczy sie w jednostkach zdyskretyzowanych."""
    ts, ev, gid = [], [], []
    for g, Wlen in enumerate(windows):
        cum = 0.0
        while True:
            T = lam * rng.exponential(1.0) ** (1.0 / k)
            gap_obs = discretize_gap(T, rng)
            if cum + gap_obs <= Wlen:
                ts.append(gap_obs); ev.append(1); gid.append(g)
                cum += gap_obs
            else:
                cens_obs = max(0.0, np.floor(Wlen - cum))
                ts.append(cens_obs); ev.append(0); gid.append(g)
                break
    return np.array(ts, float), np.array(ev, int), np.array(gid)


def measure_rounding_bias(windows, lam_true, k_true=1.0, n_reps=400, seed=SEED):
    rng = np.random.default_rng(seed)
    ks_rounded = np.empty(n_reps)
    ks_continuous = np.empty(n_reps)
    for i in range(n_reps):
        t_r, ev_r, _ = simulate_rounded_dataset(k_true, lam_true, windows, rng)
        ks_rounded[i] = w.fit_pooled(t_r, ev_r)["k"]
        t_c, ev_c, _ = e.simulate_dataset_test7(k_true, lam_true, 0.0, windows, rng)
        ks_continuous[i] = w.fit_pooled(t_c, ev_c)["k"]
    return dict(k_true=k_true, n_reps=n_reps,
               k_hat_rounded_mean=float(ks_rounded.mean()), k_hat_rounded_median=float(np.median(ks_rounded)),
               k_hat_rounded_sd=float(ks_rounded.std(ddof=1)),
               k_hat_continuous_mean=float(ks_continuous.mean()), k_hat_continuous_median=float(np.median(ks_continuous)),
               obciazenie_mean=float(ks_rounded.mean() - ks_continuous.mean()),
               obciazenie_vs_k_true=float(ks_rounded.mean() - k_true))


def main():
    windows, n_full, n_cens = load_structure()
    out = {"n_grup": len(windows), "n_full_real": n_full, "n_cens_real": n_cens}

    t0 = time.time()
    dev, lam_true = measure_deviation(windows, n_full)
    out["lam_true"] = lam_true
    out["pomiar1_odchylenie"] = dev
    print(f"[1] odchylenie: SD={dev['sd_k_hat']:.4f} mediana={dev['median_k_hat']:.4f} ({time.time()-t0:.0f}s)")

    t0 = time.time()
    calib = measure_calibration(windows, lam_true, n_outer=150)
    out["pomiar2_3_kalibracja"] = calib
    print(f"[2,3] pokrycie profil={calib['pokrycie_profil']:.3f} bootstrap={calib['pokrycie_bootstrap']:.3f} "
         f"poziom_pelnej_reguly={calib['faktyczny_poziom_pelnej_reguly']:.3f} ({time.time()-t0:.0f}s)")

    t0 = time.time()
    bias = measure_rounding_bias(windows, lam_true, n_reps=400)
    out["pomiar4_obciazenie_zaokraglenia"] = bias
    print(f"[4] obciazenie(rounded-continuous)={bias['obciazenie_mean']:.4f} "
         f"obciazenie(rounded-k_true)={bias['obciazenie_vs_k_true']:.4f} ({time.time()-t0:.0f}s)")

    threshold_lo = 1.0 - 1.96 * dev["sd_k_hat"]
    threshold_hi = 1.0 + 1.96 * dev["sd_k_hat"]
    out["prog_wykluczenia_1"] = [threshold_lo, threshold_hi]
    print(f"prog wykluczenia 1: <{threshold_lo:.3f} lub >{threshold_hi:.3f}")

    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    with open("test12_power_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test12_power_wyniki.json")


if __name__ == "__main__":
    main()
