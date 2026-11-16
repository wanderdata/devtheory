"""Study 9.7, step 3: productivity growth, decomposition and the tests of P41 and P42
(pre-analysis plan §§3.1-3.3, 3.5, 4, 5; addendum A1).

    python empirics/code/enoe/state_productivity/03_estimates.py [--reps 199]

Period values are averages over the years of a period (P0 = 2005-2007, P1 = 2017-2019,
P2 = 2022-2024). ENOE quantities for a period are built from PSU-level quarterly aggregates
(02_panel.py) summed over the period and divided by its number of quarters; unspecified industry
codes are distributed within state, period and segment. The bootstrap resamples PSUs with replacement
within state and period (one draw per period, so that the rotating panel's repeated PSUs move
together), 199 replications; PIBE and MEITEF are treated as fixed.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1]))

from activities import FINE, MAIN, MEITEF, distribute  # noqa: E402
from enoe_config import INTERIM  # noqa: E402

ROOT = HERE.parents[4]
OUT = ROOT / "empirics" / "output" / "enoe" / "state_productivity"
TMP = INTERIM / "state_productivity"
PERIODS = {"P0": [2005, 2006, 2007], "P1": [2017, 2018, 2019], "P2": [2022, 2023, 2024]}
YEARS_BETWEEN = {("P0", "P1"): 12, ("P1", "P2"): 5, ("P0", "P2"): 17}
CASES = {"Bajío": [1, 11, 22, 24], "Oil states": [4, 27], "Quintana Roo": [23]}
UNIT31 = {15: 9}  # State of Mexico combined with Mexico City
UNIT_NAME = {9: "CDMX and Méx"}
SEED = 9701


# ----------------------------------------------------------------------------------- inputs
def period_of(year):
    for p, ys in PERIODS.items():
        if year in ys:
            return p
    return None


def load():
    panel = pd.read_csv(OUT / "panel_fine.csv")
    mei = pd.read_csv(OUT / "meitef_informal.csv")
    psu = pd.read_parquet(TMP / "psu_cells.parquet")
    psu["period"] = psu["year"].map(period_of)
    psu = psu[psu["period"].notna()]
    nq = psu.groupby("period")[["year", "q"]].apply(lambda g: len(g.drop_duplicates())).to_dict()
    psu = psu.groupby(["period", "ent", "upm", "act", "seg"], as_index=False)[["w", "wh", "wy", "n"]].sum()
    mss = pd.read_parquet(TMP / "mining_services.parquet")
    mss["period"] = mss["year"].map(period_of)
    mss = mss[mss["period"].notna()].groupby(["period", "ent", "seg"], as_index=False)["w_mss"].sum()
    mss["w_mss"] /= mss["period"].map(nq)
    pop = pd.read_parquet(TMP / "population_psu.parquet")
    pop["period"] = pop["year"].map(period_of)
    pop = pop[pop["period"].notna()].groupby(["period", "ent", "upm"], as_index=False)["pop"].sum()
    return panel, mei, psu, nq, mss, pop


def pibe_periods(panel):
    p = panel.copy()
    p["period"] = p["year"].map(period_of)
    p = p[p["period"].notna()]
    return p.groupby(["period", "ent", "act"], as_index=False)[["va_k", "va_c"]].mean()


def meitef_periods(mei):
    m = mei.copy()
    m["period"] = m["year"].map(period_of)
    m = m[m["period"].notna()]
    return m.groupby(["period", "ent", "meitef_act"], as_index=False)[["iva_k", "iva_c"]].mean()


def enoe_periods(psu, nq, factor=None):
    d = psu
    if factor is not None:
        d = d.merge(factor, on=["period", "ent", "upm"])
        d = d.assign(w=d["w"] * d["f"], wh=d["wh"] * d["f"], wy=d["wy"] * d["f"], n=d["n"] * d["f"])
    a = d.groupby(["period", "ent", "act", "seg"], as_index=False)[["w", "wh", "wy", "n"]].sum()
    for c in ("w", "wh", "wy"):
        a[c] = a[c] / a["period"].map(nq)
    a = distribute(a, ["period", "ent", "seg"], ["w", "wh", "wy", "n"])
    a = a.pivot_table(index=["period", "ent", "act"], columns="seg", values=["w", "wh", "wy", "n"], fill_value=0)
    a.columns = [{"w": "emp", "wh": "hrs", "wy": "inc", "n": "n"}[v] + "_" + s for v, s in a.columns]
    return a.reset_index()


def boot_factor(pop, rng):
    """Replicate factors: PSUs drawn with replacement within state and period, then the factors are
    ratio-calibrated so that each replicate reproduces the state's weighted population aged 15+ in the
    period (D-067), as ENOE's weights are calibrated to population totals."""
    u = pop.sort_values(["period", "ent", "upm"]).reset_index(drop=True)
    sizes = u.groupby(["period", "ent"], sort=False).size().values
    f = np.concatenate([rng.multinomial(k, np.full(k, 1.0 / k)) for k in sizes]).astype(float)
    tot = u.groupby(["period", "ent"])["pop"].transform("sum")
    rep = (u["pop"] * f).groupby([u["period"], u["ent"]]).transform("sum")
    return u.assign(f=f * tot / rep)[["period", "ent", "upm", "f"]]


def half_factor(pop, half):
    """Split-sample factors: PSUs in one half (by a stable hash of the PSU code), calibrated to state
    population, so that two halves give independent estimates."""
    import zlib
    u = pop.copy()
    u["h"] = u["upm"].map(lambda x: zlib.crc32(x.encode()) % 2)
    tot = u.groupby(["period", "ent"])["pop"].transform("sum")
    sel = (u["h"] == half).astype(float)
    rep = (u["pop"] * sel).groupby([u["period"], u["ent"]]).transform("sum")
    return u.assign(f=sel * tot / rep)[["period", "ent", "upm", "f"]]


# ------------------------------------------------------------------------------ cell table
def cells(enoe, pibe, meit, units="31", cls="main", market=False, prices="2018", split="meitef",
          mss=None):
    """Cell table by period, unit and group with va (total, formal, informal), labour (persons or hours
    by segment) and the count of informal value added capped at total value added."""
    c = pibe.merge(enoe, on=["period", "ent", "act"], how="left").fillna(0)
    if mss is not None:  # robustness: workers in mining support services removed from non-oil mining
        m = mss.pivot_table(index=["period", "ent"], columns="seg", values="w_mss", fill_value=0)
        m.columns = ["mss_" + s for s in m.columns]
        c = c.merge(m.reset_index(), on=["period", "ent"], how="left").fillna(0)
        sel = c["act"] == "21np"
        for s in ("f", "i"):
            share = (c.loc[sel, "mss_" + s] / c.loc[sel, "emp_" + s].replace(0, np.nan)).fillna(0).clip(0, 1)
            c.loc[sel, "emp_" + s] -= c.loc[sel, "mss_" + s].clip(upper=c.loc[sel, "emp_" + s])
            c.loc[sel, "hrs_" + s] *= 1 - share
    c["va_2018"] = c["va_k"]
    if prices == "P0":  # value added of every period at 2005-2007 prices, cell by cell
        base = pibe[pibe["period"] == "P0"].set_index(["ent", "act"])
        defl = (base["va_c"] / base["va_k"]).rename("defl").reset_index()
        c = c.merge(defl, on=["ent", "act"], how="left")
        c["va_k"] = c["va_k"] * c["defl"].fillna(1)
    if market:
        c = c[~c["act"].isin(["53", "93"])]
    if cls == "main":
        inv = {f: g for g, fs in MAIN.items() for f in fs}
        c["group"] = c["act"].map(inv)
    else:
        c["group"] = c["act"]
    c["meitef_act"] = c["act"].map({f: g for g, fs in MEITEF.items() for f in fs})
    num = ["va_k", "va_2018", "emp_f", "emp_i", "hrs_f", "hrs_i", "inc_f", "inc_i", "n_f", "n_i"]
    # informal value added: MEITEF's, divided among the groups that share a MEITEF activity in
    # proportion to ENOE informal labour income (employment where no income is reported)
    g = c.groupby(["period", "ent", "meitef_act", "group"], as_index=False)[num].sum()
    if split == "meitef":
        base = np.where(g["inc_i"] > 0, g["inc_i"], g["emp_i"])
        tot = pd.Series(base).groupby([g["period"], g["ent"], g["meitef_act"]]).transform("sum").values
        g["alloc"] = np.divide(base, tot, out=np.zeros(len(g)), where=tot > 0)
        g = g.merge(meit, on=["period", "ent", "meitef_act"], how="left")
        g["iva"] = g["alloc"] * g["iva_k"].fillna(0) * (g["va_k"] / g["va_2018"].replace(0, np.nan)).fillna(1)
    else:  # theta = 1: value added split by the labour-income shares of the segments (study 9.3)
        t = (g["inc_f"] + g["inc_i"]).replace(0, np.nan)
        g["iva"] = (g["va_k"] * g["inc_i"] / t).fillna(0)
    g = g.groupby(["period", "ent", "group"], as_index=False)[num + ["iva"]].sum()
    g["capped"] = (g["iva"] > g["va_k"]).astype(int)
    g["va_i"] = np.minimum(g["iva"], g["va_k"])
    g["va_f"] = g["va_k"] - g["va_i"]
    g["unit"] = g["ent"].replace(UNIT31) if units == "31" else g["ent"]
    keep = ["va_k", "va_f", "va_i", "emp_f", "emp_i", "hrs_f", "hrs_i", "inc_f", "inc_i", "n_f", "n_i", "capped"]
    return g.groupby(["period", "unit", "group"], as_index=False)[keep].sum()


# ---------------------------------------------------------------------------- decomposition
def _terms(L0, Y0, L1, Y1):
    """Within, static and dynamic terms (levels) for cells with labour L and value added Y."""
    L0, Y0, L1, Y1 = (np.asarray(x, float) for x in (L0, Y0, L1, Y1))
    keep = (L0 > 0) | (L1 > 0)
    L0, Y0, L1, Y1 = L0[keep], Y0[keep], L1[keep], Y1[keep]
    p0 = np.divide(Y0, L0, out=np.full_like(Y0, np.nan), where=L0 > 0)
    p1 = np.divide(Y1, L1, out=np.full_like(Y1, np.nan), where=L1 > 0)
    p0 = np.where(np.isnan(p0), p1, p0)
    p1 = np.where(np.isnan(p1), p0, p1)
    s0, s1 = L0 / L0.sum(), L1 / L1.sum()
    W = np.sum(s0 * (p1 - p0))
    S = np.sum(p0 * (s1 - s0))
    D = np.sum((p1 - p0) * (s1 - s0))
    P0, P1 = Y0.sum() / L0.sum(), Y1.sum() / L1.sum()
    return P0, P1, W, S, D


def decompose(cell, a="P0", b="P1", labour="emp"):
    """Per unit: annual log growth of non-oil productivity split into within, static, dynamic and,
    at segment level, formalisation (segment-level reallocation minus activity-level reallocation)."""
    yrs = YEARS_BETWEEN[(a, b)]
    x0 = cell[cell["period"] == a].set_index(["unit", "group"])
    x1 = cell[cell["period"] == b].set_index(["unit", "group"])
    idx = x0.index.union(x1.index)
    x0, x1 = x0.reindex(idx).fillna(0), x1.reindex(idx).fillna(0)
    rows = []
    for u in idx.get_level_values(0).unique():
        c0, c1 = x0.loc[u], x1.loc[u]
        L0 = c0[labour + "_f"] + c0[labour + "_i"]
        L1 = c1[labour + "_f"] + c1[labour + "_i"]
        P0, P1, W, S, D = _terms(L0, c0["va_k"], L1, c1["va_k"])
        sL0 = np.concatenate([c0[labour + "_f"], c0[labour + "_i"]])
        sL1 = np.concatenate([c1[labour + "_f"], c1[labour + "_i"]])
        _, _, Ws, Ss, Ds = _terms(sL0, np.concatenate([c0["va_f"], c0["va_i"]]), sL1,
                                  np.concatenate([c1["va_f"], c1["va_i"]]))
        g = np.log(P1 / P0) / yrs
        k = g / (P1 - P0)
        rows.append({"unit": u, "P0": P0, "P1": P1, "growth": g, "within": W * k, "static": S * k,
                     "dynamic": D * k, "realloc": (S + D) * k, "within_seg": Ws * k,
                     "formalisation": ((Ss + Ds) - (S + D)) * k,
                     "formal_share_0": c0[labour + "_f"].sum() / L0.sum() if labour == "emp" else np.nan,
                     "formal_share_1": c1[labour + "_f"].sum() / L1.sum() if labour == "emp" else np.nan})
    r = pd.DataFrame(rows)
    r["d_formal_share"] = r["formal_share_1"] - r["formal_share_0"]
    return r


def national_contributions(cell, a="P0", b="P1"):
    """Contribution of each unit x group cell (within + static + dynamic) to national growth."""
    yrs = YEARS_BETWEEN[(a, b)]
    x0 = cell[cell["period"] == a].set_index(["unit", "group"])
    x1 = cell[cell["period"] == b].set_index(["unit", "group"])
    idx = x0.index.union(x1.index)
    x0, x1 = x0.reindex(idx).fillna(0), x1.reindex(idx).fillna(0)
    L0, L1 = x0["emp_f"] + x0["emp_i"], x1["emp_f"] + x1["emp_i"]
    p0 = (x0["va_k"] / L0.replace(0, np.nan))
    p1 = (x1["va_k"] / L1.replace(0, np.nan))
    p0, p1 = p0.fillna(p1), p1.fillna(p0)
    s0, s1 = L0 / L0.sum(), L1 / L1.sum()
    P0, P1 = x0["va_k"].sum() / L0.sum(), x1["va_k"].sum() / L1.sum()
    k = np.log(P1 / P0) / yrs / (P1 - P0)
    out = pd.DataFrame({"within": s0 * (p1 - p0) * k, "static": p0 * (s1 - s0) * k,
                        "dynamic": (p1 - p0) * (s1 - s0) * k, "emp_share_0": s0, "emp_share_1": s1,
                        "prod_rel_0": p0 / P0, "prod_growth": np.log(p1 / p0) / yrs})
    out["total"] = out[["within", "static", "dynamic"]].sum(axis=1)
    return out.reset_index(), np.log(P1 / P0) / yrs


# ------------------------------------------------------------------------------------ tests
def p41(dec, lo, hi):
    d = dec.merge(pd.DataFrame({"unit": lo.index, "lo": lo.values, "hi": hi.values}), on="unit")
    elig = d[(d["growth"] > 0) & (d["lo"] > 0)]
    n = len(elig)
    k = int((elig["within"] > elig["realloc"]).sum())
    share = k / n if n else np.nan
    verdict = "Supported" if share >= 2 / 3 else ("Rejected" if share < 1 / 3 else "Inconclusive")
    return {"eligible_units": n, "within_exceeds_realloc": k, "share": share, "verdict": verdict,
            "units_positive_growth": int((d["growth"] > 0).sum())}


def partial_spearman(x, y, z):
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    ex = rx - np.polyval(np.polyfit(rz, rx, 1), rz)
    ey = ry - np.polyval(np.polyfit(rz, ry, 1), rz)
    return np.corrcoef(ex, ey)[0, 1]


def p42(dec, B=1999, seed=SEED):
    x, y, z = dec["growth"].values, dec["d_formal_share"].values, np.log(dec["P0"].values)
    rho = spearmanr(x, y)[0]
    prt = partial_spearman(x, y, z)
    rng = np.random.default_rng(seed)
    bs, bp = [], []
    n = len(x)
    for _ in range(B):
        i = rng.integers(0, n, n)
        bs.append(spearmanr(x[i], y[i])[0])
        bp.append(partial_spearman(x[i], y[i], z[i]))
    lo, hi = np.nanpercentile(bs, [5, 95])
    plo, phi = np.nanpercentile(bp, [5, 95])
    verdict = "Supported" if lo > 0 else ("Rejected" if rho < 0.1 else "Inconclusive")
    return {"rho": rho, "lo": lo, "hi": hi, "partial_rho": prt, "partial_lo": plo, "partial_hi": phi,
            "units": n, "verdict": verdict}


# ------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=199)
    a = ap.parse_args()
    panel, mei, psu, nq, mss, pop = load()
    pibe, meit = pibe_periods(panel), meitef_periods(mei)
    enoe = enoe_periods(psu, nq)

    base = cells(enoe, pibe, meit)
    dec = decompose(base)

    # bootstrap of ENOE sampling error
    rng = np.random.default_rng(SEED)
    reps = []
    for r in range(a.reps):
        e = enoe_periods(psu, nq, boot_factor(pop, rng))
        d = decompose(cells(e, pibe, meit))
        d["rep"] = r
        reps.append(d)
        if r % 20 == 0:
            print("replication", r, flush=True)
    reps = pd.concat(reps, ignore_index=True)
    reps.to_csv(TMP / "bootstrap_decomposition.csv", index=False)
    q = reps.groupby("unit")[["growth", "within", "realloc", "formalisation", "d_formal_share"]].quantile([0.05, 0.95])
    lo, hi = q.xs(0.05, level=1), q.xs(0.95, level=1)
    dec = dec.merge(lo.add_suffix("_lo"), left_on="unit", right_index=True).merge(
        hi.add_suffix("_hi"), left_on="unit", right_index=True)
    dec.to_csv(OUT / "decomposition_units.csv", index=False, float_format="%.6f")

    res41 = p41(dec, lo["growth"], hi["growth"])
    # stability of the P41 outcome across replications
    stab = []
    for r, d in reps.groupby("rep"):
        e = d[(d["growth"] > 0)].merge(lo["growth"].rename("lo").reset_index(), on="unit")
        e = e[e["lo"] > 0]
        stab.append((e["within"] > e["realloc"]).mean() if len(e) else np.nan)
    res41["share_boot_lo"], res41["share_boot_hi"] = np.nanpercentile(stab, [5, 95])
    res42 = p42(dec)
    # post-plan check (D-067): growth and the change in the formal share from independent halves
    dh = [decompose(cells(enoe_periods(psu, nq, half_factor(pop, h)), pibe, meit)) for h in (0, 1)]
    split = [spearmanr(dh[0]["growth"], dh[1]["d_formal_share"])[0],
             spearmanr(dh[1]["growth"], dh[0]["d_formal_share"])[0]]
    same = [spearmanr(dh[h]["growth"], dh[h]["d_formal_share"])[0] for h in (0, 1)]
    res42.update({"split_rho_a": split[0], "split_rho_b": split[1], "same_half_rho_a": same[0],
                  "same_half_rho_b": same[1]})
    reps_rho = reps.groupby("rep")[["growth", "d_formal_share"]].apply(
        lambda g: spearmanr(g["growth"], g["d_formal_share"])[0])
    res42["sampling_err_corr_median"] = reps.groupby("unit")[["growth", "d_formal_share"]].apply(
        lambda g: np.corrcoef(g["growth"], g["d_formal_share"])[0, 1]).median()
    res42["replicate_rho_median"] = reps_rho.median()

    # robustness
    specs = {"main": {}, "hours": {"labour": "hrs"}, "fine classification": {"cls": "fine"},
             "32 states": {"units": "32"}, "market economy": {"market": True},
             "2005-2007 prices": {"prices": "P0"}, "mining support services excluded": {"mss": mss},
             "theta = 1 split (study 9.3)": {"split": "theta1"}}
    rob = []
    for name, sp in specs.items():
        lab = sp.pop("labour", "emp")
        c = cells(enoe, pibe, meit, **sp)
        d = decompose(c, labour=lab)
        dd = d.merge(dec[["unit", "growth_lo"]], on="unit", how="left") if name != "32 states" else d.assign(
            growth_lo=np.nan)
        pos = dd[dd["growth"] > 0]
        elig = pos[pos["growth_lo"] > 0] if name != "32 states" else pos
        r42 = p42(d, B=999) if lab == "emp" else {"rho": np.nan, "lo": np.nan, "hi": np.nan}
        rob.append({"specification": name, "units": len(d), "units_positive": len(pos),
                    "p41_share_within_exceeds": (elig["within"] > elig["realloc"]).mean(),
                    "p41_eligible": len(elig), "median_growth": d["growth"].median(),
                    "median_within": d["within"].median(), "median_realloc": d["realloc"].median(),
                    "median_formalisation": d["formalisation"].median(),
                    "p42_rho": r42["rho"], "p42_lo": r42["lo"], "p42_hi": r42["hi"],
                    "capped_cells": int(c["capped"].sum())})
    # later period, descriptive
    d2 = decompose(base, "P1", "P2")
    d2.to_csv(OUT / "decomposition_units_2017_2024.csv", index=False, float_format="%.6f")
    rob.append({"specification": "2017-2019 to 2022-2024 (descriptive)", "units": len(d2),
                "units_positive": int((d2["growth"] > 0).sum()), "p41_share_within_exceeds": np.nan,
                "p41_eligible": np.nan, "median_growth": d2["growth"].median(),
                "median_within": d2["within"].median(), "median_realloc": d2["realloc"].median(),
                "median_formalisation": d2["formalisation"].median(), "p42_rho": spearmanr(
                    d2["growth"], d2["d_formal_share"])[0], "p42_lo": np.nan, "p42_hi": np.nan,
                "capped_cells": int(base["capped"].sum())})
    pd.DataFrame(rob).to_csv(OUT / "robustness.csv", index=False, float_format="%.6f")

    # national contributions, P0 -> P1
    contrib, g_nat = national_contributions(base)
    contrib.to_csv(OUT / "national_contributions.csv", index=False, float_format="%.6f")
    nat = decompose(base.assign(unit=0).groupby(["period", "unit", "group"], as_index=False).sum(numeric_only=True))
    nat_seg = nat.iloc[0].to_dict()

    # unit x group detail for the fastest and slowest units and the named cases
    x0 = base[base["period"] == "P0"].set_index(["unit", "group"])
    x1 = base[base["period"] == "P1"].set_index(["unit", "group"])
    det = pd.DataFrame({"va0": x0["va_k"], "va1": x1["va_k"], "emp0": x0["emp_f"] + x0["emp_i"],
                        "emp1": x1["emp_f"] + x1["emp_i"],
                        "formal0": x0["emp_f"] / (x0["emp_f"] + x0["emp_i"]),
                        "formal1": x1["emp_f"] / (x1["emp_f"] + x1["emp_i"])}).reset_index()
    det.to_csv(OUT / "unit_group_detail.csv", index=False, float_format="%.6f")

    tests = pd.DataFrame([{"proposition": "P41", **res41}, {"proposition": "P42", **res42}])
    tests.to_csv(OUT / "tests_p41_p42.csv", index=False, float_format="%.6f")
    pd.DataFrame([{"national_growth": g_nat, **{k: nat_seg[k] for k in
                                                 ["within", "static", "dynamic", "formalisation", "within_seg"]},
                   "formal_share_0": nat_seg["formal_share_0"], "formal_share_1": nat_seg["formal_share_1"]}]).to_csv(
        OUT / "national.csv", index=False, float_format="%.6f")
    print(tests.T)


if __name__ == "__main__":
    main()
