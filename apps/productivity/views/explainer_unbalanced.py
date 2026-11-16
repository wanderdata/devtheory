"""Explainer: Baumol's unbalanced growth and the McMillan–Rodrik decomposition in one
three-sector model (theory note docs/theory/04_unbalanced_growth_and_reallocation.md, D-070).

The page solves the model in apps/productivity/unbalanced.py live from the controls; the only
data it reads is the precomputed relative-price slope of step 09 (empirics/output/<scope>/baumol).
"""
from dataclasses import fields

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from lib import (C_DYNAMIC, C_STATIC, C_WITHIN, INK, INK2, MUTED, base_layout, credit, out_dir, scope_info,
                 show)
from unbalanced import LABELS, PRESETS, SECTORS, Params, baumol_slope, decompose, solve

# One fixed colour per model sector (slots 7, 4, 5 of the shared palette, so they are not
# confused with the decomposition components, which keep their colours from the other pages).
SEC_COLORS = {"P": "#6250d6", "R": "#eda100", "S": "#e87ba4"}
NOTE_URL = ("https://github.com/wanderdata/devtheory/blob/main/docs/theory/"
            "04_unbalanced_growth_and_reallocation.md")

st.title("Explainer: unbalanced growth and the productivity decomposition")
st.markdown(
    "This page solves a three-sector model in which Baumol's mechanism of unbalanced growth and the "
    "McMillan–Rodrik decomposition can be seen side by side. Sector P produces progressive goods with fast "
    "productivity growth, R produces protected services whose prices can carry rising markups, and S produces "
    "personal services with slow productivity growth, much of them informal. Labour is the only input, prices "
    "are a markup over unit labour cost, and demand has a constant elasticity of substitution between the three "
    "goods. The derivations are in the [theory note](" + NOTE_URL + "); the numbers on this page are produced by "
    "the model from the values chosen below and do not describe any country.")
st.latex(r"p_i=\frac{\mu_i\,w_i}{A_i},\qquad s_i=\frac{\omega_i\,p_i^{\,1-\varepsilon}}{\sum_j\omega_j\,p_j^{\,1-\varepsilon}},"
         r"\qquad \ell_i=\frac{s_i/(\mu_i w_i)}{\sum_j s_j/(\mu_j w_j)}")
st.markdown(
    "Here $A_i$ is productivity, $w_i$ the wage, $\\mu_i$ the markup, $s_i$ the share of spending and $\\ell_i$ "
    "the share of employment. Value added per worker at current prices is $\\mu_i w_i$, so it differs across "
    "sectors only through wages and markups. Baumol's case is one wage for all sectors and no markups.")

# ------------------------------------------------------------------ controls --
KEYS = [f.name for f in fields(Params)]


def apply_preset():
    p = PRESETS[st.session_state["ub_preset"]]
    for k in KEYS:
        st.session_state[f"ub_{k}"] = getattr(p, k)


if "ub_g_P" not in st.session_state:
    st.session_state["ub_preset"] = list(PRESETS)[0]
    apply_preset()

st.subheader("Model settings")
st.selectbox("Starting point", list(PRESETS), key="ub_preset", on_change=apply_preset,
             help="Loads a set of parameter values; every value can then be changed below.")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("Productivity growth (per year)")
    st.slider("P: progressive goods", 0.0, 0.06, step=0.0025, format="%.4f", key="ub_g_P")
    st.slider("R: protected services", 0.0, 0.04, step=0.0025, format="%.4f", key="ub_g_R")
    st.slider("S: personal services", 0.0, 0.03, step=0.0025, format="%.4f", key="ub_g_S")
with c2:
    st.markdown("Demand")
    st.slider("Elasticity of substitution ε", 0.1, 2.0, step=0.05, key="ub_eps",
              help="Below 1: spending shifts toward goods whose relative price rises. Equal to 1: spending "
                   "shares stay constant. Above 1: spending shifts toward goods that become cheaper.")
    st.slider("Weight on P", 0.05, 0.9, step=0.05, key="ub_w_P")
    st.slider("Weight on R", 0.05, 0.9, step=0.05, key="ub_w_R")
    st.slider("Weight on S", 0.05, 0.9, step=0.05, key="ub_w_S",
              help="A higher weight on personal services stands in for demand from high-income households "
                   "when income is concentrated. Weights are normalised to sum to one.")
with c3:
    st.markdown("Wages and markups")
    st.slider("Informal wage relative to formal wage (ρ)", 0.2, 1.0, step=0.05, key="ub_rho",
              help="Wage in S relative to P and R. 1 is Baumol's case of one economy-wide wage.")
    st.slider("Share of a sector's productivity growth kept as wages (φ)", 0.0, 0.9, step=0.05, key="ub_phi",
              help="0 is Baumol's case. Above 0, wages rise faster in fast-growing sectors, as with segmented "
                   "labour markets.")
    st.slider("Growth of the markup in R (m, per year)", 0.0, 0.03, step=0.0025, format="%.4f", key="ub_m")
    st.slider("Years", 20, 100, step=5, key="ub_years")

p = Params(**{k: st.session_state[f"ub_{k}"] for k in KEYS})
df = solve(p)
dch = decompose(df, "chained")
dfx = decompose(df, "fixed")
slope_tab = baumol_slope(df)
b_model = slope_tab.attrs["slope"]
T = p.years

l = df.pivot(index="t", columns="sector", values="l")[list(SECTORS)]
m1, m2, m3, m4 = st.columns(4)
m1.metric("Aggregate growth, year 1", f"{dch['total'].iloc[0]:.2f}%")
m2.metric(f"Aggregate growth, year {T}", f"{dch['total'].iloc[-1]:.2f}%",
          delta=f"{dch['total'].iloc[-1] - dch['total'].iloc[0]:+.2f} points", delta_color="off")
m3.metric(f"Employment in S, year 0 → {T}", f"{100 * l['S'].iloc[0]:.0f}% → {100 * l['S'].iloc[-1]:.0f}%")
m4.metric("Relative-price slope in the model", f"{b_model:.2f}")

# ------------------------------------------------------- 1. employment shares --
st.subheader("Where labour goes")
fig = go.Figure()
for sec in SECTORS:
    fig.add_trace(go.Scatter(x=l.index, y=100 * l[sec], name=f"{sec}: {LABELS[sec]}", mode="lines",
                             stackgroup="one", line=dict(width=0.5, color=SEC_COLORS[sec]),
                             hovertemplate="Year %{x}: %{y:.1f}%<extra>" + LABELS[sec] + "</extra>"))
base_layout(fig, ytitle="Share of employment (%)", xtitle="Year", height=360)
fig.update_yaxes(range=[0, 100])
tab = (100 * l).round(2).reset_index().rename(columns={s: LABELS[s] + " (%)" for s in SECTORS})
show(fig, tab, key="ub_emp")
st.markdown(
    "With an elasticity of substitution below one, spending moves toward the goods whose relative price rises, "
    "which are those with slow productivity growth, and employment follows. An informal wage below the formal "
    "wage puts more workers in S for each peso spent there; a rising markup in R lets R take more spending while "
    "employing fewer workers per peso, and the labour it does not hire goes to S.")

# ----------------------------------------------------------- 2. relative prices --
st.subheader("Relative prices")
pr = df.pivot(index="t", columns="sector", values="price")[list(SECTORS)]
rel = pr.div(pr["P"], axis=0)
rel = rel / rel.iloc[0]
fig = go.Figure()
for sec in ["R", "S"]:
    fig.add_trace(go.Scatter(x=rel.index, y=rel[sec], name=f"{sec}: {LABELS[sec]}", mode="lines",
                             line=dict(width=2.5, color=SEC_COLORS[sec]),
                             hovertemplate="Year %{x}: %{y:.2f}<extra>" + LABELS[sec] + "</extra>"))
fig.add_hline(y=1, line=dict(color=MUTED, width=1, dash="dot"))
base_layout(fig, ytitle="Price relative to P (year 0 = 1)", xtitle="Year", height=340)
fig.update_yaxes(type="log")
show(fig, rel.round(4).reset_index().rename(columns={s: LABELS[s] for s in SECTORS}), key="ub_prices")
st.markdown(
    "The vertical axis is logarithmic, so a constant growth rate is a straight line. "
    "The price of each good relative to progressive goods rises with its productivity gap, less the part of that "
    "gap that its workers keep as relative wages (φ), plus any rise in its markup. In Baumol's case the price of "
    "S relative to P rises at exactly $g_P-g_S$ a year.")

# -------------------------------------------------------------- 3. decomposition --
st.subheader("The same economy in the McMillan–Rodrik decomposition, at two price bases")
st.markdown(
    "Each year's growth of output per worker is split into growth within sectors, a static reallocation term "
    "(employment changes weighted by the initial level of output per worker) and a dynamic term (employment "
    "changes weighted by the change in output per worker). The left panel values each year at the prices of "
    "the previous year, as the period decompositions in this app do; the right panel values every year at the "
    "prices of year 0, as a decomposition at the constant prices of a distant base year would.")
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.04,
                    subplot_titles=("Prices of the previous year (chained)", "Prices of year 0 (fixed)"))
for col, d in [(1, dch), (2, dfx)]:
    for term, color, label in [("within", C_WITHIN, "Within sectors"), ("static", C_STATIC, "Static reallocation"),
                               ("dynamic", C_DYNAMIC, "Dynamic reallocation")]:
        fig.add_trace(go.Bar(x=d["t"], y=d[term], name=label, marker_color=color, showlegend=(col == 1),
                             legendgroup=term, hovertemplate="Year %{x}: %{y:.3f} points<extra>" + label + "</extra>"),
                      row=1, col=col)
    fig.add_trace(go.Scatter(x=d["t"], y=d["total"], name="Total growth", mode="lines",
                             line=dict(color=INK, width=2), showlegend=(col == 1), legendgroup="total",
                             hovertemplate="Year %{x}: %{y:.3f}%<extra>Total</extra>"), row=1, col=col)
base_layout(fig, ytitle="Percentage points", height=440)
fig.update_layout(barmode="relative", bargap=0.1, margin=dict(t=90),
                  legend=dict(orientation="h", yanchor="bottom", y=1.12, xanchor="left", x=0))
fig.update_yaxes(title=None, row=1, col=2)
fig.update_annotations(font=dict(size=12, color=INK2))
tab = dch.merge(dfx, on="t", suffixes=(" (chained)", " (year-0 prices)")).round(4)
show(fig, tab, key="ub_decomp")
s_ch, s_fx = dch["static"].mean(), dfx["static"].mean()
st.markdown(
    f"Over the {T} years the static term averages {s_ch:+.3f} points a year at chained prices and {s_fx:+.3f} at "
    "year-0 prices. At chained prices the static term weights employment changes by value added per worker at "
    "current prices, which in this model equals the wage times the markup. In Baumol's case that is the same in "
    "every sector, so the static term is zero however much labour moves, and the slowdown appears in the within "
    "term (the employment weights on fast sectors shrink) and in a small negative dynamic term. At year-0 prices "
    "output per worker grows faster in the fast sector, so the same movement of labour registers as "
    "growth-reducing structural change. With an informal wage gap, the static term at chained prices is negative "
    "whenever informal employment grows; with a markup, employment growth in R counts as productive reallocation "
    "although only the markup differs.")

# --------------------------------------------------------------- 4. Baumol slope --
st.subheader("The relative-price slope: model and estimates")
info = scope_info()
emp = None
f = out_dir() / "baumol" / "slope.csv"
if f.exists():
    e = pd.read_csv(f)
    e = e[e["period"] == "2000–2019"]
    if len(e):
        emp = e.iloc[0]
x = slope_tab["real_rel_change"].to_numpy()
y = slope_tab["price_rel_change"].to_numpy()
span = max(1.0, float(np.abs(x).max()) * 1.4)
xs = np.array([-span, span])
fig = go.Figure()
if emp is not None:
    fig.add_trace(go.Scatter(x=[-span, span, span, -span], y=[-span * emp.ci90_lo, span * emp.ci90_lo,
                                                                span * emp.ci90_hi, -span * emp.ci90_hi],
                             mode="lines", fill="toself", fillcolor="rgba(195,194,183,0.35)", line=dict(width=0),
                             name=f"{info['label']}, 2000–2019: 90% interval", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=xs, y=emp.slope * xs, mode="lines", line=dict(color=MUTED, width=1.5),
                             name=f"{info['label']}, 2000–2019: {emp.slope:.2f}", hoverinfo="skip"))
fig.add_trace(go.Scatter(x=xs, y=-xs, mode="lines", line=dict(color=INK2, width=1, dash="dash"),
                         name="Baumol: −1", hoverinfo="skip"))
c = y.mean() - b_model * x.mean()
fig.add_trace(go.Scatter(x=xs, y=c + b_model * xs, mode="lines", line=dict(color=INK, width=2),
                         name=f"Model: {b_model:.2f}", hoverinfo="skip"))
for i, sec in enumerate(SECTORS):
    fig.add_trace(go.Scatter(x=[x[i]], y=[y[i]], mode="markers+text", text=[sec], textposition="top right",
                             marker=dict(size=12, color=SEC_COLORS[sec]), name=LABELS[sec], showlegend=False,
                             hovertemplate=LABELS[sec] + ": real %{x:.2f}, price %{y:.2f}<extra></extra>"))
base_layout(fig, xtitle="Change in relative real productivity (log points a year)",
            ytitle="Change in relative price (log points a year)", height=420)
fig.update_xaxes(range=[-span, span], zeroline=True, zerolinecolor="#c3c2b7")
fig.update_yaxes(range=[-span, span])
show(fig, slope_tab.round(4).assign(sector=lambda d: d["sector"].map(LABELS)), key="ub_slope")
st.markdown(
    "Each point is one sector of the model over the whole horizon. Baumol's mechanism with one wage predicts that "
    "relative prices offset relative productivity growth one for one, a slope of −1. In the model the slope equals "
    "$-(1-\\varphi)$ when markups are constant; a rising markup in a slow-growing sector pushes it below −1."
    + (f" The grey line is the slope estimated across sectors and countries for {info['label']} in 2000–2019 "
       f"(step 09 of the labour-productivity pipeline; {int(emp.n_countries)} countries, mining and utilities "
       f"excluded): {emp.slope:.2f}, with a 90% bootstrap interval over countries of {emp.ci90_lo:.2f} to "
       f"{emp.ci90_hi:.2f}. Read through the model, relative prices offset about half of the differences in real "
       "productivity growth, and the rest appears as differences in nominal value added per worker, that is, in "
       "wages and markups. Measurement error in sector employment would also pull the estimate toward zero "
       "(see the theory note, section 4)." if emp is not None else ""))

credit("Model: devtheory theory note 04 (unbalanced growth, relative prices and the reallocation term); code in "
       "apps/productivity/unbalanced.py. Estimated slopes: step 09 of the labour-productivity pipeline (UN National "
       "Accounts Main Aggregates and ILOSTAT), WP08.")
