"""Titles, units, sources and notes (ECLAC style) for the report's graphs and annex tables,
and the report text that cites numbers. Every number is formatted from the generated data in
empirics/output/carib_pdp/data/, so text and outputs cannot drift apart.

ECLAC layout: label ("Graph 1"), title starting with the geographic coverage and the number
of countries, unit in parentheses on its own line; below the figure, "Source:", "Note:" and
lettered notes. Shown as document text, never inside the figure.
"""
import pandas as pd

from config import DATA, OFFICIAL, TYPES

SRC_LP = ("Prepared by the author, on the basis of United Nations, National Accounts Main Aggregates "
          "Database (January 2026 update), and International Labour Organization (ILO), ILOSTAT database "
          "(ILO modelled estimates and national labour force surveys).")


def _g1():
    g = pd.read_csv(DATA / "g1_decomposition.csv", keep_default_na=False, na_values=[""])
    return g


def the(name):
    """Country name with the article English text needs in running prose."""
    return "the " + name if name in ("Dominican Republic", "Bahamas") else name


def fmt(x, nd=2):
    s = f"{x:.{nd}f}"
    return s.replace("-", "−")


def pooled(g, name, period, base="chained"):
    r = g[(g["unit"] == "type") & (g["name"] == name) & (g["period"] == period) & (g["base"] == base)]
    return r.iloc[0]


def country(g, name, period, base="chained"):
    r = g[(g["unit"] == "country") & (g["name"] == name) & (g["period"] == period) & (g["base"] == base)]
    return r.iloc[0]


def figure_texts():
    g = _g1()
    s2 = pd.read_csv(DATA / "g2_sectors_types.csv")
    n_g1 = g.loc[g["unit"] == "country", "iso3"].nunique()
    n_g2 = len(set(" ".join(s2["members"].unique()).split()))
    flips = g[(g["base"] == "chained") & (g["unit"] == "country") & (g["agreement"] == "sign depends on price base")]
    flips = flips.groupby("period")["name"].apply(lambda s: " and ".join(the(x) for x in sorted(s))).to_dict()
    pooled_members = s2.groupby("type")["members"].first().to_dict()

    def names(isos):
        n = [the(OFFICIAL[i]) for i in isos.split()]
        return ", ".join(n[:-1]) + " and " + n[-1]

    t = {}
    t["graph1"] = dict(
        label="Graph 1",
        title=(f"Caribbean ({n_g1} countries): contributions to labour productivity growth within sectors "
               "and from structural change, by production type, 2000–2019 and 2019–2024"),
        unit="(Percentage points per year)",
        source=SRC_LP,
        notes=[
            ("Note", "Labour productivity is value added per person employed, in seven sectors. The decomposition "
                     "follows McMillan and Rodrik (2011): within-sector growth weighted by initial employment "
                     "shares, and a structural change term for the reallocation of employment between sectors. "
                     "Values are averages of annual decompositions at previous-year prices (chained); table A.1 "
                     "of the annex gives the results at initial-year and final-year prices. “Pooled” treats the "
                     "economies of each type as a single economy, so a shift of workers between countries within "
                     "a sector counts as within-sector change. Pooled groups: resource and energy, "
                     f"{names(pooled_members['Resource and energy economies'])}; tourism and services, "
                     f"{names(pooled_members['Tourism and services economies'])}; mixed, "
                     f"{names(pooled_members['Mixed economies'])}; other Caribbean, "
                     f"{names(pooled_members['Other Caribbean economies'])}. Cuba is shown but not pooled, "
                     "because its dollar values, converted at the official exchange rate, are not comparable. "
                     "Pale bars: neither end of the period is within two years of a usable national labour "
                     "force survey, so sector employment rests on ILO modelling. Antigua and Barbuda, Dominica, "
                     "Grenada and Saint Kitts and Nevis are not shown because no series of employment by sector "
                     "is available."),
            ("a", "Value beyond the axis limit; the number shown is the value."),
            ("b", "The structural change term has a different sign at chained, initial-year and final-year "
                  f"prices ({flips.get('2000–2019', 'none')}, 2000–2019)."),
        ])
    t["graph2"] = dict(
        label="Graph 2",
        title=(f"Caribbean ({n_g2} countries): employment shares and relative labour productivity by sector "
               "and production type, 2024"),
        unit=None,
        panels={"graph2a": "A. Share of total employment\n(Percentages)",
                "graph2b": "B. Labour productivity relative to the average of the group\n"
                           "(Average of the group = 1; logarithmic scale)"},
        source=SRC_LP,
        notes=[
            ("Note", "Each production type is treated as one economy: value added at current dollars and "
                     "employment (ILO modelled estimates) are summed over its countries. Relative productivity "
                     "is a sector's value added per person employed divided by that of the whole group. Groups "
                     "as in graph 1. Cuba is excluded because its dollar values are not comparable. Tables A.2 "
                     "and A.3 of the annex give the figures by country."),
        ])
    t["graph4"] = dict(
        label="Graph 4",
        title="Caribbean (8 countries): productive coordination initiatives by country, 2023–2025",
        unit="(Number of initiatives)",
        source=("Prepared by the author, on the basis of Economic Commission for Latin America and the "
                "Caribbean (ECLAC), Panorama of Productive Development Policies in Latin America and the "
                "Caribbean, 2025 (LC/PUB.2025/16), Santiago, 2025, and ECLAC, Platform for cluster and other "
                "territorial productive articulation initiatives."),
        notes=[("Note", "Caribbean countries with no registered initiative are not shown. The platform records "
                        "712 initiatives in 20 countries, 367 of them in Brazil.")])
    t["graph5"] = dict(
        label="Graph 5",
        title="Caribbean (8 countries): science, technology and innovation policy instruments by country, 2025",
        unit="(Number of instruments)",
        source=("Prepared by the author, on the basis of Economic Commission for Latin America and the "
                "Caribbean (ECLAC), “Políticas de ciencia, tecnología e innovación para el desarrollo "
                "productivo”, Panorama de las Políticas de Desarrollo Productivo en América Latina y el "
                "Caribe, 2025, chapter II, Santiago, 2025."),
        notes=[("Note", "Counts do not reflect the size of each instrument. For comparison, the database records "
                        "136 instruments in Argentina and 109 in Brazil.")])
    t["tableA1"] = dict(
        label="Table A.1",
        title=(f"Caribbean ({n_g1} countries): decomposition of labour productivity growth by country and "
               "production type at three price bases, 2000–2019 and 2019–2024"),
        unit="(Percentage points per year)",
        source=SRC_LP,
        notes=[("Note", "Growth and within-sector terms at chained prices, as in graph 1. The structural change "
                        "term is shown at chained, initial-year and final-year prices. Fixed-base figures are "
                        "linear averages of the change over the period; chained figures are averages of annual "
                        "changes. Data grade: A, both ends of the period within two years of a usable labour force "
                        "survey; B, one end; C, neither (ILO modelled employment only)."),
               ])
    t["tableA2"] = dict(
        label="Table A.2",
        title="Caribbean (12 countries): employment by sector, 2024",
        unit="(Percentages of total employment)",
        source=SRC_LP,
        notes=[("Note", "ILO modelled estimates.")])
    t["tableA3"] = dict(
        label="Table A.3",
        title="Caribbean (11 countries): labour productivity by sector relative to the economy-wide average, 2024",
        unit="(Economy-wide average = 1)",
        source=SRC_LP,
        notes=[("Note", "Value added at current dollars per person employed (ILO modelled estimates). Cuba is "
                        "excluded because its dollar values are not comparable.")])
    return t


def report_paragraphs():
    """Paragraphs added to sections 3.1, 3.2 and 3.4 of the report, with numbers from the data."""
    g = _g1()
    s2 = pd.read_csv(DATA / "g2_sectors_types.csv").set_index(["type", "sector"])
    emp = pd.read_csv(DATA / "s34_employment.csv").set_index("iso3")
    P1, P2 = "2000–2019", "2019–2024"
    R, T, M, O = list(TYPES)
    r, tt, m, o = (pooled(g, x, P1) for x in (R, T, M, O))
    gp = g[(g["unit"] == "type") & (g["period"] == P1) & (g["base"] == "chained")]
    c1 = g[(g["unit"] == "country") & (g["period"] == P1) & (g["base"] == "chained")]
    c2 = g[(g["unit"] == "country") & (g["period"] == P2) & (g["base"] == "chained")]
    c2x = c2[c2["name"] != "Guyana"]
    guy = country(g, "Guyana", P2)
    r_init = pooled(g, R, P1, "initial")
    flips = sorted(c1.loc[c1["agreement"] == "sign depends on price base", "name"])
    lo2, hi2 = c2x.loc[c2x["growth_pp"].idxmin()], c2x.loc[c2x["growth_pp"].idxmax()]
    slo2, shi2 = c2x.loc[c2x["struct_pp"].idxmin()], c2x.loc[c2x["struct_pp"].idxmax()]
    lcs = country(g, "Saint Lucia", P1)

    def sh(t, sec):
        return s2.loc[(t, sec), "emp_share_pct"]

    def rl(t, sec):
        return s2.loc[(t, sec), "rel_lp"]

    serv = {t: sh(t, "TRH") + sh(t, "OTH") for t in TYPES}
    miu_other = max(sh(t, "MIU") for t in (T, M, O))
    miu_top = all(s2.loc[t, "rel_lp"].idxmax() == "MIU" for t in TYPES)
    assert miu_top, "text assumes mining and utilities has the highest relative productivity in every group"

    small = emp[emp["employment_thousands"] < 300]
    big = emp[emp["employment_thousands"] >= 300]
    p = {}
    p["3.1_other"] = ("Other Caribbean economies: the Dominican Republic, Haiti and Cuba. Each had more than "
                      f"{int(big.loc[['DOM', 'HTI', 'CUB'], 'employment_thousands'].min() // 1000)} million "
                      "people employed in 2024, far more than any economy in the three types above, and their "
                      "production structures differ from those types and from one another. They are shown "
                      "separately.")
    p["3.2_lead"] = ("ECLAC’s published decomposition covers the region as a whole. Graph 1 applies the same "
                     f"decomposition to {c1['iso3'].nunique()} Caribbean economies, grouped by production type, "
                     "with value added from the United Nations National Accounts Main Aggregates Database and "
                     "employment by sector from ILOSTAT; the GGDC–UNU-WIDER Economic Transformation Database "
                     "does not cover any Caribbean country. Graph 2 shows employment shares and relative "
                     "productivity by sector in 2024.")
    p["3.2_after"] = [
        (f"In {P1}, the reallocation of employment between sectors added between "
         f"{fmt(gp['struct_pp'].min())} and {fmt(gp['struct_pp'].max())} percentage points a year to labour "
         "productivity growth in the four pooled groups, at chained prices (graph 1). Differences in "
         "productivity growth between the groups came mainly from within sectors. In the tourism and services "
         f"economies, productivity grew by {fmt(tt['growth_pp'])} percent a year: reallocation added "
         f"{fmt(tt['struct_pp'])} points, and productivity within sectors subtracted "
         f"{fmt(-tt['within_pp'])}. In the mixed economies, productivity fell by {fmt(-m['growth_pp'])} percent a "
         f"year, with a within-sector term of {fmt(m['within_pp'])} points. In the resource and energy economies, "
         f"growth of {fmt(r['growth_pp'])} percent a year came from within sectors; the structural term was "
         f"{fmt(r['struct_pp'])} points at chained prices and {fmt(r_init['struct_pp'])} at initial-year prices. "
         f"In the other Caribbean group, growth was {fmt(o['growth_pp'])} percent a year, "
         f"{fmt(o['struct_pp'])} points of it from reallocation. Among individual economies, the structural "
         f"term ranged from {fmt(c1['struct_pp'].min())} points a year "
         f"({c1.loc[c1['struct_pp'].idxmin(), 'name']}) to {fmt(c1['struct_pp'].max())} "
         f"({c1.loc[c1['struct_pp'].idxmax(), 'name']}, where the within-sector term was {fmt(lcs['within_pp'])}); "
         f"in {' and '.join(the(x) for x in flips)} its sign depends on the price base."),
        (f"The period {P2} includes the pandemic and the start of oil production in Guyana, where productivity "
         f"grew by an average of {fmt(guy['growth_pp'], 1)} percent a year, {fmt(guy['within_pp'], 1)} points of "
         "it within sectors. In the other economies, productivity growth ranged from "
         f"{fmt(lo2['growth_pp'], 1)} percent a year ({lo2['name']}) to {fmt(hi2['growth_pp'], 1)} percent "
         f"({hi2['name']}), and the structural term from {fmt(slo2['struct_pp'])} points ({slo2['name']}) to "
         f"{fmt(shi2['struct_pp'])} ({shi2['name']})."),
        ("In 2024, trade, restaurants and hotels and other services together employed between "
         f"{fmt(min(serv.values()), 0)} and {fmt(max(serv.values()), 0)} percent of workers in the four groups "
         f"(graph 2), and {fmt(serv[T], 0)} percent in the tourism and services economies, where trade, "
         f"restaurants and hotels alone employed {fmt(sh(T, 'TRH'), 1)} percent at "
         f"{fmt(rl(T, 'TRH'))} times the group’s average productivity. Mining and utilities had the highest "
         f"relative productivity in every group, {fmt(rl(R, 'MIU'), 1)} times the average in the resource and "
         f"energy economies, where it employed {fmt(sh(R, 'MIU'), 1)} percent of workers; in the other groups it "
         f"employed {fmt(miu_other, 1)} percent or less. Agriculture employed {fmt(sh(O, 'AGR'), 1)} percent of "
         f"workers in the other Caribbean group, at {fmt(rl(O, 'AGR'))} times its average productivity."),
        ("These decompositions are descriptive. Employment by sector rests "
         "on ILO modelled estimates, which for some country-periods are not anchored to a labour force survey "
         "near either end of the period (pale bars in graph 1). Because constant-price value added is "
         "chain-linked, the terms depend on the price base used to weight sectors; table A.1 of the annex reports "
         "all three. Pooling treats each group as one economy, so movements of workers between countries "
         "within a sector count as within-sector change."),
    ]
    lca = emp.loc["LCA", "employment_thousands"]
    p["3.4"] = ("In 2024, total employment was below 300,000 in "
                f"{len(small)} of the {len(emp)} Caribbean economies with ILO estimates, from about "
                f"{round(small['employment_thousands'].min()):,},000 in {small['name'].iloc[0]} to about "
                f"{round(small['employment_thousands'].max()):,},000 in {small['name'].iloc[-1]}, and between "
                f"{big['employment_thousands'].min() / 1000:.1f} and {big['employment_thousands'].max() / 1000:.1f} "
                "million in the other five (ILO modelled estimates). Antigua and Barbuda, Dominica, Grenada and "
                "Saint Kitts and Nevis are not covered by these estimates. In Saint Lucia, with about "
                f"{round(lca):,},000 people employed, a cluster or firm employing 5,000 workers accounts for "
                f"{fmt(500000 / (lca * 1000), 1)} percent of employment.")
    return p


if __name__ == "__main__":
    import json
    print(json.dumps(report_paragraphs(), indent=1, ensure_ascii=False))
