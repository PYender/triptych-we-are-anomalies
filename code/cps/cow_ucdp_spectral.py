# cow_ucdp_spectral.py – Combined spectral view: COW (1816-2007) + UCDP (1946-2024)
#
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# RULES:
#   – COW spectral calculations are IDENTICAL to spectral_significance.py
#     (same functions, same data, same parameters).
#   – UCDP spectral calculations are SEPARATE, same methods, own data.
#   – No data mixing. Both series shown on dual-scaled axes only.
#   – Formal tests kept independent; no statistical conclusion crosses datasets.
#
# LAYOUT (5-panel figure):
#   [A]  Wide: time series — COW wars_smooth (left axis) + UCDP smooth (right axis)
#   [B]  COW raw wars: Fisher g-test periodogram
#   [C]  UCDP raw: Fisher g-test periodogram
#   [D]  COW wars_smooth: AR-bootstrap 95% CI
#   [E]  UCDP smooth: AR-bootstrap 95% CI
#
# NOTE on UCDP series (n=79, 1946-2024):
#   Frequency resolution = 1/79 yr⁻¹ ≈ 0.013 yr⁻¹.
#   A T=36yr cycle sits at f=0.028 yr⁻¹, only ~2 bins from DC.
#   With ~2.2 cycles in the window, spectral estimates are noisy.
#   Results are indicative, not confirmatory.

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
from scipy.signal import periodogram, detrend

# ── Import spectral functions UNCHANGED from spectral_significance.py ─────────
sys.path.insert(0, str(Path(__file__).parent))
from spectral_significance import fisher_g_test, fit_ar_aic, ar_bootstrap_periodogram

warnings.filterwarnings("ignore")

RNG      = np.random.default_rng(20240301)   # same seed as spectral_significance.py
B        = 2000
ALPHA    = 0.05
SMOOTH   = 11
MAX_AR_COW  = 20    # same as spectral_significance.py
MAX_AR_UCDP = 12    # shorter series → lower AR cap to avoid overfitting


# ── 1. Load COW (identical to spectral_significance.py) ──────────────────────

def load_cow(path: str = "wars_color.csv") -> tuple:
    df = pd.read_csv(path).set_index("year").sort_index()
    wars_raw    = df["wars"].dropna().values
    wars_smooth = df["wars_smooth"].dropna().values
    years_raw   = df["wars"].dropna().index.values
    years_sm    = df["wars_smooth"].dropna().index.values
    return wars_raw, wars_smooth, years_raw, years_sm, df


# ── 2. Build UCDP series ──────────────────────────────────────────────────────

UCDP_WEIGHTS = {2: 1.0, 3: 0.4, 4: 0.7}   # type 1 excluded (extrasystemic)

def load_ucdp(path: str = "data/ucdp/UcdpPrioConflict_v25_1.csv") -> tuple:
    raw  = pd.read_csv(path, low_memory=False)
    keep = list(UCDP_WEIGHTS.keys())
    sub  = raw[raw["type_of_conflict"].isin(keep)].copy()
    sub["w"] = sub["type_of_conflict"].map(UCDP_WEIGHTS)

    yearly = sub.groupby("year")["w"].sum().rename("ucdp_wars")
    smooth = yearly.rolling(SMOOTH, center=True, min_periods=1).mean().rename("ucdp_smooth")

    df_ucdp = pd.DataFrame({"ucdp_wars": yearly, "ucdp_smooth": smooth})

    wars_raw    = df_ucdp["ucdp_wars"].dropna().values
    wars_smooth = df_ucdp["ucdp_smooth"].dropna().values
    years_raw   = df_ucdp["ucdp_wars"].dropna().index.values
    years_sm    = df_ucdp["ucdp_smooth"].dropna().index.values

    return wars_raw, wars_smooth, years_raw, years_sm, df_ucdp


# ── 3. Run spectral analysis (same pipeline for both datasets) ────────────────

def run_spectral(wars_raw: np.ndarray, wars_smooth: np.ndarray,
                 max_ar: int, label: str) -> dict:
    """
    Runs exactly the same pipeline as spectral_significance.py main block.
    Returns all results as a dict.
    """
    print(f"\n{'='*64}")
    print(f"  SPECTRAL ANALYSIS — {label}")
    print(f"  n_raw={len(wars_raw)}, n_smooth={len(wars_smooth)}, max_ar={max_ar}")
    print(f"{'='*64}")

    # ── [A] Fisher g on raw (white-noise null) ────────────────────────────────
    x_raw   = detrend(wars_raw, type="linear")
    fg_raw  = fisher_g_test(x_raw)
    f_r, I_r = periodogram(x_raw - x_raw.mean(), fs=1.0, detrend=False)
    mask_r   = (f_r > 0) & (f_r < 0.5)

    print(f"\n[A] Fisher g — {label} raw (white-noise null)")
    print(f"    Peak period: {fg_raw['peak_period']:.1f} yr")
    print(f"    g={fg_raw['g']:.6f},  p={fg_raw['p_value']:.6f}"
          f"  {'SIGNIFICANT' if fg_raw['p_value'] < 0.05 else 'NOT significant'}")

    # ── [A2] AR prewhitening on raw ───────────────────────────────────────────
    ar_fit_raw, ar_p_raw, ar_resid_raw = fit_ar_aic(x_raw, max_lag=max_ar)
    fg_resid_raw = fisher_g_test(ar_resid_raw)
    f_rr, I_rr = periodogram(ar_resid_raw - ar_resid_raw.mean(), fs=1.0, detrend=False)
    mask_rr = (f_rr > 0) & (f_rr < 0.5)

    print(f"[A2] AR({ar_p_raw}) prewhitening — {label} raw")
    print(f"    Peak period: {fg_resid_raw['peak_period']:.1f} yr")
    print(f"    g={fg_resid_raw['g']:.6f},  p={fg_resid_raw['p_value']:.6f}"
          f"  {'SIGNIFICANT' if fg_resid_raw['p_value'] < 0.05 else 'NOT significant'}")

    # ── [B] AR prewhitening on smooth + bootstrap ─────────────────────────────
    x_smooth = detrend(wars_smooth, type="linear")
    ar_fit, ar_p, ar_resid = fit_ar_aic(x_smooth, max_lag=max_ar)
    fg_resid  = fisher_g_test(ar_resid)

    print(f"[B] AR({ar_p}) prewhitening — {label} smooth")
    print(f"    Peak period: {fg_resid['peak_period']:.1f} yr")
    print(f"    g={fg_resid['g']:.6f},  p={fg_resid['p_value']:.6f}"
          f"  {'SIGNIFICANT' if fg_resid['p_value'] < 0.05 else 'NOT significant'}")

    print(f"[B.2] AR({ar_p}) bootstrap (B={B}) …")
    boot_psd, f_smooth, I_smooth = ar_bootstrap_periodogram(
        x_smooth, ar_fit, ar_resid, n_boot=B, rng=RNG
    )
    boot_env = np.percentile(boot_psd, [5, 95], axis=0).T
    g_boot   = boot_psd.max(axis=1) / boot_psd.sum(axis=1)
    g_obs    = I_smooth.max() / I_smooth.sum()
    p_boot   = (g_boot >= g_obs).mean()

    peak_idx    = I_smooth.argmax()
    peak_f_s    = f_smooth[peak_idx]
    peak_T_s    = 1.0 / peak_f_s
    exceeds_env = I_smooth[peak_idx] > boot_env[peak_idx, 1]

    print(f"    Peak T={peak_T_s:.1f} yr,  g_obs={g_obs:.6f}")
    print(f"    Bootstrap p={p_boot:.4f}"
          f"  {'SIGNIFICANT' if p_boot < 0.05 else 'NOT significant'}")
    print(f"    Peak vs 95% CI: {'EXCEEDS' if exceeds_env else 'within'}")

    return {
        "label":     label,
        "raw": {
            "freqs": f_r[mask_r],
            "psd":   I_r[mask_r],
            "fg":    fg_raw,
        },
        "raw_resid": {
            "freqs": f_rr[mask_rr],
            "psd":   I_rr[mask_rr],
            "fg":    fg_resid_raw,
            "ar_p":  ar_p_raw,
        },
        "smooth": {
            "freqs":    f_smooth,
            "psd":      I_smooth,
            "boot_env": boot_env,
            "g_boot":   g_boot,
            "g_obs":    g_obs,
            "p_boot":   p_boot,
            "ar_p":     ar_p,
            "peak_T":   peak_T_s,
            "exceeds":  exceeds_env,
        },
    }


# ── 4. Combined figure ────────────────────────────────────────────────────────

def plot_combined(
    cow_df:       pd.DataFrame,
    ucdp_df:      pd.DataFrame,
    cow_res:      dict,
    ucdp_res:     dict,
    out_path:     str = "cow_ucdp_spectral.pdf",
) -> None:
    C_COW  = "steelblue"
    C_UCDP = "firebrick"
    C_BOOT = "grey"

    fig = plt.figure(figsize=(16, 14))
    gs  = gridspec.GridSpec(
        3, 2,
        figure=fig,
        height_ratios=[1.4, 1.0, 1.0],
        hspace=0.52, wspace=0.38,
    )

    # ── Panel A: time series (full width) ──────────────────────────────────────
    ax_ts  = fig.add_subplot(gs[0, :])
    ax_ts2 = ax_ts.twinx()

    # COW: raw (light) + smooth (bold)
    ax_ts.fill_between(
        cow_df.index, cow_df["wars"],
        alpha=0.18, color=C_COW
    )
    ax_ts.plot(
        cow_df.index, cow_df["wars"],
        color=C_COW, lw=0.8, alpha=0.5
    )
    ax_ts.plot(
        cow_df["wars_smooth"].dropna().index,
        cow_df["wars_smooth"].dropna(),
        color=C_COW, lw=2.2,
        label=f"COW wars_smooth (1816–2007, left axis)"
    )

    # UCDP: raw (light) + smooth (bold)
    ax_ts2.fill_between(
        ucdp_df.index, ucdp_df["ucdp_wars"],
        alpha=0.15, color=C_UCDP
    )
    ax_ts2.plot(
        ucdp_df.index, ucdp_df["ucdp_wars"],
        color=C_UCDP, lw=0.8, alpha=0.45
    )
    ax_ts2.plot(
        ucdp_df["ucdp_smooth"].dropna().index,
        ucdp_df["ucdp_smooth"].dropna(),
        color=C_UCDP, lw=2.2,
        label=f"UCDP smooth (1946–2024, right axis)"
    )

    # Overlap shading
    ax_ts.axvspan(1946, 2007, alpha=0.06, color="gold",
                  label="Overlap 1946–2007")
    ax_ts.axvline(2007, color="grey", lw=1.0, linestyle=":", alpha=0.7)

    ax_ts.set_ylabel("COW: active wars (weighted)", color=C_COW, fontsize=10)
    ax_ts2.set_ylabel("UCDP: active conflicts (weighted)", color=C_UCDP, fontsize=10)
    ax_ts.tick_params(axis="y", labelcolor=C_COW)
    ax_ts2.tick_params(axis="y", labelcolor=C_UCDP)
    ax_ts.set_xlabel("Year")

    lines1, labs1 = ax_ts.get_legend_handles_labels()
    lines2, labs2 = ax_ts2.get_legend_handles_labels()
    ax_ts.legend(lines1 + lines2, labs1 + labs2,
                 fontsize=8.5, loc="upper left", framealpha=0.9)

    ax_ts.set_title(
        "(A)  COW (1816–2007) + UCDP (1946–2024) — dual-scaled, calculations independent\n"
        "Shading: overlap window 1946–2007 | Vertical dotted: splice year 2007",
        fontsize=10,
    )

    # ── Helper: reference lines ─────────────────────────────────────────────────
    def vline_ref(ax, period, label=True):
        f = 1.0 / period
        ax.axvline(f, color="grey", lw=0.9, linestyle=":",
                   alpha=0.7, label=(f"T≈{period:.0f} yr" if label else "_"))

    # ── Panel B: COW raw Fisher g-test ──────────────────────────────────────────
    ax_b = fig.add_subplot(gs[1, 0])
    cr   = cow_res["raw"]
    ax_b.semilogy(cr["freqs"], cr["psd"], color=C_COW, lw=1.2, alpha=0.85)
    ax_b.semilogy(cr["freqs"][cr["psd"].argmax()], cr["psd"].max(),
                  "o", color=C_COW, ms=7,
                  label=f"peak T≈{cr['fg']['peak_period']:.1f} yr")
    vline_ref(ax_b, 36)
    ax_b.set_xlabel("Frequency  [yr⁻¹]")
    ax_b.set_ylabel("PSD  (log)")
    p_b  = cr["fg"]["p_value"]
    sig_b = "***" if p_b<0.001 else "**" if p_b<0.01 else "*" if p_b<0.05 else "n.s."
    ax_b.set_title(
        f"(B)  COW raw — Fisher g-test [white-noise null]\n"
        f"g={cr['fg']['g']:.4f},  p={p_b:.4f}  {sig_b}",
        fontsize=9,
    )
    ax_b.legend(fontsize=8)

    # ── Panel C: UCDP raw Fisher g-test ────────────────────────────────────────
    ax_c = fig.add_subplot(gs[1, 1])
    ur   = ucdp_res["raw"]
    ax_c.semilogy(ur["freqs"], ur["psd"], color=C_UCDP, lw=1.2, alpha=0.85)
    ax_c.semilogy(ur["freqs"][ur["psd"].argmax()], ur["psd"].max(),
                  "o", color=C_UCDP, ms=7,
                  label=f"peak T≈{ur['fg']['peak_period']:.1f} yr")
    vline_ref(ax_c, 36)
    ax_c.set_xlabel("Frequency  [yr⁻¹]")
    ax_c.set_ylabel("PSD  (log)")
    p_c  = ur["fg"]["p_value"]
    sig_c = "***" if p_c<0.001 else "**" if p_c<0.01 else "*" if p_c<0.05 else "n.s."
    ax_c.set_title(
        f"(C)  UCDP raw — Fisher g-test [white-noise null]  n=79\n"
        f"g={ur['fg']['g']:.4f},  p={p_c:.4f}  {sig_c}",
        fontsize=9,
    )
    ax_c.legend(fontsize=8)

    # ── Panel D: COW smooth AR-bootstrap ───────────────────────────────────────
    ax_d  = fig.add_subplot(gs[2, 0])
    cs    = cow_res["smooth"]
    ax_d.semilogy(cs["freqs"], cs["psd"], color=C_COW, lw=1.5, label="Observed PSD")
    ax_d.semilogy(cs["freqs"], cs["boot_env"][:, 1], color=C_BOOT, lw=1.0,
                  linestyle="--", label="95th pct (AR bootstrap)")
    ax_d.semilogy(cs["freqs"], cs["boot_env"][:, 0], color=C_BOOT, lw=0.8,
                  linestyle=":", alpha=0.5)
    ax_d.fill_between(cs["freqs"],
                      cs["boot_env"][:, 0], cs["boot_env"][:, 1],
                      color=C_BOOT, alpha=0.12)
    ax_d.semilogy(cs["freqs"][cs["psd"].argmax()], cs["psd"].max(),
                  "o", color=C_COW, ms=7,
                  label=f"peak T≈{cs['peak_T']:.1f} yr")
    vline_ref(ax_d, 36)
    exc_d = "EXCEEDS" if cs["exceeds"] else "within"
    ax_d.set_xlabel("Frequency  [yr⁻¹]")
    ax_d.set_ylabel("PSD  (log)")
    ax_d.set_title(
        f"(D)  COW smooth — AR({cs['ar_p']}) bootstrap  (B={B})\n"
        f"p_boot={cs['p_boot']:.4f}  |  Peak {exc_d} 95% CI",
        fontsize=9,
    )
    ax_d.legend(fontsize=7.5, loc="upper right")

    # ── Panel E: UCDP smooth AR-bootstrap ──────────────────────────────────────
    ax_e  = fig.add_subplot(gs[2, 1])
    us    = ucdp_res["smooth"]
    ax_e.semilogy(us["freqs"], us["psd"], color=C_UCDP, lw=1.5, label="Observed PSD")
    ax_e.semilogy(us["freqs"], us["boot_env"][:, 1], color=C_BOOT, lw=1.0,
                  linestyle="--", label="95th pct (AR bootstrap)")
    ax_e.semilogy(us["freqs"], us["boot_env"][:, 0], color=C_BOOT, lw=0.8,
                  linestyle=":", alpha=0.5)
    ax_e.fill_between(us["freqs"],
                      us["boot_env"][:, 0], us["boot_env"][:, 1],
                      color=C_BOOT, alpha=0.12)
    ax_e.semilogy(us["freqs"][us["psd"].argmax()], us["psd"].max(),
                  "o", color=C_UCDP, ms=7,
                  label=f"peak T≈{us['peak_T']:.1f} yr")
    vline_ref(ax_e, 36)
    exc_e = "EXCEEDS" if us["exceeds"] else "within"
    ax_e.set_xlabel("Frequency  [yr⁻¹]")
    ax_e.set_ylabel("PSD  (log)")
    ax_e.set_title(
        f"(E)  UCDP smooth — AR({us['ar_p']}) bootstrap  (B={B})  n=79\n"
        f"p_boot={us['p_boot']:.4f}  |  Peak {exc_e} 95% CI",
        fontsize=9,
    )
    ax_e.legend(fontsize=7.5, loc="upper right")

    # ── Suptitle ────────────────────────────────────────────────────────────────
    plt.suptitle(
        "CPS — Spectral Analysis: COW (1816–2007) i UCDP (1946–2024)\n"
        "Obliczenia wykonane oddzielnie — te same metody, niezależne dane\n"
        "COW: Fisher g + AR(20) bootstrap  |  UCDP: Fisher g + AR(12) bootstrap\n"
        "Szara linia przerywana: T≈36 lat (referencyjna)",
        fontsize=10, y=1.01,
    )

    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ── 5. Summary table ──────────────────────────────────────────────────────────

def print_summary(cow_res: dict, ucdp_res: dict) -> pd.DataFrame:
    rows = []
    for res in [cow_res, ucdp_res]:
        lbl = res["label"]
        rows += [
            {
                "dataset": lbl,
                "test": "Fisher g (raw, white-noise null)",
                "peak_T_yr": f"{res['raw']['fg']['peak_period']:.1f}",
                "p_value":   round(res["raw"]["fg"]["p_value"], 6),
                "significant": res["raw"]["fg"]["p_value"] < 0.05,
            },
            {
                "dataset": lbl,
                "test": f"Fisher g (AR({res['raw_resid']['ar_p']}) prewhitened raw)",
                "peak_T_yr": f"{res['raw_resid']['fg']['peak_period']:.1f}",
                "p_value":   round(res["raw_resid"]["fg"]["p_value"], 6),
                "significant": res["raw_resid"]["fg"]["p_value"] < 0.05,
            },
            {
                "dataset": lbl,
                "test": f"AR({res['smooth']['ar_p']}) bootstrap (smooth)",
                "peak_T_yr": f"{res['smooth']['peak_T']:.1f}",
                "p_value":   round(res["smooth"]["p_boot"], 4),
                "significant": res["smooth"]["p_boot"] < 0.05,
            },
        ]
    df = pd.DataFrame(rows).set_index(["dataset", "test"])
    print("\n" + "="*72)
    print("SUMMARY TABLE — COW vs. UCDP spectral results")
    print("="*72)
    print(df.to_string())
    return df


# ── 6. Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from pathlib import Path as _Path

    csv_cow  = sys.argv[1] if len(sys.argv) > 1 else "wars_color.csv"
    csv_ucdp = sys.argv[2] if len(sys.argv) > 2 else "data/ucdp/UcdpPrioConflict_v25_1.csv"
    out_dir  = _Path(csv_cow).parent

    print("Loading COW data …")
    cow_raw, cow_sm, cow_yrs_r, cow_yrs_s, cow_df = load_cow(csv_cow)
    print(f"  n_raw={len(cow_raw)}, n_smooth={len(cow_sm)}"
          f"  ({cow_yrs_r[0]}–{cow_yrs_r[-1]})")

    print("Loading UCDP data …")
    ucdp_raw, ucdp_sm, ucdp_yrs_r, ucdp_yrs_s, ucdp_df = load_ucdp(csv_ucdp)
    print(f"  n_raw={len(ucdp_raw)}, n_smooth={len(ucdp_sm)}"
          f"  ({ucdp_yrs_r[0]}–{ucdp_yrs_r[-1]})")

    # ── Spectral analysis — COW (identical to spectral_significance.py) ───────
    cow_res  = run_spectral(cow_raw,  cow_sm,  MAX_AR_COW,  "COW 1816-2007")

    # ── Spectral analysis — UCDP (separate, same methods) ────────────────────
    ucdp_res = run_spectral(ucdp_raw, ucdp_sm, MAX_AR_UCDP, "UCDP 1946-2024")

    # ── Summary table ─────────────────────────────────────────────────────────
    summary_df = print_summary(cow_res, ucdp_res)
    summary_df.to_csv(out_dir / "cow_ucdp_spectral_summary.csv")
    print(f"✓ Saved cow_ucdp_spectral_summary.csv")

    # ── Combined figure ───────────────────────────────────────────────────────
    plot_combined(
        cow_df, ucdp_df,
        cow_res, ucdp_res,
        out_path=str(out_dir / "cow_ucdp_spectral.pdf"),
    )
