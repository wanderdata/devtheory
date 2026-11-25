"""Chart specifications for graphs 2, 4 and 5, built from the generated data."""
import pandas as pd

from charts import Spec
from config import DATA, TYPE_SHORT, TYPES

SECTOR_SHORT = {"AGR": "Agriculture", "MIU": "Mining and utilities", "MAN": "Manufacturing",
                "CON": "Construction", "TRH": "Trade, restaurants and hotels",
                "TSC": "Transport and communications", "OTH": "Other services"}


def build_specs():
    s2 = pd.read_csv(DATA / "g2_sectors_types.csv")
    cats = list(SECTOR_SHORT.values())
    share = {TYPE_SHORT[t]: s2[s2["type"] == t].set_index("sector").loc[list(SECTOR_SHORT), "emp_share_pct"].round(1).tolist()
             for t in TYPES}
    rel = {TYPE_SHORT[t]: s2[s2["type"] == t].set_index("sector").loc[list(SECTOR_SHORT), "rel_lp"].round(2).tolist()
           for t in TYPES}
    g4 = pd.read_csv(DATA / "g4_clusters.csv")
    g5 = pd.read_csv(DATA / "g5_sti.csv")
    return {
        "graph2a": Spec("graph2a", cats, share, number_format="0", cell_format="0.0", axis_min=0, axis_max=50, major_unit=10,
                        height_in=3.4, gap=40),
        "graph2b": Spec("graph2b", cats, rel, number_format="General", log=True, axis_min=0.1, axis_max=10,
                        height_in=3.4, gap=40),
        "graph4": Spec("graph4", g4["name"].tolist(), {"Initiatives": g4["count"].tolist()}, number_format="0",
                       axis_min=0, axis_max=4, major_unit=1, data_labels=True, legend=False, height_in=2.7),
        "graph5": Spec("graph5", g5["name"].tolist(), {"Instruments": g5["count"].tolist()}, number_format="0",
                       axis_min=0, axis_max=14, major_unit=2, data_labels=True, legend=False, height_in=2.7),
    }
