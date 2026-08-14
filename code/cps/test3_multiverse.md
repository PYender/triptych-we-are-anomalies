# `test3_multiverse.py` — kod do niezależnej oceny (Etap B, po rozstrzygnięciach)

Wersja bliźniacza skryptu Testu 3 (rodzina 4). Ten plik nie jest wykonywany.

**Realizuje:** `TEST3_PROTOCOL.md` v1.0 (D-008) · **Status:** Etap B — do przeglądu, **NIEURUCHOMIONY**.
**Zależności:** numpy, pandas, matplotlib + import `test1_band_power` i `test0c_build_canonical`.
**Bieg:** ~10 min przy B = 2000 (Etap C; kontrola pc_1950 wycofana → −96 kombinacji).

## Konstrukcja
Siatka główna **192** = 2 poziomy × 4 wagi × 2 normalizacje (raw, pc_full) × 2 wygładzania
× 2 detrendingi × 3 okresy. Dwie wielkości: **M1** (udział mocy w paśmie T±4) i **M2**
(kontrast epok χ²). Null AR(3), rząd z góry, B = 2000, ziarno 20260812. Funkcje statystyczne
importowane z `test1_band_power.py`; serie z `test0c_build_canonical.py` (v2.1).

## Sześć punktów z §B2 — jak są rozwiązane
1. **Detrending raz, na całej serii** (D-004) — `prepare()` detrenduje pełny szereg;
   `stat_M2` tnie epoki z już zdetrendowanej serii.
2. **Ten sam filtr na surogatach** — null na `base=detrend(x)` bez MA; surogat `prepare(y,ma,det)`.
3. **Pasmo zależy od T** — `band=(T−4, T+4)`.
4. **Normalizacja przed filtrami** — normalizacja jest w serii z buildera.
5. **Ziarno raz na bieg** — jeden `rng`, losowania sekwencyjne.
6. **M2 wymaga obu epok** — `NaN` dla pustej epoki.

## Rozstrzygnięcia autora naniesione
- **Wsparcie H1 = KONIUNKCJA** M1 p<0,05 ∧ M2>0 (H1 z D-002 to dwa warunki). Reguła §6
  orzeka na `frac_H1`. Raportowane cztery odsetki (M1; M2>0; koniunkcja; najostrzejszy
  M1∧M2p<0,05∧M2>0). Uwaga: samo M2>0 ≈ 50% (rzut monetą) — sens tylko w koniunkcji.
- **Specyfikacja oryginalna** (§5.1): poziom P, wagi inherited, MA(11), raw, brak detrendingu,
  T=35,1. Uzasadnienie: 35,1 z dopasowania sinusoidy do wars_smooth bez detrendingu i bez
  per capita (mw-8 w v0.1); detrending pojawiał się dopiero w periodogramie.
- **Kontrola pc_1950 widmowa WYCOFANA.** Przy n=58 pasmo 32–40 jest węższe niż komórka
  rozdzielcza (~0,38), więc M1 mierzyłoby artefakt siatki częstotliwości; M2 i tak
  niedefiniowane. Zastąpiona przez `interpolation_control`: (A) pc_full vs pc_1950 na
  1950–2007 — identyczne z konstrukcji; (B) artefakt interpolacji dekadowej zmierzony na
  prawdzie 1950–2007 (decymacja → re-interpolacja → różnica). Ponieważ normalizacja jest
  punktowa, względna deformacja per capita = względna deformacja mianownika. M1/M2 na
  pc_1950 nie liczone.

## Punkt do odnotowania w raporcie Etapu C
Interakcja skali w `pc_full × MA(11)`: sztuczna ~10-letnia gładkość mianownika i okno
MA(11) leżą blisko — do opisania jako obciążenie (nie błąd potoku, B2.4 zachowany).

## Kod

```python
#!/usr/bin/env python3
"""
TEST 3 — analiza wielowariantowa decyzji przetwarzania (rodzina 4).
Realizuje TEST3_PROTOCOL.md v1.0 (zamrożony 12.08.2026). D-008.

NIE testuje hipotezy — mierzy, ile z wniosków (H1) jest własnością danych, a ile
wyborów przetwarzania. Metoda: multiverse (Steegen i in. 2016) + specification curve
(Simonsohn i in. 2020).

Siatka główna: 2 poziomy × 4 wagi × 2 normalizacje (raw, pc_full) × 2 wygładzania
× 2 detrendingi × 3 okresy = 192 kombinacje. Kontrola pc_1950 liczona osobno.

Wykorzystuje funkcje z test1_band_power.py (psd, band_share, fold_chi2, fit_ar_yw,
sim_ar, linear_detrend, prepare) — były weryfikowane, nie przepisujemy ich. Serie
budowane funkcjami z test0c_build_canonical.py (build_cow, apply_normalization).

Sześć punktów, na których ten test się psuje (TASK_3 §B2) — jak są rozwiązane:
  1. Detrending RAZ, na całej serii (D-004): prepare() detrenduje pełny szereg;
     W2 tnie epoki z JUŻ zdetrendowanej serii, nie detrenduje epok osobno.
  2. Ten sam filtr na surogatach: null fitowany na base=detrend(serii) BEZ MA;
     surogat dostaje prepare(y, ma, det) — czyli to samo MA co obserwacja (Slutsky-Yule).
  3. Pasmo zależy od T: band=(T-4, T+4) — dla T=32 → 28-36, T=40 → 36-44. Nie na sztywno.
  4. Normalizacja PRZED wygładzaniem/detrendingiem: normalizacja jest w serii z buildera
     (apply_normalization), więc prepare() (MA→detrend) działa już na serii per capita.
  5. Ziarno RAZ na cały bieg: jeden rng dla wszystkich 192+ kombinacji, losowania
     sekwencyjne — kombinacje NIE dzielą tych samych surogatów.
  6. W2 wymaga obu epok: kombinacje pc_1950 (od 1950) mają epokę 1 pustą → M2 = NaN
     (jawny brak), nie zero.

NIE uruchamiać przed przeglądem (TASK_3 §B3). Bieg to Etap C.

Wyjście: test3_results.csv, test3_curve.pdf, test3_diagnostics.pdf
"""
from __future__ import annotations
import argparse, hashlib, json, itertools
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import test1_band_power as t1                 # psd, band_share, fold_chi2, fit_ar_yw, sim_ar, prepare, linear_detrend
import test0c_build_canonical as bld          # build_cow, apply_normalization, WEIGHT_SETS

VERSION = "test3_multiverse.py v1.0 (Etap B — do przeglądu)"

# --- siatka zamrożona w D-008 / protokole; NIE zmieniać bez nowego protokołu -----
SEED = 20260812
B = 2000
AR_ORDER = 3                    # null AR(3), rząd ustalony z góry (Test 1 §6)
LEVELS = ("W", "P")
WEIGHTS = ("inherited", "equal", "steep", "flat")
NORMS_GRID = ("raw", "pc_full")            # pc_1950 poza siatką (kontrola)
SMOOTHINGS = (False, True)                 # brak · centrowana MA(11)
DETRENDINGS = (False, True)                # brak · liniowy na całej serii
PERIODS = (32.0, 35.1, 40.0)
EPOCH_SPLIT = 1914             # epoka 2: rok >= 1914; epoka 1: 1816..1913
EPOCH1 = (1816, 1913)
DIMS = ["level", "weights", "norm", "smooth", "detrend", "period"]
# odniesienia narracyjne (§5.1). Oryginalna: T=35,1 pochodzi z dopasowania sinusoidy
# do wars_smooth BEZ detrendingu i BEZ per capita (mw-8 w kodzie v0.1); detrending
# pojawiał się dopiero w periodogramie, czyli w innej procedurze.
SPEC_ORIGINAL = dict(level="P", weights="inherited", norm="raw",
                     smooth=True, detrend=False, period=35.1)   # jak opublikowano
SPEC_PRIMARY = dict(level="W", weights="equal", norm="raw",
                    smooth=False, detrend=True, period=35.1)    # D-001 + D-008 + D-004
# --------------------------------------------------------------------------------


# ============================ budowa serii (cache) ============================
def build_series_cache(dd: Path) -> dict:
    """(level, weights, norm) → pd.Series(value). COW liczone raz na (level, weights);
    normalizacja (raw, pc_full) nakładana na gotową serię. pc_1950 NIE liczone jako
    wariant siatki — kontrola interpolacji jest osobna (patrz interpolation_control)."""
    cache = {}
    for level in LEVELS:
        for wk in WEIGHTS:
            weights = None if wk == "inherited" else bld.WEIGHT_SETS[wk]
            cow = bld.build_cow(dd, level, weights)                 # surowa seria ważona
            for nz in NORMS_GRID:                                   # raw, pc_full
                cache[(level, wk, nz)] = bld.apply_normalization(cow, nz, dd)
    return cache


# ============================ statystyki wyjściowe ============================
def stat_M1(proc: np.ndarray, T: float) -> float:
    """M1 — udział mocy w paśmie T±4 lata (band zależy od T, B2.3)."""
    return t1.band_share(proc, (T - 4.0, T + 4.0))


def stat_M2(proc: np.ndarray, ep1: np.ndarray, ep2: np.ndarray, T: float) -> float:
    """M2 — kontrast epok χ²(1914-koniec) − χ²(1816-1913) na JUŻ przetworzonej serii.
    Detrending był raz na całej serii (B2.1); tu tylko tniemy epoki. Jeśli któraś
    epoka pusta (pc_1950) → NaN (B2.6)."""
    if ep1.sum() == 0 or ep2.sum() == 0:
        return np.nan
    return float(t1.fold_chi2(proc[ep2], T) - t1.fold_chi2(proc[ep1], T))


def run_combo(series: pd.Series, ma: bool, det: bool, T: float, rng) -> dict:
    x = series.to_numpy(float)
    years = series.index.to_numpy()
    ep2 = years >= EPOCH_SPLIT
    ep1 = (years >= EPOCH1[0]) & (years <= EPOCH1[1])

    obs = t1.prepare(x, ma, det)                       # MA→detrend (B2.4: seria już znorm.)
    m1_obs = stat_M1(obs, T)
    m2_obs = stat_M2(obs, ep1, ep2, T)

    base = t1.linear_detrend(x) if det else x.copy()   # null bez MA (B2.2), detrend jeśli det
    a, resid = t1.fit_ar_yw(base, AR_ORDER)

    m1_sur = np.empty(B)
    m2_sur = np.full(B, np.nan)
    for b in range(B):
        y = t1.sim_ar(a, resid, len(x), rng)           # ziarno wspólne, sekwencyjnie (B2.5)
        yp = t1.prepare(y, ma, det)                    # ten sam filtr na surogacie (B2.2)
        m1_sur[b] = stat_M1(yp, T)
        m2_sur[b] = stat_M2(yp, ep1, ep2, T)

    p1 = (1 + int(np.sum(m1_sur >= m1_obs))) / (B + 1)
    if np.isnan(m2_obs):
        p2 = np.nan
    else:
        p2 = (1 + int(np.sum(m2_sur >= m2_obs))) / (B + 1)
    return {"M1": round(m1_obs, 6), "p_M1": round(p1, 4),
            "M2": (np.nan if np.isnan(m2_obs) else round(m2_obs, 4)),
            "p_M2": (np.nan if np.isnan(p2) else round(p2, 4))}


def main_grid_specs():
    for level, wk, nz, ma, det, T in itertools.product(
            LEVELS, WEIGHTS, NORMS_GRID, SMOOTHINGS, DETRENDINGS, PERIODS):
        yield dict(level=level, weights=wk, norm=nz, smooth=ma, detrend=det, period=T)


def evaluate(specs, cache, rng) -> pd.DataFrame:
    rows = []
    for s in specs:
        series = cache[(s["level"], s["weights"], s["norm"])]
        r = run_combo(series, s["smooth"], s["detrend"], s["period"], rng)
        rows.append({**s, "n": int(series.notna().sum()), **r})
    return pd.DataFrame(rows)


# ============================ analiza rozkładu ============================
def variance_shares(df: pd.DataFrame, outcome: str) -> pd.DataFrame:
    """Rozbicie wariancji dla zbalansowanej pełnej siatki (ortogonalne SS): efekty
    główne + interakcje pierwszego rzędu, jako udział sumy kwadratów (§5.3 — NIE test
    istotności). Reszta = rzędy wyższe."""
    d = df.dropna(subset=[outcome]).reset_index(drop=True)
    y = d[outcome].to_numpy(float)
    grand = y.mean()
    ss_tot = float(np.sum((y - grand) ** 2))
    if ss_tot == 0:
        return pd.DataFrame(columns=["skladnik", "udzial_SS"])
    rows = []
    # efekty główne (SS = Σ n_l (mean_l − grand)²; ortogonalne dla siatki zbalansowanej)
    main = {}
    for f in DIMS:
        ss = 0.0
        for pos in d.groupby(f).indices.values():      # .indices → pozycje w y
            g = y[pos]
            ss += len(g) * (g.mean() - grand) ** 2
        main[f] = ss
        rows.append({"skladnik": f, "udzial_SS": ss / ss_tot})
    # interakcje pierwszego rzędu: SS_cell − SS_main1 − SS_main2
    for f1, f2 in itertools.combinations(DIMS, 2):
        ss = 0.0
        for pos in d.groupby([f1, f2]).indices.values():
            g = y[pos]
            ss += len(g) * (g.mean() - grand) ** 2
        ss_inter = ss - main[f1] - main[f2]
        rows.append({"skladnik": f"{f1}×{f2}", "udzial_SS": ss_inter / ss_tot})
    out = pd.DataFrame(rows).sort_values("udzial_SS", ascending=False).reset_index(drop=True)
    return out


def support_fractions(df: pd.DataFrame) -> dict:
    """§5.2 — cztery odsetki, żeby było widać, który składnik H1 zawodzi. H1 (D-002)
    to KONIUNKCJA: moc w paśmie ORAZ kontrast w kierunku przewidywanym. Reguła §6
    orzeka na `frac_H1` = M1 p<0,05 ∧ M2>0. Żaden z tych odsetków NIE jest wartością p
    (kombinacje dzielą dane, §7.3).
    Uwaga: samo M2>0 przy braku efektu wypada ~50% przypadków (rzut monetą) — nie jest
    kryterium, ma sens wyłącznie w koniunkcji."""
    m1 = df.p_M1 < 0.05
    m2pos = df.M2 > 0
    m2sig = df.p_M2 < 0.05
    return {"n": len(df),
            "frac_M1_p05": float(m1.mean()),                       # moc w paśmie obecna
            "frac_M2_pos": float(m2pos.mean()),                    # kontrast w kierunku H1 (~rzut monetą)
            "frac_H1": float((m1 & m2pos).mean()),                 # H1 jak sformułowana — ORZEKA §6
            "frac_H1_sharp": float((m1 & m2sig & m2pos).mean())}   # odczyt najostrzejszy


def interpretation(frac: float) -> str:
    """Reguła §6, zadeklarowana przed uruchomieniem. Stosowana do frac_H1 (koniunkcja)."""
    if frac < 0.05:
        return ("<5%: hipoteza nie broni się w przestrzeni specyfikacji; "
                "pojedyncze wyniki wspierające to oczekiwana liczba z 192 porównań")
    if frac <= 0.25:
        return ("5–25%: hipoteza broni się w wąskim podzbiorze specyfikacji, "
                "wymagającym niezależnego uzasadnienia — samo jego istnienie nie jest dowodem")
    return (">25%: negatywny wynik Testu 1 był specyficzny dla przyjętej tam "
            "specyfikacji i wymaga ponownego rozważenia")


def interpolation_control(dd: Path):
    """Zastępuje widmową kontrolę pc_1950. Powód (§C, decyzja autora): przy n=58
    pasmo 32–40 lat jest węższe niż komórka rozdzielcza (Δf≈0,0172; ~0,38 komórki),
    więc M1 tam nie jest estymowalne — mierzyłoby położenie prążka względem granic
    pasma, nie dane. M2 i tak niedefiniowane (brak epoki 1). Zamiast liczyć widmo na
    pc_1950, pytamy wprost: czy interpolacja deformuje wynik.

    (A) pc_full vs pc_1950 na 1950–2007: identyczne z konstrukcji (normalizacja jest
        punktowa, a po 1950 ludność jest mierzona rocznie), więc korelacja = 1 i różnica
        = 0 — potwierdzenie, że pc_1950 to dokładnie ogon pc_full.
    (B) Artefakt interpolacji dekadowej, zmierzony tam, gdzie mamy prawdę (1950–2007,
        dane roczne): decymujemy ludność do węzłów dekadowych, re-interpolujemy liniowo
        i porównujemy z prawdą. Ponieważ normalizacja jest punktowa, WZGLĘDNA deformacja
        serii per capita RÓWNA SIĘ względnej deformacji mianownika — więc ta liczba
        ogranicza, o ile interpolacja mogłaby zniekształcić per capita przed 1950."""
    df = pd.read_csv(bld.find_input(dd, "population.csv"))
    w = df[df["Entity"] == "World"].set_index("Year")["Population (historical)"].sort_index()
    yy = np.arange(1950, 2008)
    true = w.reindex(yy).astype(float)                      # prawda: roczna, mierzona
    knots = [y for y in range(1950, 2008, 10)] + [2007]     # węzły dekadowe (jak przed 1940)
    reinterp = true.where(true.index.isin(knots)).interpolate(method="linear")
    rel = ((reinterp - true).abs() / true)
    interp_years = [y for y in yy if y not in knots]
    # (A) identyczność pc_full vs pc_1950 na wspólnym oknie (jeden reprezentatywny wariant)
    cow = bld.build_cow(dd, "W", None)
    pcf = bld.apply_normalization(cow, "pc_full", dd).loc[1950:2007]
    pc50 = bld.apply_normalization(cow, "pc_1950", dd)
    ident_maxreldiff = float((pcf - pc50).abs().div(pc50).max())
    return {
        "A_pc_full_vs_pc1950_corr": float(np.corrcoef(pcf, pc50)[0, 1]),
        "A_pc_full_vs_pc1950_maxreldiff": ident_maxreldiff,     # ~0 z konstrukcji
        "B_pop_reinterp_corr": float(np.corrcoef(true, reinterp)[0, 1]),
        "B_maxreldiff_all_pct": float(rel.max() * 100),
        "B_maxreldiff_interp_years_pct": float(rel.loc[interp_years].max() * 100),
        "B_maxreldiff_knot_years_pct": float(rel.loc[knots].max() * 100),  # ~0 (węzły zachowane)
        "_curve": (yy, (rel.to_numpy() * 100)),
    }


# ============================ wykresy ============================
def _spec_index(df, spec):
    m = np.ones(len(df), bool)
    for k, v in spec.items():
        m &= (df[k] == v)
    return np.where(m.to_numpy())[0]


def specification_curve(df: pd.DataFrame, outcome: str, out: Path):
    """§5.4 — główny produkt: wyniki uporządkowane rosnąco + macierz decyzji pod spodem."""
    d = df.dropna(subset=[outcome]).reset_index(drop=True)
    order = d[outcome].sort_values().index.to_numpy()
    vals = d[outcome].to_numpy()[order]
    with PdfPages(out) as pdf:
        fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(13, 9),
                                       gridspec_kw={"height_ratios": [2, 3]}, sharex=True)
        ax0.plot(range(len(vals)), vals, lw=1)
        if outcome == "M1":
            ax0.axhline(0, lw=.5, c="k")
        ax0.set_title(f"Wykres specyfikacji — {outcome} uporządkowane rosnąco (192 kombinacje)")
        ax0.set_ylabel(outcome); ax0.grid(alpha=.3)
        # macierz decyzji: wiersz na każdą wartość każdego wymiaru
        rows, ylabels = [], []
        for f in DIMS:
            for lev in sorted(d[f].unique(), key=str):
                rows.append((d[f].to_numpy()[order] == lev).astype(float))
                ylabels.append(f"{f}={lev}")
        M = np.array(rows)
        ax1.imshow(M, aspect="auto", cmap="Greys", interpolation="none")
        ax1.set_yticks(range(len(ylabels))); ax1.set_yticks(range(len(ylabels)))
        ax1.set_yticklabels(ylabels, fontsize=6)
        ax1.set_xlabel("kombinacja (posortowana wg wyniku)")
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)


def diagnostics(df: pd.DataFrame, interp_ctrl: dict, vshare_m1, vshare_m2, out: Path):
    """§5.1 rozkłady, §5.3 rozbicie wariancji, kontrola interpolacji (nie pc_1950 widmowe)."""
    with PdfPages(out) as pdf:
        for outcome in ("M1", "M2"):
            fig, ax = plt.subplots(figsize=(11, 4))
            v = df[outcome].dropna()
            ax.hist(v, bins=40, color="steelblue", alpha=.75)
            for spec, c, lab in ((SPEC_ORIGINAL, "crimson", "oryginalna"),
                                 (SPEC_PRIMARY, "darkgreen", "pierwszorzędna")):
                idx = _spec_index(df, spec)
                if len(idx):
                    ax.axvline(df[outcome].to_numpy()[idx[0]], c=c, lw=2, label=lab)
            ax.set_title(f"Rozkład {outcome} po 192 kombinacjach")
            ax.legend(); ax.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        for name, vs in (("M1", vshare_m1), ("M2", vshare_m2)):
            fig, ax = plt.subplots(figsize=(11, 5))
            top = vs.head(12)[::-1]
            ax.barh(top.skladnik, top.udzial_SS, color="slategray")
            ax.set_title(f"Rozbicie wariancji {name} — udział sumy kwadratów (nie test istotności)")
            ax.set_xlabel("udział SS"); ax.grid(alpha=.3, axis="x")
            fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        # kontrola interpolacji: artefakt decymacji dekadowej na prawdzie 1950–2007
        yy, relpct = interp_ctrl["_curve"]
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(yy, relpct, lw=1)
        ax.set_title("Kontrola interpolacji: |re-interpolacja dekadowa − prawda| / prawda, "
                     f"1950–2007 (maks {interp_ctrl['B_maxreldiff_all_pct']:.2f}%)")
        ax.set_xlabel("rok"); ax.set_ylabel("różnica względna [%]")
        ax.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    dd, od = Path(a.data_dir), Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)

    cache = build_series_cache(dd)
    rng = np.random.default_rng(SEED)                  # jedno ziarno na cały bieg (B2.5)

    grid = evaluate(main_grid_specs(), cache, rng)     # 192
    interp = interpolation_control(dd)                 # kontrola interpolacji (nie widmowa pc_1950)

    vshare_m1 = variance_shares(grid, "M1")
    vshare_m2 = variance_shares(grid, "M2")
    frac = support_fractions(grid)

    meta = {"script": VERSION, "seed": SEED, "B": B, "null": f"AR({AR_ORDER})",
            "n_main": len(grid),
            "sha256_builder": hashlib.sha256(Path("test0c_build_canonical.py").read_bytes()).hexdigest()[:16],
            "interp_control": {k: v for k, v in interp.items() if not k.startswith("_")}}
    with open(od / "test3_results.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps({**meta, "support": frac,
                                    "interpretation_H1": interpretation(frac["frac_H1"])},
                                   ensure_ascii=False) + "\n")
        grid.to_csv(fh, index=False)

    specification_curve(grid, "M1", od / "test3_curve.pdf")
    diagnostics(grid, interp, vshare_m1, vshare_m2, od / "test3_diagnostics.pdf")

    print(f"Siatka główna: {len(grid)} kombinacji (kontrola pc_1950 widmowa wycofana).")
    print(f"Wsparcie H1 (koniunkcja M1 p<0,05 ∧ M2>0): {frac['frac_H1']*100:.1f}% "
          f"[składniki: M1 p<0,05 {frac['frac_M1_p05']*100:.1f}%, M2>0 {frac['frac_M2_pos']*100:.1f}%, "
          f"najostrzejszy {frac['frac_H1_sharp']*100:.1f}%].")
    print("Reguła §6 (na koniunkcji):", interpretation(frac["frac_H1"]))
    print(f"Kontrola interpolacji: artefakt dekadowy maks {interp['B_maxreldiff_all_pct']:.2f}% "
          f"(lata interpolowane {interp['B_maxreldiff_interp_years_pct']:.2f}%).")
    print("\nNajwiększy udział w wariancji M1:")
    print(vshare_m1.head(5).to_string(index=False))
    print("\nUWAGA: odsetek wspierających NIE jest wartością p (kombinacje dzielą dane).")


if __name__ == "__main__":
    main()
```
