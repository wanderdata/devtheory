"""Panel estimators for WP07.

Random, fixed and between effects come from `linearmodels` (cluster-robust standard errors by
country). Hausman–Taylor (1981) has no standard Python implementation, so it is written here
from the GLS-IV formulas (Baltagi, Econometric Analysis of Panel Data, ch. 7) and validated in
tests/test_estimators.py against the Cornwell–Rupert wage panel, whose HT estimates are
reported in Baltagi's textbook and in Stata's xthtaylor manual (OQ-49).

Hausman–Taylor model:  y_it = X1_it b1 + X2_it b2 + Z1_i g1 + Z2_i g2 + u_i + e_it
  X1 exogenous time-varying, X2 endogenous time-varying (correlated with u_i),
  Z1 exogenous time-invariant (includes the constant), Z2 endogenous time-invariant.
Instruments: within deviations of X1 and X2, individual means of X1, and Z1.
Identification needs at least as many variables in X1 as in Z2.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
from linearmodels.panel import BetweenOLS, PanelOLS, RandomEffects
from scipy import stats


@dataclass
class Result:
    params: pd.Series
    se: pd.Series
    nobs: int
    ngroups: int
    estimator: str
    extra: dict
    cov: pd.DataFrame = None

    @property
    def pvalues(self):
        return pd.Series(2 * stats.norm.sf(np.abs(self.params / self.se)), index=self.params.index)

    def table(self):
        return pd.DataFrame({"coef": self.params, "se": self.se, "p": self.pvalues})


def _prep(df, y, xs, entity, time):
    d = df[[entity, time, y] + xs].dropna().copy()
    return d.set_index([entity, time])


def fe(df, y, xs, entity="iso3", time="period", time_effects=True):
    d = _prep(df, y, xs, entity, time)
    r = PanelOLS(d[y], d[xs], entity_effects=True, time_effects=time_effects, drop_absorbed=True,
                 check_rank=False).fit(cov_type="clustered", cluster_entity=True)
    return Result(r.params, r.std_errors, int(r.nobs), int(r.entity_info["total"]), "FE", {}, r.cov)


def re(df, y, xs, entity="iso3", time="period", time_dummies=()):
    d = _prep(df, y, list(xs) + list(time_dummies), entity, time)
    X = d[list(xs) + list(time_dummies)].assign(const=1.0)
    r = RandomEffects(d[y], X, check_rank=False).fit(cov_type="clustered", cluster_entity=True)
    return Result(r.params, r.std_errors, int(r.nobs), int(r.entity_info["total"]), "RE", {}, r.cov)


def be(df, y, xs, entity="iso3", time="period"):
    d = _prep(df, y, xs, entity, time)
    X = d[xs].assign(const=1.0)
    r = BetweenOLS(d[y], X, check_rank=False).fit(cov_type="robust")
    return Result(r.params, r.std_errors, int(r.nobs), int(r.entity_info["total"]), "BE", {}, r.cov)


def _iv(y, X, A):
    """2SLS coefficients of y on X with instrument matrix A."""
    PA_X = A @ np.linalg.lstsq(A, X, rcond=None)[0]
    b = np.linalg.lstsq(PA_X, y, rcond=None)[0]
    return b, PA_X


def hausman_taylor(df, y, x1, x2, z1, z2, entity="iso3", time="period", constant=True):
    """Hausman–Taylor estimator for possibly unbalanced panels.

    Variance components follow the Swamy–Arora-type approach used by Stata's xthtaylor:
    sigma_e^2 from the within regression; sigma_u^2 from the step-2 residual means,
    with a T_i-specific GLS weight theta_i = 1 - sqrt(sigma_e^2 / (T_i sigma_u^2 + sigma_e^2)).
    Standard errors are the conventional GLS-IV ones (sigma_e^2 (X*' P_A X*)^-1).
    """
    cols = [entity, time, y] + list(x1) + list(x2) + list(z1) + list(z2)
    d = df[cols].dropna().sort_values([entity, time]).reset_index(drop=True)
    g = d.groupby(entity)
    Ti = g[y].transform("size").to_numpy(float)
    N, n = d[entity].nunique(), len(d)

    X = d[list(x1) + list(x2)].to_numpy(float)
    Z = d[list(z1) + list(z2)].to_numpy(float)
    if constant:
        Z = np.column_stack([np.ones(n), Z])
    zn = (["const"] if constant else []) + list(z1) + list(z2)
    xn = list(x1) + list(x2)
    yv = d[y].to_numpy(float)

    def mean_(a):
        return pd.DataFrame(a).groupby(d[entity].to_numpy()).transform("mean").to_numpy()

    Xm, ym = mean_(X), mean_(yv.reshape(-1, 1)).ravel()
    Xw, yw = X - Xm, yv - ym
    kx = X.shape[1]

    # Step 1: within estimator
    bw = np.linalg.lstsq(Xw, yw, rcond=None)[0]
    ew = yw - Xw @ bw
    s2e = ew @ ew / (n - N - kx)

    # Step 2: regress d_i = ybar_i - Xbar_i bw on Z, instruments [means of X1, Z1]
    di = ym - Xm @ bw
    k1 = len(x1)
    z1cols = Z[:, : (1 if constant else 0) + len(z1)]
    A2 = np.column_stack([Xm[:, :k1], z1cols])
    if A2.shape[1] < Z.shape[1]:
        raise ValueError("HT not identified: need at least as many X1 as Z2 variables")
    g2, _ = _iv(di, Z, A2)
    e2 = di - Z @ g2

    # Variance of the individual effect
    first = d.groupby(entity).head(1).index
    s2b = np.mean(e2[first] ** 2)
    s2u = max(s2b - s2e * np.mean(1.0 / Ti[first]), 1e-12)

    # Step 3: GLS transform and IV
    theta = 1.0 - np.sqrt(s2e / (Ti * s2u + s2e))
    Xs = X - theta[:, None] * Xm
    Zs = Z - theta[:, None] * Z            # Z is time-invariant: its mean is itself
    ys = yv - theta * ym
    W = np.column_stack([Xs, Zs])
    A = np.column_stack([Xw, Xm[:, :k1], z1cols])
    b, PA_W = _iv(ys, W, A)
    V = s2e * np.linalg.inv(PA_W.T @ PA_W)
    names = xn + zn
    return Result(pd.Series(b, index=names), pd.Series(np.sqrt(np.diag(V)), index=names), n, N, "HT",
                  {"sigma_e": float(np.sqrt(s2e)), "sigma_u": float(np.sqrt(s2u)),
                   "theta_mean": float(np.mean(theta))}, pd.DataFrame(V, index=names, columns=names))
