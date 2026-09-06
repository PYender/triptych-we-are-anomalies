#!/usr/bin/env python3
"""
TEST 13 - dodatkowy pomiar wyjasnienia B z SS7 (D-068), zamowiony PO wyniku decydujacym
(D-067) jako pomiar zapowiedziany PRZED biegiem, nie jako zmiana protokolu/reguly.

Wyjasnienie B (gestosc kodowania) zostalo w SS7/D-060 zmierzone jako REALNE, ale NIE jako
niewystarczajace. Mechanizm mozliwego artefaktu: obciazenie zaokraglenia (D-058/D-061)
zalezy od mediany odstepu, a mediana spada z ok. 15 lat (lata 50.) do ok. 1 roku (dzis).
Model zerowy z D-062/D-063/frozen SS5 uzywa JEDNEJ wspolnej skali dopasowanej do calosci
- nie odtwarza tej zmiany w czasie.

Ten skrypt buduje ALTERNATYWNY model zerowy: skala ZALEZNA OD ROKU (dopasowana do danych),
parametr ksztaltu STALY (=k_hat z dopasowania bez trendu, jak w SS5) - i sprawdza, czy
surogaty z TAKIEGO modelu zerowego (bez zadnego prawdziwego trendu w k) daja rozklad b_sur
o srodku bliskim -0,10 (wyjasnienie B odpada) czy bliskim +0,09 (surowe b_obs, wyjasnienie
B tlumaczy caly wynik).

log lambda(rok) = c + d*(rok-1985)/10, oba (c,d) dopasowane MLE do rzeczywistych danych,
k stale = k_hat_no_trend (test13_n3.fit_no_trend). NIE jest to zmiana SS5 zamrozonego
protokolu - to dodatkowy pomiar diagnostyczny z SS7, wykonany post-hoc na wyrazne zadanie
autora, zadeklarowany PRZED wykonaniem (odczyt zapowiedziany w promptcie autora).
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize

import test12_power as p12
import test13_trend as tr
import test13_n3 as n3
import test13_run as run13

SEED = tr.RNG_SEED  # to samo ziarno, jak zazadal autor
B_NULL = 2000


def negloglik_scale_trend(params, t, event, year_c, k_fixed):
    c, d = params
    lam = np.exp(c + d * year_c / 10.0)
    t_safe = np.where(t > 0, t, 1e-9)
    logh = np.log(k_fixed / lam) + (k_fixed - 1.0) * np.log(t_safe / lam)
    H = (t / lam) ** k_fixed
    ll = np.where(event == 1, logh, 0.0) - H
    if not np.all(np.isfinite(ll)):
        return 1e10
    return -float(np.sum(ll))


DEFAULT_X0_SCALE = [(2.0, 0.0), (2.0, -0.3), (2.0, 0.3), (1.5, -0.5)]


def fit_scale_trend(t, event, year_c, k_fixed, x0_list=None):
    if x0_list is None:
        x0_list = DEFAULT_X0_SCALE
    results = [minimize(negloglik_scale_trend, x0=np.array(x0, dtype=float),
                        args=(t, event, year_c, k_fixed), method="Nelder-Mead",
                        options=dict(xatol=1e-9, fatol=1e-11, maxiter=10000))
              for x0 in x0_list]
    best = min(results, key=lambda r: r.fun)
    c, d = best.x
    return dict(c=float(c), d=float(d), loglik=-float(best.fun))


def simulate_scale_null_once(k_fixed, c, d, admin_max, year_c, rng):
    t_out = np.empty(len(admin_max))
    ev_out = np.empty(len(admin_max), dtype=int)
    for i, (amax, yc) in enumerate(zip(admin_max, year_c)):
        lam_i = np.exp(c + d * yc / 10.0)
        T = lam_i * rng.exponential(1.0) ** (1.0 / k_fixed)
        gap_obs = p12.discretize_gap(T, rng)
        if gap_obs <= amax:
            t_out[i] = gap_obs; ev_out[i] = 1
        else:
            t_out[i] = max(amax, 0.0); ev_out[i] = 0
    return t_out, ev_out


def main():
    t, event, year_c, diads = run13.load_real_decisive_data()
    starts, admin_max, n_total, n_full_real = __import__("test13_etap1").load_real_starts_and_admin_max()

    fit0 = n3.fit_no_trend()
    k_fixed = fit0["k_hat"]

    fit_cd = fit_scale_trend(t, event, year_c, k_fixed)
    c_hat, d_hat = fit_cd["c"], fit_cd["d"]
    print(f"k_fixed={k_fixed:.6f} c_hat={c_hat:.6f} d_hat={d_hat:.6f} loglik={fit_cd['loglik']:.4f}")
    print(f"lambda(1950)={np.exp(c_hat+d_hat*(1950-1985)/10):.4f} "
         f"lambda(1985)={np.exp(c_hat):.4f} lambda(2020)={np.exp(c_hat+d_hat*(2020-1985)/10):.4f}")

    rng = np.random.default_rng(SEED)
    b_sur = np.empty(B_NULL)
    for i in range(B_NULL):
        t_sim, ev_sim = simulate_scale_null_once(k_fixed, c_hat, d_hat, admin_max, year_c, rng)
        fit = tr.fit_trend(t_sim, ev_sim, year_c)
        b_sur[i] = fit["b"]

    out = dict(k_fixed=k_fixed, c_hat=c_hat, d_hat=d_hat, B=B_NULL, seed=SEED,
               b_sur_mean=float(b_sur.mean()), b_sur_median=float(np.median(b_sur)),
               b_sur_sd=float(b_sur.std(ddof=1)),
               b_sur_95CI=(float(np.percentile(b_sur, 2.5)), float(np.percentile(b_sur, 97.5))))
    print(out)
    import json
    with open("test13_b_check_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test13_b_check_wyniki.json")


if __name__ == "__main__":
    main()
