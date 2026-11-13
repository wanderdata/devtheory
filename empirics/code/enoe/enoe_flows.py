"""States, transition rates and the variance decomposition (pre-analysis plan §§3–5).

State codes: 'N' (not employed) or a job cell 'sector|size|formality'. Rates are weighted by
the origin weight. The decomposition compares how much of the variance of a binary outcome is
explained by sector cells and by size x formality cells (R2 and Shapley shares).
"""
import numpy as np
import pandas as pd

from enoe_config import FORMAL, SIZE


def state(df, sfx=""):
    """Labour-market state from INEGI's precoded variables: clase2 == 1 means employed."""
    emp = df[f"clase2{sfx}"] == 1
    sector = df[f"rama_est2{sfx}"].astype("Int64").astype(str)
    size = df[f"ambito2{sfx}"].map(SIZE).fillna("other or not specified")
    form = df[f"emp_ppal{sfx}"].map(FORMAL).fillna("not specified")
    cell = sector + "|" + size + "|" + form
    return pd.Series(np.where(emp, cell, "N"), index=df.index)


def parts(cell):
    s = cell.str.split("|", expand=True)
    return s[0], s[1] + "|" + s[2]


def rates(origin, dest, weight, by):
    """Weighted exit and persistence rates by origin group `by` (a Series aligned with origin)."""
    d = pd.DataFrame({"o": origin, "d": dest, "w": weight, "g": by})
    d = d[d["o"] != "N"]
    d["exit"] = (d["d"] == "N").astype(float)
    d["stay"] = (d["d"] == d["o"]).astype(float)
    g = d.groupby("g")
    return pd.DataFrame({
        "n": g.size(),
        "exit": g.apply(lambda x: np.average(x["exit"], weights=x["w"]), include_groups=False),
        "persist": g.apply(lambda x: np.average(x["stay"], weights=x["w"]), include_groups=False),
    })


def upward(origin, dest, rank):
    """1 if the destination cell ranks above the origin cell (rank: dict cell -> earnings rank);
    0 if it ranks at or below it or is non-employment; NaN if either cell has no rank."""
    ro, rd = origin.map(rank), dest.map(rank)
    up = (rd > ro).astype(float)
    up[dest == "N"] = 0.0
    up[ro.isna() | (rd.isna() & (dest != "N"))] = np.nan
    return up


def _r2(y, X, w):
    X = np.column_stack([np.ones(len(y)), X]) if X.shape[1] else np.ones((len(y), 1))
    sw = np.sqrt(w)
    b = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]
    e = y - X @ b
    ybar = np.average(y, weights=w)
    return 1 - np.sum(w * e ** 2) / np.sum(w * (y - ybar) ** 2)


def decompose(y, sector, sizeform, w, controls=None):
    """R2 of y on sector dummies, on size x formality dummies, on both, and the Shapley shares of
    the joint R2 (two-group Shapley: average of the marginal contributions in both orders).
    With `controls` (a categorical Series), every model also includes the control dummies and the
    R2 figures are increments over the controls-only model."""
    ok = ~np.isnan(np.asarray(y, float))
    y, w = np.asarray(y, float)[ok], np.asarray(w, float)[ok]
    S = pd.get_dummies(pd.Series(sector)[ok].astype(str), drop_first=True).to_numpy(float)
    K = pd.get_dummies(pd.Series(sizeform)[ok].astype(str), drop_first=True).to_numpy(float)
    if controls is not None:
        C = pd.get_dummies(pd.Series(controls)[ok].astype(str), drop_first=True).to_numpy(float)
    else:
        C = np.empty((len(y), 0))
    r_c = _r2(y, C, w) if C.shape[1] else 0.0
    r_s = _r2(y, np.column_stack([C, S]), w) - r_c
    r_k = _r2(y, np.column_stack([C, K]), w) - r_c
    r_b = _r2(y, np.column_stack([C, S, K]), w) - r_c
    sh_s = 0.5 * (r_s + (r_b - r_k))
    sh_k = 0.5 * (r_k + (r_b - r_s))
    return {"r2_sector": r_s, "r2_sizeform": r_k, "r2_both": r_b,
            "shapley_sector": sh_s, "shapley_sizeform": sh_k, "r2_controls": r_c}
