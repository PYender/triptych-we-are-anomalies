#!/usr/bin/env python3
"""
TEST 6 — Etap A: budowa zbioru odstępów między konfliktami (rodzina 9).
Realizuje TASK_6.md Etap A / TEST6_PROTOCOL.md §2–§4 + D-012 + D-013 (scalanie w epizody).

v2.0 wdraża D-013: konflikty tej samej diady nachodzące się w czasie lub stykające się
(gap ≤ 0) są scalane w JEDEN EPIZOD (od najwcześniejszego początku do najpóźniejszego
końca w grupie, scalanie przechodnie). Odstęp liczony od końca epizodu do początku
następnego. Próg ≥3 stosowany do LICZBY EPIZODÓW (jednostka analizy), nie do surowych
wierszy pliku (D-013 §3) — to zmiana jednostki progu, nie kryterium.

Obowiązkowy wariant wrażliwości (D-013 §4): te same epizody, próg liczony na surowych
wierszach (25 diad sprzed przebudowy), bez odrzucania diad spadających <3 epizody po
scaleniu — pokazuje, czy rozstrzygnięcie progu przesądza wynik.

Źródło: Inter-StateWarData_v4.0.csv (poziom uczestnika). Ciągłość państw ODZIEDZICZONA
po kodach COW (365, 255, 640) — nic nie mapujemy ręcznie (§0.3, D-012). Kody braku dat:
-7 = trwa do zamknięcia zbioru → 2007 (korekta F1); -8/-9 = brak/nie dotyczy.

NIE liczy parametru Weibulla ani żadnej statystyki testowej — buduje wyłącznie
zbiór odstępów i jego dokumentację źródłową. Kod testu (test6_intervals.py) powstaje
w Etapie B, po przeglądzie (STOP, Krok 1 TASK_6A_RESOLUTION.md).

Wyjścia:
  test6_intervals.csv               — PIERWSZORZĘDNY: po scaleniu, próg na epizodach
  test6_intervals_sensitivity.csv   — wariant wrażliwości: po scaleniu, próg na wierszach surowych
  test6_episodes.csv                — tabela scaleń: każdy epizod i jego składowe konflikty
"""
from __future__ import annotations
import argparse, hashlib, json, itertools, collections
from pathlib import Path

import numpy as np
import pandas as pd
import test0c_build_canonical as bld     # load_cow (obsługa CR), find_input

CLOSE = 2007                             # koniec okna obserwacji (D-003)
MIN_CONFLICTS_A = 3                      # poziom A: diady ≥3 (D-013 §3: liczone na epizodach)


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


def merge_episodes(confs):
    """D-013 §1: konflikty nachodzące się (gap<0) lub stykające (gap=0) → jeden epizod.
    confs posortowane po starcie. Scalanie przechodnie (running max end)."""
    episodes = []
    cur = None
    for s, e, wn, nm in confs:
        if cur is None:
            cur = {"start": s, "end": e, "members": [(s, e, wn, nm)]}
        elif s <= cur["end"]:                       # nachodzi lub styka się (gap<=0)
            cur["end"] = max(cur["end"], e)
            cur["members"].append((s, e, wn, nm))
        else:
            episodes.append(cur)
            cur = {"start": s, "end": e, "members": [(s, e, wn, nm)]}
    if cur is not None:
        episodes.append(cur)
    return episodes


def episode_rows(dname, a, b, episodes):
    """Wiersze tabeli scaleń (§4.1 TASK_6A_RESOLUTION) — jeden wiersz na epizod."""
    rows = []
    for i, ep in enumerate(episodes, start=1):
        scalony = len(ep["members"]) > 1
        skladowe = "; ".join(f"{nm} ({s}-{e})" for s, e, wn, nm in ep["members"])
        rows.append({"diada": dname, "ccode_a": a, "ccode_b": b, "epizod_nr": i,
                     "start": ep["start"], "koniec": ep["end"],
                     "n_skladowych": len(ep["members"]), "scalony": scalony,
                     "skladowe_konflikty": skladowe})
    return rows


def interval_rows_for(dname, a, b, episodes):
    """Odstępy pełne między epizodami + jeden cenzurowany na diadę (D-013 §2, §5).
    Po scaleniu żaden odstęp pełny nie może być niedodatni — assert, nie łatanie."""
    rows = []
    for i in range(len(episodes) - 1):
        e_prev = episodes[i]["end"]
        s_next = episodes[i + 1]["start"]
        gap = s_next - e_prev
        assert gap > 0, (f"BŁĄD IMPLEMENTACJI (D-013 §2): odstęp niedodatni po scaleniu "
                          f"w {dname}: {gap} ({e_prev}->{s_next}). Zgłosić, nie łatać.")
        rows.append({"diada": dname, "ccode_a": a, "ccode_b": b,
                     "rok_konca_poprz": e_prev, "rok_poczatku_nast": s_next,
                     "dlugosc_odstepu": gap,
                     "cenzurowany": 0, "epoka_1914": "przed" if e_prev < 1914 else "po",
                     "epoka_1945": "przed" if e_prev < 1945 else "po", "flag": "ok"})
    e_last = episodes[-1]["end"]
    rows.append({"diada": dname, "ccode_a": a, "ccode_b": b,
                 "rok_konca_poprz": e_last, "rok_poczatku_nast": CLOSE,
                 "dlugosc_odstepu": CLOSE - e_last,
                 "cenzurowany": 1, "epoka_1914": "przed" if e_last < 1914 else "po",
                 "epoka_1945": "przed" if e_last < 1945 else "po", "flag": "ok"})
    return rows


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

    # uniwersum: diady spełniające PIERWOTNY próg surowy (25 diad sprzed D-013) —
    # scalanie nigdy nie zwiększa liczby epizodów, więc diady <3 surowych konfliktów
    # nie mogą osiągnąć progu po scaleniu i są poza uniwersum obu wariantów.
    raw_ge3 = {k: v for k, v in diad_all.items() if len(v) >= MIN_CONFLICTS_A}

    ep_rows, primary_int_rows, sens_int_rows = [], [], []
    dropped = []                          # diady <3 epizody po scaleniu (D-013 §3)
    for (aa, bb), confs in sorted(raw_ge3.items()):
        dname = f"{names.get(aa, aa)}–{names.get(bb, bb)}"
        episodes = merge_episodes(confs)
        ep_rows += episode_rows(dname, aa, bb, episodes)
        ivals = interval_rows_for(dname, aa, bb, episodes)
        sens_int_rows += ivals                                    # próg na wierszach surowych: wszystkie 25
        if len(episodes) >= MIN_CONFLICTS_A:                      # próg na epizodach: D-013 §3
            primary_int_rows += ivals
        else:
            dropped.append({"diada": dname, "n_konfliktow_surowych": len(confs),
                            "n_epizodow_po_scaleniu": len(episodes)})

    ep_tab = pd.DataFrame(ep_rows)
    primary_tab = pd.DataFrame(primary_int_rows)
    sens_tab = pd.DataFrame(sens_int_rows)
    dropped_tab = pd.DataFrame(dropped)

    n_scalonych = int(ep_tab.scalony.sum())
    primary_diads = sorted(primary_tab.diada.unique()) if len(primary_tab) else []
    sens_diads = sorted(sens_tab.diada.unique()) if len(sens_tab) else []

    meta_common = {"builder": "test6_build_intervals.py v2.0 (D-013: scalanie w epizody)",
                   "zrodlo": src.name, "sha256_src": hashlib.sha256(src.read_bytes()).hexdigest()[:16],
                   "diad_>=3_surowych_wierszy": len(raw_ge3), "epizodow_scalonych": n_scalonych,
                   "diady_odrzucone_po_progu_na_epizodach": dropped}

    meta_primary = dict(meta_common, wariant="PIERWSZORZĘDNY — próg ≥3 na epizodach (D-013 §3)",
                        diad=len(primary_diads),
                        odstepy_pelne=int((primary_tab.cenzurowany == 0).sum()) if len(primary_tab) else 0,
                        odstepy_cenzurowane=int((primary_tab.cenzurowany == 1).sum()) if len(primary_tab) else 0,
                        niedodatnich=0)
    with open(od / "test6_intervals.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta_primary, ensure_ascii=False) + "\n")
        primary_tab.to_csv(fh, index=False)

    meta_sens = dict(meta_common, wariant="WRAŻLIWOŚĆ — próg ≥3 na wierszach surowych (D-013 §4, poza §8)",
                     diad=len(sens_diads),
                     odstepy_pelne=int((sens_tab.cenzurowany == 0).sum()),
                     odstepy_cenzurowane=int((sens_tab.cenzurowany == 1).sum()), niedodatnich=0)
    with open(od / "test6_intervals_sensitivity.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta_sens, ensure_ascii=False) + "\n")
        sens_tab.to_csv(fh, index=False)

    with open(od / "test6_episodes.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps({"builder": meta_common["builder"], "opis":
                 "tabela scaleń: jeden wiersz na epizod, D-013 / TASK_6A_RESOLUTION §4.1"},
                 ensure_ascii=False) + "\n")
        ep_tab.to_csv(fh, index=False)

    print(json.dumps({"pierwszorzedny": meta_primary, "wrazliwosc_diad": len(sens_diads),
                      "diady_odrzucone": dropped}, ensure_ascii=False, indent=2))
    print(f"zapisano {od/'test6_intervals.csv'}, {od/'test6_intervals_sensitivity.csv'}, "
          f"{od/'test6_episodes.csv'}")


if __name__ == "__main__":
    main()
