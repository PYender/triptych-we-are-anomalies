# Rodzina dziewiąta — raport zamykający (Test 6, Test 7, S7/S7b/S7c)

**Status: rodzina dziewiąta zamknięta (autor, 2 września 2026).**

*Uwaga o strukturze tego dokumentu: został zbudowany w siedmiu częściach, jak uzgodniono —
ale dokładna, wcześniej ustalona lista tytułów tych siedmiu części nie znajduje się w żadnym
pliku repozytorium ani w bezpośrednio dostępnej części tej rozmowy, więc struktura poniżej
jest MOJĄ rekonstrukcją z precedensu (`TEST6_KROK_C_REPORT.md`) i wszystkiego, co zostało
wprost zażądane w tej rozmowie — nie kopią ustalonego wcześniej szablonu. Jeśli odbiega od
tego, co było uzgodnione, proszę o korektę; treść merytoryczna poniżej jest kompletna
niezależnie od nagłówków.*

---

## 0. Ujawnienia i dyscyplina (zakaz nr 10)

**S7b/S7c nie są pre-rejestrowane.** S7b powstał PO zobaczeniu wyniku S7 (k̂=0,9947, oba
przedziały objęły 1) — zapisane wprost w D-046, powtórzone tutaj. Argument, że nie jest to
dobieranie narzędzia pod tezę: mechanizm autora ("państwo kończy wojnę i rusza dalej")
dotyczy zegara DECYZJI O ATAKU, a S7 policzył odstępy między wszystkimi wojnami państwa,
także tymi, w których zostało napadnięte — niezgodność między hipotezą a operacjonalizacją
dawała się wskazać niezależnie od wyniku. Argument przeciwny: nikt jej nie wskazał, dopóki
S7 nie wyszedł zerowy. Oba stoją obok siebie, nierozstrzygnięte (D-046) — ocena zostaje przy
czytelniku.

**Deklaracje sprzed każdego biegu** (moc, kierunek oczekiwań, próg wykluczenia jedynki) były
zapisywane w rejestrze PRZED uruchomieniem `--run-real` dla każdego wariantu (D-032/D-037 dla
Testu 7 P1, D-042/D-043 dla S7, D-046/D-047/D-048 dla S7b/S7c) — żaden opis w tym dokumencie
nie został napisany przed zobaczeniem odpowiedniego wyniku, ale KAŻDA deklaracja mocy/progu
poniżej BYŁA zapisana przed swoim biegiem.

## 1. Metodologia wspólna (bez odstępstw między wariantami)

- Estymator: `test6_weibull.py` (`fit_pooled`/`fit_frailty`, profil wiarygodności,
  bootstrap grupowy) — NIE pisany od nowa dla żadnego wariantu tej rodziny.
- Scalanie epizodów: gap≤0 (D-013, doprecyzowane D-039 — sprawdzone wprost w kodzie Testu 6).
  Dla wariantów państwowych (S7/S7b/S7c) dodatkowo D-040: uczestnictwa TEJ SAMEJ wojny
  (ten sam `WarNum`) scalają się w jeden przedział niezależnie od odstępu kalendarzowego.
- Ekspozycja: D-014 (lata członkostwa w systemie COW, `system2016.csv`).
- Model zerowy N1: proces Poissona per grupa, ziarno 20260822, B=2000, zabezpieczenie przed
  remisem D-026 §7 — diagnostyczny, poza regułą decyzyjną §8 (D-029 pkt 2 dla diad; ta sama
  logika zastosowana wprost dla państw, bez zmiany kodu).
- N2: pominięty jednym zdaniem dla WSZYSTKICH wariantów (D-026) — zdegenerowany względem
  k̂ pulowanego z powodów algebraicznych (`negloglik_pooled` nie odwołuje się do etykiety
  grupy), niezależnie od jednostki analizy czy operacjonalizacji.
- Symulacja deklaracji mocy: mechanizm `min(T,C)` (D-031) — okno administracyjne realne per
  grupa, liczba zdarzeń jako WYNIK wyścigu zdarzenie-kontra-cenzurowanie, nigdy jako
  założenie.
- **Zastrzeżenie o bootstrapie przy małej liczbie grup (D-045).** Symulacja pokrycia na
  strukturze S7 (13 grup, 1000 replik, k_prawdziwe=1) pokazała: pokrycie przedziału
  profilowego = 95,0% (nominalne), pokrycie bootstrapowego (poziom grup) = 90,1% —
  ISTOTNIE poniżej nominalnego. Średnia szerokość obu przedziałów w tej symulacji była
  niemal identyczna (stosunek 0,976) — zawodzi CENTROWANIE rozkładu bootstrapowego przy
  małej liczbie grup, nie sama szerokość. Konsekwencja dla całej rodziny: przy trzynastu
  (S7, S7b) i dwudziestu dziewięciu (S7c) grupach przedziałowi bootstrapowemu nie należy
  ufać bardziej niż profilowemu — obserwacja, że bootstrap bywa węższy w konkretnej realnej
  replice, nie jest dowodem większej precyzji.

## 2. Tabela główna — pięć wariantów

| | **Test 6**<br>pary, próg 3 | **Test 7 P1**<br>pary, po stawce | **S7**<br>państwo, wszystkie wojny | **S7b**<br>państwo, inicjacje | **S7c**<br>państwo, cele |
|---|---|---|---|---|---|
| jednostka | diada | diada | państwo | państwo | państwo |
| n grup | 18 | 101 | 13 | 13 | 29 |
| n zdarzeń | 45 | 37 | 110 | 50 | 95 |
| statystyka decydująca | pulowana | kruchość | pulowana | pulowana | pulowana |
| k̂ (decydująca) | 0,7780 | 0,8428 | 0,9947 | 0,9299 | 0,9003 |
| CI profil | [0,6029; 0,9791] | [0,6235; 1,1024] | [0,8582; 1,1410] | [0,7443; 1,1343] | [0,7620; 1,0491] |
| — wyklucza 1? | **TAK** | nie | nie | nie | nie |
| CI bootstrap (grupy) | [0,6471; 0,9649] | [0,6720; 1,0851] | [0,9174; 1,0901] | [0,8063; 1,1053] | [0,8054; 1,0328] |
| — wyklucza 1? | **TAK** | nie | nie | nie | nie |
| N1 p (diagnostyczny) | 0,068 | 0,2655 | 0,9755 | 0,6272 | 0,4588 |
| θ̂ (kruchość, drugorzędna) | nie liczone w Kroku C | 2,655 (nie na granicy) | 4,08×10⁻⁸ (na granicy) | 1×10⁻¹⁰ (na granicy) | 1×10⁻¹⁰ (na granicy) |
| frac_theta_boundary (bootstrap kruchości) | — | — | 0,2525 | 0,6865 | 0,8075 |
| SD(k̂) zadeklarowane przed biegiem | 0,127¹ | 0,138 | 0,0782 | 0,1203 | 0,0846 |
| próg wykluczenia 1 | <0,751 / >1,249¹ | <0,730 / >1,270 | <0,847 / >1,153 | <0,764 / >1,236 | <0,834 / >1,166 |
| efekt Testu 6 (0,778) mieści się w progu? | — (to jest ten efekt) | **NIE** | TAK | **NIE** | TAK |
| **wynik przypisywalny danym czy brakowi mocy** | **danym (pozytywny)** | **brakowi mocy²** | **danym (zerowy)** | **brakowi mocy** | **danym (zerowy)** |

¹ SD Testu 6 (0,127) policzone RETROAKTYWNIE w D-031 (poprawka mechanizmu symulacji po
przeglądzie Testu 7), nie zadeklarowane przed oryginalnym biegiem Kroku C — Krok C
poprzedzał tę konwencję. Podane dla spójności tabeli, nie jako deklaracja sprzed biegu w
tym samym sensie co pozostałe cztery kolumny.

² **To nie jest nowe ustalenie tego raportu — było już zapisane w D-032, przed samym biegiem
Etapu C Testu 7**, jako powód ODŁOŻENIA tego biegu: "przy 37 zdarzeniach i odchyleniu k̂ około
0,138 przedział wykluczy jedynkę dopiero przy wartości poniżej 0,73... a efekt zaobserwowany
w Teście 6 wynosił 0,778." Konsekwentnie zastosowane tutaj do klasyfikacji w tabeli: Test 7
P1 nie miał, z własnej zadeklarowanej precyzji, mocy do wykrycia efektu wielkości Testu 6 —
jego nieodrzucenie jedynki jest więc, tą samą miarą co S7b, nierozstrzygnięciem, nie czystym
wynikiem negatywnym.

**Kruchość zapadnięta w S7/S7b/S7c (D-022, przypomniane tutaj).** We wszystkich trzech
wariantach państwowych θ̂ osiada na numerycznej granicy (S7b/S7c dosłownie na 1×10⁻¹⁰; S7
funkcjonalnie, 4×10⁻⁸), z odsetkiem replik bootstrapowych na granicy 25–81%. Model orzekający
jest w tych trzech wariantach DE FACTO PULOWANY — przedziały dla kruchości nie są
interpretowalne osobno. Nie zmienia to wniosku, bo obie statystyki (pulowana i kruchości)
dają w każdym z tych trzech wariantów praktycznie te same liczby.

## 3. Obserwacja: odchylenie od jedynki maleje monotonicznie z rozszerzaniem jednostki

Uporządkowane od najmniejszej do największej jednostki analizy:

| jednostka | k̂ |
|---|---|
| pary, próg 3 (Test 6) | **0,778** |
| pary, po stawce (Test 7 P1) | **0,843** |
| państwo, wojny jako cel (S7c) | **0,900** |
| państwo, inicjacje (S7b) | **0,930** |
| państwo, wszystkie wojny (S7) | **0,995** |

To jest obserwacja, podana bez interpretacji w tym miejscu. Dwie konkurencyjne wykładnie,
obie zapisane w D-044, żadna nie rozstrzygnięta przez dane zebrane dotąd:

**Wykładnia A.** Sygnał widoczny na parach był artefaktem mieszania jednostek o różnych
tempach regeneracji — pulowanie do większej, bardziej zagregowanej jednostki (państwo)
usuwa ten artefakt i ujawnia prawdziwy brak efektu.

**Wykładnia B.** Zegar jest własnością PARY (bilateralny), nie aktora. Pulowanie wojen
jednego państwa z różnymi przeciwnikami (Francja z Niemcami, Anglią, Chinami, Tajlandią
naraz) rozmywa realny sygnał diadowy zamiast go ujawniać — zero na poziomie państwa jest
konsekwencją zmieszania kilkunastu różnych zegarów w jeden, nie dowodem, że żaden z nich nie
istnieje.

Obie wykładnie są równie zgodne z zaobserwowaną monotonicznością. Dane rodziny dziewiątej
nie rozstrzygają między nimi.

## 4. Ograniczenia

- **Hipoteza zegara bilateralnego pozostaje nierozstrzygnięta** — nie jako wniosek z samego
  S7, tylko jako granica całej rodziny (D-044): na poziomie par nigdy nie było dość zdarzeń
  do rozdzielenia zegarów przeciwnik-po-przeciwniku; na poziomie państw ten wymiar nie jest
  w ogóle mierzony (kruchość S7/S7b/S7c mierzy heterogeniczność MIĘDZY PAŃSTWAMI, nie
  MIĘDZY PRZECIWNIKAMI tego samego państwa — dwa różne pytania, D-044 punkt 2).
- **Asymetria mocy S7b/S7c (D-048).** Kontrola negatywna (S7c, SD=0,0846) jest CZULSZA od
  testu orzekającego (S7b, SD=0,1203) — odwraca zwykłą logikę kontroli negatywnej. Zaszedł
  układ trzeci z czterech zapisanych przed biegiem: żaden przedział nie wyklucza 1. Dla S7c
  to wynik przypisywalny danym; dla S7b — nierozstrzygnięcie z braku mocy, nie świadectwo
  przeciw hipotezie zegara inicjacji.
- **Bootstrap grupowy przy małej liczbie grup zawodza centrowaniem, nie szerokością**
  (D-045, §1 wyżej) — dotyczy wszystkich trzech wariantów państwowych (13/13/29 grup),
  potencjalnie także Testu 6 (18 diad), nieprzeliczone wstecz.
- **Reguła §8 protokołu Testu 6 pozostaje niespełnialna** dla wariantów opartych na N2
  (D-026) — degeneracja jest własnością statystyki pulowanej, nie konkretnego zbioru danych.
- **Test 6 nie ma dopasowania kruchości** — model F1 nigdy nie został policzony w Kroku C,
  więc porównanie θ̂ w tabeli głównej jest niepełne dla tego jednego wiersza.

## 5. Errata zbiorcza (poprawki własnych pomyłek autora, w toku tej rodziny)

| co | błędne | poprawne | źródło |
|---|---|---|---|
| liczby kontrolne S7 (próg≥6/≥3) | 12 państw/98 zdarzeń; 37/168 | 13/110 (gap≤0 potwierdzone kodem); 39/182 | D-039 |
| przyczyna S7 v1.0 15→13 | "tylko Francja" (D-040, stwierdzenie wstępne) | siedem państw, sprostowane | D-041 |
| deklaracja S7b/S7c (próg≥3) | 14 państw/54 zdarzeń (S7b); 30/100 (S7c) | 13/50 (S7b, z D-040); 29/95 (S7c) | D-047 |
| liczby inicjacji wojen | Włochy 7, Niemcy 7 (liczone jako uczestnictwa, faza podwójnie) | Włochy 6, Niemcy 5 (liczone jako epizody) | D-046/D-047 |
| przepowiednia S7 (k̂, przedziały) | k w 0,75–0,90, profil wyklucza 1 | k=0,9947, żaden przedział nie wyklucza 1 | D-043→D-044 |
| przepowiednia S7 (szerokość bootstrap) | bootstrap wyraźnie szerszy niż profil | bootstrap węższy (stosunek 0,611), potem D-045: to efekt centrowania nie szerokości | D-043→D-045 |
| wykładnia S7 (mieszanie diad) | "grupowanie na poziomie par było artefaktem mieszania tempa" (za daleko idący wniosek) | dwie wykładnie równoważne, nierozstrzygnięte (§3 wyżej) | D-044 |
| gap dla scalania epizodów S7 (pierwotnie) | gap≤1 (nigdzie niezapisane) | gap≤0 (D-013, potwierdzone w kodzie Testu 6) | D-039 |

Wszystkie powyższe zgłoszone przez samego autora po własnej weryfikacji, nie wymuszone
przeglądem z zewnątrz — odnotowane dla kompletności rejestru, zgodnie z dyscypliną
"zgłoś rozbieżność, nie dopasowuj," stosowaną konsekwentnie w obie strony.

## 6. Status końcowy

**Rodzina dziewiąta jest zamknięta (autor, 2 września 2026).**

Jeden czysty wynik pozytywny (Test 6, pary, próg 3 — oba przedziały wykluczają 1). Dwa
czyste wyniki zerowe przypisywalne danym (S7, wszystkie wojny państwa; S7c, wojny jako cel).
Dwa nierozstrzygnięcia z braku mocy, nie świadectwa przeciw jakiejkolwiek hipotezie (Test 7
P1, pary po stawce; S7b, inicjacje). Żaden wariant o dostatecznej czułości nie potwierdził
efektu wielkości Testu 6 poza samym Testem 6.

Hipoteza zegara bilateralnego (mechanizm pary, nie aktora) pozostaje otwarta — nie obalona,
nie potwierdzona, poza zasięgiem pomiarowym tej rodziny testów z powodów strukturalnych
(§4 wyżej), nie z powodu braku wysiłku.

Wariant S7 (i jego pochodne S7b/S7c) pozostają, zgodnie z ustaleniem sprzed pierwszego biegu
(TASK_S7.md §8), WARIANTAMI WRAŻLIWOŚCI — nie awansują na wariant pierwszorzędny niezależnie
od wyniku.

Możliwy dalszy krok, wspomniany wcześniej w tej rozmowie (D-032), nie podjęty w ramach tej
rodziny: "protokół 9c" (test lokalizacji szczytu hazardu) — osobna, nowa rodzina testów,
poza zakresem tego dokumentu.
