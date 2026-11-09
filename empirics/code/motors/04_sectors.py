"""Question 4 of WP07 (pre-analysis plan B6): other candidate motors.

Each sector's value-added share at current prices replaces manufacturing in the S&V model
(no second share; RELUS, schooling, log population, openness, temperate dummy, period dummies).
A sector is a motor if its share predicts faster growth with the robustness required of
manufacturing (same verdict rule as the moderators: agreement across main and core samples
and across HT and FE).

Writes empirics/output/motors/sectors/:
    un_sectors.csv     UN AMA groups, 1970-2020, slopes by subperiod (1970-90, 1990-2005, 2005-20)
    un_verdicts.csv    verdict per sector and subperiod
    etd_sectors.csv    ETD 12 sectors, 51 countries, 1990-2020 (shares at 1990-2015), value-added
                       and employment shares, whole period
    caribbean_trh.csv  trade, restaurants & hotels (tourism proxy): Caribbean vs rest, all countries
"""
import numpy as np
import pandas as pd

from config import ETD, ETD_LABELS, ETD_SECTORS, OUTPUT, SECTOR_LABELS
from models import add_terms, fit, load_panel, sample, tidy

OUT = OUTPUT / "sectors"
EDU = "EDU_HC"
UN = ["MAN", "AGR", "MIU", "CON", "TRH", "TSC", "OTH", "SER"]
SUBS = {"1970–90": range(1970, 1990), "1990–2005": range(1990, 2005), "2005–20": range(2005, 2020)}


def run_share(d, share, est, groups=None):
    dd, terms = add_terms(d, share=share, edu=EDU, slope_groups=groups)
    return fit(dd, terms, est, edu=EDU, other_share=None)


def verdict(g):
    def one(x):
        s = np.sign(x["coef"])
        if (s > 0).all() and (x["p"] < 0.10).any():
            return 1
        if (s < 0).all() and (x["p"] < 0.10).any():
            return -1
        return 0
    a, b = one(g[g["sample"] == "main"]), one(g[g["sample"] == "core"])
    return {(1, 1): "motor", (1, 0): "motor in main sample only", (0, 1): "motor in core sample only",
            (-1, -1): "drag", (-1, 0): "drag in main sample only", (0, -1): "drag in core sample only",
            (0, 0): "no effect"}.get((a, b), "conflicting across samples")


def un_sectors(p):
    rows = []
    for sname in ["main", "core"]:
        d = sample(p, sname, start=1970, end=2015, edu=EDU)
        groups = {lab: d["period"].isin(list(r)) for lab, r in SUBS.items()}
        for share in UN:
            dd = d.dropna(subset=[share])
            for est in ["HT", "FE"]:
                r = run_share(dd, share, est, groups)
                t = tidy(r, "(1) by subperiod", {"sample": sname, "sector": share})
                t = t[t["term"].str.startswith(f"{share}[")]
                t["subperiod"] = t["term"].str.extract(r"\[(.*)\]")[0]
                rows.append(t)
                r = run_share(dd, share, est)
                t = tidy(r, "(1) whole period", {"sample": sname, "sector": share})
                rows.append(t[t["term"] == share].assign(subperiod="1970–2020"))
    t = pd.concat(rows, ignore_index=True)
    t["label"] = t["sector"].map(SECTOR_LABELS)
    t.to_csv(OUT / "un_sectors.csv", index=False)
    v = t.groupby(["sector", "subperiod"]).apply(verdict, include_groups=False).rename("verdict").reset_index()
    v["label"] = v["sector"].map(SECTOR_LABELS)
    v.to_csv(OUT / "un_verdicts.csv", index=False)
    return t, v


def etd_panel(p):
    e = pd.read_excel(ETD, sheet_name="Data")
    e = e.rename(columns={**ETD_SECTORS, "cnt": "iso3"})
    secs = list(ETD_SECTORS.values())
    out = []
    for var, suffix in [("VA", "_va"), ("EMP", "_emp")]:
        x = e[e["var"] == var].copy()
        tot = x[secs].sum(axis=1)
        sh = x[["iso3", "year"]].copy()
        for s in secs:
            sh[s + suffix] = 100 * x[s] / tot
        out.append(sh)
    sh = out[0].merge(out[1], on=["iso3", "year"])
    sh = sh.rename(columns={"year": "period"})
    q = p.merge(sh, on=["iso3", "period"], how="inner")
    return q, secs


def etd_sectors(p):
    q, secs = etd_panel(p)
    rows = []
    for sname in ["main", "core"]:
        d = sample(q, sname, start=1990, end=2015, edu=EDU)
        for s in secs:
            for kind in ["_va", "_emp"]:
                share = s + kind
                dd = d.dropna(subset=[share])
                for est in ["HT", "FE"]:
                    try:
                        r = run_share(dd, share, est)
                    except Exception:
                        continue
                    t = tidy(r, "(1) whole period", {"sample": sname, "sector": s, "measure": kind[1:]})
                    rows.append(t[t["term"] == share])
    t = pd.concat(rows, ignore_index=True)
    t["label"] = t["sector"].map(ETD_LABELS)
    v = t.groupby(["sector", "measure"]).apply(verdict, include_groups=False).rename("verdict").reset_index()
    t = t.merge(v, on=["sector", "measure"], how="left")
    t.to_csv(OUT / "etd_sectors.csv", index=False)
    return t


def caribbean_trh(p):
    """Tourism proxy: trade, restaurants & hotels share, with a separate slope for the Caribbean.
    Uses all countries (most Caribbean states have under 1 million people), 1970-2020."""
    rows = []
    d = sample(p, "all", start=1970, end=2015, edu=EDU)
    d = d[~d["iso3"].isin(__import__("config").FORMER_PLANNED)]
    groups = {"Caribbean": d["caribbean"].astype(bool), "Rest": ~d["caribbean"].astype(bool)}
    for est in ["HT", "FE"]:
        r = run_share(d.dropna(subset=["TRH"]), "TRH", est, groups)
        t = tidy(r, "(1) Caribbean slope", {"sample": "all, excl. former planned"})
        rows.append(t[t["term"].str.startswith("TRH[")])
    t = pd.concat(rows, ignore_index=True)
    t["n_caribbean_countries"] = d[d["caribbean"].astype(bool)].dropna(subset=["TRH", EDU])["iso3"].nunique()
    t.to_csv(OUT / "caribbean_trh.csv", index=False)
    return t


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p = load_panel()
    t, v = un_sectors(p)
    print(v.pivot(index="label", columns="subperiod", values="verdict").to_string())
    ht = t[(t["estimator"] == "HT")].pivot_table(index="label", columns=["sample", "subperiod"], values="coef").round(3)
    print(ht.to_string())
    e = etd_sectors(p)
    print(e[e["estimator"] == "HT"].pivot_table(index=["label", "measure"], columns="sample", values=["coef", "p"]).round(3).to_string())
    print(e.groupby(["label", "measure"]).verdict.first().to_string())
    print(caribbean_trh(p)[["estimator", "term", "coef", "p", "n_caribbean_countries"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
