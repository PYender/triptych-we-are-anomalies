# CPS_CONTEXT_PACK

**Pakiet startowy sesji — model „wojna–pokój" (CPS) z Tryptyku**
Wersja 1.1 · stan na 10 sierpnia 2026 · język roboczy: polski

---

## 0. Jak używać tego pliku

Ten plik jest wklejany **na początku każdej sesji**, przed jakimkolwiek poleceniem.
Zastępuje historię wcześniejszych rozmów, do której nowa sesja nie ma dostępu.

Jest jednym z trzech plików startowych i odpowiada na pytanie **„co wiemy i czego
nie wolno"**. Pozostałe: `CPS_OPERATING_BRIEF.md` („skąd dane, jak zacząć, kiedy
skończone"), `CPS_DECISION_LOG.md` („co już rozstrzygnięto i dlaczego")
i `TESTn_PROTOCOL.md` („jakie jest dzisiejsze zadanie"). Wklejaj w tej kolejności.

**Uwaga o dokumentach w repozytorium.** Kilka plików na `main` wygląda jak stan wiedzy
projektu, a zawiera błędy z §5 — ich lista jest w §2 briefu operacyjnego. Nie traktuj
ich jako źródła prawdy.

Jeżeli czytasz to jako Claude Code: **przeczytaj całość zanim napiszesz pierwszą linię
kodu**. Sekcje 4 i 6 są ważniejsze od reszty — opisują błędy, które już popełniono
w tym projekcie, i decyzje, których nie wolno podejmować samodzielnie.

Nie streszczaj tego pliku w odpowiedzi. Potwierdź krótko, że go przeczytałeś, i przejdź
do zadania.

---

## 1. Czym jest projekt

Tryptyk („We Are Anomal(i)es") zawiera rozdział III.3.2 — walidator operacyjny CPS
(*Cycle Prediction Sentinel*), opisujący hipotezę globalnego cyklu wojenno-pokojowego
o okresie ~35–36 lat, mierzonego na trzech strumieniach: COW (liczba konfliktów),
Google Books N-grams (indeks nastroju dyskursu COLOR) i GDELT (kontekst współczesny).

Rozdział jest obecnie **przepisywany**. Trwa równolegle: (a) errata do wersji v0.1,
(b) zaprojektowana od nowa bateria testów, (c) nowa wersja rozdziału. Twoja rola
dotyczy (b): wykonanie testów według protokołów, nie projektowanie hipotez.

**Nazwa:** w obiegu funkcjonują cztery rozwinięcia skrótu CPS. Obowiązuje jedno —
*Cycle Prediction Sentinel*. Nie używaj wariantów „Conflict Periodicity System/Series"
ani „Conflict Prediction System".

---

## 2. Twierdzenia, które są testowane

Rozstrzygnięcia D-001 i D-002 z `CPS_DECISION_LOG.md` rozdzieliły twierdzenie
z Tryptyku v0.1 na dwie niezależne hipotezy. Testy mają je sprawdzać, nie potwierdzać.

**H1 — cykliczność (główna). Seria pierwszorzędna: `A_COW_W`.**

> W epoce post-1914 seria konfliktów wykazuje strukturę fazową w paśmie 32–40 lat
> silniejszą niż w epoce przed 1914, przy czym przy obecnej długości szeregu
> nie musi być odróżnialna od procesu autoregresyjnego na poziomie α = 0,05.

Status wstępny: **przesłanki negatywne**. Orientacyjne χ² wynosi 14,53 dla epoki 1
i 6,97 dla epoki 2 — kierunek przeciwny do przewidywanego.
Kryterium falsyfikacji: jeżeli χ² epoki 2 nie przewyższa χ² epoki 1 przy serii
pierwszorzędnej i nullu AR(3), hipoteza w tej postaci zostaje odrzucona.

**H2 — umiędzynarodowienie (poboczna). Seria: `A_COW_P`.**

> Po 1914 konflikty angażują istotnie więcej stron naraz, a seria ważona liczbą
> uczestników wykazuje strukturę fazową nieobecną przed 1914.

Status wstępny: przesłanki pozytywne (χ² 7,43 wobec 39,49), interpretacja otwarta.
Zastrzeżenie obowiązkowe: na poziomie uczestnika obie wojny światowe wnoszą
po kilkanaście–kilkadziesiąt wierszo-lat i leżą blisko siebie fazowo. Profil
zdominowany przez dwa zdarzenia nie jest dowodem okresowości — wymagany wariant
z wyłączeniem 1914–1918 i 1939–1945 albo z winsoryzacją.

**H1 i H2 nie mogą być prezentowane jako jedno twierdzenie.** Jeżeli H1 upada,
a H2 się broni, rozdział opisuje falsyfikację własnej wcześniejszej tezy oraz nową
hipotezę — nie „potwierdzenie modelu".

**Czego żadna z nich NIE mówi** — i czego nie wolno w ich imieniu napisać:

- że cykl ~35 lat „istnieje" lub „został wykazany";
- że którykolwiek wynik jest istotny statystycznie (nie jest);
- że model ma zdolność predykcyjną potwierdzoną ilościowo;
- że p = 0,087 oznacza „91% szans, że sygnał jest realny" (p **nie jest** miarą
  prawdopodobieństwa hipotezy — to częsty błąd popełniony już w tym projekcie);
- że wynik z serii uczestniczej mówi cokolwiek o liczbie wojen.

**Kontekst merytoryczny, bez którego testy są źle dobrane.** Model dotyczy przede
wszystkim okresu po I wojnie światowej, bo dopiero wtedy świat stał się siecią naczyń
połączonych i analiza cykliczności w skali globalnej ma sens (przed 1914 rytm był
kontynentalny, nie planetarny; dane są też coraz dokładniejsze w czasie). Cykliczność
jest przy tym **zaburzana przez czynniki zewnętrzne** — pandemie, wyczerpanie zasobów
po II wojnie światowej — na tyle silnie, że kolejne cykle rozpadły się na serie
mniejszych konfliktów. Cykl idealny istniałby w świecie bez tych zaburzeń.

Praktyczna konsekwencja: **test typu „czy dane są odróżnialne od AR wysokiego rzędu"
nie jest właściwym kryterium falsyfikacji cyklu zaburzanego**. Właściwe pytanie
brzmi: czy struktura fazowa po 1914 jest wyraźnie silniejsza niż przed 1914.
Ten błąd doboru narzędzia pochłonął połowę sesji lutowej.

---

## 3. Warstwa danych — obowiązująca

Rozstrzygnięta w Testach 0, 0B i 0C (`TEST0_REPORT.md`, `TEST0B_REPORT.md`,
`TEST0C_REPORT.md`).

### 3.1 Plik kanoniczny

`cps_canonical_v2.csv` — jedyne dopuszczalne wejście do testów. Powstaje ze skryptu
`test0c_build_canonical.py` z plików surowych COW i UCDP. Kolumny:
`variant, year, source, value, value_ma11c, value_ma11t`.

| Wariant | Zakres | Rola |
|---|---|---|
| **`A_COW_W`** | 1816–2007 | **seria pierwszorzędna** (D-001); poziom wojny, deduplikacja po `WarNum` |
| `A_COW_P` | 1816–2007 | poziom uczestnika; hipoteza H2 i rodzina 4 |
| `B_UCDP` | 1946–2024 | jednorodna, niezależne kodowanie; replikacja |
| `C_SPLICED_W` | 1816–2024 | sklejona, poziom wojny; **D3 FAIL** (skok +1,08 SD) — ostrożnie |
| `C_SPLICED_P` | 1816–2024 | sklejona, poziom uczestnika; D2 i D3 PASS |

`cps_canonical_v1.csv` jest **wycofany** — powstał przed korektami F1–F3.

### 3.2 Ustalenia rozstrzygnięte

- **Seria COW jest w pełni odtwarzalna z plików surowych** (maks|Δ| = 0 wobec
  `wars_color.csv`). Kryterium D1 spełnione.
- **Trzy błędy agregacji w kodzie v0.1**, poprawione w serii kanonicznej v2:
  kod `-7` (wojna trwająca) traktowany jak data → 25 wojen usuniętych z serii
  w całości; kategoria Non-State (62 wojny, waga 0,4) nie wchodziła w ogóle;
  Intra-State pomijało fazę 4.
- **Seria biegnie do 2007** (D-003). Odcięcie na 2003 z Testu 0 było oparte na
  błędnej diagnozie „cenzurowania ogona".
- **Skala złączenia**: 0,449 dla poziomu W, 0,710 dla poziomu P, wyznaczana na
  oknie 1989–2007. Wartość 0,5433 z `ucdp_adapter.py` jest nieaktualna.
- **`wars_smooth` znaczy dwie różne rzeczy** w `wars_color.csv` i
  `wars_extended_2024.csv` (różnica do 1,93). Nie cytuj tej nazwy bez pliku.
- **Pliki COW mają zakończenia linii CR** — bez normalizacji pandas czyta je
  jako jeden wiersz o tysiącach kolumn.
- **Moduł COLOR jest odtwarzalny z czterech tabel CSV** (~250 kB) zamiast 3,1 GB
  plików `.gz`; weryfikacja wobec `wars_color.csv` dała maks|Δ| = 2,2e-16.
  PATCH 1D był realną poprawką (przesunięcie do 2 SD), ale nie zmienia dynamiki
  (korelacja wariantów 0,965) ani żadnego wyniku modelu.

### 3.3 Wygładzanie

- `value_ma11c` — centrowana MA(11). Do opisu kształtu i testów fazowych.
- `value_ma11t` — **jednostronna** MA(11). **Obowiązkowa** wszędzie, gdzie test dotyczy
  wyprzedzania w czasie (Granger, CCF, lead–lag, walidacja poza próbką).
  Centrowana średnia wnosi do roku *t* dane z lat *t+1…t+5* i unieważnia taki test.
- Jeżeli test porównuje dane z surogatami, **to samo wygładzenie musi być nałożone
  na surogaty**. Inaczej porównujesz serię filtrowaną z niefiltrowaną i mierzysz filtr.

### 3.4 Dane zakazane

- `wars_extended_2026.csv` — zawiera **zmyślone** punkty 2025 = 18,5 i 2026 = 21,0
  (etykieta `UCDP_EST`). To estymaty, nie pomiary. Nie wolno z nich raportować żadnego p.
  Plik pozostaje w repo wyłącznie jako zapis próby; jest w kwarantannie do czasu
  publikacji UCDP v26.1/v27.1.
- Wagi typów konfliktu {2:1,0; 3:0,4; 4:0,7} są **odziedziczone**. Ich wrażliwość bada
  osobna rodzina testów. Nie zmieniaj ich samodzielnie w innych testach.

---

## 4. Co już przetestowano — nie powtarzaj bez powodu

### 4.1 Moduł cykliczności

| Test | Skrypt | Wynik |
|---|---|---|
| Fisher g / bootstrap | `spectral_significance.py` | pik 24 lata, p = 0,021 wobec białego szumu; p = 0,947 wobec AR(20) |
| PSD z MA(11) na surogatach | `spectral_significance_v2.py` | p_band 0,465 (1816–2007) i 0,550 (1918–2007); `sin_r2` 0,153 vs **0,462** dla post-WWI |
| Epoch-folding, null AIC | `epoch_folding_test.py` | χ² 36,54 / 45,13; p 0,349 / 0,313; T_max 36,5 |
| Epoch-folding, null BIC | — | AR(18); p 0,347 / 0,314 — bez zmian |
| Epoch-folding, null AR(3) | `--max-lag 3` | χ² 38,30 / 43,73; p **0,163** / **0,143**; T_max 38,5 / 37,0 |
| Wavelet, spójność fazy | `wavelet_phase_test.py` | σ² 0,128, p = 0,615; R 0,937, p = 0,616; **61% surogatów AR(20) ma stabilniejszą fazę niż dane** |
| Cross-epoch, AR(3) | `cross_epoch_phase_test.py` | epoka 1 (1816–1913, n=98): χ² 8,62, **p = 0,866**; epoka 2 (1914–2024, n=111): χ² 49,93, **p = 0,087**; Fisher 0,269; korelacja predykcyjna 0,008 (p = 0,469) |
| Cross-epoch z danymi 2026 | `*_2026prelim*` | AIC → AR(20): p = 0,370 (artefakt rzędu); AR(3): **p = 0,109**, korelacja predykcyjna **−0,040** |
| Replikacja COW×UCDP | `ucdp_cross_validation.py` | **3/6 kryteriów**. T_dom: COW 32, UCDP 39 (ΔT = 7 ✓). Fazy: Δφ = 7,4° / 40,8° / 38,4°. Korelacje: 0,078 / −0,439 / −0,453 (kryterium r ≥ 0,70 ✗) |
| Widmo COW vs UCDP | `cow_ucdp_spectral.py` | COW T ≈ 24 (p = 0,021), UCDP T ≈ 39,5; oba znikają po prewhiteningu |
| Warstwa danych | `test0_data_layer.py` | patrz §3 |

**Diagnoza przekrojowa:** AIC na n = 90–209 wybiera AR(18–20), co daje null zużywający
~20% stopni swobody i sam quasi-periodyczny — może aproksymować sinusoidę zespolonymi
pierwiastkami charakterystycznymi. Stąd wynik testu zależy silniej od rzędu nulla
niż od danych. Uzasadniony rząd to AR(3) (Box–Jenkins dla rocznych szeregów makro:
inercja zaangażowania w konflikt).

### 4.2 Moduł COLOR — wynik negatywny, nierozliczony

| Test | Wynik |
|---|---|
| ADF | `wars` surowe p = 0,0002 → I(0); `color` p = 0,185 → I(1) |
| Granger COLOR → wars | **nieistotny przy wszystkich lagach**, na COW i na UCDP |
| Granger wars → COLOR | **p < 0,01 dla lagów 1–6** — kierunek odwrotny do hipotezy |
| Johansen/VECM | rank = 2, β przy `color_smooth` ≈ 0, połowiczny czas powrotu 11,6 roku ≈ okno wygładzania → mierzy filtr, nie mechanizm |
| ARIMAX β_color | p = 0,895 (patrz Tryptyk s. 74) |
| Rolling-origin | wariant *oracle* (znany przyszły COLOR) i *constant* praktycznie identyczne → COLOR nie wnosi informacji predykcyjnej |
| CCF UCDP vs COLOR | **znak dodatni** (+0,82), przeciwny do COW (−0,74) |

Ten wynik **nie został unieważniony** przez korektę o globalizacji — dotyczy innego
modułu. W obecnej postaci COLOR jest wskaźnikiem współbieżnym lub reaktywnym,
nie wyprzedzającym. Teza o wyprzedzaniu wraca dopiero po przebudowie leksykonu
i zmianie korpusu — do tego czasu nie wolno jej powtarzać.

### 4.3 Otwarty problem, który wymaga wyjaśnienia

Niezależna seria `B_UCDP` (1946–2024) daje χ² epoki 2 na poziomie **7,8** — czyli tyle,
co epoka przedglobalizacyjna, podczas gdy `A_COW` 1914–2003 daje 47,3. Częściowe
wyjaśnienia: n = 79 to ~2,2 cyklu; UCDP liczy w większości konflikty wewnątrzpaństwowe,
więc mierzy inną wielkość. **Tego nie wolno przemilczeć** — to dziś najsłabszy punkt tezy.

---

## 5. Errata do Tryptyku v0.1 — stan bieżący

Kategorie: **[E]** edycyjny · **[S]** spójności · **[M]** metodologiczny · **[F]** falsyfikowany.

| # | Miejsce | Opis | Kat. |
|---|---|---|---|
| 1 | s. 58 vs 64 vs 73–74 | r przy lagu 8 podany jako −0,56 / −0,41 / −0,558 / −0,407 | S |
| 2 | s. 59 vs 69 vs ADDENDA | próg alarmu: −0,6 bezwzględnie / „above 1σ" / poniżej −1σ | S |
| 3 | s. 59 | próg −0,6 nieosiągalny: MIN COLOR w danych = −0,543 | M |
| 4 | s. 62 vs 63 | mw-4 wymienia pole „Tone", kod używa `GoldsteinScale` | S |
| 5 | s. 55 vs 57 | ≈2,7 mln vs >2,5 mln wpisów GDELT; „lata ≥ 1820–2011" przy GDELT od 1979 | S |
| 6 | s. 38 vs 40 | `wars_pc` definiowane dwukrotnie i różnie; do CSV trafia druga wersja | S |
| 7 | s. 37 | `war_main` wczytywane i nieużywane (martwy kod) | E |
| 8 | s. 36–37 | Extra/Non/Intra liczą fazy 1·2·3, Inter-State tylko 1–2 | M |
| 9 | s. 39 | `years = df.index` „after set_index" — brak `set_index` w listingu | E |
| 10 | s. 42, 69 | „II.3.2.2." zamiast III; dwa punkty „A3." | E |
| 11 | s. 64–65 | wtręty polskie w tekście angielskim | E |
| 12 | całość | `curve_fit` (sin-fit) raportowany jako weryfikacja okresu — to opis, nie test | M |
| 13 | s. 57 | PSD serii po MA(11) przedstawiony jako niezależne potwierdzenie sin-fitu | M |
| 14 | s. 69 | „różnice oscylują wokół 27–35 lat" — faktyczne odstępy szczytów: 27, 7, 22, 11, 10, 12, 16 | M |
| 15 | ADDENDA Z12 | embedding/word2vec/PMI opisane jako „explicitly noted in the study" — nie ma tego w III.3.2 | S |
| 16 | s. 32–78 | teza o COLOR jako wskaźniku wyprzedzającym | **F** |
| 17 | `Podsumowanie…md` | TEST 2 to wiersz-hybryda: χ² i T z runu AIC, p z runu AR(3) | S |
| 18 | `Podsumowanie…md` | „predykcja Tryptyku 2023–2027" — Tryptyk s. 78 mówi **2027–2030** | M |
| 19 | `NOTE_2026…md` | „ostatni potwierdzony szczyt 1991" — w danych 1991 nie jest lokalnym maksimum | M |
| 20 | `NOTE_2026…md` | „największa wojna międzypaństwowa od 2003" — pomija Ukrainę od 2022 | E |
| 21 | `NOTE_2026…md` | zapowiedź „p ≈ 0,05–0,08" przy AR(3); faktycznie 0,109 — nie zaktualizowano | M |
| 22 | `Podsumowanie…md` | omija run `2026prelim_ar3` (wynik gorszy od baseline) | M |
| 23 | Test 0 | skala 0,543 raportowana jako pomiar; jest wyborem okna | M |
| 24 | Test 0 | lata 2004–2007 serii COW cenzurowane, używane we wszystkich testach | M |

**Errata działa w obie strony.** Zarzuty postawione w sesji lutowej, które okazały się
nietrafne, też są jej częścią: (a) AR-bootstrap jako kryterium falsyfikacji cyklu
zaburzanego, (b) Granger liczony na centrowanej MA, (c) teza, że epoch-folding jest
odporny na skok poziomu na złączeniu.

---

## 6. Zakazy — twarde reguły tego projektu

Każdy z nich pochodzi z błędu faktycznie popełnionego w tym projekcie.

1. **`curve_fit` nie jest testem.** Dopasowanie sinusoidy zawsze coś zwróci. Nie
   raportuj okresu z `curve_fit` jako potwierdzenia hipotezy o okresie.
2. **Nie licz Grangera, CCF ani żadnego testu lead–lag na serii wygładzonej centrowanie.**
   Używaj `value_ma11t` albo serii surowej.
3. **Nie raportuj p z nulla wybranego przez AIC bez wariantu o rzędzie ustalonym z góry.**
   Zawsze podawaj oba. Rząd nulla jest decyzją teoretyczną, nie wynikiem optymalizacji.
4. **Epoch-folding nie jest odporny na skok poziomu.** Statystyka sumuje odchylenia
   średnich w koszach od średniej globalnej — trwały skok poziomu podnosi χ²
   niezależnie od jakiegokolwiek rytmu.
5. **Nie raportuj najniższego p z wielu wariantów jako wyniku.** Wypisz wszystkie
   uruchomienia, także nieudane. Wskaż z góry, który test jest pierwszorzędny.
6. **Nie wymyślaj punktów danych.** Żadnych estymat, ekstrapolacji ani „konserwatywnych
   oszacowań" wstawianych do serii, na której liczysz statystykę.
7. **p nie jest prawdopodobieństwem hipotezy.** Nie pisz „p = 0,087 oznacza 91% szans".
8. **Nie ekstrapoluj trendu p(n).** Dwa punkty nie definiują trendu, a p nie maleje
   monotonicznie z n, o ile efekt nie jest realny — to rozumowanie kołowe.
9. **Nie używaj `C_SPLICED` ani lat COW po 2003 do testów formalnych.**
10. **Nie zmieniaj protokołu po zobaczeniu wyniku.** Jeśli wynik wymaga innego testu,
    napisz nowy protokół i powiedz wprost, że powstał po zobaczeniu poprzedniego.

---

## 7. Protokół pracy

### 7.1 Kolejność obowiązkowa

```
protokół (.md, zamrożony)  →  kod (.py + .md do niezależnej oceny)
                           →  uruchomienie  →  wyniki (.csv + .pdf)  →  raport (.md)
```

Żadna decyzja metodyczna nie zapada po zobaczeniu wyników. Protokół zawiera:
hipotezę, dane wejściowe z hashem, model zerowy z uzasadnieniem teoretycznym,
statystykę testową, liczbę replikacji i ziarno, regułę decyzyjną oraz
**kryterium falsyfikacji** — jaki wynik uznajemy za obalenie.

### 7.2 Artefakty

| Typ | Konwencja |
|---|---|
| Protokół | `TESTn_PROTOCOL.md` |
| Kod | `testn_<nazwa>.py` **oraz** `testn_<nazwa>.md` z tym samym kodem, do oceny |
| Wyniki liczbowe | `testn_<nazwa>_results.csv`, nagłówek `#` z wersją skryptu i hashami wejść |
| Wykresy | `testn_<nazwa>.pdf`, dpi ≥ 300 |
| Raport | `TESTn_REPORT.md` |

### 7.3 Reprodukowalność

Stałe ziarno (`--seed`, domyślnie 20260810), przypięte wersje bibliotek, liczba
replikacji bootstrapu podawana jawnie (domyślnie B = 2000), każdy plik wyjściowy
z nagłówkiem zawierającym wersję skryptu i sha256 plików wejściowych.

### 7.4 Środowisko

Duże pliki (GDELT ~6,4 GB, `.gz` Google Books 116–433 MB) **nie są w repozytorium**
i nie będą. Wszystko, co ich wymaga, jest zablokowane — powiedz to wprost zamiast
obiecywać test, który nie powstanie. Łańcuch zależności: `.gz` → skrypt główny →
`wars_color.csv` → testy. Do testów wystarczą pliki CSV.

---

## 8. Czego nie decydujesz samodzielnie

Zgłoś do rozstrzygnięcia autorowi, nie wybieraj sam:

- rząd i typ modelu zerowego;
- granice epok i okien;
- wagi typów konfliktu;
- kryterium falsyfikacji;
- który test jest pierwszorzędny;
- zmianę hipotezy lub jej sformułowania;
- treść wniosków merytorycznych o historii czy polityce.

Jeżeli test daje wynik sprzeczny z hipotezą — **zaraportuj go**. Nie przeprojektowuj
testu, żeby wynik się poprawił, i nie tłumacz porażki „złym doborem narzędzia",
o ile nie potrafisz wskazać konkretnej własności metody, która to uzasadnia.

---

## 9. Kolejka testów

| Nr | Rodzina | Status |
|---|---|---|
| 0 | warstwa danych i kalibracja | **wykonany** |
| 0B | odtworzenie COW z plików surowych, korekty F1–F3 | **wykonany** |
| 0C | poziomy agregacji, seria kanoniczna v2 | **wykonany** |
| 1 | okres jako własność danych, nie filtra i dopasowania (Z3, Z4, Z14) | protokół w przygotowaniu |
| 2 | kontrast epok pre-/post-1914 — **rdzeń tezy** (Z13, Z15) | do zaprojektowania |
| 3 | replikacja na niezależnej bazie; wyjaśnienie rozbieżności `B_UCDP` (Z1, Z9) | do zaprojektowania |
| 4 | odporność na wagi i normalizację per capita (Z8, Z9) | do zaprojektowania |
| 5 | COLOR jako sygnał wyprzedzający (Z5, Z6, Z10) | do zaprojektowania |
| 6 | COLOR: leksykon i korpus (Z2, Z11, Z12) | **zablokowany** — brak `.gz` w repo |

Numeracja „Z" odsyła do 15 zarzutów z ADDENDA A Tryptyku (s. 142–143), zwiniętych
do sześciu rodzin. Każdy zrealizowany test dostaje odnośnik do odpowiadającego mu
podrozdziału nowej wersji.

---

## 10. Repozytorium

`github.com/PYender/triptych-we-are-anomalies`, katalog `code/cps/`.
Wersja v0.1 Tryptyku pozostaje **zamrożona jako archiwalna**; poprawki wchodzą jako
wersjonowana errata, nie jako cicha podmiana (repo ma `CITATION.cff`).
