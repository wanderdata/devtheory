"""Study 9.4, step 6: range answers to the follow-up income question and corrected earnings bins
(pre-analysis plan, addendum A1; OQ-70, D-056).

    python empirics/code/enoe/border_mw/06_ranges.py

For wage employees aged 16-65, the answer to the income questions is classified as an amount
(`ingocup` > 0), a range (P6C codes 1-7, relative to the minimum wage read out by the interviewer,
`salario`) or no answer (P6C 8-9 or missing). Range answers are converted to intervals of monthly
income relative to M = 5,302 and spread uniformly over them (a point for code 2). Outputs in
empirics/output/enoe/border_mw/:
  ranges_did.csv    DiD (main specification) for answer shares and corrected bins
  ranges_event.csv  event studies for the answer shares
  ranges_bins.csv   corrected bins by formality
"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parent))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import border_lib as bl  # noqa: E402
import enoe_io  # noqa: E402
from enoe_config import BORDER_QUARTERS, INTERIM, KEY, OUTPUT_ROOT  # noqa: E402

did_step = importlib.import_module("03_did")
OUT = OUTPUT_ROOT / "border_mw"
TMP = INTERIM / "border_mw"
M = 5302.0
EDGES = np.array([0, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, np.inf])
BINS = ["b00_06", "b06_08", "b08_10", "b10_12", "b12_15", "b15_20", "b20_30", "b30_up"]
RANGE = {1: (0.0, 1.0), 3: (1.0, 2.0), 4: (2.0, 3.0), 5: (3.0, 5.0), 6: (5.0, 10.0), 7: (10.0, np.inf)}
SDEM = KEY + ["n_ent", "r_def", "c_res", "eda", "clase2", "pos_ocu", "emp_ppal", "ingocup", "salario", "fac", "upm",
              "mun"]


def shares_of_interval(lo, hi):
    """Fraction of a uniform interval [lo, hi) (relative to M) falling in each bin; a point if lo == hi."""
    if lo == hi:
        k = np.searchsorted(EDGES, lo, side="right") - 1
        out = np.zeros(len(BINS))
        out[min(k, len(BINS) - 1)] = 1.0
        return out
    if not np.isfinite(hi):
        out = np.zeros(len(BINS))
        k = np.searchsorted(EDGES, lo, side="right") - 1
        out[min(k, len(BINS) - 1)] = 1.0       # open top range: only reached for code 7, always >= 3 M
        return out
    a = np.clip(EDGES[:-1], lo, hi)
    b = np.clip(EDGES[1:], lo, hi)
    return (b - a) / (hi - lo)


def quarter(y, q, pre_upm):
    s = enoe_io.read("sdem", y, q, SDEM)
    c = enoe_io.read("coe2", y, q, KEY + ["n_ent", "p6b1", "p6c"])
    for k in KEY:
        s[k], c[k] = s[k].astype(str).str.strip(), c[k].astype(str).str.strip()
    for x in ["n_ent", "r_def", "c_res", "eda", "clase2", "pos_ocu", "emp_ppal", "ingocup", "salario", "fac"]:
        s[x] = pd.to_numeric(s[x], errors="coerce")
    c["n_ent"] = pd.to_numeric(c["n_ent"], errors="coerce")
    c["p6c"] = pd.to_numeric(c["p6c"].astype(str).str.strip(), errors="coerce")
    c = c.drop_duplicates(KEY + ["n_ent"], keep=False)
    s = s[(s["r_def"] == 0) & s["c_res"].isin([1, 3]) & s["eda"].between(16, 65) & (s["clase2"] == 1)
          & (s["pos_ocu"] == 1)]
    s = s.merge(c[KEY + ["n_ent", "p6c"]], on=KEY + ["n_ent"], how="left")
    s["ent_i"] = pd.to_numeric(s["ent"], errors="coerce").astype(int)
    s["mun"] = pd.to_numeric(s["mun"].astype(str).str.strip(), errors="coerce")
    s["upm"] = s["upm"].astype(str).str.strip()
    s = s[s["mun"].notna()]
    s = s[pd.Series(list(zip(s["ent_i"], s["upm"])), index=s.index).isin(pre_upm)]
    s["t"] = (y - 2016) * 4 + (q - 1)
    amount = s["ingocup"] > 0
    rng = ~amount & s["p6c"].between(1, 7)
    s["kind"] = np.where(amount, "amount", np.where(rng, "range", "none"))
    s["lab"] = np.where(s["emp_ppal"] == 2, "f", np.where(s["emp_ppal"] == 1, "i", "u"))
    # allocation to bins
    alloc = np.zeros((len(s), len(BINS)))
    inc = s["ingocup"].to_numpy(float) / M
    k = np.digitize(inc, EDGES[1:-1])
    am = amount.to_numpy()
    alloc[np.where(am)[0], k[am]] = 1.0
    sal = s["salario"].to_numpy(float) / M
    for i in np.where(rng.to_numpy())[0]:
        code = int(s["p6c"].iat[i])
        if code == 2:
            alloc[i] = shares_of_interval(sal[i], sal[i])
        else:
            lo, hi = RANGE[code]
            alloc[i] = shares_of_interval(lo * sal[i], hi * sal[i])
    for j, b in enumerate(BINS):
        s[b] = alloc[:, j]
    return s


def cells(s, W):
    w = s["fac"].to_numpy(float)
    g = s.assign(w=w)
    rows = []
    for (e, mun, t), h in g.groupby(["ent_i", "mun", "t"]):
        ww = h["w"].to_numpy()
        tot = ww.sum()
        r = {"ent_i": e, "mun": mun, "t": t}
        for kind in ["amount", "range", "none"]:
            r[f"sh_{kind}"] = ww[h["kind"] == kind].sum() / tot
        for code in range(1, 8):
            r[f"sh_p6c{code}"] = ww[(h["kind"] == "range") & (h["p6c"] == code)].sum() / tot
        known = (h["kind"] != "none").to_numpy()
        below = h[BINS[:3]].sum(1).to_numpy()
        r["below_m_corr"] = (ww * below)[known].sum() / ww[known].sum() if ww[known].sum() > 0 else np.nan
        for lab in ["f", "i"]:
            sel = (h["lab"] == lab).to_numpy()
            for b in BINS:
                r[f"{lab}c_{b}"] = (ww * h[b].to_numpy())[sel].sum()
            r[f"{lab}c_none"] = ww[sel & ~known].sum()
        rows.append(r)
    c = pd.DataFrame(rows)
    c["mid"] = c["ent_i"] * 1000 + c["mun"].astype(int)
    c = c.merge(W, on=["mid", "t"], how="left")
    for col in [x for x in c.columns if x.startswith(("fc_", "ic_"))]:
        c[col] = c[col] / c["W"]
    for lab in ["f", "i"]:
        c[f"{lab}c_missing"] = c[[f"{lab}c_{b}" for b in BINS[:3]]].sum(1)
        c[f"{lab}c_excess"] = c[[f"{lab}c_{b}" for b in BINS[3:5]]].sum(1)
    c["c_missing"] = c["fc_missing"] + c["ic_missing"]
    c["c_excess"] = c["fc_excess"] + c["ic_excess"]
    return c


def main():
    persons = pd.read_parquet(TMP / "persons.parquet", columns=["ent_i", "upm", "t"])
    pre_upm = set(map(tuple, persons.loc[persons["t"] <= 11, ["ent_i", "upm"]].drop_duplicates().to_numpy()))
    base = pd.read_parquet(TMP / "cells.parquet")
    base = base[(base["sample"] == "old") & (base["group"] == "all")]
    W = base[["mid", "t", "W"]]
    parts = []
    for y, q in BORDER_QUARTERS:
        parts.append(quarter(y, q, pre_upm))
        print(y, q, len(parts[-1]))
    s = pd.concat(parts, ignore_index=True)
    c = cells(s, W)
    keep = ["mid", "t", "zlfn", "border_state", "post", "w", "ent_i", "dist_km", "sample", "group"]
    c = c.drop(columns=["ent_i", "W"]).merge(base[keep], on=["mid", "t"], how="inner")
    c.to_parquet(TMP / "ranges_cells.parquet", index=False)

    m = did_step.sample(c, {})
    pre = m[m["zlfn"] & (m["t"] <= 11)]
    outs = ["sh_amount", "sh_range", "sh_none"] + [f"sh_p6c{k}" for k in range(1, 8)] + \
           ["below_m_corr", "c_missing", "c_excess", "fc_missing", "fc_excess", "ic_missing", "ic_excess",
            "fc_none", "ic_none"]
    rows = []
    for y in outs:
        r = bl.did(m, y, B=1999, ci=True)
        r["pre_mean_zone"] = np.average(pre[y].dropna(), weights=pre.loc[pre[y].notna(), "w"])
        rows.append(r)
    d = pd.DataFrame(rows)
    d.to_csv(OUT / "ranges_did.csv", index=False)
    ev, pt = [], []
    es = did_step.sample(c, {"last": 16})
    for y in ["sh_amount", "sh_range", "sh_p6c2", "sh_none", "below_m_corr", "c_missing", "c_excess"]:
        e, p = bl.event_study(es, y, ref=11, B=999, pre=list(range(11)))
        e["p_pretrend_wild"] = p
        ev.append(e)
    pd.concat(ev).to_csv(OUT / "ranges_event.csv", index=False)
    brows = []
    for lab, f in [("fc", "formal"), ("ic", "informal")]:
        for b in BINS + ["none"]:
            y = f"{lab}_{b}"
            r = bl.did(m, y, B=999, ci=False)
            r.update({"formality": f, "bin": b,
                      "pre_mean_zone": np.average(pre[y].dropna(), weights=pre.loc[pre[y].notna(), "w"])})
            brows.append(r)
    pd.DataFrame(brows).to_csv(OUT / "ranges_bins.csv", index=False)
    print(d[["outcome", "beta", "lo90", "hi90", "p_wild", "pre_mean_zone"]].round(4).to_string(index=False))
    print(pd.DataFrame([{"outcome": e["outcome"].iat[0], "p": e["p_pretrend_wild"].iat[0]} for e in ev]).round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
