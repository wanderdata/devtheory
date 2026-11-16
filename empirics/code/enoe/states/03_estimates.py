"""Study 9.6, step 3: adjusted state measures of one-year mobility, their signal and persistence,
and the relation with growth of GDP per person (pre-analysis plan §§1, 3-4).

    python empirics/code/enoe/states/03_estimates.py

Inputs: panels.parquet (step 2), state_quarters.csv (step 1), INEGI PIBE (gdp.py). Outputs in
empirics/output/enoe/states/:
  state_effects.csv  adjusted measure by state, measure, period and specification (estimate, s.e., EB)
  signal.csv         variance of state effects, signal share and disattenuated persistence
  growth.csv         rank correlations with growth (P40 and secondary analyses), bootstrap intervals
  state_table.csv    one row per state for tables and maps
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parent))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import sparse, stats  # noqa: E402

import gdp  # noqa: E402
from enoe_config import INTERIM, OUTPUT_ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "states"
TMP = INTERIM / "states"
PERIODS = {"2005-2011": (2005, 2011), "2012-2018": (2012, 2018), "2022-2025": (2022, 2025)}
OIL = [4, 27]                     # Campeche, Tabasco
B = 1999
SEED = 96


# --------------------------------------------------------------------- data ---

def prepare():
    p = pd.read_parquet(TMP / "panels.parquet")
    p = p[p["linked_5"].astype(bool)].copy()
    p["period"] = None
    for k, (a, b) in PERIODS.items():
        p.loc[p["start_year"].between(a, b), "period"] = k
    p = p[p["period"].notna()]
    p["emp1"] = p["state"].isin(["F", "I"])
    p["emp5"] = p["state_5"].isin(["F", "I"])
    # national median log hourly earnings by sector x formality and start year (first interviews)
    q = p[p["emp1"] & p["lnw"].notna() & p["rama_est2"].between(1, 11)]
    med = (q.groupby(["start_year", "rama_est2", "state"])
           .apply(lambda g: _wmedian(g["lnw"].to_numpy(), g["fac"].to_numpy()), include_groups=False).rename("med"))
    p = p.join(med, on=["start_year", "rama_est2", "state"])
    m5 = med.rename("med5").rename_axis(["start_year", "rama_est2_5", "state_5"])
    p = p.join(m5, on=["start_year", "rama_est2_5", "state_5"])
    p["M1"] = np.where(p["state"] == "I", (p["state_5"] == "F").astype(float), np.nan)
    ok1 = p["emp1"] & p["med"].notna()
    p["M2"] = np.where(ok1, (p["emp5"] & (p["med5"] > p["med"])).astype(float), np.nan)
    p["M3"] = np.where(p["emp1"], (~p["emp5"]).astype(float), np.nan)
    p["school"] = p["anios_esc"].where(p["anios_esc"].between(0, 24), 99).astype(int)
    p["sector"] = p["rama_est2"].where(p["rama_est2"].between(1, 11), 0).fillna(0).astype(int)
    p["cl"] = p["ent_i"].astype(str) + "_" + p["upm"].astype(str)
    p["yq"] = p["start_year"].astype(str) + "Q" + p["start_q"].astype(str)
    return p


def _wmedian(x, w):
    o = np.argsort(x)
    c = np.cumsum(w[o])
    return x[o][np.searchsorted(c, c[-1] / 2)]


# ---------------------------------------------------------------- estimator ---

def dummies(s, drop_first=True):
    codes, cats = pd.factorize(s.astype(str), sort=True)
    n, k = len(codes), len(cats)
    m = sparse.csr_matrix((np.ones(n), (np.arange(n), codes)), shape=(n, k))
    return m[:, 1:] if drop_first else m


def state_effects(d, y, controls):
    """Weighted LPM of y on 32 state dummies (no intercept) and control fixed effects. Returns the
    adjusted level for each state at the sample's average composition, with clustered s.e."""
    d = d[d[y].notna()]
    S = dummies(d["ent_i"], drop_first=False)
    blocks = [S] + [dummies(d[c]) for c in controls]
    X = sparse.hstack(blocks).tocsr()
    w = d["fac"].to_numpy(float)
    yv = d[y].to_numpy(float)
    XtW = X.T.multiply(w).tocsr()
    A = (XtW @ X).toarray()
    beta = np.linalg.solve(A, XtW @ yv)
    e = yv - X @ beta
    Ainv = np.linalg.inv(A)
    codes, inv = np.unique(d["cl"].to_numpy(), return_inverse=True)
    C = sparse.csr_matrix((np.ones(len(inv)), (inv, np.arange(len(inv)))), shape=(len(codes), len(inv)))
    Sc = (C @ X.multiply((w * e)[:, None]).tocsr()).toarray()
    G, n, k = len(codes), X.shape[0], X.shape[1]
    V = G / (G - 1) * (n - 1) / (n - k) * Ainv @ (Sc.T @ Sc) @ Ainv
    k_s = S.shape[1]
    xbar = np.asarray(X[:, k_s:].multiply(w[:, None]).sum(0)).ravel() / w.sum()
    rows = []
    ents = np.sort(d["ent_i"].unique())
    for j, ent in enumerate(ents):
        c = np.zeros(k)
        c[j] = 1.0
        c[k_s:] = xbar
        rows.append({"ent": int(ent), "theta": c @ beta, "se": float(np.sqrt(c @ V @ c)),
                     "n": int((d["ent_i"] == ent).sum()),
                     "raw": np.average(yv[d["ent_i"].to_numpy() == ent], weights=w[d["ent_i"].to_numpy() == ent])})
    return pd.DataFrame(rows)


def signal(t):
    """Variance of estimates, mean sampling variance, signal variance tau^2 and its share."""
    v = t["theta"].var(ddof=1)
    s2 = (t["se"] ** 2).mean()
    tau2 = max(v - s2, 0.0)
    return {"var_estimates": v, "mean_sampling_var": s2, "tau2": tau2, "signal_share": tau2 / v if v > 0 else np.nan}


def eb(t):
    s = signal(t)
    mu = t["theta"].mean()
    lam = s["tau2"] / (s["tau2"] + t["se"] ** 2)
    return mu + lam * (t["theta"] - mu)


# ------------------------------------------------------------------- growth ---

def gdp_per_person():
    g = gdp.state_gdp()
    pop = pd.read_csv(OUT / "state_quarters.csv").groupby(["ent_i", "year"])["pop_all"].mean().rename("pop").reset_index()
    g = g.merge(pop.rename(columns={"ent_i": "ent"}), on=["ent", "year"], how="inner")
    for c in ["gdp", "non_oil"]:
        g[f"{c}_pc"] = g[c] * 1e6 / g["pop"]          # pesos of 2018 per person
    return g


def growth(g, col, a, b):
    x = g[g["year"].isin([a, b])].pivot(index="ent", columns="year", values=col)
    return (np.log(x[b]) - np.log(x[a])) / (b - a)


def spearman_ci(x, y, z=None, seed=SEED):
    """Spearman correlation (partial on z, via ranks and OLS residuals, if z given) with a 90%
    percentile interval from resampling states."""
    def rho(ix):
        rx, ry = stats.rankdata(x[ix]), stats.rankdata(y[ix])
        if z is not None:
            Z = np.column_stack([np.ones(len(ix))] + [stats.rankdata(c[ix]) for c in z])
            rx = rx - Z @ np.linalg.lstsq(Z, rx, rcond=None)[0]
            ry = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
        return np.corrcoef(rx, ry)[0, 1]
    idx = np.arange(len(x))
    r0 = rho(idx)
    rng = np.random.default_rng(seed)
    bs = np.array([rho(rng.choice(idx, len(idx), replace=True)) for _ in range(B)])
    return r0, np.nanpercentile(bs, 5), np.nanpercentile(bs, 95)


# --------------------------------------------------------------------- main ---

def main():
    p = prepare()
    ctrl = {"M1": ["yq", "eda", "sex", "school", "sector", "urban"],
            "M2": ["yq", "eda", "sex", "school", "sector", "state", "urban"],
            "M3": ["yq", "eda", "sex", "school", "sector", "state", "urban"]}
    eff = []
    for per in PERIODS:
        d = p[p["period"] == per]
        for m in ["M1", "M2", "M3"]:
            t = state_effects(d, m, ctrl[m])
            t["eb"] = eb(t)
            t["measure"], t["period"], t["spec"] = m, per, "main"
            eff.append(t)
            print(per, m, "done", flush=True)
        t = state_effects(d[d["urban"].astype(bool)], "M1", ctrl["M1"][:-1])
        t["eb"] = eb(t)
        t["measure"], t["period"], t["spec"] = "M1", per, "urban only"
        eff.append(t)
    e = pd.concat(eff, ignore_index=True)
    e["state"] = e["ent"].map(gdp.SHORT)
    e.to_csv(OUT / "state_effects.csv", index=False, float_format="%.6g")

    # signal and persistence
    sig = []
    main = e[e["spec"] == "main"]
    for (m, per), t in main.groupby(["measure", "period"]):
        sig.append({"measure": m, "period": per, "kind": "adjusted", **signal(t)})
        tr = t.assign(theta=t["raw"])
        sig.append({"measure": m, "period": per, "kind": "unadjusted", **signal(tr)})
    for m in ["M1", "M2", "M3"]:
        for a, b in [("2005-2011", "2012-2018"), ("2012-2018", "2022-2025")]:
            x = main[(main["measure"] == m) & (main["period"] == a)].set_index("ent")
            y = main[(main["measure"] == m) & (main["period"] == b)].set_index("ent")
            j = x.index.intersection(y.index)
            r = np.corrcoef(x.loc[j, "theta"], y.loc[j, "theta"])[0, 1]
            rel = signal(x)["signal_share"] * signal(y)["signal_share"]
            rng = np.random.default_rng(SEED)
            bs = []
            for _ in range(B):
                ix = rng.choice(j, len(j), replace=True)
                bs.append(np.corrcoef(x.loc[ix, "theta"], y.loc[ix, "theta"])[0, 1])
            sig.append({"measure": m, "period": f"{a} vs {b}", "kind": "persistence", "corr": r,
                        "corr_lo90": np.nanpercentile(bs, 5), "corr_hi90": np.nanpercentile(bs, 95),
                        "disattenuated": r / np.sqrt(rel) if rel > 0 else np.nan})
    pd.DataFrame(sig).to_csv(OUT / "signal.csv", index=False, float_format="%.6g")

    # growth
    g = gdp_per_person()
    gr = pd.DataFrame({"g_2012_2019": growth(g, "gdp_pc", 2012, 2019), "g_2005_2019": growth(g, "gdp_pc", 2005, 2019),
                       "g_nonoil_2012_2019": growth(g, "non_oil_pc", 2012, 2019),
                       "lgdppc_2005": np.log(g[g["year"] == 2005].set_index("ent")["gdp_pc"]),
                       "lgdppc_2012": np.log(g[g["year"] == 2012].set_index("ent")["gdp_pc"])})
    sq = pd.read_csv(OUT / "state_quarters.csv")
    gr["formal_2005_2011"] = sq[sq["year"].between(2005, 2011)].groupby("ent_i")["formal_share"].mean()
    gr["formal_2012_2018"] = sq[sq["year"].between(2012, 2018)].groupby("ent_i")["formal_share"].mean()
    for m in ["M1", "M2", "M3"]:
        for per in PERIODS:
            gr[f"{m}_{per}"] = main[(main["measure"] == m) & (main["period"] == per)].set_index("ent")["theta"]
            gr[f"{m}_{per}_eb"] = main[(main["measure"] == m) & (main["period"] == per)].set_index("ent")["eb"]
    gr.index.name = "ent"
    gr = gr.reset_index()
    gr["state"] = gr["ent"].map(gdp.SHORT)
    gr["name"] = gr["ent"].map(gdp.STATES)
    gr.to_csv(OUT / "state_table.csv", index=False, float_format="%.6g")
    tests = []
    no = gr[~gr["ent"].isin(OIL)]

    def add(label, d, x, y, z=None, role="secondary"):
        r, lo, hi = spearman_ci(d[x].to_numpy(), d[y].to_numpy(), None if z is None else [d[c].to_numpy() for c in z])
        tests.append({"test": label, "role": role, "x": x, "y": y, "conditioning": ", ".join(z or []), "states": len(d),
                      "rho": r, "lo90": lo, "hi90": hi})

    add("P40: M1 2005-2011 vs growth 2012-2019, without Campeche and Tabasco", no, "M1_2005-2011", "g_2012_2019",
        role="P40")
    add("conditional on initial GDP per person and formal share", no, "M1_2005-2011", "g_2012_2019",
        ["lgdppc_2012", "formal_2005_2011"])
    add("M2 (upward moves) instead of M1", no, "M2_2005-2011", "g_2012_2019")
    add("M3 (exits) instead of M1", no, "M3_2005-2011", "g_2012_2019")
    add("contemporaneous: M1 2005-2011 vs growth 2005-2019", no, "M1_2005-2011", "g_2005_2019")
    add("all 32 states", gr, "M1_2005-2011", "g_2012_2019")
    add("all 32 states, non-oil GDP (added after the plan, D-061)", gr, "M1_2005-2011", "g_nonoil_2012_2019")
    add("M1 2012-2018 vs growth 2012-2019 (contemporaneous)", no, "M1_2012-2018", "g_2012_2019")
    add("descriptive: M1 2005-2011 vs formal share 2005-2011", gr, "M1_2005-2011", "formal_2005_2011", role="descriptive")
    add("descriptive: M1 2005-2011 vs log GDP per person 2005", gr, "M1_2005-2011", "lgdppc_2005", role="descriptive")
    t = pd.DataFrame(tests)
    t.to_csv(OUT / "growth.csv", index=False, float_format="%.6g")
    print(pd.DataFrame(sig).round(4).to_string(index=False))
    print(t.round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
