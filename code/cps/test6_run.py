#!/usr/bin/env python3
"""
TEST 6 — Krok 3: bieg na danych rzeczywistych (rodzina 9).
Realizuje TASK_6B_BRIEF.md §7-8. Odblokowane warunkiem D-022 (dodatek do suity poprawności
w test6_weibull.py, wykonany, bez ponownego przeglądu kodu — decyzja autora 2026-08-24).

Cztery dopasowania (brief §1): P1 (pulowany, ORZEKA) i F1 (kruchość, drugorzędny) na
test6_intervals.csv; S-A i S-B (pulowane) na wariantach wrażliwości. Dla każdego: profil
wiarygodności ORAZ bootstrap diadowy (B=2000, brief §4) — oba obowiązkowe, wartość punktowa
bez przedziału nie jest wynikiem. F1 raportuje dodatkowo `frac_theta_boundary` bootstrapu
(D-022) — jeśli wysoki, przedział dla kruchości nie jest interpretowalny.

Wyniki commitowane PRZED raportem (konwencja projektu) — ten skrypt tylko liczy i zapisuje
test6_results.csv; interpretacja (w tym reguła D-015 B/D-022 dla P1 vs F1) wchodzi do
TEST6_REPORT.md osobno.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import numpy as np
import pandas as pd

import test6_weibull as w

B_BOOTSTRAP = 2000


def fit_and_intervals(t, event, diad, model: str):
    """model: 'pooled' albo 'frailty'. Zwraca jeden wiersz wyników (dict)."""
    if model == "pooled":
        fit = w.fit_pooled(t, event)
        prof = w.profile_ci_k(w.negloglik_pooled, (t, event), fit["k"], [fit["loglam"]], fit["loglik"])
        lo, hi, ks = w.bootstrap_ci_k_pooled(t, event, diad, B=B_BOOTSTRAP)
        row = dict(model="pooled", k_hat=fit["k"], lam_hat=fit["lam"], loglik=fit["loglik"],
                  converged_same=fit["converged_same"], theta_hat=None, theta_at_boundary=None)
    else:
        fit = w.fit_frailty(t, event, diad)
        groups, gidx = np.unique(diad, return_inverse=True)
        prof = w.profile_ci_k(w.negloglik_frailty, (t, event, gidx, len(groups)), fit["k"],
                              [fit["loglam"], fit["logtheta"]], fit["loglik"])
        lo, hi, ks, frac_boundary = w.bootstrap_ci_k_frailty(t, event, diad, B=B_BOOTSTRAP)
        row = dict(model="frailty", k_hat=fit["k"], lam_hat=fit["lam"], loglik=fit["loglik"],
                  converged_same=fit["converged_same"], theta_hat=fit["theta"],
                  theta_at_boundary=fit["theta_at_boundary"])
    row.update(profile_lo=prof["lo"], profile_hi=prof["hi"],
              profile_lo_bounded=prof["lo_bounded"], profile_hi_bounded=prof["hi_bounded"],
              profile_anchor_lr=prof["anchor_lr"], profile_anchor_ok=prof["anchor_ok"],
              bootstrap_lo=lo, bootstrap_hi=hi, bootstrap_B=B_BOOTSTRAP)
    if model == "frailty":
        row["bootstrap_frac_theta_boundary"] = frac_boundary
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", default="test6_intervals.csv")
    ap.add_argument("--sa", default="test6_intervals_sensitivity_SA.csv")
    ap.add_argument("--sb", default="test6_intervals_sensitivity_SB.csv")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    od = Path(a.out_dir); od.mkdir(parents=True, exist_ok=True)

    rows = []
    sha = {}
    for path in (a.main, a.sa, a.sb):
        sha[Path(path).name] = hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]

    t, event, diad = w.load_variant(a.main)
    print(f"P1/F1 (main, n={len(t)}, diad={len(set(diad))})...")
    r = fit_and_intervals(t, event, diad, "pooled"); r["id"] = "P1"; rows.append(r)
    r = fit_and_intervals(t, event, diad, "frailty"); r["id"] = "F1"; rows.append(r)

    t, event, diad = w.load_variant(a.sa)
    print(f"S-A (n={len(t)}, diad={len(set(diad))})...")
    r = fit_and_intervals(t, event, diad, "pooled"); r["id"] = "S-A"; rows.append(r)

    t, event, diad = w.load_variant(a.sb)
    print(f"S-B (n={len(t)}, diad={len(set(diad))})...")
    r = fit_and_intervals(t, event, diad, "pooled"); r["id"] = "S-B"; rows.append(r)

    tab = pd.DataFrame(rows)[["id", "model", "k_hat", "lam_hat", "loglik", "converged_same",
                              "theta_hat", "theta_at_boundary",
                              "profile_lo", "profile_hi", "profile_lo_bounded", "profile_hi_bounded",
                              "profile_anchor_lr", "profile_anchor_ok",
                              "bootstrap_lo", "bootstrap_hi", "bootstrap_B",
                              "bootstrap_frac_theta_boundary"]]

    meta = {"runner": "test6_run.py v1.0", "krok": 3, "sha256": sha,
            "seed": w.RNG_SEED, "b_bootstrap": B_BOOTSTRAP,
            "warunek_d022": "wykonany przed biegiem, bez ponownego przegladu kodu (decyzja autora)"}
    with open(od / "test6_results.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        tab.to_csv(fh, index=False)

    print(tab.to_string(index=False))
    print(f"\nzapisano {od/'test6_results.csv'}")


if __name__ == "__main__":
    main()
