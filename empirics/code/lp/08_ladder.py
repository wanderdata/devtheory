"""Output per working-age person and the productivity ladder (D-042, D-043).

    LP_SCOPE=lac python empirics/code/lp/08_ladder.py

Working-age population W = persons aged 15+ (ILO modelled employment divided by the ILO
employment-to-population ratio; both refer to ages 15+, so the two are consistent).
Output Y = total value added of the seven sectors, valued at the initial-year prices of each
period, as in the main decomposition (D-024, D-035).

1. Terms (terms.csv). For each fixed period, growth of Y/W in log points per year, split
       ln(Y/W) = ln(Y/L) + ln(L/W)
   with ln(Y/L) divided between the within-sector and structural-change terms of
   05_decompose.py in proportion to their linear values (so the parts add up exactly).
   Two further terms are reported beside, not inside, the volume measure:
     demog_pp  ln(W/N), the working-age share of the population; N from ILOSTAT
               POP_2POP_SEX_NB_A (UN estimates) when present, otherwise PWT 11.0 (to 2023);
     tot_pp    the trading gain from the terms of trade: real gross domestic income over real
               GDP, with exports deflated by the import price deflator (SNA 2008 approach),
               prices relative to 2020. Positive when export prices rose relative to import
               prices. tot_avg_pp deflates the trade balance by the average of the export
               and import deflators instead (OQ-62).
2. Horizon statistics (horizon.csv). For every window of h = 1, 5, 10, 20 years, the annual
   log growth of Y/L and of L/W (official total value added at constant 2020 prices),
   pooled across countries: how often the two move in opposite directions, how often the
   employment-rate term is larger, and its share of the variance of growth of Y/W.
4. Frontier (frontier.csv): share of the 15+ population working in sectors at or above 25%
   and 50% of US output per worker, at PPP (one 2020 price-level factor per country, PWT).
3. Ladders (ladders.csv), verdicts (verdicts.csv) and incidence curves (incidence.csv) for
   each fixed period, at initial- and final-year prices. The zero block (persons aged 15+
   not employed) is split into unemployed and outside the labour force. A 65+ block needs
   employment aged 65+, which the ILO bulk files do not provide (D-044); terms.csv reports
   the share of the 15+ population aged 65+ (WDI SP.POP.65UP.TO.ZS) as context.

Verdict (per period): 'improvement' if the later ladder first-order dominates at both price
bases; 'improvement, weighting the lower percentiles' if it second-order dominates at both;
'deterioration' and its weighted form likewise; 'ambiguous' if the ladders cross; 'depends on
prices' if the two bases disagree. Threshold indices use z = output per employed worker at
the start of the period (and z/2), at the same prices.
"""
import numpy as np
import pandas as pd

import ladder as lad
from config import COUNTRIES, INTERIM, OUTPUT, PERIODS, PROCESSED, SCOPE_NAME, SECTOR_ORDER, SOURCE
from decompose import GRID_A, decompose, va_at_prices
from empirics.common.countries import POOL_EXCLUDE_LAC, SHORT

OUT = OUTPUT / "ladder"
HORIZONS = [1, 5, 10, 20]
BASES = ["initial", "final"]
VERDICT_ORDER = ["improvement", "improvement, weighting the lower percentiles", "ambiguous",
                 "deterioration, weighting the lower percentiles", "deterioration", "depends on prices"]


# ------------------------------------------------------------------ data ---

def load():
    p = pd.read_csv(PROCESSED / "panel_7sector.csv")
    va = p.dropna(subset=["va_cur_usd", "va_k2020usd"]).set_index(["iso3", "year", "sector"])[["va_cur_usd", "va_k2020usd"]]
    emp = p.dropna(subset=["emp_model"]).set_index(["iso3", "year", "sector"])["emp_model"]
    lab = pd.read_csv(INTERIM / "ilo_labour.csv").pivot_table(index=["iso3", "year"], columns="indicator", values="value")
    un = {}
    for k in ["k2020", "cur"]:
        u = pd.read_csv(INTERIM / f"un_va_{k}_usd.csv")
        un[k] = u.pivot_table(index=["iso3", "year"], columns="indicator", values="value")
    return va, emp, lab, un


def population(lab):
    """Total population (thousands): ILO/UN estimates if extracted, else PWT 11.0."""
    if "pop_total" in lab.columns:
        return lab["pop_total"].dropna(), "ILOSTAT POP_2POP_SEX_NB_A (UN estimates)"
    pwt = pd.read_excel(SOURCE / "pwt" / "pwt110.xlsx", sheet_name="Data", usecols=["countrycode", "year", "pop"])
    pwt = pwt[pwt["countrycode"].isin(COUNTRIES)].dropna()
    return pwt.set_index(["countrycode", "year"])["pop"].rename_axis(["iso3", "year"]) * 1000, "PWT 11.0"


def working_age(emp, lab):
    """W (thousands, 15+), employed L, and the zero-block split, by country-year."""
    L = emp.groupby(["iso3", "year"]).sum(min_count=7)
    d = pd.DataFrame({"L": L}).join(lab, how="inner").dropna(subset=["emp_rate"])
    d["W"] = d["L"] / (d["emp_rate"] / 100)
    if {"part_rate", "unemp_rate"} <= set(d.columns):
        d["unemp"] = d["W"] * d["part_rate"] / 100 * d["unemp_rate"] / 100
    else:
        d["unemp"] = np.nan
    d["notemp"] = d["W"] - d["L"]
    if {"pop_65plus", "emp_65plus"} <= set(d.columns):
        # share of the 15+ population that is 65+ and not employed, applied to the model W
        d["old_notemp"] = d["W"] * (d["pop_65plus"] - d["emp_65plus"]) / d["pop_15plus"]
    else:
        d["old_notemp"] = np.nan
    return d


def trading_gain_ratio(un, deflator="import"):
    """Real GDI / real GDP (both at 2020 prices). The trade balance at current prices is deflated
    by the import price deflator (default) or by the average of the export and import deflators
    (OQ-62); real GDP deflates exports and imports by their own deflators."""
    k, c = un["k2020"], un["cur"]
    X, M, Y = "Exports of goods and services", "Imports of goods and services", "Gross Domestic Product (GDP)"
    if not {X, M, Y} <= set(k.columns):
        return pd.Series(dtype=float)
    px, pm = c[X] / k[X], c[M] / k[M]
    p = pm if deflator == "import" else (px + pm) / 2
    gain = (c[X] - c[M]) / p - (k[X] - k[M])
    return ((k[Y] + gain) / k[Y]).dropna()


# ------------------------------------------------------------- 1. terms ---

def terms(va, emp, wa, pop, tgr, tgr_avg, grades, lab65):
    rows = []
    for iso in COUNTRIES:
        for t0, T in PERIODS:
            n = T - t0
            try:
                y = va_at_prices(va, iso, t0, T, "initial", GRID_A)
                l0, lT = emp.loc[(iso, t0)], emp.loc[(iso, T)]
                w0, wT = wa.loc[(iso, t0)], wa.loc[(iso, T)]
            except KeyError:
                continue
            r = decompose(y, l0, lT, n)
            if r is None:
                continue
            prod = 100 * np.log(r["PT"] / r["P0"]) / n
            lin = r["within_pp"] + r["struct_pp"]
            k = prod / lin if abs(lin) > 1e-12 else 0.0
            emprate = 100 * np.log((wT["L"] / wT["W"]) / (w0["L"] / w0["W"])) / n
            row = {
                "iso3": iso, "country": SHORT[iso], "period": f"{t0}–{T}", "t0": t0, "T": T,
                "grade": grades.get((iso, f"{t0}–{T}")),
                "W0": w0["W"], "WT": wT["W"], "emp_rate0": w0["emp_rate"], "emp_rateT": wT["emp_rate"],
                "ypw0": y["y0"].sum() / (w0["W"] * 1000), "ypwT": y["yT"].sum() / (wT["W"] * 1000),
                "ypw_pp": prod + emprate, "prod_pp": prod,
                "within_pp": r["within_pp"] * k, "struct_pp": r["struct_pp"] * k, "emprate_pp": emprate,
            }
            try:
                row["demog_pp"] = 100 * np.log((wT["W"] / pop.loc[(iso, T)]) / (w0["W"] / pop.loc[(iso, t0)])) / n
            except KeyError:
                row["demog_pp"] = np.nan
            row["ypc_pp"] = row["ypw_pp"] + row["demog_pp"]
            # context for ageing: share of the 15+ population aged 65+ (WDI share x ILO total population)
            for k, yr, w in [("old_share0", t0, w0), ("old_shareT", T, wT)]:
                try:
                    row[k] = 100 * lab65.loc[(iso, yr)] / 100 * pop.loc[(iso, yr)] / w["W"]
                except KeyError:
                    row[k] = np.nan
            for col, g in [("tot_pp", tgr), ("tot_avg_pp", tgr_avg)]:
                try:
                    row[col] = 100 * np.log(g.loc[(iso, T)] / g.loc[(iso, t0)]) / n
                except KeyError:
                    row[col] = np.nan
            rows.append(row)
    return pd.DataFrame(rows)


# ----------------------------------------------------------- 2. horizon ---

def horizon(un, wa):
    tot = un["k2020"]["Total Value Added"].rename("Y")
    d = wa[["L", "W"]].join(tot, how="inner").dropna()
    d = d[d.index.get_level_values("year") <= 2024]
    out = []
    pool_excl = [c for c in POOL_EXCLUDE_LAC if c in COUNTRIES]
    for sample in ["all", "excl"] if pool_excl else ["all"]:
        dd = d[~d.index.get_level_values("iso3").isin(pool_excl)] if sample == "excl" else d
        for h in HORIZONS:
            r = []
            for iso, g in dd.groupby(level="iso3"):
                g = g.droplevel("iso3")
                for t in g.index:
                    if t + h in g.index:
                        a, b = g.loc[t], g.loc[t + h]
                        r.append((100 * np.log((b.Y / b.L) / (a.Y / a.L)) / h, 100 * np.log((b.L / b.W) / (a.L / a.W)) / h))
            r = np.array(r)
            if not len(r):
                continue
            pr, em = r[:, 0], r[:, 1]
            w = pr + em
            out.append({"sample": "all countries" if sample == "all" else f"excluding {', '.join(SHORT[c] for c in pool_excl)}",
                        "horizon": h, "n_windows": len(r),
                        "share_opposite_signs": np.mean(np.sign(pr) != np.sign(em)),
                        "share_emprate_larger": np.mean(np.abs(em) > np.abs(pr)),
                        "emprate_variance_share": np.cov(em, w)[0, 1] / np.var(w, ddof=1),
                        "corr_prod_emprate": np.corrcoef(pr, em)[0, 1],
                        "median_abs_prod_pp": np.median(np.abs(pr)), "median_abs_emprate_pp": np.median(np.abs(em)),
                        "share_prod_up_ypw_down": np.mean((pr > 0) & (w < 0))})
    return pd.DataFrame(out)


# ----------------------------------------------------------- 3. ladders ---

def steps(va, emp, wa, iso, t0, T, base):
    """The two ladders of a period at one price base: lists of (step, value US$/worker, weight)."""
    y = va_at_prices(va, iso, t0, T, base, GRID_A)
    out = {}
    for yr, col in [(t0, "y0"), (T, "yT")]:
        l, w = emp.loc[(iso, yr)].reindex(SECTOR_ORDER), wa.loc[(iso, yr)]
        rows = [(s, y.loc[s, col] / (l[s] * 1000), l[s] / w["W"]) for s in SECTOR_ORDER]
        zero = w["notemp"] / w["W"]
        if pd.notna(w["old_notemp"]):
            old = w["old_notemp"] / w["W"]
            un = w["unemp"] / w["W"] if pd.notna(w["unemp"]) else 0.0
            rows = [("Z_UNEMP", 0.0, un), ("Z_OLF", 0.0, zero - un - old), ("Z_65PLUS", 0.0, old)] + rows
        elif pd.notna(w["unemp"]):
            un = w["unemp"] / w["W"]
            rows = [("Z_UNEMP", 0.0, un), ("Z_OLF", 0.0, zero - un)] + rows
        else:
            rows = [("Z_NOTEMP", 0.0, zero)] + rows
        out[yr] = rows
    return out


def classify(f1, s2):
    """Combine first- and second-order results at two price bases into one verdict."""
    def one(f, s):
        if f == 1:
            return "improvement"
        if f == -1:
            return "deterioration"
        if s == 1:
            return "improvement, weighting the lower percentiles"
        if s == -1:
            return "deterioration, weighting the lower percentiles"
        return "ambiguous"
    v = {one(f1[b], s2[b]) for b in BASES}
    return v.pop() if len(v) == 1 else "depends on prices"


def ladders(va, emp, wa, grades):
    lrows, vrows, irows = [], [], []
    for iso in COUNTRIES:
        for t0, T in PERIODS:
            per, n = f"{t0}–{T}", T - t0
            try:
                st = {b: steps(va, emp, wa, iso, t0, T, b) for b in BASES}
            except KeyError:
                continue
            if any(pd.isna(v) for b in BASES for yr in st[b] for _, v, _ in st[b][yr]):
                continue
            f1, s2 = {}, {}
            for b in BASES:
                d0 = lad.make([v for _, v, _ in st[b][t0]], [w for _, _, w in st[b][t0]])
                dT = lad.make([v for _, v, _ in st[b][T]], [w for _, _, w in st[b][T]])
                for yr in (t0, T):
                    rows = sorted(st[b][yr], key=lambda r: r[1])
                    cum = 0.0
                    for s, v, w in rows:
                        lrows.append({"iso3": iso, "period": per, "year": yr, "base": b, "step": s,
                                      "value": v, "weight": w, "cum_start": cum, "cum_end": cum + w})
                        cum += w
                z = sum(v * w for s, v, w in st[b][t0] if not s.startswith("Z")) / \
                    sum(w for s, v, w in st[b][t0] if not s.startswith("Z"))
                f1[b], s2[b] = lad.dominance(d0, dT, 1), lad.dominance(d0, dT, 2)
                rec = {"iso3": iso, "country": SHORT[iso], "period": per, "t0": t0, "T": T, "base": b,
                       "grade": grades.get((iso, per)),
                       "mean0": lad.mean(d0), "meanT": lad.mean(dT),
                       "mean_growth_pp": (lad.mean(dT) / lad.mean(d0) - 1) / n * 100,
                       "fsd": f1[b], "ssd": s2[b], "share_gained": lad.share_gained(d0, dT), "z": z}
                for lbl, zz in [("", z), ("_half", z / 2)]:
                    for a, nm in [(0, "H"), (1, "gap"), (2, "sev")]:
                        rec[f"{nm}{lbl}0"] = lad.fgt(d0, zz, a)
                        rec[f"{nm}{lbl}T"] = lad.fgt(dT, zz, a)
                vrows.append(rec)
                if b == "initial":
                    g, inc = lad.incidence(d0, dT, n, grid=(np.arange(100) + 0.5) / 100)
                    irows += [{"iso3": iso, "period": per, "pct": round(100 * p, 1), "incidence_pp": x} for p, x in zip(g, inc)]
            verdict = classify(f1, s2)
            for r in vrows[-len(BASES):]:
                r["verdict"] = verdict
    return pd.DataFrame(lrows), pd.DataFrame(vrows), pd.DataFrame(irows)


# ----------------------------------------------------------- 4. frontier ---

FRONTIER_YEARS = [1991, 2000, 2008, 2019, 2024]
FRONTIER_LINES = [0.25, 0.50]


def us_output_per_worker():
    """US total value added (constant 2020 US$) per employed person, by year, from the committed
    world files: UN AMA constant-price file and ILO modelled employment."""
    raw = pd.read_excel(SOURCE / "un_ama" / "un_ama_gdp_breakdown_constant2020_usd.xlsx", header=None)
    hdr = next(i for i in range(20) if "CountryID" in [str(v).strip() for v in raw.iloc[i]])
    df = raw.iloc[hdr + 1:].copy()
    df.columns = [str(c).strip().replace(".0", "") for c in raw.iloc[hdr]]
    row = df[(pd.to_numeric(df["CountryID"], errors="coerce") == 840) & (df["IndicatorName"].astype(str).str.strip() == "Total Value Added")]
    va = row[[c for c in df.columns if c.isdigit()]].iloc[0].astype(float)
    va.index = va.index.astype(int)
    e = pd.read_csv(next(SOURCE.glob("ilostat/EMP_2EMP_SEX_ECO_NB_A*.csv.gz")), dtype=str,
                    usecols=["ref_area", "sex", "classif1", "time", "obs_value"])
    e = e[(e["ref_area"] == "USA") & (e["sex"] == "SEX_T") & (e["classif1"] == "ECO_AGGREGATE_TOTAL")]
    emp = pd.Series(e["obs_value"].astype(float).values, index=e["time"].str[:4].astype(int))
    return (va / (emp * 1000)).dropna()


def relative_price_2020():
    """Price level of output relative to the United States in 2020 (PWT 11.0 pl_gdpo), used to
    convert constant-2020-US$ values to 2020 US$ at PPP with one factor per country."""
    p = pd.read_excel(SOURCE / "pwt" / "pwt110.xlsx", sheet_name="Data", usecols=["countrycode", "year", "pl_gdpo"])
    p = p[p["year"] == 2020].set_index("countrycode")["pl_gdpo"]
    return (p / p["USA"]).dropna()


def frontier(va, emp, wa):
    """Share of the 15+ population working in sectors whose output per worker (2020 US$ at PPP)
    is at least 25% and 50% of US output per worker in the same year, and the average and squared
    gap below those lines with the non-employed at zero (OQ-60). With one step per sector the
    shares jump when a large sector crosses a line; the gaps change continuously. One step per
    sector, valued at constant 2020 prices, so the sector values are not additive across sectors
    and the steps' mean is close to, but not exactly, output per working-age person."""
    us, rel = us_output_per_worker(), relative_price_2020()
    rows = []
    for iso in COUNTRIES:
        if iso not in rel.index:
            continue
        for yr in FRONTIER_YEARS:
            try:
                l, w = emp.loc[(iso, yr)].reindex(SECTOR_ORDER), wa.loc[(iso, yr)]
                v = va.loc[(iso, yr)].reindex(SECTOR_ORDER)["va_k2020usd"]
            except KeyError:
                continue
            if l.isna().any() or v.isna().any() or yr not in us.index:
                continue
            lp = v / (l * 1000) / rel[iso] / us[yr]          # output per worker as a share of the US
            share = l / w["W"]
            rec = {"iso3": iso, "country": SHORT[iso], "year": yr, "comparable": iso not in POOL_EXCLUDE_LAC,
                   "rel_price_2020": rel[iso], "us_output_per_worker": us[yr],
                   "output_per_worker_pct_us": 100 * (v.sum() / (l.sum() * 1000)) / rel[iso] / us[yr],
                   "share_not_employed": 1 - share.sum()}
            d = lad.make(list(lp.values) + [0.0], list(share.values) + [1 - share.sum()])
            for z in FRONTIER_LINES:
                k = int(100 * z)
                rec[f"share_ge_{k}"] = share[lp >= z].sum()
                rec[f"gap_{k}"] = lad.fgt(d, z, 1)
                rec[f"sev_{k}"] = lad.fgt(d, z, 2)
            rows.append(rec)
    return pd.DataFrame(rows)


# ------------------------------------------------------------ report ---

def f(x, nd=2):
    return "" if pd.isna(x) else f"{x:+.{nd}f}"


def write_md(t, h, v, popsrc, fr=None):
    L = [f"# Output per working-age person and the productivity ladder — {SCOPE_NAME}", "",
         "*Generated by `empirics/code/lp/08_ladder.py`; do not edit by hand. Definitions in "
         "`docs/theory/03_defining_productive_development.md` (D-042, D-043).*", "",
         "Working-age population: ages 15+. Value added at initial-year prices of each period. "
         f"Population for the demographic term: {popsrc}. Employment: ILO modelled estimates; "
         "grades as in the main decomposition (A both endpoints anchored by surveys, B one, C none).", "",
         "## 1. Growth of output per working-age person, 2000–2019 (log points per year)", "",
         "| Country | Grade | Y/W | = within | + structural | + employment rate | Demographic | Terms of trade |",
         "|---|---|---|---|---|---|---|---|"]
    for _, r in t[t.period == "2000–2019"].iterrows():
        L.append(f"| {r.country} | {r.grade} | {f(r.ypw_pp)} | {f(r.within_pp)} | {f(r.struct_pp)} | "
                 f"{f(r.emprate_pp)} | {f(r.demog_pp)} | {f(r.tot_pp)} |")
    L += ["", "## 2. Productivity and the employment rate at different horizons", "",
          "| Sample | Horizon (years) | Windows | Opposite signs | Employment-rate term larger | "
          "Its share of variance | Productivity up, Y/W down |", "|---|---|---|---|---|---|---|"]
    for _, r in h.iterrows():
        L.append(f"| {r['sample']} | {r.horizon} | {r.n_windows} | {r.share_opposite_signs:.2f} | "
                 f"{r.share_emprate_larger:.2f} | {r.emprate_variance_share:.2f} | {r.share_prod_up_ypw_down:.3f} |")
    L += ["", "## 3. Ladder verdicts by period (both price bases must agree)", "",
          "| Period | " + " | ".join(VERDICT_ORDER) + " |", "|---" * (len(VERDICT_ORDER) + 1) + "|"]
    vi = v[v.base == "initial"]
    for per in [f"{a}–{b}" for a, b in PERIODS]:
        c = vi[vi.period == per]["verdict"].value_counts()
        L.append(f"| {per} | " + " | ".join(str(int(c.get(k, 0))) for k in VERDICT_ORDER) + " |")
    L += ["", "## 4. Verdicts, 2000–2019", "", "| Country | Grade | Verdict | Mean growth (%/yr, initial prices) | "
          "Share of percentiles that gained | Share below z, start → end |", "|---|---|---|---|---|---|"]
    for _, r in vi[vi.period == "2000–2019"].iterrows():
        L.append(f"| {r.country} | {r.grade} | {r.verdict} | {f(r.mean_growth_pp)} | {r.share_gained:.2f} | "
                 f"{r.H0:.2f} → {r.HT:.2f} |")
    if fr is not None and len(fr):
        f2 = fr[fr["year"].isin([2000, 2019])]
        L += ["", "## 5. Distance from the frontier (2020 US$ at PPP; United States = 100)", "",
              "Average gap below a line at 50% of US output per worker, over the whole 15+ population "
              "(non-employed at zero; 1 = everyone at zero). Share at or above the line in brackets; with one "
              "step per sector it jumps when a large sector crosses the line. Countries marked * have US$ "
              "levels that are not comparable (D-033).", "",
              "| Country | Output per worker, % of US, 2000 | 2019 | Gap below 50% line, 2000 | 2019 |", "|---|---|---|---|---|"]
        for iso, g in f2.groupby("iso3", sort=False):
            g = g.set_index("year")
            if not {2000, 2019} <= set(g.index):
                continue
            a, b = g.loc[2000], g.loc[2019]
            L.append(f"| {a.country}{'' if a.comparable else ' *'} | {a.output_per_worker_pct_us:.1f} | "
                     f"{b.output_per_worker_pct_us:.1f} | {a.gap_50:.3f} ({a.share_ge_50:.2f}) | {b.gap_50:.3f} ({b.share_ge_50:.2f}) |")
    L += ["", "z = output per employed worker at the start of the period, at the same prices. Sector "
          "ladders treat everyone in a sector as equally productive, so dominance here is a statement "
          "about sector averages, not about workers (OQ-57)."]
    (OUT / "results.md").write_text("\n".join(L) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    va, emp, lab, un = load()
    wa = working_age(emp, lab)
    pop, popsrc = population(lab)
    tgr, tgr_avg = trading_gain_ratio(un), trading_gain_ratio(un, "average")
    m = pd.read_csv(OUTPUT / "grid_A" / "main.csv")
    grades = {(r.iso3, r.period): r.grade for r in m.itertuples()}
    lab65 = lab["pop65_share"].dropna() if "pop65_share" in lab.columns else pd.Series(dtype=float)
    t = terms(va, emp, wa, pop, tgr, tgr_avg, grades, lab65)
    h = horizon(un, wa)
    lrows, v, inc = ladders(va, emp, wa, grades)
    fr = frontier(va, emp, wa)
    fr.to_csv(OUT / "frontier.csv", index=False)
    t.to_csv(OUT / "terms.csv", index=False)
    h.to_csv(OUT / "horizon.csv", index=False)
    lrows.to_csv(OUT / "ladders.csv", index=False)
    v.to_csv(OUT / "verdicts.csv", index=False)
    inc.to_csv(OUT / "incidence.csv", index=False)
    write_md(t, h, v, popsrc, fr)
    print(f"{SCOPE_NAME}: {len(t)} country-periods, {v['iso3'].nunique()} countries with ladders")


if __name__ == "__main__":
    main()
