#!/usr/bin/env python3
"""
TEST 13 - model zerowy N3, wersja PO poprawce (errata autora, D-062/D-063).

Zastepuje permutacyjny N3 ze szkicu protokolu v0.1. Model zerowy: parametr ksztaltu
STALY (hipoteza zerowa "k jest stale w czasie", NIE "proces jest bez pamieci" - to
drugie juz rozstrzygniete w Tescie 12), symulowany na REALNYCH latach startu i REALNEJ
granicy administracyjnej (2023), z dyskretyzacja discretize_gap (D-058/D-061), a k^ i
lambda^ zasilajace symulacje pochodza z dopasowania BEZ trendu do tych samych realnych
danych (zwykly bootstrap parametryczny) - NIE z k=1 ani ze skali przyjetej z gory
(D-061 pokazal, ze obciazenie zalezy silnie od skali: -0,045 przy lambda=3 wobec
-0,125 przy lambda=10).

Wartosc p liczona WZGLEDEM ROZKLADU SUROGATOW (jego wlasnego srodka), nie wzgledem
zera - to jest sedno erraty: punktem odniesienia jest to, co sama procedura generuje
pod stalym parametrem, nie zero.
"""
from __future__ import annotations
import numpy as np

import test12_run as r12
import test12_power as p12
import test13_trend as tr
import test13_etap1 as e1

B_DEFAULT = 2000
TIE_FRAC_STOP = 0.01
SEED = tr.RNG_SEED  # prowizoryczne - do potwierdzenia przy zamrozeniu protokolu


def fit_no_trend(path="test12_intervals_prog3.csv", exclude_t0=True):
    """k^, lambda^ z dopasowania BEZ trendu (zwykly model Weibulla, bez podzialu na
    lata) do TYCH SAMYCH 294 obserwacji, ktore zasilaja decydujacy fit trendu."""
    import test6_weibull as w
    grouped = r12.load_grouped(path, exclude_t0=exclude_t0)
    _, t, event = r12.flatten(grouped)
    fit = w.fit_pooled(t, event)
    return dict(k_hat=fit["k"], lam_hat=fit["lam"], loglik=fit["loglik"], n=len(t))


def simulate_n3_once(k_true, lam_true, admin_max, rng):
    """Jeden surogat: symulacja pod stalym k_true na realnych admin_max, dyskretyzacja
    discretize_gap (D-061: jedyna metoda zgodna z realnym obciazeniem zmierzonym na
    danych UCDP)."""
    t_out = np.empty(len(admin_max))
    ev_out = np.empty(len(admin_max), dtype=int)
    for i, amax in enumerate(admin_max):
        T = lam_true * rng.exponential(1.0) ** (1.0 / k_true)
        gap_obs = p12.discretize_gap(T, rng)
        if gap_obs <= amax:
            t_out[i] = gap_obs; ev_out[i] = 1
        else:
            t_out[i] = max(amax, 0.0); ev_out[i] = 0
    return t_out, ev_out


def run_n3(b_obs=None, B=B_DEFAULT, seed=SEED, x0_list=None):
    """Buduje rozklad b_sur pod modelem zerowym poprawionym. Jesli b_obs=None (jeszcze
    nie policzone na realnych danych), zwraca sam rozklad surogatow (charakterystyka
    modelu zerowego) bez wartosci p - to jest bezpieczny zakres Etapu 2 (kalibracja),
    bez dotykania decydujacego dopasowania do realnych danych."""
    fit0 = fit_no_trend()
    k_hat, lam_hat = fit0["k_hat"], fit0["lam_hat"]
    starts, admin_max, n_total, n_full_real = e1.load_real_starts_and_admin_max()
    year_c = starts - 1985.0

    rng = np.random.default_rng(seed)
    b_sur = np.empty(B)
    for i in range(B):
        t_sim, ev_sim = simulate_n3_once(k_hat, lam_hat, admin_max, rng)
        fit = tr.fit_trend(t_sim, ev_sim, year_c, x0_list=x0_list)
        b_sur[i] = fit["b"]

    center = float(b_sur.mean())
    out = dict(k_hat_no_trend=k_hat, lam_hat_no_trend=lam_hat, B=B, seed=seed,
               b_sur_mean=center, b_sur_median=float(np.median(b_sur)),
               b_sur_sd=float(b_sur.std(ddof=1)),
               b_sur_95CI=(float(np.percentile(b_sur, 2.5)), float(np.percentile(b_sur, 97.5))))

    if b_obs is not None:
        frac_tie = float(np.mean(np.abs(b_sur - b_obs) < 1e-6))
        if frac_tie > TIE_FRAC_STOP:
            raise AssertionError(f"D-026 SS7 (analogicznie): {frac_tie:.1%} surogatow N3 remisuje - zatrzymuje.")
        dist_obs = abs(b_obs - center)
        p = (1 + int(np.sum(np.abs(b_sur - center) >= dist_obs))) / (B + 1)
        out.update(b_obs=b_obs, frac_tie=frac_tie, p=p,
                  efekt_wzgledem_odniesienia=float(b_obs - center))
    return out, b_sur


if __name__ == "__main__":
    import json
    out, _ = run_n3(b_obs=None, B=B_DEFAULT)
    print(json.dumps(out, indent=2, default=str))
    with open("test13_n3_charakterystyka.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test13_n3_charakterystyka.json (BEZ dotykania decydujacych danych realnych)")
