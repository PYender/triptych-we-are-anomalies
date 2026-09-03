# TEST 11 — PROTOKÓŁ: kształt funkcji hazardu (rodzina 9c)

**Wersja 1.0 — ZAMROŻONA 2026-09-02.** §4 zamknięty przez autora 2 września 2026.
**Numer testu: 11** (Test 10 zajęty przez kontrast epok, D-050). Ziarno modelu zerowego:
**20260822**, ten sam co N1/N2/Testu 10 w całym projekcie. Zastępuje `PROTOKOL_9c_szkic.md`
v0.1, który był pisany dla danych Testu 7 i zawierał tylko jedną (niewłaściwą) rodzinę
rozkładów.

**Specyfikacja implementacyjna dopisana przy zamrożeniu (Code):** rodzina uogólnionej gammy
zaimplementowana przez parametryzację **Stacy'ego** (`scipy.stats.gengamma(a, c, scale)`),
NIE przez algebrę Prentice'a wprost. Obie parametryzacje opisują TĘ SAMĄ rodzinę
rozkładów — Weibull jest zagnieżdżony identycznie (Stacy: `a=1`, `c`=kształt Weibulla;
Prentice: `Q=1`), a przestrzeń możliwych kształtów hazardu (rosnący/malejący/maksimum
wewnętrzne/minimum wewnętrzne) jest ta sama — sprawdzone numerycznie bezpośrednio (grid
search po `(a,c)`, oba kształty niemonotoniczne potwierdzone: maksimum wewnętrzne np. przy
`a=0,1, c=-0,3`; minimum wewnętrzne np. przy `a=0,1, c=1,5`). Wybór podyktowany dostępnością
sprawdzonej, przetestowanej implementacji w SciPy zamiast pisania algebry Prentice'a od
zera — mniejsze ryzyko błędu numerycznego. Parametry raportowane w obu układach, gdzie to
przydatne dla czytelności.

---

## §0. Ujawnienie

**Ten protokół powstał po zobaczeniu wyników rodziny dziewiątej.** Znamy wartości parametru
kształtu dla wszystkich pięciu wariantów, w tym 0,9947 dla zbioru, na którym ten test ma być
wykonany. Ujawnienie stoi na początku każdego raportu i nie może zostać usunięte.

**Argument, że nie jest to dobieranie narzędzia pod tezę.** Ograniczenie, które ten test ma
usunąć, jest własnością rodziny rozkładów zapisaną w §5 protokołu Testu 6 z 22 sierpnia:
**hazard Weibulla jest monotoniczny z definicji.** Hipoteza autora, sformułowana jako
narastanie, szczyt i opadanie, nie mieści się w tej rodzinie. Testy 6, 7 i S7 jej zatem nie
odrzuciły; **nie miały jej gdzie umieścić.** Ograniczenie istniało od początku i nie zostało
wtedy nazwane, co jest przeoczeniem projektanta.

**Argument przeciwny.** Nikt go nie nazwał, dopóki wyniki nie okazały się niekorzystne.

Oba stoją obok siebie, nierozstrzygnięte.

## §1. Pytanie

**H11.1.** Hazard międzykonfliktowy jest **niemonotoniczny**: rośnie i opada, albo opada
i rośnie, zamiast zmieniać się w jedną stronę przez cały czas oczekiwania.

**Czego test nie orzeka.** O okresowości w szeregu rocznym (Testy 1, 3, 5). O tym, gdzie
leży punkt zwrotny, chyba że autor zadeklaruje przedział w §4. **O powtarzalnym falowaniu.**
Rodziny rozkładów użyte w tym teście dopuszczają **najwyżej jeden punkt zwrotny**. Hipoteza
autora w brzmieniu „narastanie, szczyt, opadanie, znów narastanie" zawiera dwa zwroty i
**nie jest w całości sprawdzalna tym narzędziem**. Sprawdzalny jest jej pierwszy człon.

## §2. Populacja i dane

**Zbiór S7**, czyli `test6_s7_intervals.csv`: 13 państw, 110 odstępów pełnych, 13
cenzurowanych. Scalanie gap ≤ 0 (D-039) plus reguła `WarNum` (D-040), ekspozycja wg D-014,
okno 1816–2007.

**Dlaczego ten zbiór, a nie dane Testu 7.** Symulacja mocy wykonana przed napisaniem tego
protokołu, wyniki w §8: na strukturze Testu 7, czyli 37 zdarzeń i 72 procent cenzurowania,
moc wynosiła około 60 do 68 procent. Na strukturze S7, czyli 110 zdarzeń i 11 procent
cenzurowania, wynosi 98 do 100. Różnica bierze się głównie z cenzurowania: **kształt hazardu
w ogonie jest widoczny tylko wtedy, gdy obserwacje do ogona dochodzą.**

**Jedna zmiana naraz:** wobec S7 zmienia się wyłącznie rodzina rozkładów.

**Warianty kontrolne** na zbiorach Testu 6 i S7c, dla porównania z zamkniętymi wynikami.

## §3. Statystyka pierwszorzędna

**Uogólniony rozkład gamma** (parametryzacja Stacy'ego, `scipy.stats.gengamma`, patrz nota
przy zamrożeniu powyżej), trzy parametry, przeciw **rozkładowi Weibulla**, dwa parametry.
Rodziny są **zagnieżdżone**: Weibull jest przypadkiem szczególnym (`a=1`). Hazard uogólnionej
gammy może być rosnący, malejący, **z jednym maksimum wewnętrznym** albo **z jednym minimum
wewnętrznym** — sprawdzone numerycznie przy zamrożeniu.

**Wielkość orzekająca:** iloraz wiarygodności między dopasowaniem uogólnionej gammy
a Weibulla, na tych samych danych i z tym samym cenzurowaniem.

**Wartość p symulacyjna**, nie asymptotyczna. Surogaty generowane z Weibulla dopasowanego
do obserwacji, mechanizmem `min(T, C)` zgodnie z D-031, B = 2000, ziarno 20260822.
Zabezpieczenie przed remisem z D-026 §7: `frac_tie` powyżej 0,01 zatrzymuje bieg.

**Klasyfikacja kształtu**, wielkość pomocnicza i nieorzekająca sama z siebie: z dopasowanej
uogólnionej gammy liczy się hazard na siatce w zakresie obserwowanych odstępów i przypisuje
jeden z czterech kształtów: rosnący, malejący, z maksimum wewnętrznym, z minimum wewnętrznym.
Podaje się też **położenie punktu zwrotnego w latach z przedziałem ufności**.

## §4. Deklaracja kierunku — ZAMKNIĘTA przez autora, 2 września 2026

**Kierunek: GARB**, czyli maksimum wewnętrzne. Ryzyko konfliktu rośnie od zakończenia
poprzedniej wojny do pewnego momentu, po czym opada.

Zapisane przed jakimkolwiek dopasowaniem uogólnionej gammy do danych rzeczywistych i przed
symulacją mocy dla tej rodziny.

**Odnotowanie, nie zastrzeżenie.** Autor ma w tej rozmowie dwa sformułowania mechanizmu
i odpowiadają one dwóm różnym kształtom. Deklaracja wskazuje pierwszy z nich.

*Mechanizm regeneracyjny, pierwotny, z Tryptyku:* wyczerpanie, odbudowa, wymiana pokolenia,
znów wojna. Ryzyko jest niskie zaraz po wojnie, rośnie wraz z odbudową, a po przekroczeniu
pewnego czasu opada, gdy pokój się utrwala. **To jest garb** i to został zadeklarowany.

*Mechanizm rozpędu, sformułowany później:* państwo kończy wojnę i idzie za ciosem, więc
ryzyko jest wysokie zaraz po wojnie, potem spada w fazie wyczerpania i rośnie w fazie
odbudowy. **To jest wanna** i nie została zadeklarowana.

**Cena deklaracji kierunkowej.** Jeżeli dane pokażą kształt wanny, choćby najwyraźniej,
warunek drugi §6 nie będzie spełniony i H11.1 zostanie zapisana jako niewsparta. Nie wolno
tego odwrócić po fakcie ani przeliczyć na wariant bezkierunkowy. Kształt przeciwny zostanie
natomiast **zaraportowany jako obserwacja**, jawnie oznaczona jako nieorzekająca, żeby
informacja nie przepadła.

**Położenie punktu zwrotnego** pozostaje niezadeklarowane, zgodnie z D-032 §2, wraz
z zapisanym tam zakazem przedstawiania zbieżności oszacowanego położenia z jakąkolwiek
wcześniej wymienianą liczbą jako potwierdzenia.

## §5. Warianty

| id | opis | rola |
|---|---|---|
| **P1** | uogólniona gamma wobec Weibulla, zbiór S7, 13 państw | **ORZEKA dla H11.1** |
| S1 | to samo na S7c, 29 państw, 95 odstępów | wrażliwość na jednostkę |
| S2 | to samo na zbiorze głównym Testu 6, 18 diad, 45 odstępów | porównanie z zamkniętym wynikiem |
| S3 | P1 z modelem kruchości w obu rodzinach | kontrola zafałszowania, §7 |

Orzeka wyłącznie P1.

## §6. Reguła decyzyjna — zamrożona teraz

**H11.1 uznaje się za wsparte**, jeżeli spełnione są **trzy warunki naraz**:

1. wartość p dla ilorazu wiarygodności w P1 jest mniejsza od **0,05**;
2. kształt hazardu z dopasowanej uogólnionej gammy jest **niemonotoniczny w kierunku
   zadeklarowanym w §4**;
3. **punkt zwrotny leży wewnątrz zakresu obserwowanych odstępów**, a nie w ekstrapolowanym
   ogonie.

Warunek trzeci jest istotny: punkt zwrotny poza zakresem danych nie jest obserwacją, tylko
własnością dopasowanej krzywej.

**Zastrzeżenie o faktycznym poziomie istotności, wynikające z ustalenia po Teście 10
(D-053).** Reguła złożona z koniunkcji **nie ma nominalnego poziomu 0,05**. Zmierzone dla
dwóch członów: faktyczny poziom 0,007. Tutaj członów są trzy. **Faktyczny poziom tej reguły
zmierzony w symulacji z §8** (patrz D-054/D-055 w rejestrze), zamiast deklarowania
nominalnego.

**Kryterium falsyfikacji.** Jeżeli którykolwiek z trzech warunków nie jest spełniony,
H11.1 nie jest wsparte. Nie wolno wtedy zmieniać rodziny rozkładów, zbioru ani kierunku
z §4.

## §7. Kontrola zafałszowania — obowiązkowa przed wnioskowaniem

**Zmierzone przed napisaniem tego protokołu, na strukturze S7:** gdy dane pochodzą
z rosnącego hazardu wewnątrz grup połączonego z heterogenicznością między nimi, czyli gdy
**żadnego garbu nie ma**, rodzina niemonotoniczna wygrywa w **76 procentach** biegów przy
kruchości 0,6 i w **98 procentach** przy kruchości 1,5. Mieszanka rozkładów o różnych tempach
produkuje pozorny kształt.

**Dlaczego mimo to test jest wykonalny akurat na tym zbiorze.** W S7 parametr kruchości
osiadł na granicy numerycznej, a heterogeniczność między trzynastoma państwami jest
niewykrywalna. Mechanizm fałszujący nie ma czym działać.

**Ale ma to zostać sprawdzone na danych, nie założone.** Przed wnioskowaniem o kształcie
implementator dopasowuje model z kruchością (wariant S3) i podaje `θ̂` wraz z odsetkiem
replik bootstrapowych na granicy. **Jeżeli `θ̂` nie osiądzie na granicy, P1 nie orzeka**
i wynik ma zostać zaraportowany jako nierozstrzygający z powodu zafałszowania.

Kalibracja potwierdzona: przy prawdziwym braku niemonotoniczności i bez kruchości fałszywe
odrzucenia wynoszą 5 procent, a przy parametrze 0,99, czyli takim jak w S7, 7 procent.

## §8. Symulacja mocy — WYKONANA przed zamrożeniem

Wyniki pełne w `test11_power_wyniki.json`, streszczenie w rejestrze D-054/D-055.

## §9. Ograniczenia zapisane przed biegiem

1. **Najwyżej jeden punkt zwrotny.** Hipoteza autora zawiera dwa. Sprawdzamy jej pierwszy
   człon, nie całość.
2. **Wartość dla całości jest znana** i wynosi 0,9947, czyli praktycznie hazard stały.
   Kształt niemonotoniczny musiałby zatem znosić się w uśrednieniu.
3. **Trzynaście państw**, a D-045 ustaliło, że przy tej liczbie grup bootstrap ma pokrycie
   90 procent zamiast 95.
4. **Zafałszowanie przez heterogeniczność** jest wykluczone empirycznie, nie strukturalnie:
   opiera się na tym, że w tym konkretnym zbiorze kruchość zapadła się do zera — potwierdzone
   już realnym dopasowaniem S7 (D-043: θ̂≈4,08×10⁻⁸, na granicy, frac_theta_boundary=0,2525),
   reużytym tutaj bez potrzeby nowego dopasowania na danych rzeczywistych.

## §10. Zakazy

1. Jedna zmiana naraz: wobec S7 zmienia się wyłącznie rodzina rozkładów.
2. Nie dobieramy rodziny po zobaczeniu, która pasuje lepiej. Uogólniona gamma jest wybrana
   **przed** biegiem i to ona orzeka.
3. Położenie punktu zwrotnego, jeżeli wyjdzie, jest wielkością **oszacowaną, nie
   przewidzianą**, i nie wolno przedstawiać jej zbieżności z żadną wcześniejszą liczbą jako
   potwierdzenia (D-032 §2).
4. Wynik negatywny albo nierozstrzygający publikujemy tak samo jak pozytywny.
5. Ujawnienie z §0 nie może zostać usunięte.

## §11. Etapy

1. Symulacja mocy z §8 dla pełnej reguły → **STOP**, decyzja autora ✅ WYKONANE (ten dokument)
2. Zamrożenie, numer i ziarno (§4 zamknięty) ✅ WYKONANE
3. Kod plus bliźniaczy `.md`, kontrola `frac_tie` i kontrola zafałszowania z §7 → **STOP**
4. Bieg, surowe liczby bez narracji → **STOP**
5. Raport
