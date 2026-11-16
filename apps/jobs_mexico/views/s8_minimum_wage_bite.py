"""Study 9.8: the minimum-wage increases of 2019-2024 across states and activities."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from jobs_lib import C_CONTEXT, C_HIGHLIGHT, INK2, MUTED, TYPE_COLORS, base_layout, footer, load, show

st.title("9.8 Minimum-wage increases of 2019–2024 by state and activity")
st.markdown(
    "Mexico's general minimum wage rose from 88.36 pesos a day in 2018 to 248.93 in 2024. The increases reached a "
    "larger share of workers in some states and activities than in others. This page compares how wages, "
    "employment, formality and value added per worker changed in state × activity cells where, in 2018, more "
    "full-time wage employees earned less than the 2019 minimum (the bite), relative to cells in the same state and "
    "year and in the same activity and year. The comparisons are relative: they do not measure the aggregate effect "
    "of the increases.")

est = load("minimum_wage_bite", "estimates")
if est.empty:
    st.warning("No results: run `empirics/code/enoe/minimum_wage_bite/run_all.py` (needs the ENOE microdata).")
    st.stop()
tests = load("minimum_wage_bite", "tests").set_index("proposition")
ev = load("minimum_wage_bite", "event")
bite = load("minimum_wage_bite", "bite")
e = est.set_index("outcome")


def line(o, scale=10):
    r = e.loc[o]
    return (f"{r['post'] / scale:+.3f} (90% interval {r['lo90'] / scale:+.3f} to {r['hi90'] / scale:+.3f}; pre-trend "
            f"test p = {r['p_pretrend']:.2f})")


st.info(
    "Effects of 10 additional percentage points of bite, averaged over 2022–2024 relative to 2018: mean log hourly "
    f"wage of wage employees {line('w_all')}; log employment {line('lemp')}; formal share of employment "
    f"{line('formal')}; log value added per worker {line('lprod')}; mean log hourly wage of informal wage "
    f"employees {line('w_informal')}. The identifying assumption is that, without the increases, cells with higher "
    "and lower bites would have followed parallel paths after removing state × year and activity × year effects; "
    "the pre-trend tests check this for 2015–2017. The wage tests fail because 2018, the year in which the bite is "
    "measured from the same survey sample, stands out as low; with the bite measured in 2017 they pass and the wage "
    "and formality effects are smaller but of the same sign. Value added itself did not change detectably, so the "
    "rise in value added per worker reflects lower employment, mostly in agriculture.")

st.subheader("The bite in 2018")
m = bite[bite["n18"] >= 100]
fig = go.Figure(go.Histogram(x=100 * m["bite18"], nbinsx=40, marker_color=C_HIGHLIGHT))
base_layout(fig, xtitle="share of full-time wage employees below the 2019 minimum in 2018, %", ytitle="cells",
            height=320, legend=False)
show(fig, m[["unit", "group", "bite18", "bite17", "kaitz", "n18"]].round(4),
     caption=f"{len(m)} state × activity cells with at least 100 full-time wage employees with reported income in 2018.")

st.subheader("Event-study coefficients")
LAB = {"w_all": "mean log hourly wage, wage employees", "w_informal": "mean log hourly wage, informal wage employees",
       "lemp": "log employment", "formal": "formal share of employment", "lprod": "log value added per worker",
       "p10": "10th percentile, log hourly wage", "below_current": "share below the current minimum"}
o = st.selectbox("Outcome", list(LAB), format_func=LAB.get)
x = ev[ev["outcome"] == o].sort_values("year")
fig = go.Figure()
fig.add_trace(go.Scatter(x=x["year"], y=x["beta"] / 10, mode="markers+lines", marker=dict(color=C_HIGHLIGHT, size=8),
                         line=dict(color=C_HIGHLIGHT), name="coefficient",
                         error_y=dict(type="data", array=1.645 * x["se"] / 10, color=C_HIGHLIGHT)))
fig.add_hline(y=0, line=dict(color=MUTED, dash="dot"))
fig.add_vline(x=2018.5, line=dict(color=INK2, dash="dot"))
fig.add_vrect(x0=2019.5, x1=2021.5, fillcolor=C_CONTEXT, opacity=0.15, line_width=0)
base_layout(fig, xtitle="year", ytitle="effect of 10 pp of bite", height=420, legend=False)
show(fig, x[["year", "beta", "se"]].round(4),
     caption="Coefficients on bite × year relative to 2018, divided by 10 (effect of 10 percentage points of bite), with "
             "90% intervals from CR1 standard errors clustered by state. Shaded: 2020–2021, excluded from the post "
             "estimand. Weights: 2018 employment.")

st.subheader("Tests")
t = tests.reset_index()[["proposition", "outcome", "post", "lo90", "hi90", "p_pretrend", "ratio_to_first_stage", "verdict"]]
st.dataframe(t.round(3), hide_index=True, width="stretch")
st.caption("Post: mean of the 2022–2024 coefficients per unit of bite; intervals by inversion of the restricted wild "
           "cluster bootstrap. Decision rules are those of the pre-analysis plan.")
rob = load("minimum_wage_bite", "robustness")
if not rob.empty:
    with st.expander("Robustness"):
        st.dataframe(rob.round(3), hide_index=True, width="stretch")
footer("ENOE 2015–2024; INEGI, PIB por Entidad Federativa, base 2018; minimum wages from CONASAMI resolutions. "
       "Method: devtheory WP09, study 9.8.")
