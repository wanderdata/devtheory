"""Read SDEMT (and the tenure questions of COE1) for each window, apply the sample rules, and
link respondents across the five quarters (pre-analysis plan §§2–3).

    python empirics/code/enoe/01_link.py

Writes the linked long panel (person id `pid`, quarter position `pos`) to the uncommitted
empirics/data/raw/enoe_interim/<window>.parquet
and aggregate linking diagnostics to empirics/output/enoe/link_diagnostics.csv.
"""
import sys

import pandas as pd

import enoe_io
import enoe_link
from enoe_config import AGE_MAX, AGE_MIN, INTERIM, KEY, KEY_OPTIONAL, OUTPUT, RAW, WINDOWS

SDEM = KEY + ["n_ent", "eda", "sex", "clase1", "clase2", "pos_ocu", "rama_est2", "ambito2", "emp_ppal",
              "ing_x_hrs", "ingocup", "hrsocup", "cs_p13_1", "fac_tri", "fac", "r_def", "c_res", "upm", "tipo",
              "mes_cal", "d_sem", "est_d_tri", "est_d"]
COE1 = KEY + ["n_ent", "tipo", "p3r_anio", "p3r_mes", "n_inf"]


def quarter(year, q):
    s = enoe_io.read("sdem", year, q, SDEM)
    for c in ["r_def", "c_res", "eda", "n_ent", "sex", "clase2", "rama_est2", "ambito2", "emp_ppal"]:
        s[c] = pd.to_numeric(s[c], errors="coerce")
    s = s[(s["r_def"] == 0) & s["c_res"].isin([1, 3]) & s["eda"].between(AGE_MIN - 1, 98)]
    if "fac_tri" not in s.columns and "fac" in s.columns:
        s = s.rename(columns={"fac": "fac_tri"})
    try:
        c = enoe_io.read("coe1", year, q, COE1)
        c = c.drop(columns=[x for x in ["year", "q"] if x in c.columns])
        on = KEY + ["n_ent"] + [k for k in KEY_OPTIONAL if k in s.columns and k in c.columns]
        for k in on:
            if k == "n_ent":
                c[k] = pd.to_numeric(c[k], errors="coerce")
            else:
                s[k], c[k] = s[k].astype(str).str.strip(), c[k].astype(str).str.strip()
        s = s.merge(c, on=on, how="left")
    except FileNotFoundError:
        pass
    for k in KEY + [k for k in KEY_OPTIONAL if k in s.columns]:
        s[k] = s[k].astype(str).str.strip()
    return s


def main():
    have = list(RAW.glob("*")) if RAW.exists() else []
    if not have:
        print(f"No ENOE files in {RAW}: run 00_fetch.py first. Nothing done.")
        return 0
    INTERIM.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    diags = []
    for w, quarters in WINDOWS.items():
        try:
            frames = [quarter(y, q) for y, q in quarters]
        except FileNotFoundError as e:
            print(f"[skip] window {w}: {e}")
            continue
        key = KEY + [k for k in KEY_OPTIONAL if all(k in f.columns for f in frames)]
        for (y, q), f in zip(quarters, frames):
            dup = int(f.duplicated(key).sum())
            print(f"{w} {y}Q{q}: {len(f)} persons, {dup} duplicated keys (key: {', '.join(key)})")
        panel, d = enoe_link.chain(frames, key)
        d["window"], d["key"] = w, "+".join(key)
        d["quarter_from"] = [f"{y}Q{q}" for y, q in quarters[:-1]]
        diags.append(d)
        panel.to_parquet(INTERIM / f"{w}.parquet", index=False)
        print(d[["quarter_from", "eligible", "accepted", "bad_sex", "bad_age", "match_rate"]].to_string(index=False))
    if diags:
        pd.concat(diags).to_csv(OUTPUT / "link_diagnostics.csv", index=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
