#!/usr/bin/env python3
"""
TEST 0B — odtworzenie serii COW z plików surowych + korekta obsługi kodów braku.

Dwa tryby:
  --mode replica  : wierne odtworzenie reguły z analiza_poprawiona_final_GDELT.py
                    (kontrola: musi dać maks|Δ| = 0 wobec wars_color.csv)
  --mode fixed    : ta sama reguła z trzema poprawkami (patrz niżej)
  --mode both     : oba + plik porównawczy (domyślne)

Poprawki w trybie 'fixed':
  F1. Kod -7 w kolumnie End oznacza "wojna trwa w momencie zamknięcia zbioru".
      Oryginał traktuje go jak zwykłą datę, więc warunek Start <= rok <= End
      nigdy nie zachodzi i taka wojna wypada z serii CAŁKOWICIE — nie tylko
      z ogona. Dotyczy 13 wierszy Extra-State (start 2001–2004) i 12 wierszy
      Intra-State (start 1988–2014). Kody -8 i -9 pozostają wykluczone.
  F2. Non-State liczony poprawnie. Plik ma kolumny 'StartYear'/'EndYear' bez
      numeru fazy; oryginalna autodetekcja szuka po nich 'StartYear1'/'EndYear1',
      nie znajduje i zwraca pustą listę faz — kategoria wnosi do serii dokładnie
      zero we wszystkich 192 latach.
  F3. Intra-State: uwzględniona faza 4 (istnieje w v5.1, pętla oryginału idzie do 3).

Wagi (odziedziczone, nie zmieniać tutaj): Inter 1.0, Extra 0.7, Non 0.4, Intra 0.4.

Uwaga o poziomie agregacji — NIE jest korygowana, wymaga decyzji autora:
Inter-State ma 337 wierszy przy 95 wojnach, Extra-State 198 przy 163 — to pliki
na poziomie uczestnika. Non-State (62) i Intra-State (420) są na poziomie wojny.
Seria miesza więc "uczestniko-lata" z "wojno-latami".
"""
from __future__ import annotations
import argparse, hashlib, io, re
from pathlib import Path

import numpy as np
import pandas as pd

VERSION = "test0b_cow_rebuild.py v1.0"
YEARS = np.arange(1816, 2008)
CUTOFF = {"inter": 2007, "extra": 2007, "non": 2007, "intra": 2014}
WEIGHTS = {"inter": 1.0, "extra": 0.7, "non": 0.4, "intra": 0.4}
FILES = {
    "inter": "InterStateWarData_v4_0.csv",
    "extra": "ExtraStateWarData_v4_0.csv",
    "non":   "NonStateWarData_v4_0.csv",
    "intra": "INTRASTATE_WARS_v5_1_CSV.csv",
}


def load_cow(path: Path) -> pd.DataFrame:
    """Pliki COW mają zakończenia linii CR (starszy format Mac). Pandas radzi
    sobie z nimi dzięki uniwersalnym końcom linii, więc normalizacja nie jest
    konieczna — robimy ją dla niezależności od implementacji parsera."""
    with open(path, encoding="latin-1", newline="") as fh:
        raw = fh.read()
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    return pd.read_csv(io.StringIO(raw))


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

def active_counts(df: pd.DataFrame, phases: list[tuple[str, str]],
                  weight: float, fix_ongoing: bool, cutoff: int) -> np.ndarray:
    num = {c: pd.to_numeric(df[c], errors="coerce")
           for pair in phases for c in pair}
    out = np.zeros(len(YEARS))
    for i, y in enumerate(YEARS):
        mask = np.zeros(len(df), dtype=bool)
        for s_col, e_col in phases:
            s, e = num[s_col], num[e_col]
            if fix_ongoing:
                e = e.where(e != -7, cutoff)          # F1
            ok = s.notna() & (s > 0) & e.notna() & (e > 0)
            mask |= (ok & (s <= y) & (e >= y)).values
        out[i] = weight * mask.sum()
    return out


def phase_pairs(df: pd.DataFrame, base_s: str, base_e: str, kmax: int):
    p = [(f"{base_s}{k}", f"{base_e}{k}") for k in range(1, kmax + 1)
         if f"{base_s}{k}" in df.columns and f"{base_e}{k}" in df.columns]
    return p


def build(data_dir: Path, fixed: bool) -> np.ndarray:
    d = {k: load_cow(find_input(data_dir, v)) for k, v in FILES.items()}
    total = np.zeros(len(YEARS))
    # Inter-State — PATCH 3A: fazy 1 i 2
    total += active_counts(d["inter"], [("StartYear1", "EndYear1"),
                                        ("StartYear2", "EndYear2")],
                           WEIGHTS["inter"], fixed, CUTOFF["inter"])
    # Extra-State — fazy 1 i 2 (3 nie istnieje)
    total += active_counts(d["extra"], phase_pairs(d["extra"], "StartYear", "EndYear", 3),
                           WEIGHTS["extra"], fixed, CUTOFF["extra"])
    # Non-State — w oryginale nie wnosi nic (F2)
    if fixed:
        total += active_counts(d["non"], [("StartYear", "EndYear")],
                               WEIGHTS["non"], True, CUTOFF["non"])
    # Intra-State — fazy 1-3 w oryginale, 1-4 po korekcie (F3)
    total += active_counts(d["intra"], phase_pairs(d["intra"], "StartYr", "EndYr",
                                                   4 if fixed else 3),
                           WEIGHTS["intra"], fixed, CUTOFF["intra"])
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="/mnt/project")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--mode", choices=["replica", "fixed", "both"], default="both")
    ap.add_argument("--verify", default="wars_color.csv")
    a = ap.parse_args()
    dd, od = Path(a.data_dir), Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)

    cols = {"year": YEARS}
    if a.mode in ("replica", "both"):
        cols["wars_replica"] = build(dd, fixed=False)
    if a.mode in ("fixed", "both"):
        cols["wars_fixed"] = build(dd, fixed=True)
    out = pd.DataFrame(cols)

    try:
        vpath = find_input(dd, a.verify)
    except FileNotFoundError:
        vpath = None
    if "wars_replica" in out and vpath is not None:
        ref = pd.read_csv(vpath).set_index("year")["wars"].reindex(YEARS).values
        dmax = float(np.nanmax(np.abs(out.wars_replica.values - ref)))
        print(f"[D1] replika vs {a.verify}: maks|Δ| = {dmax:.6f} "
              f"→ {'PASS — seria odtwarzalna' if dmax < 1e-9 else 'FAIL'}")

    if a.mode == "both":
        r, f = out.wars_replica.values, out.wars_fixed.values
        print(f"[F]  korelacja replika/poprawiona 1816–2007: {np.corrcoef(r, f)[0,1]:.4f}")
        print(f"     średnia 1816–1990: {r[:175].mean():.2f} → {f[:175].mean():.2f}")
        print(f"     średnia 1998–2007: {r[-10:].mean():.2f} → {f[-10:].mean():.2f}")
        print(f"     rok 2007:          {r[-1]:.2f} → {f[-1]:.2f}")

    hdr = f"# {VERSION} | sha256(inter)={hashlib.sha256(find_input(dd, FILES['inter']).read_bytes()).hexdigest()[:16]}"
    with open(od / "cow_rebuilt.csv", "w", encoding="utf-8") as fh:
        fh.write(hdr + "\n"); out.to_csv(fh, index=False)
    print(f"\nZapisano {od/'cow_rebuilt.csv'}")


if __name__ == "__main__":
    main()
