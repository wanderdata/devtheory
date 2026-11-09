"""Regional summary of the LAC decompositions for WP06.

    LP_SCOPE=lac python empirics/code/lp/07_lac_summary.py

Reads the LAC panel and the country decompositions written by 05_decompose.py
(run that first, for LP_SCOPE=lac). Writes to empirics/output/lac_lp/summary/:

    pooled_periods.csv     pooled-region decompositions by period, grid and price base
    country_stats.csv      distribution of country results by period (grades A and B)
    price_agreement.csv    structural term at three price bases, classified by agreement
    sectors_pooled.csv     pooled employment shares and relative productivity by sector
    sector_contrib.csv     pooled sector contributions to within and structural terms
    summary.md             all of the above as tables (generated; do not edit)
    fig1_pooled.png, fig2_agreement.png, fig3_sectors.png

Pooling. The pooled region is treated as one economy with seven (or five) sectors:
sector value added is summed across countries in current US$ and moved forward
with each country's own sector volume index; employment is summed. Year-to-year
decompositions at previous-year prices are averaged over each period (chained,
D-032); the fixed-base versions value the whole period at its initial or final
year. Because sectors are pooled across countries, a shift of workers between
countries within a sector counts as within-sector change, not structural change.

Groups. LAC = all scope countries with sector employment except Cuba and Venezuela
(US$ levels not comparable, D-033). Caribbean = the Caribbean (broad, D-019)
members of that group. Latin America = the rest.
"""
import numpy as np
import pandas as pd

from config import OUTPUT, PROCESSED, SCOPE
from empirics.common.countries import CARIBBEAN16, POOL_EXCLUDE_LAC

PERIODS = [(1991, 2000), (2000, 2008), (2008, 2019), (2019, 2024), (2000, 2019)]
CARIB16 = set(CARIBBEAN16)
EXCLUDE = set(POOL_EXCLUDE_LAC)
GRID_B = {"AGR": "AGR", "MIU": "MIU", "MAN": "MAN", "CON": "CON", "TRH": "SER", "TSC": "SER", "OTH": "SER"}
SHORT = {"AGR": "Agriculture", "MIU": "Mining & utilities", "MAN": "Manufacturing", "CON": "Construction",
         "TRH": "Trade, restaurants & hotels", "TSC": "Transport, storage & comms", "OTH": "Other services",
         "SER": "Services (all)"}
OUT = OUTPUT / "summary"
SMALL = 0.10   # pp/yr: structural terms smaller than this in absolute value count as "near zero"


def load_panel(grid):
    p = pd.read_csv(PROCESSED / "panel_7sector.csv")
    p = p.dropna(subset=["va_cur_usd", "va_k2020usd", "emp_model"])
    if grid == "B":
        p = p.assign(sector=p["sector"].map(GRID_B))
        p = p.groupby(["iso3", "year", "sector"], as_index=False)[["va_cur_usd", "va_k2020usd", "emp_model"]].sum()
    n = 7 if grid == "A" else 5
    full = p.groupby(["iso3", "year"])["sector"].transform("nunique") == n
    return p[full]


def groups(p):
    have = set(p["iso3"])
    lac = sorted(have - EXCLUDE)
    car = [c for c in lac if c in CARIB16]
    return {"LAC": lac, "Latin America": [c for c in lac if c not in CARIB16], "Caribbean": car,
            # sensitivity: Guyana's oil (from 2019) and the Dominican Republic's weight
            "Caribbean excl. Guyana": [c for c in car if c != "GUY"],
            "Caribbean excl. Guyana and Dominican Rep.": [c for c in car if c not in ("GUY", "DOM")]}


def pooled_step(p, members, t0, t1):
    """Pooled sector y0, y1 (US$ at t0 prices) and employment l0, l1 for members present in both years."""
    a = p[(p["year"] == t0) & p["iso3"].isin(members)].set_index(["iso3", "sector"])
    b = p[(p["year"] == t1) & p["iso3"].isin(members)].set_index(["iso3", "sector"])
    idx = a.index.intersection(b.index)
    a, b = a.loc[idx], b.loc[idx]
    vol = b["va_k2020usd"] / a["va_k2020usd"]
    y0 = a["va_cur_usd"].groupby(level="sector").sum()
    y1 = (a["va_cur_usd"] * vol).groupby(level="sector").sum()
    l0 = (a["emp_model"] * 1000).groupby(level="sector").sum()
    l1 = (b["emp_model"] * 1000).groupby(level="sector").sum()
    return y0, y1, l0, l1


def mr(y0, y1, l0, l1):
    p0, p1 = y0 / l0, y1 / l1
    s0, s1 = l0 / l0.sum(), l1 / l1.sum()
    P0, P1 = y0.sum() / l0.sum(), y1.sum() / l1.sum()
    return dict(P0=P0, P1=P1, within=s0 * (p1 - p0), static=p0 * (s1 - s0), dynamic=(p1 - p0) * (s1 - s0))


def pooled_period(p, members, t0, T, base):
    """Terms in pp/yr. Chained: mean of annual contributions. Fixed: whole period at t0 or T prices."""
    if base == "chained":
        acc, sec = None, None
        for t in range(t0, T):
            r = mr(*pooled_step(p, members, t, t + 1))
            k = 100 / r["P0"]
            terms = {"growth": (r["P1"] - r["P0"]) * k, "within": r["within"].sum() * k,
                     "static": r["static"].sum() * k, "dynamic": r["dynamic"].sum() * k}
            s = pd.DataFrame({"within": r["within"] * k, "struct": (r["static"] + r["dynamic"]) * k})
            acc = terms if acc is None else {x: acc[x] + terms[x] for x in acc}
            sec = s if sec is None else sec.add(s, fill_value=0)
        n = T - t0
        res = {x: v / n for x, v in acc.items()}
        sec = sec / n
    else:
        y0, yT, l0, lT = pooled_step(p, members, t0, T)
        if base == "final":   # revalue both ends at T prices: divide t0 by the volume ratio
            r0 = mr(y0, yT, l0, lT)
            a = p[(p["year"] == T) & p["iso3"].isin(members)].set_index(["iso3", "sector"])
            b = p[(p["year"] == t0) & p["iso3"].isin(members)].set_index(["iso3", "sector"])
            idx = a.index.intersection(b.index)
            vol = a.loc[idx, "va_k2020usd"] / b.loc[idx, "va_k2020usd"]
            yT = a.loc[idx, "va_cur_usd"].groupby(level="sector").sum()
            y0 = (a.loc[idx, "va_cur_usd"] / vol).groupby(level="sector").sum()
        r = mr(y0, yT, l0, lT)
        k = 100 / r["P0"] / (T - t0)
        res = {"growth": (r["P1"] - r["P0"]) * k, "within": r["within"].sum() * k,
               "static": r["static"].sum() * k, "dynamic": r["dynamic"].sum() * k}
        sec = pd.DataFrame({"within": r["within"] * k, "struct": (r["static"] + r["dynamic"]) * k})
    res["struct"] = res["static"] + res["dynamic"]
    res["struct_share"] = res["struct"] / res["growth"] if abs(res["growth"]) > 1e-9 else np.nan
    return res, sec


def country_results(grid):
    d = OUTPUT / f"grid_{grid}"
    keep = ["iso3", "country", "period", "grade", "growth_pp", "within_pp", "struct_pp", "static_pp", "dynamic_pp"]
    ch = pd.read_csv(d / "robust_chained.csv")
    ini = pd.read_csv(d / "main.csv")
    fin = pd.read_csv(d / "robust_final_prices.csv")
    ch = ch.drop(columns=[c for c in ["grade"] if c in ch.columns]).merge(ini[["iso3", "period", "grade"]], on=["iso3", "period"])
    m = ch[keep].merge(ini[["iso3", "period", "struct_pp", "static_pp", "dynamic_pp"]].rename(
        columns={"struct_pp": "struct_initial", "static_pp": "static_initial", "dynamic_pp": "dynamic_initial"}), on=["iso3", "period"])
    m = m.merge(fin[["iso3", "period", "struct_pp"]].rename(columns={"struct_pp": "struct_final"}), on=["iso3", "period"])
    return m


def classify(row):
    v = np.array([row["struct_pp"], row["struct_initial"], row["struct_final"]])
    if (v >= SMALL).all():
        return "positive at all three"
    if (v <= -SMALL).all():
        return "negative at all three"
    if (np.abs(v) < SMALL).all():
        return "near zero at all three"
    if (v > 0).all() or (v < 0).all():
        return "same sign, size differs"
    return "sign depends on price base"


def sectors_pooled(p, members):
    rows = []
    for y in [1991, 2000, 2008, 2019, 2024]:
        a = p[(p["year"] == y) & p["iso3"].isin(members)]
        g = a.groupby("sector").agg(va=("va_cur_usd", "sum"), emp=("emp_model", "sum"))
        g["emp_share"] = 100 * g["emp"] / g["emp"].sum()
        g["va_share"] = 100 * g["va"] / g["va"].sum()
        g["rel_lp"] = 100 * (g["va"] / g["emp"]) / (g["va"].sum() / g["emp"].sum())
        g["year"] = y
        rows.append(g.reset_index())
    return pd.concat(rows, ignore_index=True)


def f(x, nd=2):
    return "—" if pd.isna(x) else f"{x:.{nd}f}"


def main():
    if SCOPE != "lac":
        raise SystemExit("Run with LP_SCOPE=lac")
    OUT.mkdir(parents=True, exist_ok=True)
    pooled, contrib = [], []
    for grid in ["A", "B"]:
        p = load_panel(grid)
        for gname, members in groups(p).items():
            for t0, T in PERIODS:
                for base in ["chained", "initial", "final"]:
                    r, sec = pooled_period(p, members, t0, T, base)
                    pooled.append({"grid": grid, "group": gname, "n_countries": len(members),
                                   "period": f"{t0}–{T}", "base": base, **r})
                    if gname == "LAC" and base == "chained":
                        contrib.append(sec.reset_index().assign(grid=grid, period=f"{t0}–{T}"))
    pooled = pd.DataFrame(pooled)
    pooled.to_csv(OUT / "pooled_periods.csv", index=False)
    contrib = pd.concat(contrib, ignore_index=True)
    contrib.to_csv(OUT / "sector_contrib.csv", index=False)

    # country distribution (grid A, chained, grades A and B, all countries incl. CUB and VEN)
    stats, agree = [], []
    for grid in ["A", "B"]:
        c = country_results(grid)
        c["agreement"] = c.apply(classify, axis=1)
        c["grid"] = grid
        agree.append(c)
        ab = c[c["grade"].isin(["A", "B"])]
        for per, g in ab.groupby("period", sort=False):
            stats.append({"grid": grid, "period": per, "n": len(g),
                          "median_growth": g["growth_pp"].median(), "median_within": g["within_pp"].median(),
                          "median_struct": g["struct_pp"].median(),
                          "share_struct_negative": (g["struct_pp"] < 0).mean(),
                          # static/dynamic read at fixed (initial-year) prices: in chained form the dynamic
                          # term is a sum of products of one-year changes and is mechanically close to zero
                          "median_static_initial": g["static_initial"].median(),
                          "median_dynamic_initial": g["dynamic_initial"].median(),
                          "share_static_pos_dynamic_neg": ((g["static_initial"] > 0) & (g["dynamic_initial"] < 0)).mean(),
                          "share_growth_negative": (g["growth_pp"] < 0).mean()})
    stats = pd.DataFrame(stats)
    stats.to_csv(OUT / "country_stats.csv", index=False)
    agree = pd.concat(agree, ignore_index=True)
    agree.to_csv(OUT / "price_agreement.csv", index=False)

    pA = load_panel("A")
    sec = sectors_pooled(pA, groups(pA)["LAC"])
    # weights and employment growth of the pooled LAC group
    lac = groups(pA)["LAC"]
    tot = pA[pA["iso3"].isin(lac)].groupby(["iso3", "year"]).agg(va=("va_cur_usd", "sum"), emp=("emp_model", "sum")).reset_index()
    w = []
    for y in [1991, 2000, 2008, 2019]:
        t = tot[tot["year"] == y].set_index("iso3")
        for c in ["MEX", "BRA", "ARG", "COL", "CHL"]:
            w.append({"year": y, "iso3": c, "va_share": t.loc[c, "va"] / t["va"].sum()})
    pd.DataFrame(w).to_csv(OUT / "weights.csv", index=False)
    eg = []
    for t0, T in PERIODS:
        a0 = tot[tot["year"] == t0]["emp"].sum(); aT = tot[tot["year"] == T]["emp"].sum()
        eg.append({"period": f"{t0}–{T}", "emp_growth_pct": 100 * ((aT / a0) ** (1 / (T - t0)) - 1)})
    pd.DataFrame(eg).to_csv(OUT / "employment_growth.csv", index=False)
    sec.to_csv(OUT / "sectors_pooled.csv", index=False)

    write_md(pooled, stats, agree, sec, contrib, groups(pA))
    L = ["", "## Pooled LAC: value-added weights (current US$) and employment growth", "",
         "| Year | " + " | ".join(["MEX", "BRA", "ARG", "COL", "CHL"]) + " |", "|---|---|---|---|---|---|"]
    wd = pd.read_csv(OUT / "weights.csv").pivot(index="year", columns="iso3", values="va_share")
    for y, r in wd.iterrows():
        L.append(f"| {y} | " + " | ".join(f"{100*r[c]:.0f}%" for c in ["MEX", "BRA", "ARG", "COL", "CHL"]) + " |")
    L += ["", "| Period | Employment growth, %/yr |", "|---|---|"]
    for _, r in pd.read_csv(OUT / "employment_growth.csv").iterrows():
        L.append(f"| {r['period']} | {r['emp_growth_pct']:.2f} |")
    with open(OUT / "summary.md", "a") as fh:
        fh.write("\n".join(L) + "\n")
    figures(pooled, agree, sec)
    print((OUT / "summary.md").read_text()[:3000])


def write_md(pooled, stats, agree, sec, contrib, grp):
    L = ["# LAC labour productivity: regional summary (WP06)", "",
         "Generated by `empirics/code/lp/07_lac_summary.py`. Do not edit by hand. "
         "Terms are contributions to average annual labour-productivity growth, pp per year; ILO modelled employment.", "",
         f"Pooled groups: **LAC** {len(grp['LAC'])} countries ({', '.join(grp['LAC'])}); **Latin America** "
         f"{len(grp['Latin America'])}; **Caribbean** {len(grp['Caribbean'])} (sensitivity groups drop Guyana, then also the "
         "Dominican Republic). Cuba and Venezuela are excluded "
         "from pooled groups (D-033). Pooling treats each group as one economy; shifts between countries within a "
         "sector count as within-sector change.", ""]
    for grid in ["A", "B"]:
        L += [f"## Pooled decompositions, grid {grid}", "",
              "| Group | Period | Price base | Growth | Within | Structural | static | dynamic | Structural share of growth |",
              "|---|---|---|---|---|---|---|---|---|"]
        x = pooled[pooled["grid"] == grid]
        for _, r in x.iterrows():
            L.append(f"| {r['group']} | {r['period']} | {r['base']} | {f(r['growth'])} | {f(r['within'])} | "
                     f"**{f(r['struct'])}** | {f(r['static'])} | {f(r['dynamic'])} | {f(100*r['struct_share'],0)}% |")
        L.append("")
    L += ["## Country results, grades A and B, chained prices (static/dynamic at initial-year prices)", "",
          "In chained form the dynamic term is a sum of products of one-year changes, so it is mechanically close to zero; "
          "the static/dynamic split is therefore read at fixed (initial-year) prices.", "",
          "| Grid | Period | n | Median growth | Median within | Median structural | Share structural < 0 | Median static (initial-year prices) | Median dynamic (initial-year prices) | Share static > 0 and dynamic < 0 (initial-year prices) | Share growth < 0 |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in stats.iterrows():
        L.append(f"| {r['grid']} | {r['period']} | {r['n']} | {f(r['median_growth'])} | {f(r['median_within'])} | "
                 f"{f(r['median_struct'])} | {r['share_struct_negative']:.0%} | {f(r['median_static_initial'])} | {f(r['median_dynamic_initial'])} | {r['share_static_pos_dynamic_neg']:.0%} | "
                 f"{r['share_growth_negative']:.0%} |")
    L += ["", f"## Does the structural term depend on the price base? (grades A and B; |term| < {SMALL} pp counts as near zero)", ""]
    for grid in ["A", "B"]:
        a = agree[(agree["grid"] == grid) & agree["grade"].isin(["A", "B"])]
        t = a.groupby("agreement").size().reindex(["positive at all three", "negative at all three", "near zero at all three",
                                                   "same sign, size differs", "sign depends on price base"]).fillna(0).astype(int)
        L += [f"**Grid {grid}** ({len(a)} country-periods): " + "; ".join(f"{k}: {v}" for k, v in t.items()), ""]
    a = agree[(agree["grid"] == "A") & agree["grade"].isin(["A", "B"]) & (agree["period"] == "2000–2019")]
    L += ["### Grid A, 2000–2019, by country", "",
          "| Country | Grade | Chained | Initial-year | Final-year | Verdict |", "|---|---|---|---|---|---|"]
    for _, r in a.sort_values("struct_pp").iterrows():
        L.append(f"| {r['country']} | {r['grade']} | {f(r['struct_pp'])} | {f(r['struct_initial'])} | {f(r['struct_final'])} | {r['agreement']} |")
    L += ["", "## Pooled LAC sectors (grid A): employment share, value-added share (current US$) and relative productivity (economy = 100)", "",
          "| Sector | " + " | ".join(f"{y} emp %" for y in sorted(sec['year'].unique())) + " | 2000 rel. LP | 2019 rel. LP | 2024 rel. LP |",
          "|---|" + "---|" * (len(sec['year'].unique()) + 3)]
    for s, g in sec.groupby("sector"):
        g = g.set_index("year")
        L.append(f"| {SHORT[s]} | " + " | ".join(f(g.loc[y, 'emp_share'], 1) for y in sorted(sec['year'].unique()))
                 + f" | {f(g.loc[2000,'rel_lp'],0)} | {f(g.loc[2019,'rel_lp'],0)} | {f(g.loc[2024,'rel_lp'],0)} |")
    c = contrib[(contrib["grid"] == "A")]
    L += ["", "## Pooled LAC sector contributions, grid A, chained (pp/yr)", "",
          "| Period | " + " | ".join(SHORT[s] + " (within / structural)" for s in ["AGR", "MIU", "MAN", "CON", "TRH", "TSC", "OTH"]) + " |",
          "|---|" + "---|" * 7]
    for per, g in c.groupby("period", sort=False):
        g = g.set_index("sector")
        L.append(f"| {per} | " + " | ".join(f"{f(g.loc[s,'within'])} / {f(g.loc[s,'struct'])}" for s in ["AGR", "MIU", "MAN", "CON", "TRH", "TSC", "OTH"]) + " |")
    (OUT / "summary.md").write_text("\n".join(L) + "\n")


def figures(pooled, agree, sec):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
    C_WITHIN, C_STATIC, C_DYNAMIC = "#2a78d6", "#eb6834", "#1baf7a"
    SECTOR_COLORS = {"AGR": "#2a78d6", "MIU": "#eb6834", "MAN": "#1baf7a", "CON": "#eda100",
                     "TRH": "#e87ba4", "TSC": "#008300", "OTH": "#6250d6"}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#c3c2b7",
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.spines.top": False, "axes.spines.right": False})

    # Fig 1: pooled LAC, Latin America, Caribbean by period, grid A, chained
    per = ["1991–2000", "2000–2008", "2008–2019", "2019–2024"]
    x = pooled[(pooled["grid"] == "A") & (pooled["base"] == "chained") & pooled["period"].isin(per)]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
    for ax, gname in zip(axes, ["LAC", "Latin America", "Caribbean"]):
        g = x[x["group"] == gname].set_index("period").loc[per]
        pos = np.arange(len(per))
        for col, c, lab in [("within", C_WITHIN, "Within-sector"), ("static", C_STATIC, "Structural: static"),
                            ("dynamic", C_DYNAMIC, "Structural: dynamic")]:
            v = g[col].values
            base = np.zeros(len(v))
            if col == "static":
                base = np.where(v >= 0, np.maximum(g["within"].values, 0), np.minimum(g["within"].values, 0))
            if col == "dynamic":
                base = np.where(v >= 0, np.maximum(g["within"].values, 0) + np.maximum(g["static"].values, 0),
                                np.minimum(g["within"].values, 0) + np.minimum(g["static"].values, 0))
            ax.bar(pos, v, bottom=base, width=0.62, color=c, label=lab, edgecolor="white", linewidth=1)
        ax.scatter(pos, g["growth"], marker="D", s=26, color=INK2, zorder=3, label="Total", edgecolors="white", linewidths=0.8)
        ax.axhline(0, color="#c3c2b7", lw=0.8)
        ax.set_xticks(pos, [p.replace("–", "–\n") for p in per])
        ax.set_title(gname + (f" ({int(g['n_countries'].iloc[0])})"), loc="left", fontsize=10, color=INK)
        ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
    axes[0].set_ylabel("pp per year")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT / "fig1_pooled.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    # Fig 2: structural term 2000–2019 across price bases, grid A, grades A/B
    a = agree[(agree["grid"] == "A") & agree["grade"].isin(["A", "B"]) & (agree["period"] == "2000–2019")]
    a = a[a["iso3"] != "GUY"].sort_values("struct_pp")
    fig, ax = plt.subplots(figsize=(6.4, 0.24 * len(a) + 0.9))
    yy = np.arange(len(a))
    lo = a[["struct_pp", "struct_initial", "struct_final"]].min(axis=1)
    hi = a[["struct_pp", "struct_initial", "struct_final"]].max(axis=1)
    ax.hlines(yy, lo, hi, color="#c3c2b7", lw=2)
    ax.scatter(a["struct_initial"], yy, marker="D", s=22, color=C_STATIC, label="Initial-year prices", zorder=3, edgecolors="white", linewidths=0.6)
    ax.scatter(a["struct_final"], yy, marker="s", s=22, color=C_DYNAMIC, label="Final-year prices", zorder=3, edgecolors="white", linewidths=0.6)
    ax.scatter(a["struct_pp"], yy, marker="o", s=34, color=C_WITHIN, label="Chained", zorder=4, edgecolors="white", linewidths=0.8)
    ax.axvline(0, color=MUTED, lw=0.8)
    short = {"Bolivia (Plurinational State of)": "Bolivia (Plur. State of)",
             "Venezuela (Bolivarian Republic of)": "Venezuela (Bol. Rep. of)"}
    ax.set_yticks(yy, [f"{short.get(c, c)} ({g})" for c, g in zip(a["country"], a["grade"])])
    ax.set_xlabel("structural-change term, 2000–2019, pp per year")
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.4, 1.0), ncol=3, fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "fig2_agreement.png", dpi=180, bbox_inches="tight"); plt.close(fig)

    # Fig 3: pooled LAC, change in employment share 2000–2019 vs log relative productivity 2000
    s0 = sec[sec["year"] == 2000].set_index("sector"); s1 = sec[sec["year"] == 2019].set_index("sector")
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    for s in s0.index:
        xv, yv = np.log(s0.loc[s, "rel_lp"] / 100), s1.loc[s, "emp_share"] - s0.loc[s, "emp_share"]
        ax.scatter(xv, yv, s=20 + 12 * s0.loc[s, "emp_share"], color=SECTOR_COLORS[s], edgecolors="white", linewidths=1.5, zorder=3)
        ax.annotate(SHORT[s], (xv, yv), xytext=(6, 4), textcoords="offset points", fontsize=8, color=INK2)
    ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlabel("ln(sector productivity / economy average), 2000 (current US$)")
    ax.set_ylabel("change in employment share, 2000–2019 (pp)")
    ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(OUT / "fig3_sectors.png", dpi=180, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    main()
