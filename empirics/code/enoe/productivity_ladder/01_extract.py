"""Study 9.3, step 1: employment, population aged 15+ and labour income by sector x formality x
establishment size, for each quarter of the ladder years (pre-analysis plan §2).

    python empirics/code/enoe/productivity_ladder/01_extract.py

Writes aggregate cells (weighted counts and income statistics, no microdata) to
empirics/output/enoe/productivity_ladder/cells.csv.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import enoe_io  # noqa: E402
from enoe_config import LADDER_YEARS, OUTPUT_ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "productivity_ladder"
SECTOR7 = {1: "AGR", 2: "MIU", 3: "MAN", 4: "CON", 5: "TRH", 6: "TRH", 7: "TSC", 8: "OTH", 9: "OTH", 10: "OTH", 11: "OTH"}
SIZE2 = {2: "micro and small", 3: "micro and small", 4: "micro and small", 5: "medium and large",
         6: "medium and large", 7: "government", 8: "other"}
COLS = ["eda", "clase2", "rama_est2", "emp_ppal", "ambito2", "pos_ocu", "ingocup", "fac", "fac_tri", "r_def", "c_res"]


def wmedian(x, w):
    o = np.argsort(x)
    x, w = np.asarray(x)[o], np.asarray(w)[o]
    c = np.cumsum(w)
    return float(x[np.searchsorted(c, c[-1] / 2)]) if len(x) else np.nan


def quarter(year, q):
    d = enoe_io.read("sdem", year, q, COLS)
    for c in COLS:
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    d["w"] = d["fac_tri"] if "fac_tri" in d.columns and d["fac_tri"].notna().any() else d["fac"]
    d = d[(d["r_def"] == 0) & d["c_res"].isin([1, 3]) & d["eda"].between(15, 98)]
    pop = d["w"].sum()
    e = d[d["clase2"] == 1].copy()
    e["sector"] = e["rama_est2"].map(SECTOR7).fillna("UNS")
    e["formality"] = e["emp_ppal"].map({1: "informal", 2: "formal"}).fillna("unspecified")
    e["size2"] = e["ambito2"].map(SIZE2).fillna("other")
    e["paid"] = e["pos_ocu"] != 4
    e["inc_ok"] = e["ingocup"] > 0
    rows = []
    for (s, f, z), g in e.groupby(["sector", "formality", "size2"]):
        paid = g[g["paid"]]
        ok = paid[paid["inc_ok"]]
        rows.append({"year": year, "quarter": q, "sector": s, "formality": f, "size2": z,
                     "emp": g["w"].sum(), "paid_emp": paid["w"].sum(), "inc_w": ok["w"].sum(),
                     "inc_sum": (ok["w"] * ok["ingocup"]).sum(), "inc_median": wmedian(ok["ingocup"], ok["w"]),
                     "n": len(g), "n_inc": len(ok), "pop15": pop})
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    parts = []
    for y in LADDER_YEARS:
        for q in (1, 2, 3, 4):
            parts.append(quarter(y, q))
            print(f"{y}Q{q}: population 15+ {parts[-1]['pop15'].iloc[0] / 1e6:.1f} m, employed {parts[-1]['emp'].sum() / 1e6:.1f} m")
    pd.concat(parts, ignore_index=True).to_csv(OUT / "cells.csv", index=False)


if __name__ == "__main__":
    main()
