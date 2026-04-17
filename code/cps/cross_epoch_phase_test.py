# cross_epoch_phase_test.py – Out-of-sample phase validation for ~36-year war cycle
# Data: wars_color.csv
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# RATIONALE:
#   The epoch-folding and wavelet tests (epoch_folding_test.py, wavelet_phase_test.py)
#   fit null and signal to the SAME 192-year window. A high-order AR null can mimic
#   the alleged cycle, making the test conservative.
#
#   This script splits the record at SPLIT_YEAR (default 1914) into two independent
#   half-records and applies two complementary tests:
#
#   TEST 1 — Independent epoch-folding (Fisher combination)
#     Compute chi² epoch-folding statistic at T_HYP in each epoch separately,
#     each with its own AR(p) surrogate null. Combine p-values via Fisher's method:
#       X = -2 * (ln p1 + ln p2)  ~  χ²(4) under independence.
#     The combined p tests whether BOTH epochs independently show phase structure
#     at T_HYP — a much stronger claim than either alone.
#
#   TEST 2 — Out-of-sample prediction correlation
#     Fit a sinusoid A*cos(2π·t/T_HYP) + B*sin(2π·t/T_HYP) + C to wars_smooth in
#     epoch 1. This gives amplitude and phase from epoch 1 alone. Then compute the
#     correlation between that prediction and wars_smooth in epoch 2 (unseen data).
#     Null: AR(p) surrogates of epoch 2 correlated with the same fixed prediction.
#     p = P(null_corr ≥ obs_corr | H₀).
#     A significant positive correlation means the phase estimated in epoch 1
#     successfully predicts the rhythm in epoch 2 — a genuine out-of-sample test.
#
# OUTPUT:
#   cross_epoch_phase_test.pdf
#   cross_epoch_phase_test_results.csv

from __future__ import annotations

import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import detrend
from scipy.stats import chi2 as chi2_dist

sys.path.insert(0, str(Path(__file__).parent))
from spectral_significance_v2 import apply_ma, generate_surrogate
from statsmodels.tsa.ar_model import AutoReg

warnings.filterwarnings("ignore")

RNG      = np.random.default_rng(20240301)
B        = 2000
ALPHA    = 0.05
MA_WIN   = 11
T_HYP    = 35.1
N_BINS   = 10
SPLIT_YEAR = 1914


# ─────────────────────────────────────────────────────────────────────────────
# helpers (mirrors spectral_significance_v2 so no cross-imports needed)
# ─────────────────────────────────────────────────────────────────────────────

def fit_ar(x: np.ndarray, max_lag: int = 20) -> tuple:
    """Fit AR(p) by AIC, capped at max_lag and N//5."""
    best, best_p, best_res, best_fit = np.inf, 1, None, None
    cap = min(max_lag, len(x) // 5)
    for p in range(1, cap + 1):
        try:
            fit = AutoReg(x, lags=p, old_names=False).fit()
            if fit.aic < best:
                best, best_p, best_res, best_fit = fit.aic, p, fit.resid, fit
        except Exception:
            pass
    return best_fit, best_p, best_res


def epoch_fold(x: np.ndarray, years: np.ndarray,
               T: float, n_bins: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Epoch-fold x at period T; returns (bin_means, bin_counts, chi2)."""
    phases  = (years.astype(float) % T) / T
    bin_idx = (phases * n_bins).astype(int) % n_bins
    m_global = x.mean()
    var_g    = x.var()
    N        = len(x)
    m_k = np.array([x[bin_idx == k].mean() if (bin_idx == k).any()
                    else m_global for k in range(n_bins)])
    n_k = np.array([(bin_idx == k).sum() for k in range(n_bins)])
    chi2 = (n_k * (m_k - m_global) ** 2).sum() / (var_g + 1e-30)
    return m_k, n_k, float(chi2)


def sinusoid_fit(x: np.ndarray, t: np.ndarray, T: float) -> np.ndarray:
    """OLS fit: x ≈ a·cos(2πt/T) + b·sin(2πt/T) + c. Returns prediction."""
    A = np.column_stack([np.cos(2 * np.pi * t / T),
                         np.sin(2 * np.pi * t / T),
                         np.ones(len(t))])
    coef, _, _, _ = np.linalg.lstsq(A, x, rcond=None)
    return A @ coef, coef


# ─────────────────────────────────────────────────────────────────────────────
# Test 1: independent epoch-folding + Fisher combination
# ─────────────────────────────────────────────────────────────────────────────

def run_epoch_test(years: np.ndarray, wars_raw: np.ndarray,
                   wars_smooth: np.ndarray, label: str,
                   n_boot: int, max_ar: int) -> dict:
    N = len(wars_raw)
    x_smooth = detrend(wars_smooth.astype(float), type="linear")
    x_raw    = detrend(wars_raw.astype(float),    type="linear")

    _, _, chi2_obs = epoch_fold(x_smooth, years, T_HYP, N_BINS)

    ar_fit, ar_p, ar_resid = fit_ar(x_raw, max_lag=min(max_ar, N // 5))
    raw_std = x_raw.std()

    boot_chi2 = np.zeros(n_boot)
    for b in range(n_boot):
        surr    = generate_surrogate(ar_fit, ar_resid, N, RNG)
        surr    = surr / (surr.std() + 1e-12) * raw_std
        surr_sm = apply_ma(surr, MA_WIN)
        x_s     = detrend(surr_sm, type="linear")
        _, _, boot_chi2[b] = epoch_fold(x_s, years, T_HYP, N_BINS)

    p = float((boot_chi2 >= chi2_obs).mean())
    return {"label": label, "N": N, "ar_p": ar_p,
            "chi2_obs": chi2_obs, "boot_chi2": boot_chi2, "p": p}


# ─────────────────────────────────────────────────────────────────────────────
# Test 2: out-of-sample prediction correlation
# ─────────────────────────────────────────────────────────────────────────────

def run_prediction_test(years1: np.ndarray, wars_raw1: np.ndarray,
                        wars_smooth1: np.ndarray,
                        years2: np.ndarray, wars_raw2: np.ndarray,
                        wars_smooth2: np.ndarray,
                        n_boot: int, max_ar: int) -> dict:
    N1 = len(years1)
    N2 = len(years2)

    x1 = detrend(wars_smooth1.astype(float), type="linear")
    x2 = detrend(wars_smooth2.astype(float), type="linear")

    # sinusoid fit from epoch 1 (using relative time index)
    t1 = np.arange(N1, dtype=float)
    _, coef1 = sinusoid_fit(x1, t1, T_HYP)

    # evaluate prediction on epoch 2 time grid (continuity of phase)
    t2 = np.arange(N1, N1 + N2, dtype=float)
    A2 = np.column_stack([np.cos(2 * np.pi * t2 / T_HYP),
                          np.sin(2 * np.pi * t2 / T_HYP),
                          np.ones(N2)])
    pred2 = A2 @ coef1          # fixed prediction from epoch 1

    obs_corr = float(np.corrcoef(pred2, x2)[0, 1])

    # null: AR surrogate of epoch-2 raw, correlated with same fixed prediction
    x2_raw = detrend(wars_raw2.astype(float), type="linear")
    ar_fit2, ar_p2, ar_resid2 = fit_ar(x2_raw, max_lag=min(max_ar, N2 // 5))
    raw_std2 = x2_raw.std()

    boot_corr = np.zeros(n_boot)
    for b in range(n_boot):
        surr    = generate_surrogate(ar_fit2, ar_resid2, N2, RNG)
        surr    = surr / (surr.std() + 1e-12) * raw_std2
        surr_sm = apply_ma(surr, MA_WIN)
        x_s     = detrend(surr_sm, type="linear")
        boot_corr[b] = np.corrcoef(pred2, x_s)[0, 1]

    p = float((boot_corr >= obs_corr).mean())
    return {"ar_p2": ar_p2, "coef1": coef1,
            "pred2": pred2, "x2": x2, "t2": t2,
            "obs_corr": obs_corr, "boot_corr": boot_corr, "p": p}


# ─────────────────────────────────────────────────────────────────────────────
# Fisher combination
# ─────────────────────────────────────────────────────────────────────────────

def fisher_p(p1: float, p2: float) -> float:
    """Fisher's combined probability: X = -2*(ln p1 + ln p2) ~ χ²(4)."""
    p1 = max(p1, 1e-6)
    p2 = max(p2, 1e-6)
    X  = -2.0 * (np.log(p1) + np.log(p2))
    return float(1.0 - chi2_dist.cdf(X, df=4))


# ─────────────────────────────────────────────────────────────────────────────
# plot
# ─────────────────────────────────────────────────────────────────────────────

def plot_results(r1: dict, r2: dict, pred: dict,
                 years1: np.ndarray, years2: np.ndarray,
                 out_path: str) -> None:

    C1 = "#e35208"   # epoch 1
    C2 = "#1869b5"   # epoch 2
    CN = "#888888"   # null

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.subplots_adjust(hspace=0.42, wspace=0.35)

    # ── Panel A: epoch-1 chi² null distribution ──────────────────────────────
    ax = axes[0, 0]
    ax.hist(r1["boot_chi2"], bins=60, density=True, color=CN, alpha=0.65,
            label="Null AR(p)")
    ax.axvline(r1["chi2_obs"], color=C1, lw=2,
               label=f"Obs χ² = {r1['chi2_obs']:.2f}")
    q95 = float(np.quantile(r1["boot_chi2"], 0.95))
    ax.axvline(q95, color="black", lw=1.2, ls="--",
               label=f"Null 95th = {q95:.2f}")
    sig = "SIGN." if r1["p"] < ALPHA else "n.s."
    ax.set_title(f"(A) Epoch-fold: {r1['label']}\n"
                 f"AR({r1['ar_p']}), p = {r1['p']:.4f}  [{sig}]", fontsize=9)
    ax.set_xlabel("χ²"); ax.set_ylabel("Density"); ax.legend(fontsize=7.5)

    # ── Panel B: epoch-2 chi² null distribution ──────────────────────────────
    ax = axes[0, 1]
    ax.hist(r2["boot_chi2"], bins=60, density=True, color=CN, alpha=0.65,
            label="Null AR(p)")
    ax.axvline(r2["chi2_obs"], color=C2, lw=2,
               label=f"Obs χ² = {r2['chi2_obs']:.2f}")
    q95 = float(np.quantile(r2["boot_chi2"], 0.95))
    ax.axvline(q95, color="black", lw=1.2, ls="--",
               label=f"Null 95th = {q95:.2f}")
    sig = "SIGN." if r2["p"] < ALPHA else "n.s."
    ax.set_title(f"(B) Epoch-fold: {r2['label']}\n"
                 f"AR({r2['ar_p']}), p = {r2['p']:.4f}  [{sig}]", fontsize=9)
    ax.set_xlabel("χ²"); ax.legend(fontsize=7.5)

    # ── Panel C: prediction correlation null distribution ────────────────────
    ax = axes[0, 2]
    ax.hist(pred["boot_corr"], bins=60, density=True, color=CN, alpha=0.65,
            label=f"Null AR({pred['ar_p2']})")
    ax.axvline(pred["obs_corr"], color=C2, lw=2,
               label=f"Obs corr = {pred['obs_corr']:.4f}")
    q95c = float(np.quantile(pred["boot_corr"], 0.95))
    ax.axvline(q95c, color="black", lw=1.2, ls="--",
               label=f"Null 95th = {q95c:.4f}")
    sig = "SIGN." if pred["p"] < ALPHA else "n.s."
    ax.set_title(f"(C) Out-of-sample corr (epoch 2)\n"
                 f"p = {pred['p']:.4f}  [{sig}]", fontsize=9)
    ax.set_xlabel("Correlation"); ax.legend(fontsize=7.5)

    # ── Panel D: sinusoid fit in epoch 1 ─────────────────────────────────────
    ax = axes[1, 0]
    t1 = np.arange(len(years1), dtype=float)
    A1_mat = np.column_stack([np.cos(2 * np.pi * t1 / T_HYP),
                               np.sin(2 * np.pi * t1 / T_HYP),
                               np.ones(len(t1))])
    pred1 = A1_mat @ pred["coef1"]
    ax.plot(years1, pred["x1"], color=C1, lw=1.4, label="Observed (detrended)")
    ax.plot(years1, pred1, color="black", lw=1.8, ls="--",
            label=f"Fit A·sin(2π·t/{T_HYP}+φ)")
    ax.set_title(f"(D) Sinusoid fit — epoch 1 ({years1[0]}–{years1[-1]})\n"
                 f"Phase and amplitude locked here, tested in epoch 2", fontsize=9)
    ax.set_xlabel("Year"); ax.set_ylabel("wars_smooth (detrended)")
    ax.legend(fontsize=7.5)

    # ── Panel E: prediction vs observed in epoch 2 ───────────────────────────
    ax = axes[1, 1]
    ax.plot(years2, pred["x2"], color=C2, lw=1.4, label="Observed (detrended)")
    ax.plot(years2, pred["pred2"], color="black", lw=1.8, ls="--",
            label="Prediction from epoch 1")
    ax.axvline(years2[0], color="grey", lw=0.8, ls=":")
    ax.set_title(f"(E) Out-of-sample prediction — epoch 2 ({years2[0]}–{years2[-1]})\n"
                 f"corr = {pred['obs_corr']:.4f},  p = {pred['p']:.4f}", fontsize=9)
    ax.set_xlabel("Year")
    ax.legend(fontsize=7.5)

    # ── Panel F: scatter observed vs predicted (epoch 2) ─────────────────────
    ax = axes[1, 2]
    ax.scatter(pred["pred2"], pred["x2"], s=12, color=C2, alpha=0.6)
    lo = min(pred["pred2"].min(), pred["x2"].min())
    hi = max(pred["pred2"].max(), pred["x2"].max())
    ax.plot([lo, hi], [lo, hi], "k--", lw=1)
    ax.set_title(f"(F) Scatter: pred vs obs (epoch 2)\n"
                 f"corr = {pred['obs_corr']:.4f}", fontsize=9)
    ax.set_xlabel("Prediction (from epoch 1)")
    ax.set_ylabel("Observed (epoch 2)")

    p_fisher = fisher_p(r1["p"], r2["p"])
    plt.suptitle(
        f"CPS — Cross-epoch out-of-sample phase test  |  Split: {SPLIT_YEAR}\n"
        f"T_hyp = {T_HYP} yr  |  Fisher p (epoch 1+2 combined) = {p_fisher:.4f}  "
        f"{'[SIGNIFICANT]' if p_fisher < ALPHA else '[not significant]'}\n"
        f"Out-of-sample corr p = {pred['p']:.4f}  |  Null: AR(AIC) surrogates, B={B}",
        fontsize=10.5, y=1.01,
    )
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# summary
# ─────────────────────────────────────────────────────────────────────────────

def print_and_save(r1: dict, r2: dict, pred: dict,
                   csv_path: str) -> None:
    SEP  = "═" * 70
    sep2 = "─" * 70
    p_fisher = fisher_p(r1["p"], r2["p"])

    print(f"\n{SEP}")
    print(f"  CROSS-EPOCH TEST  (split {SPLIT_YEAR})")
    print(SEP)
    print(f"  TEST 1a — Epoch-fold epoch 1 ({r1['label']}, n={r1['N']}, AR({r1['ar_p']}))")
    print(f"    χ²_obs = {r1['chi2_obs']:.3f},  p = {r1['p']:.4f}  "
          f"[{'SIGNIFICANT' if r1['p'] < ALPHA else 'NOT significant'}]")
    print(sep2)
    print(f"  TEST 1b — Epoch-fold epoch 2 ({r2['label']}, n={r2['N']}, AR({r2['ar_p']}))")
    print(f"    χ²_obs = {r2['chi2_obs']:.3f},  p = {r2['p']:.4f}  "
          f"[{'SIGNIFICANT' if r2['p'] < ALPHA else 'NOT significant'}]")
    print(sep2)
    print(f"  FISHER COMBINED  p = {p_fisher:.4f}  "
          f"[{'SIGNIFICANT' if p_fisher < ALPHA else 'NOT significant'}]")
    print(SEP)
    print(f"  TEST 2 — Out-of-sample prediction corr (epoch 2, AR({pred['ar_p2']}) null)")
    print(f"    Observed corr = {pred['obs_corr']:.6f}")
    print(f"    Null 95th pct = {np.quantile(pred['boot_corr'], 0.95):.6f}")
    print(f"    p = P(null ≥ obs) = {pred['p']:.4f}  "
          f"[{'SIGNIFICANT' if pred['p'] < ALPHA else 'NOT significant'}]")
    print(SEP)

    df = pd.DataFrame([{
        "split_year":        SPLIT_YEAR,
        "T_hyp_yr":          T_HYP,
        "epoch1_label":      r1["label"],
        "epoch1_n":          r1["N"],
        "epoch1_ar_p":       r1["ar_p"],
        "epoch1_chi2_obs":   round(r1["chi2_obs"], 4),
        "epoch1_p":          round(r1["p"], 4),
        "epoch2_label":      r2["label"],
        "epoch2_n":          r2["N"],
        "epoch2_ar_p":       r2["ar_p"],
        "epoch2_chi2_obs":   round(r2["chi2_obs"], 4),
        "epoch2_p":          round(r2["p"], 4),
        "fisher_p":          round(p_fisher, 4),
        "fisher_significant": p_fisher < ALPHA,
        "pred_corr_obs":     round(pred["obs_corr"], 6),
        "pred_corr_p":       round(pred["p"], 4),
        "pred_corr_significant": pred["p"] < ALPHA,
    }])
    df.to_csv(csv_path, index=False)
    print(f"✓ Saved {csv_path}")


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Cross-epoch out-of-sample phase test for ~36-year war cycle"
    )
    parser.add_argument("csv", nargs="?", default="wars_color.csv")
    parser.add_argument("--boot",     type=int, default=B)
    parser.add_argument("--split",    type=int, default=SPLIT_YEAR,
                        help="Year to split epochs (default: 1914)")
    parser.add_argument("--max-lag",  type=int, default=20,
                        help="Max AR order (default: 20)")
    args    = parser.parse_args()
    B_run   = args.boot
    SPLIT_YEAR = args.split
    max_ar  = args.max_lag
    out_dir = Path(args.csv).parent

    df = pd.read_csv(args.csv).set_index("year").sort_index()
    df = df[df.index >= 1816]

    m1 = df.index < SPLIT_YEAR
    m2 = df.index >= SPLIT_YEAR

    def get_arrays(mask):
        sub = df[mask]
        return (sub.index.values,
                sub["wars"].values.astype(float),
                sub["wars_smooth"].values.astype(float))

    years1, raw1, sm1 = get_arrays(m1)
    years2, raw2, sm2 = get_arrays(m2)

    label1 = f"{years1[0]}–{years1[-1]}"
    label2 = f"{years2[0]}–{years2[-1]}"

    print(f"{'='*70}")
    print(f"  Cross-epoch test  |  split: {SPLIT_YEAR}  |  max_lag: {max_ar}  |  B: {B_run}")
    print(f"  Epoch 1: {label1}  (n={len(years1)})")
    print(f"  Epoch 2: {label2}  (n={len(years2)})")
    print(f"{'='*70}")

    print("  → Test 1a: epoch-folding on epoch 1 …")
    r1 = run_epoch_test(years1, raw1, sm1, label1, B_run, max_ar)

    print("  → Test 1b: epoch-folding on epoch 2 …")
    r2 = run_epoch_test(years2, raw2, sm2, label2, B_run, max_ar)

    print("  → Test 2: out-of-sample prediction correlation …")

    # epoch-1 detrended smooth (needed for plot panel D)
    x1 = detrend(sm1.astype(float), type="linear")
    t1 = np.arange(len(years1), dtype=float)
    A1_mat = np.column_stack([np.cos(2 * np.pi * t1 / T_HYP),
                               np.sin(2 * np.pi * t1 / T_HYP),
                               np.ones(len(t1))])
    _, coef1 = sinusoid_fit(x1, t1, T_HYP)

    pred_result = run_prediction_test(
        years1, raw1, sm1, years2, raw2, sm2, B_run, max_ar
    )
    pred_result["x1"] = x1   # add for plotting

    print_and_save(r1, r2, pred_result,
                   csv_path=str(out_dir / "cross_epoch_phase_test_results.csv"))
    plot_results(r1, r2, pred_result, years1, years2,
                 out_path=str(out_dir / "cross_epoch_phase_test.pdf"))
