"""Reference analysis: country profile (ECLAC charts I.15–I.25, panels B–J)."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib import (COUNTRIES, C_HIGHLIGHT, C_STRUCT, C_WITHIN, INK2, SECTOR_COLORS, SHORT,
                 annual_decomp, base_layout, footer, load_labour, name, sector_long, sector_lp,
                 show, sidebar_common)

grid, series, _ = sidebar_common(key="cp")
st.title("Country profile")
st.caption("Reference format: ECLAC country panels B–J. Panel A (the productive development and employment "
           "index, IDPE) is not reproduced: its regression weights, estimated on Gallup life-satisfaction data, "
           "are not published in the reference.")

iso = st.selectbox("Country", list(COUNTRIES), format_func=name, index=list(COUNTRIES).index("DOM"))
lab = load_labour()
L = None
if lab is not None:
    L = lab[lab["iso3"] == iso].pivot_table(index="year", columns="indicator", values="value")

df = sector_long(grid, series)
d = sector_lp(df[df["iso3"] == iso])
dec, det = annual_decomp(grid, series, None)
det = det[det["iso3"] == iso]
yrs = sorted(det["year"].unique())
y2 = st.select_slider("Year for the sector panels (change from the previous year)", yrs, value=yrs[-1]) if yrs else None

# ---- headline metrics
if L is not None and len(L.dropna(subset=["lp_hour"])) > 1:
    last = int(L.dropna(subset=["lp_hour"]).index.max())
    m = st.columns(4)
    m[0].metric(f"Productivity per hour, {last}", f"{L.loc[last,'lp_hour']:.1f} PPP$",
                f"{100*(L.loc[last,'lp_hour']/L.loc[last-1,'lp_hour']-1):+.1f}% vs {last-1}")
    m[1].metric(f"Employment rate, {last}", f"{L.loc[last,'emp_rate']:.1f}%",
                f"{L.loc[last,'emp_rate']-L.loc[last-1,'emp_rate']:+.1f} pp")
    m[2].metric(f"Unemployment rate, {last}", f"{L.loc[last,'unemp_rate']:.1f}%",
                f"{L.loc[last,'unemp_rate']-L.loc[last-1,'unemp_rate']:+.1f} pp", delta_color="inverse")
    m[3].metric(f"Participation rate, {last}", f"{L.loc[last,'part_rate']:.1f}%",
                f"{L.loc[last,'part_rate']-L.loc[last-1,'part_rate']:+.1f} pp")

def panel_title(letter, text):
    st.markdown(f"**{letter}. {text}**")

# ---- B, C, D
if L is not None:
    LL = L.loc[L.index >= 2005]
    c1, c2, c3 = st.columns(3)
    with c1:
        panel_title("B", "Productivity per hour and employment rate (index, 2005 = 100)")
        fig = go.Figure()
        for col, lab_, color in [("lp_hour", "Productivity per hour", C_WITHIN), ("emp_rate", "Employment rate", C_STRUCT)]:
            s = LL[col].dropna()
            fig.add_trace(go.Scatter(x=s.index, y=100 * s / s.iloc[0], mode="lines", name=lab_,
                                     line=dict(color=color, width=2),
                                     hovertemplate=lab_ + " %{x}: %{y:.1f}<extra></extra>"))
        base_layout(fig, ytitle="2005 = 100", height=320)
        show(fig, caption="Shown on one indexed axis; the reference uses two axes.", key="B")
    with c2:
        panel_title("C", "Productivity per hour (constant 2021 PPP$)")
        fig = go.Figure(go.Scatter(x=LL.index, y=LL["lp_hour"], mode="lines", line=dict(color=C_WITHIN, width=2),
                                   hovertemplate="%{x}: %{y:.1f}<extra></extra>"))
        base_layout(fig, height=320, legend=False)
        show(fig, key="C")
    with c3:
        panel_title("D", "Employment rate (%)")
        fig = go.Figure(go.Scatter(x=LL.index, y=LL["emp_rate"], mode="lines", line=dict(color=C_STRUCT, width=2),
                                   hovertemplate="%{x}: %{y:.1f}%<extra></extra>"))
        base_layout(fig, height=320, legend=False)
        show(fig, key="D")
else:
    st.info("Panels B–D and I–J need the ILO labour-market series.")

# ---- E, F
if y2 is not None:
    c = det[det["year"] == y2].copy()
    c["label"] = c["sector"].map(SHORT)
    r = dec[(dec["iso3"] == iso) & (dec["year"] == y2)].iloc[0]
    c1, c2 = st.columns(2)
    with c1:
        panel_title("E", f"Structural change, {y2-1}–{y2} (thousand 2020 US$ and pp)")
        fig = go.Figure()
        for _, x in c.iterrows():
            fig.add_trace(go.Scatter(x=[100 * (x["s1"] - x["s0"])], y=[x["p1"] / 1000], mode="markers+text",
                                     text=[x["label"]], textposition="top center", textfont=dict(size=10, color=INK2),
                                     marker=dict(size=10 + 60 * np.sqrt(x["s1"]), color=SECTOR_COLORS[x["sector"]],
                                                 opacity=0.85, line=dict(color="white", width=2)), showlegend=False,
                                     hovertemplate=f"{x['label']}<br>Δshare {100*(x['s1']-x['s0']):.2f} pp<br>"
                                                   f"Productivity {x['p1']/1000:.1f}k<extra></extra>"))
        fig.add_vline(x=0, line=dict(color="#c3c2b7"))
        base_layout(fig, xtitle="Annual change in share of employment (pp)", ytitle="Final productivity level",
                    legend=False, height=380)
        show(fig, caption=f"Structural-change component: {r['struct']/1000:.2f}k of a total change of "
                          f"{(r['within']+r['struct'])/1000:.2f}k per worker. Bubble size = share of employment.", key="E")
    with c2:
        panel_title("F", f"Within-sector change, {y2-1}–{y2} (% of the within component)")
        wsum = c["within"].sum()
        c["pct"] = 100 * c["within"] / abs(wsum) if wsum else 0
        c = c.sort_values("pct")
        fig = go.Figure(go.Bar(x=c["pct"], y=c["label"], orientation="h",
                               marker=dict(color=[SECTOR_COLORS[s] for s in c["sector"]], cornerradius=4),
                               hovertemplate="%{y}: %{x:.0f}%<extra></extra>"))
        base_layout(fig, xtitle="% of the absolute within component", legend=False, height=380)
        fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
        show(fig, caption=f"Within component: {wsum/1000:.2f}k per worker.", key="F")

# ---- G, H
c1, c2 = st.columns(2)
with c1:
    b = 2005
    panel_title("G", f"Productivity trend by sector (index, {b} = 100)")
    t = d.pivot_table(index="year", columns="sector", values="lp")
    t = t.loc[t.index >= b]
    fig = go.Figure()
    for s in t.columns:
        fig.add_trace(go.Scatter(x=t.index, y=100 * t[s] / t[s].iloc[0], mode="lines", name=SHORT[s],
                                 line=dict(color=SECTOR_COLORS[s], width=2),
                                 hovertemplate=f"{SHORT[s]} %{{x}}: %{{y:.0f}}<extra></extra>"))
    base_layout(fig, height=400)
    show(fig, key="G")
with c2:
    hy = y2 if y2 else int(d["year"].max())
    panel_title("H", f"Productivity per worker and share of employment, by sector, {hy}")
    h = d[d["year"] == hy].sort_values("lp")
    fig = go.Figure(go.Bar(x=h["lp"] / 1000, y=h["sector"].map(SHORT), orientation="h",
                           marker=dict(color=[SECTOR_COLORS[s] for s in h["sector"]], cornerradius=4),
                           text=[f"{100*v:.0f}% of jobs" for v in h["share"]], textposition="outside",
                           hovertemplate="%{y}: %{x:.1f}k per worker<extra></extra>"))
    base_layout(fig, xtitle="thousand constant 2020 US$ per worker", legend=False, height=400)
    fig.update_xaxes(range=[0, h["lp"].max() / 1000 * 1.35])
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)")
    show(fig, key="H")

# ---- I, J
if L is not None:
    c1, c2 = st.columns(2)
    with c1:
        panel_title("I", "Change in the employment rate: Shapley contributions (pp)")
        ys = [y for y in L.index if y - 1 in L.index][-3:]
        rows = []
        for y in ys:
            p0, p1 = L.loc[y - 1, "part_rate"] / 100, L.loc[y, "part_rate"] / 100
            u0, u1 = L.loc[y - 1, "unemp_rate"] / 100, L.loc[y, "unemp_rate"] / 100
            rows.append({"year": str(y), "Contribution of participation": 100 * (p1 - p0) * (2 - u0 - u1) / 2,
                         "Contribution of unemployment": -100 * (u1 - u0) * (p0 + p1) / 2})
        s = pd.DataFrame(rows)
        fig = go.Figure()
        for col, color in [("Contribution of participation", C_WITHIN), ("Contribution of unemployment", C_STRUCT)]:
            fig.add_trace(go.Bar(x=s["year"], y=s[col], name=col, marker=dict(color=color)))
        fig.add_trace(go.Scatter(x=s["year"], y=s.iloc[:, 1:].sum(axis=1), mode="markers", name="Change in employment rate",
                                 marker=dict(color=INK2, size=9, symbol="diamond")))
        base_layout(fig, height=360)
        fig.update_layout(barmode="relative")
        fig.update_xaxes(type="category")
        show(fig, key="I")
    with c2:
        panel_title("J", "Labour-market rates (%)")
        LL = L.loc[L.index >= 2005]
        fig = go.Figure()
        for col, lab_, color in [("part_rate", "Participation rate", C_WITHIN), ("unemp_rate", "Unemployment rate", C_STRUCT)]:
            fig.add_trace(go.Scatter(x=LL.index, y=LL[col], mode="lines", name=lab_, line=dict(color=color, width=2)))
        base_layout(fig, ytitle="%", height=360)
        show(fig, key="J")
footer()
