"""Study 9.7, step 1: per-quarter extracts of employed persons aged 15+ with the industry code of
the main job (pre-analysis plan §2, D-065).

    python empirics/code/enoe/state_productivity/01_extract.py

Person-level extracts go to the uncommitted empirics/data/raw/enoe_interim/state_productivity/
q_YYYY_Q.parquet (microdata never enter the repository). Aggregation to state x activity cells is
done in step 2.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import pandas as pd  # noqa: E402

import enoe_io  # noqa: E402
from enoe_config import INTERIM, KEY  # noqa: E402

TMP = INTERIM / "state_productivity"
QUARTERS = [(y, q) for y in list(range(2005, 2020)) + [2022, 2023, 2024] for q in (1, 2, 3, 4)]
SDEM = KEY + ["tipo", "r_def", "c_res", "eda", "sex", "anios_esc", "clase2", "emp_ppal", "pos_ocu", "ingocup",
              "hrsocup", "fac", "fac_tri", "upm"]
NUM = ["r_def", "c_res", "eda", "sex", "anios_esc", "clase2", "emp_ppal", "pos_ocu", "ingocup", "hrsocup", "fac", "fac_tri"]


def process(job):
    y, q = job
    f = TMP / f"q_{y}_{q}.parquet"
    if f.exists():
        return y, q, "cached"
    s = enoe_io.read("sdem", y, q, SDEM)
    for c in NUM:
        if c in s.columns:
            s[c] = pd.to_numeric(s[c], errors="coerce")
    s["w"] = s["fac_tri"] if "fac_tri" in s.columns and s["fac_tri"].notna().any() else s["fac"]
    s = s[(s["r_def"] == 0) & s["c_res"].isin([1, 3]) & (s["eda"] >= 15) & (s["clase2"] == 1)].copy()
    keys = KEY + (["tipo"] if "tipo" in s.columns else [])
    c = enoe_io.read("coe1", y, q, keys + ["p4a"])
    for d in (s, c):
        for k in keys:
            d[k] = d[k].astype(str).str.strip()
    c = c.drop_duplicates(keys)
    s = s.merge(c, on=keys, how="left")
    s["p4a"] = pd.to_numeric(s["p4a"], errors="coerce").fillna(0).astype(int)
    s["ent"] = pd.to_numeric(s["ent"], errors="coerce").astype(int)
    s["upm"] = s["upm"].astype(str).str.strip()
    s["year"], s["q"] = y, q
    keep = ["year", "q", "ent", "upm", "w", "p4a", "emp_ppal", "pos_ocu", "ingocup", "hrsocup", "eda", "sex", "anios_esc"]
    TMP.mkdir(parents=True, exist_ok=True)
    s[keep].to_parquet(f, index=False)
    return y, q, len(s)


def main():
    from multiprocessing import Pool
    TMP.mkdir(parents=True, exist_ok=True)
    with Pool(2) as pool:
        for r in pool.imap_unordered(process, QUARTERS):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
