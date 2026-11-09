import plotly.graph_objects as go
import streamlit as st

from motors_lib import CATEGORICAL, base_layout, footer, load_proc, show

st.title("Data and method")
st.markdown("""
**Unit of observation.** A country in a five-year period (1950–55 … 2015–20); a ten-year version for robustness.

**Dependent variable.** Average annual growth of real GDP per head over the period, 100 × (y₍ₜ₊₅₎/yₜ − 1)/5, from
Penn World Table 11.0 national-accounts GDP (`rgdpna`) and population.

**Regressors, measured at the start of the period.**
- *Sector shares*: value added of the sector as a % of total value added at current prices. UN National Accounts Main
  Aggregates from 1970 (seven groups); GGDC 10-Sector Database before 1970 (about 30 countries), ratio-spliced to the
  UN level in 1970 and rescaled to add to 100. Twelve-sector shares (value added and employment) from the ETD, 1990–2018.
- *Income relative to the US*: PWT output-side GDP per head divided by the US value, same year.
- *Schooling*: average years, population 15+, Barro–Lee v2.2 (to 2010) for the replication; for the extension, years
  implied by PWT's human-capital index (which is built from Barro–Lee and extends to 2023; correlation with
  Barro–Lee 0.97).
- *Controls*: log population, openness (exports + imports, % of GDP), and for Hausman–Taylor a dummy for countries
  whose centroid lies outside the tropics (substitute for S&V's temperate-land share).
- *Conditions (question 3)*: also mining & utilities share, Rodrik's currency undervaluation index from PWT price
  levels, a post-2000 dummy.

**Estimators.** Hausman–Taylor (S&V's main estimator; implemented here and validated on the textbook example), fixed
effects and random effects with country-clustered standard errors.

**Samples.** *Main* (pre-specified): countries with at least 1 million people in 2000. *Without former planned
economies*: excludes Eastern Europe, the former USSR and Mongolia, whose shares under planned prices are not
comparable. *Core*: also excludes commodity exporters (mining & utilities over 20% of value added on average).
*Developing*: core without the 21 long-standing OECD economies.

**Pre-analysis plan.** Tests, readings and verdict rules were written before estimation
(`papers/WP07_development_motors/00_literature_and_plan.md`). Two departures are recorded: the excl.-planned and
core samples were added after the replication showed the results depend on them (D-039); system GMM was dropped
(D-040).
""")

st.subheader("Coverage")
p = load_proc("panel5.csv")
use = p.dropna(subset=["GR", "MAN", "RELUS", "EDU_HC"])
n = use.groupby("period").agg(countries=("iso3", "nunique"), lac=("lac", "sum")).reset_index()
fig = go.Figure()
fig.add_trace(go.Bar(x=n["period"], y=n["countries"], name="all countries", marker=dict(color=CATEGORICAL[0])))
fig.add_trace(go.Bar(x=n["period"], y=n["lac"], name="of which LAC", marker=dict(color=CATEGORICAL[1])))
base_layout(fig, xtitle="period start", ytitle="countries with all core variables", height=340)
fig.update_layout(barmode="overlay")
show(fig, n, caption="Countries with growth, manufacturing share, income gap and schooling, by period (before sample filters).")
footer()
