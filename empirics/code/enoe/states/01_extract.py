"""Study 9.6, step 1: per-quarter extracts of persons aged 16-70 and state population by quarter
(pre-analysis plan §2, D-059).

    python empirics/code/enoe/states/01_extract.py

Extracts go to the uncommitted empirics/data/raw/enoe_interim/states/q_YYYY_Q.parquet; state
population (all ages) and the formal share of employment by state and quarter to
empirics/output/enoe/states/state_quarters.csv.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import enoe_io  # noqa: E402
from enoe_config import INTERIM, KEY, OUTPUT_ROOT, URBAN_MAX_CD_A  # noqa: E402

OUT = OUTPUT_ROOT / "states"
TMP = INTERIM / "states"
ERAS = {"2005-2019": [(y, q) for y in range(2005, 2020) for q in (1, 2, 3, 4)],
        "2022-": [(y, q) for y in range(2022, 2027) for q in (1, 2, 3, 4)]}
SDEM = KEY + ["n_ent", "tipo", "r_def", "c_res", "eda", "sex", "anios_esc", "clase2", "emp_ppal", "rama_est2", "ingocup",
              "hrsocup", "fac", "fac_tri", "upm"]
NUM = ["n_ent", "r_def", "c_res", "eda", "sex", "anios_esc", "clase2", "emp_ppal", "rama_est2", "ingocup", "hrsocup",
       "fac", "fac_tri"]


def available(y, q):
    try:
        enoe_io.find("sdem", y, q)
        return True
    except FileNotFoundError:
        return False


def process(job):
    era, y, q = job
    f, fs = TMP / f"q_{y}_{q}.parquet", TMP / f"pop_{y}_{q}.csv"
    if f.exists() and fs.exists():
        return pd.read_csv(fs)
    s = enoe_io.read("sdem", y, q, SDEM)
    for c in NUM:
        if c in s.columns:
            s[c] = pd.to_numeric(s[c], errors="coerce")
    if "fac" not in s.columns or s["fac"].isna().all():
        s["fac"] = s["fac_tri"]
    s = s[(s["r_def"] == 0) & s["c_res"].isin([1, 3])].copy()
    keys = KEY + (["tipo"] if "tipo" in s.columns else [])
    for k in keys + ["upm"]:
        s[k] = s[k].astype(str).str.strip()
    s["ent_i"] = pd.to_numeric(s["ent"], errors="coerce").astype(int)
    s["state"] = np.where(s["clase2"] != 1, "N", np.where(s["emp_ppal"] == 2, "F", np.where(s["emp_ppal"] == 1, "I", "U")))
    s["urban"] = pd.to_numeric(s["cd_a"], errors="coerce") <= URBAN_MAX_CD_A
    s["lnw"] = np.log(np.where((s["ingocup"] > 0) & (s["hrsocup"] > 0), s["ingocup"] / (s["hrsocup"] * 4.3), np.nan))
    a = s[s["eda"].between(16, 65)]
    emp = a[a["state"].isin(["F", "I"])]
    pop = pd.DataFrame({"pop_all": s.groupby("ent_i")["fac"].sum(),
                        "pop_16_65": a.groupby("ent_i")["fac"].sum(),
                        "formal_share": emp[emp["state"] == "F"].groupby("ent_i")["fac"].sum() / emp.groupby("ent_i")["fac"].sum(),
                        "emp_rate": emp.groupby("ent_i")["fac"].sum() / a.groupby("ent_i")["fac"].sum()}).reset_index()
    pop["year"], pop["q"], pop["era"] = y, q, era
    keep = keys + ["n_ent", "ent_i", "eda", "sex", "anios_esc", "state", "rama_est2", "lnw", "fac", "upm", "urban"]
    s[s["eda"].between(16, 70)][list(dict.fromkeys(keep))].to_parquet(f, index=False)
    pop.to_csv(fs, index=False)
    print(y, q, len(s), flush=True)
    return pop


def main():
    from multiprocessing import Pool
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(era, y, q) for era, qs in ERAS.items() for y, q in qs if available(y, q)]
    with Pool(2) as pool:
        parts = pool.map(process, jobs, chunksize=1)
    pd.concat(parts).sort_values(["year", "q", "ent_i"]).to_csv(OUT / "state_quarters.csv", index=False, float_format="%.6g")
    return 0


if __name__ == "__main__":
    sys.exit(main())
