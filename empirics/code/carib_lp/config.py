"""Shared settings for the sectoral labour-productivity pipeline.

The pipeline runs for one country scope at a time, chosen with the
environment variable LP_SCOPE (default "carib"):

    carib  (D-019) the 16 member countries served by the ECLAC subregional
           headquarters for the Caribbean (Port of Spain), as listed at
           https://caribbean.eclac.org/about (checked 2026-11-05).
           Outputs in .../carib_lp/.
    lac    (D-030) the 33 Latin American and Caribbean member States of ECLAC,
           as listed at https://www.cepal.org/en/about/member-states-and-associate-members
           (checked 2026-11-09). Outputs in .../lac_lp/.

    LP_SCOPE=lac python empirics/code/carib_lp/03_build_panel.py
"""
import os
from pathlib import Path

SCOPE = os.environ.get("LP_SCOPE", "carib").lower()
if SCOPE not in ("carib", "lac"):
    raise SystemExit(f"LP_SCOPE must be 'carib' or 'lac', not {SCOPE!r}")
TAG = f"{SCOPE}_lp"
SCOPE_NAME = {"carib": "Caribbean", "lac": "Latin America and the Caribbean"}[SCOPE]

ROOT = Path(__file__).resolve().parents[3]          # repo root
RAW = ROOT / "empirics" / "data" / "raw" / TAG                  # not committed
SOURCE = ROOT / "empirics" / "data" / "source"                  # committed world files (D-029)
INTERIM = ROOT / "empirics" / "data" / "interim" / TAG          # committed, scope countries only
PROCESSED = ROOT / "empirics" / "data" / "processed" / TAG
OUTPUT = ROOT / "empirics" / "output" / TAG

# ISO3 -> (UN M49 numeric code, display name)
CARIBBEAN = {
    "ATG": (28, "Antigua and Barbuda"),
    "BHS": (44, "Bahamas"),
    "BRB": (52, "Barbados"),
    "BLZ": (84, "Belize"),
    "CUB": (192, "Cuba"),
    "DMA": (212, "Dominica"),
    "DOM": (214, "Dominican Republic"),
    "GRD": (308, "Grenada"),
    "GUY": (328, "Guyana"),
    "HTI": (332, "Haiti"),
    "JAM": (388, "Jamaica"),
    "KNA": (659, "Saint Kitts and Nevis"),
    "LCA": (662, "Saint Lucia"),
    "VCT": (670, "Saint Vincent and the Grenadines"),
    "SUR": (740, "Suriname"),
    "TTO": (780, "Trinidad and Tobago"),
}
LATIN_AMERICA_ADDED = {   # the 17 ECLAC member States not in the Caribbean scope
    "ARG": (32, "Argentina"),
    "BOL": (68, "Bolivia (Plurinational State of)"),
    "BRA": (76, "Brazil"),
    "CHL": (152, "Chile"),
    "COL": (170, "Colombia"),
    "CRI": (188, "Costa Rica"),
    "ECU": (218, "Ecuador"),
    "SLV": (222, "El Salvador"),
    "GTM": (320, "Guatemala"),
    "HND": (340, "Honduras"),
    "MEX": (484, "Mexico"),
    "NIC": (558, "Nicaragua"),
    "PAN": (591, "Panama"),
    "PRY": (600, "Paraguay"),
    "PER": (604, "Peru"),
    "URY": (858, "Uruguay"),
    "VEN": (862, "Venezuela (Bolivarian Republic of)"),
}
if SCOPE == "carib":
    COUNTRIES = dict(CARIBBEAN)
else:
    COUNTRIES = dict(sorted({**CARIBBEAN, **LATIN_AMERICA_ADDED}.items()))
M49_TO_ISO3 = {m49: iso for iso, (m49, _) in COUNTRIES.items()}

# Target sectors: the seven groupings of the UN National Accounts Main
# Aggregates Database (ISIC Rev.3 letters), with mining+utilities derived as
# (ISIC C-E) minus manufacturing (ISIC D).
SECTORS = {
    "AGR": "Agriculture, forestry, fishing",
    "MIU": "Mining and utilities",
    "MAN": "Manufacturing",
    "CON": "Construction",
    "TRH": "Trade, restaurants and hotels",
    "TSC": "Transport, storage and communication",
    "OTH": "Other services (finance, business, government, personal)",
}
SECTOR_ORDER = list(SECTORS)

# Expected raw files (names as saved in RAW; the extract step also accepts
# the names the sites give them, see 02_extract.py).
SOURCES = {
    "un_va_k2020_usd": {
        "url": "https://unstats.un.org/unsd/amaapi/api/file/6",
        "file": "un_ama_gdp_breakdown_constant2020_usd.xlsx",
        "what": "UNSD AMA, GDP and its breakdown at constant 2020 prices in US dollars",
    },
    "un_va_cur_usd": {
        "url": "https://unstats.un.org/unsd/amaapi/api/file/2",
        "file": "un_ama_gdp_breakdown_current_usd.xlsx",
        "what": "UNSD AMA, GDP and its breakdown at current prices in US dollars",
    },
    "ilo_emp_model": {
        "url": "https://rplumber.ilo.org/files/indicator/EMP_2EMP_SEX_ECO_NB_A.csv.gz",
        "file": "EMP_2EMP_SEX_ECO_NB_A.csv.gz",
        "what": "ILOSTAT, employment by sex and economic activity, ILO modelled estimates (thousands)",
    },
    "ilo_emp_survey": {
        "url": "https://rplumber.ilo.org/files/indicator/EMP_TEMP_SEX_ECO_NB_A.csv.gz",
        "file": "EMP_TEMP_SEX_ECO_NB_A.csv.gz",
        "what": "ILOSTAT, employment by sex and economic activity, national sources (thousands)",
    },
}
