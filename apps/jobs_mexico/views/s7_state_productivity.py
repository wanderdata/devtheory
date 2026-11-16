"""Study 9.7: labour productivity growth by state and activity."""
import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from jobs_lib import C_CONTEXT, C_HIGHLIGHT, INK2, MUTED, OUT, TYPE_COLORS, base_layout, footer, load, show

st.title("9.7 Labour productivity growth by state and activity")
st.markdown(
    "This page decomposes the growth of non-oil labour productivity (value added at constant 2018 prices per "
    "employed person) in each state between 2005–2007 and 2017–2019 into growth within 20 activity groups and "
    "reallocation of employment between them, and asks whether productivity growth came with formalisation and "
    "with higher pay. Value added is from INEGI's state accounts (PIBE, base 2018) and informal value added from "
    "INEGI's informal-economy accounts by state (MEITEF); employment, hours, pay and formality are from ENOE. "
    "Mexico City and the State of Mexico are combined because many people live in one and work in the other.")

dec = load("state_productivity", "decomposition_units")
if dec.empty:
    st.warning("No results: run `empirics/code/enoe/state_productivity/run_all.py` (needs the ENOE microdata).")
    st.stop()
nat = load("state_productivity", "national").iloc[0]
t12 = load("state_productivity", "tests_p41_p42").set_index("proposition")
t3 = load("state_productivity", "tests_p43").iloc[0]
names = load("states", "state_table")[["ent", "name", "state"]] if not load("states", "state_table").empty else None
NAME = dict(zip(names["ent"], names["name"])) if names is not None else {}
SHORT = dict(zip(names["ent"], names["state"])) if names is not None else {}
NAME[9], SHORT[9] = "Mexico City and State of Mexico", "CDMX+Méx"
dec["name"] = dec["unit"].map(NAME)
dec["short"] = dec["unit"].map(SHORT)
r41, r42 = t12.loc["P41"], t12.loc["P42"]

st.info(
    f"National non-oil labour productivity grew by {100 * nat['national_growth']:.2f} log points a year between "
    f"2005–2007 and 2017–2019. Growth within activity groups contributed {100 * nat['within']:.2f} points and the "
    f"reallocation of employment between groups {100 * (nat['static'] + nat['dynamic']):.2f} points. "
    f"Of the {int(r41['units_positive_growth'])} units in which productivity grew, {int(r41['eligible_units'])} had growth "
    f"whose 90% interval excludes zero; within-activity growth exceeded reallocation in {int(r41['within_exceeds_realloc'])} "
    f"of them. Across the 31 units, the rank correlation between productivity growth and the change in the formal "
    f"share of employment is {r42['rho']:.2f} (90% interval {r42['lo']:.2f} to {r42['hi']:.2f}); estimated with "
    f"growth and formality from independent halves of the sample it is {r42['split_rho_a']:.2f} and "
    f"{r42['split_rho_b']:.2f}. Across unit × activity cells, a 1% faster growth of value added per hour is associated "
    f"with a {t3['slope']:.2f}% faster growth of the hourly product wage after correction for sampling error (90% "
    f"interval {t3['lo']:.2f} to {t3['hi']:.2f}). All of these are descriptive associations.")

# ---------------------------------------------------------------- map
st.subheader("Growth of non-oil labour productivity by state")
geo = json.loads((OUT / "states" / "states.geojson").read_text())
x = dec[["unit", "name", "growth", "growth_lo", "growth_hi"]].copy()
rows = []
for _, r in x.iterrows():
    for e in ([9, 15] if r["unit"] == 9 else [r["unit"]]):
        rows.append({"loc": f"{int(e):02d}", **r.to_dict()})
m = pd.DataFrame(rows)
lim = 100 * np.abs(m["growth"]).max()
fig = go.Figure(go.Choroplethmap(
    geojson=geo, locations=m["loc"], z=100 * m["growth"], featureidkey="id", zmin=-lim, zmax=lim,
    colorscale=[[0, TYPE_COLORS["informal"]], [0.5, "#f5f4ef"], [1, C_HIGHLIGHT]],
    marker_line_color="#ffffff", marker_line_width=0.6, colorbar=dict(thickness=10, len=0.7, title="% a year"),
    customdata=np.column_stack([m["name"], 100 * m["growth"], 100 * m["growth_lo"], 100 * m["growth_hi"]]),
    hovertemplate="%{customdata[0]}: %{customdata[1]:.2f}% a year (90% interval %{customdata[2]:.2f} to "
                  "%{customdata[3]:.2f})<extra></extra>"))
fig.update_layout(height=470, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)",
                  map=dict(style="white-bg", center=dict(lon=-102.3, lat=23.8), zoom=3.9))
show(fig, dec[["name", "growth", "growth_lo", "growth_hi"]].sort_values("growth", ascending=False).round(4),
     key="growthmap",
     caption="Log points a year, 2005–2007 to 2017–2019, non-oil value added per employed person aged 15+. Intervals "
             "are 90% percentile intervals over 199 bootstrap replications of ENOE sampling units, calibrated to state "
             "population; PIBE is treated as fixed.")

# ---------------------------------------------------------------- decomposition
st.subheader("Within-activity growth and reallocation")
seg = st.toggle("Show the formalisation term (segment-level decomposition)", value=False)
d = dec.sort_values("growth")
terms = ([("within_seg", "within formal and informal segments", C_HIGHLIGHT),
          ("realloc", "reallocation between activity groups", C_CONTEXT),
          ("formalisation", "reallocation from informal to formal segments", TYPE_COLORS["informal"])] if seg else
         [("within", "within activity groups", C_HIGHLIGHT), ("static", "static reallocation", C_CONTEXT),
          ("dynamic", "dynamic reallocation", MUTED)])
fig = go.Figure()
for col, lab, c in terms:
    fig.add_trace(go.Bar(y=d["short"], x=100 * d[col], name=lab, orientation="h", marker_color=c,
                         hovertemplate="%{y}: %{x:.2f}<extra>" + lab + "</extra>"))
fig.add_trace(go.Scatter(y=d["short"], x=100 * d["growth"], mode="markers", name="total growth",
                         marker=dict(color=INK2, size=7, symbol="diamond")))
fig.update_layout(barmode="relative")
base_layout(fig, xtitle="log points a year", height=760)
show(fig, d[["name", "growth"] + [t[0] for t in terms]].round(5),
     caption="Shift-share decomposition (within, static and dynamic terms as in WP05–WP08); the log growth is divided "
             "among the terms in proportion to their linear values. In the segment-level version informal value added "
             "is MEITEF's, divided among activity groups that share a MEITEF activity in proportion to ENOE informal "
             "labour income.")

# ---------------------------------------------------------------- formality
st.subheader("Productivity growth and the change in the formal share")
fig = go.Figure(go.Scatter(x=100 * dec["growth"], y=100 * dec["d_formal_share"], mode="markers+text",
                           text=dec["short"], textposition="top center", textfont=dict(size=10, color=INK2),
                           marker=dict(color=C_HIGHLIGHT, size=8),
                           hovertemplate="%{text}: %{x:.2f}% a year, %{y:+.1f} pp<extra></extra>"))
base_layout(fig, xtitle="non-oil labour productivity, growth 2005–2007 to 2017–2019, % a year",
            ytitle="change in the formal share of employment, pp", height=460, legend=False)
show(fig, dec[["name", "growth", "d_formal_share", "formal_share_0"]].round(4),
     caption=f"Spearman ρ = {r42['rho']:.2f} (90% interval {r42['lo']:.2f} to {r42['hi']:.2f}, 1,999 resamples of units). "
             "Both variables use ENOE employment, so common sampling error could create a correlation; with growth and "
             f"formality from independent halves of the sample, ρ = {r42['split_rho_a']:.2f} and {r42['split_rho_b']:.2f}.")

# ---------------------------------------------------------------- pass-through
st.subheader("Productivity and the product wage across state × activity cells")
pc = load("state_productivity", "passthrough_cells")
if not pc.empty:
    fig = go.Figure(go.Scatter(x=100 * pc["dx"] / 12, y=100 * pc["dy"] / 12, mode="markers",
                               marker=dict(color=C_HIGHLIGHT, size=np.sqrt(pc["emp0"] / pc["emp0"].max()) * 22 + 3,
                                           opacity=0.55),
                               text=pc["group"] + ", " + pc["unit"].map(SHORT),
                               hovertemplate="%{text}: %{x:.2f}, %{y:.2f}<extra></extra>"))
    base_layout(fig, xtitle="value added per hour, growth, % a year", ytitle="hourly product wage, growth, % a year",
                height=460, legend=False)
    show(fig, pc.round(4),
         caption=f"{int(t3['cells'])} cells with at least 100 earnings respondents in each period; marker area "
                 f"proportional to initial employment. Slope with unit and group fixed effects, weighted: "
                 f"{t3['slope_uncorrected']:.2f}; corrected for sampling error in the regressor (reliability "
                 f"{t3['reliability']:.2f}): {t3['slope']:.2f} (90% interval {t3['lo']:.2f} to {t3['hi']:.2f}). The "
                 "product wage deflates hourly labour income by the PIBE price index of the state and activity.")

footer("ENOE 2005–2024; INEGI, PIB por Entidad Federativa and Mediciones de la Economía Informal Trimestral por "
       "Entidad Federativa, base 2018. Method: devtheory WP09, study 9.7.")
