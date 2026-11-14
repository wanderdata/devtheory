"""Reading INEGI's ENOE quarterly files (CSV version, zipped or not).

File names have changed over time (e.g. `sdemt419.csv` in older releases,
`ENOE_SDEMT123.csv` or `conjunto_de_datos_sdem_enoe_2023_1t.csv` in newer ones), so files are
found by table name and quarter tag rather than by an exact name. Column names are lowercased.
"""
import io
import re
import zipfile

import pandas as pd

from enoe_config import RAW

TABLES = {"sdem": "sdem", "coe1": "coe1", "hog": "hog", "viv": "viv"}


def tag(year, q):
    """INEGI's period tag, e.g. 2019 Q4 -> '419'."""
    return f"{q}{str(year)[2:]}"


def _match(name, table, year, q):
    """True if a file name is the given table for the given quarter. Accepts INEGI's naming
    patterns: a three-digit tag (`sdemt419.csv`, `ENOE_SDEMT419.csv`, `ENOEN_SDEMT123.csv`) or
    year and quarter (`conjunto_de_datos_sdem_enoe_2023_1t.csv`, `..._2023_trim1...`)."""
    n = name.lower()
    if table not in n or not n.endswith(".csv"):
        return False
    t = tag(year, q)
    if re.search(rf"(?<!\d){t}(?!\d)", n):
        return True
    return f"{year}_{q}t" in n or f"{year}_trim{q}" in n or f"{year}trim{q}" in n


def find(table, year, q, raw=RAW):
    """Return (zip path or None, member or file path) for one table and quarter."""
    for p in sorted(raw.glob("**/*")):
        if p.suffix.lower() == ".zip":
            with zipfile.ZipFile(p) as z:
                for m in z.namelist():
                    if _match(m.split("/")[-1], table, year, q):
                        return p, m
        elif p.suffix.lower() == ".csv" and _match(p.name, table, year, q):
            return None, p
    raise FileNotFoundError(f"ENOE table {table} for {year} Q{q} not found under {raw}")


def read(table, year, q, columns=None, raw=RAW):
    zp, member = find(table, year, q, raw)
    if zp is None:
        df = pd.read_csv(member, encoding="latin-1", low_memory=False)
    else:
        with zipfile.ZipFile(zp) as z, z.open(member) as f:
            df = pd.read_csv(io.BytesIO(f.read()), encoding="latin-1", low_memory=False)
    # Some INEGI files begin with a UTF-8 byte-order mark, which latin-1 decoding turns into "ï»¿"
    # at the start of the first column name.
    df.columns = [c.replace("\ufeff", "").replace("ï»¿", "").strip().lower() for c in df.columns]
    if columns:
        df = df[[c for c in columns if c in df.columns]]
    df["year"], df["q"] = year, q
    return df
