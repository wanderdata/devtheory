"""Tests for study 9.8: the reparametrised post estimand equals the mean of the 2022-2024 event-study
coefficients, and the decision rules."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("did98", HERE / "minimum_wage_bite" / "03_did.py")
did = importlib.util.module_from_spec(spec)
spec.loader.exec_module(did)


def synthetic(seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    effects = {2019: 0.1, 2020: 0.1, 2021: 0.1, 2022: 0.2, 2023: 0.3, 2024: 0.4}
    for u in range(12):
        for g in ["a", "b", "c", "d"]:
            bite = rng.uniform(0, 0.5)
            for y in did.YEARS:
                rows.append({"unit": u, "group": g, "year": y, "bite18": bite, "emp18": rng.uniform(1, 3),
                             "y": effects.get(y, 0) * bite + 0.01 * u * (y - 2015) + 0.02 * (g == "b") * y
                             + rng.normal(0, 0.001)})
    return pd.DataFrame(rows)


def test_post_is_mean_of_2022_2024():
    d = synthetic()
    out, ev = did.estimate(d, "y", wild=False)
    assert abs(out["post"] - 0.3) < 0.01
    b = ev.set_index("year")["beta"]
    assert abs(b[2022] - 0.2) < 0.01 and abs(b[2024] - 0.4) < 0.01 and abs(b[2016]) < 0.01


def test_verdicts():
    base = {"p_pretrend": 0.5}
    assert did.verdict("P44", {**base, "post": -0.2, "lo90": -0.3, "hi90": -0.1}, 0.4) == "Supported"
    assert did.verdict("P44", {**base, "post": 0.0, "lo90": -0.05, "hi90": 0.05}, 0.4) == "Rejected"
    assert did.verdict("P45", {**base, "post": 0.0, "lo90": -0.2, "hi90": 0.1}, 0.4) == "Inconclusive"
    assert did.verdict("P46", {**base, "post": 0.0, "lo90": -0.05, "hi90": 0.05}, 0.4) == "Rejected"
    assert did.verdict("P47", {"p_pretrend": 0.05, "post": 0.3, "lo90": 0.1, "hi90": 0.5}, 0.4).startswith("Inconclusive")
