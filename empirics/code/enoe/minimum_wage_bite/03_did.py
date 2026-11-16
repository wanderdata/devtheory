"""Study 9.8, step 3: event studies and tests of P44-P47 (pre-analysis plan §§1, 3, 4).

    python empirics/code/enoe/minimum_wage_bite/03_did.py [--B 1999]

Model: y_ct = cell + state x year + activity x year + sum_k beta_k bite_c 1[t = k], k != 2018, weighted
by 2018 employment, clustered by state. The post estimand (mean of the 2022-2024 coefficients) is
obtained directly by reparametrisation: the 2022-2024 interactions enter as S = D22 + D23 + D24,
D23 - D22 and D24 - D22, so that the coefficient on S is the mean. Intervals for the estimands invert
the restricted wild cluster bootstrap (study 9.4's routines); year-by-year coefficients use CR1.

Outputs (empirics/output/enoe/minimum_wage_bite/): estimates.csv, event.csv, robustness.csv,
tests.csv, implied_productivity.csv
"""
import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
_b = importlib.util.spec_from_file_location("border_lib", HERE.parents[1] / "border_mw" / "border_lib.py")
bl = importlib.util.module_from_spec(_b)
_b.loader.exec_module(bl)

ROOT = HERE.parents[4]
OUT = ROOT / "empirics" / "output" / "enoe" / "minimum_wage_bite"
YEARS = list(range(2015, 2025))
PRE = [2015, 2016, 2017]
MID = [2019, 2020, 2021]
OUTCOMES = {"w_all": "Mean log hourly wage, wage employees (first stage)",
            "lemp": "Log employment", "formal": "Formal share of employment",
            "lprod": "Log value added per worker", "w_informal": "Mean log hourly wage, informal wage employees",
            "w_formal": "Mean log hourly wage, formal wage employees", "p10": "10th percentile, log hourly wage",
            "p50": "Median log hourly wage", "below_current": "Share below the current minimum (full-time)",
            "lhours": "Log weekly hours per worker", "lva": "Log value added"}
PROPS = {"lemp": "P44", "formal": "P45", "lprod": "P46", "w_informal": "P47"}
SOUTHEAST = [4, 7, 23, 27, 31]
BORDER = [2, 5, 8, 19, 26, 28]


def load():
    c = pd.read_csv(OUT / "cells_year.csv")
    b = pd.read_csv(OUT / "bite.csv")
    c["lemp"] = np.log(c["emp"])
    c["lhours"] = np.log(c["hours"])
    c["lva"] = np.log(c["va"])
    return c.merge(b, on=["unit", "group"])


def design(d, treat):
    cols, names = [], []
    for k in PRE + MID:
        cols.append(d[treat] * (d["year"] == k))
        names.append(f"b{k}")
    D = {k: (d["year"] == k).astype(float) for k in (2022, 2023, 2024)}
    cols += [d[treat] * (D[2022] + D[2023] + D[2024]), d[treat] * (D[2023] - D[2022]), d[treat] * (D[2024] - D[2022])]
    names += ["post", "c23", "c24"]
    return np.column_stack(cols), names


def estimate(d, y, treat="bite18", weight="emp18", cluster="unit", B=1999, wild=True, detrend=False):
    d = d.dropna(subset=[y, treat]).copy()
    d = d[d[weight] > 0] if weight else d
    if detrend:  # cell-specific linear trend fitted on 2015-2018, removed from all years
        def dt(g):
            p = g[g["year"] <= 2018]
            if p[y].notna().sum() < 3:
                return g[y] * np.nan
            s = np.polyfit(p["year"], p[y], 1)
            return g[y] - np.polyval(s, g["year"])
        d[y] = d.groupby(["unit", "group"], group_keys=False)[[y, "year"]].apply(dt)
        d = d.dropna(subset=[y])
    d["cell"] = d["unit"].astype(str) + "|" + d["group"]
    d["sy"] = d["unit"].astype(str) + "|" + d["year"].astype(str)
    d["gy"] = d["group"] + "|" + d["year"].astype(str)
    X, names = design(d, treat)
    w = d[weight].to_numpy(float) if weight else np.ones(len(d))
    cl = d[cluster].astype(str).to_numpy()
    f = bl.fit(d[y], X, d[["cell", "sy", "gy"]], w, cl)
    b, V = f["b"], f["V"]
    j = names.index("post")
    se = np.sqrt(V[j, j])
    out = {"outcome": y, "treat": treat, "cells": d["cell"].nunique(), "obs": len(d), "clusters": f["G"],
           "post": b[j], "se_cr1": se, "lo_cr1": b[j] - 1.645 * se, "hi_cr1": b[j] + 1.645 * se,
           "b2019": b[names.index("b2019")], "se2019": np.sqrt(V[names.index("b2019"), names.index("b2019")])}
    if wild:
        lo, hi = bl.wild_ci(f, w, cl, j, B=max(B // 2, 499), seed=98)
        out.update({"lo90": lo, "hi90": hi, "p_post": bl.wild_wald(f, w, cl, j, B=B, seed=98)["p"],
                    "p_pretrend": bl.wild_wald(f, w, cl, [0, 1, 2], B=B, seed=98)["p"]})
    # year-by-year coefficients (CR1)
    ev = []
    for k in PRE + MID:
        i = names.index(f"b{k}")
        ev.append((k, b[i], np.sqrt(V[i, i])))
    ev.append((2018, 0.0, 0.0))
    i0, i1, i2 = names.index("post"), names.index("c23"), names.index("c24")
    L = {2022: np.eye(len(b))[i0] - np.eye(len(b))[i1] - np.eye(len(b))[i2],
         2023: np.eye(len(b))[i0] + np.eye(len(b))[i1], 2024: np.eye(len(b))[i0] + np.eye(len(b))[i2]}
    for k, l in L.items():
        ev.append((k, l @ b, np.sqrt(l @ V @ l)))
    event = pd.DataFrame(ev, columns=["year", "beta", "se"]).sort_values("year")
    event["outcome"], event["treat"] = y, treat
    return out, event


def verdict(prop, est, fs):
    lo, hi, b = est["lo90"], est["hi90"], est["post"]
    if est["p_pretrend"] < 0.10:
        return "Inconclusive (pre-trend test p < 0.10)"
    if prop == "P44":
        return "Supported" if hi < 0 else ("Rejected" if lo > -0.3 * fs else "Inconclusive")
    if prop == "P45":
        return "Supported" if hi < 0 else ("Rejected" if lo > -0.10 else "Inconclusive")
    if prop in ("P46", "P47"):
        return "Supported" if lo > 0 else ("Rejected" if hi < 0.25 * fs else "Inconclusive")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=1999)
    a = ap.parse_args()
    d = load()
    main_s = d[d["n18"] >= 100]
    ests, events = [], []
    for y in OUTCOMES:
        e, ev = estimate(main_s, y, B=a.B)
        e["label"] = OUTCOMES[y]
        ests.append(e)
        events.append(ev)
        print(y, round(e["post"], 4), round(e["lo90"], 4), round(e["hi90"], 4), "pretrend p", e["p_pretrend"], flush=True)
    est = pd.DataFrame(ests)
    est.to_csv(OUT / "estimates.csv", index=False, float_format="%.6f")
    pd.concat(events).to_csv(OUT / "event.csv", index=False, float_format="%.6f")
    fs = est.set_index("outcome").loc["w_all"]
    first_stage_ok = fs["lo90"] > 0
    tests = []
    for y, p in PROPS.items():
        r = est.set_index("outcome").loc[y]
        v = verdict(p, r, fs["post"]) if first_stage_ok else "Inconclusive (first stage not distinguishable from zero)"
        tests.append({"proposition": p, "outcome": y, "post": r["post"], "lo90": r["lo90"], "hi90": r["hi90"],
                      "p_pretrend": r["p_pretrend"], "first_stage": fs["post"], "ratio_to_first_stage":
                          r["post"] / fs["post"], "verdict": v})
    tests = pd.DataFrame(tests)
    tests.to_csv(OUT / "tests.csv", index=False, float_format="%.6f")
    print(tests[["proposition", "post", "lo90", "hi90", "p_pretrend", "verdict"]])

    # robustness (CR1 intervals; post estimand and its ratio to the first stage of the same specification)
    specs = {
        "main": (main_s, {}),
        "bite measured in 2017": (main_s, {"treat": "bite17"}),
        "Kaitz index": (main_s, {"treat": "kaitz"}),
        "bite among formal employees": (main_s, {"treat": "bite18_formal"}),
        "cells with >= 50 workers": (d[d["n18"] >= 50], {}),
        "unweighted": (main_s, {"weight": None}),
        "excluding agriculture": (main_s[main_s["group"] != "Agriculture, forestry and fishing"], {}),
        "excluding accommodation and food": (main_s[main_s["group"] != "Accommodation and food"], {}),
        "excluding professional, corporate and support services":
            (main_s[main_s["group"] != "Professional, corporate and support services"], {}),
        "excluding government": (main_s[main_s["group"] != "Government"], {}),
        "excluding southeastern states": (main_s[~main_s["unit"].isin(SOUTHEAST)], {}),
        "excluding border states": (main_s[~main_s["unit"].isin(BORDER)], {}),
        "clustered by activity": (main_s, {"cluster": "group"}),
        "cell-specific linear pre-trend removed": (main_s, {"detrend": True}),
    }
    rob = []
    for name, (dd, kw) in specs.items():
        fsr, _ = estimate(dd, "w_all", wild=False, **kw)
        for y in ["w_all", "lemp", "formal", "lprod", "w_informal"]:
            r, _ = estimate(dd, y, wild=False, **kw)
            rob.append({"specification": name, "outcome": y, "post": r["post"], "lo_cr1": r["lo_cr1"],
                        "hi_cr1": r["hi_cr1"], "ratio_to_first_stage": r["post"] / fsr["post"], "cells": r["cells"]})
    pd.DataFrame(rob).to_csv(OUT / "robustness.csv", index=False, float_format="%.6f")

    # implied effect on state productivity relative to the least-exposed cells (description, plan §6)
    bE, bV = est.set_index("outcome").loc["lemp", "post"], est.set_index("outcome").loc["lprod", "post"]
    p = main_s[main_s["year"].isin([2022, 2023, 2024])].groupby(["unit", "group"], as_index=False).agg(
        emp=("emp", "mean"), va=("va", "mean"), bite=("bite18", "first"))
    p["emp_cf"] = p["emp"] * np.exp(-bE * p["bite"])
    p["va_cf"] = p["emp_cf"] * (p["va"] / p["emp"]) * np.exp(-bV * p["bite"])
    s = p.groupby("unit")[["emp", "va", "emp_cf", "va_cf"]].sum()
    s["implied_log_effect"] = np.log((s["va"] / s["emp"]) / (s["va_cf"] / s["emp_cf"]))
    s.reset_index().to_csv(OUT / "implied_productivity.csv", index=False, float_format="%.6f")


if __name__ == "__main__":
    main()
