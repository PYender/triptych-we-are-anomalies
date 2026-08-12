# `test2b_disturbance.py` — kod do niezależnej oceny (Etap B, SZKIELET)

Wersja bliźniacza skryptu Testu 2B, wystawiona do przeglądu przed uruchomieniem
(`CPS_OPERATING_BRIEF.md` §5). Ten plik nie jest wykonywany.

**Realizuje:** `TEST2B_PROTOCOL_v2.md` (zamrożony) · lista zdarzeń wg D-007 (34 zdarzenia)
**Status:** szkielet do przeglądu — **nieuruchamiany**; β nie jest jeszcze wynikiem.
**Zależności:** numpy, pandas, matplotlib. Bez `curve_fit` — dopasowanie sinusoidy jest liniowe.

## Na co zwrócić uwagę przy przeglądzie (sześć punktów z TASK_2B §B1)

1. **Detrending raz, na całej serii 1816–2007** (D-004, B1.1) — `compute_reference()`
   liczy detrend na `fit_mask` obejmującej pełny zakres; podokres (Q1/Q2/Q3) wybiera
   tylko lata do regresji β, nie do detrendingu.
2. **Sinusoida o ustalonym T; tylko amplituda i faza** (B1.2) — `fit_cycle()` używa
   liniowych najmniejszych kwadratów w bazie [cos, sin]; `curve_fit` nie występuje.
   Sinusoida jest układem odniesienia, nie testem (zakaz nr 1).
3. **S(t) całkowitoliczbowa, nie binarna** (B1.3) — `intensity()` sumuje wskaźniki
   okien; to jedyna różnica wobec v1.0.
4. **Przesunięcie cykliczne wyczerpujące, p dokładne, bez ziarna** (B1.4) —
   `shift_null()` przechodzi k=1…n−1, β liczone dla każdego przesunięcia.
5. **Bez błędów standardowych OLS** (B1.5) — `beta_slope()` zwraca wyłącznie β;
   istotność liczona tylko z rozkładu przesunięć.
6. **S3 usuwa lata wojen PRZED dopasowaniem** (B1.6) — `fit_mask` wyklucza
   1914–1918 i 1939–1945, więc detrend i sinusoida są liczone bez nich; czas liczony
   w latach (nie indeksie), żeby luki były respektowane.

## Punkty otwarte, zgłoszone do rozstrzygnięcia w przeglądzie

- **Efekt brzegowy** (parametr `include_prewindow`, domyślnie `True`): czy S(t)
  w oknie 1900–2007 ma być zasilana przez zdarzenie sprzed okna — jedyny przypadek
  to VI pandemia cholery 1899, rzucająca cień na 1900–1903. Domyślnie tak (globalna
  definicja S z §3); do potwierdzenia.
- **S6 (COLOR) i T1 (relacja W:P przed/po 1945)** nie są zaimplementowane — brak
  wpiętej serii COLOR i rozbicia międzypaństwowego. Zwracają wiersz-zaślepkę,
  żeby nie podać fałszywej liczby. Do uzupełnienia po przeglądzie.
- **Przesunięcie po pozycjach przy lukach (S3):** `np.roll` działa na wektorze
  zachowanych lat; przy niecięgłych latach S3 jest to przesunięcie pozycyjne — do
  potwierdzenia jako zgodne z intencją nulla.

## Kod

```python
#!/usr/bin/env python3
"""
TEST 2B — natężenie zaburzeń a odchylenie od rytmu (model 2, rodzina 8).
Realizuje TEST2B_PROTOCOL_v2.md (zamrożony 11.08.2026). Lista zdarzeń: D-007.

SZKIELET DO PRZEGLĄDU — Etap B. NIE uruchamiać przed przeglądem autora (TASK_2B §B1).
β nie jest wynikiem, dopóki lista i ten kod nie przejdą przeglądu.

Sześć punktów, na których ten test typowo się psuje (TASK_2B §B1) — jak są tu
rozwiązane:
  1. Detrending liczony RAZ, na całej serii 1816–2007 (D-004), nie w podokresach.
     -> compute_reference(): detrend na fit_mask = pełny zakres; podokres tylko
        wybiera lata do regresji β, nie do detrendingu.
  2. Sinusoida o USTALONYM T; estymowane wyłącznie amplituda i faza. `curve_fit`
     NIE występuje — dopasowanie jest liniowe w bazie [cos, sin] (2 parametry),
     więc jest to układ odniesienia, nie test (zakaz nr 1).
  3. S(t) jest CAŁKOWITOLICZBOWA (liczba zdarzeń w cieniu), nie binarna — to cała
     różnica wobec v1.0. -> intensity() sumuje wskaźniki okien, bez binaryzacji.
  4. Przesunięcie cykliczne S(t) względem d(t) jest WYCZERPUJĄCE (k = 1…n−1),
     β liczone dla każdego przesunięcia; p dokładne, BEZ ziarna losowego.
     -> shift_null(): np.roll po pozycjach, pełny przebieg.
  5. Błędy standardowe OLS NIE są raportowane (reszty autoskorelowane); istotność
     wyłącznie z rozkładu przesunięć. -> zwracamy β_obs, percentyl 5 nulla, p.
  6. W S3 (bez 1914–1918 i 1939–1945) lata usuwane są z OBU szeregów PRZED
     dopasowaniem sinusoidy, nie po. -> fit_mask wyklucza te lata, więc detrend
     i sinusoida są liczone na serii bez nich; czas liczony w LATACH (nie indeksie),
     żeby luki były respektowane.

Punkty do potwierdzenia w przeglądzie (oznaczone FLAG w kodzie):
  - efekt brzegowy: czy S(t) w oknie 1900–2007 ma zasilać zdarzenie sprzed okna
    (VI pandemia cholery 1899 rzuca cień na 1900–1903). Domyślnie: tak (globalna
    definicja S z §3). Parametr include_prewindow.
  - S6 (COLOR) i T1 (relacja W:P) nie są jeszcze zaimplementowane — brak wpiętej
    serii COLOR / rozbicia międzypaństwowego; zwracają wiersz-zaślepkę.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

VERSION = "test2b_disturbance.py v0.1 (szkielet do przeglądu)"

# --- parametry zamrożone w protokole v2.0; NIE zmieniać bez nowego protokołu ----
T_HYP = 35.1                       # ustalony okres (Tryptyk s. 73; D-005) [lata]
T_ALT = (32.0, 40.0)               # wariant S2
Y_FULL = (1816, 2007)              # zakres detrendingu i dopasowania (D-004, B1.1)
Y_PRIMARY = (1900, 2007)           # podokres pierwszorzędny (jakość katalogów)
Y_PRE = (1816, 1899)               # podokres opisowy
WAR_YEARS = set(range(1914, 1919)) | set(range(1939, 1946))   # S3 (B1.6)
L_RECT = 5                         # zanik prostokątny w(k)=1 dla k∈{0..4}
EXP_TAU, EXP_KMAX = 3.0, 9         # zanik wykładniczy exp(-k/3), k≤9 (S1)
CATEGORIES = ("earthquake", "pandemic", "enso", "volcano")     # po D-007
# -------------------------------------------------------------------------------


# ============================ przygotowanie serii ============================
def load_series(data_path: Path, variant: str) -> pd.Series:
    df = pd.read_csv(data_path, comment="#")
    s = (df[df.variant == variant].set_index("year")["value"].sort_index())
    return s.loc[Y_FULL[0]:Y_FULL[1]]


def load_events(events_path: Path) -> pd.DataFrame:
    """Lista finalna: wiersze o statusie != removed (D-007)."""
    df = pd.read_csv(events_path, comment="#")
    keep = df[df.verification_status != "removed"].copy()
    return keep[["event_id", "category", "year"]].reset_index(drop=True)


def linear_detrend_years(years: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Detrending liniowy względem CZASU W LATACH (nie indeksie), żeby luki
    po wykluczeniu lat (S3, B1.6) były respektowane."""
    a = np.polyfit(years.astype(float), x, 1)
    return x - np.polyval(a, years.astype(float))


def fit_cycle(years: np.ndarray, y: np.ndarray, T: float) -> tuple[np.ndarray, float]:
    """Sinusoida o USTALONYM T; estymowane amplituda i faza (2 parametry) przez
    liniowe najmniejsze kwadraty w bazie [cos, sin]. `curve_fit` nie występuje —
    to jest układ odniesienia, nie test (zakaz nr 1, B1.2)."""
    w = 2.0 * np.pi / T
    M = np.column_stack([np.cos(w * years), np.sin(w * years)])
    coef, *_ = np.linalg.lstsq(M, y, rcond=None)
    cycle = M @ coef
    amp = float(np.hypot(coef[0], coef[1]))
    return cycle, amp


def compute_reference(series: pd.Series, T: float, fit_mask: np.ndarray):
    """Zwraca d(t) na latach fit_mask: detrend (raz, B1.1) + odjęcie sinusoidy.
    d(t) = obserwacja_po_detrendingu(t) − przewidywanie cyklu(t)  (§2)."""
    years = series.index.to_numpy()
    vals = series.to_numpy(float)
    fy, fv = years[fit_mask], vals[fit_mask]
    fv_dt = linear_detrend_years(fy, fv)
    cycle, amp = fit_cycle(fy, fv_dt, T)
    d = fv_dt - cycle
    return pd.Series(d, index=fy), amp, pd.Series(fv_dt, index=fy), pd.Series(cycle, index=fy)


# ============================ natężenie zaburzeń ============================
def intensity(years: np.ndarray, event_years, decay: str) -> np.ndarray:
    """S(t) całkowita/ważona (B1.3). decay='rect' -> w(k)=1 dla k∈{0..4};
    decay='exp' -> w(k)=exp(-k/3) dla k≤9. Sumuje po WSZYSTKICH podanych zdarzeniach
    (globalna definicja §3; sterowanie zdarzeniami sprzed okna po stronie wywołania)."""
    S = np.zeros(len(years), dtype=float)
    yidx = {int(y): i for i, y in enumerate(years)}
    for e in event_years:
        if decay == "rect":
            ks = range(0, L_RECT)
            wk = [1.0] * L_RECT
        elif decay == "exp":
            ks = range(0, EXP_KMAX + 1)
            wk = [np.exp(-k / EXP_TAU) for k in ks]
        else:
            raise ValueError(decay)
        for k, w in zip(ks, wk):
            i = yidx.get(int(e) + k)
            if i is not None:
                S[i] += w
    return S


# ============================ statystyka i null ============================
def beta_slope(S: np.ndarray, d: np.ndarray) -> float:
    """β z regresji d = α + β·S. Zwraca WYŁĄCZNIE β (bez błędu standardowego, B1.5)."""
    Sc = S - S.mean()
    var = np.dot(Sc, Sc)
    if var == 0:
        return np.nan
    return float(np.dot(Sc, d - d.mean()) / var)


def shift_null(S: np.ndarray, d: np.ndarray, beta_obs: float):
    """Wyczerpujące przesunięcie cykliczne (B1.4): S przesuwane o k=1…n−1 pozycji
    względem d, β liczone dla każdego k. p dokładne, bez ziarna.
        p = (1 + #{β_przesunięte ≤ β_obs}) / n
    """
    n = len(S)
    betas = np.array([beta_slope(np.roll(S, k), d) for k in range(1, n)])
    p = (1 + int(np.sum(betas <= beta_obs))) / n
    pct5 = float(np.percentile(betas, 5))
    return betas, p, pct5


# ============================ silnik uruchomienia ============================
def analysis_mask(years: np.ndarray, y0: int, y1: int, drop_wars: bool) -> np.ndarray:
    m = (years >= y0) & (years <= y1)
    if drop_wars:
        m &= np.array([int(y) not in WAR_YEARS for y in years])
    return m


def run_variant(spec: dict, events: pd.DataFrame, series_cache: dict,
                include_prewindow: bool = True) -> dict:
    if spec.get("stub"):
        return {"id": spec["id"], "podokres": spec.get("okno", "-"), "n": None,
                "zanik": "-", "T": "-", "beta_obs": None, "null_p05": None,
                "p": None, "decyzja": spec["stub"]}

    variant = spec["variant"]
    series = series_cache[variant]
    years_all = series.index.to_numpy()
    T = spec["T"]
    drop_wars = spec.get("drop_wars", False)

    # fit_mask: pełny zakres 1816–2007 (B1.1); S3 wyklucza lata wojen PRZED fitem (B1.6)
    fit_mask = np.ones(len(years_all), dtype=bool)
    if drop_wars:
        fit_mask &= np.array([int(y) not in WAR_YEARS for y in years_all])

    d_full, amp, _, _ = compute_reference(series, T, fit_mask)

    # podokres analizy (do regresji β i nulla)
    a_mask = analysis_mask(d_full.index.to_numpy(), spec["y0"], spec["y1"], drop_wars)
    a_years = d_full.index.to_numpy()[a_mask]
    d = d_full.to_numpy()[a_mask]

    # zdarzenia: kategoria (S5) lub wszystkie
    ev = events if spec.get("category") is None else events[events.category == spec["category"]]
    ev_years = ev.year.tolist()
    if not include_prewindow:
        ev_years = [e for e in ev_years if spec["y0"] <= e <= spec["y1"]]

    S = intensity(a_years, ev_years, spec["decay"])
    beta_obs = beta_slope(S, d)
    betas, p, pct5 = shift_null(S, d, beta_obs)

    return {"id": spec["id"], "podokres": f"{spec['y0']}-{spec['y1']}", "n": int(len(a_years)),
            "zanik": spec["decay"], "T": T, "beta_obs": round(beta_obs, 6),
            "null_p05": round(pct5, 6), "p": round(p, 4),
            "decyzja": verdict(spec["id"], beta_obs, p),
            "_betas": betas, "_S": S, "_d": d, "_amp": amp}


def verdict(rid: str, beta: float, p: float) -> str:
    """Orzeka wyłącznie Q1 (§8). Pozytywny Q1 wymaga dodatkowo S3 (znak) i S5
    (nie jedna kategoria) — sprawdzane w main(), nie tutaj."""
    if rid == "Q1":
        ok = (beta < 0) and (p < 0.05)
        return f"ORZEKA — β<0 i p<0,05 {'SPEŁNIONE' if ok else 'NIESPEŁNIONE'} (warunkowo od S3/S5)"
    return "opisowy — nie orzeka"


def build_specs() -> list[dict]:
    """Pre-rejestrowana lista uruchomień z §7 protokołu v2.0."""
    base = dict(variant="A_COW_W", T=T_HYP, decay="rect")
    S = [
        dict(id="Q1", y0=1900, y1=2007, **base),
        dict(id="Q2", y0=1816, y1=1899, **base),
        dict(id="Q3", y0=1816, y1=2007, **base),
        dict(id="S1", y0=1900, y1=2007, **{**base, "decay": "exp"}),
        dict(id="S2_T32", y0=1900, y1=2007, **{**base, "T": T_ALT[0]}),
        dict(id="S2_T40", y0=1900, y1=2007, **{**base, "T": T_ALT[1]}),
        dict(id="S3", y0=1900, y1=2007, drop_wars=True, **base),
        dict(id="S4", y0=1900, y1=2007, **{**base, "variant": "A_COW_P"}),
    ]
    for c in CATEGORIES:
        S.append(dict(id=f"S5_{c}", y0=1900, y1=2007, category=c, **base))
    # S6 i T1: jeszcze niezaimplementowane — wymagają dodatkowych danych
    S.append(dict(id="S6", stub="NIEZAIMPLEMENTOWANY — wymaga wpiętej serii COLOR (d vs COLOR, §7)"))
    S.append(dict(id="T1", stub="NIEZAIMPLEMENTOWANY — inna statystyka: udział wojen międzypaństwowych i relacja A_COW_W:A_COW_P przed/po 1945 (v1.0 §3a)"))
    return S


# ================================== wykresy ==================================
def diagnostics(rows: list[dict], series_cache: dict, out: Path):
    """Cztery panele §10 protokołu. (Szkielet — do uzupełnienia po przeglądzie.)"""
    q1 = next((r for r in rows if r["id"] == "Q1"), None)
    with PdfPages(out) as pdf:
        # Panel 1: seria z sinusoidą
        s = series_cache["A_COW_W"]
        years = s.index.to_numpy()
        _, amp, fv_dt, cycle = compute_reference(s, T_HYP, np.ones(len(years), bool))
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(fv_dt.index, fv_dt.values, lw=1, label="A_COW_W po detrendingu")
        ax.plot(cycle.index, cycle.values, lw=1.5, c="crimson",
                label=f"sinusoida T={T_HYP} (amp={amp:.2f}) — układ odniesienia")
        ax.axvline(1914, ls="--", c="k", lw=1); ax.legend(); ax.grid(alpha=.3)
        ax.set_title("Panel 1. Seria po detrendingu i sinusoida odniesienia (§2)")
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)

        # Panel 2: d(t) i S(t) na wspólnej osi
        if q1 is not None:
            yrs = np.arange(Y_PRIMARY[0], Y_PRIMARY[1] + 1)
            fig, ax1 = plt.subplots(figsize=(11, 4))
            ax1.plot(yrs, q1["_d"], lw=1, label="d(t)")
            ax2 = ax1.twinx(); ax2.step(yrs, q1["_S"], where="mid", c="darkorange", lw=1, label="S(t)")
            ax1.set_ylabel("d(t)"); ax2.set_ylabel("S(t)")
            ax1.set_title("Panel 2. Odchylenie d(t) i natężenie S(t), 1900–2007 (Q1)")
            ax1.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)

            # Panel 3: rozkład β po przesunięciach z wartością obserwowaną
            fig, ax = plt.subplots(figsize=(11, 4))
            ax.hist(q1["_betas"], bins=40, color="steelblue", alpha=.75)
            ax.axvline(q1["beta_obs"], c="crimson", lw=2, label=f"β_obs = {q1['beta_obs']:.4f}")
            ax.axvline(q1["null_p05"], c="k", ls="--", lw=1, label="5. percentyl nulla")
            ax.set_title(f"Panel 3. Rozkład β po wszystkich przesunięciach, Q1 (p={q1['p']:.4f})")
            ax.legend(); ax.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)

        # Panel 4: β osobno dla kategorii (S5)
        cat_rows = [r for r in rows if r["id"].startswith("S5_")]
        if cat_rows:
            fig, ax = plt.subplots(figsize=(11, 4))
            labels = [r["id"].replace("S5_", "") for r in cat_rows]
            ax.bar(labels, [r["beta_obs"] for r in cat_rows], color="slategray")
            ax.axhline(0, c="k", lw=.8)
            ax.set_title("Panel 4. β osobno dla każdej kategorii (S5) — czy efekt nie jest z jednej")
            ax.grid(alpha=.3, axis="y"); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="cps_canonical_v2.csv")
    ap.add_argument("--events", default="test2b_events.csv")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--include-prewindow", action="store_true", default=True,
                    help="czy zdarzenia sprzed okna zasilają S(t) w oknie (FLAG do przeglądu)")
    a = ap.parse_args()
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)

    events = load_events(Path(a.events))
    series_cache = {v: load_series(Path(a.data), v) for v in ("A_COW_W", "A_COW_P")}

    rows = [run_variant(s, events, series_cache, a.include_prewindow) for s in build_specs()]
    res = pd.DataFrame([{k: v for k, v in r.items() if not k.startswith("_")} for r in rows])

    meta = {"script": VERSION, "T_hyp": T_HYP, "n_events": int(len(events)),
            "sha256_data": hashlib.sha256(Path(a.data).read_bytes()).hexdigest()[:16],
            "sha256_events": hashlib.sha256(Path(a.events).read_bytes()).hexdigest()[:16],
            "null": "wyczerpujące przesunięcie cykliczne, p dokładne, bez ziarna"}
    with open(out / "test2b_results.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        res.to_csv(fh, index=False)
    diagnostics(rows, series_cache, out / "test2b_diagnostics.pdf")

    print(res.to_string(index=False))
    # Reguła §8: orzeka wyłącznie Q1; pozytywny wymaga S3 (znak) i S5 (nie jedna kategoria)
    def g(i): return next((r for r in rows if r["id"] == i), None)
    q1, s3 = g("Q1"), g("S3")
    s5 = [g(f"S5_{c}") for c in CATEGORIES]
    q1_ok = q1 and (q1["beta_obs"] < 0) and (q1["p"] < 0.05)
    s3_ok = s3 and (np.sign(s3["beta_obs"]) == np.sign(q1["beta_obs"]))
    s5_neg = sum(1 for r in s5 if r and r["beta_obs"] < 0)
    print(f"\nREGUŁA §8: Q1 β={q1['beta_obs']} p={q1['p']} | "
          f"S3 znak {'zgodny' if s3_ok else 'ODWRÓCONY'} | "
          f"S5: {s5_neg}/4 kategorii z β<0")
    print("WYNIK: " + ("POZYTYWNY (warunkowy)" if (q1_ok and s3_ok and s5_neg >= 2)
                       else "NEGATYWNY / NIEJEDNOZNACZNY"))
    print("Orzeka wyłącznie Q1. Wariant S6 i T1 wymagają uzupełnienia danych.")


if __name__ == "__main__":
    main()
```
