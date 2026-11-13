"""Study 9.2, step 1: one cross-section a year (first quarters 2005-2025) with the variables needed
for experience-earnings profiles (pre-analysis plan §2).

    python empirics/code/enoe/profiles/01_extract.py

Writes the person-level extract to the uncommitted empirics/data/raw/enoe_interim/profiles_cs.parquet.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # shared ENOE modules

import pandas as pd  # noqa: E402

import enoe_io  # noqa: E402
from enoe_config import CROSS_SECTIONS, INTERIM  # noqa: E402

COLS = ["ent", "upm", "ca", "eda", "sex", "anios_esc", "ing_x_hrs", "hrsocup", "pos_ocu", "ambito2", "emp_ppal",
        "rama_est2", "clase2", "fac", "fac_tri", "r_def", "c_res"]
NUM = ["eda", "sex", "anios_esc", "ing_x_hrs", "hrsocup", "pos_ocu", "ambito2", "emp_ppal", "rama_est2", "clase2",
       "r_def", "c_res"]


def extract(year, q):
    d = enoe_io.read("sdem", year, q, COLS)
    for c in NUM:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[(d["r_def"] == 0) & d["c_res"].isin([1, 3]) & d["eda"].between(15, 80)].copy()
    d["w"] = pd.to_numeric(d["fac_tri"] if "fac_tri" in d.columns else d["fac"], errors="coerce")
    d["psu"] = (d["ca"].astype(str) + "-" if "ca" in d.columns else "") + d["upm"].astype(str)
    keep = ["year", "ent", "psu", "w"] + [c for c in NUM if c not in ("r_def", "c_res")]
    return d[keep]


def main():
    INTERIM.mkdir(parents=True, exist_ok=True)
    parts = []
    for y, q in CROSS_SECTIONS:
        try:
            parts.append(extract(y, q))
            print(f"{y}Q{q}: {len(parts[-1]):,} persons aged 15-80")
        except FileNotFoundError as e:
            print(f"[skip] {e}")
    pd.concat(parts, ignore_index=True).to_parquet(INTERIM / "profiles_cs.parquet", index=False)


if __name__ == "__main__":
    main()
