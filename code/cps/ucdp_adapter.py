# ucdp_adapter.py – UCDP v25.1 → CPS format adapter
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# PURPOSE:
#   Extends the COW-based conflict series (1816–2007) with UCDP v25.1
#   data (1989–2024), then reruns the CPS sine-fit + ARIMAX model on the
#   combined series and plots the result – with the Ukraine war highlighted.
#
# DATA SOURCES:
#   COW:  wars_color.csv  (output of analiza_poprawiona_final_GDELT.py)
#   UCDP: UCDP/PRIO Armed Conflict Dataset v25.1
#         https://ucdp.uu.se/downloads/
#         File: ucdp-prio-acd-251.csv
#         (free download, no registration)
#
# UCDP conflict types used:
#   type_of_conflict == 2  → interstate       weight 1.0  (matches COW inter-state)
#   type_of_conflict == 3  → intrastate       weight 0.4  (matches COW intra-state)
#   type_of_conflict == 4  → internationalized intrastate  weight 0.7 (matches extra-state)
#
# OVERLAP:
#   COW ends at 2007.  UCDP starts at 1946.
#   We use COW for 1816–2006 and UCDP for 2007–2024.
#   The splice year is 2007 (last COW year kept in the original script).
#   A simple level-adjustment is applied so that the two series agree
#   at the splice boundary (scale factor = mean_COW / mean_UCDP over the
#   common calibration window 1989–2006).
#
# UKRAINE EVENTS marked on the plot:
#   2014 – War in Donbas (UCDP conflict id 13965)
#   2022 – Full-scale Russian invasion

from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from scipy.optimize import curve_fit
from scipy.signal import periodogram, detrend
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")

# =========================================================================
# 0. PARAMETERS  (match the baseline script)
# =========================================================================
SMOOTH_WIN   = 11
ARIMA_ORDER  = (1, 1, 1)
COLOR_LAG    = 2
SPLICE_YEAR  = 2007        # last year from COW kept; UCDP fills 2007–2024
CALIB_START  = 1989        # start of overlap window for level-alignment
CALIB_END    = 2006

UCDP_WEIGHTS = {
    2: 1.0,   # interstate
    3: 0.4,   # intrastate
    4: 0.7,   # internationalized intrastate
}

# =========================================================================
# 1. LOAD COW BASELINE (wars_color.csv)
# =========================================================================

def load_cow(csv_path: str = "wars_color.csv") -> pd.DataFrame:
    df = pd.read_csv(csv_path).set_index("year").sort_index()
    return df


# =========================================================================
# 2. LOAD & AGGREGATE UCDP v25.1
# =========================================================================

def load_ucdp(ucdp_path: str = "ucdp-prio-acd-251.csv") -> pd.Series:
    """
    Returns a yearly weighted-conflict-count Series (index = year).
    Conflict types: 2 (interstate), 3 (intrastate), 4 (intl. intrastate).
    Type 1 (extrasystemic) is excluded – near-zero post-1945.
    """
    raw = pd.read_csv(ucdp_path, encoding="utf-8", low_memory=False)

    # UCDP column names (v25.1)
    # 'year', 'type_of_conflict', 'conflict_id', 'intensity_level', ...
    keep_types = list(UCDP_WEIGHTS.keys())
    sub = raw[raw["type_of_conflict"].isin(keep_types)].copy()

    # each row = one conflict-year; count weighted by type
    sub["weight"] = sub["type_of_conflict"].map(UCDP_WEIGHTS)

    yearly = (
        sub.groupby("year")["weight"]
        .sum()
        .rename("wars_ucdp")
    )
    return yearly


# =========================================================================
# 3. SPLICE: calibrate level + merge into one series
# =========================================================================

def splice_series(
    cow_df:     pd.DataFrame,
    ucdp_raw:   pd.Series,
) -> pd.DataFrame:
    """
    Returns a combined DataFrame with:
      – wars_raw     : raw weighted conflict count (COW + UCDP)
      – wars_smooth  : 11-year centred rolling mean
      – source       : 'COW' or 'UCDP'
      – color        : carried over from cow_df where available
    """
    # ── level-alignment ────────────────────────────────────────────────
    cow_calib  = cow_df.loc[CALIB_START:CALIB_END, "wars"]
    ucdp_calib = ucdp_raw.loc[CALIB_START:CALIB_END]

    common_idx = cow_calib.index.intersection(ucdp_calib.index)
    if len(common_idx) < 5:
        scale = 1.0
        print("⚠ calibration window too small – no scaling applied")
    else:
        scale = cow_calib.loc[common_idx].mean() / ucdp_calib.loc[common_idx].mean()
        print(f"  UCDP→COW scale factor: {scale:.3f}  "
              f"(calibration {CALIB_START}–{CALIB_END})")

    ucdp_scaled = ucdp_raw * scale

    # ── build combined raw series ───────────────────────────────────────
    cow_years  = cow_df.index[cow_df.index <= SPLICE_YEAR]
    ucdp_years = ucdp_scaled.index[ucdp_scaled.index > SPLICE_YEAR]

    wars_combined = pd.concat([
        cow_df.loc[cow_years, "wars"].rename("wars_raw"),
        ucdp_scaled.loc[ucdp_years].rename("wars_raw"),
    ]).sort_index()

    out = pd.DataFrame({"wars_raw": wars_combined})

    # ── label source ────────────────────────────────────────────────────
    out["source"] = "COW"
    out.loc[out.index > SPLICE_YEAR, "source"] = "UCDP"

    # ── smooth ──────────────────────────────────────────────────────────
    out["wars_smooth"] = (
        out["wars_raw"]
        .rolling(SMOOTH_WIN, center=True, min_periods=1)
        .mean()
    )

    # ── carry over COLOR (only where COW data exists) ────────────────────
    out = out.join(cow_df[["color", "pop"]], how="left")

    return out


# =========================================================================
# 4. EXTENDED SINE-FIT + ARIMAX FORECAST
# =========================================================================

def sin_f(t, A, w, phi, C):
    return A * np.sin(w * t + phi) + C


def fit_and_forecast(df_ext: pd.DataFrame, forecast_steps: int = 20):
    """
    Fits a sine wave + ARIMAX(1,1,1) to the extended wars_smooth series.
    Returns (sin_params, arima_fit, forecast_series).
    """
    series = df_ext["wars_smooth"].dropna()
    x = np.arange(len(series))

    # sine fit
    pars, _ = curve_fit(
        sin_f, x, series.values,
        p0=[3, 2 * np.pi / 50, 0, 1],
        maxfev=20_000,
    )
    period = 2 * np.pi / pars[1]
    print(f"  Sine period ≈ {period:.1f} years  (extended series)")

    # ARIMAX
    color_col = df_ext["color"].reindex(series.index)
    exog      = color_col.shift(COLOR_LAG)
    mask      = exog.notna()

    model     = ARIMA(series[mask], order=ARIMA_ORDER, exog=exog[mask])
    arima_fit = model.fit()

    last_exog     = exog[mask].iloc[-1]
    exog_fc       = np.repeat(last_exog, forecast_steps)
    fc            = arima_fit.get_forecast(steps=forecast_steps, exog=exog_fc)
    fc_mean       = fc.predicted_mean
    fc_ci         = fc.conf_int(alpha=0.10)   # 90 % CI

    last_year     = series.index[-1]
    fc_years      = np.arange(last_year + 1, last_year + 1 + forecast_steps)
    fc_series     = pd.Series(fc_mean.values, index=fc_years, name="forecast")
    ci_lo         = pd.Series(fc_ci.iloc[:, 0].values, index=fc_years)
    ci_hi         = pd.Series(fc_ci.iloc[:, 1].values, index=fc_years)

    return pars, arima_fit, fc_series, ci_lo, ci_hi, period


# =========================================================================
# 5. PLOT – WITH UKRAINE ANNOTATIONS
# =========================================================================

UKRAINE_EVENTS = {
    2014: ("War in Donbas\n(2014)", "darkorange"),
    2022: ("Full-scale\ninvasion (2022)", "crimson"),
}


def plot_extended(
    df_ext:    pd.DataFrame,
    sin_pars,
    fc_series: pd.Series,
    ci_lo:     pd.Series,
    ci_hi:     pd.Series,
    period:    float,
    out_path:  str = "cps_extended_2024.pdf",
):
    """
    Two-panel figure:
      (a) wars_smooth (COW + UCDP) + sine fit + ARIMAX forecast + CI
          with Ukraine events annotated
      (b) Zoom: 1990–forecast end, Ukraine highlighted
    """
    series = df_ext["wars_smooth"].dropna()
    years  = series.index
    x      = np.arange(len(series))

    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False)
    fig.subplots_adjust(hspace=0.45)

    for ax_idx, ax in enumerate(axes):
        # ── data ─────────────────────────────────────────────────────────
        cow_mask  = df_ext.loc[years, "source"] == "COW"
        ucdp_mask = df_ext.loc[years, "source"] == "UCDP"

        ax.plot(years[cow_mask],  series[cow_mask],  lw=2.0,
                color="steelblue", label="COW (1816–2007)")
        ax.plot(years[ucdp_mask], series[ucdp_mask], lw=2.0,
                color="seagreen",  label="UCDP (2008–2024)")

        # sine fit (only over historical range)
        ax.plot(years, sin_f(x, *sin_pars), "--",
                color="grey", lw=1.2, label=f"sine fit (T≈{period:.0f} yr)")

        # splice marker
        ax.axvline(SPLICE_YEAR, color="grey", lw=0.8, linestyle=":")

        # forecast + CI
        ax.plot(fc_series.index, fc_series.values, lw=1.8,
                color="tomato", linestyle="--", label="ARIMAX forecast")
        ax.fill_between(fc_series.index, ci_lo, ci_hi,
                        alpha=0.18, color="tomato", label="90 % CI")

        # ── Ukraine annotations ─────────────────────────────────────────
        for yr, (label, color) in UKRAINE_EVENTS.items():
            ax.axvline(yr, color=color, lw=1.5, linestyle="-.", alpha=0.85)
            y_pos = ax.get_ylim()[1] * 0.88 if ax_idx == 0 else ax.get_ylim()[1] * 0.80
            ax.text(yr + 0.3, y_pos, label,
                    color=color, fontsize=7.5, va="top",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7))

        ax.set_ylabel("Number of conflicts (11-yr smoothed)")
        ax.legend(fontsize=8, loc="upper left")

        if ax_idx == 1:
            # zoom panel
            ax.set_xlim(1990, fc_series.index[-1] + 1)
            ax.set_title("Zoom: 1990 – forecast end  |  Ukraine in context")
        else:
            ax.set_title(
                "CPS – extended series  COW (1816–2007) + UCDP v25.1 (2008–2024)\n"
                f"ARIMAX(1,1,1) + COLOR exog  |  sine period ≈ {period:.0f} yr"
            )

    axes[1].set_xlabel("Year")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"✓ Saved {out_path}")
    plt.show()


# =========================================================================
# 6. MAIN
# =========================================================================

if __name__ == "__main__":
    import sys

    cow_csv  = "wars_color.csv"
    ucdp_csv = "ucdp-prio-acd-251.csv"

    if len(sys.argv) > 1: cow_csv  = sys.argv[1]
    if len(sys.argv) > 2: ucdp_csv = sys.argv[2]

    # ── 1. Load ────────────────────────────────────────────────────────
    print("Loading COW baseline …")
    cow_df = load_cow(cow_csv)

    print("Loading UCDP v25.1 …")
    if not Path(ucdp_csv).exists():
        print(
            f"\n  ⚠ File not found: {ucdp_csv}\n"
            "  Download from: https://ucdp.uu.se/downloads/\n"
            "  File: ucdp-prio-acd-251.csv\n"
            "  Place it in the same directory as this script and rerun.\n"
        )
        raise SystemExit(1)

    ucdp_raw = load_ucdp(ucdp_csv)

    # ── 2. Splice ──────────────────────────────────────────────────────
    print("Splicing COW + UCDP …")
    df_ext = splice_series(cow_df, ucdp_raw)
    print(f"  Combined range: {df_ext.index[0]}–{df_ext.index[-1]}"
          f"  ({len(df_ext)} years)")

    # ── 3. Fit + forecast ─────────────────────────────────────────────
    print("Fitting sine + ARIMAX …")
    sin_pars, arima_fit, fc_series, ci_lo, ci_hi, period = fit_and_forecast(df_ext)
    print(arima_fit.summary())

    # ── 4. Save extended CSV ──────────────────────────────────────────
    df_ext.to_csv("cps_extended_2024.csv")
    print("✓ Saved cps_extended_2024.csv")

    # ── 5. Plot ────────────────────────────────────────────────────────
    plot_extended(df_ext, sin_pars, fc_series, ci_lo, ci_hi, period)
