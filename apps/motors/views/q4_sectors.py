import plotly.graph_objects as go
import streamlit as st

from motors_lib import CATEGORICAL, SAMPLE_LABELS, SECTOR_LABELS, base_layout, footer, forest, load, show, unit_note

st.title("4. Other candidate motors: services and the rest")
st.markdown(
    "Each sector's share replaces manufacturing in the same specification. A sector is a *motor* if its share "
    "predicts faster growth with the same robustness demanded of manufacturing. Two data sets: UN national "
    "accounts (seven groups, all countries, 1970–2020) and the GGDC/UNU-WIDER Economic Transformation Database "
    "(twelve sectors including business and financial services, 51 developing and emerging economies, 1990–2020).")

st.subheader("Seven sector groups, 1970–2020 (UN national accounts)")
smp = st.radio("Sample", ["main", "core"], format_func=SAMPLE_LABELS.get, horizontal=True, key="q4s")
u = load("sectors/un_sectors.csv")
x = u[(u["sample"] == smp) & (u["estimator"] == "HT") & (u["subperiod"] != "1970–2020")].copy()
x["label"] = x["sector"].map(SECTOR_LABELS)
fig = forest(x, "label", group_col="subperiod", xtitle="pp of annual growth per point of the sector's share",
             order=list(SECTOR_LABELS.values()), height=520)
show(fig, x[["label", "subperiod", "coef", "se", "p", "nobs"]].round(3),
     caption="Hausman–Taylor, separate slope per subperiod. 95% intervals.")
v = load("sectors/un_verdicts.csv")
st.dataframe(v.pivot(index="label", columns="subperiod", values="verdict")[["1970–90", "1990–2005", "2005–20", "1970–2020"]],
             width="stretch")
st.caption("Verdicts combine the main and core samples and the HT and FE estimators (see page 3). The robustness "
           "page checks the same estimates across 96 specifications per sector.")
unit_note()

st.subheader("Twelve sectors, 1990–2020 (ETD): output share and employment share")
e = load("sectors/etd_sectors.csv")
y = e[(e["sample"] == "main") & (e["estimator"] == "HT")].copy()
y["measure"] = y["measure"].map({"va": "share of value added", "emp": "share of employment"})
fig = forest(y, "label", group_col="measure", xtitle="pp of annual growth per point of the sector's share", height=560,
             order=["Manufacturing", "Business services", "Financial services", "Trade services", "Transport services",
                    "Real estate", "Government services", "Other services", "Construction", "Agriculture", "Mining", "Utilities"])
show(fig, e[["label", "measure", "sample", "estimator", "coef", "se", "p", "nobs", "ncountries", "verdict"]].round(3),
     caption="Hausman–Taylor, main sample; up to 50 countries, five-year periods starting 1990–2015. Employment-share "
             "coefficients are larger in absolute value because employment shares of modern services are small.")
st.markdown(
    "- **Manufacturing: jobs, not output.** Its *employment* share predicts faster growth (robust across samples and "
    "estimators); its value-added share does not — the pattern Felipe, Mehta and Rhee (2019) describe.\n"
    "- **Business and financial services** — the services most often proposed as new motors — are associated with "
    "*slower* subsequent growth, by output and by employment. A larger modern-services share at a given income and "
    "schooling may signal an economy that has de-industrialised early rather than one with a new engine.\n"
    "- **Trade services and construction** by value-added share are associated with faster growth in this sample.")

st.subheader("The Caribbean: tourism")
c = load("sectors/caribbean_trh.csv")
st.markdown(
    "No tourism value-added series is available; trade, restaurants and hotels is the closest proxy. With a separate "
    "slope for the Caribbean (all countries regardless of size, 1970–2020): " + "; ".join(
        f"{r.estimator} {r.term.replace('TRH', 'slope ')} {r.coef:+.3f} (p = {r.p:.2f})" for r in c.itertuples()) +
    f". Only {int(c['n_caribbean_countries'].iloc[0])} Caribbean countries have all the variables. Tourism-heavy "
    "Caribbean economies grew more slowly at given income and schooling, not faster; the proxy is weak and the sample "
    "small, so this is not evidence against tourism-led growth (Cannonier & Burke 2019 find the opposite with "
    "tourism spending), only an absence of support for it here.")
footer()
