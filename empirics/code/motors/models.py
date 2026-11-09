"""Shared model machinery for WP07: samples, the S&V specification, slope shifts, marginal effects.

The S&V specification (eq. 1-2; Table 2-4): growth over a five-year period on start-of-period
    MAN (sector share), SER, RELUS, EDU, LNPOP, OPEN, TEMPERATE, period dummies
    [+ MAN x RELUS, MAN x EDU]
Hausman-Taylor classification (S&V §6.1): MAN, SER, RELUS, EDU and interactions endogenous
time-varying; LNPOP, OPEN and period dummies exogenous time-varying; TEMPERATE exogenous
time-invariant (with the constant).
"""
import numpy as np
import pandas as pd

from config import FORMER_PLANNED, PROCESSED
from estimators import be, fe, hausman_taylor, re


def load_panel(length=5):
    return pd.read_csv(PROCESSED / f"panel{length}.csv")


def sample(p, name="main", start=1950, end=2015, edu="EDU", share="MAN", years=5):
    """Country-periods for estimation (config.SAMPLES). `end` is the last period start included.
    main: population >= 1m in 2000; excl_cpe: main without former centrally planned economies;
    core: excl_cpe without commodity exporters; developing: core without advanced economies;
    no_commodity: main without commodity exporters; all: no filter."""
    d = p[(p["period"] >= start) & (p["period"] <= end) & (p["years"] == years)].copy()
    if name != "all":
        d = d[~d["small"].fillna(True).astype(bool)]
    if name in ("excl_cpe", "core", "developing"):
        d = d[~d["iso3"].isin(FORMER_PLANNED)]
    if name in ("core", "developing", "no_commodity"):
        d = d[~d["commodity"].fillna(False).astype(bool)]
    if name == "developing":
        d = d[~d["advanced"].astype(bool)]
    need = ["GR", share, "RELUS", edu, "LNPOP", "OPEN", "TEMPERATE"]
    return d.dropna(subset=need)


def period_dummies(d):
    D = pd.get_dummies(d["period"], prefix="P", drop_first=True, dtype=float)
    return pd.concat([d, D], axis=1), list(D.columns)


def add_terms(d, share="MAN", edu="EDU", interactions=(), slope_groups=None, shift_vars=None):
    """Add interactions and slope shifts.
    interactions: subset of ("REL", "EDU") -> share x RELUS, share x edu
    slope_groups: dict label -> boolean Series (same index as d); each listed variable in
                  shift_vars gets one copy per group (no common term), e.g. subperiods or LAC."""
    d = d.copy()
    terms = [share]
    if "REL" in interactions:
        d[f"{share}xREL"] = d[share] * d["RELUS"]
        terms.append(f"{share}xREL")
    if "EDU" in interactions:
        d[f"{share}xEDU"] = d[share] * d[edu]
        terms.append(f"{share}xEDU")
    if slope_groups:
        shift_vars = shift_vars or terms
        new = []
        for v in terms:
            if v in shift_vars:
                for lab, mask in slope_groups.items():
                    d[f"{v}[{lab}]"] = d[v] * mask.astype(float)
                    new.append(f"{v}[{lab}]")
            else:
                new.append(v)
        terms = new
    return d, terms


def fit(d, terms, estimator="HT", edu="EDU", other_share="SER", controls=("LNPOP", "OPEN")):
    """Fit one model. Returns estimators.Result."""
    d, pdum = period_dummies(d)
    endog = list(terms) + ([other_share] if other_share else []) + ["RELUS", edu]
    endog = list(dict.fromkeys(endog))
    exog_tv = list(controls) + pdum
    d = d.dropna(subset=endog + list(controls))
    if estimator == "HT":
        return hausman_taylor(d, "GR", x1=exog_tv, x2=endog, z1=["TEMPERATE"], z2=[], entity="iso3", time="period")
    if estimator == "RE":
        return re(d, "GR", endog + list(controls) + ["TEMPERATE"], time_dummies=pdum)
    if estimator == "FE":
        return fe(d, "GR", endog + list(controls))
    if estimator == "BE":
        return be(d, "GR", endog + list(controls) + ["TEMPERATE"])
    raise ValueError(estimator)


def tidy(res, model, extra=None):
    t = res.table().reset_index().rename(columns={"index": "term"})
    t["model"], t["estimator"], t["nobs"], t["ncountries"] = model, res.estimator, res.nobs, res.ngroups
    for k, v in (extra or {}).items():
        t[k] = v
    return t


def marginal_effect(res, share, rel, edu, group=None):
    """d GR / d share at given RELUS and schooling: a + d*REL + f*EDU, with delta-method s.e.
    `group` selects slope-shift copies, e.g. group='1990–2005' uses MAN[1990–2005] etc."""
    def nm(v):
        return f"{v}[{group}]" if group else v
    w = {}
    for v, x in [(share, 1.0), (f"{share}xREL", rel), (f"{share}xEDU", edu)]:
        if nm(v) in res.params.index:
            w[nm(v)] = x
    names = list(w)
    g = np.array([w[n] for n in names])
    b = res.params[names].to_numpy()
    V = res.cov.loc[names, names].to_numpy()
    est = float(g @ b)
    se = float(np.sqrt(g @ V @ g))
    return est, se


def me_grid(res, share, rels, edus, group=None):
    rows = []
    for r in rels:
        for e in edus:
            est, se = marginal_effect(res, share, r, e, group)
            rows.append({"RELUS": r, "EDU": e, "me": est, "se": se, "lo": est - 1.96 * se, "hi": est + 1.96 * se,
                         "group": group or "all"})
    return pd.DataFrame(rows)


def sig(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
