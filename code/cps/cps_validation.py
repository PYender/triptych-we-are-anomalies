# cps_validation.py – Rolling-Origin Out-of-Sample Validation for CPS
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# Extends: analiza_poprawiona_final_GDELT.py  (ARIMAX_1.1.1_COLOR_v1)
# License: CC BY-NC-SA 4.0
#
# USAGE:
#   python cps_validation.py
#
# REQUIREMENTS:
#   Same data files as analiza_poprawiona_final_GDELT.py +
#   the df / arima parameters produced by that script.
#   Run from the same directory that contains the data files.
#
# WHAT THIS DOES:
#   Rolling-origin (expanding window) cross-validation of the ARIMAX(1,1,1)
#   model.  For each origin t from MIN_TRAIN to the end of the series:
#     – train on years[0 : t]
#     – forecast horizons H = [1, 5, 10, 20] years ahead
#     – record predicted vs. actual wars_smooth
#   Then compute RMSE, MAE, MAPE per horizon and plot the results.
#
# KNOWN LIMITATION (v0.1 flag from the Triptych):
#   The exogenous path (COLOR) for the forecast window uses the *actual*
#   observed COLOR values (oracle exog), which gives an optimistic upper
#   bound on predictive skill.  A realistic scenario would hold COLOR
#   constant at the last in-sample value (as in the baseline script).
#   Both variants are computed; the oracle variant is labelled "(oracle exog)"
#   in the output tables and plots.

from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from statsmodels.tsa.arima.model import ARIMA
from tqdm.auto import tqdm

warnings.filterwarnings("ignore")   # suppress convergence noise

# =========================================================================
# 0. PARAMETERS
# =========================================================================
HORIZONS     = [1, 5, 10, 20]       # forecast horizons (years)
ARIMA_ORDER  = (1, 1, 1)            # matches the baseline script
COLOR_LAG    = 2                    # best_lag from the baseline script
MIN_TRAIN    = 60                   # minimum training window (years)
SMOOTH_WIN   = 11                   # must match the baseline script

# =========================================================================
# 1. HELPER – load the prepared dataframe produced by the baseline script
#    OR rebuild it here if wars_color.csv exists.
# =========================================================================

def load_df(csv_path: str = "wars_color.csv") -> pd.DataFrame:
    """
    Load the pre-computed DataFrame saved by analiza_poprawiona_final_GDELT.py.
    Expected columns: year, wars, wars_smooth, wars_pc, pop, color,
                      gdelt_wars, gdelt_goldstein
    """
    df = pd.read_csv(csv_path)
    df = df.set_index("year").sort_index()
    return df


# =========================================================================
# 2. ROLLING-ORIGIN VALIDATION
# =========================================================================

def rolling_origin_validate(
    df: pd.DataFrame,
    horizons: list[int] = HORIZONS,
    arima_order: tuple   = ARIMA_ORDER,
    color_lag: int       = COLOR_LAG,
    min_train: int       = MIN_TRAIN,
    oracle_exog: bool    = True,
) -> pd.DataFrame:
    """
    Expanding-window rolling-origin validation.

    Parameters
    ----------
    df          : DataFrame indexed by year with columns wars_smooth, color
    horizons    : list of forecast horizons h to evaluate
    arima_order : (p, d, q) for ARIMA
    color_lag   : lag of COLOR exog (same as baseline)
    min_train   : minimum number of training observations
    oracle_exog : if True, use actual future COLOR values as exog in forecast
                  (optimistic / upper-bound estimate).
                  if False, hold exog constant at last in-sample value
                  (matches the baseline forecasting strategy).

    Returns
    -------
    DataFrame with columns:
        origin_year, horizon, actual, predicted, error
    """
    series = df["wars_smooth"].dropna()
    color  = df["color"].dropna()

    # align color lag
    exog_full = color.shift(color_lag)

    records = []
    origins = range(min_train, len(series) - max(horizons))

    for t in tqdm(origins, desc="rolling origins", leave=False):
        train_y    = series.iloc[:t]
        train_exog = exog_full.iloc[:t]

        # drop NaN rows from the training exog
        valid = train_exog.notna()
        if valid.sum() < 10:
            continue

        try:
            model = ARIMA(
                train_y[valid],
                order=arima_order,
                exog=train_exog[valid],
            )
            fit = model.fit()
        except Exception:
            continue

        origin_year = series.index[t]

        for h in horizons:
            target_idx = t + h
            if target_idx >= len(series):
                continue

            actual = series.iloc[target_idx]

            if oracle_exog:
                # use actual future COLOR values
                fut_exog = exog_full.iloc[t : t + h]
                # fill any NaN with last known value
                fut_exog = fut_exog.ffill().fillna(
                    exog_full.iloc[:t].dropna().iloc[-1]
                )
            else:
                # hold constant at last in-sample value (baseline strategy)
                last_val = exog_full.iloc[:t].dropna().iloc[-1]
                fut_exog = np.repeat(last_val, h)

            try:
                fc = fit.get_forecast(steps=h, exog=fut_exog)
                predicted = fc.predicted_mean.iloc[-1]
            except Exception:
                continue

            records.append({
                "origin_year": origin_year,
                "horizon":     h,
                "actual":      actual,
                "predicted":   predicted,
                "error":       predicted - actual,
            })

    return pd.DataFrame(records)


# =========================================================================
# 3. METRICS
# =========================================================================

def compute_metrics(results: pd.DataFrame) -> pd.DataFrame:
    """
    Compute RMSE, MAE, MAPE per horizon.
    """
    rows = []
    for h, grp in results.groupby("horizon"):
        err  = grp["error"]
        act  = grp["actual"]
        rmse = np.sqrt((err ** 2).mean())
        mae  = err.abs().mean()
        # MAPE: skip near-zero actuals
        mask = act.abs() > 0.01
        mape = (err[mask].abs() / act[mask].abs()).mean() * 100

        rows.append({
            "horizon":          h,
            "n_origins":        len(grp),
            "RMSE":             round(rmse, 4),
            "MAE":              round(mae,  4),
            "MAPE_%":           round(mape, 2),
            "bias (mean_err)":  round(err.mean(), 4),
        })
    return pd.DataFrame(rows).set_index("horizon")


# =========================================================================
# 4. PLOTS
# =========================================================================

def plot_validation(
    results: pd.DataFrame,
    df: pd.DataFrame,
    metrics_oracle: pd.DataFrame,
    metrics_const:  pd.DataFrame,
    out_path: str = "cps_validation.pdf",
):
    """
    4-panel validation figure:
      (a) actual wars_smooth + rolling 1-step-ahead predictions
      (b) error distribution per horizon (box-plot)
      (c) RMSE by horizon – oracle vs constant exog
      (d) scatter: actual vs predicted for each horizon
    """
    fig = plt.figure(figsize=(14, 12))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.40, wspace=0.35)

    # ── (a) time-series: actual + h=1 predictions ──────────────────────
    ax0 = fig.add_subplot(gs[0, :])    # full width
    h1  = results[results["horizon"] == 1].set_index("origin_year")
    ax0.plot(df.index, df["wars_smooth"], lw=2,  color="steelblue",
             label="wars_smooth (actual)")
    ax0.plot(h1.index, h1["predicted"],  lw=1.2, color="tomato",
             linestyle="--", label="1-yr-ahead forecast (oracle exog)")
    ax0.fill_between(
        h1.index,
        h1["predicted"] - h1["error"].std(),
        h1["predicted"] + h1["error"].std(),
        alpha=0.15, color="tomato"
    )
    ax0.set_title("Rolling-origin 1-year-ahead forecasts vs. actual  [ARIMAX(1,1,1)]")
    ax0.set_xlabel("Year"); ax0.set_ylabel("Number of wars (11-yr smoothed)")
    ax0.legend(fontsize=9)

    # ── (b) error distributions by horizon ──────────────────────────────
    ax1 = fig.add_subplot(gs[1, 0])
    data_box = [results[results["horizon"] == h]["error"].values
                for h in HORIZONS]
    bp = ax1.boxplot(data_box, labels=[f"h={h}" for h in HORIZONS],
                     patch_artist=True, medianprops=dict(color="black"))
    for patch in bp["boxes"]:
        patch.set_facecolor("steelblue")
        patch.set_alpha(0.6)
    ax1.axhline(0, color="grey", lw=0.8, linestyle=":")
    ax1.set_title("Forecast error distribution per horizon")
    ax1.set_ylabel("predicted − actual  (wars)"); ax1.set_xlabel("Horizon")

    # ── (c) RMSE by horizon: oracle vs constant ──────────────────────────
    ax2 = fig.add_subplot(gs[1, 1])
    hor = metrics_oracle.index.astype(int)
    ax2.plot(hor, metrics_oracle["RMSE"], "o-", color="tomato",
             label="oracle exog (upper bound)")
    ax2.plot(hor, metrics_const["RMSE"],  "s--", color="steelblue",
             label="constant exog (baseline)")
    ax2.set_title("RMSE vs. forecast horizon")
    ax2.set_xlabel("Horizon (years)"); ax2.set_ylabel("RMSE (wars)")
    ax2.legend(fontsize=9)
    ax2.set_xticks(hor)

    plt.suptitle(
        "CPS – ARIMAX(1,1,1) rolling-origin validation  |  "
        "training window: expanding  |  COW 1816–2007",
        fontsize=11, y=1.01
    )
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"✓ Saved {out_path}")
    plt.show()


# =========================================================================
# 5. MAIN
# =========================================================================

if __name__ == "__main__":
    import sys

    csv_path = "wars_color.csv"
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]

    print(f"Loading data from {csv_path} …")
    df = load_df(csv_path)
    print(f"  Series length: {len(df)}  ({df.index[0]}–{df.index[-1]})")

    # ── oracle exog (optimistic) ─────────────────────────────────────────
    print("\nRunning rolling-origin validation  [oracle exog] …")
    res_oracle = rolling_origin_validate(df, oracle_exog=True)
    metrics_oracle = compute_metrics(res_oracle)

    # ── constant exog (matches baseline script) ──────────────────────────
    print("Running rolling-origin validation  [constant exog] …")
    res_const  = rolling_origin_validate(df, oracle_exog=False)
    metrics_const = compute_metrics(res_const)

    # ── print tables ─────────────────────────────────────────────────────
    print("\n" + "="*58)
    print("METRICS — oracle exog (optimistic / upper bound)")
    print("="*58)
    print(metrics_oracle.to_string())

    print("\n" + "="*58)
    print("METRICS — constant exog (baseline strategy)")
    print("="*58)
    print(metrics_const.to_string())

    # ── save results CSV ─────────────────────────────────────────────────
    res_oracle["exog_mode"] = "oracle"
    res_const["exog_mode"]  = "constant"
    combined = pd.concat([res_oracle, res_const], ignore_index=True)
    combined.to_csv("cps_validation_results.csv", index=False)
    print("\n✓ Saved cps_validation_results.csv")

    # ── plot ──────────────────────────────────────────────────────────────
    plot_validation(res_oracle, df, metrics_oracle, metrics_const)
