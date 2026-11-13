"""Tests for study 9.3: the within-sector split preserves sector value added, follows relative
income with exponent theta, and the ladder's mean equals output per working-age person."""
import importlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "productivity_ladder"))
sys.path.insert(0, str(HERE.parents[0] / "lp"))

m = importlib.import_module("02_ladder")


def cells():
    return pd.DataFrame({"sector": ["MAN", "MAN", "TRH", "TRH"], "segment": ["MAN|formal", "MAN|informal", "TRH|formal", "TRH|informal"],
                         "formality": ["formal", "informal"] * 2, "emp": [60.0, 40.0, 30.0, 70.0],
                         "inc_mean": [10.0, 5.0, 8.0, 8.0], "pop15": 400.0})


@pytest.mark.parametrize("theta", [0.5, 1.0, 2.0])
def test_split_preserves_sector_value_added(theta):
    sec_y = pd.Series({"MAN": 1000.0, "TRH": 500.0})
    st = m.split(sec_y, cells(), theta)
    tot = (st["v"] * st["emp"]).groupby(st["sector"]).sum()
    assert tot["MAN"] == pytest.approx(1000.0) and tot["TRH"] == pytest.approx(500.0)
    man = st[st["sector"] == "MAN"].set_index("segment")["v"]
    assert man["MAN|formal"] / man["MAN|informal"] == pytest.approx(2.0 ** theta)
    trh = st[st["sector"] == "TRH"]["v"]
    assert trh.iloc[0] == pytest.approx(trh.iloc[1])        # equal incomes, equal values


def test_ladder_mean_is_output_per_working_age_person():
    sec_y = pd.Series({"MAN": 1000.0, "TRH": 500.0})
    st = m.split(sec_y, cells(), 1.0)
    d = m.ladder_of(st, 400.0)
    import ladder as lad
    assert lad.mean(d) == pytest.approx(1500.0 / 400.0)
