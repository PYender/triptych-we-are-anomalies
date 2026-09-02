#!/usr/bin/env python3
"""
TEST 7 — Etap C: estymator Weibull AFT + kruchość gamma, ze zmiennymi objaśniającymi
(protokół §7: "to samo [Weibull z kruchością gamma] + zmienne objaśniające §6 (AFT)").

Rozszerza test6_weibull.py (negloglik_pooled/negloglik_frailty) o kowarianty na skali AFT:
    λ_i = λ0 · exp(-x_i·β)         (standardowy link AFT-Weibull)
    H_i(t) = (t/λ0)^k · exp(k·x_i·β)
    log h_i(t) = log(k/λ0) + (k-1)·log(t/λ0) + k·x_i·β

Przy X pustym (brak kowariantów) redukuje się dokładnie do negloglik_pooled/negloglik_frailty
z test6_weibull.py — sprawdzone testem poprawności (`test_reduces_to_no_cov`).

NIE PISANE od nowa dla samej idei modelu (Weibull+kruchość) — rozszerzone o warstwę
kowariantów, bo protokół wymaga AFT dla P2, którego test6_weibull.py nie miał (P1 Testu 6
nie ma zmiennych objaśniających).
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln

import test6_weibull as w

RNG_SEED = w.RNG_SEED


def negloglik_pooled_cov(params, t, event, X):
    p = X.shape[1]
    logk, loglam0 = params[0], params[1]
    beta = params[2:2 + p]
    k, lam0 = np.exp(logk), np.exp(loglam0)
    eta = X @ beta
    H = (t / lam0) ** k * np.exp(k * eta)
    t_safe = np.where(t > 0, t, 1.0)
    logh = np.log(k / lam0) + (k - 1.0) * np.log(t_safe / lam0) + k * eta
    ll = np.where(event == 1, logh, 0.0) - H       # log f = log h - H dla pelnych; log S = -H zawsze
    return -float(np.sum(ll))


def negloglik_frailty_cov(params, t, event, group_idx, n_groups, X):
    p = X.shape[1]
    logk, loglam0 = params[0], params[1]
    beta = params[2:2 + p]
    logtheta = params[2 + p]
    k, lam0, theta = np.exp(logk), np.exp(loglam0), max(np.exp(logtheta), 1e-10)
    eta = X @ beta
    H = (t / lam0) ** k * np.exp(k * eta)
    t_safe = np.where(t > 0, t, 1.0)
    logh = np.log(k / lam0) + (k - 1.0) * np.log(t_safe / lam0) + k * eta
    ev = event == 1
    D = np.bincount(group_idx, weights=ev.astype(float), minlength=n_groups)
    Hi = np.bincount(group_idx, weights=H, minlength=n_groups)
    sum_logh = np.bincount(group_idx[ev], weights=logh[ev], minlength=n_groups)
    total = np.sum(sum_logh + D * np.log(theta) + gammaln(1.0 / theta + D) - gammaln(1.0 / theta)
                  - (1.0 / theta + D) * np.log1p(theta * Hi))
    return -float(total)


def _multistart(negloglik, x0_list, args, maxiter=15000):
    results = [minimize(negloglik, x0=np.array(x0, dtype=float), args=args,
                        method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-11, maxiter=maxiter))
              for x0 in x0_list]
    best = min(results, key=lambda r: r.fun)
    k_by_start = [float(np.exp(r.x[0])) for r in results]
    converged_same = bool((max(k_by_start) - min(k_by_start)) < 1e-3 * max(1.0, abs(np.mean(k_by_start))))
    return best, results, converged_same


def fit_pooled_cov(t, event, X, beta0=None):
    p = X.shape[1]
    beta0 = beta0 if beta0 is not None else [0.0] * p
    x0_list = [(0.0, 3.0, *beta0), (0.5, 2.0, *beta0)]
    best, results, converged_same = _multistart(negloglik_pooled_cov, x0_list, (t, event, X))
    logk, loglam0 = best.x[0], best.x[1]
    beta = best.x[2:2 + p]
    return dict(k=float(np.exp(logk)), lam0=float(np.exp(loglam0)), beta=beta.tolist(),
               loglik=-float(best.fun), logk=float(logk), loglam0=float(loglam0),
               res=best, converged_same=converged_same, n_starts=len(x0_list))


def fit_frailty_cov(t, event, diad, X, beta0=None, x0_theta=(-4.0, -1.0, 0.0, 0.5)):
    p = X.shape[1]
    beta0 = beta0 if beta0 is not None else [0.0] * p
    groups, group_idx = np.unique(diad, return_inverse=True)
    n_groups = len(groups)
    x0_list = [(0.0, 3.0, *beta0, lt) for lt in x0_theta]
    best, results, converged_same = _multistart(negloglik_frailty_cov, x0_list,
                                                (t, event, group_idx, n_groups, X))
    logk, loglam0 = best.x[0], best.x[1]
    beta = best.x[2:2 + p]
    logtheta = best.x[2 + p]
    theta_raw = float(np.exp(logtheta))
    theta = max(theta_raw, 1e-10)
    return dict(k=float(np.exp(logk)), lam0=float(np.exp(loglam0)), beta=beta.tolist(),
               theta=theta, theta_at_boundary=bool(theta_raw <= 1e-10),
               loglik=-float(best.fun), logk=float(logk), loglam0=float(loglam0),
               logtheta=float(np.log(theta)), res=best, converged_same=converged_same,
               n_starts=len(x0_list))


def profile_ci_beta(negloglik_full, args, beta_hat, j, rest0, loglik_max,
                    level=0.95, n_grid=61, half_width_mult=6.0):
    """Profil wiarygodności dla WSPOLCZYNNIKA beta[j] (nie k) — siatka wokol beta_hat[j],
    szerokosc dobrana adaptacyjnie (half_width_mult * przyblizony SE z krzywizny numerycznej,
    z fallbackiem gdy krzywizna nieokreslona)."""
    from scipy.stats import chi2
    thresh = chi2.ppf(level, df=1)
    # siatka wokol beta_hat, szerokosc = half_width_mult * max(|beta_hat|, 1) (brak zamkniętego
    # SE analitycznego dla tego modelu, wiec siatka zamiast przyblizenia krzywizna)
    span = half_width_mult * (abs(beta_hat) if abs(beta_hat) > 1e-6 else 1.0)
    grid = np.linspace(beta_hat - span, beta_hat + span, n_grid)
    lr = np.empty(n_grid)
    rest = np.array(rest0, dtype=float)
    for i, bj in enumerate(grid):
        def obj(rest_free, bj=bj):
            full = np.insert(rest_free, j, bj)
            return negloglik_full(full, *args)
        res = minimize(obj, x0=rest, method="Nelder-Mead",
                       options=dict(xatol=1e-9, fatol=1e-11, maxiter=3000))
        rest = res.x
        lr[i] = 2.0 * (loglik_max - (-res.fun))
    idx_hat = int(np.argmin(np.abs(grid - beta_hat)))
    lo = w._interp_crossing(grid, lr, thresh, idx_hat, -1)
    hi = w._interp_crossing(grid, lr, thresh, idx_hat, +1)
    return lo, hi, grid, lr


def bootstrap_ci_beta_frailty(t, event, diad, X, j, B=1000, seed=RNG_SEED, level=0.95, beta0=None):
    groups = np.unique(diad)
    idx_by_group = {g: np.where(diad == g)[0] for g in groups}
    rng = np.random.default_rng(seed)
    betas = np.empty(B)
    at_boundary = np.zeros(B, dtype=bool)
    for b in range(B):
        sampled = rng.choice(groups, size=len(groups), replace=True)
        idx_parts, lab_parts = [], []
        for rep, g in enumerate(sampled):
            ix = idx_by_group[g]
            idx_parts.append(ix)
            lab_parts.append(np.full(len(ix), f"{g}__{rep}"))
        idx = np.concatenate(idx_parts)
        lab = np.concatenate(lab_parts)
        fit = fit_frailty_cov(t[idx], event[idx], lab, X[idx], beta0=beta0)
        betas[b] = fit["beta"][j]
        at_boundary[b] = fit["theta_at_boundary"]
    lo, hi = np.percentile(betas, [(1 - level) / 2 * 100, (1 + level) / 2 * 100])
    return float(lo), float(hi), betas, float(at_boundary.mean())


def test_reduces_to_no_cov(n_reps=5, seed=999):
    """Sprawdza, ze przy X o kolumnach zerowych (beta bez znaczenia, eta=0 zawsze) model
    kowariantowy daje IDENTYCZNE k/lambda/theta co test6_weibull.negloglik_pooled/frailty."""
    rng = np.random.default_rng(seed)
    n_full_per_group = [3]*5 + [1]*3 + [0]*4
    out = []
    for _ in range(n_reps):
        t, event, diad = w.simulate_dataset(1.2, 20.0, 0.3, n_full_per_group, rng)
        X = np.zeros((len(t), 1))
        fit_p_plain = w.fit_pooled(t, event)
        fit_p_cov = fit_pooled_cov(t, event, X)
        fit_f_plain = w.fit_frailty(t, event, diad)
        fit_f_cov = fit_frailty_cov(t, event, diad, X)
        out.append(dict(
            pooled_k_diff=abs(fit_p_plain["k"] - fit_p_cov["k"]),
            frailty_k_diff=abs(fit_f_plain["k"] - fit_f_cov["k"]),
            frailty_theta_diff=abs(fit_f_plain["theta"] - fit_f_cov["theta"]),
        ))
    return out
