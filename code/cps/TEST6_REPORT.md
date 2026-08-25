# TEST 6 — RAPORT (Etap C: bieg na danych rzeczywistych, rodzina 9)

**Realizuje:** `TASK_6B_BRIEF.md` §7–8 (Krok 3) · **Kod:** `test6_run.py` na `test6_weibull.py`
(pięć usterek naprawionych + D-022) · **Bieg:** 2026-08-24, ziarno `20260823`, B=2000
**Status:** WYNIK — pierwszy policzony rezultat testu w całym projekcie CPS.

---

## 0. Warunek odblokowania — spełniony

Krok 3 był odblokowany warunkowo (D-022): symulacja zapadania θ̂ do granicy na obu
strukturach (Test 6/Test 7) plus licznik `frac_theta_boundary` w bootstrapie — bez
ponownego przeglądu kodu. Oba wykonane i wpisane do rejestru przed tym biegiem.

## 1. Cztery dopasowania — wyniki

| id | model | zbiór (n / diad) | k̂ | profil 95% | bootstrap 95% (B=2000) |
|---|---|---|---|---|---|
| **P1** — ORZEKA | pulowany | główny (63 / 18) | **0,778** | (0,603; 0,979) | (0,647; 0,965) |
| F1 — drugorzędny | kruchość | główny (63 / 18) | 0,778 | (0,603; 0,979) | (0,647; 0,965) |
| S-A | pulowany | epizodowy×kalendarz (63 / 18) | 0,768 | (0,593; 0,970) | (0,642; 0,955) |
| S-B | pulowany | próg surowy×ekspozycja (76 / 25) | 0,784 | (0,615; 0,976) | (0,666; 0,951) |

Wszystkie cztery przedziały (profil i bootstrap, wszystkie warianty) **w pełni ograniczone**
(`bounded=True` po obu stronach — brak przypadku nieosiągniętej granicy siatki, D-022/usterka
1) i **leżą całkowicie poniżej 1** — żaden nie obejmuje wartości `k=1`.

## 2. Wynik pierwszorzędny (P1)

**k̂ = 0,778, CI wyklucza 1 w obu metodach (profil i bootstrap, zgodnie).** Zgodnie
z konwencją rodziny 9/9b konsekwentnie stosowaną od D-012 (i wprost sformułowaną
w `TEST7_PROTOCOL.md` §1 dla rodziny 9b — analogiczna definicja obowiązuje tu):

- `k>1`: ryzyko rośnie z upływem czasu — mechanizm regeneracji.
- `k=1`: ryzyko stałe, proces bez pamięci.
- `k<1`: ryzyko **maleje** z upływem czasu — **grupowanie**, hipoteza konkurencyjna.

Wynik leży jednoznacznie w trzecim reżimie: **im dłużej para nie walczyła, tym MNIEJ, nie
więcej, prawdopodobne stało się wybuchnięcie kolejnej wojny w krótkim czasie.** To jest
kierunek **przeciwny** do mechanizmu regeneracji zakładanego przez H1 oryginalnej tezy —
konflikty w tych 18 diadach grupują się w czasie, zamiast odnawiać się rytmicznie po okresie
„odpoczynku”.

**Zastrzeżenie redakcyjne.** Nie mam w tej chwili przed sobą dosłownego brzmienia reguły
decyzyjnej z `TEST6_PROTOCOL.md` §8 (dokument nie jest zapisany w repo ani w bieżących
załącznikach tej sesji) — powyższy odczyt opiera się na definicji k>1/k<1 konsekwentnie
używanej w całej rodzinie 9/9b (D-012, D-016, `TEST7_PROTOCOL.md` §1), nie na zacytowaniu
oryginalnego protokołu Testu 6. **Proszę o potwierdzenie, że to jest właściwe sformułowanie
werdyktu**, zanim trafi do rozdziału.

## 3. F1 i kruchość (D-022) — nierozstrzygające co do heterogeniczności

θ̂ = 1·10⁻¹⁰ (**na granicy numerycznej**), P1 i F1 dają identyczne k̂ i identyczne przedziały.
Bootstrap: **92,4% replik ma θ̂ na granicy** — daleko powyżej progu „kilkadziesiąt procent”,
przy którym D-022 nakazuje uznać przedział bootstrapowy dla kruchości za nieinterpretowalny.

**Zgodnie z D-022: ta zgodność P1/F1 NIE jest informacją o braku heterogeniczności między
diadami — jest niemożnością jej wykrycia przy 18 grupach.** Pytanie „czy pary różnią się
istotnie tempem, niezależnie od wspólnego kształtu k" pozostaje **nierozstrzygnięte**, nie
odpowiedziane przecząco. Wynik dla k (§2) stoi niezależnie od tego pytania.

## 4. Warianty wrażliwości — zgodne kierunkowo z P1

**S-A (wrażliwość na D-014, kalendarz zamiast ekspozycji):** k̂=0,768, oba CI poniżej 1 —
ten sam wniosek co P1. Korekta ekspozycji (D-014) nie zmienia kierunku wyniku.

**S-B (wrażliwość na D-013, próg surowy — 25 diad zamiast 18, w tym siedem diad
najsilniej zgrupowanych, które próg epizodowy usuwa z głównego zbioru):** k̂=0,784, oba CI
poniżej 1 — **praktycznie identyczne** z P1 (0,784 wobec 0,778). **To rozstrzyga empirycznie
pytanie otwarte od D-013/D-017:** kierunek obciążenia progu epizodowego był tam opisany jako
nieustalony, nie znany. Na tym wyniku okazuje się, że **wybór progu nie zmienia wniosku** —
zarówno z siedmioma najsilniej zgrupowanymi diadami, jak i bez nich, k̂ leży wyraźnie poniżej
1. Zgodnie z regułą D-017 oba warianty są tu raportowane na równi — i zgadzają się.

## 5. Założenia (D-015 A) — potwierdzone jako obowiązujące w tym biegu

1. **Zegar zatrzymany, nie wyzerowany** — odstępy o przerwanej ekspozycji (D-014) wchodzą
   jako suma lat obecności obu stron w systemie, nie jako różnica dat.
2. **Dyskretyzacja** — odstępy w pełnych latach, model ciągły; różnica nie jest korygowana,
   tylko odnotowana jako ograniczenie (istotna przy odstępach minimalnych, tu min. 1 rok).

## 6. Luka nieuzupełniona (D-015, nieistotna dla tego wyniku)

Tekst „czterech przypadków” czytania rozbieżności P1/F1 nigdy nie dotarł do Code'a (D-015,
„zastrzeżenie do uzupełnienia”). W tym biegu jest to bez znaczenia praktycznego: θ̂ leży na
granicy, więc zastosowanie ma wprost D-022 („nierozstrzygające co do heterogeniczności”),
nie żaden z czterech przypadków wymagających tamtego tekstu. Luka pozostaje do uzupełnienia
przed sytuacją, w której θ̂ NIE jest na granicy (np. Etap C Testu 7, gdzie boundary-collapse
jest rzadszy przy 120 grupach — D-022).

## 7. Ograniczenia próby — zgodnie z deklaracją sprzed biegu

18 diad, 45 odstępów pełnych, 18 cenzurowanych (główny zbiór) — mała próba dla estymacji
dwuparametrowej. Szerokość przedziałów (profil ~0,38 szerokości, bootstrap ~0,32) jest
zgodna z oczekiwaniem zapisanym w `test6_weibull.md` przed biegiem (odchylenie k̂ rzędu
0,12–0,13 z testów syntetycznych). **Mimo szerokości, oba przedziały leżą w całości poniżej
1** — to nie jest wynik nierozstrzygający co do kształtu, w przeciwieństwie do pytania
o heterogeniczność (§3).

## 8. Reprodukowalność

`test6_results.csv` (nagłówek `#` JSON: sumy kontrolne trzech plików wejściowych, ziarno
`20260823`, B=2000). Bieg: `python3 test6_run.py` na `test6_intervals.csv`,
`test6_intervals_sensitivity_SA.csv`, `test6_intervals_sensitivity_SB.csv` — wszystkie
z Kroku 1b/1c (D-013, D-014, D-020 nie dotyczy Testu 6). Kod estymatora niezmieniony od
`test6_weibull.py` zatwierdzonego w drugim przeglądzie (`PRZEGLAD2_test6_weibull.md`).

## 9. Status

Wynik dla kształtu k jest **rozstrzygnięty** (§2): k<1, CI wyklucza 1, zgodny kierunkowo
w P1/S-A/S-B. Wynik dla heterogeniczności (θ, F1 wobec P1) jest **nierozstrzygnięty** (§3,
D-022). Czekam na potwierdzenie sformułowania werdyktu wobec `TEST6_PROTOCOL.md` §8 (§2
powyżej) przed przeniesieniem do rozdziału.
