"""Extended: multi-year decompositions with survey-anchoring grades and a choice of price base."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (C_DYNAMIC, C_STATIC, C_WITHIN, GRADE_TEXT, INK2, PRICE_BASES, PRICE_NOTE,
                 base_layout, footer, load_output, output_name, price_choice, scope_info, show, verdicts)

st.sidebar.header("Settings")
grid = st.sidebar.radio("Sector grid", ["A · 7 sectors", "B · 5 sectors (services combined)"], key="gp")[0]
price = price_choice(key="pp")
st.title("Period decompositions")
st.markdown("**Extension of the baseline.** The baseline decomposes year-to-year changes. Here, growth over "
            "multi-year periods is decomposed into within-sector growth and structural change, and structural "
            "change is split into its **static** and **dynamic** parts. Each country-period is **graded** by "
            "whether its endpoints are close to real survey years. Terms are contributions to average annual "
            "productivity growth, in percentage points per year. "
            f"Price base now: **{PRICE_BASES[price]}** (change it in the sidebar).")
with st.expander("Note: how the three price bases differ, and which results to trust"):
    st.markdown(PRICE_NOTE)

specs = {"ILO modelled employment": "model",
         "Excluding mining and utilities": "no_mining",
         "Survey employment at the nearest survey years (grade A only; initial-year prices)": "survey"}
spec = st.selectbox("Specification", list(specs))
m = load_output(grid, output_name(specs[spec], price))
grades_ref = load_output(grid, "main")[["iso3", "period", "grade"]]
if m.empty:
    st.warning("No results for this specification.")
    st.stop()
if specs[spec] == "survey" and price != "initial":
    st.info("Survey employment exists only in survey years, so these decompositions cannot be chained; "
            "they are shown at initial-year prices whatever the price base selected.")
if "grade" not in m.columns:
    m = m.merge(grades_ref, on=["iso3", "period"], how="left")
c1, c2 = st.columns([2, 1])
periods = list(dict.fromkeys(grades_ref["period"]))
per = c1.radio("Period", periods, horizontal=True, index=periods.index("2000–2019") if "2000–2019" in periods else 0)
grades = c2.multiselect("Grades shown", ["A", "B", "C"], default=["A", "B"],
                        help="\n".join(GRADE_TEXT.values()))

if specs[spec] != "survey":
    m = m.merge(verdicts(grid, no_mining=specs[spec] == "no_mining"), on=["iso3", "period"], how="left")
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
base_layout(fig, xtitle="percentage points per year", height=120 + 30 * max(len(x), 3))
fig.update_layout(barmode="relative")
fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
cols = ["country", "grade", "verdict", "t0", "T", "growth_pp", "within_pp", "struct_pp", "static_pp", "dynamic_pp",
        "emp_growth_pct", "official_growth_pp"]
show(fig, x[[c for c in cols if c in x.columns]].round(2),
     caption="The label after each country is its grade. " + " · ".join(GRADE_TEXT.values()) +
             ". Static = reallocation at initial productivity levels; dynamic = growing sectors also raising "
             "productivity (positive) or productivity rising in sectors that shed workers (negative). "
             "official_growth_pp (fixed-base views) = growth of total value added per worker from the UN's "
             "chain-linked constant-price total, a check on the price base.")

# ---- robustness across price bases and specifications
st.subheader("Structural-change term across price bases and specifications")
st.caption("Grade A and B country-periods for the selected period. A result that keeps its sign and rough "
           "size across all markers does not depend on the price base or the employment source; one that "
           "flips should not be read as a finding. The verdict for each country is in the table above.")
variants = [("Initial-year prices", "main"), ("Chained", "robust_chained"),
            ("Final-year prices", "robust_final_prices"), ("Survey employment", "robust_survey"),
            ("Excl. mining & utilities", "robust_no_mining")]
rows = []
for short, key in variants:
    r = load_output(grid, key)
    if r.empty:
        continue
    rows.append(r[r["period"] == per][["country", "struct_pp"]].assign(spec=short))
rb = pd.concat(rows)
keep = load_output(grid, "main")
keep = keep[(keep["period"] == per) & (keep["grade"].isin(["A", "B"]))]["country"]
rb = rb[rb["country"].isin(keep)]
order = (rb[rb["spec"] == "Initial-year prices"].sort_values("struct_pp")["country"].tolist()
         or sorted(rb["country"].unique()))
fig = go.Figure()
sym = ["circle", "diamond", "square", "triangle-up", "x"]
colors = ["#2a78d6", "#eb6834", "#1baf7a", "#6250d6", "#898781"]
for i, (sp, g) in enumerate(rb.groupby("spec", sort=False)):
    fig.add_trace(go.Scatter(x=g["struct_pp"], y=g["country"], mode="markers", name=sp,
                             marker=dict(symbol=sym[i], size=10 if i == 0 else 8, color=colors[i],
                                         line=dict(color="white", width=1)),
                             hovertemplate="%{y}: %{x:.2f} pp/yr<extra>" + sp + "</extra>"))
fig.add_vline(x=0, line=dict(color="#c3c2b7"))
base_layout(fig, xtitle="structural-change term, pp per year", height=140 + 26 * rb["country"].nunique())
fig.update_yaxes(categoryorder="array", categoryarray=order)
fig.update_layout(legend=dict(orientation="h", y=1.0, yanchor="bottom"))
show(fig, rb.pivot_table(index="country", columns="spec", values="struct_pp").round(2).reset_index())
if "GUY" in set(m["iso3"]):
    st.caption("Guyana is a special case: its structural term is almost entirely dynamic and very sensitive to "
               "the price base, and oil dominates 2019–24 (compare the excluding-mining marker).")
footer()
