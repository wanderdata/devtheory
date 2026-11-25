"""Settings for the figures of the Caribbean productive development policy report (D-072).

    python empirics/code/carib_pdp/run_all.py

The report ("Productive Development Policy in the Caribbean", draft narrative, October 2026)
is kept outside the repository. This project builds the data, Excel charts and SVG figures
for the graphs that can be filled with data in hand, from the outputs of the labour-
productivity pipeline (empirics/code/lp, Caribbean scope) and from counts cited in the draft.
"""
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from empirics.common.countries import CARIBBEAN16, OFFICIAL, POOL_EXCLUDE_LAC, SHORT  # noqa: E402,F401

HERE = Path(__file__).resolve().parent
LP = ROOT / "empirics" / "code" / "lp"
LP_OUT = ROOT / "empirics" / "output" / "carib_lp"
LP_PANEL = ROOT / "empirics" / "data" / "processed" / "carib_lp" / "panel_7sector.csv"
INPUTS = HERE / "inputs"
OUTPUT = ROOT / "empirics" / "output" / "carib_pdp"
DATA = OUTPUT / "data"

# Production types of the report (section 3.1), as decided with the author (D-072).
# Antigua and Barbuda, Dominica, Grenada and Saint Kitts and Nevis belong to the tourism type
# but have no sector employment series, so they do not appear in the productivity figures.
TYPES = {
    "Resource and energy economies": ["GUY", "SUR", "TTO"],
    "Tourism and services economies": ["BHS", "BRB", "LCA", "VCT", "ATG", "DMA", "GRD", "KNA"],
    "Mixed economies": ["JAM", "BLZ"],
    "Other Caribbean economies": ["DOM", "HTI", "CUB"],
}
TYPE_SHORT = {"Resource and energy economies": "Resource and energy",
              "Tourism and services economies": "Tourism and services",
              "Mixed economies": "Mixed", "Other Caribbean economies": "Other Caribbean"}
TYPE_OF = {iso: t for t, members in TYPES.items() for iso in members}
assert sorted(TYPE_OF) == sorted(CARIBBEAN16)

# Cuba's US$ levels are not comparable (D-033): shown by country, never pooled.
NO_POOL = set(POOL_EXCLUDE_LAC)

PERIODS = [(2000, 2019), (2019, 2024)]
LATEST = 2024
SECTOR_LABEL = {"AGR": "Agriculture, forestry and fishing", "MIU": "Mining and utilities",
                "MAN": "Manufacturing", "CON": "Construction",
                "TRH": "Trade, restaurants and hotels", "TSC": "Transport, storage and communications",
                "OTH": "Other services"}
SECTORS = list(SECTOR_LABEL)


def load_lp(name):
    """Load a module of the lp pipeline by file path (Caribbean scope).

    The lp modules import their own config.py; this project has one too, so the lp
    directory is put first on sys.path and any cached 'config' module is set aside
    while the module loads, then restored.
    """
    os.environ["LP_SCOPE"] = "carib"
    saved = sys.modules.pop("config", None)
    sys.path.insert(0, str(LP))
    try:
        spec = importlib.util.spec_from_file_location(f"lp_{name}", LP / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(LP))
        sys.modules.pop("config", None)
        if saved is not None:
            sys.modules["config"] = saved
    return mod
