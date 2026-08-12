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
