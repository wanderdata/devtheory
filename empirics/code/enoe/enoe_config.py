"""Settings for the ENOE job-ladder study (WP09; design in
papers/WP09_job_ladders_mexico/00_pre_analysis_plan.md, D-046).

ENOE microdata are not committed: put INEGI's quarterly zips (CSV version) in
empirics/data/raw/enoe/, unchanged. Only aggregate tables are written to empirics/output/enoe/.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RAW = ROOT / "empirics" / "data" / "raw" / "enoe"
INTERIM = ROOT / "empirics" / "data" / "raw" / "enoe_interim"   # linked microdata: never committed
OUTPUT = ROOT / "empirics" / "output" / "enoe"

# Two windows of five consecutive quarters (year, quarter); no window spans the 2020 break.
WINDOWS = {
    "pre": [(2018, 4), (2019, 1), (2019, 2), (2019, 3), (2019, 4)],
    "post": [(2023, 1), (2023, 2), (2023, 3), (2023, 4), (2024, 1)],
}

AGE_MIN, AGE_MAX = 16, 65            # Donovan, Lu & Schoellman benchmark; 15+ as a variant
MIN_CELL = 200                       # unweighted origin observations before merging a cell

# Person key across visits (with N_ENT rising by one between consecutive quarters). In the 2023
# files TIPO is part of the dwelling's identity: without it 10-13% of keys are duplicated by
# different households, and with it none are; TIPO changes between visits in 0.006% of links
# (checked on 2023Q2-Q3, D-047). It is added to the key whenever all quarters of a window have it.
# MES_CAL (calendar month) changes between visits and is not used.
KEY_OPTIONAL = ["tipo"]
KEY = ["cd_a", "ent", "con", "v_sel", "n_hog", "h_mud", "n_ren"]

# Firm size: INEGI's ambito2 (ENOEN file description, SDEMT field 66): 1 is the calculated
# subtotal of micro units (2 + 3); 2 without premises, 3 with premises, 4 small, 5 medium,
# 6 large establishments, 7 government, 8 other.
SIZE = {1: "micro, premises not specified", 2: "micro, no premises", 3: "micro, with premises", 4: "small",
        5: "medium", 6: "large", 7: "government", 8: "other or not specified"}

# Self-represented cities (urban sample): CD_A below 53; 53 and above is the urban complement and
# the rest of the country (ENOEN file description, VIVT field D_SEM).
URBAN_MAX_CD_A = 52
FORMAL = {1: "informal", 2: "formal"}
