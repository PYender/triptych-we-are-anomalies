# TEST 10 — PROTOKÓŁ: kontrast epok w strukturze odstępów (H8.1)

**Wersja 1.0 — ZAMROŻONA 2026-09-02.** Numer testu: **10** (nie 8 — kolizja z roboczą nazwą
"Test 8" zarezerwowaną w D-018 dla testu wyprzedzenia retoryki COLOR; "Test 9" pominięty
celowo, żeby uniknąć mylenia z nazwą opisową "rodzina dziewiąta", pod którą w tym projekcie
odbywa się cała rozmowa o Teście 6/7/S7 — obie kolizje odnotowane, żadna nie rozstrzygana
milcząco). Ziarno modelu zerowego: **20260822**, ten sam co N1/N2 w całym projekcie
(D-023 §6, powtórzone konsekwentnie w Teście 7/S7/S7b/S7c).

Hipoteza H8.1 pozostaje nazwana zgodnie z pierwotnym numerem protokołu Testu 6 (§1
`TEST6_PROTOCOL.md`, 22 sierpnia) — numer HIPOTEZY nie zmienia się wraz z numerem TESTU,
który ją bada; to są dwie osobne numeracje w tym projekcie.

---

## §0. Ujawnienie

**Hipoteza jest pre-rejestrowana. Reguła decyzyjna nie.**

H6.2 stoi w §1 zamrożonego `TEST6_PROTOCOL.md` z 22 sierpnia 2026 w brzmieniu: „Struktura
odstępów między konfliktami zmienia się po 1914 roku". Warianty S5 i S6, czyli podziały na
1914 i 1945, są wymienione w §7 tego samego protokołu. **Żaden z nich nie został wykonany.**

Czego brakowało i brakuje do dziś: §8 protokołu Testu 6 formułuje regułę decyzyjną
**wyłącznie dla P1**, czyli dla H6.1. Dla H6.2 protokół nie przewidział kryterium. Ustalono
to w D-024 §7 i wtedy świadomie **nie dopisano reguły**, ponieważ znany był już wynik biegu
niezgodnego z §6–§8 i każde kryterium napisane w tamtym momencie byłoby kryterium napisanym
po zobaczeniu danych.

**Co się zmieniło i dlaczego piszemy regułę teraz.** Ten test wykonywany jest na **innej
jednostce i innym zbiorze** niż ten, którego wynik wtedy znaliśmy: na poziomie państw, na
danych S7, gdzie żadnego podziału epokowego nigdy nie liczono. Znany jest wynik dla całego
okresu, k̂ = 0,9947, ale **nie jest znany żaden wynik w rozbiciu na epoki**.

**Czego to nie usuwa.** Wiemy, że wartość dla całości leży praktycznie na jedynce. To ogranicza
przestrzeń możliwych wyników w rozbiciu: jeżeli epoki różnią się silnie, muszą różnić się w
przeciwne strony wokół jedynki. Ta wiedza istnieje przed zamrożeniem i musi być zapisana.

## §1. Pytanie i hipotezy

**H8.1.** Struktura odstępów między konfliktami różni się między okresem przed 1914 a po 1914.

**H8.2 (drugorzędna).** To samo dla podziału na 1945.

**Czego test nie orzeka.** O okresowości w szeregu rocznym, zamkniętej w Testach 1, 3 i 5.
O umiędzynarodowieniu konfliktów, które bada Test 4 i które jest **inną wielkością**: tam
mierzy się liczbę uczestników wojny, tu odstęp między wojnami. Zbieżność albo rozbieżność
wyniku z Testem 4 nie jest potwierdzeniem ani zaprzeczeniem żadnego z nich.

## §2. Populacja i dane

**Bez zmian wobec S7.** Zbiór `test6_s7_intervals.csv`, 13 państw, 110 odstępów pełnych,
13 cenzurowanych. Scalanie gap ≤ 0 (D-039) plus reguła `WarNum` (D-040), ekspozycja wg
D-014, okno 1816–2007.

**Jedna zmiana naraz:** dochodzi wyłącznie podział na epoki.

## §3. Przypisanie odstępu do epoki

Odstęp należy do epoki wyznaczonej przez **rok zakończenia poprzedniego epizodu**, czyli
przez moment, w którym zaczyna się mierzony czas oczekiwania. Nie przez rok początku
następnego konfliktu i nie przez środek odstępu.

Uzasadnienie: mierzoną wielkością jest czas regeneracji, a jego warunki określa stan świata
w chwili, gdy zegar rusza.

**Odstępy przecinające granicę epoki nie są dzielone ani usuwane.** Trafiają w całości do
epoki, w której się zaczęły. Odstęp cenzurowany traktowany tak samo.

**Liczby kontrolne zweryfikowane niezależnie przed zamrożeniem — ZGODNE, bez rozbieżności:**
podział 1914 daje **48 odstępów pełnych przed i 62 po** (plus 13 cenzurowanych, wszystkie w
epoce "po" z konstrukcji — okno kończy się 2007>1914 dla każdego państwa); podział 1945 daje
**69 przed i 41 po** (plus 13 cenzurowanych, wszystkie w epoce "po"). Sprawdzone bezpośrednio
na `test6_s7_intervals.csv`, dokładne dopasowanie do liczb autora.

## §4. Kierunek zadeklarowany przez autora (2026-09-02, przed zamrożeniem)

**Kierunkowa: po 1914 wartość NIŻSZA (bliżej grupowania) niż przed.** Deklaracja: po 1914
wojny skupiają się bardziej niż wcześniej.

**Cena tej deklaracji, zapisana razem z nią:** jeżeli wyjdzie odwrotnie — choćby bardzo
wyraźnie — protokół każe zapisać BRAK WSPARCIA dla H8.1. Nie wolno przeliczyć wyniku na
wariant dwustronny post factum.

**Uwaga o zgodności z poziomem ogólnym, zapisana przez autora.** Kierunek jest zgodny z tym,
co widziano dotąd w rodzinie dziewiątej — wszystkie zmierzone wartości k̂ leżą poniżej
jedynki. Ale zgodność z poziomem ogólnym NIE mówi nic o różnicy MIĘDZY epokami — to jest
osobna wielkość, mierzona tutaj po raz pierwszy.

## §5. Statystyka i wnioskowanie

**Wielkość pierwszorzędna: różnica parametrów kształtu między epokami**, `Δ = k̂_po − k̂_przed`,
oszacowana z modelu pulowanego z cenzurowaniem, osobno w każdej epoce.

**Model zerowy: przynależność do epoki nieinformatywna.** Surogaty powstają przez
**permutację etykiet epoki między odstępami, z zachowaniem liczebności obu epok** (48 i 62
dla podziału 1914).

Permutacja jest tutaj **niezdegenerowana** (w odróżnieniu od N2 Testu 6), bo statystyka
zależy od podziału na dwie podpróby, a nie tylko od multizbioru par — **potwierdzone
pomiarem**, nie przyjęte na wiarę (patrz §8, symulacja mocy, gdzie `frac_tie` mierzony na
strukturze syntetycznej: maksimum zaobserwowane w tysiącach replik = poniżej progu 0,01;
szczegóły w `test8_power_wyniki.json`).

B = 2000, ziarno **20260822**.

**Wzór — WERSJA SKORYGOWANA względem szkicu 0.1.** Szkic zapisywał wzór dla kierunku
"większa" (`Δ_sur ≥ Δ_obs`); autor zadeklarował kierunek przeciwny (§4: niższa po 1914,
`Δ_obs` oczekiwane UJEMNE). Obowiązuje wersja licząca surogaty **NIE WIĘKSZE** od obserwacji:

```
p = (1 + #{ Δ_sur ≤ Δ_obs }) / (B + 1)        WARIANT KIERUNKOWY (obowiązujący, §4)
p = (1 + #{ |Δ_sur| ≥ |Δ_obs| }) / (B + 1)    wariant dwustronny — liczony i podawany
                                                OBOK, jawnie oznaczony NIEORZEKAJĄCY
```

**Przedziały ufności** dla `k̂` w każdej epoce osobno: profil oraz bootstrap na poziomie
państw. Przy trzynastu grupach obowiązuje D-045: **bootstrapowi nie ufa się bardziej niż
profilowi**, a odsetek replik z `θ̂` na granicy podawany obok.

## §6. Warianty

| id | opis | rola |
|---|---|---|
| **P1** | podział 1914, model pulowany, 13 państw | **ORZEKA dla H8.1** |
| S1 | podział 1945 | H8.2, drugorzędny |
| S2 | P1 z modelem kruchości | wrażliwość na heterogeniczność między państwami |
| S3 | P1 na S7c, czyli wojny jako cel, 29 państw i 95 odstępów | wrażliwość na jednostkę |

Orzeka wyłącznie P1. S3 wchodzi, bo S7c był w rodzinie dziewiątej jedynym wariantem
państwowym o czułości zbliżonej do Testu 6.

## §7. Reguła decyzyjna — zamrożona teraz

**H8.1 uznaje się za wsparte**, jeżeli wartość p w P1 (wariant kierunkowy, §5) jest
mniejsza od **0,05** ORAZ przedziały ufności dla `k̂` w obu epokach **nie nakładają się na
siebie**.

Drugi warunek jest istotny. Sama wartość p mówi, że różnica jest większa, niż daje
przypadkowe przypisanie etykiet, ale przy dwóch podpróbach po kilkadziesiąt zdarzeń może to
zajść przy przedziałach szeroko zachodzących na siebie, czyli przy różnicy nieodróżnialnej
od szumu w każdej epoce z osobna.

**Kryterium falsyfikacji.** Jeżeli p wynosi 0,05 lub więcej, twierdzenie „struktura odstępów
zmienia się po 1914" nie jest wsparte. Nie wolno wtedy zmieniać roku podziału, jednostki
analizy ani statystyki.

## §8. Symulacja mocy — WYKONANA przed zamrożeniem, przed biegiem, przed czymkolwiek innym

Mechanizm `min(T,C)` (D-031), realna struktura 13/12 państw (12 z ekspozycją przed 1914,
13 po), podział 48/62. Wyniki pełne: `test8_power_wyniki.json`, streszczenie: `D-050` w
`CPS_DECISION_LOG.md`.

## §9. Ograniczenia zapisane przed biegiem

1. **Wynik dla całości jest znany** i wynosi 0,9947. Silna różnica między epokami wymagałaby
   zatem odchyleń w przeciwne strony, znoszących się w sumie. To zawęża przestrzeń wyników
   i musi być powiedziane przy interpretacji.
2. **Podział 1914 przecina pierwszą wojnę światową**, która jest jednym epizodem dla
   większości z trzynastu państw. **Zmierzone przed zamrożeniem:** z 62 odstępów pełnych po
   1914, **7 (11,3%) zaczyna się dokładnie w 1918** (koniec I wojny), kolejne **7 (11,3%)
   dokładnie w 1945** (koniec II wojny) — razem **14/62 (22,6%)** zaczyna się od zakończenia
   jednej z dwóch wojen światowych. To NIE jest większość — sklejenie jest realne i warte
   nazwania, ale nie tak silne, jak sugerowałaby sama liczba państw z epizodem obejmującym
   wojnę światową (D-042/D-048, rodzina dziewiąta).
3. **Trzynaście państw to mało**, a D-045 ustaliło, że przy tej liczbie grup bootstrap ma
   pokrycie 90 procent zamiast 95.
4. **Zbiór kończy się w 2007**, więc epoka po 1945 obejmuje 62 lata, a przed 1914 aż 98.
   Epoki nie są równe ani długością, ani liczbą zdarzeń.

## §10. Zakazy

1. Jedna zmiana naraz: dochodzi wyłącznie podział epokowy.
2. Rok podziału jest zamrożony na 1914 dla P1 i 1945 dla S1. Żadnego skanowania po latach
   podziału, ani jawnego, ani przez „sprawdzenie, czy przypadkiem nie wychodzi lepiej".
3. Wynik negatywny albo nierozstrzygający publikujemy tak samo jak pozytywny.
4. Ujawnienie z §0 nie może zostać usunięte z żadnej wersji raportu.
5. Jeżeli symulacja mocy z §8 wypadnie źle, nie ratujemy testu obniżeniem wymagań.

## §11. Etapy

1. Symulacja mocy z §8 → **STOP**, decyzja autora, czy uruchamiać ✅ WYKONANE (ten dokument)
2. Uzupełnienie §4 przez autora → zamrożenie protokołu, nadanie numeru i ziarna ✅ WYKONANE
3. Kod plus bliźniaczy `.md`, kontrola `frac_tie` → **STOP**, przegląd
4. Bieg, surowe liczby bez narracji → **STOP**
5. Raport
