"""Study 9.4, step 1: person records for 2016Q1-2020Q1 and links between consecutive quarters
(pre-analysis plan §§2-3). Microdata stay in the uncommitted interim folder.

    python empirics/code/enoe/border_mw/01_extract.py

Writes empirics/data/raw/enoe_interim/border_mw/persons.parquet (aged 15+, residents with complete
interviews) and pairs.parquet (persons linked across consecutive quarters, origin and destination
states), and the linkage diagnostics to empirics/output/enoe/border_mw/linkage.csv.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import pandas as pd  # noqa: E402

import enoe_io  # noqa: E402
import enoe_link  # noqa: E402
from enoe_config import BORDER_QUARTERS, INTERIM, KEY, OUTPUT_ROOT, RAW  # noqa: E402

OUT = OUTPUT_ROOT / "border_mw"
TMP = INTERIM / "border_mw"
COLS = KEY + ["n_ent", "eda", "sex", "anios_esc", "clase2", "pos_ocu", "emp_ppal", "ingocup", "ing_x_hrs", "hrsocup",
              "fac", "r_def", "c_res", "upm", "mun", "zona"]
NUM = ["n_ent", "eda", "sex", "anios_esc", "clase2", "pos_ocu", "emp_ppal", "ingocup", "ing_x_hrs", "hrsocup", "fac",
       "r_def", "c_res", "zona"]


def state(d):
    """F formal employed, I informal employed, N not employed (unemployed or out of the labour
    force). Employed with unknown formality: U."""
    emp = d["clase2"] == 1
    s = pd.Series("N", index=d.index)
    s[emp & (d["emp_ppal"] == 2)] = "F"
    s[emp & (d["emp_ppal"] == 1)] = "I"
    s[emp & ~d["emp_ppal"].isin([1, 2])] = "U"
    return s


def quarter(y, q):
    d = enoe_io.read("sdem", y, q, COLS)
    for c in NUM:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[(d["r_def"] == 0) & d["c_res"].isin([1, 3]) & (d["eda"] >= 15) & (d["eda"] <= 98)].copy()
    for k in KEY:
        d[k] = d[k].astype(str).str.strip()
    d["mun"] = pd.to_numeric(d["mun"].astype(str).str.strip(), errors="coerce")
    d["ent_i"] = pd.to_numeric(d["ent"], errors="coerce").astype(int)
    d["upm"] = d["upm"].astype(str).str.strip()
    d["state"] = state(d)
    d["year"], d["q"], d["t"] = y, q, (y - 2016) * 4 + (q - 1)
    return d.reset_index(drop=True)


def main():
    if not any(RAW.glob("*2019trim1*")):
        print(f"No ENOE files in {RAW}: run 00_fetch.py first. Nothing done.")
        return 0
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    keep = ["ent_i", "mun", "upm", "zona", "n_ent", "eda", "sex", "anios_esc", "pos_ocu", "state", "ingocup",
            "ing_x_hrs", "hrsocup", "fac", "year", "q", "t"]
    persons, pairs, diags = [], [], []
    prev = None
    for y, q in BORDER_QUARTERS:
        d = quarter(y, q)
        persons.append(d[keep])
        if prev is not None:
            m, dg = enoe_link.link(prev, d)
            dg.update({"year": y, "q": q})
            diags.append(dg)
            pairs.append(pd.DataFrame({
                "ent_i": m["ent_i_0"], "mun": m["mun_0"], "upm": m["upm_0"], "t": m["t_1"],
                "eda": m["eda_0"], "sex": m["sex_0"], "anios_esc": m["anios_esc_0"], "fac": m["fac_0"],
                "s0": m["state_0"], "s1": m["state_1"]}))
        prev = d
        print(y, q, len(d))
    pd.concat(persons, ignore_index=True).to_parquet(TMP / "persons.parquet", index=False)
    pd.concat(pairs, ignore_index=True).to_parquet(TMP / "pairs.parquet", index=False)
    pd.DataFrame(diags).to_csv(OUT / "linkage.csv", index=False)
    print(pd.DataFrame(diags)[["year", "q", "eligible", "accepted", "match_rate"]].round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
