"""Specification curve for the headline estimates of WP07 (pre-analysis plan B7).

192 specifications. Dimensions: estimator (HT, FE, RE) x sample (main, excl_cpe, core, developing) x period length
(5, 10 years) x manufacturing share (current, constant 2020 prices) x growth source (PWT rgdpna,
rgdpo) x schooling (PWT-based EDU_HC, Barro-Lee EDU). System GMM, listed in the plan, is not
included: no validated implementation is available here (D-040).

Estimands (each a slope on the start-of-period share, pp of annual growth per point of share):
    MAN by subperiod (1970-90, 1990-2005, 2005-20), no interactions
    LAC minus rest, MAN, by subperiod
    each UN sector share by subperiod (current prices only)

Classification per estimand across all specifications that could be estimated:
    robustly positive / negative: >= 90% of estimates of one sign and >= 50% significant at 10%
    leaning positive / negative:  >= 75% of one sign
    fragile: otherwise

Writes empirics/output/motors/speccurve/estimates.csv and summary.csv.
"""
import itertools

import numpy as np
import pandas as pd
from scipy import stats

from config import OUTPUT
from models import add_terms, fit, load_panel, sample

OUT = OUTPUT / "speccurve"
SUBS = {"1970–90": range(1970, 1990), "1990–2005": range(1990, 2005), "2005–20": range(2005, 2020)}
SECTORS = ["MAN", "AGR", "MIU", "CON", "TRH", "TSC", "OTH", "SER"]


def specs():
    for est, smp, length, share, growth, edu in itertools.product(
            ["HT", "FE", "RE"], ["main", "excl_cpe", "core", "developing"], [5, 10],
            ["MAN", "MAN_K"], ["GR", "GR_O"], ["EDU_HC", "EDU"]):
        yield dict(estimator=est, sample=smp, length=length, share=share, growth=growth, edu=edu)


def run():
    panels = {5: load_panel(5), 10: load_panel(10)}
    rows, skipped = [], []
    for s in specs():
        p = panels[s["length"]].copy()
        p["GR"] = p[s["growth"]]
        p["MAN_CUR"] = p["MAN"]
        if s["share"] == "MAN_K":
            p["MAN"] = p["MAN_K"]
        d = sample(p, s["sample"], start=1970, end=2015, edu=s["edu"], years=s["length"])
        if d["iso3"].nunique() < 20:
            skipped.append(s)
            continue
        groups = {k: d["period"].isin(list(v)) for k, v in SUBS.items()}
        lac = d["lac"].astype(bool)
        try:
            dd, terms = add_terms(d, edu=s["edu"], slope_groups=groups)
            r = fit(dd, terms, s["estimator"], edu=s["edu"])
            for k in SUBS:
                t = f"MAN[{k}]"
                if t in r.params:
                    rows.append({**s, "estimand": f"Manufacturing, {k}", "family": "Q1", "coef": r.params[t], "se": r.se[t]})
            g2 = {}
            for k, v in SUBS.items():
                inp = d["period"].isin(list(v))
                g2[f"L{k}"], g2[f"R{k}"] = inp & lac, inp & ~lac
            dd, terms = add_terms(d, edu=s["edu"], slope_groups=g2)
            r = fit(dd, terms, s["estimator"], edu=s["edu"])
            for k in SUBS:
                a, b = f"MAN[L{k}]", f"MAN[R{k}]"
                if a in r.params and b in r.params:
                    se = float(np.sqrt(r.cov.loc[a, a] + r.cov.loc[b, b] - 2 * r.cov.loc[a, b]))
                    rows.append({**s, "estimand": f"LAC minus rest, {k}", "family": "Q2",
                                 "coef": r.params[a] - r.params[b], "se": se})
                    rows.append({**s, "estimand": f"Manufacturing in LAC, {k}", "family": "Q2",
                                 "coef": r.params[a], "se": r.se[a]})
        except Exception as e:  # noqa: BLE001 - record and continue; failures are counted
            rows.append({**s, "estimand": "error", "family": "error", "coef": np.nan, "se": np.nan, "error": str(e)[:200]})
        if s["share"] == "MAN":   # sector estimands only for current-price shares
            for sec in SECTORS:
                q = p.copy()
                q["MAN"] = q["MAN_CUR"]
                d2 = sample(q, s["sample"], start=1970, end=2015, edu=s["edu"], share=sec, years=s["length"])
                if d2["iso3"].nunique() < 20:
                    continue
                gg = {k: d2["period"].isin(list(v)) for k, v in SUBS.items()}
                try:
                    dd, terms = add_terms(d2, share=sec, edu=s["edu"], slope_groups=gg)
                    r = fit(dd, terms, s["estimator"], edu=s["edu"], other_share=None)
                    for k in SUBS:
                        t = f"{sec}[{k}]"
                        if t in r.params:
                            rows.append({**s, "estimand": f"{sec}, {k}", "family": "Q4", "sector": sec,
                                         "subperiod": k, "coef": r.params[t], "se": r.se[t]})
                except Exception as e:  # noqa: BLE001
                    rows.append({**s, "estimand": "error", "family": "error", "coef": np.nan, "se": np.nan,
                                 "error": str(e)[:200]})
    t = pd.DataFrame(rows)
    t["p"] = 2 * stats.norm.sf(np.abs(t["coef"] / t["se"]))
    if skipped:   # never silently: a skipped specification is reported
        print(f"skipped {len(skipped)} specifications with fewer than 20 countries")
    return t


def classify(g):
    g = g.dropna(subset=["coef"])
    n = len(g)
    pos, neg = (g["coef"] > 0).mean(), (g["coef"] < 0).mean()
    sp, sn = ((g["coef"] > 0) & (g["p"] < 0.10)).mean(), ((g["coef"] < 0) & (g["p"] < 0.10)).mean()
    if pos >= 0.9 and sp >= 0.5:
        v = "robustly positive"
    elif neg >= 0.9 and sn >= 0.5:
        v = "robustly negative"
    elif pos >= 0.75:
        v = "leaning positive"
    elif neg >= 0.75:
        v = "leaning negative"
    else:
        v = "fragile"
    return pd.Series({"n_specs": n, "median": g["coef"].median(), "q10": g["coef"].quantile(0.1),
                      "q90": g["coef"].quantile(0.9), "share_positive": pos, "share_pos_sig": sp,
                      "share_neg_sig": sn, "verdict": v})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t = run()
    t.to_csv(OUT / "estimates.csv", index=False)
    ok = t[t["family"] != "error"]
    s = ok.groupby(["family", "estimand"]).apply(classify, include_groups=False).reset_index()
    s.to_csv(OUT / "summary.csv", index=False)
    print(f"{len(ok)} estimates from {ok[['estimator', 'sample', 'length', 'share', 'growth', 'edu']].drop_duplicates().shape[0]} "
          f"specifications; errors: {(t['family'] == 'error').sum()}")
    print(s.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
