"""Extract ILO modelled labour-market indicators for the dashboard.

    python empirics/code/lp/06_extract_labour.py [files ...]

Recognises these ILOSTAT bulk files (modelled estimates) by their indicator
column, in empirics/data/raw/<scope>_lp/ or given as arguments:
    EMP_2WAP_SEX_AGE_RT_A   employment-to-population ratio (%), 15+
    EAP_2WAP_SEX_AGE_RT_A   labour force participation rate (%), 15+
    UNE_2EAP_SEX_AGE_RT_A   unemployment rate (%), 15+
    GDP_2HRW_NOC_NB_A       output per hour worked (GDP, constant 2021 PPP $)
    HOW_2EMP_SEX_NB_A       mean weekly hours actually worked per employed person

ILO files run to 2027 with projections; years after MAX_YEAR are dropped
(2025, the reference document's last year).

Writes empirics/data/interim/<scope>_lp/ilo_labour.csv
    (iso3, year, indicator, value), indicator in {emp_rate, part_rate, unemp_rate, lp_hour, hours}
"""
import sys
from pathlib import Path

import pandas as pd

from config import COUNTRIES, INTERIM, RAW, SOURCE

MAX_YEAR = 2025
WANT = {"EMP_2WAP": "emp_rate", "EAP_2WAP": "part_rate", "UNE_2EAP": "unemp_rate",
        "GDP_2HRW": "lp_hour", "HOW_2EMP": "hours"}


def read(path):
    df = pd.read_csv(path, dtype=str, low_memory=False)
    if "indicator" not in df.columns or "ref_area" not in df.columns:
        return None
    ind = str(df["indicator"].dropna().iloc[0])
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
            print(f"[ok  ] {p.name}: {r['indicator'].iloc[0]}, {len(r)} rows, {r['iso3'].nunique()} countries")
            parts.append(r)
    if not parts:
        print("No labour-market files found.")
        return
    out = pd.concat(parts).drop_duplicates(["iso3", "year", "indicator"]).sort_values(["indicator", "iso3", "year"])
    out.to_csv(INTERIM / "ilo_labour.csv", index=False)
    print(f"wrote {INTERIM / 'ilo_labour.csv'}: {sorted(out['indicator'].unique())}")


if __name__ == "__main__":
    main(sys.argv[1:])
