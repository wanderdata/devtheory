"""State GDP from INEGI's PIBE, base 2018, read directly from the committed source files
(empirics/data/source/inegi/, D-060).

    total:   GDP at market prices, millions of 2018 pesos, 1980-2024
             (conjunto_de_datos_piber_actividad_pib2024_r.csv; 1980-2002 retropolated by INEGI)
    oil:     gross value added of oil mining (SCIAN 211, 'Minería petrolera'), millions of 2018 pesos,
             2003-2024 (conjunto_de_datos_pibe_actividad_21p2024_r.csv)
    non_oil: total minus oil (constant-price values are additive)
"""
import unicodedata
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "empirics" / "data" / "source" / "inegi"
UNIT = "Millones de pesos a precios de 2018"
# INEGI state codes (ENT) and the names used in PIBE
STATES = {1: "Aguascalientes", 2: "Baja California", 3: "Baja California Sur", 4: "Campeche",
          5: "Coahuila de Zaragoza", 6: "Colima", 7: "Chiapas", 8: "Chihuahua", 9: "Ciudad de México",
          10: "Durango", 11: "Guanajuato", 12: "Guerrero", 13: "Hidalgo", 14: "Jalisco", 15: "México",
          16: "Michoacán de Ocampo", 17: "Morelos", 18: "Nayarit", 19: "Nuevo León", 20: "Oaxaca", 21: "Puebla",
          22: "Querétaro", 23: "Quintana Roo", 24: "San Luis Potosí", 25: "Sinaloa", 26: "Sonora", 27: "Tabasco",
          28: "Tamaulipas", 29: "Tlaxcala", 30: "Veracruz de Ignacio de la Llave", 31: "Yucatán", 32: "Zacatecas"}
SHORT = {1: "Ags", 2: "BC", 3: "BCS", 4: "Camp", 5: "Coah", 6: "Col", 7: "Chis", 8: "Chih", 9: "CDMX", 10: "Dgo",
         11: "Gto", 12: "Gro", 13: "Hgo", 14: "Jal", 15: "Méx", 16: "Mich", 17: "Mor", 18: "Nay", 19: "NL", 20: "Oax",
         21: "Pue", 22: "Qro", 23: "QRoo", 24: "SLP", 25: "Sin", 26: "Son", 27: "Tab", 28: "Tamps", 29: "Tlax",
         30: "Ver", 31: "Yuc", 32: "Zac"}


def _norm(s):
    return unicodedata.normalize("NFC", s).strip()


def _read(zipname, member):
    with zipfile.ZipFile(SRC / zipname) as z:
        d = pd.read_csv(z.open(f"conjunto_de_datos/{member}"), encoding="utf-8")
    d = d[d["Descriptores"].str.startswith(UNIT + "|")].copy()
    d["name"] = d["Descriptores"].str.split("|").str[-1].str.replace("<C1>", "", regex=False).map(_norm)
    code = {_norm(v): k for k, v in STATES.items()}
    d = d[d["name"].isin(code)]
    d["ent"] = d["name"].map(code)
    years = [c for c in d.columns if c[:4].isdigit()]
    long = d.melt(id_vars=["ent"], value_vars=years, var_name="year", value_name="value")
    long["year"] = long["year"].str[:4].astype(int)
    return long


def state_gdp():
    """Long table: ent, year, gdp (total), oil, non_oil, in millions of 2018 pesos."""
    tot = _read("conjunto_de_datos_piber_csv.zip", "conjunto_de_datos_piber_actividad_pib2024_r.csv")
    oil = _read("conjunto_de_datos_pibe_csv.zip", "conjunto_de_datos_pibe_actividad_21p2024_r.csv")
    g = tot.rename(columns={"value": "gdp"}).merge(oil.rename(columns={"value": "oil"}), on=["ent", "year"], how="left")
    g["non_oil"] = g["gdp"] - g["oil"]
    assert g["ent"].nunique() == 32, "PIBE: expected 32 states"
    return g.sort_values(["ent", "year"]).reset_index(drop=True)


if __name__ == "__main__":
    g = state_gdp()
    print(g[g["year"].isin([2005, 2012, 2019, 2024])].pivot(index="ent", columns="year", values="gdp").round(0).head())
    print(g.groupby("year")[["gdp", "oil"]].sum().loc[[2005, 2019, 2024]].round(0))
