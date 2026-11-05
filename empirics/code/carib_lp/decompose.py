"""McMillan–Rodrik decomposition of labour-productivity growth (D-024, D-026).

For a period t0 -> T, with sector labour productivity p_i = Y_i / L_i, employment
shares s_i = L_i / L, and aggregate P = sum_i Y_i / L:

    P_T - P_0 = sum_i s_i0 (p_iT - p_i0)        within-sector
              + sum_i p_iT (s_iT - s_i0)        structural change (McMillan & Rodrik 2011)

The structural term splits further into static  sum_i p_i0 (s_iT - s_i0)
and dynamic sum_i (p_iT - p_i0)(s_iT - s_i0) (de Vries et al. 2015).

Price base (D-024). UN constant-price series are chain-linked and not additive
across sectors outside 2020, and a distant base year mis-weights sectors whose
relative prices moved a lot (oil, gold, bauxite). Each period is therefore
valued at the prices of its own initial year:
    Y_i0 = current-price VA_i(t0)
    Y_iT = current-price VA_i(t0) * [constant-price VA_i(T) / constant-price VA_i(t0)]
so sectors add up exactly and aggregate growth is a Laspeyres volume index.
'final' uses the prices of year T instead (Paasche); used as a robustness check.

Terms are reported as contributions to annual growth: term / P_0 / years * 100
(percentage points per year, linear), so within + structural = average annual
growth of P (linear).
"""
import numpy as np
import pandas as pd

GRID_A = {"AGR": "AGR", "MIU": "MIU", "MAN": "MAN", "CON": "CON", "TRH": "TRH", "TSC": "TSC", "OTH": "OTH"}
GRID_B = {"AGR": "AGR", "MIU": "MIU", "MAN": "MAN", "CON": "CON", "TRH": "SER", "TSC": "SER", "OTH": "SER"}
GRIDS = {"A": GRID_A, "B": GRID_B}


def va_at_prices(va, iso, t0, T, base="initial", grid=GRID_A, drop=()):
    """Sector VA at t0 and T valued at the prices of t0 ('initial') or T ('final').

    va: DataFrame indexed by (iso3, year, sector) with columns va_cur_usd, va_k2020usd
    (7 sectors). Returns DataFrame indexed by grid sector with columns y0, yT.
    """
    v = va.loc[iso]
    a, b = v.loc[t0], v.loc[T]
    vol = b["va_k2020usd"] / a["va_k2020usd"]
    if base == "initial":
        y0, yT = a["va_cur_usd"], a["va_cur_usd"] * vol
    elif base == "final":
        y0, yT = b["va_cur_usd"] / vol, b["va_cur_usd"]
    else:
        raise ValueError(base)
    out = pd.DataFrame({"y0": y0, "yT": yT})
    out = out[~out.index.isin(drop)]
    return out.groupby(out.index.map(grid)).sum()


def decompose(y, l0, lT, years):
    """y: DataFrame (sector -> y0, yT); l0, lT: Series sector -> employment.
    Returns dict of terms in pp per year plus levels."""
    sec = y.index.intersection(l0.index).intersection(lT.index)
    if len(sec) != len(y.index):
        return None
    y, l0, lT = y.loc[sec], l0.loc[sec], lT.loc[sec]
    p0, pT = y["y0"] / l0, y["yT"] / lT
    s0, sT = l0 / l0.sum(), lT / lT.sum()
    P0, PT = y["y0"].sum() / l0.sum(), y["yT"].sum() / lT.sum()
    within = (s0 * (pT - p0)).sum()
    struct = (pT * (sT - s0)).sum()
    static = (p0 * (sT - s0)).sum()
    dynamic = ((pT - p0) * (sT - s0)).sum()
    k = 100 / P0 / years
    res = {
        "P0": P0, "PT": PT,
        "growth_pp": (PT - P0) * k,
        "within_pp": within * k,
        "struct_pp": struct * k,
        "static_pp": static * k,
        "dynamic_pp": dynamic * k,
        "emp_growth_pct": 100 * ((lT.sum() / l0.sum()) ** (1 / years) - 1),
        "check": (within + struct) / (PT - P0) - 1 if PT != P0 else 0.0,
    }
    # sector detail for scatter plots: relative productivity and share change
    res["detail"] = pd.DataFrame({"p0_rel": p0 / P0, "pT_rel": pT / PT, "s0": s0, "sT": sT,
                                  "dshare_pp": 100 * (sT - s0),
                                  "within_contrib_pp": s0 * (pT - p0) * k,
                                  "struct_contrib_pp": pT * (sT - s0) * k})
    return res
