"""Study 9.4: the 2019 border minimum wage."""
import json

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from jobs_lib import C_CONTEXT, C_HIGHLIGHT, INK2, MUTED, OUT, TYPE_COLORS, base_layout, footer, load, show

st.title("9.4 The 2019 border minimum wage")
st.markdown(
    "On 1 January 2019 the daily minimum wage in the 43 municipalities of the northern border zone (Zona Libre de la "
    "Frontera Norte) doubled, from 88.36 to 176.72 pesos; elsewhere it rose 16%. The same decree cut VAT from 16% to "
    "8% and income tax for eligible firms in the same municipalities, so the estimates are of the package, not of the "
    "minimum wage alone. The comparison is with the other municipalities of the six border states, 2016Q1–2019Q4, "
    "with ENOE.")

d = load("border_mw", "did")
if d.empty:
    st.warning("No results: run `empirics/code/enoe/border_mw/run_all.py` (needs the ENOE microdata).")
    st.stop()
m = d[d["spec"] == "main"].set_index("outcome")
pre = load("border_mw", "pre_means").set_index("outcome")["pre_mean_zone"]
rr = load("border_mw", "ranges_did").set_index("outcome")
rnone = rr.loc["fc_none", "beta"] + rr.loc["ic_none", "beta"]


def ci(o, k=1, pct=False):
    r = m.loc[o]
    f = (lambda x: f"{100 * x:+.{k}f}") if pct else (lambda x: f"{x:+.{k}f}")
    return f"{f(r['beta'])} (90% interval {f(r['lo90'])} to {f(r['hi90'])})"


st.info(
    f"**Results.** Employment did not fall: the employment rate of the population aged 15+ changed by "
    f"{ci('emp_rate', 1, True)} percentage points. The reported earnings distribution moved at the new "
    f"minimum: the share of wage employees reporting less than it fell by {-100 * m.loc['below_m', 'beta']:.1f} points. "
    f"But the share reporting an amount fell by {-100 * m.loc['report', 'beta']:.1f} points at the same time. Counting "
    f"answers given in ranges of the minimum wage, between {-100 * (rr.loc['c_missing', 'beta'] + rnone):.1f} and "
    f"{-100 * rr.loc['c_missing', 'beta']:.1f} jobs per 100 people aged 15+ moved out of the range below the new minimum. "
    f"Moves from informal to formal work did not increase: the quarterly "
    f"rate changed by {ci('i_to_f', 1, True)} points, against a pre-period rate of {100 * pre['i_to_f']:.1f}%.")

with st.expander("A change in the ENOE sample in the border zone in 2019"):
    st.markdown(
        "In 2019Q1 INEGI enlarged the ENOE sample in the border-zone municipalities only: primary sampling units rose "
        "from 1,169 to 2,029 and records from about 20,800 to 34,000 a quarter, in all five rotation groups at once. "
        "A sample change at the date of the policy, and only where it applied, could produce spurious before–after "
        "differences. All estimates on this page use only the sampling units that were already in the survey in "
        "2016–2018; they leave the sample at the same pace in the border zone and elsewhere. Results with the full "
        "sample are in the robustness table.")

# ---------------------------------------------------------------- maps
st.subheader("Municipalities before, during and after")
geo = json.loads((OUT / "border_mw" / "municipalities.geojson").read_text())
mv = load("border_mw", "map_values")
MAP_OUT = {"below_m": "Share of wage employees earning below the new minimum",
           "lnw": "Mean log hourly earnings of wage employees",
           "formal_share": "Formal share of employment",
           "i_to_f": "Quarterly rate of moves from informal to formal work"}
c1, c2 = st.columns([3, 2])
o = c1.selectbox("Outcome", list(MAP_OUT), format_func=MAP_OUT.get)
shr = c2.radio("Changes", ["shrunk (empirical Bayes)", "raw"], horizontal=True)
ids = [f["id"] for f in geo["features"]]
zone_ids = [f["id"] for f in geo["features"] if f["properties"]["zlfn"]]
names = {f["id"]: f["properties"]["name"] for f in geo["features"]}


def mapfig(v, col, title, diverging, rng):
    fig = go.Figure()
    fig.add_trace(go.Choroplethmap(geojson=geo, locations=ids, z=[0] * len(ids), featureidkey="id",
                                colorscale=[[0, "#d4d3cc"], [1, "#d4d3cc"]], showscale=False,
                                marker_line_color="#ffffff", marker_line_width=0.4, hoverinfo="skip"))
    v = v[v["shown"]]
    loc = [f"{e:02d}{u:03d}" for e, u in zip(v["ent"], v["mun"])]
    scale = [[0, C_HIGHLIGHT], [0.5, "#f5f4ef"], [1, TYPE_COLORS["informal"]]] if diverging else \
        [[0, "#f5f4ef"], [1, C_HIGHLIGHT]]
    fig.add_trace(go.Choroplethmap(
        geojson=geo, locations=loc, z=v[col], featureidkey="id", colorscale=scale, zmin=rng[0], zmax=rng[1],
        marker_line_color="#ffffff", marker_line_width=0.4,
        colorbar=dict(thickness=10, len=0.7, title=None),
        customdata=np.column_stack([v["name"], v["n"], v["level"], v["change_net"], v["change_se"]]),
        hovertemplate="%{customdata[0]}<br>level %{customdata[2]:.3f}<br>net change %{customdata[3]:+.3f} "
                      "(s.e. %{customdata[4]:.3f})<br>%{customdata[1]} records<extra></extra>"))
    fig.add_trace(go.Choroplethmap(geojson=geo, locations=zone_ids, z=[1] * len(zone_ids), featureidkey="id",
                                   colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]], showscale=False,
                                   marker_line_color="#0b0b0b", marker_line_width=1.2, hoverinfo="skip"))
    # MapLibre with the blank built-in style: no tiles or other files are fetched from the web.
    fig.update_layout(height=540, margin=dict(l=0, r=0, t=30, b=0), title=dict(text=title, x=0, font=dict(size=14)),
                      paper_bgcolor="rgba(0,0,0,0)",
                      map=dict(style="white-bg", center=dict(lon=-106.6, lat=28.4), zoom=4.45))
    return fig


col = "change_eb" if shr.startswith("shrunk") else "change_net"
x = mv[mv["outcome"] == o]
ch = x[(x["period"] != "before") & x["shown"]][col]
lim = float(np.nanpercentile(np.abs(ch), 95)) if len(ch) else 1.0
t1, t2, t3 = st.tabs(["Before: 2016–2018 level", "During: 2019, change", "After: 2020Q1, change"])
with t1:
    b = x[x["period"] == "before"]
    lv = b[b["shown"]]["level"]
    show(mapfig(b, "level", "Level, 2016Q1–2018Q4", False, (float(lv.quantile(0.05)), float(lv.quantile(0.95)))),
         key="map_before")
with t2:
    show(mapfig(x[x["period"] == "during"], col, "Change from before to 2019, net of the control mean", True,
                (-lim, lim)), key="map_during")
with t3:
    show(mapfig(x[x["period"] == "after"], col, "Change from before to 2020Q1, net of the control mean", True,
                (-lim, lim)), key="map_after")
st.caption(
    "Black outline: the border zone. Coloured: municipalities with at least 300 ENOE records (aged 15+) in the "
    "period and before; grey: not sampled or too few records. ENOE is not designed to be representative by "
    "municipality, so the maps are descriptive. Near-white means no change relative to the controls. Changes are net of the population-weighted mean change in control "
    "municipalities; the shrunk version pulls each change towards its group mean in proportion to its sampling "
    "variance (bootstrap over sampling units). Control municipalities shrink almost entirely to their mean: their "
    "changes vary no more than sampling error would produce. 2020Q1 is a single quarter, so fewer municipalities "
    "qualify. Boundaries: CONABIO/INEGI 2020.")

# ---------------------------------------------------------------- discontinuity
st.subheader("Change against distance to the edge of the zone")
rd = load("border_mw", "rd_bins")
s = x[(x["period"] == "during") & x["shown"]]
r = rd[rd["outcome"] == o]
fig = go.Figure()
for z, colr, lab in [(True, TYPE_COLORS["informal"], "border-zone municipality"),
                     (False, C_CONTEXT, "control municipality")]:
    g = s[s["zlfn"] == z]
    fig.add_trace(go.Scatter(x=g["dist_km"], y=g["change_net"], mode="markers", name=lab,
                             marker=dict(color=colr, size=np.clip(np.sqrt(g["n"]) / 4, 5, 26), opacity=0.75,
                                         line=dict(color="#ffffff", width=0.5)),
                             customdata=np.column_stack([g["name"], g["n"]]),
                             hovertemplate="%{customdata[0]}<br>%{x:.0f} km<br>net change %{y:+.3f}<br>"
                                           "%{customdata[1]} records<extra></extra>"))
for side in ["inside", "outside"]:
    f = r[r["kind"] == f"fit_{side}"]
    if len(f):
        fig.add_trace(go.Scatter(x=f["dist_km"], y=f["value"], mode="lines", showlegend=False, hoverinfo="skip",
                                 line=dict(color=INK2, width=2)))
fig.add_vline(x=0, line=dict(color=MUTED, dash="dot"))
base_layout(fig, xtitle="distance from the municipality's centroid to the edge of the zone, km (negative: inside)",
            ytitle="change, 2019 against 2016–2018, net of controls", height=430)
show(fig, s[["name", "zlfn", "dist_km", "n", "level", "change_net", "change_se"]].round(4),
     caption="Each point is a municipality (size: records). Lines: population-weighted linear fits on each side, within "
             "200 km of the edge and over the observed range. This is a picture of the difference in differences across "
             "space, not a separate estimate: municipalities are large, few lie close to the edge, and centroids can be "
             "far from where people live.")

# ---------------------------------------------------------------- event studies
st.subheader("Quarter by quarter")
ev = load("border_mw", "event")
pt = load("border_mw", "pretrend").set_index("outcome")["p_pretrend_wild"]
EV_OUT = {"below_m": "Share of reporting wage employees below the new minimum", "report": "Share of wage employees "
          "reporting earnings", "lnw": "Mean log hourly earnings", "emp_rate": "Employment rate, 15+",
          "formal_share": "Formal share of employment", "i_to_f": "Informal to formal, quarterly rate",
          "missing": "Wage employees below the new minimum, per person 15+",
          "excess": "Wage employees at 1.0–1.5 times the new minimum, per person 15+"}
eo = st.selectbox("Outcome ", list(EV_OUT), format_func=EV_OUT.get)
e = ev[ev["outcome"] == eo].sort_values("t")
lab = [f"{2016 + t // 4}Q{t % 4 + 1}" for t in e["t"]]
fig = go.Figure()
fig.add_trace(go.Scatter(x=lab, y=e["beta"] + 1.645 * e["se_cr1"], mode="lines", line=dict(width=0), showlegend=False,
                         hoverinfo="skip"))
fig.add_trace(go.Scatter(x=lab, y=e["beta"] - 1.645 * e["se_cr1"], mode="lines", line=dict(width=0), fill="tonexty",
                         fillcolor="rgba(42,120,214,0.15)", showlegend=False, hoverinfo="skip"))
fig.add_trace(go.Scatter(x=lab, y=e["beta"], mode="lines+markers", line=dict(color=C_HIGHLIGHT, width=2),
                         marker=dict(size=6), showlegend=False, hovertemplate="%{x}: %{y:+.4f}<extra></extra>"))
fig.add_vline(x=11.5, line=dict(color=MUTED, dash="dot"))
base_layout(fig, ytitle="border zone minus control, relative to 2018Q4", height=380)
show(fig, e.assign(quarter=lab)[["quarter", "beta", "se_cr1"]].round(4),
     caption=f"90% intervals clustered by municipality. Joint test of no pre-period differences (wild bootstrap): "
             f"p = {pt.get(eo, np.nan):.2f}. 2020Q1 is shown but not used in the averages: the 2020 increase was 5% "
             f"in the zone and 20% elsewhere, and fieldwork was interrupted in March.")

# ---------------------------------------------------------------- bins
st.subheader("Where in the earnings distribution")
bn = load("border_mw", "bins")
bn = bn[bn["measure"] == "monthly"]
BL = {"b00_06": "< 0.6", "b06_08": "0.6–0.8", "b08_10": "0.8–1.0", "b10_12": "1.0–1.2", "b12_15": "1.2–1.5",
      "b15_20": "1.5–2", "b20_30": "2–3", "b30_up": "≥ 3", "norep": "not reported"}
fig = go.Figure()
for f, colr in [("formal", C_HIGHLIGHT), ("informal", TYPE_COLORS["informal"])]:
    g = bn[bn["formality"] == f]
    fig.add_trace(go.Bar(x=[BL[b] for b in g["bin"]], y=100 * g["beta"], name=f"{f} wage employees",
                         marker=dict(color=colr), customdata=g["p_wild"],
                         hovertemplate="%{x}: %{y:+.2f} per 100 people 15+ (p = %{customdata:.2f})<extra></extra>"))
base_layout(fig, xtitle="monthly earnings relative to the new border minimum (5,302 pesos)",
            ytitle="change per 100 people aged 15+", height=380)
fig.update_layout(barmode="group")
show(fig, bn[["formality", "bin", "beta", "p_wild", "pre_mean_zone"]].round(5),
     caption="Difference-in-differences effect on the number of wage employees in each earnings bin per person aged "
             "15+. Jobs below the new minimum fell and jobs just above it rose, mostly in formal employment; the "
             "number not reporting earnings rose by almost as much as the jobs below the minimum fell. If every "
             "additional non-reporter would have reported less than the minimum, there were almost no missing jobs; "
             "if none would have, the missing jobs are as shown. The next section counts answers given in ranges.")

# ---------------------------------------------------------------- range answers
st.subheader("Why fewer workers reported earnings")
st.markdown(
    "Respondents who give no amount are asked whether their income is below, equal to, or in ranges of the minimum "
    "wage, which the interviewer reads out: 5,302 pesos a month in the zone in 2019. An addendum to the plan, written "
    "before these answers were tabulated by zone or period, tests whether the fall in reporting is a shift to such "
    "range answers.")
ANS = {"sh_amount": "amount", "sh_range": "range (any)", "sh_p6c1": "  below the minimum", "sh_p6c2": "  equal to the "
       "minimum", "sh_p6c3": "  1–2 minimums", "sh_p6c4": "  2–3 minimums", "sh_p6c5": "  3–5 minimums",
       "sh_p6c6": "  5–10 minimums", "sh_none": "no answer (refused, don't know)"}
at = rr.loc[list(ANS)].reset_index()
at["answer"] = at["outcome"].map(ANS)
fig = go.Figure(go.Bar(y=at["answer"][::-1], x=100 * at["beta"][::-1], orientation="h",
                       marker=dict(color=[TYPE_COLORS["informal"] if "none" in o else C_HIGHLIGHT for o in at["outcome"][::-1]]),
                       error_x=dict(type="data", symmetric=False, array=100 * (at["hi90"] - at["beta"])[::-1],
                                    arrayminus=100 * (at["beta"] - at["lo90"])[::-1], color=INK2, thickness=1),
                       hovertemplate="%{y}: %{x:+.1f} points<extra></extra>"))
base_layout(fig, xtitle="change in the share of wage employees giving each answer, percentage points (90% interval)",
            height=380, legend=False)
show(fig, at[["answer", "beta", "lo90", "hi90", "p_wild", "pre_mean_zone"]].round(4),
     caption="Range answers rose by less than a quarter of the fall in reported amounts, and the rise is at and near the "
             "new minimum: 'equal to the minimum' went from 0.5% of wage employees to about 1.7%. Higher ranges fell partly "
             "because the minimum read out doubled. Most of the fall is a rise in refusals and 'don't know'.")
cb = load("border_mw", "ranges_bins")
fig = go.Figure()
for f, colr in [("formal", C_HIGHLIGHT), ("informal", TYPE_COLORS["informal"])]:
    g = cb[cb["formality"] == f]
    fig.add_trace(go.Bar(x=[BL["norep" if b == "none" else b] for b in g["bin"]], y=100 * g["beta"],
                         name=f"{f} wage employees", marker=dict(color=colr), customdata=g["p_wild"],
                         hovertemplate="%{x}: %{y:+.2f} per 100 people 15+ (p = %{customdata:.2f})<extra></extra>"))
base_layout(fig, xtitle="monthly earnings relative to the new border minimum, range answers included",
            ytitle="change per 100 people aged 15+", height=380)
fig.update_layout(barmode="group")
show(fig, cb[["formality", "bin", "beta", "p_wild", "pre_mean_zone"]].round(5),
     caption=f"Range answers spread uniformly over their intervals, using the minimum in force for each person and "
             f"quarter ('equal to the minimum' as a point). Missing jobs below the minimum: "
             f"{100 * rr.loc['c_missing', 'beta']:+.1f} per 100 ({100 * rr.loc['c_missing', 'lo90']:+.1f} to "
             f"{100 * rr.loc['c_missing', 'hi90']:+.1f}); excess at 1.0–1.5 times: {100 * rr.loc['c_excess', 'beta']:+.1f} "
             f"({100 * rr.loc['c_excess', 'lo90']:+.1f} to {100 * rr.loc['c_excess', 'hi90']:+.1f}). The remaining rise in "
             f"non-response ({100 * rnone:+.1f}) bounds missing jobs between {100 * (rr.loc['c_missing', 'beta'] + rnone):+.1f} "
             f"and {100 * rr.loc['c_missing', 'beta']:+.1f}.")

# ---------------------------------------------------------------- flows and robustness
st.subheader("Flows and robustness")
FL = {"i_to_f": "informal → formal", "n_to_f": "not employed → formal", "f_to_i": "formal → informal",
      "f_to_n": "formal → not employed", "i_to_n": "informal → not employed"}
fl = m.loc[list(FL)].reset_index()
fl["transition"] = fl["outcome"].map(FL)
fl["pre-period rate, zone"] = fl["outcome"].map(pre)
st.markdown("**Quarterly transition rates** (difference in differences, 90% wild bootstrap interval)")
st.dataframe(fl[["transition", "beta", "lo90", "hi90", "p_wild", "pre-period rate, zone"]].round(4),
             hide_index=True, width="stretch")
rob = d[d["outcome"].isin(["emp_rate", "below_m", "lnw", "i_to_f", "report"])]
piv = rob.pivot(index="spec", columns="outcome", values="beta").round(4).reset_index()
st.markdown("**Estimates under each specification**")
st.dataframe(piv, hide_index=True, width="stretch")
st.caption("Specifications set in the pre-analysis plan, plus one exploratory variant added after seeing the event "
           "studies (pre-period from 2017Q3). Groups re-estimate the main specification on subpopulations.")
footer("Municipal boundaries: CONABIO (2020), from INEGI's Marco Geoestadístico. Method: devtheory WP09, study 9.4.")
