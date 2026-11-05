"""Extended: McMillan–Rodrik scatter with fitted slope, productivity dispersion, hours."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (CARIB, COUNTRIES, C_CONTEXT, C_HIGHLIGHT, C_STRUCT, C_WITHIN, INK2, SECTOR_COLORS,
                 SHORT, base_layout, dispersion, footer, load_labour, mr_step, name, sector_long, show,
                 sidebar_common)

grid, series, agg = sidebar_common(key="es")
st.title("Reallocation and productivity gaps")
st.markdown("**Extension of the baseline.** Three additions:\n"
            "1. The original **McMillan–Rodrik scatter**, with an employment-weighted regression line. A "
            "positive slope means jobs moved toward higher-productivity sectors.\n"
            "2. A **measure of productivity dispersion across sectors** over time, to show whether gaps between "
            "sectors are narrowing.\n"
            "3. A **per-worker vs per-hour** comparison that isolates the effect of working hours.")

df = sector_long(grid, series, tuple(agg) if agg else None)

# ---- 1. MR scatter
st.subheader("Did jobs move toward more productive sectors?")
c1, c2, c3 = st.columns(3)
who = c1.selectbox("Economy", [CARIB] + list(COUNTRIES), format_func=name, index=1)
g = df[df["iso3"] == who].set_index(["year", "sector"]).sort_index()
yrs = sorted(g.index.get_level_values(0).unique())
t0 = c2.selectbox("From", yrs, index=yrs.index(2000) if 2000 in yrs else 0)
t1 = c3.selectbox("To", [y for y in yrs if y > t0], index=len([y for y in yrs if y > t0]) - 1)
out, P0, P1 = mr_step(g.loc[t0], g.loc[t1], prices="previous")
out["x"] = 100 * (out["s1"] - out["s0"])
out["y"] = np.log(out["rel0"])
wts = out["s0"]
X = np.c_[np.ones(len(out)), out["y"]]
W = np.diag(wts)
beta = np.linalg.lstsq(np.sqrt(W) @ X, np.sqrt(W) @ out["x"].values, rcond=None)[0]
fig = go.Figure()
for s, r in out.iterrows():
    fig.add_trace(go.Scatter(x=[r["y"]], y=[r["x"]], mode="markers+text", text=[SHORT[s]], textposition="top center",
                             textfont=dict(size=11, color=INK2), showlegend=False,
                             marker=dict(size=10 + 60 * np.sqrt(r["s0"]), color=SECTOR_COLORS[s], opacity=0.85,
                                         line=dict(color="white", width=2)),
                             hovertemplate=f"{SHORT[s]}<br>ln(relative productivity, {t0}) {r['y']:.2f}<br>"
                                           f"Δ share {r['x']:.2f} pp<extra></extra>"))
xs = np.linspace(out["y"].min(), out["y"].max(), 20)
fig.add_trace(go.Scatter(x=xs, y=beta[0] + beta[1] * xs, mode="lines", line=dict(color=INK2, dash="dot", width=1.5),
                         name="Employment-weighted fit", showlegend=False, hoverinfo="skip"))
fig.add_hline(y=0, line=dict(color="#c3c2b7")); fig.add_vline(x=0, line=dict(color="#c3c2b7"))
base_layout(fig, xtitle=f"ln(sector productivity / economy average), {t0}",
            ytitle=f"change in share of employment, {t0}–{t1} (pp)", legend=False, height=480)
show(fig, out[["x", "y", "s0", "s1"]].round(3).reset_index(),
     caption=f"Slope = {beta[1]:.2f} pp per log point ({'growth-enhancing' if beta[1] > 0 else 'growth-reducing'} "
             f"reallocation). Bubble size = initial share of employment. Productivity at {t0} prices.")

# ---- 2. dispersion
st.subheader("Productivity gaps between sectors over time")
dp = dispersion(df)
focus = st.selectbox("Highlight", [CARIB] + list(COUNTRIES), format_func=name, index=1, key="dfoc")
fig = go.Figure()
for iso, g2 in dp.groupby("iso3"):
    if iso == focus:
        continue
    fig.add_trace(go.Scatter(x=g2["year"], y=g2["disp"], mode="lines", line=dict(color=C_CONTEXT, width=1),
                             showlegend=False, hovertemplate=f"{name(iso)} %{{x}}: %{{y:.2f}}<extra></extra>"))
g2 = dp[dp["iso3"] == focus]
fig.add_trace(go.Scatter(x=g2["year"], y=g2["disp"], mode="lines", line=dict(color=C_HIGHLIGHT, width=2.5),
                         name=name(focus), hovertemplate=f"{name(focus)} %{{x}}: %{{y:.2f}}<extra></extra>"))
base_layout(fig, ytitle="employment-weighted SD of ln(relative productivity)", legend=False, height=400)
show(fig, dp.pivot_table(index="year", columns="iso3", values="disp").round(3).reset_index(),
     caption="Higher = larger productivity gaps between sectors. Falling dispersion means sectors are converging. "
             "That can come from low-productivity sectors catching up or from high-productivity ones slipping. "
             "Mining-heavy economies sit high because of enclave sectors.")

# ---- 3. hours
st.subheader("Per worker vs per hour")
lab = load_labour()
if lab is None or not {"lp_hour", "hours"} <= set(lab["indicator"]):
    st.info("Needs ILO output per hour and hours worked.")
else:
    w = lab.pivot_table(index=["iso3", "year"], columns="indicator", values="value").reset_index()
    y0, y1 = st.select_slider("Period", sorted(w.dropna(subset=["lp_hour"])["year"].unique()), value=(2005, 2025))
    a = w[w["year"] == y0].set_index("iso3"); b = w[w["year"] == y1].set_index("iso3")
    n = y1 - y0
    r = pd.DataFrame({"per_hour": 100 * ((b["lp_hour"] / a["lp_hour"]) ** (1 / n) - 1),
                      "hours": 100 * ((b["hours"] / a["hours"]) ** (1 / n) - 1)}).dropna()
    r["per_worker"] = 100 * ((1 + r["per_hour"] / 100) * (1 + r["hours"] / 100) - 1)
    r = r.sort_values("per_worker")
    fig = go.Figure()
    for col, lab_, color in [("per_hour", "Output per hour", C_WITHIN), ("hours", "Hours per worker", C_STRUCT)]:
        fig.add_trace(go.Bar(y=[name(i) for i in r.index], x=r[col], name=lab_, orientation="h", marker=dict(color=color)))
    fig.add_trace(go.Scatter(y=[name(i) for i in r.index], x=r["per_worker"], mode="markers", name="Output per worker",
                             marker=dict(color=INK2, size=9, symbol="diamond")))
    base_layout(fig, xtitle="average annual change, %", height=460)
    fig.update_layout(barmode="relative")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    show(fig, r.round(2).reset_index().assign(iso3=lambda d: d["iso3"].map(name)).rename(columns={"iso3": "country"}),
         caption="ILO modelled estimates (2021 PPP$). Growth in output per worker ≈ growth per hour + growth in hours. "
                 "Where hours fall, per-worker figures understate productivity gains per hour.")
footer()
