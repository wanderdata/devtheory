"""Checks on the labour-productivity outputs: decomposition identities, price-base consistency,
and the documented scope of each output folder. They read committed outputs, so they are fast;
the rebuild-and-compare check (scripts/check_outputs.py) covers reproducibility."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
OUT = ROOT / "empirics" / "output"

from decompose import GRID_A, decompose, decompose_chained, va_at_prices  # noqa: E402

FILES = ["main", "robust_chained", "robust_final_prices", "robust_no_mining",
         "robust_no_mining_chained", "robust_no_mining_final", "robust_survey"]


@pytest.mark.parametrize("scope", ["carib_lp", "lac_lp"])
@pytest.mark.parametrize("grid", ["A", "B"])
@pytest.mark.parametrize("name", FILES)
def test_terms_add_up(scope, grid, name):
    d = pd.read_csv(OUT / scope / f"grid_{grid}" / f"{name}.csv")
    assert len(d)
    assert np.allclose(d["within_pp"] + d["struct_pp"], d["growth_pp"], atol=1e-9)
    assert np.allclose(d["static_pp"] + d["dynamic_pp"], d["struct_pp"], atol=1e-9)


@pytest.mark.parametrize("scope", ["carib_lp", "lac_lp"])
def test_grades_valid(scope):
    d = pd.read_csv(OUT / scope / "grid_A" / "main.csv")
    assert set(d["grade"]) <= {"A", "B", "C"}


def _toy():
    idx = pd.MultiIndex.from_product([["X"], [2000, 2001, 2002], ["AGR", "MAN"]], names=["iso3", "year", "sector"])
    va = pd.DataFrame({"va_cur_usd": [10, 30, 12, 33, 13, 40], "va_k2020usd": [10, 30, 11, 32, 12, 35]}, index=idx)
    emp = pd.Series([5, 5, 4.5, 5.5, 4, 6], index=idx)
    return va, emp


def test_chained_equals_fixed_for_one_year():
    va, emp = _toy()
    grid = {"AGR": "AGR", "MAN": "MAN"}
    a = decompose(va_at_prices(va, "X", 2000, 2001, "initial", grid), emp.loc[("X", 2000)], emp.loc[("X", 2001)], 1)
    b = decompose_chained(va, emp, "X", 2000, 2001, grid)
    for k in ["growth_pp", "within_pp", "struct_pp"]:
        assert a[k] == pytest.approx(b[k])


def test_chained_adds_up():
    va, emp = _toy()
    r = decompose_chained(va, emp, "X", 2000, 2002, {"AGR": "AGR", "MAN": "MAN"})
    assert r["within_pp"] + r["struct_pp"] == pytest.approx(r["growth_pp"])


def test_known_reference_numbers():
    """Published numbers that must not drift silently (WP05 D-024 table, WP06 §3.3)."""
    d = pd.read_csv(OUT / "carib_lp" / "grid_A" / "main.csv").set_index(["iso3", "period"])
    assert d.loc[("GUY", "2000–2019"), "struct_pp"] == pytest.approx(-3.06, abs=0.005)
    s = pd.read_csv(OUT / "lac_lp" / "summary" / "price_agreement.csv")
    s = s[(s["grid"] == "A") & s["grade"].isin(["A", "B"])]
    assert len(s) == 109
    assert (s["agreement"] == "sign depends on price base").sum() == 20
