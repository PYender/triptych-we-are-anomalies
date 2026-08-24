#!/usr/bin/env python3
"""
TEST 6 — Etap A: budowa zbioru odstępów między konfliktami (rodzina 9).
Realizuje TASK_6.md Etap A / TEST6_PROTOCOL.md §2–§4 + D-012 + D-013 (epizody) + D-014
(ekspozycja).

v3.0 wdraża D-014: odstęp = liczba lat EKSPOZYCJI (lat, w których OBA kody ccode diady
są członkami systemu państw COW wg `system2016.csv`), nie różnica dat kalendarzowych.
Para, której jedna strona nie istnieje w systemie międzynarodowym, nie jest w tym czasie
narażona na konflikt — te lata nie są obserwacją o czasie oczekiwania (§2 protokołu).

Trzy warianty (D-014 addendum §4, nie cztery — nie krzyżujemy obu wymiarów):
  główny (test6_intervals.csv)              — próg na epizodach (D-013) × ekspozycja (D-014)
  S-A    (test6_intervals_sensitivity_SA.csv) — próg na epizodach × KALENDARZ (wrażliwość D-014)
  S-B    (test6_intervals_sensitivity_SB.csv) — próg na wierszach surowych × ekspozycja (wrażliwość D-013)

Asercje (D-014 §3): odstęp PEŁNY o ekspozycji zero → STOP, zgłoś (sprzeczność zbioru wojen
z zbiorem członkostwa). Odstęp CENZUROWANY o ekspozycji zero jest dopuszczalny (log S(0)=0);
diada zostaje w zbiorze przez swoje odstępy pełne.

Scalanie w epizody (D-013): konflikty tej samej diady nachodzące się lub stykające (gap≤0)
→ jeden epizod (najwcześniejszy start, najpóźniejszy koniec, przechodnio). Próg ≥3 na
epizodach dla wariantu głównego i S-A; na surowych wierszach (25 diad) dla S-B.

Źródło wojen: Inter-StateWarData_v4.0.csv. Źródło członkostwa: system2016.csv (COW State
System Membership v2016; kolumny ccode, year — jeden wiersz na parę ccode/rok obecności).
Ciągłość państw odziedziczona po kodach COW (D-012), nic nie mapujemy ręcznie.

NIE liczy parametru Weibulla ani żadnej statystyki testowej. Kod testu (test6_intervals.py)
powstaje w Etapie B, po przeglądzie (STOP, Krok 1b, TASK_6A_ADDENDUM.md §6).
"""
from __future__ import annotations
import argparse, hashlib, json, itertools, collections
from pathlib import Path

import numpy as np
import pandas as pd
import test0c_build_canonical as bld     # load_cow (obsługa CR), find_input

CLOSE = 2007                             # koniec okna obserwacji (D-003)
MIN_CONFLICTS_A = 3                      # próg ≥3 (D-012; jednostka wg D-013 §3)


# ============================ wojny i epizody (D-012, D-013 — bez zmian od v2.0) ============
def war_spans(df: pd.DataFrame):
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
    diad = collections.defaultdict(list)
    for wn, w in wars.items():
        for a, b in itertools.product(w["s1"], w["s2"]):
            if a != b:
                diad[tuple(sorted((a, b)))].append((w["start"], w["end"], wn, w["name"]))
    return {k: sorted(v) for k, v in diad.items()}


def merge_episodes(confs):
    episodes = []
    cur = None
    for s, e, wn, nm in confs:
        if cur is None:
            cur = {"start": s, "end": e, "members": [(s, e, wn, nm)]}
        elif s <= cur["end"]:
            cur["end"] = max(cur["end"], e)
            cur["members"].append((s, e, wn, nm))
        else:
            episodes.append(cur)
            cur = {"start": s, "end": e, "members": [(s, e, wn, nm)]}
    if cur is not None:
        episodes.append(cur)
    return episodes


def episode_rows(dname, a, b, episodes):
    rows = []
    for i, ep in enumerate(episodes, start=1):
        scalony = len(ep["members"]) > 1
        skladowe = "; ".join(f"{nm} ({s}-{e})" for s, e, wn, nm in ep["members"])
        rows.append({"diada": dname, "ccode_a": a, "ccode_b": b, "epizod_nr": i,
                     "start": ep["start"], "koniec": ep["end"],
                     "n_skladowych": len(ep["members"]), "scalony": scalony,
                     "skladowe_konflikty": skladowe})
    return rows


# ============================ członkostwo w systemie (D-014) ============================
def load_membership(dd: Path):
    """system2016.csv (COW State System Membership v2016): ccode, year → {ccode: {lata}}."""
    src = bld.find_input(dd, "system2016.csv")
    df = pd.read_csv(src)
    cols = {c.lower(): c for c in df.columns}
    ccol, ycol = cols.get("ccode"), cols.get("year")
    assert ccol and ycol, f"system2016.csv: brak kolumn ccode/year (mam: {list(df.columns)})"
    df[ccol] = pd.to_numeric(df[ccol], errors="coerce")
    df[ycol] = pd.to_numeric(df[ycol], errors="coerce")
    mem = collections.defaultdict(set)
    for cc, yr in zip(df[ccol].dropna().astype(int), df[ycol].dropna().astype(int)):
        mem[cc].add(int(yr))
    return mem, src


def exposure(mem, a, b, t0, t1):
    """Lata ekspozycji w (t0, t1] — oba ccode członkami (D-014 §3.2). Przedział otwarty
    z lewej, domknięty z prawej — zgodny z konwencją odstępu kalendarzowego t1 - t0."""
    ma, mb = mem.get(a, set()), mem.get(b, set())
    return sum(1 for y in range(t0 + 1, t1 + 1) if y in ma and y in mb)


# ============================ budowa odstępów (jeden wariant czasu naraz) ============
def interval_rows_for(dname, a, b, episodes, mem, use_exposure: bool):
    """use_exposure=True: D-014 (ekspozycja). False: kalendarzowy (wrażliwość S-A)."""
    rows = []
    for i in range(len(episodes) - 1):
        e_prev, s_next = episodes[i]["end"], episodes[i + 1]["start"]
        cal_gap = s_next - e_prev
        assert cal_gap > 0, (f"BŁĄD IMPLEMENTACJI (D-013 §2): odstęp kalendarzowy niedodatni "
                              f"po scaleniu w {dname}: {cal_gap}. Zgłosić, nie łatać.")
        if use_exposure:
            gap = exposure(mem, a, b, e_prev, s_next)
            assert gap > 0, (f"D-014 §3: odstęp PEŁNY o ekspozycji zero w {dname} "
                              f"({e_prev}->{s_next}, kalendarzowo {cal_gap}) — sprzeczność "
                              f"zbioru wojen z zbiorem członkostwa. Zgłosić, nie łatać.")
        else:
            gap = cal_gap
        rows.append({"diada": dname, "ccode_a": a, "ccode_b": b,
                     "rok_konca_poprz": e_prev, "rok_poczatku_nast": s_next,
                     "dlugosc_odstepu": gap, "dlugosc_kalendarzowa": cal_gap,
                     "cenzurowany": 0, "epoka_1914": "przed" if e_prev < 1914 else "po",
                     "epoka_1945": "przed" if e_prev < 1945 else "po", "flag": "ok"})
    e_last = episodes[-1]["end"]
    cal_gap = CLOSE - e_last
    gap = exposure(mem, a, b, e_last, CLOSE) if use_exposure else cal_gap
    # cenzurowany o ekspozycji zero dopuszczalny (D-014 §3) — brak asercji tutaj
    rows.append({"diada": dname, "ccode_a": a, "ccode_b": b,
                 "rok_konca_poprz": e_last, "rok_poczatku_nast": CLOSE,
                 "dlugosc_odstepu": gap, "dlugosc_kalendarzowa": cal_gap,
                 "cenzurowany": 1, "epoka_1914": "przed" if e_last < 1914 else "po",
                 "epoka_1945": "przed" if e_last < 1945 else "po", "flag": "ok"})
    return rows


def write_csv(path, tab, meta):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        tab.to_csv(fh, index=False)


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
    diad_all = build_diads(wars)
    mem, mem_src = load_membership(dd)

    raw_ge3 = {k: v for k, v in diad_all.items() if len(v) >= MIN_CONFLICTS_A}

    ep_rows = []
    main_rows, sa_rows, sb_rows = [], [], []      # główny, S-A (kalendarz), S-B (próg surowy)
    dropped = []
    for (aa, bb), confs in sorted(raw_ge3.items()):
        dname = f"{names.get(aa, aa)}–{names.get(bb, bb)}"
        episodes = merge_episodes(confs)
        ep_rows += episode_rows(dname, aa, bb, episodes)

        ivals_exp = interval_rows_for(dname, aa, bb, episodes, mem, use_exposure=True)
        ivals_cal = interval_rows_for(dname, aa, bb, episodes, mem, use_exposure=False)

        sb_rows += ivals_exp                                    # S-B: próg surowy, ekspozycja
        if len(episodes) >= MIN_CONFLICTS_A:                    # próg epizodowy: główny i S-A
            main_rows += ivals_exp
            sa_rows += ivals_cal
        else:
            dropped.append({"diada": dname, "n_konfliktow_surowych": len(confs),
                            "n_epizodow_po_scaleniu": len(episodes)})

    ep_tab = pd.DataFrame(ep_rows)
    main_tab, sa_tab, sb_tab = pd.DataFrame(main_rows), pd.DataFrame(sa_rows), pd.DataFrame(sb_rows)

    meta_common = {"builder": "test6_build_intervals.py v3.0 (D-013 epizody + D-014 ekspozycja)",
                   "zrodlo_wojny": src.name, "sha256_wojny": hashlib.sha256(src.read_bytes()).hexdigest()[:16],
                   "zrodlo_czlonkostwo": mem_src.name,
                   "sha256_czlonkostwo": hashlib.sha256(mem_src.read_bytes()).hexdigest()[:16],
                   "diad_>=3_surowych_wierszy": len(raw_ge3),
                   "diady_odrzucone_po_progu_na_epizodach": dropped}

    def summ(tab):
        return dict(diad=int(tab.diada.nunique()) if len(tab) else 0,
                    odstepy_pelne=int((tab.cenzurowany == 0).sum()) if len(tab) else 0,
                    odstepy_cenzurowane=int((tab.cenzurowany == 1).sum()) if len(tab) else 0)

    write_csv(od / "test6_intervals.csv", main_tab,
              dict(meta_common, wariant="GŁÓWNY — próg na epizodach × ekspozycja (D-013+D-014)",
                  **summ(main_tab)))
    write_csv(od / "test6_intervals_sensitivity_SA.csv", sa_tab,
              dict(meta_common, wariant="S-A — próg na epizodach × KALENDARZ (wrażliwość D-014, poza §8)",
                  **summ(sa_tab)))
    write_csv(od / "test6_intervals_sensitivity_SB.csv", sb_tab,
              dict(meta_common, wariant="S-B — próg na wierszach surowych × ekspozycja (wrażliwość D-013, poza §8)",
                  **summ(sb_tab)))
    write_csv(od / "test6_episodes.csv", ep_tab,
              {"builder": meta_common["builder"], "opis": "tabela scaleń (D-013)"})

    print(json.dumps({"glowny": summ(main_tab), "S-A": summ(sa_tab), "S-B": summ(sb_tab),
                      "diady_odrzucone": dropped}, ensure_ascii=False, indent=2))
    print(f"zapisano test6_intervals.csv, test6_intervals_sensitivity_SA.csv, "
          f"test6_intervals_sensitivity_SB.csv, test6_episodes.csv w {od}")


if __name__ == "__main__":
    main()
