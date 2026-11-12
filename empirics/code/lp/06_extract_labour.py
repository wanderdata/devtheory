"""Extract ILO modelled labour-market indicators for the dashboard.

    python empirics/code/lp/06_extract_labour.py [files ...]

Recognises these ILOSTAT bulk files (modelled estimates) by their indicator
column, in empirics/data/raw/<scope>_lp/ or given as arguments:
    EMP_2WAP_SEX_AGE_RT_A   employment-to-population ratio (%), 15+
    EAP_2WAP_SEX_AGE_RT_A   labour force participation rate (%), 15+
    UNE_2EAP_SEX_AGE_RT_A   unemployment rate (%), 15+
    GDP_2HRW_NOC_NB_A       output per hour worked (GDP, constant 2021 PPP $)
    HOW_2EMP_SEX_NB_A       mean weekly hours actually worked per employed person
    POP_2POP_SEX_AGE_NB_A   population by age, UN estimates (thousands): total, 15+, 65+
    EMP_2EMP_SEX_AGE_NB_A   employment by age, ILO modelled estimates (thousands): 15+, 65+
The last two are optional (steps 08 and 09 use them when present, D-043).

ILO files run to 2027 with projections; years after MAX_YEAR are dropped
(2025, the reference document's last year).

Writes empirics/data/interim/<scope>_lp/ilo_labour.csv
    (iso3, year, indicator, value), indicator in {emp_rate, part_rate, unemp_rate, lp_hour, hours,
    and, when the optional files are present, pop_total, pop_15plus, pop_65plus, emp_15plus, emp_65plus}
"""
import sys
from pathlib import Path

import pandas as pd

from config import COUNTRIES, INTERIM, RAW, SOURCE

MAX_YEAR = 2025
WANT = {"EMP_2WAP": "emp_rate", "EAP_2WAP": "part_rate", "UNE_2EAP": "unemp_rate",
        "GDP_2HRW": "lp_hour", "HOW_2EMP": "hours"}


AGE_FILES = {"POP_2POP_SEX_AGE": "pop", "EMP_2EMP_SEX_AGE": "emp"}
FIVE_YEAR_UNDER15 = ["AGE_5YRBANDS_Y00-04", "AGE_5YRBANDS_Y05-09", "AGE_5YRBANDS_Y10-14"]


def read_age(df, prefix):
    """Counts by age band (thousands) from the population or employment-by-age files.
    Uses the aggregate bands when present and falls back on sums of five-year bands."""
    df = df[df["ref_area"].isin(COUNTRIES)]
    if "sex" in df.columns:
        df = df[df["sex"].isna() | (df["sex"] == "SEX_T")]
    df = df.assign(year=df["time"].str[:4].astype(int), v=pd.to_numeric(df["obs_value"], errors="coerce"))
    w = df.pivot_table(index=["ref_area", "year"], columns="classif1", values="v", aggfunc="first")
    cols = set(w.columns)
    five65 = [c for c in cols if c.startswith("AGE_5YRBANDS_Y") and c[14:16].isdigit() and int(c[14:16]) >= 65]
    five65 += [c for c in cols if c.startswith("AGE_5YRBANDS_YGE")]
    out = {}
    if "AGE_AGGREGATE_TOTAL" in cols:
        out[f"{prefix}_total"] = w["AGE_AGGREGATE_TOTAL"]
    if "AGE_YTHADULT_YGE15" in cols:
        out[f"{prefix}_15plus"] = w["AGE_YTHADULT_YGE15"]
    elif "AGE_AGGREGATE_TOTAL" in cols and set(FIVE_YEAR_UNDER15) <= cols:
        out[f"{prefix}_15plus"] = w["AGE_AGGREGATE_TOTAL"] - w[FIVE_YEAR_UNDER15].sum(axis=1, min_count=3)
    if "AGE_AGGREGATE_YGE65" in cols:
        out[f"{prefix}_65plus"] = w["AGE_AGGREGATE_YGE65"]
    elif five65:
        out[f"{prefix}_65plus"] = w[five65].sum(axis=1, min_count=len(five65))
    if prefix == "emp":
        out.pop("emp_total", None)
    if not out:
        return None
    long = pd.DataFrame(out).stack().rename("value").reset_index()
    long.columns = ["iso3", "year", "indicator", "value"]
    long = long[long["year"] <= MAX_YEAR]
    return long.dropna()


def read(path):
    df = pd.read_csv(path, dtype=str, low_memory=False)
    if "indicator" not in df.columns or "ref_area" not in df.columns:
        return None
    ind = str(df["indicator"].dropna().iloc[0])
    age = next((v for k, v in AGE_FILES.items() if ind.startswith(k)), None)
    if age is not None:
        return read_age(df, age)
    key = next((v for k, v in WANT.items() if ind.startswith(k)), None)
    if key is None:
        return None
    df = df[df["ref_area"].isin(COUNTRIES)]
    if "sex" in df.columns:
        df = df[df["sex"].isna() | (df["sex"] == "SEX_T")]
    if "classif1" in df.columns and df["classif1"].notna().any():
        df = df[df["classif1"].isin(["AGE_YTHADULT_YGE15", "AGE_AGGREGATE_TOTAL"])]
        if df["classif1"].nunique() > 1:
            df = df[df["classif1"] == "AGE_YTHADULT_YGE15"]
    out = pd.DataFrame({"iso3": df["ref_area"], "year": df["time"].str[:4].astype(int),
                        "indicator": key, "value": pd.to_numeric(df["obs_value"], errors="coerce")})
    out = out[out["year"] <= MAX_YEAR]
    return out.dropna().drop_duplicates(["iso3", "year", "indicator"])


def main(extra):
    paths = [p for p in (list(RAW.glob("*.csv*")) if RAW.exists() else [])
             + sorted(SOURCE.glob("ilostat/*.csv.gz")) + [Path(x) for x in extra]]
    parts = []
    for p in paths:
        try:
            r = read(p)
        except Exception as e:
            print(f"[fail] {p.name}: {e}")
            continue
        if r is not None and len(r):
            print(f"[ok  ] {p.name}: {sorted(r['indicator'].unique())}, {len(r)} rows, {r['iso3'].nunique()} countries")
            parts.append(r)
    if not parts:
        print("No labour-market files found.")
        return
    out = pd.concat(parts).drop_duplicates(["iso3", "year", "indicator"]).sort_values(["indicator", "iso3", "year"])
    out.to_csv(INTERIM / "ilo_labour.csv", index=False)
    print(f"wrote {INTERIM / 'ilo_labour.csv'}: {sorted(out['indicator'].unique())}")


if __name__ == "__main__":
    main(sys.argv[1:])
