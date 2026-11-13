"""Functions for study 9.2: potential experience, sample rules, job types, weighted profile
regressions, the Heckman-Lochner-Taber (HLT) restriction and the composition decomposition."""
import numpy as np
import pandas as pd
from scipy import sparse

BINS = [0, 5, 10, 15, 20, 25, 30, 35, 40]           # five-year experience bins, 0-4 ... 35-39 (40 kept in last)
LABELS = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39"]
SECTOR6 = {1: "agriculture and mining", 2: "agriculture and mining", 3: "manufacturing", 4: "construction",
           5: "commerce", 6: "transport, restaurants, other services", 7: "transport, restaurants, other services",
           10: "transport, restaurants, other services", 8: "professional, financial, social services",
           9: "professional, financial, social services"}


def experience(age, school):
    """Potential experience (Lagakos et al. 2018, pp. 802-803): age - 18 with fewer than 12 years of
    schooling; age - schooling - 6 with 12 or more."""
    age, school = np.asarray(age, float), np.asarray(school, float)
    return np.where(school >= 12, age - school - 6, age - 18)


def prepare(d):
    d = d.copy()
    d["school"] = d["anios_esc"].where(d["anios_esc"].between(0, 24))
    d["exp"] = experience(d["eda"], d["school"])
    d.loc[d["school"].isna(), "exp"] = np.nan
    d["bin"] = pd.cut(d["exp"], BINS + [41], right=False, labels=LABELS + ["35-39"], ordered=False)
    d["bin"] = d["bin"].astype(str).replace({"nan": np.nan})
    d["employed"] = d["clase2"] == 1
    d["wage_emp"] = d["employed"] & (d["pos_ocu"] == 1)
    d["private"] = d["ambito2"] != 7
    d["fulltime"] = d["hrsocup"] >= 35
    d["formality"] = d["emp_ppal"].map({1: "informal", 2: "formal"})
    d["sector6"] = d["rama_est2"].map(SECTOR6)
    d["size2"] = d["ambito2"].map({2: "up to 10 workers", 3: "up to 10 workers", 4: "up to 10 workers",
                                   5: "more than 10 workers", 6: "more than 10 workers"})
    d["earn_ok"] = d["ing_x_hrs"] > 0
    d["lw"] = np.log(d["ing_x_hrs"].where(d["earn_ok"]))
    d["heaped"] = d["eda"] % 5 == 0
    d["cohort"] = (d["year"] - d["eda"]).astype("Int64")      # single birth years (see hlt)
    return d


def baseline(d, sex=1, fulltime=True, pos=1):
    """Lagakos et al. baseline: men, full-time, private-sector wage employees, 0-40 years of experience."""
    m = d["employed"] & (d["pos_ocu"] == pos) & d["exp"].between(0, 40) & d["bin"].notna()
    if pos == 1:
        m &= d["private"]
    if sex is not None:
        m &= d["sex"] == sex
    if fulltime:
        m &= d["fulltime"]
    return d[m]


def _onehot(values, levels):
    """Sparse indicator matrix for `levels` (values and levels compared as strings)."""
    v = pd.Series(values).astype(str).to_numpy()
    pos = {str(lv): j for j, lv in enumerate(levels)}
    col = np.array([pos.get(x, -1) for x in v])
    keep = col >= 0
    if len(levels) and not keep.any():
        raise ValueError("no observation matches any level: check value types")
    rows = np.nonzero(keep)[0]
    return sparse.csr_matrix((np.ones(len(rows)), (rows, col[keep])), shape=(len(v), len(levels)))


def dummies(s, levels):
    """Dense indicator columns for `levels` (kept for small problems and tests)."""
    return _onehot(s, levels).toarray() if len(levels) else np.empty((len(s), 0))


def _wls_blocks(y, blocks, w):
    """Weighted least squares of y on an intercept and categorical blocks [(values, levels), ...],
    using sparse indicators and the normal equations, so memory grows with the number of
    parameters rather than with rows x parameters. Returns the coefficient vector
    [intercept, block 1 levels..., block 2 levels...]."""
    n = len(y)
    X = sparse.hstack([sparse.csr_matrix(np.ones((n, 1)))] + [_onehot(v, lv) for v, lv in blocks]).tocsr()
    Xw = X.multiply(w[:, None]).tocsr()
    A = (X.T @ Xw).toarray()
    b = Xw.T @ y
    return np.linalg.lstsq(A, b, rcond=None)[0]


def cross_section(d):
    """Log hourly earnings on experience-bin dummies (0-4 omitted) and year dummies. Returns the
    bin coefficients (log points relative to 0-4)."""
    d = d.dropna(subset=["lw", "bin"])
    years = sorted(d["year"].unique())
    b = _wls_blocks(d["lw"].to_numpy(float), [(d["bin"], LABELS[1:]), (d["year"], years[1:])],
                    d["w"].to_numpy(float))
    return pd.Series(np.r_[0.0, b[1:len(LABELS)]], index=LABELS)


def hlt(d, flat=("30-34", "35-39")):
    """Heckman-Lochner-Taber restriction (Lagakos et al. §IV.B, no depreciation): no experience
    effects within the flat spot. Step 1: on flat-spot workers, log earnings on year and birth-year
    cohort dummies gives the time effects. Cohorts must be single birth years: with five-year
    groups a cohort trend within each group loads onto the time effects and the restriction no
    longer identifies them (shown in tests/test_enoe_profiles.py). Step 2: earnings net of time
    effects on experience-bin dummies below the flat spot (plus one flat-spot group) and cohort
    dummies, on all workers. Returns coefficients relative to the 0-4 bin for each bin below the
    flat spot and for the flat-spot group as a whole."""
    d = d.dropna(subset=["lw", "bin", "cohort"])
    years = sorted(d["year"].unique())
    f = d[d["bin"].isin(flat)]
    coh_f = sorted(f["cohort"].unique())
    bf = _wls_blocks(f["lw"].to_numpy(float), [(f["year"], years[1:]), (f["cohort"], coh_f[1:])],
                     f["w"].to_numpy(float))
    time = dict(zip(years, np.r_[0.0, bf[1:len(years)]]))
    y = d["lw"].to_numpy(float) - d["year"].map(time).to_numpy(float)
    below = [b for b in LABELS if b not in flat]
    expcol = np.where(d["bin"].isin(flat), "FLAT", d["bin"].astype(str))
    levels = below[1:] + ["FLAT"]
    coh = sorted(d["cohort"].unique())
    b = _wls_blocks(y, [(expcol, levels), (d["cohort"], coh[1:])], d["w"].to_numpy(float))
    out = pd.Series(np.r_[0.0, b[1:len(levels) + 1]], index=[below[0]] + levels)
    return out.rename({"FLAT": "flat spot"})


def height(coef, b="20-24"):
    return float(np.exp(coef[b]) - 1)


def psu_bootstrap(d, fn, nboot, seed):
    """Resample primary sampling units within state x year; returns a list of fn(resample)."""
    rng = np.random.default_rng(seed)
    d = d.reset_index(drop=True)
    idx = d.groupby(["year", "ent", "psu"]).indices
    strata = {}
    for (y, e, _), ix in idx.items():
        strata.setdefault((y, e), []).append(ix)
    out = []
    for _ in range(nboot):
        take = np.concatenate([np.concatenate([u[j] for j in rng.integers(0, len(u), len(u))])
                               for u in strata.values()])
        out.append(fn(d.iloc[take]))
    return out


def composition(d, coef_by_type):
    """Decompose the national profile height at 20-24 years (log points) relative to the formal one.
    With informal shares s0 (0-4 bin) and s20 (20-24 bin), profile heights cF and cI (log points,
    from the type-specific cross-sectional models) and the informal-minus-formal mean log earnings gap
    at entry g0, mean log earnings by bin give exactly
        national - formal = s20 (cI - cF) + (s20 - s0) g0          (order 1)
                          = s0 (cI - cF) + (s20 - s0) (g0 + cI - cF)  (order 2)
    The first term is the effect of flatter informal profiles (within); the second the effect of the
    informal share changing with experience (composition)."""
    x = d.dropna(subset=["lw", "bin", "formality"])
    s = x.groupby(["bin", "formality"])["w"].sum().unstack()
    s = s.div(s.sum(axis=1), axis=0)
    s0, s20 = float(s.loc["0-4", "informal"]), float(s.loc["20-24", "informal"])
    cF, cI = float(coef_by_type["formal"]["20-24"]), float(coef_by_type["informal"]["20-24"])
    g0 = _mean_gap(x[x["bin"] == "0-4"])
    national = cF + s20 * (cI - cF) + (s20 - s0) * g0
    return {"national_log": national, "formal_log": cF, "informal_log": cI, "informal_share_0_4": s0,
            "informal_share_20_24": s20, "entry_gap_log": g0,
            "within_order1": s20 * (cI - cF), "composition_order1": (s20 - s0) * g0,
            "within_order2": s0 * (cI - cF), "composition_order2": (s20 - s0) * (g0 + cI - cF)}


def _mean_gap(x):
    x = x.dropna(subset=["lw", "formality"])
    m = x.groupby("formality").apply(lambda g: np.average(g["lw"], weights=g["w"]), include_groups=False)
    return float(m.get("informal", np.nan) - m.get("formal", np.nan))
