#!/usr/bin/env python3
"""
TEST 13 — bieg decydujacy (Etap 4). ZBUDOWANY PRZY ZAMROZENIU PROTOKOLU (TEST13_PROTOCOL_
trend_ksztaltu.md, D-064), NIE URUCHOMIONY. Wymaga osobnej, wyraznej autoryzacji autora
(SS10 protokolu) przed wykonaniem - liczy decydujace dopasowanie do rzeczywistych,
obserwowanych danych (b_obs), co jest granica, ktorej nie wolno przekraczac bez autoryzacji.

Uzywa DOKLADNIE tej samej puli zerowej (B=2000, ziarno 20260823), ktora zostala juz
wygenerowana i zweryfikowana w D-063 (test13_n3.run_n3) oraz D-064 (test13_etap2,
pomiar 2) - identyczna procedura, identyczny wynik (center=-0,1030, SD=0,0425),
potwierdzone jako reprodukowalne (test13_n3_charakterystyka.json ==
test13_etap2_wyniki.json['pomiar2_falszywe_odrzucen']).
"""
from __future__ import annotations
import json
import numpy as np

import test12_run as r12
import test13_trend as tr
import test13_n3 as n3

B_NULL = 2000
SEED = tr.RNG_SEED  # 20260823, potwierdzone przy zamrozeniu (SS5/SS10 protokolu)


def load_real_decisive_data(path="test12_intervals_prog3.csv", exclude_t0=True):
    """Te same 294 obserwacje, ktore zasilaja model zerowy (SS2/SS5 protokolu):
    dlugosc/cenzurowanie realne, rok startu = ep_end (fakt egzogeniczny)."""
    import pandas as pd
    df = pd.read_csv(path, comment="#")
    if exclude_t0:
        df = df[df.t0_flag == 0]
    grouped = r12.load_grouped(path, exclude_t0=exclude_t0)
    diads, t, event = r12.flatten(grouped)
    # rok startu per wiersz - potrzebny do year_c; flatten nie niesie roku, wiec
    # budujemy rownolegle z surowego df w tej samej kolejnosci grupowania
    starts = []
    for d, g in df.groupby("dyad_id"):
        t_full_rows = g.loc[g.cenzurowany == 0]
        c_rows = g.loc[g.cenzurowany == 1]
        for _, row in t_full_rows.iterrows():
            starts.append(row["ep_end"])
        if len(c_rows):
            starts.append(c_rows.iloc[0]["ep_end"])
    starts = np.array(starts, dtype=float)
    assert len(starts) == len(t), "niezgodnosc dlugosci - kolejnosc grupowania musi byc identyczna"
    year_c = starts - 1985.0
    return t, event, year_c, diads


def run_decisive(B=B_NULL, seed=SEED):
    t, event, year_c, diads = load_real_decisive_data()
    fit_obs = tr.fit_trend(t, event, year_c)
    b_obs = fit_obs["b"]

    null_out, b_sur = n3.run_n3(b_obs=None, B=B, seed=seed)
    center_null = null_out["b_sur_mean"]
    sd_null = null_out["b_sur_sd"]

    frac_tie = float(np.mean(np.abs(b_sur - b_obs) < 1e-6))
    if frac_tie > n3.TIE_FRAC_STOP:
        raise AssertionError(f"SS5 protokolu: {frac_tie:.1%} surogatow N3 remisuje - zatrzymuje.")

    dist_obs = abs(b_obs - center_null)
    p = (1 + int(np.sum(np.abs(b_sur - center_null) >= dist_obs))) / (B + 1)

    efekt = b_obs - center_null
    ci_lo, ci_hi = efekt - 1.96 * sd_null, efekt + 1.96 * sd_null

    if p < 0.05:
        klasyfikacja = "wsparty"
    elif p < 0.10:
        klasyfikacja = "graniczny"
    else:
        klasyfikacja = "niewsparty"

    return dict(
        n=len(t), n_pelnych=int((event == 1).sum()), n_cenzurowanych=int((event == 0).sum()),
        b_obs=b_obs, a_obs=fit_obs["a"], lam_obs=fit_obs["lam"],
        center_null=center_null, sd_null=sd_null, B=B, seed=seed,
        efekt=efekt, efekt_CI95_przyblizony=(ci_lo, ci_hi),
        frac_tie=frac_tie, p=p, klasyfikacja=klasyfikacja,
    )


if __name__ == "__main__":
    raise SystemExit(
        "STOP (SS10 protokolu): bieg decydujacy wymaga osobnej, wyraznej autoryzacji "
        "autora. Skrypt zbudowany i gotowy do przegladu; nie uruchamiaj automatycznie."
    )
