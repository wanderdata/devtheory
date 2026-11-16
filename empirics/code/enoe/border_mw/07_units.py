"""Study 9.4, step 7: sampling units added to the border zone in 2019 against those already in the
sample (pre-analysis plan §2 diagnostic; implemented after the independent audit, D-064).

    python empirics/code/enoe/border_mw/07_units.py

Weighted means for persons in border-zone municipalities in 2019, by whether their primary sampling
unit was observed in 2016-2018. Output: empirics/output/enoe/border_mw/units_2019.csv.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from enoe_config import INTERIM, OUTPUT_ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "border_mw"
TMP = INTERIM / "border_mw"
M_MONTH = 5302.0


def wm(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    return float(np.sum(x * w) / np.sum(w)) if np.sum(w) > 0 else np.nan


def main():
    p = pd.read_parquet(TMP / "persons.parquet")
    geo = pd.read_csv(OUT / "municipalities.csv")
    zone = set(zip(geo.loc[geo["zlfn"], "ent"], geo.loc[geo["zlfn"], "mun"]))
    old = set(map(tuple, p.loc[p["t"] <= 11, ["ent_i", "upm"]].drop_duplicates().to_numpy()))
    p = p[p["mun"].notna()].copy()
    in_zone = pd.Series([k in zone for k in zip(p["ent_i"], p["mun"].astype(int))], index=p.index)
    p = p[in_zone & (p["year"] == 2019)].copy()
    p["old"] = pd.Series([k in old for k in zip(p["ent_i"], p["upm"])], index=p.index)
    rows = []
    for o, g in p.groupby("old"):
        we = g[(g["pos_ocu"] == 1) & g["eda"].between(16, 65) & (g["state"] != "N")]
        rep = we["ingocup"] > 0
        emp = g["state"].isin(["F", "I"])
        rows.append({"units": "observed in 2016-2018" if o else "added in 2019", "records": len(g),
                     "sampling_units": g["upm"].nunique(),
                     "employment_rate": wm(g["state"] != "N", g["fac"]),
                     "formal_share": wm(g.loc[emp, "state"] == "F", g.loc[emp, "fac"]),
                     "reporting_share": wm(rep, we["fac"]),
                     "below_minimum_share": wm(we.loc[rep, "ingocup"] < M_MONTH, we.loc[rep, "fac"]),
                     "mean_age": wm(g["eda"], g["fac"])})
    r = pd.DataFrame(rows)
    r.to_csv(OUT / "units_2019.csv", index=False, float_format="%.4f")
    print(r.round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
