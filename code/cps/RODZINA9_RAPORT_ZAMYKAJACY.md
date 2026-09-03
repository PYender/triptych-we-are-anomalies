# Rodzina dziewiąta — raport zamykający (Test 6, Test 7, S7/S7b/S7c)

**Status: rodzina dziewiąta zamknięta (autor, 2 września 2026).**

*Uwaga o strukturze: lista siedmiu wcześniej uzgodnionych części nie dotarła do Code w
pierwszej wersji tego dokumentu — odtworzył strukturę z precedensu, zamiast udawać, że ją
ma; to było postępowanie prawidłowe. Poniższa wersja zawiera cztery brakujące części,
dopisane po wskazaniu przez autora, oraz jedną poprawkę krytyczną (§3/§7 — Test 6).*

---

## 0. Rozróżnienie od Testów 1, 3 i 5

Rodzina dziewiąta bada **strukturę odstępów** między epizodami konfliktu — czas między
końcem jednego epizodu a początkiem następnego, modelowany rozkładem Weibulla (pamięć/brak
pamięci procesu). To jest pytanie o to, czy prawdopodobieństwo kolejnego konfliktu zależy od
czasu, jaki upłynął od poprzedniego.

Testy 1, 3 i 5 badały **okresowość w rocznym szeregu czasowym** zagregowanej częstości
konfliktów — czy szereg ma powtarzalny cykl o określonej długości (analiza widmowa, skan po
okresach). To jest pytanie o regularny rytm w całym systemie, nie o pamięć pojedynczego
procesu odnowy.

Te dwie hipotezy są rozłączne merytorycznie i metodologicznie — Rodzina dziewiąta w żaden
sposób nie potwierdza ani nie obala wyników Testów 1/3/5, i odwrotnie. Rozróżnienie stoi tu
na początku celowo: sklejanie tych dwóch pytań było w tym projekcie źródłem błędów, w tym
błędu autora w tekście posta zewnętrznego.

## 1. Ujawnienia i dyscyplina (zakaz nr 10)

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

## 2. Metodologia wspólna (bez odstępstw między wariantami)

- Estymator: `test6_weibull.py` (`fit_pooled`/`fit_frailty`, profil wiarygodności,
  bootstrap grupowy) — NIE pisany od nowa dla żadnego wariantu tej rodziny.
- Scalanie epizodów: gap≤0 (D-013, doprecyzowane D-039). Dla wariantów państwowych
  (S7/S7b/S7c) dodatkowo D-040: uczestnictwa TEJ SAMEJ wojny scalają się niezależnie od
  odstępu kalendarzowego.
- Ekspozycja: D-014 (lata członkostwa w systemie COW, `system2016.csv`).
- Model zerowy N1: proces Poissona per grupa, ziarno 20260822, B=2000, zabezpieczenie przed
  remisem D-026 §7.
- N2: pominięty jednym zdaniem dla wszystkich wariantów (D-026) — zdegenerowany względem k̂
  pulowanego z powodów algebraicznych, niezależnie od jednostki analizy.

Ustalenia metodologiczne wykryte PRZY OKAZJI budowy tej rodziny — degeneracja N2,
niespełnialność reguły §8, samowalidujący się charakter symulacji odzysku, zapadanie
kruchości, pokrycie bootstrapu przy małej liczbie grup — omówione osobno w §6, nie tutaj:
to jest najtrwalszy wynik całej rodziny i zasługuje na własny rozdział, nie na rozproszenie.

## 3. Tabela główna — pięć wariantów

| | **Test 6**<br>pary, próg 3 | **Test 7 P1**<br>pary, po stawce | **S7**<br>państwo, wszystkie wojny | **S7b**<br>państwo, inicjacje | **S7c**<br>państwo, cele |
|---|---|---|---|---|---|
| jednostka | diada | diada | państwo | państwo | państwo |
| n grup | 18 | 101 | 13 | 13 | 29 |
| n zdarzeń | 45 | 37 | 110 | 50 | 95 |
| **statystyka decydująca (§5–§8 protokołu)** | **symulacyjna N1** | kruchość | pulowana | pulowana | pulowana |
| k̂ (statystyki decydującej) | 0,7780 | 0,8428 | 0,9947 | 0,9299 | 0,9003 |
| N1 p | **0,068 — ORZEKAJĄCY, próg <0,05 protokołu NIEOSIĄGNIĘTY** | 0,2655 (diagnostyczny) | 0,9755 (diagnostyczny) | 0,6272 (diagnostyczny) | 0,4588 (diagnostyczny) |
| CI profil¹ | [0,6029; 0,9791] — wyklucza 1 | [0,6235; 1,1024] — nie wyklucza | [0,8582; 1,1410] — nie wyklucza | [0,7443; 1,1343] — nie wyklucza | [0,7620; 1,0491] — nie wyklucza |
| CI bootstrap (grupy)¹ | [0,6471; 0,9649] — wyklucza 1 | [0,6720; 1,0851] — nie wyklucza | [0,9174; 1,0901] — nie wyklucza | [0,8063; 1,1053] — nie wyklucza | [0,8054; 1,0328] — nie wyklucza |
| θ̂ (kruchość, drugorzędna) | nie liczone w Kroku C | 2,655 (nie na granicy) | 4,08×10⁻⁸ (na granicy) | 1×10⁻¹⁰ (na granicy) | 1×10⁻¹⁰ (na granicy) |
| SD(k̂) zadeklarowane przed biegiem | 0,127² | 0,138 | 0,0782 | 0,1203 | 0,0846 |
| próg wykluczenia 1 (deklarowany) | <0,751 / >1,249² | <0,730 / >1,270 | <0,847 / >1,153 | <0,764 / >1,236 | <0,834 / >1,166 |
| efekt Testu 6 (0,778) mieści się w progu innych wariantów? | — (to jest ten efekt) | **NIE** | TAK | **NIE** | TAK |
| **klasyfikacja wyniku** | **reguła §8 niespełnialna (D-026); próg p<0,05 nieosiągnięty (p=0,068)** | **nierozstrzygnięcie z braku mocy³** | **zerowy, przypisywalny danym** | **nierozstrzygnięcie z braku mocy** | **zerowy, przypisywalny danym** |

¹ **Przedziały dla Testu 6 pochodzą z analizy UZUPEŁNIAJĄCEJ (D-023), NIE z metody
pre-rejestrowanej.** `TASK_6B_BRIEF.md` podstawił profil wiarygodności/bootstrap zamiast
modelu zerowego N1/N2 przewidzianego przez `TEST6_PROTOCOL.md` §6–§8, bez odnotowania, że to
podstawienie metody, nie tylko nazw wariantów. D-023: *"`TEST6_REPORT.md` (k̂=0,778, profil i
bootstrap poniżej 1) NIE ORZEKA o H6.1 — zostaje jako analiza uzupełniająca/diagnostyka, nie
jako wynik testu."* `TEST6_REPORT.md` nosi do dziś nagłówek *"ANALIZA UZUPEŁNIAJĄCA (nie
orzeka o H6.1) — metoda niezgodna z §6–§8 protokołu."* Przedziały podane w tabeli dla
kompletności i dlatego, że kierunek zgadza się jakościowo z N1 (obie metody wskazują
k̂<1) — nie dlatego, że orzekają.

² SD Testu 6 (0,127) policzone retroaktywnie w D-031, nie zadeklarowane przed oryginalnym
biegiem Kroku C, który poprzedzał tę konwencję.

³ Nie nowe ustalenie — zapisane już w D-032 jako powód odłożenia biegu Etapu C: próg Testu 7
P1 (0,730) nie sięga efektu Testu 6 (0,778). Zastosowane tu konsekwentnie do klasyfikacji.

**Kruchość zapadnięta w S7/S7b/S7c (D-022).** We wszystkich trzech wariantach państwowych
θ̂ osiada na numerycznej granicy, z odsetkiem replik bootstrapowych na granicy 25–81%. Model
orzekający jest w tych trzech wariantach de facto pulowany — przedziały dla kruchości nie są
interpretowalne osobno, choć nie zmienia to wniosku (obie statystyki dają praktycznie te
same liczby).

## 4. Obserwacja: odchylenie od jedynki maleje monotonicznie z rozszerzaniem jednostki

| jednostka | k̂ |
|---|---|
| pary, próg 3 (Test 6) | **0,778** |
| pary, po stawce (Test 7 P1) | **0,843** |
| państwo, wojny jako cel (S7c) | **0,900** |
| państwo, inicjacje (S7b) | **0,930** |
| państwo, wszystkie wojny (S7) | **0,995** |

Obserwacja podana bez interpretacji. Dwie konkurencyjne wykładnie (D-044), żadna
nierozstrzygnięta przez zebrane dane:

**Wykładnia A.** Sygnał widoczny na parach był artefaktem mieszania jednostek o różnych
tempach regeneracji — pulowanie do większej jednostki usuwa artefakt i ujawnia prawdziwy
brak efektu.

**Wykładnia B.** Zegar jest własnością PARY (bilateralny), nie aktora. Pulowanie wojen
jednego państwa z różnymi przeciwnikami rozmywa realny sygnał diadowy zamiast go ujawniać.

## 5. Ograniczenia

- **Hipoteza zegara bilateralnego pozostaje nierozstrzygnięta** (D-044) — na poziomie par
  nigdy nie było dość zdarzeń do rozdzielenia zegarów przeciwnik-po-przeciwniku; na poziomie
  państw ten wymiar nie jest w ogóle mierzony (kruchość S7/S7b/S7c mierzy heterogeniczność
  MIĘDZY PAŃSTWAMI, nie MIĘDZY PRZECIWNIKAMI tego samego państwa).
- **Asymetria mocy S7b/S7c (D-048).** Kontrola negatywna (S7c, SD=0,0846) jest czulsza od
  testu orzekającego (S7b, SD=0,1203) — odwraca zwykłą logikę kontroli negatywnej. Zaszedł
  układ trzeci z czterech zapisanych przed biegiem: żaden przedział nie wyklucza 1. Dla S7c
  to wynik przypisywalny danym; dla S7b — nierozstrzygnięcie, nie świadectwo przeciw
  hipotezie zegara inicjacji.
- **Kształt hazardu nie był badany, bo nie mógł być.** Rodzina Weibulla jest monotoniczna z
  definicji (hazard stale rosnący, stale malejący, albo stały — nigdy najpierw rosnący,
  potem malejący). Ta rodzina testów nie mogła więc wyrazić ani wykluczyć hipotezy
  narastania-i-opadania ryzyka konfliktu — pytanie pozostaje otwarte niezależnie od wyniku
  liczbowego, bo narzędzie nie było w stanie go zadać.
- **Kontrast epok (H6.2/H8.1) nierozstrzygnięty — od braku reguły do braku mocy.** Protokół
  Testu 6 nie zawierał reguły decyzyjnej dla porównania epok (D-024 §7). Reguła została
  napisana i zamrożona osobno jako `TEST10_PROTOCOL_kontrast_epok.md` (D-050), z symulacją
  mocy WYKONANĄ przed jakimkolwiek biegiem: pełna reguła §7 tego protokołu (koniunkcja
  dwóch warunków) osiąga zaledwie 16,7% mocy przy różnicy parametru 0,25 i połowę dopiero
  przy ok. 0,34 (D-051) — powyżej największego rozstępu zaobserwowanego w całej rodzinie
  dziewiątej (0,2167, między S7 i Testem 6, między jednostkami analizy, nie epokami). Autor
  zdecydował NIE URUCHAMIAĆ Testu 10 (D-052) — protokół zamrożony, niewykonany, z powodu
  braku mocy, nie zmiany zdania co do H8.1. H8.1/H6.2 pozostaje nierozstrzygnięta, teraz z
  innego powodu niż na początku: nie brak kryterium, tylko brak mocy narzędzia zbudowanego
  do jego zastosowania na tej strukturze.
- **Poziom regionalny nigdy niezdefiniowany.** Żaden wariant tej rodziny nie operacjonalizował
  jednostki regionalnej (między parą a całym systemem) — nie testowany, nie odrzucony.

## 6. Ustalenia metodologiczne (rozdział własny)

Najtrwalszy wynik tej rodziny testów nie jest liczbą k̂ — jest zestawem ustaleń o samych
narzędziach, ważnych niezależnie od tego, co ostatecznie powie się o hipotezach 6.1/9b.1/9b.2:

1. **N2 jest zdegenerowany względem statystyki pulowanej, z powodów algebraicznych, nie
   danych (D-026).** `negloglik_pooled(params, t, event)` sumuje po obserwacjach bez
   odniesienia do etykiety grupy — permutacja odstępów MIĘDZY grupami nie zmienia
   multizbioru par (t, event), więc k̂_sur ≡ k̂_obs dla KAŻDEJ permutacji, z konstrukcji.
   Wykryte analitycznie, przed jakimkolwiek biegiem na danych rzeczywistych.
2. **Reguła decyzyjna §8 protokołu jest niespełnialna w obecnym brzmieniu (D-026), z
   powodu (1).** Wymaga P2(N2)<0,10 razem z dwoma innymi warunkami; skoro P2≡1 tożsamościowo,
   warunek nie może zostać spełniony przez żaden zbiór danych. Wada leży w niespójności
   protokołu (§6 kontra §5/§7), nie w implementacji.
3. **Symulacja odzysku parametrów częściowo waliduje samą siebie.** Mechanizm `min(T,C)`
   (D-031) traktuje realną SUMĘ ekspozycji per grupa jako fakt egzogeniczny (długość okna
   administracyjnego) i symuluje na niej liczbę zdarzeń jako wynik wyścigu. To poprawia
   poważną wadę wcześniejszej wersji (cenzurowanie losowane niezależnie od zdarzeń) — ale
   oznacza też, że deklaracje mocy/odchylenia nie są w pełni niezależne od struktury
   wielkości grup w realnych danych, tylko od samych wartości `t`. Świadomy kompromis
   (uzasadniony w kodzie), nie ukryta wada — ale wart nazwania wprost jako ograniczenie
   metody, nie tylko jako jej naprawę.
4. **Parametr kruchości zapada się do numerycznej granicy przy małej liczbie grup i słabym
   sygnale (D-022).** Obserwowane konsekwentnie w S7/S7b/S7c (13/13/29 grup) — model
   orzekający staje się wtedy de facto pulowany niezależnie od formalnej poprawności.
5. **Bootstrap grupowy przy małej liczbie grup zawodzi centrowaniem, nie szerokością
   (D-045).** Symulacja pokrycia (1000 replik, k_prawdziwe=1, struktura S7, 13 grup):
   pokrycie profilu = 95,0% (nominalne), pokrycie bootstrapu = 90,1% — istotnie poniżej.
   Średnia szerokość obu przedziałów w tej symulacji była niemal identyczna (stosunek
   0,976) — zawodzi kształt/centrowanie rozkładu bootstrapowego, nie sama szerokość.
   Obserwacja węższego bootstrapu w konkretnej realnej replice (S7: 0,611; S7b: 0,767;
   S7c: 0,792) nie jest dowodem większej precyzji — dotyczy potencjalnie także Testu 6
   (18 grup), nieprzeliczone wstecz.
6. **Reguła złożona z koniunkcji warunków nie ma nominalnego poziomu istotności (D-053).**
   Zmierzone na regule §7 Testu 10 (dwa warunki, każdy nominalnie ok. 0,05): faktyczny
   odsetek fałszywych odrzuceń pod prawdą zerową wyniósł **0,7%, nie 5%** — siedmiokrotnie
   ostrzejszy. Ten sam mechanizm dotyczy §8 protokołu Testu 6 (TRZY warunki naraz — jeszcze
   bardziej konserwatywna) i §8 protokołu Testu 7 (dwa warunki) — **faktyczny poziom
   żadnej z tych dwóch reguł nigdy nie został policzony**, nazwane tu wprost, nie
   przeliczone wstecz z powodów kosztowych. Konsekwencja dla Testu 6: możliwe, że P1 nie
   osiągnął progu protokołu nie dlatego, że efekt był słaby, tylko dlatego, że reguła w
   praktyce była surowsza niż deklarowany nominalny poziom — **nie zmienia to wyniku Testu
   6** (P1/N1 nie osiągnął nawet pierwszego, pojedynczego członu: p=0,068>0,05), ale jest
   ustaleniem tej samej klasy co degeneracja N2 (1) — o konstrukcji reguł tego typu w całym
   projekcie, nie tylko o tym jednym wyniku.

## 7. Errata zbiorcza

Rejestr od początku nie rozróżniał, czyje są błędy — dobra zasada, zachowana tutaj. Ale błędy
w tej rodzinie pochodziły z obu stron, nie z jednej, i tabela poniżej to odzwierciedla, żeby
nie sugerować jednostronności, której nie było.

| co | błędne | poprawne | kto zgłosił | źródło |
|---|---|---|---|---|
| silnik statystyczny Kroku 3 Testu 6 | profil/bootstrap podstawione za N1/N2 protokołu, bez odnotowania podstawienia | powtórzone zgodnie z §6–§8; profil/bootstrap zostają jako analiza uzupełniająca | autor, jako projektant briefu | D-023 |
| zatwierdzenie symulacji odzysku (pierwszy przegląd) | mechanizm nieodtwarzający cenzurowania min(T,C) zatwierdzony w drugim przeglądzie autora | naprawiony po trzecim przeglądzie | autor, jako recenzent — własna pomyłka recenzencka | D-031 |
| liczby kontrolne S7 (próg≥6/≥3) w `TASK_S7.md` | 12 państw/98 zdarzeń; 37/168 (reguła gap≤1, niezapisana) | 13/110 (gap≤0, potwierdzone kodem Testu 6); 39/182 | Code, w brifie autora | D-039 |
| przyczyna S7 v1.0 15→13 (pierwsze stwierdzenie Code) | "tylko Francja" | siedem państw | autor, w kodzie/analizie Code | D-041 |
| deklaracja S7b/S7c (próg≥3) | 14 państw/54 zdarzenia (S7b); 30/100 (S7c) — reguła sprzed D-040 | 13/50 (S7b); 29/95 (S7c) | autor, własna rozbieżność | D-047 |
| liczby inicjacji wojen | Włochy 7, Niemcy 7 (uczestnictwa liczone podwójnie za fazy) | Włochy 6, Niemcy 5 (epizody) | autor, własna rozbieżność | D-046/D-047 |
| przepowiednia S7 (k̂, przedziały, kierunek rozjazdu) | k w 0,75–0,90, profil wyklucza 1, bootstrap szerszy niż profil | k=0,9947, żaden przedział nie wyklucza 1, bootstrap węższy | autor, własna przepowiednia, wycofana po wyniku | D-043→D-044→D-045 |

## 8. Status końcowy

**Rodzina dziewiąta jest zamknięta (autor, 2 września 2026).**

**Rodzina dziewiąta nie ma ani jednego wyniku pozytywnego pod regułą pre-rejestrowaną.**
Test 6 — metoda protokołu (N1) nie osiągnęła progu istotności (p=0,068 wobec <0,05), a
reguła §8 jest niespełnialna z powodu degeneracji N2; analiza uzupełniająca (profil/
bootstrap) wskazuje kierunek zgodny z hipotezą, ale nie orzeka (D-023). Dwa warianty dały
wynik zerowy przypisywalny danym, przy dostatecznej czułości do wykrycia efektu wielkości
Testu 6: S7 (państwo, wszystkie wojny) i S7c (państwo, wojny jako cel). Dwa warianty dały
nierozstrzygnięcie z braku mocy, nie świadectwo przeciw żadnej hipotezie: Test 7 P1 (pary po
stawce) i S7b (państwo, inicjacje).

**Co konkretnie upadło, a co nie.** Zegar PAŃSTWA obejmujący wszystkie wojny upadł — w
wariancie o dostatecznej czułości (S7), efekt wielkości Testu 6 zostałby wykryty i nie
został. Zegar INICJACJI (mechanizm "państwo kończy wojnę i rusza dalej", hipoteza wyjściowa
S7b) NIE upadł — S7b był za słaby, żeby cokolwiek rozstrzygnąć w tę czy drugą stronę.
Rozróżnienie to jest w tabeli głównej (§3), stoi też tutaj wprost, żeby nie zostało
przeoczone.

Hipoteza zegara bilateralnego (mechanizm pary, nie aktora) pozostaje otwarta — nie obalona,
nie potwierdzona, poza zasięgiem pomiarowym tej rodziny z powodów strukturalnych (§5), nie z
powodu braku wysiłku. Kształt hazardu, kontrast epok (H6.2) i poziom regionalny pozostają
nierozstrzygnięte z innych, niezależnych powodów (§5).

Wariant S7 (i pochodne S7b/S7c) pozostają, zgodnie z ustaleniem sprzed pierwszego biegu
(`TASK_S7.md` §8), wariantami wrażliwości — nie awansują na wariant pierwszorzędny
niezależnie od wyniku.

**Test 10 (kontrast epok, H8.1) zamrożony i NIEWYKONANY (D-050–D-052).** Reguła decyzyjna
napisana i zamrożona po raz pierwszy (protokół Testu 6 nigdy jej nie miał). Symulacja mocy
wykonana przed jakimkolwiek biegiem: pełna reguła osiąga 16,7% mocy przy różnicy 0,25,
połowę dopiero przy ok. 0,34 — powyżej największego rozstępu zaobserwowanego w całej rodzinie
(0,2167). Autor zdecydował nie uruchamiać — powodem jest brak mocy, nie zmiana zdania co do
H8.1. Protokół pozostaje zamrożonym dokumentem na przyszłość, gdyby struktura danych się
zmieniła (np. więcej państw spełniających próg).

Możliwy dalszy krok, wspomniany wcześniej (D-032), nie podjęty w ramach tej rodziny:
"protokół 9c" (test lokalizacji szczytu hazardu) — osobna, nowa rodzina testów, poza
zakresem tego dokumentu.
