"""Study 9.7, step 4: pass-through of productivity to the product wage, test of P43
(pre-analysis plan §3.4).

    python empirics/code/enoe/state_productivity/04_passthrough.py [--reps 199]

Product wage of a unit x group cell in a period: mean hourly labour income in the main job of employees
and own-account workers (pos_ocu 1 or 3) with positive hours, each person's income deflated by the
PIBE implicit price index of their state and group in the survey year (2018 = 100), averaged with
weights adjusted for earnings non-response. Non-response adjustment: respondents (income > 0) are
weighted up to the total survey weight of their class (year x state x formality x five-year age group
x schooling level: 0-5, 6-8, 9-11, 12+ years); classes with fewer than 20 respondents are merged into
year x state x formality. Persons whose industry code does not identify a group are left out.

Regression across cells with at least 100 respondents in each of P0 and P1: change in log product
wage on change in log value added per hour, unit and group fixed effects, weighted by initial
employment. The slope is corrected for sampling error in the regressor by dividing by its reliability
(1 - mean bootstrap variance / variance, both after removing the fixed effects, weighted). The 90%
interval is the percentile interval of the corrected slope over the PSU bootstrap (adjustment factors
held fixed).
"""
import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1]))

from activities import MAIN, fine_code  # noqa: E402

_s = importlib.util.spec_from_file_location("est97", HERE.parent / "03_estimates.py")
est = importlib.util.module_from_spec(_s)
_s.loader.exec_module(est)

OUT, TMP = est.OUT, est.TMP
INV = {f: g for g, fs in MAIN.items() for f in fs}


def deflators(panel):
    p = panel.copy()
    p["group"] = p["act"].map(INV)
    p["unit"] = p["ent"].replace(est.UNIT31)
    d = p.groupby(["unit", "group", "year"], as_index=False)[["va_k", "va_c"]].sum()
    d["defl"] = d["va_c"] / d["va_k"]
    return d[["unit", "group", "year", "defl"]]


def wage_cells(panel):
    """PSU-level sums of adjusted weight x real hourly wage, adjusted weight and respondents."""
    defl = deflators(panel)
    out = []
    for f in sorted(TMP.glob("q_*.parquet")):
        d = pd.read_parquet(f)
        per = est.period_of(int(d["year"].iloc[0]))
        if per is None:
            continue
        d = d[d["pos_ocu"].isin([1, 3]) & (d["hrsocup"] > 0)].copy()
        d["group"] = pd.Series(fine_code(d["p4a"].values), index=d.index).map(INV)
        d = d[d["group"].notna()]
        d["unit"] = d["ent"].replace(est.UNIT31)
        d["seg"] = np.where(d["emp_ppal"] == 2, "f", "i")
        d["resp"] = (d["ingocup"] > 0).astype(int)
        d["age5"] = (d["eda"].clip(15, 74) // 5).astype(int)
        d["sch"] = pd.cut(d["anios_esc"].where(d["anios_esc"] < 99), [-1, 5, 8, 11, 99], labels=False).fillna(-1)
        cls = ["year", "ent", "seg", "age5", "sch"]
        tot = d.groupby(cls)["w"].transform("sum")
        rw = d["w"].where(d["resp"] == 1, 0).groupby([d[c] for c in cls]).transform("sum")
        nr = d["resp"].groupby([d[c] for c in cls]).transform("sum")
        small = nr < 20
        cls2 = ["year", "ent", "seg"]
        tot2 = d.groupby(cls2)["w"].transform("sum")
        rw2 = d["w"].where(d["resp"] == 1, 0).groupby([d[c] for c in cls2]).transform("sum")
        adj = np.where(small, tot2 / rw2.replace(0, np.nan), tot / rw.replace(0, np.nan))
        d["wa"] = d["w"] * adj * d["resp"]
        d = d.merge(defl, on=["unit", "group", "year"], how="left")
        d["hw"] = d["ingocup"] / (d["hrsocup"] * 4.33) / (d["defl"] / 100)
        d["wa_hw"] = d["wa"] * d["hw"]
        d["w0"] = d["w"] * d["resp"]
        d["w0_hw"] = d["w0"] * d["hw"]
        d["period"] = per
        out.append(d[d["resp"] == 1].groupby(["period", "ent", "upm", "unit", "group"], as_index=False)[
            ["wa_hw", "wa", "w0_hw", "w0", "resp"]].sum())
        print(f.name, flush=True)
    return pd.concat(out, ignore_index=True)


def fe_resid(df, col, w):
    """Weighted residual of col after unit and group fixed effects (alternating projections)."""
    r = df[col].astype(float).copy()
    for _ in range(200):
        prev = r.copy()
        for k in ("unit", "group"):
            m = (r * w).groupby(df[k]).transform("sum") / w.groupby(df[k]).transform("sum")
            r = r - m
        if np.max(np.abs(r - prev)) < 1e-12:
            break
    return r


def slope(df):
    w = df["emp0"]
    x, y = fe_resid(df, "dx", w), fe_resid(df, "dy", w)
    return np.sum(w * x * y) / np.sum(w * x * x), x, w


def assemble(cell, wages, factor=None, raw=False):
    wg = wages
    if raw:
        wg = wg.drop(columns=["wa_hw", "wa"]).rename(columns={"w0_hw": "wa_hw", "w0": "wa"})
    if factor is not None:
        wg = wg.merge(factor, on=["period", "ent", "upm"])
        wg = wg.assign(wa_hw=wg["wa_hw"] * wg["f"], wa=wg["wa"] * wg["f"], resp=wg["resp"] * wg["f"])
    wg = wg.groupby(["period", "unit", "group"], as_index=False)[["wa_hw", "wa", "resp"]].sum()
    wg["pw"] = wg["wa_hw"] / wg["wa"]
    c = cell.merge(wg, on=["period", "unit", "group"], how="left")
    c["vah"] = c["va_k"] / (c["hrs_f"] + c["hrs_i"])
    a, b = c[c["period"] == "P0"].set_index(["unit", "group"]), c[c["period"] == "P1"].set_index(["unit", "group"])
    df = pd.DataFrame({"dx": np.log(b["vah"] / a["vah"]), "dy": np.log(b["pw"] / a["pw"]),
                       "emp0": a["emp_f"] + a["emp_i"], "n0": a["resp"], "n1": b["resp"]}).reset_index()
    return df.replace([np.inf, -np.inf], np.nan).dropna()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=199)
    a = ap.parse_args()
    panel, mei, psu, nq, mss, pop = est.load()
    pibe, meit = est.pibe_periods(panel), est.meitef_periods(mei)
    cell = est.cells(est.enoe_periods(psu, nq), pibe, meit)
    wages = wage_cells(panel)
    df = assemble(cell, wages)
    keep = (df["n0"] >= 100) & (df["n1"] >= 100)
    base = df[keep].reset_index(drop=True)
    b_raw, xres, w = slope(base)
    rng = np.random.default_rng(est.SEED + 43)
    xs, bs = [], []
    for r in range(a.reps):
        f = est.boot_factor(pop, rng)
        c = est.cells(est.enoe_periods(psu, nq, f), pibe, meit)
        d = assemble(c, wages, f).set_index(["unit", "group"]).reindex(base.set_index(["unit", "group"]).index)
        d = d.reset_index()
        ok = d[["dx", "dy"]].notna().all(axis=1)
        xs.append(d["dx"].values)
        bs.append(slope(d[ok].reset_index(drop=True))[0] if ok.sum() > 10 else np.nan)
        if r % 20 == 0:
            print("replication", r, flush=True)
    X = np.array(xs)
    var_s = np.nanvar(X, axis=0)
    rel = 1 - np.sum(w * var_s) / np.sum(w) / (np.sum(w * xres ** 2) / np.sum(w))
    b_cor = b_raw / rel
    bs = np.array(bs) / rel
    lo, hi = np.nanpercentile(bs, [5, 95])
    bl, bh = np.nanpercentile(np.array(bs) * rel, [5, 95])
    verdict = "Supported" if (b_cor >= 0.5 and lo > 0) else ("Rejected" if hi < 0.5 else "Inconclusive")
    # unweighted and unadjusted checks (point estimates)
    unw = np.sum(fe_resid(base, "dx", base["emp0"] * 0 + 1) * fe_resid(base, "dy", base["emp0"] * 0 + 1)) / np.sum(
        fe_resid(base, "dx", base["emp0"] * 0 + 1) ** 2)
    raw = assemble(cell, wages, raw=True).set_index(["unit", "group"]).reindex(
        base.set_index(["unit", "group"]).index).reset_index().dropna()
    b_noadj = slope(raw)[0]
    res = pd.DataFrame([{"proposition": "P43", "cells": len(base), "cells_dropped_n<100": int((~keep).sum()),
                         "slope_uncorrected": b_raw, "slope_uncorrected_lo": bl, "slope_uncorrected_hi": bh,
                         "reliability": rel, "slope": b_cor, "lo": lo, "hi": hi, "slope_unweighted_uncorrected": unw,
                         "slope_no_nonresponse_adjustment_uncorrected": b_noadj,
                         "verdict": verdict}])
    res.to_csv(OUT / "tests_p43.csv", index=False, float_format="%.6f")
    base.to_csv(OUT / "passthrough_cells.csv", index=False, float_format="%.6f")
    print(res.T)


if __name__ == "__main__":
    main()
