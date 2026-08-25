# TEST 6 — Krok A (D-023): odwzorowanie wariantów S1–S8 na warstwę danych po D-013/D-014

**Status: PROPOZYCJA DO DECYZJI, nie implementacja. STOP przed Krokiem B.**

Kontekst: `TEST6_PROTOCOL.md` §7 pre-rejestruje osiem wariantów wrażliwości (S1–S8) na
populacji i definicji odstępu sprzed D-013 (scalanie w epizody) i D-014 (ekspozycja zamiast
kalendarza). Żaden z S1–S8 nie ma własnego wpisu w rejestrze aktualizującego go do nowej
warstwy danych. Dla każdego — jedna z trzech kwalifikacji, z uzasadnieniem.

---

## S1 — próg ≥4 zamiast ≥3 (wrażliwość na próg)

**Kwalifikacja: wykonywany w zmodyfikowanej postaci.**

Oryginał: próg liczony na surowych konfliktach. D-013 §3 przesunęła jednostkę progu z
surowych wierszy na epizody dla P1 ("próg dotyczy epizodów, nie surowych wierszy pliku").
Gdyby S1 pozostał na surowych konfliktach (≥4 zamiast ≥3), testowałby **dwie rzeczy naraz**
— wartość progu I jednostkę, na której się go liczy — myląc dwie osie wrażliwości, z których
druga jest już objęta osobno przez S-B (D-013/D-014, próg na wierszach surowych, wartość 3).

**Modyfikacja:** próg ≥4 stosowany do **liczby epizodów**, tą samą metodą co P1 (scalanie
D-013, potem próg). Uzasadnienie: S1 ma odpowiadać na pytanie "czy wynik zależy od wartości
progu", trzymając jednostkę stałą — inaczej wynik S1 byłby nieinterpretowalny (nie wiadomo,
czy zmiana pochodzi od wartości czy od jednostki).

## S2 — bez cenzurowania (kontrola, obciążony)

**Kwalifikacja: wykonywany bez zmian.**

Nie dotyczy jednostki progu ani definicji odstępu — usuwa wyłącznie wiersze cenzurowane
z populacji P1 (epizody, próg na epizodach, ekspozycja D-014). Pozostaje osobną, trzecią
osią wrażliwości obok S-A (kalendarz zamiast ekspozycji) i S-B (próg na wierszach) — żadna
z nich nie zastępuje S2, bo żadna nie usuwa cenzurowania.

## S3 — odstęp start→start zamiast koniec→start (wrażliwość na definicję)

**Kwalifikacja: wykonywany w zmodyfikowanej postaci, z zastrzeżeniem o nieporównywalności
(bez zmian względem sprzed D-013 w tej części).**

Oryginał już zastrzegał, że start→start mierzy **inną wielkość** niż koniec→start (miesza
czas trwania konfliktu z czasem regeneracji) — to zastrzeżenie stoi niezależnie od D-013.

**Modyfikacja wymagana przez D-013:** "start" i "koniec" odnoszą się teraz do **epizodów**
(scalonych), nie surowych konfliktów — inaczej S3 liczyłby odstępy między jednostkami
niespójnymi z P1 (P1 operuje na epizodach), co uniemożliwiłoby nawet jakościowe
porównanie. Start epizodu = najwcześniejszy start składowego konfliktu (już liczony przez
`merge_episodes`, pole `start`).

**Zastrzeżenie do zachowania w raporcie:** S3 pozostaje wariantem **opisowym**, nie
bezpośrednio porównywalnym z P1 — mierzy inną wielkość z definicji, nie tylko inną wartość.

## S4 — czas trwania poprzedniego konfliktu jako zmienna objaśniająca

**Kwalifikacja: wykonywany w zmodyfikowanej postaci.**

Oryginał: czas trwania pojedynczego surowego konfliktu. Po D-013 "poprzedni konflikt" w
sekwencji zdarzeń P1 jest epizodem, który może scalać kilka surowych wojen (np. Chiny–Japonia:
wojna chińsko-japońska + II wś w jeden epizod 1937–1945).

**Modyfikacja:** zmienna objaśniająca = **czas trwania epizodu** (start do końca scalonego
epizodu), nie pojedynczego surowego konfliktu — spójne z tym, co faktycznie poprzedza
mierzony odstęp w P1. Analogiczna decyzja została już podjęta dla Testu 7
(`TEST7_PROTOCOL.md` §6: "czas trwania poprzedniego epizodu").

## S5 — podział przed/po 1914 (H6.2, kontrast epok)

**Kwalifikacja: wykonywany bez zmian (warstwa danych już gotowa; sam wariant nigdy nie
uruchomiony).**

Kolumna `epoka_1914` istnieje już w `test6_intervals.csv` (przypisana wg roku końca
poprzedniego epizodu — ta sama logika, z której korzystał już Test 4/5 dla epoki). D-013
i D-014 nie zmieniają definicji podziału, tylko przeliczają, które lata trafiają do której
epoki wraz z resztą zbioru. **Nic do zmiany w konstrukcji S5 — ale S5 nigdy nie został
faktycznie policzony** (brak k, brak N1/N2, brak p dla kontrastu epokowego).

## S6 — podział przed/po 1945 (konsolidacja europejska)

**Kwalifikacja: wykonywany bez zmian, z ograniczeniem interpretacyjnym już odnotowanym
(D-014).**

Kolumna `epoka_1945` istnieje analogicznie do `epoka_1914`. **Ograniczenie do przeniesienia
z `TEST6_DATA_REPORT.md` §12:** twierdzenie o konsolidacji Europy po 1945 jest niemierzalne
dla par niemieckich, bo COW nie zna zjednoczonych Niemiec 1945–1990 (RFN 260/NRD 265 to inne
kody, nieużywane przez ten builder). S6 ma zostać wykonany, ale jego wynik dla diad z udziałem
Niemiec musi być czytany przez ten pryzmat, nie jako czyste świadectwo o konsolidacji.
Nigdy nie wykonany dotąd.

## S7 — poziom B, państwa ≥6 konfliktów (rytm agresji pojedynczego aktora)

**Kwalifikacja: wymaga decyzji autora przed wykonaniem — nie mieści się czysto w żadnej
z trzech kategorii.**

To jedyny wariant, dla którego mechaniczne zastosowanie D-013 nie jest oczywiste. Scalanie
epizodów (D-013) zostało zdefiniowane **na poziomie diady**: "konflikty **tej samej diady**...
nachodzące się lub stykające". Na poziomie państwa pojedynczy kraj może prowadzić kilka wojen
naraz z **różnymi** przeciwnikami — pytanie, czy takie nakładające się wojny z różnymi
przeciwnikami mają się scalać w jeden epizod państwa (analogicznie do diady), czy pozostać
osobnymi zdarzeniami mimo nakładania się w czasie, nie ma odpowiedzi w D-013 i wymaga nowego
rozstrzygnięcia, nie tylko technicznego przeniesienia.

**Rekomendacja, nie decyzja:** scalać tylko wojny tego samego państwa, które nachodzą się
**i** dotyczą przynajmniej częściowo tego samego przeciwnika/koalicji (bliżej duchowi D-013:
brak przerwy regeneracyjnej), a NIE każde dwie wojny państwa nakładające się w czasie
niezależnie od przeciwnika — ale to jest propozycja implementatora, nie fakt wynikający
z istniejących decyzji, i wymaga jawnego zatwierdzenia albo odrzucenia. Nigdy nie wykonany.

## S8 — poziom A rozszerzony o Extra-State

**Kwalifikacja: wykonywany w zmodyfikowanej postaci (rozszerzenie danych wejściowych).**

`TEST6_DATA_REPORT.md` §8 (Etap A) już odnotował ten wariant jako świadomie odłożony:
"Zbiór ogranicza się do `Inter-StateWarData_v4.0.csv`... Rozszerzenie na Extra-/Intra-State
zmieniałoby definicję diady i nie jest podejmowane teraz." S8 jest dokładnie tym
odłożonym rozszerzeniem — pre-rejestrowanym od początku, nie nowym pomysłem.

**Modyfikacja:** `build_diads`/`war_spans`/`merge_episodes` (D-013) i ekspozycja (D-014)
stosowane identycznie, na konfliktach z `Inter-StateWarData_v4.0.csv` **i**
`Extra-StateWarData_v4.0.csv` łącznie. Mechanika scalania i ekspozycji nie jest specyficzna
dla kategorii COW — generalizuje się bez nowej decyzji merytorycznej. Nigdy nie wykonany.

---

## Podsumowanie

| wariant | kwalifikacja | wymaga decyzji autora poza techniczną? |
|---|---|---|
| S1 | zmodyfikowany (próg na epizodach) | nie |
| S2 | bez zmian | nie |
| S3 | zmodyfikowany (start epizodu) + zastrzeżenie o nieporównywalności (bez zmian) | nie |
| S4 | zmodyfikowany (czas trwania epizodu) | nie |
| S5 | bez zmian w danych; nigdy nie uruchomiony | nie |
| S6 | bez zmian w danych + ograniczenie niemiecko-dyadyczne; nigdy nie uruchomiony | nie |
| S7 | **wymaga nowej decyzji** (reguła scalania na poziomie państwa nieokreślona) | **tak** |
| S8 | zmodyfikowany (dodanie Extra-State) | nie |

Żaden wariant nie jest bezprzedmiotowy po D-013/D-014 — wszystkie osiem pozostaje sensowne
i wykonalne, siedem przez techniczne (nie merytoryczne) przeniesienie na nową jednostkę
(epizod, ekspozycja), jeden (S7) wymaga jawnego rozstrzygnięcia reguły scalania na poziomie
państwa, zanim można go zaimplementować.

**STOP.** Czekam na zatwierdzenie powyższego odwzorowania (w szczególności rekomendacji dla
S1/S3/S4/S8 i pytania o S7) przed Krokiem B (implementacja N1/N2).
