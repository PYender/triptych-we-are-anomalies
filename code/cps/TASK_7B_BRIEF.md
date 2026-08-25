# TASK 7B — ETAP B TESTU 7: estymacja, bez uruchamiania

**Realizuje:** `TEST7_PROTOCOL.md` §7, §11 etap B · **Wprowadza:** D-021 ·
**Zakres:** wyłącznie **H9b.1**. P2 i zmienne z §6 odłożone do czasu dostarczenia COW NMC
(D-029 — decyzja odłożenia P2 zapisana w rejestrze, powód niezależny od jakiegokolwiek wyniku,
warunek odblokowania: dostarczenie `NMC_v6.0` z sumą kontrolną).

**Przegląd (PRZEGLĄD_TASK_7B.md, 2026-08-25):** brief NIE podmienia niczego, czego protokół
nie ustala — błąd typu D-023 (podstawienie silnika wnioskowania) nie występuje. Cztery luki
wykryte i naprawione poniżej, jedna poważna (§2), reszta formalna/redakcyjna. Po naprawie
**Etap B odblokowany**.

---

## 0. Etap A — przyjęty, z jedną przeliczką

Warstwa danych jest w porządku. Liczby kontrolne zgodne po sprostowaniu D-020, kontrola
ekspozycji 213/225 wyjaśniona co do sztuki, kontrola nazw zgodna z D-016. Zgłoszenie
czterech epizodów częściowych zamiast cichego rozstrzygnięcia było prawidłowe.

Nowa kategoria luk — **przerwa między okresami rywalizacji** — działa i jest istotna.
Chiny–Japonia tracą 51 lat ekspozycji na przerwie 1945–1996. Bez tego para dostałaby 62 lata
pokoju w czasie, gdy nie było między nimi żywej rywalizacji. Ten mechanizm sam z siebie
uzasadnia przejście na tę populację.

**Wykonane:** D-021 (reguła zdarzeń — start epizodu w oknie) zastosowane, zbiór przeliczony.
Dodatkowo wykryto i rozstrzygnięto D-025 (wykluczenie jednego odstępu Italy–Ethiopia,
ekspozycja zero — konsekwencja D-021, nieprzewidziana w tym briefie). Nowe liczby
zaraportowane obok dotychczasowych w `TEST7_DATA_REPORT.md` §6–§8: t0 62→64, cenzurowany
62→42, cenzurowany_bez_epizodow 58→56, pełny 43→43 (na poziomie modelu, mimo zmiany w
budowie sekwencji zdarzeń), przesunięte okno Cambodia–Vietnam (1970→1975, Skutek B).
Dodatkowo zweryfikowano i udokumentowano zasięg Skutku A poza cztery pierwotnie zgłoszone
przypadki (22/64 diad z epizodami — `TEST7_DATA_REPORT.md` §8, własność strukturalna
zbioru). **Ten punkt jest zamknięty — nie STOP już na tym etapie.**

## 1. Kolejność prac — punkt wspólny obu testów

Estymator jest ten sam. `test6_weibull.py` implementuje Weibulla pulowanego i Weibulla
z kruchością gamma, czyli dokładnie to, czego potrzebuje Test 7. **Nie pisz drugiego
estymatora.**

Przegląd Kroku 2 Testu 6 wykazał pięć usterek (`PRZEGLAD_test6_weibull.md`), wszystkie
naprawione i zweryfikowane dwukrotnie. Krok C Testu 6 zamknięty (D-027, `TEST6_KROK_C_REPORT.md`)
— estymator sprawdzony w realnym użyciu, na realnych danych, z realną regułą decyzyjną.
Warunek „estymator musi przetrwać rzeczywisty bieg Testu 6" jest spełniony.

## 2. Reguła decyzyjna — cytat protokołu (LUKA POWAŻNA naprawiona)

**Poprzednia wersja tego briefu pisała przy P1 tylko „ORZEKA dla H9b.1" i pomijała połowę
reguły decyzyjnej — ta sama klasa usterki co D-023 (podmiana metodologii), tylko przez
pominięcie zamiast przez podstawienie.** Poniżej §8 protokołu **w całości, jako cytat**, nie
streszczenie, zgodnie z regułą z D-024:

> **§8. Reguła decyzyjna — zadeklarowana przed biegiem**
>
> **H9b.1 uznaje się za wsparte**, jeżeli przedział ufności dla `k` z profilu wiarygodności
> w P1 **nie obejmuje 1** oraz ten sam kierunek utrzymuje się w S1 i S3.
>
> **H9b.2 uznaje się za wsparte**, jeżeli w P2 współczynnik przy koszcie poprzedniego epizodu
> (czas trwania albo straty) jest istotny na poziomie 0,05 i ma znak dodatni (dłuższy pokój po
> kosztowniejszej wojnie), oraz nie odwraca się po usunięciu wojen światowych (S1).
>
> **Przedziały ufności obowiązkowe**, w dwóch postaciach: profil wiarygodności oraz bootstrap
> losujący **całe diady**. Wartość punktowa bez przedziału nie jest wynikiem.
>
> **Wynik nierozstrzygający jest dopuszczalnym wynikiem.** Przy przedziale obejmującym 1
> raportujemy to jako brak rozstrzygnięcia, nie szukamy wariantu, w którym nie obejmuje.

**Do wykonawcy: reguła dla H9b.1 wymaga DWÓCH warunków naraz — CI z P1 nie obejmuje 1, ORAZ
ten sam kierunek w S1 i S3.** Sam CI z P1 nie wystarcza do rozstrzygnięcia, niezależnie od
tego, jak wyraźnie wyklucza 1.

## 3. Dopasowania Testu 7 — pięć, nie więcej

**Uwaga na różnicę wobec Testu 6:** tam orzekał model **pulowany**, tutaj orzeka model
**z kruchością**. Wynika to z §7 protokołu i z uzasadnienia D-015 B: przy 120 diadach
o rażąco różnych tempach model pulowany odpowiadałby na pytanie o mieszankę, nie o rytm
wewnątrz pary.

| id | model | zbiór | rola |
|---|---|---|---|
| **P1** | Weibull z kruchością gamma | 120 diad, bez `t0` | **ORZEKA dla H9b.1** (reguła §2 wyżej) |
| S1 | P1, bez epizodów obejmujących 1914–18 i 1939–45 | — | wrażliwość na synchronizację |
| S2 | P1 na `spatial=1` **i** `positional=0` | — | wrażliwość na typ rywalizacji |
| S3 | P1 z `t0` włączonym jako odstęp pełny | — | wrażliwość na założenie §5 |
| S4 | P1 na `td_rivalries` (Thompson i Dreyer 2012) | — | wrażliwość na kodowanie źródła |

Dopasowanie pulowane policz **jako diagnostykę**, nie jako wariant: jest granicą θ→0 modelu
P1, więc kosztuje zero, a różnica P1 wobec pulowanego jest wprost miarą heterogeniczności
temp. Raportuj obok, oznaczone jako diagnostyka.

## 4. Symulacja odzysku parametrów — na strukturze Testu 7, przed biegiem

Powtórz test odzysku z `TASK_6B_BRIEF.md` §3 punkt 2, ale **na strukturze tego zbioru**:
120 grup, około 43 zdarzeń pełnych, 120 obserwacji cenzurowanych, z rozkładem liczby zdarzeń
na grupę odczytanym z `test7_intervals.csv` (samą strukturę, nigdy wartości `t`).

Cenzurowanie w symulacji ma być **administracyjne**, niezależne od czasu zdarzenia — patrz
usterka 4 w przeglądzie. Cenzurowanie zależne od `T` zawyża `k̂` o około pięć punktów
procentowych, w stronę hipotezy.

Ta symulacja jest ważniejsza niż w Teście 6, bo struktura jest znacznie trudniejsza —
patrz §5. Ma odpowiedzieć na pytanie, jak szeroki będzie przedział, **zanim** zobaczymy dane.

## 5. Trzy ostrzeżenia zapisane przed biegiem

**Zdarzeń jest mniej, nie więcej.** 43 odstępy pełne wobec 45 w Teście 6. Wzrost ze 18 do 120
diad dotyczy liczby **grup**, nie liczby zdarzeń. Odchylenie `k̂` będzie zatem co najmniej
takie jak zmierzone dla Testu 6 przy prawidłowym cenzurowaniu, czyli **około 0,12**,
i prawdopodobnie większe.

**Zbiór jest w reżimie ciężkiego cenzurowania.** 120 obserwacji cenzurowanych wobec 43
zdarzeń to 74% cenzurowania. Nie unieważnia to testu — cenzurowanie jest tu właśnie
poszukiwaną informacją — ale zmienia problem estymacyjny i musi być nazwane.

**Kruchość będzie słabo identyfikowalna.** Parametr θ szacuje się z wielokrotnych zdarzeń
wewnątrz grupy. 58 diad nie ma żadnego zdarzenia, a wśród pozostałych 62 średnia to około
1,7 epizodu na parę, więc większość wnosi zero albo jeden odstęp. Grup niosących informację
o heterogeniczności jest kilkanaście. Spodziewaj się bardzo szerokiego przedziału dla θ
i zaraportuj go, zamiast podawać wartość punktową.

Wszystkie trzy mają trafić do raportu Etapu C jako deklaracja sprzed biegu, nie jako
wyjaśnienie po fakcie.

## 6. Przedziały ufności — i pomiar obowiązkowy poza regułą (LUKA MERYTORYCZNA)

Jak w `TASK_6B_BRIEF.md` §4: profil wiarygodności **oraz** bootstrap losujący całe diady.
Przy 120 grupach bootstrap diadowy jest znacznie stabilniejszy niż przy 18, więc rozbieżność
z profilem będzie bardziej wymowna niż w Teście 6.

**Doświadczenie z Kroku C Testu 6 (D-026/D-027), zadeklarowane TERAZ, przed biegiem Testu 7,
nie po zobaczeniu jego wyniku.** Na tych samych danych Testu 6 (18 diad): CI z profilu
(0,603–0,979) i CI bootstrapowy (0,647–0,965) oba wykluczyły 1, ALE wartość p z modelu
zerowego N1 (skalibrowanego na rzeczywistą różnorodność temp między diadami) wyszła 0,068,
bo model zerowy centruje się na k̂≈0,91, nie na 1,0 — CI porównuje z 1 wprost, więc jest
**systematycznie bardziej liberalny** w kierunku k<1 niż test z modelem zerowym. Gdyby regułą
Testu 6 był sam CI, H6.1 zostałaby uznana za wspartą; regułą był model zerowy i nie została.

**§8 Testu 7 opiera H9b.1 wyłącznie na CI. Reguły NIE zmieniamy** — jest zamrożona, a zmiana
po doświadczeniu z Testu 6 byłaby zmianą po zobaczeniu wyniku, choćby wyniku cudzego testu.
**Ale Etap B ma dodatkowo policzyć model zerowy typu N1 na strukturze Testu 7 i podać wartość
p obok obu przedziałów — obowiązkowo, poza regułą §8, wyłącznie do pokazania rozjazdu.** Ze
120 diadami rozjazd będzie prawdopodobnie szerszy niż w Teście 6 (18 diad) — heterogeniczność
temp większa, model zerowy centrować się będzie dalej od 1,0. Jeżeli CI wykluczy 1, a p
przekroczy 0,05, raport ma postawić to obok siebie wprost, tak jak zrobił to `TEST6_KROK_C_REPORT.md`.

**Raport ma też podawać odsetek replik bootstrapowych z θ̂ na granicy numerycznej (D-022)
obok każdego przedziału.** §8 mówi o CI dla modelu z kruchością, nie wspomina o θ̂ — ale jeśli
θ̂ zapada się do granicy w znacznej części biegów (D-022), model z kruchością staje się
tożsamy z pulowanym, i zdanie „orzeka model z kruchością" przestaje być prawdziwe mimo że
reguła §8 stosuje się mechanicznie poprawnie. Wysoki odsetek ma być nazwany wprost: decyzja
zapadła de facto na modelu pulowanym.

## 7. Czego nie robimy

Nie dodajemy szóstego wariantu. Nie wprowadzamy progu liczby wojen w żadnej postaci — 58
diad bez zdarzeń musi zostać w zbiorze. Nie wybieramy między Testem 6 a Testem 7 po
zobaczeniu, który wypadł korzystniej; różnica między nimi jest wynikiem mówiącym o wpływie
doboru populacji. Nie proponujemy wersji 2.0 protokołu przy wyniku nierozstrzygającym.

## 8. Kolejność i zatrzymania

Przeliczenie D-021/D-025 → **wykonane** (§0). Kod plus bliźniaczy `.md` plus symulacja
odzysku (§4) plus model zerowy N1 (§6) → **STOP**. Bieg na danych rzeczywistych dopiero po
przeglądzie kodu.
