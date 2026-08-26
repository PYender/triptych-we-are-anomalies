#!/usr/bin/env python3
"""
TEST 7 — Etap B (D-029): estymacja P1 (kruchość gamma, orzekający dla H9b.1) na strukturze
120 diad rodziny 9b, plus symulacja odzysku parametrów i model zerowy N1 diagnostyczny.
Realizuje `TEST7_PROTOCOL.md` §5, §7, §8 i `TASK_7B_BRIEF.md` §2-§6.

Estymator: `test6_weibull.py` (naprawiony, pięć usterek + D-022 + zweryfikowany w Kroku C
Testu 6, D-027) — NIE pisany od nowa, zgodnie z brief §1 „Nie pisz drugiego estymatora".

Różnica strukturalna wobec Testu 6, obsłużona tutaj (nie w test6_weibull.py):
  1. `t0` wyłączone z modelu głównego zawsze (protokół §5) — `load_grouped(include_t0=False)`.
     S3 (`include_t0=True`) włącza je jako odstęp pełny, zgodnie z definicją wariantu.
  2. Diada może mieć 0 ALBO 1 obserwację cenzurowaną w modelu głównym, NIE zawsze dokładnie 1
     jak w Teście 6 — konsekwencja Skutku A z D-021 (okno domyka się na zdarzeniu, bez odstępu
     cenzurowanego po nim). Zweryfikowane na realnej strukturze: 98 diad z 1 cenzurowanym
     wierszem, 8 z zerem (wszystkie 0/1, żadna z >1) — patrz test7_estimate.md §1.
  3. **14 diad (na 120) wnoszą ZERO wierszy do modelu głównego** — pojedynczy epizod +
     Skutek A + wyłączenie t0 razem zostawiają taką diadę bez żadnej obserwacji. Zgodne z
     protokołem (§5 wyklucza t0, D-021 nie tworzy odstępu cenzurowanego po Skutku A), ale
     zmienia efektywne N modelu głównego z 120 na 106 diad wnoszących coś — patrz test7_estimate.md §1.

NIE URUCHAMIANE na `test7_intervals.csv` w tym pliku poza testami poprawności na strukturze
(nigdy na wartościach `t`) i sprawdzeniami mechanicznymi jawnie tak oznaczonymi. `main()`
blokuje `--run-real` (STOP, brief §8/D-029).
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

import numpy as np
import pandas as pd

import test6_weibull as w

SEED_PROTOCOL_N1 = 20260822        # ten sam ziarno modeli zerowych co Test 6 (§6 protokołu Testu 6,
                                    # przywołane w D-029 pkt 2 dla N1 diagnostycznego Testu 7)
B_NULL = 2000
B_BOOTSTRAP = 2000


# ============================ dane — model główny (D-029, protokół §5) ============================
def load_grouped(path: str = "test7_intervals.csv", include_t0: bool = False):
    """Zwraca listę (diad, t_full: np.ndarray, c: float|None) — jedna pozycja PER DIADA
    obecna w pliku, ale tylko diady z >=1 wierszem kwalifikującym trafiają na listę (diady
    całkowicie nieobecne w modelu głównym — patrz moduł docstring pkt 3 — po prostu nie mają
    tu wpisu; to jest fakt strukturalny, nie błąd).

    include_t0=False (domyślne, model główny, protokół §5): wiersze `t0_flag==1` wyłączone,
    ORAZ diady `ucieta==1` wyłączone W CAŁOŚCI — protokół §3 (cytat): „Diady te muszą być
    oznaczone kolumną ucięta=1 i wchodzić do wariantu S3, nie do modelu głównego." Zdanie nie
    zostawia alternatywy (przegląd `PRZEGLAD_test7_estimate.md` §2) — to jest wymóg protokołu,
    nie kwestia interpretacji, poprawione po tym, jak pierwsza wersja tego kodu błędnie
    zostawiała te diady w modelu głównym (wykluczała tylko ich `t0`, tak jak wszystkie inne).
    include_t0=True (S3): wiersze t0 dołączone jako PEŁNE (cenzurowany==0), diady `ucieta==1`
    WRACAJĄ do zbioru (to jest dokładnie ich miejsce wg §3)."""
    df = pd.read_csv(path, comment="#")
    if not include_t0:
        df = df[df["t0_flag"] == 0]
        df = df[df["ucieta"] == 0]
    out = []
    for d, g in df.groupby("diada"):
        t_full = g.loc[g["cenzurowany"] == 0, "ekspozycja"].to_numpy(float)
        c_rows = g.loc[g["cenzurowany"] == 1, "ekspozycja"].to_numpy(float)
        assert len(c_rows) <= 1, f"diada {d}: {len(c_rows)} obserwacji cenzurowanych w modelu głównym, oczekiwano <=1"
        if len(t_full) == 0 and len(c_rows) == 0:
            continue                                    # diada bez żadnej obserwacji w tym modelu — pomijana
        c = float(c_rows[0]) if len(c_rows) == 1 else None
        out.append((d, t_full, c))
    return out


def flatten(grouped):
    """(diad, t, event) — c=None diady nie wnoszą wiersza cenzurowanego (brak, nie zero)."""
    diads, t, event = [], [], []
    for d, t_full, c in grouped:
        for x in t_full:
            diads.append(d); t.append(x); event.append(1)
        if c is not None:
            diads.append(d); t.append(c); event.append(0)
    return np.array(diads), np.array(t, float), np.array(event, int)


def structure_report(grouped, label=""):
    """Liczby wierszy przed/po — D-028, obowiązkowe przy każdej decyzji dotyczącej warstwy
    danych. Tu: ile diad wnosi coś do tego konkretnego modelu (główny/S3/...)."""
    n_full_total = sum(len(t_full) for _, t_full, _ in grouped)
    n_cens_total = sum(1 for _, _, c in grouped if c is not None)
    return dict(label=label, n_diady_z_wierszem=len(grouped),
               n_pelne=n_full_total, n_cenzurowane=n_cens_total)


# ============================ P1: dopasowanie ============================
def fit_p1(grouped):
    """Zwraca (fit_frailty=orzekający wg protokołu §7, fit_pooled=diagnostyka θ→0, brief §3)."""
    diads, t, event = flatten(grouped)
    fit_pooled = w.fit_pooled(t, event)
    fit_frailty = w.fit_frailty(t, event, diads)
    return diads, t, event, fit_pooled, fit_frailty


def ci_p1(diads, t, event, fit_pooled, fit_frailty, B=B_BOOTSTRAP, seed=w.RNG_SEED):
    """Oba przedziały (protokół §8 obowiązkowo w dwóch postaciach) dla obu dopasowań.

    D-022 / PRZEGLAD2_test6_weibull.md §4 / PRZEGLAD_test7_estimate.md §5: przedział
    bootstrapowy dla modelu z kruchością MUSI być podany razem z odsetkiem replik, w których
    θ̂ osiadło na granicy numerycznej — bez tej liczby nie jest interpretowalny. Pierwsza
    wersja tego kodu wywoływała `bootstrap_ci_k_frailty` (która ten odsetek już zwraca od
    D-022) i po prostu nie rozpakowywała/etykietowała czwartego elementu — poprawione."""
    prof_pooled = w.profile_ci_k(w.negloglik_pooled, (t, event), fit_pooled["k"],
                                 [fit_pooled["loglam"]], fit_pooled["loglik"])
    groups, gidx = np.unique(diads, return_inverse=True)
    prof_frailty = w.profile_ci_k(w.negloglik_frailty, (t, event, gidx, len(groups)),
                                  fit_frailty["k"], [fit_frailty["loglam"], fit_frailty["logtheta"]],
                                  fit_frailty["loglik"])
    boot_lo_p, boot_hi_p, _ = w.bootstrap_ci_k_pooled(t, event, diads, B=B, seed=seed)
    boot_lo_f, boot_hi_f, _, frac_theta_boundary = w.bootstrap_ci_k_frailty(t, event, diads, B=B, seed=seed)
    return dict(
        profile_pooled=dict(lo=prof_pooled[0], hi=prof_pooled[1]),
        profile_frailty=dict(lo=prof_frailty[0], hi=prof_frailty[1]),
        bootstrap_pooled=dict(lo=boot_lo_p, hi=boot_hi_p),
        bootstrap_frailty=dict(lo=boot_lo_f, hi=boot_hi_f,
                               frac_theta_boundary=frac_theta_boundary,
                               interpretowalny=frac_theta_boundary < 0.30))


# ============================ symulacja odzysku parametrów (brief §4) ============================
def group_specs_from(path: str = "test7_intervals.csv", include_t0: bool = False):
    """Lista (n_full, ma_cenzurowany: bool) per diada — struktura REALNA modelu głównego,
    odczytana wyłącznie ze struktury (liczby wierszy), NIGDY z wartości `t`. Różni się od
    `test6_weibull.group_sizes_from`, które zakłada zawsze dokładnie 1 cenzurowany/diadę —
    założenie nieprawdziwe tutaj (moduł docstring pkt 2-3)."""
    grouped = load_grouped(path, include_t0=include_t0)
    return [(len(t_full), c is not None) for _, t_full, c in grouped]


def simulate_dataset_test7(k, lam, theta, group_specs, rng):
    """Jak `test6_weibull.simulate_dataset`, ale każda grupa ma cenzurowanie WEDŁUG
    `group_specs` (0 albo 1 obserwacja cenzurowana), nie zawsze dokładnie 1. Cenzurowanie,
    gdy obecne, jest ADMINISTRACYJNE (niezależne od czasu zdarzenia) — brief §4, usterka 4
    przeglądu Testu 6: cenzurowanie zależne od T zawyża k̂ o ok. 5 pkt proc."""
    ts, ev, gid = [], [], []
    for g, (n_full, has_cens) in enumerate(group_specs):
        u = 1.0 if theta <= 0 else rng.gamma(shape=1.0 / theta, scale=theta)
        for _ in range(int(n_full)):
            e = rng.exponential(1.0)
            t = lam * (e / u) ** (1.0 / k)
            ts.append(t); ev.append(1); gid.append(g)
        if has_cens:
            c = rng.exponential(scale=lam)              # administracyjne, niezależne od u/zdarzeń
            ts.append(c); ev.append(0); gid.append(g)
    return np.array(ts, float), np.array(ev, int), np.array(gid)


def test_parameter_recovery_test7(group_specs, k_true, lam_true, theta_true, label, seed=w.RNG_SEED):
    rng = np.random.default_rng(seed)
    t, event, diad = simulate_dataset_test7(k_true, lam_true, theta_true, group_specs, rng)
    fit_p = w.fit_pooled(t, event)
    x0_list = list(w.DEFAULT_X0_FRAILTY) + [(fit_p["logk"], fit_p["loglam"], np.log(1e-4))]
    fit_f = w.fit_frailty(t, event, diad, x0_list=x0_list)
    return dict(label=label, k_true=k_true, lam_true=lam_true, theta_true=theta_true,
               n_events=int(event.sum()), n_censored=int((1 - event).sum()),
               n_groups=len(group_specs),
               pooled_k_hat=fit_p["k"], pooled_converged_same=fit_p["converged_same"],
               frailty_k_hat=fit_f["k"], frailty_theta_hat=fit_f["theta"],
               frailty_theta_at_boundary=fit_f["theta_at_boundary"],
               frailty_converged_same=fit_f["converged_same"])


def test_frailty_boundary_collapse_test7(group_specs, k_true=1.2, n_reps=60,
                                         theta_grid=(0.0, 0.3, 0.6, 1.0), lam_true=20.0,
                                         boundary_floor=1e-10):
    """D-022, przeniesione na strukturę Testu 7 (PRZEGLAD_test7_estimate.md §3 — brak tego
    pomiaru w pierwszej wersji był brakiem, nie formalnością: w Teście 7 ORZEKA model z
    kruchością, więc jeśli θ̂ zapada się w większości biegów, reguła §8 rozstrzyga w praktyce
    na modelu pulowanym). Analogiczne do `test6_weibull.test_frailty_boundary_collapse`, ale
    na `simulate_dataset_test7`/`group_specs` (0/1-cenzurowanie), nie na
    `test6_weibull.simulate_dataset` (zawsze-1-cenzurowany, niepoprawne dla tej struktury)."""
    rng = np.random.default_rng(w.RNG_SEED)
    out = {}
    for theta_true in theta_grid:
        thetas = np.empty(n_reps)
        for i in range(n_reps):
            t, event, diad = simulate_dataset_test7(k_true, lam_true, theta_true, group_specs, rng)
            thetas[i] = w.fit_frailty(t, event, diad)["theta"]
        at_boundary = thetas <= boundary_floor
        out[str(theta_true)] = dict(theta_true=theta_true, n_reps=n_reps,
                                    frac_at_boundary=float(at_boundary.mean()),
                                    median_theta_hat=float(np.median(thetas)))
    return out


# ============================ model zerowy N1 diagnostyczny (D-029 pkt 2) ============================
def simulate_n1_once_test7(grouped, rng):
    """Jak `test6_null.simulate_n1_once`, generalizowane na 0/1 cenzurowanie per diada.
    Zwraca też etykiety diad (`diad_sim`) — wymagane, żeby ten sam surogat dało się ocenić
    ZARÓWNO statystyką pulowaną (etykiety ignorowane), JAK I statystyką z kruchością
    (etykiety wymagane) — patrz PRZEGLAD_test7_estimate.md §4."""
    diad_sim, t_sim, event_sim = [], [], []
    for d, t_full, c in grouped:
        n = len(t_full)
        total_exposure = float(t_full.sum() + (c if c is not None else 0.0))
        lam_hat = n / total_exposure if total_exposure > 0 else 0.0
        new_full = rng.exponential(1.0 / lam_hat, size=n) if (n > 0 and lam_hat > 0) else np.array([])
        for x in new_full:
            diad_sim.append(d); t_sim.append(x); event_sim.append(1)
        if c is not None:
            diad_sim.append(d); t_sim.append(c); event_sim.append(0)
    return np.array(diad_sim), np.array(t_sim, float), np.array(event_sim, int)


def tie_fraction(k_sur, kobs, tol=1e-6):
    """D-026 §7 — zabezpieczenie przed remisem, przeniesione z test6_null.py: każdy model
    zerowy oparty na symulacji wymaga jawnego wykrywania remisów, nie tylko ufności w
    algebrę. Patrz test6_null.py dla pełnego uzasadnienia."""
    return float(np.mean(np.abs(k_sur - kobs) < tol))


TIE_FRAC_STOP = 0.01


def _p_from_ksur(k_sur, kobs, B):
    return (1 + int(np.sum(np.abs(k_sur - 1.0) >= np.abs(kobs - 1.0)))) / (B + 1)


def run_n1_test7(path: str = "test7_intervals.csv", B: int = B_NULL, B_frailty: int = 500,
                  seed: int = SEED_PROTOCOL_N1, include_t0: bool = False):
    """Model zerowy N1 na strukturze Testu 7 — DIAGNOSTYCZNY (D-029 pkt 2), nie wchodzi do
    reguły decyzyjnej §8, wyłącznie do pokazania rozjazdu CI-kontra-p, zadeklarowanego przed
    biegiem Testu 7.

    POPRAWKA (PRZEGLAD_test7_estimate.md §4): pierwsza wersja liczyła k_obs i wszystkie
    surogaty przez `fit_pooled`, a statystyką ORZEKAJĄCĄ w Teście 7 jest `fit_frailty` (§7
    protokołu) — diagnostyka pokazywała więc rozjazd dla statystyki, która nie rozstrzyga
    H9b.1, nie odpowiadając na pytanie, dla którego powstała (`PRZEGLAD_TASK_7B.md` §2).
    Liczy teraz OBIE wersje i podaje oba `p` obok siebie: `pooled` przy pełnym B (tanie),
    `frailty` przy zredukowanym `B_frailty=500` (kompromis kosztowy zaakceptowany w
    przeglądzie — dopasowanie z kruchością jest znacząco droższe: wielostart + optymalizacja
    3-parametrowa per replika)."""
    grouped = load_grouped(path, include_t0=include_t0)
    diads, t, event = flatten(grouped)
    kobs_pooled = w.fit_pooled(t, event)["k"]
    kobs_frailty = w.fit_frailty(t, event, diads)["k"]

    rng = np.random.default_rng(seed)
    k_sur_pooled = np.empty(B)
    k_sur_frailty = np.empty(B_frailty)
    for b in range(B):
        diad_sim, t_sim, event_sim = simulate_n1_once_test7(grouped, rng)
        k_sur_pooled[b] = w.fit_pooled(t_sim, event_sim)["k"]
        if b < B_frailty:
            k_sur_frailty[b] = w.fit_frailty(t_sim, event_sim, diad_sim)["k"]

    frac_tie_pooled = tie_fraction(k_sur_pooled, kobs_pooled)
    frac_tie_frailty = tie_fraction(k_sur_frailty, kobs_frailty)
    for name, frac in (("pooled", frac_tie_pooled), ("frailty", frac_tie_frailty)):
        if frac > TIE_FRAC_STOP:
            raise AssertionError(
                f"D-026 §7 / D-029: {frac:.1%} surogatów N1 ({name}, Test 7) remisuje z "
                "obserwacją — oznaka degeneracji. Zatrzymuję bieg zamiast zwracać p bez treści.")

    return dict(model="N1_test7", poza_regula_decyzyjna_S8="diagnostyczny (D-029 pkt 2), nie orzeka",
               seed=seed,
               pooled=dict(k_obs=kobs_pooled, p=_p_from_ksur(k_sur_pooled, kobs_pooled, B), B=B,
                          k_sur_mean=float(k_sur_pooled.mean()), k_sur_median=float(np.median(k_sur_pooled)),
                          k_sur_sd=float(k_sur_pooled.std(ddof=1)), frac_tie=frac_tie_pooled),
               frailty=dict(k_obs=kobs_frailty, p=_p_from_ksur(k_sur_frailty, kobs_frailty, B_frailty),
                           B=B_frailty,
                           k_sur_mean=float(k_sur_frailty.mean()), k_sur_median=float(np.median(k_sur_frailty)),
                           k_sur_sd=float(k_sur_frailty.std(ddof=1)), frac_tie=frac_tie_frailty,
                           uwaga="statystyka ORZEKAJĄCA (§7 protokołu) — to jest ta wersja, "
                                 "która odpowiada na pytanie postawione w D-029 pkt 2"))


# ============================ testy poprawności (brief §3-§4, obowiązkowe przed --run-real) ========
def test_theta_zero_limit_test7(group_specs):
    """theta=1e-6 (wartość użyta w wersji Testu 6) NIE zbiega tu poniżej progu 1e-4 —
    sprawdzone bezpośrednio: różnica maleje monotonicznie i gładko wraz z θ (0,35 przy
    logθ=-6 do 4e-6 przy logθ=-20), więc to wolniejsze tempo zbieżności na tej strukturze
    (nie błąd) — użyto θ=1e-9, bliżej rzeczywistej podłogi numerycznej (1e-10) stosowanej
    gdzie indziej w kodzie, żeby granica była zademonstrowana z tą samą precyzją co w Teście 6."""
    rng = np.random.default_rng(w.RNG_SEED)
    t, event, diad = simulate_dataset_test7(1.3, 20.0, 0.0, group_specs, rng)
    groups, gidx = np.unique(diad, return_inverse=True)
    ll_pooled = -w.negloglik_pooled(np.array([np.log(1.3), np.log(20.0)]), t, event)
    ll_frailty = -w.negloglik_frailty(np.array([np.log(1.3), np.log(20.0), np.log(1e-9)]),
                                      t, event, gidx, len(groups))
    diff = abs(ll_pooled - ll_frailty)
    return dict(loglik_pooled=ll_pooled, loglik_frailty_theta1e9=ll_frailty,
               abs_diff=diff, ok=diff < 1e-4)


def censoring_realism_check(intervals_csv, group_specs, k_true=1.0, lam_true=20.0, theta_true=0.0,
                            seed=w.RNG_SEED):
    """PRZEGLAD_test7_estimate.md §6 (nie blokujące, ale zlecone): cenzurowanie w symulacji
    (`c = Exponential(scale=lam)`, administracyjne) ma odsetek zgodny z konstrukcją, ale jego
    ROZKŁAD nie musi przypominać realnego (gdzie czas cenzurowany to pozostała ekspozycja, a
    dla 56 diad bez epizodów — całe okno). Podaje stosunek mediany czasów cenzurowanych do
    mediany czasów zdarzeń, realnie i w symulacji, żeby dało się ocenić, na ile symulacja
    odzysku przewiduje zachowanie na realnym zbiorze."""
    df = pd.read_csv(intervals_csv, comment="#")
    df = df[(df["t0_flag"] == 0) & (df["ucieta"] == 0)]
    real_full = df.loc[df["cenzurowany"] == 0, "ekspozycja"].to_numpy(float)
    real_cens = df.loc[df["cenzurowany"] == 1, "ekspozycja"].to_numpy(float)
    real_ratio = float(np.median(real_cens) / np.median(real_full)) if len(real_full) and len(real_cens) else float("nan")

    rng = np.random.default_rng(seed)
    t, event, _ = simulate_dataset_test7(k_true, lam_true, theta_true, group_specs, rng)
    sim_full = t[event == 1]
    sim_cens = t[event == 0]
    sim_ratio = float(np.median(sim_cens) / np.median(sim_full)) if len(sim_full) and len(sim_cens) else float("nan")

    return dict(real_median_cens=float(np.median(real_cens)), real_median_full=float(np.median(real_full)),
               real_ratio=real_ratio, sim_median_cens=float(np.median(sim_cens)),
               sim_median_full=float(np.median(sim_full)), sim_ratio=sim_ratio,
               k_true=k_true, lam_true=lam_true, theta_true=theta_true)


def run_correctness_suite_test7(intervals_csv: str = "test7_intervals.csv"):
    group_specs = group_specs_from(intervals_csv)
    out = {"n_groups_with_rows": len(group_specs),
          "n_full_total": sum(n for n, _ in group_specs),
          "n_cens_total": sum(1 for _, has in group_specs if has)}
    out["theta_zero_limit"] = test_theta_zero_limit_test7(group_specs)
    out["recovery"] = [
        test_parameter_recovery_test7(group_specs, k_true=1.0, lam_true=20.0, theta_true=0.0,
                                      label="k=1 (bez pamieci), theta=0 (bez kruchosci)"),
        test_parameter_recovery_test7(group_specs, k_true=1.5, lam_true=15.0, theta_true=0.3,
                                      label="k=1.5 (rosnacy hazard), theta=0.3 (kruchosc umiarkowana)"),
        test_parameter_recovery_test7(group_specs, k_true=0.7, lam_true=25.0, theta_true=0.6,
                                      label="k=0.7 (malejacy hazard/grupowanie), theta=0.6 (kruchosc silna)"),
    ]
    out["frailty_boundary_collapse"] = test_frailty_boundary_collapse_test7(group_specs)
    out["censoring_realism"] = censoring_realism_check(intervals_csv, group_specs)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intervals", default="test7_intervals.csv")
    ap.add_argument("--run-real", action="store_true",
                    help="ZABLOKOWANE — Etap B (D-029), STOP przed przeglądem")
    a = ap.parse_args()
    if a.run_real:
        raise SystemExit("Etap B Testu 7: uruchamianie na danych rzeczywistych zablokowane do "
                         "przeglądu kodu (brief §8, D-029). Usuń --run-real dopiero po akceptacji.")
    print("Etap B Testu 7: kod gotowy do przeglądu. Użyj --run-real po akceptacji.")


if __name__ == "__main__":
    main()
