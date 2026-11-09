"""Baseline analysis: employment."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (countries, C_CONTEXT, C_HIGHLIGHT, C_STRUCT, C_WITHIN, INK2, base_layout,
                 footer, labour_or_note, name, show)

st.title("Employment")
st.caption("Productivity and employment together: the employment rate, its split into participation and "
           "unemployment, and how productivity and employment moved jointly. Source: ILO modelled estimates, "
           "population aged 15+.")

lab = labour_or_note(["emp_rate", "part_rate", "unemp_rate", "lp_hour"])
if lab is None:
    st.stop()
w = lab.pivot_table(index=["iso3", "year"], columns="indicator", values="value").reset_index()
w = w[w["iso3"].isin(countries())]
years = sorted(w.dropna(subset=["lp_hour"])["year"].unique())

# ---- quadrant
st.subheader("Productivity and employment: annual change")
yr = st.select_slider("Year", years[1:], value=years[-1])
a = w[w["year"] == yr - 1].set_index("iso3")
b = w[w["year"] == yr].set_index("iso3")
q = pd.DataFrame({"d_lp": 100 * (b["lp_hour"] / a["lp_hour"] - 1),
                  "d_emp": 100 * (b["emp_rate"] / a["emp_rate"] - 1)}).dropna()
q["income"] = q["d_lp"] + q["d_emp"]
fig = go.Figure()
fig.add_trace(go.Scatter(x=q["d_emp"], y=q["d_lp"], mode="markers+text", text=[name(i) for i in q.index],
                         textposition="top center", textfont=dict(size=11, color=INK2),
                         marker=dict(size=10, color=C_HIGHLIGHT, line=dict(color="white", width=2)),
                         hovertemplate="%{text}<br>Employment rate %{x:.1f}%<br>Productivity per hour %{y:.1f}%<extra></extra>"))
fig.add_hline(y=0, line=dict(color="#c3c2b7")); fig.add_vline(x=0, line=dict(color="#c3c2b7"))
base_layout(fig, xtitle="Change in the employment rate (%)", ytitle="Change in productivity per hour (%)",
            legend=False, height=500)
show(fig, q.round(2).reset_index().assign(iso3=lambda d: d["iso3"].map(name)).rename(
         columns={"iso3": "country", "d_lp": "productivity_per_hour_%", "d_emp": "employment_rate_%",
                  "income": "approx_contribution_to_income_per_capita_%"}),
     caption="Top right: both rose, so income per head rose (holding the working-age share constant). Bottom left: both fell. "
             "The other two quadrants depend on which change was larger.")

# ---- employment rate
st.subheader("Employment rate")
focus = st.selectbox("Highlight", list(countries()), format_func=name, index=list(countries()).index("DOM"))
def lines(col, ytitle, key):
    fig = go.Figure()
    for iso, g in w.dropna(subset=[col]).groupby("iso3"):
        hi = iso == focus
        fig.add_trace(go.Scatter(x=g["year"], y=g[col], mode="lines", name=name(iso), showlegend=False,
                                 line=dict(color=C_HIGHLIGHT if hi else C_CONTEXT, width=2.5 if hi else 1),
                                 hovertemplate=f"{name(iso)}<br>%{{x}}: %{{y:.1f}}%<extra></extra>"))
    g = w[w["iso3"] == focus].dropna(subset=[col]).sort_values("year")
    if len(g):
        fig.add_annotation(x=g["year"].iloc[-1], y=g[col].iloc[-1], text=name(focus), showarrow=False,
                           xanchor="left", xshift=6, font=dict(color=INK2))
    base_layout(fig, ytitle=ytitle, legend=False, height=380)
    show(fig, w.pivot_table(index="year", columns="iso3", values=col).round(1).reset_index(), key=key)
lines("emp_rate", "Employed as % of population 15+", "er")

# ---- Shapley split
st.subheader("Change in the employment rate: participation and unemployment")
st.caption("e = p·(1 − u). Shapley split: participation contributes Δp·(average of 1−u); unemployment "
           "contributes −Δu·(average p). The two contributions add up exactly to Δe.")
yy = st.slider("Years", int(w["year"].min()) + 1, int(w["year"].max()), (int(w["year"].max()) - 2, int(w["year"].max())))
rows = []
for iso, g in w.groupby("iso3"):
    g = g.set_index("year")
    for y in range(yy[0], yy[1] + 1):
        if y - 1 in g.index and y in g.index:
            p0, p1 = g.loc[y - 1, "part_rate"] / 100, g.loc[y, "part_rate"] / 100
            u0, u1 = g.loc[y - 1, "unemp_rate"] / 100, g.loc[y, "unemp_rate"] / 100
            rows.append({"iso3": iso, "year": y,
                         "participation": 100 * (p1 - p0) * ((1 - u0) + (1 - u1)) / 2,
                         "unemployment": -100 * (u1 - u0) * (p0 + p1) / 2,
                         "d_emp_rate": 100 * (p1 * (1 - u1) - p0 * (1 - u0))})
sh = pd.DataFrame(rows)
who = st.selectbox("Country", list(countries()), format_func=name, index=list(countries()).index("DOM"), key="sh")
s = sh[sh["iso3"] == who]
fig = go.Figure()
fig.add_trace(go.Bar(x=s["year"].astype(str), y=s["participation"], name="Contribution of participation",
                     marker=dict(color=C_WITHIN), hovertemplate="%{x}: %{y:.2f} pp<extra>Participation</extra>"))
fig.add_trace(go.Bar(x=s["year"].astype(str), y=s["unemployment"], name="Contribution of unemployment",
                     marker=dict(color=C_STRUCT), hovertemplate="%{x}: %{y:.2f} pp<extra>Unemployment</extra>"))
fig.add_trace(go.Scatter(x=s["year"].astype(str), y=s["d_emp_rate"], mode="markers", name="Change in employment rate",
                         marker=dict(color=INK2, size=9, symbol="diamond", line=dict(color="white", width=1))))
base_layout(fig, ytitle="percentage points", height=380)
fig.update_layout(barmode="relative")
fig.update_xaxes(type="category")
show(fig, s.round(2))

# ---- unemployment and participation
st.subheader("Unemployment and participation rates")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Unemployment rate** (% of labour force)")
    lines("unemp_rate", "%", "ur")
with c2:
    st.markdown("**Participation rate** (% of population 15+)")
    lines("part_rate", "%", "pr")
footer()
