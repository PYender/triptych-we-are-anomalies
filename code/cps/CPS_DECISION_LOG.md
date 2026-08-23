# CPS_DECISION_LOG

Rejestr decyzji metodycznych podejmowanych **przed** uruchomieniem testów.
Każdy wpis jest datowany i zawiera uzasadnienie niezależne od wyniku, którego dotyczy.
Wpisów nie usuwa się ani nie modyfikuje — zmiany wchodzą jako nowe decyzje
z odwołaniem do poprzedniej.

---

## D-001 · 2026-08-10 · Poziom agregacji serii COW

**Rozstrzygnięcie.** Serią pierwszorzędną dla rodzin testów 1–3 jest
**`A_COW_W`** — poziom wojny, z deduplikacją po `WarNum`.
Seria `A_COW_P` (poziom uczestnika) pozostaje w obiegu jako wariant porównawczy
i jako przedmiot odrębnego pytania badawczego (D-002).

**Uzasadnienie, niezależne od wyniku testu.**

1. Rozdział III.3.2 definiuje zmienną jako liczbę wojen. `A_COW_W` jest jedyną
   serią zgodną z tą definicją. Zmiana definicji po zobaczeniu wyników byłaby
   naruszeniem zakazu nr 10.
2. `A_COW_W` koreluje z niezależnym zbiorem UCDP na poziomie 0,73–0,88 na wszystkich
   badanych oknach wspólnych; `A_COW_P` koreluje na poziomie 0,00–0,24, miejscami
   ujemnie. Kryterium zbieżności dwóch niezależnie kodowanych zbiorów wskazuje
   jednoznacznie na poziom wojny.
3. Poziom wojny jest jednorodny między czterema kategoriami COW. Poziom uczestnika
   jest dostępny tylko dla Inter- i Extra-State, więc seria `P` miesza dwa poziomy
   agregacji w jednej wielkości.

**Świadomie przyjęty koszt.** Wybór jest niekorzystny dla dotychczasowego wyniku:
przy poziomie wojny kontrast epok odwraca się (χ² 14,53 w epoce 1 wobec 6,97
w epoce 2), podczas gdy przy poziomie uczestnika wynosi 7,43 wobec 39,49.
Decyzja zapada mimo tego i właśnie dlatego jest wiążąca.

**Zakres.** Obowiązuje dla rodzin 1, 2 i 3. Rodzina 4 testuje wrażliwość na ten
wybór i raportuje oba warianty obok siebie.

---

## D-002 · 2026-08-10 · Rozdzielenie dwóch hipotez

**Rozstrzygnięcie.** Twierdzenie bronione w Tryptyku v0.1 zostaje rozdzielone na
dwie niezależne hipotezy, testowane osobno i raportowane osobno.

**H1 — cykliczność (hipoteza główna, seria `A_COW_W`).**
W epoce post-1914 seria konfliktów wykazuje strukturę fazową w paśmie 32–40 lat
silniejszą niż w epoce przed 1914.
*Status wstępny: przesłanki są NEGATYWNE.* Statystyki orientacyjne wskazują kierunek
przeciwny do przewidywanego. Rodzina 2 rozstrzyga formalnie.
*Kryterium falsyfikacji:* jeżeli χ² epoki 2 nie przewyższa χ² epoki 1 przy
serii pierwszorzędnej i nullu AR(3), hipoteza w tej postaci zostaje odrzucona.

**H2 — umiędzynarodowienie (hipoteza poboczna, seria `A_COW_P`).**
Po 1914 konflikty angażują istotnie więcej stron naraz, a seria ważona liczbą
uczestników wykazuje strukturę fazową nieobecną przed 1914.
*Status wstępny: przesłanki są POZYTYWNE, ale niejednoznaczne co do interpretacji.*
*Zastrzeżenie obowiązkowe:* na poziomie uczestnika I i II wojna światowa wnoszą
po kilkanaście–kilkadziesiąt wierszo-lat i leżą blisko siebie fazowo. Profil złożony
zdominowany przez dwa zdarzenia **nie jest** dowodem okresowości. Rodzina 2 musi
zawierać wariant z wyłączeniem lat 1914–1918 i 1939–1945 albo z winsoryzacją.

**Konsekwencja redakcyjna.** H1 i H2 nie mogą być prezentowane jako jedno
twierdzenie. Jeżeli H1 upada, a H2 się broni, rozdział opisuje falsyfikację
własnej wcześniejszej tezy oraz nową hipotezę — nie „potwierdzenie modelu".

---

## D-003 · 2026-08-10 · Zakres serii COW

**Rozstrzygnięcie.** Seria COW biegnie do **2007** (bez odcięcia na 2003).

**Uzasadnienie.** Odcięcie z Testu 0 wynikało z diagnozy „cenzurowania ogona",
która okazała się błędna. Faktyczną przyczyną deformacji końcówki był błąd obsługi
kodu `-7` w kodzie agregującym (Test 0B, korekta F1). Po korekcie ogon nie jest
zdeformowany i nie ma podstaw do skracania szeregu.

---

## D-004 · 2026-08-11 · Zakres detrendingu przesądza znak kontrastu epok (wiążące dla rodziny 2)

**Ustalenie (empiryczne, z Testu 1).** Znak kontrastu epok w statystyce χ²
epoch-folding (T = 35,1, faza od pierwszego roku okna) na `A_COW_W` **odwraca się**
w zależności od zakresu, na jakim wykonano detrending liniowy:

| Zakres detrendingu | χ² epoka 2 (1914–2007) | χ² epoka 1 (1816–1913) | Znak |
|---|---|---|---|
| bez detrendingu | 14,73 | 22,23 | epoka 1 > epoka 2 |
| detrending w oknie epoki | 25,77 | 22,04 | epoka 2 > epoka 1 |
| detrending na całej serii | 18,00 | 20,54 | epoka 1 > epoka 2 |

χ² epoki 2 waha się od 14,7 do 25,8 wyłącznie od tej decyzji. Tylko detrending
w oknie stawia epokę 2 wyżej (kierunek zgodny z hipotezą H1).

**Rozstrzygnięcie.** Zakres detrendingu jest decyzją metodyczną zastrzeżoną dla
autora (context pack §8: granice okien). **Protokół rodziny 2 musi deklarować
zakres detrendingu przed policzeniem jakiejkolwiek statystyki.** Bez tej deklaracji
znak rdzeniowego wyniku tezy (kontrast epok) zależy od wyboru podjętego po
zobaczeniu danych — naruszenie zakazu nr 10. Ten wpis **nie wybiera** zakresu;
ustala wymóg jego jawnej pre-rejestracji.

**Uwaga o nieporównywalności.** Powyższe liczby używają fazy „od pierwszego roku
okna" (konwencja kodu Testu 1). Przy konwencji lutowej `rok mod T` od roku 0 te
same okna dają: detrending w oknie 11,25 / 15,03; seria MA(11) 6,97 / 14,53
(odtworzenie orientacyjnych χ² z context packu §2). Konwencja fazy jest drugą osią
nieporównywalności i również musi być zadeklarowana w protokole rodziny 2.

**Powiązane:** `TEST1_REPORT.md` §6.1.

---

## D-005 · 2026-08-11 · Okres 35,1 roku jest produktem łańcucha przetwarzania

**Ustalenie.** Obie procedury z Tryptyku odtworzone wiernie na serii oryginalnej:

| procedura | oryginał (przed F1–F3) | `A_COW_W` po korektach |
|---|---|---|
| sin-fit (`curve_fit`, p0 = 2π/50) | **35,08** (Tryptyk podaje 35,1) | **42,9** |
| pik periodogramu | **96,0 lat** | 64,0 lat |

Dwa wnioski:

1. **Wartość 35,1 nie była błędem rachunkowym.** Procedura była zaimplementowana
   poprawnie; liczba odtwarza się co do drugiego miejsca po przecinku. Jest jednak
   produktem konkretnego łańcucha decyzji (poziom agregacji, wygładzanie, obsługa
   kodów braku) — po korektach ta sama procedura daje 42,9 roku dla wojen
   i 47,6 dla uczestników.
2. **Periodogram nigdy nie potwierdzał 36 lat.** Najsilniejszy pik widma serii
   oryginalnej leży przy **96 latach** (moc 328); 38,4 roku jest pikiem **drugim**
   (moc 274). Wartość 0,028/rok podana na s. 57 nie odpowiada żadnemu prążkowi
   Fouriera przy n = 192 (sąsiednie: 0,0260 i 0,0312), co wskazuje na odczyt
   z wykresu log-log. Twierdzenie o „niezależnym potwierdzeniu" nie ma podstawy —
   była jedna metoda, nie dwie.

**Konsekwencja dla erraty.** Pozycja 13 (PSD jako niezależne potwierdzenie sin-fitu)
zostaje uzupełniona o powyższe liczby. Dochodzi nowa pozycja: okres nie jest
wielkością zmierzoną, lecz zależną od łańcucha przetwarzania — zmiana dowolnego
ogniwa przesuwa go o kilkanaście lat.

**Konsekwencja dla Testu 2B.** T = 35,1 przyjmujemy, by testować hipotezę
w jej oryginalnej postaci — nie dlatego, że jest to wartość wyprowadzona z danych.

---

## D-006 · 2026-08-11 · Zaniechanie Testu 2A i status katalogu zaburzeń

**Test 2A zaniechany.** Okna C1–C8 (Tryptyk s. 70–72) opisują *fazy* przebiegu
krzywej („climb up to a high ridge", „sustained ridge and tail", „the rise before
World War I", „plateau"), nie punkty szczytowe, i pokrywają 65% szeregu. Nie nadają
się na listę do testu trafień. Wcześniejszy rachunek odstępów między środkami tych
okien (mediana 19,5 roku) opierał się na błędnym odczycie i **zostaje wycofany**.

**Katalog zaburzeń jest otwarty.** Ustalenie autora: Tryptyk podaje czynniki
zaburzające jako przykłady, nie jako listę zamkniętą. Priorytetu dokumentacyjnego
zatem nie ma. Zastępuje go generowanie list z **progów zewnętrznych i wyczerpujących
katalogów** (Test 2B §3), z zakazem redakcji listy wynikowej.

**Zdarzenie 1945 (użycie broni jądrowej) traktowane osobno.** Tryptyk (C9) twierdzi,
że odstraszanie **przesuwa ciężar konfliktu na mniejsze wojny zastępcze**, a nie że
go tłumi. To predykcja o zmianie struktury, nie o spadku liczby — testowana wariantem
T1, nie w liście tłumiącej.

**Obserwacja post-hoc do zbadania na danych wstrzymanych.** W serii `A_COW_P` pasmo
20–32 lat mieści 31,4% mocy wobec 8,9% w paśmie 32–40 (Test 1). Obserwacja
wygenerowana przez dane, **nie hipoteza postawiona przed nimi** — nie wolno jej
testować na tym samym materiale. Droga czysta: UCDP 2008–2024 albo okres przed 1900
zatrzymany jako próba wstrzymana.

---

## D-007 · 2026-08-11 · Wyłączenie kategorii endogenicznych z listy zaburzeń

**Rozstrzygnięcie.** Kategorie `treaty` (3 pozycje) i `energy` (2 pozycje) zostają
usunięte z listy zdarzeń zaburzających. Lista finalna: **34 zdarzenia** w czterech
kategoriach — trzęsienia ziemi (13), pandemie (12), ENSO (5), wulkany (4).

**Uzasadnienie.** Wersja 1.0 protokołu (§3b) wykluczyła „koszty wyczerpania po
wielkich wojnach" jako endogeniczne — zdefiniowane przez samą serię wojenną, więc ich
użycie do wyjaśniania odchyleń tej serii jest kołowe. To samo kryterium stosuje się do
dwóch kategorii, które w szkicu listy zostały uwzględnione niekonsekwentnie:

- **Traktaty rozbrojeniowe** są zawierane w okresach odprężenia, czyli jako skutek
  opadającego napięcia. Wyjaśnianie spadku konfliktowości traktatami odwraca kierunek
  zależności.
- **Szoki naftowe** w naszym oknie są następstwem konfliktów: 1973 — embargo OPEC
  w odpowiedzi na wojnę Jom Kipur, 1979 — rewolucja irańska.

Cztery pozostałe kategorie (aktywność sejsmiczna, wulkaniczna, pandemie, ENSO) są
bezspornie zewnętrzne wobec dynamiki konfliktu.

**Kolejność.** Decyzja zapadła przed obliczeniem jakiejkolwiek statystyki wiążącej
odchylenia z zaburzeniami i wynika z kryterium zadeklarowanego w v1.0, nie
z obserwacji wyniku. Wykrycie niespójności zawdzięczamy przeglądowi listy przez
Claude Code w Etapie A.

**Skutek liczbowy.** Pokrycie 1900–2007 przy L = 5: 79% → **75%**. S(t): średnia
1,35 → **1,12**, odchylenie 1,07 → **0,93**. Zmienność objaśniająca zachowana.

**Konsekwencja uboczna.** Znika jedyna kategoria bez wyczerpującego katalogu, czyli
najbardziej podatna na arbitralność doboru.

---

## D-008 · 2026-08-12 · Parametry analizy wielowariantowej (rodzina 4)

**Kontekst.** Rodzina 4 nie testuje hipotezy — mierzy, ile z dotychczasowych wniosków
jest własnością danych, a ile wyborów przetwarzania. Metoda: multiverse analysis
(Steegen i in. 2016). Siatka: 2 poziomy agregacji × 4 zestawy wag × 2 normalizacje
× 2 wygładzania × 2 detrendingi × 3 okresy = **192 kombinacje**.

**D-A — wariant per capita wchodzi do siatki głównej.**
`population.csv` podaje ludność świata co dekadę do 1940 i rocznie od 1950; na 192 lata
przypada 71 pomiarów. Wariant per capita przed 1950 opiera się więc w ~79% na
interpolacji, która wprowadza sztuczną gładkość o skali dziesięciu lat do mianownika.

Mimo tego wchodzi. Wykluczenie byłoby wyborem podjętym **po** zobaczeniu problemu,
a problem jest opisywalny i zostaje opisany w protokole §2.1. Dodatkowo zarzut Z9
z ADDENDA dotyczy właśnie normalizacji per capita — pominięcie oznaczałoby, że nie
został sprawdzony. Obowiązkowy wariant kontrolny 1950–2007 na danych rocznych.

**D-B — punktem odniesienia w narracji są wagi równe (1/1/1).**
Wagi odziedziczone 1,0/0,7/0,4 raportowane obok jako „specyfikacja oryginalna".
Uzasadnienie: wagi równe nie zawierają założenia; odziedziczone kalibrowano — jak
wykazał Test 0C — na wielkości innej niż deklarowana (ważono uczestniko-lata, opisując
je jako wojno-lata), więc ich uzasadnienie odnosi się do miary, której już nie używamy.

Rozkład obejmuje oba zestawy niezależnie od tej decyzji; dotyczy ona wyłącznie tego,
wobec czego mierzymy odchylenia w opisie.

**Reguła interpretacji zadeklarowana przed uruchomieniem** (protokół §6): poniżej 5%
kombinacji wspierających H1 — hipoteza nie broni się w przestrzeni specyfikacji;
5–25% — broni się w wąskim podzbiorze wymagającym niezależnego uzasadnienia;
powyżej 25% — wynik Testu 1 był specyficzny dla tamtej specyfikacji.

**Zastrzeżenie.** Kombinacje dzielą te same dane, więc odsetek wspierających **nie jest
wartością p** i nie może być tak interpretowany.

---

## D-009 · 2026-08-12 · Luka w projekcie testów: dryf fazy

**Ustalenie.** Test 2B badał jedną z dwóch możliwych postaci twierdzenia o zaburzeniach:
**zaburzoną amplitudę przy zachowanym zegarze**. Nie badał postaci drugiej —
**zaburzonego zegara**, w której zdarzenie zewnętrzne przesuwa szczyt w czasie,
a kolejny odliczany jest od nowej pozycji (okres lokalnie stały, globalnie dryfujący).

**Dlaczego to ma znaczenie.** Postać druga jest bliższa temu, co twierdzi rozdział
III.3.2. Sekcja C9 nie mówi, że wyczerpanie po II wojnie osłabiło kolejny szczyt —
mówi, że kolejne cykle „rozpadły się na serie mniejszych konfliktów", co opisuje
przesunięcie i rozproszenie, nie tłumienie amplitudy. Test 2B zbudowano zatem na
węższej interpretacji własnego tekstu, niż tekst dopuszcza.

**Status wyniku Testu 2B.** Pozostaje w mocy dla tego, co testował, i usuwa jeden
z argumentów obronnych. Nie zamyka drugiego.

**Zastrzeżenie o kolejności.** Ograniczenie analizy widmowej wobec procesów o dryfującej
fazie było zadeklarowane w protokole Testu 1 **przed** jego uruchomieniem (§5,
deklaracja mocy). Niniejszy wpis nie jest wymówką dorobioną po fakcie, lecz odnotowaniem
luki w projekcie testów.

**Warunek konieczny testu na dryf.** Wymaga deklaracji, **ile lat dryfu na cykl jeszcze
mieści się w hipotezie**. Bez tej liczby hipoteza przestaje cokolwiek przewidywać —
cykl mogący przesunąć się dowolnie jest nieodróżnialny od procesu bez cyklu. Liczba
jest decyzją merytoryczną, zastrzeżoną dla autora, i musi zostać zapisana przed
uruchomieniem testu. **Status: nierozstrzygnięta.**

---

## D-010 · 2026-08-14 · Wycofanie zarzutu o dominacji wojen światowych

**Kontekst.** D-002 zapisało zastrzeżenie obowiązkowe do hipotezy H2: „na poziomie
uczestnika I i II wojna światowa wnoszą po kilkanaście–kilkadziesiąt wierszo-lat i leżą
blisko siebie fazowo. Profil złożony zdominowany przez dwa zdarzenia **nie jest** dowodem
okresowości." Na tej podstawie zaplanowano test z wyłączeniem lat 1914–1918 i 1939–1945.

**Ustalenie — zarzut nietrafny.** Kontrola wykonalności przed Testem 4:

| seria | 12 najwyższych lat epoki 2 | wojen światowych wśród 20 najwyższych |
|---|---|---|
| `A_COW_P` | 1991, 1941, 1970, 1971, 1918, 1973, 1919, 1920, 1945, 1953, 1952, 1944 | 8/20 |
| `A_COW_W` | 1920, 1992, 1991, 1978, 1987, 1982, 1979, 1999, 1919, 1986, 1983, 1993 | **0/20** |

Maksimum serii uczestniczej wypada na **1991** (koalicja Zatoki Perskiej), nie na wojnę
światową. W serii wojno-poziomowej rok 1942 ma wartość **1,0** — najniższą w stuleciu,
bo II wojna światowa jest *jedną* wojną. Wyłączenie 12 lat usuwa 19% masy epoki 2
(`A_COW_P`) i 6,9% (`A_COW_W`).

**Struktura epoki 2 nie jest zdominowana przez dwa zdarzenia.** Zastrzeżenie z D-002
w tej postaci zostaje **wycofane**.

**Zarzut w postaci właściwej.** Pytanie brzmi nie „czy to dwie wojny światowe", lecz
**ile obserwacji trzeba usunąć, żeby kontrast zniknął**. Test 4 bada odporność na wpływ
obserwacji odstających (krzywa M2 przy usuwaniu k najwyższych lat, k = 0…10), z pasmem
odniesienia z usuwania k lat losowych. Wariant z wyłączeniem wojen światowych zachowany
jako rozbrojenie zarzutu, który i tak zostanie postawiony publicznie.

**Obserwacja uboczna do zbadania.** Szczyty serii uczestniczej w epoce 2 wypadają
w okolicach 1918–1920, 1941–1945, 1952–1953, 1970–1973 i 1991 — odstępy rzędu 23, 11,
18 i 20 lat. Nie jest to rytm 35-letni. Zgodne z Testem 3, gdzie kontrast pojawiał się
przy T = 32 (26/64 kombinacji) i nie pojawiał się nigdy przy T = 40 (0/64). Obserwacja
post-hoc, do zbadania wyłącznie na danych wstrzymanych (por. D-006).

---

## D-011 · 2026-08-15 · Przejście od testu jednego okresu do skanu ze statystyką maksymalną

**Kontekst.** Testy 1, 3 i 4 badały wyłącznie pasmo 32–40 lat, przyjęte z Tryptyku.
Po wyniku negatywnym (Test 3: 0/192) autor postawił pytanie o inne okresy, wskazując
intuicyjnie ok. 18 lat.

**Rozstrzygnięcie.** Nie testujemy okresu 18 lat osobno. Uruchamiamy **skan po całym
zakresie 8–60 lat** (Test 5) z modelem zerowym zbudowanym na **statystyce maksymalnej
po skanie** — korekta na wielokrotne testowanie jest wtedy wbudowana w konstrukcję testu,
a nie doklejona po fakcie.

**Uzasadnienie.** Testowanie wielu hipotez jest praktyką normalną; problemem jest
raportowanie najlepszej jako jedynej. Przy ~21 niezależnych częstotliwościach w zakresie
8–60 lat jeden okres wypadnie „istotnie" przypadkiem. Porównanie maksimum z danych
z rozkładem **maksimów** surogatów rozwiązuje to konstrukcyjnie (Davies 1977/1987;
Baluev 2008).

**Status liczby 18.** Nie jest hipotezą prerejestrowaną. Pochodzi z obserwacji odstępów
między szczytami serii uczestniczej w epoce 2 (ok. 23, 11, 18, 20 lat) — czyli z danych,
które już wykorzystaliśmy. Wchodzi do skanu na równych prawach z każdym innym okresem.

**Sprostowanie do wcześniejszego rachunku.** Odstępy między oknami C1–C8 (mediana
19,5 roku), przywoływane jako niezależne wsparcie dla ok. 18–20 lat, **zostały wycofane
w D-006** — sekcje C opisują fazy przebiegu krzywej, nie punkty szczytowe. Ten rachunek
nie może być źródłem hipotezy.

**Deklaracja mocy przed uruchomieniem.** W paśmie 12–20 lat przypada 6,40 komórki
rozdzielczej i 10–16 powtórzeń w szeregu 192-letnim, wobec 1,73 komórki i 4,3–6,0
powtórzeń w badanym dotąd paśmie 32–45 lat. Moc jest tam **nieporównanie wyższa** —
co znaczy również, że **wynik negatywny Testu 5 będzie znacznie mocniejszy** niż wynik
negatywny Testu 1: brak sygnału w paśmie krótkookresowym nie da się usprawiedliwić
krótkością szeregu.

**Zakres i krok zamrożone** (8–60 lat, krok 0,5 roku, 105 punktów). Zmiana zakresu po
zobaczeniu wyniku zmienia rozkład statystyki maksymalnej i unieważnia korektę.

---

## D-012 · 2026-08-22 · Zejście z poziomu świata na poziom diady

**Kontekst.** Testy 1, 3 i 5 wykazały brak okresowości w zagregowanym szeregu światowym
w całym zakresie 8–60 lat. Autor wskazał, że agregacja globalna może wygaszać rytm:
jeżeli każda para przeciwników ma własny cykl o innej fazie, ich suma jest
nieodróżnialna od szumu.

**Rozstrzygnięcie.** Test 6 schodzi na poziom **pary państw** i bada inną wielkość —
**strukturę odstępów między konfliktami**, nie okres w szeregu rocznym.

**Odstęp liczony od KOŃCA jednego konfliktu do POCZĄTKU następnego** (decyzja autora,
przyjęta). Uzasadnienie: przy mechanizmie regeneracyjnym zegar rusza w momencie
zakończenia wojny; liczenie start→start mieszałoby czas trwania z czasem regeneracji.

**Ciągłość państw odziedziczona po COW.** Kody realizują ciągłość wskazaną przez autora
bez naszej ingerencji: Rosja/ZSRR = 365, Prusy/Niemcy = 255, Osmanie/Turcja = 640.
Decyzja pochodzi od twórców zbioru, co usuwa ryzyko dostrajania definicji pod wynik.
Zakres: jest to konwencja kodowania jednostki politycznej, **nie** twierdzenie
o tożsamości ani podmiotowości państwa; test nie orzeka o takich kwestiach.

**UJAWNIENIE.** Przy kontroli wykonalności policzono współczynniki zmienności odstępów
dla pięciu mocarstw: Rosja 0,85, Turcja 0,59, Niemcy 0,91, Francja 0,95, W. Brytania 0,76
— wszystkie poniżej 1. **Liczby te były znane przed zamrożeniem protokołu.** Nie są
wynikiem: policzono je bez modelu zerowego, bez korekty na cenzurowanie i bez korekty
na wielokrotność. Statystyka pierwszorzędna (parametr kształtu Weibulla) i modele zerowe
wybrano niezależnie od nich — są standardem dla tego pytania (Cox & Oakes 1984).
Dobór jednostek odbywa się wyłącznie progiem liczbowym; nazwy par wymienione w rozmowie
nie są listą wejściową.

**Cenzurowanie jako element konieczny.** Po 1945 większość europejskich par przestała
walczyć, więc ostatni odstęp każdej pary jest cenzurowany prawostronnie. Pominięcie tych
obserwacji zaniżałoby średni odstęp i **zawyżało pozorną regularność** — działałoby na
korzyść hipotezy. Estymacja z cenzurowaniem obowiązkowa; wariant bez niego raportowany
jawnie jako obciążony i nie może być jedynym osiągającym istotność (§8).

**Zależność diad.** Rosja występuje w kilku parach naraz, a te same wojny światowe wnoszą
odstępy do wielu diad. Obowiązkowy bootstrap na poziomie diad.

**Zmienne ekonomiczne** (straty wobec potencjału gospodarczego) poza zakresem tej wersji —
szeregi PKB dla 1816–2007 są niekompletne i wymagają własnej warstwy danych.

---

## D-013 · 2026-08-23 · Odstępy ujemne i zerowe w rodzinie 9: scalanie w epizody, próg na epizodach

**Kontekst.** `TEST6_DATA_REPORT.md` §6 zgłosił 11 odstępów niedodatnich na 62 pełnych
(8 ujemnych, 3 zerowe), wszystkie pochodzące z konfliktów nakładających się, jednoczesnych
albo z jednej wojny policzonej dwukrotnie wskutek zmiany strony (Bułgaria w II wojnie
światowej). Analiza przeżycia wymaga czasu oczekiwania > 0, więc wartości te nie mogą wejść
jako surowe. Code zatrzymał się zgodnie z §A2 i nie rozstrzygał sam.

### Rozstrzygnięcie

**1. Scalanie w epizody.** Konflikty tej samej diady, których przedziały trwania nachodzą
na siebie lub stykają się, tworzą **jeden epizod**. Epizod = przedział od najwcześniejszego
początku do najpóźniejszego końca w scalanej grupie.

**2. Definicja odstępu bez zmian.** Odstęp liczony od **końca epizodu** do **początku
epizodu następnego**. Po scaleniu żaden odstęp nie może być niedodatni; jeśli po
przebudowie taki się pojawi, jest to błąd implementacji, nie danych — zgłosić, nie łatać.

**3. Próg ≥ 3 stosowany do epizodów, nie do surowych wierszy.** Jednostką analizy jest czas
oczekiwania, więc próg zawsze powinien był dotyczyć epizodów; zastosowanie go do wierszy
pliku było wyborem niezadeklarowanym. Diady spadające poniżej progu po scaleniu wypadają
ze zbioru — z jawną listą w raporcie.

**4. Wariant wrażliwości.** Osobne uruchomienie z progiem liczonym na surowych wierszach
(zbiór szerszy) raportowane obok, poza regułą decyzyjną §8. Ma pokazać, czy rozstrzygnięcie
progu przesądza wynik.

**5. Cenzurowanie bez zmian.** Jeden odstęp cenzurowany na diadę, od końca ostatniego
epizodu do końca zakresu zbioru (2007 dla `Inter-StateWarData_v4.0.csv`). Obowiązkowe,
zgodnie z §4 protokołu.

### Uzasadnienie

Kryterium nie jest nowe. §2 protokołu definiuje mierzoną wielkość jako **czas regeneracji**:
zegar rusza, gdy walka ustaje. Dwa konflikty nachodzące na siebie w czasie nie rozdzielają
się okresem regeneracji, więc nie są dwoma czasami oczekiwania — są jednym okresem walki
opisanym w bazie dwoma wierszami. Scalanie stosuje istniejącą definicję konsekwentnie;
pozostałe dwie drogi jej nie stosują.

**Droga odrzucenia (opcja 1) ma określony kierunek obciążenia i jest on korzystny dla
hipotezy.** Usuwa wyłącznie okresy najintensywniejsze, pozostawiając odstępy liczone od
błędnych kotwic, co skraca ogon rozkładu i obniża współczynnik zmienności — czyli podnosi
pozorną regularność. **Droga podłogi (opcja 3)** wpisuje do zbioru wartości, których w
danych nie ma.

Scalanie jest przy tym **ostrożniejsze niż odrzucenie**: daje mniej obserwacji (grupa k
nachodzących konfliktów wnosi k−1 odstępów mniej), a każdy pozostały odstęp jest zakotwiczony
poprawnie. Kierunek jego wpływu na parametr kształtu nie jest przesądzony a priori — i to
jest zaleta wobec opcji 1.

### Kolejność i ujawnienie

Decyzja zapada **przed** policzeniem parametru Weibulla i przed napisaniem kodu testu; Code
zatrzymał się na STOP i żadnej statystyki testowej nie wyliczono.

**Ujawnienie wymagane przez zakaz nr 10:** w chwili podejmowania decyzji znane były
współczynniki zmienności policzone w Etapie A — pulowy CV odstępów dodatnich 0,901 wobec
1,181 przy włączeniu wartości niedodatnich (`TEST6_DATA_REPORT.md` §4). Są to statystyki
opisowe bez modelu zerowego i bez cenzurowania, ale zostały obejrzane i musi to być
zapisane. Uzasadnienie rozstrzygnięcia odwołuje się wyłącznie do §2 protokołu, nie do
tych liczb.

### Skutek liczbowy (do uzupełnienia po przebudowie)

Zbiór wejściowy przed decyzją: 25 diad, 62 odstępy pełne, 25 cenzurowanych, z czego
11 odstępów niedodatnich. Po scaleniu spodziewane jest zmniejszenie liczby epizodów w
diadach China–Japan, USSR–China, USSR–Japan, Germany–USSR, USSR–Finland, USA–Vietnam,
Cambodia–Vietnam oraz w trzech diadach bułgarskich (Bulgaria–Romania, France–Bulgaria,
Italy–Bulgaria). Trzy ostatnie mogą spaść poniżej progu, ponieważ ich powtórzenie wynikało
z jednej wojny policzonej dwukrotnie po zmianie strony.

### Konsekwencje uboczne

**Porównanie z §0.2 przestaje być bezpośrednie.** Współczynniki zmienności z §0.2 policzono
najprawdopodobniej po pominięciu nakładań (droga 1), a nie po scaleniu. §0.2 pozostaje
punktem odniesienia dokumentacyjnym, nie celem do odtworzenia — raport ma podać obie
wielkości obok siebie i nie traktować rozbieżności jako błędu.

**Ograniczenie nr 3 protokołu pozostaje w mocy i się pogłębia.** Próg wybiera pary walczące
często; scalanie dodatkowo zmniejsza liczbę epizodów właśnie u par o konfliktach gęstych.
Kierunek obciążenia bez zmian — w stronę pozornej regularności.
