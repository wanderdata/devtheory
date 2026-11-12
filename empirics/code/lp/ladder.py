"""The productivity ladder: the working-age population distributed over the productivity of
the activity each person works in, with people who are not employed at zero (D-042, D-043).

A ladder is a discrete distribution: a list of (value, weight) pairs, where the weights are
shares of the working-age population and sum to one. With sector data each sector is one step
(its average output per worker), so the ladder ignores dispersion within sectors.

Comparisons between two ladders (functions below):
  dominance(a, b, order=1)  first-order stochastic dominance: b's quantile function lies on
                            or above a's at every percentile (b's CDF on or below a's).
  dominance(a, b, order=2)  second-order (generalised Lorenz): the cumulative area under b's
                            quantile function is at least a's at every percentile. Implies an
                            improvement for any criterion that values more output and gives
                            more weight to the lower percentiles.
  share_gained(a, b)        share of percentiles whose quantile did not fall.
  incidence(a, b, ...)      change in the quantile function at each percentile, as a share of
                            a's mean; its average over percentiles is the change in the mean.
  fgt(dist, z, alpha)       Foster-Greer-Thorbecke indices below a productivity line z:
                            alpha=0 share below z, 1 average gap, 2 squared gap.
"""
import numpy as np

TOL = 1e-9


def make(values, weights):
    """Normalise to a sorted array of values and weights summing to one; drop zero weights."""
    v, w = np.asarray(values, float), np.asarray(weights, float)
    keep = w > 0
    v, w = v[keep], w[keep]
    o = np.argsort(v, kind="stable")
    return v[o], w[o] / w.sum()


def mean(d):
    v, w = d
    return float((v * w).sum())


def cdf(d, x):
    v, w = d
    return np.array([w[v <= xi + TOL * max(1.0, abs(xi))].sum() for xi in np.atleast_1d(x)])


def quantile(d, p):
    """Left-continuous quantile function Q(p) = min{x: F(x) >= p}, for p in (0, 1]."""
    v, w = d
    c = np.cumsum(w)
    idx = np.searchsorted(c, np.atleast_1d(p) - TOL, side="left")
    return v[np.minimum(idx, len(v) - 1)]


def gen_lorenz(d, p):
    """GL(p) = integral of Q from 0 to p (piecewise linear in p)."""
    v, w = d
    c = np.concatenate([[0.0], np.cumsum(w)])
    area = np.concatenate([[0.0], np.cumsum(v * w)])
    out = []
    for pi in np.atleast_1d(p):
        k = np.searchsorted(c, pi, side="right") - 1
        k = min(k, len(v) - 1)
        out.append(area[k] + (pi - c[k]) * v[k])
    return np.array(out)


def _breaks(a, b):
    return np.unique(np.clip(np.concatenate([np.cumsum(a[1]), np.cumsum(b[1]), [0.0, 1.0]]), 0, 1))


def dominance(a, b, order=1):
    """+1 if b dominates a, -1 if a dominates b, 0 if neither (curves cross) or identical.
    Order 1 compares CDFs at every support point; order 2 compares generalised Lorenz curves
    at every breakpoint of either ladder (both are linear between the union of breakpoints)."""
    scale = max(mean(a), mean(b), 1e-12)
    if order == 1:
        xs = np.unique(np.concatenate([a[0], b[0]]))
        diff = cdf(a, xs) - cdf(b, xs)               # >= 0 everywhere when b dominates
        tol = TOL
    elif order == 2:
        ps = _breaks(a, b)
        diff = (gen_lorenz(b, ps) - gen_lorenz(a, ps)) / scale
        tol = TOL
    else:
        raise ValueError(order)
    if np.all(np.abs(diff) <= tol):
        return 0
    if np.all(diff >= -tol):
        return 1
    if np.all(diff <= tol):
        return -1
    return 0


def share_gained(a, b):
    """Share of percentiles at which b's quantile function is at or above a's (1 under
    first-order dominance of b). Measured exactly on the union of both ladders' breakpoints."""
    ps = _breaks(a, b)
    widths = ps[1:] - ps[:-1]
    mids = (ps[:-1] + ps[1:]) / 2
    up = quantile(b, mids) >= quantile(a, mids) - TOL * mean(a)
    return float(widths[up].sum())


def incidence(a, b, years, grid=None):
    """Change in the quantile function at each percentile, in percent of a's mean per year.
    With the default grid (midpoints of 1,000 equal bins) its average equals the linear annual
    growth of the mean up to discretisation error."""
    if grid is None:
        grid = (np.arange(1000) + 0.5) / 1000
    return grid, (quantile(b, grid) - quantile(a, grid)) / mean(a) / years * 100


def fgt(d, z, alpha):
    v, w = d
    below = v < z
    if alpha == 0:
        return float(w[below].sum())
    return float((w[below] * ((z - v[below]) / z) ** alpha).sum())
