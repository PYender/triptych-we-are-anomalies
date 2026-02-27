# spectral_significance_v2.py – Corrected spectral significance test for ~36-year war cycle
# Data: wars_color.csv
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# DESIGN (corrects v1 flaws):
#
#   v1 problem: AR(p) was fitted directly to wars_smooth and then residuals
#   were tested. This is wrong: AR(p) fitted to an MA(11)-smoothed series
#   absorbs the 36-year component into AR coefficients (AR(13) can approximate
#   a quasi-sinusoid), so the cycle disappears by construction.
#
#   Correct approach (this script):
#     1. Fit AR(p) to wars_raw (AIC selection) — the null model
#     2. Generate B=2000 surrogate wars_raw series from AR(p)
#     3. Apply the same MA(11) filter (rolling, center=True, min_periods=1)
#        to each surrogate → surrogate_smooth
#     4. Compute PSD of observed wars_smooth and each surrogate_smooth
#     5. Under the null (AR process, no cycle), the surrogate distribution
#        already incorporates MA(11) spectral shaping
#     6. If observed wars_smooth PSD exceeds the 95th-percentile envelope
#        in the 30–45 year band → the cycle is GENUINE, not a filter artifact
#
#   Two test statistics (both reported):
#     a) Band power: integrated PSD in [1/45, 1/30] yr⁻¹ (30–45 yr period)
#        → robust to cycle period uncertainty and disturbances (pandemics,
#          post-WWII exhaustion, nuclear deterrence) — key feature of the model
#     b) Peak PSD near f = 1/36 yr⁻¹ ± 0.005 yr⁻¹
#        → sensitive but may miss a shifted or broadened peak
#
#   Two analysis windows:
#     - Full:     1816–2007 (n=192)
#     - Post-WWI: 1918–2007 (n=90) — globalized world, better data quality,
#                 where the model's cyclicality claim is strongest
#
# OUTPUT:
#   spectral_significance_v2.pdf
#   spectral_significance_v2_results.csv

from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.signal import periodogram, detrend
from statsmodels.tsa.ar_model import AutoReg

warnings.filterwarnings("ignore")

RNG       = np.random.default_rng(20240301)
B         = 2000
ALPHA     = 0.05
MA_WIN    = 11
CYCLE_T   = 36.0          # target period [yr]
BAND      = (1/45, 1/30)  # 30–45 yr period band [yr⁻¹]
PEAK_TOL  = 0.005         # ±0.005 yr⁻¹ around 1/36


# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

def apply_ma(x: np.ndarray, window: int = MA_WIN) -> np.ndarray:
    """Replicate pandas rolling(window, center=True, min_periods=1).mean()."""
    return (
        pd.Series(x)
        .rolling(window, center=True, min_periods=1)
        .mean()
        .values
    )


def fit_ar_aic(x: np.ndarray, max_lag: int = 20):
    """Fit AR(p) to x, select p by AIC. Returns (fit, p, residuals)."""
    best_aic, best_p, best_res, best_fit = np.inf, 1, None, None
    cap = min(max_lag, len(x) // 5)
    for p in range(1, cap + 1):
        try:
            fit = AutoReg(x, lags=p, old_names=False).fit()
            if fit.aic < best_aic:
                best_aic, best_p, best_res, best_fit = fit.aic, p, fit.resid, fit
        except Exception:
            pass
    return best_fit, best_p, best_res


def generate_surrogate(ar_fit, ar_resid: np.ndarray, N: int,
                       rng: np.random.Generator) -> np.ndarray:
    """One parametric AR surrogate of length N (bootstrap residuals)."""
    all_lags = ar_fit.model._lags
    p_max    = int(all_lags[-1])
    coefs    = ar_fit.params          # [const, phi_1, ..., phi_p]
    eps      = rng.choice(ar_resid, size=N + p_max, replace=True)
    xs       = np.zeros(N + p_max)
    xs[:p_max] = ar_resid[:p_max]    # realistic burn-in
    for t in range(p_max, N + p_max):
        xs[t] = coefs[0]
        for ki, lag in enumerate(all_lags, start=1):
            xs[t] += coefs[ki] * xs[t - lag]
        xs[t] += eps[t]
    return xs[p_max:]


def psd(x: np.ndarray):
    """Compute periodogram of detrended x; return (f, I) excluding DC/Nyquist."""
    xd = detrend(x, type="linear")
    f, I = periodogram(xd, fs=1.0, detrend=False)
    mask = (f > 0) & (f < 0.5)
    return f[mask], I[mask]


def band_power(f: np.ndarray, I: np.ndarray,
               band: tuple = BAND) -> float:
    """Integrated PSD in frequency band."""
    return float(I[(f >= band[0]) & (f <= band[1])].sum())


def peak_psd(f: np.ndarray, I: np.ndarray,
             T: float = CYCLE_T, tol: float = PEAK_TOL) -> float:
    """Max PSD within ±tol of 1/T."""
    target = 1.0 / T
    mask   = np.abs(f - target) <= tol
    return float(I[mask].max()) if mask.any() else float(I[np.argmin(np.abs(f - target))])


# ─────────────────────────────────────────────────────────────────────────────
# main test
# ─────────────────────────────────────────────────────────────────────────────

def run_test(years, wars_raw, wars_smooth, label: str, n_boot: int = B) -> dict:
    """
    Full MA-corrected bootstrap test.

    Null: wars_raw is an AR(p) process (no hidden periodicity).
    Surrogate wars_smooth = MA(11)(AR surrogate).
    Test: is observed wars_smooth band power / peak PSD unusual?
    """
    N = len(wars_raw)

    # observed
    f_obs, I_obs = psd(wars_smooth)
    obs_bp   = band_power(f_obs, I_obs)
    obs_peak = peak_psd(f_obs, I_obs)

    # fit AR to raw (detrended)
    x_raw = detrend(wars_raw.astype(float), type="linear")
    ar_fit, ar_p, ar_resid = fit_ar_aic(x_raw, max_lag=min(20, N // 5))

    # scale residuals to match raw variance
    raw_std = x_raw.std()

    # bootstrap
    boot_bp   = np.zeros(n_boot)
    boot_peak = np.zeros(n_boot)
    boot_psd_mat = []

    for b in range(n_boot):
        surr_raw = generate_surrogate(ar_fit, ar_resid, N, RNG)
        # rescale to same std as original detrended raw
        surr_raw = surr_raw / (surr_raw.std() + 1e-12) * raw_std
        # apply MA(11) — same as original pipeline
        surr_smooth = apply_ma(surr_raw, MA_WIN)
        f_b, I_b = psd(surr_smooth)
        # interpolate onto observed freq grid if needed
        if len(I_b) != len(I_obs):
            I_b = np.interp(f_obs, f_b, I_b)
        boot_bp[b]   = band_power(f_obs, I_b)
        boot_peak[b] = peak_psd(f_obs, I_b)
        boot_psd_mat.append(I_b)

    boot_psd_arr = np.array(boot_psd_mat)
    env_lo = np.percentile(boot_psd_arr, 5,  axis=0)
    env_hi = np.percentile(boot_psd_arr, 95, axis=0)

    p_bp   = float((boot_bp   >= obs_bp).mean())
    p_peak = float((boot_peak >= obs_peak).mean())

    # sin-fit R²
    t = np.arange(N)
    T_fit   = 35.1
    sin_reg = np.column_stack([
        np.ones(N),
        np.sin(2 * np.pi * t / T_fit),
        np.cos(2 * np.pi * t / T_fit),
        t,
    ])
    y = detrend(wars_smooth, type="linear")
    coef, res, _, _ = np.linalg.lstsq(sin_reg[:, :3], y + y.mean(), rcond=None)
    y_hat    = sin_reg[:, :3] @ coef
    ss_tot   = ((y + y.mean() - (y + y.mean()).mean()) ** 2).sum()
    ss_res   = ((y + y.mean() - y_hat) ** 2).sum()
    r2_sin   = float(1 - ss_res / ss_tot) if ss_tot > 0 else np.nan

    return {
        "label":     label,
        "N":         N,
        "ar_p":      ar_p,
        "f":         f_obs,
        "I_obs":     I_obs,
        "env_lo":    env_lo,
        "env_hi":    env_hi,
        "boot_bp":   boot_bp,
        "boot_peak": boot_peak,
        "obs_bp":    obs_bp,
        "obs_peak":  obs_peak,
        "p_bp":      p_bp,
        "p_peak":    p_peak,
        "r2_sin":    r2_sin,
    }


# ─────────────────────────────────────────────────────────────────────────────
# plot
# ─────────────────────────────────────────────────────────────────────────────

def plot_results(results: list[dict], out_path: str) -> None:
    n_rows = len(results)
    fig = plt.figure(figsize=(14, 5 * n_rows))
    gs  = gridspec.GridSpec(n_rows, 2, figure=fig, hspace=0.55, wspace=0.38)

    for row, r in enumerate(results):
        f    = r["f"]
        I    = r["I_obs"]
        lo   = r["env_lo"]
        hi   = r["env_hi"]
        label = r["label"]
        C    = "steelblue" if row == 0 else "firebrick"

        # ── left: PSD vs. bootstrap envelope ──────────────────────────────
        ax = fig.add_subplot(gs[row, 0])
        ax.semilogy(f, I,  color=C, lw=1.5, label="Observed wars_smooth")
        ax.semilogy(f, hi, color="grey", lw=1.0, ls="--",
                    label=f"95th pct (AR({r['ar_p']}) surrogate, B={B})")
        ax.semilogy(f, lo, color="grey", lw=0.7, ls=":", alpha=0.5,
                    label="5th pct")
        ax.fill_between(f, lo, hi, color="grey", alpha=0.12)

        # mark 30–45 yr band
        ax.axvspan(*BAND, color="gold", alpha=0.18, label="30–45 yr band")
        ax.axvline(1/CYCLE_T, color="darkgreen", lw=1.2, ls=":",
                   label=f"T={CYCLE_T:.0f} yr  (1/36)")

        bp_sig  = "SIGNIFICANT" if r["p_bp"]   < ALPHA else "n.s."
        pk_sig  = "SIGNIFICANT" if r["p_peak"] < ALPHA else "n.s."
        ax.set_xlabel("Frequency  [yr⁻¹]")
        ax.set_ylabel("PSD  (log scale)")
        ax.set_title(
            f"PSD — {label}  (n={r['N']}, AR({r['ar_p']}))\n"
            f"Band p={r['p_bp']:.3f} [{bp_sig}]   "
            f"Peak p={r['p_peak']:.3f} [{pk_sig}]   "
            f"sin-fit R²={r['r2_sin']:.3f}",
            fontsize=8.5,
        )
        ax.legend(fontsize=7, loc="upper right")

        # ── right: band-power bootstrap distribution ───────────────────────
        ax2 = fig.add_subplot(gs[row, 1])
        ax2.hist(r["boot_bp"], bins=50, color="grey", alpha=0.6,
                 density=True, label=f"Null (AR({r['ar_p']}) surrogates)")
        ax2.axvline(r["obs_bp"], color=C, lw=2.0,
                    label=f"Observed  (p={r['p_bp']:.3f})")
        q95 = np.quantile(r["boot_bp"], 0.95)
        ax2.axvline(q95, color="black", lw=1.2, ls="--",
                    label=f"95th pct = {q95:.1f}")
        ax2.set_xlabel("Band power  (30–45 yr)")
        ax2.set_ylabel("Density")
        sig_str = "SIGNIFICANT" if r["p_bp"] < ALPHA else "not significant"
        ax2.set_title(
            f"Band-power distribution — {label}\n"
            f"p = {r['p_bp']:.4f}  → {sig_str}",
            fontsize=8.5,
        )
        ax2.legend(fontsize=8)

    plt.suptitle(
        "CPS — MA(11)-corrected spectral significance test for ~36-year war cycle\n"
        "Null: AR(p) surrogate wars_raw → apply MA(11) → compare wars_smooth PSD",
        fontsize=11, y=1.01,
    )
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="MA-corrected spectral significance test for ~36-year war cycle"
    )
    parser.add_argument("csv", nargs="?", default="wars_color.csv")
    parser.add_argument("--boot", type=int, default=B)
    args   = parser.parse_args()
    B_run  = args.boot
    out_dir = Path(args.csv).parent

    df = pd.read_csv(args.csv).set_index("year").sort_index()

    windows = [
        ("Full 1816–2007",  df.index >= 1816),
        ("Post-WWI 1918–2007", df.index >= 1918),
    ]

    all_results = []
    summary_rows = []

    for label, mask in windows:
        sub = df[mask].copy()
        wars_raw    = sub["wars"].values.astype(float)
        wars_smooth = sub["wars_smooth"].values.astype(float)
        years       = sub.index.values

        print(f"\n{'='*68}")
        print(f"  Window: {label}  (n={len(wars_raw)})")
        print(f"{'='*68}")

        r = run_test(years, wars_raw, wars_smooth, label, n_boot=B_run)
        all_results.append(r)

        peak_f = r["f"][r["I_obs"].argmax()]
        peak_T = 1.0 / peak_f if peak_f > 0 else np.inf

        print(f"  AR order (AIC):    p = {r['ar_p']}")
        print(f"  Dominant PSD peak: T = {peak_T:.1f} yr  (f = {peak_f:.4f} yr⁻¹)")
        print(f"  Band power (30–45 yr):  obs={r['obs_bp']:.2f},  "
              f"95th-pct={np.quantile(r['boot_bp'], 0.95):.2f},  "
              f"p={r['p_bp']:.4f}  "
              f"[{'SIGNIFICANT' if r['p_bp'] < 0.05 else 'NOT significant'}]")
        print(f"  Peak PSD (±0.005 of 1/36):  obs={r['obs_peak']:.2f},  "
              f"95th-pct={np.quantile(r['boot_peak'], 0.95):.2f},  "
              f"p={r['p_peak']:.4f}  "
              f"[{'SIGNIFICANT' if r['p_peak'] < 0.05 else 'NOT significant'}]")
        print(f"  Sin-fit R² (T≈35.1 yr):  {r['r2_sin']:.4f}")

        summary_rows.append({
            "window":       label,
            "n":            r["N"],
            "ar_p":         r["ar_p"],
            "dominant_T_yr": round(peak_T, 1),
            "obs_band_power": round(r["obs_bp"], 2),
            "p_band":       round(r["p_bp"], 4),
            "band_significant": r["p_bp"] < 0.05,
            "obs_peak_psd": round(r["obs_peak"], 2),
            "p_peak":       round(r["p_peak"], 4),
            "peak_significant": r["p_peak"] < 0.05,
            "sin_r2":       round(r["r2_sin"], 4),
        })

    print(f"\n{'='*68}")
    print("SUMMARY TABLE")
    print(f"{'='*68}")
    summary_df = pd.DataFrame(summary_rows).set_index("window")
    print(summary_df.to_string())

    csv_path = out_dir / "spectral_significance_v2_results.csv"
    summary_df.to_csv(csv_path)
    print(f"\n✓ Saved {csv_path}")

    plot_results(all_results, str(out_dir / "spectral_significance_v2.pdf"))
