"""Shared settings for the sectoral labour-productivity pipeline (empirics/code/lp).

The pipeline runs for one country scope at a time, chosen with the
environment variable LP_SCOPE (default "carib"):

    carib  (D-019) the 16 member countries served by the ECLAC subregional
           headquarters for the Caribbean (Port of Spain). Outputs in .../carib_lp/.
    lac    (D-030) the 33 Latin American and Caribbean member States of ECLAC.
           Outputs in .../lac_lp/.

    LP_SCOPE=lac python empirics/code/lp/03_build_panel.py
    python empirics/code/lp/run_all.py          # every step, both scopes

Country lists and names come from empirics/common/countries.py.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # repo root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from empirics.common.countries import CARIBBEAN16, LAC33, M49, OFFICIAL, SCOPES  # noqa: E402

SCOPE = os.environ.get("LP_SCOPE", "carib").lower()
if SCOPE not in SCOPES:
    raise SystemExit(f"LP_SCOPE must be one of {sorted(SCOPES)}, not {SCOPE!r}")
TAG = SCOPES[SCOPE]["tag"]
SCOPE_NAME = SCOPES[SCOPE]["label"]

RAW = ROOT / "empirics" / "data" / "raw" / TAG                  # not committed
SOURCE = ROOT / "empirics" / "data" / "source"                  # committed world files (D-029)
INTERIM = ROOT / "empirics" / "data" / "interim" / TAG          # committed, scope countries only
PROCESSED = ROOT / "empirics" / "data" / "processed" / TAG
OUTPUT = ROOT / "empirics" / "output" / TAG

# ISO3 -> (UN M49 numeric code, official name); order fixes the order of report rows.
_order = CARIBBEAN16 if SCOPE == "carib" else LAC33
COUNTRIES = {iso: (M49[iso], OFFICIAL[iso]) for iso in _order}
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
