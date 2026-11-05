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
MAX_X_SHARE = 0.25  # survey country-years with more workers unclassified than this are unusable (D-023)


# ------------------------------------------------------------ value added --

def _wide(kind):
    f = INTERIM / f"{kind}.csv"
    if not f.exists():
        return None
    df = pd.read_csv(f)
    return df[df["target"].notna()].pivot_table(index=["iso3", "year"], columns="target",
                                                values="value", aggfunc="first")


def load_va(kind):
    """Wide VA table. Constant-price series are chain-linked, so components do
    not add up outside the 2020 base year; mining+utilities in constant prices
    is therefore built as current-price (C-E minus D) deflated by the C-E
    deflator (D-023), not as a constant-price residual, which can go negative."""
    w = _wide(kind)
    if w is None:
        return None
    if {"_CDE", "MAN"} <= set(w.columns):
        w["MIU"] = w["_CDE"] - w["MAN"]
        w["MIU_residual"] = w["MIU"]
        cur = _wide("un_va_cur_usd") if kind != "un_va_cur_usd" else None
        if cur is not None:
            defl = w["_CDE"] / cur["_CDE"].reindex(w.index)
            w["MIU"] = (cur["_CDE"] - cur["MAN"]).reindex(w.index) * defl
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
        if total and x / total > MAX_X_SHARE:
            notes.append((iso, src, yr, f"{label}: {x/total:.0%} of workers unclassified; country-year dropped"))
            missing = ["UNCLASSIFIED>25%"]
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
    emp = emp[emp["missing_sectors"] == ""]  # usable country-years only
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

    emp_m = emp_s = emp_all = pd.DataFrame()
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
        for lab, e, eall in [("model", emp_m, emp_m), ("survey", emp_s, emp_all)]:
            if e.empty:
                continue
            ei = e[e["iso3"] == iso]
            full = ei.groupby("year").filter(lambda g: g["missing_sectors"].iloc[0] == "")
            r[f"{lab}_years"], r[f"{lab}_n"], r[f"{lab}_gaps"] = span(full["year"])
            ea = eall[eall["iso3"] == iso]
            r[f"{lab}_partial_years"] = int(ea["year"].nunique() - full["year"].nunique())
            r[f"{lab}_schemes"] = ",".join(sorted(ei["scheme"].unique()))
            r[f"{lab}_max_xshare"] = ei["x_share"].max() if len(ei) else np.nan
            r[f"{lab}_max_addup_gap"] = ei["addup_gap"].abs().max() if len(ei) else np.nan
            if lab == "survey":
                r["survey_sources"] = "; ".join(sorted({str(s).split(":")[0] for s in ei["source"]}))
                r["survey_year_list"] = ", ".join(str(y) for y in sorted(full["year"].unique()))
        cov.append(r)
    cov = pd.DataFrame(cov)
    cov = cov.merge(summary(va_k, emp_m, emp_s), on="iso3", how="left")
    cov.to_csv(OUTPUT / "coverage.csv", index=False)
    write_report(cov, panel, notes)
    print(cov.to_string())


def six_group_years():
    """Survey years that have ILO's six broad groups (AGR, MEL, MAN, CON, MKT, PUB)
    but no usable seven-sector ISIC breakdown: a possible coarser extension."""
    f = INTERIM / "ilo_emp_survey.csv"
    if not f.exists():
        return {}
    s = pd.read_csv(f, low_memory=False)
    s = s[(s["sex"] == "SEX_T") & s["classif1"].str.startswith("ECO_AGGREGATE") & s["obs_value"].notna()]
    groups = s.groupby(["ref_area", "time"])["classif1"].agg(lambda x: {c.split("_")[-1] for c in x})
    ok = groups[groups.map(lambda g: {"AGR", "MAN", "CON", "MEL", "MKT", "PUB"} <= g)]
    out = {}
    for (iso, yr) in ok.index:
        out.setdefault(iso, set()).add(int(yr))
    return out


FULL_SECTIONS = {"ISIC4": set("ABCDEFGHIJKLMNOPQRS"), "ISIC3": set("ABCDEFGHIJKLMNO")}


def missing_sections(emp_s):
    """ISIC sections absent from the survey country-years used in the panel.
    An absent section was merged by the national survey into another one; when
    the merge crosses target sectors (e.g. business services into J), the
    7-sector split is distorted even though all 7 sectors are present."""
    f = INTERIM / "ilo_emp_survey.csv"
    if emp_s.empty or not f.exists():
        return {}
    s = pd.read_csv(f, low_memory=False)
    s = s[(s["sex"] == "SEX_T") & s["obs_value"].notna()]
    sel = emp_s[["iso3", "year", "source", "scheme"]].drop_duplicates()
    s["time"] = s["time"].astype(str).str[:4].astype(int)
    s = s.merge(sel, left_on=["ref_area", "time", "source"], right_on=["iso3", "year", "source"])
    s = s[[c.startswith(f"ECO_{sc}_") for c, sc in zip(s["classif1"], s["scheme"])]]
    out = {}
    for (iso, yr, sc), g in s.groupby(["iso3", "year", "scheme"]):
        have = {c for code in g["classif1"] for c in code.split("_")[-1] if code.split("_")[-1] not in ("TOTAL", "X")}
        miss = "".join(sorted(FULL_SECTIONS.get(sc, set()) - have))
        if miss:
            out.setdefault(iso, {}).setdefault(f"{sc} {miss}", []).append(int(yr))
    return {iso: "; ".join(f"{k} ({span(v)[0]})" for k, v in d.items()) for iso, d in out.items()}


def summary(va_k, emp_m, emp_s):
    """Per country: what a decomposition can rest on."""
    six = six_group_years()
    miss = missing_sections(emp_s)
    rows = []
    for iso in COUNTRIES:
        r = {"iso3": iso}
        va_years = set(va_k.loc[iso].index[va_k.loc[iso]["sum7"].notna()]) if va_k is not None and iso in va_k.index.get_level_values(0) else set()
        m_years = set(emp_m.loc[emp_m["iso3"] == iso, "year"]) if not emp_m.empty else set()
        s_years = set(emp_s.loc[emp_s["iso3"] == iso, "year"]) if not emp_s.empty else set()
        both_m = va_years & m_years
        r["lp_model_span"] = span(both_m)[0]
        r["lp_model_n"] = len(both_m)
        anchored = s_years & both_m
        r["model_years_with_survey"] = len(anchored)
        r["model_survey_anchor_share"] = len(anchored) / len(both_m) if both_m else np.nan
        r["lp_survey_n"] = len(va_years & s_years)
        r["six_group_only_years"] = len(six.get(iso, set()) - s_years)
        # modelled vs survey employment shares in common years (mean absolute difference, pp)
        if anchored:
            def shares(e):
                x = e[(e["iso3"] == iso) & e["year"].isin(anchored)].pivot_table(index="year", columns="sector", values="emp")
                return x.div(x.sum(axis=1), axis=0)
            d = (shares(emp_m) - shares(emp_s)).abs()
            r["model_vs_survey_share_mad_pp"] = 100 * d.mean().mean()
            r["model_vs_survey_share_max_pp"] = 100 * d.max().max()
            tot = lambda e: e[(e["iso3"] == iso) & e["year"].isin(anchored)].groupby("year")["emp"].sum()
            r["model_over_survey_total"] = (tot(emp_m) / tot(emp_s)).median()
        r["survey_missing_sections"] = miss.get(iso, "")
        rows.append(r)
    return pd.DataFrame(rows)


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
    if has("lp_model_n"):
        L += ["## Summary: what a decomposition can rest on", "",
              "*LP years* = years with both value added (7 sectors) and employment (7 sectors). "
              "*Survey-anchored* = share of modelled years that are also usable survey years; the rest are ILO interpolation or extrapolation. "
              "*Model vs survey* = mean absolute gap between modelled and survey employment shares in common years, in percentage points (max in brackets). "
              "*Model/survey total* = median ratio of modelled to survey total employment in common years. "
              "*Six-group-only years* = survey years with ILO's six broad groups but no usable 7-sector detail.", "",
              "| Country | LP years, modelled employment | Survey-anchored | LP years, survey employment | Model vs survey shares (pp) | Model/survey total | Six-group-only years |",
              "|---|---|---|---|---|---|---|"]
        for _, r in cov.iterrows():
            mvs = "—" if pd.isna(r.get("model_vs_survey_share_mad_pp")) else f"{r['model_vs_survey_share_mad_pp']:.1f} ({r['model_vs_survey_share_max_pp']:.1f})"
            L.append(f"| {r['country']} | {fmt(r.get('lp_model_span'))} ({fmt(r.get('lp_model_n'))}) | "
                     f"{fmt(r.get('model_survey_anchor_share'), True) if r.get('lp_model_n') else '—'} | {fmt(r.get('lp_survey_n'))} | {mvs} | "
                     f"{'—' if pd.isna(r.get('model_over_survey_total')) else format(r['model_over_survey_total'], '.2f')} | {fmt(r.get('six_group_only_years'))} |")
        L.append("")
    if has("va_years"):
        L += ["## Value added (UN National Accounts Main Aggregates, constant 2020 US$)", "",
              "Constant-price series are chain-linked, so the seven sectors add up to total value added only in the 2020 base year "
              "(current-price series add up exactly). The add-up gap column shows the largest departure. Mining+utilities in constant "
              "prices is built from current prices with the C–E deflator, so it cannot go negative (D-023).", "",
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
    if has("survey_missing_sections"):
        L += ["## ISIC sections missing from usable survey years", "",
              "A missing section was merged by the national survey into another one. Harmless when both fall in the same target "
              "sector (e.g. J into H); distorting when they do not (e.g. business services M–N into J moves workers from OTH to TSC).", "",
              "| Country | Missing sections (years) |", "|---|---|"]
        for _, r in cov.iterrows():
            if r.get("survey_missing_sections"):
                L.append(f"| {r['country']} | {r['survey_missing_sections']} |")
        L.append("")
    if notes:
        L += ["## Mapping notes", ""] + [f"- {i} {y} ({s}): {t}" for i, s, y, t in notes[:200]]
        if len(notes) > 200:
            L.append(f"- … {len(notes) - 200} more")
        L.append("")
    (OUTPUT / "coverage.md").write_text("\n".join(L))


if __name__ == "__main__":
    main()
