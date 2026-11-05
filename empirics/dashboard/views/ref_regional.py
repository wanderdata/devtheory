"""Baseline analysis: regional productivity."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (CARIB, COUNTRIES, C_CONTEXT, C_HIGHLIGHT, C_STRUCT, C_WITHIN, INK2,
                 aggregate_lp, annual_decomp, base_layout, footer, load_labour, name,
                 sector_long, show, sidebar_common)

grid, series, agg = sidebar_common(key="rr")
st.title("Regional productivity")
st.caption("Labour productivity levels, ranking and annual change, and the McMillan–Rodrik split of each "
           "year's change into within-sector and structural-change components.")

df = sector_long(grid, series, tuple(agg) if agg else None)
lp = aggregate_lp(df)
lab = load_labour()
has_hour = lab is not None and "lp_hour" in set(lab["indicator"])

measure = st.radio("Productivity measure", ["Per worker (constant 2020 US$)", "Per hour (constant 2021 PPP$, ILO)"],
                   horizontal=True, index=0)
per_hour = measure.startswith("Per hour")
if per_hour and not has_hour:
    st.info("**Data pending.** Output per hour needs ILO `GDP_2HRW_NOC_NB_A`; showing per worker instead.")
    per_hour = False
if per_hour:
    lv = lab[lab["indicator"] == "lp_hour"].rename(columns={"value": "lp"})[["iso3", "year", "lp"]]
    unit = "2021 PPP$ per hour"
else:
    lv = lp[["iso3", "year", "lp"]]
    unit = "constant 2020 US$ per worker"

# ---- level over time
st.subheader("Labour productivity over time")
focus = st.selectbox("Highlight", [CARIB] + list(COUNTRIES), format_func=name,
                     index=0 if (not per_hour and agg) else 1)
fig = go.Figure()
for iso, g in lv.groupby("iso3"):
    if iso == focus or iso == CARIB:
        continue
    fig.add_trace(go.Scatter(x=g["year"], y=g["lp"], mode="lines", line=dict(color=C_CONTEXT, width=1),
                             name=name(iso), showlegend=False,
                             hovertemplate=f"{name(iso)}<br>%{{x}}: %{{y:,.0f}}<extra></extra>"))
g = lv[lv["iso3"] == focus]
if len(g):
    fig.add_trace(go.Scatter(x=g["year"], y=g["lp"], mode="lines", line=dict(color=C_HIGHLIGHT, width=2.5),
                             name=name(focus), hovertemplate=f"{name(focus)}<br>%{{x}}: %{{y:,.0f}}<extra></extra>"))
    last = g.sort_values("year").iloc[-1]
    fig.add_annotation(x=last["year"], y=last["lp"], text=name(focus) if focus != CARIB else "Caribbean",
                       showarrow=False, xanchor="left", xshift=6, font=dict(color=INK2))
base_layout(fig, ytitle=unit, legend=False)
show(fig, lv.pivot_table(index="year", columns="iso3", values="lp").round(0).reset_index(),
     caption="Grey lines: other countries. " + ("Aggregate pools the countries chosen in the sidebar." if not per_hour else ""))

# ---- ranking and annual change
c1, c2 = st.columns(2)
years = sorted(lv["year"].unique())
with c1:
    st.subheader("Ranking")
    yr = st.select_slider("Year", years, value=years[-1], key="rank_year")
    r = lv[(lv["year"] == yr) & (lv["iso3"] != CARIB)].sort_values("lp")
    fig = go.Figure(go.Bar(x=r["lp"], y=[name(i) for i in r["iso3"]], orientation="h",
                           marker=dict(color=C_HIGHLIGHT, cornerradius=4),
                           text=[f"{v:,.0f}" for v in r["lp"]], textposition="outside",
                           hovertemplate="%{y}: %{x:,.0f}<extra></extra>"))
    base_layout(fig, xtitle=unit, height=460, legend=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    show(fig, r.assign(country=[name(i) for i in r["iso3"]])[["country", "lp"]].round(0))
with c2:
    st.subheader("Annual change")
    y2 = st.select_slider("Latest year", years[1:], value=years[-1], key="chg_year")
    y1 = y2 - 1
    w = lv.pivot_table(index="iso3", columns="year", values="lp")
    ch = pd.DataFrame({f"{y1}": 100 * (w[y1] / w[y1 - 1] - 1) if y1 - 1 in w else None,
                       f"{y2}": 100 * (w[y2] / w[y1] - 1)}).dropna(how="all")
    ch = ch[ch.index != CARIB].sort_values(f"{y2}")
    fig = go.Figure()
    for col, color in [(f"{y1}", C_CONTEXT), (f"{y2}", C_HIGHLIGHT)]:
        fig.add_trace(go.Bar(y=[name(i) for i in ch.index], x=ch[col], name=col, orientation="h",
                             marker=dict(color=color, cornerradius=4),
                             hovertemplate="%{y}: %{x:.1f}%<extra>" + col + "</extra>"))
    base_layout(fig, xtitle="% change", height=460)
    fig.update_layout(barmode="group")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    show(fig, ch.round(1).reset_index().assign(iso3=lambda d: d["iso3"].map(name)).rename(columns={"iso3": "country"}))

# ---- components of the annual change
st.subheader("Within-sector and structural-change components of the annual change")
dec, _ = annual_decomp(grid, series, tuple(agg) if agg else None)
who = st.selectbox("Economy", [CARIB] + list(COUNTRIES), format_func=name, key="dec_who",
                   index=0 if agg else 1)
d = dec[dec["iso3"] == who].sort_values("year")
if series == "survey":
    st.caption("With survey employment, only consecutive survey years can be decomposed.")
fig = go.Figure()
fig.add_trace(go.Bar(x=d["year"], y=d["within"] / 1000, name="Within-sector component",
                     marker=dict(color=C_WITHIN, cornerradius=0), hovertemplate="%{x}: %{y:.2f}k<extra>Within</extra>"))
fig.add_trace(go.Bar(x=d["year"], y=d["struct"] / 1000, name="Structural-change (between) component",
                     marker=dict(color=C_STRUCT, cornerradius=0), hovertemplate="%{x}: %{y:.2f}k<extra>Between</extra>"))
fig.add_trace(go.Scatter(x=d["year"], y=(d["within"] + d["struct"]) / 1000, mode="markers", name="Total change",
                         marker=dict(color=INK2, size=8, symbol="diamond", line=dict(color="white", width=1)),
                         hovertemplate="%{x}: %{y:.2f}k<extra>Total</extra>"))
base_layout(fig, ytitle="thousand constant 2020 US$ per worker")
fig.update_layout(barmode="relative")
avg = d[["within", "struct"]].mean() / 1000
show(fig, d[["year", "within", "struct", "growth_pct"]].round(1),
     caption=f"Average {int(d['year'].min()) if len(d) else ''}–{int(d['year'].max()) if len(d) else ''}: "
             f"within {avg['within']:.2f}k, between {avg['struct']:.2f}k per year. McMillan–Rodrik (2011) "
             "decomposition: ΔP = Σ θᵢ,ₜ₋₁ Δpᵢ + Σ pᵢ,ₜ Δθᵢ, with sector value added at constant 2020 prices.")
footer()
