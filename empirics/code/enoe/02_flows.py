"""Flows, rates by job cell and the test of P-RG3 (pre-analysis plan §§4–5).

    python empirics/code/enoe/02_flows.py

Reads the linked panels written by 01_link.py and writes aggregate tables only, to
empirics/output/enoe/:
  quarterly_rates.csv   employment exit and job-finding rates, quarter to quarter (§5.1)
  rates_<dim>.csv       exit (1 quarter, 1 year), persistence and upward transition (1 year)
                        by sector, by size x formality and by job cell (§5.2)
  decomposition.csv     R2 and Shapley shares of sector vs size x formality, with bootstrap
                        intervals over primary sampling units, for the main sample and the
                        measurement-error variants (§§5.3–5.4)
  misreport.csv         employees with the same employer start date in consecutive quarters
                        whose size class or formality changes (§5.4 c)
  results.md            report
"""
import sys

import numpy as np
import pandas as pd

import enoe_flows as fl
import enoe_link
from enoe_config import AGE_MAX, AGE_MIN, INTERIM, MIN_CELL, OUTPUT, URBAN_MAX_CD_A, WINDOWS

NBOOT = 499
SEED = 20261112
COLS = ["state", "fac_tri", "eda", "psu", "ent", "ing_x_hrs", "pos_ocu", "p3r_anio", "p3r_mes", "proxy", "cd_a",
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
    for c in ["fac_tri", "ing_x_hrs", "eda", "pos_ocu", "p3r_anio", "p3r_mes", "cd_a", "mes_cal", "year", "q"]:
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
    first quarter."""
    if not (w[f"q_{i + 1}"] == 1).all():
        return np.nan
    e = (w[f"pos_ocu_{i}"] == 1) & (w[f"pos_ocu_{i + 1}"] == 1) & (w[f"state_{i}"] != "N") & (w[f"state_{i + 1}"] != "N")
    x = w[e & w[f"p3r_anio_{i + 1}"].between(1900, 2100) & w[f"p3r_mes_{i + 1}"].between(1, 12)]
    if not len(x):
        return np.nan
    months = (x[f"year_{i + 1}"] * 12 + x[f"mes_cal_{i + 1}"]) - (x[f"p3r_anio_{i + 1}"] * 12 + x[f"p3r_mes_{i + 1}"])
    return wavg(months < 3, x[f"fac_tri_{i}"])


def annual(p):
    """Person-level sample for 1-year outcomes: employed at position 0, observed at 1, 3 and 4."""
    w = pairs(p, 0, 4)
    w = w[w["state_0"] != "N"].copy()
    emp0 = w[w["ing_x_hrs_0"] > 0]
    med = emp0.groupby("state_0").apply(lambda x: wmedian(x["ing_x_hrs_0"], x["fac_tri_0"]), include_groups=False)
    rank = med.rank(method="first").to_dict()
    w["exit_y"] = (w["state_4"] == "N").astype(float)
    w["persist_y"] = (w["state_4"] == w["state_0"]).astype(float)
    w["up_y"] = fl.upward(w["state_0"], w["state_4"], rank)
    w["sector"], w["sizeform"] = fl.parts(w["state_0"])
    w["exit_q"] = np.where(w["state_1"].isna(), np.nan, (w["state_1"] == "N").astype(float))
    w["confirmed"] = (w["state_1"] == w["state_0"]) & (w["state_3"] == w["state_4"])
    w["selfreport"] = w["proxy_0"] == False  # noqa: E712  (NaN when unknown)
    return w


def by_cell(w, col):
    g = w.groupby(col)
    out = pd.DataFrame({"n": g.size()})
    for y in ["exit_q", "exit_y", "persist_y", "up_y"]:
        out[y] = g.apply(lambda x: wavg(x[y].dropna(), x.loc[x[y].notna(), "fac_tri_0"]), include_groups=False)
    return out.reset_index()


def boot_decomp(w, y, nboot=NBOOT, seed=SEED):
    d = w.dropna(subset=[y])
    est = fl.decompose(d[y].to_numpy(float), d["sector"], d["sizeform"], d["fac_tri_0"].to_numpy(float))
    rng = np.random.default_rng(seed)
    d = d.reset_index(drop=True)
    idx = d.groupby(["ent_0", "psu_0"]).indices
    strata = {}
    for (e, _), ix in idx.items():
        strata.setdefault(e, []).append(ix)
    y_, w_ = d[y].to_numpy(float), d["fac_tri_0"].to_numpy(float)
    sec, sf = d["sector"].to_numpy(), d["sizeform"].to_numpy()
    diffs = []
    for _ in range(nboot):
        take = np.concatenate([np.concatenate([u[j] for j in rng.integers(0, len(u), len(u))])
                               for u in strata.values()])
        r = fl.decompose(y_[take], sec[take], sf[take], w_[take])
        diffs.append(r["shapley_sizeform"] - r["shapley_sector"])
    est.update({"n": len(d), "diff": est["shapley_sizeform"] - est["shapley_sector"],
                "diff_lo90": np.percentile(diffs, 5), "diff_hi90": np.percentile(diffs, 95)})
    return est


def misreport(p):
    """Employees with the same reported employer start date at two first-quarter visits (the only
    quarters with the start-date question): share whose size class or formality differs. With
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
                    & (w[f"p3r_anio_{i}"] == w[f"p3r_anio_{j}"]) & (w[f"p3r_mes_{i}"] == w[f"p3r_mes_{j}"])
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
    qr, cells, dec, mis = [], {"sector": [], "sizeform": [], "state_0": []}, [], []
    for win, f in files.items():
        p = prepare(pd.read_parquet(f))
        qr.append(quarterly_rates(p, win))
        w = annual(p)
        n0 = w["state_0"].value_counts()
        w["state_0"] = merge_small(w["state_0"], n0)
        w["sector"], w["sizeform"] = fl.parts(w["state_0"])
        for col in cells:
            cells[col].append(by_cell(w, col).assign(window=win))
        for variant, d in [("main", w), ("confirmed transitions", w[w["confirmed"]]),
                           ("self-reported only", w[w["selfreport"]])]:
            for y in ["exit_y", "up_y"]:
                if d[y].notna().sum() > 1000:
                    r = boot_decomp(d, y)
                    r.update({"window": win, "variant": variant, "outcome": y})
                    dec.append(r)
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
    print(dec.round(4).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
