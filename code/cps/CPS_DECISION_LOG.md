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

---

## D-014 · 2026-08-23 · Odstęp liczony jako czas ekspozycji, nie jako różnica dat

**Kontekst.** Przegląd przebudowanej warstwy danych Testu 6 (`TEST6_DATA_REPORT.md` v2,
builder v2.0) wykazał, że odstępy i czasy cenzurowane liczone są w latach kalendarzowych,
bez kontroli, czy w tych latach **obie strony diady są członkami systemu państw COW**.
`system2016.csv` pokazuje, że w kilku przypadkach nie są.

### Rozstrzygnięcie

**1. Definicja odstępu.** Odstęp między epizodami oraz odstęp cenzurowany liczony jest jako
**liczba lat ekspozycji** — lat w przedziale, w których **oba** kody państw występują w
`system2016.csv` — a nie jako różnica dat kalendarzowych.

**2. Wariant kalendarzowy** (obecna definicja) zostaje jako wrażliwość, raportowany obok,
poza regułą decyzyjną §8 protokołu.

**3. Kontrola.** Jeżeli po korekcie jakikolwiek odstęp **pełny** miałby ekspozycję zero,
kod zatrzymuje się i zgłasza — oznaczałoby to konflikt między zbiorem wojen a zbiorem
członkostwa. Odstęp **cenzurowany** o ekspozycji zero jest dopuszczalny i wnosi do
log-wiarygodności log S(0) = 0, czyli nic; diada pozostaje w zbiorze przez swoje odstępy pełne.

### Uzasadnienie

Kryterium nie jest nowe. §2 protokołu definiuje mierzoną wielkość jako **czas regeneracji**
między konfliktami tej samej pary. Para, której jedna strona nie istnieje jako podmiot
systemu międzynarodowego, nie jest w tym czasie narażona na konflikt — brak wojny między
stronami, z których jedna nie istnieje, nie jest obserwacją o czasie oczekiwania. Liczenie
takich lat jest tą samą klasą błędu co obsługa kodu −7 w wersji v0.1 (F1): kod przypisuje
danym treść, której one nie mają.

### Skutek liczbowy

Dotkniętych jest 9 z 63 obserwacji, wszystkie z ogona rozkładu:

| diada | typ | lata kalendarzowe | lata ekspozycji | przyczyna |
|---|---|---|---|---|
| Austria-Hungary–Italy | cenzurowany | 89 | **0** | ccode 300 opuszcza system w 1918 |
| France–Germany | cenzurowany | 62 | **18** | ccode 255 nieobecny 1945–1990 |
| Germany–Yugoslavia | pełny 1945→1999 | 54 | **10** | ccode 255 nieobecny 1945–1990 |
| Spain–Morocco | pełny 1910→1957 | 47 | **4** | ccode 600 nieobecny 1912–1956 |
| China–Japan | cenzurowany | 62 | 56 | ccode 740 nieobecny 1945–1952 |
| USSR–Japan | cenzurowany | 62 | 56 | ccode 740 nieobecny 1945–1952 |
| Greece–Turkey | cenzurowany | 85 | 83 | ccode 350 nieobecny 1941–1944 |
| Yugoslavia–Turkey | pełny 1918→1999 | 81 | 79 | ccode 345 nieobecny 1941–1944 |
| Syria–Israel | pełny 1949→1967 | 18 | 16 | ccode 652 nieobecny 1958–1961 |

Sumy: odstępy pełne 839 → **748** lat, cenzurowane 956 → **809** lat.

### Kolejność i ujawnienie

Decyzja zapada przed policzeniem parametru Weibulla i przed napisaniem kodu testu; Code
zatrzymał się na STOP po Kroku 1 i żadnej statystyki testowej nie wyliczono.

**Ujawnienie wymagane przez zakaz nr 10:** przed sformułowaniem tego rozstrzygnięcia
policzono pulowy współczynnik zmienności odstępów pełnych w obu wersjach — **0,955**
kalendarzowo i **0,983** po korekcie ekspozycji (n = 45 w obu przypadkach). Różnica jest
znikoma, obie wartości leżą blisko jedności, a uzasadnienie odwołuje się wyłącznie do §2
protokołu — ale liczby zostały obejrzane i musi to być zapisane.

### Konsekwencje uboczne

**Ograniczenie zakresu, o którym trzeba napisać wprost.** Po korekcie Francja–Niemcy ma
osiemnaście lat ekspozycji od 1945, nie sześćdziesiąt dwa, ponieważ COW nie zna
zjednoczonych Niemiec w latach 1945–1990 (RFN 260 i NRD 265 to inne kody). Twierdzenie o
konsolidacji Europy po II wojnie światowej jest w tym zbiorze **niemierzalne** dla par
niemieckich; wariant epokowy S6 (podział 1945) musi to odnotować jako ograniczenie danych,
a nie prezentować jako wynik.

**Kierunek obciążenia progu epizodowego (D-013) jest teraz znany.** Siedem diad, które
wypadły po scaleniu, to dokładnie pary o konfliktach nachodzących na siebie, czyli
najsilniej zgrupowane w całym zbiorze (USA–Vietnam: trzy konflikty w dziesięć lat, jeden
epizod, zero odstępów pełnych). Grupowanie jest hipotezą alternatywną wobec rytmu, więc
reguła progowa usuwa selektywnie świadectwa przeciwko hipotezie. Reguły **nie zmieniamy** —
byłaby to zmiana po zobaczeniu, które diady wypadły — ale wariant wrażliwości z progiem na
wierszach surowych przestaje być formalnością i musi być raportowany na równi z wynikiem
głównym, z jawnie nazwanym kierunkiem obciążenia.

**Sprostowanie (D-017): wniosek liczbowy powyżej jest błędny.** Zobacz D-017.

---

## D-017 · 2026-08-23 · Sprostowanie D-014: kierunek obciążenia progu epizodowego jest nieustalony

**Kontekst.** D-014 („konsekwencje uboczne") stwierdziła, że próg epizodowy (D-013) „usuwa
selektywnie świadectwa przeciwko hipotezie" i że kierunek obciążenia jest „teraz znany" —
w stronę korzystną dla hipotezy H1 rodziny 9. Argument strukturalny (siedem odrzuconych diad
to najsilniej zgrupowane pary w zbiorze) jest poprawny. **Wniosek liczbowy nie jest.**

### Sprostowanie

Sześć odstępów pełnych, które wariant S-B dokłada do zbioru głównego (18 diad → 25 diad),
wynosi **2, 19, 19, 21, 21 i 29 lat**. Pięć z sześciu leży blisko średniej zbioru głównego
(16,6 roku) i powyżej jego mediany (11 lat). Ich włączenie **obniża** pulowy CV z 0,983
(główny) do 0,926 (S-B) — zbiór wygląda **bardziej** regularny po dołożeniu tych odstępów,
nie mniej. Para faktycznie najsilniej zgrupowana, USA–Vietnam, **nie wnosi żadnego odstępu
pełnego w żadnym wariancie** — po scaleniu ma jeden epizod, więc nie ma czego wnieść.

Próg nie usuwa w rozpoznany sposób świadectw przeciwko regularności — usuwa parę bez
odstępów w ogóle (USA–Vietnam) i pary, których dołożone odstępy akurat zbliżają zbiór do
średniej. **Kierunek obciążenia progu epizodowego jest nieustalony**, nie „znany i
niekorzystny dla wiarygodności wyniku pozytywnego".

### Co zostaje w mocy

Wymóg raportowania S-B na równi z wynikiem głównym w Etapie C **nie zmienia się** — ale
uzasadnienie jest inne: nie dlatego, że S-B ujawnia ukryte świadectwa przeciwne hipotezie,
lecz dlatego, że próg widocznie przesuwa CV (w tym wypadku w dół, nie w górę) i wyboru
między wariantami nie wolno dokonywać po zobaczeniu wyniku (zakaz nr 5, protokół rodziny 9).

### Pochodzenie

Błąd wykryty w przeglądzie przed otwarciem rodziny 9b (D-016), nie przez Code. Sprostowanie
dotyczy wyłącznie interpretacji liczb już policzonych w Kroku 1b — nie wymaga przebudowy
zbioru ani nowego biegu.

---

## D-015 · 2026-08-23 · Etap B Testu 6: model orzekający, założenia zegara i dyskretyzacji

**Kontekst.** `TASK_6B_BRIEF.md` otwiera Etap B (kod estymacji Weibulla, bez uruchamiania na
danych rzeczywistych) i wprowadza dwa rozstrzygnięcia numerowane jako D-015, poza już
przyjętymi D-012–D-014. Wpis rejestruje je w formie, w jakiej zostały podane w briefie.

### D-015 A — założenia estymacji, do nazwania w kodzie i w raporcie

**1. Zegar zatrzymany, nie wyzerowany.** Odstęp o przerwanej ekspozycji (lata, w których
jedna ze stron diady nie jest członkiem systemu COW, D-014) liczy się jako jeden czas
oczekiwania równy **sumie** lat ekspozycji — proces podejmuje odliczanie tam, gdzie je
przerwał, nie od zera. Przy modelu Weibulla to nie jest założenie puste, bo hazard zależy
od czasu, jaki już upłynął od poprzedniego zdarzenia. Brief podaje, że dotyczy to pięciu
obserwacji; nie rederywuję tu samodzielnie, które to konkretnie pięć spośród dziewięciu
obserwacji dotkniętych przez D-014 — patrz zastrzeżenie niżej.

**2. Dyskretyzacja.** Odstępy są zapisane w pełnych latach, a model jest ciągły (Weibull).
Dla najkrótszych odstępów (minimum 1 rok) różnica między czasem dyskretnym a ciągłym nie
jest zaniedbywalna. Przyjmuje się to jako **zadeklarowane założenie**, nie jako coś do
korygowania (np. przez losowe rozmycie wewnątrz roku).

### D-015 B — dwa dopasowania, role nierówne

**P1 (Weibull pulowany, bez kruchości) ORZEKA** dla H9 (protokół §8). **F1 (Weibull z
kruchością gamma dzieloną w obrębie diady) jest wariantem drugorzędnym**, nie
równorzędnym — liczony wyłącznie na zbiorze głównym, nie na wariantach wrażliwości S-A/S-B.
Rozbieżność między P1 i F1, jeśli wystąpi, czytana jest wg reguły zadeklarowanej w D-015
**przed** biegiem, w czterech przypadkach (brief §6) — **nie po zobaczeniu wyniku**.

**Zastrzeżenie do uzupełnienia.** Tekst czterech przypadków interpretacji rozbieżności
P1/F1 nie został przekazany Code'owi w treści `TASK_6B_BRIEF.md` — jest tam wyłącznie
przywołany przez odniesienie. Etap B (pisanie kodu) tego nie wymaga: reguła dotyczy
czytania wyniku w Etapie C, nie implementacji estymatora. Nie jest tu domyślana ani
wymyślana — zgłoszona jako brak, do uzupełnienia przed Krokiem 3.

---

## D-016 · 2026-08-23 · Populacja rodziny 9b: rywalizacje przestrzenne zamiast progu liczby wojen

*(Dopisane po D-017 z powodu kolejności, w jakiej wpisy dotarły do Code'a — numer
zachowany jak nadany w źródle, zgodnie z precedensem D-007, który też wszedł do rejestru
po numerach wyższych od siebie. D-017 poprawia D-014 i nie wynika logicznie z D-016 —
to dwa niezależne wpisy z tego samego dnia.)*

**Kontekst.** Test 6 (rodzina 9) wchodzi do zbioru przez próg „≥ 3 wspólne konflikty". Próg
ten był zadeklarowany od D-012 wraz z jego znanym ograniczeniem: wybiera pary walczące często
i obciąża wynik w stronę pozornej regularności. Ma jednak wadę poważniejszą, wpisaną
w ograniczenia od początku — **selekcjonuje po tej samej wielkości, którą mierzy**. Pary
wybieramy według liczby konfliktów, a badamy odstępy między konfliktami.

Uwagi autora z 2026-08-23 wskazały trzy niezależne problemy z obecną definicją diady:
brak wymogu wspólnej stawki, mieszanie mocarstw z resztą, oraz status wojen światowych jako
zdarzenia synchronizującego, które tworzy pary pozorne. Wszystkie trzy dotyczą **doboru
populacji**, nie modelu.

### Rozstrzygnięcie

**Nowy test (rodzina 9b) dobiera diady przez przynależność do rywalizacji strategicznych
o składniku przestrzennym, bez jakiegokolwiek progu liczby wojen.**

Źródło: Thompson, Sakuwa i Suhas (2021), *Strategic Rivalries*, 1494–2020, w postaci
maszynowej rozprowadzanej z pakietem `peacesciencer` (obiekt `tss_rivalries`, 264 rywalizacje).
Kryterium: znacznik `spatial = 1`.

**Test 6 pozostaje bez zmian** i zostaje dokończony na swojej pierwotnej populacji. Rodzina 9b
jest osobnym testem o osobnym protokole, nie poprawką.

### Uzasadnienie

**1. Kryterium jest niezależne od mierzonej wielkości.** Kodowanie Thompsona powstaje
z odczytu relacji dyplomatycznych — z tego, czy strony wzajemnie traktowały się jako
zagrożenie — a nie z liczenia sporów. Zrywa to koło, w którym tkwi Test 6. Z tego samego
powodu **wyklucza się użycie rywalizacji trwałych Diehla i Goertza**, które definiuje się
przez gęstość sporów w oknie czasowym; jako filtr byłyby dla tego pytania tautologią.

**2. Znacznik przestrzenny operacjonalizuje „wspólną strefę konfliktu" bez definicji własnej.**
Kontrola: USA–ZSRR figuruje jako rywalizacja, ale ze składnikiem przestrzennym równym zero
(pozycyjna, ideologiczna, interwencyjna) — znacznik oddziela spór o wspólny obszar od
projekcji siły na odległość, czyli robi dokładnie to, o co chodziło.

**3. Kryterium jest binarne, nie kategoryzujące.** Typ przedmiotu sporu nie wchodzi do
selekcji. Dziewięć wojen o minerały nie jest osobną populacją, tylko podzbiorem; dzielenie
po typach zasobu zniszczyłoby próbę tak samo jak stratyfikacja po mocarstwach.

### Skutek liczbowy — populacja i okno ryzyka

| wielkość | wartość |
|---|---|
| rywalizacje przestrzenne (wiersze) | 152 |
| **unikalnych diad** | **141** |
| diady z niepustym oknem ryzyka w latach 1816–2007 | **129** |
| sumaryczne lata ryzyka | 6 232 |
| mediana długości okna | 31 lat (kwartyle 13,5 / 61; maks. 176) |
| rywalizacje rozpoczęte przed 1816 | 18 |
| rywalizacje trwające po 2007 | 36 |

Dla porównania, populacja przez próg liczby wojen: 342 diady kiedykolwiek walczące,
z tego 60 z ≥ 2 wojnami i 23 z ≥ 3 (obecny Test 6).

**Diady przecinające oba kryteria:** spośród 141 rywalizacji przestrzennych 71 miało
co najmniej jedną wojnę międzypaństwową COW, a **30 co najmniej dwie** (łącznie 90 wojen).

### Co ta zmiana daje

**Obserwacje cenzurowane, których dotąd nie widzieliśmy.** Siedemdziesiąt rywalizacji
przestrzennych nie doszło do wojny ani razu. W układzie z progiem są niewidoczne; tutaj są
pełnoprawnymi obserwacjami cenzurowanymi — parami, które miały wspólną stawkę i mimo to
nie walczyły. Jest to najmocniejsza informacja o czasie oczekiwania, jaką można mieć, i jej
pominięcie było źródłem obciążenia w Teście 6.

**Więcej grup dla modelu kruchości.** Trzydzieści diad z co najmniej dwiema wojnami wobec
osiemnastu w Teście 6, a przy uwzględnieniu odstępów od początku rywalizacji — do 129.
Identyfikowalność parametru kruchości zależy od liczby grup, nie tylko obserwacji.

**Okno ryzyka wyznaczone przez rywalizację, nie przez zakres zbioru.** W Teście 6 zegar
cenzurowania biegnie do 2007 niezależnie od tego, czy para wciąż ma o co walczyć. Tutaj okno
domyka się z chwilą wygaśnięcia rywalizacji.

### Kontrole zgodności wykonane przed zamrożeniem

| sprawdzenie | wynik |
|---|---|
| USA–Wietnam | **nie figuruje** w zbiorze rywalizacji — zgodnie z zastrzeżeniem autora |
| USA–ZSRR | rywalizacja, ale `spatial = 0` — znacznik działa zgodnie z zamiarem |
| Niemcy–Polska, Francja–Anglia | **obie są rywalizacjami przestrzennymi** — ich brak w Teście 6 wynika z okna czasowego COW, nie z pojęcia |
| pary powstałe z koalicji II wojny (Francja–Bułgaria, Włochy–Bułgaria, ZSRR–Finlandia) | **nie są rywalizacjami** — filtr usuwa artefakty synchronizacji samodzielnie |
| 18 diad zbioru głównego Testu 6 | 17 przechodzi filtr rywalizacji, 16 ma składnik przestrzenny |

### Ujawnienie

Wszystkie liczby powyżej dotyczą **składu populacji**, nie hipotezy. Przed zamrożeniem tego
rozstrzygnięcia **nie policzono żadnej statystyki czasów oczekiwania** na zbiorze
przefiltrowanym — ani współczynnika zmienności, ani parametru kształtu, ani niczego, co
wchodzi do reguły decyzyjnej. Ta granica jest tu istotna: po jej przekroczeniu nie dałoby się
już uczciwie wybierać między wariantami definicji filtru.

Znane były natomiast wyniki Testu 6 do poziomu współczynników zmienności (0,983 / 0,955 /
0,926) oraz dekompozycja wariancji między diadami.

### Zastrzeżenia zapisane z góry

**Kodowanie Thompsona jest osądem z historii dyplomatycznej, nie pomiarem.** Daty początku
i końca rywalizacji mają niepewność, której zbiór nie kwantyfikuje. Wariant kontrolny na
wcześniejszej wersji (Thompson i Dreyer 2012, 197 rywalizacji) ma pokazać wrażliwość na to
kodowanie.

**Lewostronne ucięcie.** Osiemnaście rywalizacji przestrzennych zaczyna się przed 1816 rokiem,
czyli przed początkiem zbioru COW. Dla nich okno ryzyka otwiera się w 1816, a pierwszy
obserwowany odstęp nie jest odstępem od początku rywalizacji. Musi to być obsłużone jako
ucięcie, nie zignorowane.

**Niezależność diad pozostaje naruszona.** Ustalenie z Testu 6 — 27% epizodów kończy się
w 1918 albo 1945 — dotyczy tak samo tej populacji. Wojny światowe narzucają wspólny zegar
parom skądinąd niezależnym. Problem nierozwiązany, do nazwania w raporcie.

---

## D-018 · 2026-08-23 · Status zmiennej COLOR: obciążenie datowaniem publikacji

**Kontekst.** Dotychczasowy zapis oznaczał kierunek wojny→COLOR (istotny, p<0,01, opóźnienia
1–6) jako niecytowalny z jednego powodu — częściowe liczenie na MA(11) centrowanej, która
przecieka informacją z przyszłości. Pełna treść ustalenia: `ERRATA_COLOR_datowanie.md`.

**Ustalenie.** Jest drugi, poważniejszy powód, którego nie da się usunąć filtrem. Szereg
COLOR (korpus Google Books) datuje **publikację**, nie **wypowiedzenie** retoryki — mowy,
depesze i wspomnienia są najpierw wygłaszane, potem drukowane, z opóźnieniem które jest
(1) jednostronne — publikacja nigdy nie wyprzedza wypowiedzenia, (2) nieznane co do
wielkości w tych danych, (3) niestacjonarne — tempo druku i zasięg nakładów zmieniały się
radykalnie między 1816 a 2007.

**Konsekwencja.** Wynik „wojny wyprzedzają COLOR na opóźnieniach 1–6" jest nieodróżnialny od
tego, czego należałoby oczekiwać, gdyby retoryka wyprzedzała wojny, a druk opóźniał jej zapis
o kilka lat. To nie jest świadectwo przeciw hipotezie wyprzedzającej retoryki — to brak
świadectwa w którąkolwiek stronę. Dotyczy wszystkich wyników z COLOR jako zmienną czasową
(Granger w obu kierunkach, korelacja skrośna, kointegracja), nie tylko jednego testu.

**Rozstrzygnięcie.** Zmienna COLOR pozostaje użyteczna jako **wskaźnik poziomu**, nie jako
**wskaźnik momentu**. Test wyprzedzenia retoryki (roboczo Test 8) **nie ma sensu przed
korektą datowania** — dałby wynik metodologicznie poprawny i pusty. Droga wyjścia (oszacowanie
rozkładu opóźnienia wydawniczego na próbie z obiema datami, test na paśmie prawdopodobnych
opóźnień zamiast jednej liczbie) opisana w `ERRATA_COLOR_datowanie.md` §6; kryterium
rozstrzygające zadeklarowane tam z góry (§6): odwrócenie kierunku przy przesunięciu o 3 lata
w granicach prawdopodobnego opóźnienia = mierzymy datowanie wydawnicze, nie relację czasową.

**Zakres.** Niezależne od Testu 6 i Testu 7 — dotyczy rozdziału III.3.2 i każdego zdania
przypisującego COLOR rolę wyprzedzającą albo nadążającą. Nie blokuje żadnego z bieżących
testów rodziny 9/9b, które nie używają COLOR.

---

## D-019 · 2026-08-24 · Obecność na `main` nie oznacza akceptacji: PR #15 (Test 6) zmergowany bez przeglądu kodu

**Kontekst.** Przy scalaniu PR #14 (infrastruktura współdzielona, D-016–D-018) do `main`
zmergowany został równolegle **PR #15**, obejmujący całą zawartość gałęzi
`claude/cps-test-6` — w tym `test6_weibull.py`, `test6_weibull.md` i wszystkie wyniki
Etapu B (Krok 2). Nie był to świadomy akt akceptacji kodu: przegląd Etapu B, wymagany przez
`TASK_6B_BRIEF.md` §8 („Krok 2... STOP — przegląd kodu") przed Krokiem 3, **nie odbył się**.

**Rozstrzygnięcie.** Obecność kodu Testu 6 na `main` od tego momentu **nie jest** tożsama
z zatwierdzeniem Etapu B. Krok 3 (bieg P1/F1/S-A/S-B na `test6_intervals*.csv`) pozostaje
**zablokowany** do czasu odrębnego, jawnego przeglądu — dokładnie tego samego, którego
wymagałby brief, gdyby merge nastąpił po nim, a nie przed. Merge PR #15 **nie jest cofany**:
nic nie zostało jeszcze policzone na danych rzeczywistych, więc revert kosztowałby więcej
(rozdwojenie historii, ponowne rozstrzyganie tego samego kodu na innej gałęzi) niż daje.

**Co ma zostać przedstawione do przeglądu przed odblokowaniem Kroku 3:**

1. `test6_weibull.py` + bliźniaczy `test6_weibull.md` — kod czterech dopasowań (P1, F1, S-A,
   S-B), przedziałów ufności (profil wiarygodności, bootstrap diadowy).
2. Wynik testu granicy θ→0: log-wiarygodność z kruchością (θ=1e-6) zgodna z pulowaną co do
   ~6 miejsc po przecinku, przy tych samych `k`, `λ`.
3. Wynik testu odzysku parametrów na danych syntetycznych o strukturze zbioru rzeczywistego
   (18 grup, 45 zdarzeń pełnych, 18 obserwacji cenzurowanych), dla co najmniej trzech
   zestawów `(k,θ)`, w tym `k=1` i `θ=0`.

Oba testy poprawności zostały już wykonane i są udokumentowane w `test6_weibull.md` §5 —
nie wymagają ponownego liczenia, wymagają **przeglądu przez autora**, zanim Krok 3 ruszy.

**Uzasadnienie.** Symulacja odzysku parametrów pokazuje szerokość przedziału ufności
niezależnie od tego, co powiedzą dane rzeczywiste — bez jej przeglądu wynik nierozstrzygający
z Kroku 3 byłby nieodróżnialny od wyniku źle policzonego. Zatwierdzenie kodu musi poprzedzać
jego uruchomienie na danych, niezależnie od tego, na której gałęzi kod fizycznie leży.

---

## D-022 · 2026-08-24 · θ̂ na granicy nie oznacza braku heterogeniczności — poprawka do czytania D-015

**Kontekst.** Drugi przegląd `test6_weibull.py` (po naprawie pięciu usterek z pierwszego)
zmierzył własność estymatora kruchości, nie usterkę kodu: parametr θ̂ zapada się do
granicy numerycznej (podłoga 1e-10) **także wtedy, gdy prawdziwa heterogeniczność
istnieje**. Na strukturze Testu 6 (18 grup, 45 zdarzeń), k=1,2, 60 powtórzeń: przy
prawdziwym θ=0,3 granica w 35% biegów (mediana θ̂=0,0003); przy θ=0,6 w 17% (mediana 0,20);
przy θ=1,0 w 0% biegów, ale mediana wciąż 0,42 — ponad dwukrotne zaniżenie.

Code odtworzył pomiar niezależnie (`test_frailty_boundary_collapse`, ten sam protokół:
k=1,2, 60 powtórzeń) na obu strukturach:

| θ prawdziwe | Test 6 (18 grup): % granica / mediana θ̂ | Test 7 (120 grup, 58 bez zdarzeń): % granica / mediana θ̂ |
|---|---|---|
| 0,0 | 60,0% / 1e-10 | 26,7% / 6,0e-8 |
| 0,3 | 33,3% / 0,0050 | 18,3% / 0,0428 |
| 0,6 | 11,7% / 0,231 | 6,7% / 0,268 |
| 1,0 | 1,7% / 0,454 | 0,0% / 0,643 |

Zgodne co do rzędu wielkości z pomiarem przeglądu (różnice — inny strumień losowań).
Test 7 (więcej grup, mimo że 58 bez zdarzeń) identyfikuje θ nieco lepiej niż Test 6 na
każdym poziomie — odnotowane, nie tłumaczone dalej.

### Rozstrzygnięcie

**θ̂ na granicy numerycznej nie jest dowodem braku heterogeniczności — jest niemożnością
jej wykrycia przy tej wielkości próby.** Reguła czytania rozbieżności/zgodności P1 i F1
zadeklarowana w D-015 B wymaga poprawki: zgodność P1 z F1 (oba modele dają ten sam wynik)
jest informacją o braku heterogeniczności **tylko wtedy, gdy θ̂ nie leży na granicy**.
Jeżeli θ̂ jest na granicy, F1 staje się algebraicznie tożsamy z P1 i ich zgodność jest
trywialna — nie wolno jej czytać jako „przypadek pierwszy" reguły D-015 („brak świadectwa
rytmu"), niezależnie od tego, czy heterogeniczność naprawdę istnieje.

**Wynik przy θ̂ na granicy raportowany jest jako nierozstrzygający co do heterogeniczności**,
osobno od wyniku dla parametru kształtu k — nie jako potwierdzenie modelu pulowanego.

### Zmiany w kodzie (weszły do suity na stałe)

1. `test_frailty_boundary_collapse` — powyższa symulacja, uruchamiana na obu strukturach
   (Test 6 i Test 7) jako stały element `run_correctness_suite`.
2. `bootstrap_ci_k_frailty` zwraca teraz `frac_theta_boundary` obok przedziału — jeśli
   przekracza kilkadziesiąt procent replik, przedział bootstrapowy dla kruchości nie jest
   interpretowalny i ma być tak opisany w raporcie, nie podany jako liczba bez zastrzeżenia.
3. `group_sizes_from` poprawiony, by grupować po WSZYSTKICH wierszach (nie tylko pełnych) —
   inaczej 58 diad Testu 7 bez żadnego zdarzenia znikało po cichu ze struktury syntetycznej.
4. `negloglik_frailty` zwektoryzowany (`np.bincount` zamiast pętli Python po grupach) —
   wymagane wydajnościowo przez tę symulację na strukturze 120-grupowej Testu 7;
   zweryfikowane jako identyczne co do zaokrąglenia ze starą wersją przed zamianą.

### Kolejność i zakres

Warunek dotyczył testu, nie kodu — Krok 3 Testu 6 nie wymaga nowego przeglądu, tylko
wykonania tej symulacji i przejścia dalej (ustalone przez autora). Wynik trafia do raportu
Etapu C jako deklaracja sprzed biegu, nie jako wyjaśnienie po fakcie — zgodnie z zasadą
stosowaną konsekwentnie w obu testach rodziny 9/9b.

---

## D-023 · 2026-08-24 · Krok 3 Testu 6 podstawił inny silnik statystyczny niż §6–§8 protokołu — powtórzyć zgodnie z pre-rejestracją

**Kontekst.** `TEST6_PROTOCOL.md` v1.0 (zamrożony 22 sierpnia) pre-rejestruje w §6–§8
konkretny model zerowy — **N1** (proces Poissona per diada, ta sama struktura cenzurowania,
B=2000, ziarno `20260822`) i **N2** (permutacja odstępów między diadami) — z wartością p
liczoną wzorem `p = (1 + #{|k_sur−1| ≥ |k_obs−1|})/(B+1)`, oraz regułę decyzyjną w §8
(P1(N1) p<0,05 **i** P2(N2) p<0,10 **i** S2 bez cenzurowania nie jest jedynym istotnym
wariantem). Lista wariantów §7 to P1, P2, S1–S8.

`TASK_6B_BRIEF.md`, na podstawie którego Code napisał `test6_weibull.py` i wykonał Krok 3,
powstał **bez `TEST6_PROTOCOL.md` w kontekście** i podstawił inny silnik — MLE Weibulla
z profilem wiarygodności i bootstrapem diadowym — nie odnotowując, że to jest podstawienie
metody, nie tylko nazw wariantów (P1/F1/S-A/S-B zamiast P1/P2/S1–S8).

**Sprawdzone w rejestrze:** D-013 zmienia §3 protokołu (próg na epizodach), D-014 zmienia
§4 (ekspozycja zamiast kalendarza), D-015 dokłada model kruchości jako wariant drugorzędny.
**Dla §5–§8 (statystyka, model zerowy, reguła decyzyjna) nie ma żadnego wpisu.** Protokół
w tej części obowiązuje w brzmieniu z 22 sierpnia.

### Rozstrzygnięcie

**Krok 3 powtarzamy zgodnie z §6–§8 protokołu.** Nie zmieniamy protokołu pod już
policzony wynik. `TEST6_REPORT.md` (k̂=0,778, profil i bootstrap poniżej 1) **nie orzeka
o H6.1** — zostaje jako analiza uzupełniająca/diagnostyka, nie jako wynik testu.

**Argument merytoryczny, niezależny od formalnego.** Drugi przegląd `test6_weibull.py`
wykazał, że przy 45 zdarzeniach estymator ma ok. 3% obciążenia k̂ w górę przy prawdziwym
k=1, a przedział z profilu wiarygodności opiera się na przybliżeniu asymptotycznym
niegwarantowanym przy tej liczebności. Model zerowy N1 pochłania to obciążenie
automatycznie, bo surogaty przechodzą przez ten sam estymator, więc metoda protokołu jest
tu lepsza od tej, którą podstawiono — nie tylko formalnie pierwotna.

### Kolejność, z dwoma zatrzymaniami

**Krok A (decyzja, nie implementacja — STOP przed biegiem).** Odwzorowanie wariantów S1–S8
z §7 na warstwę danych po D-013/D-014: dla każdego jedna z trzech kwalifikacji —
wykonywany bez zmian / wykonywany w zmodyfikowanej postaci (jakiej, dlaczego) /
bezprzedmiotowy po D-013/D-014 (co konkretnie unieważniło). Szczególna uwaga na S1 (próg
liczony na konfliktach, nie epizodach) i S3 (definicja odstępu sprzed scalania). S5, S6,
S7, S8 nigdy nie zostały wykonane — odnotować to wprost.

**Krok B.** Implementacja N1 i N2 wg §6, z naprawionym `test6_weibull.py` (pięć poprawek
z pierwszego przeglądu pozostają w mocy) do liczenia k̂ wewnątrz obu modeli zerowych.
Bliźniaczy `.md`. STOP na przegląd, bez uruchamiania na danych rzeczywistych.

**Krok C.** Bieg, sprawdzenie reguły §8 w trzech warunkach naraz, raport.

### Wymogi dla raportu Kroku C (obowiązkowe)

1. `TEST6_REPORT.md` (analiza niezgodna z protokołem) dostaje nagłówek wprost mówiący,
   że nie orzeka o H6.1 — nie jest usuwany, estymacja punktowa i bootstrap zostają jako
   diagnostyka.
2. **Ujawnienie wymagane przez zakaz nr 10 w obie strony.** Bieg zgodny z protokołem
   wykonywany jest ze znajomością wyniku niezgodnego (k̂=0,778, oba przedziały poniżej 1).
   Test pre-rejestrowany wykonany ze znajomością wyniku nie ma pełnej mocy pre-rejestracji —
   ma to stać w raporcie Kroku C wprost, nie być przemilczane. Zakaz nr 10 zabrania zarówno
   zmiany protokołu po zobaczeniu wyniku, jak i udawania, że wyniku się nie widziało.
3. **Porównanie obu metod na tych samych danych jest samodzielnym wynikiem.** Jeżeli p z N1
   i przedział z profilu prowadzą do różnych wniosków, to jest informacja o zachowaniu
   estymatora przy tej wielkości próby, nie tylko o Teście 6 — ma zostać nazwane wprost.

### Zakres

Nie dotyczy Testu 7 — `TEST7_PROTOCOL.md` i `TASK_7B_BRIEF.md` świadomie opisują
wnioskowanie przez przedziały ufności od początku, są spójne same ze sobą i nowsze. Test 7
pozostaje wstrzymany do osobnego potwierdzenia tej spójności przez autora, niezależnie od
niniejszego wpisu.

---

## D-024 · 2026-08-24 · Zatwierdzenie odwzorowania S1–S8 (D-023, Krok A), z trzema korektami

**Kontekst.** `TASK_6C_S1S8_MAPPING.md` przedstawił odwzorowanie ośmiu wariantów wrażliwości
na warstwę danych po D-013/D-014. Pięć przyjęto bez zmian: S2, S3 (co do zmiany jednostki —
start epizodu zamiast surowego konfliktu, z zachowanym zastrzeżeniem o nieporównywalności),
S5, S6, oraz uzasadnienie progu w S1. Trzy wymagały korekty.

### S1 — dopisana konsekwencja liczbowa

Rozkład epizodów na diadę: 10 diad ma 3, 7 ma 4, 1 ma 5. Próg ≥4 epizodów zostawia **8 diad,
25 zdarzeń** — niecałą połowę zbioru głównego (18/45). Odchylenie k̂ rośnie z ok. 0,12 do
ok. 0,16 (rząd wielkości z symulacji odzysku, nie z biegu na S1 — S1 samo nie zostało jeszcze
policzone). **Ma to stać w raporcie PRZED wynikiem S1**: bez tego zastrzeżenia zgodność
S1 z P1 zostałaby po fakcie odczytana jako potwierdzenie, podczas gdy przy tej różnicy
precyzji nie jest ani potwierdzeniem, ani zaprzeczeniem — przedziały tej szerokości mogą się
zgadzać przez brak mocy, nie przez zgodność merytoryczną.

### S7 — rekomendacja implementatora ODWRÓCONA

Code zaproponował scalanie na poziomie państwa tylko z tym samym przeciwnikiem/koalicją.
**Rozstrzygnięcie: scalamy WSZYSTKIE nakładające się lub stykające się wojny tego samego
państwa, niezależnie od przeciwnika.** Uzasadnienie: zegar mierzy regenerację **podmiotu**,
którego zegar liczymy — państwo kończące wojnę z jednym przeciwnikiem i prowadzące nadal
wojnę z innym **nie regeneruje się**, niezależnie od tego, czy przeciwnik jest ten sam.
Reguła Code'a policzyłaby jako czas oczekiwania okres, w którym państwo faktycznie walczy —
błąd tej samej klasy, jaki D-013 naprawiło na poziomie diady. Kryterium z D-013 przenosi się
przez **tożsamość podmiotu**, nie przez tożsamość przeciwnika. Zgłoszenie tego jako decyzji
do podjęcia (zamiast rozstrzygnięcia po cichu) było prawidłowym trybem.

### S8 — kwalifikacja zmieniona: WYMAGA decyzji, nie jest czysto techniczne

Konflikty Extra-State toczą się przeciw podmiotom bez kodu w `system2016.csv` (nie-państwowym
albo nieuznanym). D-014 wymaga obecności **obu** kodów w danym roku dla policzenia ekspozycji;
zastosowane dosłownie do S8 wyzerowałoby ekspozycję całego wariantu, czyli usunęło go
efektywnie, nie rozszerzyło. **Rozstrzygnięcie:** ekspozycja dla par Extra-State liczona
**wyłącznie po stronie państwowej** (obecność w `system2016.csv` tylko dla strony, która ma
kod); okno domyka się na 2007 albo na wyjście strony państwowej z systemu, w zależności co
wcześniejsze. **S8 raportowany jako wariant opisowy**, nie wchodzi do reguły §8 na równi z P1 —
metodologia ekspozycji jest tu z konieczności inna, więc porównanie ilościowe z P1 byłoby
mylące.

### S4 — brakujący model zerowy, uzupełniony

Wzór z §6 jest zdefiniowany dla parametru kształtu k, a S4 pyta o współczynnik przy czasie
trwania poprzedniego epizodu — inna wielkość, ten sam wzór nie stosuje się wprost.
**Deklaracja:** te same surogaty N1 (proces Poissona per diada), statystyka testowa
`|β̂_czas_trwania|` zamiast `|k̂−1|`, ten sam wzór p podstawiony pod tę statystykę. **S4 nie
wchodzi do reguły decyzyjnej §8** — jest odrębnym pytaniem („czy dłuższa wojna wydłuża
regenerację"), nie wariantem wrażliwości P1.

### Luka nienaprawiona, do raportu

`TEST6_PROTOCOL.md` §1 stawia H6.2 (kontrast epok), ale §8 formułuje regułę decyzyjną
**wyłącznie dla P1** — protokół nie ma kryterium falsyfikacji dla kontrastu epokowego.
**Nie dopisuję go teraz** — zrobienie tego po zapoznaniu się z wynikiem biegu niezgodnego
(D-023) naruszałoby zakaz nr 10 w tę samą stronę, co dopisywanie kryterium do P1 po wyniku.
**S5 i S6 pozostają opisowe; raport Kroku C ma stwierdzić wprost, że H6.2 nie została w
Teście 6 rozstrzygnięta** — nie „wsparta" ani „obalona", tylko nieobjęta regułą decyzyjną.

### Krok B odblokowany

Implementacja N1 i N2 wg §6 (ziarno `20260822`, B=2000), `test6_weibull.py` po naprawie
(pięć usterek + D-022) jako estymator k̂ wewnątrz obu modeli zerowych, plus bliźniaczy `.md`.
STOP na przegląd, bez uruchamiania na danych rzeczywistych.

### Reguła proceduralna dodana na przyszłość

Dwa błędy w ciągu jednej doby (D-023 i przeoczenia w pierwotnym odwzorowaniu S1–S8) wynikły
z pracy na streszczeniu dokumentu źródłowego zamiast na jego tekście. **Każdy brief ma odtąd
cytować paragraf protokołu, który realizuje, zamiast go streszczać.**

## D-026 · 2026-08-25 · N2 zdegenerowany względem k̂ pulowanego — wada protokołu, nie implementacji

**Kontekst.** Przegląd Kroku B (`test6_null.py`) wykrył, że model zerowy N2 (permutacja
odstępów między diadami, §6) jest **algebraicznie zdegenerowany** względem statystyki
pierwszorzędnej z §5/§7 (k̂ z `fit_pooled`). `negloglik_pooled(params, t, event)` sumuje po
wszystkich obserwacjach bez odniesienia do etykiety diady — k̂ zależy wyłącznie od
multizbioru par `(t, event)`. Permutacja N2 przenosi wartości MIĘDZY diadami, ale nie zmienia
tego multizbioru (te same wartości `t` i `event`, tylko inaczej przypisane do diad) — k̂_sur
jest więc identyczne z k̂_obs dla KAŻDEJ permutacji, z konstrukcji, niezależnie od danych.

**Zweryfikowane niezależnie (Code), na danych syntetycznych o strukturze Testu 6** (18 grup,
rozkład wielkości 1×4/7×3/10×2), 5 permutacji zgodnie z mechanizmem `simulate_n2_once`: k̂_sur
identyczne do k̂_obs do ~8 miejsca po przecinku (różnice rzędu 1e-8, w granicach tolerancji
optymalizatora Nelder-Mead, nie prawdziwa różnica) — potwierdza zgłoszenie przeglądu.

**Konsekwencja — poprawiona po dodatkowej weryfikacji na danych realnych (Code).**
Teoretycznie `p = (1 + #{|k_sur−1| ≥ |k_obs−1|}) / (B+1) = (1+B)/(B+1)` powinno wynosić
tożsamościowo **1,000**, skoro k̂_sur ≡ k̂_obs matematycznie. **W praktyce, uruchamiając
dosłownie kod i wzór §6 na `test6_intervals.csv` (B=2000), tak nie jest:** `k_sur_sd ≈
7,7·10⁻⁹` potwierdza degenerację (to szum optymalizatora, nie sygnał), ale wynikowe `p` =
**0,253** (ziarno protokołu `20260822`) i **0,266** (inne ziarno) — nie 1,000, nie 0,5,
tylko pozornie sensowna, w praktyce przypadkowa liczba zależna od ziarna (deterministyczna
przy ustalonym ziarnie — powtórzone uruchomienie daje identyczny wynik — ale bez treści).
Przyczyna: porównanie `|k_sur−1| >= |k_obs−1|` rozstrzyga o remisie na poziomie szumu
zmiennoprzecinkowego (permutacja zmienia kolejność sumowania tych samych wartości w
`np.sum(ll)`, nieasocjatywność arytmetyki przesuwa optimum Nelder-Mead o ~1e-8 w tę lub inną
stronę) — to JEST ta sama degeneracja, tylko widoczna na innym poziomie precyzji, nie inne
zjawisko. **Ani „1,000" (teoria), ani „0,253"/"0,266" (to, co kod faktycznie zwraca) nie są
prawdziwym wynikiem** — raportowanie którejkolwiek z tych liczb jako p-wartości byłoby
mylące; poprawnie jest opisać zjawisko (degeneracja, brak treści), nie podawać liczbę.
Reguła decyzyjna §8 wymaga trzech warunków naraz, w tym P2<0,10 — skoro P2 nie niesie
żadnej treści o danych (ani w teorii, ani w praktycznym wykonaniu kodu), **żaden zbiór
danych nie może w informacyjny sposób spełnić §8**. Zamrożony protokół (w obecnym brzmieniu
§6) nie ma osiągalnego wyniku pozytywnego dla H6.1.

**To nie jest wada implementacji.** `test6_null.py` odtwarza §6 dosłownie i poprawnie —
problem leży w tym, że §6 opisuje model niszczący strukturę wewnątrz diady (sensowny dla
statystyki wrażliwej na grupowanie, np. θ z modelu kruchości), podczas gdy §5/§7 ustanowiły
statystyką pierwszorzędną k̂ pulowane, które grupowanie ignoruje z definicji. Paragraf szósty
zakłada inną statystykę niż ustanawiają paragrafy piąty i siódmy — niespójność wewnętrzna
protokołu, nie błąd realizacji.

### Rozstrzygnięcie

1. **P1 liczymy i raportujemy normalnie** — N1 tej wady nie ma (permutuje/losuje wewnątrz
   struktury per-diady, nie między diadami, więc nie jest degenerowany względem k̂ pulowanego).
2. **P2 raportowany jako zdegenerowany/nieinformacyjny, z wyjaśnieniem mechanizmu** —
   NIE jako liczba „1,000" (teoria) ani jako liczba, którą faktycznie zwraca kod (~0,25,
   artefakt szumu numerycznego przy dokładnej remisie) — żadna z tych liczb nie ma treści.
3. **Reguła §8 raportowana jako niespełnialna w obecnym brzmieniu.** H6.1 pozostaje
   **nierozstrzygnięta w ramach zamrożonego protokołu** — nie „obalona" ani „wsparta częściowo".
4. **Nie podstawiamy w miejsce N2 innego modelu zerowego, żeby regułę §8 uratować.** Byłoby to
   dokładnie to podstawienie metodologii po zobaczeniu problemu, które doprowadziło do D-023 —
   tym razem świadome, więc gorsze, nie lepsze.
5. **Wolno (nie: trzeba) policzyć N2 dla modelu kruchości F1**, gdzie permutacja faktycznie
   niszczy mierzoną strukturę (θ zależy od grupowania wewnątrz diady, więc permutacja między
   diadami jest tam informacyjna) — wyłącznie jako diagnostyka, jawnie oznaczona jako **poza
   §8**, nie jako zamiennik P2. Zastrzeżenie: przy zapadaniu się θ do granicy numerycznej
   (D-022) wynik może wyjść nieinformacyjny i ma być tak opisany, nie przemilczany.

### Dwie weryfikacje przed biegiem P1 (zlecone w przeglądzie, wykonane przez Code)

**A. Rozbicie średniego k̂_sur≈0,92 (N1) na dwa składniki.** Zmierzone niezależnie na danych
syntetycznych: (a) mieszanka wykładniczych o różnych λ̂ per diada, dopasowana jednym wspólnym
k, ciągnie k̂ w dół (mechanizm z D-015/F1) oraz (b) sam estymator `fit_pooled` ma przy n=45
zdarzeniach obciążenie w górę — zmierzone tutaj na strukturze 18 grup (1×4/7×3/10×2) pod
**jednorodną** prawdą (k=1, jedno wspólne λ dla wszystkich diad, więc składnik (a) jest z
konstrukcji zerowy): średnie k̂ = 1,024 (mediana 1,015), **obciążenie ≈ +2,4%** — rząd
wielkości zgodny ze zgłoszonymi ~3% z drugiego przeglądu. Oba składniki działają w
przeciwne strony (mieszanka w dół, obciążenie małej próby w górę) i oba mają trafić do
raportu Kroku C osobno, nie jako jedna zbiorcza liczba.

**B. Czy Σt_sim+c surogatu N1 mieści się w realnym oknie obserwacji diady.** Sprawdzone na
realnej strukturze `test6_intervals.csv` (18 diad, B=2000 na diadę): **75,4% surogatowych
replik ma Σt_sim+c przekraczające realną długość okna diady** (zakres per-diada: 41%–98%,
rośnie z udziałem cenzurowania `c/T` w oknie). **To NIE jest zjawisko marginalne.** Przyczyna
algebraiczna: `λ̂ = n/T` (T = realna ekspozycja całkowita, włącznie z `c`), więc
`E[Σt_sim] = n·(1/λ̂) = T`, a surogat dokłada do tego jeszcze niezmienione `c` — stąd
`E[Σt_sim+c] = T+c > T` systematycznie, dla każdej diady z `c>0`. Jest to dodatkowe źródło
wariancji rozkładu zerowego N1 (surogaty generują historie dłuższe niż diada mogła realnie
mieć), co czyni test N1 **konserwatywnym** (trudniej odrzucić H0, niż gdyby surogaty były
ograniczone do realnego okna) — ma być nazwane wprost w raporcie Kroku C, nie tylko
zasygnalizowane jedną liczbą.

### Ujawnienie do raportu Kroku C (obok D-023 §5)

Wada §8 (degeneracja N2) została wykryta **przy przeglądzie kodu, przed jakimkolwiek biegiem
na danych rzeczywistych.** Kolejność ta jest sprawdzalna niezależnie od zaufania do
oświadczenia: degeneracja N2 jest własnością algebraiczną, niezależną od danych (zależy
wyłącznie od tego, że `negloglik_pooled` nie używa etykiety diady) — jej wykrycie nie mogło
zostać zainspirowane wynikiem, bo nie wymagało żadnego wyniku do zaobserwowania.

### Zakres

Dotyczy wyłącznie N2 (permutacja międzydiadyczna) w kontekście statystyki k̂ pulowanego.
Nie dotyczy N1 (poprawny). Nie unieważnia Kroku B jako całości — P1(N1) pozostaje
prawidłową, obliczalną ścieżką do wyniku dla H6.1, tylko bez towarzyszącego jej P2 jako
drugiego, niezależnego potwierdzenia przewidzianego przez §8.
