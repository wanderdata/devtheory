import pandas as pd
import streamlit as st

from motors_lib import SAMPLE_LABELS, footer, forest, load, show

st.title("3. Why does manufacturing work as a motor only in some contexts?")
st.markdown(
    "Each candidate condition is interacted with the manufacturing share, one at a time, in the S&V "
    "specification (1950–2020). The interaction measures how much manufacturing's growth effect changes as the "
    "condition changes; the mechanism each stands for, and the sign it predicts, were fixed before estimation. "
    "Conditions are centred at the median developing country.")

q = load("questions/q3_moderators.csv")
one = q[q["mode"] == "one at a time"].copy()
mech = {"EDU_HC": "+", "RELUS": "−", "OPEN": "+", "LNPOP": "+", "MIU": "−", "UNDERVAL": "+", "POST2000": "−"}
one["condition"] = one["label"]
v = one.groupby("condition").agg(predicted=("moderator", lambda s: mech[s.iloc[0]]), verdict=("verdict", "first")).reset_index()

st.subheader("Verdicts")
st.dataframe(v.rename(columns={"condition": "Condition (mechanism)", "predicted": "Predicted sign", "verdict": "Verdict"}),
             hide_index=True, width="stretch")
st.caption("Verdict rule: within a sample, the condition counts as supported if Hausman–Taylor and fixed effects "
           "both give the predicted sign and at least one is significant at 10%. It is *supported* if that holds in "
           "both the main and the core sample, *in one sample only* if in one, *conflicting* if the samples point in "
           "opposite directions.")

st.subheader("Estimates")
smp = st.radio("Sample", ["main", "core"], format_func=SAMPLE_LABELS.get, horizontal=True)
x = one[one["sample"] == smp]
fig = forest(x, "condition", group_col="estimator", xtitle="change in the manufacturing slope per unit of the condition")
show(fig, x[["condition", "estimator", "coef", "se", "p", "predicted_sign", "nobs"]].round(4),
     caption="Units differ by condition (years of schooling, ratio to US income, % of GDP, log points, % of value "
             "added, index, dummy), so compare signs and significance, not sizes.")

st.subheader("Reading")
st.markdown(
    "- **The income gap** is S&V's central condition (manufacturing pays more the poorer the country). It holds in "
    "the main sample and *reverses* in the core sample. The main-sample result depends on 13 observations from "
    "three Gulf oil states recorded at 1.6 to 9.8 times US income per head between 1970 and 2000.\n"
    "- **Schooling** raises manufacturing's payoff in the core sample, as S&V argued; in the main sample the sign "
    "is the same but not significant.\n"
    "- **Currency undervaluation** strongly raises manufacturing's payoff in the core sample (consistent with "
    "Rodrik's argument about tradables). In the main sample it has the opposite sign (significant with "
    "Hausman–Taylor), where planned and oil economies' price levels dominate the index.\n"
    "- **Country size** raises manufacturing's payoff in the main sample only.\n"
    "- **After 2000** manufacturing's payoff falls in the core sample, consistent with competition from China.\n"
    "- **Openness and commodity dependence** show no effect.")
footer()
