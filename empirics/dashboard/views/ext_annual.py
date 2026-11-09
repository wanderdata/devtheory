"""Extended: annual decomposition at additive (previous-year) prices, with survey anchoring."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (CARIB, countries, C_DYNAMIC, C_STATIC, C_WITHIN, GRADE_COLORS, INK2,
                 annual_decomp, base_layout, footer, name, show, sidebar_common, survey_years)

grid, series, agg = sidebar_common(key="ea")
st.title("Annual decomposition, additive prices")
st.markdown("**Extension of the baseline.** This is the same year-to-year decomposition as the baseline, "
            "with three changes:\n"
            "1. Each year is valued at the **previous year's prices**, so sectors add up exactly. In "
            "constant-2020-price series, chain-linking means sectors do not sum to the total.\n"
            "2. Results are expressed as **contributions to growth (%)**, not dollar differences, so countries "
            "of different size can be compared.\n"
            "3. Years in which **both ends are actual survey years** are marked. Other years rely on ILO "
            "interpolation of employment shares, which smooths structural change.")

tuple_agg = tuple(agg) if agg else None
add, _ = annual_decomp(grid, series, tuple_agg, prices="previous")
ref, _ = annual_decomp(grid, series, tuple_agg, prices="constant2020")
who = st.selectbox("Economy", [CARIB] + list(countries()), format_func=name, index=1)
a = add[add["iso3"] == who].sort_values("year").copy()
for c in ["within", "static", "dynamic", "struct"]:
    a[c + "_pp"] = 100 * a[c] / a["P0"]
sy = set(survey_years(grid).get(who, [])) if who != CARIB else set()
a["anchored"] = [(y in sy) and (y - 1 in sy) for y in a["year"]]

fig = go.Figure()
for col, lab, color in [("within_pp", "Within-sector", C_WITHIN), ("static_pp", "Structural: static", C_STATIC),
                        ("dynamic_pp", "Structural: dynamic", C_DYNAMIC)]:
    fig.add_trace(go.Bar(x=a["year"], y=a[col], name=lab, marker=dict(color=color),
                         hovertemplate="%{x}: %{y:.2f} pp<extra>" + lab + "</extra>"))
fig.add_trace(go.Scatter(x=a["year"], y=a["growth_pct"], mode="markers", name="Productivity growth (%)",
                         marker=dict(color=INK2, size=8, symbol="diamond", line=dict(color="white", width=1))))
anch = a[a["anchored"]]
if len(anch):
    top = a[["within_pp", "static_pp", "dynamic_pp"]].clip(lower=0).sum(axis=1).max()
    fig.add_trace(go.Scatter(x=anch["year"], y=[top * 1.12] * len(anch), mode="markers",
                             name="Both years are survey years", marker=dict(symbol="triangle-down", size=9,
                                                                             color=GRADE_COLORS["A"]),
                             hovertemplate="%{x}: survey-based<extra></extra>"))
base_layout(fig, ytitle="contribution to growth, percentage points", height=460)
fig.update_layout(barmode="relative")
show(fig, a[["year", "growth_pct", "within_pp", "static_pp", "dynamic_pp", "anchored"]].round(2))

if len(a):
    s_all = a["struct_pp"].abs().mean()
    s_anch = a.loc[a["anchored"], "struct_pp"].abs().mean() if a["anchored"].any() else float("nan")
    s_int = a.loc[~a["anchored"], "struct_pp"].abs().mean()
    c = st.columns(3)
    c[0].metric("Average |structural term|, all years", f"{s_all:.2f} pp")
    c[1].metric("…survey-to-survey years", "—" if pd.isna(s_anch) else f"{s_anch:.2f} pp")
    c[2].metric("…interpolated years", f"{s_int:.2f} pp")
    st.caption("If the structural term is much smaller in interpolated years than in survey-to-survey years, ILO "
               "smoothing is suppressing reallocation in those years. Read them with care.")

st.subheader("How much the price base matters")
r = ref[ref["iso3"] == who][["year", "growth_pct"]].rename(columns={"growth_pct": "ref"})
cmp_ = a[["year", "growth_pct"]].merge(r, on="year")
fig = go.Figure()
fig.add_trace(go.Scatter(x=cmp_["year"], y=cmp_["ref"], mode="lines", name="Constant 2020 prices (baseline)",
                         line=dict(color="#c3c2b7", width=2)))
fig.add_trace(go.Scatter(x=cmp_["year"], y=cmp_["growth_pct"], mode="lines", name="Previous-year prices (additive)",
                         line=dict(color=C_WITHIN, width=2)))
base_layout(fig, ytitle="productivity growth, %", height=360)
show(fig, cmp_.round(2), caption="The two lines diverge most where relative prices moved a lot (oil, gold, bauxite).")
footer()
