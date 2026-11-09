import plotly.graph_objects as go
import streamlit as st

from motors_lib import (CATEGORICAL, MUTED, SAMPLE_LABELS, SUBPERIODS, base_layout, footer, forest, load, show,
                 unit_note)

st.title("1. Is manufacturing still a motor of development?")
st.markdown(
    "The test: does a larger manufacturing share of value added at the start of a five-year period predict "
    "faster growth of GDP per head over the period, holding income relative to the US, schooling, population, "
    "openness and the period constant? Szirmai and Verspagen (S&V) asked this for 1950–2005; here the panel "
    "runs to 2020.")

st.sidebar.header("Settings")
smp = st.sidebar.radio("Sample", ["main", "core"], format_func=SAMPLE_LABELS.get, key="q1s")
est = st.sidebar.radio("Estimator", ["HT", "FE"], format_func={"HT": "Hausman–Taylor (S&V's)", "FE": "Fixed effects"}.get,
                       key="q1e")

st.subheader("The manufacturing slope by period")
q = load("questions/q1_subperiods.csv")
x = q[(q["sample"] == smp) & (q["estimator"] == est) & q["model"].str.startswith("(1)") & q["term"].str.startswith("MAN[")].copy()
x["subperiod"] = x["term"].str.extract(r"\[(.*)\]")[0]
fig = forest(x, "subperiod", xtitle="pp of annual growth per point of manufacturing share", order=SUBPERIODS,
             color=CATEGORICAL[0], height=300)
show(fig, x[["subperiod", "coef", "se", "p", "nobs", "ncountries"]].round(3),
     caption="One regression with a separate manufacturing slope for each subperiod (S&V Table 4, model 1). "
             "Bars: 95% intervals. 1950–70 rests on about 30 countries with sector data before 1970.")
unit_note()

st.subheader("When did it change? 20-year rolling windows")
r = load("questions/q1_rolling.csv")
r = r[(r["model"].str.startswith("(1)"))]
fig = go.Figure()
for i, (sname, g) in enumerate(r.groupby("sample", sort=False)):
    mid = g["start"] + 10
    fig.add_trace(go.Scatter(x=mid, y=g["coef_MAN"] + 1.96 * g["se_MAN"], mode="lines", line=dict(width=0),
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=mid, y=g["coef_MAN"] - 1.96 * g["se_MAN"], mode="lines", line=dict(width=0),
                             fill="tonexty", fillcolor=["rgba(42,120,214,0.15)", "rgba(235,104,52,0.15)"][i],
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=mid, y=g["coef_MAN"], mode="lines+markers", name=SAMPLE_LABELS[sname],
                             line=dict(color=CATEGORICAL[i], width=2), marker=dict(size=7),
                             customdata=g[["window", "nobs"]],
                             hovertemplate="%{customdata[0]}: %{y:.3f} (%{customdata[1]} obs)<extra></extra>"))
fig.add_hline(y=0, line=dict(color=MUTED, width=1))
base_layout(fig, xtitle="middle year of the 20-year window", ytitle="manufacturing slope", height=380)
show(fig, r[["sample", "window", "coef_MAN", "se_MAN", "nobs", "ncountries"]].round(3),
     caption="Hausman–Taylor estimate within each 20-year window (four five-year periods); shaded: 95% interval. "
             "The slope is close to zero or positive for windows centred on the 1970s and turns negative for windows "
             "covering 1980–2010.")

st.subheader("Where would it still work? The marginal effect by schooling and income gap")
st.markdown("With S&V's interactions (manufacturing × income relative to the US, manufacturing × schooling), the "
            "effect of manufacturing depends on where a country stands. Green cells: significantly positive; "
            "orange: significantly negative; grey: not distinguishable from zero.")
sub = st.radio("Subperiod", SUBPERIODS, index=3, horizontal=True)
sf = load("questions/q1_me_surface.csv")
g = sf[(sf["sample"] == smp) & (sf["group"] == sub)]
piv = g.pivot(index="EDU", columns="RELUS", values="me")
sig = g.assign(s=lambda d: (d["lo"] > 0).astype(int) - (d["hi"] < 0).astype(int)).pivot(index="EDU", columns="RELUS", values="s")
fig = go.Figure(go.Heatmap(z=sig.values, x=piv.columns, y=piv.index, text=piv.round(3).values,
                           colorscale=[[0, "#eb6834"], [0.5, "#e1e0d9"], [1, "#1baf7a"]], zmin=-1, zmax=1,
                           showscale=False, hovertemplate="income/US %{x}<br>schooling %{y} yrs<br>effect %{text}<extra></extra>"))
me = load("questions/q1_me_reference.csv")
ref = me[(me["sample"] == smp) & (me["estimator"] == "HT") & me["model"].str.startswith("(3)") & (me["subperiod"] == sub)]
if len(ref):
    fig.add_trace(go.Scatter(x=ref["RELUS_ref"], y=ref["EDU_ref"], mode="markers", name="median developing country",
                             marker=dict(symbol="x", size=13, color="#0b0b0b"),
                             hovertemplate="median developing country<br>effect %{customdata:.3f}<extra></extra>",
                             customdata=ref["me"]))
base_layout(fig, xtitle="GDP per head relative to the US", ytitle="years of schooling (15+)", height=430)
show(fig, g[["RELUS", "EDU", "me", "lo", "hi"]].round(3),
     caption="Hausman–Taylor, model with both interactions, slope shifts by subperiod; schooling from PWT's human-"
             "capital index. Cross: median developing country in the subperiod.")
footer()
