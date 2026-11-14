"""Study 9.4, step 4: municipality values for the maps and the discontinuity plot (pre-analysis
plan §4). Descriptive: ENOE is not designed to be representative by municipality.

    python empirics/code/enoe/border_mw/04_maps.py

For each municipality of the six border states (main sample: sampling units observed in
2016-2018), outcome and period (before 2016Q1-2018Q4, during 2019Q1-Q4, after 2020Q1):
  level        the ratio estimate
  change_net   change from before, minus the population-weighted mean change in control municipalities
  change_eb    change_net shrunk towards its group mean (border zone or control) by empirical Bayes,
               with sampling variances from a bootstrap over primary sampling units within the municipality
  shown        at least MIN_N person records (aged 15+) in both periods
Outputs: map_values.csv and rd_bins.csv (binned means and side-specific linear fits by distance).
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
M_MONTH = 5302.0
BORDER_STATES = [2, 5, 8, 19, 26, 28]
PERIODS = {"before": range(0, 12), "during": range(12, 16), "after": range(16, 17)}
MIN_N = 300
B = 200
RD_BW = 200        # km on each side for the linear fits
RD_BIN = 50        # km


def ratio_parts(persons, pairs):
    """Numerator and denominator by (mid, period, upm) for each mapped outcome."""
    p = persons.copy()
    w = p["fac"].astype(float)
    we = (p["pos_ocu"] == 1) & p["eda"].between(16, 65) & (p["state"] != "N")
    rep = we & (p["ingocup"] > 0)
    hr = we & (p["ing_x_hrs"] > 0)
    parts = {
        "below_m": (w * (rep & (p["ingocup"] < M_MONTH)), w * rep),
        "lnw": (w * hr * np.log(p["ing_x_hrs"].where(hr, 1.0)), w * hr),
        "formal_share": (w * (p["state"] == "F"), w * p["state"].isin(["F", "I"])),
    }
    frames = []
    for k, (num, den) in parts.items():
        frames.append(pd.DataFrame({"mid": p["mid"], "period": p["period"], "upm": p["upm"], "outcome": k,
                                    "num": num.astype(float), "den": den.astype(float)}))
    q = pairs
    wq = q["fac"].astype(float)
    frames.append(pd.DataFrame({"mid": q["mid"], "period": q["period"], "upm": q["upm"], "outcome": "i_to_f",
                                "num": wq * ((q["s0"] == "I") & (q["s1"] == "F")), "den": wq * (q["s0"] == "I")}))
    f = pd.concat(frames, ignore_index=True)
    return f.groupby(["outcome", "mid", "period", "upm"], as_index=False)[["num", "den"]].sum()


def boot(g, rng):
    num, den = g["num"].to_numpy(), g["den"].to_numpy()
    if den.sum() == 0:
        return np.nan, np.nan
    est = num.sum() / den.sum()
    n = len(num)
    idx = rng.integers(0, n, size=(B, n))
    bs = num[idx].sum(1) / np.where(den[idx].sum(1) > 0, den[idx].sum(1), np.nan)
    return est, np.nanvar(bs, ddof=1)


def eb(x, v):
    """Shrink x (with sampling variances v) towards their mean; method of moments for tau^2."""
    ok = np.isfinite(x) & np.isfinite(v)
    if ok.sum() < 3:
        return x
    mu = x[ok].mean()
    tau2 = max(0.0, x[ok].var(ddof=1) - v[ok].mean())
    lam = tau2 / (tau2 + v)
    return mu + lam * (x - mu)


def main():
    persons = pd.read_parquet(TMP / "persons.parquet")
    pairs = pd.read_parquet(TMP / "pairs.parquet")
    geo = pd.read_csv(OUT / "municipalities.csv")
    geo["mid"] = geo["ent"] * 1000 + geo["mun"]
    pre_upm = set(map(tuple, persons.loc[persons["t"] <= 11, ["ent_i", "upm"]].drop_duplicates().to_numpy()))
    per = {t: k for k, r in PERIODS.items() for t in r}
    out = []
    for name, d in [("persons", persons), ("pairs", pairs)]:
        d = d[d["mun"].notna() & d["ent_i"].isin(BORDER_STATES)]
        d = d[pd.Series(list(zip(d["ent_i"], d["upm"])), index=d.index).isin(pre_upm)].copy()
        d["mid"] = d["ent_i"] * 1000 + d["mun"].astype(int)
        d["period"] = d["t"].map(per)
        out.append(d)
    persons, pairs = out
    counts = persons.groupby(["mid", "period"]).size().rename("n").reset_index()
    parts = ratio_parts(persons, pairs)
    rng = np.random.default_rng(94)
    rows = []
    for (o, mid, period), g in parts.groupby(["outcome", "mid", "period"]):
        est, var = boot(g, rng)
        rows.append({"outcome": o, "mid": mid, "period": period, "level": est, "var": var})
    v = pd.DataFrame(rows).merge(counts, on=["mid", "period"], how="left")
    v = v.merge(geo[["mid", "ent", "mun", "name", "zlfn", "dist_km"]], on="mid", how="left")
    w0 = persons[persons["period"] == "before"].groupby("mid")["fac"].sum() / 12
    v["pop15"] = v["mid"].map(w0)
    before = v[v["period"] == "before"].set_index(["outcome", "mid"])
    res = []
    for period in ["before", "during", "after"]:
        x = v[v["period"] == period].copy()
        b = before.reindex(pd.MultiIndex.from_frame(x[["outcome", "mid"]]))
        x["n_before"] = b["n"].to_numpy()
        x["change"] = x["level"].to_numpy() - b["level"].to_numpy() if period != "before" else 0.0
        x["change_var"] = x["var"].to_numpy() + b["var"].to_numpy() if period != "before" else x["var"]
        x["shown"] = (x["n"] >= MIN_N) & (x["n_before"] >= MIN_N)
        for o, g in x.groupby("outcome"):
            ctrl = g[~g["zlfn"] & g["shown"]]
            cm = np.average(ctrl["change"], weights=ctrl["pop15"]) if len(ctrl) and period != "before" else 0.0
            x.loc[g.index, "change_net"] = g["change"] - cm
            for z in [True, False]:
                gi = g[(g["zlfn"] == z) & g["shown"]].index
                x.loc[gi, "change_eb"] = eb(x.loc[gi, "change_net"].to_numpy(float),
                                            x.loc[gi, "change_var"].to_numpy(float))
        res.append(x)
    r = pd.concat(res, ignore_index=True)
    r["se"] = np.sqrt(r["var"])
    r["change_se"] = np.sqrt(r["change_var"])
    cols = ["outcome", "period", "mid", "ent", "mun", "name", "zlfn", "dist_km", "pop15", "n", "n_before", "shown",
            "level", "se", "change_net", "change_se", "change_eb"]
    r[cols].sort_values(["outcome", "period", "mid"]).to_csv(OUT / "map_values.csv", index=False, float_format="%.6g")

    # discontinuity plot: binned means and weighted linear fits on each side, period 'during'
    rd = []
    s = r[(r["period"] == "during") & r["shown"]]
    for o, g in s.groupby("outcome"):
        g = g.assign(bin=(np.floor(g["dist_km"] / RD_BIN) * RD_BIN + RD_BIN / 2))
        for bnum, h in g.groupby("bin"):
            rd.append({"outcome": o, "kind": "bin", "dist_km": bnum, "value": np.average(h["change_net"], weights=h["pop15"]),
                       "municipalities": len(h)})
        for side, h in [("inside", g[g["dist_km"] < 0]), ("outside", g[g["dist_km"] >= 0])]:
            h = h[h["dist_km"].abs() <= RD_BW]
            if len(h) >= 3:
                b1, b0 = np.polyfit(h["dist_km"], h["change_net"], 1, w=np.sqrt(h["pop15"]))
                ends = [h["dist_km"].min(), 0] if side == "inside" else [0, h["dist_km"].max()]   # observed range only
                for e in ends:
                    rd.append({"outcome": o, "kind": f"fit_{side}", "dist_km": e, "value": b0 + b1 * e,
                               "municipalities": len(h)})
    pd.DataFrame(rd).to_csv(OUT / "rd_bins.csv", index=False, float_format="%.6g")
    print(r[r["shown"]].groupby(["outcome", "period", "zlfn"])["change_net"].agg(["count", "mean"]).round(4).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
