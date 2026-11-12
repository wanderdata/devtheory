"""Relative prices and measured productivity by sector: how much of a sector's change in
relative productivity at current prices is a change in its relative price (D-043).

    LP_SCOPE=lac python empirics/code/lp/09_baumol.py

For sector i and the whole economy (official total value added), with nominal (current US$)
and real (constant 2020 US$) value added per worker, the identity

    p_i^nom / P^nom  =  (p_i^real / P^real)  x  (pi_i / pi)

holds exactly, where pi_i and pi are the implicit deflators (current / constant). Over a
period, the change in a sector's relative productivity at current prices splits exactly into
a real part and a relative-price part (log points per year):

    d_nom_pp = d_real_pp + d_price_pp

Baumol's cost-disease mechanism predicts that sectors with slow real productivity growth see
their relative prices rise, roughly one for one: across sectors, d_price falls with d_real
with a slope near -1. Section 2 of the report estimates that slope (pooled OLS, with a
bootstrap over countries for the interval). Mining and utilities are reported but kept out of
the slope: their relative prices are set by world commodity prices, not by cost disease.

Section 3 re-estimates the slope for grade-A country-periods between their anchoring survey
years, with survey and with modelled employment (OQ-59).

Outputs in empirics/output/<scope>_lp/baumol/: sectors.csv, slope.csv, slope_anchored.csv, results.md.
"""
import numpy as np
import pandas as pd

from config import COUNTRIES, INTERIM, OUTPUT, PERIODS, PROCESSED, SCOPE_NAME, SECTOR_ORDER, SECTORS
from empirics.common.countries import POOL_EXCLUDE_LAC, SHORT

OUT = OUTPUT / "baumol"
SEED = 20261112
NBOOT = 999


def load():
    p = pd.read_csv(PROCESSED / "panel_7sector.csv").set_index(["iso3", "year", "sector"])
    tot = {}
    for k in ["k2020", "cur"]:
        u = pd.read_csv(INTERIM / f"un_va_{k}_usd.csv")
        tot[k] = u[u["indicator"] == "Total Value Added"].set_index(["iso3", "year"])["value"]
    L = p["emp_model"].groupby(["iso3", "year"]).sum(min_count=7)
    return p, tot, L


def rel(p, tot, L, iso, yr, col="emp_model"):
    """Sector relative productivity at current and constant prices, and relative deflator.
    col selects the employment series (ILO modelled, or survey in survey years)."""
    s = p.loc[(iso, yr)].reindex(SECTOR_ORDER)
    Lt = L.loc[(iso, yr)] if col == "emp_model" else s[col].sum(min_count=7)
    Pn, Pr = tot["cur"].loc[(iso, yr)] / Lt, tot["k2020"].loc[(iso, yr)] / Lt
    nom = s["va_cur_usd"] / s[col] / Pn
    real = s["va_k2020usd"] / s[col] / Pr
    return nom, real, nom / real


def anchored(p, tot, L):
    """Grade-A country-periods (both endpoints within two years of a usable survey year, D-026):
    the split computed between the two survey years, once with survey employment and once with
    ILO modelled employment, on the same years. The relative-price term does not involve
    employment, so the two differ only in the real term (OQ-59)."""
    m = pd.read_csv(OUTPUT / "grid_A" / "main.csv")
    m = m[(m["grade"] == "A") & m["anchor_t0"].notna() & m["anchor_T"].notna()]
    rows = []
    for r in m.itertuples():
        a0, aT = int(r.anchor_t0), int(r.anchor_T)
        if aT <= a0:
            continue
        n = aT - a0
        for col, lab in [("emp_survey", "survey"), ("emp_model", "model")]:
            try:
                n0, r0, q0 = rel(p, tot, L, r.iso3, a0, col)
                nT, rT, qT = rel(p, tot, L, r.iso3, aT, col)
            except KeyError:
                continue
            if pd.concat([r0, rT, q0, qT]).isna().any():
                continue
            for sec in SECTOR_ORDER:
                rows.append({"iso3": r.iso3, "period": r.period, "a0": a0, "aT": aT, "employment": lab,
                             "sector": sec, "d_real_pp": 100 * np.log(rT[sec] / r0[sec]) / n,
                             "d_price_pp": 100 * np.log(qT[sec] / q0[sec]) / n})
    d = pd.DataFrame(rows)
    if d.empty:
        return d
    keep = d.groupby(["iso3", "period"])["employment"].nunique()
    keep = keep[keep == 2].index
    return d.set_index(["iso3", "period"]).loc[keep].reset_index()


def sectors(p, tot, L):
    rows = []
    for iso in COUNTRIES:
        for t0, T in PERIODS:
            n = T - t0
            try:
                n0, r0, q0 = rel(p, tot, L, iso, t0)
                nT, rT, qT = rel(p, tot, L, iso, T)
            except KeyError:
                continue
            if pd.concat([n0, nT, r0, rT]).isna().any():
                continue
            s0 = p.loc[(iso, t0)].reindex(SECTOR_ORDER)["emp_model"]
            s0 = s0 / s0.sum()
            for sec in SECTOR_ORDER:
                rows.append({"iso3": iso, "country": SHORT[iso], "period": f"{t0}–{T}", "sector": sec,
                             "emp_share0": s0[sec], "rel_nom0": n0[sec], "rel_nomT": nT[sec],
                             "rel_real0": r0[sec], "rel_realT": rT[sec],
                             "d_nom_pp": 100 * np.log(nT[sec] / n0[sec]) / n,
                             "d_real_pp": 100 * np.log(rT[sec] / r0[sec]) / n,
                             "d_price_pp": 100 * np.log(qT[sec] / q0[sec]) / n,
                             "low0": bool(n0[sec] < 1)})
    return pd.DataFrame(rows)


def slope(d, seed=SEED, nboot=NBOOT):
    """OLS slope of d_price on d_real, with a country-cluster bootstrap 90% interval."""
    def b(x):
        X = np.column_stack([np.ones(len(x)), x["d_real_pp"]])
        return np.linalg.lstsq(X, x["d_price_pp"].to_numpy(), rcond=None)[0][1]
    est = b(d)
    rng = np.random.default_rng(seed)
    groups = {k: g for k, g in d.groupby("iso3")}
    keys = list(groups)
    draws = [b(pd.concat([groups[k] for k in rng.choice(keys, len(keys))])) for _ in range(nboot)]
    return est, np.percentile(draws, 5), np.percentile(draws, 95)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p, tot, L = load()
    d = sectors(p, tot, L)
    d.to_csv(OUT / "sectors.csv", index=False)
    excl = [c for c in POOL_EXCLUDE_LAC if c in COUNTRIES]
    base = d[(d["sector"] != "MIU") & ~d["iso3"].isin(excl)]
    srows = []
    for per in [f"{a}–{b}" for a, b in PERIODS]:
        x = base[base["period"] == per]
        if x["iso3"].nunique() >= 5:
            e, lo, hi = slope(x)
            srows.append({"period": per, "n_obs": len(x), "n_countries": x["iso3"].nunique(),
                          "slope": e, "ci90_lo": lo, "ci90_hi": hi,
                          "corr": np.corrcoef(x["d_real_pp"], x["d_price_pp"])[0, 1]})
    sl = pd.DataFrame(srows)
    sl.to_csv(OUT / "slope.csv", index=False)

    an = anchored(p, tot, L)
    arows = []
    if not an.empty:
        an = an[(an["sector"] != "MIU") & ~an["iso3"].isin(excl)]
        for per in [f"{a}–{b}" for a, b in PERIODS]:
            for lab in ["model", "survey"]:
                x = an[(an["period"] == per) & (an["employment"] == lab)]
                if x["iso3"].nunique() >= 5:
                    e, lo, hi = slope(x)
                    arows.append({"period": per, "employment": lab, "n_obs": len(x), "n_countries": x["iso3"].nunique(),
                                  "slope": e, "ci90_lo": lo, "ci90_hi": hi,
                                  "sd_real": x["d_real_pp"].std()})
    asl = pd.DataFrame(arows)
    asl.to_csv(OUT / "slope_anchored.csv", index=False)

    L_ = [f"# Relative prices and measured productivity by sector — {SCOPE_NAME}", "",
          "*Generated by `empirics/code/lp/09_baumol.py`; do not edit by hand (D-043).*", "",
          "Change in each sector's productivity relative to the economy-wide average, at current "
          "prices, split exactly into a real part (constant 2020 prices) and a relative-price part. "
          "Log points per year; ILO modelled employment; official total value added as the denominator.", "",
          "## 1. Low-productivity sectors, 2000–2019: medians across countries"
          + (f" (excluding {', '.join(SHORT[c] for c in excl)})" if excl else ""), "",
          "Sectors whose value added per worker at current prices was below the economy-wide "
          "average in 2000.", "",
          "| Sector | Countries | Relative productivity, current prices | = real | + relative price |",
          "|---|---|---|---|---|"]
    y = d[(d["period"] == "2000–2019") & d["low0"] & ~d["iso3"].isin(excl)]
    for sec in SECTOR_ORDER:
        z = y[y["sector"] == sec]
        if len(z):
            L_.append(f"| {SECTORS[sec]} | {len(z)} | {z['d_nom_pp'].median():+.2f} | "
                      f"{z['d_real_pp'].median():+.2f} | {z['d_price_pp'].median():+.2f} |")
    L_ += ["", "Medians of each column are taken separately, so they need not add up.", "",
           "## 2. Baumol slope: relative-price change on real relative-productivity change", "",
           "Pooled across countries and sectors (mining and utilities excluded). Cost disease "
           "predicts a slope near −1.", "",
           "| Period | Observations | Countries | Slope | 90% interval (country bootstrap) | Correlation |",
           "|---|---|---|---|---|---|"]
    for _, r in sl.iterrows():
        L_.append(f"| {r.period} | {r.n_obs} | {r.n_countries} | {r.slope:+.2f} | "
                  f"[{r.ci90_lo:+.2f}, {r.ci90_hi:+.2f}] | {r['corr']:+.2f} |")
    if len(asl):
        L_ += ["", "## 3. Same slope between survey years, survey versus modelled employment (grade A only)", "",
               "Each grade-A country-period recomputed between its two anchoring survey years, with survey "
               "employment and with ILO modelled employment for the same years. The relative-price term is the "
               "same in both; only the real term changes.", "",
               "| Period | Employment | Observations | Countries | Slope | 90% interval | SD of real term |",
               "|---|---|---|---|---|---|---|"]
        for _, r in asl.iterrows():
            L_.append(f"| {r.period} | {r.employment} | {r.n_obs} | {r.n_countries} | {r.slope:+.2f} | "
                      f"[{r.ci90_lo:+.2f}, {r.ci90_hi:+.2f}] | {r.sd_real:.2f} |")
    L_ += ["", "Measurement error pulls the slope in both directions. An error in a sector's employment "
           "moves its real and nominal relative productivity together and leaves the relative-price "
           "term unchanged, so it biases the slope toward zero. An error in a sector's deflator moves "
           "the real and relative-price terms in opposite directions and biases the slope toward −1 "
           "(OQ-59)."]
    (OUT / "results.md").write_text("\n".join(L_) + "\n")
    print(f"{SCOPE_NAME}: {len(d)} sector-periods; slopes {sl['slope'].round(2).tolist()}")


if __name__ == "__main__":
    main()
