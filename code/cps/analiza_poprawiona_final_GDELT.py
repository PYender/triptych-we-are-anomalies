# analiza_poprawiona_final_GDELT.py – version: ARIMAX_1.1.1_COLOR_v1, date: 2025-08-05 (mw-0 … mw-13)
# Source: Triptych "We are Anomal(i)es" v0.1 by Mariusz Włodarczyk
# Segment: III.3.2. OPERATIONAL VALIDATOR – OPERATIONALIZATION OF THE GLOBAL "WAR-PEACE" CYCLE
# – CYCLE PREDICTION SENTINEL (CPS)
# License: CC BY-NC-SA 4.0

import gzip
from pathlib import Path
from functools import lru_cache
import re
import time
import pickle
import collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import periodogram, detrend
from scipy.optimize import curve_fit
from statsmodels.tsa.arima.model import ARIMA
from tqdm.auto import tqdm

# -------------------------------------------------------------------------
# 0. GLOBAL YEARLY TOKEN COUNTER (mw-0)
# -------------------------------------------------------------------------
from collections import defaultdict
# if not yet imported
TOTAL_YEAR_CNT = defaultdict(int)  # <- before INIT of 1-grams

# -------------------------------------------------------------------------
# 1. PATHS (mw-1)
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.resolve()  # directory of analiza_poprawiona_final_GDELT.py
DATA = BASE_DIR       # CSV + GDELT + .gz live here
NGRAM_DIR = DATA      # .gz files are not in a separate folder

# -------------------------------------------------------------------------
# 2. WORD LISTS (mw-2)
# -------------------------------------------------------------------------
RED_WORDS = [
    "war", "enemy", "conquer", "attack", "strike", "dominate",
    "battle", "conflict", "invasion", "hostility"
]
BLUE_WORDS = [
    "peace", "trust", "cooperation", "cultivate", "innovate",
    "harmony", "diplomacy", "alliance", "treaty", "reconciliation"
]
TARGET_WORDS = set(RED_WORDS) | set(BLUE_WORDS)

# -------------------------------------------------------------------------
# 3. N-GRAMS (mw-3, improved parser + cache)
# -------------------------------------------------------------------------
import atexit

# —— 3A. PREPROCESS 1-GRAMS → pickle (runs only once) ——
NGRAM_STAMP = "20120701"   # (kept)
DATA_DIR    = Path(__file__).parent
CACHE_DIR   = DATA_DIR / "_pkl"
CACHE_DIR.mkdir(exist_ok=True)
SMOOTH_WIN  = 11           # smoothing window in years


def precompute_letter(letter: str):
    """
    Parses the 1-gram file for a single letter and updates:
    • counts         – number of tokens for that letter per year
    • TOTAL_YEAR_CNT – total number of tokens (all letters) per year
    • wordcnt        – tokens of TARGET_WORDS per year
    """
    import re, time, gzip, collections, pickle

    # --- CACHE: if pickle already exists, load instead of parsing .gz
    pkl = CACHE_DIR / f"{letter}.pkl"
    if pkl.exists():
        with pkl.open("rb") as fh:
            counts, wordcnt = pickle.load(fh)
        # reconstruct the global token counter so that the 'color' index works
        for yr, cnt in counts.items():
            TOTAL_YEAR_CNT[yr] += cnt
        _LETTER_CACHE[letter] = (counts, wordcnt)  # keep in memory
        return counts, wordcnt

    # --- if pickle is missing, continue and parse the .gz file ---
    t0     = time.time()
    counts  = collections.defaultdict(int)                              # year → total tokens
    wordcnt = collections.defaultdict(lambda: collections.Counter())

    fname = DATA_DIR / f"googlebooks-eng-all-1gram-{NGRAM_STAMP}-{letter}.gz"
    if not fname.exists():
        raise FileNotFoundError(fname)

    with gzip.open(fname, "rt", encoding="utf-8", errors="ignore") as f:
        for ln, line in enumerate(f, 1):
            # split by comma, tab or multiple spaces
            parts = re.split(r"[,\t\s]+", line.strip())
            if len(parts) < 3:
                continue
            tok_raw, yr, cnt = parts[:3]
            try:
                yr  = int(yr)
                cnt = int(cnt)
            except ValueError:
                if ln <= 3:
                    continue
            tok              = tok_raw.split("_")[0].lower().strip('"\'')
            counts[yr]       += cnt
            TOTAL_YEAR_CNT[yr] += cnt
            if tok in TARGET_WORDS:
                wordcnt[yr][tok] += cnt

    # write to pickle (cache)
    pkl = CACHE_DIR / f"{letter}.pkl"
    with pkl.open("wb") as fh:
        pickle.dump((dict(counts), {y: dict(c) for y, c in wordcnt.items()}), fh)
    print(f" ► preprocessed {letter} in {time.time()-t0:.1f}s")
    return counts, wordcnt


_LETTER_CACHE = {}   # letter → (counts, wordcnt)


def _ensure_letter(letter: str):
    if letter not in _LETTER_CACHE:
        _LETTER_CACHE[letter] = precompute_letter(letter)
    return _LETTER_CACHE[letter]


@atexit.register   # save cache on exit
def _save_cache():
    for letter, data in _LETTER_CACHE.items():
        pkl = CACHE_DIR / f"{letter}.pkl"
        if not pkl.exists():
            with pkl.open("wb") as fh:
                pickle.dump(data, fh)


# -------------------------------------------------------------------------
# total number of tokens for a letter in a given year
# -------------------------------------------------------------------------
@lru_cache(maxsize=None)
def total_tokens_letter_year(letter: str, year: int) -> int:
    counts, _ = _ensure_letter(letter)
    return counts.get(year, 0)


# -------------------------------------------------------------------------
# helper: total number of tokens (all letters) in a given year
# -------------------------------------------------------------------------
@lru_cache(maxsize=None)
def year_total_tokens(year: int) -> int:
    return TOTAL_YEAR_CNT.get(year, 0)


# -------------------------------------------------------------------------
# frequency of a specific word in a given year (also cached)
# -------------------------------------------------------------------------
@lru_cache(maxsize=None)
def ngram_freq(word: str, year: int) -> float:
    letter = word[0].lower()
    counts, wordcnt = _ensure_letter(letter)
    total = year_total_tokens(year)   # PATCH 1D – global denominator
    if total == 0:
        return 0.0
    return wordcnt.get(year, {}).get(word, 0) / total


# -------------------------------------------------------------------------
# [INIT] load only those 1-gram letters for which .gz files exist
# -------------------------------------------------------------------------
from string import ascii_lowercase
AVAILABLE = {p.name.split("-")[-1][0]    # letter from file name
             for p in Path.cwd().glob("googlebooks-eng-all-1gram-*.gz")}
REQUIRED  = {w[0].lower() for w in TARGET_WORDS}
TO_LOAD   = REQUIRED & AVAILABLE

missing = REQUIRED - AVAILABLE
if missing:
    print("⚠ missing 1-gram files for letters:", ",".join(sorted(missing)))
for ch in TO_LOAD:
    precompute_letter(ch)

# -------------------------------------------------------------------------
# 4. WARS + POPULATION (mw-4)
# -------------------------------------------------------------------------
YEARS = list(range(1816, 2008))


def load_warfile(filename: str, start_hint: str, end_hint: str, weight: float):
    """
    Returns a list [len(YEARS)]: number of ongoing wars in a given year × weight.
    Automatically detects start/end columns, accepting both 'Year' and 'Yr'.
    """
    w = pd.read_csv(DATA / filename, encoding="latin-1")

    # --- automatic matching of start / end columns -------------------------
    if start_hint not in w.columns or end_hint not in w.columns:
        def is_year_col(col: str, kind: str):
            c = col.lower()
            return c.startswith(kind) and ("year" in c or "yr" in c)
        start_candidates = [c for c in w.columns if is_year_col(c, "start")]
        end_candidates   = [c for c in w.columns if is_year_col(c, "end")]
        for s in start_candidates:
            suffix = s.lower().replace("start", "")
            match  = [e for e in end_candidates
                      if e.lower().replace("end", "") == suffix]
            if match:
                start_hint, end_hint = s, match[0]
                break
        else:
            raise KeyError(
                f"{filename}: missing date columns; fields: {list(w.columns)[:15]}"
            )

    # ---------------------------------------------------------------------
    # PATCH 3B – counts ALL phases (1 · 2 · 3) of the same war
    base_start = start_hint.rstrip("1")   # e.g., 'StartYear'
    base_end   = end_hint.rstrip("1")     # e.g., 'EndYear'

    # build a list of (start_k, end_k) for all phases that exist in the file
    phase_cols = []
    for k in (1, 2, 3):
        s = f"{base_start}{k}"
        e = f"{base_end}{k}"
        if s in w.columns and e in w.columns:
            phase_cols.append((s, e))

    def active_any_phase(row, year):
        return any(
            pd.notna(row[s]) and pd.notna(row[e]) and (row[s] <= year <= row[e])
            for (s, e) in phase_cols
        )

    return [
        weight * w.apply(active_any_phase, axis=1, year=y).sum()
        for y in YEARS
    ]


# Inter-State (v4.0)
war_main = pd.read_csv(DATA / "Inter-StateWarData_v4.0.csv", encoding="latin-1")

### ⬇ PATCH 3A – Inter-State with phase 2
war_int = pd.read_csv(DATA / "Inter-StateWarData_v4.0.csv", encoding="latin-1")

def active_in_year(row, y):
    def _in(s, e):
        return pd.notna(s) and pd.notna(e) and (s <= y <= e)
    return _in(row["StartYear1"], row["EndYear1"]) or \
           _in(row.get("StartYear2"), row.get("EndYear2"))

wars_inter = [
    war_int.apply(active_in_year, axis=1, y=yr).sum()
    for yr in YEARS
]
### ⬆ END PATCH 3A

# Extra-, Non-, Intra-State
wars_extra = load_warfile("Extra-StateWarData_v4.0.csv",  "StartYear1", "EndYear1", 0.7)
wars_non   = load_warfile("Non-StateWarData_v4.0.csv",    "StartYear1", "EndYear1", 0.4)
wars_intra = load_warfile("INTRA-STATE WARS v5.1 CSV.csv","StartYr1",   "EndYr1",   0.4)

# World population
pop_raw = pd.read_csv(DATA / "population.csv")
pop = pop_raw[pop_raw["Entity"] == "World"][["Year", "Population (historical)"]]
pop.columns = ["year", "pop"]

# Combined dataframe
df = pd.DataFrame({
    "year": YEARS,
    "wars": (np.array(wars_inter)
             + np.array(wars_extra)
             + np.array(wars_non)
             + np.array(wars_intra)),
}).merge(pop, how="left")

# --- per capita -----------------------------------------------------------
df["wars_pc"]        = df["wars"] / df["pop"]   # wars / population
df["wars_pc_smooth"] = (
    df["wars_pc"].rolling(SMOOTH_WIN, center=True, min_periods=1).mean()
)

# -------------------------------------------------------------------------
# 5. GDELT (mw-5) – 17-column Reduced V2
# -------------------------------------------------------------------------
gdelt_file    = DATA / "GDELT.MASTERREDUCEDV2.txt"
idx_date      = 0   # Date (YYYYMMDD)
idx_eventcode = 3   # CAMEOCode
idx_goldstein = 7   # GoldsteinScale from Events DB (this is NOT GKG Tone)
usecols       = [idx_date, idx_eventcode, idx_goldstein]

wars_gdelt = {y: 0   for y in YEARS}
gold_sum   = {y: 0.0 for y in YEARS}
gold_n     = {y: 0   for y in YEARS}

for chunk in pd.read_csv(
        gdelt_file,
        sep="\t",
        header=0,
        usecols=usecols,
        dtype="string",
        chunksize=400_000,
        low_memory=False,
        encoding="utf-8",
        on_bad_lines="skip"):

    # unambiguous column labels
    chunk.columns = ["SQLDATE", "CAMEOCode", "GoldsteinScale"]

    # conversions; "---" → NaN
    chunk["CAMEOCode"]     = pd.to_numeric(chunk["CAMEOCode"],     errors="coerce")
    chunk["GoldsteinScale"]= pd.to_numeric(chunk["GoldsteinScale"],errors="coerce")

    years  = (chunk["SQLDATE"].astype("Int64") // 10_000).astype(int)
    # root-code :: 18 = Assault, 19 = Fight, 20 = UMV
    is_war = (chunk["CAMEOCode"].fillna(0).astype(int) // 10).isin([18, 19, 20])

    for y, flag, g in zip(years, is_war, chunk["GoldsteinScale"].fillna(0.0)):
        if y in wars_gdelt:
            if flag:
                wars_gdelt[y] += 1
            gold_sum[y] += float(g)
            gold_n[y]   += 1

gdelt_wars      = [wars_gdelt[y] for y in YEARS]
gdelt_goldstein = [(gold_sum[y] / gold_n[y]) if gold_n[y] else np.nan
                   for y in YEARS]

df["gdelt_wars"]      = gdelt_wars
df["gdelt_goldstein"] = gdelt_goldstein

# -------------------------------------------------------------------------
# 6. COLOR INDEX (mw-6)
# -------------------------------------------------------------------------
def color_index(y: int) -> float:
    red  = sum(ngram_freq(w, y) for w in RED_WORDS)
    blue = sum(ngram_freq(w, y) for w in BLUE_WORDS)
    return (blue - red) / (blue + red + 1e-9)

# compute the index for each year …
df["color"] = [color_index(y) for y in tqdm(df.year, desc="indeks color")]

# ─── DIAGNOSTICS (temporary) ───
print("\n► COLOR – first and last year:",
      df['color'].iloc[0], df['color'].iloc[-1])
print("► MIN, MAX, STD:",
      df['color'].min(), df['color'].max(), df['color'].std())
print("► Example components 1950:",
      {w: ngram_freq(w, 1950) for w in ['war', 'peace']})

# -------------------------------------------------------------------------
# 7. 11-YEAR SMOOTHING (mw-7) + fill gaps in the color index
# -------------------------------------------------------------------------
df["wars_smooth"] = (
    df["wars"].rolling(SMOOTH_WIN, center=True, min_periods=1).mean()
)

# remove single NaNs in color (at edges of years with missing n-grams)
if "color" in df.columns:
    df["color"] = df["color"].interpolate(limit_direction="both")
    print("NaNs in color column:", df["color"].isna().sum())
print("———")

# -------------------------------------------------------------------------
# 8. ANALYSES: SIN-FIT, LAG, PER CAPITA (mw-8)
# -------------------------------------------------------------------------
def sin_f(t, A, w, phi, C):
    return A * np.sin(w * t + phi) + C

years = df.index          # after set_index – index is the time axis
x     = years - years.min()   # x-vector for sine fitting

pars, _ = curve_fit(
    sin_f, x, df["wars_smooth"],
    p0=[3, 2 * np.pi / 50, 0, 1],
    maxfev=10000
)
period = 2 * np.pi / pars[1]

corr_basic = np.corrcoef(df["color"], df["wars_smooth"])[0, 1]
lag        = 8
corr_lag   = np.corrcoef(
    df["color"].shift(lag)[lag:],
    df["wars_smooth"][lag:]
)[0, 1]

df["wars_pc"] = df["wars_smooth"] / df["pop"]
corr_pc = df["color"].corr(df["wars_pc_smooth"])  # ↓ NaN years are already skipped

# -------- correlation table for different lags ----------------------------
print("\nCorrelations color ↔ wars_smooth for different lags:")
max_lag = 10
for lag in range(0, max_lag + 1):
    pair = df[["color", "wars_smooth"]].copy()
    pair["wars_shift"] = pair["wars_smooth"].shift(lag)
    corr = pair.dropna()["color"].corr(pair.dropna()["wars_shift"])
    print(f"lag {lag:>2} years → corr = {corr:+.3f}")

# -------------------------------------------------------------------------
# 9. POWER SPECTRAL DENSITY (mw-9)
# -------------------------------------------------------------------------
f_wars, Pxx_wars = periodogram(detrend(df["wars_smooth"]), fs=1.0)
f_col,  Pxx_col  = periodogram(detrend(df["color"]),       fs=1.0)

# -------------------------------------------------------------------------
# 10. ARIMAX (1,1,1) for wars_smooth (mw-10)
# -------------------------------------------------------------------------
best_lag = 2                          # ← lag
exog     = df["color"].shift(best_lag)
mask     = exog.notna()               # drop NaNs after shifting

model     = ARIMA(df["wars_smooth"][mask], order=(1, 1, 1), exog=exog[mask])
arima_fit = model.fit()

last_exog      = exog.dropna().iloc[-1]   # repeat last exog value
exog_forecast  = np.repeat(last_exog, 20)
arima_forecast = arima_fit.get_forecast(steps=20, exog=exog_forecast).predicted_mean

# -------------------------------------------------------------------------
# 11. PRINT METRICS (mw-11)
# -------------------------------------------------------------------------
print(f"— Sine period ≈ {period:.1f} years")
print(f"— correlation         = {corr_basic:+.3f}")
print(f"— correlation (lag 8) = {corr_lag:+.3f}")
print(f"— per-capita correlation = {corr_pc:+.3f}")
print(arima_fit.summary())

# -------------------------------------------------------------------------
# 12. PLOTS (mw-12)
# -------------------------------------------------------------------------
years = df.index

plt.figure(figsize=(10, 10))

plt.subplot(411)
plt.plot(years, df["wars_smooth"], label=f"{SMOOTH_WIN}-year mean")
plt.plot(years, sin_f(x, *pars), "--", label="sin-fit")
plt.ylabel("number of wars")
plt.legend()

plt.subplot(412)
plt.loglog(f_wars[1:], Pxx_wars[1:], label="wars PSD")
plt.loglog(f_col[1:],  Pxx_col[1:],  label="color PSD")
plt.xlabel("frequency [1/year]")
plt.ylabel("PSD (log-scale)")

plt.subplot(413)
plt.plot(years, df["wars_pc"] * 1e9)
plt.ylabel("wars / pop ·1e9")
plt.xlabel("year")

plt.subplot(414)
years_forecast = np.arange(years[-1] + 1, years[-1] + 1 + len(arima_forecast))
plt.plot(years,         df["wars_smooth"],  label="hist")
plt.plot(years_forecast, arima_forecast,   "--", label="ARIMA forecast")
plt.ylabel("number of wars")
plt.xlabel("year")
plt.legend()

plt.tight_layout()
plt.savefig("analiza_wojny_color.pdf", dpi=300)
plt.show()

# -------------------------------------------------------------------------
# 13. CSV SAVE (full set)
# -------------------------------------------------------------------------
df[[
    "year", "wars", "wars_smooth", "wars_pc", "pop", "color",
    "gdelt_wars", "gdelt_goldstein"
]].to_csv("wars_color.csv", index=False)
print("✓ Saved wars_color.csv (8 columns)")
