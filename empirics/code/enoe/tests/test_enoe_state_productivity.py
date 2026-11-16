"""Tests for study 9.7: industry-code mapping, distribution of unspecified codes, the decomposition
identities and the fixed-effects residualisation, on synthetic data."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "state_productivity"))

import activities as act  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), HERE / "state_productivity" / name)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


est = load("03_estimates.py")


def test_fine_code():
    codes = [1110, 1130, 1199, 2110, 2131, 3110, 3380, 3360, 3399, 4390, 4610, 6130, 6250, 9310, 9700, 0]
    assert list(act.fine_code(np.array(codes))) == [
        "111", "otros11", "U11", "OIL", "21np", "311", "U31", "333_336", "339", "U43", "46", "61", "62", "93",
        "UALL", "UALL"]


def test_classifications_partition_fine():
    main = sorted(f for fs in act.MAIN.values() for f in fs)
    meitef = sorted(f for fs in act.MEITEF.values() for f in fs)
    assert main == sorted(act.FINE) == meitef
    assert len(act.MAIN) == 20


def test_distribute_preserves_totals():
    d = pd.DataFrame({"k": [1, 1, 1, 1, 1], "act": ["311", "312", "U31", "46", "UALL"],
                      "w": [30.0, 10.0, 8.0, 50.0, 10.0]})
    r = act.distribute(d, ["k"], ["w"]).set_index("act")["w"]
    assert r.sum() == pytest.approx(108.0)
    # U31 split 3:1 between 311 and 312; UALL split 30:10:50 before U31 is added
    assert r["311"] == pytest.approx(30 + 6 + 10 * 30 / 90)
    assert r["46"] == pytest.approx(50 + 10 * 50 / 90)


def test_terms_identity():
    rng = np.random.default_rng(1)
    L0, L1 = rng.uniform(1, 10, 6), rng.uniform(1, 10, 6)
    Y0, Y1 = L0 * rng.uniform(1, 5, 6), L1 * rng.uniform(1, 5, 6)
    P0, P1, W, S, D = est._terms(L0, Y0, L1, Y1)
    assert W + S + D == pytest.approx(P1 - P0)


def test_decompose_shares_add_up():
    rows = []
    rng = np.random.default_rng(2)
    for per in ("P0", "P1"):
        for g in "abc":
            ef, ei = rng.uniform(1, 5), rng.uniform(1, 5)
            va = rng.uniform(10, 50)
            rows.append({"period": per, "unit": 1, "group": g, "va_k": va, "va_f": 0.7 * va, "va_i": 0.3 * va,
                         "emp_f": ef, "emp_i": ei, "hrs_f": 40 * ef, "hrs_i": 35 * ei})
    d = est.decompose(pd.DataFrame(rows)).iloc[0]
    assert d["within"] + d["static"] + d["dynamic"] == pytest.approx(d["growth"])
    assert d["within_seg"] + d["realloc"] + d["formalisation"] == pytest.approx(d["growth"])


def test_p42_verdicts():
    n = 31
    x = np.linspace(-1, 1, n)
    dec = pd.DataFrame({"growth": x, "d_formal_share": x + 0.01 * np.sin(np.arange(n)), "P0": np.exp(x)})
    assert est.p42(dec, B=199)["verdict"] == "Supported"
    dec["d_formal_share"] = -x
    assert est.p42(dec, B=199)["verdict"] == "Rejected"


def test_fe_resid_removes_means():
    pt = load("04_passthrough.py")
    df = pd.DataFrame({"unit": [1, 1, 2, 2, 3, 3], "group": ["a", "b", "a", "b", "a", "b"],
                       "v": [1.0, 2.0, 3.0, 5.0, 2.0, 4.0]})
    w = pd.Series(np.ones(6))
    r = pt.fe_resid(df, "v", w)
    assert r.groupby(df["unit"]).mean().abs().max() < 1e-9
    assert r.groupby(df["group"]).mean().abs().max() < 1e-9
