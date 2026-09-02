#!/usr/bin/env python3
"""
TEST 7 — warstwa danych P2a/P2b (D-034, zastępuje D-032 §4).

Dwa modele, dwie populacje, jak w D-034 §1 (cytat z tabeli):
  P2a: cinc, status mocarstwowy | 132 wiersze, 101 diad (pełna populacja, wraz z parami
       bez żadnej wojny) | ORZEKA dla H9b.2 (D-034 §2)
  P2b: czas trwania poprzedniego epizodu, straty w poprzednim epizodzie | 77 wierszy,
       46 diad (wyłącznie pary, które już walczyły) | OPISOWY, poza regułą decyzyjną

P2a: cinc/status liczone w roku ROZPOCZĘCIA obserwowanego odstępu (`rok_start`) — jedyny rok
odniesienia wspólny dla WSZYSTKICH 132 wierszy, w tym `cenzurowany_bez_epizodow` (gdzie
`rok_start` = otwarcie okna, bo nie ma poprzedniego epizodu). Zmienne P2a nie wymagają
poprzedniego epizodu (D-034 §1: "określone dla każdej pary i każdego roku"), w
przeciwieństwie do P2b.

P2b: identyczne jak poprzednia wersja `test7_build_p2_variables.py` (D-033) dla dwóch
zmiennych opartych na poprzednim epizodzie — ten plik NIE zawiera już cinc/status (rozdzielone
do P2a, D-034 §1), żeby uniknąć dwuznaczności, które zmienne należą do którego modelu.

Status mocarstwowy: `cow_majors.rda` (D-034 — podmiana źródła majors2016.csv, ten sam
archiwum peacesciencer, ten sam commit co NMC/rywalizacje), zapisana jako niezgodność z
§12 protokołu identycznie jak przy NMC (D-033).

ŻADNA ESTYMACJA nie jest tu uruchamiana — wyłącznie warstwa danych (D-032 §4 / D-034 §3).
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadr

import test0c_build_canonical as bld
import test6_build_intervals as t6


MAJORS_VERSION_NOTE = {
    "protokol_oczekuje": "majors2016.csv, w repo (TEST7_PROTOCOL.md SS12)",
    "rzeczywistosc": "plik nie istnieje w repozytorium (sprawdzone bezposrednio, D-033)",
    "dostarczone_D034": "cow_majors.rda z svmiller/peacesciencer, ten sam commit co NMC/"
                        "rywalizacje (fe150a2648056fbd4fbbbd833f0c9e437b2ed04b)",
    "zgodnosc_tresci": "14 wierszy, pole version=2016 na wszystkich wierszach - trescia "
                       "zgodne z majors2016.csv (nazwa pliku inna, zawartosc ta sama wersja)",
    "niezgodnosc_z_SS12": "niezgodnosc NAZWY/SCIEZKI zrodla (protokol oczekuje pliku "
                          "majors2016.csv 'w repo', dostarczono cow_majors.rda z zewnetrznego "
                          "archiwum) - odnotowana identycznie jak przy NMC (D-033), nie "
                          "podmieniona po cichu. Tresciowo (version=2016) BEZ rozbieznosci.",
}


def load_rda_single(path: Path):
    obj = pyreadr.read_r(str(path))
    return list(obj.values())[0]


def is_major(majors: pd.DataFrame, ccode: int, year: int) -> bool:
    rows = majors[majors["ccode"] == ccode]
    for r in rows.itertuples():
        if r.styear <= year <= r.endyear:
            return True
    return False


def cinc_lookup(nmc: pd.DataFrame, ccode: int, year: int):
    row = nmc[(nmc["ccode"] == ccode) & (nmc["year"] == year)]
    return float(row["cinc"].iloc[0]) if not row.empty else None


def build_diad_episodes(dd: Path):
    war_src = bld.find_input(dd, "InterStateWarData_v4_0.csv")
    wdf = bld.load_cow(war_src)
    wars, _ = t6.war_spans(wdf)
    diad_all = t6.build_diads(wars)
    return {k: t6.merge_episodes(v) for k, v in diad_all.items()}, war_src, wdf


def batdeath_for_episode(wdf: pd.DataFrame, members, a: int, b: int):
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


def build_p2a(main_model: pd.DataFrame, nmc: pd.DataFrame, majors: pd.DataFrame):
    rows = []
    for r in main_model.itertuples():
        a, b, yr = int(r.ccode_a), int(r.ccode_b), int(r.rok_start)
        cinc_a, cinc_b = cinc_lookup(nmc, a, yr), cinc_lookup(nmc, b, yr)
        cinc_sum = (cinc_a + cinc_b) if (cinc_a is not None and cinc_b is not None) else None
        cinc_ratio = (cinc_a / cinc_b) if (cinc_a is not None and cinc_b not in (None, 0)) else None
        maj_a, maj_b = is_major(majors, a, yr), is_major(majors, b, yr)
        status = int(maj_a) + int(maj_b)
        rows.append(dict(diada=r.diada, ccode_a=a, ccode_b=b, typ=r.typ, rok_odniesienia=yr,
                         cinc_a=cinc_a, cinc_b=cinc_b, cinc_suma=cinc_sum, cinc_stosunek=cinc_ratio,
                         major_a=maj_a, major_b=maj_b, status_mocarstwowy=status))
    return pd.DataFrame(rows)


def build_p2b(main_model: pd.DataFrame, diad_episodes, wdf: pd.DataFrame):
    p2_rows = main_model[main_model["typ"].isin(["pelny", "cenzurowany"])]
    rows = []
    for r in p2_rows.itertuples():
        key = (int(r.ccode_a), int(r.ccode_b))
        episodes = diad_episodes.get(key, [])
        prev_ep = next((ep for ep in episodes if ep["end"] == r.rok_start), None)
        row = dict(diada=r.diada, ccode_a=key[0], ccode_b=key[1], typ=r.typ,
                   rok_start=r.rok_start, rok_koniec=r.rok_koniec)
        if prev_ep is None:
            row.update(epizod_dopasowany=False, czas_trwania=None, straty_batdeath=None,
                      straty_log=None, straty_status="brak_dopasowania_epizodu")
            rows.append(row)
            continue
        dur = prev_ep["end"] - prev_ep["start"]
        bd, bd_status = batdeath_for_episode(wdf, prev_ep["members"], key[0], key[1])
        row.update(epizod_dopasowany=True, epizod_start=prev_ep["start"], epizod_koniec=prev_ep["end"],
                   czas_trwania=dur, straty_batdeath=bd,
                   straty_log=(np.log(bd) if (bd is not None and bd > 0) else None),
                   straty_status=bd_status)
        rows.append(row)
    return pd.DataFrame(rows)


def full_coverage_diads(tab: pd.DataFrame, col: str):
    ok = set()
    for d, g in tab.groupby("diada"):
        if len(g) > 0 and g[col].notna().all():
            ok.add(d)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--intervals", default="test7_intervals.csv")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    dd, od = Path(a.data_dir), Path(a.out_dir)

    nmc_path = dd / "rivalries" / "cow_nmc.rda"
    majors_path = dd / "rivalries" / "cow_majors.rda"
    nmc = load_rda_single(nmc_path)
    majors = load_rda_single(majors_path)
    sha_nmc = hashlib.sha256(nmc_path.read_bytes()).hexdigest()
    sha_majors = hashlib.sha256(majors_path.read_bytes()).hexdigest()
    assert sha_nmc.startswith("c265ab4f"), sha_nmc[:16]
    assert sha_majors.startswith("673cb752"), sha_majors[:16]

    diad_episodes, war_src, wdf = build_diad_episodes(dd)

    df = pd.read_csv(a.intervals, comment="#")
    main_model = df[(df["t0_flag"] == 0) & (df["ucieta"] == 0)].copy()
    n_main = len(main_model)
    n_diad_main = main_model["diada"].nunique()

    p2a = build_p2a(main_model, nmc, majors)
    p2b = build_p2b(main_model, diad_episodes, wdf)

    # rozbior 132 -> 77 (D-034 zadanie): ile zdarzen (pelny) i cenzurowanych zostaje w P2b
    p2b_pelny = int((p2b["typ"] == "pelny").sum())
    p2b_cens = int((p2b["typ"] == "cenzurowany").sum())
    n_full_main_model = int((main_model["typ"] == "pelny").sum())

    meta = {
        "builder": "test7_build_p2ab_variables.py v1.0 (D-034)",
        "sha256_nmc": sha_nmc[:16], "sha256_majors": sha_majors[:16],
        "majors_wersja": MAJORS_VERSION_NOTE,
        "liczby_wierszy_D028": {
            "model_glowny_wiersze": n_main, "model_glowny_diady": n_diad_main,
            "P2a_wiersze": len(p2a), "P2a_diady": p2a["diada"].nunique(),
            "P2b_wiersze": len(p2b), "P2b_diady": p2b["diada"].nunique(),
            "rozbior_132_na_77": {
                "razem_w_P2b": len(p2b),
                "typ_pelny_w_P2b": p2b_pelny,
                "typ_cenzurowany_w_P2b": p2b_cens,
                "wszystkie_zdarzenia_pelne_modelu_glownego": n_full_main_model,
                "wszystkie_37_zdarzen_przetrwaly": bool(p2b_pelny == n_full_main_model),
            },
        },
        "pokrycie": {
            "cinc_suma_diady_pelne_pokrycie_z_101": len(full_coverage_diads(p2a, "cinc_suma")),
            "status_mocarstwowy_diady_pelne_pokrycie_z_101": len(full_coverage_diads(p2a, "status_mocarstwowy")),
            "czas_trwania_diady_pelne_pokrycie_z_46": len(full_coverage_diads(p2b, "czas_trwania")),
            "straty_diady_pelne_pokrycie_z_46": len(full_coverage_diads(p2b, "straty_batdeath")),
        },
    }

    with open(od / "test7_p2a_variables.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n"); p2a.to_csv(fh, index=False)
    with open(od / "test7_p2b_variables.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n"); p2b.to_csv(fh, index=False)

    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print("zapisano test7_p2a_variables.csv, test7_p2b_variables.csv")


if __name__ == "__main__":
    main()
