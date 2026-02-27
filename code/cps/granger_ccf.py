# granger_ccf.py – Granger Causality & Cross-Correlation Analysis for CPS
# COLOR (N-gram hostility index) ↔ wars_smooth (11-yr smoothed war count)
# Data: wars_color.csv  (COW inter-state wars 1816–2007)
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# USAGE:
#   python granger_ccf.py [path/to/wars_color.csv]
#
# OUTPUT (all written to the same directory as wars_color.csv):
#   granger_ccf.pdf          – 4-panel publication figure
#   granger_ccf_adf.csv      – ADF stationarity test results
#   granger_ccf_ccf.csv      – CCF values (levels + first differences)
#   granger_ccf_granger.csv  – Granger F-test results per lag, both directions
#
# METHODOLOGY NOTE:
#   wars_smooth is an 11-year centred moving average, so adjacent observations
#   are highly autocorrelated (effective n < 192).  All significance levels
#   should be interpreted conservatively.  The differenced series (Δ) reduces
#   this autocorrelation and is used for the formal Granger tests.
#   CCF is computed on both levels (for comparison with Table C1 in the paper)
#   and first differences (for formal inference).
#
# CCF SIGN CONVENTION:
#   CCF(wars, color)[lag=k] = corr(wars[t], color[t-k])
#   positive lag k  →  color preceded wars by k years  →  COLOR LEADS
#   negative lag k  →  color followed wars by k years  →  wars LEAD

from __future__ import annotations
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

warnings.filterwarnings("ignore")

MAX_LAG  = 12  # maximum lag for Granger tests and CCF
ADF_LAGS = 5   # max lag for ADF (AIC-selected within this range)

# ─────────────────────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────

def load_df(csv_path: str = "wars_color.csv") -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df.set_index("year").sort_index()
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 2. ADF STATIONARITY TESTS
# ─────────────────────────────────────────────────────────────────────────────

def adf_report(series: pd.Series, name: str, maxlag: int = ADF_LAGS) -> dict:
    """Run augmented Dickey-Fuller test and return results as a dict."""
    clean = series.dropna()
    stat, p, lags_used, nobs, crit, _ = adfuller(clean, maxlag=maxlag, autolag="AIC")
    return {
        "series":        name,
        "ADF stat":      round(stat, 4),
        "p-value":       round(p, 4),
        "lags used":     lags_used,
        "nobs":          nobs,
        "crit 1%":       round(crit["1%"], 4),
        "crit 5%":       round(crit["5%"], 4),
        "crit 10%":      round(crit["10%"], 4),
        "stationary @5%": p < 0.05,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 3. CROSS-CORRELATION FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def compute_ccf(x: pd.Series, y: pd.Series, nlags: int = MAX_LAG) -> tuple:
    """
    Compute CCF(x, y)[k] = corr(x[t], y[t-k]) for k in [-nlags, +nlags].

    Interpretation (when x = wars, y = color):
      k > 0  →  color preceded wars by k years  →  COLOR LEADS
      k < 0  →  color followed wars by k years  →  wars LEAD
      k = 0  →  contemporaneous correlation

    Returns
    -------
    lags   : np.ndarray, integer lags from -nlags to +nlags
    values : np.ndarray, Pearson r at each lag
    ci     : float, 95% confidence half-width = 1.96 / sqrt(n)
    """
    xc, yc = x.dropna().align(y.dropna(), join="inner")
    n = len(xc)
    ci = 1.96 / np.sqrt(n)

    results = {}
    xv, yv = xc.values, yc.values

    for k in range(-nlags, nlags + 1):
        if k == 0:
            a, b = xv, yv
        elif k > 0:
            # corr(x[t], y[t-k]):  x from index k onward, y from start
            a = xv[k:]
            b = yv[:-k]
        else:
            # k < 0: let m = -k > 0
            # corr(x[t], y[t+m]):  x up to T-m, y from index m onward
            m = -k
            a = xv[:-m]
            b = yv[m:]
        results[k] = np.corrcoef(a, b)[0, 1]

    lags   = np.arange(-nlags, nlags + 1)
    values = np.array([results[k] for k in lags])
    return lags, values, ci


# ─────────────────────────────────────────────────────────────────────────────
# 4. GRANGER CAUSALITY TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_granger(
    caused: pd.Series,
    causing: pd.Series,
    maxlag: int = MAX_LAG,
) -> pd.DataFrame:
    """
    Test H₀: `causing` does NOT Granger-cause `caused`.

    Uses the F-test (sum-of-squared-residuals form) from statsmodels.
    Both series are passed as first differences if they are I(1).

    Returns a DataFrame indexed by lag with F-stat, p-value, chi²-stat, chi²-p.
    """
    df2 = pd.concat([caused, causing], axis=1).dropna()
    df2.columns = ["caused", "causing"]

    raw = grangercausalitytests(df2[["caused", "causing"]], maxlag=maxlag, verbose=False)

    rows = []
    for lag, res in raw.items():
        f_test   = res[0]["ssr_ftest"]    # (F, p, df_denom, df_num)
        chi_test = res[0]["ssr_chi2test"] # (chi2, p, df)
        rows.append({
            "lag":       lag,
            "F_stat":    round(f_test[0],   4),
            "F_pvalue":  round(f_test[1],   4),
            "chi2_stat": round(chi_test[0], 4),
            "chi2_pval": round(chi_test[1], 4),
            "df_denom":  int(f_test[2]),
        })

    return pd.DataFrame(rows).set_index("lag")


# ─────────────────────────────────────────────────────────────────────────────
# 5. SUMMARY TABLE  (human-readable significance stars)
# ─────────────────────────────────────────────────────────────────────────────

def significance_stars(p: float) -> str:
    if p < 0.001: return "***"
    if p < 0.01:  return "**"
    if p < 0.05:  return "*"
    if p < 0.10:  return "."
    return ""


def print_granger_table(df: pd.DataFrame, title: str) -> None:
    print(f"\n{title}")
    print("-" * 52)
    print(f"{'lag':>4}  {'F-stat':>8}  {'p(F)':>8}  {'sig':>4}  {'chi²-p':>8}")
    print("-" * 52)
    for lag, row in df.iterrows():
        stars = significance_stars(row["F_pvalue"])
        print(
            f"{lag:>4}  {row['F_stat']:>8.4f}  {row['F_pvalue']:>8.4f}"
            f"  {stars:>4}  {row['chi2_pval']:>8.4f}"
        )
    print("Signif. codes: *** p<0.001  ** p<0.01  * p<0.05  . p<0.10")


# ─────────────────────────────────────────────────────────────────────────────
# 6. PLOT
# ─────────────────────────────────────────────────────────────────────────────

def plot_results(
    df: pd.DataFrame,
    lags_lv: np.ndarray, ccf_lv: np.ndarray, ci_lv: float,
    lags_df: np.ndarray, ccf_df: np.ndarray, ci_df: float,
    granger_fwd: pd.DataFrame,
    granger_rev: pd.DataFrame,
    out_path: str = "granger_ccf.pdf",
) -> None:
    """
    4-panel figure:
      (a) raw time series (dual y-axis)
      (b) CCF at levels
      (c) CCF at first differences
      (d) Granger causality F-test p-values
    """
    C1, C2 = "steelblue", "firebrick"

    fig = plt.figure(figsize=(14, 12))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.44, wspace=0.38)

    # ── (a) Raw time series ──────────────────────────────────────────────────
    ax0   = fig.add_subplot(gs[0, 0])
    ax0_r = ax0.twinx()

    ax0.plot(df.index, df["wars_smooth"], color=C1, lw=1.8, label="wars_smooth")
    ax0_r.plot(df.index, df["color"], color=C2, lw=1.2, linestyle="--",
               alpha=0.85, label="COLOR")

    ax0.set_xlabel("Year")
    ax0.set_ylabel("Wars (11-yr smooth)", color=C1)
    ax0_r.set_ylabel("COLOR index", color=C2)
    ax0.tick_params(axis="y", labelcolor=C1)
    ax0_r.tick_params(axis="y", labelcolor=C2)
    ax0.set_title("(a) Raw series: wars_smooth & COLOR")

    lines1, lab1 = ax0.get_legend_handles_labels()
    lines2, lab2 = ax0_r.get_legend_handles_labels()
    ax0.legend(lines1 + lines2, lab1 + lab2, fontsize=8, loc="upper right")

    # ── (b) CCF – levels ────────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 1])

    bar_colors_lv = [C2 if r < 0 else C1 for r in ccf_lv]
    ax1.bar(lags_lv, ccf_lv, color=bar_colors_lv, alpha=0.75, width=0.8)
    ax1.axhline(0,     color="black", lw=0.8)
    ax1.axhline( ci_lv, color="grey", lw=1.0, linestyle="--",
                label=f"95% CI (±{ci_lv:.3f})")
    ax1.axhline(-ci_lv, color="grey", lw=1.0, linestyle="--")
    ax1.axvline(0,     color="black", lw=0.5, linestyle=":")

    best_lv = lags_lv[np.argmax(np.abs(ccf_lv))]
    ax1.axvline(best_lv, color=C2, lw=1.5, linestyle="-.",
                label=f"max |CCF| at lag={best_lv}")

    ax1.set_xlabel("Lag  (positive = COLOR leads wars)")
    ax1.set_ylabel("Cross-correlation  r")
    ax1.set_title("(b) CCF: COLOR vs. wars_smooth  [levels]")
    ax1.legend(fontsize=8)
    ax1.set_xticks(lags_lv[::2])

    # ── (c) CCF – first differences ─────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])

    bar_colors_df = [C2 if r < 0 else C1 for r in ccf_df]
    ax2.bar(lags_df, ccf_df, color=bar_colors_df, alpha=0.75, width=0.8)
    ax2.axhline(0,     color="black", lw=0.8)
    ax2.axhline( ci_df, color="grey", lw=1.0, linestyle="--",
                label=f"95% CI (±{ci_df:.3f})")
    ax2.axhline(-ci_df, color="grey", lw=1.0, linestyle="--")
    ax2.axvline(0,     color="black", lw=0.5, linestyle=":")

    best_df = lags_df[np.argmax(np.abs(ccf_df))]
    ax2.axvline(best_df, color=C2, lw=1.5, linestyle="-.",
                label=f"max |CCF| at lag={best_df}")

    ax2.set_xlabel("Lag  (positive = ΔCOLOR leads Δwars)")
    ax2.set_ylabel("Cross-correlation  r")
    ax2.set_title("(c) CCF: ΔCOLOR vs. Δwars_smooth  [first differences]")
    ax2.legend(fontsize=8)
    ax2.set_xticks(lags_df[::2])

    # ── (d) Granger p-values ─────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])

    ax3.plot(granger_fwd.index, granger_fwd["F_pvalue"], "o-", color=C2, lw=1.8,
             label="COLOR → wars  (H₀: COLOR does NOT Granger-cause wars)")
    ax3.plot(granger_rev.index, granger_rev["F_pvalue"], "s--", color=C1, lw=1.4,
             label="wars → COLOR  (reverse / spuriousness check)")

    ax3.axhline(0.05, color="black", lw=1.0, linestyle="--", label="α = 0.05")
    ax3.axhline(0.01, color="grey",  lw=0.8, linestyle=":",  label="α = 0.01")
    ax3.set_yscale("log")
    ax3.set_xlabel("Lag (years)")
    ax3.set_ylabel("F-test p-value  (log scale)")
    ax3.set_title("(d) Granger causality  [Δwars_smooth, ΔCOLOR]")
    ax3.legend(fontsize=7.5, loc="upper right")
    ax3.set_xticks(granger_fwd.index)

    plt.suptitle(
        "CPS – Granger Causality & Cross-Correlation Analysis\n"
        "COLOR (N-gram hostility index) vs. wars_smooth (COW 1816–2007)",
        fontsize=11,
        y=1.02,
    )

    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 7. MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from pathlib import Path

    csv_path = "wars_color.csv"
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]

    out_dir = Path(csv_path).parent

    print(f"Loading data from {csv_path} …")
    df = load_df(csv_path)
    print(f"  Series length: {len(df)}  ({df.index[0]}–{df.index[-1]})")

    wars  = df["wars_smooth"].dropna()
    color = df["color"].dropna()

    wars_d  = wars.diff().dropna()
    color_d = color.diff().dropna()

    # ── 7A. ADF stationarity ─────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print("ADF STATIONARITY TESTS")
    print("═" * 64)
    adf_df = pd.DataFrame([
        adf_report(wars,    "wars_smooth"),
        adf_report(wars_d,  "Δwars_smooth"),
        adf_report(color,   "color"),
        adf_report(color_d, "Δcolor"),
    ]).set_index("series")
    print(adf_df.to_string())

    # ── 7B. CCF – levels ─────────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print("CCF – LEVELS   CCF(wars, color)[k] = corr(wars[t], color[t-k])")
    print("  positive lag k → COLOR preceded wars by k years  (COLOR LEADS)")
    print("═" * 64)

    lags_lv, ccf_lv, ci_lv = compute_ccf(wars, color, nlags=MAX_LAG)

    best_idx_lv = np.argmax(np.abs(ccf_lv))
    best_lag_lv = lags_lv[best_idx_lv]
    print(f"  Max |CCF| = {ccf_lv[best_idx_lv]:.4f} at lag = {best_lag_lv}")
    print(f"  95% CI: ±{ci_lv:.4f}")
    print()

    ccf_lv_df = pd.DataFrame({
        "lag": lags_lv,
        "CCF": np.round(ccf_lv, 4),
        "sig": [significance_stars(
                    max(0.0, 1 - abs(r) / ci_lv * 1.96 * ci_lv)   # rough p-proxy
                ) for r in ccf_lv],
    }).set_index("lag")

    # Simpler: just flag which lags exceed the CI
    print(f"  {'lag':>4}  {'CCF':>8}  {'|r|>CI':>7}")
    for k, r in zip(lags_lv, ccf_lv):
        flag = "  *" if abs(r) > ci_lv else ""
        print(f"  {k:>4}  {r:>8.4f}{flag}")

    # ── 7C. CCF – first differences ──────────────────────────────────────────
    print("\n" + "═" * 64)
    print("CCF – FIRST DIFFERENCES   corr(Δwars[t], Δcolor[t-k])")
    print("  positive lag k → ΔCOLOR preceded Δwars by k years  (COLOR LEADS)")
    print("═" * 64)

    lags_df, ccf_df, ci_df = compute_ccf(wars_d, color_d, nlags=MAX_LAG)

    best_idx_df = np.argmax(np.abs(ccf_df))
    best_lag_df = lags_df[best_idx_df]
    print(f"  Max |CCF| = {ccf_df[best_idx_df]:.4f} at lag = {best_lag_df}")
    print(f"  95% CI: ±{ci_df:.4f}")
    print()

    print(f"  {'lag':>4}  {'CCF':>8}  {'|r|>CI':>7}")
    for k, r in zip(lags_df, ccf_df):
        flag = "  *" if abs(r) > ci_df else ""
        print(f"  {k:>4}  {r:>8.4f}{flag}")

    # ── 7D. Granger causality ─────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print("GRANGER CAUSALITY TESTS  (on first-differenced series)")
    print("═" * 64)
    print("  NOTE: wars_smooth is an 11-yr MA; effective n is reduced.")
    print("  Interpret significance levels conservatively.\n")

    granger_fwd = run_granger(wars_d, color_d, maxlag=MAX_LAG)
    granger_rev = run_granger(color_d, wars_d, maxlag=MAX_LAG)

    print_granger_table(
        granger_fwd,
        "H₀: ΔCOLOR does NOT Granger-cause Δwars_smooth  (COLOR → wars)"
    )
    print_granger_table(
        granger_rev,
        "H₀: Δwars_smooth does NOT Granger-cause ΔCOLOR  (wars → COLOR,  reverse check)"
    )

    # ── 7E. Save CSV outputs ──────────────────────────────────────────────────
    adf_path = out_dir / "granger_ccf_adf.csv"
    adf_df.to_csv(adf_path)
    print(f"\n✓ Saved {adf_path}")

    ccf_out = pd.DataFrame({
        "lag":        lags_lv,
        "CCF_levels": np.round(ccf_lv, 6),
        "CCF_diff":   np.round(ccf_df, 6),
        "CI_95_levels": round(ci_lv, 6),
        "CI_95_diff":   round(ci_df, 6),
    }).set_index("lag")
    ccf_path = out_dir / "granger_ccf_ccf.csv"
    ccf_out.to_csv(ccf_path)
    print(f"✓ Saved {ccf_path}")

    granger_fwd_out = granger_fwd.copy()
    granger_fwd_out["direction"] = "COLOR→wars"
    granger_rev_out = granger_rev.copy()
    granger_rev_out["direction"] = "wars→COLOR"
    granger_all = pd.concat([granger_fwd_out, granger_rev_out])
    granger_path = out_dir / "granger_ccf_granger.csv"
    granger_all.to_csv(granger_path)
    print(f"✓ Saved {granger_path}")

    # ── 7F. Plot ──────────────────────────────────────────────────────────────
    pdf_path = str(out_dir / "granger_ccf.pdf")
    plot_results(
        df,
        lags_lv, ccf_lv, ci_lv,
        lags_df, ccf_df, ci_df,
        granger_fwd, granger_rev,
        out_path=pdf_path,
    )
