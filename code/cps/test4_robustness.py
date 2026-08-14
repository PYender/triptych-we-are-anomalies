#!/usr/bin/env python3
"""
TEST 4 — odporność kontrastu epok na obserwacje odstające (rodzina 2, kontrola H2).
Realizuje TEST4_PROTOCOL.md v1.0 (zamrożony 14.08.2026). D-010, D-004, D-001, D-002.

Bada JEDYNE twierdzenie w projekcie z żywym poparciem (Test 3: kontrast epok M2>0
w 96/96 kombinacji na A_COW_P). Pytanie: czy kontrast jest własnością rozkładu, czy
kilku lat skrajnych. Orzeka wyłącznie P1 (krzywa M2(k), k=0..10, A_COW_P, T=35,1).

Wykorzystuje funkcje z test1_band_power.py (fit_ar_yw, sim_ar, linear_detrend);
NIE przepisuje ich. Test 4 czyta gotowy cps_canonical_v2.csv (builder v2.0 wystarcza —
nie zmieniamy wag ani normalizacji).

Sześć punktów, na których ten test się psuje (TASK_4 §A2) — jak są rozwiązane:
  1. Faza z NUMERU ROKU, nie z pozycji w wektorze. fold_chi2_years() liczy fazę jako
     ((rok − początek_okna) mod T); usunięcie lat NIE przesuwa fazy pozostałych.
     (fold_chi2 z Testu 1 liczy z indeksu — poprawnie tam, bo brak luk; tu byłoby błędne.)
  2. Detrending RAZ, na całej serii 1816–2007 (D-004), PRZED podziałem na epoki i PRZED
     usuwaniem lat. detrend_mode="global". (S5 liczy to samo z detrendingiem wewnątrz
     epoki jako kontrolę raportowaną OBOK — nie wchodzi do reguły §6.)
  3. To samo przetwarzanie na surogatach: surogat jest detrendowany i przechodzi TĘ SAMĄ
     transformację (usunięcie lat / winsoryzacja) co obserwacja, potem M2.
  4. R3 dla surogatów: każdy surogat ma usunięte WŁASNE k najwyższych lat epoki 2,
     nie te same lata kalendarzowe co dane (inaczej test antykonserwatywny).
  5. Winsoryzacja (R2) liczona OSOBNO dla każdej epoki, każda swoim percentylem.
  6. S4 (usuwanie k losowych lat) używa OSOBNEGO strumienia losowego niż surogaty.

Ranking „k najwyższych": na serii PO DETRENDINGU (na niej liczone jest M2), nie na
surowej — bo detrending globalny ściąga późne szczyty serii uczestniczej mocniej niż
wczesne, więc listy się różnią (raport podaje obie).

NIE uruchamiać przed przeglądem (TASK_4 §A4). Bieg to Etap B.

Wyjście: test4_results.csv, test4_curves.pdf
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

import test1_band_power as t1        # fit_ar_yw, sim_ar, linear_detrend

VERSION = "test4_robustness.py v1.0 (Etap A — do przeglądu)"

# --- parametry zamrożone w protokole; NIE zmieniać bez nowego protokołu ----------
SEED = 20260814
B = 2000
AR_ORDER = 3
NBINS = 10
T_PRIMARY = 35.1
T_ALT = (32.0, 40.0)
E1 = (1816, 1913)                 # epoka 1
E2 = (1914, 2007)                 # epoka 2
WAR_YEARS = sorted(set(range(1914, 1919)) | set(range(1939, 1946)))   # R1 (12 lat)
K_MAX = 10                        # R3: k = 0..10
K_DECIDE = 5                      # §6: próg orzekania (5,3% epoki 2)
S4_REPS = 500                     # S4: powtórzenia losowego usuwania
WINSOR_PCTS = (95, 90)            # R2: percentyle
S4_SEED = SEED + 1                # OSOBNY strumień losowy (A2.6)
# --------------------------------------------------------------------------------


# ============================ statystyka M2 ============================
def fold_chi2_years(vals: np.ndarray, years: np.ndarray, T: float, phase0: int,
                    nbins: int = NBINS) -> float:
    """Epoch-folding χ² z fazą liczoną z NUMERU ROKU (A2.1): faza = (rok − phase0) mod T.
    Odporne na luki po usunięciu lat — każdy pozostały rok zachowuje swoją fazę
    bezwzględną. Dla okna ciągłego redukuje się do fold_chi2 z Testu 1 (phase0 = pierwszy
    rok okna)."""
    if len(vals) == 0:
        return 0.0
    b = ((((years - phase0) % T) / T) * nbins).astype(int) % nbins
    g, var = vals.mean(), vals.var(ddof=1)
    if var == 0:
        return 0.0
    return float(sum(((b == k).sum() * (vals[b == k].mean() - g) ** 2) / var
                     for k in range(nbins) if (b == k).sum() > 0))


def M2(e2y, e2v, e1y, e1v, T: float) -> float:
    """M2 = χ²(epoka 2) − χ²(epoka 1); faza od pierwszego roku każdego okna (1914, 1816)."""
    return fold_chi2_years(e2v, e2y, T, E2[0]) - fold_chi2_years(e1v, e1y, T, E1[0])


# ============================ przygotowanie serii ============================
def load_raw(data: Path, variant: str) -> tuple[np.ndarray, np.ndarray]:
    df = pd.read_csv(data, comment="#")
    s = df[df.variant == variant].set_index("year")["value"].sort_index().loc[1816:2007]
    return s.index.to_numpy(), s.to_numpy(float)


def epochs(years: np.ndarray, vals: np.ndarray, detrend_mode: str):
    """Zwraca (e1y,e1v,e2y,e2v). detrend_mode='global' → detrending RAZ na całej serii
    przed podziałem (D-004, B2.2). detrend_mode='epoch' → osobno w każdej epoce (S5)."""
    if detrend_mode == "global":
        v = t1.linear_detrend(vals)
        m1 = (years >= E1[0]) & (years <= E1[1]); m2 = (years >= E2[0]) & (years <= E2[1])
        return years[m1], v[m1], years[m2], v[m2]
    if detrend_mode == "epoch":
        m1 = (years >= E1[0]) & (years <= E1[1]); m2 = (years >= E2[0]) & (years <= E2[1])
        return (years[m1], t1.linear_detrend(vals[m1]),
                years[m2], t1.linear_detrend(vals[m2]))
    raise ValueError(detrend_mode)


# ============================ transformacje epoki 2 ============================
def remove_highest(y, v, k):
    if k <= 0:
        return y, v
    keep = np.argsort(v)[:len(v) - k]           # usuń k o najwyższej wartości
    keep = np.sort(keep)
    return y[keep], v[keep]


def remove_calendar(y, v, years_set):
    mask = np.array([yr not in years_set for yr in y])
    return y[mask], v[mask]


def remove_random(y, v, k, rng):
    if k <= 0:
        return y, v
    drop = rng.choice(len(v), size=k, replace=False)
    keep = np.setdiff1d(np.arange(len(v)), drop)
    return y[keep], v[keep]


def winsorize(v, pct):
    """Winsoryzacja górna na poziomie `pct` percentyla, liczonym we WŁASNYM rozkładzie
    (A2.5). Stosowana osobno do każdej epoki przez wywołującego."""
    cap = np.percentile(v, pct)
    return np.minimum(v, cap)


# ============================ model zerowy ============================
def make_surrogates(base: np.ndarray, years_full: np.ndarray, detrend_mode: str, rng):
    """B surogatów AR(3) całej serii; każdy detrendowany tą samą metodą i dzielony na
    epoki. Zwraca listę (e1y,e1v,e2y,e2v). Jedno wywołanie na (seria, detrend_mode)."""
    a, resid = t1.fit_ar_yw(base, AR_ORDER)
    out = []
    for _ in range(B):
        y = t1.sim_ar(a, resid, len(base), rng)
        out.append(epochs(years_full, y, detrend_mode))
    return out


def pval(m2_obs: float, m2_sur: np.ndarray) -> float:
    """Jednostronne (H2: M2>0): p = (1 + #{M2_sur ≥ M2_obs}) / (B+1)."""
    return (1 + int(np.sum(m2_sur >= m2_obs))) / (B + 1)


# ============================ warianty odporności ============================
def run_R3_curve(years, vals, T, detrend_mode, rng):
    """R3: krzywa M2(k), p(k) dla k=0..K_MAX. Surogaty usuwają WŁASNE k najwyższych (A2.4).
    Epoka 1 nietknięta (R3 zdejmuje tylko z epoki 2). Surogaty generowane raz i reużywane
    dla wszystkich k (spójny ansambl); własne k najwyższych zdejmowane przy każdym k."""
    e1y, e1v, e2y, e2v = epochs(years, vals, detrend_mode)
    base = t1.linear_detrend(vals)                # baza AR: seria detrend. globalnie (stacjonarna)
    surs = make_surrogates(base, years, detrend_mode, rng)
    chi1 = fold_chi2_years(e1v, e1y, T, E1[0])
    sur_chi1 = np.array([fold_chi2_years(s1v, s1y, T, E1[0]) for (s1y, s1v, _, _) in surs])
    rows, highest_years = [], list(e2y[np.argsort(e2v)[::-1]][:K_MAX])
    for k in range(0, K_MAX + 1):
        ry, rv = remove_highest(e2y, e2v, k)
        m2_obs = fold_chi2_years(rv, ry, T, E2[0]) - chi1
        m2_sur = np.array([
            (fold_chi2_years(*remove_highest(s2y, s2v, k)[::-1], T, E2[0]) - c1)
            for (_, _, s2y, s2v), c1 in zip(surs, sur_chi1)])
        rows.append({"k": k, "n": len(rv), "M2": round(m2_obs, 4), "p": round(pval(m2_obs, m2_sur), 4)})
    return rows, highest_years


def run_R1(years, vals, T, detrend_mode, rng):
    """R1: wyłączenie lat wojen światowych (te same lata kalendarzowe u obs i surogatów, A2.3)."""
    e1y, e1v, e2y, e2v = epochs(years, vals, detrend_mode)
    base = t1.linear_detrend(vals)
    surs = make_surrogates(base, years, detrend_mode, rng)
    ws = set(WAR_YEARS)
    ry, rv = remove_calendar(e2y, e2v, ws)
    m2_obs = M2(ry, rv, e1y, e1v, T)
    m2_sur = np.array([M2(*remove_calendar(s2y, s2v, ws), s1y, s1v, T)
                       for (s1y, s1v, s2y, s2v) in surs])
    return {"n": len(rv), "M2": round(m2_obs, 4), "p": round(pval(m2_obs, m2_sur), 4)}


def run_R2(years, vals, T, pct, detrend_mode, rng):
    """R2: winsoryzacja obu epok, każda własnym percentylem (A2.5). Bez luk."""
    e1y, e1v, e2y, e2v = epochs(years, vals, detrend_mode)
    base = t1.linear_detrend(vals)
    surs = make_surrogates(base, years, detrend_mode, rng)
    m2_obs = M2(e2y, winsorize(e2v, pct), e1y, winsorize(e1v, pct), T)
    m2_sur = np.array([M2(s2y, winsorize(s2v, pct), s1y, winsorize(s1v, pct), T)
                       for (s1y, s1v, s2y, s2v) in surs])
    return {"n": len(e2v), "M2": round(m2_obs, 4), "p": round(pval(m2_obs, m2_sur), 4)}


def run_S4_band(years, vals, T, detrend_mode):
    """S4 (§5, interpretacyjnie konieczny): dla k=0..K_MAX usuwa k LOSOWYCH lat epoki 2,
    S4_REPS powtórzeń, OSOBNY strumień losowy (A2.6). Zwraca rozkład M2 (mean, sd) na k —
    pasmo odniesienia dla krzywej R3."""
    e1y, e1v, e2y, e2v = epochs(years, vals, detrend_mode)
    chi1 = fold_chi2_years(e1v, e1y, T, E1[0])
    rng = np.random.default_rng(S4_SEED)
    rows = []
    for k in range(0, K_MAX + 1):
        if k == 0:
            vals_k = [fold_chi2_years(e2v, e2y, T, E2[0]) - chi1]
        else:
            vals_k = []
            for _ in range(S4_REPS):
                ry, rv = remove_random(e2y, e2v, k, rng)
                vals_k.append(fold_chi2_years(rv, ry, T, E2[0]) - chi1)
        arr = np.array(vals_k)
        rows.append({"k": k, "ref_mean": round(float(arr.mean()), 4),
                     "ref_sd": round(float(arr.std(ddof=1)) if len(arr) > 1 else 0.0, 4)})
    return rows


# ============================ silnik / lista uruchomień ============================
def decide(p1_rows, s4_rows) -> str:
    """Reguła §6: pozytywny ⟺ M2>0 i p<0,05 przy k=5 ORAZ spadek M2 (k0→k5) nie przekracza
    oczekiwanego z S4 o więcej niż 2 odchylenia rozkładu S4."""
    r5 = next(r for r in p1_rows if r["k"] == K_DECIDE)
    r0 = next(r for r in p1_rows if r["k"] == 0)
    s5 = next(r for r in s4_rows if r["k"] == K_DECIDE)
    drop_obs = r0["M2"] - r5["M2"]
    drop_ref = r0["M2"] - s5["ref_mean"]            # oczekiwany spadek przy losowym usuwaniu
    within = drop_obs <= drop_ref + 2 * s5["ref_sd"]
    cond1 = (r5["M2"] > 0) and (r5["p"] < 0.05)
    ok = cond1 and within
    return (f"P1 k=5: M2={r5['M2']} p={r5['p']} | spadek obs={drop_obs:.3f} vs "
            f"S4 {drop_ref:.3f}±{2*s5['ref_sd']:.3f} → "
            f"{'POZYTYWNY' if ok else 'NIEWSPARTY'} (warunek1={cond1}, w paśmie S4={within})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="cps_canonical_v2.csv")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)               # strumień surogatów (osobny od S4)

    series = {v: load_raw(Path(a.data), v) for v in ("A_COW_P", "A_COW_W")}
    rows = []

    def add(idv, seria, wariant, T, payload, extra=None):
        base = {"id": idv, "seria": seria, "wariant": wariant, "T": T}
        for r in (payload if isinstance(payload, list) else [payload]):
            rows.append({**base, **r, **(extra or {})})

    yP, vP = series["A_COW_P"]; yW, vW = series["A_COW_W"]

    # P1 — R3 krzywa, A_COW_P, T=35,1 (ORZEKA)
    p1_rows, p1_high = run_R3_curve(yP, vP, T_PRIMARY, "global", rng)
    s4_rows = run_S4_band(yP, vP, T_PRIMARY, "global")
    add("P1", "A_COW_P", "R3", T_PRIMARY, p1_rows)
    add("S4", "A_COW_P", "S4_ref", T_PRIMARY, s4_rows)
    # P2 — R1 (wyłączenie wojen światowych)
    add("P2", "A_COW_P", "R1", T_PRIMARY, run_R1(yP, vP, T_PRIMARY, "global", rng))
    # S1 — R2 winsoryzacja 95 i 90
    for pct in WINSOR_PCTS:
        add(f"S1_w{pct}", "A_COW_P", f"R2_w{pct}", T_PRIMARY, run_R2(yP, vP, T_PRIMARY, pct, "global", rng))
    # S2 — R3 przy T=32 i T=40
    for T in T_ALT:
        r, _ = run_R3_curve(yP, vP, T, "global", rng)
        add(f"S2_T{int(T)}", "A_COW_P", "R3", T, r)
    # S3 — R1, R2, R3 na A_COW_W
    s3_r3, s3_high = run_R3_curve(yW, vW, T_PRIMARY, "global", rng)
    add("S3_R3", "A_COW_W", "R3", T_PRIMARY, s3_r3)
    add("S3_R1", "A_COW_W", "R1", T_PRIMARY, run_R1(yW, vW, T_PRIMARY, "global", rng))
    for pct in WINSOR_PCTS:
        add(f"S3_R2_w{pct}", "A_COW_W", f"R2_w{pct}", T_PRIMARY, run_R2(yW, vW, T_PRIMARY, pct, "global", rng))
    # S5 — kontrola: detrending WEWNĄTRZ epoki (obie serie), raportowana OBOK (poza §6)
    s5P, _ = run_R3_curve(yP, vP, T_PRIMARY, "epoch", rng)
    s5W, _ = run_R3_curve(yW, vW, T_PRIMARY, "epoch", rng)
    add("S5_P", "A_COW_P", "R3_epochdetr", T_PRIMARY, s5P)
    add("S5_W", "A_COW_W", "R3_epochdetr", T_PRIMARY, s5W)

    res = pd.DataFrame(rows)
    verdict = decide(p1_rows, s4_rows)

    # listy k najwyższych: surowa (opis historyczny, D-010) i po detrendingu (usuwana przez R3)
    raw_high_P = list(pd.Series(vP, index=yP).loc[E2[0]:E2[1]].sort_values(ascending=False).head(K_MAX).index)
    meta = {"script": VERSION, "seed": SEED, "B": B, "null": f"AR({AR_ORDER})",
            "sha256_data": hashlib.sha256(Path(a.data).read_bytes()).hexdigest()[:16],
            "P1_verdict": verdict,
            "highest_P_detrended": [int(x) for x in p1_high],
            "highest_P_raw": [int(x) for x in raw_high_P]}
    with open(out / "test4_results.csv", "w", encoding="utf-8") as fh:
        fh.write("# " + json.dumps(meta, ensure_ascii=False) + "\n")
        res.to_csv(fh, index=False)
    curves(res, p1_rows, s4_rows, s3_r3, series, p1_high, out / "test4_curves.pdf")

    print(res.to_string(index=False))
    print("\n" + verdict)
    print(f"k najwyższych (po detrend., usuwane przez R3): {[int(x) for x in p1_high]}")
    print(f"k najwyższych (surowe, D-010): {[int(x) for x in raw_high_P]}")
    print("Orzeka wyłącznie P1. S5 (detrending w epoce) jest kontrolą obok, poza §6.")


# ================================== wykresy ==================================
def curves(res, p1_rows, s4_rows, s3_rows, series, p1_high, out: Path):
    """§8: panel 1 krzywa M2(k)+p(k) dla P1 z pasmem S4; panel 2 to samo dla A_COW_W;
    panel 3 epoka 2 z zaznaczonymi k najwyższymi latami; panel 4 winsoryzacja."""
    ks = [r["k"] for r in p1_rows]
    with PdfPages(out) as pdf:
        # Panel 1: P1 M2(k), p(k), pasmo S4
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.plot(ks, [r["M2"] for r in p1_rows], "o-", label="M2(k) — A_COW_P (P1)")
        ref_m = np.array([r["ref_mean"] for r in s4_rows]); ref_s = np.array([r["ref_sd"] for r in s4_rows])
        ax.fill_between(ks, ref_m - 2 * ref_s, ref_m + 2 * ref_s, alpha=.2, color="gray",
                        label="pasmo S4 (usuwanie losowe, ±2σ)")
        ax.axvline(K_DECIDE, ls="--", c="crimson", lw=1, label=f"k={K_DECIDE} (§6)")
        ax.set_xlabel("k (liczba usuniętych najwyższych lat epoki 2)"); ax.set_ylabel("M2")
        ax2 = ax.twinx(); ax2.plot(ks, [r["p"] for r in p1_rows], "s--", c="green", label="p(k)")
        ax2.axhline(0.05, ls=":", c="green", lw=1); ax2.set_ylabel("p")
        ax.set_title("Panel 1. P1: M2(k) i p(k) z pasmem odniesienia S4"); ax.legend(loc="upper right")
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        # Panel 2: A_COW_W (S3 R3)
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot([r["k"] for r in s3_rows], [r["M2"] for r in s3_rows], "o-", c="slategray")
        ax.axhline(0, lw=.6, c="k"); ax.set_xlabel("k"); ax.set_ylabel("M2")
        ax.set_title("Panel 2. A_COW_W (S3, R3) — porównanie z serią wojno-poziomową")
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        # Panel 3: epoka 2 A_COW_P z zaznaczonymi k najwyższymi (po detrendingu)
        yP, vP = series["A_COW_P"]; v = t1.linear_detrend(vP)
        m2 = (yP >= E2[0]) & (yP <= E2[1])
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.plot(yP[m2], v[m2], lw=1)
        hi = set(int(x) for x in p1_high[:K_DECIDE])
        ax.scatter([y for y in yP[m2] if y in hi], [v[list(yP).index(y)] for y in yP[m2] if y in hi],
                   c="crimson", zorder=5, label=f"{K_DECIDE} najwyższych (po detrend.)")
        ax.set_title("Panel 3. Epoka 2 A_COW_P po detrendingu — najwyższe lata usuwane przez R3")
        ax.legend(); ax.grid(alpha=.3); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
        # Panel 4: winsoryzacja (M2 przy 95/90 vs bez)
        fig, ax = plt.subplots(figsize=(11, 4))
        w = res[res.wariant.str.startswith("R2")]
        ax.bar([f"{r.id}" for _, r in w.iterrows()], [r.M2 for _, r in w.iterrows()], color="steelblue")
        ax.axhline(0, lw=.6, c="k"); ax.set_ylabel("M2")
        ax.set_title("Panel 4. Winsoryzacja (R2) — A_COW_P")
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)


if __name__ == "__main__":
    main()
