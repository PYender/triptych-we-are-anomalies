# TEST 0B — RAPORT: odtworzenie serii COW i korekta agregacji

**Skrypt:** `test0b_cow_rebuild.py` v1.0
**Wejście:** `InterStateWarData_v4.0.csv`, `Extra-StateWarData_v4.0.csv`,
`Non-StateWarData_v4.0.csv`, `INTRA-STATE WARS v5.1 CSV.csv`
**Wyjście:** `cow_rebuilt.csv` (kolumny `wars_replica`, `wars_fixed`)

---

## 1. Kryterium D1 — spełnione

Replika reguły z `analiza_poprawiona_final_GDELT.py` daje wobec `wars_color.csv`:

```
maks|Δ| = 0.000000
```

Seria bazowa jest **w pełni odtwarzalna z plików surowych**. Pozycja erraty
„brak odtwarzalności serii COW" zostaje zamknięta, a `wars_color.csv` przestaje
być plikiem o nieznanej proweniencji.

Uwaga techniczna: pliki `Inter-`, `Extra-`, `Non-StateWarData` i `COW-country-codes`
mają zakończenia linii **CR** (starszy format Mac). Bez normalizacji pandas czyta
je jako jeden wiersz o tysiącach kolumn. Skrypt to obsługuje.

## 2. Trzy błędy w regule agregacji

### F1 — kod `-7` unieważnia całe wojny, nie tylko ich ogony

COW koduje brakujące dane jako `-7` / `-8` / `-9`, przy czym **`-7` oznacza
„trwa w momencie zamknięcia zbioru"**. Warunek `Start ≤ rok ≤ End` przy `End = -7`
nie zachodzi **nigdy**, więc taka wojna wypada z serii we wszystkich latach —
także tych, w których na pewno trwała.

Dotyczy 25 wierszy: **13 Extra-State** (start 2001–2004: opór afgański i iracki)
oraz **12 Intra-State** (start 1988–2014, długotrwałe wojny domowe).

To nie jest efekt brzegowy. Wojna rozpoczęta w 1988 i trwająca w 2014 nie jest
liczona ani razu, więc zniekształcenie sięga **dwóch ostatnich dekad** serii.

### F2 — kategoria Non-State wnosi dokładnie zero

`load_warfile` wykrywa kolumny `StartYear`/`EndYear`, po czym obcina z nazwy
końcową jedynkę i szuka `StartYear1`/`EndYear1`. Plik Non-State nie ma kolumn
numerowanych fazami, więc lista faz jest pusta, `active_any_phase` zwraca zawsze
`False`, a kategoria — 62 wojny, waga 0,4 — **nie wchodzi do serii w żadnym roku**.

Policzona poprawnie wnosi średnio 0,39 rocznie (ok. 4,6% serii), w 87 latach ze 192.

### F3 — Intra-State pomija fazę 4

Pętla `for k in (1, 2, 3)` ignoruje kolumny `StartYr4`/`EndYr4`, które w v5.1 istnieją.

## 3. Skutek korekty

| | replika | poprawiona |
|---|---|---|
| korelacja obu serii 1816–2007 | — | **0,958** |
| średnia 1816–1990 | 8,40 | 8,82 |
| średnia 1998–2007 | 7,76 | **13,80** |
| rok 2007 | 1,60 | **11,50** |

Do 1990 zmiana jest marginalna. Ostatnie dwie dekady zmieniają się zasadniczo:
rzekomy „zjazd do zera" na końcu serii **znika**.

## 4. Rewizja Testu 0

Diagnoza z Testu 0 („prawostronne cenzurowanie zbioru") była **częściowo błędna**.
Kontrtest na INTRA-STATE v5.1, który sięga 2014 i mógłby pokazać, czy spadek
kończy się na granicy v4.0, dał wynik niejednoznaczny — spadek trwa dalej.
Właściwą przyczyną nie jest cenzurowanie w rozumieniu „brakuje danych po roku X",
tylko **błędna obsługa kodu `-7` w kodzie agregującym**. Dane są w plikach;
kod je odrzucał.

### Konsekwencje

**Odcięcie serii na 2003 jest niepotrzebne.** Po korekcie ogon nie jest zdeformowany
i seria może biec do 2007. Odzyskujemy cztery lata.

**Kalibracja złączenia COW↔UCDP staje się stabilna:**

| okno | replika | poprawiona |
|---|---|---|
| 1946–2007 | 0,811 | 0,895 |
| 1970–2007 | 0,673 | 0,772 |
| 1989–2006 | 0,543 | 0,708 |
| 1997–2007 | 0,463 | 0,799 |
| 2000–2007 | 0,401 | 0,872 |
| **iloraz max/min** | **2,02 → D2 FAIL** | **1,26 → D2 PASS** |

Kryterium D2 przechodzi. **Seria sklejona przestaje być odrzucona** i wraca jako
dopuszczalne wejście do testów formalnych — po przeliczeniu skali na poprawionej serii.

**Kontrast epok utrzymuje się i nieznacznie rośnie** (χ², T = 35,1, MA-11, wartości
orientacyjne — pełne p wymaga bootstrapu):

| | replika | poprawiona |
|---|---|---|
| epoka 1 (1816–1913) | 9,84 | 7,43 |
| epoka 2 (1914–2007) | 46,10 | 39,49 |
| **stosunek** | 4,7 | **5,3** |

Obie statystyki maleją, ale epoka 1 mocniej — więc kontrast, na którym opiera się
teza, jest po korekcie *lepiej* widoczny, nie gorzej.

## 5. Problem otwarty — niejednorodny poziom agregacji

**Nie jest korygowany w tym teście, wymaga decyzji autora.**

| zbiór | wierszy | unikalnych wojen | poziom |
|---|---|---|---|
| Inter-State v4.0 | 337 | 95 | **uczestnik** |
| Extra-State v4.0 | 198 | 163 | **uczestnik** |
| Non-State v4.0 | 62 | 62 | wojna |
| Intra-State v5.1 | 420 | 420 | wojna |

Reguła zlicza wiersze aktywne w danym roku, więc dla dwóch kategorii liczy
**uczestniko-lata**, a dla dwóch — **wojno-lata**. Inter-State jest przez to
zawyżony około 3,5-krotnie względem swojej wagi nominalnej 1,0: wojna
dwudziestostronna waży dwadzieścia razy tyle, co dwustronna.

Rozdział opisuje tę zmienną jako „liczbę wojen". W obecnej postaci jest to
hybryda. Trzy możliwe decyzje:

1. deduplikacja po `WarNum` → wszystko na poziomie wojny (zgodne z opisem);
2. świadome zachowanie uczestników jako miary intensywności → wymaga przepisania
   opisu zmiennej i wag;
3. wariantowo, jako element rodziny testów 4 (odporność na wagi i normalizację).

Rekomendacja: wariant 3 jako test, wariant 1 jako seria kanoniczna — bo tylko on
odpowiada temu, co rozdział deklaruje mierzyć.

## 6. Wpisy do erraty

- **[M]** kod `-7` (wojna trwająca) traktowany jak data → 25 wojen usuniętych z serii w całości;
- **[M]** kategoria Non-State (62 wojny, waga 0,4) nie wchodzi do serii wskutek błędu autodetekcji kolumn;
- **[M]** Intra-State: pominięta faza 4;
- **[M]** seria miesza uczestniko-lata (Inter, Extra) z wojno-latami (Non, Intra), a opisana jest jako „liczba wojen";
- **[S]** diagnoza „cenzurowania ogona" z Testu 0 wymaga przeformułowania na „błąd obsługi kodu braku";
- **[E]** pliki COW mają zakończenia linii CR — do udokumentowania w README, bo psuje wczytywanie.
