"""Study 9.4, step 2: municipality x quarter cells (pre-analysis plan §§2-3).

    python empirics/code/enoe/border_mw/02_cells.py

Inputs: persons.parquet and pairs.parquet (step 1), municipalities.csv (step 0). For each sample
(old sampling units only, the main specification; full sample) and group (all; women; men;
schooling below or at least 12 years), cells hold weighted rates and means for the population
aged 15+, wage employees aged 16-65 and quarterly transitions. All cells go to the uncommitted
interim folder; the cells of the six border states for all persons are also written to
empirics/output/enoe/border_mw/cells.csv.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from enoe_config import INTERIM, OUTPUT_ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "border_mw"
TMP = INTERIM / "border_mw"
M_MONTH = 5302.0                 # 2019 border minimum: 176.72 pesos a day x 30
M_HOUR = 176.72 / 8              # per hour of an 8-hour day
EDGES = [0, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, np.inf]
BINS = ["b00_06", "b06_08", "b08_10", "b10_12", "b12_15", "b15_20", "b20_30", "b30_up"]
BORDER_STATES = [2, 5, 8, 19, 26, 28]
LAST_PRE = 11                    # 2018Q4; t = 0 is 2016Q1
GROUPS = {"all": lambda d: d.index == d.index,
          "women": lambda d: d["sex"] == 2, "men": lambda d: d["sex"] == 1,
          "school_lt12": lambda d: d["anios_esc"] < 12, "school_ge12": lambda d: d["anios_esc"].between(12, 30)}


def wmean(x, w):
    w = np.where(np.isnan(x), 0.0, w)
    s = w.sum()
    return np.nan if s == 0 else float(np.nansum(x * w) / s)


def person_cells(p):
    """Rates and means for one municipality x quarter."""
    w = p["fac"].to_numpy(float)
    W = w.sum()
    s = p["state"].to_numpy()
    r = {"n": len(p), "W": W,
         "emp_rate": w[s != "N"].sum() / W, "formal_rate": w[s == "F"].sum() / W,
         "informal_rate": w[s == "I"].sum() / W}
    fi = w[s == "F"].sum() + w[s == "I"].sum()
    r["formal_share"] = w[s == "F"].sum() / fi if fi > 0 else np.nan
    we = p[(p["pos_ocu"] == 1) & p["eda"].between(16, 65) & (p["state"] != "N")]
    ww = we["fac"].to_numpy(float)
    inc = we["ingocup"].to_numpy(float)
    hr = we["ing_x_hrs"].to_numpy(float)
    rep = inc > 0
    r["n_we"] = len(we)
    r["we_rate"] = ww.sum() / W
    r["report"] = ww[rep].sum() / ww.sum() if ww.sum() > 0 else np.nan
    r["lnw"] = wmean(np.where(hr > 0, np.log(np.where(hr > 0, hr, 1)), np.nan), ww)
    r["below_m"] = ww[rep & (inc < M_MONTH)].sum() / ww[rep].sum() if ww[rep].sum() > 0 else np.nan
    r["hours"] = wmean(we["hrsocup"].to_numpy(float), ww)
    for f, lab in [("F", "f"), ("I", "i")]:
        sel = (we["state"] == f).to_numpy()
        rel = inc / M_MONTH
        idx = np.digitize(rel, EDGES[1:-1])
        for k, b in enumerate(BINS):
            r[f"{lab}_{b}"] = ww[sel & rep & (idx == k)].sum() / W
        r[f"{lab}_norep"] = ww[sel & ~rep].sum() / W
        relh = hr / M_HOUR
        idxh = np.digitize(relh, EDGES[1:-1])
        for k, b in enumerate(BINS):
            r[f"{lab}h_{b}"] = ww[sel & (hr > 0) & (idxh == k)].sum() / W
    own = p[(p["pos_ocu"] == 3) & p["eda"].between(16, 65)]
    oh = own["ing_x_hrs"].to_numpy(float)
    r["lnw_own"] = wmean(np.where(oh > 0, np.log(np.where(oh > 0, oh, 1)), np.nan), own["fac"].to_numpy(float))
    return r


def flow_cells(p):
    w, s0, s1 = p["fac"].to_numpy(float), p["s0"].to_numpy(), p["s1"].to_numpy()
    r = {"n_pairs": len(p)}
    for o, d, name in [("I", "F", "i_to_f"), ("N", "F", "n_to_f"), ("F", "I", "f_to_i"), ("F", "N", "f_to_n"),
                       ("I", "N", "i_to_n")]:
        den = w[s0 == o].sum()
        r[name] = w[(s0 == o) & (s1 == d)].sum() / den if den > 0 else np.nan
        r[f"n_{o}"] = int((s0 == o).sum())
    return r


def build(persons, pairs, geo):
    pre_upm = set(map(tuple, persons.loc[persons["t"] <= LAST_PRE, ["ent_i", "upm"]].drop_duplicates().to_numpy()))
    out = []
    for sample in ["old", "full"]:
        P, Q = persons, pairs
        if sample == "old":
            P = P[pd.Series(list(zip(P["ent_i"], P["upm"])), index=P.index).isin(pre_upm)]
            Q = Q[pd.Series(list(zip(Q["ent_i"], Q["upm"])), index=Q.index).isin(pre_upm)]
        for g, sel in GROUPS.items():
            a = P[sel(P)].groupby(["ent_i", "mun", "t"]).apply(lambda x: pd.Series(person_cells(x)), include_groups=False)
            b = Q[sel(Q)].groupby(["ent_i", "mun", "t"]).apply(lambda x: pd.Series(flow_cells(x)), include_groups=False)
            c = a.join(b, how="outer").reset_index()
            c["sample"], c["group"] = sample, g
            out.append(c)
            print(sample, g, len(c))
    c = pd.concat(out, ignore_index=True)
    c["mid"] = c["ent_i"] * 1000 + c["mun"].astype(int)
    z = set((geo.loc[geo["zlfn"], "ent"] * 1000 + geo.loc[geo["zlfn"], "mun"]).tolist())
    c["zlfn"] = c["mid"].isin(z)
    c["border_state"] = c["ent_i"].isin(BORDER_STATES)
    # fixed weights: mean weighted population 15+ over 2016-2018 in the full sample, all persons
    base = c[(c["sample"] == "full") & (c["group"] == "all") & (c["t"] <= LAST_PRE)].groupby("mid")["W"].mean()
    c["w"] = c["mid"].map(base)
    c["post"] = c["t"].between(LAST_PRE + 1, LAST_PRE + 4)
    c = c.merge(geo[["ent", "mun", "dist_km"]].assign(mid=lambda g: g["ent"] * 1000 + g["mun"])[["mid", "dist_km"]],
                on="mid", how="left")
    return c


def main():
    persons = pd.read_parquet(TMP / "persons.parquet")
    pairs = pd.read_parquet(TMP / "pairs.parquet")
    persons = persons[persons["mun"].notna()]
    pairs = pairs[pairs["mun"].notna()]
    geo = pd.read_csv(OUT / "municipalities.csv")
    c = build(persons, pairs, geo)
    c.to_parquet(TMP / "cells.parquet", index=False)
    six = c[c["border_state"] & (c["group"] == "all")].sort_values(["sample", "mid", "t"])
    six.to_csv(OUT / "cells.csv", index=False, float_format="%.6g")
    zcheck = c[(c["group"] == "all") & (c["sample"] == "full") & c["zlfn"]]
    print("treated municipalities:", zcheck["mid"].nunique(), "control (six states):",
          c[(c["group"] == "all") & c["border_state"] & ~c["zlfn"]]["mid"].nunique(),
          "all municipalities:", c["mid"].nunique())
    return 0


if __name__ == "__main__":
    sys.exit(main())
