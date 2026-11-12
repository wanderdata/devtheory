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

# Person key across visits (with N_ENT rising by one between consecutive quarters).
KEY = ["cd_a", "ent", "con", "v_sel", "n_hog", "h_mud", "n_ren"]

# Firm size: INEGI's ambito2 (codes to be verified against the file description, OQ-63).
SIZE = {1: "micro, no premises", 2: "micro, no premises", 3: "micro, with premises", 4: "small",
        5: "medium", 6: "large", 7: "government", 8: "other or not specified"}
FORMAL = {1: "informal", 2: "formal"}
