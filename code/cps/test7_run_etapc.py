#!/usr/bin/env python3
"""
TEST 7 — Etap C (D-037): uruchomienie P1 -> P2a -> P2b -> S1 & S3 na danych rzeczywistych.

Autoryzacja: D-037 (2 wrzesnia 2026), zapisana PRZED tym biegiem, bez znajomosci wyniku.

Ten skrypt WYLACZNIE liczy i zapisuje surowe liczby (D-037 / klauzula STOP): zadnej narracji,
zadnej oceny "czy hipoteza wsparta" — to jest zastrzezone dla autora po zobaczeniu wynikow
nagich (uzasadnienie autora: "raport pisany razem z liczbami zbyt latwo staje sie ich
uzasadnieniem").

FLAGA METODOLOGICZNA NIEROZSTRZYGNIETA (do zgloszenia, nie do cichego wyboru): D-034 podaje
dla P2a "pieć parametrow" (3 bazowe k/lambda0/theta + 2 kowarianty), ale protokol SS6 opisuje
"postac" zmiennej potencjal-gospodarczy jako "suma i stosunek stron" (DWIE mozliwe operacjonalizacje
CINC, nie jedna) — uzycie obu naraz dawaloby 6 parametrow na 37 zdarzen, sprzeczne z "pieć"
D-034. Nie rozstrzygnietone tutaj samodzielnie: P2a policzone w DWOCH wariantach kowariantu
CINC (stosunek — logarytm, standardowa operacjonalizacja "power ratio" w literaturze IR: i
suma — logarytm, "polaczony potencjal"), oba z tym samym drugim kowariantem (status
mocarstwowy), oba wciaz przy pieciu parametrach. Zaden nie oznaczony jako "ten wlasciwy" —
oba surowe wyniki podane obok siebie, wybor pozostawiony autorowi.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from scipy.stats import chi2

import test6_weibull as w
import test7_estimate as e
import test7_p2_fit as pf

SEED = w.RNG_SEED


def run_variant(label, intervals_path, include_t0=False, B_boot=e.B_BOOTSTRAP,
                B_null=e.B_NULL, B_null_frailty=500):
    grouped = e.load_grouped(intervals_path, include_t0=include_t0)
    struct = e.structure_report(grouped, label=label)
    diads, t, event, fit_pooled, fit_frailty = e.fit_p1(grouped)
    ci = e.ci_p1(diads, t, event, fit_pooled, fit_frailty, B=B_boot, seed=SEED)
    n1 = e.run_n1_test7(intervals_path, B=B_null, B_frailty=B_null_frailty,
                        seed=e.SEED_PROTOCOL_N1, include_t0=include_t0)
    return dict(
        label=label, struktura=struct,
        fit_pooled=dict(k=fit_pooled["k"], lam=fit_pooled["lam"], loglik=fit_pooled["loglik"]),
        fit_frailty=dict(k=fit_frailty["k"], lam=fit_frailty["lam"], theta=fit_frailty["theta"],
                         loglik=fit_frailty["loglik"],
                         theta_na_granicy=bool(fit_frailty["theta"] <= 1e-10)),
        przedzialy=ci,
        n1_diagnostyczny=n1,
    )


def _profile_ci_and_boot_p2(negloglik, args_fn, grouped_fit_fn, t, event, diad, X, j,
                            beta_hat, n_beta, level=0.95, B=400):
    """UWAGA (usterka złapana w teście dymnym, poprawiona przed biegiem rzeczywistym):
    `pf.profile_ci_beta`'s `j` musi być pozycją w PEŁNYM wektorze parametrów
    [logk, loglam0, beta_0..beta_{p-1}, logtheta] (bo `np.insert(rest_free, j, bj)` wstawia
    tam z powrotem), NIE pozycją kowariantu w X. Pierwsza wersja przekazywała gołe `j`
    (0 albo 1) — dla P2a/P2b z p=2 to wstawiało wartość na miejsce logk albo loglam0,
    dając bezsensowny przedział (np. lo=6.6 > hi=6.5, oba dodatnie, dla współczynnika
    o wartości -0,16). Sprawdzone bezpośrednio na wyniku testu dymnego przed pełnym biegiem."""
    fit = grouped_fit_fn()
    rest0 = [fit["logk"], fit["loglam0"], *[b for i, b in enumerate(fit["beta"]) if i != j], fit["logtheta"]]
    j_full = 2 + j
    def negloglik_full(full, t, event, gidx, n_groups, X):
        return pf.negloglik_frailty_cov(full, t, event, gidx, n_groups, X)
    groups, gidx = np.unique(diad, return_inverse=True)
    lo, hi, grid, lr = pf.profile_ci_beta(negloglik_full, (t, event, gidx, len(groups), X),
                                          beta_hat, j_full, rest0, fit["loglik"], level=level)
    beta0_rest = [b for i, b in enumerate(fit["beta"])]
    blo, bhi, betas, frac_boundary = pf.bootstrap_ci_beta_frailty(t, event, diad, X, j, B=B,
                                                                  seed=SEED, level=level,
                                                                  beta0=beta0_rest)
    return dict(profil=dict(lo=lo, hi=hi), bootstrap=dict(lo=blo, hi=bhi, frac_theta_boundary=frac_boundary))


def run_p2a_variant(cinc_col, label):
    df_int = pd.read_csv("test7_intervals.csv", comment="#")
    main_model = df_int[(df_int["t0_flag"] == 0) & (df_int["ucieta"] == 0)].reset_index(drop=True)
    p2a = pd.read_csv("test7_p2a_variables.csv", comment="#").reset_index(drop=True)
    assert len(main_model) == len(p2a), (len(main_model), len(p2a))
    assert (main_model["diada"].values == p2a["diada"].values).all(), "p2a: rozjazd kolejnosci wierszy z modelem glownym"
    assert (main_model["rok_start"].values == p2a["rok_odniesienia"].values).all()

    t = main_model["ekspozycja"].to_numpy(float)
    event = (main_model["cenzurowany"] == 0).astype(int).to_numpy()
    diad = main_model["diada"].to_numpy()

    x1 = np.log(p2a[cinc_col].to_numpy(float))
    x2 = p2a["status_mocarstwowy"].to_numpy(float)
    X = np.column_stack([x1, x2])
    Xz = (X - X.mean(axis=0)) / X.std(axis=0)   # standaryzacja dla stabilnosci optymalizacji, nie zmienia istotnosci

    def fit_fn():
        return pf.fit_frailty_cov(t, event, diad, Xz)
    fit = fit_fn()

    ci_cinc = _profile_ci_and_boot_p2(None, None, fit_fn, t, event, diad, Xz, 0, fit["beta"][0], 2)
    ci_status = _profile_ci_and_boot_p2(None, None, fit_fn, t, event, diad, Xz, 1, fit["beta"][1], 2)

    n_params = 3 + len(fit["beta"])  # k, lam0, theta + p kowariantow = 5 przy p=2
    n_events = int(event.sum())

    return dict(
        label=label, kowariant_cinc=cinc_col, n_wierszy=len(main_model), n_diady=int(main_model["diada"].nunique()),
        n_zdarzen=n_events, n_parametrow=n_params, zdarzen_na_parametr=n_events / n_params,
        standaryzacja="X standaryzowane (srednia 0, sd 1) przed dopasowaniem — zwracane wspolczynniki "
                     "SA na skali standaryzowanej (interpretacja: zmiana o 1 SD zmiennej)",
        k=fit["k"], lam0=fit["lam0"], theta=fit["theta"], theta_na_granicy=fit["theta_at_boundary"],
        loglik=fit["loglik"], converged_same_starts=fit["converged_same"],
        beta_log_cinc=fit["beta"][0], beta_status=fit["beta"][1],
        przedzial_beta_cinc=ci_cinc, przedzial_beta_status=ci_status,
    )


def run_p2b():
    df_int = pd.read_csv("test7_intervals.csv", comment="#")
    main_model = df_int[(df_int["t0_flag"] == 0) & (df_int["ucieta"] == 0)]
    main_model = main_model[main_model["typ"].isin(["pelny", "cenzurowany"])].reset_index(drop=True)
    p2b = pd.read_csv("test7_p2b_variables.csv", comment="#").reset_index(drop=True)
    assert len(main_model) == len(p2b), (len(main_model), len(p2b))
    assert (main_model["diada"].values == p2b["diada"].values).all(), "p2b: rozjazd kolejnosci wierszy z modelem glownym"

    t = main_model["ekspozycja"].to_numpy(float)
    event = (main_model["cenzurowany"] == 0).astype(int).to_numpy()
    diad = main_model["diada"].to_numpy()

    x1 = p2b["czas_trwania"].to_numpy(float)
    x2 = p2b["straty_log"].to_numpy(float)
    X = np.column_stack([x1, x2])
    Xz = (X - X.mean(axis=0)) / X.std(axis=0)

    def fit_fn():
        return pf.fit_frailty_cov(t, event, diad, Xz)
    fit = fit_fn()

    ci_dur = _profile_ci_and_boot_p2(None, None, fit_fn, t, event, diad, Xz, 0, fit["beta"][0], 2)
    ci_bd = _profile_ci_and_boot_p2(None, None, fit_fn, t, event, diad, Xz, 1, fit["beta"][1], 2)

    n_params = 3 + len(fit["beta"])
    n_events = int(event.sum())

    return dict(
        label="P2b (opisowy, poza regula decyzyjna SS8, D-034)", n_wierszy=len(main_model),
        n_diady=int(main_model["diada"].nunique()), n_zdarzen=n_events, n_parametrow=n_params,
        zdarzen_na_parametr=n_events / n_params,
        standaryzacja="X standaryzowane (srednia 0, sd 1) przed dopasowaniem",
        k=fit["k"], lam0=fit["lam0"], theta=fit["theta"], theta_na_granicy=fit["theta_at_boundary"],
        loglik=fit["loglik"], converged_same_starts=fit["converged_same"],
        beta_czas_trwania=fit["beta"][0], beta_straty_log=fit["beta"][1],
        przedzial_beta_czas_trwania=ci_dur, przedzial_beta_straty_log=ci_bd,
    )


def main():
    wynik = {}

    print("=== P1 ==="); wynik["P1"] = run_variant("P1", "test7_intervals.csv", include_t0=False)
    print(json.dumps(wynik["P1"], indent=2, default=str))

    print("=== P2a (kowariant CINC: log stosunek) ===")
    wynik["P2a_stosunek"] = run_p2a_variant("cinc_stosunek", "P2a — wariant log(stosunek CINC) [prowizoryczny, nierozstrzygniety wybor]")
    print(json.dumps(wynik["P2a_stosunek"], indent=2, default=str))

    print("=== P2a (kowariant CINC: log suma) ===")
    wynik["P2a_suma"] = run_p2a_variant("cinc_suma", "P2a — wariant log(suma CINC) [prowizoryczny, nierozstrzygniety wybor]")
    print(json.dumps(wynik["P2a_suma"], indent=2, default=str))

    print("=== P2b ===")
    wynik["P2b"] = run_p2b()
    print(json.dumps(wynik["P2b"], indent=2, default=str))

    print("=== S1 ==="); wynik["S1"] = run_variant("S1", "test7_s1_intervals.csv", include_t0=False)
    print(json.dumps(wynik["S1"], indent=2, default=str))

    print("=== S3 ==="); wynik["S3"] = run_variant("S3", "test7_intervals.csv", include_t0=True)
    print(json.dumps(wynik["S3"], indent=2, default=str))

    with open("test7_etapc_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(wynik, fh, indent=2, default=str, ensure_ascii=False)
    print("zapisano test7_etapc_wyniki.json")


if __name__ == "__main__":
    main()
