"""Study 9.2: which jobs build skills? Experience-earnings profiles by type of job."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from jobs_lib import C_HIGHLIGHT, CATEGORICAL, MUTED, TYPE_COLORS, base_layout, footer, load, show

st.title("9.2 Which jobs build skills?")
st.markdown(
    "Wages rise much less with experience in poor countries than in rich ones (Lagakos, Moll, Porzio, Qian and "
    "Schoellman 2018). For Mexico, on the 1990–2010 censuses, men with 20–24 years of experience earned 41% more "
    "than men just starting; in rich countries the figure was about 89%. This page asks whether Mexico's flat "
    "profile is **general** or **concentrated** in some types of job, using ENOE first quarters 2005–2025 "
    "(about 860,000 observations).\n\n"
    "**Sample.** Men, full-time, private-sector wage employees with positive hourly earnings and 0–40 years of "
    "potential experience (age − 18, or age − schooling − 6 with 12 or more years of schooling), as in Lagakos et al. "
    "The *height* of a profile is earnings at 20–24 years of experience relative to 0–4 years.")

h = load("profiles", "heights")
if h.empty:
    st.warning("No results: run `empirics/code/enoe/profiles/run_all.py` (needs the ENOE microdata).")
    st.stop()
cs = h[h["method"] == "cross-section"].set_index("group")

st.info(
    f"**Results.** Profiles are flat across the board: {cs.loc['all (baseline)', 'height']:.0%} for all baseline "
    f"workers, {cs.loc['formal', 'height']:.0%} in formal and {cs.loc['informal', 'height']:.0%} in informal jobs. "
    "Within the same sector, formal and informal profiles are about equal; differences across sectors are larger "
    "than the difference by formality, so the pre-registered proposition that formality is what separates steep "
    "from flat profiles is rejected. Formal profiles have flattened since 2005 and are now close to informal ones. "
    "The cohort-adjusted method of Lagakos et al. gives implausible negative profiles in these data and is not used "
    "for conclusions (see the last section).")

# ---- 1. profiles
st.subheader("Earnings by years of experience")
p = load("profiles", "profiles")
p = p[p["method"] == "cross-section"]
order = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39"]
opts = list(dict.fromkeys(p["group"]))
pick = st.multiselect("Groups", opts, default=["all (baseline)", "formal", "informal"])
fig = go.Figure()
for k, g in enumerate(pick):
    x = p[p["group"] == g].set_index("bin").reindex(order)
    others = [c for c in CATEGORICAL if c not in TYPE_COLORS.values()]
    col = TYPE_COLORS.get(g, others[k % len(others)])
    if x["lo90"].notna().all():
        fig.add_trace(go.Scatter(x=order + order[::-1], y=list(x["hi90"]) + list(x["lo90"])[::-1], fill="toself",
                                 fillcolor=col, opacity=0.15, line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=order, y=x["height"], mode="lines+markers", name=g, line=dict(color=col, width=2),
                             hovertemplate=g + "<br>%{x} years: %{y:+.1%}<extra></extra>"))
fig.add_hline(y=0.893, line=dict(color=MUTED, dash="dot"), annotation_text="rich countries, 20–24 years (Lagakos et al.)",
              annotation_position="top left")
fig.add_hline(y=0.411, line=dict(color=MUTED, dash="dash"), annotation_text="Mexico, censuses 1990–2010 (Lagakos et al.)",
              annotation_position="top left")
base_layout(fig, xtitle="years of potential experience", ytitle="earnings relative to 0–4 years", height=460)
fig.update_yaxes(tickformat=".0%")
fig.update_xaxes(type="category", categoryorder="array", categoryarray=order)
show(fig, p[p["group"].isin(pick)][["group", "bin", "height", "lo90", "hi90", "n"]].round(3),
     caption="Coefficients of five-year experience bins in a weighted regression of log hourly earnings with year "
             "effects, pooled over 2005–2025, converted to percentage differences from the 0–4 bin. Bands: 90% "
             "intervals from a bootstrap over primary sampling units (199 replications). Reference lines from "
             "Lagakos et al. (2018, Table 2), who use census data and the same sample definition.")

# ---- 2. heights by group
st.subheader("Height at 20–24 years, by type of job")
x = cs.drop(index=[g for g in cs.index if g.startswith("baseline, ages")], errors="ignore").sort_values("height")
fig = go.Figure(go.Scatter(
    x=x["height"], y=x.index, mode="markers", marker=dict(color=C_HIGHLIGHT, size=9),
    error_x=dict(type="data", symmetric=False, array=x["hi90"] - x["height"], arrayminus=x["height"] - x["lo90"],
                 thickness=1.2, width=0),
    customdata=x[["n"]], hovertemplate="%{y}: %{x:+.1%} (n = %{customdata[0]:,})<extra></extra>"))
fig.add_vline(x=0, line=dict(color=MUTED, width=1))
base_layout(fig, xtitle="earnings at 20–24 years relative to 0–4 years", legend=False, height=140 + 26 * len(x))
fig.update_xaxes(tickformat=".0%")
fig.update_yaxes(type="category", categoryorder="array", categoryarray=list(x.index), gridcolor="rgba(0,0,0,0)")
show(fig, x[["height", "lo90", "hi90", "n"]].round(3).reset_index(),
     caption="Sector groups combine ENOE's 11 sector groups into six. Formal and informal profiles are shown within "
             "manufacturing and commerce, the two sectors with enough informal wage workers. Own-account men "
             "(all hours) earn less with experience. Women's profiles are flatter than men's, as in Lagakos et al.")

# ---- 3. over time
st.subheader("Profiles have flattened since 2005")
dg = load("profiles", "diagnostics")
t = dg[dg["analysis"] == "cross-section by period"]
fig = go.Figure()
for k, g in enumerate(["all (baseline)", "formal", "informal"]):
    y = t[t["group"] == g]
    fig.add_trace(go.Scatter(x=y["period"], y=y["height_20_24"], mode="lines+markers", name=g,
                             line=dict(color=TYPE_COLORS[g], width=2),
                             hovertemplate=g + " %{x}: %{y:+.1%}<extra></extra>"))
base_layout(fig, ytitle="height at 20–24 years", height=360)
fig.update_yaxes(tickformat=".0%", rangemode="tozero")
nr = load("profiles", "nonresponse")
show(fig, t[["period", "group", "height_20_24", "n"]].round(3),
     caption="Same model estimated separately for each period (exploratory; not in the pre-analysis plan). The formal "
             "profile fell from about 36% to 19% while the informal one stayed near 15%. The share of baseline "
             "workers reporting earnings fell over the period (formal: 90% in 2005, 57% in 2025) by similar amounts "
             "at every level of experience, so differential non-response is an unlikely explanation, but it cannot "
             "be excluded.")

# ---- 4. composition
st.subheader("Is the national profile flat because of who works where?")
comp = load("profiles", "composition")
c = comp[comp["method"] == "cross-section"].iloc[0]
st.markdown(
    f"Informal jobs are {c['informal_share_0_4']:.0%} of baseline jobs at 0–4 years of experience and "
    f"{c['informal_share_20_24']:.0%} at 20–24 years, and informal entrants earn {abs(c['entry_gap_log']):.2f} log "
    "points less than formal entrants. Moving from informal to formal work with experience therefore *steepens* the "
    f"national profile (composition term {c['composition_order1']:+.3f} log points), while flatter informal profiles "
    f"flatten it ({c['within_order1']:+.3f}). The two roughly cancel: the national height "
    f"({c['national_log']:.3f} log points) is almost equal to the formal one ({c['formal_log']:.3f}). The flatness of "
    "Mexico's profile is not a composition effect; formal jobs themselves are flat.")

# ---- 5. methods
with st.expander("Cohort adjustment and within-person estimates: what did not work"):
    hl = h[h["method"].str.startswith("HLT")].set_index(["group", "method"])
    st.markdown(
        "Cross-sectional profiles mix experience with differences between birth cohorts. Lagakos et al. separate them "
        "by assuming that wages no longer rise with experience in the last ten years of a career (the "
        "Heckman–Lochner–Taber restriction). In these data that method gives **negative** profiles: "
        f"{hl.loc[('all (baseline)', 'HLT, flat spot 30-39'), 'height']:.0%} for all baseline workers. The result is the same "
        "on 2005–2018 alone, before the large minimum-wage increases from 2019, so those increases are not the "
        "explanation. The more likely reason is that the assumption fails in Mexico: cross-sectional earnings fall "
        "after 30 years of experience, especially in formal jobs, and the relative wages of older, less-schooled "
        "workers shifted over the period. Under those conditions the restriction attributes economy-wide changes to "
        "experience. These estimates are reported in the paper but not used for conclusions.\n\n"
        "Within-person earnings growth over a year, from the panels of study 9.1, avoids cohort effects but has 90% "
        "intervals from about −55% to over +300% for the implied height: one rotation group in two windows is too "
        "small, and reported earnings are noisy. A version using all five-quarter windows from 2005 onward would be "
        "large enough.")
    st.dataframe(h[h["method"] != "cross-section"][["group", "method", "height", "lo90", "hi90", "n"]].round(3),
                 hide_index=True, width="stretch")
    ph = load("profiles", "panel_heights")
    st.dataframe(ph.round(3), hide_index=True, width="stretch")
footer("First quarters 2005–2025 and the linked panels of study 9.1. Method: devtheory WP09, study 9.2, after "
       "Lagakos, Moll, Porzio, Qian and Schoellman (2018).")
