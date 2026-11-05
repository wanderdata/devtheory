"""Extract the 16 countries from the raw world files into small, committed CSVs.

    python empirics/code/carib_lp/02_extract.py [extra raw files ...]

Looks in empirics/data/raw/carib_lp/ and in any paths given on the command
line. Files are recognised by content, not name, so the names the UN and ILO
sites give them (e.g. 'Download-GDPconstant-USD-countries.xlsx') work as-is.

Writes to empirics/data/interim/carib_lp/:
    un_va_k2020_usd.csv, un_va_cur_usd.csv     (long: iso3, indicator, target, year, value)
    ilo_emp_model.csv, ilo_emp_survey.csv     (ILO columns, 16 countries only)
    sources.csv                                (which raw file fed which output)
"""
import re
import sys
from pathlib import Path

import pandas as pd

from config import COUNTRIES, INTERIM, M49_TO_ISO3, RAW
from concordance import map_un_indicator

NAME_TO_ISO3 = {name.lower(): iso for iso, (_, name) in COUNTRIES.items()}
NAME_TO_ISO3.update({"bahamas, the": "BHS", "the bahamas": "BHS",
                     "st. kitts and nevis": "KNA", "st. lucia": "LCA",
                     "st. vincent and the grenadines": "VCT"})


# ---------------------------------------------------------------- UN AMA ----

def read_un_xlsx(path: Path):
    """Return (kind, long DataFrame) for a UN AMA 'GDP and its breakdown' workbook."""
    raw = pd.read_excel(path, header=None, dtype=object)
    head_text = " ".join(str(v) for v in raw.head(6).values.ravel() if pd.notna(v)).lower()
    if "constant" in head_text and "us dollar" in head_text:
        kind = "un_va_k2020_usd"
        base = re.search(r"constant (\d{4}) prices", head_text)
        if base and base.group(1) != "2020":
            print(f"  note: constant-price base year is {base.group(1)}, not 2020")
    elif "current" in head_text and "us dollar" in head_text:
        kind = "un_va_cur_usd"
    else:
        return None, None
    # header row = the row containing 'CountryID' (or 'Country' plus year cells)
    hdr = None
    for i in range(min(20, len(raw))):
        cells = [str(v).strip() for v in raw.iloc[i].tolist()]
        if "CountryID" in cells or ("Country" in cells and any(re.fullmatch(r"\d{4}(\.0)?", c) for c in cells)):
            hdr = i
            break
    if hdr is None:
        raise ValueError(f"{path.name}: could not find the header row")
    df = raw.iloc[hdr + 1:].copy()
    df.columns = [str(c).strip().replace(".0", "") for c in raw.iloc[hdr].tolist()]
    ind_col = next(c for c in df.columns if c.lower().startswith("indicator"))
    if "CountryID" in df.columns:
        df["iso3"] = pd.to_numeric(df["CountryID"], errors="coerce").map(M49_TO_ISO3)
    else:
        df["iso3"] = df["Country"].str.strip().str.lower().map(NAME_TO_ISO3)
    df = df[df["iso3"].notna()]
    years = [c for c in df.columns if re.fullmatch(r"\d{4}", c)]
    long = df.melt(id_vars=["iso3", ind_col], value_vars=years, var_name="year", value_name="value")
    long = long.rename(columns={ind_col: "indicator"})
    long["indicator"] = long["indicator"].astype(str).str.strip()
    long["target"] = long["indicator"].map(map_un_indicator)
    long["year"] = long["year"].astype(int)
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long = long[long["value"].notna()].sort_values(["iso3", "indicator", "year"])
    return kind, long[["iso3", "indicator", "target", "year", "value"]]


# ---------------------------------------------------------------- ILO -------

LABEL_SCHEMES = {
    "isic-rev.4": "ISIC4", "isic-rev.3.1": "ISIC3", "isic-rev.3": "ISIC3",
    "isic-rev.2": "ISIC2", "detailed": "DETAILS",
    "aggregate": "AGGREGATE", "broad sector": "SECTOR",
}


def label_to_code(label: str) -> str:
    """Convert an ILOSTAT explorer label such as
    'Economic activity (ISIC-Rev.4): A. Agriculture; forestry and fishing'
    to the bulk-file code 'ECO_ISIC4_A'. Unrecognised labels are returned unchanged."""
    s = str(label)
    if s.startswith("ECO_"):
        return s
    m = re.match(r"Economic activity \(([^)]+)\):\s*(.*)$", s)
    if not m:
        return s
    scheme = LABEL_SCHEMES.get(m.group(1).strip().lower())
    rest = m.group(2).strip()
    if scheme is None:
        return s
    if rest.lower().startswith("total"):
        return f"ECO_{scheme}_TOTAL"
    if rest.startswith("X.") or "not elsewhere classified" in rest.lower():
        return f"ECO_{scheme}_X"
    code = re.match(r"([A-Z0-9]+)\.", rest)
    if code:
        return f"ECO_{scheme}_{code.group(1)}"
    tag = re.search(r"~ISIC rev\.4 ([A-Z][A-Z;\s]*)", rest)  # detailed modelled labels, if present
    if tag:
        return f"ECO_{scheme}_" + re.sub(r"[;\s]", "", tag.group(1))
    return s


def read_ilo(path: Path):
    if path.suffix == ".rds":
        import pyreadr
        df = next(iter(pyreadr.read_r(str(path)).values()))
    else:
        df = pd.read_csv(path, dtype=str, low_memory=False)
    cols = {c: c.replace(".label", "") for c in df.columns}
    if "ref_area" not in df.columns and "ref_area.label" in df.columns:
        df = df.rename(columns=cols)
        df["ref_area"] = df["ref_area"].str.strip().str.lower().map(NAME_TO_ISO3)
    if "indicator" not in df.columns or "classif1" not in df.columns:
        return None, None
    ind = str(df["indicator"].dropna().iloc[0])
    if ind.startswith("EMP_2EMP") or "modelled" in ind.lower():
        kind = "ilo_emp_model"
    elif ind.startswith("EMP_TEMP") or "employment by sex and economic activity" in ind.lower():
        kind = "ilo_emp_survey"
    else:
        return None, None
    df = df[df["ref_area"].isin(COUNTRIES)].copy()
    df["classif1"] = df["classif1"].map(label_to_code)
    if "sex" in df.columns:
        df["sex"] = df["sex"].replace({"Total": "SEX_T", "Sex: Total": "SEX_T",
                                       "Male": "SEX_M", "Sex: Male": "SEX_M",
                                       "Female": "SEX_F", "Sex: Female": "SEX_F"})
    keep = [c for c in ["ref_area", "source", "indicator", "sex", "classif1", "time",
                        "obs_value", "obs_status", "note_classif", "note_indicator",
                        "note_source"] if c in df.columns]
    df = df[keep]
    df["obs_value"] = pd.to_numeric(df["obs_value"], errors="coerce")
    return kind, df.sort_values(["ref_area", "time", "classif1"])


# ---------------------------------------------------------------- main ------

def candidates(extra):
    paths = list(RAW.glob("*")) if RAW.exists() else []
    paths += [Path(p) for p in extra]
    return [p for p in paths if p.is_file()]


def main(extra):
    INTERIM.mkdir(parents=True, exist_ok=True)
    found = []
    for p in candidates(extra):
        name = p.name.lower()
        try:
            if name.endswith((".xlsx", ".xls")):
                kind, df = read_un_xlsx(p)
            elif name.endswith((".csv", ".csv.gz", ".rds")):
                kind, df = read_ilo(p)
            else:
                continue
        except Exception as e:
            print(f"[fail] {p.name}: {e}")
            continue
        if kind is None:
            print(f"[skip] {p.name}: not a recognised UN AMA or ILO file")
            continue
        out = INTERIM / f"{kind}.csv"
        df.to_csv(out, index=False)
        n_ctry = df.iloc[:, 0].nunique()
        print(f"[ok  ] {p.name} -> {out.name}: {len(df):,} rows, {n_ctry} countries")
        found.append({"output": out.name, "raw_file": p.name, "bytes": p.stat().st_size})
    log = INTERIM / "sources.csv"
    old = pd.read_csv(log) if log.exists() else pd.DataFrame(columns=["output"])
    new = pd.DataFrame(found, columns=["output", "raw_file", "bytes"])
    old = old[~old["output"].isin(new["output"])]
    pd.concat([old, new]).sort_values("output").to_csv(log, index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
