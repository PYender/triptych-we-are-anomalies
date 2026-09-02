#!/usr/bin/env python3
"""
TEST 6 — S7 Etap 3 (D-043): bieg na danych rzeczywistych, poziom państwa.

Autoryzacja: D-043 (2 września 2026), zapisana PRZED tym biegiem.

Estymator i model zerowy N1: `test6_weibull.py` / `test6_null.py`, NIE pisane od nowa —
obie funkcje `fit_pooled`/`fit_frailty`/`profile_ci_k`/`bootstrap_ci_k_pooled`/
`bootstrap_ci_k_frailty` oraz `simulate_n1_once`/`tie_fraction` są generyczne względem
etykiety grupy (przyjmują dowolną tablicę etykiet) — tutaj etykietą jest `ccode`
(państwo) zamiast `diada`, żadna z tych funkcji nie wymagała zmiany.

N2 pominięty jednym zdaniem (D-026: zdegenerowany względem k̂ pulowanego, poza regułą
decyzyjną §8, niezależnie od jednostki analizy — degeneracja jest własnością statystyki
pulowanej, nie struktury danych).

STOP po biegu, przed jakąkolwiek narracją (D-043) — ten skrypt wyłącznie liczy i drukuje
surowe liczby.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd

import test6_weibull as w
import test6_null as n0

B_BOOT = 2000
B_NULL = 2000
SEED_NULL = n0.SEED_PROTOCOL     # 20260822, protokołowe, §6


def load_grouped_s7(path: str = "test6_s7_intervals.csv"):
    df = pd.read_csv(path, comment="#")
    out = []
    for cc, g in df.groupby("ccode"):
        t_full = g.loc[g.cenzurowany == 0, "dlugosc_odstepu"].to_numpy(float)
        c_rows = g.loc[g.cenzurowany == 1, "dlugosc_odstepu"].to_numpy(float)
        assert len(c_rows) == 1, f"panstwo {cc}: oczekiwano dokladnie 1 cenzurowanej, jest {len(c_rows)}"
        out.append((int(cc), t_full, float(c_rows[0])))
    return out


def flatten(grouped):
    ccodes, t, event = [], [], []
    for cc, t_full, c in grouped:
        for x in t_full:
            ccodes.append(cc); t.append(x); event.append(1)
        ccodes.append(cc); t.append(c); event.append(0)
    return np.array(ccodes), np.array(t, float), np.array(event, int)


def main():
    grouped = load_grouped_s7()
    ccodes, t, event = flatten(grouped)
    n_states = len(grouped)
    n_full = int((event == 1).sum())
    n_cens = int((event == 0).sum())

    fit_pooled = w.fit_pooled(t, event)
    fit_frailty = w.fit_frailty(t, event, ccodes)

    prof_pooled = w.profile_ci_k(w.negloglik_pooled, (t, event), fit_pooled["k"],
                                 [fit_pooled["loglam"]], fit_pooled["loglik"])
    groups, gidx = np.unique(ccodes, return_inverse=True)
    prof_frailty = w.profile_ci_k(w.negloglik_frailty, (t, event, gidx, len(groups)),
                                  fit_frailty["k"], [fit_frailty["loglam"], fit_frailty["logtheta"]],
                                  fit_frailty["loglik"])

    boot_lo_p, boot_hi_p, ks_p = w.bootstrap_ci_k_pooled(t, event, ccodes, B=B_BOOT, seed=w.RNG_SEED)
    boot_lo_f, boot_hi_f, ks_f, frac_theta_boundary = w.bootstrap_ci_k_frailty(
        t, event, ccodes, B=B_BOOT, seed=w.RNG_SEED)

    # N1 (test6_null.py, funkcje generyczne wzgledem etykiety grupy - zadna zmiana kodu)
    rng = np.random.default_rng(SEED_NULL)
    k_sur = np.empty(B_NULL)
    for b in range(B_NULL):
        t_sim, event_sim = n0.simulate_n1_once(grouped, rng)
        k_sur[b] = w.fit_pooled(t_sim, event_sim)["k"]
    frac_tie = n0.tie_fraction(k_sur, fit_pooled["k"])
    if frac_tie > n0.TIE_FRAC_STOP:
        raise AssertionError(f"D-026 SS7: {frac_tie:.1%} surogatow N1 remisuje z obserwacja - zatrzymuje.")
    p_n1 = (1 + int(np.sum(np.abs(k_sur - 1.0) >= np.abs(fit_pooled["k"] - 1.0)))) / (B_NULL + 1)

    rozjazd_profil_bootstrap_pooled = dict(
        profil_szerokosc=prof_pooled["hi"] - prof_pooled["lo"] if not (np.isnan(prof_pooled["lo"]) or np.isnan(prof_pooled["hi"])) else None,
        bootstrap_szerokosc=boot_hi_p - boot_lo_p,
        stosunek_bootstrap_do_profilu=(
            (boot_hi_p - boot_lo_p) / (prof_pooled["hi"] - prof_pooled["lo"])
            if not (np.isnan(prof_pooled["lo"]) or np.isnan(prof_pooled["hi"])) else None
        ),
    )

    out = dict(
        struktura=dict(n_panstw=n_states, n_pelnych=n_full, n_cenzurowanych=n_cens),
        fit_pooled=dict(k=fit_pooled["k"], lam=fit_pooled["lam"], loglik=fit_pooled["loglik"]),
        fit_frailty=dict(k=fit_frailty["k"], lam=fit_frailty["lam"], theta=fit_frailty["theta"],
                         loglik=fit_frailty["loglik"], theta_na_granicy=bool(fit_frailty["theta"] <= 1e-10)),
        przedzialy_pooled=dict(
            profil=dict(lo=prof_pooled["lo"], hi=prof_pooled["hi"],
                       lo_bounded=prof_pooled["lo_bounded"], hi_bounded=prof_pooled["hi_bounded"],
                       anchor_ok=prof_pooled["anchor_ok"]),
            bootstrap_panstwa=dict(lo=boot_lo_p, hi=boot_hi_p),
        ),
        przedzialy_frailty=dict(
            profil=dict(lo=prof_frailty["lo"], hi=prof_frailty["hi"],
                       lo_bounded=prof_frailty["lo_bounded"], hi_bounded=prof_frailty["hi_bounded"],
                       anchor_ok=prof_frailty["anchor_ok"]),
            bootstrap_panstwa=dict(lo=boot_lo_f, hi=boot_hi_f, frac_theta_boundary=frac_theta_boundary),
        ),
        rozjazd_profil_bootstrap_pooled=rozjazd_profil_bootstrap_pooled,
        n1_diagnostyczny=dict(model="N1", k_obs=fit_pooled["k"], p=p_n1, B=B_NULL, seed=SEED_NULL,
                              k_sur_mean=float(k_sur.mean()), k_sur_median=float(np.median(k_sur)),
                              k_sur_sd=float(k_sur.std(ddof=1)), frac_tie=frac_tie,
                              poza_regula_decyzyjna_S8="diagnostyczny (D-029 pkt 2 analogia), nie orzeka"),
        n2="pominiety jednym zdaniem (D-026): zdegenerowany wzgledem k-hat pulowanego, "
           "niezaleznie od jednostki analizy - degeneracja jest wlasnoscia statystyki, nie danych.",
    )
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    with open("test6_s7_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test6_s7_wyniki.json")


if __name__ == "__main__":
    main()
