"""Three-sector model of unbalanced growth for the explainer page (theory note
docs/theory/04_unbalanced_growth_and_reallocation.md; D-070).

No data are used: the page solves this closed-form model live from the slider values.

Sectors
    P  progressive goods (productivity grows fast; where innovating firms concentrate)
    R  protected services and inputs (energy, telecom, finance, licensed professions)
    S  stagnant personal services (mostly replicative, often informal)

Technology and prices. Labour is the only input: Y_i = A_i L_i, A_i(t) = exp(g_i t).
Prices are a markup over unit labour cost, p_i = mu_i w_i / A_i, so nominal value
added per worker is p_i A_i = mu_i w_i.

Wages. w_i(t) = rho_i exp(phi g_i t): rho_S = rho <= 1 is the informal wage relative
to the formal wage, and phi in [0, 1) is the share of a sector's productivity growth
kept as higher wages in that sector (segmented labour markets). phi = 0 and rho = 1
is Baumol's case of one economy-wide wage.

Markups. mu_P = mu_S = 1; mu_R(t) = exp(m t), so m > 0 is a rising markup in the
protected sector.

Demand. CES over the three goods with elasticity eps and weights omega, so the
nominal spending share of sector i is s_i = omega_i p_i^(1-eps) / sum_j omega_j p_j^(1-eps).
Employment follows from spending: L_i = s_i E / (mu_i w_i), normalised to sum to one.

Decomposition (McMillan and Rodrik 2011; static/dynamic split of de Vries et al. 2015),
year t -> t+1, value added per worker y_i valued at fixed prices:
    within  = sum_i l_i,t (y_i,t+1 - y_i,t)
    static  = sum_i y_i,t (l_i,t+1 - l_i,t)
    dynamic = sum_i (y_i,t+1 - y_i,t)(l_i,t+1 - l_i,t)
expressed as percentage points of the year-t level. 'chained' values each year at the
prices of year t (as in the repository's period decompositions, D-024); 'fixed' values
every year at the prices of year 0 (a distant constant-price base).
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd

SECTORS = ("P", "R", "S")
LABELS = {"P": "Progressive goods", "R": "Protected services", "S": "Personal services"}


@dataclass(frozen=True)
class Params:
    g_P: float = 0.030      # productivity growth, progressive goods (per year)
    g_R: float = 0.010      # productivity growth, protected services
    g_S: float = 0.005      # productivity growth, personal services
    eps: float = 0.5        # elasticity of substitution between the three goods
    w_P: float = 0.40       # demand weights (normalised to sum to one)
    w_R: float = 0.25
    w_S: float = 0.35
    m: float = 0.0          # growth of the markup in R (per year)
    rho: float = 1.0        # informal wage relative to formal wage (sector S)
    phi: float = 0.0        # share of sector productivity growth kept as sector wages
    years: int = 60

    @property
    def g(self):
        return np.array([self.g_P, self.g_R, self.g_S])

    @property
    def omega(self):
        w = np.array([self.w_P, self.w_R, self.w_S], dtype=float)
        return w / w.sum()


PRESETS = {
    "Baumol: one wage, no markups": Params(),
    "Dual economy: informal wage gap and segmented wages": Params(rho=0.45, phi=0.5),
    "Dual economy with rising markups in protected services": Params(rho=0.45, phi=0.5, m=0.01),
}


def solve(p: Params) -> pd.DataFrame:
    """Levels by year and sector: A, w, mu, price, spending share s, employment share l,
    nominal value added per worker (mu*w), real output per worker of the economy."""
    t = np.arange(p.years + 1)[:, None]
    A = np.exp(p.g * t)
    rho = np.array([1.0, 1.0, p.rho])
    w = rho * np.exp(p.phi * p.g * t)
    mu = np.ones_like(A)
    mu[:, 1] = np.exp(p.m * t[:, 0])
    price = mu * w / A
    num = p.omega * price ** (1 - p.eps)
    s = num / num.sum(axis=1, keepdims=True)
    lab = s / (mu * w)
    l = lab / lab.sum(axis=1, keepdims=True)
    rows = []
    for k, sec in enumerate(SECTORS):
        rows.append(pd.DataFrame({"t": t[:, 0], "sector": sec, "A": A[:, k], "w": w[:, k], "mu": mu[:, k],
                                  "price": price[:, k], "s": s[:, k], "l": l[:, k],
                                  "va_per_worker_nominal": mu[:, k] * w[:, k]}))
    return pd.concat(rows, ignore_index=True)


def _wide(df, col):
    return df.pivot(index="t", columns="sector", values=col)[list(SECTORS)].to_numpy()


def decompose(df: pd.DataFrame, prices: str = "chained") -> pd.DataFrame:
    """Annual within / static / dynamic terms (percentage points of the year-t level)."""
    A, price, l = _wide(df, "A"), _wide(df, "price"), _wide(df, "l")
    out = []
    for t in range(len(A) - 1):
        base = price[t] if prices == "chained" else price[0]
        y0, y1 = base * A[t], base * A[t + 1]
        dl = l[t + 1] - l[t]
        P0 = (l[t] * y0).sum()
        within = (l[t] * (y1 - y0)).sum()
        static = (y0 * dl).sum()
        dynamic = ((y1 - y0) * dl).sum()
        total = (l[t + 1] * y1).sum() - P0
        out.append({"t": t + 1, "within": 100 * within / P0, "static": 100 * static / P0,
                    "dynamic": 100 * dynamic / P0, "total": 100 * total / P0})
    return pd.DataFrame(out)


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate real output per worker (chained Laspeyres index, year 0 = 1) and the
    aggregate price deflator implied by nominal output per worker."""
    d = decompose(df, "chained")
    index = np.concatenate([[1.0], np.cumprod(1 + d["total"].to_numpy() / 100)])
    nominal = (df.assign(x=df["l"] * df["va_per_worker_nominal"]).groupby("t")["x"].sum()).to_numpy()
    return pd.DataFrame({"t": np.arange(len(index)), "real_lp": index, "nominal_lp": nominal,
                         "deflator": nominal / nominal[0] / index})


def baumol_slope(df: pd.DataFrame) -> pd.DataFrame:
    """Across sectors, over the whole horizon: change in the log relative price against the
    change in log relative real productivity (both relative to the economy). Returns one row per
    sector and the OLS slope in df.attrs['slope']. Identity: slope = -1 + cov(dln mu + dln w, dln A)
    / var(dln A); with m = 0 it equals -(1 - phi)."""
    ag = aggregate(df)
    T = df["t"].max()
    a = df[df["t"] == 0].set_index("sector").loc[list(SECTORS)]
    b = df[df["t"] == T].set_index("sector").loc[list(SECTORS)]
    x = np.log(b["A"] / a["A"]) - np.log(ag["real_lp"].iloc[-1])
    y = np.log(b["price"] / a["price"]) - np.log(ag["deflator"].iloc[-1])
    xc, yc = x - x.mean(), y - y.mean()
    slope = float((xc * yc).sum() / (xc ** 2).sum())
    res = pd.DataFrame({"sector": list(SECTORS), "real_rel_change": x.to_numpy() / T * 100,
                        "price_rel_change": y.to_numpy() / T * 100})
    res.attrs["slope"] = slope
    return res
