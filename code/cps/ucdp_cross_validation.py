# ucdp_cross_validation.py — Replikacja krzyżowa COW × UCDP
#
# Pytanie walidacyjne:
#   Czy dwie niezależne bazy danych (COW i UCDP) — kodowane przez różne
#   zespoły, z różnymi definicjami konfliktu i różnymi źródłami — zgadzają
#   się co do KSZTAŁTU, FAZY i PRZYBLIŻONEGO OKRESU cyklu wojennego
#   w oknie nakładania 1946–2007?
#
# Jeśli tak  → cykl nie jest artefaktem metodologii jednej bazy.
# Jeśli nie  → cykl jest co najmniej częściowo artefaktem kodowania.
#
# Trzy niezależne serie UCDP (różne miary konfliktu):
#   A: ważona liczba konfliktów   (typy 2/3/4, wagi 1.0/0.4/0.7)
#   B: log1p(ofiary w bitwach)    (typy 2+3+4, bd_best)
#   C: log1p(ofiary w bitwach)    (typy 2+4 interstate, bd_best)
#
# Kryteria walidacji (każde 0/1):
#   1–3. Korelacja Pearsona r ≥ 0.70 w oknie 1946–2007 (osobno A, B, C)
#   4–6. |T_dom_COW − T_dom_UCDP| ≤ 8 lat               (osobno A, B, C)
#
# Źródło: Triptych "We are Anomal(i)es" v0.1, Mariusz Włodarczyk
# Licencja: CC BY-NC-SA 4.0

from __future__ import annotations

import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from scipy import signal
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

warnings.filterwarnings("ignore")

# ── Ścieżki i stałe ───────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent
COW_PATH  = BASE_DIR / "wars_color.csv"
PRIO_PATH = BASE_DIR / "data/ucdp/UcdpPrioConflict_v25_1.csv"
BD_PATH   = BASE_DIR / "data/ucdp/BattleDeaths_v25_1.csv"

SMOOTH_WIN    = 11
OVERLAP_START = 1946
OVERLAP_END   = 2007
CYCLE_BAND    = (30, 45)   # lata — spodziewany przedział cyklu

UCDP_WEIGHTS  = {2: 1.0, 3: 0.4, 4: 0.7}


# ══════════════════════════════════════════════════════════════════════════════
# 1. Ładowanie danych
# ══════════════════════════════════════════════════════════════════════════════

def load_cow(path: Path = COW_PATH) -> pd.Series:
    """wars_smooth (MA11) z wars_color.csv, indeks = rok."""
    df = pd.read_csv(path).set_index("year").sort_index()
    return df["wars_smooth"].astype(float)


def load_ucdp_count(path: Path = PRIO_PATH) -> pd.Series:
    """
    Seria A: ważona liczba konfliktów UCDP (typy 2/3/4).
    Jedna obserwacja to conflict_id × rok w UcdpPrioConflict.
    """
    raw = pd.read_csv(path, low_memory=False)
    keep = list(UCDP_WEIGHTS.keys())
    sub = raw[raw["type_of_conflict"].isin(keep)].copy()
    sub["weight"] = sub["type_of_conflict"].map(UCDP_WEIGHTS)
    yearly = sub.groupby("year")["weight"].sum().rename("A_raw").astype(float)
    return yearly


def load_ucdp_deaths(path: Path = BD_PATH) -> pd.DataFrame:
    """
    Seria B: log1p(bd_best) — wszystkie typy 2+3+4.
    Seria C: log1p(bd_best) — interstate (typy 2+4), najbliższe COW.
    """
    raw = pd.read_csv(path, low_memory=False)
    raw["bd_best"] = pd.to_numeric(raw["bd_best"], errors="coerce").fillna(0)

    bd_B = (raw[raw["type_of_conflict"].isin([2, 3, 4])]
            .groupby("year")["bd_best"].sum()
            .rename("B_raw").astype(float))

    bd_C = (raw[raw["type_of_conflict"].isin([2, 4])]
            .groupby("year")["bd_best"].sum()
            .rename("C_raw").astype(float))

    return pd.DataFrame({"B_raw": bd_B, "C_raw": bd_C})


# ══════════════════════════════════════════════════════════════════════════════
# 2. Przetwarzanie sygnału
# ══════════════════════════════════════════════════════════════════════════════

def smooth_ma(series: pd.Series, window: int = SMOOTH_WIN) -> pd.Series:
    return series.rolling(window, center=True, min_periods=1).mean()


def zscore_in_window(series: pd.Series,
                     start: int = OVERLAP_START,
                     end: int = OVERLAP_END) -> pd.Series:
    """Normalizacja z-score na podstawie statystyk z okna nakładania."""
    ref = series.loc[start:end]
    mu, sigma = ref.mean(), ref.std()
    if sigma < 1e-12:
        return series * 0.0
    return (series - mu) / sigma


def dominant_period_welch(series: pd.Series,
                           band: tuple = CYCLE_BAND) -> tuple[float, np.ndarray, np.ndarray]:
    """
    Dominant T (lat) w zadanym paśmie (lat) metodą Welcha.
    Zwraca: (T_dom, freqs, psd).
    Seria jest liniowo odtrendowana przed obliczeniem widma.
    """
    x = series.dropna().values
    n = len(x)
    if n < 16:
        return np.nan, np.array([0.0]), np.array([0.0])

    # odtrendowanie liniowe
    t = np.arange(n)
    x = x - np.polyval(np.polyfit(t, x, 1), t)

    nperseg = min(n, max(16, n // 2))
    freqs, psd = signal.welch(
        x, fs=1.0, window="hann", nperseg=nperseg,
        noverlap=nperseg // 2, scaling="density"
    )

    lo_f = 1.0 / band[1]
    hi_f = 1.0 / band[0]
    mask = (freqs > lo_f) & (freqs <= hi_f)
    if mask.sum() == 0:
        return np.nan, freqs, psd

    peak_f = freqs[mask][np.argmax(psd[mask])]
    return (1.0 / peak_f if peak_f > 0 else np.nan), freqs, psd


def fit_sine(series: pd.Series, T: float) -> dict:
    """
    Dopasowanie: y = A·sin(2π·t/T + φ) + B·t + C
    Zwraca słownik z φ w stopniach, R² i flagą sukcesu.
    """
    s = series.dropna()
    t_arr = s.index.values.astype(float)
    y_arr = s.values
    omega = 2.0 * np.pi / T

    def model(t, A, phi, B, C):
        return A * np.sin(omega * t + phi) + B * t + C

    A0 = (y_arr.max() - y_arr.min()) / 2.0

    try:
        popt, _ = curve_fit(
            model, t_arr, y_arr,
            p0=[A0, 0.0, 0.0, y_arr.mean()],
            maxfev=20_000,
            bounds=([-np.inf, -2*np.pi, -np.inf, -np.inf],
                    [ np.inf,  2*np.pi,  np.inf,  np.inf])
        )
        y_pred = model(t_arr, *popt)
        ss_res = np.sum((y_arr - y_pred) ** 2)
        ss_tot = np.sum((y_arr - y_arr.mean()) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
        phi_deg = float(np.degrees(popt[1])) % 360.0
        return {"A": popt[0], "phi_deg": phi_deg, "B": popt[2],
                "C": popt[3], "r2": r2, "success": True}
    except Exception as exc:
        return {"A": np.nan, "phi_deg": np.nan, "B": np.nan,
                "C": np.nan, "r2": np.nan, "success": False, "error": str(exc)}


def phase_diff_deg(phi1: float, phi2: float) -> float:
    """Najkrótsza różnica kątowa ∈ [0, 180]°."""
    d = abs(phi1 - phi2) % 360.0
    return min(d, 360.0 - d)


# ══════════════════════════════════════════════════════════════════════════════
# 3. Wizualizacja
# ══════════════════════════════════════════════════════════════════════════════

C_COW = "#1f77b4"   # niebieski
C_A   = "#d62728"   # czerwony
C_B   = "#2ca02c"   # zielony
C_C   = "#ff7f0e"   # pomarańczowy


def plot_cross_validation(
    cow_smooth:   pd.Series,
    ucdp_A_sm:    pd.Series,
    ucdp_B_sm:    pd.Series,
    ucdp_C_sm:    pd.Series,
    cow_norm:     pd.Series,
    ucdp_A_norm:  pd.Series,
    ucdp_B_norm:  pd.Series,
    ucdp_C_norm:  pd.Series,
    f_cow: np.ndarray, psd_cow: np.ndarray,
    f_A:   np.ndarray, psd_A:   np.ndarray,
    f_B:   np.ndarray, psd_B:   np.ndarray,
    f_C:   np.ndarray, psd_C:   np.ndarray,
    corr_A: float, p_val_A: float,
    corr_B: float, p_val_B: float,
    corr_C: float, p_val_C: float,
    T_cow: float, T_A: float, T_B: float, T_C: float,
    sine_cow: dict, sine_A: dict, sine_B: dict, sine_C: dict,
    out_path: str = "ucdp_cross_validation.pdf",
) -> None:

    fig = plt.figure(figsize=(16, 14))
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.54, wspace=0.38)

    # ── Panel 1: Pełny zakres ─────────────────────────────────────────────────
    ax1   = fig.add_subplot(gs[0, :])
    ax1r  = ax1.twinx()

    ax1.plot(cow_smooth.index, cow_smooth.values,
             color=C_COW, lw=2.4, label="COW wars_smooth (1816–2007)")
    ax1r.plot(ucdp_A_norm.loc[OVERLAP_START:].index,
              ucdp_A_norm.loc[OVERLAP_START:].values,
              color=C_A, lw=1.7, ls="--", label="UCDP-A: liczba konfliktów (z-score)")
    ax1r.plot(ucdp_B_norm.loc[OVERLAP_START:].index,
              ucdp_B_norm.loc[OVERLAP_START:].values,
              color=C_B, lw=1.2, ls=":", alpha=0.85, label="UCDP-B: log ofiary wsz. (z-score)")
    ax1r.plot(ucdp_C_norm.loc[OVERLAP_START:].index,
              ucdp_C_norm.loc[OVERLAP_START:].values,
              color=C_C, lw=1.2, ls="-.", alpha=0.85, label="UCDP-C: log ofiary inter. (z-score)")

    ax1.axvspan(OVERLAP_START, OVERLAP_END, alpha=0.09, color="grey",
                label=f"Okno nakładania {OVERLAP_START}–{OVERLAP_END}")
    ax1.set_xlim(1816, 2026)
    ax1.set_ylabel("COW wars_smooth", color=C_COW, fontsize=9)
    ax1r.set_ylabel("UCDP (z-score w oknie 1946–2007)", color=C_A, fontsize=9)
    ax1.tick_params(axis="y", labelcolor=C_COW)
    ax1r.tick_params(axis="y", labelcolor=C_A)
    ax1.set_title(
        "(1) Pełny zakres — COW (1816–2007) i UCDP (1946–2024)\n"
        "Serie UCDP znormalizowane z-score w oknie nakładania (szary pasek)",
        fontsize=10
    )
    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax1r.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, fontsize=7.5, loc="upper left", ncol=2)

    # ── Panel 2: Okno nakładania ──────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])
    ov  = slice(OVERLAP_START, OVERLAP_END)

    ax2.plot(cow_norm.loc[ov].index,    cow_norm.loc[ov],
             color=C_COW, lw=2.5, label="COW (z-score)")
    ax2.plot(ucdp_A_norm.loc[ov].index, ucdp_A_norm.loc[ov],
             color=C_A, lw=1.8, ls="--",
             label=f"UCDP-A  r={corr_A:.3f} (p={p_val_A:.3f})")
    ax2.plot(ucdp_B_norm.loc[ov].index, ucdp_B_norm.loc[ov],
             color=C_B, lw=1.4, ls=":", alpha=0.9,
             label=f"UCDP-B  r={corr_B:.3f} (p={p_val_B:.3f})")
    ax2.plot(ucdp_C_norm.loc[ov].index, ucdp_C_norm.loc[ov],
             color=C_C, lw=1.4, ls="-.", alpha=0.9,
             label=f"UCDP-C  r={corr_C:.3f} (p={p_val_C:.3f})")

    ax2.axhline(0, color="grey", lw=0.8, ls=":")
    ax2.set_title(
        f"(2) Okno nakładania {OVERLAP_START}–{OVERLAP_END}  (n=62)\n"
        "Korelacja Pearsona z-score — kryterium r ≥ 0.70",
        fontsize=10
    )
    ax2.set_xlabel("Rok")
    ax2.set_ylabel("z-score")
    ax2.legend(fontsize=7.5, loc="upper right")

    # ── Panel 3: Welch PSD ─────────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])

    def _plot_psd(ax, freqs, psd, color, label, lw=2.0, ls="-"):
        mask = (freqs > 0) & (1.0 / freqs >= 5) & (1.0 / freqs <= 100)
        if mask.sum() == 0:
            return
        periods = 1.0 / freqs[mask]
        ax.plot(periods, psd[mask], color=color, lw=lw, ls=ls, label=label)

    _plot_psd(ax3, f_cow, psd_cow, C_COW,
              f"COW  (T_dom={T_cow:.0f} lat)")
    _plot_psd(ax3, f_A, psd_A, C_A,
              f"UCDP-A  (T_dom={T_A:.0f} lat)", ls="--")
    _plot_psd(ax3, f_B, psd_B, C_B,
              f"UCDP-B  (T_dom={T_B:.0f} lat)", lw=1.3, ls=":")
    _plot_psd(ax3, f_C, psd_C, C_C,
              f"UCDP-C  (T_dom={T_C:.0f} lat)", lw=1.3, ls="-.")

    ax3.axvspan(CYCLE_BAND[0], CYCLE_BAND[1], alpha=0.13, color="purple",
                label=f"Pasmo {CYCLE_BAND[0]}–{CYCLE_BAND[1]} lat")
    ax3.set_xlabel("Okres (lata)")
    ax3.set_ylabel("PSD (Welch)")
    ax3.set_title(
        "(3) Welch PSD — dominujące okresy\n"
        "(odtrendowanie liniowe; kryterium |ΔT| ≤ 8 lat)",
        fontsize=10
    )
    ax3.legend(fontsize=8)
    ax3.set_xlim(5, 80)

    # ── Panel 4: Tabela podsumowująca ─────────────────────────────────────────
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis("off")

    def _v_r(r: float) -> str:
        if r >= 0.70: return f"✓ {r:.3f}"
        if r >= 0.50: return f"~ {r:.3f}"
        return f"✗ {r:.3f}"

    def _v_T(t1: float, t2: float, tol: float = 8.0) -> str:
        if np.isnan(t1) or np.isnan(t2):
            return "b.d."
        diff = abs(t1 - t2)
        if diff <= tol: return f"✓ |ΔT|={diff:.0f}yr"
        return f"✗ |ΔT|={diff:.0f}yr"

    def _v_phi(phi1: float, phi2: float, tol: float = 45.0) -> str:
        if np.isnan(phi1) or np.isnan(phi2):
            return "b.d."
        diff = phase_diff_deg(phi1, phi2)
        if diff <= tol: return f"✓ |Δφ|={diff:.0f}°"
        return f"✗ |Δφ|={diff:.0f}°"

    headers = ["Miara", "COW\n(1816–2007)", "UCDP-A\nważona\nliczba",
               "UCDP-B\nlog ofiary\nwsz.", "UCDP-C\nlog ofiary\ninter."]

    rows = [
        ["Zakres danych", "1816–2007", "1946–2024", "1946–2024", "1946–2024"],
        ["Kryterium 1–3\nKorelacja z COW\n(1946–2007)",
         "—",
         _v_r(corr_A), _v_r(corr_B), _v_r(corr_C)],
        ["Kryterium 4–6\nT_dom w paśmie\n30–45 lat",
         f"{T_cow:.0f} lat",
         _v_T(T_cow, T_A), _v_T(T_cow, T_B), _v_T(T_cow, T_C)],
        ["Faza φ (sinusoid.)\nw oknie 1946–2007",
         f"{sine_cow['phi_deg']:.0f}°\n(R²={sine_cow['r2']:.2f})",
         _v_phi(sine_cow["phi_deg"], sine_A["phi_deg"]),
         _v_phi(sine_cow["phi_deg"], sine_B["phi_deg"]),
         _v_phi(sine_cow["phi_deg"], sine_C["phi_deg"])],
    ]

    tbl = ax4.table(
        cellText=rows, colLabels=headers,
        loc="center", cellLoc="center"
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1.15, 2.6)

    # styl nagłówka
    for j in range(5):
        cell = tbl[0, j]
        cell.set_facecolor("#2c3e50")
        cell.set_text_props(color="white", fontweight="bold")

    # kolorowanie komórek wyników
    color_map = {"✓": "#a8e6a3", "~": "#f5e6a3", "✗": "#f5a3a3"}
    for i_r in range(1, len(rows) + 1):
        for j_c in range(1, 5):
            txt = tbl[i_r, j_c].get_text().get_text()
            for sym, clr in color_map.items():
                if txt.startswith(sym):
                    tbl[i_r, j_c].set_facecolor(clr)
                    break

    ax4.set_title(
        "(4) Tabela podsumowująca kryteria walidacji krzyżowej\n"
        "✓ zielony: kryterium spełnione  |  ~ żółty: częściowo  |  ✗ czerwony: niespełnione",
        fontsize=10, pad=14
    )

    plt.suptitle(
        "Replikacja krzyżowa COW × UCDP\n"
        f"Czy niezależne bazy danych potwierdzają ten sam cykl wojenny? "
        f"(pasmo {CYCLE_BAND[0]}–{CYCLE_BAND[1]} lat, okno {OVERLAP_START}–{OVERLAP_END})",
        fontsize=12, y=1.01
    )
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"✓ Saved {out_path}")
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 4. Main
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import os
    os.chdir(BASE_DIR)

    SEP  = "═" * 68
    sep2 = "─" * 68

    print(SEP)
    print("  REPLIKACJA KRZYŻOWA COW × UCDP v25.1")
    print("  Test: czy dwie niezależne bazy potwierdzają ten sam cykl?")
    print(SEP)

    # ── Ładowanie ─────────────────────────────────────────────────────────────
    cow_sm = load_cow()
    ucdp_A_raw = load_ucdp_count()
    ucdp_BD    = load_ucdp_deaths()

    print(f"\n  COW:    {cow_sm.index[0]}–{cow_sm.index[-1]}  (n={len(cow_sm)})")
    print(f"  UCDP-A: {ucdp_A_raw.index[0]}–{ucdp_A_raw.index[-1]}  (n={len(ucdp_A_raw)})")
    print(f"  UCDP-BD:{ucdp_BD.index[0]}–{ucdp_BD.index[-1]}")

    # ── Pełne zakresy lat (reindeksowanie) ───────────────────────────────────
    yr_min = min(cow_sm.index.min(), ucdp_A_raw.index.min())
    yr_max = max(cow_sm.index.max(), ucdp_A_raw.index.max())
    all_yr = pd.RangeIndex(yr_min, yr_max + 1)

    A_full = ucdp_A_raw.reindex(all_yr, fill_value=0.0)
    B_full = ucdp_BD["B_raw"].reindex(all_yr, fill_value=0.0)
    C_full = ucdp_BD["C_raw"].reindex(all_yr, fill_value=0.0)

    # ── Wygładzanie ───────────────────────────────────────────────────────────
    ucdp_A_sm = smooth_ma(A_full)
    ucdp_B_sm = smooth_ma(np.log1p(B_full))
    ucdp_C_sm = smooth_ma(np.log1p(C_full))

    # ── Normalizacja z-score w oknie 1946–2007 ────────────────────────────────
    cow_norm    = zscore_in_window(cow_sm)
    ucdp_A_norm = zscore_in_window(ucdp_A_sm)
    ucdp_B_norm = zscore_in_window(ucdp_B_sm)
    ucdp_C_norm = zscore_in_window(ucdp_C_sm)

    # ── Korelacje Pearsona w oknie nakładania ─────────────────────────────────
    ov = slice(OVERLAP_START, OVERLAP_END)

    cow_ov = cow_norm.loc[ov].dropna()

    def _corr(ucdp_norm_series):
        u = ucdp_norm_series.loc[ov].reindex(cow_ov.index).dropna()
        c = cow_ov.reindex(u.index)
        return pearsonr(c, u)

    corr_A, pv_A = _corr(ucdp_A_norm)
    corr_B, pv_B = _corr(ucdp_B_norm)
    corr_C, pv_C = _corr(ucdp_C_norm)

    # ── Dominujące okresy (Welch PSD) ─────────────────────────────────────────
    # COW: pełna seria 1816–2007 (maksymalna rozdzielczość spektralna)
    T_cow, f_cow, psd_cow = dominant_period_welch(cow_sm)
    # UCDP: od 1946 do końca dostępnych danych
    T_A, f_A, psd_A = dominant_period_welch(ucdp_A_sm.loc[OVERLAP_START:])
    T_B, f_B, psd_B = dominant_period_welch(ucdp_B_sm.loc[OVERLAP_START:])
    T_C, f_C, psd_C = dominant_period_welch(ucdp_C_sm.loc[OVERLAP_START:])

    # ── Fazy sinusoidalne (dopasowanie w oknie 1946–2007) ─────────────────────
    # Używamy T_cow dla COW i T własnego dla każdej serii UCDP
    T_cow_fit = T_cow if not np.isnan(T_cow) else 36.0
    T_A_fit   = T_A   if not np.isnan(T_A)   else 36.0
    T_B_fit   = T_B   if not np.isnan(T_B)   else 36.0
    T_C_fit   = T_C   if not np.isnan(T_C)   else 36.0

    sine_cow = fit_sine(cow_norm.loc[ov],    T_cow_fit)
    sine_A   = fit_sine(ucdp_A_norm.loc[ov], T_A_fit)
    sine_B   = fit_sine(ucdp_B_norm.loc[ov], T_B_fit)
    sine_C   = fit_sine(ucdp_C_norm.loc[ov], T_C_fit)

    # ══════════════════════════════════════════════════════════════════════════
    # Wydruk wyników
    # ══════════════════════════════════════════════════════════════════════════

    def _vr(r, p):
        mark = "✓" if r >= 0.70 else ("~" if r >= 0.50 else "✗")
        return f"{mark}  r = {r:.4f}  p = {p:.4f}"

    def _vT(t1, t2, tol=8.0):
        if np.isnan(t1) or np.isnan(t2):
            return "b.d."
        diff = abs(t1 - t2)
        mark = "✓" if diff <= tol else "✗"
        return f"{mark}  |ΔT| = {diff:.1f} lat"

    def _vphi(phi1, phi2, tol=45.0):
        if np.isnan(phi1) or np.isnan(phi2):
            return "b.d."
        diff = phase_diff_deg(phi1, phi2)
        mark = "✓" if diff <= tol else "✗"
        return f"{mark}  |Δφ| = {diff:.1f}°"

    print(f"\n{sep2}")
    print("KRYTERIUM 1–3: KORELACJA PEARSONA  (okno 1946–2007, z-score, n≈62)")
    print(f"{sep2}")
    print(f"  COW vs. UCDP-A (ważona liczba konf.):  {_vr(corr_A, pv_A)}")
    print(f"  COW vs. UCDP-B (log ofiary wsz.):      {_vr(corr_B, pv_B)}")
    print(f"  COW vs. UCDP-C (log ofiary interstate):{_vr(corr_C, pv_C)}")
    print(f"  Próg walidacji: r ≥ 0.70")

    print(f"\n{sep2}")
    print(f"KRYTERIUM 4–6: DOMINUJĄCE OKRESY WELCH PSD  (pasmo {CYCLE_BAND[0]}–{CYCLE_BAND[1]} lat)")
    print(f"{sep2}")
    print(f"  COW  (1816–2007, pełna seria):  T_dom = {T_cow:.1f} lat")
    print(f"  UCDP-A (1946–2024):             T_dom = {T_A:.1f} lat  →  {_vT(T_cow, T_A)}")
    print(f"  UCDP-B (1946–2024):             T_dom = {T_B:.1f} lat  →  {_vT(T_cow, T_B)}")
    print(f"  UCDP-C (1946–2024):             T_dom = {T_C:.1f} lat  →  {_vT(T_cow, T_C)}")
    print(f"  Próg walidacji: |ΔT| ≤ 8 lat")

    print(f"\n{sep2}")
    print("INFORMACYJNIE: FAZY SINUSOIDALNE  (dopasowanie w oknie 1946–2007)")
    print(f"{sep2}")
    print(f"  COW:    φ = {sine_cow['phi_deg']:.1f}°  R² = {sine_cow['r2']:.3f}"
          f"  (T_fit={T_cow_fit:.0f} lat)")
    print(f"  UCDP-A: φ = {sine_A['phi_deg']:.1f}°  R² = {sine_A['r2']:.3f}"
          f"  (T_fit={T_A_fit:.0f} lat)  →  {_vphi(sine_cow['phi_deg'], sine_A['phi_deg'])}")
    print(f"  UCDP-B: φ = {sine_B['phi_deg']:.1f}°  R² = {sine_B['r2']:.3f}"
          f"  (T_fit={T_B_fit:.0f} lat)  →  {_vphi(sine_cow['phi_deg'], sine_B['phi_deg'])}")
    print(f"  UCDP-C: φ = {sine_C['phi_deg']:.1f}°  R² = {sine_C['r2']:.3f}"
          f"  (T_fit={T_C_fit:.0f} lat)  →  {_vphi(sine_cow['phi_deg'], sine_C['phi_deg'])}")
    print(f"  (fazy informacyjne — dopasowanie sinusoidy do n=62 przy T≈36 lat jest niestabilne)")

    # Zliczanie spełnionych kryteriów 1–6
    crit_met = [
        corr_A >= 0.70,
        corr_B >= 0.70,
        corr_C >= 0.70,
        (not np.isnan(T_A)) and abs(T_cow - T_A) <= 8.0,
        (not np.isnan(T_B)) and abs(T_cow - T_B) <= 8.0,
        (not np.isnan(T_C)) and abs(T_cow - T_C) <= 8.0,
    ]
    n_met = sum(crit_met)

    print(f"\n{SEP}")
    print("WNIOSEK WALIDACYJNY")
    print(SEP)
    print(f"  Liczba spełnionych kryteriów (1–6): {n_met}/6")
    if n_met >= 5:
        print("  WYNIK ✓✓: Wysokie potwierdzenie — COW i UCDP są wzajemnie spójne.")
        print("            Cykl nie jest artefaktem kodowania jednej bazy danych.")
    elif n_met >= 3:
        print("  WYNIK  ~: Częściowa zgodność — ostrożna interpretacja.")
        print("            Przynajmniej część cyklu pojawia się w obu bazach.")
    else:
        print("  WYNIK ✗✗: Brak zgodności — dane COW i UCDP nie potwierdzają")
        print("            tego samego cyklu w oknie nakładania.")
    print(SEP)

    # ── Zapis CSV ─────────────────────────────────────────────────────────────
    summary = pd.DataFrame([
        {"seria": "COW",
         "zakres": "1816–2007",
         "T_dom_lat": round(T_cow, 2),
         "phi_deg": round(sine_cow["phi_deg"], 2),
         "sine_r2": round(sine_cow["r2"], 4),
         "corr_z_COW_1946_2007": 1.0,
         "p_corr": 0.0,
         "kryterium_r_ge_070": True,
         "kryterium_T_le_8lat": True},
        {"seria": "UCDP-A",
         "zakres": "1946–2024",
         "T_dom_lat": round(T_A, 2),
         "phi_deg": round(sine_A["phi_deg"], 2),
         "sine_r2": round(sine_A["r2"], 4),
         "corr_z_COW_1946_2007": round(corr_A, 4),
         "p_corr": round(pv_A, 4),
         "kryterium_r_ge_070": corr_A >= 0.70,
         "kryterium_T_le_8lat": (not np.isnan(T_A)) and abs(T_cow - T_A) <= 8.0},
        {"seria": "UCDP-B",
         "zakres": "1946–2024",
         "T_dom_lat": round(T_B, 2),
         "phi_deg": round(sine_B["phi_deg"], 2),
         "sine_r2": round(sine_B["r2"], 4),
         "corr_z_COW_1946_2007": round(corr_B, 4),
         "p_corr": round(pv_B, 4),
         "kryterium_r_ge_070": corr_B >= 0.70,
         "kryterium_T_le_8lat": (not np.isnan(T_B)) and abs(T_cow - T_B) <= 8.0},
        {"seria": "UCDP-C",
         "zakres": "1946–2024",
         "T_dom_lat": round(T_C, 2),
         "phi_deg": round(sine_C["phi_deg"], 2),
         "sine_r2": round(sine_C["r2"], 4),
         "corr_z_COW_1946_2007": round(corr_C, 4),
         "p_corr": round(pv_C, 4),
         "kryterium_r_ge_070": corr_C >= 0.70,
         "kryterium_T_le_8lat": (not np.isnan(T_C)) and abs(T_cow - T_C) <= 8.0},
    ]).set_index("seria")

    out_csv = BASE_DIR / "ucdp_cross_validation_summary.csv"
    summary.to_csv(out_csv)
    print(f"\n✓ Saved {out_csv.name}")

    # ── Wykres ────────────────────────────────────────────────────────────────
    plot_cross_validation(
        cow_sm, ucdp_A_sm, ucdp_B_sm, ucdp_C_sm,
        cow_norm, ucdp_A_norm, ucdp_B_norm, ucdp_C_norm,
        f_cow, psd_cow,
        f_A, psd_A,
        f_B, psd_B,
        f_C, psd_C,
        corr_A, pv_A,
        corr_B, pv_B,
        corr_C, pv_C,
        T_cow, T_A, T_B, T_C,
        sine_cow, sine_A, sine_B, sine_C,
        out_path=str(BASE_DIR / "ucdp_cross_validation.pdf"),
    )
