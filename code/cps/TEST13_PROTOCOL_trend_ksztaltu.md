# TEST 13 — protokół (ZAMROŻONY)

**Numer:** 13
**Ziarno (RNG_SEED):** 20260823
**Wersja:** 1.0 (zamrożona), zastępuje SZKIC v0.1
**Status:** Etap 1 (§7) i Etap 2 (§8) wykonane i przyjęte. Etap 3 (to zamrożenie) —
autoryzowany. Etap 4 (bieg, obliczenie `b_obs` na danych rzeczywistych) — **wymaga
osobnej autoryzacji autora**, nie jest częścią tego zamrożenia.

---

## §1. Cel, hipoteza, filozofia raportowania

**Hipoteza:** parametr kształtu Weibulla `k` zmienia się liniowo w skali logarytmicznej
z rokiem kalendarzowym startu odstępu, na tle par UCDP wieloepizodowych (próg≥3, t0 pary
406 wykluczone, D-057).

**Filozofia raportowania (obowiązująca od D-059, formalizowana tutaj):** wynikiem
pierwszorzędnym jest **wielkość efektu z przedziałem** (§4), nie sama klasyfikacja
wsparty/niewsparty. Reguła decyzyjna (§6) jest wtórna wobec efektu — raportowane są
zawsze oba: liczba i próg.

**Wynik nieistotny statystycznie nie jest równoznaczny z brakiem efektu** — patrz §9
(ograniczenia wynikające z mocy).

## §2. Dane i model

Model: `log k(rok) = a + b·(rok−1985)/10`, skala `λ` wspólna (nie zależy od roku).
Parametr orzekający: `b` (zmiana `log k` na dekadę).

Dane: UCDP Dyadic v25.1, pary z ≥3 epizodami (próg≥3), pierwszy odstęp pary 406
wykluczony (D-057, t0_flag=1). N=294 obserwacji (220 pełnych, 74 cenzurowanych na
granicy administracyjnej 2023). Rok „startu zegara” = `ep_end` poprzedniego epizodu
(fakt egzogeniczny).

## §3. Estymator

`test13_trend.py`: `negloglik_trend` (log-wiarygodność Weibulla z cenzurowaniem),
`fit_trend` (multistart Nelder-Mead, `DEFAULT_X0_TREND`, 4 starty), `profile_ci_b`,
`bootstrap_ci_b`. Zwalidowany na danych syntetycznych o znanych parametrach (odzyskuje
a,b,λ zadane). Kontrola: bez cenzurowania (admin_max=∞) estymator daje b̂≈0,004±0,048 —
sam estymator nie niesie wbudowanego obciążenia; obciążenie opisane w §4/§5 pochodzi
WYŁĄCZNIE z interakcji cenzurowania administracyjnego (2023) z dyskretyzacją rocznikową,
nie z samego estymatora.

## §4. Wielkość raportowana (efekt) — definicja

**Ustalone jako element metody (D-063/D-064), nie jako ciekawostka:** procedura
pomiarowa pod prawdziwie stałym `k` (brak trendu) generuje niezerowy pozorny trend
(artefakt administracyjnego ucięcia w 2023 r. w interakcji z dyskretyzacją rocznikową,
§5). Zmierzono (pomiar 3, D-064), że artefakt dokłada się w przybliżeniu **addytywnie**:
przy trendzie prawdziwym 0,10 surowe oszacowanie wynosi −0,012 ≈ 0,10 + (−0,103).

**Wielkość raportowana jako efekt:**

```
efekt = b_obs − center_null
```

gdzie `center_null` = średnia rozkładu surogatów modelu zerowego (§5), ustalona
(pomiar 1, D-063) na **−0,1030** (B=2000, ziarno 20260823, odchylenie 0,0425).

**Przedział:** przybliżony 95%, zbudowany na odchyleniu rozkładu zerowego (nie
literalne zero jako punkt odniesienia):

```
efekt ± 1,96 · SD_null,   SD_null = 0,0425  →  efekt ± 0,083 (szerokość ≈ 0,17)
```

Ta sama zasada „punkt odniesienia = to, co generuje procedura pod stałym parametrem, nie
zero" obowiązuje jednolicie dla efektu, przedziału i wartości p (§5/§6) — to jest sedno
erraty D-062.

## §5. Model zerowy N3 (PO POPRAWCE — errata D-062/D-063, zastępuje permutacyjny N3
ze szkicu v0.1)

Model zerowy: **parametryczny**, nie permutacyjny. `k̂` i `λ̂` pochodzą z dopasowania
Weibulla **BEZ trendu** (`test6_weibull.fit_pooled`, `test13_n3.fit_no_trend`) do TYCH
SAMYCH rzeczywistych danych, które zasilają dopasowanie decydujące — zwykły bootstrap
parametryczny. **Nie k=1** — hipoteza zerowa tego testu brzmi „parametr kształtu jest
stały w czasie", nie „proces jest bez pamięci" (to drugie rozstrzygnięte w Teście 12).

Ustalone wartości (dane rzeczywiste, próg≥3, t0 wykluczone): **k̂=0,709628,
λ̂=6,803500**. Skala MUSI pochodzić z dopasowania do danych, nie być przyjęta z góry —
obciążenie zależy silnie od skali (D-061: −0,045 przy λ=3 wobec −0,125 przy λ=10 na
skali dobranej ad hoc), więc zła skala przesuwa punkt odniesienia całego testu.

Surogaty: dla każdej rzeczywistej obserwacji — jej REALNY rok startu i REALNA granica
administracyjna (2023−rok_startu, fakt egzogeniczny); `T~Weibull(k̂,λ̂)` ciągłe,
dyskretyzacja przez `discretize_gap` (D-058/D-061 — jedyna metoda zgodna ze zmierzonym
obciążeniem na rzeczywistych danych UCDP; `floor` z minimum 1 rok ODRZUCONY, D-061, bo
ignoruje fazę zdarzenia w roku kalendarzowym i daje obciążenie przeciwnego znaku na
zweryfikowanym pomiarze D-056). Zdarzenie pełne jeśli zdyskretyzowane T ≤ admin_max,
inaczej cenzura na admin_max.

B=2000, ziarno=20260823 (potwierdzone przy zamrożeniu). Jeśli frac_tie
(|b_sur−b_obs|<1e-6) > 0,01 — STOP (analogicznie D-026 SS7).

Implementacja: `test13_n3.py`.

## §6. Reguła decyzyjna

Wartość p liczona **względem rozkładu b_sur, NIE względem zera**:

```
p = (1 + #{i : |b_sur_i − center_null| ≥ |b_obs − center_null|}) / (B+1)
```

Jednowarunkowa (single-condition), zgodnie z filozofią efekt-najpierw tego testu:
- p < 0,05 → **wsparty**
- 0,05 ≤ p < 0,10 → **graniczny**
- p ≥ 0,10 → **niewsparty**

Klasyfikacja jest wtórna — zawsze raportowana razem z efektem i przedziałem (§4), nigdy
samodzielnie.

## §7. Trzy wyjaśnienia konkurencyjne (Etap 1 — WYKONANE, D-060)

**A. Ucinanie przez koniec okna 2023.** Zmierzone pod prawdziwie stałym k=0,7096: b̂
średnie −0,1252 (wersja wstępna, skala kalibrowana; wartość finalna po poprawnej skali:
patrz §4/§5, −0,1030). Kierunek UJEMNY — przeciwny do obserwowanego trendu (rosnący k).
**Nie tłumaczy trendu — działa przeciw niemu.** Odrzucone jako kandydat na artefakt
tłumaczący kierunek zjawiska (choć realny mechanizm statystyczny sam w sobie).

**B. Gęstość kodowania.** Silnie rosnąca (14–24 diado-lat/rok w latach 40. → 63–70
obecnie). Mediana odstępu pełnego spada z rzędu 15 do rzędu 1 w oknach pięcioletnich —
ogólnie malejąco, nie ściśle monotonicznie. Opisowe, nie zmierzone jako samodzielnie
wystarczające.

**C. Zmiana składu par.** Pary sprzed 1985: średnio 4,29 epizodu; po 1985: średnio 3,77.
Różnica realna, ale niewielka wobec różnicy k̂ (0,625 vs 0,793) — nie wygląda na
wystarczającą samodzielnie.

**Wniosek: żadne z trzech nie tłumaczy trendu w całości — test orzeka, Etap 1 nie
blokuje.**

## §8. Symulacja mocy i kalibracji (Etap 2 — WYKONANE, D-063/D-064)

Na realnej strukturze, mechanizmem min(T,C), z `discretize_gap`.

**Pomiar 1 (odchylenie pod brakiem trendu):** center_null=−0,1030, SD=0,0425, 95% CI
[−0,196; −0,029] (B=2000, ziarno 20260823).

**Pomiar 2 (udział fałszywych odrzuceń):** N=2000, konstrukcja leave-one-out
(każde ciągnienie potraktowane jako "obserwacja" wobec pozostałych N−1, środek liczony
też z pozostałych — zachowuje wymienność). Wynik: **0,0495** wobec nominalnego 0,05.
Kalibracja potwierdzona empirycznie — porównanie względem środka rozkładu zerowego
poprawne mimo asymetrii rozkładu.

**Pomiar 3 (moc przy trzech wielkościach trendu):** b_true ∈ {0,025; 0,05; 0,10}/dekadę
(środkowa = 0,2 na cztery dekady, cel autora z obserwacji S3 Testu 12; skrajne — połowa
i podwojenie, propozycja Code'a, zaakceptowana). M=500 replik/wielkość, ta sama STAŁA
pula zerowa z pomiaru 1/2 jako odniesienie.

| b_true | b̂ średnie (surowe) | moc |
|---|---|---|
| 0,025 | −0,0874 | 9,4% |
| 0,05 | −0,0614 | 19,6% |
| 0,10 | −0,0120 | 59,8% |

Zgodność z modelem addytywnym artefaktu (§4) potwierdzona: surowe b̂ ≈ b_true +
center_null we wszystkich trzech przypadkach, w granicach szumu Monte Carlo.

**Niska moc (ok. 20% przy trendzie oczekiwanej wielkości) NIE jest powodem
nieuruchamiania testu — wynikiem pierwszorzędnym jest wielkość efektu z przedziałem
(§4), nie sama moc/klasyfikacja.** Konsekwencje interpretacyjne — §9.

## §9. Ograniczenia (zapisane PRZED biegiem, wynikające z mocy ok. 20%)

1. **Wynik nieistotny nic nie powie.** Przy mocy ok. 20% brak odrzucenia jest
   spodziewany nawet przy prawdziwym trendzie wielkości obserwowanej (S3 Testu 12) — nie
   wolno go czytać jako świadectwa przeciw hipotezie. Cztery razy na pięć nie zobaczymy
   trendu, który istnieje.

2. **Wynik istotny będzie znaczył sporo.** Przy dwudziestoprocentowej mocy odrzucenie
   wymaga albo trendu silniejszego niż zakładane 0,05/dekadę, albo szczęścia — to
   pierwsze jest bardziej prawdopodobne. Istotny wynik należy więc czytać jako
   wskazanie na trend WIĘKSZY niż 0,05 na dekadę, nie tylko jako potwierdzenie
   istnienia trendu.

3. **Przedział będzie szeroki i to jest wynik, nie jego brak.** Odchylenie rozkładu
   zerowego (0,0425) daje przedział o szerokości ok. 0,17 — od zera do wartości
   trzykrotnie większej od obserwowanej. Taki przedział wyklucza jedynie trendy bardzo
   duże; to informacja, nie porażka pomiaru.

## §10. Kolejność wykonania i autoryzacje

Etap 1 (§7) — wykonane, D-060. Etap 2 (§8) — wykonane, D-063/D-064. **Etap 3 (to
zamrożenie: numer, ziarno, protokół, kod) — wykonane niniejszym dokumentem.** Etap 4
(bieg — obliczenie `b_obs` na danych rzeczywistych, `test13_run.py`) — **wymaga osobnej,
wyraźnej autoryzacji autora**, nie następuje automatycznie po zamrożeniu.

## §11. Historia zmian względem SZKICU v0.1

- §5: permutacyjny N3 → parametryczny (errata D-062, na żądanie autora).
- §4: dodana definicja wielkości raportowanej jako `b_obs − center_null` z przedziałem
  na SD_null (D-064, formalizacja obserwacji o addytywności artefaktu).
- §9: dodane trzy zdania o konsekwencjach mocy ~20% (D-064, na żądanie autora).
- Dyskretyzacja: `discretize_gap` potwierdzona jako jedyna metoda w całej rodzinie
  (D-061, po zdiagnozowaniu i odrzuceniu `floor` z minimum 1 roku).
