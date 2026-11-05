"""Extended: multi-year decompositions with survey-anchoring grades (WP05 main results)."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (C_DYNAMIC, C_STATIC, C_WITHIN, GRADE_COLORS, GRADE_TEXT, INK2, base_layout,
                 footer, load_output, show)

st.sidebar.header("Settings")
grid = st.sidebar.radio("Sector grid", ["A · 7 sectors", "B · 5 sectors (services combined)"], key="gp")[0]
st.title("Anchored period decompositions")
st.markdown("**Extension of the baseline.** The baseline decomposes year-to-year changes. Here, growth over the "
            "multi-year periods of WP05 is decomposed into within-sector growth and structural change, and "
            "structural change is split into its **static** and **dynamic** parts. Each country-period is "
            "**graded** by whether its endpoints are close to real survey years. Sectors are valued at each "
            "period's initial-year prices, which makes them add up exactly. Terms are contributions to average "
            "annual productivity growth, in percentage points per year.")

specs = {"Main: ILO modelled employment, initial-year prices": "main",
         "Robustness: survey employment at the nearest survey years (grade A only)": "robust_survey",
         "Robustness: final-year prices": "robust_final_prices",
         "Robustness: excluding mining and utilities": "robust_no_mining"}
spec = st.selectbox("Specification", list(specs))
m = load_output(grid, specs[spec])
main = load_output(grid, "main")
if m.empty:
    st.warning("No results for this specification.")
    st.stop()
if "grade" not in m.columns:
    m = m.merge(main[["iso3", "period", "grade"]], on=["iso3", "period"], how="left")
c1, c2 = st.columns([2, 1])
periods = list(dict.fromkeys(main["period"]))
per = c1.radio("Period", periods, horizontal=True, index=periods.index("2000–2019") if "2000–2019" in periods else 0)
grades = c2.multiselect("Grades shown", ["A", "B", "C"], default=["A", "B"],
                        help="\n".join(GRADE_TEXT.values()))

x = m[(m["period"] == per) & (m["grade"].isin(grades))].sort_values("growth_pp")
labels = [f"{r.country}  ·  {r.grade}" for r in x.itertuples()]
fig = go.Figure()
for col, lab, color in [("within_pp", "Within-sector", C_WITHIN), ("static_pp", "Structural: static", C_STATIC),
                        ("dynamic_pp", "Structural: dynamic", C_DYNAMIC)]:
    fig.add_trace(go.Bar(y=labels, x=x[col], name=lab, orientation="h", marker=dict(color=color),
                         hovertemplate="%{y}<br>" + lab + ": %{x:.2f} pp/yr<extra></extra>"))
fig.add_trace(go.Scatter(y=labels, x=x["growth_pp"], mode="markers", name="Total productivity growth",
                         marker=dict(color=INK2, size=9, symbol="diamond", line=dict(color="white", width=1)),
                         hovertemplate="%{y}<br>Total: %{x:.2f} pp/yr<extra></extra>"))
base_layout(fig, xtitle="percentage points per year", height=120 + 38 * max(len(x), 3))
fig.update_layout(barmode="relative")
fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
cols = ["country", "grade", "t0", "T", "growth_pp", "within_pp", "struct_pp", "static_pp", "dynamic_pp", "emp_growth_pct"]
show(fig, x[[c for c in cols if c in x.columns]].round(2),
     caption="The label after each country is its grade. " + " · ".join(GRADE_TEXT.values()) +
             ". Static = reallocation at initial productivity levels; dynamic = growing sectors also raising "
             "productivity (positive) or productivity rising in sectors that shed workers (negative).")

st.subheader("Structural-change term across specifications")
st.caption("Grade A and B country-periods for the selected period. Results that hold up keep their sign and "
           "rough size across specifications.")
rows = []
for lab, key in specs.items():
    r = load_output(grid, key)
    if r.empty:
        continue
    short = {"main": "Main", "robust_survey": "Survey employment", "robust_final_prices": "Final-year prices",
             "robust_no_mining": "Excl. mining & utilities"}[key]
    r = r[r["period"] == per][["country", "struct_pp"]].assign(spec=short)
    rows.append(r)
rb = pd.concat(rows)
rb = rb[rb["country"].isin(main[(main["period"] == per) & (main["grade"].isin(["A", "B"]))]["country"])]
fig = go.Figure()
sym = ["circle", "diamond", "square", "triangle-up"]
colors = ["#2a78d6", "#eb6834", "#1baf7a", "#6250d6"]
for i, (sp, g) in enumerate(rb.groupby("spec", sort=False)):
    fig.add_trace(go.Scatter(x=g["struct_pp"], y=g["country"], mode="markers", name=sp,
                             marker=dict(symbol=sym[i], size=10, color=colors[i], line=dict(color="white", width=1)),
                             hovertemplate="%{y}: %{x:.2f} pp/yr<extra>" + sp + "</extra>"))
fig.add_vline(x=0, line=dict(color="#c3c2b7"))
base_layout(fig, xtitle="structural-change term, pp per year", height=120 + 34 * rb["country"].nunique())
fig.update_layout(legend=dict(orientation="v", y=1.02, yanchor="bottom"))
show(fig, rb.pivot_table(index="country", columns="spec", values="struct_pp").round(2).reset_index())
st.caption("Guyana is a special case: its structural term is almost entirely dynamic and depends on the price "
           "base (2000–19: −3.06 at initial-year prices, −0.26 at final-year prices), and oil dominates "
           "2019–24 (+7.75; +0.04 without mining).")
footer()
