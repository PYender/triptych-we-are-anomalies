#!/usr/bin/env python3
"""
TEST 7 — warstwa danych dla zmiennych objaśniających H9b.2 (D-032, protokół §6).

Buduje WYŁĄCZNIE dane. Żadnej estymacji z udziałem tych zmiennych — D-032: "Code buduje
wyłącznie warstwę danych i nie uruchamia żadnej estymacji z udziałem zmiennych
objaśniających" do czasu, aż autor zadeklaruje kolejność ich wprowadzania.

Cztery zmienne z §6 protokołu, źródła:
  - czas trwania poprzedniego epizodu   — COW inter-state (lata)
  - straty poprzedniego epizodu          — BatDeath, suma po obu stronach DIADY (nie
                                            wszystkich uczestników wojny), logarytm
  - status mocarstwowy                   — majors2016.csv — BRAK W REPO, patrz §X niżej,
                                            zmienna NIEZBUDOWANA (zablokowana brakiem danych)
  - potencjał gospodarczy (CINC)         — COW NMC v7.0 (D-032, patrz uwaga o wersji),
                                            suma i stosunek stron

Zastosowane do obserwacji, które MAJĄ zdefiniowany poprzedni epizod — protokół §6: "Liczone
dla poprzedniego epizodu, więc niedostępne dla t0 i dla diad bez epizodów — te obserwacje
wchodzą do modelu H9b.1, nie do H9b.2." Populacja P2-kwalifikująca się = wiersze `pelny` +
wiersze `cenzurowany` (NIE `cenzurowany_bez_epizodow`, NIE `t0`) z modelu głównego (t0
wyłączone, ucieta wyłączone — D-030/§1b test7_estimate.md).

Rok odniesienia dla CINC: koniec poprzedniego epizodu — konsekwentnie z regułą dla statusu
mocarstwowego ("w roku końca epizodu"), niejawne w tabeli §6 dla CINC, ale przyjęte tu jako
spójna interpretacja, do potwierdzenia.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadr

import test0c_build_canonical as bld
import test6_build_intervals as t6


# ============================ D-032: uwaga o wersji NMC ============================
NMC_VERSION_NOTE = {
    "protokol_oczekuje": "NMC_v6.0 (konczy sie ok. 2016, wg TEST7_PROTOCOL.md SS12)",
    "dostarczone": "COW NMC v7.0 (potwierdzone w dokumentacji zrodlowej peacesciencer, "
                   "data-raw/cow_nmc.R + man/cow_nmc.Rd: \"These are version 7.0\")",
    "zrodlo": "svmiller/peacesciencer, commit fe150a2648056fbd4fbbbd833f0c9e437b2ed04b "
             "(TEN SAM commit co tss_rivalries.rda), plik data/cow_nmc.rda",
    "sha256": None,  # uzupełniane w main()
    "konsekwencja_dla_okna_do_2007": (
        "NIEZNANA co do wielkosci, nie zalatana po cichu. v6.0 vs v7.0 moga sie roznic nie "
        "tylko zasiegiem lat (2016 vs 2022), ale tez rewizjami wartosci historycznych CINC "
        "wewnatrz okna 1816-2007 - dokumentacja NMC ostrzega wprost o niespojnosciach nawet "
        "w ramach jednej wersji (np. suma CINC != 1 w wiekszosci lat). Nie mam v6.0 do "
        "bezposredniego porownania. UZYWAM v7.0, bo to jedyna wersja dostepna przez wskazany "
        "kanal (D-032) - jawnie oznaczone, nie ciche podstawienie. Zero brakow w cinc w oknie "
        "1816-2007 (sprawdzone bezposrednio), wiec przynajmniej KOMPLETNOSC nie jest problemem."
    ),
}


def load_nmc(dd: Path):
    src = dd / "cow_nmc.rda"
    if not src.exists():
        hits = list(dd.rglob("cow_nmc.rda"))
        if len(hits) != 1:
            raise FileNotFoundError(f"cow_nmc.rda nie znalezione jednoznacznie w {dd}: {hits}")
        src = hits[0]
    obj = pyreadr.read_r(str(src))
    df = list(obj.values())[0]
    return df, src


def build_diad_episodes(dd: Path):
    """Ta sama konstrukcja co test7_build_windows.py: wszystkie diady, wszystkie epizody,
    bez progu (zakaz nr 2) — zwraca {(ccode_a,ccode_b): [epizod,...]} posortowane rosnąco
    po ccode, epizod = {"start","end","members":[(s,e,wn,nm),...]}."""
    war_src = bld.find_input(dd, "InterStateWarData_v4_0.csv")
    wdf = bld.load_cow(war_src)
    wars, _ = t6.war_spans(wdf)
    diad_all = t6.build_diads(wars)
    out = {}
    for (a, b), confs in diad_all.items():
        out[(a, b)] = t6.merge_episodes(confs)
    return out, war_src, wdf


def batdeath_for_episode(wdf: pd.DataFrame, members, a: int, b: int):
    """Suma BatDeath po OBU stronach DIADY (a,b) dla konfliktów składowych epizodu —
    protokół §6: 'suma po obu stronach danej diady, z wyłączeniem uczestników spoza pary'.
    BatDeath==-9 (sentinel COW) traktowane jako brak, nie zero."""
    total, any_missing, any_found = 0.0, False, False
    for s, e, wn, nm in members:
        rows = wdf[(wdf["WarNum"] == wn) & (wdf["ccode"].isin([a, b]))]
        if rows.empty:
            continue
        any_found = True
        bd = pd.to_numeric(rows["BatDeath"], errors="coerce")
        if (bd < 0).any():
            any_missing = True
        bd = bd.where(bd >= 0)
        if bd.notna().any():
            total += float(bd.sum())
    if not any_found:
        return None, "brak_dopasowania_WarNum"
    if any_missing and total == 0.0:
        return None, "wszystkie_wartosci_sentinel(-9)"
    return total, ("czesciowo_brak(-9)_pominiete" if any_missing else "ok")


def cinc_for_year(nmc: pd.DataFrame, ccode: int, year: int):
    row = nmc[(nmc["ccode"] == ccode) & (nmc["year"] == year)]
    if row.empty:
        return None
    return float(row["cinc"].iloc[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--intervals", default="test7_intervals.csv")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    dd, od = Path(a.data_dir), Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)

    nmc, nmc_src = load_nmc(dd)
    NMC_VERSION_NOTE["sha256"] = hashlib.sha256(nmc_src.read_bytes()).hexdigest()
    assert NMC_VERSION_NOTE["sha256"].startswith("c265ab4f"), \
        f"suma kontrolna cow_nmc.rda nie zgadza się z D-032: {NMC_VERSION_NOTE['sha256'][:16]}"

    diad_episodes, war_src, wdf = build_diad_episodes(dd)

    df = pd.read_csv(a.intervals, comment="#")
    main_model = df[(df["t0_flag"] == 0) & (df["ucieta"] == 0)]
    n_main_before = len(df)
    n_main_after_t0_ucieta = len(main_model)

    p2_rows = main_model[main_model["typ"].isin(["pelny", "cenzurowany"])].copy()
    n_p2_candidate = len(p2_rows)

    out_rows = []
    diady_z_p2_wierszem = set()
    diady_pelne_pokrycie = {"czas_trwania": set(), "straty": set(), "cinc": set()}
    diady_wszystkie_z_p2 = set()

    for r in p2_rows.itertuples():
        key = (int(r.ccode_a), int(r.ccode_b))
        episodes = diad_episodes.get(key, [])
        prev_ep = next((ep for ep in episodes if ep["end"] == r.rok_start), None)
        diady_wszystkie_z_p2.add(r.diada)
        row = dict(diada=r.diada, ccode_a=r.ccode_a, ccode_b=r.ccode_b, typ=r.typ,
                   rok_start=r.rok_start, rok_koniec=r.rok_koniec)
        if prev_ep is None:
            row.update(epizod_dopasowany=False, czas_trwania=None, straty_batdeath=None,
                      straty_log=None, straty_status="brak_dopasowania_epizodu",
                      cinc_a=None, cinc_b=None, cinc_suma=None, cinc_stosunek=None)
            out_rows.append(row)
            continue

        diady_z_p2_wierszem.add(r.diada)
        dur = prev_ep["end"] - prev_ep["start"]
        bd, bd_status = batdeath_for_episode(wdf, prev_ep["members"], key[0], key[1])
        cinc_a = cinc_for_year(nmc, key[0], prev_ep["end"])
        cinc_b = cinc_for_year(nmc, key[1], prev_ep["end"])
        cinc_sum = (cinc_a + cinc_b) if (cinc_a is not None and cinc_b is not None) else None
        cinc_ratio = (cinc_a / cinc_b) if (cinc_a is not None and cinc_b not in (None, 0)) else None

        row.update(epizod_dopasowany=True, epizod_start=prev_ep["start"], epizod_koniec=prev_ep["end"],
                   czas_trwania=dur, straty_batdeath=bd,
                   straty_log=(np.log(bd) if (bd is not None and bd > 0) else None),
                   straty_status=bd_status, cinc_a=cinc_a, cinc_b=cinc_b,
                   cinc_suma=cinc_sum, cinc_stosunek=cinc_ratio)
        out_rows.append(row)

        if dur is not None:
            diady_pelne_pokrycie["czas_trwania"].add(r.diada)
        if bd is not None:
            diady_pelne_pokrycie["straty"].add(r.diada)
        if cinc_sum is not None:
            diady_pelne_pokrycie["cinc"].add(r.diada)

    out_tab = pd.DataFrame(out_rows)

    # pelne pokrycie diady = wszystkie jej wiersze P2 maja wartosc (nie tylko czesc)
    def full_coverage(varcol):
        ok = set()
        for d, g in out_tab.groupby("diada"):
            if g[varcol].notna().all() and len(g) > 0:
                ok.add(d)
        return ok

    coverage = {
        "czas_trwania_pelne_pokrycie_diad": len(full_coverage("czas_trwania")),
        "straty_pelne_pokrycie_diad": len(full_coverage("straty_batdeath")),
        "cinc_pelne_pokrycie_diad": len(full_coverage("cinc_suma")),
        "status_mocarstwowy_pelne_pokrycie_diad": 0,  # zablokowane, patrz meta
    }

    meta = {
        "builder": "test7_build_p2_variables.py v1.0 (D-032)",
        "zrodlo_nmc": nmc_src.name, "sha256_nmc": NMC_VERSION_NOTE["sha256"][:16],
        "nmc_wersja": NMC_VERSION_NOTE,
        "zrodlo_wojny": war_src.name, "sha256_wojny": hashlib.sha256(war_src.read_bytes()).hexdigest()[:16],
        "status_mocarstwowy": "NIEZBUDOWANE - majors2016.csv brak w repo (protokol SS12 twierdzi "
                              "'w repo', ale plik nie istnieje - sprawdzone bezposrednio); "
                              "zmienna nie liczona, kolumna nieobecna w wyjsciu",
        "liczby_wierszy_D028": {
            "model_glowny_wszystkie_wiersze_przed_filtrowaniem_typu": n_main_before,
            "model_glowny_po_t0_ucieta": n_main_after_t0_ucieta,
            "P2_kandydujace_wiersze_pelny_plus_cenzurowany": n_p2_candidate,
            "P2_z_dopasowanym_epizodem": len(out_tab[out_tab["epizod_dopasowany"]]),
            "P2_bez_dopasowanego_epizodu": len(out_tab[~out_tab["epizod_dopasowany"]]),
        },
        "pokrycie_diad_101": coverage,
        "n_diad_z_jakimkolwiek_wierszem_P2": len(diady_wszystkie_z_p2),
    }

    with open(od / "test7_p2_variables.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        out_tab.to_csv(fh, index=False)

    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"zapisano test7_p2_variables.csv w {od}")


if __name__ == "__main__":
    main()
