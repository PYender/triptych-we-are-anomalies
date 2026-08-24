#!/usr/bin/env python3
"""
TEST 7 — Etap A: budowa zbioru okien ryzyka i czasów oczekiwania (rodzina 9b).
Realizuje TEST7_PROTOCOL.md §2-§5 / TASK_7A_BRIEF.md. D-013, D-014, D-015 A, D-016.

Populacja: diady figurujące w tss_rivalries (Thompson, Sakuwa, Suhas 2021) ze znacznikiem
spatial=1 — ŻADNEGO progu liczby wojen (§2 protokołu, zakaz nr 2). Diada bez ani jednej
wojny wchodzi jako obserwacja w pełni cenzurowana.

Okno ryzyka (§3): dla diady (a,b), per okres rywalizacji (niektóre diady mają >1 okres w
zbiorze — 141 diad / 152 wiersze). Okresy NIE są sklejane w jedno okno (TASK_7A_BRIEF.md §3.1)
— przerwa między okresami rywalizacji to czas bez wspólnej stawki, więc nie jest czasem
ryzyka. Ekspozycja sumowana po wszystkich okresach diady, analogicznie do przerw w
członkostwie (D-014): liczy się rok, w którym oba państwa są w system2016.csv I trwa
KTÓRYKOLWIEK okres rywalizacji tej diady.

Epizody (§4, D-013): scalanie przechodnie nachodzących/stykających się konfliktów, funkcje
reużyte z test6_build_intervals.py (ta sama definicja). Brane wyłącznie epizody wpadające w
okno ryzyka; epizody częściowo w oknie są ZGŁASZANE (tabela), nie obcinane po cichu.

NIE liczy żadnej statystyki czasów oczekiwania (§6 brief) — buduje wyłącznie zbiór.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, collections
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadr

import test0c_build_canonical as bld
import test6_build_intervals as t6          # war_spans, build_diads, merge_episodes,
                                             # load_membership (reużyte bez zmian, D-013/D-014)

CLOSE = 2007          # koniec zakresu Inter-StateWarData_v4.0.csv (§3 protokołu)
OPEN = 1816            # początek zbioru COW


# ============================ rywalizacje (tss_rivalries) ============================
def find_rda(dd: Path, fname: str) -> Path:
    """find_input (test0c) szuka wyłącznie *.csv — .rda potrzebuje własnego wyszukiwania."""
    exact = dd / fname
    if exact.exists():
        return exact
    hits = list(dd.rglob(fname))
    if len(hits) == 1:
        return hits[0]
    raise FileNotFoundError(f"nie znaleziono '{fname}' w {dd}" if not hits
                            else f"niejednoznaczne dopasowanie '{fname}': {hits}")


def load_rivalries(dd: Path, fname="tss_rivalries.rda"):
    src = find_rda(dd, fname)
    obj = pyreadr.read_r(str(src))
    df = list(obj.values())[0]
    return df, src


def spatial_diad_periods(df: pd.DataFrame):
    """spatial==1, klucz = para nieuporządkowana. Zwraca {diad: [(start,end), ...]} —
    NIEKTÓRE diady mają >1 wiersz (152 wiersze / 141 diad, §3.1 brief)."""
    sp = df[df.spatial == 1]
    out = collections.defaultdict(list)
    for r in sp.itertuples():
        key = tuple(sorted((int(r.ccode1), int(r.ccode2))))
        out[key].append((int(r.start), int(r.end)))
    return {k: sorted(v) for k, v in out.items()}


# ============================ okna ryzyka (§3) ============================
def entry_exit_years(mem: dict):
    return {cc: min(ys) for cc, ys in mem.items()}, {cc: max(ys) for cc, ys in mem.items()}


def build_windows(diad_periods, mem, entry, exitr):
    """Dla każdej diady: lista okresów po przycięciu do (rywalizacja ∩ członkostwo obu stron
    ∩ [1816,2007]), z flagą `ucieta` gdy oryginalny start rywalizacji < 1816 (§3 protokołu)."""
    windows = {}
    for (a, b), periods in diad_periods.items():
        ea = entry.get(a); xa = exitr.get(a)
        eb = entry.get(b); xb = exitr.get(b)
        valid = []
        for rs, re in periods:
            if ea is None or eb is None:      # strona nigdy nie w system2016.csv
                continue
            t0 = max(rs, ea, eb, OPEN)
            t1 = min(re, xa, xb, CLOSE)
            ucieta = int(rs < OPEN)
            if t1 > t0:
                valid.append({"rs": rs, "re": re, "t0": t0, "t1": t1, "ucieta": ucieta})
        if valid:
            windows[(a, b)] = valid
    return windows


def rivalry_year_ok(y, periods):
    return any(p["t0"] <= y <= p["t1"] for p in periods)


def exposure_multi(mem, a, b, t0, t1, periods):
    """Jak D-014, plus warunek: rok musi też należeć do KTÓREGOŚ okresu rywalizacji tej
    diady (§3.1 brief — przerwa między okresami nie jest czasem ryzyka)."""
    ma, mb = mem.get(a, set()), mem.get(b, set())
    return sum(1 for y in range(t0 + 1, t1 + 1) if y in ma and y in mb and rivalry_year_ok(y, periods))


# ============================ epizody w oknie (§4, §3.3 brief) ============================
def episode_window_status(ep, periods):
    """'inside' (start i koniec w tym samym okresie), 'outside' (poza wszystkimi
    okresami), 'partial' (przecina granicę okresu/okna — do zgłoszenia, nie do obcięcia)."""
    for p in periods:
        if p["t0"] <= ep["start"] and ep["end"] <= p["t1"]:
            return "inside", p
    starts_in = any(p["t0"] <= ep["start"] <= p["t1"] for p in periods)
    ends_in = any(p["t0"] <= ep["end"] <= p["t1"] for p in periods)
    if starts_in or ends_in:
        return "partial", None
    return "outside", None


# ============================ struktura obserwacji (§5) ============================
def diad_rows(dname, a, b, periods, episodes, mem):
    """Zwraca (interval_rows, partial_flags). t0 (otwarcie->pierwszy epizod) zapisany z
    flagą `t0_flag=1`, poza modelem głównym (§5 protokołu). Diada bez epizodów w oknie:
    jedna obserwacja w pełni cenzurowana o długości całego okna (sumy okresów)."""
    rows, partials = [], []
    inside = []
    for ep in episodes:
        status, p = episode_window_status(ep, periods)
        if status == "inside":
            inside.append(ep)
        elif status == "partial":
            partials.append({"diada": dname, "start": ep["start"], "end": ep["end"],
                             "nazwa": ep["name"]})
        # 'outside': poza oknem, poza analizą — nie jest to przypadek do zgłoszenia
    inside.sort(key=lambda e: e["start"])

    win_start = periods[0]["t0"]
    win_end = periods[-1]["t1"]
    ucieta_any = int(any(p["ucieta"] for p in periods))

    if not inside:
        gap = exposure_multi(mem, a, b, win_start, win_end, periods)
        rows.append({"diada": dname, "ccode_a": a, "ccode_b": b, "typ": "cenzurowany_bez_epizodow",
                     "rok_start": win_start, "rok_koniec": win_end, "ekspozycja": gap,
                     "cenzurowany": 1, "t0_flag": 0, "ucieta": ucieta_any})
        return rows, partials

    # t0: od otwarcia okna do pierwszego epizodu — zapisany, POZA modelem głównym
    e0 = exposure_multi(mem, a, b, win_start, inside[0]["start"], periods)
    rows.append({"diada": dname, "ccode_a": a, "ccode_b": b, "typ": "t0",
                 "rok_start": win_start, "rok_koniec": inside[0]["start"], "ekspozycja": e0,
                 "cenzurowany": 0, "t0_flag": 1, "ucieta": ucieta_any})

    for i in range(len(inside) - 1):
        e_prev, s_next = inside[i]["end"], inside[i + 1]["start"]
        gap = exposure_multi(mem, a, b, e_prev, s_next, periods)
        assert gap > 0, (f"D-013 §2 / brief §3.4: odstęp pełny o ekspozycji<=0 w {dname} "
                         f"({e_prev}->{s_next}). Zgłosić, nie łatać.")
        rows.append({"diada": dname, "ccode_a": a, "ccode_b": b, "typ": "pelny",
                     "rok_start": e_prev, "rok_koniec": s_next, "ekspozycja": gap,
                     "cenzurowany": 0, "t0_flag": 0, "ucieta": ucieta_any})

    e_last = inside[-1]["end"]
    gap = exposure_multi(mem, a, b, e_last, win_end, periods)
    rows.append({"diada": dname, "ccode_a": a, "ccode_b": b, "typ": "cenzurowany",
                 "rok_start": e_last, "rok_koniec": win_end, "ekspozycja": gap,
                 "cenzurowany": 1, "t0_flag": 0, "ucieta": ucieta_any})
    return rows, partials


# ============================ główny bieg ============================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    dd, od = Path(a.data_dir), Path(a.out_dir); od.mkdir(parents=True, exist_ok=True)

    tss, tss_src = load_rivalries(dd, "tss_rivalries.rda")
    diad_periods = spatial_diad_periods(tss)

    mem, mem_src = t6.load_membership(dd)
    entry, exitr = entry_exit_years(mem)
    windows = build_windows(diad_periods, mem, entry, exitr)
    dropped_empty = sorted(set(diad_periods) - set(windows))

    war_src = bld.find_input(dd, "InterStateWarData_v4_0.csv")
    wdf = bld.load_cow(war_src)
    names = dict(zip(pd.to_numeric(wdf.ccode, errors="coerce").dropna().astype(int), wdf.StateName))
    abbrev = dict(zip(pd.read_csv(mem_src)["ccode"], pd.read_csv(mem_src)["stateabb"]))

    def nm(cc):
        return names.get(cc) or abbrev.get(cc) or str(cc)

    wars, minus7 = t6.war_spans(wdf)
    diad_all = t6.build_diads(wars)   # WSZYSTKIE diady, bez progu (zakaz nr 2)

    win_rows, int_rows, partial_rows = [], [], []
    for (a, b), periods in sorted(windows.items()):
        dname = f"{nm(a)}–{nm(b)}"
        for p in periods:
            win_rows.append({"diada": dname, "ccode_a": a, "ccode_b": b, **p})
        confs = diad_all.get((a, b), [])
        episodes = [{"start": ep["start"], "end": ep["end"],
                    "name": "; ".join(m[3] for m in ep["members"])}
                   for ep in t6.merge_episodes(confs)]
        rows, partials = diad_rows(dname, a, b, periods, episodes, mem)
        int_rows += rows
        partial_rows += partials

    win_tab = pd.DataFrame(win_rows)
    int_tab = pd.DataFrame(int_rows)
    partial_tab = pd.DataFrame(partial_rows)

    meta = {"builder": "test7_build_windows.py v1.0", "zrodlo_rywalizacje": tss_src.name,
            "sha256_tss_rda": hashlib.sha256(tss_src.read_bytes()).hexdigest()[:16],
            "zrodlo_wojny": war_src.name, "sha256_wojny": hashlib.sha256(war_src.read_bytes()).hexdigest()[:16],
            "zrodlo_czlonkostwo": mem_src.name, "sha256_czlonkostwo": hashlib.sha256(mem_src.read_bytes()).hexdigest()[:16],
            "spatial_wiersze": int((tss.spatial == 1).sum()), "spatial_diad": len(diad_periods),
            "diad_z_niepustym_oknem": len(windows), "diady_odrzucone_puste_okno": len(dropped_empty),
            "epizody_czesciowo_w_oknie": len(partial_rows)}

    with open(od / "test7_windows.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n"); win_tab.to_csv(fh, index=False)
    with open(od / "test7_intervals.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n"); int_tab.to_csv(fh, index=False)
    partial_tab.to_csv(od / "test7_partial_episodes.csv", index=False)

    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"diady odrzucone (puste okno): {dropped_empty}")
    print(f"zapisano test7_windows.csv, test7_intervals.csv, test7_partial_episodes.csv w {od}")


if __name__ == "__main__":
    main()
