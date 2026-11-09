"""Loaders and chart helpers for the development-motors app (WP07).

The app only displays results computed by empirics/code/motors/ (run_all.py); it estimates
nothing itself.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from apps.common.theme import (AXIS, CATEGORICAL, C_CONTEXT, C_HIGHLIGHT, GRID, INK, INK2, MUTED,  # noqa: E402,F401
                               base_layout, credit, show)

OUT = ROOT / "empirics" / "output" / "motors"
PROC = ROOT / "empirics" / "data" / "processed" / "motors"

SECTOR_LABELS = {
    "MAN": "Manufacturing", "AGR": "Agriculture", "MIU": "Mining & utilities", "CON": "Construction",
    "TRH": "Trade, restaurants & hotels", "TSC": "Transport, storage & comms",
    "OTH": "Other services (finance, business, government, personal)", "SER": "All services",
}
SAMPLE_LABELS = {
    "main": "Main (pre-specified): countries over 1 million people",
    "excl_cpe": "Main, without former planned economies",
    "core": "Core: without former planned economies and commodity exporters",
    "developing": "Core, developing countries only",
}
VERDICT_COLORS = {
    "robustly positive": "#1baf7a", "leaning positive": "#8fd6b8", "fragile": "#c3c2b7",
    "leaning negative": "#f2a988", "robustly negative": "#eb6834",
}
SUBPERIODS = ["1950–70", "1970–90", "1990–2005", "2005–20"]


@st.cache_data
def load(rel):
    f = OUT / rel
    return pd.read_csv(f) if f.exists() else pd.DataFrame()


@st.cache_data
def load_proc(name):
    return pd.read_csv(PROC / name, low_memory=False)


def footer():
    credit("Sources: Penn World Table 11.0 (Feenstra, Inklaar & Timmer 2015); UN Statistics Division, National "
           "Accounts Main Aggregates (Jan 2026); GGDC 10-Sector Database (Timmer, de Vries & de Vries 2015); "
           "GGDC/UNU-WIDER Economic Transformation Database (de Vries et al. 2021); Barro & Lee (2013). "
           "Method: devtheory WP07, updating Szirmai & Verspagen (2015).")


def forest(df, label_col, est_col="coef", se_col="se", color=None, height=None, xtitle="", ref=0.0, order=None,
           group_col=None, legend=True):
    """Dot-and-interval chart: one row per label, 95% intervals, optional colour groups."""
    fig = go.Figure()
    groups = [(None, df)] if group_col is None else list(df.groupby(group_col, sort=False))
    sym = ["circle", "diamond", "square", "triangle-up"]
    for i, (g, x) in enumerate(groups):
        lo, hi = x[est_col] - 1.96 * x[se_col], x[est_col] + 1.96 * x[se_col]
        fig.add_trace(go.Scatter(
            x=x[est_col], y=x[label_col], mode="markers", name=str(g) if g is not None else "",
            marker=dict(size=9, symbol=sym[i % 4], color=(color or CATEGORICAL[i % len(CATEGORICAL)]),
                        line=dict(color="white", width=1.5)),
            error_x=dict(type="data", symmetric=False, array=hi - x[est_col], arrayminus=x[est_col] - lo,
                         color=(color or CATEGORICAL[i % len(CATEGORICAL)]), thickness=1.5, width=0),
            hovertemplate="%{y}<br>%{x:.3f}<extra>" + (str(g) if g is not None else "") + "</extra>"))
    fig.add_vline(x=ref, line=dict(color=MUTED, width=1))
    n = df[label_col].nunique()
    base_layout(fig, xtitle=xtitle, height=height or (120 + 34 * n), legend=legend and group_col is not None)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)", autorange="reversed",
                     categoryorder="array", categoryarray=order or list(dict.fromkeys(df[label_col])))
    return fig


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def verdict_chip(v):
    c = VERDICT_COLORS.get(v, "#c3c2b7")
    return f"<span style='background:{c};color:#0b0b0b;padding:1px 8px;border-radius:10px;font-size:0.85em'>{v}</span>"


def spec_summary():
    return load("speccurve/summary.csv")


def headline(estimand):
    s = spec_summary()
    r = s[s["estimand"] == estimand]
    return r.iloc[0] if len(r) else None


def unit_note():
    st.caption("Units: change in average annual growth of GDP per head (percentage points) for a "
               "1-point higher share of the sector in value added at the start of a five-year period, "
               "holding income relative to the US, schooling, population, openness and the period constant. "
               "A coefficient of 0.05 means a 10-point larger share goes with 0.5 points faster growth.")
