# spectral_significance.py – Spectral significance tests for the ~36-year war cycle
# Data: wars_color.csv (COW inter-state wars 1816–2007)
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# CONTEXT:
#   PSD analysis in analiza_poprawiona_final_GDELT.py identified a dominant
#   spectral peak at ≈ 0.028 yr⁻¹ (period ≈ 35.7 yr) in wars_smooth.
#   This script tests whether that peak is statistically significant,
#   distinguishing a genuine structural cycle from an artifact of
#   (a) finite sample length, (b) the 11-year MA smoothing, or
#   (c) autocorrelation structure that any AR model would capture.
#
# THREE TESTS:
#   1. Fisher's g-test (white-noise null):
#        g = I_max / ΣI_j
#        P(G > g) via exact formula [Fisher 1929]
#        CAVEAT: only valid if series is white noise — violated for wars_smooth.
#        Applied to raw `wars` series (counts) as the more appropriate target.
#
#   2. AR-prewhitened Fisher's g-test (colored-noise null):
#        Fit AR(p) with AIC-selected lag to wars_smooth.
#        Apply Fisher's g-test to the AR residuals.
#        Tests whether a hidden periodicity remains AFTER accounting for
#        all autocorrelation structure. This is the correct test for
#        smooth, autocorrelated series.
#
#   3. Parametric AR-bootstrap periodogram (95% pointwise CI):
#        Same AR(p) model → draw B=2000 bootstrap series → compute
#        periodogram for each → build empirical 95% envelope.
#        Check whether observed peak at ≈ 0.028 yr⁻¹ exceeds the envelope.
#        Most general: does not assume white-noise null.
#
# IMPORTANT CAVEAT ON wars_smooth:
#   An 11-year centred MA is a low-pass filter with transfer function
#   |H(f)|² = sin²(11πf) / (11 sin(πf))².
#   This ARTIFICIALLY amplifies the low-frequency part of the spectrum
#   relative to white noise. Tests 1 & 2 on wars_smooth require
#   this filter effect to be accounted for — Test 2 (AR prewhitening)
#   does so implicitly; Test 1 applied directly to wars_smooth would be
#   severely anti-conservative (too many false positives).
#
# OUTPUT:
#   spectral_significance.pdf
#   spectral_significance_results.csv

from __future__ import annotations
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.signal import periodogram, detrend
from scipy.stats import chi2
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import acf
from math import comb

warnings.filterwarnings("ignore")

RNG   = np.random.default_rng(20240301)
B     = 2000       # bootstrap replicates
ALPHA = 0.05       # significance level


# ─────────────────────────────────────────────────────────────────────────────
# 1. FISHER'S g-TEST (exact p-value)
# ─────────────────────────────────────────────────────────────────────────────

def fisher_g_test(x: np.ndarray) -> dict:
    """
    Fisher's g-test for hidden periodicity (white-noise null).

    Fisher (1929): g = I_max / Σ I_j
    P(G > g₀) = Σ_{k=1}^{floor(1/g₀)} (-1)^(k-1) C(m,k) (1 - k·g₀)^(m-1)

    Parameters
    ----------
    x : 1-D array, mean-removed

    Returns
    -------
    dict with g, p_value, peak_freq, peak_period, n_freqs
    """
    x = np.asarray(x, dtype=float) - x.mean()
    N = len(x)

    f, I = periodogram(x, fs=1.0, detrend=False)
    # exclude DC (f=0) and Nyquist (f=0.5)
    mask = (f > 0) & (f < 0.5)
    f, I = f[mask], I[mask]
    m    = len(I)

    g_obs   = I.max() / I.sum()
    peak_f  = f[I.argmax()]
    peak_T  = 1.0 / peak_f if peak_f > 0 else np.inf

    # exact p-value (alternating series)
    K      = int(1.0 / g_obs)
    pvalue = 0.0
    for k in range(1, K + 1):
        base = 1.0 - k * g_obs
        if base <= 0:
            break
        pvalue += (-1) ** (k - 1) * comb(m, k) * base ** (m - 1)

    pvalue = min(max(pvalue, 0.0), 1.0)

    return {
        "g":           g_obs,
        "p_value":     pvalue,
        "peak_freq":   peak_f,
        "peak_period": peak_T,
        "n_freqs":     m,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 2. AR PREWHITENING
# ─────────────────────────────────────────────────────────────────────────────

def fit_ar_aic(x: np.ndarray, max_lag: int = 20) -> tuple[object, int, np.ndarray]:
    """
    Fit AR(p) to x, select p by AIC, return (result, p, residuals).
    """
    x = np.asarray(x, dtype=float)
    best_aic, best_p, best_res = np.inf, 1, None
    best_fit = None
    for p in range(1, max_lag + 1):
        try:
            fit = AutoReg(x, lags=p, old_names=False).fit()
            if fit.aic < best_aic:
                best_aic = fit.aic
                best_p   = p
                best_res = fit.resid
                best_fit = fit
        except Exception:
            pass
    return best_fit, best_p, best_res


# ─────────────────────────────────────────────────────────────────────────────
# 3. AR-BOOTSTRAP PERIODOGRAM
# ─────────────────────────────────────────────────────────────────────────────

def ar_bootstrap_periodogram(
    x: np.ndarray,
    ar_fit,
    ar_resid: np.ndarray,
    n_boot: int = B,
    rng: np.random.Generator = RNG,
) -> np.ndarray:
    """
    Parametric AR bootstrap.
    For each replicate: draw residuals with replacement, reconstruct series,
    return matrix of periodogram ordinates (shape: n_boot × n_freqs).

    Uses the *same AR coefficients* as the fitted model — the null is
    "the data were generated by this AR(p) with random disturbances".
    If the observed PSD peak exceeds the 95th-percentile envelope of
    bootstrap peaks, the cycle cannot be explained by AR structure alone.
    """
    x     = np.asarray(x, dtype=float)
    N     = len(x)
    all_lags = ar_fit.model._lags       # list [1, 2, ..., p]
    p_max    = int(all_lags[-1])        # highest lag included
    coefs    = ar_fit.params            # [const, phi_1, ..., phi_p]

    f0, I0 = periodogram(x - x.mean(), fs=1.0, detrend=False)
    mask   = (f0 > 0) & (f0 < 0.5)
    n_f    = mask.sum()

    boot_psd = np.zeros((n_boot, n_f))

    for b in range(n_boot):
        # draw residuals with replacement
        eps  = rng.choice(ar_resid, size=N + p_max, replace=True)
        xs   = np.zeros(N + p_max)
        xs[:p_max] = x[:p_max]      # start from actual initial conditions
        for t in range(p_max, N + p_max):
            xs[t] = coefs[0]        # intercept
            for ki, lag in enumerate(all_lags, start=1):
                xs[t] += coefs[ki] * xs[t - lag]
            xs[t] += eps[t]
        xs = xs[p_max:]             # drop burn-in

        _, I_b = periodogram(xs - xs.mean(), fs=1.0, detrend=False)
        boot_psd[b] = I_b[mask]

    return boot_psd, f0[mask], I0[mask]


# ─────────────────────────────────────────────────────────────────────────────
# 4. PLOT
# ─────────────────────────────────────────────────────────────────────────────

def plot_all(results: dict, out_path: str) -> None:
    """4-panel figure."""
    C1, C2, C3 = "steelblue", "firebrick", "darkorange"

    fig = plt.figure(figsize=(14, 11))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.48, wspace=0.38)

    # helper: draw reference vertical line at ~36 yr
    def vline_36(ax):
        ax.axvline(1/36, color="grey", lw=1.0, linestyle=":", alpha=0.7,
                   label="T≈36 yr  (0.028 yr⁻¹)")

    # ── (a) Raw wars – Fisher g-test ─────────────────────────────────────────
    ax0 = fig.add_subplot(gs[0, 0])
    r   = results["raw"]
    f_r = r["freqs"]
    I_r = r["psd"]

    ax0.semilogy(f_r, I_r, color=C1, lw=1.2, alpha=0.8)
    ax0.semilogy(f_r[I_r.argmax()], I_r.max(),
                 "o", color=C1, ms=7,
                 label=f"peak T≈{r['fg']['peak_period']:.1f} yr")
    vline_36(ax0)

    ax0.set_xlabel("Frequency  [yr⁻¹]")
    ax0.set_ylabel("PSD  (log scale)")
    plab = f"p = {r['fg']['p_value']:.4f}" if r['fg']['p_value'] >= 0.0001 \
           else f"p < 0.0001"
    sig  = "***" if r['fg']['p_value'] < 0.001 else \
           "**"  if r['fg']['p_value'] < 0.01  else \
           "*"   if r['fg']['p_value'] < 0.05  else "n.s."
    ax0.set_title(
        f"(a) wars (raw) — Fisher g-test\n"
        f"g={r['fg']['g']:.4f}, {plab}  {sig}  [white-noise null]",
        fontsize=9,
    )
    ax0.legend(fontsize=8)

    # ── (b) wars_smooth – AR-bootstrap 95% CI ────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 1])
    s   = results["smooth"]
    f_s = s["freqs"]
    I_s = s["psd"]
    env = s["boot_env"]   # shape (n_f, 2) — [5th, 95th] percentile

    ax1.semilogy(f_s, I_s,        color=C2, lw=1.5, label="Observed PSD")
    ax1.semilogy(f_s, env[:, 1],  color="grey", lw=1.0, linestyle="--",
                 label="95th pct (AR bootstrap)")
    ax1.semilogy(f_s, env[:, 0],  color="grey", lw=0.8, linestyle=":",
                 alpha=0.5, label="5th pct")
    ax1.fill_between(f_s, env[:, 0], env[:, 1], color="grey", alpha=0.15)
    ax1.semilogy(f_s[I_s.argmax()], I_s.max(),
                 "o", color=C2, ms=7,
                 label=f"peak T≈{1/f_s[I_s.argmax()]:.1f} yr")
    vline_36(ax1)

    exc = "EXCEEDS" if I_s.max() > env[I_s.argmax(), 1] else "within"
    ax1.set_xlabel("Frequency  [yr⁻¹]")
    ax1.set_ylabel("PSD  (log scale)")
    ax1.set_title(
        f"(b) wars_smooth — AR({s['ar_p']}) bootstrap\n"
        f"Observed peak {exc} 95% CI  [B={B}]",
        fontsize=9,
    )
    ax1.legend(fontsize=7, loc="upper right")

    # ── (c) AR residuals – Fisher g-test ─────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])
    sr  = results["smooth_resid"]
    f_resid = sr["freqs"]
    I_resid = sr["psd"]

    ax2.semilogy(f_resid, I_resid, color=C3, lw=1.2, alpha=0.85)
    ax2.semilogy(f_resid[I_resid.argmax()], I_resid.max(),
                 "o", color=C3, ms=7,
                 label=f"peak T≈{sr['fg']['peak_period']:.1f} yr")
    # 95% critical line for white-noise Fisher g-test
    n_f   = len(f_resid)
    g_crit = (1 - ALPHA ** (1 / (n_f - 1))) / n_f   # approx critical g
    psd_sum = I_resid.sum()
    ax2.axhline(g_crit * psd_sum, color="grey", lw=1.0, linestyle="--",
                label=f"I_crit (g₀.₀₅≈{g_crit:.4f})")
    vline_36(ax2)

    plab2 = f"p = {sr['fg']['p_value']:.4f}" if sr['fg']['p_value'] >= 0.0001 \
            else "p < 0.0001"
    sig2  = "***" if sr['fg']['p_value'] < 0.001 else \
            "**"  if sr['fg']['p_value'] < 0.01  else \
            "*"   if sr['fg']['p_value'] < 0.05  else "n.s."
    ax2.set_xlabel("Frequency  [yr⁻¹]")
    ax2.set_ylabel("PSD  (log scale)")
    ax2.set_title(
        f"(c) wars_smooth AR({s['ar_p']}) residuals — Fisher g-test\n"
        f"g={sr['fg']['g']:.4f}, {plab2}  {sig2}  [after prewhitening]",
        fontsize=9,
    )
    ax2.legend(fontsize=8)

    # ── (d) Bootstrap distribution of g-statistic ─────────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])
    g_boot = s["g_boot"]
    g_obs  = s["g_obs"]
    p_boot = (g_boot >= g_obs).mean()

    ax3.hist(g_boot, bins=50, color="grey", alpha=0.6, density=True,
             label=f"Bootstrap g  (B={B})")
    ax3.axvline(g_obs, color=C2, lw=2.0,
                label=f"Observed g = {g_obs:.4f}")
    q95 = np.quantile(g_boot, 0.95)
    ax3.axvline(q95, color="black", lw=1.2, linestyle="--",
                label=f"95th pct = {q95:.4f}")
    ax3.set_xlabel("g-statistic  (I_max / ΣI_j)")
    ax3.set_ylabel("Density")
    sig3  = "SIGNIFICANT" if p_boot < 0.05 else "not significant"
    ax3.set_title(
        f"(d) wars_smooth: bootstrap p-value for g-stat\n"
        f"p_boot = {p_boot:.4f}  → {sig3}  [AR({s['ar_p']}) null]",
        fontsize=9,
    )
    ax3.legend(fontsize=8)

    plt.suptitle(
        "CPS — Spectral Significance Tests for the ~36-year War Cycle\n"
        "Fisher's g-test + AR-bootstrap periodogram  (COW 1816–2007)",
        fontsize=11, y=1.02,
    )
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 5. MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Spectral significance tests for ~36-year war cycle"
    )
    parser.add_argument("csv", nargs="?", default="wars_color.csv")
    parser.add_argument("--boot", type=int, default=B,
                        help=f"Bootstrap replicates (default {B})")
    parser.add_argument("--max-ar", type=int, default=20,
                        help="Max AR lag for AIC selection (default 20)")
    args   = parser.parse_args()
    B_run  = args.boot
    out_dir = Path(args.csv).parent

    # ── load data ────────────────────────────────────────────────────────────
    df = pd.read_csv(args.csv).set_index("year").sort_index()
    wars_raw    = df["wars"].dropna().values
    wars_smooth = df["wars_smooth"].dropna().values

    print("=" * 68)
    print(f"  Series lengths: wars_raw={len(wars_raw)},  "
          f"wars_smooth={len(wars_smooth)}")
    print(f"  Bootstrap replicates: {B_run}")
    print("=" * 68)

    # ── TEST A: raw wars, Fisher g-test ──────────────────────────────────────
    print("\n[A] Fisher's g-test — wars (raw, white-noise null)")
    x_raw   = detrend(wars_raw, type="linear")
    fg_raw  = fisher_g_test(x_raw)
    f_r, I_r = periodogram(x_raw - x_raw.mean(), fs=1.0, detrend=False)
    mask_r  = (f_r > 0) & (f_r < 0.5)

    print(f"  m (Fourier frequencies):  {fg_raw['n_freqs']}")
    print(f"  g-statistic:              {fg_raw['g']:.6f}")
    print(f"  Peak frequency:           {fg_raw['peak_freq']:.4f} yr⁻¹")
    print(f"  Peak period:              {fg_raw['peak_period']:.1f} yr")
    print(f"  Exact p-value:            {fg_raw['p_value']:.6f}  "
          f"({'SIGNIFICANT' if fg_raw['p_value'] < 0.05 else 'NOT significant'} at 5%)")
    print("  NOTE: white-noise null may be too lenient for count data; "
          "        check if peak is at ~36 yr or elsewhere")

    # ── TEST B: wars_smooth, AR prewhitening ─────────────────────────────────
    print("\n[B] AR-prewhitening — wars_smooth")
    x_smooth = detrend(wars_smooth, type="linear")
    ar_fit, ar_p, ar_resid = fit_ar_aic(x_smooth, max_lag=args.max_ar)
    print(f"  AIC-selected AR order:    p = {ar_p}")
    print(f"  AR(1–{ar_p}) coefficients (excl. const):")
    for i, c in enumerate(ar_fit.params[1:], start=1):
        print(f"    φ_{i} = {c:.4f}")

    # Fisher g-test on AR residuals
    fg_resid = fisher_g_test(ar_resid)
    print(f"\n  [B.1] Fisher g-test on AR residuals:")
    print(f"    m:            {fg_resid['n_freqs']}")
    print(f"    g:            {fg_resid['g']:.6f}")
    print(f"    Peak period:  {fg_resid['peak_period']:.1f} yr")
    print(f"    p-value:      {fg_resid['p_value']:.6f}  "
          f"({'SIGNIFICANT' if fg_resid['p_value'] < 0.05 else 'NOT significant'} at 5%)")

    # bootstrap periodogram
    print(f"\n  [B.2] AR({ar_p}) parametric bootstrap periodogram  (B={B_run}) …")
    boot_psd, f_smooth, I_smooth = ar_bootstrap_periodogram(
        x_smooth, ar_fit, ar_resid, n_boot=B_run
    )
    boot_env = np.percentile(boot_psd, [5, 95], axis=0).T   # (n_f, 2)

    # g-statistic bootstrap distribution
    g_boot = boot_psd.max(axis=1) / boot_psd.sum(axis=1)
    g_obs  = I_smooth.max() / I_smooth.sum()
    p_boot = (g_boot >= g_obs).mean()

    peak_idx    = I_smooth.argmax()
    peak_f_s    = f_smooth[peak_idx]
    peak_T_s    = 1.0 / peak_f_s
    exceeds_env = I_smooth[peak_idx] > boot_env[peak_idx, 1]

    print(f"    Observed peak:  T = {peak_T_s:.1f} yr  (f = {peak_f_s:.4f} yr⁻¹)")
    print(f"    Observed g:     {g_obs:.6f}")
    print(f"    Bootstrap 95th pct of g: {np.quantile(g_boot, 0.95):.6f}")
    print(f"    Bootstrap p-value (g):   {p_boot:.4f}  "
          f"({'SIGNIFICANT' if p_boot < 0.05 else 'NOT significant'} at 5%)")
    print(f"    Peak PSD vs. 95% CI envelope: "
          f"{'EXCEEDS' if exceeds_env else 'within'}  "
          f"(obs={I_smooth[peak_idx]:.2f}, CI95={boot_env[peak_idx,1]:.2f})")

    # ── summary table ────────────────────────────────────────────────────────
    print("\n" + "=" * 68)
    print("SUMMARY TABLE")
    print("=" * 68)
    rows = [
        {
            "test":         "Fisher g (raw wars, white-noise null)",
            "peak_period":  f"{fg_raw['peak_period']:.1f}",
            "g":            round(fg_raw["g"], 6),
            "p_value":      round(fg_raw["p_value"], 6),
            "significant":  fg_raw["p_value"] < 0.05,
        },
        {
            "test":         f"Fisher g (wars_smooth AR({ar_p}) residuals)",
            "peak_period":  f"{fg_resid['peak_period']:.1f}",
            "g":            round(fg_resid["g"], 6),
            "p_value":      round(fg_resid["p_value"], 6),
            "significant":  fg_resid["p_value"] < 0.05,
        },
        {
            "test":         f"AR({ar_p}) bootstrap g (wars_smooth)",
            "peak_period":  f"{peak_T_s:.1f}",
            "g":            round(g_obs, 6),
            "p_value":      round(p_boot, 4),
            "significant":  p_boot < 0.05,
        },
    ]
    res_df = pd.DataFrame(rows).set_index("test")
    print(res_df.to_string())

    # ── interpretation ────────────────────────────────────────────────────────
    print("\n" + "─" * 68)
    print("INTERPRETATION:")
    print("  The key question is test [B.2] (AR bootstrap) and [B.1] (AR residuals).")
    print("  If the cycle survives prewhitening: it is a genuine structural cycle,")
    print("  not just autocorrelation from the 11-year MA smoothing.")
    print("  If it does NOT survive: the 'cycle' is an artifact of autocorrelation")
    print("  structure that any AR model would generate.")
    print()
    if fg_resid["p_value"] < 0.05 and p_boot < 0.05:
        print("  RESULT: Both prewhitened tests are SIGNIFICANT.")
        print("  → The ~36-year cycle is a genuine structural feature beyond AR structure.")
    elif fg_resid["p_value"] < 0.05 or p_boot < 0.05:
        print("  RESULT: Mixed — one prewhitened test significant, one not.")
        print("  → The cycle is borderline; interpret with caution.")
    else:
        print("  RESULT: Neither prewhitened test is significant at 5%.")
        print("  → The peak at ~36 yr is explained by AR autocorrelation structure")
        print("    and/or the 11-year MA filter. NOT a robust structural cycle.")
    print("─" * 68)

    # ── save CSV ─────────────────────────────────────────────────────────────
    csv_path = out_dir / "spectral_significance_results.csv"
    res_df.to_csv(csv_path)
    print(f"\n✓ Saved {csv_path}")

    # ── plot ──────────────────────────────────────────────────────────────────
    all_results = {
        "raw": {
            "freqs": f_r[mask_r],
            "psd":   I_r[mask_r],
            "fg":    fg_raw,
        },
        "smooth": {
            "freqs":    f_smooth,
            "psd":      I_smooth,
            "boot_env": boot_env,
            "g_boot":   g_boot,
            "g_obs":    g_obs,
            "ar_p":     ar_p,
        },
        "smooth_resid": {
            "freqs": periodogram(ar_resid - ar_resid.mean(), fs=1.0, detrend=False)[0][
                (periodogram(ar_resid - ar_resid.mean(), fs=1.0, detrend=False)[0] > 0) &
                (periodogram(ar_resid - ar_resid.mean(), fs=1.0, detrend=False)[0] < 0.5)
            ],
            "psd": periodogram(ar_resid - ar_resid.mean(), fs=1.0, detrend=False)[1][
                (periodogram(ar_resid - ar_resid.mean(), fs=1.0, detrend=False)[0] > 0) &
                (periodogram(ar_resid - ar_resid.mean(), fs=1.0, detrend=False)[0] < 0.5)
            ],
            "fg": fg_resid,
        },
    }

    # fix the residual psd computation (avoid recomputing 4 times)
    f_res_tmp, I_res_tmp = periodogram(
        ar_resid - ar_resid.mean(), fs=1.0, detrend=False
    )
    mask_res = (f_res_tmp > 0) & (f_res_tmp < 0.5)
    all_results["smooth_resid"]["freqs"] = f_res_tmp[mask_res]
    all_results["smooth_resid"]["psd"]   = I_res_tmp[mask_res]

    plot_all(all_results, str(out_dir / "spectral_significance.pdf"))
