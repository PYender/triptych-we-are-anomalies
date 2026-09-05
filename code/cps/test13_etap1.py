#!/usr/bin/env python3
"""
TEST 13 — Etap 1 (SS7 protokolu): trzy wyjasnienia konkurencyjne, PRZED czymkolwiek innym.

A. Ucinanie przez koniec okna (2023) - symulacja: dla kazdej z 294 realnych obserwacji
   (220 pelnych + 74 cenzurowanych, PO wykluczeniu t0 pary 406) uzywamy jej REALNEGO roku
   startu (ep_end, fakt egzogeniczny, nie symulowany) i pytamy: pod PRAWDZIWIE STALYM k (bez
   trendu), co dalaby administracyjna granica 2023? admin_max = 2023 - rok_startu (per
   obserwacja, ZNANE z danych). Symulacja: T~Weibull(k_true,lam_true) ciagle, dyskretyzacja
   rok-po-roku (ta sama funkcja co D-058/test12_power.discretize_gap), potem: jesli
   dyskretyzowane T <= admin_max -> pelne T; inaczej -> cenzurowane na admin_max. Dopasuj
   model trendu, zbierz rozklad b-hat pod PRAWDA b=0.

B. Gestosc kodowania - opisowe, na surowych danych UCDP: liczba diado-lat na rok
   kalendarzowy w oknie; mediana odstepu pelnego w piecioletnich podokresach.

C. Zmiana skladu par - opisowe: rozklad liczby epizodow na pare, osobno dla par
   zaczynajacych przed/po 1985.

STOP po tych trzech - ocena, czy test w ogole orzeka, zanim jakikolwiek inny krok.
"""
from __future__ import annotations
import json, time
import numpy as np
import pandas as pd

import test12_power as p12
import test13_trend as tr

WINDOW_END = 2023
SEED = tr.RNG_SEED


def load_real_starts_and_admin_max(path="test12_intervals_prog3.csv"):
    df = pd.read_csv(path, comment="#")
    df = df[df.t0_flag == 0]
    starts = df["ep_end"].to_numpy(float)
    admin_max = WINDOW_END - starts
    return starts, admin_max, len(df), int((df.cenzurowany == 0).sum())


def simulate_one_rep_A(k_true, lam_true, admin_max, rng):
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


def calibrate_lam(k_true, admin_max, target_frac_full, rng, lam_grid):
    best = None
    for lam in lam_grid:
        fracs = []
        for _ in range(20):
            t_, ev_ = simulate_one_rep_A(k_true, lam, admin_max, rng)
            fracs.append(ev_.mean())
        frac = np.mean(fracs)
        diff = abs(frac - target_frac_full)
        if best is None or diff < best[0]:
            best = (diff, lam, frac)
    return best


def measure_A(n_reps=400, seed=SEED):
    starts, admin_max, n_total, n_full_real = load_real_starts_and_admin_max()
    target_frac = n_full_real / n_total
    k_true = 0.7096  # obserwowane k-hat P1 Testu 12 (D-055/wyniki), jako reprezentatywna stala

    rng = np.random.default_rng(seed)
    _, lam_true, frac_at_best = calibrate_lam(k_true, admin_max, target_frac, rng,
                                              lam_grid=[4, 5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 10, 12])
    year_c = starts - 1985.0

    bs = np.empty(n_reps)
    fracs_full = np.empty(n_reps)
    for i in range(n_reps):
        t_sim, ev_sim = simulate_one_rep_A(k_true, lam_true, admin_max, rng)
        fracs_full[i] = ev_sim.mean()
        fit = tr.fit_trend(t_sim, ev_sim, year_c)
        bs[i] = fit["b"]

    return dict(n_reps=n_reps, k_true=k_true, lam_true=lam_true,
               target_frac_full=target_frac, frac_full_calib_check=float(frac_at_best),
               frac_full_sim_mean=float(fracs_full.mean()),
               b_mean=float(bs.mean()), b_median=float(np.median(bs)), b_sd=float(bs.std(ddof=1)),
               frac_b_positive=float((bs > 0).mean()),
               b_95CI=(float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))))


def measure_B():
    df = pd.read_csv("data/ucdp/Dyadic_v25_1.csv")
    df = df[df.year <= 2023]
    per_year = df.groupby("year").size()
    density = dict(pierwsze_5_lat=per_year.head(5).to_dict(), ostatnie_5_lat=per_year.tail(5).to_dict(),
                   min=int(per_year.min()), max=int(per_year.max()), mean=float(per_year.mean()))

    iv = pd.read_csv("test12_intervals_prog3.csv", comment="#")
    iv = iv[iv.t0_flag == 0]
    full = iv[iv.cenzurowany == 0].copy()
    full["okres5"] = (full.ep_end // 5) * 5
    med = full.groupby("okres5")["dlugosc"].agg(["median", "mean", "count"])
    monotonicznie_malejaca = bool(np.all(np.diff(med["median"].to_numpy()) <= 0.5))  # tolerancja szumu malych N
    return dict(gestosc_kodowania=density, mediana_w_5letnich_okresach=med.reset_index().to_dict(orient="records"),
               mediana_generalnie_malejaca=monotonicznie_malejaca)


def measure_C():
    df = pd.read_csv("data/ucdp/Dyadic_v25_1.csv")
    df = df[df.year <= 2023]
    years_by_dyad = df.groupby("dyad_id")["year"].apply(lambda s: sorted(set(s))).to_dict()

    def episodes_from_years(years):
        eps = []
        cur = [years[0]]
        for y in years[1:]:
            if y == cur[-1] + 1:
                cur.append(y)
            else:
                eps.append((cur[0], cur[-1])); cur = [y]
        eps.append((cur[0], cur[-1]))
        return eps

    rows = []
    for d, years in years_by_dyad.items():
        eps = episodes_from_years(years)
        if len(eps) < 3:
            continue
        rows.append(dict(dyad_id=d, n_epizodow=len(eps), pierwszy_rok=eps[0][0]))
    tab = pd.DataFrame(rows)
    tab["grupa"] = np.where(tab.pierwszy_rok < 1985, "przed_1985", "po_1985")
    return tab.groupby("grupa")["n_epizodow"].describe().reset_index().to_dict(orient="records")


def main():
    out = {}
    t0 = time.time()
    out["A_uciecie_2023"] = measure_A()
    print(f"[A] b_mean={out['A_uciecie_2023']['b_mean']:.4f} b_sd={out['A_uciecie_2023']['b_sd']:.4f} "
         f"frac_b_positive={out['A_uciecie_2023']['frac_b_positive']:.3f} ({time.time()-t0:.0f}s)")

    out["B_gestosc_kodowania"] = measure_B()
    print("[B] mediana_generalnie_malejaca=", out["B_gestosc_kodowania"]["mediana_generalnie_malejaca"])

    out["C_zmiana_skladu_par"] = measure_C()
    print("[C]", out["C_zmiana_skladu_par"])

    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    with open("test13_etap1_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test13_etap1_wyniki.json")


if __name__ == "__main__":
    main()
