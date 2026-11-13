"""Study 9.3, step 2: sector-only and segmented productivity ladders for Mexico, dominance
verdicts, and the segment-level decomposition (pre-analysis plan §§3-5).

    python empirics/code/enoe/productivity_ladder/02_ladder.py

Inputs: cells.csv (step 1) and the UN sector value added used by WP08
(empirics/data/processed/lac_lp/panel_7sector.csv). Outputs in
empirics/output/enoe/productivity_ladder/:
  segments.csv      employment, income and implied productivity by year x sector x formality
  verdicts.csv      verdict by period, price base and specification
  decomposition.csv growth of output per working-age person, sector- and segment-level terms
  ladders.csv       steps of every ladder (for the app)
  incidence.csv     incidence curves, main specification
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parents[2] / "lp"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import ladder as lad  # noqa: E402  (empirics/code/lp/ladder.py)
from decompose import decompose, va_at_prices  # noqa: E402  (empirics/code/lp/decompose.py)
from enoe_config import LADDER_YEARS, OUTPUT_ROOT, ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "productivity_ladder"
SECTORS = ["AGR", "MIU", "MAN", "CON", "TRH", "TSC", "OTH"]
PERIODS = [(2005, 2008), (2008, 2019), (2019, 2024), (2005, 2019)]
BASES = ["initial", "final"]
THETAS = [0.5, 1.0, 1.5, 2.0]
ORDER = ["improvement", "improvement, weighting the lower percentiles", "ambiguous",
         "deterioration, weighting the lower percentiles", "deterioration"]


# --------------------------------------------------------------------- cells ---

def annual_cells(by=("sector", "formality")):
    """Average of the four quarters; employment with no sector (or no formality) distributed in
    proportion to specified employment (plan §2). Income statistics from specified cells."""
    c = pd.read_csv(OUT / "cells.csv")
    by = list(by)
    pop = c.groupby(["year", "quarter"])["pop15"].first().groupby("year").mean()
    a = c.groupby(["year", "quarter"] + by)[["emp", "paid_emp", "inc_w", "inc_sum"]].sum().groupby(["year"] + by).mean()
    med = (c.assign(mw=c["inc_median"] * c["inc_w"]).groupby(["year", "quarter"] + by)[["mw", "inc_w"]].sum()
           .groupby(["year"] + by).mean())
    a["inc_median"] = med["mw"] / med["inc_w"]          # income-weighted average of cell medians
    a = a.reset_index()
    a = a[a["formality"] != "unspecified"] if "formality" in by else a
    out = []
    for (y, *rest), g in a.groupby(["year"] + [b for b in by if b != "sector"]):
        uns = g.loc[g["sector"] == "UNS", "emp"].sum()
        spec = g[g["sector"] != "UNS"].copy()
        spec["emp"] = spec["emp"] * (1 + uns / spec["emp"].sum())
        out.append(spec)
    a = pd.concat(out)
    a["inc_mean"] = a["inc_sum"] / a["inc_w"]
    a["reporting"] = a["inc_w"] / a["paid_emp"]
    a["pop15"] = a["year"].map(pop)
    return a


def split(sec_y, cells, theta=1.0, stat="inc_mean"):
    """Output per worker by segment within each sector: sector output per worker times relative
    income raised to theta, normalised so that segments add up to the sector's value added."""
    rows = []
    for s, g in cells.groupby("sector"):
        L = g["emp"].sum()
        rel = g[stat] ** theta
        norm = (g["emp"] / L * rel).sum()
        v = sec_y[s] / L * rel / norm
        rows.append(pd.DataFrame({"sector": s, "segment": g["segment"], "emp": g["emp"].to_numpy(), "v": v.to_numpy()}))
    return pd.concat(rows, ignore_index=True)


# ------------------------------------------------------------------- ladders ---

def ladder_of(steps, pop15):
    """Steps (value per worker, employment) plus the zero block, as a ladder distribution."""
    zero = pop15 - steps["emp"].sum()
    return lad.make(list(steps["v"]) + [0.0], list(steps["emp"]) + [zero])


def classify(f, s):
    out = set()
    for b in BASES:
        if f[b] == 1:
            out.add("improvement")
        elif f[b] == -1:
            out.add("deterioration")
        elif s[b] == 1:
            out.add("improvement, weighting the lower percentiles")
        elif s[b] == -1:
            out.add("deterioration, weighting the lower percentiles")
        else:
            out.add("ambiguous")
    return out.pop() if len(out) == 1 else "depends on prices"


def specs():
    """(name, cell grouping, theta, income statistic) for the main specification and robustness."""
    s = [("sector only", None, None, None)]
    s += [(f"sector x formality, theta {t:g}", ("sector", "formality"), t, "inc_mean") for t in THETAS]
    s += [("sector x formality, medians", ("sector", "formality"), 1.0, "inc_median"),
          ("sector x formality x establishment size", ("sector", "formality", "size2"), 1.0, "inc_mean")]
    return s


def main():
    va = (pd.read_csv(ROOT / "empirics" / "data" / "processed" / "lac_lp" / "panel_7sector.csv")
          .query("iso3 == 'MEX'").set_index(["iso3", "year", "sector"])[["va_cur_usd", "va_k2020usd"]])
    cells = {}
    for name, by, theta, stat in specs():
        if by is None:
            c = annual_cells(("sector", "formality"))
            c = c.groupby(["year", "sector"], as_index=False).agg(emp=("emp", "sum"), pop15=("pop15", "first"))
            c["segment"] = c["sector"]
            c["inc_mean"] = 1.0
        else:
            c = annual_cells(by)
            c["segment"] = c[list(by)].astype(str).agg("|".join, axis=1)
        cells[name] = c

    # implied ratios and reporting (plan §5 rules), main specification
    seg_rows, rule_rows = [], []
    main = cells["sector x formality, theta 1"]
    for y in LADDER_YEARS:
        g = main[main["year"] == y]
        for s, h in g.groupby("sector"):
            h = h.set_index("formality")
            if {"formal", "informal"} <= set(h.index):
                ratio = h.loc["informal", "inc_mean"] / h.loc["formal", "inc_mean"]
                gap = h.loc["formal", "reporting"] - h.loc["informal", "reporting"]
                rule_rows.append({"year": y, "sector": s, "informal_formal_ratio": ratio, "reporting_gap": gap,
                                  "informal_share": h.loc["informal", "emp"] / h["emp"].sum(),
                                  "ratio_out_of_range": not (0.1 <= ratio <= 1.0), "reporting_gap_over_20pp": abs(gap) > 0.20})
            for f, r in h.iterrows():
                seg_rows.append({"year": y, "sector": s, "formality": f, "emp": r["emp"], "inc_mean": r["inc_mean"],
                                 "inc_median": r["inc_median"], "reporting": r["reporting"]})
    rules = pd.DataFrame(rule_rows)
    pd.DataFrame(seg_rows).merge(rules, on=["year", "sector"], how="left").to_csv(OUT / "segments.csv", index=False)

    vrows, drows, lrows, irows = [], [], [], []
    for t0, T in PERIODS:
        per, n = f"{t0}–{T}", T - t0
        for name, by, theta, stat in specs():
            c = cells[name]
            f1, s2, res = {}, {}, {}
            for b in BASES:
                y = va_at_prices(va, "MEX", t0, T, b)
                lads, stepsets = {}, {}
                for yr, col in [(t0, "y0"), (T, "yT")]:
                    cy = c[c["year"] == yr]
                    sec_y = y[col]
                    if by is None:
                        st = pd.DataFrame({"sector": cy["sector"], "segment": cy["segment"], "emp": cy["emp"].to_numpy(),
                                           "v": (sec_y.reindex(cy["sector"]).to_numpy() / cy["emp"].to_numpy())})
                    else:
                        st = split(sec_y, cy, theta, stat)
                    stepsets[yr] = st
                    lads[yr] = ladder_of(st, cy["pop15"].iloc[0])
                    for _, r in st.iterrows():
                        lrows.append({"period": per, "spec": name, "base": b, "year": yr, "segment": r["segment"],
                                      "sector": r["sector"], "value": r["v"], "emp": r["emp"], "pop15": cy["pop15"].iloc[0]})
                d0, dT = lads[t0], lads[T]
                f1[b], s2[b] = lad.dominance(d0, dT, 1), lad.dominance(d0, dT, 2)
                res[b] = {"mean0": lad.mean(d0), "meanT": lad.mean(dT), "share_gained": lad.share_gained(d0, dT)}
                if b == "initial":
                    if name in ("sector only", "sector x formality, theta 1"):
                        grid, inc = lad.incidence(d0, dT, n, grid=(np.arange(100) + 0.5) / 100)
                        irows += [{"period": per, "spec": name, "pct": round(100 * p, 1), "incidence_pp": x}
                                  for p, x in zip(grid, inc)]
                    # decomposition of output per worker on these steps, and the employment-rate term
                    s0, sT = stepsets[t0].set_index("segment"), stepsets[T].set_index("segment")
                    yy = pd.DataFrame({"y0": s0["v"] * s0["emp"], "yT": sT["v"] * sT["emp"]}).dropna()
                    r = decompose(yy, s0["emp"].reindex(yy.index), sT["emp"].reindex(yy.index), n)
                    w0 = c[c["year"] == t0]["pop15"].iloc[0]
                    wT = c[c["year"] == T]["pop15"].iloc[0]
                    er = 100 * np.log((sT["emp"].sum() / wT) / (s0["emp"].sum() / w0)) / n
                    drows.append({"period": per, "spec": name, "growth_pp": r["growth_pp"], "within_pp": r["within_pp"],
                                  "between_pp": r["struct_pp"], "static_pp": r["static_pp"], "dynamic_pp": r["dynamic_pp"],
                                  "emprate_log_pp": er, "P0": r["P0"], "PT": r["PT"]})
            verdict = classify(f1, s2)
            for b in BASES:
                vrows.append({"period": per, "spec": name, "base": b, "fsd": f1[b], "ssd": s2[b], "verdict": verdict,
                              "mean_growth_pp": (res[b]["meanT"] / res[b]["mean0"] - 1) / n * 100,
                              "share_gained": res[b]["share_gained"]})
    v = pd.DataFrame(vrows)
    v.to_csv(OUT / "verdicts.csv", index=False)
    d = pd.DataFrame(drows)
    # between segments within sectors = segment-level between minus sector-level between (plan §4.3)
    sec = d[d["spec"] == "sector only"].set_index("period")
    d["between_sector_pp"] = d["period"].map(sec["between_pp"])
    d["between_within_sector_pp"] = d["between_pp"] - d["between_sector_pp"]
    d["within_sector_level_pp"] = d["period"].map(sec["within_pp"])
    d.to_csv(OUT / "decomposition.csv", index=False)
    pd.DataFrame(lrows).to_csv(OUT / "ladders.csv", index=False)
    pd.DataFrame(irows).to_csv(OUT / "incidence.csv", index=False)
    print(v[v["base"] == "initial"].pivot(index="spec", columns="period", values="verdict").to_string())
    print(d[["period", "spec", "growth_pp", "within_pp", "between_sector_pp", "between_within_sector_pp",
             "emprate_log_pp"]].round(3).to_string(index=False))
    print(rules.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
