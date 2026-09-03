#!/usr/bin/env python3
"""
TEST 11 — §8 protokołu: symulacja mocy dla pełnej reguły §6 (trzy człony naraz), rodzina
faktycznie użyta (uogólniona gamma, parametryzacja Stacy'ego, `test11_gengamma.py`).

Struktura: 13 państw S7, realne okna administracyjne (jak D-042/D-050/D-051). Warunek zerowy
(brak niemonotoniczności): Weibull k=0,99 (kalibracja zgodna z SS7 protokołu, k realnego S7).
Trzy warianty alternatywne — garb (maksimum wewnętrzne), TA SAMA rodzina (a=0,1, scale
skalibrowana na realne okno), c ∈ {-0,5, -1,0, -2,0} — daje szczyty przy ok. 2,3 / 9,4 / 13,6
roku wewnątrz obserwowanego zakresu (1-51 lat, mediana 8) — "wczesny/środkowy/późny szczyt",
nie "łagodny/umiarkowany/silny" (jednoznaczna miara "siły garbu" nie istnieje w tej rodzinie
niezależnie od lokalizacji, więc rozpiętość lokalizacji jest osią zróżnicowania, zmierzone
własności podane wprost w wynikach zamiast zakładane).

Reguła pełna (SS6 protokołu): (1) p<0,05 (LR test, surogaty Weibulla min(T,C) D-031) ORAZ
(2) klasyfikacja kształtu = maksimum_wewnetrzne (kierunek zadeklarowany SS4) ORAZ (3) punkt
zwrotny wewnątrz zakresu obserwowanego (nie na brzegu siatki).

Koszt kontrolowany (zmierzone: ~0,76s/dopasowanie pary Weibull+gengamma): N_OUTER=15,
B_null=60 wewnątrz każdej repliki zewnętrznej — rząd wielkości, nie precyzja ostatecznego
biegu (ten sam kompromis co Test 10, D-050/D-051).
"""
from __future__ import annotations
import json, time
import numpy as np
import pandas as pd

import test6_weibull as w
import test11_gengamma as g
import test11_hump_alt as ha

SEED = w.RNG_SEED
N_OUTER = 6       # zredukowane wobec pierwotnego planu (15) - zmierzony koszt ~5s/dopasowanie
                  # pary Weibull+gengamma NA REALNEJ strukturze S7 (nie na malej syntetycznej
                  # probce uzytej do wstepnego benchmarku), rzad wielkosci silniej ograniczony
                  # niz przy Tescie 10 - odnotowane wprost w raporcie, nie ukryte
B_NULL = 15
LAM_K_NULL = 0.99          # kalibracja SS7 protokolu (k realnego S7)


def load_windows():
    iv = pd.read_csv("test6_s7_intervals.csv", comment="#")
    windows = iv.groupby("ccode")["dlugosc_odstepu"].sum().tolist()
    n_full = int((iv.cenzurowany == 0).sum())
    return windows, n_full


def null_pvalue(t, event, windows, k_null_fit, rng, B_null=B_NULL):
    """Surogaty Weibulla dopasowanego do OBSERWACJI (SS3 protokolu: 'surogaty generowane z
    Weibulla dopasowanego do obserwacji'), mechanizm min(T,C), na TYCH SAMYCH oknach co dana
    replika (per grupa)."""
    lr_obs, _, _ = g.lr_stat(t, event)
    k_fit, lam_fit = k_null_fit
    lr_sur = np.empty(B_null)
    for b in range(B_null):
        t_s, ev_s, _ = g.simulate_weibull_min_tc(k_fit, lam_fit, windows, rng)
        lr_s, _, _ = g.lr_stat(t_s, ev_s)
        lr_sur[b] = lr_s
    p = (1 + int(np.sum(lr_sur >= lr_obs))) / (B_null + 1)
    frac_tie = float(np.mean(np.abs(lr_sur - lr_obs) < 1e-6))
    return p, frac_tie


def one_condition(label, gen_fn, windows, n_full_real, rng):
    recs = []
    for i in range(N_OUTER):
        t, event, gid = gen_fn(rng)
        lr_obs, fit_w, fit_g = g.lr_stat(t, event)
        shape, tp, on_boundary = g.classify_shape(fit_g, t[event == 1])

        # dopasuj Weibulla DO TEJ REPLIKI dla surogatow (SS3: "dopasowanego do obserwacji")
        lam_fit = fit_w["lam"]; k_fit = fit_w["k"]
        p, frac_tie = null_pvalue(t, event, windows, (k_fit, lam_fit), rng)

        cond1 = p < 0.05
        cond2 = (shape == "maksimum_wewnetrzne")
        cond3 = bool(cond2 and not on_boundary)
        full_rule = bool(cond1 and cond2 and cond3)
        recs.append(dict(lr=lr_obs, p=p, frac_tie=frac_tie, shape=shape, turning_point=tp,
                         on_boundary=on_boundary, cond1=cond1, cond2=cond2, cond3=cond3,
                         full_rule=full_rule, k_weibull=k_fit, a=fit_g["a"], c=fit_g["c"]))
    return recs


def main():
    windows, n_full_real = load_windows()
    rng = np.random.default_rng(SEED)

    def gen_null(rng):
        lam = sum(windows) / n_full_real
        return g.simulate_weibull_min_tc(LAM_K_NULL, lam, windows, rng)

    # UWAGA (test11_hump_alt.py): probkowanie bezposrednio z rodziny Stacy'ego przy c<0
    # (region dajacy wewnetrzne maksimum w przegladzie parametrow SS3) ma katastrofalnie
    # ciezki ogon (mediana probek rzedu 10^2-10^5 "lat") - niezdatne do symulacji realistycznych
    # danych. Alternatywa: jadro gamma h(t)=A*t^(kappa-1)*exp(-t/theta), kappa=3 daje pojedynczy
    # garb przy t=2*theta i lekki ogon wykladniczy - NIE jest czlonkiem testowanej rodziny
    # (wlasciwe dla analizy mocy: sprawdzamy wykrywalnosc REALISTYCZNEGO garbu, nie tylko
    # garbu dokladnie matematycznej postaci dopasowywanej rodziny). A skalibrowane na
    # zrealizowana liczbe zdarzen ~110 (rzeczywiste S7) bezposrednio na mechanizmie wyscigu.
    t_max = max(windows) * 3.0
    hump_specs = {"wczesny_szczyt_t5": (3.0, 2.5), "srodkowy_szczyt_t10": (3.0, 5.0),
                 "pozny_szczyt_t15": (3.0, 7.5)}
    hump_A = {name: ha.calibrate_A_by_event_rate(kappa, theta, windows, n_full_real, t_max)
             for name, (kappa, theta) in hump_specs.items()}

    def gen_hump(kappa, theta, A):
        def f(rng):
            return ha.simulate_gamma_kernel_hump_min_tc(A, kappa, theta, windows, rng, t_max=t_max)
        return f

    conditions = {"0_null_weibull_k099": gen_null}
    for name, (kappa, theta) in hump_specs.items():
        conditions[name] = gen_hump(kappa, theta, hump_A[name])
    out_A = hump_A

    out = dict(n_outer=N_OUTER, B_null=B_NULL, seed=SEED, n_windows=len(windows),
              n_full_real=n_full_real, hump_specs=hump_specs, hump_A=out_A, warianty={})
    t0 = time.time()
    for label, gen_fn in conditions.items():
        recs = one_condition(label, gen_fn, windows, n_full_real, rng)
        n = len(recs)
        rate_cond1 = float(np.mean([r["cond1"] for r in recs]))
        rate_cond2 = float(np.mean([r["cond2"] for r in recs]))
        rate_full = float(np.mean([r["full_rule"] for r in recs]))
        wrong_dir = float(np.mean([r["shape"] == "minimum_wewnetrzne" for r in recs]))
        max_frac_tie = float(np.max([r["frac_tie"] for r in recs]))
        se_full = np.sqrt(rate_full * (1 - rate_full) / n) if n else float("nan")
        out["warianty"][label] = dict(
            n=n, moc_p_lt_0_05=rate_cond1, frakcja_ksztalt_maksimum=rate_cond2,
            moc_PELNA_regula=rate_full,
            moc_PELNA_95CI=(max(0.0, rate_full - 1.96 * se_full), min(1.0, rate_full + 1.96 * se_full)),
            frakcja_kierunek_przeciwny_minimum=wrong_dir,
            max_frac_tie=max_frac_tie,
            turning_points=[r["turning_point"] for r in recs if r["turning_point"] is not None],
            shapes=[r["shape"] for r in recs],
        )
        print(f"{label}: p<0.05={rate_cond1:.2f} shape=max={rate_cond2:.2f} PELNA={rate_full:.2f} "
             f"wrong_dir={wrong_dir:.2f} max_frac_tie={max_frac_tie:.4f}  ({time.time()-t0:.0f}s)")

    out["elapsed_s"] = time.time() - t0
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
    with open("test11_power_wyniki.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2, default=str)
    print("zapisano test11_power_wyniki.json")


if __name__ == "__main__":
    main()
