#!/usr/bin/env python3
"""
TEST 5 — skan po okresach ze statystyką maksymalną (rodzina 1 rozszerzona).
Realizuje TEST5_PROTOCOL.md v1.0 (zamrożony 15.08.2026). D-011, D-004, D-001.

Pyta o CAŁY zakres 8–60 lat naraz, nie o jeden okres. Korekta na wielokrotne
testowanie jest wbudowana: rozkład zerowy to rozkład MAKSIMÓW statystyki po skanie
(problem Daviesa 1977/1987). Nie zakłada okresu 18 lat ani żadnego innego.

Wykorzystuje gotowe funkcje: psd, band_share, fit_ar_yw, sim_ar, linear_detrend, prepare,
moving_average z test1_band_power.py oraz fold_chi2_years z test4_robustness.py. Nie
przepisuje ich. Test 5 czyta gotowy cps_canonical_v2.csv.

Sześć punktów, na których ten test się psuje (TASK_5 §A2):
  1. Rozkład zerowy = rozkład MAKSIMÓW. Każdy surogat przechodzi pełny skan po 105
     punktach → jego Wmax; p = (1 + #{Wmax_sur ≥ Wmax_obs}) / (B+1). Porównanie Wmax
     danych z rozkładem W(T*) przy jednym T unieważnia test.
  2. Pasmo W1 przesuwa się z T (T±4); mianownik (4–100 lat) STAŁY dla wszystkich T.
  3. Detrending RAZ, na całym oknie analizowanym, przed skanem — dla danych i każdego
     surogatu osobno. Nie detrendować przy każdym T.
  4. JEDEN zestaw surogatów na konfigurację (seria, okno, filtr); wszystkie 105 punktów
     skanu jednego surogatu z tej samej realizacji.
  5. Targmax surogatów zbierany i raportowany (histogram, kontrola jednorodności).
  6. S5 (MA(11)): filtr nakładany również na każdy surogat, przed skanem.

NIE uruchamiać przed przeglądem (TASK_5 §A5). Bieg to Etap B.

Wyjście: test5_results.csv, test5_scan.csv, test5_scan.pdf
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import test1_band_power as t1        # psd, band_share, fit_ar_yw, sim_ar, linear_detrend, prepare
import test4_robustness as t4        # fold_chi2_years

VERSION = "test5_periodscan.py v1.0 (Etap A — do przeglądu)"

# --- parametry zamrożone w protokole; NIE zmieniać bez nowego protokołu ----------
SCAN = np.arange(8.0, 60.0 + 1e-9, 0.5)      # T ∈ [8,60], krok 0,5 → 105 punktów (§3)
REF_BAND = (4.0, 100.0)                       # mianownik W1, STAŁY (§4)
BAND_HALFWIDTH = 4.0                          # pasmo W1 = T ± 4 lata
NBINS = 10                                    # kosze fazowe W2
SEED = 20260815
B = 2000
AR_ORDER = 3
# --------------------------------------------------------------------------------
assert len(SCAN) == 105, f"siatka skanu ma {len(SCAN)} punktów, powinna 105"


# ============================ statystyki po skanie ============================
def w1_from_spectrum(f: np.ndarray, p: np.ndarray, T: float) -> float:
    """W1(T) = moc w paśmie T±4 / moc w paśmie 4–100 (mianownik stały, A2.2).
    Czyta z GOTOWEGO widma — widmo nie zależy od T, tylko granice sumowania (A4)."""
    lo, hi = T - BAND_HALFWIDTH, T + BAND_HALFWIDTH
    num = (f >= 1.0 / hi) & (f <= 1.0 / lo)
    den = (f >= 1.0 / REF_BAND[1]) & (f <= 1.0 / REF_BAND[0])
    return float(p[num].sum() / p[den].sum())


def scan_W1(vals: np.ndarray) -> np.ndarray:
    """Pełny skan W1 po 105 punktach. psd liczone RAZ (A4)."""
    f, p = t1.psd(vals)
    return np.array([w1_from_spectrum(f, p, T) for T in SCAN])


def scan_W2(vals: np.ndarray, years: np.ndarray, phase0: int) -> np.ndarray:
    """Pełny skan W2 (χ² epoch-folding, faza z numeru roku). Faza zależy od T —
    optymalizacja jak dla W1 niemożliwa (A4)."""
    return np.array([t4.fold_chi2_years(vals, years, T, phase0, NBINS) for T in SCAN])


def maxstat(curve: np.ndarray) -> tuple[float, float]:
    i = int(np.argmax(curve))
    return float(curve[i]), float(SCAN[i])


# ============================ silnik: jedna konfiguracja ============================
def run_config(vals_raw: np.ndarray, years: np.ndarray, phase0: int, ma: bool,
               stats: tuple, rng) -> dict:
    """Jeden zestaw B surogatów AR(3) na konfigurację (A2.4). Zwraca dla każdej
    statystyki: krzywą danych, Wmax/Targmax danych, rozkład maksimów surogatów,
    Targmax surogatów, p oraz per-T 95. percentyl surogatów (do wykresu)."""
    # obserwacja: detrending raz na oknie (A2.3); dla S5 dodatkowo MA(11) (A2.6)
    obs = t1.prepare(vals_raw, ma, True)                      # MA?(11) → detrend
    base = t1.linear_detrend(vals_raw)                        # baza AR: detrend. (stacjonarna)
    a, resid = t1.fit_ar_yw(base, AR_ORDER)

    out = {}
    obs_curves = {s: (scan_W1(obs) if s == "W1" else scan_W2(obs, years, phase0)) for s in stats}
    sur_curves = {s: np.empty((B, len(SCAN))) for s in stats}
    for b in range(B):
        y = t1.sim_ar(a, resid, len(vals_raw), rng)          # jedna realizacja → cały skan (A2.4)
        yp = t1.prepare(y, ma, True)                         # ten sam filtr na surogacie (A2.6)
        for s in stats:
            sur_curves[s][b] = scan_W1(yp) if s == "W1" else scan_W2(yp, years, phase0)

    for s in stats:
        wmax_obs, targ_obs = maxstat(obs_curves[s])
        sur_max = sur_curves[s].max(axis=1)                  # Wmax każdego surogatu (A2.1)
        sur_targ = SCAN[sur_curves[s].argmax(axis=1)]        # Targmax surogatów (A2.5)
        p = (1 + int(np.sum(sur_max >= wmax_obs))) / (B + 1)
        out[s] = {"obs_curve": obs_curves[s], "Wmax": round(wmax_obs, 6),
                  "Targmax": round(targ_obs, 1),
                  "null_max_p95": round(float(np.percentile(sur_max, 95)), 6),
                  "p": round(p, 4), "sur_targmax": sur_targ,
                  "sur_p95_curve": np.percentile(sur_curves[s], 95, axis=0)}
    return out


# ============================ lista uruchomień ============================
def load(data: Path, variant: str, y0: int, y1: int):
    df = pd.read_csv(data, comment="#")
    s = df[df.variant == variant].set_index("year")["value"].sort_index().loc[y0:y1]
    return s.index.to_numpy(), s.to_numpy(float)


# Uruchomienia grupowane po KONFIGURACJI (seria, okno, filtr): jeden zestaw surogatów
# na konfigurację (A2.4), więc P1(W1) i P2(W2) dzielą te same realizacje A_COW_W —
# obie statystyki liczone na wspólnym zestawie surogatów (zatwierdzone). Kolejność
# konfiguracji przesądza, które realizacje trafiają gdzie (jeden strumień rng), dlatego
# jest zapisywana w nagłówku CSV (run_order) — inaczej ten sam seed po zmianie kolejności
# dałby inne liczby.
CONFIGS = [   # seria, y0, y1, ma, [(statystyka, id, rola), ...]
    ("A_COW_W", 1816, 2007, False, [("W1", "P1", "PIERWSZORZĘDNY — ORZEKA"),
                                    ("W2", "P2", "współpierwszorzędny")]),
    ("A_COW_P", 1816, 2007, False, [("W1", "S1", "H2"), ("W2", "S1", "H2")]),
    ("A_COW_W", 1914, 2007, False, [("W1", "S2", "epoka 2, opisowy"),
                                    ("W2", "S2", "epoka 2, opisowy")]),
    ("A_COW_P", 1914, 2007, False, [("W1", "S3", "epoka 2, H2, opisowy"),
                                    ("W2", "S3", "epoka 2, H2, opisowy")]),
    ("B_UCDP",  1946, 2024, False, [("W1", "S4", "replikacja niezależna"),
                                    ("W2", "S4", "replikacja niezależna")]),
    ("A_COW_W", 1816, 2007, True,  [("W1", "S5", "ile skan przesuwa MA(11)")]),
]


def verdict(rid, stat, p):
    if rid == "P1" and stat == "W1":
        return f"ORZEKA — p<0,05 {'SPEŁNIONE' if p < 0.05 else 'NIESPEŁNIONE'} (warunkowo od P2 i rozkładu Targmax)"
    if rid == "P2" and stat == "W2":
        return f"POTWIERDZA — p<0,10 {'SPEŁNIONE' if p < 0.10 else 'NIESPEŁNIONE'}"
    return "opisowy — nie orzeka"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="cps_canonical_v2.csv")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)                        # jedno ziarno na cały bieg

    res_rows, scan_rows, plot, run_order = [], [], {}, []
    for var, y0, y1, ma, items in CONFIGS:
        stats = tuple(dict.fromkeys(s for s, _, _ in items))   # unikalne statystyki, kolejność zachowana
        years, vals = load(Path(a.data), var, y0, y1)
        r = run_config(vals, years, y0, ma, stats, rng)        # jeden zestaw surogatów na konfigurację
        run_order.append(f"{var}:{y0}-{y1}:{'MA11' if ma else 'surowa'}({','.join(stats)})")
        for s, rid, rola in items:
            d = r[s]
            res_rows.append({"id": rid, "seria": var, "okno": f"{y0}-{y1}",
                             "filtr": "MA11" if ma else "surowa", "statystyka": s,
                             "n": len(vals), "Wmax": d["Wmax"], "Targmax": d["Targmax"],
                             "null_max_p95": d["null_max_p95"], "p": d["p"],
                             "decyzja": verdict(rid, s, d["p"])})
            for T, wobs, wp95 in zip(SCAN, d["obs_curve"], d["sur_p95_curve"]):
                scan_rows.append({"id": rid, "seria": var, "statystyka": s,
                                  "T": round(float(T), 1), "W_obs": round(float(wobs), 6),
                                  "W_sur_p95": round(float(wp95), 6)})
            plot[(rid, s)] = d
        print(f"{var} {y0}-{y1} {'MA11' if ma else 'surowa':7s} | " +
              " · ".join(f"{rid}/{s}: Wmax={r[s]['Wmax']:.4g} @T={r[s]['Targmax']} p={r[s]['p']:.4f}"
                         for s, rid, _ in items))

    res = pd.DataFrame(res_rows)
    meta = {"script": VERSION, "seed": SEED, "B": B, "null": f"AR({AR_ORDER})",
            "scan": f"[{SCAN[0]:.0f},{SCAN[-1]:.0f}] krok 0,5 ({len(SCAN)} pkt)",
            "run_order": run_order,      # kolejność losowania (jeden strumień rng) — dla odtwarzalności
            "note_P1P2": "P1(W1) i P2(W2) na wspólnych realizacjach surogatów A_COW_W — skorelowane, nie dwa niezależne potwierdzenia",
            "sha256_data": hashlib.sha256(Path(a.data).read_bytes()).hexdigest()[:16]}
    with open(out / "test5_results.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n"); res.to_csv(fh, index=False)
    pd.DataFrame(scan_rows).to_csv(out / "test5_scan.csv", index=False)
    figures(plot, out / "test5_scan.pdf")

    p1 = res[(res.id == "P1") & (res.statystyka == "W1")].p.iloc[0]
    p2 = res[(res.id == "P2") & (res.statystyka == "W2")].p.iloc[0]
    print(f"\nREGUŁA §7: P1(W1) p={p1:.4f} (<0,05) · P2(W2) p={p2:.4f} (<0,10) "
          f"· + kontrola jednorodności Targmax surogatów (patrz histogram).")
    print("WYNIK: " + ("POZYTYWNY (warunkowo od kontroli Targmax)" if (p1 < 0.05 and p2 < 0.10)
                       else "NEGATYWNY / NIEJEDNOZNACZNY — twierdzenie o okresowości niewsparte"))
    print("Orzeka wyłącznie P1. Okres wskazany przez skan to KANDYDAT, wymaga danych niezależnych (§9.2).")


# ================================== wykresy ==================================
def figures(plot: dict, outfile: Path):
    with PdfPages(outfile) as pdf:
        # Panel 1: W1(T) dla P1 z pasmem 95. percentyla surogatów
        d = plot[("P1", "W1")]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(SCAN, d["obs_curve"], lw=1.6, color="#1f5fa8", label="A_COW_W 1816–2007 (dane)")
        ax.plot(SCAN, d["sur_p95_curve"], lw=1, ls="--", color="#888", label="95. percentyl surogatów (per T)")
        ti = d["Targmax"]; ax.axvline(ti, ls=":", c="crimson", label=f"Targmax danych = {ti} lat")
        ax.set_xlabel("T [lata]"); ax.set_ylabel("W1 (udział mocy w paśmie T±4)")
        ax.set_title(f"Panel 1. P1 — skan mocy w paśmie; Wmax p={d['p']:.4f} (rozkład maksimów)")
        ax.legend(fontsize=8); ax.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        # Panel 2: W2(T) dla P2
        d2 = plot[("P2", "W2")]
        fig, ax = plt.subplots(figsize=(11, 4.5))
        ax.plot(SCAN, d2["obs_curve"], lw=1.6, color="#2e8b57", label="χ² epoch-folding (dane)")
        ax.plot(SCAN, d2["sur_p95_curve"], lw=1, ls="--", color="#888", label="95. percentyl surogatów")
        ax.axvline(d2["Targmax"], ls=":", c="crimson", label=f"Targmax = {d2['Targmax']} lat")
        ax.set_xlabel("T [lata]"); ax.set_ylabel("W2 (χ²)")
        ax.set_title(f"Panel 2. P2 — skan χ²; Wmax p={d2['p']:.4f}")
        ax.legend(fontsize=8); ax.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        # Panel 3: histogram Targmax surogatów (P1) z pozycją danych (A2.5)
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.hist(d["sur_targmax"], bins=SCAN[::2], color="steelblue", alpha=.75)
        ax.axvline(d["Targmax"], c="crimson", lw=2, label=f"Targmax danych = {d['Targmax']} lat")
        ax.set_xlabel("Targmax [lata]"); ax.set_ylabel("liczba surogatów")
        ax.set_title("Panel 3. Rozkład Targmax surogatów (kontrola jednorodności, §5/§7)")
        ax.legend(); ax.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        # Panel 4: porównanie serii/okien (W1)
        fig, ax = plt.subplots(figsize=(11, 4.5))
        for rid, s in [("P1", "W1"), ("S1", "W1"), ("S2", "W1"), ("S4", "W1")]:
            if (rid, s) in plot:
                ax.plot(SCAN, plot[(rid, s)]["obs_curve"], lw=1.2, label=rid)
        ax.set_xlabel("T [lata]"); ax.set_ylabel("W1")
        ax.set_title("Panel 4. Porównanie serii i okien (W1)")
        ax.legend(fontsize=8); ax.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)


if __name__ == "__main__":
    main()
