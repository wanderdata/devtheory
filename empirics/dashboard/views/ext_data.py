"""Extended: data quality, anchoring and validation."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (countries, load_excluded_surveys, C_WITHIN, INK2, out_dir, SECTOR_COLORS, SHORT, base_layout, footer,
                 load_emp5, load_output, load_panel, name, show)

st.title("Data quality and coverage")
st.markdown("**Extension of the baseline.** Shows where the employment data come from, how far the ILO modelled "
            "series can be trusted, and which results rest on real survey data.")

# ---- anchoring timeline
st.subheader("Where employment data come from, by year")
p = load_panel(); e5 = load_emp5()
excl = load_excluded_surveys()
years = list(range(1991, 2025))
z, txt = [], []
for iso in countries():
    a = set(p[(p["iso3"] == iso) & p["emp_survey"].notna()]["year"])
    b = set(e5[(e5["iso3"] == iso) & (e5["series"] == "survey")]["year"])
    c = excl.get(iso, {})
    row, trow = [], []
    for y in years:
        if y in a:
            row.append(3); trow.append("Survey, 7 sectors (grids A and B)")
        elif y in b:
            row.append(2); trow.append("Survey, six broad groups only (grid B)")
        elif y in c:
            row.append(1); trow.append(f"Survey not used: covers {c[y]:.0%} of national employment (urban or partial)")
        else:
            row.append(0); trow.append("ILO model only")
    z.append(row); txt.append(trow)
fig = go.Figure(go.Heatmap(z=z, x=years, y=[name(i) for i in countries()], text=txt, zmin=0, zmax=3,
                           hovertemplate="%{y} %{x}: %{text}<extra></extra>",
                           colorscale=[[0, "#ecebe6"], [0.24, "#ecebe6"], [0.25, "#f2c46d"], [0.49, "#f2c46d"],
                                       [0.5, "#86b6ef"], [0.74, "#86b6ef"], [0.75, "#1c5cab"], [1, "#1c5cab"]],
                           showscale=False, xgap=2, ygap=2))
base_layout(fig, height=120 + 22 * len(countries()), legend=False)
fig.update_yaxes(gridcolor="rgba(0,0,0,0)", autorange="reversed")
show(fig, caption="Dark blue: usable survey with 7-sector detail. Light blue: survey with six broad groups only "
                  "(usable in grid B). Amber: a survey exists but covers less than 80% of national employment "
                  "(urban-only or partial coverage, e.g. Argentina) and is not used. Grey: ILO model only "
                  "(interpolated or extrapolated).")

# ---- validation
st.subheader("How well does the ILO model reproduce survey-based structural change?")
v = out_dir() / "validation"
g = st.radio("Grid", ["A", "B"], horizontal=True)
pairs = pd.read_csv(v / f"pairs_{g}.csv")
summ = pd.read_csv(v / "summary.csv").set_index("grid").loc[g]
lim = max(pairs[["struct_pp_survey", "struct_pp_model"]].abs().max()) * 1.1
fig = go.Figure()
fig.add_trace(go.Scatter(x=[-lim, lim], y=[-lim, lim], mode="lines", line=dict(color="#c3c2b7", dash="dot"),
                         hoverinfo="skip", showlegend=False))
fig.add_trace(go.Scatter(x=pairs["struct_pp_survey"], y=pairs["struct_pp_model"], mode="markers",
                         marker=dict(size=9, color=C_WITHIN, line=dict(color="white", width=1)),
                         text=[f"{name(r.iso3)} {r.t0}–{r.T}" for r in pairs.itertuples()],
                         hovertemplate="%{text}<br>survey %{x:.2f}, model %{y:.2f}<extra></extra>", showlegend=False))
base_layout(fig, xtitle="structural term with survey employment (pp/yr)",
            ytitle="structural term with ILO modelled employment (pp/yr)", legend=False, height=460)
show(fig, pairs.round(2),
     caption=f"{int(summ['pairs'])} pairs of survey years in {int(summ['countries'])} countries. Correlation "
             f"{summ['corr_struct']:.2f}; median absolute gap {summ['median_ad_struct_pp']:.2f} pp/yr; same sign in "
             f"{100*summ['sign_agree_share']:.0f}% of pairs. Points far from the dotted line are mostly survey-type "
             "switches (census vs labour force survey) or merged ISIC sections.")

# ---- model vs survey shares
st.subheader("Modelled vs survey employment shares, by sector")
who = st.selectbox("Country", list(countries()), format_func=name, index=list(countries()).index("DOM"))
q = p[p["iso3"] == who]
fig = go.Figure()
for s, gg in q.groupby("sector"):
    m = gg.dropna(subset=["emp_model"])
    tot_m = q.groupby("year")["emp_model"].sum()
    fig.add_trace(go.Scatter(x=m["year"], y=100 * m["emp_model"].values / tot_m.loc[m["year"]].values, mode="lines",
                             name=SHORT[s], line=dict(color=SECTOR_COLORS[s], width=2), legendgroup=s))
    sv = gg.dropna(subset=["emp_survey"])
    if len(sv):
        tot_s = q.groupby("year")["emp_survey"].sum()
        fig.add_trace(go.Scatter(x=sv["year"], y=100 * sv["emp_survey"].values / tot_s.loc[sv["year"]].values,
                                 mode="markers", marker=dict(color=SECTOR_COLORS[s], size=8, line=dict(color="white", width=1)),
                                 name=SHORT[s] + " (survey)", legendgroup=s, showlegend=False))
base_layout(fig, ytitle="share of employment, %", height=440)
show(fig, caption="Lines: ILO modelled estimates. Dots: national survey years (grid A). Large gaps between "
                  "dots and lines show where the model departs from the surveys.")

# ---- grades
st.subheader("Anchoring grades by country and period")
gg = st.radio("Grid ", ["A", "B"], horizontal=True, key="gg")
mm = load_output(gg, "main")
tab = mm.pivot_table(index="country", columns="period", values="grade", aggfunc="first")
st.dataframe(tab, width="stretch")
st.caption("A: both endpoints within 2 years of a usable survey year (interpreted). B: one (flagged). C: none (not interpreted).")
footer()
