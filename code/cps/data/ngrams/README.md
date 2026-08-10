# data/ngrams

Produkt pośredni COLOR z Google Books N-grams (Poziom 2 wg
`CPS_OPERATING_BRIEF.md` §3.3): w repo są tabele roczne, nie pliki `.gz`.

## Zawartość
| Plik | Zawartość |
|---|---|
| `ngram_word_year_counts.csv` | litera, słowo, rok, licznik — 20 słów RED/BLUE |
| `ngram_letter_year_totals.csv` | sumy tokenów per litera i rok |
| `ngram_color_rebuilt.csv` | odtworzony COLOR (red, blue, color) |
| `ngram_year_totals.csv` | globalny mianownik na rok |

## Pochodzenie
`googlebooks-eng-all-1gram-20120701-{a,b,c,d,e,h,i,p,r,s,t,w}.gz`,
przetworzone skryptem `pkl_to_csv.py`, zakres 1505–2008.
COLOR odtworzony z tych tabel zgadza się z `wars_color.csv` do `maks|Δ| = 2,2e-16`.

## Do uzupełnienia (§3.3)
Manifest źródeł z sha256 każdego `.gz` (URL + stamp `20120701`).
