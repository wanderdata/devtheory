"""Shared data loading, computations and chart helpers for the Caribbean
labour-productivity dashboard. Everything is computed from files committed in
the repository (empirics/data/... and empirics/output/...), so the app runs on
Streamlit Community Cloud with no downloads.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "empirics" / "data" / "processed" / "carib_lp"
INTERIM = ROOT / "empirics" / "data" / "interim" / "carib_lp"
OUT = ROOT / "empirics" / "output" / "carib_lp"

COUNTRIES = {
    "BHS": "Bahamas", "BRB": "Barbados", "BLZ": "Belize", "CUB": "Cuba",
    "DOM": "Dominican Republic", "GUY": "Guyana", "HTI": "Haiti", "JAM": "Jamaica",
    "LCA": "Saint Lucia", "VCT": "Saint Vincent and the Grenadines", "SUR": "Suriname",
    "TTO": "Trinidad and Tobago",
}
NOT_COVERED = ["Antigua and Barbuda", "Dominica", "Grenada", "Saint Kitts and Nevis"]
CARIB = "CAR"  # code for the pooled Caribbean aggregate
CARIB_NAME = "Caribbean (selected countries, pooled)"

SECTORS_A = ["AGR", "MIU", "MAN", "CON", "TRH", "TSC", "OTH"]
SECTORS_B = ["AGR", "MIU", "MAN", "CON", "SER"]
SECTOR_NAMES = {
    "AGR": "Agriculture, forestry, fishing", "MIU": "Mining and utilities",
    "MAN": "Manufacturing", "CON": "Construction", "TRH": "Trade, restaurants, hotels",
    "TSC": "Transport, storage, communication", "OTH": "Other services",
    "SER": "Services (all)",
}
SHORT = {"AGR": "Agriculture", "MIU": "Mining & utilities", "MAN": "Manufacturing",
         "CON": "Construction", "TRH": "Trade & hotels", "TSC": "Transport & comms",
         "OTH": "Other services", "SER": "Services"}
GRID_MAP = {"A": {s: s for s in SECTORS_A},
            "B": {"AGR": "AGR", "MIU": "MIU", "MAN": "MAN", "CON": "CON",
                  "TRH": "SER", "TSC": "SER", "OTH": "SER"}}

# Validated categorical palette (dataviz reference instance), fixed per sector.
SECTOR_COLORS = {"AGR": "#2a78d6", "MIU": "#eb6834", "MAN": "#1baf7a", "CON": "#eda100",
                 "TRH": "#e87ba4", "TSC": "#008300", "OTH": "#6250d6", "SER": "#6250d6"}
C_WITHIN, C_STRUCT = "#2a78d6", "#eb6834"          # component colours (slots 1, 2)
C_STATIC, C_DYNAMIC = "#eb6834", "#1baf7a"
C_HIGHLIGHT, C_CONTEXT = "#2a78d6", "#c3c2b7"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
GRADE_COLORS = {"A": "#0ca30c", "B": "#fab219", "C": "#d03b3b"}
GRADE_TEXT = {"A": "A · both endpoints near survey years",
              "B": "B · one endpoint near a survey year",
              "C": "C · no survey anchor (ILO model only)"}


# ------------------------------------------------------------------ loading --

@st.cache_data
def load_panel():
    p = pd.read_csv(PROC / "panel_7sector.csv")
    p = p[p["iso3"].isin(COUNTRIES)]
    return p


@st.cache_data
def load_emp5():
    return pd.read_csv(PROC / "emp_5sector.csv")


@st.cache_data
def load_output(grid, name):
    f = OUT / f"grid_{grid}" / f"{name}.csv"
    return pd.read_csv(f) if f.exists() else pd.DataFrame()


@st.cache_data
def load_labour():
    """ILO modelled labour-market indicators (optional; from 06_extract_labour.py)."""
    f = INTERIM / "ilo_labour.csv"
    if not f.exists():
        return None
    return pd.read_csv(f)


def labour_or_note(indicators):
    lab = load_labour()
    if lab is None or not set(indicators) <= set(lab["indicator"].unique()):
        st.info("**Data pending.** This chart needs ILO modelled labour-market series "
                f"({', '.join(indicators)}). Add the files and run "
                "`empirics/code/carib_lp/06_extract_labour.py`.")
        return None
    return lab


@st.cache_data
def sector_long(grid, emp_series="model", countries=None):
    """Long table iso3, year, sector, va_k (constant 2020 US$), va_cur, emp (thousands)
    on the chosen grid, plus a pooled Caribbean aggregate over `countries`."""
    p = load_panel()
    va = p[["iso3", "year", "sector", "va_k2020usd", "va_cur_usd"]].dropna()
    va = va.assign(sector=va["sector"].map(GRID_MAP[grid]))
    va = va.groupby(["iso3", "year", "sector"], as_index=False)[["va_k2020usd", "va_cur_usd"]].sum()
    if grid == "A":
        col = f"emp_{emp_series}"
        e = p[["iso3", "year", "sector", col]].dropna().rename(columns={col: "emp"})
    else:
        e5 = load_emp5()
        e = e5[e5["series"] == emp_series][["iso3", "year", "sector", "emp"]]
    df = va.merge(e, on=["iso3", "year", "sector"], how="inner")
    df = df[df["iso3"].isin(COUNTRIES)]
    # keep only country-years with every sector of the grid
    n = len(SECTORS_A if grid == "A" else SECTORS_B)
    df = df.groupby(["iso3", "year"]).filter(lambda g: len(g) == n)
    if countries:
        sub = df[df["iso3"].isin(countries)]
        full = sub.groupby("year")["iso3"].nunique()
        yrs = full[full == len(countries)].index
        agg = (sub[sub["year"].isin(yrs)].groupby(["year", "sector"], as_index=False)
               [["va_k2020usd", "va_cur_usd", "emp"]].sum())
        agg["iso3"] = CARIB
        df = pd.concat([df, agg], ignore_index=True)
    return df


def name(iso):
    return CARIB_NAME if iso == CARIB else COUNTRIES.get(iso, iso)


# ------------------------------------------------------------ computations --

def aggregate_lp(df):
    """Aggregate LP per worker (constant 2020 US$) by iso3-year."""
    g = df.groupby(["iso3", "year"]).agg(va=("va_k2020usd", "sum"), emp=("emp", "sum"))
    g["lp"] = g["va"] / (g["emp"] * 1000)
    return g.reset_index()


def sector_lp(df):
    d = df.copy()
    d["lp"] = d["va_k2020usd"] / (d["emp"] * 1000)
    tot = aggregate_lp(df)[["iso3", "year", "lp"]].rename(columns={"lp": "lp_total"})
    d = d.merge(tot, on=["iso3", "year"])
    d["rel"] = 100 * d["lp"] / d["lp_total"]
    d["share"] = d["emp"] / d.groupby(["iso3", "year"])["emp"].transform("sum")
    return d


def mr_step(d0, d1, prices="constant2020"):
    """McMillan–Rodrik decomposition between two years for one economy.
    d0, d1: sector-indexed frames with va_k2020usd, va_cur_usd, emp.
    prices='constant2020' : reference style (fixed 2020 prices, as in ECLAC's
                            constant-2018-dollar series); levels in US$ per worker.
    prices='previous'     : sectors valued at year-0 prices (additive; WP05 method).
    Returns per-sector contributions (US$ per worker) and totals."""
    if prices == "constant2020":
        y0, y1 = d0["va_k2020usd"], d1["va_k2020usd"]
    else:
        vol = d1["va_k2020usd"] / d0["va_k2020usd"]
        y0, y1 = d0["va_cur_usd"], d0["va_cur_usd"] * vol
    l0, l1 = d0["emp"] * 1000, d1["emp"] * 1000
    p0, p1 = y0 / l0, y1 / l1
    s0, s1 = l0 / l0.sum(), l1 / l1.sum()
    P0, P1 = y0.sum() / l0.sum(), y1.sum() / l1.sum()
    out = pd.DataFrame({
        "within": s0 * (p1 - p0), "struct": p1 * (s1 - s0),
        "static": p0 * (s1 - s0), "dynamic": (p1 - p0) * (s1 - s0),
        "p0": p0, "p1": p1, "s0": s0, "s1": s1, "rel0": p0 / P0, "rel1": p1 / P1,
    })
    return out, P0, P1


@st.cache_data
def annual_decomp(grid, emp_series, countries, prices="constant2020"):
    df = sector_long(grid, emp_series, tuple(countries) if countries else None)
    rows, det = [], []
    for iso, g in df.groupby("iso3"):
        g = g.set_index(["year", "sector"]).sort_index()
        yrs = sorted(g.index.get_level_values(0).unique())
        for a, b in zip(yrs, yrs[1:]):
            if b != a + 1:
                continue
            out, P0, P1 = mr_step(g.loc[a], g.loc[b], prices)
            rows.append({"iso3": iso, "year": b, "P0": P0, "P1": P1,
                         "within": out["within"].sum(), "struct": out["struct"].sum(),
                         "static": out["static"].sum(), "dynamic": out["dynamic"].sum()})
            o = out.reset_index().assign(iso3=iso, year=b)
            det.append(o)
    r = pd.DataFrame(rows)
    r["growth_pct"] = 100 * (r["P1"] / r["P0"] - 1)
    return r, pd.concat(det, ignore_index=True)


@st.cache_data
def survey_years(grid):
    """Usable survey years per country for the grid (for anchoring markers)."""
    if grid == "A":
        p = load_panel()
        s = p.dropna(subset=["emp_survey"])
    else:
        e5 = load_emp5()
        s = e5[e5["series"] == "survey"]
    return {iso: sorted(set(g["year"])) for iso, g in s.groupby("iso3")}


def dispersion(df):
    """Employment-weighted standard deviation of log relative sector productivity."""
    d = sector_lp(df)
    d["lr"] = np.log(d["lp"] / d["lp_total"])
    def wsd(g):
        m = (g["share"] * g["lr"]).sum()
        return np.sqrt((g["share"] * (g["lr"] - m) ** 2).sum())
    return d.groupby(["iso3", "year"]).apply(wsd, include_groups=False).rename("disp").reset_index()


# ----------------------------------------------------------------- charts ---

def base_layout(fig, title=None, ytitle=None, xtitle=None, height=420, legend=True):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=INK), x=0, xanchor="left") if title else None,
        height=height, margin=dict(l=10, r=10, t=50 if title else 20, b=10),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="system-ui, -apple-system, Segoe UI, sans-serif", size=12, color=INK2),
        hoverlabel=dict(font_size=12), showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0, title=None),
        bargap=0.25,
    )
    fig.update_xaxes(title=xtitle, showgrid=False, linecolor="#c3c2b7", ticks="outside",
                     tickcolor="#c3c2b7", zeroline=False)
    fig.update_yaxes(title=ytitle, gridcolor=GRID, gridwidth=1, zeroline=True,
                     zerolinecolor="#c3c2b7", zerolinewidth=1, linecolor="rgba(0,0,0,0)")
    return fig


def show(fig, table=None, caption=None, key=None):
    fig.update_traces(cliponaxis=False, selector=dict(type="scatter"))
    fig.update_traces(cliponaxis=False, selector=dict(type="bar"))
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False}, key=key)
    if caption:
        st.caption(caption)
    if table is not None:
        with st.expander("Data table"):
            st.dataframe(table, width="stretch", hide_index=True)


def fmt_k(x):
    return f"{x/1000:,.1f}k"


def footer():
    st.divider()
    st.caption("Sources: UN Statistics Division, National Accounts Main Aggregates (Jan 2026 upload); "
               "ILOSTAT, employment by economic activity (ILO modelled estimates and national sources), "
               "downloaded 2026-11-05. Method: devtheory WP05. Not covered (no sector employment data): "
               + ", ".join(NOT_COVERED) + ".")


def sidebar_common(grid_choice=True, series_choice=True, key=""):
    st.sidebar.header("Settings")
    grid = "A"
    if grid_choice:
        g = st.sidebar.radio("Sector grid", ["A · 7 sectors", "B · 5 sectors (services combined)"],
                             key=f"grid{key}", help="Grids A and B are separate analyses (WP05 D-025).")
        grid = g[0]
    series = "model"
    if series_choice:
        s = st.sidebar.radio("Employment series", ["ILO modelled estimates", "National surveys (gaps)"],
                             key=f"ser{key}")
        series = "model" if s.startswith("ILO") else "survey"
    agg = st.sidebar.multiselect("Countries in the Caribbean aggregate", list(COUNTRIES),
                                 default=list(COUNTRIES), format_func=lambda c: COUNTRIES[c],
                                 key=f"agg{key}",
                                 help="The aggregate pools value added (constant 2020 US$) and employment. "
                                      "Cuba's US$ values depend on its official exchange rate; consider excluding it.")
    return grid, series, agg
