import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from motors_lib import CATEGORICAL, MUTED, VERDICT_COLORS, base_layout, footer, load, show

st.title("Robustness: every specification")
st.markdown(
    "Each headline estimate is re-run under every combination of six choices: **estimator** (Hausman–Taylor, fixed "
    "effects, random effects), **sample** (main, without former planned economies, core, developing only), **period "
    "length** (5 or 10 years), **manufacturing share** at current or constant prices, **growth** from PWT's "
    "national-accounts or output-side GDP, and **schooling** from Barro–Lee or PWT's human-capital index — 192 "
    "specifications (96 for the sector comparisons, which use current-price shares only).")

s = load("speccurve/summary.csv")
st.subheader("Summary")
show_cols = ["estimand", "n_specs", "median", "q10", "q90", "share_positive", "share_pos_sig", "share_neg_sig", "verdict"]
st.dataframe(s[show_cols].round(3), hide_index=True, width="stretch")
st.caption("Verdicts: robustly positive (negative) = at least 90% of estimates of one sign and at least half "
           "significant at 10%; leaning = at least 75% of one sign; fragile = otherwise.")

st.subheader("Specification curve")
est = load("speccurve/estimates.csv")
choice = st.selectbox("Estimate", s["estimand"].tolist(), index=s["estimand"].tolist().index("Manufacturing, 1990–2005"))
g = est[est["estimand"] == choice].dropna(subset=["coef"]).sort_values("coef").reset_index(drop=True)
g["rank"] = range(1, len(g) + 1)
g["sig"] = g["p"] < 0.10
dims = [("estimator", ["HT", "FE", "RE"]), ("sample", ["main", "excl_cpe", "core", "developing"]),
        ("length", [5, 10]), ("share", ["MAN", "MAN_K"]), ("growth", ["GR", "GR_O"]), ("edu", ["EDU_HC", "EDU"])]
rows = sum(len(v) for _, v in dims)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.45, 0.55], vertical_spacing=0.03)
fig.add_trace(go.Scatter(x=g["rank"], y=g["coef"], mode="markers",
                         marker=dict(size=6, color=[CATEGORICAL[0] if s_ else "#c3c2b7" for s_ in g["sig"]]),
                         error_y=dict(type="data", array=1.96 * g["se"], color="#e1e0d9", thickness=1, width=0),
                         hovertemplate="%{y:.3f}<extra></extra>", showlegend=False), row=1, col=1)
fig.add_hline(y=0, line=dict(color=MUTED, width=1), row=1, col=1)
labels, k = [], 0
for dim, vals in dims:
    for v in vals:
        m = g[g[dim].astype(str) == str(v)]
        fig.add_trace(go.Scatter(x=m["rank"], y=[f"{dim}: {v}"] * len(m), mode="markers",
                                 marker=dict(symbol="line-ns-open", size=8, color=INK if False else "#52514e"),
                                 hoverinfo="skip", showlegend=False), row=2, col=1)
        labels.append(f"{dim}: {v}")
base_layout(fig, height=720, legend=False)
fig.update_yaxes(title="estimate", row=1, col=1)
fig.update_yaxes(categoryorder="array", categoryarray=labels[::-1], gridcolor="rgba(0,0,0,0)", row=2, col=1)
fig.update_xaxes(title="specifications, sorted by estimate", row=2, col=1)
show(fig, g[["coef", "se", "p", "estimator", "sample", "length", "share", "growth", "edu"]].round(4),
     caption="Top: estimates sorted from lowest to highest, with 95% intervals; blue = significant at 10%. Bottom: "
             "which choices each specification made. System GMM, listed in the pre-analysis plan, is not included "
             "(no validated implementation available here; D-040).")
footer()
