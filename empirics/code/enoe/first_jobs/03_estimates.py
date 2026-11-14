"""Study 9.5, step 3: first jobs, where they lead, and the tests of P34-P37 (pre-analysis plan
§§1, 3-5).

    python empirics/code/enoe/first_jobs/03_estimates.py

Inputs: cohorts.parquet (step 2), the quarterly extracts (step 1) for the stock of young workers'
jobs. Outputs in empirics/output/enoe/first_jobs/:
  composition.csv  first jobs against the stock of jobs of employed 15-24-year-olds
  transitions.csv  state at interviews 3-5 by type of entry at interview 2
  estimates.csv    linear probability estimates for P35-P37, main and robustness
  oster.csv        sensitivity to selection on unobservables (P35, P36)
  earnings.csv     monthly earnings of first jobs relative to the minimum wage in force
  checks.csv       recall of never-worked answers, sample sizes
"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parent))
sys.path.append(str(HERE.parents[1] / "border_mw"))   # after this folder: both have an 01_extract.py

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import border_lib as bl  # noqa: E402

ex = importlib.import_module("01_extract")
TMP, OUT = ex.TMP, ex.OUT
PREMISES = [3, 4, 5, 6]          # ambito2: micro with premises, small, medium, large establishments
POS = {1: "wage employee", 2: "employer", 3: "own-account", 4: "unpaid"}
SECT = {1: "agriculture", 2: "mining and utilities", 3: "manufacturing", 4: "construction", 5: "commerce",
        6: "restaurants and lodging", 7: "transport and communications", 8: "professional and financial",
        9: "social services", 10: "other services", 11: "government"}
Z90 = 1.645


def entry_type(state, pos, amb):
    """Type of entry at an interview: formal; informal wage job in a unit with premises; informal wage job
    elsewhere; informal own-account or unpaid; employer or unknown; not employed."""
    t = np.select([state == "F", (state == "I") & (pos == 1) & np.isin(amb, PREMISES), (state == "I") & (pos == 1),
                   (state == "I") & np.isin(pos, [3, 4]), state == "N"],
                  ["formal", "informal wage, premises", "informal wage, other", "informal own-account or unpaid",
                   "not employed"], "other")
    return t


def prepare(c):
    c = c.copy()
    for v in range(1, 6):
        if f"state_{v}" in c:
            c[f"formal_{v}"] = (c[f"state_{v}"] == "F").astype(float)
            c[f"informal_{v}"] = (c[f"state_{v}"] == "I").astype(float)
            c[f"notemp_{v}"] = (c[f"state_{v}"] == "N").astype(float)
    c["entry2"] = entry_type(c["state_2"].to_numpy(), c["pos_ocu_2"].to_numpy(), c["ambito2_2"].to_numpy())
    c["entry3"] = entry_type(c["state_3"].to_numpy(), c["pos_ocu_3"].to_numpy(), c["ambito2_3"].to_numpy())
    c["wage_prem_5"] = (c["state_5"].isin(["F", "I"]) & (c["pos_ocu_5"] == 1) & c["ambito2_5"].isin(PREMISES)).astype(float)
    c["yq"] = c["start"]
    c["cl"] = c["ent_1"].astype(str) + "_" + c["upm_1"].astype(str)
    c["age"] = c["eda_1"].astype(int)
    c["school"] = c["anios_esc_1"].where(c["anios_esc_1"].between(0, 24), 99).astype(int)
    c["attend"] = (c["cs_p17_1"] == 1).astype(float)
    c["rel"] = (c["par_c_1"] // 100).fillna(9).astype(int)
    c["woman"] = (c["sex_1"] == 2).astype(float)
    c["hhf"] = c["hh_formal_1"].clip(upper=3)
    c["hhi"] = c["hh_informal_1"].clip(upper=3)
    c["urban"] = c["urban_1"].astype(float)
    c["w"] = c["fac_1"].astype(float)
    return c


FE_FULL = ["yq", "ent_1", "age", "school", "rel"]
CONT = ["woman", "attend", "hhf", "hhi", "urban"]


def lpm(d, y, treat, controls=True):
    """Weighted LPM of y on treatment dummies, with fixed effects and controls; CR1 by sampling unit."""
    d = d.dropna(subset=[y, "w"])
    cont = [x for x in CONT if d[x].nunique() > 1] if controls else []    # e.g. sex within a sex group
    X = d[treat + cont].to_numpy(float)
    fe = d[FE_FULL] if controls else d[["yq"]]
    f = bl.fit(d[y], X, fe, d["w"], d["cl"])
    w = d["w"].to_numpy()
    yv = d[y].to_numpy(float)
    sst = (w * (yv - np.average(yv, weights=w)) ** 2).sum()
    r2 = 1 - (w * f["e"] ** 2).sum() / sst
    out = []
    for j, t in enumerate(treat):
        se = np.sqrt(f["V"][j, j])
        out.append({"treatment": t, "beta": f["b"][j], "se": se, "lo90": f["b"][j] - Z90 * se,
                    "hi90": f["b"][j] + Z90 * se, "n": len(d), "n_treated": int(d[t].sum()), "r2": r2,
                    "mean_control": np.average(yv[d[t].to_numpy() == 0], weights=w[d[t].to_numpy() == 0])})
    return out


def short_r2(d, y, t):
    """Weighted regression of y on a constant and one treatment dummy (Oster's short regression)."""
    d = d.dropna(subset=[y, "w"])
    w, yv, x = d["w"].to_numpy(), d[y].to_numpy(float), d[t].to_numpy(float)
    X = np.column_stack([np.ones(len(x)), x])
    b = np.linalg.solve((X.T * w) @ X, (X.T * w) @ yv)
    e = yv - X @ b
    sst = (w * (yv - np.average(yv, weights=w)) ** 2).sum()
    return b[1], 1 - (w * e ** 2).sum() / sst


def oster_delta(b_short, r_short, b_long, r_long, rmax):
    """Approximate Oster (2019) delta that would bring the coefficient to zero."""
    if b_short == b_long or rmax <= r_long:
        return np.nan
    return b_long * (r_long - r_short) / ((b_short - b_long) * (rmax - r_long))


def samples(c, ages=(15, 24), entry=2):
    """P35, P36 and P37 samples for entry at interview 2 (outcome at 5) or 3 (outcome at 5)."""
    a = c[c["age"].between(*ages) & c["linked_5"].astype(bool) & c[f"linked_{entry}"].astype(bool)]
    if entry == 3:
        a = a[(a["state_2"] == "N") & a["never_2"].astype(bool)]
    e = a[f"entry{entry}"]
    never_e = a[f"never_{entry}"].astype(bool)
    p35 = a[(e == "not employed") & never_e | e.str.startswith("informal")].copy()
    p35["inf_entry"] = e.loc[p35.index].str.startswith("informal").astype(float)
    p36 = a[(e == "formal") | e.str.startswith("informal")].copy()
    p36["formal_entry"] = (e.loc[p36.index] == "formal").astype(float)
    p37 = a[e.isin(["informal wage, premises", "informal own-account or unpaid"])].copy()
    p37["premises_entry"] = (e.loc[p37.index] == "informal wage, premises").astype(float)
    return p35, p36, p37


def attrition_weights(c, entry=2):
    """Inverse probability of being linked to interview 5 among those linked at the entry interview,
    by cells of age group, sex, era and entry type."""
    a = c[c[f"linked_{entry}"].astype(bool)].copy()
    a["cell"] = (a["age"] // 5).astype(str) + a["woman"].astype(str) + a["era"] + a[f"entry{entry}"]
    rate = a.groupby("cell").apply(lambda g: np.average(g["linked_5"].astype(float), weights=g["w"]), include_groups=False)
    return c.assign(w=c["w"] / c.assign(cell=(c["age"] // 5).astype(str) + c["woman"].astype(str) + c["era"]
                                        + c[f"entry{entry}"])["cell"].map(rate))


def run_tests(c, label, ages=(15, 24), entry=2, controls=True):
    print("estimating:", label, flush=True)
    p35, p36, p37 = samples(c, ages, entry)
    rows = []
    for prop, d, t in [("P35", p35, "inf_entry"), ("P36", p36, "formal_entry"), ("P37", p37, "premises_entry")]:
        if len(d) < 200 or d[t].nunique() < 2:
            continue
        for r in lpm(d, "formal_5", [t], controls):
            r.update({"proposition": prop, "spec": label, "outcome": "formal_5"})
            rows.append(r)
    return rows


def main():
    c = prepare(pd.read_parquet(TMP / "cohorts.parquet"))
    main_c = c[c["age"].between(15, 24)]
    # ------------------------------------------------------------ composition (P34)
    stock = pd.read_csv(OUT / "stock.csv")
    ent = main_c[main_c["linked_2"].astype(bool) & main_c["state_2"].isin(["F", "I"])]
    w = ent["w"]
    comp = []
    for col, labels, name in [("state_2", {"F": "formal", "I": "informal"}, "formality"), ("pos_ocu_2", POS, "position"),
                              ("rama_est2_2", SECT, "sector"), ("entry2", None, "entry type")]:
        g = ent.groupby(col)["w"].sum() / w.sum()
        for k, v in g.items():
            comp.append({"dimension": name, "category": (labels or {}).get(k, k), "first_jobs": v})
    comp = pd.DataFrame(comp)
    # stock composition from the quarterly extracts (employed 15-24, all quarters used)
    sparts = []
    for f in sorted(TMP.glob("q_*.parquet")):
        s = pd.read_parquet(f, columns=["eda", "state", "pos_ocu", "rama_est2", "fac"])
        s = s[s["eda"].between(15, 24) & s["state"].isin(["F", "I"])]
        sparts.append(s)
    st_ = pd.concat(sparts)
    srows = []
    for col, labels, name in [("state", {"F": "formal", "I": "informal"}, "formality"), ("pos_ocu", POS, "position"),
                              ("rama_est2", SECT, "sector")]:
        g = st_.groupby(col)["fac"].sum() / st_["fac"].sum()
        for k, v in g.items():
            srows.append({"dimension": name, "category": labels.get(k, k), "stock": v})
    comp = comp.merge(pd.DataFrame(srows), on=["dimension", "category"], how="left")
    comp.to_csv(OUT / "composition.csv", index=False)

    # ------------------------------------------------------------ transitions
    tr = []
    a = main_c[main_c["linked_2"].astype(bool)]
    a = a[(a["entry2"] != "not employed") | a["never_2"].astype(bool)]
    for v in [3, 4, 5]:
        b = a[a[f"linked_{v}"].astype(bool)]
        for e, g in b.groupby("entry2"):
            tot = g["w"].sum()
            for s_, lab in [("F", "formal"), ("I", "informal"), ("N", "not employed"), ("U", "employed, formality unknown")]:
                tr.append({"entry": e, "interview": v, "state": lab, "share": g.loc[g[f"state_{v}"] == s_, "w"].sum() / tot,
                           "n": len(g)})
    pd.DataFrame(tr).to_csv(OUT / "transitions.csv", index=False)

    # ------------------------------------------------------------ estimates
    rows = run_tests(c, "main")
    rows += run_tests(c, "no controls", controls=False)
    rows += run_tests(c, "ages 15-29", ages=(15, 29))
    rows += run_tests(c, "entry at interview 3", entry=3)
    rows += run_tests(attrition_weights(c), "attrition weights")
    rows += run_tests(c[c["era"] == "2005-2019"], "2005-2019 only")
    rows += run_tests(c[c["attend"] == 0], "not attending school")
    for lab, sub in [("women", c["woman"] == 1), ("men", c["woman"] == 0), ("schooling < 12", c["school"] < 12),
                     ("schooling >= 12", c["school"].between(12, 24))]:
        rows += run_tests(c[sub], f"group: {lab}")
    per = {"2005-2008": (2005, 2008), "2009-2014": (2009, 2014), "2015-2019": (2015, 2019), "2022-": (2022, 2030)}
    for lab, (a0, a1) in per.items():
        rows += run_tests(c[c["year_1"].between(a0, a1)], f"period: {lab}")
    est = pd.DataFrame(rows)

    # probit average marginal effects (P35, P36), main sample
    import statsmodels.api as sm
    p35, p36, p37 = samples(c)
    for prop, d, t in [("P35", p35, "inf_entry"), ("P36", p36, "formal_entry")]:
        d = d.dropna(subset=["formal_5"])
        # Point estimates only (a comparison with the LPM); year rather than quarter effects and no
        # clustered covariance, to keep the dense design within the workspace's memory.
        X = pd.get_dummies(d[["year_1", "age", "rel"]].astype(str), drop_first=True).astype(np.float32)
        X[["school"]] = d[["school"]]
        X["school2"] = d["school"] ** 2
        X[[t] + CONT] = d[[t] + CONT]
        X = sm.add_constant(X)
        m = sm.GLM(d["formal_5"], X.astype(float), family=sm.families.Binomial(link=sm.families.links.Probit()),
                   var_weights=d["w"] / d["w"].mean()).fit()
        X1, X0 = X.copy(), X.copy()
        X1[t], X0[t] = 1.0, 0.0
        ame = np.average(m.predict(X1) - m.predict(X0), weights=d["w"])
        est = pd.concat([est, pd.DataFrame([{"proposition": prop, "spec": "probit AME", "treatment": t, "beta": ame,
                                             "n": len(d), "outcome": "formal_5"}])], ignore_index=True)
    est.to_csv(OUT / "estimates.csv", index=False)

    # ------------------------------------------------------------ Oster sensitivity
    orows = []
    for prop, d, t in [("P35", p35, "inf_entry"), ("P36", p36, "formal_entry"), ("P37", p37, "premises_entry")]:
        bs, rs = short_r2(d, "formal_5", t)
        lg = lpm(d, "formal_5", [t])[0]
        for mult in [1.3, 2.0]:
            rmax = min(1.0, mult * lg["r2"])
            orows.append({"proposition": prop, "beta_short": bs, "r2_short": rs, "beta_long": lg["beta"], "r2_long": lg["r2"],
                          "rmax": rmax, "rmax_rule": f"{mult} x R2 long",
                          "delta_for_zero": oster_delta(bs, rs, lg["beta"], lg["r2"], rmax)})
    pd.DataFrame(orows).to_csv(OUT / "oster.csv", index=False)

    # ------------------------------------------------------------ earnings of first jobs
    er = ent[(ent["ingocup_2"] > 0) & (ent["salario_2"] > 0)].copy()
    er["rel_min"] = er["ingocup_2"] / er["salario_2"]
    erows = []
    for e, g in er.groupby("entry2"):
        o = np.argsort(g["rel_min"].to_numpy())
        cw = np.cumsum(g["w"].to_numpy()[o]) / g["w"].sum()
        vals = g["rel_min"].to_numpy()[o]
        erows.append({"entry": e, "median_rel_min": vals[np.searchsorted(cw, 0.5)], "p25": vals[np.searchsorted(cw, 0.25)],
                      "p75": vals[np.searchsorted(cw, 0.75)], "hours_mean": np.average(g["hrsocup_2"].fillna(0), weights=g["w"]),
                      "reporting": len(g) / int((ent["entry2"] == e).sum()), "n": len(g)})
    pd.DataFrame(erows).to_csv(OUT / "earnings.csv", index=False)

    # ------------------------------------------------------------ checks
    b = main_c[main_c["linked_2"].astype(bool) & (main_c["state_2"] == "N")]
    checks = {"cohort persons (15-29, never worked, not employed at interview 1)": len(c),
              "of which aged 15-24": len(main_c),
              "aged 15-24 linked to interview 2": int(main_c["linked_2"].sum()),
              "aged 15-24 linked to interview 5": int(main_c["linked_5"].sum()),
              "first-job entrants at interview 2 (15-24), formal or informal": len(ent),
              "entrants linked to interview 5": int(ent["linked_5"].sum()),
              "not employed at 2: share now reporting having worked (recall check)":
                  float(np.average(~b["never_2"].astype(bool), weights=b["w"])),
              "informal share of first jobs": float(comp.query("dimension == 'formality' and category == 'informal'")["first_jobs"].iloc[0]),
              "informal share of stock 15-24": float(comp.query("dimension == 'formality' and category == 'informal'")["stock"].iloc[0])}
    pd.Series(checks, name="value").rename_axis("check").to_csv(OUT / "checks.csv")
    print(pd.Series(checks).to_string())
    print(est[est["spec"].isin(["main", "no controls", "probit AME"])][["proposition", "spec", "beta", "lo90", "hi90", "n",
                                                                         "n_treated", "mean_control"]].round(4).to_string(index=False))
    print(pd.DataFrame(orows).round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
