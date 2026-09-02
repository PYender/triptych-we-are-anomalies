#!/usr/bin/env python3
"""
S7 — symulacja pokrycia przedziału profilowego i bootstrapowego (autor, po D-044).

Pytanie: czy odwrócony rozjazd (bootstrap węższy niż profil, D-043/D-044 errata) jest
artefaktem bootstrapu blokowego przy trzynastu klastrach (podejrzenie Code, NIE ustalenie),
czy czymś innym. Test: symulacja k_prawdziwe=1 na strukturze S7 (13 realnych okien
administracyjnych, mechanizm min(T,C) z D-031, `simulate_dataset_test7` reużyty bez zmian),
tysiąc replik (żądanie autora), sprawdzenie w każdej replice, czy 1 mieści się w przedziale
profilowym i czy mieści się w przedziale bootstrapowym (poziom państw, B=300 wewnętrznych
replik na zewnętrzną replikę — kompromis kosztowy, zmierzony: ~1,7s/replika zewnętrzna,
~29 min na tysiąc, zaakceptowalny background run, ten sam typ kompromisu co B_frailty=500
gdzie indziej w projekcie).

Jeżeli pokrycie bootstrapowe istotnie < 95%, hipoteza Code (bootstrap blokowy przy N=13
zaniża niepewność) jest potwierdzona i staje się ustaleniem o NARZĘDZIU — ważnym wstecz dla
każdego biegu w tym projekcie, który używał bootstrapu grupowego na małej liczbie grup
(diady Testu 6 miały 18, Testu 7 101 — S7 z 13 jest ekstremalnym przypadkiem, ale kierunek
mógłby dotyczyć też Testu 6).
"""
from __future__ import annotations
import json, time
import numpy as np
import pandas as pd

import test6_weibull as w
import test7_estimate as e

N_REPS = 1000
B_INNER = 300
SEED = w.RNG_SEED


def main():
    iv = pd.read_csv("test6_s7_intervals.csv", comment="#")
    windows = iv.groupby("ccode")["dlugosc_odstepu"].sum().tolist()
    n_full_real = int((iv.cenzurowany == 0).sum())
    lam_true = sum(windows) / n_full_real

    rng = np.random.default_rng(SEED)
    cover_profile = np.zeros(N_REPS, dtype=bool)
    cover_bootstrap = np.zeros(N_REPS, dtype=bool)
    profile_widths = np.empty(N_REPS)
    bootstrap_widths = np.empty(N_REPS)
    k_hats = np.empty(N_REPS)
    n_full_sim = np.empty(N_REPS, dtype=int)

    t0 = time.time()
    for i in range(N_REPS):
        t, event, gid = e.simulate_dataset_test7(1.0, lam_true, 0.0, windows, rng)
        fit = w.fit_pooled(t, event)
        k_hats[i] = fit["k"]
        n_full_sim[i] = int((event == 1).sum())

        prof = w.profile_ci_k(w.negloglik_pooled, (t, event), fit["k"], [fit["loglam"]], fit["loglik"])
        lo_p, hi_p = prof["lo"], prof["hi"]
        cover_profile[i] = bool((not np.isnan(lo_p)) and (not np.isnan(hi_p)) and lo_p <= 1.0 <= hi_p)
        profile_widths[i] = (hi_p - lo_p) if not (np.isnan(lo_p) or np.isnan(hi_p)) else np.nan

        lo_b, hi_b, _ = w.bootstrap_ci_k_pooled(t, event, gid, B=B_INNER, seed=SEED + 7919 * (i + 1))
        cover_bootstrap[i] = bool(lo_b <= 1.0 <= hi_b)
        bootstrap_widths[i] = hi_b - lo_b

    elapsed = time.time() - t0

    def coverage_ci(cov_bool):
        p = float(cov_bool.mean())
        n = len(cov_bool)
        se = float(np.sqrt(p * (1 - p) / n))
        return dict(pokrycie=p, se=se, pokrycie_95pct_CI=(max(0.0, p - 1.96 * se), min(1.0, p + 1.96 * se)))

    out = dict(
        n_reps=N_REPS, B_inner_bootstrap=B_INNER, seed=SEED, elapsed_s=elapsed,
        lam_true=lam_true, k_true=1.0, theta_true=0.0,
        n_windows=len(windows), n_full_real=n_full_real,
        n_full_sim_mean=float(n_full_sim.mean()), n_full_sim_median=float(np.median(n_full_sim)),
        k_hat_mean=float(k_hats.mean()), k_hat_median=float(np.median(k_hats)), k_hat_sd=float(k_hats.std(ddof=1)),
        pokrycie_profil=coverage_ci(cover_profile),
        pokrycie_bootstrap=coverage_ci(cover_bootstrap),
        srednia_szerokosc_profil=float(np.nanmean(profile_widths)),
        srednia_szerokosc_bootstrap=float(np.nanmean(bootstrap_widths)),
        stosunek_szerokosci_bootstrap_do_profilu=float(np.nanmean(bootstrap_widths) / np.nanmean(profile_widths)),
        hipoteza_Code_potwierdzona_pokrycie_bootstrap_ponizej_95=bool(
            coverage_ci(cover_bootstrap)["pokrycie_95pct_CI"][1] < 0.95),
    )
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    with open("test6_s7_coverage_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test6_s7_coverage_wyniki.json")


if __name__ == "__main__":
    main()
