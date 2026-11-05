"""Build the country x sector x year panel and the coverage report.

    python empirics/code/carib_lp/03_build_panel.py

Inputs:  empirics/data/interim/carib_lp/*.csv (from 02_extract.py)
Outputs: empirics/data/processed/carib_lp/panel_7sector.csv
         empirics/data/processed/carib_lp/emp_all_sources.csv
         empirics/output/carib_lp/coverage.csv, coverage.md
"""
from collections import defaultdict

import numpy as np
import pandas as pd

from config import COUNTRIES, INTERIM, OUTPUT, PROCESSED, SECTOR_ORDER, SECTORS
from concordance import SCHEME_RANK, map_ilo_code

TOL = 0.02  # tolerance for adding-up checks (share of total)


# ------------------------------------------------------------ value added --

def load_va(kind):
    f = INTERIM / f"{kind}.csv"
    if not f.exists():
        return None
    df = pd.read_csv(f)
    w = df[df["target"].notna()].pivot_table(index=["iso3", "year"], columns="target",
                                             values="value", aggfunc="first")
    if {"_CDE", "MAN"} <= set(w.columns):
        w["MIU"] = w["_CDE"] - w["MAN"]
    have = [s for s in SECTOR_ORDER if s in w.columns]
    w["sum7"] = w[have].sum(axis=1, min_count=len(SECTOR_ORDER))
    if "TOTAL_VA" in w.columns:
        w["gap_vs_total"] = w["sum7"] / w["TOTAL_VA"] - 1
    return w


# ------------------------------------------------------------- employment --

SOURCE_PREF = ["BA", "BB", "BX", "HA", "HB", "HX", "AA", "DA", "EA"]  # LFS first, census later


def source_rank(src):
    code = str(src).split(":")[0]
    return SOURCE_PREF.index(code) if code in SOURCE_PREF else len(SOURCE_PREF)


def sectorize(df, label):
    """Collapse ILO detail to 7 sectors for each (country, source, year).

    Uses the most detailed scheme present (ISIC4 > DETAILS > ISIC3 > ISIC2).
    Workers not classified by activity (X) are allocated in proportion to
    the classified ones; their share is kept as x_share.
    """
    if "sex" in df.columns:
        df = df[df["sex"] == "SEX_T"]
    df = df[df["obs_value"].notna()].copy()
    mapped = df["classif1"].map(map_ilo_code)
    df["scheme"] = [m[0] for m in mapped]
    df["kind"] = [m[1] for m in mapped]
    df["sector"] = [m[2] for m in mapped]
    df = df[df["scheme"].notna()]
    rows, notes = [], []
    for (iso, src, yr), g in df.groupby(["ref_area", "source", "time"]):
        schemes = sorted({s for s in g.loc[g["kind"] == "detail", "scheme"]}, key=SCHEME_RANK.get)
        if not schemes:
            continue
        sch = schemes[0]
        gs = g[g["scheme"] == sch]
        bad = gs[gs["kind"].isin(["mixed", "unknown"]) & (gs["obs_value"] > 0)]
        if len(bad):
            notes.append((iso, src, yr, f"{label}: {sch} codes not mapped: {sorted(bad['classif1'])}"))
        det = gs[gs["kind"] == "detail"].groupby("sector")["obs_value"].sum()
        x = gs.loc[gs["kind"] == "x", "obs_value"].sum()
        tot_rows = gs.loc[gs["kind"] == "total", "obs_value"]
        total = tot_rows.iloc[0] if len(tot_rows) else det.sum() + x
        classified = det.sum()
        gap = (classified + x) / total - 1 if total else np.nan
        missing = [s for s in SECTOR_ORDER if s not in det.index]
        scale = total / classified if classified else np.nan
        for s in SECTOR_ORDER:
            rows.append({
                "iso3": iso, "year": int(str(yr)[:4]), "source": src, "scheme": sch,
                "sector": s, "emp_raw": det.get(s, np.nan), "emp": det.get(s, np.nan) * scale,
                "total": total, "x_share": x / total if total else np.nan,
                "addup_gap": gap, "missing_sectors": ",".join(missing),
            })
    return pd.DataFrame(rows), notes


def pick_survey_source(emp):
    """One survey source per country-year: labour force survey first, then others."""
    if emp.empty:
        return emp
    keys = emp[["iso3", "year", "source"]].drop_duplicates()
    keys["rank"] = keys["source"].map(source_rank)
    best = keys.sort_values(["iso3", "year", "rank", "source"]).groupby(["iso3", "year"]).head(1)
    return emp.merge(best[["iso3", "year", "source"]], on=["iso3", "year", "source"])


# ------------------------------------------------------------------ build --

def span(years):
    years = sorted(set(int(y) for y in years))
    if not years:
        return "—", 0, ""
    gaps = [f"{a+1}-{b-1}" if b - a > 2 else str(a + 1) for a, b in zip(years, years[1:]) if b - a > 1]
    return f"{years[0]}–{years[-1]}", len(years), ", ".join(gaps)


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    notes = []

    va_k = load_va("un_va_k2020_usd")
    va_c = load_va("un_va_cur_usd")

    emp_m = emp_s = pd.DataFrame()
    if (INTERIM / "ilo_emp_model.csv").exists():
        emp_m, n = sectorize(pd.read_csv(INTERIM / "ilo_emp_model.csv", low_memory=False), "model")
        notes += n
    if (INTERIM / "ilo_emp_survey.csv").exists():
        emp_all, n = sectorize(pd.read_csv(INTERIM / "ilo_emp_survey.csv", low_memory=False), "survey")
        notes += n
        if not emp_all.empty:
            emp_all.to_csv(PROCESSED / "emp_all_sources.csv", index=False)
        emp_s = pick_survey_source(emp_all)

    # ---- panel
    parts = []
    if va_k is not None:
        parts.append(va_k[SECTOR_ORDER].stack().rename("va_k2020usd"))
    if va_c is not None:
        parts.append(va_c[SECTOR_ORDER].stack().rename("va_cur_usd"))
    panel = pd.concat(parts, axis=1).reset_index() if parts else pd.DataFrame(columns=["iso3", "year", "target"])
    panel = panel.rename(columns={"target": "sector", "level_2": "sector"})
    for lab, e in [("model", emp_m), ("survey", emp_s)]:
        if e.empty:
            continue
        e2 = e[["iso3", "year", "sector", "emp", "source", "scheme", "x_share"]].rename(columns={
            "emp": f"emp_{lab}", "source": f"src_{lab}", "scheme": f"scheme_{lab}", "x_share": f"xshare_{lab}"})
        panel = panel.merge(e2, on=["iso3", "year", "sector"], how="outer")
    if "va_k2020usd" in panel.columns:
        for lab in ["model", "survey"]:
            if f"emp_{lab}" in panel.columns:
                # VA in US dollars (units as published), employment in thousands -> USD per worker
                panel[f"lp_{lab}"] = panel["va_k2020usd"] / (panel[f"emp_{lab}"] * 1000)
    panel["sector_name"] = panel["sector"].map(SECTORS)
    panel = panel.sort_values(["iso3", "year", "sector"])
    panel.to_csv(PROCESSED / "panel_7sector.csv", index=False)

    # ---- coverage
    cov = []
    for iso, (_, name) in COUNTRIES.items():
        r = {"iso3": iso, "country": name}
        if va_k is not None and iso in va_k.index.get_level_values(0):
            v = va_k.loc[iso]
            full = v[v["sum7"].notna()]
            r["va_years"], r["va_n"], r["va_gaps"] = span(full.index)
            if "gap_vs_total" in v:
                r["va_max_addup_gap"] = full["gap_vs_total"].abs().max()
            if "MIU" in v:
                r["va_neg_MIU_years"] = int((full["MIU"] < 0).sum())
        for lab, e in [("model", emp_m), ("survey", emp_s)]:
            if e.empty:
                continue
            ei = e[e["iso3"] == iso]
            full = ei.groupby("year").filter(lambda g: g["missing_sectors"].iloc[0] == "")
            r[f"{lab}_years"], r[f"{lab}_n"], r[f"{lab}_gaps"] = span(full["year"])
            r[f"{lab}_partial_years"] = int(ei["year"].nunique() - full["year"].nunique())
            r[f"{lab}_schemes"] = ",".join(sorted(ei["scheme"].unique()))
            r[f"{lab}_max_xshare"] = ei["x_share"].max() if len(ei) else np.nan
            r[f"{lab}_max_addup_gap"] = ei["addup_gap"].abs().max() if len(ei) else np.nan
            if lab == "survey":
                r["survey_sources"] = "; ".join(sorted({str(s).split(":")[0] for s in ei["source"]}))
                r["survey_year_list"] = ", ".join(str(y) for y in sorted(full["year"].unique()))
        cov.append(r)
    cov = pd.DataFrame(cov)
    cov.to_csv(OUTPUT / "coverage.csv", index=False)
    write_report(cov, panel, notes)
    print(cov.to_string())


def fmt(x, pct=False):
    if pd.isna(x) or x == "":
        return "—"
    if pct:
        return f"{x:.1%}"
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


def write_report(cov, panel, notes):
    L = ["# Caribbean labour productivity: data coverage",
         "",
         "Generated by `empirics/code/carib_lp/03_build_panel.py`. Do not edit by hand.",
         "",
         "Sectors: " + "; ".join(f"**{k}** {v}" for k, v in SECTORS.items()) + ".",
         "",
         "A year counts as covered when all seven sectors are present. Survey years use one source per year "
         "(labour force survey preferred); the source codes are ILO's (BA = labour force survey, AA = population census, "
         "HA/HB = other household surveys, DA = official estimates).",
         ""]
    has = lambda c: c in cov.columns
    if has("va_years"):
        L += ["## Value added (UN National Accounts Main Aggregates, constant 2020 US$)", "",
              "| Country | Years | n | Gaps | Max add-up gap vs total VA | Years with negative mining+utilities |",
              "|---|---|---|---|---|---|"]
        for _, r in cov.iterrows():
            L.append(f"| {r['country']} | {fmt(r.get('va_years'))} | {fmt(r.get('va_n'))} | {fmt(r.get('va_gaps'))} | "
                     f"{fmt(r.get('va_max_addup_gap'), True)} | {fmt(r.get('va_neg_MIU_years'))} |")
        L.append("")
    for lab, title in [("model", "Employment, ILO modelled estimates"), ("survey", "Employment, national survey and census data (ILOSTAT)")]:
        if not has(f"{lab}_years"):
            continue
        L += [f"## {title}", ""]
        if lab == "model":
            L += ["| Country | Years (7 sectors) | n | Partial years | Scheme | Max unclassified share | Max add-up gap |",
                  "|---|---|---|---|---|---|---|"]
            for _, r in cov.iterrows():
                L.append(f"| {r['country']} | {fmt(r.get('model_years'))} | {fmt(r.get('model_n'))} | {fmt(r.get('model_partial_years'))} | "
                         f"{fmt(r.get('model_schemes'))} | {fmt(r.get('model_max_xshare'), True)} | {fmt(r.get('model_max_addup_gap'), True)} |")
        else:
            L += ["| Country | Years with 7 sectors | n | Partial years | Sources | Scheme | Max unclassified share |",
                  "|---|---|---|---|---|---|---|"]
            for _, r in cov.iterrows():
                L.append(f"| {r['country']} | {fmt(r.get('survey_year_list'))} | {fmt(r.get('survey_n'))} | {fmt(r.get('survey_partial_years'))} | "
                         f"{fmt(r.get('survey_sources'))} | {fmt(r.get('survey_schemes'))} | {fmt(r.get('survey_max_xshare'), True)} |")
        L.append("")
    if notes:
        L += ["## Mapping notes", ""] + [f"- {i} {y} ({s}): {t}" for i, s, y, t in notes[:200]]
        if len(notes) > 200:
            L.append(f"- … {len(notes) - 200} more")
        L.append("")
    (OUTPUT / "coverage.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
