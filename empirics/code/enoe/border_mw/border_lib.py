"""Estimation tools for study 9.4: two-way fixed-effects regressions on municipality x quarter
cells, cluster-robust variances and the wild cluster bootstrap (pre-analysis plan §3).

The fixed effects are partialled out by a weighted QR projection on the dummies (Frisch-Waugh),
which is exact on unbalanced panels. The wild bootstrap imposes the null (restricted residuals),
uses Rademacher weights by cluster and the CR1 t or Wald statistic, following Cameron, Gelbach and
Miller (2008) and MacKinnon and Webb (2018).
"""
import numpy as np
import pandas as pd


class Projector:
    """Weighted projection off a set of fixed effects. `fe` is a DataFrame of id columns; `w` the
    regression weights. Apply with .resid(v) to an (n,) or (n, k) array."""

    def __init__(self, fe, w):
        self.sw = np.sqrt(np.asarray(w, float))
        cols = []
        for j, c in enumerate(fe.columns):
            d = pd.get_dummies(fe[c].astype(str), drop_first=j > 0).to_numpy(float)
            cols.append(d)
        D = np.hstack(cols) * self.sw[:, None]
        q, r = np.linalg.qr(D)
        keep = np.abs(np.diag(r)) > 1e-10 * np.abs(np.diag(r)).max()
        self.Q = q[:, keep]

    def resid(self, v):
        v = np.asarray(v, float)
        one = v.ndim == 1
        v = v[:, None] if one else v
        s = v * self.sw[:, None]
        out = (s - self.Q @ (self.Q.T @ s)) / self.sw[:, None]
        return out[:, 0] if one else out


def _ols(yt, Xt, w):
    XtW = Xt.T * w
    A = XtW @ Xt
    b = np.linalg.solve(A, XtW @ yt)
    return b, np.linalg.inv(A)


def _cluster_matrix(cl):
    from scipy import sparse
    codes, inv = np.unique(np.asarray(cl), return_inverse=True)
    return sparse.csr_matrix((np.ones(len(inv)), (inv, np.arange(len(inv)))), shape=(len(codes), len(inv)))


def cr1(Xt, e, w, cl, Ainv, C=None):
    """CR1 cluster-robust variance for a weighted regression on partialled-out regressors."""
    n, k = Xt.shape
    C = _cluster_matrix(cl) if C is None else C
    S = C @ (Xt * (w * e)[:, None])
    G = S.shape[0]
    c = G / (G - 1) * (n - 1) / max(n - k, 1)
    return c * Ainv @ (S.T @ S) @ Ainv


def fit(y, X, fe, w, cl, proj=None):
    """Weighted two-way FE regression of y on X (n x k). Returns dict with b, V (CR1), partialled
    arrays and the projector."""
    y, X, w = np.asarray(y, float), np.atleast_2d(np.asarray(X, float).T).T, np.asarray(w, float)
    P = proj or Projector(fe, w)
    yt, Xt = P.resid(y), P.resid(X)
    b, Ainv = _ols(yt, Xt, w)
    e = yt - Xt @ b
    V = cr1(Xt, e, w, cl, Ainv)
    return {"b": b, "V": V, "yt": yt, "Xt": Xt, "e": e, "Ainv": Ainv, "proj": P, "G": len(np.unique(cl))}


def _rademacher(cl, B, rng):
    codes, inv = np.unique(np.asarray(cl), return_inverse=True)
    W = rng.choice([-1.0, 1.0], size=(len(codes), B))
    return W[inv]


def wild_wald(f, w, cl, idx, r0=None, B=1999, seed=0):
    """Restricted wild cluster bootstrap p-value for H0: b[idx] = r0, using the CR1 Wald statistic
    (t^2 for one restriction). `f` is the output of fit()."""
    idx = list(np.atleast_1d(idx))
    r0 = np.zeros(len(idx)) if r0 is None else np.atleast_1d(np.asarray(r0, float))
    yt, Xt, Ainv = f["yt"], f["Xt"], f["Ainv"]
    k = Xt.shape[1]
    free = [j for j in range(k) if j not in idx]

    def wald(b, V):
        d = b[idx] - r0
        return float(d @ np.linalg.pinv(V[np.ix_(idx, idx)]) @ d)

    W0 = wald(f["b"], f["V"])
    # restricted fit: y - X_idx r0 on the free regressors
    yr = yt - Xt[:, idx] @ r0
    if free:
        br, _ = _ols(yr, Xt[:, free], w)
        fitted = Xt[:, free] @ br + Xt[:, idx] @ r0
    else:
        fitted = Xt[:, idx] @ r0
    u = yt - fitted
    rng = np.random.default_rng(seed)
    Wb = _rademacher(cl, B, rng)
    Ystar = fitted[:, None] + u[:, None] * Wb
    Ystar = f["proj"].resid(Ystar)          # flipping clusters breaks orthogonality to the FE
    XtW = Xt.T * w
    Bs = Ainv @ (XtW @ Ystar)               # k x B
    E = Ystar - Xt @ Bs
    C = _cluster_matrix(cl)
    n = Xt.shape[0]
    G = C.shape[0]
    cadj = G / (G - 1) * (n - 1) / max(n - k, 1)
    if k == 1:
        S = C @ (Xt[:, 0][:, None] * w[:, None] * E)              # G x B
        V = cadj * Ainv[0, 0] ** 2 * (np.asarray(S) ** 2).sum(0)
        stats = (Bs[0] - r0[0]) ** 2 / V
    else:
        stats = np.empty(B)
        for j in range(B):
            V = cr1(Xt, E[:, j], w, cl, Ainv, C)
            stats[j] = wald(Bs[:, j], V)
    return {"stat": W0, "p": float((stats >= W0).mean())}


def wild_ci(f, w, cl, j=0, level=0.90, B=999, npts=41, seed=0):
    """Confidence interval for b[j] by inverting the restricted wild bootstrap test on a grid of
    +-4 CR1 standard errors around the estimate (refined linearly between grid points)."""
    b, se = f["b"][j], np.sqrt(f["V"][j, j])
    grid = np.linspace(b - 4 * se, b + 4 * se, npts)
    ps = np.array([wild_wald(f, w, cl, j, r0=g, B=B, seed=seed)["p"] for g in grid])
    alpha = 1 - level
    acc = ps >= alpha
    if not acc.any():
        return np.nan, np.nan
    i0, i1 = np.argmax(acc), len(acc) - 1 - np.argmax(acc[::-1])

    def cross(a, c):
        if a < 0 or c >= len(grid):
            return grid[min(max(a, 0), len(grid) - 1)]
        pa, pc = ps[a], ps[c]
        return grid[a] + (alpha - pa) * (grid[c] - grid[a]) / (pc - pa) if pc != pa else grid[c]

    lo = cross(i0 - 1, i0) if i0 > 0 else -np.inf
    hi = cross(i1 + 1, i1) if i1 < len(grid) - 1 else np.inf
    return lo, hi


def did(cells, y, treat="zlfn", post="post", unit="mid", time="t", weight="w", B=1999, ci=True, fe_extra=None):
    """Difference in differences on cells (pre-analysis plan §3): unit and time effects (or the
    columns in fe_extra), clustered by unit, wild bootstrap p-value and interval."""
    d = cells.dropna(subset=[y, weight])
    d = d[d[weight] > 0]
    X = (d[treat].astype(float) * d[post].astype(float)).to_numpy()
    fe = d[[unit] + (fe_extra or [time])]
    f = fit(d[y], X, fe, d[weight], d[unit])
    out = {"outcome": y, "beta": f["b"][0], "se_cr1": np.sqrt(f["V"][0, 0]), "clusters": f["G"],
           "treated_clusters": d.loc[d[treat].astype(bool), unit].nunique(), "cells": len(d)}
    out["p_wild"] = wild_wald(f, d[weight].to_numpy(), d[unit].to_numpy(), 0, B=B)["p"]
    if ci:
        out["lo90"], out["hi90"] = wild_ci(f, d[weight].to_numpy(), d[unit].to_numpy(), 0, B=max(B // 2, 499))
    return out


def event_study(cells, y, ref, treat="zlfn", unit="mid", time="t", weight="w", B=999, pre=None):
    """One coefficient per period relative to `ref`; CR1 intervals and a restricted wild bootstrap
    Wald test that the pre-period coefficients (periods in `pre`) are jointly zero."""
    d = cells.dropna(subset=[y, weight])
    d = d[d[weight] > 0]
    periods = [p for p in sorted(d[time].unique()) if p != ref]
    X = np.column_stack([(d[treat].astype(bool) & (d[time] == p)).to_numpy(float) for p in periods])
    f = fit(d[y], X, d[[unit, time]], d[weight], d[unit])
    se = np.sqrt(np.diag(f["V"]))
    rows = [{"outcome": y, "t": p, "beta": b, "se_cr1": s} for p, b, s in zip(periods, f["b"], se)]
    rows.append({"outcome": y, "t": ref, "beta": 0.0, "se_cr1": 0.0})
    res = pd.DataFrame(rows).sort_values("t")
    pt = np.nan
    if pre:
        idx = [i for i, p in enumerate(periods) if p in pre]
        pt = wild_wald(f, d[weight].to_numpy(), d[unit].to_numpy(), idx, B=B)["p"]
    return res, pt
