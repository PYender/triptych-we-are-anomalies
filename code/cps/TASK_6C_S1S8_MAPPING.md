# TEST 6 — Krok A (D-023): odwzorowanie wariantów S1–S8 na warstwę danych po D-013/D-014

**Status: ZATWIERDZONE z trzema korektami (D-024). Krok B odblokowany i wykonany
(`test6_null.py`), czeka na przegląd przed uruchomieniem na danych rzeczywistych.**

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

**Konsekwencja liczbowa (D-024) — MA STAĆ W RAPORCIE PRZED wynikiem S1.** Rozkład epizodów
na diadę w zbiorze głównym: 10 diad ma 3, 7 ma 4, 1 ma 5. Próg ≥4 zostawia **8 diad, 25
zdarzeń** — niecałą połowę zbioru głównego (18/45). Odchylenie k̂ rośnie z ok. 0,12 do
ok. 0,16 (rząd wielkości z symulacji odzysku parametrów, nie z biegu na S1 — S1 samo jeszcze
nie policzone). Bez tego zastrzeżenia zgodność S1 z P1 zostałaby po fakcie odczytana jako
potwierdzenie, podczas gdy przy tej różnicy precyzji nie jest ani potwierdzeniem, ani
zaprzeczeniem — przedziały tej szerokości mogą się zgadzać przez brak mocy, nie przez
zgodność merytoryczną.

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

**Model zerowy dopisany (D-024) — S4 nie ma go automatycznie z §6.** Wzór §6 jest
zdefiniowany dla parametru kształtu k; S4 pyta o współczynnik przy czasie trwania
poprzedniego epizodu — inna wielkość, ten sam wzór nie stosuje się wprost. Ten sam surogat
N1 (proces Poissona per diada), ale statystyka testowa to `|β̂_czas_trwania|` zamiast
`|k̂−1|`, podstawiona pod ten sam wzór p. **S4 nie wchodzi do reguły decyzyjnej §8** — jest
odrębnym pytaniem („czy dłuższa wojna wydłuża regenerację"), nie wariantem wrażliwości P1.

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

**Kwalifikacja: ROZSTRZYGNIĘTE (D-024) — reguła implementatora ODWRÓCONA.**

To jedyny wariant, dla którego mechaniczne zastosowanie D-013 nie było oczywiste. Scalanie
epizodów (D-013) zostało zdefiniowane **na poziomie diady**: "konflikty **tej samej diady**...
nachodzące się lub stykające". Na poziomie państwa pojedynczy kraj może prowadzić kilka wojen
naraz z **różnymi** przeciwnikami — pytanie, czy takie nakładające się wojny mają się scalać
w jeden epizod państwa niezależnie od przeciwnika, czy tylko gdy dotyczą tego samego
przeciwnika, nie miało odpowiedzi w D-013 wprost i wymagało rozstrzygnięcia.

Pierwotna rekomendacja implementatora (scalać tylko wojny z tym samym przeciwnikiem/koalicją)
**była błędna i została odrzucona.** **Rozstrzygnięcie: scalamy WSZYSTKIE nakładające się lub
stykające się wojny tego samego państwa, niezależnie od przeciwnika.** Uzasadnienie: zegar
mierzy regenerację **podmiotu**, którego zegar liczymy — państwo kończące wojnę z jednym
przeciwnikiem i prowadzące nadal wojnę z innym **nie regeneruje się**, niezależnie od tego,
czy przeciwnik jest ten sam. Reguła implementatora policzyłaby jako czas oczekiwania okres,
w którym państwo faktycznie walczy — błąd tej samej klasy, jaki D-013 naprawiło na poziomie
diady. Kryterium z D-013 przenosi się przez **tożsamość podmiotu**, nie przez tożsamość
przeciwnika. Nigdy nie wykonany (implementacja pozostaje do Etapu z krokiem realizującym S7,
nie do Kroku B, który dotyczy N1/N2 na zbiorze głównym).

## S8 — poziom A rozszerzony o Extra-State

**Kwalifikacja: ZMIENIONA (D-024) — WYMAGAŁO decyzji, nie było czysto techniczne, jak
pierwotnie sklasyfikowano.**

`TEST6_DATA_REPORT.md` §8 (Etap A) już odnotował ten wariant jako świadomie odłożony:
"Zbiór ogranicza się do `Inter-StateWarData_v4.0.csv`... Rozszerzenie na Extra-/Intra-State
zmieniałoby definicję diady i nie jest podejmowane teraz." S8 jest dokładnie tym
odłożonym rozszerzeniem — pre-rejestrowanym od początku, nie nowym pomysłem.

Pierwotna klasyfikacja tego wariantu jako „czysto technicznego" była błędna: konflikty
Extra-State toczą się przeciw podmiotom bez kodu w `system2016.csv` (nie-państwowym albo
nieuznanym). D-014 wymaga obecności **obu** kodów w danym roku dla policzenia ekspozycji;
zastosowane dosłownie do S8 wyzerowałoby ekspozycję całego wariantu, czyli usunęło go
efektywnie, nie rozszerzyło — to wymagało rozstrzygnięcia, nie tylko technicznego
przeniesienia.

**Rozstrzygnięcie:** ekspozycja dla par Extra-State liczona **wyłącznie po stronie
państwowej** (obecność w `system2016.csv` tylko dla strony, która ma kod); okno domyka się
na 2007 albo na wyjście strony państwowej z systemu, w zależności co wcześniejsze. **S8
raportowany jako wariant opisowy**, nie wchodzi do reguły decyzyjnej §8 na równi z P1 —
metodologia ekspozycji jest tu z konieczności inna, więc porównanie ilościowe z P1 byłoby
mylące. Mechanika scalania (D-013) stosowana identycznie na konfliktach z
`Inter-StateWarData_v4.0.csv` **i** `Extra-StateWarData_v4.0.csv` łącznie. Nigdy nie
wykonany.

---

## Podsumowanie (po D-024)

| wariant | kwalifikacja | wymagało decyzji autora poza techniczną? |
|---|---|---|
| S1 | zmodyfikowany (próg na epizodach) + konsekwencja liczbowa (8 diad/25 zdarzeń, SD≈0,16) raportowana PRZED wynikiem | nie |
| S2 | bez zmian | nie |
| S3 | zmodyfikowany (start epizodu) + zastrzeżenie o nieporównywalności (bez zmian) | nie |
| S4 | zmodyfikowany (czas trwania epizodu) + własny model zerowy (`\|β̂_czas_trwania\|`), poza regułą §8 | nie |
| S5 | bez zmian w danych; nigdy nie uruchomiony | nie |
| S6 | bez zmian w danych + ograniczenie niemiecko-dyadyczne; nigdy nie uruchomiony | nie |
| S7 | **reguła implementatora ODWRÓCONA** — scalanie niezależne od przeciwnika (tożsamość podmiotu, nie przeciwnika) | **tak — rozstrzygnięte** |
| S8 | **reklasyfikowany** — ekspozycja tylko po stronie państwowej, wariant opisowy, poza regułą §8 | **tak — rozstrzygnięte** |

Żaden wariant nie jest bezprzedmiotowy po D-013/D-014 — wszystkie osiem pozostaje sensowne
i wykonalne. Dwa (S7, S8) wymagały jawnego rozstrzygnięcia merytorycznego, nie tylko
technicznego przeniesienia na nową jednostkę (epizod, ekspozycja) — oba rozstrzygnięte
w D-024, w obu przypadkach odwracając albo poprawiając pierwotną (błędną) klasyfikację
implementatora.

**Luka nieporuszona (D-024), celowo.** `TEST6_PROTOCOL.md` §1 stawia H6.2 (kontrast epok),
ale §8 formułuje regułę decyzyjną wyłącznie dla P1 — protokół nie ma kryterium falsyfikacji
dla kontrastu epokowego (S5/S6). Nie dopisano go po fakcie — zrobienie tego po zapoznaniu
się z wynikiem biegu niezgodnego (D-023) naruszałoby zakaz nr 10 w tę samą stronę, co
dopisywanie kryterium do P1 po wyniku. S5 i S6 pozostają opisowe; raport Kroku C ma stwierdzić
wprost, że H6.2 nie została w Teście 6 rozstrzygnięta — nie „wsparta" ani „obalona", tylko
nieobjęta regułą decyzyjną.

**STATUS: zatwierdzone, Krok B odblokowany i wykonany.** `test6_null.py` (N1/N2 per §6,
ziarno 20260822, B=2000, `test6_weibull.fit_pooled` jako estymator) zaimplementowany,
z bliźniaczym `.md` — czeka na przegląd przed uruchomieniem na danych rzeczywistych
(`--run-real`).
