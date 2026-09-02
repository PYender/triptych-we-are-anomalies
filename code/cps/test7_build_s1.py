#!/usr/bin/env python3
"""
TEST 7 — S1: wariant wrażliwości bez epizodów obejmujących wojny światowe (D-035, protokół §7/§8).

Mechanizm (Claude, wiadomość po D-035): lata epizodu wojny światowej traktowane jak czas
POZA OKNEM RYZYKA — dokładnie tym samym mechanizmem, którym `test7_build_windows.py` już
obsługuje przerwę między okresami rywalizacji (np. Chiny–Japonia, przerwa 1945–1996 między
dwoma rozłącznymi okresami rywalizacji tej diady). Odstęp biegnący ku wojnie domyka się jako
CENZUROWANY w chwili jej wybuchu (rok startu epizodu); po zakończeniu epizodu otwiera się
nowe okno i zaczyna nowy odstęp (od roku końca epizodu).

Kryterium usunięcia (D-035, dosłownie): epizod, którego przedział trwania PRZECINA lata
1914–1918 albo 1939–1945 — przecięcie, nie zawieranie. Epizod 1937–1945 też wypada w
całości (jako jeden, nierozdzielny epizod scalony D-013).

Implementacja: `periods` diady (z `test7_build_windows.build_windows`) są przycinane —
`[epizod.start, epizod.end]` wycięte z każdego pokrywającego się okresu, dokładnie jak
istniejąca przerwa między okresami rywalizacji (brak jakiegokolwiek nowego mechanizmu w
`classify_events`/`diad_rows`/`exposure_multi` — te funkcje REUŻYTE bez zmian z
`test7_build_windows.py`, tylko nakarmione już przyciętymi `periods` i `episodes` z
usuniętymi epizodami dyskwalifikującymi). Diady bez żadnego epizodu przecinającego wojny
światowe są w S1 IDENTYCZNE jak w P1 — sprawdzane wprost jako test spójności.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import pandas as pd

import test0c_build_canonical as bld
import test6_build_intervals as t6
import test7_build_windows as w7

WWI = (1914, 1918)
WWII = (1939, 1945)


def intersects(ep_start, ep_end, lo, hi):
    return ep_start <= hi and ep_end >= lo


def disqualifying(episodes):
    """Epizody, których przedział PRZECINA (nie: zawiera się w) 1914-18 albo 1939-45."""
    return [ep for ep in episodes
           if intersects(ep["start"], ep["end"], *WWI) or intersects(ep["start"], ep["end"], *WWII)]


def carve_out(periods, excluded_spans):
    """Wycina [es,ee] z każdego okresu pokrywającego się z tym przedziałem — dokładnie
    ten sam efekt co naturalna przerwa między dwoma rozłącznymi okresami rywalizacji
    (Chiny-Japonia). Lewa część zamyka się NA es (odstęp domyka się w chwili wybuchu wojny,
    D-035); prawa część otwiera się OD ee (nowe okno od końca epizodu, ta sama konwencja
    co Skutek B D-021: `new_open = ep["end"]`)."""
    result = [dict(p) for p in periods]
    for es, ee in excluded_spans:
        nxt = []
        for p in result:
            if ee < p["t0"] or es > p["t1"]:
                nxt.append(p)
                continue
            if p["t0"] < es:
                left = dict(p); left["t1"] = es
                if left["t1"] > left["t0"]:
                    nxt.append(left)
            if p["t1"] > ee:
                right = dict(p); right["t0"] = ee
                if right["t1"] > right["t0"]:
                    nxt.append(right)
        result = nxt
    return sorted(result, key=lambda p: p["t0"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--p1-intervals", default="test7_intervals.csv",
                    help="P1 dla porownania liczb zdarzen/cenzurowanych i testu spojnosci na diadach bez wojny")
    args = ap.parse_args()
    dd, od = Path(args.data_dir), Path(args.out_dir); od.mkdir(parents=True, exist_ok=True)

    tss, tss_src = w7.load_rivalries(dd, "tss_rivalries.rda")
    diad_periods = w7.spatial_diad_periods(tss)
    mem, mem_src = t6.load_membership(dd)
    entry, exitr = w7.entry_exit_years(mem)
    windows = w7.build_windows(diad_periods, mem, entry, exitr)

    war_src = bld.find_input(dd, "InterStateWarData_v4_0.csv")
    wdf = bld.load_cow(war_src)
    names = dict(zip(pd.to_numeric(wdf.ccode, errors="coerce").dropna().astype(int), wdf.StateName))
    abbrev = dict(zip(pd.read_csv(mem_src)["ccode"], pd.read_csv(mem_src)["stateabb"]))

    def nm(cc):
        return names.get(cc) or abbrev.get(cc) or str(cc)

    wars, _ = t6.war_spans(wdf)
    diad_all = t6.build_diads(wars)

    win_rows, int_rows, excluded_rows = [], [], []
    diady_dotkniete, epizody_wypadle, diady_okno_pochloniete = set(), [], []

    for (a, b), periods in sorted(windows.items()):
        dname = f"{nm(a)}–{nm(b)}"
        confs = diad_all.get((a, b), [])
        all_episodes = [{"start": ep["start"], "end": ep["end"],
                         "name": "; ".join(m[3] for m in ep["members"])}
                        for ep in t6.merge_episodes(confs)]
        disq = disqualifying(all_episodes)
        if disq:
            diady_dotkniete.add(dname)
            for ep in disq:
                epizody_wypadle.append({"diada": dname, "start": ep["start"], "end": ep["end"],
                                        "nazwa": ep["name"]})
            spans = [(ep["start"], ep["end"]) for ep in disq]
            periods_s1 = carve_out(periods, spans)
            episodes_s1 = [ep for ep in all_episodes if ep not in disq]
        else:
            periods_s1 = periods
            episodes_s1 = all_episodes

        if not periods_s1:
            # cale okno diady pochloniete przez wykluczony epizod (rzadkie — diada
            # istniala w rywalizacji tylko w czasie wojny swiatowej) — diada wypada z S1,
            # analogicznie do diad odrzucanych z powodu pustego okna w P1
            diady_okno_pochloniete.append(dname)
            continue

        rows, shifted, periods_adj, excluded = w7.diad_rows(dname, a, b, periods_s1, episodes_s1, mem)
        int_rows += rows
        excluded_rows += excluded
        for p in periods_adj:
            win_rows.append({"diada": dname, "ccode_a": a, "ccode_b": b, **p})

    AUTORYZOWANE_D025 = {"Italy–Ethiopia", "Ethiopia–Italy"}
    nieautoryzowane = [e for e in excluded_rows if e["diada"] not in AUTORYZOWANE_D025]
    if nieautoryzowane:
        raise AssertionError(
            "S1: nowy, nieautoryzowany przypadek ekspozycji<=0 poza Italy-Ethiopia: "
            f"{nieautoryzowane}. Zgłosić do decyzji, nie wykluczać po cichu.")

    int_tab = pd.DataFrame(int_rows)

    # test spojnosci: diady BEZ epizodu dyskwalifikujacego musza byc identyczne z P1
    p1 = pd.read_csv(args.p1_intervals, comment="#")
    cols_cmp = ["diada", "ccode_a", "ccode_b", "typ", "rok_start", "rok_koniec", "ekspozycja",
               "cenzurowany", "t0_flag", "ucieta"]
    niedotkniete = sorted(set(int_tab["diada"]) - diady_dotkniete)
    p1_niedotkniete = p1[p1["diada"].isin(niedotkniete)][cols_cmp].sort_values(cols_cmp).reset_index(drop=True)
    s1_niedotkniete = int_tab[int_tab["diada"].isin(niedotkniete)][cols_cmp].sort_values(cols_cmp).reset_index(drop=True)
    identyczne = p1_niedotkniete.equals(s1_niedotkniete)

    # liczby S1 vs P1 (t0/ucieta wykluczone, model glowny, D-028)
    def main_counts(df):
        m = df[(df["t0_flag"] == 0) & (df["ucieta"] == 0)]
        return dict(wiersze=len(m), pelne=int((m["typ"] == "pelny").sum()),
                   cenzurowane=int((m["typ"].isin(["cenzurowany", "cenzurowany_bez_epizodow"])).sum()),
                   diady=m["diada"].nunique())

    p1_counts = main_counts(p1)
    s1_counts = main_counts(int_tab)

    meta = {
        "builder": "test7_build_s1.py v1.0 (D-035)",
        "epizody_wypadle_n": len(epizody_wypadle),
        "diady_dotkniete_n": len(diady_dotkniete),
        "diady_dotkniete": sorted(diady_dotkniete),
        "epizody_wypadle": epizody_wypadle,
        "diady_okno_calkowicie_pochloniete_przez_wojne": diady_okno_pochloniete,
        "test_spojnosci_diady_niedotkniete_identyczne_z_P1": bool(identyczne),
        "n_diady_niedotkniete_porownane": len(niedotkniete),
        "P1_model_glowny": p1_counts,
        "S1_model_glowny": s1_counts,
        "kierunek_zgodny_z_D035_SS3": bool(s1_counts["pelne"] <= p1_counts["pelne"]
                                          and s1_counts["cenzurowane"] >= p1_counts["cenzurowane"]),
    }

    with open(od / "test7_s1_windows.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        pd.DataFrame(win_rows).to_csv(fh, index=False)
    with open(od / "test7_s1_intervals.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        int_tab.to_csv(fh, index=False)

    print(json.dumps(meta, ensure_ascii=False, indent=2, default=str))
    print("zapisano test7_s1_windows.csv, test7_s1_intervals.csv")


if __name__ == "__main__":
    main()
