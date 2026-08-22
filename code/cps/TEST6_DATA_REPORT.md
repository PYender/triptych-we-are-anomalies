# TEST 6 — RAPORT DANYCH (Etap A: zbiór odstępów między konfliktami)

**Protokół:** `TEST6_PROTOCOL.md` v1.0 (D-012) · **Zadanie:** `TASK_6.md` Etap A · **Data:** 2026-08-22
**Źródło:** `Inter-StateWarData_v4.0.csv` (sha256 `2535e30b…`) · **Builder:** `test6_build_intervals.py`
**Status:** **STOP** — parametr Weibulla nie liczony, kod testu nie pisany. **Pytanie do autora niżej (§6).**

---

## 0. Droga techniczna (§ „Nowa biblioteka")

`lifelines` **nie jest dostępne** w środowisku. Nie instaluję go — w Etapie B
zaimplementuję **MLE Weibulla z cenzurowaniem prawostronnym ręcznie** (`scipy.optimize.minimize`
na log-wiarygodności: obserwacje pełne wnoszą log f(t), cenzurowane log S(t)). Funkcja jest
krótka i nie wymaga nowej zależności.

## 1. Liczby kontrolne — zgodne z §3

| wielkość | wartość | §3 protokołu |
|---|---|---|
| diady ≥3 wspólne konflikty (poziom A) | **25** | 25 ✓ |
| odstępy pełne | **62** | 62 ✓ |
| odstępy cenzurowane (jeden na diadę) | **25** | — (§4) |
| wierszy z kodem `-7` (F1) | 0 | — |

Zbiór `test6_intervals.csv` zawiera **wszystkie 87 wierszy** (62 pełne + 25 cenzurowanych),
nic nie usunięto. Odstępy ujemne/zerowe są **oznaczone** kolumną `flag`, nie odrzucone (§A2).

## 2. Pełna lista diad wchodzących do analizy (wynik progu ≥3, nie doboru)

To jest **wynik kryterium liczbowego**, nie dobór ręczny — tak ma być podpisane (§A3):

Egypt–Israel (5), China–Japan (5), France–China (4), Austria-Hungary–Italy (4),
Greece–Turkey (4), Bulgaria–Romania (4), USSR–Turkey (4), USSR–Japan (4),
Syria–Israel (4), India–Pakistan (4), USA–Vietnam (3), Guatemala–El Salvador (3),
France–Germany (3), France–Bulgaria (3), Spain–Morocco (3), Germany–Yugoslavia (3),
Germany–USSR (3), Italy–Bulgaria (3), Yugoslavia–Bulgaria (3), Yugoslavia–Turkey (3),
Greece–Bulgaria (3), USSR–Finland (3), USSR–China (3), Jordan–Israel (3), Cambodia–Vietnam (3).
*(w nawiasie liczba wspólnych konfliktów; lata konfliktów każdej diady — w `test6_intervals.csv`).*

**Kontrola nazw z rozmowy autora (§A3 — kryterium działa w obie strony):**
- **Rosja–Turcja** → obecna (USSR–Turkey, kody 365–640; 4 konflikty). ✓
- **Niemcy–Francja** → obecna (France–Germany, 255–220; 3 konflikty). ✓
- **Francja–Anglia** (220–200) → **nie wchodzi** — mniej niż 3 wspólne wojny międzypaństwowe COW.
- **Niemcy–Polska** (255–290) → **nie wchodzi** — mniej niż 3 wspólne wojny międzypaństwowe COW.

Dwie z czterech par wymienionych w rozmowie nie spełniają progu i **nie wchodzą** — zgodnie
z zakazem doboru ręcznego odnotowuję to wprost.

## 3. Rozkład odstępów

| rodzaj | n | min | mediana | maks |
|---|---|---|---|---|
| pełne (tylko dodatnie, `flag=ok`) | 51 | 1 | 18 | 81 |
| cenzurowane | 25 | 8 | 62 | 101 |

Cenzurowane są systematycznie długie (mediana 62 lata) — to pary, które po ostatnim
konflikcie **przestały walczyć** (najczęściej po 1945). Pominięcie ich zaniżałoby średni
odstęp i zawyżało pozorną regularność (§4) — dlatego są obowiązkowe.

## 4. Surowe CV i porównanie z §0.2

**CV surowe na odstępach pełnych** (odchylenie/średnia, bez cenzurowania, jak §0.2):
- tylko dodatnie (`flag=ok`, n=51): **0,901**
- wszystkie pełne z ujemnymi/zerowymi (n=62): 1,181

Pulowy CV dodatnich (0,90) mieści się w zakresie §0.2 (0,59–0,95). **Per-państwo moje liczby
są jednak wyższe niż tabela §0.2** — i to jest diagnostyczne:

| państwo | §0.2 (odstępów / CV) | tu (odstępów dodatnich / CV) |
|---|---|---|
| Rosja/ZSRR | 11 / 0,85 | 11* / ~0,85 po odrzuceniu nakładań |
| Turcja | 9 / 0,59 | więcej, CV wyższe |
| Niemcy | 6 / 0,91 | więcej, CV wyższe |

Różnica bierze się z **traktowania odstępów ujemnych/zerowych**: §0.2 najwyraźniej je
**pominęło** (Rosja: 16 wojen → 11 odstępów = 15 kolejnych minus ~4 nakładające się). To
prowadzi wprost do pytania z §6 — i jego rozstrzygnięcie przesądzi, czy per-państwo
odtworzymy tabelę §0.2. **Uwaga:** liczby §0.2 są obserwacją opisową sprzed zamrożenia,
bez modelu zerowego i bez cenzurowania — nie są celem do „trafienia", lecz punktem
odniesienia (§0.2, §5).

## 5. Odstępy według epok (odstępy pełne dodatnie, wg roku końca poprzedniego konfliktu)

| podział | przed | po |
|---|---|---|
| 1914 (→ S5, H6.2) | 23 | 28 |
| 1945 (→ S6, konsolidacja europejska) | 36 | 15 |

## 6. PYTANIE DO ROZSTRZYGNIĘCIA — odstępy ujemne i zerowe (§A2, nie decyduję sam)

Jest **8 odstępów ujemnych i 3 zerowe** (razem 11 z 62 pełnych). Wszystkie pochodzą
z **nakładających się lub jednoczesnych konfliktów** tej samej diady:

| diada | gap | konflikt poprzedni → następny |
|---|---|---|
| China–Japan | −2 | III wojna chińsko-japońska (1937–41) → II wś (1939–45) |
| USSR–China | 0 | Boxer Rebellion (1900) → Sino-Russian (1900) |
| USSR–Japan | 0 | Nomonhan (1939) → II wś (1939–45) |
| Germany–USSR | 0 | I wś (1914–18) → Latvian Liberation (1918–20) |
| USSR–Finland | −1 | Russo-Finnish (1939–40) → II wś (1939–45) |
| Bulgaria–Romania | −6 | II wś → II wś *(Bułgaria zmieniła stronę — ta sama wojna liczona dwa razy)* |
| France–Bulgaria | −6 | II wś → II wś *(j.w.)* |
| Italy–Bulgaria | −6 | II wś → II wś *(j.w.)* |
| USA–Vietnam | −7 | Wojna wietnamska, faza 2 (1965–75) → II wojna laotańska (1968–73) |
| USA–Vietnam | −3 | II wojna laotańska (1968–73) → Communist Coalition (1970–71) |
| Cambodia–Vietnam | −5 | Wojna wietnamska, faza 2 (1965–75) → Communist Coalition (1970–71) |

Trzy typy: (a) **jedna wojna licząca się dwa razy** wskutek zmiany strony (Bułgaria w II wś)
— to raczej artefakt, nie dwa konflikty; (b) **nakładające się różne wojny** (Wietnam,
chińsko-japońska ⊂ II wś); (c) **jednoczesne** (rok 0).

Weibull/analiza przeżycia wymaga czasu oczekiwania **> 0**, więc te 11 nie może wejść jako
surowe wartości. Możliwe drogi (nie rozstrzygam):

1. **Odrzucić** ujemne/zerowe (51 pełnych odstępów) — najprawdopodobniej to zrobiło §0.2;
   traci część danych z okresów intensywnych.
2. **Scalić nakładające się konflikty w jeden epizod** przed liczeniem odstępów (semantyka
   „zegara regeneracji" z §2) — może obniżyć liczbę konfliktów niektórych diad poniżej progu.
3. **Podłoga** (np. 0,5 roku) — zachowuje je jako bardzo krótkie odstępy.

Każda droga zmienia zbiór analizowany i porównanie z §0.2. **Proszę o decyzję przed
finalizacją** — do tego czasu `test6_intervals.csv` zawiera wszystkie odstępy z flagą,
nic nie usunięte.

## 7. STOP

Zbiór odstępów zbudowany i udokumentowany; liczby kontrolne §3 zgodne. **Nie liczę Weibulla,
nie piszę kodu testu.** Czekam na rozstrzygnięcie odstępów ujemnych/zerowych (§6); po nim
sfinalizuję Etap A i przejdę do Etapu B (kod, z sześcioma punktami B1).
