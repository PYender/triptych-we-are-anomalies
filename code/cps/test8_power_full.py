#!/usr/bin/env python3
"""
TEST 10 — §8 protokołu, symulacja mocy wg PEŁNEJ reguły §7 (oba człony naraz).

Rozszerza `test8_power.py` (D-050): ten sam mechanizm min(T,C), te same okna/kalibracja,
ten sam wzór permutacyjny (kierunkowy, skorygowany). DODATKOWO liczy drugi człon reguły §7 —
przedziały ufności PROFILOWE (nie bootstrap, D-045) dla k̂ w każdej epoce z osobna, na danych
TEJ repliki (nie permutowanych) — replika "odrzuca" pod PEŁNĄ regułą tylko jeśli p<0,05 ORAZ
przedziały profilowe obu epok się NIE nakładają.

Powód (autor, po przeglądzie D-050): przy podpróbach rzędu pięćdziesięciu zdarzeń przedziały
profilowe mają szerokość rzędu 0,4 — drugi człon jest przy tej liczebności warunkiem
znacznie ostrzejszym niż sama wartość p. Podana wcześniej moc (D-050) jest górnym
ograniczeniem; ta symulacja mierzy PEŁNĄ regułę, nie zgaduje jej.

Koszt kontrolowany: N_OUTER=150 (jak w D-050), B_PERM zmniejszone do 150 (z 200), profil
liczony raz na epokę na dane repliki (nie w pętli permutacyjnej — drugi człon nie wymaga
permutacji, tylko dopasowania obserwowanego w tej replice).
"""
from __future__ import annotations
import json, time
import numpy as np
import pandas as pd

import test6_weibull as w
import test7_estimate as e

SEED = w.RNG_SEED
N_OUTER = 150
B_PERM = 150
DELTAS = [0.0, 0.15, 0.25, 0.40]
X0_SINGLE = [(0.0, 3.0)]


def load_epoch_windows(cutoff=1914):
    iv = pd.read_csv("test6_s7_intervals.csv", comment="#")
    przed = iv[iv.rok_konca_poprz < cutoff]
    po = iv[iv.rok_konca_poprz >= cutoff]
    n_przed = int((przed.cenzurowany == 0).sum())
    n_po = int((po.cenzurowany == 0).sum())
    windows_przed = przed.groupby("ccode")["dlugosc_odstepu"].sum().tolist()
    windows_po = po.groupby("ccode")["dlugosc_odstepu"].sum().tolist()
    return windows_przed, windows_po, n_przed, n_po


def ci_no_overlap(t, event):
    fit = w.fit_pooled(t, event)
    prof = w.profile_ci_k(w.negloglik_pooled, (t, event), fit["k"], [fit["loglam"]], fit["loglik"])
    return fit["k"], prof["lo"], prof["hi"]


def one_rep(delta, lam_przed, lam_po, windows_przed, windows_po, rng, B_perm=B_PERM):
    t_p, ev_p, _ = e.simulate_dataset_test7(1.0, lam_przed, 0.0, windows_przed, rng)
    t_o, ev_o, _ = e.simulate_dataset_test7(1.0 - delta, lam_po, 0.0, windows_po, rng)

    k_przed, lo_przed, hi_przed = ci_no_overlap(t_p, ev_p)
    k_po, lo_po, hi_po = ci_no_overlap(t_o, ev_o)
    delta_obs = k_po - k_przed

    # nienakladajace sie przedzialy: hi_przed < lo_po (przed nizej) LUB hi_po < lo_przed
    bounded = not (np.isnan(lo_przed) or np.isnan(hi_przed) or np.isnan(lo_po) or np.isnan(hi_po))
    no_overlap = bool(bounded and (hi_przed < lo_po or hi_po < lo_przed))

    t_all = np.concatenate([t_p, t_o]); ev_all = np.concatenate([ev_p, ev_o])
    n_p, n_o = len(t_p), len(t_o); n_tot = n_p + n_o
    delta_sur = np.empty(B_perm)
    for b in range(B_perm):
        perm = rng.permutation(n_tot)
        ip, io = perm[:n_p], perm[n_p:]
        kps = w.fit_pooled(t_all[ip], ev_all[ip], x0_list=X0_SINGLE)["k"]
        kos = w.fit_pooled(t_all[io], ev_all[io], x0_list=X0_SINGLE)["k"]
        delta_sur[b] = kos - kps
    p = (1 + int(np.sum(delta_sur <= delta_obs))) / (B_perm + 1)

    p_ok = p < 0.05
    full_rule_reject = bool(p_ok and no_overlap)
    return dict(delta_obs=delta_obs, p=p, p_ok=p_ok, no_overlap=no_overlap,
               full_rule_reject=full_rule_reject, n_p=n_p, n_o=n_o)


def main():
    windows_przed, windows_po, n_przed_real, n_po_real = load_epoch_windows(1914)
    lam_przed = sum(windows_przed) / n_przed_real
    lam_po = sum(windows_po) / n_po_real

    out = dict(n_outer=N_OUTER, B_perm=B_PERM, seed=SEED, warianty={})
    rng = np.random.default_rng(SEED)
    t0 = time.time()
    for delta in DELTAS:
        recs = [one_rep(delta, lam_przed, lam_po, windows_przed, windows_po, rng) for _ in range(N_OUTER)]
        p_ok_rate = float(np.mean([r["p_ok"] for r in recs]))
        no_overlap_rate = float(np.mean([r["no_overlap"] for r in recs]))
        full_rate = float(np.mean([r["full_rule_reject"] for r in recs]))
        n = N_OUTER
        se_full = np.sqrt(full_rate * (1 - full_rate) / n)
        out["warianty"][str(delta)] = dict(
            delta_true=delta,
            moc_pierwszy_czlon_p_lt_0_05=p_ok_rate,
            frakcja_przedzialy_sie_nie_nakladaja=no_overlap_rate,
            moc_PELNA_regula_S7=full_rate,
            moc_PELNA_95pct_CI=(max(0.0, full_rate - 1.96 * se_full), min(1.0, full_rate + 1.96 * se_full)),
        )
        print(f"delta={delta}: p<0.05={p_ok_rate:.3f}, brak_nakladania={no_overlap_rate:.3f}, "
             f"PELNA_REGULA={full_rate:.3f}  ({time.time()-t0:.0f}s elapsed)")

    out["elapsed_s"] = time.time() - t0
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    with open("test8_power_full_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test8_power_full_wyniki.json")


if __name__ == "__main__":
    main()
