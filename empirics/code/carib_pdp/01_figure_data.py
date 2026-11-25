"""Step 01: data behind the report's graphs, written to empirics/output/carib_pdp/data/.

    g1_decomposition.csv   Graph 1: McMillan-Rodrik terms (pp/yr) by country and pooled by
                           production type, 2000-2019 and 2019-2024, three price bases
    g2_sectors_types.csv   Graph 2: employment shares and relative productivity by sector,
                           pooled by production type, 2024 (current US$)
    a2_sectors_countries.csv  Annex: the same by country
    g4_clusters.csv, g5_sti.csv  Graphs 4 and 5: counts cited in the draft (inputs/)
    s34_employment.csv     Section 3.4: total employment by country, 2024 (ILO modelled)
    box1_sectors.csv       Box 1: sector contributions to the within and structural terms, tourism and
                           services economies pooled, 2000-2019 and 2019-2024, three price bases (D-073)
    box1_relprices.csv     Box 1: change in relative productivity of trade, restaurants and hotels and of
                           other services, split into real and relative-price parts, 2000-2019 (lp step 09)

Country terms are read from the lp pipeline's outputs (grid A, 7 sectors). Pooled terms use
the lp pipeline's own pooling function (07_lac_summary.pooled_period): a type is treated as one
economy, sector value added summed in current US$ and moved with each country's volume index.
Cuba is shown by country and never pooled (D-033).
"""
import numpy as np
import pandas as pd

from config import (DATA, INPUTS, LATEST, LP_OUT, LP_PANEL, NO_POOL, OFFICIAL, PERIODS, SECTOR_LABEL,
                    SECTORS, SHORT, TYPE_OF, TYPES, load_lp)

summ = load_lp("07_lac_summary")
BASES = {"initial": "initial", "final": "final", "chained": "chained"}


def period_label(t0, T):
    return f"{t0}–{T}"


def country_terms():
    labels = [period_label(*p) for p in PERIODS]
    ini = pd.read_csv(LP_OUT / "grid_A" / "main.csv")
    fin = pd.read_csv(LP_OUT / "grid_A" / "robust_final_prices.csv")
    ch = pd.read_csv(LP_OUT / "grid_A" / "robust_chained.csv")
    keep = ["iso3", "period", "growth_pp", "within_pp", "struct_pp", "static_pp", "dynamic_pp"]
    rows = []
    for base, d in [("initial", ini), ("final", fin), ("chained", ch)]:
        x = d[d["period"].isin(labels)][keep].copy()
        x["base"] = base
        rows.append(x)
    out = pd.concat(rows, ignore_index=True)
    out = out.merge(ini[ini["period"].isin(labels)][["iso3", "period", "grade"]], on=["iso3", "period"])
    out["unit"] = "country"
    out["name"] = out["iso3"].map(SHORT)
    return out


def pooled_terms(panel):
    rows = []
    for t, members in TYPES.items():
        m = [c for c in members if c in set(panel["iso3"]) and c not in NO_POOL]
        if not m:
            continue
        for t0, T in PERIODS:
            for base in BASES:
                r, _ = summ.pooled_period(panel, m, t0, T, base)
                rows.append(dict(iso3="", period=period_label(t0, T), growth_pp=r["growth"], within_pp=r["within"],
                                 struct_pp=r["struct"], static_pp=r["static"], dynamic_pp=r["dynamic"], base=base,
                                 grade="pooled", unit="type", name=t, members=" ".join(m)))
    return pd.DataFrame(rows)


def agreement(g1):
    """Classify the structural term across the three price bases, with the lp pipeline's rule."""
    w = g1.pivot_table(index=["unit", "name", "period"], columns="base", values="struct_pp").reset_index()
    w = w.rename(columns={"chained": "struct_pp", "initial": "struct_initial", "final": "struct_final"})
    w["agreement"] = w.apply(summ.classify, axis=1)
    return w[["unit", "name", "period", "agreement"]]


def sector_table(panel, members, year):
    a = panel[(panel["year"] == year) & panel["iso3"].isin(members)]
    g = a.groupby("sector").agg(va=("va_cur_usd", "sum"), emp=("emp_model", "sum")).reindex(SECTORS)
    g["emp_share_pct"] = 100 * g["emp"] / g["emp"].sum()
    g["rel_lp"] = (g["va"] / g["emp"]) / (g["va"].sum() / g["emp"].sum())
    return g.reset_index()


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    panel = summ.load_panel("A")

    g1 = pd.concat([country_terms(), pooled_terms(panel)], ignore_index=True)
    g1["type"] = np.where(g1["unit"] == "type", g1["name"], g1["iso3"].map(TYPE_OF))
    g1 = g1.merge(agreement(g1), on=["unit", "name", "period"])
    g1["members"] = g1["members"].fillna("")
    cols = ["type", "unit", "iso3", "name", "members", "period", "base", "grade", "growth_pp", "within_pp",
            "struct_pp", "static_pp", "dynamic_pp", "agreement"]
    order = {t: i for i, t in enumerate(TYPES)}
    g1 = g1[cols].sort_values(["period", "base", "type", "unit", "name"],
                              key=lambda s: s.map(order) if s.name == "type" else s,
                              ascending=[True, True, True, False, True])
    g1.to_csv(DATA / "g1_decomposition.csv", index=False)

    rows = []
    for t, members in TYPES.items():
        m = [c for c in members if c in set(panel["iso3"]) and c not in NO_POOL]
        s = sector_table(panel, m, LATEST)
        s.insert(0, "type", t)
        s.insert(1, "members", " ".join(m))
        rows.append(s)
    g2 = pd.concat(rows, ignore_index=True)
    g2["sector_name"] = g2["sector"].map(SECTOR_LABEL)
    g2.to_csv(DATA / "g2_sectors_types.csv", index=False)

    rows = []
    for iso in sorted(set(panel["iso3"]), key=lambda c: (list(TYPES).index(TYPE_OF[c]), SHORT[c])):
        s = sector_table(panel, [iso], LATEST)
        s.insert(0, "iso3", iso)
        s.insert(1, "name", SHORT[iso])
        s.insert(2, "type", TYPE_OF[iso])
        rows.append(s)
    a2 = pd.concat(rows, ignore_index=True)
    a2["sector_name"] = a2["sector"].map(SECTOR_LABEL)
    a2.to_csv(DATA / "a2_sectors_countries.csv", index=False)

    counts = pd.read_csv(INPUTS / "draft_counts.csv")
    counts["name"] = counts["iso3"].map(SHORT)
    counts["type"] = counts["iso3"].map(TYPE_OF)
    for g, fname in [("G4", "g4_clusters.csv"), ("G5", "g5_sti.csv")]:
        (counts[counts["graph"] == g].sort_values(["count", "name"], ascending=[False, True])
         .drop(columns="graph").to_csv(DATA / fname, index=False))

    p = pd.read_csv(LP_PANEL)
    e = p[p["year"] == LATEST].groupby("iso3", as_index=False)["emp_model"].sum(min_count=7)
    e = e.dropna()
    e["name"] = e["iso3"].map(SHORT)
    e["official_name"] = e["iso3"].map(OFFICIAL)
    e["type"] = e["iso3"].map(TYPE_OF)
    e = e.rename(columns={"emp_model": "employment_thousands"}).sort_values("employment_thousands")
    e[["iso3", "name", "official_name", "type", "employment_thousands"]].to_csv(DATA / "s34_employment.csv", index=False)
    tour = "Tourism and services economies"
    m = [c for c in TYPES[tour] if c in set(panel["iso3"]) and c not in NO_POOL]
    rows = []
    for t0, T in PERIODS:
        for base in BASES:
            _, sec = summ.pooled_period(panel, m, t0, T, base)
            sec = sec.reindex(SECTORS).reset_index().rename(columns={"index": "sector", "within": "within_pp",
                                                                       "struct": "struct_pp"})
            sec.insert(0, "period", period_label(t0, T))
            sec.insert(1, "base", base)
            sec["members"] = " ".join(m)
            rows.append(sec)
    b1 = pd.concat(rows, ignore_index=True)
    b1["sector_name"] = b1["sector"].map(SECTOR_LABEL)
    b1.to_csv(DATA / "box1_sectors.csv", index=False)
    bm = pd.read_csv(LP_OUT / "baumol" / "sectors.csv")
    bm = bm[bm["iso3"].isin(m) & bm["sector"].isin(["TRH", "OTH"]) & (bm["period"] == "2000–2019")]
    bm = bm[["iso3", "country", "period", "sector", "emp_share0", "rel_nom0", "rel_nomT", "d_nom_pp", "d_real_pp",
             "d_price_pp"]]
    bm.to_csv(DATA / "box1_relprices.csv", index=False)
    print("figure data written to", DATA)


if __name__ == "__main__":
    main()
