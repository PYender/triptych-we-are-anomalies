# wavelet_phase_test.py – Wavelet phase-coherence test for ~36-year war cycle
# Data: wars_color.csv
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# RATIONALE:
#   Epoch-folding (epoch_folding_test.py) tests whether the folded profile is
#   non-flat — a global measure of phase coherence across all cycles. The wavelet
#   test adds a LOCAL, time-resolved picture: it shows WHEN the cycle is strong
#   and whether the phase drifts or remains locked throughout 1816–2007.
#
#   This directly addresses the Triptych's claim (pages 52–78) that:
#     (a) amplitude is non-stationary — dampened post-1945 by nuclear deterrence,
#         institutional architecture, and post-war exhaustion;
#     (b) the RHYTHM (phase, period) is stable across the entire 1816–2007 window.
#
#   The wavelet gives us A(t) and ψ(t) separately:
#     A(t) = |W(t, s)|      — instantaneous amplitude at scale s ≈ 35 yr
#     ψ(t) = ∠W(t, s)       — instantaneous phase
#   Claim (a) → A(t) should drop post-1945.
#   Claim (b) → ψ(t), after removing the expected linear trend 2π·t/T_HYP,
#               should have small, stationary residuals Δψ(t).
#
# DESIGN:
#   Morlet wavelet  ψ(η) = π^(-1/4) · exp(i·ω₀·η) · exp(−η²/2), ω₀ = 6.
#   Scale–period relationship: T = 2π · s / ω₀.
#   For T_HYP = 35.1 yr → s_target = T_HYP · ω₀ / (2π) ≈ 33.5.
#
#   CWT is computed via FFT convolution for efficiency.
#
#   Cone of influence (COI): for the Morlet wavelet at scale s, the e-folding
#   time of the wavelet envelope is τ_e = s · √2. Phase estimates within τ_e
#   of the series edges are edge-affected and trimmed before computing test
#   statistics (but shown in plots for visual context with hatching).
#
#   Two test statistics on the trimmed phase residuals Δψ(t):
#     stat_A: σ²_Δψ = var(Δψ)       — phase residual variance
#             Small σ²_Δψ → phase coherent → evidence for cycle.
#             p_A = P(σ²_null ≤ σ²_obs | H₀)   [small is significant]
#
#     stat_B: R = |mean(exp(i·Δψ))| — mean resultant length (circular coherence)
#             R → 1 : perfect coherence.  R → 0 : incoherent.
#             p_B = P(R_null ≥ R_obs | H₀)      [small is significant]
#
#   Null: AR(p) surrogate wars_raw (AIC, same pipeline as spectral_significance_v2)
#         → MA(11) → CWT → extract Δψ → compute both statistics.
#
#   Analysis: FULL WINDOW ONLY (1816–2007, n = 192).
#   The post-WWI window (n = 90) provides fewer than 2 COI-trimmed cycles at
#   s ≈ 33.5; wavelet phase estimates are unreliable there.
#
# OUTPUT:
#   wavelet_phase_test.pdf
#   wavelet_phase_test_results.csv

from __future__ import annotations

import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from pathlib import Path
from scipy.signal import detrend

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

RNG    = np.random.default_rng(20240301)
B      = 2000
ALPHA  = 0.05
MA_WIN = 11
OMEGA0 = 6.0                            # Morlet central frequency
T_HYP  = 35.1                          # Triptych sin-fit period [yr]
S_TGT  = T_HYP * OMEGA0 / (2 * np.pi) # target scale ≈ 33.5

# Visualisation: scalogram range
T_VIZ_LO, T_VIZ_HI = 8.0, 80.0        # period range for scalogram [yr]


# ─────────────────────────────────────────────────────────────────────────────
# Morlet CWT via FFT
# ─────────────────────────────────────────────────────────────────────────────

def morlet_wavelet_fft(x: np.ndarray, scales: np.ndarray,
                       omega0: float = OMEGA0) -> np.ndarray:
    """
    Continuous Morlet wavelet transform via FFT convolution.

    Parameters
    ----------
    x       : input signal, length N (assumed fs = 1 yr⁻¹)
    scales  : 1D array of scales [yr]
    omega0  : Morlet central frequency (default 6)

    Returns
    -------
    W : complex array, shape (len(scales), N)
        W[j, t] = CWT coefficient at scale scales[j] and time t.
    """
    N    = len(x)
    xf   = np.fft.fft(x, n=N)
    omegas = 2 * np.pi * np.fft.fftfreq(N, d=1.0)  # angular frequencies

    W = np.zeros((len(scales), N), dtype=complex)
    for j, s in enumerate(scales):
        # Fourier transform of the scaled Morlet wavelet (unit norm)
        psi_hat = (
            np.pi ** (-0.25)
            * np.sqrt(2 * np.pi * s)
            * np.exp(-0.5 * (s * omegas - omega0) ** 2)
        )
        psi_hat[omegas < 0] = 0.0   # analytic wavelet: zero for negative freqs
        W[j] = np.fft.ifft(xf * psi_hat)
    return W


def coi_halfwidth(s: float) -> float:
    """
    Cone-of-influence half-width (e-folding distance) for Morlet wavelet
    at scale s: τ_e = s · √2.
    """
    return s * np.sqrt(2.0)


# ─────────────────────────────────────────────────────────────────────────────
# phase residual extraction
# ─────────────────────────────────────────────────────────────────────────────

def phase_residuals(W_target: np.ndarray, N: int,
                    T: float, coi_trim: int) -> np.ndarray:
    """
    Extract instantaneous phase residuals Δψ(t) from the CWT at s_target.

    Steps:
      1. ψ(t) = angle(W_target)
      2. Unwrap to remove 2π jumps.
      3. Fit linear trend ψ̂(t) = ψ₀ + (2π/T)·t by OLS.
      4. Δψ(t) = ψ(t) − ψ̂(t)
      5. Trim coi_trim samples from each end.

    Returns Δψ trimmed (length N − 2·coi_trim), or empty array if too short.
    """
    t    = np.arange(N, dtype=float)
    psi  = np.unwrap(np.angle(W_target))

    # OLS: fit ψ = a + b·t; b should be close to 2π/T under cycle hypothesis
    A_mat = np.column_stack([np.ones(N), t])
    coef, _, _, _ = np.linalg.lstsq(A_mat, psi, rcond=None)
    psi_trend = coef[0] + coef[1] * t
    delta_psi = psi - psi_trend

    # trim COI
    if coi_trim * 2 >= N:
        return np.array([])
    return delta_psi[coi_trim: N - coi_trim]


def phase_stats(delta_psi: np.ndarray) -> tuple[float, float]:
    """
    Compute two phase-coherence statistics from Δψ residuals.

    Returns
    -------
    sigma2 : variance of Δψ (smaller → more coherent)
    R      : mean resultant length |mean(exp(i·Δψ))| ∈ [0, 1]
             (larger → more coherent)
    """
    if len(delta_psi) == 0:
        return np.nan, np.nan
    sigma2 = float(np.var(delta_psi))
    R      = float(np.abs(np.mean(np.exp(1j * delta_psi))))
    return sigma2, R


# ─────────────────────────────────────────────────────────────────────────────
# main test
# ─────────────────────────────────────────────────────────────────────────────

def run_test(years: np.ndarray, wars_raw: np.ndarray, wars_smooth: np.ndarray,
             n_boot: int = B, criterion: str = "aic") -> dict:
    """
    Full wavelet phase-coherence test for wars_smooth (full window only).

    Two statistics on COI-trimmed phase residuals Δψ(t):
      σ²_Δψ : phase residual variance  (H₁: smaller than null)
      R      : mean resultant length    (H₁: larger than null)

    p_sigma2 = P(σ²_null ≤ σ²_obs | H₀)  — small → evidence for cycle
    p_R      = P(R_null ≥ R_obs   | H₀)  — small → evidence for cycle
    """
    N = len(wars_raw)
    x_smooth = detrend(wars_smooth.astype(float), type="linear")

    # ── scales for visualisation scalogram ──────────────────────────────────
    scales_viz = np.unique(np.concatenate([
        np.linspace(T_VIZ_LO * OMEGA0 / (2 * np.pi),
                    T_VIZ_HI * OMEGA0 / (2 * np.pi), 80),
        np.array([S_TGT]),
    ]))
    scales_viz = np.sort(scales_viz)

    # ── CWT on observed series ───────────────────────────────────────────────
    W_viz    = morlet_wavelet_fft(x_smooth, scales_viz)
    s_idx    = int(np.argmin(np.abs(scales_viz - S_TGT)))
    W_target = W_viz[s_idx]                # complex, shape (N,)

    amp  = np.abs(W_target)               # A(t)
    psi  = np.unwrap(np.angle(W_target))  # ψ(t) unwrapped

    coi_trim = max(1, int(np.ceil(coi_halfwidth(S_TGT))))
    delta_psi_obs = phase_residuals(W_target, N, T_HYP, coi_trim)
    sigma2_obs, R_obs = phase_stats(delta_psi_obs)

    # linear trend over full series for plotting
    t_full = np.arange(N, dtype=float)
    A_mat  = np.column_stack([np.ones(N), t_full])
    coef, _, _, _ = np.linalg.lstsq(A_mat, psi, rcond=None)
    psi_trend_full = coef[0] + coef[1] * t_full

    # ── AR surrogate null ────────────────────────────────────────────────────
    x_raw = detrend(wars_raw.astype(float), type="linear")
    ar_fit, ar_p, ar_resid = fit_ar_criterion(x_raw, max_lag=min(20, N // 5),
                                               criterion=criterion)
    raw_std = x_raw.std()

    boot_sigma2 = np.zeros(n_boot)
    boot_R      = np.zeros(n_boot)
    # store a few surrogate phase curves for visual comparison
    surr_psi_sample = []

    for b in range(n_boot):
        surr_raw = generate_surrogate(ar_fit, ar_resid, N, RNG)
        surr_raw = surr_raw / (surr_raw.std() + 1e-12) * raw_std
        surr_sm  = apply_ma(surr_raw, MA_WIN)
        x_surr   = detrend(surr_sm, type="linear")

        W_surr  = morlet_wavelet_fft(x_surr, np.array([S_TGT]))[0]
        dp_surr = phase_residuals(W_surr, N, T_HYP, coi_trim)
        s2, r   = phase_stats(dp_surr)
        boot_sigma2[b] = s2
        boot_R[b]      = r

        if b < 20:   # keep 20 surrogate phase curves for plotting
            surr_psi_sample.append(np.unwrap(np.angle(W_surr)))

    # remove nan surrogates (shouldn't happen but guard)
    boot_sigma2 = boot_sigma2[~np.isnan(boot_sigma2)]
    boot_R      = boot_R[~np.isnan(boot_R)]

    # p-values: direction aligned with H₁ (cycle → small σ², large R)
    p_sigma2 = float((boot_sigma2 <= sigma2_obs).mean())
    p_R      = float((boot_R      >= R_obs).mean())

    return {
        "N":                N,
        "criterion":        criterion,
        "ar_p":             ar_p,
        "years":            years,
        "x_smooth":         x_smooth,
        "scales_viz":       scales_viz,
        "W_viz":            W_viz,
        "s_idx":            s_idx,
        "S_tgt":            S_TGT,
        "T_hyp":            T_HYP,
        "amp":              amp,
        "psi":              psi,
        "psi_trend":        psi_trend_full,
        "delta_psi_obs":    delta_psi_obs,
        "coi_trim":         coi_trim,
        "sigma2_obs":       sigma2_obs,
        "R_obs":            R_obs,
        "boot_sigma2":      boot_sigma2,
        "boot_R":           boot_R,
        "p_sigma2":         p_sigma2,
        "p_R":              p_R,
        "surr_psi_sample":  surr_psi_sample,
    }


# ─────────────────────────────────────────────────────────────────────────────
# plot
# ─────────────────────────────────────────────────────────────────────────────

def plot_results(r: dict, out_path: str) -> None:
    years = r["years"]
    N     = r["N"]
    C_OBS = "steelblue"
    C_SUR = "lightcoral"

    fig = plt.figure(figsize=(16, 14))
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.52, wspace=0.38)

    # ── Panel A: wars_smooth + A(t) overlay ─────────────────────────────────
    ax_a  = fig.add_subplot(gs[0, :])
    ax_a2 = ax_a.twinx()

    ax_a.fill_between(years, r["x_smooth"],
                      alpha=0.20, color=C_OBS)
    ax_a.plot(years, r["x_smooth"], color=C_OBS, lw=1.6,
              label="wars_smooth (detrended)")
    ax_a2.plot(years, r["amp"], color="darkred", lw=1.8, ls="--",
               label=f"A(t)  — instantaneous amplitude at T≈{r['T_hyp']:.0f} yr")

    # shade post-1945 (nuclear deterrence era per Triptych)
    ax_a.axvspan(1945, years[-1], alpha=0.07, color="orange",
                 label="Post-1945: nuclear deterrence era (Triptych)")

    ax_a.set_xlabel("Year")
    ax_a.set_ylabel("wars_smooth detrended", color=C_OBS)
    ax_a2.set_ylabel(f"Wavelet amplitude  A(t)  at T≈{r['T_hyp']:.0f} yr",
                     color="darkred")
    ax_a.tick_params(axis="y", labelcolor=C_OBS)
    ax_a2.tick_params(axis="y", labelcolor="darkred")
    l1, lb1 = ax_a.get_legend_handles_labels()
    l2, lb2 = ax_a2.get_legend_handles_labels()
    ax_a.legend(l1 + l2, lb1 + lb2, fontsize=7.5, loc="upper left")
    ax_a.set_title(
        f"(A) Instantaneous amplitude A(t) at T≈{r['T_hyp']:.1f} yr  "
        f"[scale s≈{r['S_tgt']:.1f}, Morlet ω₀={OMEGA0:.0f}]\n"
        "If Triptych model is correct: A(t) should decline post-1945",
        fontsize=9.5,
    )

    # ── Panel B: scalogram ───────────────────────────────────────────────────
    ax_b = fig.add_subplot(gs[1, 0])

    # periods for y-axis
    periods_viz = 2 * np.pi * r["scales_viz"] / OMEGA0
    power       = np.abs(r["W_viz"]) ** 2
    # clip to T_VIZ range
    mask_p = (periods_viz >= T_VIZ_LO) & (periods_viz <= T_VIZ_HI)

    im = ax_b.contourf(
        years,
        periods_viz[mask_p],
        power[mask_p],
        levels=30, cmap="YlOrRd",
    )
    plt.colorbar(im, ax=ax_b, label="Wavelet power")

    # mark T_HYP
    ax_b.axhline(r["T_hyp"], color="white", lw=1.2, ls="--",
                 label=f"T_hyp = {r['T_hyp']:.1f} yr")

    # cone of influence (COI)
    coi_t_left  = r["S_tgt"] * np.sqrt(2) * np.ones(2)
    coi_t_right = r["S_tgt"] * np.sqrt(2) * np.ones(2)
    T_range = [T_VIZ_LO, T_VIZ_HI]
    ax_b.fill_betweenx(
        T_range,
        [years[0], years[0]],
        [years[0] + coi_t_left[0], years[0] + coi_t_left[0]],
        color="grey", alpha=0.35, label="COI (edge-affected)",
    )
    ax_b.fill_betweenx(
        T_range,
        [years[-1] - coi_t_right[0], years[-1] - coi_t_right[0]],
        [years[-1], years[-1]],
        color="grey", alpha=0.35,
    )

    ax_b.set_xlabel("Year")
    ax_b.set_ylabel("Period  [yr]")
    ax_b.set_title(
        "(B) Wavelet power scalogram (Morlet, ω₀=6)\n"
        "Hatched: cone of influence (edge-affected region)",
        fontsize=9,
    )
    ax_b.legend(fontsize=7.5, loc="upper right")

    # ── Panel C: instantaneous phase ψ(t) and residuals ─────────────────────
    ax_c = fig.add_subplot(gs[1, 1])

    # plot a few surrogate phases for comparison
    for psi_s in r["surr_psi_sample"]:
        ax_c.plot(years, psi_s, color=C_SUR, lw=0.5, alpha=0.35)

    ax_c.plot(years, r["psi"], color=C_OBS, lw=1.8,
              label="Observed ψ(t) (unwrapped)")
    ax_c.plot(years, r["psi_trend"], color="black", lw=1.2, ls="--",
              label=f"Linear trend (OLS fit to ψ)")

    # mark COI trim region
    coi_yr = int(np.ceil(r["coi_trim"]))
    ax_c.axvspan(years[0], years[0] + coi_yr, alpha=0.12, color="grey",
                 label="COI trim region")
    ax_c.axvspan(years[-1] - coi_yr, years[-1], alpha=0.12, color="grey")

    ax_c.set_xlabel("Year")
    ax_c.set_ylabel("Phase ψ(t)  [rad, unwrapped]")
    ax_c.set_title(
        f"(C) Instantaneous phase at T≈{r['T_hyp']:.1f} yr\n"
        f"20 AR surrogates shown (red) vs. observed (blue)",
        fontsize=9,
    )
    ax_c.legend(fontsize=7.5, loc="upper left")

    # ── Panel D: σ²_Δψ bootstrap distribution ───────────────────────────────
    ax_d = fig.add_subplot(gs[2, 0])

    ax_d.hist(r["boot_sigma2"], bins=50, color="grey", alpha=0.55,
              density=True, label=f"Null AR({r['ar_p']}) surrogates")
    ax_d.axvline(r["sigma2_obs"], color=C_OBS, lw=2.0,
                 label=f"Observed σ² = {r['sigma2_obs']:.4f}")
    q05_s2 = float(np.quantile(r["boot_sigma2"], 0.05))
    ax_d.axvline(q05_s2, color="black", lw=1.2, ls="--",
                 label=f"Null 5th pct = {q05_s2:.4f}")

    sig_d = "SIGNIFICANT" if r["p_sigma2"] < ALPHA else "n.s."
    ax_d.set_xlabel("σ²_Δψ  (phase residual variance)")
    ax_d.set_ylabel("Density")
    ax_d.set_title(
        f"(D) Phase variance — {r['N']} obs, AR({r['ar_p']})\n"
        f"p_σ² = P(null ≤ obs) = {r['p_sigma2']:.4f}  [{sig_d}]\n"
        "Small σ² → phase stable → evidence for cycle",
        fontsize=9,
    )
    ax_d.legend(fontsize=7.5)

    # ── Panel E: R bootstrap distribution ───────────────────────────────────
    ax_e = fig.add_subplot(gs[2, 1])

    ax_e.hist(r["boot_R"], bins=50, color="grey", alpha=0.55,
              density=True, label=f"Null AR({r['ar_p']}) surrogates")
    ax_e.axvline(r["R_obs"], color=C_OBS, lw=2.0,
                 label=f"Observed R = {r['R_obs']:.4f}")
    q95_R = float(np.quantile(r["boot_R"], 0.95))
    ax_e.axvline(q95_R, color="black", lw=1.2, ls="--",
                 label=f"Null 95th pct = {q95_R:.4f}")

    sig_e = "SIGNIFICANT" if r["p_R"] < ALPHA else "n.s."
    ax_e.set_xlabel("R  (mean resultant length)")
    ax_e.set_ylabel("Density")
    ax_e.set_title(
        f"(E) Phase coherence R — {r['N']} obs, AR({r['ar_p']})\n"
        f"p_R = P(null ≥ obs) = {r['p_R']:.4f}  [{sig_e}]\n"
        "R → 1 : phase coherent → evidence for cycle",
        fontsize=9,
    )
    ax_e.legend(fontsize=7.5)

    crit_label = r.get("criterion", "aic").upper()
    plt.suptitle(
        f"CPS — Wavelet phase-coherence test for ~36-year war cycle  [{crit_label} null]\n"
        f"Full window 1816–2007  |  Morlet CWT, ω₀={OMEGA0:.0f}, "
        f"T_hyp={r['T_hyp']:.1f} yr, s≈{r['S_tgt']:.1f}  |  "
        f"COI trim: ±{r['coi_trim']} yr  |  AR({r['ar_p']}) null, B={B}",
        fontsize=10.5, y=1.01,
    )
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# summary print + CSV
# ─────────────────────────────────────────────────────────────────────────────

def print_and_save(r: dict, csv_path: str) -> None:
    SEP  = "═" * 70
    sep2 = "─" * 70

    n_trimmed = len(r["delta_psi_obs"])
    print(f"\n{SEP}")
    print("  WAVELET PHASE-COHERENCE TEST  (Full window 1816–2007)")
    print(SEP)
    print(f"  n = {r['N']}  |  AR({r['ar_p']}) null  |  "
          f"T_hyp = {r['T_hyp']:.1f} yr  |  s_target = {r['S_tgt']:.2f}")
    print(f"  COI trim: ±{r['coi_trim']} yr  →  "
          f"{n_trimmed} obs used for phase statistics "
          f"(~{n_trimmed / r['T_hyp']:.1f} cycles)")
    print(sep2)
    print("  STATISTIC A: σ²_Δψ  (phase residual variance)")
    print(f"    Observed  σ²_Δψ = {r['sigma2_obs']:.6f}")
    print(f"    Null 5th pct    = {np.quantile(r['boot_sigma2'], 0.05):.6f}")
    print(f"    p_σ²  =  P(null ≤ obs) = {r['p_sigma2']:.4f}  "
          f"[{'SIGNIFICANT' if r['p_sigma2'] < ALPHA else 'NOT significant'}]")
    print(sep2)
    print("  STATISTIC B: R  (mean resultant length)")
    print(f"    Observed  R = {r['R_obs']:.6f}")
    print(f"    Null 95th pct = {np.quantile(r['boot_R'], 0.95):.6f}")
    print(f"    p_R   =  P(null ≥ obs) = {r['p_R']:.4f}  "
          f"[{'SIGNIFICANT' if r['p_R'] < ALPHA else 'NOT significant'}]")
    print(SEP)

    df = pd.DataFrame([{
        "window":               "Full 1816–2007",
        "n":                    r["N"],
        "ar_p":                 r["ar_p"],
        "T_hyp_yr":             r["T_hyp"],
        "s_target":             round(r["S_tgt"], 2),
        "coi_trim_yr":          r["coi_trim"],
        "n_obs_trimmed":        n_trimmed,
        "n_cycles_trimmed":     round(n_trimmed / r["T_hyp"], 2),
        "sigma2_obs":           round(r["sigma2_obs"], 6),
        "null_5th_pct_sigma2":  round(float(np.quantile(r["boot_sigma2"], 0.05)), 6),
        "p_sigma2":             round(r["p_sigma2"], 4),
        "significant_sigma2":   r["p_sigma2"] < ALPHA,
        "R_obs":                round(r["R_obs"], 6),
        "null_95th_pct_R":      round(float(np.quantile(r["boot_R"], 0.95)), 6),
        "p_R":                  round(r["p_R"], 4),
        "significant_R":        r["p_R"] < ALPHA,
    }]).set_index("window")

    print(df.T.to_string())
    df.to_csv(csv_path)
    print(f"\n✓ Saved {csv_path}")


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Wavelet phase-coherence test for ~36-year war cycle"
    )
    parser.add_argument("csv", nargs="?", default="wars_color.csv")
    parser.add_argument("--boot", type=int, default=B)
    parser.add_argument("--criterion", choices=["aic", "bic"], default="aic",
                        help="AR order selection criterion (default: aic)")
    args    = parser.parse_args()
    B_run   = args.boot
    crit    = args.criterion
    out_dir = Path(args.csv).parent
    suffix  = f"_{crit}" if crit != "aic" else ""

    df_data = pd.read_csv(args.csv).set_index("year").sort_index()

    # Full window only — see DESIGN note on COI and post-WWI window
    mask        = df_data.index >= 1816
    sub         = df_data[mask].copy()
    wars_raw    = sub["wars"].values.astype(float)
    wars_smooth = sub["wars_smooth"].values.astype(float)
    years       = sub.index.values

    print(f"{'='*70}")
    print(f"  Running wavelet phase-coherence test [{crit.upper()}]  (n={len(wars_raw)})")
    print(f"  T_hyp={T_HYP} yr  |  s_target≈{S_TGT:.2f}  |  B={B_run}")
    print(f"{'='*70}")

    r = run_test(years, wars_raw, wars_smooth, n_boot=B_run, criterion=crit)

    print_and_save(
        r,
        csv_path=str(out_dir / f"wavelet_phase_test_results{suffix}.csv"),
    )
    plot_results(
        r,
        out_path=str(out_dir / f"wavelet_phase_test{suffix}.pdf"),
    )
