"""Study 9.8, step 2: state x activity x year cells with outcomes and the 2018 bite (pre-analysis plan §2).

    python empirics/code/enoe/minimum_wage_bite/02_cells.py

Outputs (empirics/output/enoe/minimum_wage_bite/):
    bite.csv        unit, group, bite18, bite17, kaitz, bite18_formal, n18 (full-time wage employees with income
                    in 2018), emp18 (employed persons 15+, 2018)
    cells_year.csv  unit, group, year: emp, formal, w_all, w_formal, w_informal, p10, p50, below_current, hours,
                    va, lprod, n_emp, n_wage
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parents[1] / "state_productivity"))

from activities import FINE, MAIN, distribute, fine_code, to_main  # noqa: E402
from enoe_config import INTERIM  # noqa: E402

_p = importlib.util.spec_from_file_location("panel97", HERE.parents[1] / "state_productivity" / "02_panel.py")
pm = importlib.util.module_from_spec(_p)
_p.loader.exec_module(pm)

ROOT = HERE.parents[4]
OUT = ROOT / "empirics" / "output" / "enoe" / "minimum_wage_bite"
TMP = INTERIM / "minimum_wage_bite"
UNIT31 = {15: 9}
# daily minimum wage (pesos): general; northern border zone from 2019 (L169). 2015: general area from
# October 2015 (70.10); 2017: 80.04 until November, 88.36 from December.
MW = {2015: 70.10, 2016: 73.04, 2017: 80.04, 2018: 88.36, 2019: 102.68, 2020: 123.22, 2021: 141.70, 2022: 172.87,
      2023: 207.44, 2024: 248.93}
MW_ZONE = {2019: 176.72, 2020: 185.56, 2021: 213.39, 2022: 260.34, 2023: 312.41, 2024: 374.89}
RATIO = MW[2019] / MW[2018]


def wq(x, w, q):
    o = np.argsort(x)
    x, w = np.asarray(x)[o], np.asarray(w)[o]
    c = np.cumsum(w) / w.sum()
    return x[np.searchsorted(c, q)]


def zone_set():
    z = pd.read_csv(ROOT / "empirics" / "output" / "enoe" / "border_mw" / "municipalities.csv")
    return set(zip(z["ent"][z["zlfn"]], z["mun"][z["zlfn"]]))


def nonresponse_weights(d):
    """Weighting classes for earnings non-response among wage employees with positive hours (study 9.7)."""
    d = d.copy()
    d["resp"] = (d["ingocup"] > 0).astype(int)
    d["age5"] = (d["eda"].clip(15, 74) // 5).astype(int)
    d["sch"] = pd.cut(d["anios_esc"].where(d["anios_esc"] < 99), [-1, 5, 8, 11, 99], labels=False).fillna(-1)
    out = np.zeros(len(d))
    for cls in (["year", "ent", "seg", "age5", "sch"], ["year", "ent", "seg"]):
        tot = d.groupby(cls)["w"].transform("sum")
        rw = d["w"].where(d["resp"] == 1, 0).groupby([d[c] for c in cls]).transform("sum")
        nr = d["resp"].groupby([d[c] for c in cls]).transform("sum")
        adj = (tot / rw.replace(0, np.nan)).values
        if cls[-1] == "sch":
            fine, small = adj, (nr < 20).values
        else:
            out = np.where(small, adj, fine)
    return d["w"].values * out * d["resp"].values


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    zones = zone_set()
    files = sorted(TMP.glob("q_*.parquet"))
    emp_rows, wages = [], []
    for f in files:
        d = pd.read_parquet(f)
        d["unit"] = d["ent"].replace(UNIT31)
        d["seg"] = np.where(d["emp_ppal"] == 2, "f", "i")
        e = d[d["clase2"] == 1].copy()
        e["act"] = fine_code(e["p4a"].values)
        e["wf"] = e["w"] * (e["seg"] == "f")
        e["wh"] = e["w"] * e["hrsocup"].fillna(0)
        e["n"] = 1
        emp_rows.append(e.groupby(["year", "q", "ent", "act"], as_index=False)[["w", "wf", "wh", "n"]].sum())
        x = e[(e["pos_ocu"] == 1) & (e["hrsocup"] > 0)].copy()
        x["group"] = pd.Series(to_main(x["act"].values), index=x.index)
        x = x[x["group"].notna()]
        x["zone"] = [(a, b) in zones for a, b in zip(x["ent"], x["mun"])]
        wages.append(x[["year", "q", "ent", "unit", "mun", "zone", "group", "seg", "w", "ingocup", "hrsocup", "eda",
                        "anios_esc"]])
        print(f.name, flush=True)
    # employment, formal share, hours (unspecified codes distributed within state and year)
    q = pd.concat(emp_rows, ignore_index=True)
    nq = q.groupby("year")["q"].nunique()
    a = q.groupby(["year", "ent", "act"], as_index=False)[["w", "wf", "wh", "n"]].sum()
    for c in ("w", "wf", "wh"):
        a[c] /= a["year"].map(nq)
    a = distribute(a, ["year", "ent"], ["w", "wf", "wh", "n"])
    a["group"] = to_main(a["act"].values)
    a["unit"] = a["ent"].replace(UNIT31)
    E = a.groupby(["unit", "group", "year"], as_index=False)[["w", "wf", "wh", "n"]].sum()
    E = E.rename(columns={"w": "emp", "n": "n_emp"})
    E["formal"] = E["wf"] / E["emp"]
    E["hours"] = E["wh"] / E["emp"]
    # value added
    pibe = pd.concat([pm.pibe_activity(c) for c in FINE], ignore_index=True)
    pibe["group"] = to_main(pibe["act"].values)
    pibe["unit"] = pibe["ent"].replace(UNIT31)
    V = pibe[pibe["year"].between(2015, 2024)].groupby(["unit", "group", "year"], as_index=False)["va_k"].sum()
    # wages
    W = pd.concat(wages, ignore_index=True)
    W["wa"] = nonresponse_weights(W)
    W["mw"] = [MW_ZONE[y] if (z and y >= 2019) else MW[y] for y, z in zip(W["year"], W["zone"])]
    r = W[W["ingocup"] > 0].copy()
    r["lw"] = np.log(r["ingocup"] / (4.33 * r["hrsocup"]))
    rows = []
    for (u, g, y), x in r.groupby(["unit", "group", "year"]):
        ft = x[x["hrsocup"] >= 35]
        row = {"unit": u, "group": g, "year": y, "n_wage": len(x),
               "w_all": np.average(x["lw"], weights=x["wa"]),
               "p10": wq(x["lw"].values, x["wa"].values, 0.10), "p50": wq(x["lw"].values, x["wa"].values, 0.50),
               "below_current": np.average(ft["ingocup"] < 30.4 * ft["mw"], weights=ft["w"]) if len(ft) else np.nan}
        for s, lab in (("f", "w_formal"), ("i", "w_informal")):
            xs = x[x["seg"] == s]
            row[lab] = np.average(xs["lw"], weights=xs["wa"]) if len(xs) >= 20 else np.nan
        rows.append(row)
    Wc = pd.DataFrame(rows)
    cells = E.merge(V, on=["unit", "group", "year"], how="left").merge(Wc, on=["unit", "group", "year"], how="left")
    cells["va"] = cells["va_k"]
    cells["lprod"] = np.log(cells["va"] / cells["emp"])
    cells = cells[["unit", "group", "year", "emp", "formal", "w_all", "w_formal", "w_informal", "p10", "p50",
                   "below_current", "hours", "va", "lprod", "n_emp", "n_wage"]]
    cells.sort_values(["unit", "group", "year"]).to_csv(OUT / "cells_year.csv", index=False, float_format="%.6f")
    # bite (2018), 2017 version, Kaitz, formal-only
    ft = r[r["hrsocup"] >= 35].copy()
    t18 = ft[ft["year"] == 2018].copy()
    t18["thr"] = 30.4 * np.where(t18["zone"], MW_ZONE[2019], MW[2019])
    t17 = ft[(ft["year"] == 2017) & (ft["q"] <= 3)].copy()
    t17["thr"] = 30.4 * RATIO * MW[2017] * np.where(t17["zone"], MW_ZONE[2019] / MW[2019], 1.0)
    b = []
    for (u, g), x in t18.groupby(["unit", "group"]):
        x17 = t17[(t17["unit"] == u) & (t17["group"] == g)]
        xf = x[x["seg"] == "f"]
        b.append({"unit": u, "group": g, "n18": len(x),
                  "bite18": np.average(x["ingocup"] < x["thr"], weights=x["w"]),
                  "bite17": np.average(x17["ingocup"] < x17["thr"], weights=x17["w"]) if len(x17) else np.nan,
                  "kaitz": 30.4 * MW[2018] / wq(x["ingocup"].values, x["w"].values, 0.5),
                  "bite18_formal": np.average(xf["ingocup"] < xf["thr"], weights=xf["w"]) if len(xf) else np.nan})
    b = pd.DataFrame(b).merge(E[E["year"] == 2018][["unit", "group", "emp"]].rename(columns={"emp": "emp18"}),
                              on=["unit", "group"], how="left")
    b.to_csv(OUT / "bite.csv", index=False, float_format="%.6f")
    print(f"cells {len(b)}, with n18 >= 100: {(b['n18'] >= 100).sum()}; national bite "
          f"{np.average(t18['ingocup'] < t18['thr'], weights=t18['w']):.3f}")


if __name__ == "__main__":
    main()
