#!/usr/bin/env python3
"""
TEST 13 — estymator: parametr ksztaltu Weibulla jako funkcja roku (SS4 protokolu).

log k(rok) = a + b*(rok-1985)/10, skala `lam` wspolna (nie zalezy od roku).
Wielkosc orzekajaca: `b` (zmiana log k na dekade).
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2

RNG_SEED = 20260823


def negloglik_trend(params, t, event, year_c):
    a, b, log_lam = params
    lam = np.exp(log_lam)
    k = np.exp(a + b * year_c / 10.0)
    t_safe = np.where(t > 0, t, 1e-9)
    logh = np.log(k / lam) + (k - 1.0) * np.log(t_safe / lam)
    H = (t / lam) ** k
    ll = np.where(event == 1, logh, 0.0) - H
    if not np.all(np.isfinite(ll)):
        return 1e10
    return -float(np.sum(ll))


DEFAULT_X0_TREND = [(-0.3, 0.0, 2.0), (-0.3, 0.3, 2.0), (-0.3, -0.3, 2.0), (-0.3, 0.5, 2.0)]


def fit_trend(t, event, year_c, x0_list=None):
    if x0_list is None:
        x0_list = DEFAULT_X0_TREND
    results = [minimize(negloglik_trend, x0=np.array(x0, dtype=float), args=(t, event, year_c),
                        method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-11, maxiter=10000))
              for x0 in x0_list]
    best = min(results, key=lambda r: r.fun)
    a, b, log_lam = best.x
    b_by_start = [float(r.x[1]) for r in results]
    converged_same = bool((max(b_by_start) - min(b_by_start)) < 1e-2 * max(1.0, abs(np.mean(b_by_start))))
    return dict(a=float(a), b=float(b), lam=float(np.exp(log_lam)), loglik=-float(best.fun),
               log_lam=float(log_lam), res=best, converged_same=converged_same, n_starts=len(x0_list))


def implied_k(fit, year):
    return float(np.exp(fit["a"] + fit["b"] * (year - 1985) / 10.0))


def profile_ci_b(t, event, year_c, b_hat, a_hat, log_lam_hat, loglik_max, level=0.95, n_grid=61, span_mult=6.0):
    thresh = chi2.ppf(level, df=1)
    span = span_mult * (abs(b_hat) if abs(b_hat) > 1e-3 else 0.3)
    grid = np.linspace(b_hat - span, b_hat + span, n_grid)
    lr = np.empty(n_grid)
    rest = np.array([a_hat, log_lam_hat])
    for i, bj in enumerate(grid):
        def obj(rest_free, bj=bj):
            full = np.array([rest_free[0], bj, rest_free[1]])
            return negloglik_trend(full, t, event, year_c)
        res = minimize(obj, x0=rest, method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-11, maxiter=4000))
        rest = res.x
        lr[i] = 2.0 * (loglik_max - (-res.fun))
    idx_hat = int(np.argmin(np.abs(grid - b_hat)))

    def interp_crossing(direction):
        i = idx_hat
        while 0 <= i + direction < n_grid:
            if lr[i + direction] >= thresh:
                x0, x1 = grid[i], grid[i + direction]
                y0, y1 = lr[i], lr[i + direction]
                if y1 == y0:
                    return x1, True
                frac = (thresh - y0) / (y1 - y0)
                return x0 + frac * (x1 - x0), True
            i += direction
        return (grid[0] if direction < 0 else grid[-1]), False

    lo, lo_b = interp_crossing(-1)
    hi, hi_b = interp_crossing(+1)
    return dict(lo=lo, hi=hi, lo_bounded=lo_b, hi_bounded=hi_b, grid=grid, lr=lr)


def bootstrap_ci_b(t, event, year_c, diad, B=2000, seed=RNG_SEED, level=0.95, x0=(-0.3, 0.0, 2.0)):
    groups = np.unique(diad)
    idx_by_group = {g: np.where(diad == g)[0] for g in groups}
    rng = np.random.default_rng(seed)
    bs = np.empty(B)
    for bi in range(B):
        sampled = rng.choice(groups, size=len(groups), replace=True)
        idx = np.concatenate([idx_by_group[g] for g in sampled])
        fit = fit_trend(t[idx], event[idx], year_c[idx], x0_list=[x0])
        bs[bi] = fit["b"]
    lo, hi = np.percentile(bs, [(1 - level) / 2 * 100, (1 + level) / 2 * 100])
    return float(lo), float(hi), bs
