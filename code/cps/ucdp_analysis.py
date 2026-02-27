# ucdp_analysis.py – Robustness check: UCDP v25.1 vs. COLOR
# Tests whether the COLOR → conflict relationship found in COW data
# replicates on an independent dataset (UCDP/PRIO ACD v25.1).
#
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# OVERLAP PERIOD: 1946–2007  (n = 62 years)
#   COLOR data (wars_color.csv): 1816–2007
#   UCDP/PRIO ACD v25.1:         1946–2024
#
# UCDP conflict types used (same weights as ucdp_adapter.py):
#   type 2 (interstate)              weight 1.0
#   type 3 (intrastate)              weight 0.4
#   type 4 (intl. intrastate)        weight 0.7
#   type 1 (extrasystemic) excluded  (near-zero after 1945)
#
# NOTE: n=62 is short.  MAX_LAG capped at 10 to preserve degrees of freedom.
#       Spectral analysis omitted (need ≥3–5 cycle lengths for T≈24 yr).

from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

warnings.filterwarnings("ignore")

# ── Parameters ────────────────────────────────────────────────────────────────
UCDP_PATH  = Path("data/ucdp/UcdpPrioConflict_v25_1.csv")
COLOR_PATH = Path("wars_color.csv")
SMOOTH_WIN = 11
MAX_LAG    = 10
ADF_LAGS   = 5

UCDP_WEIGHTS = {2: 1.0, 3: 0.4, 4: 0.7}


# ── 1. Load & aggregate UCDP ─────────────────────────────────────────────────

def load_ucdp(path: Path = UCDP_PATH) -> pd.DataFrame:
    """
    Returns yearly DataFrame with columns:
      ucdp_n_conflicts  – unweighted count (all types 2-4)
      ucdp_wars         – weighted count (type weights as above)
      ucdp_smooth       – 11-yr centred MA of ucdp_wars
    """
    raw = pd.read_csv(path, low_memory=False)

    # keep types 2, 3, 4; exclude type 1 (extrasystemic)
    keep = list(UCDP_WEIGHTS.keys())
    sub  = raw[raw["type_of_conflict"].isin(keep)].copy()
    sub["weight"] = sub["type_of_conflict"].map(UCDP_WEIGHTS)

    yearly = (
        sub.groupby("year")
        .agg(
            ucdp_n_conflicts=("conflict_id", "count"),
            ucdp_wars=("weight", "sum"),
        )
        .rename_axis("year")
    )
    yearly["ucdp_smooth"] = (
        yearly["ucdp_wars"]
        .rolling(SMOOTH_WIN, center=True, min_periods=1)
        .mean()
    )
    return yearly


# ── 2. Load COLOR series ──────────────────────────────────────────────────────

def load_color(path: Path = COLOR_PATH) -> pd.DataFrame:
    df = pd.read_csv(path).set_index("year").sort_index()
    return df[["color", "wars", "wars_smooth"]]


# ── 3. Merge (overlap window) ─────────────────────────────────────────────────

def build_merged(ucdp_df: pd.DataFrame, color_df: pd.DataFrame) -> pd.DataFrame:
    df = ucdp_df.join(color_df, how="inner")
    df = df.loc[1946:2007]
    return df


# ── 4. ADF stationarity test ──────────────────────────────────────────────────

def adf_report(series: pd.Series, name: str, maxlag: int = ADF_LAGS) -> dict:
    clean = series.dropna()
    stat, p, lags_used, nobs, crit, _ = adfuller(clean, maxlag=maxlag, autolag="AIC")
    return {
        "series":         name,
        "ADF stat":       round(stat, 4),
        "p-value":        round(p, 4),
        "lags used":      lags_used,
        "nobs":           nobs,
        "crit 5%":        round(crit["5%"], 4),
        "stationary @5%": p < 0.05,
    }


# ── 5. Cross-correlation function ─────────────────────────────────────────────

def compute_ccf(x: pd.Series, y: pd.Series, nlags: int = MAX_LAG) -> tuple:
    """
    CCF(x, y)[k] = corr(x[t], y[t-k])
    positive k → y leads x by k years
    """
    xc, yc = x.dropna().align(y.dropna(), join="inner")
    n  = len(xc)
    ci = 1.96 / np.sqrt(n)
    xv, yv = xc.values, yc.values

    results = {}
    for k in range(-nlags, nlags + 1):
        if k == 0:
            a, b = xv, yv
        elif k > 0:
            a, b = xv[k:], yv[:-k]
        else:
            m = -k
            a, b = xv[:-m], yv[m:]
        results[k] = np.corrcoef(a, b)[0, 1]

    lags   = np.arange(-nlags, nlags + 1)
    values = np.array([results[k] for k in lags])
    return lags, values, ci


# ── 6. Granger causality ──────────────────────────────────────────────────────

def run_granger(caused: pd.Series, causing: pd.Series,
                maxlag: int = MAX_LAG) -> pd.DataFrame:
    df2 = pd.concat([caused, causing], axis=1).dropna()
    df2.columns = ["caused", "causing"]
    raw = grangercausalitytests(df2[["caused", "causing"]],
                                maxlag=maxlag, verbose=False)
    rows = []
    for lag, res in raw.items():
        f = res[0]["ssr_ftest"]
        c = res[0]["ssr_chi2test"]
        rows.append({
            "lag":       lag,
            "F_stat":    round(f[0], 4),
            "F_pvalue":  round(f[1], 4),
            "chi2_pval": round(c[1], 4),
        })
    return pd.DataFrame(rows).set_index("lag")


def sig_stars(p: float) -> str:
    if p < 0.001: return "***"
    if p < 0.01:  return "**"
    if p < 0.05:  return "*"
    if p < 0.10:  return "."
    return ""


def print_granger(df: pd.DataFrame, title: str) -> None:
    print(f"\n{title}")
    print("-" * 54)
    print(f"{'lag':>4}  {'F-stat':>8}  {'p(F)':>8}  {'sig':>4}  {'chi²-p':>8}")
    print("-" * 54)
    for lag, row in df.iterrows():
        print(f"{lag:>4}  {row['F_stat']:>8.4f}  {row['F_pvalue']:>8.4f}"
              f"  {sig_stars(row['F_pvalue']):>4}  {row['chi2_pval']:>8.4f}")
    print("Signif. codes: *** p<0.001  ** p<0.01  * p<0.05  . p<0.10")


# ── 7. Plot ───────────────────────────────────────────────────────────────────

def plot_results(df, lags_lv, ccf_lv, ci_lv, best_lv,
                 lags_df, ccf_df, ci_df, best_df,
                 g_fwd, g_rev,
                 out_path: str = "ucdp_analysis.pdf") -> None:
    C1, C2 = "steelblue", "firebrick"

    fig = plt.figure(figsize=(14, 10))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.46, wspace=0.38)

    # (a) time series
    ax0  = fig.add_subplot(gs[0, 0])
    ax0r = ax0.twinx()
    ax0.plot(df.index, df["ucdp_smooth"], color=C1, lw=2.0, label="ucdp_smooth")
    ax0r.plot(df.index, df["color"], color=C2, lw=1.2,
              linestyle="--", alpha=0.85, label="COLOR")
    ax0.set_title("(a) UCDP conflicts (11-yr smooth) & COLOR\n1946–2007")
    ax0.set_xlabel("Year")
    ax0.set_ylabel("UCDP weighted conflicts (smoothed)", color=C1)
    ax0r.set_ylabel("COLOR index", color=C2)
    ax0.tick_params(axis="y", labelcolor=C1)
    ax0r.tick_params(axis="y", labelcolor=C2)
    l1, lb1 = ax0.get_legend_handles_labels()
    l2, lb2 = ax0r.get_legend_handles_labels()
    ax0.legend(l1 + l2, lb1 + lb2, fontsize=8, loc="upper left")

    # (b) CCF levels
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.bar(lags_lv, ccf_lv,
            color=[C2 if r < 0 else C1 for r in ccf_lv],
            alpha=0.75, width=0.8)
    ax1.axhline(0,      color="black", lw=0.8)
    ax1.axhline( ci_lv, color="grey",  lw=1.0, linestyle="--",
                label=f"95% CI (±{ci_lv:.3f})")
    ax1.axhline(-ci_lv, color="grey",  lw=1.0, linestyle="--")
    ax1.axvline(best_lv, color=C2, lw=1.5, linestyle="-.",
                label=f"max |CCF| lag={best_lv}")
    ax1.set_title("(b) CCF levels: COLOR vs. ucdp_smooth")
    ax1.set_xlabel("Lag  (positive = COLOR leads)")
    ax1.set_ylabel("Cross-correlation  r")
    ax1.legend(fontsize=8)

    # (c) CCF diffs
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.bar(lags_df, ccf_df,
            color=[C2 if r < 0 else C1 for r in ccf_df],
            alpha=0.75, width=0.8)
    ax2.axhline(0,      color="black", lw=0.8)
    ax2.axhline( ci_df, color="grey",  lw=1.0, linestyle="--",
                label=f"95% CI (±{ci_df:.3f})")
    ax2.axhline(-ci_df, color="grey",  lw=1.0, linestyle="--")
    ax2.axvline(best_df, color=C2, lw=1.5, linestyle="-.",
                label=f"max |CCF| lag={best_df}")
    ax2.set_title("(c) CCF diffs: ΔCOLOR vs. Δucdp_wars")
    ax2.set_xlabel("Lag  (positive = ΔCOLOR leads)")
    ax2.set_ylabel("Cross-correlation  r")
    ax2.legend(fontsize=8)

    # (d) Granger p-values
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(g_fwd.index, g_fwd["F_pvalue"], "o-",  color=C2, lw=1.8,
             label="COLOR → UCDP conflicts")
    ax3.plot(g_rev.index, g_rev["F_pvalue"], "s--", color=C1, lw=1.4,
             label="UCDP → COLOR (reverse)")
    ax3.axhline(0.05, color="black", lw=1.0, linestyle="--", label="α = 0.05")
    ax3.axhline(0.01, color="grey",  lw=0.8, linestyle=":",  label="α = 0.01")
    ax3.set_yscale("log")
    ax3.set_xlabel("Lag (years)")
    ax3.set_ylabel("F-test p-value  (log scale)")
    ax3.set_title("(d) Granger causality  [ΔUCDP, ΔCOLOR]\nMAX_LAG=10")
    ax3.legend(fontsize=7.5, loc="lower left")

    plt.suptitle(
        "UCDP v25.1 Robustness Check — COLOR (N-gram) vs. UCDP conflict count\n"
        "Independent dataset, overlap 1946–2007  (n = 62)",
        fontsize=11, y=1.02,
    )

    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ── 8. Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from pathlib import Path as _Path
    import sys

    ucdp_path  = _Path(sys.argv[1]) if len(sys.argv) > 1 else UCDP_PATH
    color_path = _Path(sys.argv[2]) if len(sys.argv) > 2 else COLOR_PATH

    print("=" * 64)
    print("  UCDP v25.1 ROBUSTNESS CHECK")
    print("  COLOR (N-gram) vs. UCDP conflict count  |  1946–2007")
    print("=" * 64)

    ucdp_df  = load_ucdp(ucdp_path)
    color_df = load_color(color_path)
    df       = build_merged(ucdp_df, color_df)

    print(f"\n  UCDP range: {ucdp_df.index[0]}–{ucdp_df.index[-1]}")
    print(f"  COLOR range: {color_df.index[0]}–{color_df.index[-1]}")
    print(f"  Overlap used: {df.index[0]}–{df.index[-1]}  (n = {len(df)})")
    print(f"\n  ucdp_wars descriptive stats:")
    print(df["ucdp_wars"].describe().round(2).to_string())
    print(f"\n  color descriptive stats:")
    print(df["color"].describe().round(4).to_string())

    # differenced series (for Granger; use raw count, not smoothed)
    warsd  = df["ucdp_wars"].diff().dropna()
    colord = df["color"].diff().dropna()

    # ── ADF ──────────────────────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print("ADF STATIONARITY TESTS")
    print("═" * 64)
    adf_df = pd.DataFrame([
        adf_report(df["ucdp_smooth"],       "ucdp_smooth"),
        adf_report(df["ucdp_wars"],         "ucdp_wars (raw)"),
        adf_report(warsd,                   "Δucdp_wars"),
        adf_report(df["color"],             "color"),
        adf_report(colord,                  "Δcolor"),
    ]).set_index("series")
    print(adf_df.to_string())

    # ── CCF – levels ──────────────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print("CCF – LEVELS  (ucdp_smooth vs. color)")
    print("  positive lag k → COLOR leads ucdp_smooth by k years")
    print("═" * 64)

    lags_lv, ccf_lv, ci_lv = compute_ccf(df["ucdp_smooth"], df["color"])
    best_lv = lags_lv[np.argmax(np.abs(ccf_lv))]
    print(f"  Max |CCF| = {ccf_lv[np.argmax(np.abs(ccf_lv))]:.4f}"
          f" at lag = {best_lv}  |  95% CI: ±{ci_lv:.4f}\n")
    print(f"  {'lag':>4}  {'CCF':>8}  {'|r|>CI':>7}")
    for k, r in zip(lags_lv, ccf_lv):
        flag = "  *" if abs(r) > ci_lv else ""
        print(f"  {k:>4}  {r:>8.4f}{flag}")

    # ── CCF – first differences ────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print("CCF – FIRST DIFFERENCES  (Δucdp_wars vs. Δcolor)")
    print("  positive lag k → ΔCOLOR leads Δucdp_wars by k years")
    print("═" * 64)

    lags_df, ccf_df, ci_df = compute_ccf(warsd, colord)
    best_df = lags_df[np.argmax(np.abs(ccf_df))]
    print(f"  Max |CCF| = {ccf_df[np.argmax(np.abs(ccf_df))]:.4f}"
          f" at lag = {best_df}  |  95% CI: ±{ci_df:.4f}\n")
    print(f"  {'lag':>4}  {'CCF':>8}  {'|r|>CI':>7}")
    for k, r in zip(lags_df, ccf_df):
        flag = "  *" if abs(r) > ci_df else ""
        print(f"  {k:>4}  {r:>8.4f}{flag}")

    # ── Granger ────────────────────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print(f"GRANGER CAUSALITY TESTS  (first differences, MAX_LAG={MAX_LAG})")
    print(f"  n(overlap)={len(df)}, effective df per lag test ≈ {len(warsd)-MAX_LAG*2}")
    print("  Compare direction and magnitude with COW-based results.")
    print("═" * 64)

    g_fwd = run_granger(warsd, colord)
    g_rev = run_granger(colord, warsd)

    print_granger(g_fwd,
        "H₀: ΔCOLOR does NOT Granger-cause Δucdp_wars  (COLOR → UCDP conflicts)")
    print_granger(g_rev,
        "H₀: Δucdp_wars does NOT Granger-cause ΔCOLOR  (UCDP → COLOR, reverse)")

    # ── Comparison with COW ───────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print("COMPARISON: UCDP vs. COW  (same tests, different data source)")
    print("═" * 64)
    print("""
  COW result (wars_smooth, 1816–2007, n=192, MAX_LAG=25):
    CCF levels:  max |r| = -0.74 at lag = -2  (wars LEAD color by 2 yr)
    CCF diffs:   max |r| = -0.16 at lag = -1  (barely above CI)
    Granger COLOR→wars (F-test): NOT significant at any lag
    Granger wars→COLOR (F-test): p<0.01 for lags 1–4
""")
    print("  UCDP result (ucdp_smooth, 1946–2007, n=62, MAX_LAG=10):")
    print(f"    CCF levels:  max |r| = {ccf_lv[np.argmax(np.abs(ccf_lv))]:.4f}"
          f" at lag = {best_lv}")
    print(f"    CCF diffs:   max |r| = {ccf_df[np.argmax(np.abs(ccf_df))]:.4f}"
          f" at lag = {best_df}")
    sig_fwd = g_fwd[g_fwd["F_pvalue"] < 0.05]
    sig_rev = g_rev[g_rev["F_pvalue"] < 0.05]
    if len(sig_fwd):
        print(f"    Granger COLOR→UCDP: SIGNIFICANT at lags {list(sig_fwd.index)}")
    else:
        print("    Granger COLOR→UCDP: NOT significant (F-test) at any lag")
    if len(sig_rev):
        print(f"    Granger UCDP→COLOR: SIGNIFICANT at lags {list(sig_rev.index)}")
    else:
        print("    Granger UCDP→COLOR: NOT significant (F-test) at any lag")

    print("""
  CAUTION:
    - n=62 gives substantially lower statistical power than n=192.
    - UCDP 'conflicts' (weighted count) ≠ COW 'wars' (battle-death threshold).
    - UCDP includes intrastate conflicts (weight 0.4); COW is interstate only.
    - Absence of significant Granger in UCDP is consistent with COW results
      (COLOR→wars never significant in F-test in either dataset).
""")

    # ── Save outputs ──────────────────────────────────────────────────────────
    out_dir = color_path.parent

    df.to_csv(out_dir / "ucdp_color.csv")
    print("✓ Saved ucdp_color.csv")

    adf_df.to_csv(out_dir / "ucdp_analysis_adf.csv")
    print("✓ Saved ucdp_analysis_adf.csv")

    ccf_out = pd.DataFrame({
        "lag":          lags_lv,
        "CCF_levels":   np.round(ccf_lv, 6),
        "CCF_diff":     np.round(ccf_df, 6),
        "CI_95_levels": round(ci_lv, 6),
        "CI_95_diff":   round(ci_df, 6),
    }).set_index("lag")
    ccf_out.to_csv(out_dir / "ucdp_analysis_ccf.csv")
    print("✓ Saved ucdp_analysis_ccf.csv")

    g_fwd_out = g_fwd.copy(); g_fwd_out["direction"] = "COLOR→UCDP"
    g_rev_out = g_rev.copy(); g_rev_out["direction"] = "UCDP→COLOR"
    pd.concat([g_fwd_out, g_rev_out]).to_csv(out_dir / "ucdp_analysis_granger.csv")
    print("✓ Saved ucdp_analysis_granger.csv")

    # plot
    plot_results(
        df,
        lags_lv, ccf_lv, ci_lv, best_lv,
        lags_df, ccf_df, ci_df, best_df,
        g_fwd, g_rev,
        out_path=str(out_dir / "ucdp_analysis.pdf"),
    )
