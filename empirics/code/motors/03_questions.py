"""Questions 1-3 of WP07 (pre-analysis plan B3-B5), on manufacturing.

Extension sample: five-year periods starting 1950-2015 (growth to 2020), education from PWT's
human-capital index (EDU_HC, consistent over the whole span). Samples: main and core (D-039);
estimators: Hausman-Taylor (main) and fixed effects (check).

Writes empirics/output/motors/questions/:
    q1_subperiods.csv     MAN slope by subperiod (1950-70, 1970-90, 1990-2005, 2005-20), models 1 and 3
    q1_me_reference.csv   marginal effect of MAN by subperiod at the median developing country
    q1_me_surface.csv     marginal effect over a grid of RELUS x schooling, by subperiod (HT, model 3)
    q1_rolling.csv        20-year rolling windows: MAN coefficient (model 1) and reference marginal effect
    q2_lac.csv            MAN slope for LAC and for the rest of the sample, by subperiod
    q2_kaldor.csv         Kaldor's first law by era: GDP growth on manufacturing growth, LAC vs rest
    q3_moderators.csv     MAN x moderator, one at a time and jointly, with predicted signs and verdicts
"""
import numpy as np
import pandas as pd

from config import GGDC10, OUTPUT, PROCESSED, SUBPERIODS_EXT, UN_K
from models import add_terms, fit, load_panel, marginal_effect, me_grid, sample, tidy

OUT = OUTPUT / "questions"
EDU = "EDU_HC"
SAMPLES = ["main", "core"]
ESTS = ["HT", "FE"]


def masks(d, groups):
    return {lab: d["period"].isin(list(r)) for lab, r in groups.items()}


def reference_points(d):
    """Median RELUS and schooling of developing countries (not in the 21 advanced) by subperiod."""
    dev = d[~d["advanced"].astype(bool)]
    out = {}
    for lab, r in SUBPERIODS_EXT.items():
        x = dev[dev["period"].isin(list(r))]
        out[lab] = (float(x["RELUS"].median()), float(x[EDU].median()))
    return out


def q1(p):
    sub_rows, me_rows, surf, roll = [], [], [], []
    for sname in SAMPLES:
        d = sample(p, sname, start=1950, end=2015, edu=EDU)
        ref = reference_points(d)
        for est in ESTS:
            for lab, inter in [("(1) no interactions", ()), ("(3) interactions", ("REL", "EDU"))]:
                dd, terms = add_terms(d, edu=EDU, interactions=inter, slope_groups=masks(d, SUBPERIODS_EXT))
                r = fit(dd, terms, est, edu=EDU)
                sub_rows.append(tidy(r, lab, {"sample": sname}))
                for g, (rel, edu) in ref.items():
                    m, se = marginal_effect(r, "MAN", rel, edu, group=g)
                    me_rows.append({"sample": sname, "estimator": est, "model": lab, "subperiod": g,
                                    "RELUS_ref": rel, "EDU_ref": edu, "me": m, "se": se,
                                    "p": float(2 * (1 - __import__("scipy").stats.norm.cdf(abs(m / se))))})
                if est == "HT" and lab.startswith("(3)"):
                    for g in SUBPERIODS_EXT:
                        surf.append(me_grid(r, "MAN", np.round(np.linspace(0.05, 0.85, 17), 2),
                                            np.arange(1, 13, 0.5), group=g).assign(sample=sname))
        # rolling 20-year windows (four five-year periods), HT, models 1 and 3
        for s0 in range(1950, 2005, 5):
            w = d[(d["period"] >= s0) & (d["period"] <= s0 + 15)]
            if w["period"].nunique() < 4:
                continue
            for lab, inter in [("(1) no interactions", ()), ("(3) interactions", ("REL", "EDU"))]:
                dd, terms = add_terms(w, edu=EDU, interactions=inter)
                try:
                    r = fit(dd, terms, "HT", edu=EDU)
                except Exception:
                    continue
                dev = w[~w["advanced"].astype(bool)]
                m, se = marginal_effect(r, "MAN", float(dev["RELUS"].median()), float(dev[EDU].median()))
                roll.append({"sample": sname, "model": lab, "window": f"{s0}–{s0 + 20}", "start": s0,
                             "coef_MAN": r.params["MAN"], "se_MAN": r.se["MAN"], "me_ref": m, "se_me": se,
                             "nobs": r.nobs, "ncountries": r.ngroups})
    pd.concat(sub_rows).to_csv(OUT / "q1_subperiods.csv", index=False)
    pd.DataFrame(me_rows).to_csv(OUT / "q1_me_reference.csv", index=False)
    pd.concat(surf).to_csv(OUT / "q1_me_surface.csv", index=False)
    pd.DataFrame(roll).to_csv(OUT / "q1_rolling.csv", index=False)


def q2(p):
    rows = []
    for sname in SAMPLES:
        d = sample(p, sname, start=1950, end=2015, edu=EDU)
        lac = d["lac"].astype(bool)
        groups = {}
        for lab, r in SUBPERIODS_EXT.items():
            inp = d["period"].isin(list(r))
            groups[f"LAC {lab}"] = inp & lac
            groups[f"Rest {lab}"] = inp & ~lac
        for est in ESTS:
            dd, terms = add_terms(d, edu=EDU, slope_groups=groups)
            r = fit(dd, terms, est, edu=EDU)
            t = tidy(r, "(1) LAC x subperiod", {"sample": sname})
            t = t[t["term"].str.startswith("MAN[")]
            t["group"] = t["term"].str.extract(r"MAN\[(LAC|Rest) ")[0]
            t["subperiod"] = t["term"].str.extract(r"MAN\[(?:LAC|Rest) (.*)\]")[0]
            n_lac = d[lac].groupby(d["period"].map(lambda x: next((k for k, v in SUBPERIODS_EXT.items() if x in v), None))
                                   )["iso3"].nunique()
            t["n_lac_countries"] = t["subperiod"].map(n_lac)
            rows.append(t)
            # difference LAC - rest by subperiod, with its standard error
            for lab in SUBPERIODS_EXT:
                a, b = f"MAN[LAC {lab}]", f"MAN[Rest {lab}]"
                if a in r.params and b in r.params:
                    diff = r.params[a] - r.params[b]
                    se = float(np.sqrt(r.cov.loc[a, a] + r.cov.loc[b, b] - 2 * r.cov.loc[a, b]))
                    rows.append(pd.DataFrame([{"term": f"LAC minus rest [{lab}]", "coef": diff, "se": se,
                                               "p": float(2 * (1 - __import__("scipy").stats.norm.cdf(abs(diff / se)))),
                                               "model": "(1) LAC x subperiod", "estimator": est, "sample": sname,
                                               "group": "LAC minus rest", "subperiod": lab, "nobs": r.nobs,
                                               "ncountries": r.ngroups}]))
    pd.concat(rows, ignore_index=True).to_csv(OUT / "q2_lac.csv", index=False)
    kaldor()


def kaldor():
    """Kaldor's first law by era: country growth of real GDP (PWT rgdpna) on growth of real
    manufacturing value added, decade averages, LAC vs rest. Manufacturing volumes: UN AMA
    (constant 2020 US$) from 1970; GGDC 10-Sector constant prices before 1970."""
    a = pd.read_csv(PROCESSED / "annual.csv", low_memory=False)
    k = pd.read_excel(UN_K, header=2)
    yrs = [c for c in k.columns if str(c)[:2] in ("19", "20")]
    k = k[k["IndicatorName"] == "Manufacturing (ISIC D)"].melt(id_vars=["CountryID"], value_vars=yrs,
                                                                 var_name="year", value_name="man_k")
    iso = pd.read_csv(PROCESSED.parents[1] / "source" / "reference" / "iso3166_lukes_all.csv", keep_default_na=False)
    k["iso3"] = k["CountryID"].map(iso.assign(m=iso["country-code"].astype(int)).set_index("m")["alpha-3"])
    k["year"] = k["year"].astype(float).astype(int)
    t = pd.read_excel(GGDC10, sheet_name="dataset")
    t.columns = [c.strip() for c in t.columns]
    g = t[t["Variable"].isin(["VA_Q05", "VA_Q10", "VA_Q91"]) & ~t["Country"].str.contains("alt")]
    g = g.sort_values("Variable").drop_duplicates(["Country", "Year"])
    g = g.rename(columns={"Country": "iso3", "Year": "year", "Manufacturing": "man_g"})[["iso3", "year", "man_g"]]
    g["iso3"] = g["iso3"].replace({"DEW": "DEU", "MOR": "MAR"})
    m = a[["iso3", "year", "rgdpna", "lac"]] if "lac" in a else a[["iso3", "year", "rgdpna"]]
    m = m.merge(k[["iso3", "year", "man_k"]], on=["iso3", "year"], how="left").merge(g, on=["iso3", "year"], how="left")
    c = pd.read_csv(PROCESSED / "countries.csv")
    m = m.merge(c[["iso3", "lac", "small", "commodity"]], on="iso3", how="left", suffixes=("", "_c"))
    rows = []
    for d0 in range(1950, 2020, 10):
        d1 = d0 + 10 if d0 < 2010 else 2020
        src = "man_g" if d0 < 1970 else "man_k"
        x = m[m["year"].isin([d0, d1])].pivot_table(index="iso3", columns="year", values=["rgdpna", src])
        try:
            gy = 100 * ((x[("rgdpna", d1)] / x[("rgdpna", d0)]) ** (1 / (d1 - d0)) - 1)
            gm = 100 * ((x[(src, d1)] / x[(src, d0)]) ** (1 / (d1 - d0)) - 1)
        except KeyError:
            continue
        z = pd.DataFrame({"gy": gy, "gm": gm}).dropna()
        z = z.join(c.set_index("iso3")[["lac", "small", "commodity"]])
        z = z[~z["small"].fillna(True).astype(bool)]
        for grp, zz in [("LAC", z[z["lac"].astype(bool)]), ("Rest", z[~z["lac"].astype(bool)])]:
            zz = zz[(zz["gm"].abs() < 30)]
            if len(zz) < 5:
                continue
            X = np.column_stack([np.ones(len(zz)), zz["gm"]])
            b, res, *_ = np.linalg.lstsq(X, zz["gy"], rcond=None)
            e = zz["gy"] - X @ b
            V = np.linalg.inv(X.T @ X) * (e @ e) / (len(zz) - 2)
            rows.append({"decade": f"{d0}s", "start": d0, "group": grp, "n": len(zz), "slope": b[1],
                         "se": float(np.sqrt(V[1, 1])), "intercept": b[0], "corr": zz["gy"].corr(zz["gm"]),
                         "mean_gy": zz["gy"].mean(), "mean_gm": zz["gm"].mean()})
    pd.DataFrame(rows).to_csv(OUT / "q2_kaldor.csv", index=False)


MODERATORS = {  # variable, mechanism, predicted sign
    "EDU_HC": ("Education (absorptive capacity)", +1),
    "RELUS": ("Income relative to the US (negative = catch-up bonus)", -1),
    "OPEN": ("Openness (export markets)", +1),
    "LNPOP": ("Population (home-market scale)", +1),
    "MIU": ("Mining & utilities share (commodity dependence)", -1),
    "UNDERVAL": ("Currency undervaluation (profitability of tradables)", +1),
    "POST2000": ("Periods from 2000 (competition from China)", -1),
}


def sample_sign(g, sign):
    """Within one sample: +1 if both estimators have the predicted sign and at least one is
    significant at 10%; -1 if both have the opposite sign and at least one is significant; else 0."""
    s = np.sign(g["coef"]) * sign
    if (s > 0).all() and (g["p"] < 0.10).any():
        return 1
    if (s < 0).all() and (g["p"] < 0.10).any():
        return -1
    return 0


def verdicts(t, key):
    """Combine main and core (D-039): supported / supported in one sample only / opposite /
    conflicting across samples / no evidence."""
    out = {}
    for k, g in t.groupby(key):
        sign = g["predicted_sign"].iloc[0]
        a = sample_sign(g[g["sample"] == "main"], sign)
        b = sample_sign(g[g["sample"] == "core"], sign)
        out[k] = {(1, 1): "supported", (1, 0): "supported in main sample only", (0, 1): "supported in core sample only",
                  (-1, -1): "opposite sign", (-1, 0): "opposite sign in main sample only",
                  (0, -1): "opposite sign in core sample only", (0, 0): "no evidence"}.get((a, b), "conflicting across samples")
    return pd.Series(out, name="verdict").rename_axis(key).reset_index()


def q3(p):
    rows = []
    for sname in SAMPLES:
        d = sample(p, sname, start=1950, end=2015, edu=EDU).copy()
        d["POST2000"] = (d["period"] >= 2000).astype(float)
        d["UNDERVAL"] = d["UNDERVAL"].clip(*d["UNDERVAL"].quantile([0.01, 0.99]))
        d = d.dropna(subset=["MIU", "UNDERVAL"])
        dev = d[~d["advanced"].astype(bool)]
        for est in ESTS:
            for mode in ["one at a time", "joint"]:
                dd = d.copy()
                terms = ["MAN"]
                mods = list(MODERATORS) if mode == "joint" else None
                todo = [[m] for m in MODERATORS] if mode == "one at a time" else [mods]
                for ms in todo:
                    dd = d.copy()
                    terms = ["MAN"]
                    for mname in ms:
                        c = float(dev[mname].median())   # centre at the median developing country
                        dd[f"MANx{mname}"] = dd["MAN"] * (dd[mname] - c)
                        terms.append(f"MANx{mname}")
                    extra_ctrl = [m for m in ms if m not in ("RELUS", "EDU_HC", "LNPOP", "OPEN", "POST2000")]
                    r = fit(dd, terms, est, edu=EDU, controls=("LNPOP", "OPEN", *extra_ctrl))
                    for mname in ms:
                        term = f"MANx{mname}"
                        lab, sign = MODERATORS[mname]
                        rows.append({"sample": sname, "estimator": est, "mode": mode, "moderator": mname,
                                     "label": lab, "predicted_sign": sign, "coef": r.params[term], "se": r.se[term],
                                     "p": r.pvalues[term], "MAN_at_median": r.params["MAN"],
                                     "nobs": r.nobs, "ncountries": r.ngroups})
    t = pd.DataFrame(rows)

    t = t.merge(verdicts(t[t["mode"] == "one at a time"], "moderator"), on="moderator", how="left")
    t.to_csv(OUT / "q3_moderators.csv", index=False)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p = load_panel()
    q1(p)
    q2(p)
    q3(p)
    me = pd.read_csv(OUT / "q1_me_reference.csv")
    print(me[me["model"].str.startswith("(3)")].round(3).to_string(index=False))
    l2 = pd.read_csv(OUT / "q2_lac.csv")
    print(l2[l2["estimator"] == "HT"][["sample", "term", "coef", "p", "n_lac_countries"]].round(3).to_string(index=False))
    print(pd.read_csv(OUT / "q2_kaldor.csv").round(2).to_string(index=False))
    q = pd.read_csv(OUT / "q3_moderators.csv")
    print(q[q["mode"] == "one at a time"][["sample", "estimator", "moderator", "predicted_sign", "coef", "p", "verdict"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
