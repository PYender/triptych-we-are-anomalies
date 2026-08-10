#!/usr/bin/env python3
"""
Konwersja cache'u Google Books N-grams (_pkl/*.pkl) na przenośne tabele CSV.

Powód: pickle jest zależny od wersji bibliotek i niebezpieczny przy wczytywaniu
z obcego źródła, więc nie nadaje się do repozytorium publicznego. Te same dane
w CSV mają ~200 kB i są czytelne dla każdego — a zastępują 3,1 GB plików .gz
w zakresie potrzebnym do odtworzenia indeksu COLOR.

Struktura każdego pliku `<litera>.pkl` (zgodnie z linią 113
analiza_poprawiona_final_GDELT.py):

    (counts, wordcnt)
      counts  : {rok: łączna liczba tokenów tej litery w tym roku}
      wordcnt : {rok: {słowo: licznik}}  — tylko słowa z list RED/BLUE

Wyjście:
    ngram_letter_year_totals.csv   litera, rok, tokeny_litery
    ngram_word_year_counts.csv     litera, słowo, rok, licznik
    ngram_year_totals.csv          rok, tokeny_globalne  (suma po literach)
    ngram_color_rebuilt.csv        rok, red, blue, color (odtworzony indeks)

Uruchomienie:
    python pkl_to_csv.py --pkl-dir "C:/sciezka/do/_pkl" --out-dir .
    python pkl_to_csv.py --pkl-dir ./_pkl --verify wars_color.csv
"""
from __future__ import annotations
import argparse, pickle, sys
from pathlib import Path

import pandas as pd

RED_WORDS = ["war", "enemy", "conquer", "attack", "strike", "dominate",
             "battle", "conflict", "invasion", "hostility"]
BLUE_WORDS = ["peace", "trust", "cooperation", "cultivate", "innovate",
              "harmony", "diplomacy", "alliance", "treaty", "reconciliation"]


def load_pkl(path: Path):
    """Zwraca (counts, wordcnt). Odporne na to, czy zapisano dict, defaultdict
    czy Counter — wszystkie zachowują się tak samo przy odczycie."""
    with path.open("rb") as fh:
        obj = pickle.load(fh)
    if not (isinstance(obj, tuple) and len(obj) == 2):
        raise ValueError(f"{path.name}: oczekiwano krotki (counts, wordcnt), "
                         f"jest {type(obj).__name__}")
    return obj[0], obj[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl-dir", required=True, help="katalog _pkl")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--verify", default=None,
                    help="opcjonalnie: wars_color.csv do porównania kolumny color")
    a = ap.parse_args()

    pkl_dir, out = Path(a.pkl_dir), Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    files = sorted(pkl_dir.glob("*.pkl"))
    if not files:
        print(f"BŁĄD: brak plików .pkl w {pkl_dir}", file=sys.stderr)
        return 1

    tot_rows, word_rows = [], []
    for f in files:
        letter = f.stem.lower()
        counts, wordcnt = load_pkl(f)
        for yr, n in counts.items():
            tot_rows.append({"letter": letter, "year": int(yr), "letter_tokens": int(n)})
        for yr, words in wordcnt.items():
            for w, n in words.items():
                word_rows.append({"letter": letter, "word": w,
                                  "year": int(yr), "count": int(n)})
        print(f"  {letter}: {len(counts)} lat, "
              f"{sum(len(v) for v in wordcnt.values())} par słowo-rok")

    totals = pd.DataFrame(tot_rows).sort_values(["letter", "year"])
    words = pd.DataFrame(word_rows).sort_values(["word", "year"])

    # globalny mianownik = suma po wszystkich wczytanych literach
    year_tot = (totals.groupby("year")["letter_tokens"].sum()
                .rename("total_tokens").reset_index())

    # odtworzenie indeksu COLOR wzorem z linii 333-336 skryptu głównego
    piv = words.pivot_table(index="year", columns="word", values="count",
                            aggfunc="sum").fillna(0)
    for w in RED_WORDS + BLUE_WORDS:          # słowa nieobecne w cache → zera
        if w not in piv.columns:
            piv[w] = 0
    denom = year_tot.set_index("year")["total_tokens"].reindex(piv.index)
    red = piv[RED_WORDS].sum(axis=1) / denom
    blue = piv[BLUE_WORDS].sum(axis=1) / denom
    color = (blue - red) / (blue + red + 1e-9)
    rebuilt = pd.DataFrame({"year": piv.index, "red": red.values,
                            "blue": blue.values, "color": color.values})

    totals.to_csv(out / "ngram_letter_year_totals.csv", index=False)
    words.to_csv(out / "ngram_word_year_counts.csv", index=False)
    year_tot.to_csv(out / "ngram_year_totals.csv", index=False)
    rebuilt.to_csv(out / "ngram_color_rebuilt.csv", index=False)

    print(f"\nZapisano do {out.resolve()}")
    print(f"  litery: {sorted(totals.letter.unique())}")
    print(f"  lata:   {totals.year.min()}–{totals.year.max()}")
    print(f"  słowa:  {len(words.word.unique())} z 20 oczekiwanych")
    brak = sorted(set(RED_WORDS + BLUE_WORDS) - set(words.word.unique()))
    if brak:
        print(f"  UWAGA — brak w cache: {brak} (litery początkowe: "
              f"{sorted({w[0] for w in brak})})")

    # kontrola: czy mianownik faktycznie się skraca (PATCH 1D)
    r2 = piv[RED_WORDS].sum(axis=1)
    b2 = piv[BLUE_WORDS].sum(axis=1)
    color_nodenom = (b2 - r2) / (b2 + r2 + 1e-9)
    d = float((color - color_nodenom).abs().max())
    print(f"\n  maks. |COLOR z mianownikiem − COLOR bez mianownika| = {d:.2e}")
    print("  → mianownik skraca się w indeksie COLOR" if d < 1e-6
          else "  → mianownik NIE skraca się — sprawdzić dlaczego")

    if a.verify:
        ref = pd.read_csv(a.verify)[["year", "color"]].dropna()
        m = ref.merge(rebuilt[["year", "color"]], on="year",
                      suffixes=("_ref", "_new"))
        if m.empty:
            print("\n  weryfikacja: brak wspólnych lat")
        else:
            diff = (m.color_ref - m.color_new).abs()
            print(f"\n  weryfikacja wobec {a.verify}: n={len(m)}, "
                  f"maks|Δ|={diff.max():.2e}, śr|Δ|={diff.mean():.2e}, "
                  f"korelacja={m.color_ref.corr(m.color_new):.6f}")
            print("  → odtworzenie zgodne" if diff.max() < 1e-6
                  else "  → ROZBIEŻNOŚĆ — zgłoś przed użyciem tabel")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
