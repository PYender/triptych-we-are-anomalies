#!/usr/bin/env python3
"""
TEST 13 - SS8 protokolu (Etap 2): symulacja mocy i kalibracji, PRZED zamrozeniem.
Trzy pomiary na realnej strukturze (min(T,C), discretize_gap):

1. Odchylenie oszacowania b pod prawdziwym brakiem trendu - JUZ WYKONANE w D-063
   (test13_n3.run_n3): srodek -0,1030, SD 0,0425.

2. Udzial falszywych odrzucen (NAJWAZNIEJSZY, brakujacy): jak czesto wartosc p, liczona
   dwustronnie wzgledem srodka rozkladu surogatow, wychodzi ponizej 0,05, gdy trendu
   naprawde nie ma. Konstrukcja: N niezaleznych ciagnien pod stalym parametrem; kazde po
   kolei traktowane jak "obserwacja", porownywane z ROZKLADEM ZEROWYM ZBUDOWANYM Z
   POZOSTALYCH N-1 ciagnien (nie z samym soba - zachowuje wymiennosc/exchangeability,
   klasyczny argument teorii testow Monte Carlo). Srodek liczony TEZ z pozostalych N-1
   (nie wlaczajac "obserwacji"), zeby uniknac obciazenia. To unika drogiej zagniezdzonej
   petli B_outer x B_inner - jest matematycznie rownowazne (do poprawki O(1/N) na srednia
   bez jednego elementu), bo rozklad zerowy jest ten sam niezaleznie od tego, ktore
   ciagniecie akurat udaje "obserwacje".

3. Moc przy trzech wielkosciach trendu (w tym ~0,2 na cztery dekady, tj. b~0,05/dekade -
   tyle, ile sugeruje S3 Testu 12). Test uzywa TEGO SAMEGO stalego rozkladu zerowego z
   pomiaru 1/2 (nie generuje nowego zerowego per replika mocy - tak samo jak w Testach
   10/11). Niska moc NIE jest powodem niepodejmowania decyzji o biegu - wynikiem
   pierwszorzedowym jest wielkosc efektu z przedzialem, nie proste orzeczenie moc/brak.
"""
from __future__ import annotations
import json
import time
import numpy as np

import test12_power as p12
import test13_trend as tr
import test13_etap1 as e1
import test13_n3 as n3

SEED_POMIAR2 = 20260823
SEED_POMIAR3 = 20260824
N_POMIAR2 = 2000
M_POMIAR3 = 500
B_TRUE_LIST = [0.025, 0.05, 0.10]  # propozycja - srodkowa (~0,2/4dekady) wskazana przez autora,
                                     # skrajne dobrane jako polowa/podwojenie do rozpiecia skali;
                                     # FLAGOWANE jako moj wybor, nie autora decyzja


def pomiar2_falszywe_odrzucenia(N=N_POMIAR2, seed=SEED_POMIAR2):
    fit0 = n3.fit_no_trend()
    k_hat, lam_hat = fit0["k_hat"], fit0["lam_hat"]
    starts, admin_max, n_total, n_full_real = e1.load_real_starts_and_admin_max()
    year_c = starts - 1985.0

    rng = np.random.default_rng(seed)
    b = np.empty(N)
    for i in range(N):
        t_sim, ev_sim = n3.simulate_n3_once(k_hat, lam_hat, admin_max, rng)
        fit = tr.fit_trend(t_sim, ev_sim, year_c)
        b[i] = fit["b"]

    total = b.sum()
    p_vals = np.empty(N)
    for i in range(N):
        center_i = (total - b[i]) / (N - 1)
        dist_i = abs(b[i] - center_i)
        others = np.delete(b, i)
        p_vals[i] = (1 + int(np.sum(np.abs(others - center_i) >= dist_i))) / N

    frac_reject = float(np.mean(p_vals < 0.05))
    return dict(N=N, seed=seed, k_hat_no_trend=k_hat, lam_hat_no_trend=lam_hat,
               b_mean=float(b.mean()), b_sd=float(b.std(ddof=1)),
               frac_falszywych_odrzucen=frac_reject,
               nominalne=0.05), b


def simulate_power_once(k_hat, lam_hat, admin_max, year_c, b_true, rng):
    a = np.log(k_hat)
    t_out = np.empty(len(admin_max))
    ev_out = np.empty(len(admin_max), dtype=int)
    for i, (amax, yc) in enumerate(zip(admin_max, year_c)):
        k_i = np.exp(a + b_true * yc / 10.0)
        T = lam_hat * rng.exponential(1.0) ** (1.0 / k_i)
        gap_obs = p12.discretize_gap(T, rng)
        if gap_obs <= amax:
            t_out[i] = gap_obs; ev_out[i] = 1
        else:
            t_out[i] = max(amax, 0.0); ev_out[i] = 0
    return t_out, ev_out


def pomiar3_moc(b_null_ref, M=M_POMIAR3, seed=SEED_POMIAR3, b_true_list=B_TRUE_LIST):
    fit0 = n3.fit_no_trend()
    k_hat, lam_hat = fit0["k_hat"], fit0["lam_hat"]
    starts, admin_max, n_total, n_full_real = e1.load_real_starts_and_admin_max()
    year_c = starts - 1985.0
    center_ref = float(b_null_ref.mean())
    N_ref = len(b_null_ref)

    out = {}
    for b_true in b_true_list:
        rng = np.random.default_rng(seed + int(round(b_true * 10000)))
        bs = np.empty(M)
        ps = np.empty(M)
        for i in range(M):
            t_sim, ev_sim = simulate_power_once(k_hat, lam_hat, admin_max, year_c, b_true, rng)
            fit = tr.fit_trend(t_sim, ev_sim, year_c)
            bs[i] = fit["b"]
            dist = abs(bs[i] - center_ref)
            ps[i] = (1 + int(np.sum(np.abs(b_null_ref - center_ref) >= dist))) / (N_ref + 1)
        out[f"b_true={b_true}"] = dict(
            b_true=b_true, M=M, N_ref=N_ref,
            b_hat_mean=float(bs.mean()), b_hat_median=float(np.median(bs)),
            b_hat_sd=float(bs.std(ddof=1)),
            b_hat_95CI=(float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))),
            moc=float(np.mean(ps < 0.05)))
        print(f"[pomiar3] b_true={b_true}: b_hat_mean={out[f'b_true={b_true}']['b_hat_mean']:.4f} "
             f"moc={out[f'b_true={b_true}']['moc']:.3f}")
    return out


def main():
    t0 = time.time()
    out = {}
    print("=== pomiar 2: falszywe odrzucenia ===")
    p2, b_null_pool = pomiar2_falszywe_odrzucenia()
    out["pomiar2_falszywe_odrzucenia"] = p2
    print(f"[2] frac_falszywych_odrzucen={p2['frac_falszywych_odrzucen']:.4f} "
         f"(nominalne 0,05) ({time.time()-t0:.0f}s)")

    print("=== pomiar 3: moc przy trzech wielkosciach trendu ===")
    out["pomiar3_moc"] = pomiar3_moc(b_null_pool)

    with open("test13_etap2_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print(f"zapisano test13_etap2_wyniki.json ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
