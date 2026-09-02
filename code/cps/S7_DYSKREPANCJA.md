# S7 — rozbieżność liczb kontrolnych (TASK_S7.md §4)

**ROZSTRZYGNIĘTA (D-039 + D-040, 2 września 2026).** Rozbieżność była autora: liczby
kontrolne `TASK_S7.md` §4 pochodziły z nigdzie niezapisanej reguły `gap≤1`, nie z reguły
`gap≤0` faktycznie użytej przez kod Testu 6 (`test6_build_intervals.merge_episodes`,
sprawdzone bezpośrednio w źródle — D-039). Autor dodatkowo zdecydował (D-040), że
uczestnictwa tej samej wojny (ten sam `WarNum`, rozbite na wiersze lub fazy) scalają się w
jeden przedział niezależnie od kalendarzowego odstępu. Liczby obowiązujące: **13 państw /
110 odstępów pełnych przy progu ≥6; 39 państw / 182 przy progu ≥3** (D-040). Autora liczby
12/98 i 37/168 idą do erraty. Dokument poniżej to zapis dochodzenia sprzed rozstrzygnięcia,
zachowany do wglądu.

Zgłoszona zgodnie z wprost daną instrukcją zadania: „Twoje liczby mają się zgodzić albo
rozbieżność ma zostać zgłoszona, nie dopasowana." Poniżej wszystkie warianty sprawdzone
przed napisaniem tego zgłoszenia — żaden nie został przyjęty jako budowa domyślna wyłącznie
dlatego, że pasuje liczbowo.

## Co się zgadza dokładnie

| sprawdzenie | oczekiwane | policzone |
|---|---|---|
| wierszy uczestnictw w oknie 1816–2007 | 337 | **337** |
| przedziałów po rozbiciu faz (337 + 19 z poprawną fazą 2) | 356 | **356** |
| państw w pliku | 98 | **98** |

## Co się NIE zgadza

Budowa domyślna tego pliku (`test6_build_s7.py`): scalanie epizodów regułą D-024 §5
dosłownie = D-013 (`gap = start_nast − koniec_poprz ≤ 0`), fazy 2 jako OSOBNE wpisy
wejściowe do scalania (czytanie dosłowne TASK_S7.md §3: „fazy drugie... traktowane jako
osobne przedziały").

| sprawdzenie | oczekiwane | policzone (gap≤0) |
|---|---|---|
| państw przy progu ≥6 epizodów | 12 | **15** |
| odstępów pełnych przy progu ≥6 | 98 | **123** |
| państw przy progu ≥3 epizody | 37 | **40** |
| odstępów pełnych przy progu ≥3 | 168 | **190** |

`pelne_ekspozycja_zero = 0` w obu progach — **rozbieżność nie pochodzi z nałożenia
ekspozycji** (ekspozycja nie zmienia LICZBY odstępów, wyłącznie ich długość, i żaden
odstęp pełny nie ma tu ekspozycji zerowej). To wyklucza hipotezę zadania („różnice mogą
wyniknąć z obsługi ekspozycji, której ja nie nakładałem") jako źródło TEJ rozbieżności —
odnotowane wprost, nie przemilczane.

## Warianty sprawdzone przed zgłoszeniem

| wariant | państw ≥6 | pełnych ≥6 | państw ≥3 | pełnych ≥3 |
|---|---|---|---|---|
| **gap≤0, faza 2 osobno (budowa domyślna, powyżej)** | 15 | 123 | 40 | 190 |
| gap≤0, faza 2 scalona z fazą 1 w ramach (ccode,WarNum) | 13 | 110 | 39 | 182 |
| gap≤0, span per-wiersz (formuła `endyr` Testu 6 zastosowana per wiersz, bez łączenia duplikatów ccode+WarNum) | 13 | 110 | 39 | 182 |
| gap≤1 (tolerancja NIEUDOKUMENTOWANA, sprzeczna z tekstem D-013) | 12 | 97 | 37 | 167 |
| gap≤2 | 11 | 82 | 35 | 148 |

Wariant `gap≤1` odtwarza LICZBĘ PAŃSTW dokładnie (12 i 37) w obu progach, ale nie liczbę
odstępów pełnych (97 wobec 98, 167 wobec 168 — rozbieżność o dokładnie 1 w obu przypadkach,
sugerująca jeszcze jeden pojedynczy brakujący/nadmiarowy odstęp niezależnie od reguły gap).
**Nie przyjęty jako budowa domyślna** — reguła gap≤0 jest tą, którą TASK_S7.md §3 przywołuje
wprost („zgodnie z D-024 §5", które z kolei jest regułą D-013: „nachodzące się lub stykające
(gap≤0)"). Przyjęcie gap≤1 bez wyraźnej decyzji autora byłoby dopasowywaniem reguły do
wyniku — dokładnie to, czego zadanie zabrania.

## Kandydujące źródła rozbieżności (nierozstrzygnięte)

1. **Duplikaty (ccode, WarNum)** — 5 przypadków w danych (Francja/WWII, Łotwa/1919 [x2],
   Włochy/WWII, Bułgaria/WWII, Rumunia/WWII — państwa zmieniające stronę lub wznawiające
   udział w tej samej wojnie pod innym epizodem). Traktowane tu jako osobne uczestnictwa
   (nie scalane sztucznie w jeden wiersz) — to może, ale nie musi, być zgodne z liczeniem
   autora.
2. **Interpretacja „faza 2 jako osobny przedział"** — czytanie dosłowne (osobny wpis
   wejściowy do scalania) daje WIĘCEJ epizodów niż czytanie „faza 2 wydłuża koniec tego
   samego wpisu" (formuła `endyr` Testu 6 per wiersz) — oba sprawdzone, żaden nie trafia
   w 12/98.
3. **Definicja `gap`** — jedyny wariant trafiający w liczbę państw (gap≤1) jest
   niezgodny z tekstem D-013/D-024 §5 przywołanym przez to zadanie.

## Wniosek tego zgłoszenia

Trzy pierwsze liczby kontrolne (337, 356, 98) zgadzają się dokładnie — źródło danych i
podstawowe wczytanie są poprawne. Rozbieżność zaczyna się dopiero na etapie SCALANIA W
EPIZODY, nie na etapie wczytania czy ekspozycji. Potrzebne rozstrzygnięcie autora: czy
duplikaty (ccode,WarNum) mają być scalane, czy reguła `gap` ma inną definicję niż D-013,
zanim ten builder zostanie uznany za wersję ostateczną Etapu 1.

**Zgodnie z TASK_S7.md §7 (STOP po Etapie 1): budowa zbioru i liczby kontrolne są gotowe,
ale ZATRZYMUJĘ SIĘ tutaj — nie przechodzę do Etapu 2 (symulacja odchylenia), dopóki ta
rozbieżność nie zostanie rozstrzygnięta, bo Etap 2 zależy od liczby zdarzeń (98 vs 123),
która jest właśnie przedmiotem sporu.**
