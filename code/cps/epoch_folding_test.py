# epoch_folding_test.py – Epoch-folding phase-coherence test for ~36-year war cycle
# Data: wars_color.csv
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# RATIONALE:
#   spectral_significance_v2.py tested AMPLITUDE (band power, peak PSD) against
#   an AR null. The Triptych model, however, claims PHASE STABILITY with variable
#   amplitude: nuclear deterrence and institutional architecture dampen the
#   amplitude of the cycle post-1945 while preserving its rhythm (pages 52–78).
#   Amplitude-based tests are therefore misaligned with the model's core claim.
#
#   Epoch-folding tests PHASE COHERENCE directly:
#     – If a cycle of period T exists, folding the series on T and averaging
#       across epochs produces a structured profile (recurring peak + trough).
#     – If there is no cycle, folding on any T produces a flat profile.
#     – Crucially: the test is insensitive to epoch-to-epoch amplitude variation.
#       Each epoch contributes its shape regardless of local amplitude level.
#
# DESIGN:
#   1. Detrend wars_smooth (linear) within each analysis window.
#   2. Fold on T_HYP = 35.1 yr (Triptych's sin-fit period) into N_BINS = 10 bins
#      → ~5–6 observations per bin for n = 192, ~2–3 for n = 90.
#   3. Test statistic:
#        chi2 = Σ_k  n_k · (m_k − m_global)² / var_global
#      → weighted squared deviation of each bin mean from the grand mean,
#        normalised by total variance. Measures how much of the total variance
#        is "explained" by a repeating period-T profile.
#   4. Null: AR(p) surrogate wars_raw (AIC selection, same as v2) → MA(11)
#      → fold → chi2_null. Same AR-bootstrap pipeline and seed as v2.
#   5. Period scan: T ∈ [28, 48] yr in 0.5-yr steps.
#      Primary test at T_HYP (pre-specified). Scan is exploratory; p-values
#      reported uncorrected (no claim of discovery).
#   6. Two windows: Full 1816–2007 (n = 192) and Post-WWI 1918–2007 (n = 90).
#
# OUTPUT:
#   epoch_folding_test.pdf
#   epoch_folding_test_results.csv

from __future__ import annotations

import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from scipy.signal import detrend

# ── Import AR-bootstrap helpers (identical pipeline to spectral_significance_v2) ─
sys.path.insert(0, str(Path(__file__).parent))
from spectral_significance_v2 import apply_ma, generate_surrogate
from statsmodels.tsa.ar_model import AutoReg

warnings.filterwarnings("ignore")


def fit_ar_criterion(x: np.ndarray, max_lag: int = 20,
                     criterion: str = "aic"):
    """Fit AR(p) to x, select p by AIC or BIC. Returns (fit, p, residuals)."""
    best_val, best_p, best_res, best_fit = np.inf, 1, None, None
    cap = min(max_lag, len(x) // 5)
    for p in range(1, cap + 1):
        try:
            fit = AutoReg(x, lags=p, old_names=False).fit()
            val = fit.bic if criterion == "bic" else fit.aic
            if val < best_val:
                best_val, best_p, best_res, best_fit = val, p, fit.resid, fit
        except Exception:
            pass
    return best_fit, best_p, best_res


RNG    = np.random.default_rng(20240301)   # same seed as spectral_significance_v2
B      = 2000
ALPHA  = 0.05
MA_WIN = 11
T_HYP  = 35.1                             # Triptych sin-fit period [yr]
N_BINS = 10                               # phase bins (balanced with available cycles)
T_SCAN = np.arange(28.0, 48.5, 0.5)      # exploratory period scan [yr]


# ─────────────────────────────────────────────────────────────────────────────
# epoch-folding core
# ─────────────────────────────────────────────────────────────────────────────

def epoch_fold(x: np.ndarray, years: np.ndarray,
               T: float, n_bins: int = N_BINS) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Fold detrended series x on period T.

    Parameters
    ----------
    x     : detrended signal (1D, length N)
    years : integer year array aligned with x
    T     : folding period [yr]
    n_bins: number of phase bins

    Returns
    -------
    m_k   : bin means      (n_bins,)
    n_k   : bin counts     (n_bins,)
    chi2  : test statistic = Σ_k n_k·(m_k − m_global)² / var_global

    Interpretation
    --------------
    chi2 large  → folded profile is structured   → evidence for period-T cycle
    chi2 ≈ 0    → folded profile is flat         → no period-T coherence
    """
    phases  = (years.astype(float) % T) / T      # ∈ [0, 1)
    bin_idx = (phases * n_bins).astype(int) % n_bins

    m_global   = x.mean()
    var_global = x.var()
    N          = len(x)

    m_k = np.array([
        x[bin_idx == k].mean() if (bin_idx == k).any() else m_global
        for k in range(n_bins)
    ])
    n_k = np.array([(bin_idx == k).sum() for k in range(n_bins)])

    if var_global < 1e-12 or N == 0:
        return m_k, n_k, 0.0

    chi2 = float(np.sum(n_k * (m_k - m_global) ** 2) / var_global)
    return m_k, n_k, chi2


# ─────────────────────────────────────────────────────────────────────────────
# main test
# ─────────────────────────────────────────────────────────────────────────────

def run_test(years: np.ndarray, wars_raw: np.ndarray, wars_smooth: np.ndarray,
             label: str, n_boot: int = B, criterion: str = "aic") -> dict:
    """
    Full epoch-folding test with AR(p) surrogate null.

    Null H₀ : wars_raw is an AR(p) process (no embedded periodicity).
    Surrogates: AR(p) wars_raw → MA(11) → detrend → fold at same T.

    Primary test : T = T_HYP (pre-specified, one p-value).
    Scan         : T ∈ T_SCAN (exploratory, uncorrected p-values).
    """
    N        = len(wars_raw)
    x_smooth = detrend(wars_smooth.astype(float), type="linear")

    # ── observed statistics ──────────────────────────────────────────────────
    m_obs, n_obs, chi2_obs = epoch_fold(x_smooth, years, T_HYP, N_BINS)

    scan_chi2_obs = np.array([
        epoch_fold(x_smooth, years, T, N_BINS)[2] for T in T_SCAN
    ])

    # ── AR(p) surrogate null ─────────────────────────────────────────────────
    x_raw = detrend(wars_raw.astype(float), type="linear")
    ar_fit, ar_p, ar_resid = fit_ar_criterion(x_raw, max_lag=min(20, N // 5),
                                               criterion=criterion)
    raw_std = x_raw.std()

    boot_chi2_primary = np.zeros(n_boot)
    boot_scan_chi2    = np.zeros((n_boot, len(T_SCAN)))
    boot_profiles     = np.zeros((n_boot, N_BINS))   # for null profile envelope

    for b in range(n_boot):
        surr_raw = generate_surrogate(ar_fit, ar_resid, N, RNG)
        surr_raw = surr_raw / (surr_raw.std() + 1e-12) * raw_std
        surr_sm  = apply_ma(surr_raw, MA_WIN)
        x_surr   = detrend(surr_sm, type="linear")

        m_b, _, chi2_b          = epoch_fold(x_surr, years, T_HYP, N_BINS)
        boot_chi2_primary[b]    = chi2_b
        boot_profiles[b]        = m_b
        boot_scan_chi2[b]       = np.array([
            epoch_fold(x_surr, years, T, N_BINS)[2] for T in T_SCAN
        ])

    p_primary = float((boot_chi2_primary >= chi2_obs).mean())

    scan_env_lo = np.percentile(boot_scan_chi2, 5,  axis=0)
    scan_env_hi = np.percentile(boot_scan_chi2, 95, axis=0)
    scan_env_99 = np.percentile(boot_scan_chi2, 99, axis=0)
    scan_p      = np.array([
        float((boot_scan_chi2[:, i] >= scan_chi2_obs[i]).mean())
        for i in range(len(T_SCAN))
    ])

    # per-bin null envelope for folded profile
    prof_env_lo = np.percentile(boot_profiles, 5,  axis=0)
    prof_env_hi = np.percentile(boot_profiles, 95, axis=0)

    # index of T_HYP in the scan (nearest)
    hyp_idx = int(np.argmin(np.abs(T_SCAN - T_HYP)))

    return {
        "label":             label,
        "criterion":         criterion,
        "N":                 N,
        "ar_p":              ar_p,
        "years":             years,
        "x_smooth":          x_smooth,
        "T_hyp":             T_HYP,
        "n_bins":            N_BINS,
        "m_obs":             m_obs,
        "n_obs":             n_obs,
        "chi2_obs":          chi2_obs,
        "boot_chi2_primary": boot_chi2_primary,
        "p_primary":         p_primary,
        "prof_env_lo":       prof_env_lo,
        "prof_env_hi":       prof_env_hi,
        "T_scan":            T_SCAN,
        "scan_chi2_obs":     scan_chi2_obs,
        "scan_env_lo":       scan_env_lo,
        "scan_env_hi":       scan_env_hi,
        "scan_env_99":       scan_env_99,
        "scan_p":            scan_p,
        "hyp_idx":           hyp_idx,
    }


# ─────────────────────────────────────────────────────────────────────────────
# plot
# ─────────────────────────────────────────────────────────────────────────────

def plot_results(results: list[dict], out_path: str) -> None:
    n_rows = len(results)
    fig = plt.figure(figsize=(16, 5.5 * n_rows))
    gs  = gridspec.GridSpec(n_rows, 3, figure=fig, hspace=0.56, wspace=0.40)

    colours = ["steelblue", "firebrick"]

    for row, r in enumerate(results):
        C     = colours[row]
        label = r["label"]
        T_bin = np.linspace(0, r["T_hyp"], r["n_bins"], endpoint=False)
        bin_w = r["T_hyp"] / r["n_bins"]

        # ── Panel A: folded profile ──────────────────────────────────────────
        ax_a = fig.add_subplot(gs[row, 0])

        ax_a.fill_between(
            T_bin + bin_w / 2,
            r["prof_env_lo"], r["prof_env_hi"],
            color="grey", alpha=0.30, label=f"Null 5–95% (AR({r['ar_p']}), B={B})",
            step="mid",
        )
        ax_a.bar(
            T_bin + bin_w / 2, r["m_obs"],
            width=bin_w * 0.80, color=C, alpha=0.80,
            label="Observed profile", zorder=3,
        )
        ax_a.axhline(0, color="grey", lw=0.8, ls=":")
        ax_a.set_xlabel(f"Phase within T = {r['T_hyp']:.1f} yr  [yr]")
        ax_a.set_ylabel("wars_smooth detrended (mean per bin)")
        sig_str = "SIGNIFICANT" if r["p_primary"] < ALPHA else "n.s."
        ax_a.set_title(
            f"(A) Folded profile — {label}\n"
            f"χ² = {r['chi2_obs']:.2f},  p = {r['p_primary']:.3f}  [{sig_str}]",
            fontsize=9,
        )
        ax_a.legend(fontsize=7.5)

        # ── Panel B: period scan ─────────────────────────────────────────────
        ax_b = fig.add_subplot(gs[row, 1])

        ax_b.fill_between(r["T_scan"], r["scan_env_lo"], r["scan_env_hi"],
                          color="grey", alpha=0.25,
                          label="Null 5–95%")
        ax_b.plot(r["T_scan"], r["scan_env_99"],
                  color="grey", lw=1.0, ls=":", alpha=0.7,
                  label="Null 99th pct")
        ax_b.plot(r["T_scan"], r["scan_chi2_obs"],
                  color=C, lw=1.8, label="Observed χ²(T)")

        # mark T_HYP
        ax_b.axvline(r["T_hyp"], color="darkgreen", lw=1.2, ls="--",
                     label=f"T_hyp = {r['T_hyp']:.1f} yr")

        # mark scan maximum
        scan_max_idx = int(np.argmax(r["scan_chi2_obs"]))
        T_max        = r["T_scan"][scan_max_idx]
        chi2_max     = r["scan_chi2_obs"][scan_max_idx]
        p_max        = r["scan_p"][scan_max_idx]
        ax_b.plot(T_max, chi2_max, "o", color=C, ms=7,
                  label=f"Scan max T={T_max:.1f} yr, p={p_max:.3f} (uncorr.)")

        ax_b.set_xlabel("Folding period T  [yr]")
        ax_b.set_ylabel("χ²(T)")
        ax_b.set_title(
            f"(B) Period scan — {label}\n"
            f"χ²(T_hyp={r['T_hyp']:.1f}) = {r['scan_chi2_obs'][r['hyp_idx']]:.2f}  |  "
            f"Scan max at T={T_max:.1f} yr",
            fontsize=9,
        )
        ax_b.legend(fontsize=7.0, loc="upper left")

        # ── Panel C: bootstrap distribution ─────────────────────────────────
        ax_c = fig.add_subplot(gs[row, 2])

        ax_c.hist(r["boot_chi2_primary"], bins=50, color="grey",
                  alpha=0.55, density=True,
                  label=f"Null AR({r['ar_p']}) surrogates")
        ax_c.axvline(r["chi2_obs"], color=C, lw=2.0,
                     label=f"Observed χ² = {r['chi2_obs']:.2f}")
        q95 = float(np.quantile(r["boot_chi2_primary"], 0.95))
        ax_c.axvline(q95, color="black", lw=1.2, ls="--",
                     label=f"Null 95th pct = {q95:.2f}")
        ax_c.set_xlabel(f"χ²  (T = {r['T_hyp']:.1f} yr)")
        ax_c.set_ylabel("Density")
        ax_c.set_title(
            f"(C) Null distribution — {label}\n"
            f"p = {r['p_primary']:.4f}  →  "
            f"{'SIGNIFICANT' if r['p_primary'] < ALPHA else 'not significant'}",
            fontsize=9,
        )
        ax_c.legend(fontsize=7.5)

    criterion_used = results[0].get("criterion", "aic").upper()
    plt.suptitle(
        f"CPS — Epoch-folding phase-coherence test for ~36-year war cycle  [{criterion_used} null]\n"
        "Null: AR(p) surrogate wars_raw → MA(11) → fold at T_hyp = 35.1 yr\n"
        "Tests PHASE STABILITY (not amplitude) — aligned with Triptych model claim",
        fontsize=10.5, y=1.01,
    )
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# summary print + CSV
# ─────────────────────────────────────────────────────────────────────────────

def print_and_save(results: list[dict], csv_path: str) -> None:
    SEP  = "═" * 70
    sep2 = "─" * 70

    rows = []
    for r in results:
        scan_max_idx = int(np.argmax(r["scan_chi2_obs"]))
        T_max        = float(r["T_scan"][scan_max_idx])
        chi2_max     = float(r["scan_chi2_obs"][scan_max_idx])
        p_max        = float(r["scan_p"][scan_max_idx])
        q95          = float(np.quantile(r["boot_chi2_primary"], 0.95))

        print(f"\n{SEP}")
        print(f"  Window : {r['label']}  (n = {r['N']}, AR({r['ar_p']}))")
        print(f"  T_hyp  : {r['T_hyp']:.1f} yr  |  N_bins = {r['n_bins']}"
              f"  (~{r['N'] / r['T_hyp']:.1f} complete cycles)")
        print(sep2)
        print(f"  PRIMARY TEST  (T = {r['T_hyp']:.1f} yr)")
        print(f"    χ²_obs  = {r['chi2_obs']:.3f}")
        print(f"    Null 95th pct = {q95:.3f}")
        print(f"    p = {r['p_primary']:.4f}  "
              f"[{'SIGNIFICANT' if r['p_primary'] < ALPHA else 'NOT significant'}]")
        print(sep2)
        print(f"  PERIOD SCAN  (exploratory, uncorrected p-values)")
        print(f"    Maximum χ² at T = {T_max:.1f} yr  "
              f"(χ² = {chi2_max:.3f},  p = {p_max:.4f} uncorr.)")
        print(f"    χ² at T_hyp in scan : "
              f"{r['scan_chi2_obs'][r['hyp_idx']]:.3f}  "
              f"(p = {r['scan_p'][r['hyp_idx']]:.4f} uncorr.)")

        rows.append({
            "window":           r["label"],
            "n":                r["N"],
            "ar_p":             r["ar_p"],
            "n_cycles":         round(r["N"] / r["T_hyp"], 2),
            "T_hyp_yr":         r["T_hyp"],
            "chi2_obs":         round(r["chi2_obs"], 4),
            "null_95th_pct":    round(q95, 4),
            "p_primary":        round(r["p_primary"], 4),
            "significant":      r["p_primary"] < ALPHA,
            "scan_T_max_yr":    round(T_max, 1),
            "scan_chi2_max":    round(chi2_max, 4),
            "scan_p_max_uncorr": round(p_max, 4),
        })

    print(f"\n{SEP}")
    df = pd.DataFrame(rows).set_index("window")
    print("SUMMARY TABLE")
    print(SEP)
    print(df.to_string())

    df.to_csv(csv_path)
    print(f"\n✓ Saved {csv_path}")


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Epoch-folding phase-coherence test for ~36-year war cycle"
    )
    parser.add_argument("csv", nargs="?", default="wars_color.csv")
    parser.add_argument("--boot", type=int, default=B)
    parser.add_argument("--criterion", choices=["aic", "bic"], default="aic",
                        help="AR order selection criterion (default: aic)")
    args      = parser.parse_args()
    B_run     = args.boot
    crit      = args.criterion
    out_dir   = Path(args.csv).parent
    suffix    = f"_{crit}" if crit != "aic" else ""

    df = pd.read_csv(args.csv).set_index("year").sort_index()

    windows = [
        ("Full 1816–2007",      df.index >= 1816),
        ("Post-WWI 1918–2007",  df.index >= 1918),
    ]

    all_results = []
    for label, mask in windows:
        sub         = df[mask].copy()
        wars_raw    = sub["wars"].values.astype(float)
        wars_smooth = sub["wars_smooth"].values.astype(float)
        years       = sub.index.values

        print(f"\n{'='*70}")
        print(f"  Running epoch-folding test [{crit.upper()}] — {label}  (n={len(wars_raw)})")
        print(f"{'='*70}")

        r = run_test(years, wars_raw, wars_smooth, label,
                     n_boot=B_run, criterion=crit)
        all_results.append(r)

    print_and_save(
        all_results,
        csv_path=str(out_dir / f"epoch_folding_test_results{suffix}.csv"),
    )
    plot_results(
        all_results,
        out_path=str(out_dir / f"epoch_folding_test{suffix}.pdf"),
    )
