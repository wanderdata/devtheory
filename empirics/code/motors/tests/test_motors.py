"""Checks on the WP07 panel and results: construction rules and published reference numbers."""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[4]
PROC = ROOT / "empirics" / "data" / "processed" / "motors"
OUT = ROOT / "empirics" / "output" / "motors"


def test_panel_growth_definition():
    a = pd.read_csv(PROC / "annual.csv", low_memory=False).set_index(["iso3", "year"])
    p = pd.read_csv(PROC / "panel5.csv")
    r = p[(p["iso3"] == "MEX") & (p["period"] == 1990)].iloc[0]
    y0, y1 = a.loc[("MEX", 1990), "y_na"], a.loc[("MEX", 1995), "y_na"]
    assert r["GR"] == pytest.approx(100 * (y1 / y0 - 1) / 5)
    assert r["MAN"] == pytest.approx(a.loc[("MEX", 1990), "MAN"])


def test_shares_are_percentages():
    p = pd.read_csv(PROC / "panel5.csv")
    for c in ["MAN", "AGR", "SER"]:
        x = p[c].dropna()
        assert (x >= 0).all() and (x <= 100).all()


def test_splice_has_no_jump_at_1970():
    a = pd.read_csv(PROC / "annual.csv", low_memory=False)
    w = a[a["iso3"].isin(["GBR", "ZMB", "GHA"]) & a["year"].isin([1969, 1970])].pivot(index="iso3", columns="year", values="MAN")
    assert (abs(w[1970] - w[1969]) < 4).all()


def test_replication_reference_numbers():
    """WP07 §2: the S&V interaction model in the sample without former planned economies."""
    c = pd.read_csv(OUT / "replication" / "comparison.csv")
    r = c[(c["sample"] == "excl_cpe") & (c["model"] == "(3) +MANxREL+MANxEDU")].set_index("term")
    assert r.loc["MANxREL", "coef"] == pytest.approx(-0.24, abs=0.03)
    assert r.loc["MANxEDU", "coef"] > 0 and r.loc["MANxEDU", "p"] < 0.05
    core = c[(c["sample"] == "core") & (c["model"] == "(3) +MANxREL+MANxEDU")].set_index("term")
    assert core.loc["MANxREL", "coef"] > 0


def test_speccurve_headlines():
    s = pd.read_csv(OUT / "speccurve" / "summary.csv").set_index("estimand")
    assert s.loc["Manufacturing, 1990–2005", "verdict"] == "robustly negative"
    assert s.loc["SER, 2005–20", "verdict"] == "robustly negative"
    assert s.loc["Manufacturing, 1970–90", "n_specs"] == 192      # 3 x 4 x 2 x 2 x 2 x 2: every specification ran
    assert (s.loc[s["family"] == "Q4", "n_specs"] == 96).all()
