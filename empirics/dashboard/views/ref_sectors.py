"""Reference analysis: sectors and structural change (ECLAC charts I.7–I.10)."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (CARIB, COUNTRIES, INK2, SECTOR_COLORS, SHORT, annual_decomp, base_layout,
                 footer, name, sector_long, sector_lp, show, sidebar_common)

grid, series, agg = sidebar_common(key="rs")
st.title("Sectors and structural change")
st.caption("Reference format: ECLAC charts I.7 (relative productivity and employment share), I.8 (sector "
           "productivity trends), I.9 (sector contributions to the within component) and I.10 (sector "
           "contributions to the between component).")

df = sector_long(grid, series, tuple(agg) if agg else None)
who = st.selectbox("Economy", [CARIB] + list(COUNTRIES), format_func=name, index=0 if agg else 1)
d = sector_lp(df[df["iso3"] == who])
if d.empty:
    st.warning("No data for this selection.")
    st.stop()
years = sorted(d["year"].unique())

# ---- I.7 relative productivity and employment share (variable-width bars)
st.subheader("Relative productivity and share of employment, by sector")
yr = st.select_slider("Year", years, value=years[-1], key="rel_year")
x = d[d["year"] == yr].sort_values("rel", ascending=True)  # ladder: low to high productivity
x["w"] = 100 * x["share"]
x["left"] = x["w"].cumsum() - x["w"]
fig = go.Figure()
for _, r in x.iterrows():
    fig.add_trace(go.Bar(x=[r["left"] + r["w"] / 2], y=[r["rel"]], width=[max(r["w"] - 0.4, r["w"] * 0.6)],
                         marker=dict(color=SECTOR_COLORS[r["sector"]], cornerradius=4),
                         name=SHORT[r["sector"]],
                         hovertemplate=f"{SHORT[r['sector']]}<br>Relative productivity: {r['rel']:.0f}"
                                       f"<br>Employment share: {r['w']:.1f}%<extra></extra>"))
fig.add_hline(y=100, line=dict(color=INK2, width=1, dash="dot"),
              annotation_text="Economy average = 100", annotation_position="top right")
base_layout(fig, xtitle="Cumulative share of employment (%)", ytitle="Relative productivity per worker (economy = 100)")
fig.update_xaxes(range=[0, 100])
fig.update_layout(bargap=0)
show(fig, x.assign(sector=x["sector"].map(SHORT), employment_share=x["w"].round(1),
                   relative_productivity=x["rel"].round(0))[["sector", "relative_productivity", "employment_share"]],
     caption="Bar width = share of employment; height = sector productivity relative to the economy (100). "
             "Wide, low bars show where most workers are in low-productivity activities.")

# ---- I.8 sector productivity trend, index
st.subheader("Productivity trend by sector")
b = st.select_slider("Base year (= 100)", years, value=2005 if 2005 in years else years[0], key="base")
t = d.pivot_table(index="year", columns="sector", values="lp")
idx = 100 * t / t.loc[b]
tot = d.groupby("year")["lp_total"].first()
idx["TOTAL"] = 100 * tot / tot.loc[b]
fig = go.Figure()
for s in [c for c in idx.columns if c != "TOTAL"]:
    fig.add_trace(go.Scatter(x=idx.index, y=idx[s], mode="lines", name=SHORT[s],
                             line=dict(color=SECTOR_COLORS[s], width=2),
                             hovertemplate=f"{SHORT[s]}<br>%{{x}}: %{{y:.0f}}<extra></extra>"))
fig.add_trace(go.Scatter(x=idx.index, y=idx["TOTAL"], mode="lines", name="Total economy",
                         line=dict(color=INK2, width=3, dash="dot"),
                         hovertemplate="Total<br>%{x}: %{y:.0f}<extra></extra>"))
base_layout(fig, ytitle=f"Index, {b} = 100")
show(fig, idx.round(1).reset_index())

# ---- I.9 and I.10 annual contributions by sector
st.subheader("Sector contributions to the annual change in productivity")
dec, det = annual_decomp(grid, series, tuple(agg) if agg else None)
det = det[det["iso3"] == who]
yrs = sorted(det["year"].unique())
if not yrs:
    st.info("No consecutive years available for this selection.")
    st.stop()
y2 = st.select_slider("Year (change from the previous year)", yrs, value=yrs[-1], key="contrib_year")
c = det[det["year"] == y2].copy()
c["label"] = c["sector"].map(SHORT)
c = c.sort_values("s1")
c["pos"] = ["top center" if i % 2 == 0 else "bottom center" for i in range(len(c))]
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Within-sector component** — productivity change in each sector against its employment share")
    fig = go.Figure()
    for _, r in c.iterrows():
        fig.add_trace(go.Scatter(x=[100 * r["s1"]], y=[(r["p1"] - r["p0"]) / 1000], mode="markers+text",
                                 text=[r["label"]], textposition=r["pos"], textfont=dict(size=11, color=INK2),
                                 marker=dict(size=12, color=SECTOR_COLORS[r["sector"]], line=dict(color="white", width=2)),
                                 name=r["label"], showlegend=False,
                                 hovertemplate=f"{r['label']}<br>Share {100*r['s1']:.1f}%<br>Δp {(r['p1']-r['p0'])/1000:.2f}k"
                                               f"<br>Contribution {r['within']/1000:.2f}k<extra></extra>"))
    base_layout(fig, xtitle=f"Share of employment in {y2} (%)",
                ytitle="Δ productivity per worker (k 2020 US$)", legend=False, height=440)
    w = c["within"].sum()
    show(fig, c.assign(contribution_k=(c["within"] / 1000).round(3),
                       pct_of_within=(100 * c["within"] / w).round(0) if w else np.nan)[["label", "contribution_k", "pct_of_within"]],
         caption=f"Within component in {y2}: {w/1000:.2f}k. Contribution of a sector = previous-year share × change in productivity.")
with c2:
    st.markdown("**Structural-change component** — change in employment share against productivity level")
    fig = go.Figure()
    for _, r in c.iterrows():
        fig.add_trace(go.Scatter(x=[100 * (r["s1"] - r["s0"])], y=[r["p1"] / 1000], mode="markers+text",
                                 text=[r["label"]], textposition="top center", textfont=dict(size=11, color=INK2),
                                 marker=dict(size=10 + 60 * np.sqrt(r["s1"]), color=SECTOR_COLORS[r["sector"]],
                                             opacity=0.85, line=dict(color="white", width=2)),
                                 name=r["label"], showlegend=False,
                                 hovertemplate=f"{r['label']}<br>Δshare {100*(r['s1']-r['s0']):.2f} pp<br>Productivity "
                                               f"{r['p1']/1000:.1f}k<br>Contribution {r['struct']/1000:.2f}k<extra></extra>"))
    fig.add_vline(x=0, line=dict(color="#c3c2b7", width=1))
    base_layout(fig, xtitle="Annual change in share of employment (pp)",
                ytitle=f"Productivity level in {y2} (thousand 2020 US$)", legend=False, height=440)
    s = c["struct"].sum()
    show(fig, c.assign(contribution_k=(c["struct"] / 1000).round(3))[["label", "contribution_k"]],
         caption=f"Structural-change component in {y2}: {s/1000:.2f}k. Bubble size = share of employment. "
                 "Contribution = final productivity × change in share.")
if series == "model":
    st.caption("Annual changes in employment shares from the ILO modelled series are interpolated between survey "
               "years. See *Annual decomposition, additive prices* for which years are survey-based.")
footer()
