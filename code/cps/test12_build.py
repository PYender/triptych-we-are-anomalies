#!/usr/bin/env python3
"""
TEST 12 (rodzina 10) — Etap 1: budowa zbioru z UCDP Dyadic v25.1, wariant A (D-0xx).

Zrodlo: data/ucdp/Dyadic_v25_1.csv, 3432 diado-lata, 684 diady, 1946-2024 (zgodne z
protokolem SS3). Okno przycinane do 2023 (rok 2024 odrzucony, decyzja autora).

Epizod: maksymalny ciag KOLEJNYCH lat aktywnosci pary (przerwa jednoroczna konczy epizod).
Prog: >=3 epizody orzeka (P1), >=2 wariant wrazliwosci (S1).

Odstep (wariant A, SS4 protokolu): pelny = rok_start_nastepnego - rok_koniec_poprzedniego - 1
(rzeczywiste lata bez walk). Cenzurowany = 2023 - rok_koniec_ostatniego (okno domyka sie na
staлym roku kalendarzowym, nie na kolejnym epizodzie, wiec bez odejmowania jedynki).
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import pandas as pd


def episodes_from_years(years):
    eps = []
    cur = [years[0]]
    for y in years[1:]:
        if y == cur[-1] + 1:
            cur.append(y)
        else:
            eps.append((cur[0], cur[-1]))
            cur = [y]
    eps.append((cur[0], cur[-1]))
    return eps


def build(years_by_dyad, min_episodes, window_end=2023):
    rows = []
    t0_dyads = []
    for dyad_id, years in years_by_dyad.items():
        eps = episodes_from_years(years)
        if len(eps) < min_episodes:
            continue
        is_t0 = eps[0][0] == window_end - (window_end - 1946)  # == 1946, pierwszy rok okna
        if eps[0][0] == 1946:
            t0_dyads.append(dyad_id)
        for i in range(len(eps) - 1):
            e_prev, s_next = eps[i][1], eps[i + 1][0]
            gap = s_next - e_prev - 1
            t0_flag = int(is_t0 and i == 0)
            rows.append(dict(dyad_id=dyad_id, typ="pelny", cenzurowany=0,
                             dlugosc=gap, epizod_nr=i + 1, t0_flag=t0_flag,
                             ep_start=eps[i][0], ep_end=eps[i][1],
                             next_ep_start=eps[i + 1][0]))
        e_last = eps[-1][1]
        cens = window_end - e_last
        rows.append(dict(dyad_id=dyad_id, typ="cenzurowany", cenzurowany=1,
                         dlugosc=cens, epizod_nr=len(eps), t0_flag=0,
                         ep_start=eps[-1][0], ep_end=eps[-1][1], next_ep_start=None))
    return pd.DataFrame(rows), t0_dyads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/ucdp")
    ap.add_argument("--out-dir", default=".")
    args = ap.parse_args()
    dd, od = Path(args.data_dir), Path(args.out_dir); od.mkdir(parents=True, exist_ok=True)

    src = dd / "Dyadic_v25_1.csv"
    df = pd.read_csv(src)
    sha = hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    df = df[df.year <= 2023]
    years_by_dyad = df.groupby("dyad_id")["year"].apply(lambda s: sorted(set(s))).to_dict()

    tab3, t0_3 = build(years_by_dyad, 3)
    tab2, t0_2 = build(years_by_dyad, 2)

    def summarize(tab):
        full = tab[tab.typ == "pelny"]
        cens = tab[tab.typ == "cenzurowany"]
        return dict(pary=int(tab.dyad_id.nunique()), pelne=len(full), cenzurowane=len(cens),
                   mediana_pelny=float(full.dlugosc.median()), srednia_pelny=float(full.dlugosc.mean()),
                   zakres_pelny=[int(full.dlugosc.min()), int(full.dlugosc.max())],
                   jednoroczne_pelne=int((full.dlugosc == 1).sum()),
                   jednoroczne_pct=round(100 * (full.dlugosc == 1).mean(), 1),
                   mediana_cenzurowany=float(cens.dlugosc.median()))

    meta = {
        "builder": "test12_build.py v1.0 (TEST12_PROTOCOL, wariant A)",
        "zrodlo": src.name, "sha256": sha,
        "n_diado_lata_zrodlo": len(pd.read_csv(src)), "n_dyad_id_zrodlo": int(pd.read_csv(src).dyad_id.nunique()),
        "prog3": summarize(tab3), "prog2": summarize(tab2),
        "lewostronne_uciecie_t0": {"prog3_dyad_id": t0_3, "prog2_dyad_id": t0_2,
                                   "n_prog3": len(t0_3), "n_prog2": len(t0_2)},
    }

    with open(od / "test12_intervals_prog3.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False, default=str) + "\n")
        tab3.to_csv(fh, index=False)
    with open(od / "test12_intervals_prog2.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False, default=str) + "\n")
        tab2.to_csv(fh, index=False)

    print(json.dumps(meta, ensure_ascii=False, indent=2, default=str))
    print("zapisano test12_intervals_prog3.csv, test12_intervals_prog2.csv")


if __name__ == "__main__":
    main()
