#!/usr/bin/env python3
"""
S7b/S7c — bieg na danych rzeczywistych (D-049).

Reużywa `test6_run_s7.py` (`load_grouped_s7`, `flatten`) i `test6_weibull.py`/`test6_null.py`
bez żadnej zmiany — jedyna różnica względem S7 jest w PLIKU wejściowym (już zbudowanym przez
`test6_build_s7bc.py`), nie w kodzie estymacji.

STOP po biegu, przed jakąkolwiek narracją (D-049) — wyłącznie surowe liczby.
"""
from __future__ import annotations
import json
import numpy as np

import test6_weibull as w
import test6_null as n0
import test6_run_s7 as r7

B_BOOT = 2000
B_NULL = 2000
SEED_NULL = n0.SEED_PROTOCOL


def run_variant(path, label):
    grouped = r7.load_grouped_s7(path)
    ccodes, t, event = r7.flatten(grouped)
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

    boot_lo_p, boot_hi_p, _ = w.bootstrap_ci_k_pooled(t, event, ccodes, B=B_BOOT, seed=w.RNG_SEED)
    boot_lo_f, boot_hi_f, _, frac_theta_boundary = w.bootstrap_ci_k_frailty(
        t, event, ccodes, B=B_BOOT, seed=w.RNG_SEED)

    rng = np.random.default_rng(SEED_NULL)
    k_sur = np.empty(B_NULL)
    for b in range(B_NULL):
        t_sim, event_sim = n0.simulate_n1_once(grouped, rng)
        k_sur[b] = w.fit_pooled(t_sim, event_sim)["k"]
    frac_tie = n0.tie_fraction(k_sur, fit_pooled["k"])
    if frac_tie > n0.TIE_FRAC_STOP:
        raise AssertionError(f"D-026 SS7 ({label}): {frac_tie:.1%} surogatow N1 remisuje - zatrzymuje.")
    p_n1 = (1 + int(np.sum(np.abs(k_sur - 1.0) >= np.abs(fit_pooled["k"] - 1.0)))) / (B_NULL + 1)

    prof_w = prof_pooled["hi"] - prof_pooled["lo"] if not (np.isnan(prof_pooled["lo"]) or np.isnan(prof_pooled["hi"])) else None
    boot_w = boot_hi_p - boot_lo_p
    rozjazd = dict(
        profil_szerokosc=prof_w, bootstrap_szerokosc=boot_w,
        stosunek_bootstrap_do_profilu=(boot_w / prof_w) if prof_w else None,
    )

    return dict(
        label=label,
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
        rozjazd_profil_bootstrap_pooled=rozjazd,
        n1_diagnostyczny=dict(model="N1", k_obs=fit_pooled["k"], p=p_n1, B=B_NULL, seed=SEED_NULL,
                              k_sur_mean=float(k_sur.mean()), k_sur_median=float(np.median(k_sur)),
                              k_sur_sd=float(k_sur.std(ddof=1)), frac_tie=frac_tie,
                              poza_regula_decyzyjna_S8="diagnostyczny, nie orzeka"),
        n2="pominiety jednym zdaniem (D-026): zdegenerowany wzgledem k-hat pulowanego.",
    )


def main():
    out = dict(
        S7b=run_variant("test6_s7b_prog3_intervals.csv", "S7b (zegar inicjacji, orzekajacy)"),
        S7c=run_variant("test6_s7c_prog3_intervals.csv", "S7c (kontrola negatywna)"),
    )
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    with open("test6_s7bc_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test6_s7bc_wyniki.json")


if __name__ == "__main__":
    main()
