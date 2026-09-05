#!/usr/bin/env python3
"""
TEST 12 — bieg P1->S1->S2->S3 na danych rzeczywistych (D-057/D-058, autoryzacja w promptcie
autora "Uruchamiamy, po wpisaniu jednej deklaracji" - deklaracja D-058 zapisana przed tym
biegiem).

P1: prog>=3, model glowny, pierwszy odstep pary 406 wykluczony (D-057, t0_flag==1).
S1: prog>=2, ta sama zasada t0.
S2: P1 z modelem kruchosci - raportowany jako czesc P1 (fit_frailty juz tam liczony), tutaj
    wydzielony osobno z frac_theta_boundary na widoku (zgodnie z zadaniem SS6 protokolu).
S3: P1 podzielony na epoki 1989 (rok konca poprzedniego epizodu decyduje o przynaleznosci,
    analogicznie do SS3 Testu 10) - OPISOWY, bez reguly decyzyjnej, bez N1.

Model zerowy N1: mechanizm ROZSZERZONY o dyskretyzacje rocznikowa surogatow (D-058) -
`simulate_n1_once_discretized`, NIE zwykly `test6_null.simulate_n1_once` - zmierzone w D-058,
ze zwyklym mechanizmem N1 nie odzwierciedlaloby pomiaru realnych danych (zaokraglonych do lat).
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd

import test6_weibull as w
import test12_power as p12

SEED_N1 = 20260822
B_NULL = 2000
B_BOOT = 2000
TIE_FRAC_STOP = 0.01


def load_grouped(path, exclude_t0=True):
    df = pd.read_csv(path, comment="#")
    if exclude_t0:
        df = df[df.t0_flag == 0]
    out = []
    for d, g in df.groupby("dyad_id"):
        t_full = g.loc[g.cenzurowany == 0, "dlugosc"].to_numpy(float)
        c_rows = g.loc[g.cenzurowany == 1, "dlugosc"].to_numpy(float)
        c = float(c_rows[0]) if len(c_rows) else None
        out.append((d, t_full, c))
    return out


def flatten(grouped):
    diads, t, event = [], [], []
    for d, t_full, c in grouped:
        for x in t_full:
            diads.append(d); t.append(x); event.append(1)
        if c is not None:
            diads.append(d); t.append(c); event.append(0)
    return np.array(diads), np.array(t, float), np.array(event, int)


def simulate_n1_once_discretized(grouped, rng):
    """D-058: surogaty N1 przechodza przez TA SAMA dyskretyzacje rocznikowa co realne dane
    (floor(phi+T)-1, ta sama funkcja co w symulacji odchylenia test12_power.discretize_gap) -
    inaczej model zerowy nie odzwierciedla mechanizmu pomiaru."""
    diads_sim, t_sim, event_sim = [], [], []
    for d, t_full, c in grouped:
        n = len(t_full)
        total_exposure = float(t_full.sum() + (c if c is not None else 0.0))
        lam_hat = n / total_exposure if total_exposure > 0 else 0.0
        for _ in range(n):
            if lam_hat > 0:
                T = rng.exponential(1.0 / lam_hat)
                gap_obs = p12.discretize_gap(T, rng)
            else:
                gap_obs = 0.0
            diads_sim.append(d); t_sim.append(gap_obs); event_sim.append(1)
        if c is not None:
            diads_sim.append(d); t_sim.append(c); event_sim.append(0)
    return np.array(diads_sim), np.array(t_sim, float), np.array(event_sim, int)


def tie_fraction(k_sur, kobs, tol=1e-6):
    return float(np.mean(np.abs(k_sur - kobs) < tol))


def run_n1(grouped, kobs, B=B_NULL, seed=SEED_N1):
    rng = np.random.default_rng(seed)
    k_sur = np.empty(B)
    for b in range(B):
        _, t_sim, ev_sim = simulate_n1_once_discretized(grouped, rng)
        k_sur[b] = w.fit_pooled(t_sim, ev_sim)["k"]
    frac_tie = tie_fraction(k_sur, kobs)
    if frac_tie > TIE_FRAC_STOP:
        raise AssertionError(f"D-026 SS7: {frac_tie:.1%} surogatow N1 remisuje - zatrzymuje.")
    p = (1 + int(np.sum(np.abs(k_sur - 1.0) >= np.abs(kobs - 1.0)))) / (B + 1)
    return dict(k_obs=kobs, p=p, B=B, seed=seed, k_sur_mean=float(k_sur.mean()),
               k_sur_median=float(np.median(k_sur)), k_sur_sd=float(k_sur.std(ddof=1)),
               frac_tie=frac_tie,
               faktyczny_poziom_pelnej_reguly_D058="1.3% (D-056), nie nominalne 5% - podac obok")


def fit_and_intervals(t, event, diads, do_frailty=True):
    fit_pooled = w.fit_pooled(t, event)
    prof_pooled = w.profile_ci_k(w.negloglik_pooled, (t, event), fit_pooled["k"],
                                 [fit_pooled["loglam"]], fit_pooled["loglik"])
    boot_lo_p, boot_hi_p, _ = w.bootstrap_ci_k_pooled(t, event, diads, B=B_BOOT, seed=w.RNG_SEED)
    out = dict(
        fit_pooled=dict(k=fit_pooled["k"], lam=fit_pooled["lam"], loglik=fit_pooled["loglik"]),
        przedzialy_pooled=dict(
            profil=dict(lo=prof_pooled["lo"], hi=prof_pooled["hi"],
                       lo_bounded=prof_pooled["lo_bounded"], hi_bounded=prof_pooled["hi_bounded"],
                       anchor_ok=prof_pooled["anchor_ok"]),
            bootstrap=dict(lo=boot_lo_p, hi=boot_hi_p)),
    )
    if do_frailty:
        fit_frailty = w.fit_frailty(t, event, diads)
        groups, gidx = np.unique(diads, return_inverse=True)
        prof_frailty = w.profile_ci_k(w.negloglik_frailty, (t, event, gidx, len(groups)),
                                      fit_frailty["k"], [fit_frailty["loglam"], fit_frailty["logtheta"]],
                                      fit_frailty["loglik"])
        boot_lo_f, boot_hi_f, _, frac_theta_boundary = w.bootstrap_ci_k_frailty(
            t, event, diads, B=B_BOOT, seed=w.RNG_SEED)
        out["fit_frailty"] = dict(k=fit_frailty["k"], lam=fit_frailty["lam"], theta=fit_frailty["theta"],
                                  loglik=fit_frailty["loglik"], theta_na_granicy=bool(fit_frailty["theta"] <= 1e-10))
        out["przedzialy_frailty"] = dict(
            profil=dict(lo=prof_frailty["lo"], hi=prof_frailty["hi"],
                       lo_bounded=prof_frailty["lo_bounded"], hi_bounded=prof_frailty["hi_bounded"],
                       anchor_ok=prof_frailty["anchor_ok"]),
            bootstrap=dict(lo=boot_lo_f, hi=boot_hi_f, frac_theta_boundary=frac_theta_boundary))
    return out


def run_variant(path, label, exclude_t0=True, with_n1=True, do_frailty=True):
    grouped = load_grouped(path, exclude_t0=exclude_t0)
    diads, t, event = flatten(grouped)
    struktura = dict(n_pary=len(grouped), n_pelnych=int((event == 1).sum()), n_cenzurowanych=int((event == 0).sum()))
    res = fit_and_intervals(t, event, diads, do_frailty=do_frailty)
    res["label"] = label
    res["struktura"] = struktura
    if with_n1:
        res["n1_diagnostyczny"] = run_n1(grouped, res["fit_pooled"]["k"])
    res["n2"] = "pominiety jednym zdaniem (D-026): zdegenerowany wzgledem k-hat pulowanego."
    return res


def run_s3_epoki(path, cutoff=1989, exclude_t0=True):
    df = pd.read_csv(path, comment="#")
    if exclude_t0:
        df = df[df.t0_flag == 0]
    # rok "startu zegara" = ep_end poprzedniego epizodu (koniec_poprzedniego), analogicznie SS3 Testu 10
    przed = df[df.ep_end < cutoff]
    po = df[df.ep_end >= cutoff]

    def summarize(sub):
        diads_l, t_l, event_l = [], [], []
        for d, g in sub.groupby("dyad_id"):
            t_full = g.loc[g.cenzurowany == 0, "dlugosc"].to_numpy(float)
            c_rows = g.loc[g.cenzurowany == 1, "dlugosc"].to_numpy(float)
            for x in t_full:
                diads_l.append(d); t_l.append(x); event_l.append(1)
            if len(c_rows):
                diads_l.append(d); t_l.append(float(c_rows[0])); event_l.append(0)
        diads_l, t_l, event_l = np.array(diads_l), np.array(t_l, float), np.array(event_l, int)
        if len(t_l) == 0:
            return None
        fit = fit_and_intervals(t_l, event_l, diads_l, do_frailty=False)
        fit["struktura"] = dict(n_wierszy=len(t_l), n_pelnych=int((event_l == 1).sum()),
                                n_cenzurowanych=int((event_l == 0).sum()))
        return fit

    return dict(label=f"S3 (opisowy, podzial {cutoff}, bez reguly decyzyjnej, bez N1)",
               przed=summarize(przed), po=summarize(po))


def main():
    out = {}
    print("=== P1 (prog>=3) ===")
    out["P1"] = run_variant("test12_intervals_prog3.csv", "P1 (prog>=3, orzekajacy)", exclude_t0=True)
    print(json.dumps(out["P1"], indent=2, default=str))

    print("=== S1 (prog>=2) ===")
    out["S1"] = run_variant("test12_intervals_prog2.csv", "S1 (prog>=2, wrazliwosc)", exclude_t0=True)
    print(json.dumps(out["S1"], indent=2, default=str))

    print("=== S2 (P1 kruchosc - juz w P1, wydzielone tutaj dla przejrzystosci) ===")
    out["S2_kruchosc_z_P1"] = out["P1"].get("fit_frailty"), out["P1"].get("przedzialy_frailty")

    print("=== S3 (epoki 1989, opisowy) ===")
    out["S3"] = run_s3_epoki("test12_intervals_prog3.csv", cutoff=1989, exclude_t0=True)
    print(json.dumps(out["S3"], indent=2, default=str))

    with open("test12_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test12_wyniki.json")


if __name__ == "__main__":
    main()
