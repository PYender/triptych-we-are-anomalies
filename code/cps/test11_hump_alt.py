#!/usr/bin/env python3
"""
TEST 11 — generator alternatywy "garb" o REALISTYCZNYM ogonie.

Bezpośrednie próbkowanie z rodziny Stacy'ego przy c<0 (region dający wewnętrzne maksimum w
moim przeglądzie parametrów przy zamrożeniu protokołu) okazało się mieć KATASTROFALNIE ciężki
ogon (mediana próbek rzędu 10^2-10^5 lat, mimo hazardu wyglądającego rozsądnie na siatce
0-55 lat) — c ujemne w tej parametryzacji odwraca rolę ogona i daje rozkład bez praktycznie
skończonych momentów. Sprawdzone bezpośrednio (`gengamma.rvs`), NIE nadaje się do symulacji
realistycznych danych.

Zamiast tego: hazard skonstruowany jako JĄDRO GAMMA (nie rozkład gamma, tylko kształt
funkcji), h(t) = A * t^(kappa-1) * exp(-t/theta), kappa>1 daje POJEDYNCZY GARB przy
t=(kappa-1)*theta i OGON WYKŁADNICZY (lekki, dobrze zachowany — theta kontroluje tempo
zaniku). Próbkowanie przez odwrócenie skumulowanego hazardu na siatce (metoda standardowa
dla procesów niejednorodnych Poissona), NIE przez rodzinę uogólnionej gammy — alternatywa
NIE jest członkiem rodziny testowanej (uogólniona gamma kontra Weibull), co jest WŁAŚCIWE dla
analizy mocy: sprawdzamy, czy test wykrywa REALISTYCZNY garb, nie tylko garb dokładnie tej
postaci matematycznej, którą test dopasowuje.
"""
from __future__ import annotations
import numpy as np


def gamma_kernel_hazard(t, A, kappa, theta):
    return A * np.power(t, kappa - 1.0) * np.exp(-t / theta)


def build_cumhazard_grid(A, kappa, theta, t_max, n=20000):
    tg = np.linspace(1e-6, t_max, n)
    hg = gamma_kernel_hazard(tg, A, kappa, theta)
    Hg = np.concatenate([[0.0], np.cumsum((hg[1:] + hg[:-1]) / 2.0 * np.diff(tg))])
    return tg, Hg


def calibrate_A_by_event_rate(kappa, theta, windows, target_n_full, t_max, n_grid=20000,
                              n_iter=10, seed=0):
    """Kalibracja BEZPOSREDNIA na rzeczywistym mechanizmie wyscigu (nie na posredniej probce
    nieucietej) - dostosowuje A tak, zeby zrealizowana liczba zdarzen pelnych zblizala sie do
    target_n_full (rzeczywiste S7: 110 z 123 wierszy, ~89%). Wyszukiwanie geometryczne."""
    A = 0.005
    for i in range(n_iter):
        rng = np.random.default_rng(seed + i)
        t, ev, gid = simulate_gamma_kernel_hump_min_tc(A, kappa, theta, windows, rng, t_max=t_max, n_grid=n_grid)
        n_full = int(ev.sum())
        if n_full == 0:
            A *= 3.0
            continue
        ratio = target_n_full / n_full
        A *= np.clip(ratio, 0.3, 3.0)
    return A


def simulate_gamma_kernel_hump_min_tc(A, kappa, theta, windows, rng, t_max=None, n_grid=20000):
    if t_max is None:
        t_max = max(windows) * 3.0
    tg, Hg = build_cumhazard_grid(A, kappa, theta, t_max, n_grid)
    ts, ev, gid = [], [], []
    for grp, Wlen in enumerate(windows):
        cum = 0.0
        while True:
            E = rng.exponential(1.0)
            T = float(np.interp(E, Hg, tg, right=t_max * 10))
            if cum + T <= Wlen:
                ts.append(T); ev.append(1); gid.append(grp)
                cum += T
            else:
                ts.append(Wlen - cum); ev.append(0); gid.append(grp)
                break
    return np.array(ts, float), np.array(ev, int), np.array(gid)
