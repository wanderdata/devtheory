"""Study 9.1: which jobs are rungs? Flows by sector, firm size and formality (ENOE rotating panel)."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from jobs_lib import C_CONTEXT, C_HIGHLIGHT, INK2, MUTED, SECTORS as ENOE_SECTORS, base_layout, footer, load, show

st.title("9.1 Which jobs are rungs?")
st.markdown(
    "This page uses Mexico's quarterly labour-force survey (ENOE), which interviews the same dwellings in five "
    "consecutive quarters, to follow workers for a year. It asks which characteristics of a job predict whether "
    "the person holding it stays employed and moves to better-paid work: the job's **sector**, or its **firm size "
    "and formality**. Two windows are compared: 2018 Q4–2019 Q4 and 2023 Q1–2024 Q1. Ages 16–65. The design was "
    "written down before the data were opened (pre-analysis plan of study 9.1); results are descriptive, not causal.")

dec = load("ladders", "decomposition")
if dec.empty:
    st.warning("No results: run `empirics/code/enoe/run_all.py` (needs the ENOE microdata).")
    st.stop()

WIN = {"pre": "2018 Q4–2019 Q4", "post": "2023 Q1–2024 Q1"}
OUT = {"exit_y": "Not employed one year later", "up_y": "In a better-paid job cell one year later",
       "up_emp_y": "In a better-paid job cell one year later, with a new employer",
       "persist_y": "In the same job cell one year later", "exit_q": "Not employed one quarter later"}

st.info(
    "**Verdict under the pre-analysis plan: inconclusive.** Firm size × formality accounts for more of the variation "
    "in upward moves than sector does, in every variant. For exits to non-employment it accounts for more in the main "
    "sample, but not when a transition must be confirmed at the following visit, which the plan makes decisive. "
    "With formality alone in place of size × formality, sector explains upward moves as well or better, so the case "
    "for size × formality rests on firm size, which workers report inconsistently (see the last section). "
    "Reweighting for attrition changes nothing of substance. Both dimensions together explain 1–7% of what "
    "happens to individual workers within a year.")

# ---- 1. rates by cell
st.subheader("Rates by type of job")
c1, c2, c3 = st.columns([2, 2, 1])
dim = c1.radio("Group jobs by", ["Firm size × formality", "Sector"], horizontal=True)
out = c2.selectbox("Outcome", ["exit_y", "up_emp_y", "up_y", "persist_y", "exit_q"], format_func=OUT.get)
wts = c3.radio("Weights", ["origin weights", "reweighted for attrition"], key="jw",
               help="Reweighting adjusts the people still in the panel a year later to the age, sex and "
                    "labour-force-status mix of everyone who could have been followed.")
if dim == "Sector":
    r = load("ladders", "rates_sector").assign(cell=lambda d: d["sector"].astype(str).map(ENOE_SECTORS))
    if wts != "origin weights":
        st.caption("Sector rates are shown with origin weights only.")
else:
    r = load("ladders", "rates_sizeform").rename(columns={"sizeform": "cell"})
    r = r[r["weights"] == wts] if "weights" in r.columns else r
    r["cell"] = r["cell"].str.replace("|", " · ", regex=False)
r = r.dropna(subset=[out])
r = r[r["n"] >= 200]
order = r[r["window"] == "post"].sort_values(out)["cell"].tolist()
order += [c for c in r["cell"].unique() if c not in order]
fig = go.Figure()
for win, col, sym in [("pre", C_CONTEXT, "circle"), ("post", C_HIGHLIGHT, "diamond")]:
    g = r[r["window"] == win].set_index("cell").reindex(order).dropna(subset=[out])
    if len(g):
        fig.add_trace(go.Scatter(x=g[out], y=g.index, mode="markers", name=WIN[win],
                                 marker=dict(color=col, size=10, symbol=sym),
                                 customdata=g[["n"]], hovertemplate="%{y}<br>%{x:.3f} (n = %{customdata[0]:,})<extra>" + WIN[win] + "</extra>"))
base_layout(fig, xtitle="share of workers employed in that type of job at the first visit", height=140 + 26 * len(order))
fig.update_yaxes(type="category", categoryorder="array", categoryarray=order, gridcolor="rgba(0,0,0,0)")
show(fig, r[["window", "cell", "n", out]].round(3),
     caption="Weighted shares among people employed in each type of job at the first visit and observed again one "
             "year later (one quarter later for the quarterly exit rate). The new-employer outcome can be measured only "
             "in 2023–24, because the start date with the employer is asked only in first quarters. Cells with fewer "
             "than 200 observations are not shown; 'other sizes' groups small cells of a sector.")

# ---- 2. which dimension explains more
st.subheader("Which dimension explains more: sector or firm size × formality?")
st.markdown(
    "For each outcome, the share of the variance across workers explained by sector and by firm size × formality is "
    "split with a Shapley decomposition. The chart shows the difference (size × formality minus sector) with a 90% "
    "interval from a bootstrap over primary sampling units. Positive values favour size × formality.")
variants = list(dict.fromkeys(dec["variant"]))
default = [v for v in variants if v in ("main", "confirmed transitions", "reweighted for attrition",
                                       "formality alone vs sector")]
pick = st.multiselect("Variants", variants, default=default)
d = dec[dec["variant"].isin(pick)].copy()
d["label"] = d["outcome"].map(OUT) + " · " + d["window"].map(WIN)
labels = list(dict.fromkeys(d.sort_values(["outcome", "window"])["label"]))
fig = go.Figure()
palette = [C_HIGHLIGHT, "#eb6834", "#1baf7a", INK2, "#eda100", "#8a63d2", MUTED]
for k, v in enumerate(pick):
    g = d[d["variant"] == v]
    fig.add_trace(go.Scatter(
        x=g["diff"], y=g["label"], mode="markers", name=v, marker=dict(color=palette[k % len(palette)], size=9),
        error_x=dict(type="data", symmetric=False, array=g["diff_hi90"] - g["diff"], arrayminus=g["diff"] - g["diff_lo90"],
                     thickness=1.2, width=0),
        customdata=g[["shapley_sector", "shapley_sizeform", "n"]],
        hovertemplate="%{y}<br>difference %{x:+.4f}<br>sector %{customdata[0]:.4f}, size × formality "
                      "%{customdata[1]:.4f}<br>n = %{customdata[2]:,}<extra>" + v + "</extra>"))
fig.add_vline(x=0, line=dict(color=MUTED, width=1))
base_layout(fig, xtitle="difference in variance explained (positive: size × formality)",
            height=200 + 34 * len(labels))
fig.update_yaxes(type="category", categoryorder="array", categoryarray=labels, gridcolor="rgba(0,0,0,0)")
show(fig, d[["window", "outcome", "variant", "n", "shapley_sector", "shapley_sizeform", "diff", "diff_lo90", "diff_hi90"]].round(4),
     caption="Where the main and reweighted estimates coincide, the reweighted marker covers the main one. "
             "Variants: confirmed transitions keep only people whose state at the first and last visits is repeated "
             "at the adjacent visit (removes many spurious transitions); self-reported only drops answers given by "
             "another household member; reweighted for attrition adjusts for people lost between visits; "
             "'formality alone' replaces size × formality by formality only, because firm size is reported "
             "inconsistently; the rank-decile variant (exploratory, not in the plan) allows for the ceiling on upward "
             "moves from cells already near the top.")

# ---- 3. manufacturing vs services
st.subheader("Manufacturing versus services in the same type of firm")
stt = load("ladders", "sector_test")
if not stt.empty:
    if "weights" not in stt.columns:
        stt["weights"] = "origin weights"
    stt["label"] = stt["outcome"].map(OUT) + " · " + stt["window"].map(WIN)
    labels = list(dict.fromkeys(stt.sort_values(["outcome", "window"])["label"]))
    fig = go.Figure()
    for k, (wl, g) in enumerate(stt.groupby("weights", sort=False)):
        fig.add_trace(go.Scatter(x=g["manufacturing_minus_services"], y=g["label"], mode="markers", name=wl,
                                 marker=dict(color=[C_HIGHLIGHT, "#eb6834"][k % 2], size=9),
                                 error_x=dict(type="data", symmetric=False, array=g["hi90"] - g["manufacturing_minus_services"],
                                              arrayminus=g["manufacturing_minus_services"] - g["lo90"], thickness=1.2, width=0),
                                 hovertemplate="%{y}<br>%{x:+.3f}<extra>" + wl + "</extra>"))
    fig.add_vline(x=0, line=dict(color=MUTED, width=1))
    base_layout(fig, xtitle="manufacturing minus services (share of workers)", height=160 + 34 * len(labels))
    fig.update_yaxes(type="category", categoryorder="array", categoryarray=labels, gridcolor="rgba(0,0,0,0)")
    show(fig, stt.drop(columns="label").round(4),
         caption="Weighted regression on a manufacturing indicator (services: commerce, restaurants and accommodation, "
                 "transport and communications, professional, social and other services), with firm size × "
                 "formality, age group, sex and schooling level as controls. Manufacturing jobs lead more often to "
                 "better-paid cells but are not less likely to end in non-employment.")

# ---- 4. transitions between segments
st.subheader("Moving between not employed, informal and formal work")
tr = load("ladders", "transitions")
if not tr.empty:
    c1, c2, c3 = st.columns(3)
    hz = c1.radio("Horizon", ["year", "quarter"], horizontal=True, format_func=lambda h: f"One {h}")
    wn = c2.radio("Window", ["pre", "post"], horizontal=True, format_func=WIN.get, key="trw")
    tw = c3.radio("Weights", ["origin weights", "reweighted for attrition"], key="trwt")
    t = tr[(tr["horizon"] == hz) & (tr["window"] == wn) & (tr["weights"] == tw)]
    seg = [s for s in ["not employed", "informal", "formal"] if s in set(t["origin"])]
    colors = {"not employed": "#c3c2b7", "informal": "#eb6834", "formal": C_HIGHLIGHT,
              "employed, formality not specified": MUTED}
    fig = go.Figure()
    for dst in [s for s in ["not employed", "informal", "formal", "employed, formality not specified"] if s in set(t["destination"])]:
        g = t[t["destination"] == dst].set_index("origin").reindex(seg)
        fig.add_trace(go.Bar(y=seg, x=g["share"], name=dst, orientation="h", marker=dict(color=colors[dst]),
                             hovertemplate="from %{y}: %{x:.1%} " + dst + "<extra></extra>"))
    base_layout(fig, xtitle="share of each starting group", height=300)
    fig.update_layout(barmode="stack")
    fig.update_xaxes(tickformat=".0%", range=[0, 1])
    fig.update_yaxes(categoryorder="array", categoryarray=seg[::-1], gridcolor="rgba(0,0,0,0)")
    show(fig, t.pivot_table(index="origin", columns="destination", values="share").round(3).reset_index(),
         caption="Ages 16–65 at the first visit. Formality follows INEGI's labour-informality definition (no access to "
                 "social security through the job, or work in an informal unit). Quarterly matrices are averages of "
                 "the window's four consecutive pairs.")

# ---- 5. earnings growth
st.subheader("Earnings growth over a year")
eg = load("ladders", "earnings_growth")
if not eg.empty:
    wn = st.radio("Window", ["pre", "post"], horizontal=True, format_func=WIN.get, key="egw")
    e = eg[(eg["dimension"] == "sizeform") & (eg["window"] == wn) & (eg["n"] >= 200)].copy()
    e["cell"] = e["cell"].str.replace("|", " · ", regex=False)
    order = e[e["group"] == "same cell"].sort_values("median_dlog")["cell"].tolist()
    order += [c for c in e["cell"].unique() if c not in order]
    fig = go.Figure()
    for grp, col in [("same cell", C_CONTEXT), ("moved", C_HIGHLIGHT)]:
        g = e[e["group"] == grp].set_index("cell").reindex(order).dropna(subset=["median_dlog"])
        fig.add_trace(go.Scatter(x=g["median_dlog"], y=g.index, mode="markers", name=f"stayed in {grp}" if grp == "same cell" else "moved to another job cell",
                                 marker=dict(color=col, size=9), customdata=g[["n", "share_valid"]],
                                 hovertemplate="%{y}<br>median change %{x:+.3f}<br>n = %{customdata[0]:,}, "
                                               "valid earnings %{customdata[1]:.0%}<extra></extra>"))
    fig.add_vline(x=0, line=dict(color=MUTED, width=1))
    base_layout(fig, xtitle="median change in log hourly earnings (nominal)", height=140 + 26 * len(order))
    fig.update_yaxes(type="category", categoryorder="array", categoryarray=order, gridcolor="rgba(0,0,0,0)")
    show(fig, e.drop(columns="dimension").round(3),
         caption="People employed at both visits with positive hourly earnings at both, by job cell at the first visit. "
                 "Earnings are nominal: annual inflation (about 3–5% in both windows) is not removed, so zero growth "
                 "is a real fall. A large share of workers do not report earnings, especially in informal and "
                 "own-account work; see the valid-earnings column.")

# ---- 6. data quality
st.subheader("How reliable are the job characteristics?")
mis = load("ladders", "misreport")
if not mis.empty:
    m = mis.iloc[0]
    st.markdown(
        f"Among {int(m['n']):,} employees who reported the same start date with their employer at two first-quarter "
        f"visits a year apart (2023 and 2024), **{m['size_changes']:.0%} reported a different firm-size class** and "
        f"**{m['formality_changes']:.0%} a different formality status**. Some genuine growth across a size boundary is "
        "possible in a year, but most of the size changes are reporting error. Results that rely on firm size are "
        "therefore weaker than their intervals suggest; formality is reported far more consistently.")
footer("2018 Q4–2019 Q4 and 2023 Q1–2024 Q1. Method: devtheory WP09, study 9.1, after Donovan, Lu and Schoellman (2023).")
