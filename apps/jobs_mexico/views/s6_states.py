"""Study 9.6: where workers move up."""
import json

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from jobs_lib import C_CONTEXT, C_HIGHLIGHT, INK2, MUTED, OUT, TYPE_COLORS, base_layout, footer, load, show

st.title("9.6 Job mobility and growth across states")
st.markdown(
    "For each state, how often do workers move up within a year: from informal to formal employment, or into a "
    "better-paid type of job? Rates are adjusted for age, sex, schooling, sector and urban residence, so that states are "
    "compared at the same workforce composition. They rest on 2.8 million people followed for a year in ENOE, "
    "2005–2025. GDP is INEGI's state accounts (base 2018).")

st_ = load("states", "state_table")
if st_.empty:
    st.warning("No results: run `empirics/code/enoe/states/run_all.py` (needs the ENOE microdata).")
    st.stop()
sig = load("states", "signal")
gr = load("states", "growth")
p40 = gr[gr["role"] == "P40"].iloc[0]
per = sig[(sig["measure"] == "M1") & (sig["period"] == "2005-2011 vs 2012-2018")].iloc[0]
s1 = sig[(sig["measure"] == "M1") & (sig["period"] == "2005-2011") & (sig["kind"] == "adjusted")].iloc[0]
lo, hi = st_.loc[st_["M1_2005-2011"].idxmin()], st_.loc[st_["M1_2005-2011"].idxmax()]
st.info(
    f"In panels starting in 2005–2011, the adjusted one-year rate at which informally employed persons become formally "
    f"employed ranges from {100 * lo['M1_2005-2011']:.1f}% in {lo['name']} to {100 * hi['M1_2005-2011']:.1f}% in "
    f"{hi['name']}; sampling error accounts for about {100 * (1 - s1['signal_share']):.0f}% of the variance across states. "
    f"The correlation of state rates between the 2005–2011 and 2012–2018 panels is {per['corr']:.2f}. Across the 30 states "
    f"other than Campeche and Tabasco, the 2005–2011 rate has a Spearman correlation of {p40['rho']:.2f} (90% interval "
    f"{p40['lo90']:.2f} to {p40['hi90']:.2f}) with growth of GDP per person over 2012–2019; the correlation with growth over "
    "2005–2019 is close to zero. The correlations describe co-movement, not an effect of mobility on growth.")

MEAS = {"M1": "informal → formal within a year", "M2": "move to a better-paid type of job within a year",
        "M3": "exit to non-employment within a year"}
PER = ["2005-2011", "2012-2018", "2022-2025"]

# ---------------------------------------------------------------- map
st.subheader("Mobility by state")
c1, c2 = st.columns([3, 2])
m = c1.selectbox("Measure", list(MEAS), format_func=MEAS.get)
p = c2.select_slider("Panels starting in", PER, value="2005-2011")
geo = json.loads((OUT / "states" / "states.geojson").read_text())
col = f"{m}_{p}_eb"
x = st_.assign(loc=st_["ent"].map(lambda e: f"{e:02d}"))
fig = go.Figure(go.Choroplethmap(
    geojson=geo, locations=x["loc"], z=100 * x[col], featureidkey="id",
    colorscale=[[0, "#f5f4ef"], [1, C_HIGHLIGHT if m != "M3" else TYPE_COLORS["informal"]]],
    marker_line_color="#ffffff", marker_line_width=0.6, colorbar=dict(thickness=10, len=0.7, title="%"),
    customdata=np.column_stack([x["name"], 100 * x[f"{m}_{p}"]]),
    hovertemplate="%{customdata[0]}: %{customdata[1]:.1f}%<extra></extra>"))
fig.update_layout(height=470, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)",
                  map=dict(style="white-bg", center=dict(lon=-102.3, lat=23.8), zoom=3.9))
show(fig, x[["name", f"{m}_{p}", col]].sort_values(f"{m}_{p}", ascending=False).round(4), key="statemap",
     caption="Adjusted rates at the national average composition; colours use empirical-Bayes estimates, which here "
             "differ little from the raw estimates because state samples are large. Boundaries dissolved from "
             "CONABIO/INEGI 2020 municipal boundaries.")

# ---------------------------------------------------------------- persistence
st.subheader("Persistence of state rates")
a, b = st.columns(2)
pa = a.selectbox("Earlier panels", PER[:2], index=0)
pb = b.selectbox("Later panels", PER[1:], index=0 if pa == "2005-2011" else 1)
fig = go.Figure(go.Scatter(x=100 * st_[f"{m}_{pa}"], y=100 * st_[f"{m}_{pb}"], mode="markers+text", text=st_["state"],
                           textposition="top center", textfont=dict(size=10, color=INK2),
                           marker=dict(color=C_HIGHLIGHT, size=8),
                           hovertemplate="%{text}: %{x:.1f}% → %{y:.1f}%<extra></extra>"))
lim = [100 * min(st_[f"{m}_{pa}"].min(), st_[f"{m}_{pb}"].min()) - 1,
       100 * max(st_[f"{m}_{pa}"].max(), st_[f"{m}_{pb}"].max()) + 1]
fig.add_trace(go.Scatter(x=lim, y=lim, mode="lines", line=dict(color=MUTED, dash="dot"), hoverinfo="skip", showlegend=False))
base_layout(fig, xtitle=f"{MEAS[m]}, panels {pa}, %", ytitle=f"panels {pb}, %", height=440, legend=False)
r = np.corrcoef(st_[f"{m}_{pa}"], st_[f"{m}_{pb}"])[0, 1]
show(fig, st_[["state", f"{m}_{pa}", f"{m}_{pb}"]].round(4),
     caption=f"Correlation across states: {r:.2f}. Dotted line: no change.")

# ---------------------------------------------------------------- growth
st.subheader("Mobility and growth of GDP per person")
oil = st.toggle("Include Campeche and Tabasco (non-oil GDP)", value=False)
yv = "g_nonoil_2012_2019" if oil else "g_2012_2019"
g = st_ if oil else st_[~st_["ent"].isin([4, 27])]
g = g.dropna(subset=[yv]) if yv in g else g
if yv not in st_:
    st.caption("Non-oil growth not available in this output.")
else:
    fig = go.Figure(go.Scatter(x=100 * g["M1_2005-2011"], y=100 * g[yv], mode="markers+text", text=g["state"],
                               textposition="top center", textfont=dict(size=10, color=INK2),
                               marker=dict(color=C_HIGHLIGHT, size=8),
                               hovertemplate="%{text}: %{x:.1f}%, %{y:+.2f}% a year<extra></extra>"))
    b1, b0 = np.polyfit(100 * g["M1_2005-2011"], 100 * g[yv], 1)
    xs = np.array([100 * g["M1_2005-2011"].min(), 100 * g["M1_2005-2011"].max()])
    fig.add_trace(go.Scatter(x=xs, y=b0 + b1 * xs, mode="lines", line=dict(color=MUTED, dash="dot"), hoverinfo="skip"))
    base_layout(fig, xtitle="informal → formal within a year, panels 2005–2011, % (adjusted)",
                ytitle=("non-oil " if oil else "") + "GDP per person, growth 2012–2019, % a year", height=460, legend=False)
    show(fig, g[["state", "M1_2005-2011", yv, "lgdppc_2012", "formal_2005_2011"]].round(4),
         caption="Each point is a state. Dotted line: least-squares fit, for reference; the test is a rank correlation.")
gt = gr[gr["role"] != "descriptive"][["test", "states", "rho", "lo90", "hi90"]].round(3)
st.dataframe(gt, hide_index=True, width="stretch")
st.caption("Spearman rank correlations with 90% intervals from 1,999 bootstrap resamples of states. The first row is the "
           "test set in the pre-analysis plan; the non-oil row was added after it. Over 2005–2019 as a whole there is no "
           "relation, which shows how much a correlation across 30 states depends on the window.")
footer("ENOE 2005–2026; INEGI, PIB por Entidad Federativa, base 2018. Method: devtheory WP09, study 9.6.")
