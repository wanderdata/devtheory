"""Study 9.3: a productivity ladder for Mexico with formal and informal steps."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from jobs_lib import C_CONTEXT, C_HIGHLIGHT, INK2, MUTED, TYPE_COLORS, base_layout, footer, load, show

st.title("9.3 A productivity ladder for Mexico")
st.markdown(
    "WP08 places every person aged 15 and over at the output per worker of the sector they work in, with people not "
    "employed at zero, and asks whether the resulting distribution improved over time. For Mexico, with one step per "
    "sector, no period since 2000 shows an unambiguous change. This page splits each sector into **formal and "
    "informal** workers. National-accounts value added is allocated between them in proportion to their labour "
    "income from ENOE, raised to a power θ (θ = 1: productivity differs as income does), keeping each sector's "
    "total unchanged.")

v = load("productivity_ladder", "verdicts")
if v.empty:
    st.warning("No results: run `empirics/code/enoe/productivity_ladder/run_all.py` (needs the ENOE microdata).")
    st.stop()
d = load("productivity_ladder", "decomposition")
dm = d[(d["spec"] == "sector x formality, theta 1") & (d["period"] == "2005–2019")].iloc[0]
st.info(
    "**Results.** Splitting sectors into formal and informal steps changes no verdict, in any period or "
    "specification (the pre-registered expectation that it would make them worse is rejected). It does change the "
    "decomposition: between 2005 and 2019 the movement of workers from informal to formal work within sectors added "
    f"{dm['between_within_sector_pp']:+.2f} percentage points a year to output per worker, while productivity within "
    f"the formal and informal segments fell by {-dm['within_pp']:.2f} points a year, faster than the sector "
    f"figures ({-dm['within_sector_level_pp']:.2f} a year) indicate.")

# ---- verdicts
st.subheader("Verdicts")
tab = v[v["base"] == "initial"].pivot(index="spec", columns="period", values="verdict")
tab = tab.loc[[x for x in dict.fromkeys(v["spec"])], [p for p in dict.fromkeys(v["period"])]]
st.dataframe(tab.reset_index(), hide_index=True, width="stretch")
st.caption("A verdict requires agreement at initial- and final-year prices. 'Improvement, weighting the lower "
           "percentiles' means second-order stochastic dominance; 'ambiguous' means the ladders cross.")

# ---- ladder
st.subheader("The ladder")
lr = load("productivity_ladder", "ladders")
c1, c2, c3 = st.columns([2, 2, 1])
per = c1.selectbox("Period", list(dict.fromkeys(lr["period"])), index=3)
specs = ["sector only"] + [s for s in dict.fromkeys(lr["spec"]) if s != "sector only"]
spec = c2.selectbox("Steps", specs, index=specs.index("sector x formality, theta 1"))
base = c3.radio("Prices", ["initial", "final"], format_func=lambda b: f"{b}-year")
x = lr[(lr["period"] == per) & (lr["spec"] == spec) & (lr["base"] == base)]
years = sorted(x["year"].unique())
fig = go.Figure()
for yr, col in zip(years, [C_CONTEXT, C_HIGHLIGHT]):
    g = x[x["year"] == yr].sort_values("value")
    pop = g["pop15"].iloc[0]
    zero = 1 - g["emp"].sum() / pop
    xs, ys, cum = [0.0, 100 * zero], [0.0, 0.0], zero
    labels = []
    for _, r in g.iterrows():
        xs += [100 * cum, 100 * (cum + r["emp"] / pop)]
        ys += [r["value"] / 1000] * 2
        labels.append((100 * (cum + r["emp"] / pop / 2), r["value"] / 1000, r["segment"], r["emp"] / pop))
        cum += r["emp"] / pop
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=2.5), name=str(yr), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[a for a, *_ in labels], y=[b for _, b, *_ in labels], mode="markers",
                             marker=dict(color=col, size=6), showlegend=False,
                             customdata=[[s.replace("|", " · "), 100 * w] for *_, s, w in labels],
                             hovertemplate=f"{yr}: %{{customdata[0]}}<br>%{{customdata[1]:.1f}}% of the population "
                                           "aged 15+<br>US$ %{y:.1f}k per worker<extra></extra>"))
cap = sorted(x["value"] / 1000)
ymax = cap[-3] * 1.3 if len(cap) > 3 else cap[-1] * 1.1
base_layout(fig, xtitle="cumulative share of the population aged 15+ (%)",
            ytitle=f"output per worker, US$ thousand ({years[0] if base == 'initial' else years[-1]} prices)", height=460)
fig.update_xaxes(range=[0, 100])
fig.update_yaxes(range=[0, ymax])
show(fig, x[["year", "segment", "emp", "value"]].assign(value=lambda t: (t["value"] / 1000).round(2)),
     caption="The flat stretch at zero is the population aged 15+ not employed. Mining and utilities, the highest "
             "step, is above the axis. Employment: ENOE, average of four quarters; value added: UN National "
             "Accounts Main Aggregates.")

# ---- decomposition
st.subheader("Where output per worker changed")
th = st.radio("Width of the within-sector gap", ["sector x formality, theta 0.5", "sector x formality, theta 1",
                                                 "sector x formality, theta 1.5", "sector x formality, theta 2",
                                                 "sector x formality, medians"], index=1, horizontal=True,
              format_func=lambda s: s.replace("sector x formality, ", ""))
dd = d[d["spec"] == th]
fig = go.Figure()
for col, lab, color in [("within_pp", "within formal and informal segments", C_HIGHLIGHT),
                        ("between_within_sector_pp", "between formal and informal within sectors", TYPE_COLORS["informal"]),
                        ("between_sector_pp", "between sectors", INK2)]:
    fig.add_trace(go.Bar(x=dd["period"], y=dd[col], name=lab, marker=dict(color=color),
                         hovertemplate="%{x}: %{y:+.3f}<extra>" + lab + "</extra>"))
fig.add_trace(go.Scatter(x=dd["period"], y=dd["growth_pp"], mode="markers", name="total",
                         marker=dict(color="#0b0b0b", size=10, symbol="diamond")))
base_layout(fig, ytitle="percentage points a year", height=400)
fig.update_layout(barmode="relative")
show(fig, dd[["period", "growth_pp", "within_pp", "between_within_sector_pp", "between_sector_pp",
              "within_sector_level_pp", "emprate_log_pp"]].round(3),
     caption="McMillan–Rodrik decomposition of the growth of output per employed worker on formal and informal "
             "segments (initial-year prices). The 'between formal and informal' term is reallocation that a "
             "sector-level decomposition counts as within-sector productivity growth (data table: "
             "'within_sector_level_pp').")

# ---- segments
st.subheader("Informality and income gaps by sector")
s = load("productivity_ladder", "segments")
inf = s[s["formality"] == "informal"]
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Informal share of sector employment**")
    st.dataframe(inf.pivot(index="sector", columns="year", values="informal_share").round(3).rename(columns=str).reset_index(),
                 hide_index=True, width="stretch")
with c2:
    st.markdown("**Informal / formal mean monthly labour income**")
    st.dataframe(inf.pivot(index="sector", columns="year", values="informal_formal_ratio").round(3).rename(columns=str).reset_index(),
                 hide_index=True, width="stretch")
st.caption("Sectors: AGR agriculture; MIU mining and utilities; MAN manufacturing; CON construction; TRH trade, "
           "restaurants and hotels; TSC transport, storage and communications; OTH finance, business, government "
           "and personal services.")
footer("Four-quarter averages for 2005, 2008, 2019 and 2024; UN National Accounts Main Aggregates. Method: devtheory "
       "WP09, study 9.3, extending WP08.")
