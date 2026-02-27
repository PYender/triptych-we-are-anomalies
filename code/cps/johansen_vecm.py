# johansen_vecm.py – Johansen Cointegration Test & VECM for CPS
# COLOR_smooth (N-gram hostility index, smoothed) vs. wars_smooth
# Data: wars_color.csv  (COW inter-state wars 1816–2007)
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# License: CC BY-NC-SA 4.0
#
# RATIONALE:
#   Granger tests on first differences found no COLOR→wars predictability.
#   The Triptych identifies a key cause: "different clocks and filters" —
#   COLOR is annual, wars_smooth is an 11-year centred MA.  Applying the
#   same smoothing to COLOR (as suggested by §III.3.2) puts both series on
#   the same temporal scale and permits testing whether a long-run equilibrium
#   relationship (cointegration) exists even when short-run Granger does not.
#
# METHODOLOGY:
#   1. Compute color_smooth = centred moving average of color (window W)
#   2. ADF tests: confirm both series are I(1) after smoothing
#   3. Johansen trace test: determine cointegration rank r
#   4. If r ≥ 1: fit VECM, extract cointegrating vector + adjustment speeds
#   5. CCF on (wars_smooth, color_smooth) levels and first differences
#   6. 4-panel figure
#
# USAGE:
#   python johansen_vecm.py [wars_color.csv] [--window W]
#
#   W = smoothing window for COLOR (default 11, same as wars_smooth)
#       Triptych suggests 5–11; both are reported.
#
# OUTPUT:
#   johansen_vecm_W{W}.pdf
#   johansen_vecm_adf_W{W}.csv
#   johansen_vecm_johansen_W{W}.csv
#   johansen_vecm_vecm_W{W}.csv   (VECM coefficients, if cointegrated)

from __future__ import annotations
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM

warnings.filterwarnings("ignore")

ADF_LAGS = 5
MAX_CCF  = 15   # lags for CCF display

# ─────────────────────────────────────────────────────────────────────────────
# 1. DATA
# ─────────────────────────────────────────────────────────────────────────────

def load_and_prepare(csv_path: str, window: int) -> pd.DataFrame:
    """
    Load wars_color.csv, compute color_smooth as a centred MA of `color`
    with the given window, return aligned DataFrame with both smooth series.
    """
    df = pd.read_csv(csv_path).set_index("year").sort_index()

    # centred moving average — same method as wars_smooth
    df["color_smooth"] = (
        df["color"]
        .rolling(window=window, center=True, min_periods=window)
        .mean()
    )

    # keep only rows where both smoothed series are defined
    df = df.dropna(subset=["wars_smooth", "color_smooth"])
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 2. ADF
# ─────────────────────────────────────────────────────────────────────────────

def adf_report(series: pd.Series, name: str, maxlag: int = ADF_LAGS) -> dict:
    clean = series.dropna()
    stat, p, lags_used, nobs, crit, _ = adfuller(clean, maxlag=maxlag, autolag="AIC")
    return {
        "series":         name,
        "ADF stat":       round(stat, 4),
        "p-value":        round(p, 4),
        "lags used":      lags_used,
        "nobs":           nobs,
        "crit 1%":        round(crit["1%"], 4),
        "crit 5%":        round(crit["5%"], 4),
        "stationary @5%": p < 0.05,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 3. CCF
# ─────────────────────────────────────────────────────────────────────────────

def compute_ccf(x: pd.Series, y: pd.Series, nlags: int = MAX_CCF) -> tuple:
    """
    CCF(x, y)[k] = corr(x[t], y[t-k])
    positive k → y preceded x by k years  (y LEADS x)
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


# ─────────────────────────────────────────────────────────────────────────────
# 4. JOHANSEN TEST
# ─────────────────────────────────────────────────────────────────────────────

def run_johansen(s1: pd.Series, s2: pd.Series, k_ar_diff: int = 2) -> dict:
    """
    Johansen trace test for cointegration between s1 and s2.

    det_order = 0: constant restricted to cointegrating space
                   (standard choice when series have no deterministic trend
                    beyond what the cointegrating vector captures)

    Returns a dict with trace statistics, eigenvalues, critical values,
    and the determined cointegration rank.
    """
    aligned = pd.concat([s1, s2], axis=1).dropna()
    aligned.columns = ["wars_smooth", "color_smooth"]

    result = coint_johansen(aligned.values, det_order=0, k_ar_diff=k_ar_diff)

    # trace statistics and 95% critical values
    trace_stat = result.lr1          # shape (2,): H0: r=0, H0: r≤1
    trace_cv   = result.cvt[:, 1]   # 95% critical values (col 1 = 95%)
    eig_stat   = result.lr2          # max eigenvalue statistics
    eig_cv     = result.cvm[:, 1]

    # determine rank: smallest r such that trace_stat[r] < trace_cv[r]
    rank = 0
    for i in range(len(trace_stat)):
        if trace_stat[i] > trace_cv[i]:
            rank = i + 1

    return {
        "trace_stat":  trace_stat,
        "trace_cv95":  trace_cv,
        "eig_stat":    eig_stat,
        "eig_cv95":    eig_cv,
        "rank":        rank,
        "eigenvectors": result.evec,   # cointegrating vectors (columns)
        "raw":         result,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 5. VECM
# ─────────────────────────────────────────────────────────────────────────────

def run_vecm(s1: pd.Series, s2: pd.Series,
             coint_rank: int, k_ar_diff: int = 2) -> object:
    """
    Fit VECM(k_ar_diff) with given cointegration rank.
    Variable order: [wars_smooth, color_smooth]
    """
    aligned = pd.concat([s1, s2], axis=1).dropna()
    aligned.columns = ["wars_smooth", "color_smooth"]

    model  = VECM(aligned, k_ar_diff=k_ar_diff,
                  coint_rank=coint_rank, deterministic="ci")
    result = model.fit()
    return result, aligned


def print_vecm_summary(result, aligned: pd.DataFrame) -> None:
    """Print the key VECM coefficients in a readable format."""
    print("\n  Cointegrating vector β  (normalized on wars_smooth):")
    beta = result.beta          # shape (k, r)
    print(f"    wars_smooth:   {beta[0, 0]:.4f}  (normalized to 1)")
    print(f"    color_smooth:  {beta[1, 0]:.4f}")
    if beta.shape[0] > 2:
        print(f"    const:         {beta[2, 0]:.4f}")

    print("\n  Speed-of-adjustment α  (how fast each variable corrects):")
    alpha = result.alpha        # shape (k, r)
    print(f"    α_wars:   {alpha[0, 0]:.4f}  "
          f"({'corrects' if alpha[0,0] < 0 else 'diverges'})")
    print(f"    α_color:  {alpha[1, 0]:.4f}  "
          f"({'corrects' if alpha[1,0] < 0 else 'diverges'})")

    # half-life of adjustment
    for name, a in zip(["wars", "color"], alpha[:, 0]):
        if a != 0 and a < 0:
            hl = -np.log(2) / np.log(1 + a)
            print(f"    half-life of {name} adjustment: {hl:.1f} years")


# ─────────────────────────────────────────────────────────────────────────────
# 6. PLOT
# ─────────────────────────────────────────────────────────────────────────────

def plot_all(
    df: pd.DataFrame,
    lags_lv: np.ndarray, ccf_lv: np.ndarray, ci_lv: float,
    lags_df: np.ndarray, ccf_df: np.ndarray, ci_df: float,
    johansen_result: dict,
    vecm_result,
    aligned: pd.DataFrame,
    window: int,
    out_path: str,
) -> None:
    """
    4-panel figure:
      (a) wars_smooth & color_smooth (dual y-axis)
      (b) CCF levels
      (c) Johansen trace statistics vs. 95% critical values
      (d) VECM fitted vs. actual wars_smooth  (or CCF diff if no cointegration)
    """
    C1, C2 = "steelblue", "firebrick"

    fig = plt.figure(figsize=(14, 12))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.44, wspace=0.38)

    # ── (a) smoothed series ──────────────────────────────────────────────────
    ax0   = fig.add_subplot(gs[0, 0])
    ax0_r = ax0.twinx()

    ax0.plot(df.index, df["wars_smooth"],   color=C1, lw=1.8,
             label="wars_smooth")
    ax0_r.plot(df.index, df["color_smooth"], color=C2, lw=1.4,
               linestyle="--", alpha=0.9, label=f"color_smooth (W={window})")

    ax0.set_xlabel("Year")
    ax0.set_ylabel("wars_smooth", color=C1)
    ax0_r.set_ylabel(f"color_smooth (W={window})", color=C2)
    ax0.tick_params(axis="y", labelcolor=C1)
    ax0_r.tick_params(axis="y", labelcolor=C2)
    ax0.set_title(f"(a) wars_smooth & color_smooth  [W={window}]")

    lines1, lab1 = ax0.get_legend_handles_labels()
    lines2, lab2 = ax0_r.get_legend_handles_labels()
    ax0.legend(lines1 + lines2, lab1 + lab2, fontsize=8, loc="upper right")

    # ── (b) CCF – levels ────────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 1])

    bar_colors = [C2 if r < 0 else C1 for r in ccf_lv]
    ax1.bar(lags_lv, ccf_lv, color=bar_colors, alpha=0.75, width=0.8)
    ax1.axhline(0,      color="black", lw=0.8)
    ax1.axhline( ci_lv, color="grey",  lw=1.0, linestyle="--",
                label=f"95% CI (±{ci_lv:.3f})")
    ax1.axhline(-ci_lv, color="grey",  lw=1.0, linestyle="--")
    ax1.axvline(0,      color="black", lw=0.5, linestyle=":")

    best_lv = lags_lv[np.argmax(np.abs(ccf_lv))]
    ax1.axvline(best_lv, color=C2, lw=1.5, linestyle="-.",
                label=f"max |CCF| at lag={best_lv}")

    ax1.set_xlabel("Lag  (positive = color_smooth leads wars_smooth)")
    ax1.set_ylabel("Cross-correlation  r")
    ax1.set_title(f"(b) CCF: color_smooth vs. wars_smooth  [levels, W={window}]")
    ax1.legend(fontsize=8)
    ax1.set_xticks(lags_lv[::3])

    # ── (c) Johansen trace test ──────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])

    hypotheses = ["H₀: r = 0", "H₀: r ≤ 1"]
    x_pos = np.array([0, 1])
    bar_w = 0.3

    bars_stat = ax2.bar(x_pos - bar_w/2,
                        johansen_result["trace_stat"],
                        width=bar_w, color=C2, alpha=0.8,
                        label="Trace statistic")
    bars_cv   = ax2.bar(x_pos + bar_w/2,
                        johansen_result["trace_cv95"],
                        width=bar_w, color="grey", alpha=0.6,
                        label="95% critical value")

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(hypotheses)
    ax2.set_ylabel("Trace statistic")
    ax2.set_title(f"(c) Johansen trace test  [W={window},  rank={johansen_result['rank']}]")
    ax2.legend(fontsize=8)

    # annotate with values
    for bar, val in zip(bars_stat, johansen_result["trace_stat"]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f"{val:.2f}", ha="center", va="bottom", fontsize=8)
    for bar, val in zip(bars_cv, johansen_result["trace_cv95"]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f"{val:.2f}", ha="center", va="bottom", fontsize=8, color="grey")

    rank = johansen_result["rank"]
    coint_label = f"Cointegration rank = {rank}" if rank > 0 else "No cointegration detected"
    ax2.set_xlabel(coint_label)

    # ── (d) VECM fitted vs. actual  OR  CCF diff ────────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])

    if vecm_result is not None:
        # VECM in-sample fitted values for wars_smooth
        fitted   = vecm_result.fittedvalues
        n_fitted = len(fitted)
        idx      = aligned.index[-n_fitted:]
        actual   = aligned["wars_smooth"].iloc[-n_fitted:]

        ax3.plot(idx, actual.values,   color=C1, lw=1.8, label="wars_smooth (actual)")
        ax3.plot(idx, fitted[:, 0], color=C2, lw=1.2, linestyle="--",
                 alpha=0.85, label="VECM fitted")
        ax3.set_xlabel("Year")
        ax3.set_ylabel("wars_smooth")
        ax3.set_title(f"(d) VECM in-sample fit  [W={window}]")
        ax3.legend(fontsize=8)
    else:
        # fall back to CCF on differences
        bar_colors_df = [C2 if r < 0 else C1 for r in ccf_df]
        ax3.bar(lags_df, ccf_df, color=bar_colors_df, alpha=0.75, width=0.8)
        ax3.axhline(0,      color="black", lw=0.8)
        ax3.axhline( ci_df, color="grey",  lw=1.0, linestyle="--",
                    label=f"95% CI (±{ci_df:.3f})")
        ax3.axhline(-ci_df, color="grey",  lw=1.0, linestyle="--")
        ax3.axvline(0,      color="black", lw=0.5, linestyle=":")
        best_df = lags_df[np.argmax(np.abs(ccf_df))]
        ax3.axvline(best_df, color=C2, lw=1.5, linestyle="-.",
                    label=f"max |CCF| at lag={best_df}")
        ax3.set_xlabel("Lag  (positive = Δcolor_smooth leads Δwars_smooth)")
        ax3.set_ylabel("Cross-correlation  r")
        ax3.set_title(f"(d) CCF: Δcolor_smooth vs. Δwars_smooth  [diff, W={window}]")
        ax3.legend(fontsize=8)

    plt.suptitle(
        f"CPS – Johansen Cointegration & VECM\n"
        f"color_smooth (W={window}) vs. wars_smooth  (COW 1816–2007)",
        fontsize=11, y=1.02,
    )
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"\n✓ Saved {out_path}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 7. MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Johansen cointegration & VECM for CPS"
    )
    parser.add_argument("csv", nargs="?", default="wars_color.csv")
    parser.add_argument("--window", type=int, default=11,
                        help="Smoothing window for color_smooth (default 11)")
    parser.add_argument("--k-ar-diff", type=int, default=2,
                        help="Lagged differences in VAR/VECM (default 2)")
    args = parser.parse_args()

    W         = args.window
    K         = args.k_ar_diff
    csv_path  = args.csv
    out_dir   = Path(csv_path).parent
    tag       = f"W{W}"

    print(f"Loading {csv_path}  |  color smoothing window = {W}  |  k_ar_diff = {K}")
    df = load_and_prepare(csv_path, window=W)
    print(f"  Usable observations after smoothing: {len(df)}  "
          f"({df.index[0]}–{df.index[-1]})")

    wars_s  = df["wars_smooth"]
    color_s = df["color_smooth"]

    # ── 7A. ADF ──────────────────────────────────────────────────────────────
    print("\n" + "═" * 64)
    print(f"ADF STATIONARITY TESTS  [color smoothed W={W}]")
    print("═" * 64)
    adf_rows = [
        adf_report(wars_s,           "wars_smooth"),
        adf_report(wars_s.diff(),    "Δwars_smooth"),
        adf_report(color_s,          f"color_smooth_W{W}"),
        adf_report(color_s.diff(),   f"Δcolor_smooth_W{W}"),
    ]
    adf_df = pd.DataFrame(adf_rows).set_index("series")
    print(adf_df.to_string())

    # ── 7B. CCF – levels ─────────────────────────────────────────────────────
    print(f"\n" + "═" * 64)
    print(f"CCF – LEVELS  (color_smooth_W{W} vs. wars_smooth)")
    print(f"  positive lag k → color_smooth preceded wars_smooth by k years")
    print("═" * 64)

    lags_lv, ccf_lv, ci_lv = compute_ccf(wars_s, color_s, nlags=MAX_CCF)
    best_lv = lags_lv[np.argmax(np.abs(ccf_lv))]
    print(f"  Max |CCF| = {ccf_lv[np.argmax(np.abs(ccf_lv))]:.4f} at lag = {best_lv}")
    print(f"  95% CI: ±{ci_lv:.4f}\n")

    print(f"  {'lag':>4}  {'CCF':>8}  {'|r|>CI':>7}")
    for k, r in zip(lags_lv, ccf_lv):
        flag = "  *" if abs(r) > ci_lv else ""
        print(f"  {k:>4}  {r:>8.4f}{flag}")

    # ── 7C. CCF – first differences ──────────────────────────────────────────
    wars_d  = wars_s.diff().dropna()
    color_d = color_s.diff().dropna()

    lags_df, ccf_df, ci_df = compute_ccf(wars_d, color_d, nlags=MAX_CCF)
    best_df = lags_df[np.argmax(np.abs(ccf_df))]
    print(f"\n" + "═" * 64)
    print(f"CCF – FIRST DIFFERENCES")
    print("═" * 64)
    print(f"  Max |CCF| = {ccf_df[np.argmax(np.abs(ccf_df))]:.4f} at lag = {best_df}")
    print(f"  95% CI: ±{ci_df:.4f}\n")
    print(f"  {'lag':>4}  {'CCF':>8}  {'|r|>CI':>7}")
    for k, r in zip(lags_df, ccf_df):
        flag = "  *" if abs(r) > ci_df else ""
        print(f"  {k:>4}  {r:>8.4f}{flag}")

    # ── 7D. Johansen test ─────────────────────────────────────────────────────
    print(f"\n" + "═" * 64)
    print(f"JOHANSEN COINTEGRATION TEST  [W={W}, k_ar_diff={K}]")
    print("  det_order=0: constant restricted to cointegrating space")
    print("═" * 64)

    joh = run_johansen(wars_s, color_s, k_ar_diff=K)

    print(f"\n  {'Hypothesis':<16}  {'Trace stat':>11}  {'CV 95%':>8}  {'Reject H₀?':>11}")
    print(f"  {'-'*52}")
    for i, (h, ts, cv) in enumerate(
        zip(["r = 0", "r ≤ 1"],
            joh["trace_stat"],
            joh["trace_cv95"])
    ):
        reject = "YES  ***" if ts > cv else "no"
        print(f"  H₀: {h:<12}  {ts:>11.4f}  {cv:>8.4f}  {reject:>11}")

    print(f"\n  → Determined cointegration rank: {joh['rank']}")

    # ── 7E. VECM (if cointegrated) ────────────────────────────────────────────
    vecm_result = None
    aligned     = None

    if joh["rank"] >= 1:
        print(f"\n" + "═" * 64)
        print(f"VECM  [rank={joh['rank']}, k_ar_diff={K}]")
        print("  Variable order: [wars_smooth, color_smooth]")
        print("  α < 0 on wars_smooth → wars corrects toward equilibrium  (COLOR leads)")
        print("  α < 0 on color_smooth → color corrects              (wars leads)")
        print("═" * 64)

        vecm_result, aligned = run_vecm(wars_s, color_s,
                                        coint_rank=joh["rank"],
                                        k_ar_diff=K)
        print_vecm_summary(vecm_result, aligned)
        print(f"\n  Log-likelihood: {vecm_result.llf:.2f}")

        # save VECM summary to CSV
        beta  = vecm_result.beta
        alpha = vecm_result.alpha
        vecm_csv = pd.DataFrame({
            "parameter": ["beta_wars", "beta_color", "alpha_wars", "alpha_color"],
            "value":     [beta[0,0], beta[1,0], alpha[0,0], alpha[1,0]],
        })
        vecm_path = out_dir / f"johansen_vecm_vecm_{tag}.csv"
        vecm_csv.to_csv(vecm_path, index=False)
        print(f"\n✓ Saved {vecm_path}")
    else:
        print("\n  No cointegration detected — VECM not fitted.")

    # ── 7F. Save CSV outputs ──────────────────────────────────────────────────
    adf_path = out_dir / f"johansen_vecm_adf_{tag}.csv"
    adf_df.to_csv(adf_path)
    print(f"✓ Saved {adf_path}")

    joh_csv = pd.DataFrame({
        "hypothesis":  ["r=0", "r<=1"],
        "trace_stat":  joh["trace_stat"],
        "trace_cv95":  joh["trace_cv95"],
        "eig_stat":    joh["eig_stat"],
        "eig_cv95":    joh["eig_cv95"],
        "reject_H0":   joh["trace_stat"] > joh["trace_cv95"],
    })
    joh_path = out_dir / f"johansen_vecm_johansen_{tag}.csv"
    joh_csv.to_csv(joh_path, index=False)
    print(f"✓ Saved {joh_path}")

    ccf_out = pd.DataFrame({
        "lag":        lags_lv,
        "CCF_levels": np.round(ccf_lv, 6),
        "CCF_diff":   np.round(ccf_df, 6),
    }).set_index("lag")
    ccf_path = out_dir / f"johansen_vecm_ccf_{tag}.csv"
    ccf_out.to_csv(ccf_path)
    print(f"✓ Saved {ccf_path}")

    # ── 7G. Plot ──────────────────────────────────────────────────────────────
    pdf_path = str(out_dir / f"johansen_vecm_{tag}.pdf")
    plot_all(
        df,
        lags_lv, ccf_lv, ci_lv,
        lags_df, ccf_df, ci_df,
        joh,
        vecm_result,
        aligned if aligned is not None else pd.concat([wars_s, color_s], axis=1),
        window=W,
        out_path=pdf_path,
    )
