import streamlit as st

from motors_lib import SAMPLE_LABELS, footer, load

st.title("Replicating Szirmai & Verspagen (2015)")
st.markdown(
    "S&V estimated growth of GDP per head over five-year periods (1950–2005) on start-of-period manufacturing and "
    "services shares, income relative to the US, schooling, population, openness, a temperate-climate dummy and "
    "period dummies, with Hausman–Taylor as the main estimator. Their country list is not published and some "
    "sources differ here (PWT instead of Maddison, UN national accounts instead of WDI, a latitude-based climate "
    "dummy), so the test is whether **signs, rough sizes and significance** come out the same — fixed before "
    "estimation.")

c = load("replication/comparison.csv")
st.subheader("Verdict by coefficient and sample")
piv = c.pivot_table(index=["table", "model", "term"], columns="sample", values="verdict", aggfunc="first", sort=False)
st.dataframe(piv[["main", "excl_cpe", "core"]].rename(columns={k: SAMPLE_LABELS[k] for k in SAMPLE_LABELS}),
             width="stretch")

st.subheader("Coefficients")
smp = st.radio("Sample", ["main", "excl_cpe", "core"], format_func=SAMPLE_LABELS.get, horizontal=True)
x = c[c["sample"] == smp][["table", "model", "term", "sv_coef", "coef", "se", "p", "verdict", "nobs", "ncountries"]]
st.dataframe(x.rename(columns={"sv_coef": "S&V", "coef": "here"}).round(3), hide_index=True, width="stretch")
st.caption(f"Observations and countries: {int(x['nobs'].iloc[0])} and {int(x['ncountries'].iloc[0])} "
           "(S&V: 790 and 88).")

st.subheader("What replicates and what does not")
st.markdown(
    "- **The unconditional manufacturing effect does not replicate** in any sample: S&V's +0.045 (a 10-point larger "
    "share, 0.45 points faster growth) is close to zero or negative here.\n"
    "- **The interactions replicate closely in the sample without former planned economies** — manufacturing × "
    "income gap −0.24 (S&V −0.241), manufacturing × schooling +0.04 (S&V +0.027), both significant — and in every "
    "subperiod.\n"
    "- **They reverse in the core sample** that also excludes commodity exporters. The income-gap interaction rests "
    "on 13 observations from three Gulf oil states recorded at 1.6–9.8 times US income per head in 1970–2000; without "
    "them it turns positive.\n"
    "- Fixed and random effects agree with Hausman–Taylor, so the difference is the sample, not the estimator.\n\n"
    "The Hausman–Taylor implementation used here reproduces the published estimates for the standard textbook "
    "example (Cornwell–Rupert wage data) to five decimal places.")
footer()
