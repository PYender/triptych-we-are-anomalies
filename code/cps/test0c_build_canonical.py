#!/usr/bin/env python3
"""
TEST 0C — budowa serii kanonicznej v2.

Zmiany wobec v1:
  • COW liczony z plików surowych z korektami F1–F3 (patrz TEST0B_REPORT.md),
    a nie przyjmowany jako dany z wars_color.csv;
  • seria COW w DWÓCH poziomach agregacji, rozstrzyganych w rodzinie testów 4:
        W = wojna       (deduplikacja po WarNum — zgodne z opisem w rozdziale)
        P = uczestnik   (zliczanie wierszy — stan faktyczny w v0.1)
  • brak odcięcia na 2003 — po korekcie F1 ogon serii nie jest zdeformowany;
  • skala złączenia COW→UCDP wyznaczana osobno dla każdego poziomu.

Wyjście: cps_canonical_v2.csv, test0c_calibration.csv
Warianty: A_COW_W, A_COW_P, B_UCDP, C_SPLICED_W, C_SPLICED_P
Kolumny wartości: value, value_ma11c (centrowana), value_ma11t (jednostronna)
"""
from __future__ import annotations
import argparse, hashlib, io, json, re
from pathlib import Path

import numpy as np
import pandas as pd

VERSION = "test0c_build_canonical.py v2.1"
YEARS = np.arange(1816, 2008)
SMOOTH = 11
CAL_WINDOWS = [(1946, 2007), (1970, 2007), (1989, 2006), (1989, 2007),
               (1997, 2007), (2000, 2007)]
CAL_PRIMARY = (1989, 2007)
D2_MAX_RATIO, D3_MAX_SD = 1.5, 0.5
UCDP_W = {2: 1.0, 3: 0.4, 4: 0.7}
COW = {  # plik, waga (domyślna = inherited), kolumny faz, rok zamknięcia zbioru
    "inter": ("InterStateWarData_v4_0.csv", 1.0, [("StartYear1", "EndYear1"),
                                                  ("StartYear2", "EndYear2")], 2007),
    "extra": ("ExtraStateWarData_v4_0.csv", 0.7, [("StartYear1", "EndYear1"),
                                                  ("StartYear2", "EndYear2")], 2007),
    "non":   ("NonStateWarData_v4_0.csv",   0.4, [("StartYear", "EndYear")], 2007),
    "intra": ("INTRASTATE_WARS_v5_1_CSV.csv", 0.4,
              [(f"StartYr{k}", f"EndYr{k}") for k in (1, 2, 3, 4)], 2014),
}

# --- Test 3 (rodzina 4): wagi i normalizacja jako parametry multiwersum (D-008) ---
# Domyślne wartości odtwarzają zachowanie v2.0 bit w bit (dowód regresji: §A2 zadania).
# Wagi F1–F3 to poprawki błędów, NIE wymiar multiwersum — obowiązują we wszystkich.
WEIGHT_SETS = {                       # Inter / Extra / Non / Intra
    "inherited": {"inter": 1.0, "extra": 0.7, "non": 0.4,  "intra": 0.4},   # jak opublikowano
    "equal":     {"inter": 1.0, "extra": 1.0, "non": 1.0,  "intra": 1.0},
    "steep":     {"inter": 1.0, "extra": 0.5, "non": 0.25, "intra": 0.25},
    "flat":      {"inter": 1.0, "extra": 0.7, "non": 0.7,  "intra": 0.7},
}
NORMALIZATIONS = ("raw", "pc_full", "pc_1950")
PC_1950_RANGE = (1950, 2007)


def load_cow(path: Path) -> pd.DataFrame:
    with open(path, encoding="latin-1", newline="") as fh:
        raw = fh.read()
    return pd.read_csv(io.StringIO(raw.replace("\r\n", "\n").replace("\r", "\n")))


def find_input(data_dir: Path, wanted: str) -> Path:
    """Znajduje plik wejściowy niezależnie od konwencji nazw i układu katalogów.

    Repozytorium używa nazw oryginalnych COW ('Inter-StateWarData_v4.0.csv',
    'INTRA-STATE WARS v5.1 CSV.csv') rozłożonych po data/cow i data/ucdp;
    kopie robocze bywają płaskie i z podkreśleniami. Porównujemy nazwy po
    normalizacji do samych znaków alfanumerycznych, rekurencyjnie w --data-dir.
    """
    def norm(s: str) -> str:
        s = re.sub(r"[^a-z0-9]", "", s.lower())
        while s.endswith("csv"):          # 'INTRA-STATE WARS v5.1 CSV' == '... v5.1'
            s = s[:-3]
        return s
    target = norm(Path(wanted).stem)
    exact = data_dir / wanted
    if exact.exists():
        return exact
    hits = [p for p in data_dir.rglob("*.csv") if norm(p.stem) == target]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise FileNotFoundError(
            f"nie znaleziono '{wanted}' (ani odpowiednika po normalizacji nazwy) "
            f"w {data_dir} — sprawdź --data-dir")
    raise FileNotFoundError(f"niejednoznaczne dopasowanie '{wanted}': {[str(h) for h in hits]}")

def war_id(df: pd.DataFrame) -> pd.Series:
    col = [c for c in df.columns if c.lower() == "warnum"][0]
    return df[col]


def counts(df, phases, weight, cutoff, level):
    """level='P' → zlicza wiersze; level='W' → unikalne WarNum."""
    phases = [(s, e) for s, e in phases if s in df.columns and e in df.columns]
    num = {c: pd.to_numeric(df[c], errors="coerce") for p in phases for c in p}
    wid = war_id(df)
    out = np.zeros(len(YEARS))
    for i, y in enumerate(YEARS):
        mask = np.zeros(len(df), dtype=bool)
        for s_col, e_col in phases:
            s = num[s_col]
            e = num[e_col].where(num[e_col] != -7, cutoff)   # F1
            mask |= (s.notna() & (s > 0) & e.notna() & (e > 0)
                     & (s <= y) & (e >= y)).values
        n = wid[mask].nunique() if level == "W" else int(mask.sum())
        out[i] = weight * n
    return out


def build_cow(dd: Path, level: str, weights: dict | None = None) -> pd.Series:
    """weights=None → zestaw odziedziczony (wartości z COW) → zachowanie v2.0."""
    tot = np.zeros(len(YEARS))
    for cat, (fname, w_default, ph, cut) in COW.items():
        w = w_default if weights is None else weights[cat]
        tot += counts(load_cow(find_input(dd, fname)), ph, w, cut, level)
    return pd.Series(tot, index=YEARS, name="value")


def world_population(dd: Path) -> pd.Series:
    """Ludność świata (OWID), reindeksowana na 1816–2007 i interpolowana liniowo.
    Dane są dekadowe do 1940 i roczne od 1950 (71 pomiarów). Lata przed pierwszym
    pomiarem (1816–1819, przed 1820) są wypełniane wartością najbliższą (backfill) —
    to jedyna ekstrapolacja; jest zadeklarowana i policzona w raporcie buildera."""
    df = pd.read_csv(find_input(dd, "population.csv"))
    w = df[df["Entity"] == "World"].set_index("Year")["Population (historical)"].sort_index()
    full = w.reindex(range(YEARS.min(), YEARS.max() + 1))
    return full.interpolate(method="linear", limit_direction="both")


def apply_normalization(s: pd.Series, mode: str, dd: Path) -> pd.Series:
    """raw → bez zmian (identyczność, gwarancja regresji). Normalizacja jest
    własnością zmiennej i jest nakładana PRZED wygładzaniem/detrendingiem (frame())."""
    if mode == "raw":
        return s
    pop = world_population(dd)
    if mode == "pc_full":
        return (s / pop.reindex(s.index)).rename("value")
    if mode == "pc_1950":
        a, b = PC_1950_RANGE
        s2 = s.loc[a:b]
        return (s2 / pop.reindex(s2.index)).rename("value")
    raise ValueError(mode)


def build_ucdp(dd: Path) -> pd.Series:
    u = pd.read_csv(find_input(dd, "UcdpPrioConflict_v25_1.csv"))
    g = u[u.type_of_conflict.isin(UCDP_W)].copy()
    g["w"] = g.type_of_conflict.map(UCDP_W)
    return g.groupby("year")["w"].sum().sort_index()


def calibrate(cow: pd.Series, ucdp: pd.Series):
    rows = []
    for y0, y1 in CAL_WINDOWS:
        c, u = cow.loc[y0:y1], ucdp.loc[y0:y1]
        rows.append({"okno": f"{y0}-{y1}", "skala": c.mean() / u.mean(),
                     "corr": float(np.corrcoef(c, u)[0, 1])})
    t = pd.DataFrame(rows)
    ratio = t.skala.max() / t.skala.min()
    scale = float(t.loc[t.okno == f"{CAL_PRIMARY[0]}-{CAL_PRIMARY[1]}", "skala"].iloc[0])
    j = YEARS.max()
    left, right = cow.loc[j - 9:j].mean(), (ucdp.loc[j + 1:j + 10] * scale).mean()
    jump_sd = (right - left) / cow.std(ddof=1)
    return t, ratio, scale, jump_sd


def frame(s: pd.Series, variant: str, source) -> pd.DataFrame:
    d = pd.DataFrame({"variant": variant, "year": s.index.astype(int),
                      "source": source, "value": s.values})
    d["value_ma11c"] = d["value"].rolling(SMOOTH, center=True, min_periods=1).mean()
    d["value_ma11t"] = d["value"].rolling(SMOOTH, center=False, min_periods=1).mean()
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="/mnt/project")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--weights", choices=list(WEIGHT_SETS), default="inherited",
                    help="zestaw wag kategorii COW (D-008 §3.2); domyślnie odziedziczone")
    ap.add_argument("--normalization", choices=list(NORMALIZATIONS), default="raw",
                    help="normalizacja serii (D-008 §3.3); domyślnie raw")
    a = ap.parse_args()
    dd, od = Path(a.data_dir), Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)

    # Domyślne (inherited, raw) → weights=None, brak normalizacji → ścieżka v2.0 bit w bit.
    weights = None if a.weights == "inherited" else WEIGHT_SETS[a.weights]
    ucdp = build_ucdp(dd)
    parts, cal_all = [], []
    meta = {"script": VERSION, "ucdp_weights": UCDP_W,
            "weights": a.weights, "normalization": a.normalization}

    for level in ("W", "P"):
        cow = build_cow(dd, level, weights)
        t, ratio, scale, jump = calibrate(cow, ucdp)   # kalibracja zawsze na surowym cow
        t.insert(0, "poziom", level)
        cal_all.append(t)
        meta[f"level_{level}"] = {"scale": round(scale, 4), "D2_ratio": round(ratio, 3),
                                  "D2_pass": bool(ratio < D2_MAX_RATIO),
                                  "D3_jump_sd": round(float(jump), 3),
                                  "D3_pass": bool(abs(jump) < D3_MAX_SD)}
        cow_v = apply_normalization(cow, a.normalization, dd)   # identyczność, gdy raw
        parts.append(frame(cow_v, f"A_COW_{level}", "COW"))
        spl = pd.concat([cow, ucdp.loc[YEARS.max() + 1:] * scale])
        spl_v = apply_normalization(spl, a.normalization, dd)
        parts.append(frame(spl_v, f"C_SPLICED_{level}",
                           np.where(spl_v.index <= YEARS.max(), "COW", "UCDP_scaled")))
        print(f"[{level}] skala={scale:.3f} | D2 iloraz={ratio:.2f} "
              f"{'PASS' if ratio < D2_MAX_RATIO else 'FAIL'} | "
              f"D3 skok={jump:+.2f} SD {'PASS' if abs(jump) < D3_MAX_SD else 'FAIL'} | "
              f"2007={cow.loc[2007]:.1f}")

    parts.append(frame(ucdp, "B_UCDP", "UCDP"))
    out = pd.concat(parts, ignore_index=True)[
        ["variant", "year", "source", "value", "value_ma11c", "value_ma11t"]]

    hdr = "# " + json.dumps(meta, ensure_ascii=False)
    with open(od / "cps_canonical_v2.csv", "w", encoding="utf-8") as fh:
        fh.write(hdr + "\n"); out.to_csv(fh, index=False)
    pd.concat(cal_all).to_csv(od / "test0c_calibration.csv", index=False)
    print("\nwarianty:", out.variant.unique().tolist())
    print(f"zapisano {od/'cps_canonical_v2.csv'}")


if __name__ == "__main__":
    main()
