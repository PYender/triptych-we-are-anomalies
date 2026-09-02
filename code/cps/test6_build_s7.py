#!/usr/bin/env python3
"""
TEST 6 — S7: wariant wrażliwości poziomu B (państwo), TASK_S7.md, TEST6_PROTOCOL.md §3/§7.
Reguła scalania: D-024 §5 (wszystkie wojny tego samego państwa, niezależnie od przeciwnika).
Jednostka progu: epizody, D-038 (wpisana przed tą budową).

Jednostka: pojedyncze ccode. Źródło: InterStateWarData_v4_0.csv WYŁĄCZNIE (S8 z Extra-State
jest osobnym wariantem, tu nie wchodzi). Okno 1816-2007 (CLOSE=2007, jak w test6_build_intervals).

v2.0 — ROZSTRZYGNIĘCIE ROZBIEŻNOŚCI Z v1.0 (autor, wiadomość po S7_DYSKREPANCJA.md):

1. **Próg scalania między różnymi wojnami = gap<=0.** Sprawdzone wprost w kodzie Testu 6
   (`test6_build_intervals.merge_episodes`: `elif s <= cur["end"]`) — jednoznaczne, żadnej
   innej tolerancji nigdzie w tamtym pliku. S7 zmienia WYŁĄCZNIE jednostkę analizy wobec
   Testu 6, więc reguła scalania musi być identyczna — używana tu bez zmian.

2. **D-040 (nowa decyzja autora): uczestnictwa TEJ SAMEJ wojny (ten sam WarNum) scalają się
   w JEDEN przedział niezależnie od kalendarzowego odstępu między nimi** — czy to z powodu
   rozbicia na fazy (StartYear2/EndYear2), czy z powodu dwóch osobnych wierszy (zmiana
   strony w trakcie wojny: Francja/Włochy/Bułgaria/Rumunia WWII, Łotwa 1919 — 5 przypadków
   w danych). Uzasadnienie: zmiana strony w trakcie wojny nie jest przerwą w regeneracji —
   to wciąż ta sama wojna. W praktyce 4 z 5 przypadków i tak scalały się już pod samym
   gap<=0 (odstęp między ich fazami = 0 lat) — jedynym przypadkiem, gdzie D-040 realnie
   zmienia wynik, jest Francja: WWII faza 1 (1939-1941, łącznie z wojną francusko-tajską,
   osobny WarNum) kończy się 1941, faza 2 („Wolna Francja") zaczyna się 1944 — 3-letni
   realny odstęp kalendarzowy, teraz scalony w jeden epizod 1939-1945 na mocy D-040, a nie
   dlatego, że gap<=0 by go i tak scalił (nie scaliłby: 1944-1941=3>0).

Etap 1 v1.0 (gap<=0, brak D-040) dał 15 państw / 123 odstępy pełne przy progu >=6 — te
liczby ZASTĄPIONE przez policzone poniżej (v2.0, gap<=0 + D-040). Autora liczby 12/98
(oparte na nierozstrzygniętym wtedy progu, jak się okazało — gap<=1) idą do erraty
(`S7_DYSKREPANCJA.md` zawiera pełny zapis dochodzenia).
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


def _endyr_single(e):
    """Jeden kandydat na koniec (EndYear1 albo EndYear2) po obsłudze sentynela -7 (wciąż
    trwa w 2007) - None gdy nie dotyczy (-8)."""
    if pd.isna(e):
        return None
    if e == -7:
        return CLOSE
    if e > 0:
        return e
    return None


def state_conflicts(df: pd.DataFrame):
    """{ccode: [(start,end,wn,name), ...]}.

    D-040 (2026-09-02, decyzja autora): uczestnictwa tego samego państwa w TEJ SAMEJ wojnie
    (ten sam WarNum) - czy to z powodu rozbicia na fazy (StartYear2/EndYear2), czy z powodu
    dwóch osobnych wierszy (zmiana strony w trakcie wojny - 5 przypadków w danych: Francja/
    Włochy/Bułgaria/Rumunia WWII, Łotwa 1919) - SCALAJĄ SIĘ W JEDEN PRZEDZIAŁ niezależnie od
    kalendarzowego odstępu między nimi (min start, max end po wszystkich wierszach i fazach
    tego (ccode,WarNum)). Uzasadnienie autora: zmiana strony w trakcie wojny nie jest przerwą
    w walce/regeneracji - to WCIĄŻ ta sama wojna. Dopiero PO tym scaleniu działa ogólna reguła
    D-013/D-024 SS5 (gap<=0) MIĘDZY różnymi wojnami (WarNum)."""
    for c in ("ccode", "WarNum", "StartYear1", "EndYear1", "StartYear2", "EndYear2"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    per_war = collections.defaultdict(lambda: {"starts": [], "ends": [], "name": None})
    for r in df.itertuples():
        key = (int(r.ccode), int(r.WarNum))
        g = per_war[key]
        g["name"] = str(r.WarName)
        if pd.notna(r.StartYear1) and r.StartYear1 > 0:
            g["starts"].append(int(r.StartYear1))
        for e in (r.EndYear1, r.EndYear2):
            v = _endyr_single(e)
            if v is not None:
                g["ends"].append(int(v))

    out = collections.defaultdict(list)
    n_multi_row_war = 0
    for (cc, wn), g in per_war.items():
        if not g["starts"] or not g["ends"]:
            continue
        out[cc].append((min(g["starts"]), max(g["ends"]), wn, g["name"]))
    n_multi_row_war = sum(1 for (cc, wn), g in per_war.items() if len(g["starts"]) > 1 or len(g["ends"]) > 1)
    return {k: sorted(v) for k, v in out.items()}, n_multi_row_war


def state_exposure(mem: dict, cc: int, t0: int, t1: int):
    """Lata ekspozycji w (t0,t1] wg system2016.csv - WYLACZNIE to jedno panstwo (D-014,
    zastosowane do jednej strony zamiast dwoch, bo drugiej tu nie ma - TASK_S7.md SS3)."""
    m = mem.get(cc, set())
    return sum(1 for y in range(t0 + 1, t1 + 1) if y in m)


def build(df, mem, entry, exitr, names, min_episodes):
    confs_by_state, _n_multi_row_war = state_conflicts(df.copy())
    ep_rows, int_rows, dropped = [], [], []

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

    return pd.DataFrame(ep_rows), pd.DataFrame(int_rows), dropped


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

    ep6, int6, dropped6 = build(df, mem, entry, exitr, names, MIN_EPISODES_MAIN)
    ep3, int3, dropped3 = build(df, mem, entry, exitr, names, MIN_EPISODES_CHECK)

    # kontrolna liczba "356" (SS4) jest niezalezna od D-040 (scalanie tego samego WarNum) -
    # to jest surowa liczba przedzialow PRZED jakimkolwiek scalaniem, wylacznie po rozbiciu faz
    n_rozbicie_faz = len(df) + int(((df.StartYear2 > 0) & (df.EndYear2 > 0)).sum())
    _, n_multi_row_war = state_conflicts(df.copy())

    meta = {
        "builder": "test6_build_s7.py v2.0 (D-038 + D-040, TASK_S7.md)",
        "zrodlo_wojny": src.name, "sha256_wojny": hashlib.sha256(src.read_bytes()).hexdigest()[:16],
        "zrodlo_czlonkostwo": mem_src.name,
        "D040_panstw_wojen_wielowierszowych_scalonych": n_multi_row_war,
        "liczby_kontrolne_SS4": {
            "wierszy_uczestnictw_1816_2007": {"oczekiwane": 337, "policzone": len(df)},
            "przedzialow_po_rozbiciu_faz": {"oczekiwane": 356, "policzone": n_rozbicie_faz},
            "panstw_w_pliku": {"oczekiwane": 98, "policzone": int(pd.to_numeric(df.ccode, errors="coerce").nunique())},
            "panstw_prog_ge6": {"oczekiwane": 12, "policzone": summarize(int6)["panstwa"]},
            "odstepow_pelnych_prog_ge6": {"oczekiwane": 98, "policzone": summarize(int6)["odstepy_pelne"]},
            "panstw_prog_ge3": {"oczekiwane": 37, "policzone": summarize(int3)["panstwa"]},
            "odstepow_pelnych_prog_ge3": {"oczekiwane": 168, "policzone": summarize(int3)["odstepy_pelne"]},
        },
        "rozbieznosc_v1_rozstrzygnieta": "gap<=0 potwierdzone kodem Testu 6 + D-040 (scalanie "
                                        "wewnatrz tego samego WarNum) - patrz S7_DYSKREPANCJA.md "
                                        "dla historii dochodzenia, autora liczby 12/98 w erracie",
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
