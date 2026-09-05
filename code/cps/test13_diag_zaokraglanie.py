#!/usr/bin/env python3
"""
TEST 13 — diagnoza rozbieznosci znaku pomiaru A (D-060 vs. niezalezna replikacja autora).

Autor zglosil: jego wlasna symulacja (skala Weibulla lam=3, zaokraglenie
"do pelnych lat z podloga jeden" tj. floor(T) z minimum 1, 295 obserwacji, 200 replik,
3 starty optymalizatora) dala b_mean=+0.035 (SD=0.026, 89.5% dodatnich) - znak PRZECIWNY
do mojego pomiaru A z test13_etap1.py (b_mean=-0.1252, uzywajacego mechanizmu fazowego
discretize_gap/D-058 i skali skalibrowanej lam~10).

Autor: "Dwa podejrzenia... Zglos roznice, nie dopasowuj."

Ten skrypt: eksperyment 2x2 (metoda dyskretyzacji x skala), na TYCH SAMYCH 294 realnych
admin_max, k_true=0.7096, plus krzyzowa kontrola przeciwko juz ustalonemu (D-056) pomiarowi
odchylenia zaokraglenia na realnej strukturze median-2 (S7/Test12), zeby ustalic, ktora
metoda dyskretyzacji jest zgodna z rzeczywistymi danymi UCDP.
"""
from __future__ import annotations
import json
import numpy as np

import test12_power as p12
import test13_trend as tr
import test13_etap1 as e1

SEED = 42
N_REPS_22 = 200
X0_LIST = [(-0.3, 0.0, 2.0), (-0.3, 0.3, 2.0), (-0.3, -0.3, 2.0)]


def discretize_floor_min1(T):
    """Metoda autora: zaokraglenie w dol, minimum 1 rok. Brak modelowania fazy w roku."""
    return max(float(np.floor(T)), 1.0)


def simulate_one_rep_A_method(k_true, lam_true, admin_max, rng, method):
    disc = p12.discretize_gap if method == "phi" else (lambda T, r: discretize_floor_min1(T))
    t_out = np.empty(len(admin_max))
    ev_out = np.empty(len(admin_max), dtype=int)
    for i, amax in enumerate(admin_max):
        T = lam_true * rng.exponential(1.0) ** (1.0 / k_true)
        gap_obs = disc(T, rng)
        if gap_obs <= amax:
            t_out[i] = gap_obs; ev_out[i] = 1
        else:
            t_out[i] = max(amax, 0.0); ev_out[i] = 0
    return t_out, ev_out


def run_2x2(n_reps=N_REPS_22, seed=SEED):
    starts, admin_max, n_total, n_full_real = e1.load_real_starts_and_admin_max()
    year_c = starts - 1985.0
    k_true = 0.7096
    out = {}
    for method in ("phi", "floor_min1"):
        for lam_true in (3.0, 10.0):
            rng = np.random.default_rng(seed)
            bs = np.empty(n_reps)
            fracs = np.empty(n_reps)
            for i in range(n_reps):
                t_sim, ev_sim = simulate_one_rep_A_method(k_true, lam_true, admin_max, rng, method)
                fracs[i] = ev_sim.mean()
                fit = tr.fit_trend(t_sim, ev_sim, year_c, x0_list=X0_LIST)
                bs[i] = fit["b"]
            key = f"method={method} lam={lam_true}"
            out[key] = dict(b_mean=float(bs.mean()), b_sd=float(bs.std(ddof=1)),
                            frac_pos=float((bs > 0).mean()), frac_full=float(fracs.mean()))
            print(f"{key}: b_mean={out[key]['b_mean']:.4f} sd={out[key]['b_sd']:.4f} "
                 f"frac_pos={out[key]['frac_pos']:.3f} frac_full={out[key]['frac_full']:.3f}")
    return out


def simulate_rounded_floor_min1(k, lam, windows, rng):
    """Odpowiednik test12_power.simulate_rounded_dataset, z discretize_floor_min1 zamiast
    discretize_gap (fazowego) - do krzyzowej kontroli przeciwko juz ustalonemu D-056."""
    ts, ev, gid = [], [], []
    for g, Wlen in enumerate(windows):
        cum = 0.0
        while True:
            T = lam * rng.exponential(1.0) ** (1.0 / k)
            gap_obs = discretize_floor_min1(T)
            if cum + gap_obs <= Wlen:
                ts.append(gap_obs); ev.append(1); gid.append(g)
                cum += gap_obs
            else:
                cens_obs = max(0.0, np.floor(Wlen - cum))
                ts.append(cens_obs); ev.append(0); gid.append(g)
                break
    return np.array(ts, float), np.array(ev, int), np.array(gid)


def run_bias_crosscheck(seed=42, n_reps=300):
    """Dokladny odpowiednik test12_power.measure_rounding_bias (D-056: k_true=1.0,
    realna struktura okien median-2 z Testu 12/S7), z JEDYNA zmiana: discretize_floor_min1
    zamiast fazowego discretize_gap. Test, czy metoda autora odtwarza znak odchylenia juz
    ustalony na realnych danych UCDP (D-056: -0.0353), czy daje znak przeciwny."""
    import test6_weibull as w
    import test7_estimate as e
    windows, n_full, n_cens = p12.load_structure()
    lam_true = sum(windows) / n_full
    k_true = 1.0
    rng = np.random.default_rng(seed)
    ks_rounded = np.empty(n_reps)
    ks_continuous = np.empty(n_reps)
    for i in range(n_reps):
        t_r, ev_r, _ = simulate_rounded_floor_min1(k_true, lam_true, windows, rng)
        ks_rounded[i] = w.fit_pooled(t_r, ev_r)["k"]
        t_c, ev_c, _ = e.simulate_dataset_test7(k_true, lam_true, 0.0, windows, rng)
        ks_continuous[i] = w.fit_pooled(t_c, ev_c)["k"]
    out = dict(k_true=k_true, lam_true=lam_true, n_reps=n_reps,
               k_hat_rounded_mean=float(ks_rounded.mean()),
               k_hat_continuous_mean=float(ks_continuous.mean()),
               obciazenie_mean=float(ks_rounded.mean() - ks_continuous.mean()))
    print(f"[floor_min1 crosscheck] rounded={out['k_hat_rounded_mean']:.4f} "
         f"continuous={out['k_hat_continuous_mean']:.4f} obciazenie={out['obciazenie_mean']:+.4f} "
         f"(D-056 referencyjnie z phi: rounded=0.9672 continuous=1.0025 obciazenie=-0.0353)")
    return out


if __name__ == "__main__":
    res = run_2x2()
    res["D056_crosscheck_floor_min1"] = run_bias_crosscheck()
    with open("test13_diag_zaokraglanie_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
    print("zapisano test13_diag_zaokraglanie_wyniki.json")
