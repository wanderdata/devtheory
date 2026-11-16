"""Study 9.7, step 1b: population aged 15+ by quarter, state and PSU (weighted), used to calibrate the
bootstrap replicates to state population (D-067).

    python empirics/code/enoe/state_productivity/01b_population.py

Output (uncommitted): empirics/data/raw/enoe_interim/state_productivity/population_psu.parquet
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import pandas as pd  # noqa: E402

import enoe_io  # noqa: E402
from enoe_config import INTERIM, KEY  # noqa: E402

TMP = INTERIM / "state_productivity"
YEARS = [2005, 2006, 2007, 2017, 2018, 2019, 2022, 2023, 2024]


def process(job):
    y, q = job
    s = enoe_io.read("sdem", y, q, KEY + ["r_def", "c_res", "eda", "fac", "fac_tri", "upm"])
    for c in ("r_def", "c_res", "eda", "fac", "fac_tri"):
        if c in s.columns:
            s[c] = pd.to_numeric(s[c], errors="coerce")
    s["w"] = s["fac_tri"] if "fac_tri" in s.columns and s["fac_tri"].notna().any() else s["fac"]
    s = s[(s["r_def"] == 0) & s["c_res"].isin([1, 3]) & (s["eda"] >= 15)]
    s["ent"] = pd.to_numeric(s["ent"], errors="coerce").astype(int)
    s["upm"] = s["upm"].astype(str).str.strip()
    g = s.groupby(["ent", "upm"], as_index=False)["w"].sum().rename(columns={"w": "pop"})
    g["year"], g["q"] = y, q
    return g


def main():
    from multiprocessing import Pool
    with Pool(2) as pool:
        out = pool.map(process, [(y, q) for y in YEARS for q in (1, 2, 3, 4)])
    pd.concat(out, ignore_index=True).to_parquet(TMP / "population_psu.parquet", index=False)
    print("done")


if __name__ == "__main__":
    main()
