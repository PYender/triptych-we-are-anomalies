#!/usr/bin/env python3
"""
S7b/S7c — zegar inicjacji / kontrola negatywna (D-046).

UJAWNIENIE (D-046, powtórzone tutaj w kodzie): S7b powstał PO zobaczeniu wyniku S7
(k̂=0,9947, oba przedziały objęły 1) — NIE jest pre-rejestrowany. Argumenty za i przeciw
temu, czy to dobieranie narzędzia pod tezę, zapisane w D-046, nie tutaj.

Konstrukcja: identyczna z S7 (`test6_build_s7.py` — `state_conflicts`, `build`, `summarize`
REUŻYTE bez zmian), z JEDNĄ zmianą: do sekwencji epizodów państwa wchodzą wyłącznie wiersze
`InterStateWarData_v4_0.csv` o określonej wartości `Initiator` (S7b: ==1, państwo było
inicjatorem; S7c: ==2, państwo NIE było inicjatorem — kontrola negatywna). Scalanie gap≤0
(D-039), reguła WarNum (D-040), ekspozycja (D-014), cenzurowanie do 2007 — wszystko bez
zmian względem S7.

Próg: TRZY epizody (nie sześć) dla obu wariantów — odstępstwo od poziomu B protokołu Testu 6,
zadeklarowane i uzasadnione w D-046 (moc przy progu 6 gorsza niż Test 7). Oba progi (3 i 6)
liczone i raportowane, próg 3 orzeka.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import pandas as pd

import test0c_build_canonical as bld
import test6_build_intervals as t6
import test6_build_s7 as s7

MIN_EPISODES_DECIDING = 3
MIN_EPISODES_ALT = 6


def build_variant(df_filtered, mem, entry, exitr, names, label):
    ep3, int3, dropped3 = s7.build(df_filtered, mem, entry, exitr, names, MIN_EPISODES_DECIDING)
    ep6, int6, dropped6 = s7.build(df_filtered, mem, entry, exitr, names, MIN_EPISODES_ALT)
    return dict(label=label, ep3=ep3, int3=int3, ep6=ep6, int6=int6,
               podsumowanie_prog3=s7.summarize(int3), podsumowanie_prog6=s7.summarize(int6))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out-dir", default=".")
    args = ap.parse_args()
    dd, od = Path(args.data_dir), Path(args.out_dir); od.mkdir(parents=True, exist_ok=True)

    src = bld.find_input(dd, "InterStateWarData_v4_0.csv")
    df = bld.load_cow(src)
    df["Initiator"] = pd.to_numeric(df["Initiator"], errors="coerce")
    names = dict(zip(pd.to_numeric(df.ccode, errors="coerce").dropna().astype(int), df.StateName))
    mem, mem_src = t6.load_membership(dd)
    entry = {cc: min(ys) for cc, ys in mem.items()}
    exitr = {cc: max(ys) for cc, ys in mem.items()}

    df_s7b = df[df.Initiator == 1].copy()
    df_s7c = df[df.Initiator == 2].copy()

    res_b = build_variant(df_s7b, mem, entry, exitr, names, "S7b (zegar inicjacji, Initiator==1)")
    res_c = build_variant(df_s7c, mem, entry, exitr, names, "S7c (kontrola negatywna, Initiator==2)")

    # fakt do raportu (D-046): liczba inicjacji per panstwo, cala baza, bez progu/scalania
    init_counts = (df[df.Initiator == 1].drop_duplicates(subset=["ccode", "WarNum"])
                  .groupby("ccode").size().sort_values(ascending=False))
    top_inicjatorzy = [{"ccode": int(cc), "panstwo": names.get(int(cc), int(cc)), "n_wojen_zainicjowanych": int(n)}
                       for cc, n in init_counts.head(10).items()]

    meta = {
        "builder": "test6_build_s7bc.py v1.0 (D-046)",
        "zrodlo_wojny": src.name, "sha256_wojny": hashlib.sha256(src.read_bytes()).hexdigest()[:16],
        "top10_inicjatorow_cala_baza_bez_progu": top_inicjatorzy,
        "fakt_autora_do_weryfikacji": {
            "twierdzenie": "Rosja 10, Francja 8, USA/Japonia/Wlochy/Niemcy po 7",
            "policzone": "Rosja(365)=10, Francja(220)=8, USA(2)=7, Japonia(740)=7, "
                        "Wlochy(325)=6 (NIE 7), Niemcy(255)=5 (NIE 7)",
            "rozbieznosc": "TAK dla Wloch i Niemiec - zgloszona, nie dopasowana, patrz raport",
        },
        "S7b": {
            "prog3_decyduje": res_b["podsumowanie_prog3"],
            "prog6_alternatywny": res_b["podsumowanie_prog6"],
        },
        "S7c": {
            "prog3_decyduje": res_c["podsumowanie_prog3"],
            "prog6_alternatywny": res_c["podsumowanie_prog6"],
        },
    }

    for tag, res in (("s7b", res_b), ("s7c", res_c)):
        with open(od / f"test6_{tag}_prog3_episodes.csv", "w", encoding="utf-8") as fh:
            fh.write("# " + json.dumps(meta, ensure_ascii=False, default=str) + "\n")
            res["ep3"].to_csv(fh, index=False)
        with open(od / f"test6_{tag}_prog3_intervals.csv", "w", encoding="utf-8") as fh:
            fh.write("# " + json.dumps(meta, ensure_ascii=False, default=str) + "\n")
            res["int3"].to_csv(fh, index=False)
        with open(od / f"test6_{tag}_prog6_intervals.csv", "w", encoding="utf-8") as fh:
            fh.write("# " + json.dumps(meta, ensure_ascii=False, default=str) + "\n")
            res["int6"].to_csv(fh, index=False)

    print(json.dumps(meta, ensure_ascii=False, indent=2, default=str))
    print("zapisano test6_s7b_prog3_{episodes,intervals}.csv, test6_s7b_prog6_intervals.csv, "
         "test6_s7c_prog3_{episodes,intervals}.csv, test6_s7c_prog6_intervals.csv")


if __name__ == "__main__":
    main()
