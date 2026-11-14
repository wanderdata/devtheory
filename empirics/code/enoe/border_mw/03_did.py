"""Study 9.4, step 3: differences in differences, event studies, earnings bins, robustness and
placebo (pre-analysis plan §§3, 5).

    python empirics/code/enoe/border_mw/03_did.py

Input: cells.parquet (step 2). Outputs in empirics/output/enoe/border_mw/:
  did.csv     one row per specification x outcome: estimate, CR1 s.e., wild bootstrap p and 90% interval
  event.csv   event-study coefficients (main sample), with the pre-trend test in pretrend.csv
  bins.csv    effects by earnings bin and formality (main specification)
  pre_means.csv  pre-period means in the border zone (for relative effects)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parent))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import border_lib as bl  # noqa: E402
from enoe_config import INTERIM, OUTPUT_ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "border_mw"
TMP = INTERIM / "border_mw"
LAST_PRE, LAST_POST, T2020 = 11, 15, 16
BINS = ["b00_06", "b06_08", "b08_10", "b10_12", "b12_15", "b15_20", "b20_30", "b30_up"]
BELOW, EXCESS = BINS[:3], BINS[3:5]
PRIMARY = ["lnw", "emp_rate", "formal_rate", "formal_share", "i_to_f", "below_m", "missing", "excess",
           "i_missing", "i_excess"]
SECONDARY = ["informal_rate", "we_rate", "report", "hours", "n_to_f", "f_to_i", "f_to_n", "i_to_n", "lnw_own",
             "f_missing", "f_excess", "f_norep", "i_norep"]
B_MAIN = 1999


def add_sums(c):
    for lab in ["f", "i"]:
        c[f"{lab}_missing"] = c[[f"{lab}_{b}" for b in BELOW]].sum(1, min_count=1)
        c[f"{lab}_excess"] = c[[f"{lab}_{b}" for b in EXCESS]].sum(1, min_count=1)
    c["missing"] = c["f_missing"] + c["i_missing"]
    c["excess"] = c["f_excess"] + c["i_excess"]
    return c


def sample(c, spec):
    """Cells for a specification: control group, sample and period."""
    s = c[(c["group"] == spec.get("group", "all")) & (c["sample"] == spec.get("sample", "old"))]
    ctrl = spec.get("control", "six")
    if ctrl == "six":
        s = s[s["border_state"]]
    elif ctrl == "near200":
        s = s[s["zlfn"] | (s["border_state"] & (s["dist_km"] <= 200))]
    s = s[s["t"].between(spec.get("first", 0), spec.get("last", LAST_POST))].copy()
    if "fake_post" in spec:
        s["post"] = s["t"] >= spec["fake_post"]
    if spec.get("unweighted"):
        s["w"] = 1.0
    s["ent_t"] = s["ent_i"].astype(str) + "_" + s["t"].astype(str)
    return s


SPECS = {
    "main": {},
    "full sample": {"sample": "full"},
    "national control": {"control": "national"},
    "control within 200 km": {"control": "near200"},
    "state x quarter effects": {"fe": ["ent_t"]},
    "unweighted cells": {"unweighted": True},
    "placebo 2018Q1": {"last": LAST_PRE, "fake_post": 8},
}
# Exploratory, added after seeing the event studies (D-055): pre-period from 2017Q3, where the
# pre-period coefficients of the earnings outcomes are flat.
EXPLORATORY = {"exploratory: pre-period from 2017Q3": {"first": 6}}
GROUP_SPECS = {f"group: {g}": {"group": g} for g in ["women", "men", "school_lt12", "school_ge12"]}


def main():
    c = add_sums(pd.read_parquet(TMP / "cells.parquet"))
    rows = []
    for name, spec in {**SPECS, **GROUP_SPECS, **EXPLORATORY}.items():
        s = sample(c, spec)
        outs = PRIMARY + SECONDARY if name == "main" else PRIMARY + ["report", "f_norep", "i_norep"] \
            if name.startswith("exploratory") else PRIMARY
        for y in outs:
            ci = name in ("main", "full sample", "placebo 2018Q1") or name.startswith(("group", "exploratory"))
            r = bl.did(s, y, B=B_MAIN if name == "main" else 999, ci=ci, fe_extra=spec.get("fe") and spec["fe"])
            r["spec"] = name
            rows.append(r)
        print(name, "done")
    d = pd.DataFrame(rows)
    # pre-period means in the border zone (main sample) for relative effects
    m = sample(c, {})
    pre = m[m["zlfn"] & (m["t"] <= LAST_PRE)]
    pm = {y: np.average(pre[y].dropna(), weights=pre.loc[pre[y].notna(), "w"]) for y in PRIMARY + SECONDARY}
    pd.Series(pm, name="pre_mean_zone").rename_axis("outcome").to_csv(OUT / "pre_means.csv")
    d["pre_mean_zone"] = d["outcome"].map(pm)
    d.to_csv(OUT / "did.csv", index=False)

    # event studies, main sample, including 2020Q1
    ev, pt = [], []
    es_cells = sample(c, {"last": T2020})
    for y in PRIMARY + ["report"]:
        e, p = bl.event_study(es_cells, y, ref=LAST_PRE, B=999, pre=list(range(LAST_PRE)))
        ev.append(e)
        pt.append({"outcome": y, "p_pretrend_wild": p})
    pd.concat(ev).to_csv(OUT / "event.csv", index=False)
    pd.DataFrame(pt).to_csv(OUT / "pretrend.csv", index=False)

    # bins, main specification
    brows = []
    for lab in ["f", "i"]:
        for b in BINS + ["norep"]:
            y = f"{lab}_{b}"
            r = bl.did(m, y, B=999, ci=False)
            r.update({"formality": {"f": "formal", "i": "informal"}[lab], "bin": b, "pre_mean_zone":
                      np.average(pre[y].dropna(), weights=pre.loc[pre[y].notna(), "w"]), "measure": "monthly"})
            brows.append(r)
            if b != "norep":
                yh = f"{lab}h_{b}"
                r = bl.did(m, yh, B=999, ci=False)
                r.update({"formality": {"f": "formal", "i": "informal"}[lab], "bin": b, "measure": "hourly",
                          "pre_mean_zone": np.average(pre[yh].dropna(), weights=pre.loc[pre[yh].notna(), "w"])})
                brows.append(r)
    pd.DataFrame(brows).to_csv(OUT / "bins.csv", index=False)
    show = d[d["spec"] == "main"][["outcome", "beta", "se_cr1", "p_wild", "lo90", "hi90", "pre_mean_zone",
                                   "clusters", "treated_clusters"]]
    print(show.round(4).to_string(index=False))
    print(pd.DataFrame(pt).round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
