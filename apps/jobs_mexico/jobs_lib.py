"""Shared helpers for the Jobs in Mexico app (WP09). Displays precomputed outputs only."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apps.common.theme import (AUTHOR, C_CONTEXT, C_HIGHLIGHT, CATEGORICAL, INK, INK2, MUTED,  # noqa: E402,F401
                               base_layout, credit, show)

OUT = ROOT / "empirics" / "output" / "enoe"


@st.cache_data
def load(study, name):
    """Aggregate table `name` of study folder `study` (ladders, profiles); empty if absent."""
    f = OUT / study / f"{name}.csv"
    return pd.read_csv(f) if f.exists() else pd.DataFrame()


# ENOE sector groups (rama_est2).
SECTORS = {"0": "Not specified", "1": "Agriculture, forestry, fishing", "2": "Mining and electricity",
           "3": "Manufacturing", "4": "Construction", "5": "Commerce", "6": "Restaurants and accommodation",
           "7": "Transport and communications", "8": "Professional, financial and corporate services",
           "9": "Social services", "10": "Other services", "11": "Government"}

SOURCE = "Source: INEGI, Encuesta Nacional de Ocupación y Empleo (ENOE), quarterly microdata."


# Fixed colours for job types, used on every page.
TYPE_COLORS = {"all (baseline)": INK2, "formal": C_HIGHLIGHT, "informal": "#eb6834"}


def footer(extra=""):
    credit(SOURCE + (" " + extra if extra else ""))
