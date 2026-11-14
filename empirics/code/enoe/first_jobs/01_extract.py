"""Study 9.5, step 1: one cached extract per quarter of persons aged 15-30, with household
variables and the never-worked answer, plus the stock of jobs of employed 15-24-year-olds
(pre-analysis plan §2, D-057).

    python empirics/code/enoe/first_jobs/01_extract.py

Quarters: 2005Q1-2019Q4 and 2022Q1 onward. Extracts go to the uncommitted
empirics/data/raw/enoe_interim/first_jobs/q_YYYY_Q.parquet; the stock to
empirics/output/enoe/first_jobs/stock.csv.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import enoe_io  # noqa: E402
from enoe_config import INTERIM, KEY, OUTPUT_ROOT, URBAN_MAX_CD_A  # noqa: E402

OUT = OUTPUT_ROOT / "first_jobs"
TMP = INTERIM / "first_jobs"
ERAS = {"2005-2019": [(y, q) for y in range(2005, 2020) for q in (1, 2, 3, 4)],
        "2022-": [(y, q) for y in range(2022, 2027) for q in (1, 2, 3, 4)]}
SDEM = KEY + ["n_ent", "tipo", "r_def", "c_res", "eda", "sex", "par_c", "anios_esc", "cs_p17", "clase2", "pos_ocu",
              "emp_ppal", "ambito2", "rama_est2", "ingocup", "hrsocup", "salario", "fac", "fac_tri", "upm"]
NUM = ["n_ent", "r_def", "c_res", "eda", "sex", "par_c", "anios_esc", "cs_p17", "clase2", "pos_ocu", "emp_ppal",
       "ambito2", "rama_est2", "ingocup", "hrsocup", "salario", "fac", "fac_tri"]
HH = ["cd_a", "ent", "con", "v_sel", "n_hog", "h_mud"]


def available(y, q):
    try:
        enoe_io.find("sdem", y, q)
        return True
    except FileNotFoundError:
        return False


def quarter(y, q):
    s = enoe_io.read("sdem", y, q, SDEM)
    for c in NUM:
        if c in s.columns:
            s[c] = pd.to_numeric(s[c], errors="coerce")
    if "fac" not in s.columns or s["fac"].isna().all():
        s["fac"] = s["fac_tri"]
    s = s[(s["r_def"] == 0) & s["c_res"].isin([1, 3]) & (s["eda"] >= 12) & (s["eda"] <= 98)].copy()
    keys = KEY + (["tipo"] if "tipo" in s.columns else [])
    for k in keys + ["upm"]:
        s[k] = s[k].astype(str).str.strip()
    s["state"] = np.where(s["clase2"] != 1, "N", np.where(s["emp_ppal"] == 2, "F", np.where(s["emp_ppal"] == 1, "I", "U")))
    # household variables from all members aged 15+
    hh = HH + (["tipo"] if "tipo" in s.columns else [])
    a = s.loc[s["eda"] >= 15, hh + ["state"]]
    hv = (a.assign(hh_formal=a["state"] == "F", hh_informal=a["state"] == "I", hh_adults=1)
          .groupby(hh)[["hh_formal", "hh_informal", "hh_adults"]].sum().reset_index())
    s = s.merge(hv, on=hh, how="left")
    c = enoe_io.read("coe1", y, q, keys + ["n_ent", "p2h4"])
    for k in keys:
        c[k] = c[k].astype(str).str.strip()
    c["n_ent"] = pd.to_numeric(c["n_ent"], errors="coerce")
    c["never"] = c["p2h4"].astype(str).str.strip() == "4"
    c = c.drop_duplicates(keys + ["n_ent"], keep=False)
    s = s.merge(c[keys + ["n_ent", "never"]], on=keys + ["n_ent"], how="left")
    s["never"] = s["never"].fillna(False).astype(bool)
    s["urban"] = pd.to_numeric(s["cd_a"], errors="coerce") <= URBAN_MAX_CD_A
    s["year"], s["q"] = y, q
    return s


def process(job):
    """Extract one quarter (skipped if its files exist) and return its stock row."""
    era, y, q = job
    f, fs = TMP / f"q_{y}_{q}.parquet", TMP / f"stock_{y}_{q}.csv"
    if f.exists() and fs.exists():
        return pd.read_csv(fs).iloc[0].to_dict()
    s = quarter(y, q)
    young = s[s["eda"].between(15, 24)]
    emp = young[young["state"].isin(["F", "I"])]
    row = {"year": y, "q": q, "era": era, "emp_15_24": emp["fac"].sum(),
           "informal_share": emp.loc[emp["state"] == "I", "fac"].sum() / emp["fac"].sum(),
           "never_share_15_24_notemp": young.loc[young["state"] == "N", "never"].mean()}
    keep = [c for c in KEY + ["tipo", "n_ent", "ent", "eda", "sex", "par_c", "anios_esc", "cs_p17", "state", "pos_ocu",
                              "ambito2", "rama_est2", "ingocup", "hrsocup", "salario", "fac", "upm", "never",
                              "hh_formal", "hh_informal", "hh_adults", "urban", "year", "q"] if c in s.columns]
    s[s["eda"].between(15, 30)][keep].loc[:, lambda d: ~d.columns.duplicated()].to_parquet(f, index=False)
    pd.DataFrame([row]).to_csv(fs, index=False)
    print(y, q, len(s), round(row["informal_share"], 3), flush=True)
    return row


def main():
    from multiprocessing import Pool
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(era, y, q) for era, qs in ERAS.items() for y, q in qs if available(y, q)]
    with Pool(2) as pool:
        stock = pool.map(process, jobs, chunksize=1)
    pd.DataFrame(stock).sort_values(["year", "q"]).to_csv(OUT / "stock.csv", index=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
