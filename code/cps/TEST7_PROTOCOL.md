# TEST 7 — PROTOKÓŁ (rodzina 9b): czas oczekiwania na wojnę w rywalizacjach przestrzennych

**Wersja:** 1.0 · **Zamrożony:** 2026-08-23 · **Rejestr:** D-016
**Status:** zamrożony przed jakimkolwiek obliczeniem statystyki czasów oczekiwania na tej populacji.

Protokół jest zamknięty. Zmiana któregokolwiek z paragrafów §1–§9 po rozpoczęciu obliczeń
wymaga nowego wpisu w rejestrze i unieważnia bieg.

---

## §0. Stosunek do Testu 6

Rodzina 9b **nie zastępuje** Testu 6 i nie jest jego poprawką. Test 6 zostaje dokończony na
swojej pierwotnej populacji i raportowany osobno. Wyniki obu testów nie są wymienne — mierzą
tę samą wielkość na **różnych populacjach**, dobranych według kryteriów, z których jedno
(Test 6) selekcjonuje po liczbie konfliktów, a drugie (tutaj) nie.

Jeśli oba testy dadzą różne wyniki, **różnica jest wynikiem** i mówi o wpływie doboru
populacji. Nie wolno wybrać tego, który wypadnie korzystniej.

## §1. Pytanie i hipotezy

**Pytanie.** Czy w parach państw o wspólnej stawce terytorialnej ryzyko wybuchu wojny zależy
od czasu, jaki upłynął od poprzedniej — a jeśli tak, czy zależy od jej kosztu?

**H9b.1 — kształt.** Rozkład czasów oczekiwania ma parametr kształtu Weibulla różny od 1.
- `k > 1`: ryzyko rośnie z upływem czasu — mechanizm regeneracji, wsparcie dla H1
- `k = 1`: ryzyko stałe, rozkład bez pamięci
- `k < 1`: ryzyko maleje — grupowanie, hipoteza konkurencyjna

**H9b.2 — mechanizm.** Czas oczekiwania jest tym dłuższy, im kosztowniejszy był poprzedni
konflikt (dłuższy, krwawszy).

H9b.2 jest twierdzeniem **mocniejszym i ciekawszym** niż H9b.1, bo pyta wprost o mechanizm
zamiast wnioskować o nim z kształtu rozkładu.

## §2. Populacja (D-016)

Diada wchodzi wtedy i tylko wtedy, gdy figuruje w `tss_rivalries` (Thompson, Sakuwa, Suhas
2021) ze znacznikiem `spatial = 1`. **141 diad.**

**Żadnego progu liczby wojen.** Diada, która nie miała ani jednej wojny, wchodzi jako
obserwacja w pełni cenzurowana.

**Zakaz doboru ręcznego.** Żadnej pary nie wolno dodać ani usunąć poza tym kryterium,
w szczególności żadnej pary wymienionej w rozmowie z autorem. Kontrola nazw ma być wykonana
i raportowana **w obie strony**, jak w rodzinie 9.

## §3. Okno ryzyka

Dla diady *(a, b)* okno otwiera się w roku

```
t_start = max( start_rywalizacji, wejście_a_do_systemu, wejście_b_do_systemu, 1816 )
```

i domyka w roku

```
t_end = min( koniec_rywalizacji, wyjście_a, wyjście_b, 2007 )
```

**Ekspozycja liczona jak w D-014:** do czasu wchodzą wyłącznie lata, w których oba państwa
figurują w `system2016.csv` **i** rywalizacja trwa. Zegar zatrzymuje się, nie zeruje (D-015 A).

Rok 2007 to koniec zakresu `Inter-StateWarData_v4.0.csv`. Diady o oknie zerowym lub ujemnym
wypadają — jest ich 12 ze 141, zostaje **129**.

**Lewostronne ucięcie.** Dla 18 rywalizacji zaczynających się przed 1816 okno otwiera się
w 1816, a pierwszy odstęp **nie jest** odstępem od początku rywalizacji. Diady te muszą być
oznaczone kolumną `ucięta = 1` i wchodzić do wariantu S3 (§7), nie do modelu głównego.

## §4. Zdarzenia

Zdarzeniem jest **epizod** konfliktu w rozumieniu D-013: konflikty tej samej diady
o przedziałach nachodzących się lub stykających scalane przechodnio w jeden epizod. Źródło:
`Inter-StateWarData_v4.0.csv`.

Kod `-7` i wartości ujemne obsługiwane zgodnie z F1 — zgłaszane, nie zastępowane zerem.

## §5. Struktura obserwacji

Każda diada wnosi ciąg czasów, wszystkie mierzone w latach ekspozycji:

| składnik | opis | status |
|---|---|---|
| `t0` | od otwarcia okna do pierwszego epizodu | **poza modelem głównym** — patrz niżej |
| `t1 … t_{m−1}` | odstępy między kolejnymi epizodami | pełne |
| `t_m` | od ostatniego epizodu do domknięcia okna | cenzurowany prawostronnie |

Diada bez żadnego epizodu wnosi jedną obserwację w pełni cenzurowaną, o długości całego okna.

**Założenie o `t0`, deklarowane jawnie.** Czas od otwarcia okna do pierwszej wojny nie jest tą
samą wielkością co odstęp między wojnami: początek rywalizacji jest punktem odniesienia
nadanym z zewnątrz, a nie zdarzeniem odnawiającym proces. **Model główny liczy się bez `t0`
dla diad, które miały co najmniej jeden epizod**, i z pełnym cenzurowaniem dla diad bez
epizodów. Włączenie `t0` jako pełnoprawnego odstępu jest wariantem S3.

## §6. Zmienne objaśniające (dla H9b.2)

Liczone dla **poprzedniego epizodu**, więc niedostępne dla `t0` i dla diad bez epizodów —
te obserwacje wchodzą do modelu H9b.1, nie do H9b.2.

| zmienna | źródło | postać |
|---|---|---|
| czas trwania poprzedniego epizodu | COW inter-state | lata |
| straty poprzedniego epizodu | `BatDeath`, suma po obu stronach diady | logarytm |
| status mocarstwowy | `majors2016.csv`, w roku końca epizodu | 0 / 1 / 2 mocarstwa w diadzie |
| potencjał gospodarczy | **COW NMC (do wgrania)** | CINC: suma i stosunek stron |
| istotność stawki | **ICOW roszczenia terytorialne (do wgrania, opcjonalne)** | indeks namacalny i nienamacalny, osobno |
| kontrola wojen światowych | COW | poprzedni epizod obejmował 1914–18 lub 1939–45: 0/1 |

**Agregacja strat do poziomu diady jest wyborem, nie danymi** — `BatDeath` jest kodowane na
uczestnika. Reguła: suma po obu stronach danej diady, z wyłączeniem uczestników spoza pary.
Zapisać w raporcie.

Zmiennych nie wolno dodawać po biegu. Jeśli NMC albo ICOW nie zostaną dostarczone, model H9b.2
liczy się bez nich i fakt ten jest raportowany — nie zastępujemy ich substytutami.

## §7. Model i warianty — cztery dopasowania

| id | model | zbiór | rola |
|---|---|---|---|
| **P1** | Weibull z kruchością gamma, cenzurowanie prawostronne, bez zmiennych | 129 diad, bez `t0` | **ORZEKA dla H9b.1** |
| **P2** | to samo + zmienne objaśniające §6 (AFT) | diady z ≥ 1 epizodem | **ORZEKA dla H9b.2** |
| S1 | P1 bez epizodów obejmujących wojny światowe | — | wrażliwość na synchronizację |
| S2 | P1 na rywalizacjach o `spatial = 1` **i** `positional = 0` | — | wrażliwość na typ rywalizacji |
| S3 | P1 z włączonym `t0` jako odstępem pełnym | — | wrażliwość na założenie §5 |
| S4 | P1 na `td_rivalries` (Thompson i Dreyer 2012, 197 rywalizacji) | — | wrażliwość na kodowanie źródła |

Cztery dopasowania orzekające i pomocnicze plus cztery wrażliwości. **Nie krzyżować wymiarów**
— każda wrażliwość zmienia jedną rzecz wobec P1.

Kruchość gamma dzielona w obrębie diady, wiarygodność brzegowa jak w `TASK_6B_BRIEF.md` §3,
z obowiązkowym testem granicy θ → 0 i testem odzysku parametrów na danych syntetycznych
o strukturze zbioru rzeczywistego.

## §8. Reguła decyzyjna — zadeklarowana przed biegiem

**H9b.1 uznaje się za wsparte**, jeżeli przedział ufności dla `k` z profilu wiarygodności
w P1 **nie obejmuje 1** oraz ten sam kierunek utrzymuje się w S1 i S3.

**H9b.2 uznaje się za wsparte**, jeżeli w P2 współczynnik przy koszcie poprzedniego epizodu
(czas trwania albo straty) jest istotny na poziomie 0,05 i ma znak dodatni (dłuższy pokój po
kosztowniejszej wojnie), oraz nie odwraca się po usunięciu wojen światowych (S1).

**Przedziały ufności obowiązkowe**, w dwóch postaciach: profil wiarygodności oraz bootstrap
losujący **całe diady**. Wartość punktowa bez przedziału nie jest wynikiem.

**Wynik nierozstrzygający jest dopuszczalnym wynikiem.** Przy przedziale obejmującym 1
raportujemy to jako brak rozstrzygnięcia, nie szukamy wariantu, w którym nie obejmuje.

## §9. Zakazy

1. Nie zmieniać definicji populacji (§2) po rozpoczęciu obliczeń.
2. Nie wprowadzać progu liczby wojen w żadnej postaci — to zniszczyłoby jedyną przewagę tego
   testu nad Testem 6.
3. Nie używać rywalizacji trwałych Diehla i Goertza jako filtru (tautologia — definiowane
   przez gęstość sporów).
4. Nie dodawać zmiennych objaśniających po biegu.
5. Nie wybierać między P1 a wariantami wrażliwości po zobaczeniu wyników.
6. Nie wybierać między Testem 6 a Testem 7 po zobaczeniu, który wypadł korzystniej.
7. Nie zgadywać zawartości zbiorów niedostarczonych.

## §10. Ograniczenia, zapisane przed biegiem

**Kodowanie rywalizacji jest osądem z historii dyplomatycznej**, nie pomiarem. Daty początku
i końca mają niekwantyfikowaną niepewność. S4 pokazuje wrażliwość, ale jej nie usuwa.

**Lewostronne ucięcie** dotyczy 18 rywalizacji sprzed 1816 (§3).

**Niezależność diad jest naruszona.** Ustalenie z Testu 6 — 27% epizodów kończy się w 1918
albo 1945 — przenosi się na tę populację. Bootstrap po diadach nie łapie zależności *między*
diadami. Problem nierozwiązany; S1 pokazuje jego skalę, nie naprawia go.

**Zakres COW.** Rywalizacje istniejące przed 1816 i wojny inne niż międzypaństwowe pozostają
poza analizą. Niemcy–Polska i Francja–Anglia są rywalizacjami przestrzennymi, ale ich historia
konfliktowa leży w znacznej części przed początkiem zbioru — ich wejście do populacji nie
oznacza, że test cokolwiek o nich powie.

**Mediana okna ryzyka to 31 lat** przy kwartylach 13,5 i 61. Wiele diad wnosi krótkie okna
i jedną obserwację cenzurowaną. Realna informacja pochodzi z mniejszości par.

## §11. Etapy

**A — dane.** Budowa zbioru okien ryzyka, epizodów i czasów. Raport z liczbami kontrolnymi,
kontrolą nazw w obie strony, listą diad odpadających z powodu pustego okna. **STOP.**

**B — kod.** Implementacja P1, P2 i wrażliwości, z testami poprawności (granica θ → 0, odzysk
parametrów). Bez uruchamiania na danych rzeczywistych. **STOP.**

**C — bieg.** Wyniki commitowane przed raportem. Raport podaje przedziały, nie wartości
punktowe, i zestawia P1 z S1–S4 oraz z wynikiem Testu 6.

## §12. Zbiory wejściowe

| zbiór | status |
|---|---|
| `tss_rivalries` (Thompson i in. 2021) | osiągalny przez `codeload.github.com` — archiwum `svmiller/peacesciencer`, plik `data/tss_rivalries.rda` |
| `td_rivalries` (Thompson i Dreyer 2012) | j.w., `data/td_rivalries.rda` |
| `Inter-StateWarData_v4.0.csv` | w repo |
| `system2016.csv`, `majors2016.csv` | w repo |
| **COW NMC** (potencjał gospodarczy) | **do wgrania z sumą kontrolną** |
| **ICOW roszczenia terytorialne** (istotność stawki) | **do wgrania, opcjonalne** |

Dla każdego zbioru pobranego z zewnątrz raport podaje sumę kontrolną. Przy niedostępności
zbioru — zgłoszenie i zatrzymanie, nigdy odtwarzanie zawartości z pamięci.
