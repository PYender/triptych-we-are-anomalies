#!/usr/bin/env python3
"""
TEST 1 — czy okres 32–40 lat jest własnością danych.
Realizuje TEST1_PROTOCOL.md v1.0. Rodzina 1 (zarzuty Z3, Z4, Z14).

Bez zależności od statsmodels — AR estymowany metodą Yule'a–Walkera na numpy/scipy,
żeby wynik nie zależał od zawartości środowiska.

Uruchomienie:
    python test1_band_power.py --data cps_canonical_v2.csv --out-dir out/ -B 2000

Wyjście: test1_results.csv, test1_diagnostics.pdf
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.linalg import solve_toeplitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

VERSION = "test1_band_power.py v1.0"

# --- parametry zamrożone w protokole; NIE zmieniać bez nowego protokołu -------
BAND = (32.0, 40.0)          # pasmo badane [lata]
BAND_ALT = (30.0, 42.0)      # wariant S1e
REF_BAND = (4.0, 100.0)      # mianownik udziału mocy
PAD = 4                      # uzupełnienie zerami (zagęszcza próbkowanie, nie rozdzielczość)
T_HYP = 35.1                 # okres hipotetyczny dla epoch-folding
NBINS = 10                   # kosze fazowe
SCAN = np.arange(28.0, 48.0 + 1e-9, 0.5)
MA_WIN = 11
BLOCK_MEAN = 10              # średnia długość bloku, bootstrap stacjonarny
AR_BURN = 200
SEED = 20260810
# -----------------------------------------------------------------------------


# ============================ przetwarzanie serii ============================
def linear_detrend(x: np.ndarray) -> np.ndarray:
    t = np.arange(len(x), dtype=float)
    return x - np.polyval(np.polyfit(t, x, 1), t)


def moving_average(x: np.ndarray, win: int) -> np.ndarray:
    """Centrowana średnia ruchoma z min_periods=1 — identyczna z pandas
    rolling(center=True, min_periods=1), używaną przy budowie serii kanonicznej."""
    return pd.Series(x).rolling(win, center=True, min_periods=1).mean().to_numpy()


def prepare(x: np.ndarray, ma: bool, detrend: bool) -> np.ndarray:
    if ma:
        x = moving_average(x, MA_WIN)
    if detrend:
        x = linear_detrend(x)
    return x


# ============================ statystyki testowe =============================
def psd(x: np.ndarray):
    """Periodogram z oknem Hanna i uzupełnieniem zerami ×PAD."""
    n = len(x)
    xw = x * np.hanning(n)
    nfft = PAD * n
    p = np.abs(np.fft.rfft(xw, n=nfft)) ** 2
    f = np.fft.rfftfreq(nfft, d=1.0)
    return f, p


def band_share(x: np.ndarray, band=BAND) -> float:
    """S1 — udział mocy w paśmie okresów `band` w mocy pasma referencyjnego."""
    f, p = psd(x)
    num = (f >= 1.0 / band[1]) & (f <= 1.0 / band[0])
    den = (f >= 1.0 / REF_BAND[1]) & (f <= 1.0 / REF_BAND[0])
    return float(p[num].sum() / p[den].sum())


def fold_chi2(x: np.ndarray, T: float, nbins: int = NBINS) -> float:
    """S2 — epoch folding. Faza liczona od pierwszego roku analizowanego okna."""
    idx = np.arange(len(x), dtype=float)
    b = ((idx % T) / T * nbins).astype(int) % nbins
    g, v = x.mean(), x.var(ddof=1)
    if v == 0:
        return 0.0
    return float(sum(((b == k).sum() * (x[b == k].mean() - g) ** 2) / v
                     for k in range(nbins) if (b == k).sum() > 0))


def scan_max(x: np.ndarray):
    """S3 — skan po T. Zwraca (T_max, chi2_max). Opisowe."""
    vals = np.array([fold_chi2(x, T) for T in SCAN])
    i = int(vals.argmax())
    return float(SCAN[i]), float(vals[i]), vals


# ============================== modele zerowe ================================
def fit_ar_yw(x: np.ndarray, p: int):
    """Yule-Walker. Zwraca (współczynniki, reszty)."""
    x = x - x.mean()
    n = len(x)
    r = np.array([np.dot(x[:n - k], x[k:]) / n for k in range(p + 1)])
    if p == 0:
        return np.zeros(0), x.copy()
    a = solve_toeplitz((r[:p], r[:p]), r[1:p + 1])
    resid = np.array([x[t] - np.dot(a, x[t - p:t][::-1]) for t in range(p, n)])
    return a, resid


def ar_order_aic(x: np.ndarray, pmax: int = 20) -> int:
    """Rząd AR minimalizujący AIC. Używany wyłącznie w wariantach wrażliwości."""
    n = len(x)
    best, best_aic = 1, np.inf
    for p in range(1, pmax + 1):
        _, e = fit_ar_yw(x, p)
        s2 = np.var(e, ddof=0)
        aic = n * np.log(s2) + 2 * p
        if aic < best_aic:
            best, best_aic = p, aic
    return best


def sim_ar(a: np.ndarray, resid: np.ndarray, n: int, rng) -> np.ndarray:
    """Surogat AR(p): rekurencja z resztami losowanymi ze zbioru empirycznego."""
    p = len(a)
    m = n + AR_BURN
    e = rng.choice(resid, size=m, replace=True)
    y = np.zeros(m)
    for t in range(p, m):
        y[t] = (np.dot(a, y[t - p:t][::-1]) + e[t]) if p else e[t]
    return y[AR_BURN:]


def stationary_bootstrap(x: np.ndarray, n: int, rng, mean_block=BLOCK_MEAN) -> np.ndarray:
    """Politis & Romano (1994): bloki o długości geometrycznej, owijanie cykliczne."""
    N = len(x)
    pblk = 1.0 / mean_block
    out = np.empty(n)
    i = rng.integers(N)
    for t in range(n):
        out[t] = x[i % N]
        i = rng.integers(N) if rng.random() < pblk else i + 1
    return out


# ================================ silnik testu ===============================
def run_one(spec: dict, series: dict, rng) -> dict:
    x_raw = series[spec["variant"]].loc[spec["y0"]:spec["y1"]].to_numpy(float)
    n = len(x_raw)
    ma, det = spec["ma"], spec["detrend"]

    base = linear_detrend(x_raw) if det else x_raw.copy()   # seria do estymacji nulla
    obs = prepare(x_raw, ma, det)
    stat = spec["stat"]
    band = spec.get("band", BAND)

    def statistic(v):
        if stat == "S1":
            return band_share(v, band)
        if stat == "S2":
            return fold_chi2(v, T_HYP)
        raise ValueError(stat)

    s_obs = statistic(obs)

    # generator surogatów
    if spec["null"] == "block":
        gen = lambda: stationary_bootstrap(base, n, rng)
        null_desc = f"blok~geom(śr. {BLOCK_MEAN})"
        ar_p = None
    else:
        ar_p = ar_order_aic(base) if spec["null"] == "AR_AIC" else int(spec["null"][2:])
        a, resid = fit_ar_yw(base, ar_p)
        gen = lambda: sim_ar(a, resid, n, rng)
        null_desc = f"AR({ar_p})" + (" [AIC]" if spec["null"] == "AR_AIC" else "")

    B = spec["B"]
    sur = np.empty(B)
    for b in range(B):
        y = gen()
        y = prepare(y, ma, det)          # identyczny filtr na surogacie
        sur[b] = statistic(y)

    p = (1 + int((sur >= s_obs).sum())) / (B + 1)
    return sur, {"id": spec["id"], "wariant": spec["variant"], "okno": f"{spec['y0']}-{spec['y1']}",
            "n": n, "filtr": "MA11" if ma else "surowa", "detrend": det,
            "statystyka": stat, "pasmo": f"{band[0]:.0f}-{band[1]:.0f}" if stat == "S1" else "-",
            "null": null_desc, "ar_p": ar_p, "B": B,
            "S_obs": round(s_obs, 6), "null_p95": round(float(np.percentile(sur, 95)), 6),
            "p": round(p, 4), "rola": spec["rola"], "decyzja": verdict(spec["id"], p)}


def verdict(rid: str, p: float) -> str:
    """Kolumna 'decyzja' wymagana przez §10. Orzeka wyłącznie P1 (§9)."""
    if rid == "P1":
        return f"ORZEKA — próg p<0,05 {'SPEŁNIONY' if p < 0.05 else 'NIESPEŁNIONY'}"
    if rid == "P2":
        return f"POTWIERDZA — próg p<0,10 {'SPEŁNIONY' if p < 0.10 else 'NIESPEŁNIONY'}"
    if rid in ("S1c1", "S1c5"):
        return f"KONTROLA — warunek p≤0,50 {'SPEŁNIONY' if p <= 0.50 else 'NIESPEŁNIONY'}"
    return "opisowy — nie orzeka"


def build_specs(B: int) -> list[dict]:
    """Pre-rejestrowana lista uruchomień z §7 protokołu. Kolejność bez znaczenia,
    zawartość zamrożona."""
    d = dict(ma=False, detrend=True, stat="S1", B=B)
    S = [
        dict(id="P1",  variant="A_COW_W", y0=1816, y1=2007, null="AR3",    rola="PIERWSZORZĘDNY", **d),
        dict(id="P2",  variant="A_COW_W", y0=1816, y1=2007, null="block",  rola="współpierwszorzędny", **d),
        dict(id="S1a", variant="A_COW_W", y0=1816, y1=2007, null="AR3",    rola="pomocniczy",
             **{**d, "ma": True}),
        dict(id="S1b", variant="A_COW_W", y0=1816, y1=2007, null="AR_AIC", rola="wrażliwość: rząd", **d),
        dict(id="S1c1", variant="A_COW_W", y0=1816, y1=2007, null="AR1",   rola="wrażliwość: rząd", **d),
        dict(id="S1c5", variant="A_COW_W", y0=1816, y1=2007, null="AR5",   rola="wrażliwość: rząd", **d),
        dict(id="S1d", variant="A_COW_W", y0=1816, y1=2007, null="AR3",    rola="wrażliwość: detrending",
             **{**d, "detrend": False}),
        dict(id="S1e", variant="A_COW_W", y0=1816, y1=2007, null="AR3",    rola="wrażliwość: pasmo",
             **{**d, "band": BAND_ALT}),
        dict(id="S2a", variant="A_COW_W", y0=1816, y1=2007, null="AR3",    rola="dziedzina fazy",
             **{**d, "stat": "S2"}),
        dict(id="S2b", variant="A_COW_W", y0=1816, y1=2007, null="AR_AIC", rola="porównanie z sesją lutową",
             **{**d, "stat": "S2"}),
        dict(id="E1_S1", variant="A_COW_W", y0=1914, y1=2007, null="AR3",  rola="opis epoki 2", **d),
        dict(id="E1_S2", variant="A_COW_W", y0=1914, y1=2007, null="AR3",  rola="opis epoki 2",
             **{**d, "stat": "S2"}),
        dict(id="E2_S1", variant="A_COW_W", y0=1816, y1=1913, null="AR3",  rola="opis epoki 1", **d),
        dict(id="E2_S2", variant="A_COW_W", y0=1816, y1=1913, null="AR3",  rola="opis epoki 1",
             **{**d, "stat": "S2"}),
        dict(id="R1_S1", variant="A_COW_P", y0=1816, y1=2007, null="AR3",  rola="hipoteza H2", **d),
        dict(id="R1_S2", variant="A_COW_P", y0=1816, y1=2007, null="AR3",  rola="hipoteza H2",
             **{**d, "stat": "S2"}),
        dict(id="R2_S1", variant="B_UCDP",  y0=1946, y1=2024, null="AR3",  rola="replikacja", **d),
        dict(id="R2_S2", variant="B_UCDP",  y0=1946, y1=2024, null="AR3",  rola="replikacja",
             **{**d, "stat": "S2"}),
    ]
    return S


# ================================== wykresy ==================================
def diagnostics(series, nulls: dict, res: pd.DataFrame, scan_vals, out: Path):
    """Cztery panele wymagane przez §10 protokołu."""
    with PdfPages(out) as pdf:
        # --- Panel 1: serie surowe i po detrendingu ---
        fig, ax = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
        for v in ("A_COW_W", "A_COW_P"):
            s = series[v]
            ax[0].plot(s.index, s.values, lw=1, label=v)
            m = (s.index >= 1816) & (s.index <= 2007)
            ax[1].plot(s.index[m], linear_detrend(s[m].to_numpy(float)), lw=1, label=v)
        for a_ in ax:
            a_.axvline(1914, ls="--", c="k", lw=1); a_.legend(); a_.grid(alpha=.3)
        ax[0].set_title("Panel 1a. Serie surowe (pionowa linia: 1914)")
        ax[1].set_title("Panel 1b. Te same serie po detrendingu liniowym (1816–2007)")
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)

        # --- Panel 2: periodogramy z zaznaczonym pasmem ---
        fig, ax = plt.subplots(figsize=(11, 5))
        for v, style in (("A_COW_W", "-"), ("A_COW_P", "--")):
            s = series[v]; m = (s.index >= 1816) & (s.index <= 2007)
            f, pw = psd(linear_detrend(s[m].to_numpy(float)))
            sel = (f > 0) & (f <= 0.25)
            ax.loglog(1 / f[sel], pw[sel], style, lw=1, label=v)
        ax.axvspan(BAND[0], BAND[1], color="crimson", alpha=.15, label="pasmo 32–40 lat")
        ax.set_xlabel("okres [lata]"); ax.set_ylabel("moc")
        ax.set_title("Panel 2. Periodogram (detrend, okno Hanna, uzupełnienie zerami ×4)")
        ax.legend(); ax.grid(alpha=.3, which="both")
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)

        # --- Panel 3: rozkłady zerowe P1 i P2 z wartością obserwowaną ---
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
        for k, rid in enumerate(("P1", "P2")):
            sur = nulls[rid]
            row = res.loc[res.id == rid].iloc[0]
            ax[k].hist(sur, bins=40, color="steelblue", alpha=.75)
            ax[k].axvline(row.S_obs, c="crimson", lw=2,
                          label=f"obserwowane = {row.S_obs:.4f}")
            ax[k].axvline(np.percentile(sur, 95), c="k", ls="--", lw=1,
                          label="95. percentyl nulla")
            ax[k].set_title(f"Panel 3{'ab'[k]}. {rid} — null: {row.null}\np = {row.p:.4f}")
            ax[k].set_xlabel("S1 (udział mocy w paśmie)")
            ax[k].legend(fontsize=8); ax[k].grid(alpha=.3)
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)

        # --- Panel 4: skan S3 (opisowy) ---
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(SCAN, scan_vals, lw=1.5)
        i = int(np.argmax(scan_vals))
        ax.axvline(SCAN[i], ls="--", c="crimson",
                   label=f"maksimum przy T = {SCAN[i]:.1f} lat (opisowo, bez p)")
        ax.axvspan(BAND[0], BAND[1], color="crimson", alpha=.10)
        ax.set_xlabel("T [lata]"); ax.set_ylabel("χ²")
        ax.set_title("Panel 4. Skan epoch-folding po T — statystyka opisowa (§5, S3)")
        ax.legend(); ax.grid(alpha=.3)
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="cps_canonical_v2.csv")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("-B", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args()
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(a.data, comment="#")
    series = {v: g.set_index("year")["value"].sort_index()
              for v, g in df.groupby("variant")}

    rng = np.random.default_rng(a.seed)
    rows, nulls = [], {}
    for spec in build_specs(a.B):
        sur, row = run_one(spec, series, rng)
        rows.append(row); nulls[spec["id"]] = sur
    res = pd.DataFrame(rows)

    x = linear_detrend(series["A_COW_W"].loc[1816:2007].to_numpy(float))
    T_max, chi_max, scan_vals = scan_max(x)

    meta = {"script": VERSION, "seed": a.seed, "B": a.B,
            "sha256_data": hashlib.sha256(Path(a.data).read_bytes()).hexdigest()[:16],
            "scan_T_max_descriptive": T_max}
    with open(out / "test1_results.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        res.to_csv(fh, index=False)
    diagnostics(series, nulls, res, scan_vals, out / "test1_diagnostics.pdf")

    print(res.to_string(index=False))
    p1 = float(res.loc[res.id == "P1", "p"].iloc[0])
    p2 = float(res.loc[res.id == "P2", "p"].iloc[0])
    c1 = float(res.loc[res.id == "S1c1", "p"].iloc[0])
    c5 = float(res.loc[res.id == "S1c5", "p"].iloc[0])
    ok = (p1 < 0.05) and (p2 < 0.10) and (c1 <= 0.50) and (c5 <= 0.50)
    print(f"\nREGUŁA §8: P1={p1:.4f} (<0,05) · P2={p2:.4f} (<0,10) · "
          f"AR1={c1:.4f} AR5={c5:.4f} (żaden >0,50)")
    print("WYNIK: " + ("POZYTYWNY — okres jest własnością danych"
                       if ok else "NEGATYWNY / NIEJEDNOZNACZNY — twierdzenie niewsparte"))
    print(f"Skan (opisowo, bez p): maksimum χ² przy T = {T_max:.1f} lat, χ² = {chi_max:.2f}")
    print(f"\nLiczba uruchomień: {len(res)}. Orzeka wyłącznie P1; P2 potwierdza.")


if __name__ == "__main__":
    main()
