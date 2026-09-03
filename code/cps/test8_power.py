#!/usr/bin/env python3
"""
TEST 8 — §8 protokołu: symulacja mocy kontrastu epok (PRZED zamrożeniem/biegiem).

Mechanizm min(T,C) (D-031), reużyty bez zmian (`test7_estimate.simulate_dataset_test7`).
Struktura realna: okna administracyjne per państwo, osobno per epoka (12 państw z ekspozycją
przed 1914, suma 718; 13 państw po, suma 901 — z `test6_s7_intervals.csv`, dotyka WYŁĄCZNIE
sum ekspozycji per państwo/epoka, fakt egzogeniczny jak w D-031, nigdy wartości `t` realnych
zdarzeń).

Model: k_prawdziwe_przed=1,0 (baza neutralna), k_prawdziwe_po=1,0-Δ (kierunek zadeklarowany
przez autora: niższa po 1914). λ kalibrowane osobno per epoka na Σokno/n_zdarzeń_realnych
(48 dla przed, 62 dla po) — symulowana liczba zdarzeń ma zbiegać do tych wartości.

Statystyka: Δ_sim = k̂_po,sim − k̂_przed,sim (pulowany, dopasowany OSOBNO w każdej epoce).
Model zerowy: permutacja etykiet epoki MIĘDZY ODSTĘPAMI (nie państwami — statystyka jest
pulowana, protokół §5 dosłownie: "permutacja etykiet epoki między odstępami, z zachowaniem
liczebności obu epok"), z zachowaniem n_przed/n_po TEJ repliki. Wzór jednostronny
SKORYGOWANY (autor, wiadomość z 2 września): kierunek "niższa po 1914" ⇒ Δ_obs oczekiwane
UJEMNE ⇒ p liczy surogaty NIE WIĘKSZE od obserwacji: p=(1+#{Δ_sur≤Δ_obs})/(B+1).

Kompromis kosztowy (zmierzony): dopasowania permutacyjne pojedynczy start (nie domyślny
dwupunktowy wielostart `fit_pooled`) — punktowe oszacowania epoki (Δ_obs) zachowują pełny
wielostart. Ten sam wzorzec co `bootstrap_ci_k_pooled` gdzie indziej w projekcie.

STOP po tej symulacji — brak jakiegokolwiek dotknięcia realnych wartości `t` (tylko sumy
ekspozycji per państwo/epoka) i brak `--run-real`.
"""
from __future__ import annotations
import json, time
import numpy as np
import pandas as pd

import test6_weibull as w
import test7_estimate as e

SEED = w.RNG_SEED
N_OUTER = 150
B_PERM = 200
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


def one_rep(delta, lam_przed, lam_po, windows_przed, windows_po, rng, B_perm=B_PERM):
    t_p, ev_p, _ = e.simulate_dataset_test7(1.0, lam_przed, 0.0, windows_przed, rng)
    t_o, ev_o, _ = e.simulate_dataset_test7(1.0 - delta, lam_po, 0.0, windows_po, rng)
    kp = w.fit_pooled(t_p, ev_p)["k"]
    ko = w.fit_pooled(t_o, ev_o)["k"]
    delta_obs = ko - kp

    t_all = np.concatenate([t_p, t_o]); ev_all = np.concatenate([ev_p, ev_o])
    n_p, n_o = len(t_p), len(t_o); n_tot = n_p + n_o
    delta_sur = np.empty(B_perm)
    for b in range(B_perm):
        perm = rng.permutation(n_tot)
        ip, io = perm[:n_p], perm[n_p:]
        kps = w.fit_pooled(t_all[ip], ev_all[ip], x0_list=X0_SINGLE)["k"]
        kos = w.fit_pooled(t_all[io], ev_all[io], x0_list=X0_SINGLE)["k"]
        delta_sur[b] = kos - kps

    frac_tie = float(np.mean(np.abs(delta_sur - delta_obs) < 1e-6))
    p = (1 + int(np.sum(delta_sur <= delta_obs))) / (B_perm + 1)   # wzor skorygowany (autor)
    return delta_obs, p, frac_tie, n_p, n_o


def main():
    windows_przed, windows_po, n_przed_real, n_po_real = load_epoch_windows(1914)
    lam_przed = sum(windows_przed) / n_przed_real
    lam_po = sum(windows_po) / n_po_real

    out = dict(n_outer=N_OUTER, B_perm=B_PERM, seed=SEED,
              n_panstw_przed=len(windows_przed), n_panstw_po=len(windows_po),
              suma_okna_przed=sum(windows_przed), suma_okna_po=sum(windows_po),
              n_zdarzen_realnych_przed=n_przed_real, n_zdarzen_realnych_po=n_po_real,
              lam_przed=lam_przed, lam_po=lam_po, warianty={})

    rng = np.random.default_rng(SEED)
    t0 = time.time()
    for delta in DELTAS:
        deltas_obs = np.empty(N_OUTER)
        ps = np.empty(N_OUTER)
        frac_ties = np.empty(N_OUTER)
        n_p_sims = np.empty(N_OUTER, dtype=int)
        n_o_sims = np.empty(N_OUTER, dtype=int)
        for i in range(N_OUTER):
            d_obs, p, ft, n_p, n_o = one_rep(delta, lam_przed, lam_po, windows_przed, windows_po, rng)
            deltas_obs[i] = d_obs; ps[i] = p; frac_ties[i] = ft
            n_p_sims[i] = n_p; n_o_sims[i] = n_o
        rejrate = float(np.mean(ps < 0.05))
        out["warianty"][str(delta)] = dict(
            delta_true=delta,
            moc_p_lt_0_05=rejrate,
            moc_95pct_CI=(max(0.0, rejrate - 1.96 * np.sqrt(rejrate * (1 - rejrate) / N_OUTER)),
                         min(1.0, rejrate + 1.96 * np.sqrt(rejrate * (1 - rejrate) / N_OUTER))),
            delta_obs_mean=float(deltas_obs.mean()), delta_obs_median=float(np.median(deltas_obs)),
            delta_obs_sd=float(deltas_obs.std(ddof=1)),
            frac_tie_mean=float(frac_ties.mean()), frac_tie_max=float(frac_ties.max()),
            n_przed_sim_mean=float(n_p_sims.mean()), n_po_sim_mean=float(n_o_sims.mean()),
        )
        print(f"delta={delta}: moc(p<0.05)={rejrate:.3f}, delta_obs_mean={deltas_obs.mean():.4f}, "
             f"frac_tie_max={frac_ties.max():.4f}  ({time.time()-t0:.0f}s elapsed)")

    out["elapsed_s"] = time.time() - t0
    out["UWAGA_zakres"] = ("Moc liczona WYLACZNIE wg kryterium p<0.05 permutacyjnego (SS7 "
                           "czlon pierwszy). Drugi czlon reguly SS7 (nienakladajace sie "
                           "przedzialy ufnosci) NIE jest tu liczony z powodow kosztowych - "
                           "podana moc jest wiec GORNYM OGRANICZENIEM mocy pod pelna regula "
                           "SS7, nie jej dokladna wartoscia.")
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    with open("test8_power_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test8_power_wyniki.json")


if __name__ == "__main__":
    main()
