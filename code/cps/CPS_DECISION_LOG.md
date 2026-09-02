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

## D-020 · 2026-08-24 · Sprostowanie liczby kontrolnej w D-016: 120 diad z niepustym oknem, nie 129

**Kontekst.** D-016 i `TEST7_PROTOCOL.md` §3 podają jako liczbę kontrolną „diady z niepustym
oknem ryzyka w latach 1816–2007: **129**" (12 ze 141 diad odrzuconych). Etap A Testu 7
(`test7_build_windows.py`), stosując wzór §3 **dosłownie** — łącznie z warunkiem
`wejście_a_do_systemu`/`wyjście_a` z `system2016.csv` — dał **120** diad z niepustym oknem
(21 odrzuconych). Code zatrzymał się i zgłosił rozbieżność zamiast dopasowywać wynik do
liczby z protokołu.

### Rozstrzygnięcie

**Wzór §3 protokołu pozostaje bez zmian — jest poprawny.** Liczba kontrolna „129" w D-016
i `TEST7_PROTOCOL.md` §3 była policzona **z pominięciem warunku członkostwa**
(`system2016.csv`) — czyli innym wzorem niż ten, który protokół faktycznie deklaruje.
Liczba była błędna, nie wzór. **Obowiązuje 120 diad z niepustym oknem, 21 odrzuconych.**

### Rozbicie 21 odrzuconych diad (ustalone w Etapie A, do raportu)

| grupa | n | przyczyna |
|---|---|---|
| A | 9 | okres rywalizacji leży **całkowicie przed 1816** — koniec rywalizacji wypada przed początkiem zbioru COW, niezależnie od członkostwa |
| B | 3 | okres rywalizacji leży **całkowicie po 2007** — zaczyna się po końcu zakresu `Inter-StateWarData_v4.0.csv` |
| C | 9 | **brak wspólnych lat członkostwa w oknie** — w przedziale [1816,2007] ∩ [okres rywalizacji] żaden rok nie ma obu stron jednocześnie w `system2016.csv` |

Grupy A i B (12 diad) odpowiadają dokładnie pierwotnej liczbie „12" z D-016 — to jest
poprawny rdzeń tamtego ustalenia. Grupa C (9 diad) została pominięta w obliczeniu, które
dało 129.

**Przykład grupy C, wart odnotowania.** Niemcy–Austria (rywalizacja 1740–1870) odpada, bo
COW koduje Austro-Węgry jako ccode 300 do 1918, a Austrię jako ccode 305 dopiero od 1919 —
w całym przedziale [1816,2007] ∩ [1740,1870] = [1816,1870] nie ma roku, w którym ccode 305
istnieje w `system2016.csv`. **To jest ograniczenie konwencji kodowania COW, nie twierdzenie
historyczne** o nieistnieniu Austrii jako podmiotu w tym okresie (zgodnie z zasadą przyjętą
już w D-012 dla ciągłości państw: kody realizują konwencję zbioru, nie orzekają o tożsamości
politycznej).

### Kolejność i ujawnienie

Rozstrzygnięcie zapadło po zatrzymaniu się Code'a na rozbieżności liczby kontrolnej, przed
policzeniem jakiejkolwiek statystyki czasów oczekiwania — zgodnie z §6 `TASK_7A_BRIEF.md`.
Etap A kontynuowany na zbiorze 120 diad.

---

## D-021 · 2026-08-24 · Epizody częściowo w oknie ryzyka (Test 7, rodzina 9b)

**Kontekst.** `TEST7_DATA_REPORT.md` §5 zgłosił cztery epizody, których przedział trwania
przecina granicę okna ryzyka diady: początek albo koniec mieści się w oknie, ale nie oba
naraz. Builder wykluczył je z sekwencji zdarzeń i wypisał osobno, zamiast obcinać po cichu.
Zgłoszenie do decyzji było prawidłowe.

| diada | epizod | okno diady | strona przecięta |
|---|---|---|---|
| France–Italy | II wś 1939–1945 | [1881, 1940] | koniec okna w trakcie wojny |
| Germany–Poland | II wś 1939–1945 | [1918, 1939] | koniec okna na starcie wojny |
| Italy–Ethiopia | II wś 1939–1945 | [1898, 1943] | koniec okna w trakcie wojny |
| Cambodia–Vietnam | Wietnam + Communist Coalition 1965–1975 | [1970, 1983] | początek okna w trakcie konfliktu |

### Rozstrzygnięcie — jedna reguła, dwa skutki

**Epizod jest zdarzeniem wtedy i tylko wtedy, gdy jego POCZĄTEK wypada wewnątrz okna
ryzyka.** Data końca epizodu nie ma dla kwalifikacji znaczenia.

Skutek A — **epizod rozpoczynający się w oknie liczy się jako zdarzenie**, nawet jeśli trwa
poza domknięciem okna. Okno domyka się na tym zdarzeniu; nie powstaje z niego odstęp
cenzurowany. Dotyczy France–Italy, Germany–Poland i Italy–Ethiopia.

Skutek B — **epizod trwający już w chwili otwarcia okna nie jest zdarzeniem**, bo jego
początku nie obserwowaliśmy. Okno otwiera się dopiero z **końcem** tego epizodu, a lata
trwania konfliktu nie wchodzą do ekspozycji. Dotyczy Cambodia–Vietnam: okno przesuwa się
z 1970 na 1975.

### Uzasadnienie

§1 protokołu definiuje mierzoną wielkość jako czas **do wybuchu** konfliktu, a §5 liczy
odstępy od końca jednego epizodu do **początku** następnego. Zdarzeniem jest zatem początek,
a nie zakończenie. Reguła stosuje tę definicję konsekwentnie do brzegów okna, zamiast
wprowadzać dla nich osobne kryterium.

**Dlaczego nie wykluczenie wszystkich czterech.** Trzy z nich to realne wybuchy wojny, które
nastąpiły w czasie żywej rywalizacji. Zamiana ich na obserwacje cenzurowane sztucznie
wydłużyłaby czasy oczekiwania, czyli obciążyłaby wynik **w stronę hipotezy**. To jest
kierunek, którego nie wolno przyjąć przez zaniechanie.

**Dlaczego nie przycinanie epizodu do granicy okna.** Przycięcie zmieniałoby datę zdarzenia,
a data wybuchu jest wielkością obserwowaną, nie modelowaną.

### Zastrzeżenie o pochodzeniu reguły

Trzy z czterech przypadków to II wojna światowa kończąca okres rywalizacji, ponieważ
konwencja kodowania Thompsona zamyka rywalizację wraz z wojną, która ją rozstrzyga. Reguła
przyznaje więc zdarzenie parze **Niemcy–Polska**, wymienionej wcześniej przez autora jako
przedmiot zainteresowania.

Odnotowuję to wprost: reguła wynika z §1 i §5 protokołu, nie została dobrana pod ten
przypadek, a przy jednym epizodzie para Niemcy–Polska i tak nie wnosi żadnego odstępu
pełnego — wnosi wyłącznie odstęp `t0`, który w modelu głównym nie uczestniczy (§5 protokołu).
Wpływ tej reguły na wynik pierwszorzędny jest zatem zerowy dla tej pary.

### Skutek liczbowy do przeliczenia w Etapie A

Po zastosowaniu reguły builder ma przeliczyć i zaraportować zmianę: liczbę zdarzeń
(dotąd 43 odstępy pełne oraz 62 `t0`), liczbę obserwacji cenzurowanych oraz nowe okno
Cambodia–Vietnam. Zmiana dotyczy czterech diad i nie rusza pozostałych stu szesnastu.

### Ograniczenie, do zapisania w raporcie

Reguła nie usuwa problemu, na który wskazuje sam fakt istnienia tych czterech przypadków:
**konwencja kodowania rywalizacji wiąże koniec rywalizacji z wojną, która ją rozstrzyga**,
więc dla części par zdarzenie i domknięcie okna są z definicji równoczesne. Nie jest to
niezależna obserwacja czasu oczekiwania w tym samym sensie co pozostałe. Dotyczy trzech
diad ze stu dwudziestu i ma zostać nazwane w Etapie C jako ograniczenie, nie skorygowane.

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

---

## D-025 · 2026-08-24 · Wykluczenie odstępu Italy–Ethiopia (ekspozycja zero, konsekwencja D-021)

**Kontekst.** Zastosowanie D-021 sprawiło, że II wś liczy się jako zdarzenie dla diady
Italy–Ethiopia (start 1939 w oknie [1898,1943], Skutek A). Powstał przez to odstęp między
poprzednim epizodem („Conquest of Ethiopia", 1935–1936) a II wś (1939): 1936→1939. W tym
przedziale Etiopia jest **całkowicie nieobecna w `system2016.csv`** (aneksja włoska
1937–1940 — Etiopia formalnie nie istnieje jako podmiot systemu międzypaństwowego aż do
wyzwolenia w 1941, już w trakcie II wś). Ekspozycja tego odstępu wynosi **0**, co narusza
wymóg dodatniej długości odstępu pełnego (asercja z D-013/D-014 zatrzymała bieg, zgodnie
z przeznaczeniem — zgłoszone, nie załatane po cichu).

### Rozstrzygnięcie

**Odstęp Italy–Ethiopia (1936→1939) wykluczony z analizy głównej**, z jawną flagą
i uzasadnieniem — nie z całej diady, tylko z tego jednego odstępu. Diada pozostaje
w zbiorze przez swoje pozostałe obserwacje (epizody, okno), ale nie wnosi tego konkretnego
czasu oczekiwania.

**Uzasadnienie (poprawione po przeglądzie — nie jest to wyjątek, tylko D-013 zastosowane
w czasie ekspozycji).** D-013 nakazuje scalać epizody stykające się lub nakładające się w
czasie. Między „Conquest of Ethiopia" (1935–1936) a II wś (od 1939) nie ma **ani jednego
roku ekspozycji** — w zegarze, którym faktycznie mierzymy odstępy (suma lat ekspozycji, nie
kalendarz), te dwa epizody się stykają. D-013 zastosowane poprawnie w tym zegarze każe je
scalić, a nie traktować jako dwa osobne zdarzenia oddzielone odstępem. Scalenie i
wykluczenie dają identyczny wynik liczbowy dla tej diady (zero wniesionych obserwacji
`pelny`/`cenzurowany` z tego przejścia), więc decyzja operacyjna (wykluczenie jednego
odstępu z jawną flagą, zamiast przepisywania `merge_episodes`) zostaje bez zmian, ale
przestaje być traktowana jako wyjątek wymagający osobnej licencji — jest konsekwencją D-013
już obowiązującego, tylko dotąd niezastosowanego w prawidłowej jednostce czasu. Analogia do
Polski walczącej z zaborcami, nieistniejącej formalnie jako podmiot, pozostaje trafną
ilustracją *dlaczego* zerowa ekspozycja oznacza zerowy dystans między epizodami — ale nie
jest już samodzielną podstawą decyzji.

**Kierunek obciążenia (dopisany po przeglądzie).** Usunięcie odstępu o zerowej długości
usuwa masę z **dolnego końca** rozkładu odstępów. To podnosi oszacowany parametr kształtu
k̂ w stronę 1, czyli w stronę modelu zerowego (brak pamięci) — **działa przeciw hipotezie
H9b (malejący hazard/regeneracja), nie na jej korzyść**. Decyzja nie jest więc podejrzana
o naginanie danych pod oczekiwany wynik; gdyby czegokolwiek dotyczyła stronniczo, to
zaniżenia efektu, nie jego wzmocnienia.

**Dlaczego nie usunięcie całej diady (droga odrzucona).** Diada wnosi też inne, poprawne
informacje (epizody, ekspozycję poza tym jednym odstępem); usunięcie całości byłoby
nadmiarowe wobec problemu, który dotyczy jednego konkretnego przejścia między dwoma
konkretnymi epizodami.

### Zakres

Jeden odstęp, jedna diada ze stu dwudziestu. Mechanizm implementacyjny: asercja `gap>0`
zamieniona na zgłoszenie + wykluczenie z listy zdarzeń, z zapisem w osobnej tabeli
wykluczeń (diada, lata, przyczyna, ekspozycja) — analogicznie do tabeli epizodów
częściowych z D-021, nic nie znika bez śladu.

### Dodatek — weryfikacja hipotezy o zasięgu Skutku A (przegląd 2026-08-25)

Po przeliczeniu Etapu A zauważono, że liczba obserwacji cenzurowanych spadła ze 120
(62 `cenzurowany` + 58 `cenzurowany_bez_epizodow`, po jednej na diadę) do 98
(42 + 56) — 22 diady straciły ogon cenzurowany, mimo że D-021 explicite dotyczyło tylko
4 zgłoszonych przypadków. Hipoteza zgłoszona do weryfikacji: Skutek A działa wszędzie tam,
gdzie ostatni kwalifikujący epizod kończy się w chwili domknięcia okna ryzyka lub później
(`last["end"] >= win_end`), niezależnie od tego, czy przypadek był wcześniej zgłoszony.

**Potwierdzone bezpośrednim przeliczeniem.** Dokładnie 22 z 64 diad z epizodami mają
`last["end"] >= win_end`: United States of America–Japan, Brazil–Paraguay,
Paraguay–Argentina, United Kingdom–Germany, United Kingdom–China, United Kingdom–Japan,
France–Austria-Hungary, France–Italy, France–China, France–Thailand, Germany–Poland,
Germany–USSR, Austria-Hungary–Italy, Austria-Hungary–Yugoslavia, Austria-Hungary–USSR,
Hungary–Yugoslavia, Italy–Ethiopia, Yugoslavia–Turkey, Bulgaria–Romania, USSR–Turkey,
USSR–Japan, Uganda–Tanzania. W większości (I i II wś) to konwencja kodowania Thompsona,
która kończy okres rywalizacji razem z wojną, która ją rozstrzyga; kilka przypadków
niezwiązanych ze światowymi wojnami (Lopez War 1870, Boxer Rebellion 1900, Franco-Thai
1941, Uganda-Tanzania 1979) pokazuje, że mechanizm jest ogólny, nie ograniczony do
konfliktów światowych.

**Status: własność strukturalna zbioru, nie margines.** Zachowanie kodu jest poprawne —
D-021 to jedna reguła zastosowana jednolicie do wszystkich 120 diad, nie cztery reguły
punktowe. Ale przy 22/64 = 34% diad z epizodami zdarzenie i domknięcie okna są z
**definicji równoczesne** — to nie są niezależne obserwacje czasu oczekiwania w tym samym
sensie co pozostałe 42, gdzie okno domyka się niezależnie od tego, kiedy skończyła się
ostatnia wojna. Zapisane w `TEST7_DATA_REPORT.md` (Etap A), nie odłożone do Etapu C — przy
4 przypadkach byłaby to uwaga na marginesie, przy 22 jest to fakt o strukturze danych, z
którym Etap B musi się liczyć od początku (możliwy wpływ na sposób traktowania obserwacji
`cenzurowany` kontra `pelny`/`t0`-only w modelu — nie rozstrzygane tutaj, tylko
udokumentowane).

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

### §7 — Sprostowanie (Claude, po weryfikacji Code'a) i reguła ogólna

**Sprostowanie.** Twierdzenie „P2 wynosi dokładnie 1,000" jest prawdziwe wyłącznie w
arytmetyce dokładnej: statystyka jest niezmiennicza względem permutacji, więc w arytmetyce
dokładnej wszystkie surogaty remisują z obserwacją, a wzór §6 z nierównością nieostrą daje
P2 równe jeden. Wniosek o tym, co zwróci KOD, jest twierdzeniem o implementacji, nie o
algebrze — w arytmetyce zmiennoprzecinkowej permutacja zmienia kolejność sumowania tych
samych wartości w `np.sum(ll)`, co przez nieasocjatywność przesuwa optimum Nelder-Mead o
rząd 10⁻⁸ i rozstrzyga remis losowo. Sprawdzian pięciu permutacji na danych syntetycznych,
który dał różnicę dokładnie zero, był przypadkiem: przy małej liczbie wierszy i wartościach
całkowitych sumy wyszły bitowo identyczne, więc ścieżka optymalizatora się nie rozjechała.
Przy B=2000 na pełnym zbiorze realnym rozjeżdża się i daje **p=0,253** (ziarno protokołu
`20260822`) / **0,266** (inne ziarno) — deterministyczne przy ustalonym ziarnie, ale
pozbawione treści. **Raportujemy zjawisko (degenerację), nie żadną z tych liczb.**

**Reguła ogólna.** Każdy model zerowy oparty na symulacji, w którym surogat może remisować
z obserwacją, wymaga jawnego wykrywania remisów. Nierówność nieostra z §6 jest poprawna i
konserwatywna, ale tylko wtedy, gdy remis zostanie rozpoznany jako remis. **Do każdego
kolejnego testu tej rodziny wchodzi kontrola: odsetek surogatów z `|k_sur − k_obs| < 10⁻⁶`
(`tie_fraction`, `TIE_TOL=1e-6`). Wartość istotnie większa od zera (próg `TIE_FRAC_STOP=0,01`)
oznacza degenerację i zatrzymuje bieg** (`AssertionError`, nie ciche zwrócenie p bez treści).
Wbudowane w `run_n1`/`run_n2` (test6_null.py), zweryfikowane własnym testem
(`test_tie_detector_discriminates`) na przypadku znanym-zdegenerowanym i
znanym-niezdegenerowanym, oraz w stałej suicie (`run_null_correctness_suite`), obok
`n1_window_exceedance`.

**Przekroczenie okna N1 (75,4%) — dokładniejsze sformułowanie.** Nie efekt uboczny, tylko
strukturalna własność N1 w dosłownym brzmieniu §6. `λ̂ = n/(Σt+c)`, więc oczekiwana długość
pojedynczego losowanego odstępu wynosi `(Σt+c)/n`, a suma n odstępów daje w oczekiwaniu
`Σt+c` (=T, realna ekspozycja). Po dołożeniu niezmienionego `c` surogatowa diada ma
oczekiwany czas całkowity `Σt+2c` (=`T+c`) wobec obserwowanego `T` — **nadmiar równa się
DOKŁADNIE `c`, jest systematyczny, nie losowy.** Stąd ~3/4 replik przekracza okno.
**Konsekwencja dla czytania wyniku, asymetryczna:** rozkład zerowy N1 ma zawyżoną wariancję,
więc P1 jest konserwatywne — niska wartość P1 jest wiarygodna Z NADWYŻKĄ (trudniej o nią
przez przypadek, skoro null jest już rozdęty), natomiast wysoka wartość P1 jest **częściowo
przypisywalna samej konstrukcji modelu zerowego, nie danym**. Ta asymetria jest ważniejsza
niż sam odsetek i ma trafić do raportu Kroku C wprost. Nie naprawiane — z tego samego powodu
co N2: opisujemy zjawisko protokołu, nie łatamy go po zobaczeniu problemu.

**Zamknięcie przeglądu Kroku B (Claude).** Po dopisaniu tego paragrafu i powyższym
doprecyzowaniu, przegląd kodu Kroku B jest zamknięty bez dalszych zastrzeżeń.

## D-027 · 2026-08-25 · Autoryzacja Kroku C

**Kontekst.** Po D-026 (wada §8 wykryta i rozstrzygnięta przed jakimkolwiek biegiem na danych
rzeczywistych) Claude rekomendował udzielenie autoryzacji: kod przejrzany dwukrotnie, wady
protokołu opisane przed biegiem, warunki raportowania zapisane. Autoryzacja nie leży w
kompetencji ani Code'a, ani Claude — obaj to odnotowali wprost.

**Rozstrzygnięcie (autor).** Krok C autoryzowany. `test6_null.py --run-real` odblokowane.
Bieg wykonywany ze znajomością wyniku analizy niezgodnej (`TEST6_REPORT.md`, D-023) i ze
znajomością wady §8 (D-026) — obie okoliczności ujawnione w raporcie Kroku C wprost, zgodnie
z zakazem nr 10 w obie strony (nie zmieniać metodologii po wyniku, ale też nie udawać, że
się go nie widziało).

## D-028 · 2026-08-25 · Tryb przeglądu decyzji warstwy danych — zawężenie przyjęte

**Kontekst.** Po D-025 (Test 7) Claude zauważył, że decyzje zmieniające zbiór danych
(usuwanie obserwacji, przesuwanie okien, zmiana reguły kwalifikacji zdarzeń) mają tę
własność, że ich skutek nie widać w liczbach, dopóki nie jest za późno — D-025 wyszło dobrze
merytorycznie, ale dopiero przy weryfikacji arytmetyki ujawniło się, że przy okazji 22 diady
straciły ogon cenzurowany (dodatek do D-025).

**Rozstrzygnięcie (autor).** Przyjęte, z zawężeniem: decyzje o warstwie danych pozostają w
gestii autora bez zmian, ale odtąd Code przy każdej takiej decyzji dołącza liczbę wierszy
przed i po (rozbicie na typy obserwacji), a Claude sprawdza arytmetykę przed decyzją autora,
nie po niej. Dokłada to jedną turę, ale wyłapuje dokładnie ten rodzaj rozjazdu między
uzasadnieniem merytorycznym a niezamierzonym skutkiem ubocznym. Decyzje interpretacyjne
(nie zmieniające zbioru) zostają w dotychczasowym trybie.
---

## D-029 · 2026-08-25 · Przegląd `TASK_7B_BRIEF.md` wobec `TEST7_PROTOCOL.md` — cztery luki, jedna poważna

**Kontekst.** Wykonany na żądanie z D-023 §8 (warunek przed odblokowaniem Etapu B Testu 7):
sprawdzenie, czy `TASK_7B_BRIEF.md` podmienia cokolwiek, czego `TEST7_PROTOCOL.md` nie
ustala — dokładnie ten typ błędu, który dotknął Test 6. **Werdykt: podmiany nie ma.**
Statystyka, model i cztery warianty zgadzają się z §7 protokołu co do joty. Znaleziono
cztery luki, jedną poważną, trzy formalne/redakcyjne.

### 1. LUKA POWAŻNA — brief pomijał połowę reguły decyzyjnej §8

Brief pisał przy P1 wyłącznie „ORZEKA dla H9b.1", gubiąc drugi człon reguły §8: wymóg, żeby
ten sam kierunek utrzymał się w S1 i S3. Wykonawca czytający sam brief uznałby, że wystarczy
CI z P1. **Ta sama klasa usterki co D-023 — tylko przez pominięcie, nie przez podstawienie**
— dokładnie to, dla czego powstała reguła z D-024 (brief cytuje paragraf protokołu, nie
streszcza go).

**Naprawa:** §8 protokołu wklejony do `TASK_7B_BRIEF.md` w całości, jako cytat, przed tabelą
dopasowań (brief §2).

### 2. LUKA MERYTORYCZNA — Krok C Testu 6 pokazał, że CI i model zerowy mogą wskazać różne strony progu

Reguła §8 Testu 7 opiera H9b.1 wyłącznie na CI. Krok C Testu 6 (D-026/D-027) dał na tych
samych danych: CI z profilu (0,603–0,979) i CI bootstrapowy (0,647–0,965) — oba wykluczają 1
— ale wartość p z modelu zerowego N1 wyszła **0,068**. Gdyby regułą Testu 6 był sam CI, H6.1
zostałaby uznana za wspartą; regułą był model zerowy (§8 Testu 6) i nie została.

Przyczyna: model zerowy skalibrowany na rzeczywistą różnorodność temp między diadami centruje
się na k̂≈0,91, nie na 1,0 (mechanizm F1/D-015, ten sam co w Teście 6) — CI porównuje z 1
wprost, więc jest **systematycznie bardziej liberalny** w kierunku k<1. W Teście 7 diad jest
120 zamiast 18, więc różnorodność temp będzie większa, a rozjazd prawdopodobnie szerszy.

**Rozstrzygnięcie: reguły §8 Testu 7 NIE zmieniamy.** Jest zamrożona; zmiana po doświadczeniu
z Testu 6 byłaby zmianą po zobaczeniu wyniku, choćby wyniku cudzego testu — to samo
zobowiązanie co przy D-026 dla Testu 6. **Dokładamy natomiast obowiązkowy pomiar POZA regułą:**
Etap B Testu 7 ma dodatkowo policzyć model zerowy typu N1 na strukturze Testu 7 i podać
wartość p obok obu przedziałów. Nie orzeka — służy wyłącznie do pokazania, o ile obie miary
się rozjeżdżają na tym zbiorze. Deklarowane TERAZ, przed jakimkolwiek biegiem Testu 7, z
powodem zapisanym: doświadczenie z Testu 6, nie podejrzenie co do wyniku Testu 7.

### 3. LUKA FORMALNA — odłożenie H9b.2 nie miało wpisu w rejestrze

Brief odkładał P2 i zmienne z §6 protokołu „do czasu dostarczenia COW NMC" jedynie zdaniem
w treści briefu, mimo że §7 protokołu ustanawia P2 jako orzekające dla H9b.2 — pominięcie
takiego zakresu wymaga wpisu w rejestrze, nie zdania w briefie.

**Wpis:** H9b.2 NIE jest testowana w tym etapie Testu 7. Powód: brak `COW NMC` (`NMC_v6.0`)
— potencjał gospodarczy wymagany przez §6 protokołu jako zmienna objaśniająca (CINC, suma
i stosunek stron) nie został dostarczony. Powód jest niezależny od jakiegokolwiek wyniku —
zbiór nigdy nie był dostępny do wglądu, nie jest to decyzja podjęta po zobaczeniu czegokolwiek.
**Warunek odblokowania:** dostarczenie `NMC_v6.0` z sumą kontrolną (§12 protokołu). ICOW
(istotność stawki) pozostaje opcjonalne i odłożone z tego samego powodu.

### 4. LUKA DROBNA — tabela §7 protokołu ma nieaktualną liczbę diad

Tabela `TEST7_PROTOCOL.md` §7 podaje przy P1 „129 diad". D-020 sprostowało tę liczbę na
**120** dla §3, ale tabeli §7 nigdy nie poprawiono — protokół jest zamrożony (zmiana §1–§9
po rozpoczęciu obliczeń wymaga nowego wpisu i unieważnia bieg), więc tekst protokołu
**pozostaje niezmieniony**, a rozbieżność jest odnotowana tutaj jako erratum redakcyjne, bez
wpływu na treść: wszystkie faktyczne biegi (Etap A, `TASK_7B_BRIEF.md`) używają poprawnej
liczby 120, zgodnie z D-020.

### 5. Zapis dodatkowy, wynikający z D-022

§8 protokołu Testu 7 mówi o CI dla `k` w modelu z kruchością i nie wspomina o parametrze
kruchości. D-022 (Test 6) ustaliło, że θ̂ zapada się do granicy numerycznej w znacznej części
biegów, a wtedy model z kruchością staje się tożsamy z pulowanym. Reguła §8 stosuje się wtedy
mechanicznie i formalnie poprawnie, ale zdanie „orzeka model z kruchością" przestaje być
prawdziwe. **Raport Etapu C Testu 7 ma podawać odsetek replik bootstrapowych z θ̂ na granicy
obok każdego przedziału** i, jeżeli jest wysoki, stwierdzać wprost, że rozstrzygnięcie
zapadło de facto na modelu pulowanym.

### Rozstrzygnięcie

Punkty 1, 3, 4 to poprawki redakcyjne/wpisy do rejestru (wykonane w `TASK_7B_BRIEF.md` i
powyżej). Punkt 2 dokłada jedno obowiązkowe obliczenie diagnostyczne, poza regułą §8. Po ich
wykonaniu **Etap B Testu 7 jest odblokowany**, w kolejności z brief §8: przeliczenie
D-021/D-025 (wykonane), kod plus bliźniaczy `.md`, symulacja odzysku na strukturze Testu 7
z cenzurowaniem administracyjnym plus model zerowy N1 diagnostyczny, **STOP** na przegląd,
dopiero potem bieg na danych rzeczywistych.

`TEST7_PROTOCOL.md` i `TASK_7B_BRIEF.md` (po naprawach) commitowane do repo w tym wpisie —
oba dokumenty były dotąd przekazywane wyłącznie jako tekst w rozmowie, nigdy nie zapisane
jako pliki, co przyczyniło się pośrednio do ryzyka błędu typu D-023 (praca na streszczeniu
zamiast na źródle).

## D-030 · 2026-08-25 · Przegląd `test7_estimate.py` — naruszenie protokołu naprawione, nowe odkrycie o kruchości

**Kontekst.** Przegląd `PRZEGLAD_test7_estimate.md` sprawdził obie luki zgłoszone w Etapie B
(D-029 §5b/§6, patrz `test7_estimate.md` pierwszej wersji) w źródłach, zamiast rozstrzygać
z pamięci, i znalazł dodatkowo trzy braki wobec wymagań już zapisanych.

### Luka 1 (`positional`) — rozstrzygnięta

Brak wartości w `positional` oznacza nieobecność składnika (0) — konwencja już użyta w
projekcie dla `spatial` (kontrola 152, D-016). Zweryfikowane niezależnie: S2 = `spatial==1`
i `positional!=1` daje **76 wierszy, 73 diady** — wykonalny, nie pusty. Budowa S2 pozostaje
do zrobienia, poza zakresem tego Etapu B.

### Luka 2 (diady ucięte) — NARUSZENIE PROTOKOŁU, naprawione

`TEST7_PROTOCOL.md` §3 nie zostawia alternatywy: diady lewostronnie ucięte „muszą... wchodzić
do wariantu S3, nie do modelu głównego". Pierwsza wersja `test7_estimate.py` błędnie
traktowała to jako lukę interpretacyjną i zostawiała te diady (5 diad, 9 wierszy) w modelu
głównym. **Naprawione:** `load_grouped` wyklucza teraz całe diady `ucieta==1` z modelu
głównego, włącza je z powrotem w S3. Liczby przed/po (D-028): n 106→**101**, pełne 43→**37**,
cenzurowane 98→**95**.

### Brak 1 — pomiar procentowy zapadania θ̂, wykonany, wynik NIEOCZEKIWANY

`test_frailty_boundary_collapse_test7` (60 powtórzeń/θ, jak D-022): odsetek na granicy jest
NISKI na tej strukturze (0–1,7%, nie 60% jak w Teście 6 przy θ=0) — ale **mediana θ̂ wynosi
1,4–1,6 niezależnie od θ prawdziwego, włącznie z θ=0**. Zweryfikowane, że to nie awaria
wielostartu: wszystkie 4 starty zbiegają do tego samego θ̂≈1,60 (przy θ_prawdziwe=0),
z log-wiarygodnością (−189,13) WYŻSZĄ niż na granicy (−192,14, = pulowany) — **to jest
prawdziwe, dobrze zidentyfikowane maksimum, nie błąd optymalizacji**. Przy tylko 11 z 101
grup niosących ≥2 zdarzenia (informujących o kruchości), gamma-kruchość MLE ma tendencję do
znajdowania pozornej heterogeniczności nawet bez prawdziwej — **poważniejszy problem niż
„szeroki przedział" przewidywany w brief §5**: to nie kwestia szerokości wokół prawdy, tylko
systematyczne przesunięcie punktowe, dobrze zidentyfikowane, więc bez prostego sygnału
ostrzegawczego typu „θ̂ na granicy". Wpływa na `k̂` orzekający (kruchość), nie tylko na `θ̂`.
**Nie rozstrzygnięte samodzielnie — zgłoszone do oceny przed Etapem C**, analogicznie do
D-022, ale poważniejsze.

### Brak 2 — model zerowy N1 liczył niewłaściwą statystykę, naprawione

`run_n1_test7` liczył `k_obs` i surogaty wyłącznie przez `fit_pooled`, podczas gdy
statystyką orzekającą w Teście 7 jest `fit_frailty` (§7 protokołu) — diagnostyka
(D-029 pkt 2) nie odpowiadała na pytanie, dla którego powstała. **Naprawione:** liczy teraz
obie wersje, `pooled` (B=2000) i `frailty` (statystyka orzekająca, `B_frailty=500` —
kompromis kosztowy zaakceptowany w przeglądzie), oba `p` raportowane obok siebie.

### Brak 3 — bootstrap nie raportował odsetka θ̂ na granicy, naprawione

`bootstrap_ci_k_frailty` zwraca ten odsetek od D-022; `ci_p1` woła funkcję i nie
rozpakowywała/etykietowała czwartego elementu zwracanej krotki. Naprawione: `ci_p1` zwraca
`frac_theta_boundary` i flagę `interpretowalny` (próg 30%) jawnie obok przedziału
bootstrapowego dla kruchości. Uwaga zapisana: przy strukturze Testu 7 problemem może być NIE
granica (rzadka, patrz „Brak 1"), więc `frac_theta_boundary` sam nie wykryje rozjazdu w górę
— ma być czytany razem z §3b/§3c `test7_estimate.md`, nie osobno.

### Uwagi niebolkujące, uwzględnione

**Realizm cenzurowania w symulacji.** Stosunek mediany cenzurowanej do mediany pełnej: w
danych realnych **2,25** (18 wobec 8 lat), w symulacji **0,90** — symulacja nie odtwarza
asymetrii realnych danych (cenzurowane obserwacje są tam typowo znacznie dłuższe). Wyniki
symulacji odzysku mają być czytane orientacyjnie, nie jako precyzyjna kalibracja. Nie
naprawiane teraz.

**14 diad typu Troi.** Diady, których jedyna wojna zakończyła rywalizację, nie wnoszą nic do
modelu głównego (§1 `test7_estimate.md`) — nie obciąża to estymacji, ale zmienia, o czym
test orzeka: populacja dobrana po stawce (nie po liczbie wojen) miała objąć właśnie takie
pary, a model główny i tak ich nie widzi. Ma trafić do ograniczeń raportu Etapu C.

### Rozstrzygnięcie

Cztery punkty blokujące (luka 2, braki 1-3) naprawione. Bieg na danych rzeczywistych
pozostaje **zablokowany** — kod wymaga ponownego przeglądu (bez dodatkowej tury zgodnie z
§7 przeglądu, „po ich wykonaniu przegląd kodu bez ponownej tury"), a Etap C wymaga osobnej,
jawnej autoryzacji autora, analogicznie do D-027. Odkrycie o rozjeździe θ̂ (Brak 1) ma zostać
ocenione przed tą autoryzacją — wpływa na to, jak czytać `k̂` orzekający, nie jest samo w
sobie powodem do zatrzymania budowy kodu, ale jest powodem do namysłu przed biegiem.

## D-031 · 2026-08-27 · Symulacja odzysku miała zły mechanizm cenzurowania — „rozjazd θ̂" z D-030 WYCOFANY

**Kontekst.** Drugi przegląd `test7_estimate.py` wykrył usterkę we własnym kodzie
recenzenta, wcześniej zatwierdzonym: `simulate_dataset_test7` (i analogicznie
`test6_weibull.simulate_dataset`) ustalała z góry liczbę zdarzeń pełnych i istnienie
obserwacji cenzurowanej (z realnej struktury, `group_specs`), a czas cenzurowania losowała
**niezależnie** od czasów zdarzeń. W rzeczywistości obserwacja jest cenzurowana, gdy czas
administracyjny wypada PRZED zdarzeniem — widzimy `min(T,C)`, a liczba zdarzeń pełnych jest
WYNIKIEM tego wyścigu, nie założeniem wejściowym. Stara konstrukcja nigdy nie odtwarzała
tego wyścigu — zdarzenie i cenzurowanie „nigdy się nie spotykały".

**Zmierzone przez recenzenta (k_prawdziwe=1):** właściwy mechanizm daje nieobciążone k̂ na
każdym poziomie cenzurowania (mediana 0,989–1,013 przy 15%/34%/48% cenzurowania). Stara
konstrukcja jest nieobciążona TYLKO, gdy skala cenzurowania przypadkiem równa się λ (mediana
1,025) — i zaniża k̂ o **jedną trzecią** przy skali 2,5×λ (mediana 0,670). Realne dane leżą
dokładnie w tym drugim reżimie: stosunek median cenzurowane/pełne = 2,25.

### Naprawa

`window_lengths_from` (nowa funkcja) odczytuje realną długość okna administracyjnego per
diada — Σ wszystkich realnych `ekspozycja` tej diady w modelu głównym. To fakt
**egzogeniczny/strukturalny** (długość okna wynika z dat kalendarzowych i członkostwa w
systemie, nie z procesu wojen, który mamy zmierzyć) — analogiczne do `T` już używanego w
`test6_null.py`/D-026 (λ̂=n/T per diada), nie nowe naruszenie zasady „nigdy wartości t".
`simulate_dataset_test7` symuluje teraz właściwy wyścig: kolejne odstępy T losowane, dopóki
suma mieści się w oknie (pełne); pierwszy, który by je przekroczył, ucina się do reszty
okna (cenzurowany). **Liczba zdarzeń pełnych jest wynikiem symulacji, nie parametrem
wejściowym** — dokładnie tak, jak zażądał przegląd.

### WYCOFANIE — D-030 „spuriously podwyższone θ̂"

D-030 zgłosiło (na podstawie starego, wadliwego mechanizmu): θ̂ na strukturze Testu 7 nie
zapada się do granicy jak w Teście 6, tylko konsekwentnie ląduje w dobrze zidentyfikowanym,
ale spuriously podwyższonym miejscu (mediana 1,4–1,6) NIEZALEŻNIE od θ prawdziwego, z
weryfikacją, że wszystkie 4 starty multistartu zbiegały do tego samego, lepszego niż granica,
optimum. **Po naprawie mechanizmu to zjawisko ZNIKA.** Pomiar procentowy powtórzony
(60 biegów/θ, poprawiony mechanizm): odsetek na granicy maleje monotonicznie z θ prawdziwym
(48,3%/26,7%/16,7%/3,3% dla θ=0/0,3/0,6/1,0), mediana θ̂ rośnie w stronę prawdy (0,0088 →
0,950) — **wzorzec analogiczny do D-022 (Test 6)**, nie odrębny, poważniejszy problem.

Wielostart faktycznie konsekwentnie zbiegał do jednego optimum za każdym razem — ale było to
optimum WŁAŚCIWE DLA ŹLE SKONSTRUOWANYCH DANYCH SYNTETYCZNYCH, nie realna własność struktury
Testu 7 ani artefakt samego wielostartu. **Wniosek D-030 o „poważniejszym problemie niż
brief §5 przewidywał" jest niniejszym wycofany** — analogicznie do tego, jak sam recenzent
wycofał własne wcześniejsze podejrzenie o usterce przy θ→0 (sprawdził: różnica maleje
liniowo z θ, zachowanie poprawne).

### Zadeklarowane odchylenie — przeliczone dla obu testów (zlecone przez recenzenta)

SD(k̂) pod prawdą k=1/θ=0, poprawiony mechanizm, λ skalibrowane do realnej liczby zdarzeń:

| test | statystyka orzekająca | n grup | n powtórzeń | mediana k̂ | SD k̂ |
|---|---|---|---|---|---|
| Test 6 | pulowana | 18 | 300 | 1,010 | **0,127** |
| Test 7 | kruchość | 101 | 150 | 1,013 | **0,138** |

Test 6: 0,127, praktycznie identyczne z wcześniej deklarowanym „~0,12" — `test6_weibull.
simulate_dataset` domyślnie losuje cenzurowanie ze skalą `censor_scale=lam`, dokładnie
przypadek, który recenzent zmierzył jako przypadkowo nieobciążony; **deklaracja Testu 6
nie wymaga korekty.** Test 7: 0,138, nieco niżej niż wcześniej cytowane „~0,15" — różnica w
granicach szumu (150 vs 300 powtórzeń), nie precyzyjna do trzeciego miejsca.

### Rozkład liczby zdarzeń na diadę (zażądane przez recenzenta)

Struktura Testu 7 (101 diad modelu głównego): 0 zdarzeń — 82 diady, 1 — 8, 2 — 5, 3 — 5,
4 — 1.

### Uwaga metodologiczna do zachowania

Ta sama klasa błędu co D-023/D-026/D-030 §Luka2: usterka wykryta przez konstrukcję
(zamrożony protokół, druga para oczu, obowiązek pomiaru zamiast założenia), nie przez wynik
— żadna z tych usterek nie byłaby widoczna w samych liczbach końcowych. Trzecia z rzędu
usterka wykryta we własnym, wcześniej zatwierdzonym kodzie recenzenta — odnotowana przez
niego wprost, bez próby ukrycia wcześniejszego zatwierdzenia.

### Zakres

Dotyczy wyłącznie narzędzia symulacji odzysku/testów poprawności (`simulate_dataset_test7`,
`test6_weibull.simulate_dataset`) — używanego do deklarowania oczekiwanej precyzji i
testowania własności estymatora na danych syntetycznych o znanej prawdzie. **Nie dotyczy
decyzyjnego wyniku Kroku C Testu 6** (D-027, p=0,068) — ten wynik pochodzi z `test6_null.py`
(model N1), który używa realnej wartości `c` per diada trzymanej na stałe, nie symulowanej
z arbitralnego rozkładu, więc nie ma tej usterki z konstrukcji.

## D-032 · 2026-09-02 · Trzy decyzje autora: kolejność Etapu C, brak deklaracji szczytu, dopuszczalny dryf fazy

*Wpis przekazany przez autora w całości, wklejony bez skrótów — dokument źródłowy
`D032.md`.*

### 1. Etap C Testu 7 odłożony do czasu modelu ze zmiennymi objaśniającymi

Bieg P1 na obecnym zbiorze **nie jest uruchamiany teraz**. Powód zadeklarowany przed
odłożeniem: przy 37 zdarzeniach i odchyleniu `k̂` około 0,138 przedział wykluczy jedynkę
dopiero przy wartości poniżej 0,73 albo powyżej 1,27, a efekt zaobserwowany w Teście 6
wynosił 0,778. Model ze zmiennymi objaśniającymi wyciąga z tej samej liczby zdarzeń więcej
informacji.

**To jest odłożenie, nie anulowanie.** P1 pozostaje wariantem orzekającym dla H9b.1 i
zostanie policzony. Kolejność zmienia się tak, że najpierw powstaje warstwa danych dla P2.

**Zapisane dla porządku:** decyzja zapada bez znajomości wyniku P1, który nie został
policzony na danych rzeczywistych. Blokada `--run-real` pozostaje aktywna.

### 2. Położenie szczytu hazardu — autor świadomie NIE deklaruje przedziału

Do §4 protokołu 9c: **autor nie podaje przedziału dla położenia maksimum hazardu**,
z uzasadnieniem, że wskazanie tej wartości jest zadaniem testu, a nie jego założeniem.

**Konsekwencja, zapisana przed biegiem.** Test odpowiada wyłącznie na pytanie, **czy garb
istnieje**, a nie na pytanie, czy wypada tam, gdzie przewiduje hipoteza. Jest to test
**słabszy** od wersji z zadeklarowanym przedziałem:

- wynik pozytywny stwierdzi tylko tyle, że hazard nie jest monotoniczny;
- **nie potwierdzi żadnej konkretnej długości cyklu**;
- położenie szczytu, które z niego wyjdzie, jest wielkością **oszacowaną, nie potwierdzoną**,
  i nie wolno jej później przedstawiać jako przewidzianej.

Stanowisko autora jest spójne z D-005, które ustaliło, że okres 35,1 roku jest produktem
łańcucha przetwarzania, a nie wielkością mierzoną. Autor nie ma zatem liczby, do której
mógłby się zobowiązać, i deklarowanie jej wyłącznie po to, żeby wzmocnić test, byłoby
zobowiązaniem pozornym.

**Zakaz wynikający z tej decyzji.** Jeżeli test wskaże szczyt w okolicy jakiejkolwiek liczby
bliskiej wcześniejszym hipotezom, **nie wolno tego przedstawiać jako potwierdzenia**.
Zbieżność liczby nieprzewidzianej z liczbą wcześniej wymienianą nie jest predykcją.
To zdanie ma stać w raporcie niezależnie od wyniku.

### 3. Dopuszczalny dryf fazy: 5–7 lat (D-009 zamknięte)

Autor deklaruje dopuszczalny dryf fazy na **5 do 7 lat**. Zamyka to pytanie otwarte od
D-009.

**Operacjonalizacja, konieczna, bo sama liczba nie jest jeszcze regułą.** Przyjmuję
i wprowadzam do protokołu 9c oraz do wznowionego wariantu D-009:

> Dryf mierzy się jako **różnicę położenia maksimum hazardu między epokami** wyznaczonymi
> podziałem na okres przed 1914 i po 1914 (ten sam podział co S5 Testu 6). Zjawisko uznaje
> się za **to samo zjawisko przesunięte**, a nie za dwa różne, jeżeli różnica położeń nie
> przekracza zadeklarowanego progu.

**Wariant pierwszorzędny: 7 lat. Wariant wrażliwości: 5 lat.**

Wybór szerszej wartości jako pierwszorzędnej jest celowy i wymaga wyjaśnienia, bo działa
w obie strony. Większa dopuszczalna tolerancja **ułatwia** uznanie zjawiska za wspólne, więc
wynik negatywny przy siedmiu latach jest mocny, a wynik pozytywny słaby. Odwrotnie przy
pięciu. Raport ma podać obie wartości obok siebie i ta asymetria ma być w nim nazwana.

**Zastrzeżenie o mocy.** Przy 37 zdarzeniach w Teście 7 i 45 w Teście 6 podział na dwie
epoki zostawia po około dwadzieścia zdarzeń na epokę. Oszacowanie położenia szczytu w każdej
z nich będzie miało przedział ufności prawdopodobnie szerszy niż sam próg siedmiu lat.
**W takim wypadku test dryfu nie rozstrzygnie niczego** i ta możliwość ma zostać zapisana
teraz, przed biegiem, a nie użyta później jako wyjaśnienie.

### 4. Kolejność zmiennych objaśniających — odłożona świadomie

Autor nie deklaruje jeszcze kolejności czterech zmiennych z §6 protokołu Testu 7. Decyzja
odłożona do czasu, gdy powstanie warstwa danych.

**Warunek wiążący:** kolejność musi zostać zadeklarowana **przed pierwszym dopasowaniem
modelu ze zmiennymi**, nie po. Do tego czasu Code buduje wyłącznie warstwę danych i nie
uruchamia żadnej estymacji z udziałem zmiennych objaśniających.

### 5. Skutek dla harmonogramu

1. Pobranie i weryfikacja NMC, budowa czterech zmiennych → **STOP**
2. Deklaracja kolejności zmiennych przez autora → zamrożenie
3. Symulacja mocy dla protokołu 9c (§7 szkicu) → **STOP**, decyzja o uruchomieniu 9c
4. Etap C Testu 7 z P2, potem P1

## D-033 · 2026-09-02 · NMC pobrane i zweryfikowane; warstwa danych P2 zbudowana dla 3 z 4 zmiennych — status mocarstwowy zablokowany brakiem `majors2016.csv`

**Kontekst.** Wykonanie kroku 1 harmonogramu D-032 §5: pobranie COW NMC, weryfikacja, budowa
warstwy danych dla czterech zmiennych §6 protokołu. Żadna estymacja nie uruchomiona.

### NMC — pobrane i zweryfikowane

Sklonowane `svmiller/peacesciencer` z tym samym commitem co `tss_rivalries.rda`
(`fe150a2648056fbd4fbbbd833f0c9e437b2ed04b`), plik `data/cow_nmc.rda` skopiowany do repo
(`code/cps/data/rivalries/cow_nmc.rda`). Zweryfikowane bezpośrednio: suma kontrolna
`c265ab4ffa73c87ddc565ce08a12963e8a6aa5020a56e3658108add14b24e82d` (zgadza się z podaną
`c265ab4f...`), 17121 wierszy, kolumny `ccode, year, milex, milper, irst, pec, tpop, upop,
cinc` (zgadza się), zakres lat 1816–2022 (zgadza się), zero braków w `cinc` w całym zbiorze
i w szczególności w oknie Testu 7 (1816–2007).

### Wersja — sprawdzona, NIEZGODNA z §12 protokołu, ujawniona zgodnie z instrukcją

Dokumentacja źródłowa (`data-raw/cow_nmc.R`, `man/cow_nmc.Rd` w klonie peacesciencer)
potwierdza wprost: *„These are version 7.0 of the Correlates of War National Military
Capabilities data."* `TEST7_PROTOCOL.md` §12 wymienia `NMC_v6.0`. **To jest niezgodność
wersji, nie podmieniona po cichu:**

- **Konsekwencja dla okna do 2007, nieznana co do wielkości.** v6.0 i v7.0 mogą się różnić
  nie tylko zasięgiem lat (2016 vs 2022), ale też rewizjami wartości historycznych CINC
  wewnątrz okna 1816–2007 — dokumentacja NMC ostrzega wprost o niespójnościach nawet
  wewnątrz jednej wersji (np. suma CINC ≠ 1 w większości lat). Brak dostępu do v6.0 do
  bezpośredniego porównania w tym kroku.
- **Rozstrzygnięcie operacyjne (Code, nie autor):** użyto v7.0, bo to jedyna wersja
  dostępna przez wskazany kanał (D-032, svmiller/peacesciencer, ten sam commit co
  rywalizacje) — jawnie oznaczone w metadanych wyjściowego pliku
  (`test7_p2_variables.csv`, klucz `nmc_wersja`), nie milcząco przyjęte. Kompletność
  (brak braków w oknie) nie jest problemem niezależnie od wersji.
- **Do potwierdzenia przez autora** przed jakąkolwiek estymacją z udziałem CINC: czy v7.0
  jest akceptowalna, czy potrzebne jest dotarcie do v6.0 konkretnie.

### Status mocarstwowy — NIEZBUDOWANY, `majors2016.csv` brak w repo

`TEST7_PROTOCOL.md` §12 twierdzi „w repo" dla `majors2016.csv` (razem z `system2016.csv`) —
sprawdzone bezpośrednio: plik **nie istnieje** nigdzie w repozytorium, `system2016.csv` nie
ma kolumny oznaczającej mocarstwo. Zmienna „status mocarstwowy" (0/1/2 mocarstwa w diadzie)
**nie została zbudowana** — brakuje jej wprost w wyjściu (`test7_p2_variables.csv` nie ma tej
kolumny), nie zastąpiona substytutem. Trzy pozostałe zmienne (czas trwania, straty, CINC)
zbudowane w całości.

### Warstwa danych P2 — liczby (D-028)

`test7_build_p2_variables.py`, wyjście `test7_p2_variables.csv`:

| | liczba |
|---|---|
| wiersze modelu głównego (t0, ucieta wyłączone) | 132 |
| z tego kandydujące do P2 (`pelny`+`cenzurowany`, wyłączone `cenzurowany_bez_epizodow`) | 77 |
| P2 z dopasowanym poprzednim epizodem | **77 (100%)** |
| P2 bez dopasowania | 0 |
| diady ze 101 mające ≥1 wiersz P2 | **46** |

**Pokrycie per zmienna (spośród 101 diad modelu głównego, pełne pokrycie = wszystkie
wiersze P2 tej diady mają wartość, nie tylko część):**

| zmienna | diady w pełni pokryte |
|---|---|
| czas trwania poprzedniego epizodu | 46 / 101 |
| straty (BatDeath, suma diady, log) | 46 / 101 |
| CINC (suma + stosunek, rok końca epizodu) | 46 / 101 |
| status mocarstwowy | **0 / 101 — zablokowane** |

Pokrycie identyczne (46/46) dla trzech zbudowanych zmiennych — zero braków wewnątrz
populacji P2-kwalifikującej się (77 wierszy, wszystkie trzy zmienne policzalne dla każdego).
Górne ograniczenie pokrycia to sama definicja P2 (§6 protokołu wyklucza `t0` i diady bez
epizodów z definicji) — 46/101 to nie usterka, to rozmiar populacji, dla której H9b.2 jest
w ogóle zdefiniowana.

### Zakres roku dla CINC — decyzja techniczna, do potwierdzenia

Protokół §6 nie podaje explicite roku odniesienia dla CINC (w przeciwieństwie do statusu
mocarstwowego, „w roku końca epizodu"). Przyjęto konsekwentnie **rok końca poprzedniego
epizodu**, tę samą regułę co dla statusu mocarstwowego — wybór implementatora, nie
rozstrzygnięcie protokołu, do potwierdzenia przy deklaracji kolejności zmiennych (D-032 §4).

### STOP

Żadna estymacja z udziałem tych zmiennych nie uruchomiona, zgodnie z D-032 §4. Czeka na:
(a) potwierdzenie akceptowalności NMC v7.0, (b) dostarczenie lub rezygnację z
`majors2016.csv`, (c) deklarację kolejności wprowadzania zmiennych przez autora — dopiero
wtedy pierwsze dopasowanie modelu ze zmiennymi.

## D-034 · 2026-09-02 · Wariant B: dwa modele ze zmiennymi objaśniającymi, z podziałem populacji i regułami zadeklarowanymi przed biegiem

*Wpis przekazany przez autora w całości, wklejony bez skrótów — dokument źródłowy
`D034.md`. Realizuje wybór autora spośród trzech możliwości z D-033 §4. Zastępuje
nierozstrzygniętą deklarację kolejności zmiennych z D-032 §4.*

### 1. Podział na dwa modele

| id | zmienne | populacja | pytanie |
|---|---|---|---|
| **P2a** | potencjał gospodarczy (`cinc`), status mocarstwowy | **132 wiersze, 101 diad** — pełna, wraz z parami, które nigdy nie walczyły | czy ryzyko wojny zależy od siły i pozycji stron |
| **P2b** | czas trwania poprzedniego epizodu, straty w poprzednim epizodzie | **77 wierszy, 46 diad** — wyłącznie pary, które już walczyły | czy poprzednia wojna wydłuża regenerację |

Podział wynika z dostępności zmiennych, nie z wyboru. Dwie górne zmienne są określone dla
każdej pary i każdego roku. Dwie dolne wymagają poprzedniego epizodu i dla par, które nigdy
nie walczyły, po prostu nie istnieją.

### 2. Który model orzeka — deklaracja przed biegiem

§7 protokołu ustanawia P2 jako orzekające dla **H9b.2**. Po podziale trzeba wskazać, który
z dwóch przejmuje tę rolę, i wskazanie musi paść teraz.

**Orzeka P2a.** Powód: zachowuje populację, dla której zbudowano Test 7, w tym pięćdziesiąt
sześć par bez ani jednej wojny. Model, który je usuwa, nie może orzekać o hipotezie
sformułowanej dla populacji dobranej po stawce.

**P2b jest wariantem opisowym.** Odpowiada na pytanie węższe, o pary, które już walczyły,
i jego wynik nie wchodzi do żadnej reguły decyzyjnej. Ma być tak oznaczony w raporcie,
w tytule tabeli, a nie tylko w przypisie.

### 3. Trzy zakazy, konieczne właśnie przy dwóch modelach

**Zakaz wyboru po fakcie.** Nie wolno po zobaczeniu wyników uznać P2b za orzekające ani
przedstawić go jako „model właściwy". Role są rozdane w §2 i nie zmieniają się.

**Zakaz doboru zmiennych.** W każdym modelu **obie zmienne wchodzą naraz**. Nie ma selekcji
krokowej, nie ma usuwania zmiennej nieistotnej, nie ma modelu z jedną zmienną prezentowanego
jako główny. Przy trzydziestu siedmiu zdarzeniach i pięciu parametrach łącznie mamy około
siedmiu zdarzeń na parametr, co jest na granicy dopuszczalności i nie zniesie żadnego
majstrowania.

**Reguła rozbieżności, zadeklarowana zanim ją zobaczymy.** Jeżeli P2a i P2b wskażą przeciwne
kierunki dla czegokolwiek wspólnego, **nie rozstrzygamy tego na korzyść żadnego z nich**.
Raport ma stwierdzić, że modele na różnych populacjach dały różne odpowiedzi, i wskazać
podział populacji jako najbardziej prawdopodobną przyczynę.

### 4. Kolejność uruchomień

**P1 idzie pierwsze.** H9b.1 jest hipotezą pierwszorzędną i to dla niej zbudowano populację
stu jeden diad. Odkładanie go za modele ze zmiennymi odwracałoby kolejność ważności,
na co zwróciłem uwagę w D-033 §4.

1. **P1** bez zmiennych, sto jeden diad, model z kruchością — **orzeka o H9b.1**
2. **P2a** — **orzeka o H9b.2**
3. **P2b** — opisowy
4. Warianty S1 i S3 z §8 protokołu, bo reguła decyzyjna wymaga utrzymania kierunku w obu

Każdy krok kończy się zapisem wyniku, zanim ruszy następny. Nie wolno oglądać wszystkich
naraz i dopiero potem opisywać.

### 5. Ograniczenia do zapisania teraz

**Moc.** Pięć parametrów na trzydzieści siedem zdarzeń w P2a. Przedziały ufności dla
współczynników będą szerokie i najbardziej prawdopodobnym wynikiem jest brak rozstrzygnięcia.
To zdanie ma stać w raporcie przed wynikiem.

**Zapadanie się kruchości.** Nadal obowiązuje D-022: jeżeli `θ̂` osiądzie na granicy, model
orzekający jest w praktyce pulowany. Odsetek replik bootstrapowych z `θ̂` na granicy podawany
obok każdego przedziału.

**Wersja NMC.** Używamy v7.0 zamiast v6.0 wymienionej w §12 protokołu, zgodnie z D-033 §2.
Różnica wartości `cinc` względem v6.0 pozostaje niezmierzona, chyba że próba pobrania
starszego wydania się powiedzie.

**P2b nie zastępuje P1.** Jego populacja jest zawężona przez kryterium, które Test 7 miał
usunąć, czyli przez to, czy para w ogóle walczyła. To ma być powiedziane wprost w raporcie,
nie pozostawione czytelnikowi do wywnioskowania.

## D-035 · 2026-09-02 · Wykonanie D-034: majors podmienione (bez rozbieżności treści), P2a/P2b zbudowane, NMC v6.0 odnalezione i zmierzone

**Kontekst.** Wykonanie zleceń „Dla Code" z D-034: status mocarstwowy przez `cow_majors.rda`,
budowa P2a/P2b z rozbiorem i pokryciem, próba pobrania NMC v6.0 z pomiarem różnicy. Żadna
estymacja nie uruchomiona.

### Status mocarstwowy — źródło podmienione, TREŚĆ zgodna

`cow_majors.rda` skopiowane z tego samego commitu `svmiller/peacesciencer` co NMC i
rywalizacje. Suma kontrolna `673cb752c2d1af045ea8e2c602b45bc037b84dda9537bfb060142ff255c7f2b6`
— zgadza się z podaną. Zawartość zweryfikowana bezpośrednio: **14 wierszy, pole `version`
równe 2016 na wszystkich** — potwierdza, że to ta sama wersja co nazwany w protokole
`majors2016.csv` (§12), plik którego fizycznie nie ma w repozytorium (D-033). **Niezgodność
z §12 dotyczy wyłącznie nazwy/ścieżki źródła, nie treści** — odnotowana tym samym trybem co
przy NMC, nie podmieniona po cichu.

### NMC v6.0 — ODNALEZIONE i zmierzone (próba się powiodła)

Historia `svmiller/peacesciencer` (fetch do 491 commitów, poza domyślną płytką kopią)
pokazuje commit `4b2a02d` („update cow_nmc to v. 7.0"), którego rodzic `28cb294` ma
`data-raw/cow_nmc.R` wskazujące dosłownie na `NMC-60-abridged.csv` — **genuinie NMC v6.0**.
Wyodrębniony `data/cow_nmc.rda` z tego commitu: 15951 wierszy (nie 17121), zakres lat
**1816–2016** (nie 2022) — zgodne co do joty z oczekiwaniem „kończy się ok. 2016".

**Pomiar różnicy `cinc` na oknie do 2007, dla 101 ccode Testu 7** (8732 dopasowane pary
ccode-rok): **mediana różnicy względnej = 0,0** (dosłowne zero — zdecydowana większość
wartości identyczna między wersjami), **maksimum różnicy względnej ≈ 10,2%** (ccode 692,
Bahrajn, lata 2001–2006 — mały kraj, mały mianownik, różnica bezwzględna rzędu 4-5
dziesięciotysięcznych). Tylko 216 z 8732 par (2,5%) ma różnicę względną powyżej 1%.

**Wniosek: podmiana v7.0→v6.0 (D-033) ma znikomą konsekwencję praktyczną dla okna do 2007.**
Rewizje między wersjami są rzadkie, małe, i skupione na małych państwach o marginalnym
wpływie na `cinc_suma`/`cinc_stosunek` diad Testu 7. `cow_nmc_v6_weryfikacja.rda` zachowane
w repo jako dowód tej weryfikacji, NIE jako źródło używane do budowy zmiennych (P2a nadal
liczy z v7.0, zgodnie z D-033/D-034 §5 — sama różnica jest teraz zmierzona, nie tylko
domniemana).

### P2a/P2b — zbudowane (`test7_build_p2ab_variables.py`)

| | P2a | P2b |
|---|---|---|
| wiersze | 132 | 77 |
| diady | 101 | 46 |

**Rozbiór 132→77 (zadanie z D-034):** P2b zachowuje **37 wierszy `pelny` + 40 wierszy
`cenzurowany`** = 77. **Wszystkie 37 zdarzeń pełnych modelu głównego przetrwały** —
potwierdzone wprost (żadne nie odpadło przy dopasowaniu do poprzedniego epizodu: 77 na 77
kandydujących wierszy dopasowanych, zero bez dopasowania, zgodnie z wcześniejszym pomiarem
D-033).

**Pokrycie (pełne pokrycie diady = wszystkie jej wiersze modelu mają wartość):**

| zmienna | model | pełne pokrycie |
|---|---|---|
| `cinc_suma` (+ stosunek) | P2a | **101 / 101** |
| status mocarstwowy | P2a | **101 / 101** |
| czas trwania poprzedniego epizodu | P2b | **46 / 46** |
| straty (BatDeath, log) | P2b | **46 / 46** |

Zero braków w żadnej z czterech zmiennych, w obu populacjach.

### STOP

Żadna estymacja nie uruchomiona. Kolejność uruchomień z D-034 §4 (P1 → P2a → P2b → S1/S3,
zapis wyniku po każdym kroku) przyjęta do wykonania, gdy padnie osobna autoryzacja Etapu C —
blokada `--run-real` pozostaje aktywna, zgodnie z D-034 §4. S1 (wykluczenie epizodów
1914–18/1939–45, wymaga przebudowy sekwencji zdarzeń) nadal niezbudowane — zgłoszone już w
`test7_estimate.md` §5, poza zakresem tego wpisu.

## D-036 · 2026-09-02 · S1 zbudowany (reguła okna, D-035); sprostowanie do pytania o Bahrajn

**Kontekst.** Wykonanie zleceń z wiadomości po potwierdzeniu D-035: budowa S1 wg reguły
okna, oraz dosprawdzenie maksimum różnicy `cinc` v6/v7 ograniczonego do kodów państw
Testu 7. Żadna estymacja nie uruchomiona.

### S1 — mechanizm

`test7_build_s1.py`: lata epizodu przecinającego 1914–1918 albo 1939–1945 (przecięcie, nie
zawieranie) wycięte z `periods` diady — dokładnie ten sam mechanizm co istniejąca przerwa
między okresami rywalizacji (Chiny–Japonia), bez żadnej zmiany w `classify_events`/
`diad_rows`/`exposure_multi` (reużyte z `test7_build_windows.py` bez modyfikacji, nakarmione
już przyciętymi `periods`/`episodes`). Odstęp przed wykluczonym epizodem domyka się jako
cenzurowany na roku jego startu; po roku jego końca otwiera się nowy odcinek okna.

**Test spójności (obowiązkowy, wykonany):** 92 diady bez żadnego epizodu przecinającego
wojny światowe dają w S1 wiersze **identyczne co do wartości** z P1 — potwierdzone
bezpośrednim porównaniem (`test_spojnosci_diady_niedotkniete_identyczne_z_P1: true`).

### Liczby przed biegiem (zadanie z wiadomości)

- **Epizody wypadłe: 34**, dotykające **28 diad**.
- **1 diada (France–Thailand) traci całe okno** — jedyny epizod (Franco-Thai, 1940–41) był
  jednocześnie jedynym źródłem okna ryzyka tej pary; po wykluczeniu okno puste, diada
  wypada z S1 w całości. W P1 ta diada i tak nie wnosiła nic do modelu głównego (jedyny
  wiersz to `t0` o zerowej rozpiętości — Skutek A natychmiastowy), więc nie ubywa żaden
  wiersz modelu głównego P1.
- **8 diad zyskuje wiersz modelu głównego, którego nie miały w P1** (Austria-Hungary–
  Yugoslavia, France–Italy, Germany–Poland, Hungary–Yugoslavia, Italy–Ethiopia, United
  Kingdom–Germany, United Kingdom–Japan, United States of America–Japan) — mechanizm:
  w P1 ich JEDYNY epizod kwalifikujący był epizodem wojny światowej ze Skutkiem A (D-021),
  więc wnosiły zero wierszy do modelu głównego; w S1 ten epizod przestaje kwalifikować,
  więc diada staje się `cenzurowany_bez_epizodow` na całym oknie. Żadna diada nie traci
  wiersza, który miała w P1 (zbiór P1∖S1 na poziomie diad modelu głównego jest pusty).

| | P1 (model główny) | S1 (model główny) |
|---|---|---|
| wiersze | 132 | 131 |
| pełne (zdarzenia) | 37 | **23** |
| cenzurowane | 95 | **108** |
| diady | 101 | 109 |

**Kierunek zgodny z oczekiwaniem D-035 §3** („spadek liczby zdarzeń i wzrost cenzurowania,
czyli mniejsza moc niż P1") — sprawdzone programowo (`kierunek_zgodny_z_D035_SS3: true`),
nie tylko opisowo. Spadek zdarzeń jest istotny (37→23, −38%), zgodnie z przewidywaniem.

### NMC v6/v7 — sprostowanie, nie nowy pomiar

Poprzednio podane maksimum różnicy względnej (≈10,2%, ccode 692) **już było** ograniczone
do kodów państw ze stu jeden diad Testu 7 (zbiór `ccode_a`/`ccode_b` modelu głównego,
zweryfikowany jako dokładnie 101 unikalnych kodów). **Ccode 692 to Bahrajn, i JEST w tej
populacji** — diada `BAH–Qatar` (ccode 692/694) jest jedną ze stu jeden diad modelu
głównego, zweryfikowane bezpośrednio. Przypuszczenie, że Bahrajn „najpewniej" nie występuje
w tej populacji, jest błędne — sprawdzone, nie założone. Liczba się nie zmienia: **mediana
różnicy względnej = 0,0, maksimum ≈ 10,2% (Bahrajn–Katar, ccode 692, lata 2001–2006)**,
216 z 8732 dopasowanych par ccode-rok (2,5%) powyżej 1% różnicy.

### STOP

Żadna estymacja nie uruchomiona. Wraz z S1, S3 (już gotowe od Etapu B, `test7_estimate.py`
`load_grouped(include_t0=True)`) i P2a/P2b (D-035), komplet zbiorów wymaganych przez
regułę decyzyjną §8 protokołu jest na miejscu. Kolejność uruchomień (D-034 §4): P1, P2a,
P2b, S1, S3, każdy z zapisem wyniku przed kolejnym krokiem. Blokada `--run-real` pozostaje
do osobnej, jawnej autoryzacji Etapu C przez autora.

## D-037 · 2026-09-02 · Autoryzacja Etapu C Testu 7

*Wiadomość nazywała ten wpis „D-036" — numer już zajęty (S1/sprostowanie Bahrajnu, wpis
powyżej, ten sam dzień). Użyty następny wolny numer, D-037, żeby nie nadpisywać ani nie
przenumerowywać istniejącego wpisu w dzienniku append-only. Odnotowane jawnie, nie
przemilczane.*

**Rozstrzygnięcie (autor).** Etap C Testu 7 autoryzowany. Blokada `--run-real` zdjęta.

**Zapisane przed jakimkolwiek dopasowaniem na danych rzeczywistych** — autoryzacja zapadła
bez znajomości jakiegokolwiek wyniku P1/P2a/P2b/S1/S3 na `test7_intervals.csv` i pochodnych
(żaden z tych biegów nie został wykonany przed tym wpisem).

### Kolejność uruchomień (bez zmian wobec D-034 §4)

1. **P1** — bez zmiennych, 101 diad, model z kruchością — orzeka o H9b.1.
2. **P2a** — potencjał gospodarczy + status mocarstwowy, pełna populacja — orzeka o H9b.2.
3. **P2b** — czas trwania + straty poprzedniego epizodu, 46 diad — opisowy.
4. **S1 i S3** — wymagane przez regułę §8.

Każdy krok kończy się zapisem wyniku, zanim ruszy następny.

### Wymogi obowiązkowe do każdego dopasowania

- Oba przedziały: z profilu wiarygodności i bootstrapowy.
- Wartość p z modelu zerowego N1, dla OBU statystyk (pulowanej i kruchości), jawnie
  oznaczona jako diagnostyczna, poza regułą §8 (D-029 pkt 2 / D-026 §5).
- Odsetek replik bootstrapowych z θ̂ na granicy (D-022) — bez niego przedział dla modelu
  z kruchością nie jest interpretowalny.
- `frac_tie` (zabezpieczenie D-026 §7) — obowiązuje nadal.

### Reguła §8 — sprawdzana w obu członach naraz

„H9b.1 uznaje się za wsparte, jeżeli przedział ufności dla k z profilu wiarygodności w P1
nie obejmuje 1 ORAZ ten sam kierunek utrzymuje się w S1 i S3" (protokół §8, cytat z briefu
D-029). **Nie wolno zaraportować spełnienia pierwszego członu jako spełnienia reguły.**
Jeżeli θ̂ osiądzie na granicy w P1, ma to być napisane wprost: model orzekający jest w
praktyce pulowany (D-022) — poprawność formalna reguły tego nie zmienia.

### Deklaracje sprzed biegu — do przepisania do raportu, nie do wyprowadzenia po fakcie

- Odchylenie `k̂` w P1 ≈ 0,138 (D-031 §3e) — przedział wykluczy 1 dopiero przy wartości
  poniżej 0,73 albo powyżej 1,27.
- Pięć parametrów na trzydzieści siedem zdarzeń w P2a (D-034 §3, D-035) — moc niska,
  najbardziej prawdopodobny wynik to brak rozstrzygnięcia.
- Czternaście diad typu Troi, których model główny nie widzi (D-030 §6 `test7_estimate.md`).
- Wersja NMC siódma zamiast szóstej wymienionej w §12 protokołu, maksymalna różnica
  względna `cinc` = 10,2% (Bahrajn–Katar, ccode 692), w populacji 101 diad Testu 7 (D-033,
  D-036).
- **Deklaracja mocy S1 (nowa, przed tym biegiem):** 23 zdarzenia, odchylenie `k̂` rzędu
  0,175, udział cenzurowania 82% (zweryfikowane bezpośrednio na `test7_s1_intervals.csv`:
  23/131=17,6% zdarzeń, 82,4% cenzurowania — zgodne). **Przy tej precyzji niespełnienie
  warunku kierunku w S1 NIE jest świadectwem przeciw hipotezie**: przy prawdziwym k w
  okolicy 0,778 (efekt Testu 6) prawdopodobieństwo, że sam szum wskaże stronę przeciwną
  (k̂>1), wynosi ok. 10% (przybliżenie normalne, z=(1−0,778)/0,175=1,269,
  P(Z>1,269)=0,102 — zweryfikowane bezpośrednio); przy prawdziwym k bliższym 1 (≈0,85)
  rośnie do ok. 20% (z=0,857, P=0,196). **Odwrotnie: spełnienie warunku jest przy tej
  precyzji słabym potwierdzeniem**, z tych samych powodów.

### Reguła rozbieżności (D-034 §3) — obowiązuje

Jeżeli P2a i P2b wskażą przeciwne kierunki dla czegokolwiek wspólnego, nie rozstrzygamy na
korzyść żadnego z nich — raport ma to nazwać wprost, ze wskazaniem podziału populacji jako
najbardziej prawdopodobnej przyczyny.

### STOP po komplecie, przed raportem

Po wykonaniu wszystkich pięciu kroków: **STOP, surowe liczby przedstawione bez narracji,
zanim powstanie ich opis.** Powód zapisany przez autora: raport pisany razem z liczbami zbyt
łatwo staje się ich uzasadnieniem.

---

## D-038 · 2026-09-02 · S7 (poziom państwa, Test 6 poziom B): jednostka progu

**Wpisane PRZED budową zbioru**, zgodnie z TASK_S7.md §2 — decyzja, nie odczyt protokołu.

**Kontekst.** `TEST6_PROTOCOL.md` §3 poziom B wymaga „≥ 6 konfliktów" dla wariantu S7. Po
D-013 (scalanie konfliktów w epizody) pytanie brzmi, czy próg liczyć na SUROWYCH
uczestnictwach (wiersze pliku `InterStateWarData_v4_0.csv`, w tym rozbite fazy) czy na
EPIZODACH (po scaleniu D-024 §5).

**Rozstrzygnięcie: próg liczony na epizodach.** Precedens D-024 §2 dla S1: próg ma zmieniać
wartość przy STAŁEJ jednostce analizy, inaczej wariant miesza dwie osie naraz (jednostkę
progu i jednostkę estymacji). Ta sama jednostka, której używa estymacja (odstęp między
epizodami), ma być jednostką progu.

**Scalanie, D-024 §5 (przywołane, nie ponownie rozstrzygane tutaj):** wszystkie nakładające
się lub stykające się (gap≤0, ta sama definicja co D-013 dla diad) wojny TEGO SAMEGO państwa,
niezależnie od przeciwnika, scalają się w jeden epizod.

**Konsekwencja dla stanu 12 kontra 6 poprzednich testów.** Państwo przy progu ≥6 epizodów ma
istotnie więcej zdarzeń niż jakakolwiek diada w Teście 6 (≥3 epizody) czy Teście 7 — właśnie
dlatego wariant jest atrakcyjny mocą, i właśnie dlatego próg musi być zdefiniowany na tej samej
jednostce, którą się potem estymuje, żeby liczba `12 państw / N zdarzeń` znaczyła to, co ma
znaczyć.

---

## D-039 · 2026-09-02 · Doprecyzowanie D-013: próg scalania epizodów = gap ≤ 0

**Kontekst.** Etap 1 S7 (`test6_build_s7.py` v1.0) dał inne liczby kontrolne niż deklarował
autor (15 państw/123 odstępy pełne wobec deklarowanych 12/98 przy progu ≥6). Autor przyznał,
że jego własne liczby pochodziły z reguły `gap ≤ 1`, nigdzie w `TASK_S7.md` niezapisanej, i
poprosił o sprawdzenie w kodzie, jakiego progu faktycznie użył builder Testu 6, zamiast
rozstrzygać z góry.

**Sprawdzone wprost w kodzie.** `test6_build_intervals.py:86`, funkcja `merge_episodes`:

```python
elif s <= cur["end"]:
```

To jest **gap ≤ 0** (`s_next − end_poprz ≤ 0`, czyli odstęp kalendarzowy zerowy lub ujemny —
epizody stykające się lub nachodzące). Ta sama funkcja jest reużywana bez zmian dla wariantu
głównego, S-A i S-B Testu 6 — nigdzie w tym pliku nie ma żadnej innej tolerancji `gap`.

**Rozstrzygnięcie.** D-013 doprecyzowana: próg scalania epizodów (Test 6, wszystkie warianty
diadowe, oraz S7 poziomu B) to **gap ≤ 0**, bez wyjątków. S7 zmienia wyłącznie jednostkę
analizy wobec Testu 6 (D-038) — reguła scalania musi być identyczna, inaczej porównanie
poziomu par z poziomem państw mieszałoby dwie zmiany naraz.

**Errata.** Liczby kontrolne autora z `TASK_S7.md` §4 (12 państw / 98 odstępów pełnych przy
progu ≥6; 37/168 przy progu ≥3) pochodziły z reguły `gap ≤ 1`, nie `gap ≤ 0` — **błędne**,
idą do erraty. Właściwe liczby pod gap≤0 + D-040 (poniżej) w D-040 §3.

---

## D-040 · 2026-09-02 · S7: uczestnictwa tej samej wojny scalają się niezależnie od odstępu

**Kontekst.** Pięć przypadków w `InterStateWarData_v4_0.csv`, gdzie państwo ma DWA wpisy dla
tego samego `WarNum` — zmiana strony lub wznowienie udziału w trakcie tej samej wojny:
Francja (WWII, faza 1 kończy się 1941, faza 2 „Wolna Francja" zaczyna się 1944), Włochy,
Bułgaria i Rumunia (WWII, zmiana strony 1943-44), Łotwa (Wyzwolenie Łotewskie, 1919).

**Rozstrzygnięcie (autor).** Uczestnictwa tego samego `WarNum` scalają się w **jeden**
przedział konfliktu niezależnie od kalendarzowego odstępu między nimi (min. start, maks.
koniec po wszystkich wierszach/fazach tego `WarNum` dla danego państwa) — PRZED zastosowaniem
ogólnej reguły D-013/D-039 (gap≤0) MIĘDZY różnymi wojnami. Uzasadnienie: zmiana strony w
trakcie wojny nie jest przerwą w walce ani w regeneracji — to wciąż ta sama wojna, niezależnie
od tego, jak COW rozbił ją na wiersze administracyjnie.

**Sprawdzone bezpośrednio, które przypadki to realnie zmienia.** 4 z 5 (Włochy, Bułgaria,
Rumunia, Łotwa) i tak scalały się już pod samym gap≤0, bo kalendarzowy odstęp między ich
fazami/wierszami wynosi 0 lat. Jedyny przypadek, gdzie D-040 realnie zmienia wynik: Francja,
gdzie odstęp 1941→1944 wynosi 3 lata (> 0) — bez D-040 dałoby to 2 osobne epizody WWII,
z D-040 daje jeden epizod 1939–1945 (wchłaniający też wojnę francusko-tajską 1940–1941,
osobny `WarNum`, nakładającą się czasowo).

**Liczby kontrolne po gap≤0 (D-039) + D-040 — zastępują liczby z Etapu 1 v1.0 i erratę
autora (D-039), policzone przez `test6_build_s7.py` v2.0:**

| sprawdzenie | v1.0 (gap≤0, bez D-040) | **v2.0 (gap≤0 + D-040) — obowiązujące** | erraty (autor, gap≤1) |
|---|---|---|---|
| państw przy progu ≥6 | 15 | **13** | 12 |
| odstępów pełnych przy progu ≥6 | 123 | **110** | 98 |
| państw przy progu ≥3 | 40 | **39** | 37 |
| odstępów pełnych przy progu ≥3 | 190 | **182** | 168 |

23 (ccode,WarNum) pary w całym pliku miały więcej niż jeden wiersz/fazę scalone przez D-040
(nie tylko te 5 „zmiany strony" — także zwykłe rozbicia faza1/faza2 bez zmiany strony).

**Osobno wyjaśniona rozbieżność 97 kontra 98 (pytanie autora, `gap≤1`, diagnostyczne, POZA
regułą obowiązującą powyżej).** Dwa niezależne testy `gap≤1` w toku dochodzenia dały różne
sumy (97 i 98) przy tej samej liczbie państw (12) — źródłem NIE były duplikaty
(ccode,WarNum), tylko to, czy faza 2 była osobnym wpisem wejściowym do scalania, czy złożona
w koniec tego samego wiersza (formuła `endyr` Testu 6 zastosowana per wiersz) — sprawdzone
bezpośrednio, obie wersje trzymały duplikaty ccode+WarNum jako osobne wpisy identycznie.
Diagnostyczne wyłącznie — `gap≤1` nie jest regułą obowiązującą (D-039).

---

## D-041 · 2026-09-02 · Uzupełnienie D-040 (trzy punkty + zastrzeżenie merytoryczne)

**Wpisane na żądanie autora, po przyjęciu Etapu 1.** D-040 nie jest zmieniana ani usuwana
(reguła dziennika, nagłówek pliku) — poniższe to DOPRECYZOWANIE dopisane jako część tego
samego wątku decyzyjnego, z odwołaniem wprost do D-040.

**1. Kolejność w czasie.** Reguła D-040 (uczestnictwa tej samej wojny scalają się
niezależnie od odstępu) została zaproponowana przez autora PRZED policzeniem czegokolwiek
na przebudowanym zbiorze S7 — we wiadomości, która jeszcze pytała o rozbieżność 97 wobec 98
i zawierała podejrzenie (błędne, patrz wyżej) o duplikatach jako jej źródle. Liczby 13/110
powstały PO przyjęciu reguły, nie odwrotnie.

**2. Zakres skutku — SPROSTOWANIE własnego wcześniejszego stwierdzenia.** Wpis D-040 mówił
„jedynym przypadkiem, gdzie D-040 realnie zmienia wynik, jest Francja" — **nieprecyzyjne**,
sprawdzone teraz na wszystkich 98 państwach, nie tylko na 5 przypadkach duplikatu
(ccode,WarNum) zgłoszonych przez autora. D-040 zmienia liczbę epizodów dla **siedmiu**
państw, każde traci DOKŁADNIE JEDEN epizod:

| państwo | epizodów bez D-040 | epizodów z D-040 | próg ≥6 | próg ≥3 |
|---|---|---|---|---|
| Francja | 18 | 17 | bez zmian (w zbiorze) | bez zmian (w zbiorze) |
| Włochy | 12 | 11 | bez zmian (w zbiorze) | bez zmian (w zbiorze) |
| Niemcy | 8 | 7 | bez zmian (w zbiorze) | bez zmian (w zbiorze) |
| Austro-Węgry | 6 | 5 | **wypada** (6→5) | bez zmian (w zbiorze) |
| Jugosławia | 6 | 5 | **wypada** (6→5) | bez zmian (w zbiorze) |
| Bułgaria | 4 | 3 | poza zbiorem oba razy | bez zmian (w zbiorze) |
| Dania | 3 | 2 | poza zbiorem oba razy | **wypada** (3→2) |

**3. Kierunek skutku.** We wszystkich siedmiu przypadkach D-040 DZIAŁA PRZECIW liczbie
zdarzeń — nigdzie nie zwiększa liczby epizodów ani nie wprowadza nowego państwa do zbioru
przy żadnym progu. Rozbicie różnicy 123→110 (próg ≥6): −3 z redukcji epizodów w państwach,
które zostają w zbiorze (Francja, Włochy, Niemcy, po jednym odstępie pełnym każde), −10 z
całkowitego wypadnięcia dwóch państw (Austro-Węgry i Jugosławia, po pięć odstępów pełnych
każde) = −13, dokładnie 123−110. Reguła nie została więc dobrana pod wynik — działa w
kierunku ZMNIEJSZAJĄCYM moc testu, nie zwiększającym.

**4. Zastrzeżenie merytoryczne autora (zapisane, decyzja bez zmian).** Przypadek Francji
jest wątpliwy w drugą stronę: Vichy i Wolna Francja mają ten sam kod COW (220), ale nie są
tą samą stroną konfliktu. Kryterium `WarNum` (ten sam numer wojny w COW) jest obiektywne i
nie wymaga oceny merytorycznej co do tego, kto reprezentował państwo — dlatego decyzja D-040
pozostaje bez zmian — ale zastrzeżenie ma zostać widoczne w rejestrze, żeby nie sądzić, że
nie zostało zauważone.

---

## D-042 · 2026-09-02 · S7 Etap 2: trzy pomiary przed biegiem (TASK_S7.md §5)

**1. Deklaracja mocy — POTWIERDZONA symulacją, nie przyjęta z szacunku autora.** Mechanizm
`min(T,C)` (D-031, `test7_estimate.simulate_dataset_test7`, reużyty bez zmian — funkcja jest
ogólna względem tego, co reprezentuje „grupa"), okna = realna suma `ekspozycja` per państwo
(13 wartości, Σ=1619), `k_true=1,0`, `θ_true=0` (statystyka pierwszorzędna: pulowana, §6
zadania), `λ_true=14,72` (kalibrowane na Σokien/n_zdarzeń = 1619/110). Sprawdzone: symulowana
liczba zdarzeń zbiega do 110,3 (mediana 110,0) — kalibracja poprawna. **2000 replik:
SD(k̂) = 0,0782.** Deklaracja autora (≈0,081) potwierdzona — różnica trzeciego miejsca po
przecinku. Próg wykluczenia jedynki (przybliżenie normalne, ten sam wzór co P1 Testu 7,
D-037: 1±1,96·SD): poniżej **0,847** albo powyżej **1,153** (autor: ≈0,84/≈1,16 — zgodne).

**2. Odstępy krótkie — POLICZONE, NIE usuwane.**

| zbiór | n pełnych | zerowe | jednoroczne | razem ≤1 rok |
|---|---|---|---|---|
| S7 (próg ≥6) | 110 | 0 (0,0%) | 9 (8,2%) | 9 (8,2%) |
| Test 6 główny (próg ≥3, diady) | 45 | 0 (0,0%) | 7 (15,6%) | 7 (15,6%) |

Zero odstępów zerowych w obu zbiorach — strukturalnie niemożliwe: scalanie D-013/D-039
(gap≤0) wchłania każdy odstęp kalendarzowy ≤0 w epizod, więc odstęp między epizodami jest
zawsze ≥1 rok z konstrukcji. Wynik dla kolumny `dlugosc_kalendarzowa` i `dlugosc_odstepu`
(ekspozycja) identyczny w obu zbiorach — żaden z tych krótkich odstępów nie traci dodatkowo
ekspozycji z powodu nieczłonkostwa w systemie. S7 ma NIŻSZY odsetek jednorocznych odstępów
niż Test 6 główny (8,2% wobec 15,6%) — odwrotnie niż mogłoby sugerować samo przejście na
częstsze, bardziej „skłócone" jednostki.

**3. Sklejenie próby.**

- Państw z epizodem obejmującym 1914–18: **9/13** (69%) — ccode 2, 200, 220, 255, 325, 350,
  365, 640, 740.
- Państw z epizodem obejmującym 1939–45: **9/13** (69%) — ccode 2, 200, 220, 255, 325, 350,
  365, 710, 740.
- Państw z KTÓRYMKOLWIEK z dwóch: **10/13 (77%)** — większość, zgodnie z oczekiwaniem autora.
- Państw z OBOMA: **8/13 (62%)**.
- Odstępów pełnych zaczynających się dokładnie od końca wojny światowej (1918 albo 1945):
  **14/110 (12,7%)**.

Sklejenie jest silne na poziomie PAŃSTW (77% miało epizod nakładający się na którąś wojnę
światową) ale znacznie słabsze na poziomie ODSTĘPÓW (12,7%) — bo przeciętne państwo w
zbiorze ma około ośmiu epizodów, a tylko jeden lub dwa graniczą z wojną światową. 110
odstępów nie jest więc liczbą tak imponującą pod względem niezależności, jak sugerowałaby
sama liczba epizodów, ale zależność koncentruje się w mniejszości obserwacji, nie w
większości — obie liczby podane obok siebie, bez rozstrzygania która ma być brana pod uwagę.

**STOP po tych trzech pomiarach, przed Etapem 3 (bieg), zgodnie z TASK_S7.md §7.**

---

## D-043 · 2026-09-02 · S7 Etap 3: autoryzacja + deklaracje sprzed biegu

**Autoryzacja.** Autor autoryzuje Etap 3 wariantu S7. Blokada `--run-real` zdjęta. Zapadła
PRZED jakimkolwiek dopasowaniem na danych rzeczywistych — żaden bieg na `test6_s7_intervals.csv`
nie został wykonany przed tym wpisem.

**Deklaracja 1 — wykrywalność (moc).** SD(k̂)=0,0782 (D-042) daje próg wykluczenia jedynki
poniżej 0,847 albo powyżej 1,153. Test 6 dał k̂=0,778, Test 7 (P1, kruchość) dał k̂=0,843 —
**oba obserwowane dotąd efekty mieszczą się w zakresie wykrywalności S7.** Jeżeli ten sam
efekt istnieje na poziomie państw, S7 go zobaczy. Jeżeli S7 NIE odrzuci jedynki, będzie to
**pierwszy wynik negatywny tej rodziny przypisywalny danym, nie brakowi mocy narzędzia.**

**Deklaracja 2 — kanał sklejenia próby, poprawka względem D-042.** Sklejenie działa innym
kanałem niż zakładano w zadaniu przed Etapem 2: NIE przez odstępy zaczynające się od końca
wojny światowej (tych jest 12,7%, D-042) — przez to, że TE SAME wojny wchodzą do
życiorysów wielu państw naraz (9/13 dla obu wojen światowych, D-042). Miarą będzie **rozjazd
między przedziałem z profilu a przedziałem bootstrapowym na poziomie państw** (nie
odstępów) — to jest najważniejsza liczba tego biegu, bo mówi, ile ze 110 odstępów jest
efektywnie niezależnych.

**Deklaracja 3 — oczekiwania autora, spisane przed wynikiem (żeby uniknąć wrażenia
dopasowania opisu do liczb post factum).** Parametr w okolicach 0,75–0,90 (podobny do Testu
6 i 7), odrzucenie jedynki przez przedział z profilu. Przedział bootstrapowy WYRAŹNIE
szerszy niż profilowy (bo trzynaście państw dzieli te same wojny) i traktowany jako
właściwa miara niepewności, nie profilowy. Jeżeli OBA przedziały wykluczą jedynkę — pierwszy
wynik pozytywny rodziny dziewiątej. Jeżeli wykluczy TYLKO profil — wynik jak w Teście 6:
sygnał widoczny narzędziem optymistycznym, znikający pod ostrożniejszym.

**Specyfikacja biegu (bez odstępstw od §5–§8 protokołu Testu 6).** Statystyka pierwszorzędna:
k̂ pulowane (§5). Kruchość obok jako drugorzędna, z odsetkiem replik bootstrapowych z θ̂ na
granicy. N1, ziarno 20260822, B=2000, zabezpieczenie przed remisem D-026 §7. N2 pominięty
jednym zdaniem (D-026: zdegenerowany wobec statystyki pulowanej). Oba przedziały (profil +
bootstrap) **na poziomie państw**, podane obok siebie z rozjazdem, żadien nie wybrany jako
"ten właściwy".

**§8 zadania obowiązuje niezależnie od wyniku:** S7 pozostaje wariantem wrażliwości. Nawet
korzystniejszy wynik niż Test 6/7 nie awansuje go na wariant pierwszorzędny.

**STOP po biegu, przed jakąkolwiek narracją** — surowe liczby, jak przy Kroku C Testu 6 i
Etapie C Testu 7.
