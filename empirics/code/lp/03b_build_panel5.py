"""Grid B: 5-sector employment panel (AGR, MIU, MAN, CON, SER) (D-025).

    python empirics/code/lp/03b_build_panel5.py      (run after 03_build_panel.py)

Services (trade, hotels, transport, communication, finance, business,
government, personal) are one sector. This lets survey years that ILO only
publishes as six broad groups (ECO_AGGREGATE: AGR, MEL, MAN, CON, MKT, PUB)
enter the panel, at the cost of hiding all reallocation within services.

Employment only: value added for grid B is built in the decomposition step by
summing the 7-sector values after they are re-referenced to a common price
year, so it stays additive.

Output: empirics/data/processed/<scope>_lp/emp_5sector.csv
        (iso3, year, series, source, origin, sector, emp, x_share)
"""
import numpy as np
import pandas as pd

from config import INTERIM, PROCESSED
from importlib import import_module

bp = import_module("03_build_panel")

GRID5 = {"AGR": "AGR", "MIU": "MIU", "MAN": "MAN", "CON": "CON",
         "TRH": "SER", "TSC": "SER", "OTH": "SER"}
SECTORS5 = ["AGR", "MIU", "MAN", "CON", "SER"]
AGG6 = {"AGR": "AGR", "MEL": "MIU", "MAN": "MAN", "CON": "CON", "MKT": "SER", "PUB": "SER"}


def collapse7(emp7, series):
    """7-sector rows (complete years only) -> 5 sectors."""
    e = emp7[emp7["missing_sectors"] == ""].copy()
    e["sector5"] = e["sector"].map(GRID5)
    g = (e.groupby(["iso3", "year", "source", "sector5"], as_index=False)
           .agg(emp=("emp", "sum"), x_share=("x_share", "first")))
    g = g.rename(columns={"sector5": "sector"})
    g["series"], g["origin"] = series, "isic"
    return g


def from_six_groups(totals):
    """Survey country-years from ILO's six broad groups (all six present)."""
    s = pd.read_csv(INTERIM / "ilo_emp_survey.csv", low_memory=False)
    s = s[(s["sex"] == "SEX_T") & s["classif1"].str.startswith("ECO_AGGREGATE_") & s["obs_value"].notna()]
    s["grp"] = s["classif1"].str.split("_").str[-1]
    s["year"] = s["time"].astype(str).str[:4].astype(int)
    rows = []
    for (iso, src, yr), g in s.groupby(["ref_area", "source", "year"]):
        v = g.set_index("grp")["obs_value"]
        if not set(AGG6) <= set(v.index):
            continue
        x = v.get("X", 0.0)
        total = v.get("TOTAL", v[list(AGG6)].sum() + x)
        if total and x / total > bp.MAX_X_SHARE:
            continue
        mt = totals.get((iso, yr), np.nan)
        if np.isfinite(mt) and total / mt < bp.MIN_COVERAGE:   # not national (D-031)
            continue
        classified = v[list(AGG6)].sum()
        scale = total / classified
        for sec in SECTORS5:
            val = sum(v[k] for k, t in AGG6.items() if t == sec) * scale
            rows.append({"iso3": iso, "year": yr, "source": src, "sector": sec, "emp": val,
                         "x_share": x / total, "series": "survey", "origin": "six_group"})
    return pd.DataFrame(rows)


def main():
    emp_all = pd.read_csv(PROCESSED / "emp_all_sources.csv", keep_default_na=False,
                          na_values=[""], dtype={"missing_sectors": str})
    emp_all["missing_sectors"] = emp_all["missing_sectors"].fillna("")
    model7, _ = bp.sectorize(pd.read_csv(INTERIM / "ilo_emp_model.csv", low_memory=False), "model")

    model5 = collapse7(model7, "model")
    surv_isic = collapse7(emp_all, "survey")
    surv_six = from_six_groups(bp.model_totals(model7).to_dict())
    # ISIC-derived years take precedence; six-group years fill the rest.
    have = set(zip(surv_isic["iso3"], surv_isic["year"]))
    surv_six = surv_six[[(i, y) not in have for i, y in zip(surv_six["iso3"], surv_six["year"])]]
    surv = pd.concat([surv_isic, surv_six], ignore_index=True)
    # one source per country-year, same preference as grid A
    keys = surv[["iso3", "year", "source"]].drop_duplicates()
    keys["rank"] = keys["source"].map(bp.source_rank)
    best = keys.sort_values(["iso3", "year", "rank", "source"]).groupby(["iso3", "year"]).head(1)
    surv = surv.merge(best[["iso3", "year", "source"]], on=["iso3", "year", "source"])

    out = pd.concat([model5, surv], ignore_index=True).sort_values(["series", "iso3", "year", "sector"])
    out.to_csv(PROCESSED / "emp_5sector.csv", index=False)
    n = surv.groupby(["iso3", "origin"])["year"].nunique().unstack(fill_value=0)
    print("Grid B survey years by origin:\n", n)


if __name__ == "__main__":
    main()
