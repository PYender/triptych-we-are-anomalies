# Test 13 — raport zamykający (trend parametru kształtu k, UCDP)

**Status: Etap 4 wykonany, wynik przyjęty przez autora, wyjaśnienie B sprawdzone i
odrzucone (D-067/D-068). Raport poniżej domyka test.**

---

## 0. Ujawnienie na początku: geneza protokołu

**Ten protokół powstał PO zobaczeniu wyniku.** Test 13 nie był pre-rejestrowany niezależnie
od danych — wynikł wprost z obserwacji S3 Testu 12 (podział epoki 1989, opisowy, bez reguły
decyzyjnej): k̂ dla par przed 1989 = 0,625 (n=64 wiersze), k̂ dla par po 1989 = 0,793 (n=230
wierszy). Autor zauważył, że to nie wygląda na złamanie w jednym punkcie (S3 było testem
"break", nie trendu) tylko na monotoniczny dryf w czasie, i zbudował protokół Testu 13 wokół
tej obserwacji.

Konsekwencja wprost: **efekt zaobserwowany w S3 jest tym samym zjawiskiem, które Test 13
mierzy formalnie** — nie jest to niezależna replikacja. To nie unieważnia wyniku (Test 13 ma
własny model zerowy, własną regułę decyzyjną i własne dane kontrolne), ale znaczy, że ani
sam fakt istnienia trendu, ani jego przybliżony kierunek, nie były zaskoczeniem w momencie
zamrażania protokołu — w przeciwieństwie do konkretnej WIELKOŚCI efektu (0,195/dekadę,
znacznie większej niż deklarowane przed biegiem 0,05/dekadę, D-067) oraz kierunku obu
pomiarów wyjaśnień konkurencyjnych (§4 poniżej), które BYŁY zaskoczeniem względem
deklaracji sprzed biegu.

## 1. Pytanie i czego test nie orzeka

**Pytanie:** czy parametr kształtu Weibulla k, opisujący strukturę odstępów między
epizodami konfliktu tej samej pary UCDP, zmienia się systematycznie z rokiem kalendarzowym
startu odstępu.

**Czego test NIE orzeka:**

- **Nie orzeka o przyczynie.** Trend jest zmierzony jako zjawisko opisowe na poziomie
  parametru statystycznego. Test nie rozstrzyga, czy przyczyną jest zmiana charakteru
  konfliktów, zmiana definicji/kodowania UCDP, zmiana składu geopolitycznego świata, czy
  cokolwiek innego — poza dwoma konkretnymi konkurencyjnymi mechanizmami zmierzonymi i
  odrzuconymi w §4.
- **Nie orzeka o pojedynczej parze.** k jest parametrem populacyjnym (wspólnym dla wszystkich
  294 obserwacji ważonych modelem), nie cechą żadnej konkretnej pary konfliktu.
- **Nie orzeka o okresowości/rytmie.** To jest, tak jak cała rodzina dziewiąta (Test 6/7/S7),
  pytanie o strukturę POJEDYNCZEGO procesu odnowy (pamięć/brak pamięci), nie o regularny
  cykl w zagregowanym szeregu czasowym — rozróżnienie ustalone już w raporcie rodziny
  dziewiątej (§0 tamtego dokumentu) i tu w pełni obowiązujące. Górna granica przedziału dla
  2020 (1,013) dotyka k=1 (brak pamięci) — dane nie pokazują nigdzie przejścia w stronę k>1
  (rytmiczność).
- **Nie orzeka poza zmierzonym zakresem lat.** Krzywa jest oszacowana dla lat 1948–2023 (zakres
  rzeczywistych danych); ekstrapolacja poza ten zakres nie jest częścią wyniku.

## 2. Wynik — wielkość efektu jako liczba pierwszorzędna

Zgodnie z filozofią raportowania tego testu (§1 protokołu, `TEST13_PROTOCOL_trend_ksztaltu.md`),
wynikiem pierwszorzędnym jest wielkość efektu z przedziałem, nie sama klasyfikacja.

| wielkość | wartość |
|---|---|
| b_obs (surowe, dopasowanie bez korekty) | 0,0923 |
| środek rozkładu zerowego (D-063) | −0,1030 |
| **efekt (b_obs − środek zerowy)** | **0,1953** |
| przedział (≈95%, ±1,96·SD_null) | **[0,112; 0,279]** |
| wartość p (dwustronna, względem rozkładu surogatów) | 0,001 |
| reguła (jednoczłonowa, próg 0,05) | spełniona, z ok. 50-krotnym zapasem |

**Implikowane wartości k(rok), 95% CI bootstrap (klastrowanie po parze):**

| rok | k(rok) | 95% CI |
|---|---|---|
| 1950 | 0,474 | [0,380; 0,607] |
| 1985 | 0,654 | [0,602; 0,721] |
| 2020 | 0,904 | [0,801; 1,013] |

Przedziały dla 1950 i 2020 nie nakładają się, z dużym marginesem. Efekt (0,195/dekadę) jest
**ok. czterokrotnie większy** niż deklarowana przed biegiem wielkość referencyjna
(0,05/dekadę, D-064) — przy tamtej deklarowanej wielkości i mocy ok. 20% (§8 protokołu),
odrzucenie było zdarzeniem mało prawdopodobnym samo w sobie; wystąpiło mimo to, co per
deklarację sprzed biegu (§5 poniżej, ograniczenie 2) wskazuje na trend silniejszy niż
zakładany, nie na przypadek.

**Kierunek zmiany:** k rośnie z rokiem — od struktury silnie skupiającej epizody konfliktu
w czasie (k≈0,47 w 1950: krótki czas od ostatniego starcia silnie zapowiada kolejne) w
stronę struktury bliskiej procesowi bez pamięci (k≈0,90 w 2020), bez przekroczenia w stronę
rytmiczności.

## 3. Metoda raportowania — obciążenie działa PRZECIW obserwacji, nie na jej korzyść

Kluczowe dla interpretacji wielkości efektu: gdyby efekt liczyć naiwnie względem zera (b_obs
wprost), wyszłoby 0,0923 — **dwukrotnie mniej** niż właściwa wielkość 0,1953. Sposób
raportowania ustalony w D-059/§4 protokołu (efekt względem środka rozkładu zerowego, nie
względem zera) w tym konkretnym przypadku WZMOCNIŁ wynik, nie osłabił — bo procedura
pomiarowa pod stałym parametrem produkuje pozorny SPADEK (środek zerowy −0,103), podczas gdy
obserwacja idzie w górę. Artefakt ciągnie w dół, obserwacja mimo to idzie w górę — te dwie
wielkości (surowe b_obs, środek zerowy, oba efekty) pokazane naraz w wykresie efektu
(publikowany artefakt, panel 2) są, zdaniem obu stron, najczytelniejszym przedstawieniem
tego argumentu w całym projekcie.

## 4. Dwa pomiary wyjaśnień konkurencyjnych — oba wyszły przeciwnie do naiwnej intuicji

**A. Ucinanie przez koniec okna 2023 (D-060/D-063).** Naiwna intuicja (zasygnalizowana przez
autora przed pomiarem): krótsze obserwowane odstępy w późniejszych latach, przez ucinanie w
2023 r., powinny dawać WYŻSZY pozorny parametr kształtu w późniejszych latach — czyli
artefakt idący W TĘ SAMĄ stronę co obserwacja (dodatni), co osłabiałoby wynik. Zmierzone:
środek rozkładu zerowego = **−0,103** (D-063, k̂/λ̂ z dopasowania bez trendu, discretize_gap) —
**ujemny**, przeciwny do intuicji autora. Wyjaśnienie: właściwie zbudowana wiarygodność z
cenzurowaniem WŁĄCZA ucięte obserwacje do dopasowania przez ich funkcję przeżycia, nie tylko
je odrzuca — to różnica między "ignorować cenzurowanie" (intuicja autora, poprawna dla
naiwnej analizy) a "modelować cenzurowanie" (co robi ten estymator). Rezultat: artefakt
działa PRZECIW obserwacji, nie na jej korzyść — wzmacnia wynik po korekcie, zamiast go
osłabiać.

**B. Gęstość kodowania / malejąca mediana odstępu (D-068).** Naiwna intuicja (autor, po
wyniku D-067): skoro mediana odstępu spada z ok. 15 lat (l. 50.) do ok. 1 roku (dziś), a
oryginalny model zerowy (§5) używa jednej wspólnej skali dopasowanej do całości, to
uwzględnienie zmieniającej się skali POWINNO przesunąć środek modelu zerowego w stronę
surowego b_obs (+0,092) — czyli częściowo WYTŁUMACZYĆ obserwowany trend. Zmierzone: model
zerowy ze skalą zależną od roku (log λ(rok)=c+d·(rok−1985)/10, dopasowane MLE do danych,
k stałe) dał środek **−0,135** — DALEJ od zera niż oryginalny (−0,103), nie bliżej +0,092.
Wyjaśnienie: gdy skala kurczy się z czasem do rzędu jednostki zaokrąglenia (rok
kalendarzowy), zniekształcenie estymacji k przez dyskretyzację robi się WZGLĘDNIE silniejsze,
nie słabsze — więc pozwolenie skali na spadek pogłębia ten sam artefakt zaokrąglenia, zamiast
go tłumaczyć realnym mechanizmem gęstości kodowania. Rezultat: efekt liczony względem tego
alternatywnego środka wychodzi WIĘKSZY (0,228), nie mniejszy.

**Wspólny mianownik obu pomiarów:** w obu przypadkach naiwna intuicja o kierunku artefaktu
była odwrócona przez właściwie zbudowany mechanizm cenzurowania/dyskretyzacji. To nie jest
przypadek — jest strukturalną cechą tego rodzaju pomiaru (już widoczną wcześniej w Teście 12,
pomiar A, D-060) i powodem, dla którego ten projekt mierzy artefakty zamiast zakładać ich
kierunek.

## 5. Ograniczenia

Trzy zapisane PRZED biegiem (§9 protokołu, wynikające z mocy ok. 20% przy deklarowanej
wielkości referencyjnej 0,05/dekadę):

1. **Wynik nieistotny nic by nie powiedział.** Przy mocy ok. 20% brak odrzucenia byłby
   spodziewany nawet przy prawdziwym trendzie wielkości referencyjnej — nie stało się tak
   (reguła spełniona z dużym zapasem), ale to ograniczenie odnosi się do tego, jak CZYTAĆ
   ewentualny wynik nieistotny w tej rodzinie testów w przyszłości, nie unieważnia obecnego.
2. **Wynik istotny znaczy sporo.** Przy dwudziestoprocentowej mocy odrzucenie wymagało albo
   trendu silniejszego niż zakładane 0,05/dekadę, albo szczęścia — pierwsze bardziej
   prawdopodobne. Zmierzony efekt (0,195) jest rzeczywiście ok. czterokrotnie większy niż
   zakładane 0,05 — zgodne z tą przesłanką.
3. **Przedział jest szeroki i to jest wynik, nie jego brak.** Przedział [0,112; 0,279] ma
   szerokość zbliżoną do tego, co przewidziano (ok. 0,17 przy założonym efekcie) — wyklucza
   trendy bardzo małe i bardzo duże, nie jest precyzyjnym punktowym oszacowaniem.

Czwarte — niezmierzone, dopisane teraz na żądanie autora:

4. **Rozdzielczość pomiaru w ostatnich dekadach.** Mediana odstępu spadła z rzędu 15 lat
   (lata 50.) do rzędu 1 roku (dziś, D-060/§7B). W konsekwencji w ostatnich dekadach niemal
   wszystkie obserwacje leżą w jednym lub dwóch punktach siatki rocznej (1 lub 2 lata). Czy
   parametr kształtu k jest tam jeszcze wielkością mierzoną w sensowny sposób, czy w
   praktyce funkcją samej rozdzielczości pomiaru (rok kalendarzowy), pozostaje pytaniem
   otwartym. Model zerowy (§5 protokołu) przechodzi przez TĘ SAMĄ dyskretyzację co dane
   rzeczywiste, więc formalnie tę sytuację obsługuje — ale granica, od której pomiar
   przestaje nieść informację o k i zaczyna odzwierciedlać wyłącznie siatkę roczną, nie
   została zmierzona.

## 6. Ustalenia metodologiczne (rozdział własny)

**Obciążenie z dyskretyzacji jest ok. 2,4–2,5 raza większe od własnego rozrzutu.** Środek
rozkładu zerowego (−0,1030) podzielony przez jego odchylenie standardowe (0,0425) daje
|−0,1030|/0,0425 ≈ **2,42**. Konsekwencja praktyczna: gdyby porównywać surowe b_obs z zerem
(zamiast ze środkiem rozkładu zerowego), w niemal KAŻDYM biegu tej procedury — nawet przy
prawdziwym braku trendu — wyszłoby "istotne odchylenie" na czystym artefakcie pomiarowym.
Test bez poprawki (D-062/D-063: k̂/λ̂ z dopasowania bez trendu, nie k=1; skala z danych, nie
przyjęta z góry; p względem rozkładu surogatów, nie zera) byłby generatorem fałszywych
wyników, nie pomiarem — to ustalenie ogólne, wykraczające poza Test 13, dotyczące każdego
podobnego pomiaru na danych UCDP zaokrąglonych do lat kalendarzowych z niejednorodną skalą
w czasie.

**Kalibracja poprawionej procedury zweryfikowana empirycznie, nie założona.** Konstrukcja
"każde ciągnienie jako obserwacja wobec pozostałych" (D-064, N=2000) dała udział fałszywych
odrzuceń 0,0495 wobec nominalnego 0,05 — potwierdza, że porównanie dwustronne względem
środka (niekoniecznie symetrycznego) rozkładu zerowego jest poprawnie skalibrowane, zamiast
zakładać to na podstawie teorii testów Monte Carlo bez sprawdzenia.

**Addytywność artefaktu potwierdzona pomiarem mocy (D-064), nie założona.** Przy trzech
zadanych wielkościach prawdziwego trendu (0,025/0,05/0,10 na dekadę) surowe oszacowanie
b̂ ≈ b_true + środek_zerowy w granicach szumu Monte Carlo we wszystkich trzech przypadkach —
podstawa dla traktowania `efekt = b_obs − środek_zerowy` jako sensownego oszacowania
prawdziwego trendu, nie tylko jako wygodnej definicji.

## 7. Historia decyzji

D-060 (Etap 1, trzy wyjaśnienia konkurencyjne, wynik A odwrotny do intuicji) → D-061
(diagnoza rozbieżności znaku z niezależną replikacją autora, discretize_gap potwierdzony) →
D-062 (errata §5, model parametryczny zamiast permutacyjnego, na żądanie autora) → D-063
(obie decyzje autora rozstrzygnięte: k̂/λ̂ z dopasowania bez trendu, discretize_gap wszędzie;
charakterystyka poprawionego modelu zerowego) → D-064 (Etap 2 dokończony: kalibracja 0,0495,
moc 9,4/19,6/59,8%, addytywność artefaktu) → D-065 (Etap 3: zamrożenie protokołu, numer 13,
ziarno 20260823) → D-066 (autoryzacja Etapu 4, zapisana przed obliczeniem b_obs) → D-067
(wynik decydujący: efekt 0,195/dekadę, p=0,001) → D-068 (sprawdzenie wyjaśnienia B, odrzucone
— nowy środek −0,135, dalej od zera niż oryginalny, nie bliżej surowego b_obs).

## 8. Status końcowy

**Test 13 orzeka. Reguła jednoczłonowa spełniona z dużym zapasem (p=0,001 wobec progu 0,05).
Wielkość efektu: 0,195/dekadę, przedział [0,112; 0,279]. Oba konkurencyjne wyjaśnienia
zmierzone i odrzucone jako źródła obserwowanego kierunku trendu — w obu przypadkach
zmierzony kierunek artefaktu okazał się przeciwny do naiwnej intuicji, wzmacniając zamiast
osłabiać wynik. Pozostaje otwarte pytanie o rozdzielczość pomiaru w ostatnich dekadach (§5,
ograniczenie 4) — niezmierzone, nie unieważnia wyniku, ale ogranicza jego interpretację w
najnowszym końcu szeregu.**

Klasyfikacja merytoryczna (wsparty/graniczny/niewsparty per §6 protokołu) nie jest tu
osobno powtarzana jako punkt sporny — wynika wprost z p=0,001 < 0,05 — ale zgodnie z
filozofią tego testu (§1 protokołu) to wielkość efektu, nie etykieta, jest tu wynikiem
głównym.
