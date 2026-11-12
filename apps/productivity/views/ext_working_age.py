"""Extended: growth of output per working-age person, split into productivity and employment rate."""
import plotly.graph_objects as go
import streamlit as st

from lib import (C_STRUCT, C_WITHIN, GRADE_TEXT, INK2, base_layout, footer, load_extra, show)

C_EMP = "#1baf7a"

st.title("Output per working-age person")
st.markdown(
    "Output per worker leaves out people who are not working. Output per working-age person (ages 15 and "
    "over) includes them, and it changes for two reasons: output per worker changes, or the share of the "
    "working-age population in work changes. In logs the two add up exactly:\n\n"
    "growth of output per working-age person = within-sector productivity + structural change + employment rate\n\n"
    "The first two terms are the decomposition on the *Period decompositions* page, rescaled to log points so "
    "that the three add up. Value added is at initial-year prices of each period. Two further terms are shown "
    "in the table but are not part of this sum: the change in the working-age share of the population "
    "(demographics; add it to get output per person) and the gain from the terms of trade (add it to get real "
    "income rather than output).")

t = load_extra("ladder", "terms")
if t.empty:
    st.warning("No results: run `empirics/code/lp/08_ladder.py`.")
    st.stop()

c1, c2 = st.columns([2, 1])
periods = list(dict.fromkeys(t["period"]))
per = c1.radio("Period", periods, horizontal=True, index=periods.index("2000–2019") if "2000–2019" in periods else 0)
grades = c2.multiselect("Grades shown", ["A", "B", "C"], default=["A", "B"], help="\n".join(GRADE_TEXT.values()))
x = t[(t["period"] == per) & (t["grade"].isin(grades))].sort_values("ypw_pp")
labels = [f"{r.country}  ·  {r.grade}" for r in x.itertuples()]
fig = go.Figure()
for col, lab, color in [("within_pp", "Within-sector productivity", C_WITHIN),
                        ("struct_pp", "Structural change", C_STRUCT),
                        ("emprate_pp", "Employment rate", C_EMP)]:
    fig.add_trace(go.Bar(y=labels, x=x[col], name=lab, orientation="h", marker=dict(color=color),
                         hovertemplate="%{y}<br>" + lab + ": %{x:.2f}<extra></extra>"))
fig.add_trace(go.Scatter(y=labels, x=x["ypw_pp"], mode="markers", name="Output per working-age person",
                         marker=dict(color=INK2, size=9, symbol="diamond", line=dict(color="white", width=1)),
                         hovertemplate="%{y}<br>Total: %{x:.2f}<extra></extra>"))
base_layout(fig, xtitle="log points per year (×100)", height=120 + 30 * max(len(x), 3))
fig.update_layout(barmode="relative")
fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
cols = {"country": "Country", "grade": "Grade", "ypw0": "Output per working-age person, start (US$)",
        "ypwT": "Output per working-age person, end (US$, start-year prices)", "emp_rate0": "Employment rate, start (%)",
        "emp_rateT": "Employment rate, end (%)", "ypw_pp": "Total", "within_pp": "Within", "struct_pp": "Structural",
        "emprate_pp": "Employment rate", "demog_pp": "Demographic", "ypc_pp": "Output per person",
        "tot_pp": "Terms of trade", "tot_avg_pp": "Terms of trade (average deflator)", "old_share0": "Aged 65+, % of 15+ population, start",
        "old_shareT": "Aged 65+, % of 15+ population, end"}
show(fig, x[[c for c in cols if c in x.columns]].rename(columns=cols).round(2),
     caption="The label after each country is its survey-anchoring grade. Employment: ILO modelled estimates. "
             "Demographic term: working-age share of the total population (ILOSTAT population, UN estimates). "
             "The data table also shows the share of the 15+ population aged 65 and over (World Bank WDI), since "
             "people over 65 are part of the working-age population here. Terms of trade: real gross domestic income over real GDP, with "
             "the trade balance deflated by import prices; the data table also gives the result with the average of "
             "export and import prices, which differs little.")

st.subheader("How much does the employment rate matter, and over what horizon?")
h = load_extra("ladder", "horizon")
samples = list(dict.fromkeys(h["sample"]))
smp = st.radio("Countries", samples, horizontal=True, key="hz_sample")
hh = h[h["sample"] == smp]
fig = go.Figure()
for col, lab, color in [("share_emprate_larger", "Employment-rate term larger than the productivity term", C_EMP),
                        ("emprate_variance_share", "Employment-rate term's share of the variance of growth", C_WITHIN),
                        ("share_prod_up_ypw_down", "Productivity up while output per working-age person fell", C_STRUCT)]:
    fig.add_trace(go.Scatter(x=hh["horizon"], y=hh[col], mode="lines+markers", name=lab, line=dict(color=color, width=2),
                             hovertemplate=lab + "<br>%{x}-year windows: %{y:.2f}<extra></extra>"))
base_layout(fig, xtitle="length of window (years)", ytitle="share", height=380)
fig.update_xaxes(tickvals=list(hh["horizon"]))
a, b = hh.set_index("horizon").loc[hh["horizon"].min()], hh.set_index("horizon").loc[hh["horizon"].max()]
show(fig, hh.drop(columns="sample").round(3),
     caption="Every window of the given length between 1991 and 2024, pooled across countries; output per worker "
             "uses official total value added at constant 2020 prices. "
             f"Over {hh['horizon'].min()}-year windows the employment-rate term is the larger of the two in "
             f"{a.share_emprate_larger:.0%} of cases and accounts for {a.emprate_variance_share:.0%} of the variance of "
             f"growth of output per working-age person; over {hh['horizon'].max()}-year windows the figures are "
             f"{b.share_emprate_larger:.0%} and {b.emprate_variance_share:.0%}. The two terms have opposite signs in "
             f"{hh['share_opposite_signs'].min():.0%}–{hh['share_opposite_signs'].max():.0%} of windows at every "
             "horizon, but over long windows the employment-rate term is usually small.")

with st.expander("Definitions and limits"):
    st.markdown(
        "- **Working-age population**: ages 15 and over, obtained as ILO modelled employment divided by the ILO "
        "employment-to-population ratio, so both refer to the same population. People aged 65 and over are "
        "included, so the demographic and employment-rate terms are affected by ageing. They cannot yet be shown "
        "separately in the zero block: ILO employment estimates by age stop at a '25 and over' band.\n"
        "- **Log points**: 100 × the change in the natural log divided by the number of years. The within and "
        "structural terms are the linear terms of the period decomposition, rescaled in proportion so that they add "
        "up to the log growth of output per worker.\n"
        "- **Terms of trade**: the trading gain, (exports at current prices ÷ the import price deflator − exports at "
        "constant prices), added to constant-price GDP and expressed as the growth of the ratio to GDP. "
        "Positive when export prices rose relative to import prices.\n"
        "- The employment rate for recent years, and for countries with few surveys, is modelled by the ILO, so "
        "the employment-rate term for those cases is partly a model result (see the grades).")
footer("ILOSTAT population by sex (UN estimates), downloaded 2026-11-12; World Bank WDI, population aged 65+ (% of total).")
