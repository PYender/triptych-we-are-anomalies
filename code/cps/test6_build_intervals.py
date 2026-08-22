#!/usr/bin/env python3
"""
TEST 6 — Etap A: budowa zbioru odstępów między konfliktami (rodzina 9).
Realizuje TASK_6.md Etap A / TEST6_PROTOCOL.md §2–§4. D-012.

NIE liczy parametru Weibulla ani żadnej statystyki testowej — buduje wyłącznie
zbiór odstępów i jego dokumentację źródłową. Kod testu (test6_intervals.py) powstaje
w Etapie B, po przeglądzie.

Źródło: Inter-StateWarData_v4.0.csv (poziom uczestnika). Ciągłość państw ODZIEDZICZONA
po kodach COW (365, 255, 640) — nic nie mapujemy ręcznie (§0.3). Kody braku dat:
-7 = trwa do zamknięcia zbioru → 2007 (korekta F1); -8/-9 = brak/nie dotyczy.

Odstęp: KONIEC jednego konfliktu → POCZĄTEK następnego (§2). Jeden cenzurowany na diadę
(2007 − koniec ostatniego konfliktu, §4). Odstępy ujemne/zerowe (nakładające się lub
jednoczesne konflikty) są FLAGOWANE, nie usuwane — rozstrzygnięcie należy do autora (§A2).

Wyjście: test6_intervals.csv (surowy, kompletny: 62 pełne + 25 cenzurowanych).
"""
from __future__ import annotations
import argparse, hashlib, json, itertools, collections
from pathlib import Path

import numpy as np
import pandas as pd
import test0c_build_canonical as bld     # load_cow (obsługa CR), find_input

CLOSE = 2007                             # koniec okna obserwacji (D-003)
MIN_CONFLICTS_A = 3                      # poziom A: diady ≥3 wspólne konflikty (§3)


def war_spans(df: pd.DataFrame):
    """Dla każdej wojny: (start, koniec, nazwa, ccode strony 1, ccode strony 2).
    start = min StartYear1 (ważny); koniec = max ważny z {EndYear1, EndYear2} (−7→2007)."""
    for c in ("ccode", "Side", "WarNum", "StartYear1", "EndYear1", "StartYear2", "EndYear2"):
        df[c] = pd.to_numeric(df[c], errors="coerce")

    def endyr(row):
        ends = []
        for e in (row.EndYear1, row.EndYear2):
            if pd.isna(e):
                continue
            ends.append(CLOSE if e == -7 else e) if (e == -7 or e > 0) else None
        return max(ends) if ends else np.nan

    minus7 = int(((df.EndYear1 == -7) | (df.EndYear2 == -7)).sum())
    wars = {}
    for wn, g in df.groupby("WarNum"):
        st = [s for s in g.StartYear1 if pd.notna(s) and s > 0]
        en = [e for e in (endyr(r) for r in g.itertuples()) if pd.notna(e)]
        if not st or not en:
            continue
        wars[wn] = dict(start=int(min(st)), end=int(max(en)),
                        name=str(g.WarName.iloc[0]),
                        s1=sorted(set(g.loc[g.Side == 1, "ccode"].dropna().astype(int))),
                        s2=sorted(set(g.loc[g.Side == 2, "ccode"].dropna().astype(int))))
    return wars, minus7


def build_diads(wars):
    """diada = uporządkowana para (ccode_strona1, ccode_strona2); klucz = sorted((a,b))."""
    diad = collections.defaultdict(list)
    for wn, w in wars.items():
        for a, b in itertools.product(w["s1"], w["s2"]):
            if a != b:
                diad[tuple(sorted((a, b)))].append((w["start"], w["end"], wn, w["name"]))
    return {k: sorted(v) for k, v in diad.items()}


def intervals_rows(diad, names):
    """Wiersze odstępów dla poziomu A (diady ≥3 konflikty). Pełne + jeden cenzurowany
    na diadę. Ujemne/zerowe FLAGOWANE w kolumnie `flag`, nie usuwane."""
    rows = []
    A = {k: v for k, v in diad.items() if len(v) >= MIN_CONFLICTS_A}
    for (a, b), confs in sorted(A.items()):
        dname = f"{names.get(a, a)}–{names.get(b, b)}"
        for i in range(len(confs) - 1):
            s_prev, e_prev, wn_prev, nm_prev = confs[i]
            s_next, e_next, wn_next, nm_next = confs[i + 1]
            gap = s_next - e_prev
            flag = "ok" if gap > 0 else ("zero" if gap == 0 else "negatywny")
            rows.append({"diada": dname, "ccode_a": a, "ccode_b": b,
                         "rok_konca_poprz": e_prev, "rok_poczatku_nast": s_next,
                         "dlugosc_odstepu": gap, "czas_trwania_poprz": e_prev - s_prev,
                         "cenzurowany": 0, "epoka_1914": "przed" if e_prev < 1914 else "po",
                         "epoka_1945": "przed" if e_prev < 1945 else "po",
                         "flag": flag, "wojna_poprz": nm_prev, "wojna_nast": nm_next})
        # jeden odstęp cenzurowany na diadę (§4)
        s_last, e_last, wn_last, nm_last = confs[-1]
        rows.append({"diada": dname, "ccode_a": a, "ccode_b": b,
                     "rok_konca_poprz": e_last, "rok_poczatku_nast": CLOSE,
                     "dlugosc_odstepu": CLOSE - e_last, "czas_trwania_poprz": e_last - s_last,
                     "cenzurowany": 1, "epoka_1914": "przed" if e_last < 1914 else "po",
                     "epoka_1945": "przed" if e_last < 1945 else "po",
                     "flag": "ok", "wojna_poprz": nm_last, "wojna_nast": "(cenzurowany do 2007)"})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    dd, od = Path(a.data_dir), Path(a.out_dir); od.mkdir(parents=True, exist_ok=True)

    src = bld.find_input(dd, "InterStateWarData_v4_0.csv")
    df = bld.load_cow(src)
    names = dict(zip(pd.to_numeric(df.ccode, errors="coerce").dropna().astype(int), df.StateName))
    wars, minus7 = war_spans(df)
    diad = build_diads(wars)
    tab = intervals_rows(diad, names)

    meta = {"builder": "test6_build_intervals.py v1.0", "zrodlo": src.name,
            "sha256_src": hashlib.sha256(src.read_bytes()).hexdigest()[:16],
            "wierszy_-7": minus7, "diad_>=3": int((pd.Series({k: len(v) for k, v in diad.items()}) >= 3).sum()),
            "odstepy_pelne": int((tab.cenzurowany == 0).sum()),
            "odstepy_cenzurowane": int((tab.cenzurowany == 1).sum()),
            "ujemne": int((tab.flag == "negatywny").sum()), "zerowe": int((tab.flag == "zero").sum())}
    with open(od / "test6_intervals.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        tab.to_csv(fh, index=False)
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"zapisano {od/'test6_intervals.csv'}")


if __name__ == "__main__":
    main()
