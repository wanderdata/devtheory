"""Flows, rates by job cell and the test of P-RG3 (pre-analysis plan §§4–5).

    python empirics/code/enoe/ladders/02_flows.py

Reads the linked panels written by 01_link.py and writes aggregate tables only, to
empirics/output/enoe/ladders/:
  quarterly_rates.csv   employment exit and job-finding rates, quarter to quarter (§5.1)
  rates_<dim>.csv       exit (1 quarter, 1 year), persistence and upward transition (1 year)
                        by sector, by size x formality and by job cell (§5.2)
  decomposition.csv     R2 and Shapley shares of sector vs size x formality, with bootstrap
                        intervals over primary sampling units, for the main sample and the
                        measurement-error variants (§§5.3–5.4)
  misreport.csv         employees with the same employer start date at two first-quarter visits
                        whose size class or formality changes (§5.4 c)
  sector_test.csv       manufacturing minus services within size x formality cells (§5.3)
  earnings_growth.csv   change in log hourly earnings over a year by origin cell (outcome 5)
  transitions.csv       not employed / informal / formal transition matrices, quarter and year
Robustness: every decomposition and the sector test are also run with weights adjusted for
attrition (age group x sex x labour-force status, plan §2), and the decomposition with formality
alone in place of size x formality (OQ-65).
  results.md            report
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # shared ENOE modules

import numpy as np
import pandas as pd

import enoe_flows as fl
import enoe_link
from enoe_config import AGE_MAX, AGE_MIN, INTERIM, MIN_CELL, OUTPUT, URBAN_MAX_CD_A, WINDOWS

NBOOT = 499
SEED = 20261112
COLS = ["state", "fac_tri", "eda", "sex", "cs_p13_1", "psu", "ent", "ing_x_hrs", "pos_ocu", "p3r_anio", "p3r_mes", "proxy", "cd_a",
        "year", "q", "mes_cal"]


def wavg(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    return float(np.average(x, weights=w)) if len(x) and w.sum() > 0 else np.nan


def wmedian(x, w):
    o = np.argsort(x)
    x, w = np.asarray(x)[o], np.asarray(w)[o]
    c = np.cumsum(w)
    return x[np.searchsorted(c, c[-1] / 2)]


def prepare(panel):
    p = panel.copy()
    p["state"] = fl.state(p)
    for c in ["n_inf", "n_ren"]:
        if c in p.columns:
            p[c] = pd.to_numeric(p[c], errors="coerce")
    p["proxy"] = (p["n_inf"] != p["n_ren"]) if "n_inf" in p.columns else np.nan
    # primary sampling unit: CA + UPM in ENOEN (file description, "Consideraciones importantes")
    p["psu"] = (p["ca"].astype(str) + "-" if "ca" in p.columns else "") + p["upm"].astype(str)
    for c in ["fac_tri", "ing_x_hrs", "eda", "sex", "cs_p13_1", "pos_ocu", "p3r_anio", "p3r_mes", "cd_a", "mes_cal",
              "year", "q"]:
        if c in p.columns:
            p[c] = pd.to_numeric(p[c], errors="coerce")
    for c in COLS:
        if c not in p.columns:
            p[c] = np.nan
    # Interview month: MES_CAL where present (2023-24); otherwise from D_SEM, whose last two
    # digits are the week of the quarter (01-13), so month = 3(q-1) + ceil(week / 4.33).
    if "d_sem" in p.columns:
        week = pd.to_numeric(p["d_sem"], errors="coerce") % 100
        approx = 3 * (p["q"] - 1) + np.clip(np.ceil(week / (13 / 3)), 1, 3)
        p["mes_cal"] = p["mes_cal"].where(p["mes_cal"].between(1, 12), approx)
    return p


def merge_small(state, n, min_cell=MIN_CELL):
    """Merge job cells with too few origin observations into 'sector|other sizes|formality'."""
    small = set(n[n < min_cell].index)
    def f(s):
        if s == "N" or s not in small:
            return s
        sec, _, form = s.split("|")
        return f"{sec}|other sizes|{form}"
    return state.map(f)


def pairs(p, a, b):
    """Persons observed at positions a and b, origin aged AGE_MIN-AGE_MAX, origin weight."""
    w = enoe_link.wide(p, COLS)
    need = [f"state_{a}", f"state_{b}"]
    w = w.dropna(subset=need)
    w = w[w[f"eda_{a}"].between(AGE_MIN, AGE_MAX)]
    return w


def quarterly_rates(p, window):
    rows = []
    for i in range(4):
        w = pairs(p, i, i + 1)
        for area, ww in [("all", w), ("self-represented cities", w[w[f"cd_a_{i}"] <= URBAN_MAX_CD_A])]:
            o, d, wt = ww[f"state_{i}"], ww[f"state_{i + 1}"], ww[f"fac_tri_{i}"]
            e, n = o != "N", o == "N"
            rows.append({"window": window, "pair": i, "area": area,
                         "exit_rate": wavg(d[e] == "N", wt[e]),
                         "job_finding_rate": wavg(d[n] != "N", wt[n]),
                         "n_employed": int(e.sum()), "n_not_employed": int(n.sum()),
                         "job_to_job_rate": job_to_job(ww, i)})
    return pd.DataFrame(rows)


def job_to_job(w, i):
    """Employees at i and i+1 whose start date with the current employer, reported at i+1, is less
    than three months before the interview (Donovan et al., footnote 6). The start date is asked
    only in the extended questionnaire (first quarters), so this is defined only when i+1 is a
    first quarter. The month is asked only of those who started in the current or the previous
    year; anyone with an earlier start year has more than a year of tenure. The denominator is all
    employees with a valid start year; those who started in the last two years without a valid
    month are left out."""
    if not (w[f"q_{i + 1}"] == 1).all():
        return np.nan
    e = (w[f"pos_ocu_{i}"] == 1) & (w[f"pos_ocu_{i + 1}"] == 1) & (w[f"state_{i}"] != "N") & (w[f"state_{i + 1}"] != "N")
    x = w[e & w[f"p3r_anio_{i + 1}"].between(1900, 2100)]
    yr, an, mo = x[f"year_{i + 1}"], x[f"p3r_anio_{i + 1}"], x[f"p3r_mes_{i + 1}"]
    recent = an >= yr - 1
    x = x[~recent | mo.between(1, 12)]
    if not len(x):
        return np.nan
    months = (x[f"year_{i + 1}"] * 12 + x[f"mes_cal_{i + 1}"]) - (x[f"p3r_anio_{i + 1}"] * 12 + x[f"p3r_mes_{i + 1}"].where(x[f"p3r_mes_{i + 1}"].between(1, 12), 1))
    new = (x[f"p3r_anio_{i + 1}"] >= x[f"year_{i + 1}"] - 1) & months.between(0, 2)
    return wavg(new, x[f"fac_tri_{i}"])


def annual(p):
    """Person-level sample for 1-year outcomes: employed at position 0, observed at 1, 3 and 4."""
    w = pairs(p, 0, 4)
    w = w[w["state_0"] != "N"].copy()
    emp0 = w[w["ing_x_hrs_0"] > 0]
    med = emp0.groupby("state_0").apply(lambda x: wmedian(x["ing_x_hrs_0"], x["fac_tri_0"]), include_groups=False)
    rank = med.rank(method="first").to_dict()
    w["rank_decile"] = pd.qcut(w["state_0"].map(rank), 10, labels=False, duplicates="drop")
    w["exit_y"] = (w["state_4"] == "N").astype(float)
    w["persist_y"] = (w["state_4"] == w["state_0"]).astype(float)
    w["same_cell"] = w["state_4"] == w["state_0"]          # before small cells are merged
    w["up_y"] = fl.upward(w["state_0"], w["state_4"], rank)
    w["sector"], w["sizeform"] = fl.parts(w["state_0"])
    # Employer change between visits 0 and 4, from the start date reported at visit 4 (only when
    # visit 4 is a first quarter). Month is asked only of those who started in the current or
    # previous year; an earlier start year means no change.
    if (w["q_4"] == 1).all() and (w["q_0"] == 1).all():
        an, mo = w["p3r_anio_4"], w["p3r_mes_4"]
        start = an * 12 + mo.where(mo.between(1, 12), np.nan)
        start = start.where(an >= w["year_4"] - 1, -np.inf)
        w["changed_employer"] = np.where(an.between(1900, 2100) & start.notna(),
                                         (start > w["year_0"] * 12 + w["mes_cal_0"]).astype(float), np.nan)
        w.loc[w["state_4"] == "N", "changed_employer"] = 0.0
        # Plan §5.5: with same-employer misreporting above 10%, an upward transition counts only
        # when it involves a change of employer.
        w["up_emp_y"] = np.where(w["changed_employer"].isna() | w["up_y"].isna(), np.nan,
                                 w["up_y"] * w["changed_employer"])
    else:
        w["changed_employer"], w["up_emp_y"] = np.nan, np.nan
    w["exit_q"] = np.where(w["state_1"].isna(), np.nan, (w["state_1"] == "N").astype(float))
    w["confirmed"] = (w["state_1"] == w["state_0"]) & (w["state_3"] == w["state_4"])
    w["selfreport"] = w["proxy_0"] == False  # noqa: E712  (NaN when unknown)
    return w


def by_cell(w, col):
    g = w.groupby(col)
    out = pd.DataFrame({"n": g.size()})
    for y in ["exit_q", "exit_y", "persist_y", "up_y", "up_emp_y", "changed_employer"]:
        out[y] = g.apply(lambda x: wavg(x[y].dropna(), x.loc[x[y].notna(), "fac_tri_0"]), include_groups=False)
    return out.reset_index()


def boot_decomp(w, y, nboot=NBOOT, seed=SEED, control=None):
    d = w.dropna(subset=[y])
    ctl = d[control] if control else None
    est = fl.decompose(d[y].to_numpy(float), d["sector"], d["sizeform"], d["fac_tri_0"].to_numpy(float), ctl)
    rng = np.random.default_rng(seed)
    d = d.reset_index(drop=True)
    idx = d.groupby(["ent_0", "psu_0"]).indices
    strata = {}
    for (e, _), ix in idx.items():
        strata.setdefault(e, []).append(ix)
    y_, w_ = d[y].to_numpy(float), d["fac_tri_0"].to_numpy(float)
    sec, sf = d["sector"].to_numpy(), d["sizeform"].to_numpy()
    cc = d[control].to_numpy() if control else None
    diffs = []
    for _ in range(nboot):
        take = np.concatenate([np.concatenate([u[j] for j in rng.integers(0, len(u), len(u))])
                               for u in strata.values()])
        r = fl.decompose(y_[take], sec[take], sf[take], w_[take], None if cc is None else cc[take])
        diffs.append(r["shapley_sizeform"] - r["shapley_sector"])
    est.update({"n": len(d), "diff": est["shapley_sizeform"] - est["shapley_sector"],
                "diff_lo90": np.percentile(diffs, 5), "diff_hi90": np.percentile(diffs, 95)})
    return est


MANUF, SERVICES = "3", {"5", "6", "7", "8", "9", "10"}     # rama_est2 codes (file description, SDEMT field 63)


def _wls(y, X, w):
    sw = np.sqrt(w)
    return np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]


def sector_test(w, y, nboot=NBOOT, seed=SEED):
    """Second rejection condition of P-RG3 (plan §5.3): within size x formality cells, do
    manufacturing jobs have lower exit rates and higher upward-transition rates than service jobs?
    WLS of y on a manufacturing indicator (services = rama_est2 5-10) with size x formality,
    age-group, sex and schooling-level dummies; 90% interval from the UPM bootstrap."""
    d = w[w["sector"].isin({MANUF} | SERVICES)].dropna(subset=[y]).reset_index(drop=True)
    if len(d) < 1000:
        return None
    age = pd.cut(d["eda_0"], [15, 24, 34, 44, 54, 65], labels=False).astype(str)
    edu = pd.cut(d["cs_p13_1_0"].where(d["cs_p13_1_0"] < 99), [-1, 2, 3, 6, 9], labels=False).astype(str)
    ctl = pd.get_dummies(pd.DataFrame({"sf": d["sizeform"], "age": age, "sex": d["sex_0"].astype(str), "edu": edu}),
                         drop_first=True).to_numpy(float)
    X = np.column_stack([np.ones(len(d)), (d["sector"] == MANUF).astype(float), ctl])
    yv, wv = d[y].to_numpy(float), d["fac_tri_0"].to_numpy(float)
    est = _wls(yv, X, wv)[1]
    rng = np.random.default_rng(seed)
    idx = d.groupby(["ent_0", "psu_0"]).indices
    strata = {}
    for (e, _), ix in idx.items():
        strata.setdefault(e, []).append(ix)
    draws = []
    for _ in range(nboot):
        take = np.concatenate([np.concatenate([u[j] for j in rng.integers(0, len(u), len(u))]) for u in strata.values()])
        draws.append(_wls(yv[take], X[take], wv[take])[1])
    return {"outcome": y, "n": len(d), "manufacturing_minus_services": est,
            "lo90": np.percentile(draws, 5), "hi90": np.percentile(draws, 95),
            "mean_services": np.average(yv[d["sector"] != MANUF], weights=wv[d["sector"] != MANUF])}


AGE_GROUPS = [15, 24, 34, 44, 54, 65]


def attrition_factor(p, a, b):
    """Reweighting for attrition (plan §2): factor per person observed at a and b so that the
    linked sample matches, by age group x sex x labour-force status at a, the weighted
    distribution of everyone at a who could have been observed at b (visit number <= 5 - (b - a))."""
    full = p[(p["pos"] == a) & p["eda"].between(AGE_MIN, AGE_MAX) & (p["n_ent"] <= 5 - (b - a))].copy()
    seen = set(p.loc[p["pos"] == b, "pid"])
    full["linked"] = full["pid"].isin(seen)
    full["cell"] = (pd.cut(full["eda"], AGE_GROUPS, labels=False).astype(str) + "|" + full["sex"].astype(str)
                    + "|" + (full["state"] == "N").map({True: "N", False: "E"}))
    tot = full.groupby("cell")["fac_tri"].sum()
    lnk = full[full["linked"]].groupby("cell")["fac_tri"].sum()
    f = (tot / lnk).rename("factor")
    out = full[full["linked"]][["pid", "cell"]].join(f, on="cell").set_index("pid")["factor"]
    return out


def reweighted(w, factor):
    """Copy of an annual sample with fac_tri_0 replaced by the attrition-adjusted weight."""
    x = w.copy()
    x["fac_tri_0"] = x["fac_tri_0"] * x.index.map(factor).to_numpy(float)
    return x[x["fac_tri_0"].notna()]


def formality_only(w):
    """Copy of an annual sample whose 'sizeform' column holds formality alone (OQ-65)."""
    x = w.copy()
    x["sizeform"] = x["sizeform"].str.split("|").str[1]
    return x


def earnings_growth(w):
    """Plan outcome 5 (secondary): change in log hourly earnings between visits 0 and 4 for people
    employed at both with positive hourly earnings, by origin size x formality and by sector, for
    those in the same job cell and those who moved. Earnings non-response is reported."""
    emp4 = w["state_4"] != "N"
    x = w[emp4].copy()
    x["valid"] = (x["ing_x_hrs_0"] > 0) & (x["ing_x_hrs_4"] > 0)
    x["dlog"] = np.where(x["valid"], np.log(x["ing_x_hrs_4"].where(x["valid"]) / x["ing_x_hrs_0"].where(x["valid"])), np.nan)
    x["mover"] = np.where(x["same_cell"], "same cell", "moved")
    rows = []
    for col in ["sizeform", "sector"]:
        for (c, m), g in x.groupby([col, "mover"]):
            v = g[g["valid"]]
            rows.append({"dimension": col, "cell": c, "group": m, "n": len(g), "share_valid": g["valid"].mean(),
                         "mean_dlog": wavg(v["dlog"], v["fac_tri_0"]) if len(v) else np.nan,
                         "median_dlog": wmedian(v["dlog"].to_numpy(), v["fac_tri_0"].to_numpy()) if len(v) else np.nan})
    return pd.DataFrame(rows)


def segment(state):
    return np.where(state == "N", "not employed", np.where(state.str.endswith("|formal"), "formal",
                    np.where(state.str.endswith("|informal"), "informal", "employed, formality not specified")))


def transitions(p, w_all):
    """Weighted transition matrix between not employed, informal and formal employment over one
    quarter (average of the window's pairs) and over one year (first to fifth visit), ages 16-65,
    with origin weights and with attrition-adjusted weights."""
    rows = []
    specs = [("quarter", i, i + 1) for i in range(4)] + [("year", 0, 4)]
    for horizon, a, b in specs:
        w = pairs(p, a, b)
        fac = attrition_factor(p, a, b)
        w["o"], w["d"] = segment(w[f"state_{a}"]), segment(w[f"state_{b}"])
        for wt_name, wt in [("origin weights", w[f"fac_tri_{a}"]),
                            ("reweighted for attrition", w[f"fac_tri_{a}"] * w.index.map(fac).to_numpy(float))]:
            d = pd.DataFrame({"o": w["o"], "d": w["d"], "wt": wt}).dropna()
            m = d.groupby(["o", "d"])["wt"].sum().unstack(fill_value=0)
            m = m.div(m.sum(axis=1), axis=0)
            for o in m.index:
                for dd in m.columns:
                    rows.append({"horizon": horizon, "pair": a, "weights": wt_name, "origin": o, "destination": dd,
                                 "share": m.loc[o, dd]})
    t = pd.DataFrame(rows)
    return t.groupby(["horizon", "weights", "origin", "destination"], as_index=False)["share"].mean()


def misreport(p):
    """Employees with the same reported employer start date at two first-quarter visits (the only
    quarters with the start-date question): same year and month, or, for those who started
    before the previous year (month not asked), the same year. Share whose size class or
    formality differs. With
    the same employer, a change of class is either genuine growth across a size boundary or
    misreporting, so this bounds misreporting from above (§5.4 c)."""
    rows = []
    pos = sorted(p.loc[p["q"] == 1, "pos"].unique())
    for i in pos:
        for j in pos:
            if j <= i:
                continue
            w = pairs(p, i, j)
            same = ((w[f"pos_ocu_{i}"] == 1) & (w[f"pos_ocu_{j}"] == 1)
                    & (w[f"p3r_anio_{i}"] == w[f"p3r_anio_{j}"])
                    & ((w[f"p3r_mes_{i}"] == w[f"p3r_mes_{j}"])
                       | (~w[f"p3r_mes_{i}"].between(1, 12) & ~w[f"p3r_mes_{j}"].between(1, 12)
                          & (w[f"p3r_anio_{i}"] < w[f"year_{i}"] - 1)))
                    & w[f"p3r_anio_{i}"].between(1900, 2100)
                    & (w[f"state_{i}"] != "N") & (w[f"state_{j}"] != "N"))
            x = w[same]
            if not len(x):
                continue
            _, sf0 = fl.parts(x[f"state_{i}"])
            _, sf1 = fl.parts(x[f"state_{j}"])
            s0, s1 = sf0.str.split("|").str[0], sf1.str.split("|").str[0]
            f0, f1 = sf0.str.split("|").str[1], sf1.str.split("|").str[1]
            rows.append({"from_pos": i, "to_pos": j, "n": len(x),
                         "size_changes": wavg(s0 != s1, x[f"fac_tri_{i}"]),
                         "formality_changes": wavg(f0 != f1, x[f"fac_tri_{i}"])})
    return pd.DataFrame(rows)


def main():
    files = {w: INTERIM / f"{w}.parquet" for w in WINDOWS}
    files = {w: f for w, f in files.items() if f.exists()}
    if not files:
        print("No linked panels: run 01_link.py first. Nothing done.")
        return 0
    OUTPUT.mkdir(parents=True, exist_ok=True)
    qr, cells, dec, mis, st, eg, tr = [], {"sector": [], "sizeform": [], "state_0": []}, [], [], [], [], []
    for win, f in files.items():
        p = prepare(pd.read_parquet(f))
        qr.append(quarterly_rates(p, win))
        w = annual(p)
        n0 = w["state_0"].value_counts()
        w["state_0"] = merge_small(w["state_0"], n0)
        w["sector"], w["sizeform"] = fl.parts(w["state_0"])
        for col in cells:
            cells[col].append(by_cell(w, col).assign(window=win, weights="origin weights"))
        factor = attrition_factor(p, 0, 4)
        w_rw = reweighted(w, factor)
        for variant, d in [("main", w), ("confirmed transitions", w[w["confirmed"]]),
                           ("self-reported only", w[w["selfreport"]]),
                           ("reweighted for attrition", w_rw),
                           ("formality alone vs sector", formality_only(w)),
                           ("formality alone vs sector, confirmed transitions", formality_only(w[w["confirmed"]]))]:
            for y in ["exit_y", "up_y", "up_emp_y"]:
                if d[y].notna().sum() > 1000:
                    r = boot_decomp(d, y)
                    r.update({"window": win, "variant": variant, "outcome": y})
                    dec.append(r)
        # Exploratory, not in the plan (D-048): upward transitions have a ceiling for cells already
        # high in the earnings ranking, which favours whichever dimension tracks earnings more
        # closely. Same decomposition, conditional on the origin cell's earnings-rank decile.
        if w["up_y"].notna().sum() > 1000:
            r = boot_decomp(w, "up_y", control="rank_decile")
            r.update({"window": win, "variant": "main, conditional on origin rank decile (exploratory)",
                      "outcome": "up_y"})
            dec.append(r)
        for wlab, ww in [("origin weights", w), ("reweighted for attrition", w_rw)]:
            for y in ["exit_y", "up_y", "up_emp_y"]:
                r = sector_test(ww, y) if ww[y].notna().sum() > 1000 else None
                if r:
                    st.append({**r, "window": win, "weights": wlab})
        cells["sizeform"].append(by_cell(w_rw, "sizeform").assign(window=win, weights="reweighted for attrition"))
        eg.append(earnings_growth(w).assign(window=win))
        tr.append(transitions(p, w).assign(window=win))
        m = misreport(p)
        if len(m):
            mis.append(m.assign(window=win))
    pd.concat(qr).to_csv(OUTPUT / "quarterly_rates.csv", index=False)
    for col, name in [("sector", "sector"), ("sizeform", "sizeform"), ("state_0", "job")]:
        pd.concat(cells[col]).to_csv(OUTPUT / f"rates_{name}.csv", index=False)
    dec = pd.DataFrame(dec)
    dec.to_csv(OUTPUT / "decomposition.csv", index=False)
    if mis:
        pd.concat(mis).to_csv(OUTPUT / "misreport.csv", index=False)
    pd.concat(eg).to_csv(OUTPUT / "earnings_growth.csv", index=False)
    pd.concat(tr).to_csv(OUTPUT / "transitions.csv", index=False)
    st = pd.DataFrame(st)
    st.to_csv(OUTPUT / "sector_test.csv", index=False)
    print(st.round(4).to_string(index=False))
    print(dec.round(4).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
