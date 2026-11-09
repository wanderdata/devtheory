"""Settings for the development-motors project (WP07).

    python empirics/code/motors/run_all.py

Design and tests are fixed in papers/WP07_development_motors/00_literature_and_plan.md (D-037).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from empirics.common.countries import CARIBBEAN16, LAC33  # noqa: E402,F401

SOURCE = ROOT / "empirics" / "data" / "source"
PROCESSED = ROOT / "empirics" / "data" / "processed" / "motors"
OUTPUT = ROOT / "empirics" / "output" / "motors"

PWT = SOURCE / "pwt" / "pwt110.xlsx"
UN_CUR = SOURCE / "un_ama" / "un_ama_gdp_breakdown_current_usd.xlsx"
UN_K = SOURCE / "un_ama" / "un_ama_gdp_breakdown_constant2020_usd.xlsx"
GGDC10 = SOURCE / "ggdc" / "10sd_jan15_2014.xlsx"
ETD = SOURCE / "ggdc" / "ETD_230918.xlsx"
BARROLEE = SOURCE / "barrolee" / "BL2013_MF1599_v2.2.csv"
ISO = SOURCE / "reference" / "iso3166_lukes_all.csv"
LATLON = SOURCE / "reference" / "google_dspl_countries.csv"

# Five-year periods: growth from t to t+5, regressors at t (S&V). 2020-23 is short and is kept
# only as a flagged final period, never in the main estimates.
PERIOD_STARTS = list(range(1950, 2020, 5))
LAST_YEAR = 2023

# Subperiods (S&V: 1950-70, 1970-90, 1990-2005; extension adds 2005-20). Keyed by period start.
SUBPERIODS_SV = {"1950–70": range(1950, 1970), "1970–90": range(1970, 1990), "1990–2005": range(1990, 2005)}
SUBPERIODS_EXT = {**SUBPERIODS_SV, "2005–20": range(2005, 2020)}

# The 21 advanced economies (long-standing OECD members), as S&V's split of 21 advanced and
# 67 developing countries implies; S&V do not list theirs.
ADVANCED21 = ["AUS", "AUT", "BEL", "CAN", "CHE", "DEU", "DNK", "ESP", "FIN", "FRA", "GBR", "GRC",
              "IRL", "ITA", "JPN", "NLD", "NOR", "NZL", "PRT", "SWE", "USA"]

# Former centrally planned economies (Eastern Europe, former USSR, Mongolia, former Yugoslavia):
# current-price sector shares under planned prices are not comparable, and their 1990s
# transition collapse is a different phenomenon; S&V note they are under-represented (D-039).
FORMER_PLANNED = ["ALB", "ARM", "AZE", "BGR", "BIH", "BLR", "CZE", "EST", "GEO", "HRV", "HUN", "KAZ",
                  "KGZ", "LTU", "LVA", "MDA", "MKD", "MNE", "MNG", "POL", "ROU", "RUS", "SRB", "SVK",
                  "SVN", "TJK", "TKM", "UKR", "UZB"]

# Estimation samples (D-037 pre-specified: main, developing; D-039 post hoc after replication:
# excl_cpe, core). Verdicts in WP07 require agreement between main and core.
SAMPLES = {
    "main": "Population of at least 1 million in 2000 (pre-specified)",
    "excl_cpe": "Main, without former centrally planned economies",
    "core": "Main, without former centrally planned economies and commodity exporters",
    "developing": "Core, without the 21 advanced economies",
}

MIN_POP_MILLIONS = 1.0       # main sample: population of at least 1 million in 2000 (S&V-like)
COMMODITY_SHARE = 20.0       # mining & utilities share of value added (%, country mean) marking commodity exporters

# UN AMA rows -> short names (current-price shares of total value added)
UN_SECTORS = {
    "Agriculture, hunting, forestry, fishing (ISIC A-B)": "AGR",
    "Mining, Manufacturing, Utilities (ISIC C-E)": "IND_CE",
    "Manufacturing (ISIC D)": "MAN",
    "Construction (ISIC F)": "CON",
    "Wholesale, retail trade, restaurants and hotels (ISIC G-H)": "TRH",
    "Transport, storage and communication (ISIC I)": "TSC",
    "Other Activities (ISIC J-P)": "OTH",
    "Total Value Added": "TVA",
}
SECTOR_LABELS = {
    "MAN": "Manufacturing", "AGR": "Agriculture", "MIU": "Mining & utilities", "CON": "Construction",
    "TRH": "Trade, restaurants & hotels", "TSC": "Transport, storage & communications",
    "OTH": "Other services (finance, business, government, personal)", "SER": "All services",
}
# Former UN entities whose series fill the current country's gaps
UN_FORMER = {230: "ETH", 736: "SDN", 835: "TZA"}

# ETD sectors (12) -> short names
ETD_SECTORS = {"Agriculture": "AGR", "Mining": "MIN", "Manufacturing": "MAN", "Utilities": "UTL",
               "Construction": "CON", "Trade services": "TRD", "Transport services": "TRA",
               "Business services": "BUS", "Financial services": "FIN", "Real estate": "RES",
               "Government services": "GOV", "Other services": "OSV"}
ETD_LABELS = {"MAN": "Manufacturing", "BUS": "Business services", "FIN": "Financial services",
              "TRD": "Trade services", "TRA": "Transport services", "RES": "Real estate",
              "GOV": "Government services", "OSV": "Other services", "CON": "Construction",
              "AGR": "Agriculture", "MIN": "Mining", "UTL": "Utilities"}
