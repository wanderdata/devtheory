import plotly.graph_objects as go
import streamlit as st

from motors_lib import (MUTED, VERDICT_COLORS, base_layout, footer, headline, load, show, spec_summary, unit_note,
                 verdict_chip)

st.title("Development motors: is manufacturing still the engine of growth?")
st.markdown("**Paul Wander** · Division of Production, Productivity and Management, UN-ECLAC · devtheory WP07")
st.markdown(
    "Szirmai and Verspagen (2015) found that a larger manufacturing share predicted faster growth in developing "
    "countries over 1950–2005, especially where schooling was higher and the gap to the United States larger, "
    "but that the road had become harder after 1990. This dashboard **replicates their test, extends it to "
    "2020, asks whether it ever held in Latin America and the Caribbean, which conditions make it work, and "
    "whether services or other sectors now play the role.** The tests and what would count as evidence were "
    "written down before any estimation.")

m70, m90, m05 = (headline(f"Manufacturing, {k}") for k in ["1970–90", "1990–2005", "2005–20"])
l90 = headline("LAC minus rest, 1990–2005")
ser = headline("SER, 2005–20")
oth = headline("OTH, 2005–20")
agr = headline("AGR, 2005–20")


def fmt(r):
    return f"median {r['median']:+.3f} across {int(r['n_specs'])} specifications" if r is not None else ""


st.subheader("Four answers")
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        f"**1. Is manufacturing still a motor? Not in the sense tested here.** Since 1990 a larger manufacturing "
        f"share has not predicted faster growth: the estimate is {verdict_chip(m90['verdict'])} for 1990–2005 "
        f"({fmt(m90)}) and {verdict_chip(m05['verdict'])} for 2005–20 ({fmt(m05)}). Even for 1970–90, the "
        f"period S&V found strongest, it is {verdict_chip(m70['verdict'])} once services are controlled for.",
        unsafe_allow_html=True)
    st.markdown(
        f"**2. Was it ever a motor in LAC?** Not distinguishably from the rest of the world. Latin America and "
        f"the Caribbean's manufacturing slope is never robustly different from other countries'; after 1990 it "
        f"was somewhat *less* negative ({verdict_chip(l90['verdict'])}, {fmt(l90)}). Manufacturing and GDP "
        "growth moved closely together in the region (Kaldor's first law), but that held in its boom and its bust.",
        unsafe_allow_html=True)
with c2:
    st.markdown(
        "**3. Why only in some contexts?** The conditions S&V emphasised are fragile. Their key interaction (a "
        "bigger payoff the poorer the country) rests on a few oil states; without commodity exporters and former "
        "planned economies it reverses. Of the moderators tested, schooling and a post-2000 penalty hold in the "
        "core sample, country size in the main sample; openness and commodity dependence show nothing.")
    st.markdown(
        f"**4. Other motors?** No sector share robustly predicts faster growth after 2005 except agriculture "
        f"({verdict_chip(agr['verdict'])}), which most plausibly reflects room to move workers out of farming. "
        f"Services as a whole ({verdict_chip(ser['verdict'])}) and finance, business, government and personal "
        f"services ({verdict_chip(oth['verdict'])}) are associated with *slower* growth. In the ETD's 51 "
        "countries, manufacturing's *employment* share predicts growth while its output share does not.",
        unsafe_allow_html=True)

st.subheader("The headline in one chart")
s = spec_summary()
x = s[s["family"] == "Q4"].copy()
x["sector"] = x["estimand"].str.split(",").str[0]
x["subperiod"] = x["estimand"].str.split(", ").str[1]
from motors_lib import SECTOR_LABELS  # noqa: E402

x["label"] = x["sector"].map(SECTOR_LABELS)
fig = go.Figure()
subs = ["1970–90", "1990–2005", "2005–20"]
for i, k in enumerate(subs):
    y = x[x["subperiod"] == k]
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", name=k,       # legend: shape only
                             marker=dict(size=10, symbol=["circle", "diamond", "square"][i], color="#ffffff",
                                         line=dict(color="#52514e", width=1.5))))
    fig.add_trace(go.Scatter(
        x=y["median"], y=y["label"], mode="markers", name=k, showlegend=False,
        marker=dict(size=11, symbol=["circle", "diamond", "square"][i],
                    color=[VERDICT_COLORS[v] for v in y["verdict"]], line=dict(color=["#52514e", "#52514e", "#0b0b0b"][i], width=1.5)),
        error_x=dict(type="data", symmetric=False, array=y["q90"] - y["median"], arrayminus=y["median"] - y["q10"],
                     color=MUTED, thickness=1, width=0),
        customdata=y[["verdict", "n_specs"]],
        hovertemplate="%{y} · " + k + "<br>median %{x:.3f}<br>%{customdata[0]} (%{customdata[1]} specifications)<extra></extra>"))
fig.add_vline(x=0, line=dict(color=MUTED, width=1))
base_layout(fig, xtitle="effect of a 1-point larger share on annual growth (pp)", height=480)
fig.update_yaxes(gridcolor="rgba(0,0,0,0)", autorange="reversed")
show(fig, x[["label", "subperiod", "median", "q10", "q90", "verdict", "n_specs"]].round(3),
     caption="Median estimate across specifications, with the 10th–90th percentile range. Marker shape = subperiod; colour = robustness verdict (green robustly positive, orange robustly negative, "
             "pale = leaning, grey = fragile). Each sector is tested on its own in the Szirmai–Verspagen specification.")
unit_note()

st.subheader("What this does and does not show")
st.markdown(
    "- These are **associations conditional on income, schooling, size, openness and the period**, estimated with "
    "methods (Hausman–Taylor, fixed effects) that reduce but do not remove reverse causation. A negative "
    "manufacturing coefficient does not show that manufacturing harms growth: commodity booms, for instance, "
    "raise growth while shrinking manufacturing's share (Dutch disease).\n"
    "- \"Motor\" here means: a larger share predicts faster subsequent growth. Manufacturing can matter in other "
    "ways — learning, exports, good jobs — that this test does not capture; the employment-share result hints at that.\n"
    "- Sectors are sectors: formal and informal segments within them cannot be separated with these data.")
footer()
