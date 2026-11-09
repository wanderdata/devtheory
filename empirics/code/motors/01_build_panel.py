"""Build the annual country data and the five-year panel for WP07.

Outputs (empirics/data/processed/motors/):
    annual.csv   country-year: PWT variables, sector shares, openness, schooling
    panel5.csv   country-period (start year t): growth t->t+5 and regressors at t
    countries.csv  country attributes: name, groups, temperate-zone instrument

Variables (D-037, D-038):
    GR       100 * (y_{t+5} / y_t - 1) / 5, y = PWT rgdpna / pop (S&V's definition, Maddison there)
    GR_O     the same with rgdpo / pop (robustness)
    RELUS    (rgdpo/pop) / (rgdpo/pop of the USA), same year, ratio
    MAN, AGR, MIU, CON, TRH, TSC, OTH, SER   value-added shares at current prices, % of total
             value added: UN AMA from 1970; GGDC 10-Sector before 1970 (national-currency shares)
    MAN_K    manufacturing share at constant 2020 prices (UN AMA), robustness
    EDU      average years of schooling, 15+, Barro-Lee v2.2 (1950-2010)
    EDU_HC   years of schooling implied by PWT's human-capital index (inverting PWT's
             Mincerian mapping), 1950-2023; used for the extension (consistent over time)
    LNPOP    log population (millions), PWT
    OPEN     exports + imports, % of GDP (UN AMA current US$); PWT shares before 1970
    UNDERVAL Rodrik's (2008) undervaluation index: residual of ln(1/pl_gdpo) on ln GDP per
             capita with year effects (positive = undervalued currency)
    TEMPERATE 1 if the country's geographic centroid lies outside the tropics (|latitude| >= 23.44);
             substitute for S&V's temperate-land share (OQ-48, D-038)
"""
import numpy as np
import pandas as pd

from config import (ADVANCED21, BARROLEE, COMMODITY_SHARE, GGDC10, ISO, LAC33, LAST_YEAR, LATLON,
                    MIN_POP_MILLIONS, PERIOD_STARTS, PROCESSED, PWT, UN_CUR, UN_FORMER, UN_K, UN_SECTORS)
from empirics.common.countries import CARIBBEAN16


def iso_table():
    t = pd.read_csv(ISO, keep_default_na=False)
    t["m49"] = t["country-code"].astype(int)
    return t


def load_un(path):
    d = pd.read_excel(path, header=2)
    yrs = [c for c in d.columns if str(c)[:2] in ("19", "20")]
    d = d[d["IndicatorName"].isin(list(UN_SECTORS) + ["Gross Domestic Product (GDP)",
                                                       "Exports of goods and services",
                                                       "Imports of goods and services"])]
    long = d.melt(id_vars=["CountryID", "IndicatorName"], value_vars=yrs, var_name="year", value_name="v")
    long["year"] = long["year"].astype(float).astype(int)
    w = long.pivot_table(index=["CountryID", "year"], columns="IndicatorName", values="v").reset_index()
    iso = iso_table().set_index("m49")["alpha-3"]
    w["iso3"] = w["CountryID"].map(iso)
    # former entities fill gaps of their successor
    former = w[w["CountryID"].isin(UN_FORMER)].assign(iso3=lambda x: x["CountryID"].map(UN_FORMER))
    cur = w.dropna(subset=["iso3"])
    cur = pd.concat([cur, former]).sort_values(["iso3", "year", "CountryID"])
    cur["is_former"] = cur["CountryID"].isin(UN_FORMER)
    # keep current entity where it has data, else former
    cur["has"] = cur["Total Value Added"].notna()
    cur = cur.sort_values(["iso3", "year", "has", "is_former"], ascending=[True, True, False, True])
    return cur.drop_duplicates(["iso3", "year"]).drop(columns=["has", "is_former", "CountryID"])


def un_shares():
    c = load_un(UN_CUR)
    k = load_un(UN_K)
    out = c[["iso3", "year"]].copy()
    tva = c["Total Value Added"]
    for name, short in UN_SECTORS.items():
        if short != "TVA":
            out[short] = 100 * c[name] / tva
    out["MIU"] = out["IND_CE"] - out["MAN"]
    # UN rows where C-E is smaller than D are internally inconsistent (e.g. Cabo Verde 1970s): missing
    out.loc[out["MIU"] < -0.05, "MIU"] = np.nan
    out["MIU"] = out["MIU"].clip(lower=0)
    out["SER"] = out["TRH"] + out["TSC"] + out["OTH"]
    out["OPEN"] = 100 * (c["Exports of goods and services"] + c["Imports of goods and services"]) / c["Gross Domestic Product (GDP)"]
    kk = k.set_index(["iso3", "year"])
    out = out.set_index(["iso3", "year"])
    out["MAN_K"] = 100 * kk["Manufacturing (ISIC D)"] / kk["Total Value Added"]
    out["VA_CUR_USD"] = c.set_index(["iso3", "year"])["Total Value Added"]
    out["SRC_SHARES"] = "UN AMA"
    return out.drop(columns=["IND_CE"]).reset_index()


def ggdc_shares():
    t = pd.read_excel(GGDC10, sheet_name="dataset")
    t.columns = [c.strip() for c in t.columns]
    va = t[t["Variable"] == "VA"].copy()
    va["iso3"] = va["Country"].str.replace("(alt)", "", regex=False).str.strip()
    va = va[~t.loc[va.index, "Country"].str.contains("alt")]
    va["iso3"] = va["iso3"].replace({"DEW": "DEU", "MOR": "MAR"})
    s = va["Summation of sector GDP"]
    o = pd.DataFrame({"iso3": va["iso3"], "year": va["Year"].astype(int)})
    o["AGR"] = 100 * va["Agriculture"] / s
    o["MAN"] = 100 * va["Manufacturing"] / s
    o["MIU"] = 100 * (va["Mining"] + va["Utilities"]) / s
    o["CON"] = 100 * va["Construction"] / s
    o["TRH"] = 100 * va["Trade, restaurants and hotels"] / s
    o["TSC"] = 100 * va["Transport, storage and communication"] / s
    o["OTH"] = 100 * (va["Finance, insurance, real estate and business services"] + va["Government services"]
                      + va["Community, social and personal services"]) / s
    o["SER"] = o["TRH"] + o["TSC"] + o["OTH"]
    o["SRC_SHARES"] = "GGDC 10-Sector"
    return o.dropna(subset=["MAN"])


def splice(gg, un, year=1970):
    """Ratio-splice GGDC 10-Sector shares (before `year`) to the UN AMA level in `year`, country by
    country and sector by sector, so the series do not jump where the source changes (D-038).
    Countries or sectors without an overlap value keep GGDC levels (flagged in SRC_SHARES)."""
    cols = ["AGR", "MAN", "MIU", "CON", "TRH", "TSC", "OTH"]
    u = un[un["year"] == year].set_index("iso3")[cols].astype(float)
    g = gg[gg["year"] == year].set_index("iso3")[cols].astype(float)
    u, g = u.align(g, join="inner")
    ratio = u / g.where(g > 0)
    out = gg[gg["year"] < year].copy()
    for c in cols:
        r = out["iso3"].map(ratio[c])
        out[c] = np.where(r.notna(), out[c] * r, out[c])
    tot = out[cols].sum(axis=1, min_count=len(cols))
    out[cols] = out[cols].mul(100 / tot, axis=0).where(tot.notna(), out[cols])   # keep shares adding to 100
    out["SER"] = out["TRH"] + out["TSC"] + out["OTH"]
    has = out["iso3"].isin(ratio.dropna(subset=["MAN"]).index)
    out["SRC_SHARES"] = np.where(has, "GGDC 10-Sector, spliced to UN 1970", "GGDC 10-Sector, unspliced")
    return out


def pwt():
    p = pd.read_excel(PWT, sheet_name="Data")
    p = p.rename(columns={"countrycode": "iso3"})
    keep = ["iso3", "country", "year", "rgdpna", "rgdpo", "pop", "hc", "pl_gdpo", "csh_x", "csh_m"]
    p = p[keep].copy()
    for k in keep[3:]:
        p[k] = pd.to_numeric(p[k], errors="coerce")
    p["y_na"] = p["rgdpna"] / p["pop"]
    p["y_o"] = p["rgdpo"] / p["pop"]
    us = p[p["iso3"] == "USA"].set_index("year")["y_o"]
    p["RELUS"] = p["y_o"] / p["year"].map(us)
    p["LNPOP"] = np.log(p["pop"])
    p["OPEN_PWT"] = 100 * (p["csh_x"].abs() + p["csh_m"].abs())
    # Rodrik (2008) undervaluation: ln RER = ln(1/pl_gdpo); regress on ln y with year effects
    d = p.dropna(subset=["pl_gdpo", "y_o"]).copy()
    d = d[(d["pl_gdpo"] > 0) & (d["y_o"] > 0)]
    d["lnrer"] = -np.log(d["pl_gdpo"])
    d["lny"] = np.log(d["y_o"])
    yd = pd.get_dummies(d["year"], prefix="y", drop_first=True, dtype=float)
    X = np.column_stack([np.ones(len(d)), d["lny"], yd.to_numpy()])
    b = np.linalg.lstsq(X, d["lnrer"].to_numpy(), rcond=None)[0]
    d["UNDERVAL"] = d["lnrer"] - X @ b
    p = p.merge(d[["iso3", "year", "UNDERVAL"]], on=["iso3", "year"], how="left")
    p["EDU_HC"] = hc_to_years(p["hc"])
    return p


def hc_to_years(hc):
    """Invert PWT's mapping hc = exp(phi(s)), phi piecewise linear with returns 13.4% (s<=4),
    10.1% (4<s<=8), 6.8% (s>8) (PWT documentation; Psacharopoulos 1994)."""
    lh = np.log(hc)
    a, b = 0.134 * 4, 0.134 * 4 + 0.101 * 4
    return np.where(lh <= a, lh / 0.134, np.where(lh <= b, 4 + (lh - a) / 0.101, 8 + (lh - b) / 0.068))


def barro_lee():
    b = pd.read_csv(BARROLEE)
    b = b[(b["agefrom"] == 15) & (b["ageto"] == 999)]
    return b.rename(columns={"WBcode": "iso3", "yr_sch": "EDU"})[["iso3", "year", "EDU"]]


def countries_table(annual):
    iso = iso_table()
    ll = pd.read_csv(LATLON, keep_default_na=False)
    ll = ll.merge(iso[["alpha-2", "alpha-3"]], left_on="country", right_on="alpha-2", how="left")
    lat = pd.to_numeric(ll.dropna(subset=["alpha-3"]).set_index("alpha-3")["latitude"], errors="coerce")
    c = annual.groupby("iso3").agg(country=("country", "first")).reset_index()
    c["latitude"] = c["iso3"].map(lat)
    c["TEMPERATE"] = (c["latitude"].abs() >= 23.44).astype(float)
    c.loc[c["latitude"].isna(), "TEMPERATE"] = np.nan
    c["advanced"] = c["iso3"].isin(ADVANCED21)
    c["lac"] = c["iso3"].isin(LAC33)
    c["caribbean"] = c["iso3"].isin(CARIBBEAN16)
    pop2000 = annual[annual["year"] == 2000].set_index("iso3")["pop"]
    c["pop2000"] = c["iso3"].map(pop2000)
    c["small"] = c["pop2000"] < MIN_POP_MILLIONS
    miu = annual.groupby("iso3")["MIU"].mean()
    c["commodity"] = c["iso3"].map(miu) >= COMMODITY_SHARE
    reg = iso.set_index("alpha-3")
    c["region"] = c["iso3"].map(reg["region"])
    c["subregion"] = c["iso3"].map(reg["sub-region"])
    return c


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    p = pwt()
    un = un_shares()
    gg = ggdc_shares()
    gg = splice(gg, un)                            # GGDC fills only the years before UN AMA starts
    shares = pd.concat([un, gg], ignore_index=True)
    a = p.merge(shares, on=["iso3", "year"], how="left").merge(barro_lee(), on=["iso3", "year"], how="left")
    a["OPEN"] = a["OPEN"].fillna(a["OPEN_PWT"])     # before 1970 (and gaps): PWT trade shares
    a = a[a["year"] <= LAST_YEAR]
    a.to_csv(PROCESSED / "annual.csv", index=False)

    c = countries_table(a)
    c.to_csv(PROCESSED / "countries.csv", index=False)

    for length, fname in [(5, "panel5.csv"), (10, "panel10.csv")]:
        build_periods(a, c, length).to_csv(PROCESSED / fname, index=False)
    panel = pd.read_csv(PROCESSED / "panel5.csv")
    v = panel.dropna(subset=["GR", "MAN", "RELUS", "EDU"])
    print(f"annual rows {len(a)}, countries {a['iso3'].nunique()}; panel rows {len(panel)}; "
          f"with GR, MAN, RELUS, EDU: {len(v)} obs, {v['iso3'].nunique()} countries")


def build_periods(a, c, length):
    starts = PERIOD_STARTS if length == 5 else list(range(1950, 2020, 10))
    rows = []
    idx = a.set_index(["iso3", "year"])
    reg = ["RELUS", "MAN", "AGR", "MIU", "CON", "TRH", "TSC", "OTH", "SER", "MAN_K", "EDU", "EDU_HC",
           "LNPOP", "OPEN", "UNDERVAL", "SRC_SHARES"]
    for iso3 in a["iso3"].unique():
        for t in starts:
            T = min(t + length, LAST_YEAR)
            try:
                y0, yT = idx.loc[(iso3, t)], idx.loc[(iso3, T)]
            except KeyError:
                continue
            n = T - t
            r = {"iso3": iso3, "period": t, "years": n,
                 "GR": 100 * (yT["y_na"] / y0["y_na"] - 1) / n,
                 "GR_O": 100 * (yT["y_o"] / y0["y_o"] - 1) / n}
            r.update({k: y0[k] for k in reg})
            rows.append(r)
    panel = pd.DataFrame(rows).merge(c[["iso3", "TEMPERATE", "advanced", "lac", "caribbean", "small", "commodity", "region"]],
                                     on="iso3", how="left")
    return panel.dropna(subset=["GR"])


if __name__ == "__main__":
    main()
