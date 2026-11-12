"""Extended: the productivity ladder, with people not in work at zero, and dominance verdicts."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (C_CONTEXT, C_HIGHLIGHT, GRADE_TEXT, INK2, LADDER_VERDICTS, MUTED, SHORT, STEP_NAMES, base_layout,
                 footer, load_extra, name, show)

st.title("Ladder of the working-age population")
st.markdown(
    "Each working-age person (15 and over) is placed at the output per worker of the sector they work in; people "
    "who are not employed are placed at zero. Sorting everyone from lowest to highest gives a ladder: the width of "
    "each step is the sector's share of the working-age population, its height the sector's output per worker. "
    "The area under the ladder equals output per working-age person. Unlike the ladder on the *Sectors and "
    "structural change* page, which covers employed workers only, this one includes everyone aged 15 and over.\n\n"
    "Comparing the ladder at the start and end of a period gives a verdict that does not depend on how gains at "
    "different points are weighted:\n"
    "- **improvement**: the later ladder is at or above the earlier one at every percentile (first-order dominance);\n"
    "- **improvement, weighting the lower percentiles**: the cumulative area is larger at every percentile "
    "(second-order dominance), so the change is an improvement for any criterion that gives at least as much "
    "weight to gains lower down;\n"
    "- **ambiguous**: the ladders cross in a way that neither criterion settles;\n"
    "- **depends on prices**: the verdict differs between initial- and final-year prices.\n\n"
    "Sector data give one step per sector, so everyone in a sector is treated as equally productive. The verdicts "
    "are about sector averages; splitting sectors into formal and informal, or by firm size, would add steps and "
    "could change them.")

lr, v, inc = load_extra("ladder", "ladders"), load_extra("ladder", "verdicts"), load_extra("ladder", "incidence")
if v.empty:
    st.warning("No results: run `empirics/code/lp/08_ladder.py`.")
    st.stop()

# ---- 1. one country
st.subheader("One country")
cs = sorted(v["iso3"].unique(), key=name)
c1, c2, c3 = st.columns([2, 2, 1])
iso = c1.selectbox("Country", cs, format_func=name, index=cs.index("MEX") if "MEX" in cs else 0)
periods = list(dict.fromkeys(v[v["iso3"] == iso]["period"]))
per = c2.selectbox("Period", periods, index=periods.index("2000–2019") if "2000–2019" in periods else 0)
base = c3.radio("Prices", ["initial", "final"], format_func=lambda b: f"{b.capitalize()}-year")
r = v[(v["iso3"] == iso) & (v["period"] == per) & (v["base"] == base)].iloc[0]
color = LADDER_VERDICTS[r["verdict"]]
st.markdown(
    f"<span style='background:{color};padding:2px 8px;border-radius:4px;color:#0b0b0b'>{r['verdict']}</span> "
    f"&nbsp; grade {r['grade']} · output per working-age person {(r['meanT'] / r['mean0']) ** (1 / (r['T'] - r['t0'])) * 100 - 100:+.2f}% a year · "
    f"{r['share_gained']:.0%} of percentiles at or above their starting level",
    unsafe_allow_html=True)

L = lr[(lr["iso3"] == iso) & (lr["period"] == per) & (lr["base"] == base)]
full = st.checkbox("Full height of the top step", value=False,
                   help="The top step (usually mining and utilities) is often several times higher than the rest. "
                        "By default the axis is cut above the second-highest step so the lower steps can be read.")


def label(s):
    return STEP_NAMES.get(s, SHORT.get(s, s))


fig = go.Figure()
tops = []
for yr, col, width in [(r["t0"], C_CONTEXT, 2.5), (r["T"], C_HIGHLIGHT, 2.5)]:
    g = L[L["year"] == yr].sort_values("cum_start")
    xs = list(100 * g["cum_start"]) + [100.0]
    ys = list(g["value"] / 1000) + [g["value"].iloc[-1] / 1000]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(shape="hv", color=col, width=width), name=str(yr),
                             hoverinfo="skip"))
    fig.add_trace(go.Scatter(
        x=100 * (g["cum_start"] + g["cum_end"]) / 2, y=g["value"] / 1000, mode="markers",
        marker=dict(size=6, color=col), showlegend=False,
        customdata=np.c_[[label(s) for s in g["step"]], 100 * g["weight"]],
        hovertemplate=f"{yr}: %{{customdata[0]}}<br>%{{customdata[1]:.1f}}% of the working-age population"
                      "<br>US$ %{y:.1f}k per worker<extra></extra>"))
    tops += sorted(g["value"] / 1000)[-2:]
gT = L[L["year"] == r["T"]].sort_values("cum_start")
for _, s in gT.iterrows():
    if s["weight"] > 0.035:
        fig.add_annotation(x=100 * (s["cum_start"] + s["cum_end"]) / 2, y=s["value"] / 1000, text=label(s["step"]),
                           showarrow=False, yshift=12, font=dict(size=10, color=INK2))
ymax = max(tops) * 1.08 if full else sorted(tops)[-3] * 1.35
base_layout(fig, xtitle="cumulative share of the population aged 15+ (%)",
            ytitle=f"output per worker, US$ thousand ({r['t0'] if base == 'initial' else r['T']} prices)", height=460)
fig.update_xaxes(range=[0, 100])
fig.update_yaxes(range=[0, ymax])
cut = [label(s) for s, val in zip(gT["step"], gT["value"] / 1000) if val > ymax]
tbl = L.assign(step=L["step"].map(label), share_pct=100 * L["weight"], usd_k=L["value"] / 1000)[
    ["year", "step", "share_pct", "usd_k"]].round(2)
show(fig, tbl, caption=f"Grey: {r['t0']}; blue: {r['T']}. Both years at {r['t0'] if base == 'initial' else r['T']} "
                       "prices (sector volumes from constant-price series). "
                       + (f"Above the axis: {', '.join(cut)} (see the data table). " if cut else "")
                       + "Steps under 3.5% of the population are not labelled.")

st.markdown("**Where along the ladder the change happened.** Change at each percentile, as a share of the starting "
            "mean, per year (initial-year prices). The average of the curve equals the growth of output per "
            "working-age person.")
ic = inc[(inc["iso3"] == iso) & (inc["period"] == per)]
fig = go.Figure(go.Scatter(x=ic["pct"], y=ic["incidence_pp"], mode="lines", line=dict(shape="hv", color=C_HIGHLIGHT, width=2),
                           hovertemplate="percentile %{x:.1f}: %{y:.2f}% of the starting mean a year<extra></extra>"))
fig.add_hline(y=ic["incidence_pp"].mean(), line=dict(color=MUTED, dash="dot"),
              annotation_text="average", annotation_position="top left")
base_layout(fig, xtitle="percentile of the population aged 15+", ytitle="% of starting mean per year", legend=False, height=320)
show(fig, ic[["pct", "incidence_pp"]].round(3), caption="Spikes at the top come from the narrow highest step; flat "
                                                         "stretches at the bottom are the zero block.")

st.markdown("**Below a productivity line.** z = output per employed worker at the start of the period (same prices). "
            "Share of the working-age population below the line, average gap (as a share of z) and squared gap.")
fg = pd.DataFrame({
    "Line": ["z", "z", "z / 2", "z / 2"], "Year": [r["t0"], r["T"]] * 2,
    "Share below": [r["H0"], r["HT"], r["H_half0"], r["H_halfT"]],
    "Average gap": [r["gap0"], r["gapT"], r["gap_half0"], r["gap_halfT"]],
    "Squared gap": [r["sev0"], r["sevT"], r["sev_half0"], r["sev_halfT"]]}).round(3)
st.dataframe(fg, hide_index=True, width="stretch")
st.caption(f"z = US$ {r['z'] / 1000:.1f}k per worker. Everyone not employed is below any positive line, so these "
           "indices fall when the employment rate rises even if no sector's productivity changes.")

# ---- 2. all countries
st.subheader("All countries")
grades = st.multiselect("Grades shown", ["A", "B", "C"], default=["A", "B"], help="\n".join(GRADE_TEXT.values()))
vi = v[(v["base"] == "initial") & (v["grade"].isin(grades))]
order = list(LADDER_VERDICTS)
cnt = vi.groupby(["period", "verdict"]).size().unstack(fill_value=0).reindex(columns=order, fill_value=0)
cnt = cnt.reindex([p for p in dict.fromkeys(v["period"]) if p in cnt.index])
fig = go.Figure()
for k in order:
    fig.add_trace(go.Bar(x=list(cnt.index), y=cnt[k], name=k, marker=dict(color=LADDER_VERDICTS[k]),
                         hovertemplate="%{x}: %{y} countries<extra>" + k + "</extra>"))
base_layout(fig, ytitle="countries", height=380)
fig.update_layout(barmode="stack", legend=dict(traceorder="normal"))
tab = vi.pivot_table(index="country", columns="period", values="verdict", aggfunc="first")
tab = tab[[p for p in dict.fromkeys(v["period"]) if p in tab.columns]].reset_index()
show(fig, tab, caption="Verdicts combine both price bases. The period 2019–2024 includes the pandemic; employment "
                       "in 2024 is largely modelled.")
footer()
