# ERRATA — status zmiennej COLOR: obciążenie datowaniem publikacji

**Data:** 2026-08-23 · **Dotyczy:** wszystkich wyników opartych na szeregu COLOR, w
szczególności przyczynowości Grangera w obu kierunkach, korelacji skrośnej i kointegracji
· **Status:** do wniesienia przy najbliższym PR; wymaga wpisu w rejestrze decyzji (D-018)

---

## 1. Dotychczasowy zapis — niepełny

W dotychczasowej dokumentacji kierunek **wojny → COLOR** (istotny, p < 0,01, opóźnienia 1–6)
był oznaczony jako niecytowalny z **jednego** powodu: policzono go częściowo na szeregu
wygładzonym **centrowaną** średnią ruchomą MA(11), która przecieka informacją z przyszłości
do przeszłości i sama z siebie może wytworzyć pozorne wyprzedzenie. Replikacja na średniej
jednostronnej pozostaje wymagana.

**Powodów jest dwa, a drugi jest poważniejszy** — filtru można się pozbyć, datowania nie.

## 2. Powód drugi: COLOR mierzy datę wydania, nie datę wypowiedzenia

Szereg COLOR pochodzi z korpusu Google Books, który datuje **publikację**. Retoryka wojenna
i pokojowa — przemówienia, mowy parlamentarne, depesze, wspomnienia — jest w znacznej części
najpierw **wygłaszana**, a dopiero potem drukowana. Dodatkowo pierwsze wydania bywały
niskonakładowe, a do szerokiego obiegu trafiały dopiero wznowienia.

Wynikają z tego trzy własności obciążenia:

1. **Jest jednostronne.** Publikacja nigdy nie wyprzedza wypowiedzenia. Opóźnienie jest
   z definicji dodatnie.
2. **Jest nieznane co do wielkości.** Rozkład odstępu wygłoszenie–publikacja nie jest w tych
   danych obserwowalny.
3. **Jest niestacjonarne.** Tempo druku, struktura rynku wydawniczego i zasięg pierwszych
   nakładów zmieniały się między 1816 a 2007 radykalnie.

## 3. Konsekwencja: hipotezy nierozróżnialne

Szereg COLOR jest opóźnioną wersją retoryki rzeczywistej, o opóźnieniu dodatnim i zmiennym.
Aparat wyprzedzenia mierzy więc **sumę** opóźnienia zjawiska i opóźnienia wydawniczego, bez
możliwości ich rozdzielenia.

Konkretnie: wynik „wojny wyprzedzają COLOR na opóźnieniach 1–6" jest **dokładnie tym**, czego
należałoby oczekiwać, gdyby retoryka wyprzedzała wojny o rok, a druk opóźniał ją o 3–7 lat.
Hipoteza autora (retoryka wyprzedza konflikt) i wynik obserwowany (konflikt wyprzedza
retorykę) są w obecnych danych **nieodróżnialne**.

**To nie jest słabe świadectwo przeciw hipotezie wyprzedzającej retoryki. To jest brak
świadectwa w którąkolwiek stronę.**

## 4. Zasięg erraty jest szerszy niż jeden test

Niestacjonarne opóźnienie pomiaru w szeregu użytym do analizy wyprzedzenia może wytworzyć
pozorną strukturę okresową z niczego. Dotyczy to nie tylko kierunku Grangera, lecz **wszystkich
wyników, w których COLOR wchodzi jako zmienna czasowa** — korelacji skrośnej, kointegracji,
oraz każdego wniosku o relacji COLOR z aktywnością konfliktową.

Wyniki te nie stają się przez to fałszywe. Stają się **nieinterpretowalne co do kierunku
w czasie**, dopóki datowanie nie zostanie skorygowane albo objęte analizą wrażliwości.

## 5. Skutek dla planowanych prac

**Test wyprzedzenia (roboczo Test 8) nie ma sensu przed korektą datowania.** Protokół
przyczynowości Grangera zbudowany na zmiennej o nieznanym, dodatnim i niestacjonarnym
opóźnieniu dałby wynik metodologicznie poprawny i pusty. Lepiej go nie wykonywać, niż
wykonać i opublikować.

Dotyczy to tak samo hipotezy autora o **dwóch cyklach** — cyklu wojny i pokoju poprzedzonym
wyprzedzającym go cyklem retoryki. Hipoteza ta **nie została dotąd przetestowana**: Testy 1,
3 i 5 badały wyłącznie okresowość pojedynczego szeregu zagregowanego i nie dotykały
wyprzedzenia. Jej test wymaga jednak zmiennej retorycznej o kontrolowanym datowaniu.

## 6. Droga wyjścia — możliwa, choć pracochłonna

Dat wygłoszenia nie da się odzyskać dla całego korpusu n-gramów. Da się natomiast:

1. **Oszacować rozkład opóźnienia wydawniczego** na próbie, dla której znane są obie daty —
   mowy parlamentarne, depesze dyplomatyczne, datowane przemówienia — i sprawdzić, czy
   rozkład ten zmienia się w czasie.
2. **Puścić test wyprzedzenia przy całym paśmie prawdopodobnych opóźnień**, zamiast przy
   jednym oszacowaniu, i sprawdzić odporność wyniku. To jest rozwiązanie uczciwsze niż
   przesunięcie szeregu o jedną liczbę, bo nie udaje precyzji, której nie ma.

**Kryterium rozstrzygające, do zadeklarowania z góry:** jeżeli kierunek zależności odwraca
się przy przesunięciu o trzy lata w granicach prawdopodobnego opóźnienia, to znaczy, że
w tych danych nie mierzymy relacji czasowej, tylko datowanie wydawnicze — i tak należy to
zaraportować.

## 7. Zapis do przeniesienia do rozdziału

Zmienna COLOR pozostaje użyteczna jako **wskaźnik poziomu** obecności retoryki wojennej
i pokojowej w druku. Nie jest w obecnej postaci użyteczna jako **wskaźnik momentu**. Każde
zdanie w rozdziale III.3.2 przypisujące COLOR rolę wyprzedzającą albo nadążającą wymaga
przeformułowania albo usunięcia.
