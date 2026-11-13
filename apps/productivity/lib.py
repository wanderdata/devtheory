"""Shared data loading, computations and chart helpers for the sectoral
labour-productivity dashboard (Latin America and the Caribbean, and the Caribbean).

Everything is computed from files committed in the repository (empirics/data/...
and empirics/output/...), so the app runs on Streamlit Community Cloud with no
downloads.

Scope. The region is chosen per session in the sidebar (app.py) and read here from
st.session_state["scope"]; nothing scope-dependent is stored in module globals,
because Streamlit serves all sessions from one process. Cached loaders take the
scope as an argument so each scope has its own cache entries.
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
from apps.common.theme import (AUTHOR, AXIS, C_CONTEXT, C_HIGHLIGHT, GRID, INK, INK2, MUTED,  # noqa: E402,F401
                               base_layout, credit, fmt_k, show)
from empirics.common import countries as cc  # noqa: E402

# Display names (ECLAC short forms used in figures), from the shared module.
NAMES = dict(cc.SHORT)
CARIBBEAN16 = list(cc.CARIBBEAN16)

SCOPES = {
    "lac": dict(label=cc.SCOPES["lac"]["label"], tag=cc.SCOPES["lac"]["tag"],
                members=sorted(NAMES, key=lambda c: NAMES[c]),
                agg_name="Latin America and the Caribbean (pooled)", agg_short="LAC",
                # US$ levels unusable for pooling: Venezuela (2020-price conversion after
                # hyperinflation), Cuba (official exchange rate). D-033.
                agg_exclude=list(cc.POOL_EXCLUDE_LAC),
                blurb="the **33 Latin American and Caribbean member States of ECLAC**"),
    "carib": dict(label=cc.SCOPES["carib"]["label"], tag=cc.SCOPES["carib"]["tag"], members=CARIBBEAN16,
                  agg_name="Caribbean (selected countries, pooled)", agg_short="Caribbean",
                  agg_exclude=[],
                  blurb="the **16 Caribbean member States of ECLAC served by its subregional "
                        "headquarters in Port of Spain** (the broad definition of the Caribbean, "
                        "including Cuba, the Dominican Republic and Haiti)"),
}
CARIB = "AGG"  # code for the pooled aggregate of the active scope


def scope():
    return st.session_state.get("scope", "lac")


def scope_info(sc=None):
    return SCOPES[sc or scope()]


def proc_dir(sc=None):
    return ROOT / "empirics" / "data" / "processed" / scope_info(sc)["tag"]


def interim_dir(sc=None):
    return ROOT / "empirics" / "data" / "interim" / scope_info(sc)["tag"]


def out_dir(sc=None):
    return ROOT / "empirics" / "output" / scope_info(sc)["tag"]


@st.cache_data
def _countries(sc):
    """Members of the scope with sectoral employment (ILO modelled), in display order."""
    p = pd.read_csv(proc_dir(sc) / "panel_7sector.csv", usecols=["iso3", "emp_model"])
    have = set(p.dropna(subset=["emp_model"])["iso3"])
    return {c: NAMES[c] for c in sorted(have, key=lambda c: NAMES[c])}


def countries():
    return _countries(scope())


def not_covered():
    return [NAMES[c] for c in scope_info()["members"] if c not in countries()]


def agg_default():
    return [c for c in countries() if c not in scope_info()["agg_exclude"]]


def default_country():
    c = countries()
    return list(c).index("DOM") if "DOM" in c else 0

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

# Validated colour-blind-safe categorical palette, one fixed colour per sector.
SECTOR_COLORS = {"AGR": "#2a78d6", "MIU": "#eb6834", "MAN": "#1baf7a", "CON": "#eda100",
                 "TRH": "#e87ba4", "TSC": "#008300", "OTH": "#6250d6", "SER": "#6250d6"}
C_WITHIN, C_STRUCT = "#2a78d6", "#eb6834"          # component colours (slots 1, 2)
C_STATIC, C_DYNAMIC = "#eb6834", "#1baf7a"
GRADE_COLORS = {"A": "#0ca30c", "B": "#fab219", "C": "#d03b3b"}
GRADE_TEXT = {"A": "A · both endpoints near survey years",
              "B": "B · one endpoint near a survey year",
              "C": "C · no survey anchor (ILO model only)"}


# ------------------------------------------------------------------ loading --

@st.cache_data
def _load_panel(sc):
    p = pd.read_csv(proc_dir(sc) / "panel_7sector.csv")
    return p[p["iso3"].isin(_countries(sc))]


def load_panel():
    return _load_panel(scope())


@st.cache_data
def _load_emp5(sc):
    return pd.read_csv(proc_dir(sc) / "emp_5sector.csv")


def load_emp5():
    return _load_emp5(scope())


@st.cache_data
def _load_excluded_surveys(sc):
    f = proc_dir(sc) / "emp_all_sources.csv"
    if not f.exists():
        return {}
    e = pd.read_csv(f, usecols=["iso3", "year", "missing_sectors", "cov_ratio"])
    e = e[e["missing_sectors"] == "PARTIAL_COVERAGE"].drop_duplicates(["iso3", "year"])
    return {iso: dict(zip(g["year"], g["cov_ratio"])) for iso, g in e.groupby("iso3")}


def load_excluded_surveys():
    """Survey years not used because they are not national (D-031): {iso3: {year: coverage ratio}}."""
    return _load_excluded_surveys(scope())


@st.cache_data
def _load_output(sc, grid, name):
    f = out_dir(sc) / f"grid_{grid}" / f"{name}.csv"
    if not f.exists():
        return pd.DataFrame()
    d = pd.read_csv(f)
    if {"iso3", "country"} <= set(d.columns):
        d["country"] = d["iso3"].map(NAMES).fillna(d["country"])
    return d


def load_output(grid, name):
    return _load_output(scope(), grid, name)


@st.cache_data
def _load_extra(sc, folder, name):
    f = out_dir(sc) / folder / f"{name}.csv"
    if not f.exists():
        return pd.DataFrame()
    d = pd.read_csv(f)
    if "iso3" in d.columns:
        d["country"] = d["iso3"].map(NAMES).fillna(d["iso3"])
    return d


def load_extra(folder, name):
    """Outputs of steps 08 (folder 'ladder') and 09 (folder 'baumol')."""
    return _load_extra(scope(), folder, name)


# Ladder verdicts (08_ladder.py), best to worst, with fixed colours.
LADDER_VERDICTS = {
    "improvement": "#1baf7a",
    "improvement, weighting the lower percentiles": "#9fd9c2",
    "ambiguous": "#c3c2b7",
    "depends on prices": "#eda100",
    "deterioration, weighting the lower percentiles": "#f5b99f",
    "deterioration": "#eb6834",
}
STEP_NAMES = {"Z_UNEMP": "Unemployed", "Z_OLF": "Outside the labour force", "Z_65PLUS": "Aged 65+, not employed",
              "Z_NOTEMP": "Not employed"}


@st.cache_data
def _load_labour(sc):
    f = interim_dir(sc) / "ilo_labour.csv"
    return pd.read_csv(f) if f.exists() else None


def load_labour():
    """ILO modelled labour-market indicators (from 06_extract_labour.py)."""
    return _load_labour(scope())


def labour_or_note(indicators):
    lab = load_labour()
    if lab is None or not set(indicators) <= set(lab["indicator"].unique()):
        st.info("**Data pending.** This chart needs ILO modelled labour-market series "
                f"({', '.join(indicators)}). Add the files and run "
                "`empirics/code/carib_lp/06_extract_labour.py`.")
        return None
    return lab


def sector_long(grid, emp_series="model", countries=None):
    """Long table iso3, year, sector, va_k (constant 2020 US$), va_cur, emp (thousands)
    on the chosen grid, plus a pooled aggregate (code CARIB) over `countries`."""
    return _sector_long(scope(), grid, emp_series, tuple(countries) if countries else None)


@st.cache_data
def _sector_long(sc, grid, emp_series, countries):
    p = _load_panel(sc)
    va = p[["iso3", "year", "sector", "va_k2020usd", "va_cur_usd"]].dropna()
    va = va.assign(sector=va["sector"].map(GRID_MAP[grid]))
    va = va.groupby(["iso3", "year", "sector"], as_index=False)[["va_k2020usd", "va_cur_usd"]].sum()
    if grid == "A":
        col = f"emp_{emp_series}"
        e = p[["iso3", "year", "sector", col]].dropna().rename(columns={col: "emp"})
    else:
        e5 = _load_emp5(sc)
        e = e5[e5["series"] == emp_series][["iso3", "year", "sector", "emp"]]
    df = va.merge(e, on=["iso3", "year", "sector"], how="inner")
    df = df[df["iso3"].isin(_countries(sc))]
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


AGG_LABEL = "Regional aggregate (pooled)"


def name(iso):
    # Session-independent on purpose: widget labels must not depend on state read at format time.
    return AGG_LABEL if iso == CARIB else NAMES.get(iso, iso)


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
    prices='constant2020' : baseline (fixed constant 2020 prices); levels in US$
                            per worker.
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


def annual_decomp(grid, emp_series, countries, prices="constant2020"):
    return _annual_decomp(scope(), grid, emp_series, tuple(countries) if countries else None, prices)


@st.cache_data
def _annual_decomp(sc, grid, emp_series, countries, prices):
    df = _sector_long(sc, grid, emp_series, countries)
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


def survey_years(grid):
    """Usable survey years per country for the grid (for anchoring markers)."""
    return _survey_years(scope(), grid)


@st.cache_data
def _survey_years(sc, grid):
    if grid == "A":
        p = _load_panel(sc)
        s = p.dropna(subset=["emp_survey"])
    else:
        e5 = _load_emp5(sc)
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

def footer(extra=""):
    nc = not_covered()
    credit("Sources: UN Statistics Division, National Accounts Main Aggregates (Jan 2026 upload); "
           "ILOSTAT, employment by economic activity (ILO modelled estimates and national sources), "
           "downloaded 2026-11-09. " + (extra + " " if extra else "") + "Method: devtheory WP05, WP06 and WP08."
           + (" Not covered (no sector employment data): " + ", ".join(nc) + "." if nc else ""))


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
    info = scope_info()
    excl = ", ".join(NAMES[c] for c in info["agg_exclude"])
    agg = st.sidebar.multiselect(
        f"Countries in the {info['agg_short']} aggregate", list(countries()),
        default=agg_default(), format_func=lambda c: NAMES[c], key=f"agg{key}_{scope()}",
        help="The aggregate pools value added (constant 2020 US$) and employment, so large economies "
             "dominate it. " + (f"Excluded by default: {excl}. Their US$ levels are not comparable "
             "(Venezuela: conversion at 2020 prices after hyperinflation; Cuba: official exchange rate), "
             "although their growth rates can be read country by country." if excl else
             "Cuba's US$ values depend on its official exchange rate; consider excluding it."))
    return grid, series, agg


# ---------------------------------------------------------- price bases ----

PRICE_BASES = {
    "initial": "Initial-year prices of each period",
    "chained": "Chained (previous-year prices, averaged)",
    "final": "Final-year prices of each period",
}

PRICE_NOTE = """
**Why the price base matters.** A decomposition has to add sectors' value added together, so it must
value every sector at a common set of prices. The UN's constant-2020-price series cannot be used for that:
they are chain-linked and do not add up across sectors outside 2020. Three treatments are offered, and
**each can fail in a known way**.

- **Initial-year prices (default).** The whole period is valued at the prices of its first year
  (WP05's method, D-024). Only the two endpoints enter, so year-to-year noise in employment shares does not
  accumulate. It fails where a sector's relative price later falls a lot. Uruguay is the main case: the volume of
  transport, storage and communications (which includes telecoms) rose 7.5-fold over 2000–19 while its relative
  price fell, so productivity growth is 3.5% a year at 2000 prices, against 1.4% from the official
  chain-linked total.
- **Chained.** One decomposition per year at previous-year prices, averaged over the period, so relative
  prices are updated every year (D-032). This fixes the Uruguay problem (1.8% a year). It fails where annual
  employment shares are noisy. Where ILO's estimates track annual surveys, sampling noise moves shares back and
  forth every year, and chaining turns that noise into reallocation that never happened. Bolivia is the clearest
  case: its agriculture share goes 36.6 → 41.8 → 39.7 → 32.7% in 2000–03, and its 2000–19 structural term is
  −0.24 chained against +0.46 and +0.38 at the two fixed bases (D-035).
- **Final-year prices.** The whole period is valued at the prices of its last year. It has the opposite
  relative-price bias to initial-year prices and works as a bound.

Fixed-base totals are linear averages, (P_T − P_0)/P_0 per year. The chained total is a mean of annual rates.
In chained form the dynamic term is close to zero by construction, so read the static/dynamic split at a
fixed base.

**Read a structural-change result only where the three treatments agree.** The *Verdict* column classifies
each country-period: positive (or negative) at all three, near zero at all three (|term| < 0.1 pp), same sign
but different size, or sign depends on the price base. In LAC about a fifth of well-anchored country-periods
fall in the last group. Pooled regional results are much less sensitive, because noise and relative-price
swings partly cancel across countries.
"""


SMALL = 0.10


def verdict(vals):
    v = np.array(vals, dtype=float)
    if np.isnan(v).any():
        return "incomplete"
    if (v >= SMALL).all():
        return "positive at all three"
    if (v <= -SMALL).all():
        return "negative at all three"
    if (np.abs(v) < SMALL).all():
        return "near zero at all three"
    if (v > 0).all() or (v < 0).all():
        return "same sign, size differs"
    return "sign depends on price base"


def verdicts(grid, no_mining=False):
    """Agreement of the structural term across the three price bases, by (iso3, period)."""
    names = (["robust_no_mining", "robust_no_mining_chained", "robust_no_mining_final"] if no_mining
             else ["main", "robust_chained", "robust_final_prices"])
    parts = []
    for n in names:
        d = load_output(grid, n)
        if d.empty:
            return pd.DataFrame(columns=["iso3", "period", "verdict"])
        parts.append(d.set_index(["iso3", "period"])["struct_pp"].rename(n))
    w = pd.concat(parts, axis=1)
    w["verdict"] = [verdict(r) for r in w[names].values]
    return w.reset_index()[["iso3", "period", "verdict"]]


def price_choice(key=""):
    p = st.sidebar.radio("Price base", list(PRICE_BASES), format_func=PRICE_BASES.get,
                         key=f"price{key}", help="See the note on price bases on this page.")
    return p


def output_name(spec, price):
    """File stem in empirics/output/<scope>/grid_X/ for a specification and price base."""
    if spec == "survey":
        return "robust_survey"
    base = {"chained": "robust_chained", "initial": "main", "final": "robust_final_prices"}[price]
    if spec == "no_mining":
        return {"chained": "robust_no_mining_chained", "initial": "robust_no_mining",
                "final": "robust_no_mining_final"}[price]
    return base
