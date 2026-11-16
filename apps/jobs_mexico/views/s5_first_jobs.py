"""Study 9.5: where careers start."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from jobs_lib import C_CONTEXT, C_HIGHLIGHT, INK2, MUTED, TYPE_COLORS, base_layout, footer, load, show

st.title("9.5 First jobs and employment three quarters later")
st.markdown(
    "A first job is defined by the respondent's own answer: a person aged 15–24 who, at their first ENOE interview, "
    "is not working and says they have never worked, and who is working at the next interview, three months later. "
    "The same people are seen at three more interviews, so this page shows where first jobs lead within three "
    "quarters. Data pool about seventy five-quarter panels, 2005–2019 and 2022 onward.")

est = load("first_jobs", "estimates")
if est.empty:
    st.warning("No results: run `empirics/code/enoe/first_jobs/run_all.py` (needs the ENOE microdata).")
    st.stop()
chk = load("first_jobs", "checks").set_index("check")["value"]
m = est[est["spec"] == "main"].set_index("proposition")


def pp(r):
    return f"{100 * r['beta']:.1f} percentage points (90% interval {100 * r['lo90']:.1f} to {100 * r['hi90']:.1f})"


st.info(
    f"Of first jobs, {100 * chk['informal share of first jobs']:.1f}% are informal, against "
    f"{100 * chk['informal share of stock 15-24']:.1f}% of all jobs held by employed 15–24-year-olds. Conditional on age, "
    "sex, schooling, school attendance, household employment, state, urban residence and quarter, entering an informal "
    f"job is associated with a probability of formal employment three quarters later that is {pp(m.loc['P35'])} higher "
    f"than for never-worked young people who remained without work, whose rate is {100 * m.loc['P35', 'mean_control']:.1f}%. "
    f"Entering a formal rather than an informal job is associated with a difference of {pp(m.loc['P36'])}; this estimate is "
    "sensitive to selection on unobservables (see below). Among informal first jobs, the difference between wage jobs in "
    f"units with premises and own-account or unpaid work is {pp(m.loc['P37'])}. These are conditional associations, "
    "not causal effects.")

# ---------------------------------------------------------------- composition
st.subheader("Composition of first jobs")
comp = load("first_jobs", "composition")
dim = st.radio("By", ["formality", "position", "sector"], horizontal=True)
c = comp[comp["dimension"] == dim].sort_values("first_jobs")
fig = go.Figure()
fig.add_trace(go.Bar(y=c["category"], x=100 * c["stock"], name="all jobs of employed 15–24-year-olds", orientation="h",
                     marker=dict(color=C_CONTEXT), hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
fig.add_trace(go.Bar(y=c["category"], x=100 * c["first_jobs"], name="first jobs", orientation="h",
                     marker=dict(color=C_HIGHLIGHT), hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
base_layout(fig, xtitle="share, %", height=120 + 34 * len(c))
fig.update_layout(barmode="group")
show(fig, c[["category", "first_jobs", "stock"]].round(4),
     caption="First jobs: entrants aged 15–24 at the interview after the one where they said they had never worked; "
             "weighted. All jobs: every employed person aged 15–24 in the same quarters.")

# ---------------------------------------------------------------- where they lead
st.subheader("Employment status after entry")
tr = load("first_jobs", "transitions")
v = st.select_slider("Interview", options=[3, 4, 5], value=5,
                     format_func=lambda x: {3: "one quarter after entry", 4: "two quarters after", 5: "three quarters after"}[x])
t = tr[tr["interview"] == v]
order = ["formal", "informal wage, premises", "informal wage, other", "informal own-account or unpaid", "not employed"]
t = t[t["entry"].isin(order)]
SC = {"formal": C_HIGHLIGHT, "informal": TYPE_COLORS["informal"], "not employed": C_CONTEXT,
      "employed, formality unknown": MUTED}
fig = go.Figure()
for s_, colr in SC.items():
    g = t[t["state"] == s_].set_index("entry").reindex(order)
    fig.add_trace(go.Bar(y=[e if e != "not employed" else "kept not working" for e in order], x=100 * g["share"],
                         name=s_, orientation="h", marker=dict(color=colr),
                         hovertemplate="%{y}: %{x:.1f}% " + s_ + "<extra></extra>"))
base_layout(fig, xtitle="share at the later interview, %", height=330)
fig.update_layout(barmode="stack")
show(fig, t[["entry", "state", "share", "n"]].round(4),
     caption="Rows: the first job at entry (informal jobs split by type of unit and position), and young people who "
             "had never worked and still were not working at the same interview. Not adjusted for who takes which job.")

# ---------------------------------------------------------------- estimates
st.subheader("Conditional comparisons")
LAB = {"P35": "informal first job vs. kept not working", "P36": "formal vs. informal first job",
       "P37": "informal wage job with premises vs. informal own-account or unpaid"}
p = st.selectbox("Comparison", list(LAB), format_func=LAB.get)
e = est[(est["proposition"] == p) & est["lo90"].notna()].copy()
e = e.sort_values("spec", key=lambda s: s.map(lambda x: (x != "main", x.startswith(("group", "period")), x)))
fig = go.Figure(go.Scatter(x=100 * e["beta"], y=e["spec"], mode="markers",
                           marker=dict(color=[C_HIGHLIGHT if s == "main" else INK2 for s in e["spec"]], size=9),
                           error_x=dict(type="data", symmetric=False, array=100 * (e["hi90"] - e["beta"]),
                                        arrayminus=100 * (e["beta"] - e["lo90"]), color=MUTED, thickness=1.2),
                           hovertemplate="%{y}: %{x:+.1f} points<extra></extra>"))
fig.add_vline(x=0, line=dict(color=MUTED, dash="dot"))
base_layout(fig, xtitle="difference in the probability of formal employment three quarters later, points (90% interval)",
            height=140 + 26 * len(e), legend=False)
fig.update_yaxes(autorange="reversed")
show(fig, e[["spec", "beta", "lo90", "hi90", "mean_control", "n", "n_treated"]].round(4),
     caption="Weighted linear probability models with fixed effects for quarter, state, age, schooling and relationship to "
             "the household head, and controls for sex, school attendance, employed household members and urban residence; "
             "standard errors clustered by primary sampling unit.")
o = load("first_jobs", "oster")
o = o[o["proposition"] == p]
st.markdown(
    f"Selection on unobservables: adding the controls moves the estimate from {100 * o['beta_short'].iloc[0]:+.1f} to "
    f"{100 * o['beta_long'].iloc[0]:+.1f} points. Following Oster (2019), selection on unobserved characteristics would "
    f"have to be {o['delta_for_zero'].iloc[0]:.1f} times as strong as selection on the observed ones (with R² max = 1.3 × "
    f"the controlled R²) to bring the difference to zero.")

# ---------------------------------------------------------------- earnings
st.subheader("Pay and hours in first jobs")
er = load("first_jobs", "earnings")
er = er[er["entry"].isin(order[:-1])]
st.dataframe(er.rename(columns={"median_rel_min": "median, × minimum wage", "p25": "25th percentile", "p75": "75th percentile",
                                "hours_mean": "weekly hours", "reporting": "share reporting earnings"}).round(2),
             hide_index=True, width="stretch")
st.caption("Monthly earnings at entry relative to the monthly minimum wage in force where the person lives, among those "
           "reporting an amount.")
footer("Panels 2005–2019 and 2022 onward. Method: devtheory WP09, study 9.5.")
