import plotly.graph_objects as go
import streamlit as st

from motors_lib import CATEGORICAL, MUTED, SAMPLE_LABELS, SUBPERIODS, base_layout, footer, forest, load, show, unit_note

st.title("2. Was manufacturing ever a motor in Latin America and the Caribbean?")
st.markdown(
    "Two lenses. First, the S&V test with a separate manufacturing slope for LAC countries in each subperiod, "
    "including the import-substitution years before 1970 (nine Latin American countries have sector data that "
    "far back). Second, Kaldor's first law: did faster manufacturing growth go with faster GDP growth, decade by decade?")

st.sidebar.header("Settings")
smp = st.sidebar.radio("Sample", ["main", "core"], format_func=SAMPLE_LABELS.get, key="q2s")
est = st.sidebar.radio("Estimator", ["HT", "FE"], format_func={"HT": "Hausman–Taylor", "FE": "Fixed effects"}.get, key="q2e")

st.subheader("Manufacturing slope: LAC and the rest of the world")
q = load("questions/q2_lac.csv")
x = q[(q["sample"] == smp) & (q["estimator"] == est) & q["group"].isin(["LAC", "Rest"])].copy()
x["group"] = x["group"].map({"LAC": "Latin America and the Caribbean", "Rest": "Rest of the world"})
fig = forest(x, "subperiod", group_col="group", xtitle="pp of annual growth per point of manufacturing share",
             order=SUBPERIODS, height=340)
d = q[(q["sample"] == smp) & (q["estimator"] == est) & (q["group"] == "LAC minus rest")]
show(fig, x[["group", "subperiod", "coef", "se", "p", "n_lac_countries"]].round(3),
     caption="One regression with separate slopes for LAC and the rest in each subperiod. Number of LAC countries "
             "in the sample: " + ", ".join(f"{k} {int(v)}" for k, v in x[x['group'].str.startswith('Latin')]
                                            .set_index('subperiod')['n_lac_countries'].dropna().items()) + ".")
st.markdown("**Difference, LAC minus rest:** " + "; ".join(
    f"{r.subperiod} {r.coef:+.3f} (p = {r.p:.2f})" for r in d.itertuples()) +
    ". With Hausman–Taylor no difference is significant in either sample. With fixed effects in the main sample, "
    "LAC's slope is significantly higher than the rest's after 1990 (that is, less negative); in the core sample no "
    "difference is significant with either estimator. Across all 192 specifications the LAC difference is *fragile* "
    "for 1970–90 and 2005–20 and *leaning positive* for 1990–2005 (robustness page). By this test manufacturing "
    "never worked distinguishably better in LAC than elsewhere; if anything, its decline after 1990 cost LAC less.")
unit_note()

st.subheader("Kaldor's first law, decade by decade")
k = load("questions/q2_kaldor.csv")
fig = go.Figure()
for i, (grp, g) in enumerate(k.groupby("group", sort=False)):
    fig.add_trace(go.Scatter(x=g["decade"], y=g["slope"], mode="lines+markers",
                             name={"LAC": "Latin America and the Caribbean", "Rest": "Rest of the world"}[grp],
                             line=dict(color=CATEGORICAL[i], width=2), marker=dict(size=8),
                             error_y=dict(type="data", array=1.96 * g["se"], color=CATEGORICAL[i], thickness=1, width=0),
                             customdata=g[["n", "mean_gy", "mean_gm"]],
                             hovertemplate="%{x}: slope %{y:.2f}<br>%{customdata[0]} countries<br>mean GDP growth "
                                           "%{customdata[1]:.1f}%, manufacturing %{customdata[2]:.1f}%<extra></extra>"))
base_layout(fig, ytitle="slope: GDP growth on manufacturing growth", height=360)
show(fig, k.round(2),
     caption="Cross-country regression of average annual real GDP growth on real manufacturing value-added growth, "
             "by decade (countries over 1 million people). Manufacturing volumes: GGDC 10-Sector before 1970, UN "
             "constant-price data after. A slope well above manufacturing's share of GDP (about 0.15–0.30) is what "
             "Kaldor's argument predicts.")
st.markdown(
    "Manufacturing and GDP growth moved closely together in LAC in every decade (slopes 0.37–0.74), as Kaldor's law "
    "predicts, and more steeply than elsewhere in the 1960s, 1970s, 1980s and 2010s. But this held in the debt-crisis "
    "1980s and the stagnant 2010s as much as in the boom years: it shows that the region's growth was tied to its "
    "manufacturing, not that manufacturing drove it. Common shocks move both.")
footer()
