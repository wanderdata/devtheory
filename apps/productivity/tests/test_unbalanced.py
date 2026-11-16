"""Tests of the explainer's three-sector model (apps/productivity/unbalanced.py): the
identities the theory note relies on hold numerically."""
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unbalanced import PRESETS, Params, aggregate, baumol_slope, decompose, solve  # noqa: E402

BAUMOL = PRESETS["Baumol: one wage, no markups"]


@pytest.mark.parametrize("p", list(PRESETS.values()))
def test_shares_sum_to_one(p):
    df = solve(p)
    sums = df.groupby("t")[["s", "l"]].sum()
    assert np.allclose(sums, 1.0)


@pytest.mark.parametrize("p", list(PRESETS.values()))
@pytest.mark.parametrize("prices", ["chained", "fixed"])
def test_decomposition_adds_up(p, prices):
    d = decompose(solve(p), prices)
    assert np.allclose(d["within"] + d["static"] + d["dynamic"], d["total"])


def test_baumol_labour_moves_to_slow_sector_and_growth_slows():
    df = solve(BAUMOL)
    lS = df[df.sector == "S"].sort_values("t")["l"].to_numpy()
    assert np.all(np.diff(lS) > 0)
    d = decompose(df, "chained")
    assert d["total"].iloc[-1] < d["total"].iloc[0]
    # aggregate growth stays above the slowest sector's rate and below the fastest
    assert (d["total"] > 100 * BAUMOL.g_S).all() and (d["total"] < 100 * (np.exp(BAUMOL.g_P) - 1)).all()


def test_baumol_static_term_is_zero_at_chained_prices():
    # one wage and no markups: nominal value added per worker is equal across sectors
    d = decompose(solve(BAUMOL), "chained")
    assert np.allclose(d["static"], 0.0, atol=1e-12)
    assert (d["dynamic"] < 0).all()


def test_fixed_prices_show_negative_structural_change_in_baumol_case():
    d = decompose(solve(BAUMOL), "fixed")
    assert (d["static"].iloc[10:] < 0).all()


def test_unit_elasticity_keeps_shares_constant():
    df = solve(replace(BAUMOL, eps=1.0))
    assert np.allclose(df.groupby("sector")["s"].std(), 0.0)


@pytest.mark.parametrize("phi", [0.0, 0.3, 0.5, 0.8])
def test_slope_equals_minus_one_plus_passthrough(phi):
    assert baumol_slope(solve(replace(BAUMOL, phi=phi))).attrs["slope"] == pytest.approx(-(1 - phi), abs=1e-10)


def test_rising_markup_in_slow_sector_steepens_slope():
    # R grows slower than average, so a rising R markup is negatively correlated with productivity growth:
    # the relative price of R rises by more than its productivity gap predicts and the slope falls below -1
    s0 = baumol_slope(solve(BAUMOL)).attrs["slope"]
    s1 = baumol_slope(solve(replace(BAUMOL, m=0.01))).attrs["slope"]
    assert s1 < s0


def test_informal_wage_gap_makes_static_term_negative():
    d = decompose(solve(replace(BAUMOL, rho=0.45)), "chained")
    assert (d["static"] < 0).all()


def test_aggregate_index_and_deflator():
    ag = aggregate(solve(BAUMOL))
    assert ag["real_lp"].iloc[0] == 1.0 and ag["deflator"].iloc[0] == pytest.approx(1.0)
    assert (np.diff(ag["real_lp"]) > 0).all()
