"""Checks on output per working-age person, the productivity ladders (08_ladder.py) and the
relative-price split (09_baumol.py): the dominance functions on cases with known answers,
accounting identities on the committed outputs, and reference results (D-042, D-043)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
OUT = ROOT / "empirics" / "output"

import ladder as lad  # noqa: E402

SCOPES = ["carib_lp", "lac_lp"]


# ------------------------------------------------- dominance, synthetic ---

def test_uniform_shift_is_first_order():
    a = lad.make([0, 10, 20], [0.4, 0.4, 0.2])
    b = lad.make([0, 12, 25], [0.4, 0.4, 0.2])
    assert lad.dominance(a, b, 1) == 1 and lad.dominance(b, a, 1) == -1
    assert lad.dominance(a, b, 2) == 1
    assert lad.share_gained(a, b) == pytest.approx(1.0)


def test_smaller_zero_block_is_first_order():
    a = lad.make([0, 10], [0.5, 0.5])
    b = lad.make([0, 10], [0.4, 0.6])
    assert lad.dominance(a, b, 1) == 1


def test_gain_at_bottom_loss_at_top_same_mean_is_second_order_only():
    a = lad.make([0, 10, 30], [0.4, 0.4, 0.2])       # mean 10
    b = lad.make([0, 12, 26], [0.4, 0.4, 0.2])       # mean 10: middle gains, top loses
    assert lad.mean(a) == pytest.approx(lad.mean(b))
    assert lad.dominance(a, b, 1) == 0
    assert lad.dominance(a, b, 2) == 1


def test_crossing_with_higher_mean_is_ambiguous():
    a = lad.make([0, 10, 20], [0.4, 0.4, 0.2])
    b = lad.make([0, 8, 40], [0.4, 0.4, 0.2])        # top gains a lot, middle loses
    assert lad.mean(b) > lad.mean(a)
    assert lad.dominance(a, b, 1) == 0 and lad.dominance(a, b, 2) == 0


def test_identical_is_no_change():
    a = lad.make([0, 10], [0.3, 0.7])
    assert lad.dominance(a, a, 1) == 0 and lad.dominance(a, a, 2) == 0


def test_incidence_averages_to_mean_growth():
    a = lad.make([0, 10, 20], [0.35, 0.45, 0.2])
    b = lad.make([0, 11, 26], [0.30, 0.48, 0.22])
    _, inc = lad.incidence(a, b, 10, grid=(np.arange(100000) + 0.5) / 100000)
    assert inc.mean() == pytest.approx((lad.mean(b) / lad.mean(a) - 1) / 10 * 100, abs=1e-3)


def test_fgt():
    d = lad.make([0, 5, 20], [0.5, 0.3, 0.2])
    assert lad.fgt(d, 10, 0) == pytest.approx(0.8)
    assert lad.fgt(d, 10, 1) == pytest.approx(0.5 * 1 + 0.3 * 0.5)
    assert lad.fgt(d, 10, 2) == pytest.approx(0.5 * 1 + 0.3 * 0.25)


# ------------------------------------------------- committed outputs ---

@pytest.mark.parametrize("scope", SCOPES)
def test_terms_add_up(scope):
    t = pd.read_csv(OUT / scope / "ladder" / "terms.csv")
    assert len(t)
    assert np.allclose(t["within_pp"] + t["struct_pp"], t["prod_pp"], atol=1e-9)
    assert np.allclose(t["prod_pp"] + t["emprate_pp"], t["ypw_pp"], atol=1e-9)
    # log growth of Y/W matches the levels
    lv = 100 * np.log(t["ypwT"] / t["ypw0"]) / (t["T"] - t["t0"])
    assert np.allclose(lv, t["ypw_pp"], atol=1e-9)


@pytest.mark.parametrize("scope", SCOPES)
def test_ladders_are_distributions_with_the_right_mean(scope):
    lr = pd.read_csv(OUT / scope / "ladder" / "ladders.csv")
    g = lr.groupby(["iso3", "period", "year", "base"])
    assert np.allclose(g["weight"].sum(), 1.0, atol=1e-12)
    assert (lr["weight"] >= -1e-12).all()
    t = pd.read_csv(OUT / scope / "ladder" / "terms.csv").set_index(["iso3", "period"])
    area = (lr.assign(a=lr["value"] * lr["weight"])[lr["base"] == "initial"]
            .groupby(["iso3", "period", "year"])["a"].sum())
    for (iso, per, yr), a in area.items():
        r = t.loc[(iso, per)]
        assert a == pytest.approx(r["ypw0"] if yr == r["t0"] else r["ypwT"], rel=1e-9)


@pytest.mark.parametrize("scope", SCOPES)
def test_verdicts_consistent(scope):
    v = pd.read_csv(OUT / scope / "ladder" / "verdicts.csv")
    assert set(v["fsd"]) <= {-1, 0, 1} and set(v["ssd"]) <= {-1, 0, 1}
    assert not ((v["fsd"] == 1) & (v["ssd"] == -1)).any()       # first order implies second order
    assert ((v["fsd"] != 1) | (v["share_gained"] > 1 - 1e-9)).all()
    assert v.groupby(["iso3", "period"])["verdict"].nunique().max() == 1


@pytest.mark.parametrize("scope", SCOPES)
def test_baumol_identity(scope):
    d = pd.read_csv(OUT / scope / "baumol" / "sectors.csv")
    assert np.allclose(d["d_real_pp"] + d["d_price_pp"], d["d_nom_pp"], atol=1e-9)


# ------------------------------------------------- reference results ---
# Changing any of these is a decision (CLAUDE.md): log it and update the value here.

def test_reference_lac():
    h = pd.read_csv(OUT / "lac_lp" / "ladder" / "horizon.csv").set_index(["sample", "horizon"])
    assert h.loc[("all countries", 1), "share_emprate_larger"] == pytest.approx(0.3427, abs=5e-4)
    assert h.loc[("all countries", 20), "emprate_variance_share"] == pytest.approx(0.0778, abs=5e-4)
    v = pd.read_csv(OUT / "lac_lp" / "ladder" / "verdicts.csv")
    v = v[(v["period"] == "2000–2019") & (v["base"] == "initial")].set_index("iso3")["verdict"]
    assert v["CHL"] == "improvement"
    assert v["MEX"] == "ambiguous"
    assert v["URY"] == "depends on prices"
    t = pd.read_csv(OUT / "lac_lp" / "ladder" / "terms.csv").set_index(["iso3", "period"])
    assert t.loc[("MEX", "2000–2019"), "ypw_pp"] == pytest.approx(-0.2151, abs=5e-4)
    s = pd.read_csv(OUT / "lac_lp" / "baumol" / "slope.csv").set_index("period")
    assert s.loc["2000–2019", "slope"] == pytest.approx(-0.4797, abs=5e-4)


@pytest.mark.parametrize("scope", SCOPES)
def test_frontier_bounds(scope):
    f = pd.read_csv(OUT / scope / "ladder" / "frontier.csv")
    assert len(f)
    for k in (25, 50):
        assert f[f"gap_{k}"].between(0, 1).all() and f[f"sev_{k}"].between(0, 1).all()
        assert (f[f"sev_{k}"] <= f[f"gap_{k}"] + 1e-12).all()
        assert (f[f"share_ge_{k}"] <= 1 - f["share_not_employed"] + 1e-12).all()
        # the non-employed are below any positive line, so the gap is at least their share
        assert (f[f"gap_{k}"] >= f["share_not_employed"] - 1e-12).all()
    assert (f["share_ge_50"] <= f["share_ge_25"] + 1e-12).all()


@pytest.mark.parametrize("scope", SCOPES)
def test_terms_of_trade_variants_close(scope):
    t = pd.read_csv(OUT / scope / "ladder" / "terms.csv").dropna(subset=["tot_pp", "tot_avg_pp"])
    assert np.corrcoef(t["tot_pp"], t["tot_avg_pp"])[0, 1] > 0.95


def test_anchored_slope_survey_close_to_model():
    a = pd.read_csv(OUT / "lac_lp" / "baumol" / "slope_anchored.csv").set_index(["period", "employment"])
    assert a.loc[("2000–2019", "survey"), "slope"] == pytest.approx(-0.30, abs=0.01)
    assert a.loc[("2000–2019", "model"), "slope"] == pytest.approx(-0.34, abs=0.01)
