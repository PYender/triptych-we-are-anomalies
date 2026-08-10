# data/ngrams

Produkt pośredni COLOR z Google Books N-grams (Poziom 2 wg
`CPS_OPERATING_BRIEF.md` §3.3): do repo trafiają tabele roczne, nie pliki `.gz`.

## Zawartość docelowa
Cztery tabele z konwersji `.pkl` (skrypt `pkl_to_csv.py`) — jeszcze nie dodane.
Do odtworzenia modułu COLOR nie są potrzebne pliki `.gz` (116–433 MB każdy),
tylko roczne częstości słów kluczowych plus globalny mianownik (~192 wiersze).

## Wymagane przy dodawaniu (§3.3)
Manifest źródeł: URL, stamp `20120701`, sha256 każdego `.gz`.

Katalog pusty (`.gitkeep`) do czasu wgrania tabel.
