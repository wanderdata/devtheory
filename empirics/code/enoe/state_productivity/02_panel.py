"""Study 9.7, step 2: the state x activity x year panel (pre-analysis plan §2, addendum A1).

    python empirics/code/enoe/state_productivity/02_panel.py

ENOE: annual averages of the quarterly weighted counts of employed persons aged 15+ and of hours in
the main job, by state, FINE activity and segment (formal, informal), after distributing unspecified
industry codes (activities.py). PSU-level quarterly aggregates for the bootstrap go to the uncommitted
interim folder.
PIBE: gross value added by state and FINE activity, constant 2018 and current prices.
MEITEF: informal-economy value added by state and MEITEF activity, constant 2018 and current prices.

Outputs (empirics/output/enoe/state_productivity/):
    panel_fine.csv      ent, year, act, va_k, va_c, emp_f, emp_i, hrs_f, hrs_i, inc_f, inc_i, n_f, n_i
                        (inc: weighted sum of reported monthly labour income in the main job, pesos)
    meitef_informal.csv ent, year, meitef_act, iva_k, iva_c
    panel_checks.csv    consistency checks
"""
import importlib.util
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1]))

from activities import FINE, MEITEF, distribute, fine_code  # noqa: E402
from enoe_config import INTERIM  # noqa: E402

_spec = importlib.util.spec_from_file_location("gdp97", HERE.parents[1] / "states" / "gdp.py")
gdp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gdp)

ROOT = HERE.parents[4]
OUT = ROOT / "empirics" / "output" / "enoe" / "state_productivity"
TMP = INTERIM / "state_productivity"
SRC = ROOT / "empirics" / "data" / "source" / "inegi"
K_UNIT, C_UNIT = "Millones de pesos a precios de 2018", "Millones de pesos"


def pibe_activity(code):
    name = f"conjunto_de_datos/conjunto_de_datos_pibe_actividad_{code}2024_r.csv"
    with zipfile.ZipFile(SRC / "conjunto_de_datos_pibe_csv.zip") as z:
        d = pd.read_csv(z.open(name), encoding="utf-8")
    unit = d["Descriptores"].str.split("|").str[0]
    d["name"] = d["Descriptores"].str.split("|").str[-1].str.replace("<C1>", "", regex=False).map(gdp._norm)
    codes = {gdp._norm(v): k for k, v in gdp.STATES.items()}
    years = [c for c in d.columns if c[:4].isdigit()]
    out = []
    for u, col in ((K_UNIT, "va_k"), (C_UNIT, "va_c")):
        x = d[(unit == u) & d["name"].isin(codes)].copy()
        x["ent"] = x["name"].map(codes)
        x = x.melt(id_vars=["ent"], value_vars=years, var_name="year", value_name=col)
        x["year"] = x["year"].str[:4].astype(int)
        x[col] = pd.to_numeric(x[col], errors="coerce")
        out.append(x.set_index(["ent", "year"]))
    r = pd.concat(out, axis=1).reset_index()
    r["act"] = code
    return r


def pibe_panel():
    p = pd.concat([pibe_activity(c) for c in FINE], ignore_index=True)
    bv = pibe_activity("b.1bv").rename(columns={"va_k": "gva_k", "va_c": "gva_c"}).drop(columns="act")
    oil = pibe_activity("21p").rename(columns={"va_k": "oil_k", "va_c": "oil_c"}).drop(columns="act")
    chk = p.groupby(["ent", "year"])[["va_k", "va_c"]].sum().reset_index().merge(bv, on=["ent", "year"]).merge(
        oil, on=["ent", "year"])
    chk["gap_k"] = (chk["va_k"] - (chk["gva_k"] - chk["oil_k"])) / chk["gva_k"]
    chk["gap_c"] = (chk["va_c"] - (chk["gva_c"] - chk["oil_c"])) / chk["gva_c"]
    return p, chk


def meitef():
    m = pd.read_csv(SRC / "meitef_annual.csv.gz")
    m = m[(m["variable"] == "gva") & (m["component"] == "informal_economy")
          & m["measure"].isin(["mxn_m_2018", "mxn_m_current"]) & m["activity"].isin(list(MEITEF))]
    codes = {gdp._norm(v): k for k, v in gdp.STATES.items()}
    m = m[m["state"].map(gdp._norm).isin(codes)].copy()
    m["ent"] = m["state"].map(gdp._norm).map(codes)
    m = m.pivot_table(index=["ent", "year", "activity"], columns="measure", values="value").reset_index()
    return m.rename(columns={"activity": "meitef_act", "mxn_m_2018": "iva_k", "mxn_m_current": "iva_c"})


def enoe_panel():
    files = sorted(TMP.glob("q_*.parquet"))
    rows, psu, mss = [], [], []
    for f in files:
        d = pd.read_parquet(f)
        d["act"] = fine_code(d["p4a"].values)
        d["seg"] = np.where(d["emp_ppal"] == 2, "f", "i")
        d["wh"] = d["w"] * d["hrsocup"].fillna(0)
        d["wy"] = d["w"] * d["ingocup"].where(d["ingocup"] > 0, 0).fillna(0)
        d["n"] = 1
        d["w_mss"] = d["w"] * (d["p4a"] // 10 == 213)
        mss.append(d.groupby(["year", "q", "ent", "seg"], as_index=False)["w_mss"].sum())
        g = d.groupby(["year", "q", "ent", "upm", "act", "seg"], as_index=False)[["w", "wh", "wy", "n"]].sum()
        psu.append(g)
        rows.append(g.groupby(["year", "q", "ent", "act", "seg"], as_index=False)[["w", "wh", "wy", "n"]].sum())
        print(f.name, flush=True)
    pd.concat(psu, ignore_index=True).to_parquet(TMP / "psu_cells.parquet", index=False)
    pd.concat(mss, ignore_index=True).to_parquet(TMP / "mining_services.parquet", index=False)
    q = pd.concat(rows, ignore_index=True)
    nq = q.groupby("year")["q"].nunique()
    a = q.groupby(["year", "ent", "act", "seg"], as_index=False)[["w", "wh", "wy", "n"]].sum()
    for c in ("w", "wh", "wy"):
        a[c] /= a["year"].map(nq)
    lost = a[a["act"] != "OIL"].groupby("year")["w"].sum()
    a = distribute(a, ["year", "ent", "seg"], ["w", "wh", "wy", "n"])
    lost = 1 - a.groupby("year")["w"].sum() / lost
    a = a.pivot_table(index=["ent", "year", "act"], columns="seg", values=["w", "wh", "wy", "n"], fill_value=0)
    a.columns = [{"w": "emp", "wh": "hrs", "wy": "inc", "n": "n"}[v] + "_" + s for v, s in a.columns]
    return a.reset_index(), lost


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p, chk = pibe_panel()
    e, lost = enoe_panel()
    panel = p.merge(e, on=["ent", "year", "act"], how="left")
    panel = panel[panel["year"].isin(e["year"].unique())]
    cols = ["emp_f", "emp_i", "hrs_f", "hrs_i", "inc_f", "inc_i", "n_f", "n_i"]
    panel[cols] = panel[cols].fillna(0)
    panel = panel.sort_values(["ent", "year", "act"])
    panel.to_csv(OUT / "panel_fine.csv", index=False, float_format="%.4f")
    m = meitef()
    m.sort_values(["ent", "year", "meitef_act"]).to_csv(OUT / "meitef_informal.csv", index=False, float_format="%.4f")
    checks = pd.DataFrame({
        "check": ["PIBE: max |sum of FINE activities - (B.1bV - oil)| / B.1bV, constant prices",
                  "PIBE: same, current prices",
                  "ENOE: max share of non-oil employment lost when distributing unspecified codes (by year)",
                  "ENOE: employed persons 15+ (millions), 2019 annual average",
                  "Cells (state x FINE activity x year) with no ENOE observation"],
        "value": [chk["gap_k"].abs().max(), chk["gap_c"].abs().max(), lost.abs().max(),
                  panel.loc[panel["year"] == 2019, ["emp_f", "emp_i"]].sum().sum() / 1e6,
                  int(((panel["n_f"] + panel["n_i"]) == 0).sum())]})
    checks.to_csv(OUT / "panel_checks.csv", index=False)
    print(checks.to_string(index=False))


if __name__ == "__main__":
    main()
