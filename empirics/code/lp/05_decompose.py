"""Decompositions for grids A (7 sectors) and B (5 sectors), kept separate (D-025, D-026).

    python empirics/code/lp/05_decompose.py

Main specification (D-026)
  * Employment: ILO modelled estimates (complete, harmonized totals; validated
    against surveys in 04_validate.py).
  * Periods: fixed benchmark periods PERIODS. Each country-period is graded by
    survey anchoring: an endpoint is anchored if a usable survey year (for that
    grid) lies within ANCHOR_WINDOW years of it.
        A = both endpoints anchored   -> interpreted
        B = one endpoint anchored     -> reported, flagged
        C = neither                   -> appendix only (pure ILO model)
  * Prices: initial-year prices of each period (decompose.py).

Robustness (same grid)
  R1 survey employment between the nearest usable survey years (grade A only)
  R2 final-year prices
  R3 excluding mining and utilities (sector dropped from VA and employment)

Outputs per grid in empirics/output/<scope>_lp/grid_{A,B}/:
  main.csv, robust_survey.csv, robust_final_prices.csv, robust_no_mining.csv,
  sectors_main.csv (sector detail for scatter plots), and results.md (all grids).
"""
import numpy as np
import pandas as pd

from config import COUNTRIES, INTERIM, OUTPUT, PERIODS, PROCESSED, SCOPE_NAME, TAG
from decompose import GRIDS, decompose, decompose_chained, va_at_prices

ANCHOR_WINDOW = 2


def load():
    p = pd.read_csv(PROCESSED / "panel_7sector.csv")
    va = p.dropna(subset=["va_cur_usd", "va_k2020usd"]).set_index(["iso3", "year", "sector"])[["va_cur_usd", "va_k2020usd"]]
    e5 = pd.read_csv(PROCESSED / "emp_5sector.csv")
    emp = {
        ("A", "model"): p.dropna(subset=["emp_model"]).set_index(["iso3", "year", "sector"])["emp_model"],
        ("A", "survey"): p.dropna(subset=["emp_survey"]).set_index(["iso3", "year", "sector"])["emp_survey"],
        ("B", "model"): e5[e5.series == "model"].set_index(["iso3", "year", "sector"])["emp"],
        ("B", "survey"): e5[e5.series == "survey"].set_index(["iso3", "year", "sector"])["emp"],
    }
    # official aggregate for the check: total VA at constant 2020 prices
    tot = pd.read_csv(INTERIM / "un_va_k2020_usd.csv")
    tot = tot[tot.target == "TOTAL_VA"].set_index(["iso3", "year"])["value"]
    return va, emp, tot


def years(s, iso):
    return sorted(s.loc[iso].index.get_level_values(0).unique()) if iso in s.index.get_level_values(0) else []


def nearest(target, avail, window=ANCHOR_WINDOW):
    c = [y for y in avail if abs(y - target) <= window]
    return min(c, key=lambda y: (abs(y - target), y)) if c else None


def run(grid, va, emp, tot, base="initial", drop=(), series="model", survey_endpoints=False):
    m, s = emp[(grid, "model")], emp[(grid, series if series == "survey" else "survey")]
    use = emp[(grid, series)]
    gmap = GRIDS[grid]
    drop_g = {gmap[d] for d in drop}
    rows, detail = [], []
    for iso in COUNTRIES:
        if not years(m, iso):
            continue
        sy = years(s, iso)
        for t0, T in PERIODS:
            a0, aT = nearest(t0, sy), nearest(T, sy)
            grade = "A" if a0 and aT else ("B" if a0 or aT else "C")
            if survey_endpoints:
                if grade != "A" or a0 == aT:
                    continue
                e0, eT = a0, aT
            else:
                e0, eT = t0, T
            if e0 not in years(use, iso) or eT not in years(use, iso):
                continue
            l0, lT = use.loc[(iso, e0)], use.loc[(iso, eT)]
            l0, lT = l0[~l0.index.isin(drop_g)], lT[~lT.index.isin(drop_g)]
            if base == "chained":
                r = decompose_chained(va, use, iso, e0, eT, gmap, drop=drop)
            else:
                y = va_at_prices(va, iso, e0, eT, base, gmap, drop=drop)
                r = decompose(y, l0, lT, eT - e0)
            if r is None:
                continue
            row = {"iso3": iso, "country": COUNTRIES[iso][1], "period": f"{t0}–{T}",
                   "t0": e0, "T": eT, "grade": grade, "anchor_t0": a0, "anchor_T": aT}
            row.update({k: v for k, v in r.items() if k != "detail"})
            # check: Laspeyres growth vs official chain-linked total VA per worker
            if not drop and (iso, e0) in tot.index and (iso, eT) in tot.index:
                off = (tot[(iso, eT)] / lT.sum()) / (tot[(iso, e0)] / l0.sum())
                row["official_growth_pp"] = (off - 1) * 100 / (eT - e0)
            rows.append(row)
            d = r["detail"].reset_index().rename(columns={"index": "sector"})
            d.insert(0, "period", row["period"]); d.insert(0, "iso3", iso)
            detail.append(d)
    out = pd.DataFrame(rows)
    det = pd.concat(detail, ignore_index=True) if detail else pd.DataFrame()
    return out, det


def main():
    va, emp, tot = load()
    results = {}
    for grid in ["A", "B"]:
        d = OUTPUT / f"grid_{grid}"
        d.mkdir(parents=True, exist_ok=True)
        main_, det = run(grid, va, emp, tot)
        r1, _ = run(grid, va, emp, tot, series="survey", survey_endpoints=True)
        r2, _ = run(grid, va, emp, tot, base="final")
        r3, _ = run(grid, va, emp, tot, drop=("MIU",))
        r4, det4 = run(grid, va, emp, tot, base="chained")
        r5, det5 = run(grid, va, emp, tot, base="final")
        det4.to_csv(d / "sectors_chained.csv", index=False)
        det5.to_csv(d / "sectors_final_prices.csv", index=False)
        for b in ("chained", "final"):
            run(grid, va, emp, tot, base=b, drop=("MIU",))[0].to_csv(d / f"robust_no_mining_{b}.csv", index=False)
        for name, df in [("main", main_), ("robust_survey", r1), ("robust_final_prices", r2),
                         ("robust_no_mining", r3), ("robust_chained", r4)]:
            df.to_csv(d / f"{name}.csv", index=False)
        det.to_csv(d / "sectors_main.csv", index=False)
        assert main_["check"].abs().max() < 1e-9, "decomposition does not add up"
        results[grid] = dict(main=main_, survey=r1, final=r2, nomin=r3, chained=r4, det=det)
    write_md(results)
    for g, r in results.items():
        print(f"\n=== Grid {g}")
        print(r["main"].pivot_table(index="iso3", columns="period", values="struct_pp").round(2))


def f(x, nd=2):
    return "—" if pd.isna(x) else f"{x:.{nd}f}"


def write_md(results):
    names = {"A": "Grid A — 7 sectors", "B": "Grid B — 5 sectors (services combined)"}
    L = [f"# {SCOPE_NAME} labour productivity: decomposition results (first pass)", "",
         "Generated by `empirics/code/lp/05_decompose.py`. Do not edit by hand. "
         "Method: see WP05 §2. Grids A and B are separate analyses (D-025); do not mix them.", "",
         "Terms are contributions to average annual labour-productivity growth, in percentage points per year "
         "(within + structural = growth). Grade: A = both period endpoints within "
         f"{ANCHOR_WINDOW} years of a usable survey year (interpreted); B = one endpoint (flagged); C = none (pure ILO model, not interpreted).", ""]
    for g, r in results.items():
        m = r["main"]
        L += [f"## {names[g]}", "", "### Main: modelled employment, initial-year prices", ""]
        for per in [f"{a}–{b}" for a, b in PERIODS]:
            x = m[m.period == per]
            if x.empty:
                continue
            L += [f"**{per}**", "",
                  "| Country | Grade | Growth | Within | Structural | of which static | dynamic | Employment growth (%/yr) | Official VA/worker growth |",
                  "|---|---|---|---|---|---|---|---|---|"]
            for _, row in x.sort_values(["grade", "country"]).iterrows():
                L.append(f"| {row['country']} | {row['grade']} | {f(row['growth_pp'])} | {f(row['within_pp'])} | "
                         f"**{f(row['struct_pp'])}** | {f(row['static_pp'])} | {f(row['dynamic_pp'])} | "
                         f"{f(row['emp_growth_pct'], 1)} | {f(row.get('official_growth_pp'))} |")
            L.append("")
        # robustness: structural term side by side
        L += ["### Robustness: structural-change term (pp/yr) across specifications", "",
              "Survey column uses the nearest usable survey years as endpoints (shown in brackets); grade-A country-periods only. "
              "Chained prices: one decomposition per year at previous-year prices, averaged over the period (D-032); "
              "its growth column is the mean annual growth rate, so it is not identical in definition to the linear "
              "average used by the fixed-base columns.", "",
              "| Country | Period | Grade | Main | Survey employment | Final-year prices | Chained prices | Excl. mining & utilities |",
              "|---|---|---|---|---|---|---|---|"]
        key = ["iso3", "period"]
        rob = m[key + ["country", "grade", "struct_pp"]]
        for nm, df in [("svy", r["survey"]), ("fin", r["final"]), ("chn", r["chained"]), ("nom", r["nomin"])]:
            if df.empty:
                rob[f"struct_{nm}"] = np.nan
                continue
            cols = key + ["struct_pp"] + (["t0", "T"] if nm == "svy" else [])
            rob = rob.merge(df[cols].rename(columns={"struct_pp": f"struct_{nm}", "t0": "s0", "T": "sT"}), on=key, how="left")
        for _, row in rob[rob.grade != "C"].sort_values(["period", "country"]).iterrows():
            sv = "—" if pd.isna(row.get("struct_svy")) else f"{row['struct_svy']:.2f} ({int(row['s0'])}–{int(row['sT'])})"
            L.append(f"| {row['country']} | {row['period']} | {row['grade']} | {f(row['struct_pp'])} | {sv} | "
                     f"{f(row.get('struct_fin'))} | {f(row.get('struct_chn'))} | {f(row.get('struct_nom'))} |")
        L.append("")
    (OUTPUT / "results.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
