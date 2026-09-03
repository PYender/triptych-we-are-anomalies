#!/usr/bin/env python3
"""
TEST 11 — estymator: uogólniony rozkład gamma (parametryzacja Stacy'ego, scipy.stats.gengamma)
przeciw Weibullowi (test6_weibull.py, reużyty bez zmian dla modelu zagnieżdżonego).

Rodzina Stacy'ego (a>0, c!=0, scale>0): przy a=1 REDUKUJE SIĘ DOKŁADNIE do Weibulla o
kształcie c (sprawdzone testem poprawności `test_reduces_to_weibull`) — to jest ta sama
rodzina rozkładów co parametryzacja Prentice'a (mu,sigma,Q), tylko innym układem
współrzędnych; nota o wyborze w `TEST11_PROTOCOL_ksztalt_hazardu.md`.

Hazard: h(t) = exp(logpdf(t) - logsf(t)) — liczony na siatce w obserwowanym zakresie,
klasyfikowany jako rosnący / malejący / maksimum wewnętrzne / minimum wewnętrzne.
"""
from __future__ import annotations
import numpy as np
from scipy.stats import gengamma
from scipy.optimize import minimize

import test6_weibull as w

RNG_SEED = w.RNG_SEED
C_FLOOR = 1e-4          # unikniecie c=0 (osobliwosc, granica log-normalna poza rodzina Stacy'ego)


LOG_A_BOUNDS = (-3.0, 3.0)      # a w (0,05, 20) -- generalized gamma ma znana slaba
                                 # identyfikowalnosc (grzbiet w wiarygodnosci); bez tych granic
                                 # optymalizator znajduje zdegenerowane rozwiazania (a rzedu 10+,
                                 # scale rzedu milionow) dajace POZORNY garb na czystych danych
                                 # Weibulla -- zlapane testem poprawnosci `test_reduces_to_weibull`
LOG_SCALE_BOUNDS = (-3.0, 6.0)   # scale w (0,05, 400) -- rzedu skali realnych odstepow (lata)
C_BOUNDS = (-5.0, 5.0)


def negloglik_gengamma_pooled(params, t, event):
    log_a, log_scale, c = params
    if not (LOG_A_BOUNDS[0] <= log_a <= LOG_A_BOUNDS[1] and
            LOG_SCALE_BOUNDS[0] <= log_scale <= LOG_SCALE_BOUNDS[1] and
            C_BOUNDS[0] <= c <= C_BOUNDS[1]):
        return 1e10                  # kara zamiast przepelnienia exp poza rozsadnym zakresem
    a = np.exp(log_a); scale = np.exp(log_scale)
    if abs(c) < C_FLOOR:
        c = C_FLOOR if c >= 0 else -C_FLOOR
    logpdf = gengamma.logpdf(t, a, c, scale=scale)
    logsf = gengamma.logsf(t, a, c, scale=scale)
    ll = np.where(event == 1, logpdf, logsf)
    if not np.all(np.isfinite(ll)):
        return 1e10
    return -float(np.sum(ll))


DEFAULT_X0_GENGAMMA = [
    (0.0, 3.0, 1.0),      # a=1 (Weibull), c=1 -- start bliski zagnieżdżonemu modelowi
    (0.0, 3.0, -1.0),
    (np.log(0.3), 2.0, -0.8),     # region maksimum wewnetrznego (mala a, ujemne c)
]


def fit_gengamma_pooled(t, event, x0_list=None, maxiter=1500):
    if x0_list is None:
        x0_list = DEFAULT_X0_GENGAMMA
    results = [minimize(negloglik_gengamma_pooled, x0=np.array(x0, dtype=float), args=(t, event),
                        method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=maxiter))
              for x0 in x0_list]
    best = min(results, key=lambda r: r.fun)
    log_a, log_scale, c = best.x
    a = float(np.exp(log_a)); scale = float(np.exp(log_scale))
    a_by_start = [float(np.exp(r.x[0])) for r in results]
    converged_same = bool((max(a_by_start) - min(a_by_start)) < 1e-2 * max(1.0, abs(np.mean(a_by_start))))
    return dict(a=a, scale=scale, c=float(c), loglik=-float(best.fun),
               log_a=float(log_a), log_scale=float(log_scale),
               res=best, n_starts=len(x0_list), converged_same=converged_same)


def hazard_grid(fit, t_grid):
    a, c, scale = fit["a"], fit["c"], fit["scale"]
    logpdf = gengamma.logpdf(t_grid, a, c, scale=scale)
    logsf = gengamma.logsf(t_grid, a, c, scale=scale)
    return np.exp(logpdf - logsf)


def classify_shape(fit, t_obs, n_grid=400, tol_rel=1e-3):
    """Klasyfikuje ksztalt hazardu na siatce w zakresie OBSERWOWANYCH odstepow (SS3 protokolu).
    Zwraca (ksztalt, punkt_zwrotny_albo_None, na_brzegu_zakresu)."""
    t_grid = np.linspace(max(t_obs.min(), 1e-3), t_obs.max(), n_grid)
    h = hazard_grid(fit, t_grid)
    if not np.all(np.isfinite(h)):
        return "niepoliczalny", None, None
    tol = tol_rel * (h.max() - h.min() + 1e-12)
    dh = np.diff(h)
    rising = dh > tol
    falling = dh < -tol
    if not falling.any():
        return "rosnacy", None, False
    if not rising.any():
        return "malejacy", None, False
    idx_max = int(np.argmax(h)); idx_min = int(np.argmin(h))
    on_boundary_max = idx_max <= 1 or idx_max >= n_grid - 2
    on_boundary_min = idx_min <= 1 or idx_min >= n_grid - 2
    # maksimum wewnetrzne: rosnie potem maleje
    if h[idx_max] > h[0] + tol and h[idx_max] > h[-1] + tol and not on_boundary_max:
        return "maksimum_wewnetrzne", float(t_grid[idx_max]), False
    if h[idx_min] < h[0] - tol and h[idx_min] < h[-1] - tol and not on_boundary_min:
        return "minimum_wewnetrzne", float(t_grid[idx_min]), False
    return "niemonotoniczny_brzegowy", float(t_grid[idx_max if h[idx_max] >= h[idx_min] else idx_min]), True


def simulate_weibull_min_tc(k, lam, windows, rng):
    """Surogat Weibulla, mechanizm min(T,C) (D-031) - identyczny mechanizm co
    `test7_estimate.simulate_dataset_test7`, tutaj bez kruchosci (theta=0 zawsze, model
    zerowy tego testu to CZYSTY Weibull, SS3 protokolu: 'surogaty generowane z Weibulla')."""
    ts, ev, gid = [], [], []
    for g, Wlen in enumerate(windows):
        cum = 0.0
        while True:
            T = lam * rng.exponential(1.0) ** (1.0 / k)
            if cum + T <= Wlen:
                ts.append(T); ev.append(1); gid.append(g)
                cum += T
            else:
                ts.append(Wlen - cum); ev.append(0); gid.append(g)
                break
    return np.array(ts, float), np.array(ev, int), np.array(gid)


def lr_stat(t, event):
    fit_w = w.fit_pooled(t, event)
    fit_g = fit_gengamma_pooled(t, event)
    lr = 2.0 * (fit_g["loglik"] - fit_w["loglik"])
    return max(lr, 0.0), fit_w, fit_g


def test_reduces_to_weibull(n_reps=5, seed=999):
    """Test poprawnosci: przy danych symulowanych z CZYSTEGO Weibulla, dopasowanie gengamma
    powinno dawac a blisko 1 i c blisko prawdziwego ksztaltu Weibulla, z loglik >= Weibulla
    (model zagniezdzony, wiecej parametrow)."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n_reps):
        windows = [50.0] * 13
        t, event, _ = simulate_weibull_min_tc(0.85, 15.0, windows, rng)
        fit_w = w.fit_pooled(t, event)
        fit_g = fit_gengamma_pooled(t, event)
        out.append(dict(a=fit_g["a"], c=fit_g["c"], k_weibull=fit_w["k"],
                        loglik_gap=fit_g["loglik"] - fit_w["loglik"]))
    return out
