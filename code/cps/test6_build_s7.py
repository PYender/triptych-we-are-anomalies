#!/usr/bin/env python3
"""
TEST 6 — S7: wariant wrażliwości poziomu B (państwo), TASK_S7.md, TEST6_PROTOCOL.md §3/§7.
Reguła scalania: D-024 §5 (wszystkie wojny tego samego państwa, niezależnie od przeciwnika).
Jednostka progu: epizody, D-038 (wpisana przed tą budową).

Jednostka: pojedyncze ccode. Źródło: InterStateWarData_v4_0.csv WYŁĄCZNIE (S8 z Extra-State
jest osobnym wariantem, tu nie wchodzi). Okno 1816-2007 (CLOSE=2007, jak w test6_build_intervals).

Fazy drugie (StartYear2/EndYear2) traktowane jako OSOBNE przedziały uczestnictwa (TASK_S7.md
§3) — czytanie dosłowne: gdy wiersz ma poprawną fazę 2, to DWA wpisy wejściowe do scalania
epizodów (D-013/D-024 §5 mechanizm), nie jeden span rozciągnięty do końca fazy 2. Duplikaty
(ccode,WarNum) (5 przypadków w danych — państwo zmieniające stronę w tej samej wojnie, np.
Włochy/Bułgaria/Rumunia w WWII 1943-44) NIE są sztucznie łączone — to legalnie osobne
uczestnictwa z osobnymi latami.

ROZBIEŻNOŚĆ Z LICZBAMI KONTROLNYMI AUTORA (TASK_S7.md §4) — zgłoszona, NIE dopasowana
(instrukcja zadania wprost tego zabrania). Zob. `S7_DYSKREPANCJA.md` dla pełnego zapisu
sprawdzonych wariantów. Ten builder używa reguły gap<=0, zgodnej dosłownie z D-013/D-024 §5
(cytowanej wprost przez to zadanie) — NIE przyjęto żadnej niezadeklarowanej tolerancji gap,
mimo że jedna z testowanych (gap<=1) dawała wynik bliższy oczekiwanemu.
"""
from __future__ import annotations
import argparse, hashlib, json, collections
from pathlib import Path

import numpy as np
import pandas as pd

import test0c_build_canonical as bld
import test6_build_intervals as t6

CLOSE = 2007
MIN_EPISODES_MAIN = 6      # próg S7 głowny (TEST6_PROTOCOL.md SS3 poziom B)
MIN_EPISODES_CHECK = 3     # drugi próg z liczb kontrolnych SS4 (TASK_S7.md), do weryfikacji


def endyr(row):
    ends = []
    for e in (row.EndYear1, row.EndYear2):
        if pd.isna(e):
            continue
        if e == -7 or e > 0:
            ends.append(CLOSE if e == -7 else e)
    return max(ends) if ends else np.nan


def state_conflicts(df: pd.DataFrame):
    """{ccode: [(start,end,wn,name), ...]} - fazy 2 jako OSOBNE wpisy gdy obecne (D-038/
    czytanie doslowne TASK_S7.md SS3)."""
    for c in ("ccode", "WarNum", "StartYear1", "EndYear1", "StartYear2", "EndYear2"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    out = collections.defaultdict(list)
    n_phase2 = 0
    for r in df.itertuples():
        cc = int(r.ccode)
        e1 = CLOSE if r.EndYear1 == -7 else r.EndYear1
        if pd.notna(r.StartYear1) and r.StartYear1 > 0 and pd.notna(e1) and e1 > 0:
            out[cc].append((int(r.StartYear1), int(e1), int(r.WarNum), str(r.WarName)))
        if pd.notna(r.StartYear2) and r.StartYear2 > 0:
            e2 = CLOSE if r.EndYear2 == -7 else r.EndYear2
            if pd.notna(e2) and e2 > 0:
                out[cc].append((int(r.StartYear2), int(e2), int(r.WarNum), str(r.WarName) + " (faza 2)"))
                n_phase2 += 1
    return {k: sorted(v) for k, v in out.items()}, n_phase2


def state_exposure(mem: dict, cc: int, t0: int, t1: int):
    """Lata ekspozycji w (t0,t1] wg system2016.csv - WYLACZNIE to jedno panstwo (D-014,
    zastosowane do jednej strony zamiast dwoch, bo drugiej tu nie ma - TASK_S7.md SS3)."""
    m = mem.get(cc, set())
    return sum(1 for y in range(t0 + 1, t1 + 1) if y in m)


def build(df, mem, entry, exitr, names, min_episodes):
    confs_by_state, n_phase2 = state_conflicts(df.copy())
    ep_rows, int_rows, dropped = [], [], []
    n_states_raw = len(confs_by_state)

    for cc, confs in sorted(confs_by_state.items()):
        episodes = t6.merge_episodes(confs)
        if len(episodes) < min_episodes:
            dropped.append({"ccode": cc, "panstwo": names.get(cc, cc), "n_epizodow": len(episodes)})
            continue
        for i, ep in enumerate(episodes, start=1):
            ep_rows.append({"ccode": cc, "panstwo": names.get(cc, cc), "epizod_nr": i,
                            "start": ep["start"], "koniec": ep["end"],
                            "n_skladowych": len(ep["members"]), "scalony": len(ep["members"]) > 1})
        for i in range(len(episodes) - 1):
            e_prev, s_next = episodes[i]["end"], episodes[i + 1]["start"]
            cal_gap = s_next - e_prev
            assert cal_gap > 0, f"S7: odstep kalendarzowy niedodatni po scaleniu, ccode {cc}: {cal_gap}"
            exp = state_exposure(mem, cc, e_prev, s_next)
            int_rows.append({"ccode": cc, "panstwo": names.get(cc, cc),
                             "rok_konca_poprz": e_prev, "rok_poczatku_nast": s_next,
                             "dlugosc_odstepu": exp, "dlugosc_kalendarzowa": cal_gap,
                             "cenzurowany": 0, "ekspozycja_zero": exp == 0})
        e_last = episodes[-1]["end"]
        x_end = exitr.get(cc)
        cens_end = min(CLOSE, x_end) if x_end is not None else CLOSE
        cal_gap = cens_end - e_last
        exp = state_exposure(mem, cc, e_last, cens_end) if cal_gap > 0 else 0
        int_rows.append({"ccode": cc, "panstwo": names.get(cc, cc),
                         "rok_konca_poprz": e_last, "rok_poczatku_nast": cens_end,
                         "dlugosc_odstepu": exp, "dlugosc_kalendarzowa": max(cal_gap, 0),
                         "cenzurowany": 1, "ekspozycja_zero": exp == 0})

    return pd.DataFrame(ep_rows), pd.DataFrame(int_rows), dropped, n_states_raw, n_phase2


def summarize(int_tab):
    if len(int_tab) == 0:
        return dict(panstwa=0, odstepy_pelne=0, odstepy_cenzurowane=0, pelne_ekspozycja_zero=0)
    full = int_tab[int_tab.cenzurowany == 0]
    return dict(panstwa=int(int_tab.ccode.nunique()),
               odstepy_pelne=int((int_tab.cenzurowany == 0).sum()),
               odstepy_cenzurowane=int((int_tab.cenzurowany == 1).sum()),
               pelne_ekspozycja_zero=int((full.ekspozycja_zero).sum()) if len(full) else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out-dir", default=".")
    args = ap.parse_args()
    dd, od = Path(args.data_dir), Path(args.out_dir); od.mkdir(parents=True, exist_ok=True)

    src = bld.find_input(dd, "InterStateWarData_v4_0.csv")
    df = bld.load_cow(src)
    names = dict(zip(pd.to_numeric(df.ccode, errors="coerce").dropna().astype(int), df.StateName))
    mem, mem_src = t6.load_membership(dd)
    entry = {cc: min(ys) for cc, ys in mem.items()}
    exitr = {cc: max(ys) for cc, ys in mem.items()}

    ep6, int6, dropped6, n_states_raw, n_phase2 = build(df, mem, entry, exitr, names, MIN_EPISODES_MAIN)
    ep3, int3, dropped3, _, _ = build(df, mem, entry, exitr, names, MIN_EPISODES_CHECK)

    # liczby przed nalozeniem ekspozycji (struktura czysta, D-028) - z build() ponownie
    # liczac odstepy PRZED sprawdzeniem ekspozycji: to juz sa te same liczby (ekspozycja nie
    # zmienia LICZBY odstepow, tylko ich DLUGOSC) - jawnie pokazane w podsumowaniu ponizej.

    meta = {
        "builder": "test6_build_s7.py v1.0 (D-038, TASK_S7.md)",
        "zrodlo_wojny": src.name, "sha256_wojny": hashlib.sha256(src.read_bytes()).hexdigest()[:16],
        "zrodlo_czlonkostwo": mem_src.name,
        "liczby_kontrolne_SS4": {
            "wierszy_uczestnictw_1816_2007": {"oczekiwane": 337, "policzone": len(df)},
            "przedzialow_po_rozbiciu_faz": {"oczekiwane": 356, "policzone": n_states_raw and sum(
                len(v) for v in state_conflicts(df.copy())[0].values())},
            "panstw_w_pliku": {"oczekiwane": 98, "policzone": int(pd.to_numeric(df.ccode, errors="coerce").nunique())},
            "panstw_prog_ge6": {"oczekiwane": 12, "policzone": summarize(int6)["panstwa"]},
            "odstepow_pelnych_prog_ge6": {"oczekiwane": 98, "policzone": summarize(int6)["odstepy_pelne"]},
            "panstw_prog_ge3": {"oczekiwane": 37, "policzone": summarize(int3)["panstwa"]},
            "odstepow_pelnych_prog_ge3": {"oczekiwane": 168, "policzone": summarize(int3)["odstepy_pelne"]},
        },
        "rozbieznosc_odnotowana": "TAK - patrz S7_DYSKREPANCJA.md, nie dopasowywane na sile (TASK_S7.md SS4)",
        "podsumowanie_ge6": summarize(int6),
        "podsumowanie_ge3": summarize(int3),
        "panstwa_odrzucone_prog_ge6_liczba": len(dropped6),
    }

    with open(od / "test6_s7_episodes.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False, default=str) + "\n")
        ep6.to_csv(fh, index=False)
    with open(od / "test6_s7_intervals.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False, default=str) + "\n")
        int6.to_csv(fh, index=False)
    with open(od / "test6_s7_intervals_prog3_kontrolne.csv", "w", encoding="utf-8") as fh:
        fh.write("# kontrolne, prog>=3, wylacznie do weryfikacji liczb SS4 - nie model glowny\n")
        int3.to_csv(fh, index=False)

    print(json.dumps(meta, ensure_ascii=False, indent=2, default=str))
    print("zapisano test6_s7_episodes.csv, test6_s7_intervals.csv, test6_s7_intervals_prog3_kontrolne.csv")


if __name__ == "__main__":
    main()
