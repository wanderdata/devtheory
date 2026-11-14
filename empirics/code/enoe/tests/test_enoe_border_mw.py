"""Tests for study 9.4's estimation tools on synthetic panels: the FE projection reproduces a
dummy-variable regression on an unbalanced panel, the DiD recovers a known effect, the wild
bootstrap has roughly correct size under the null with few treated clusters, and the event study
returns zero pre-period effects when there are none."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "border_mw"))

import border_lib as bl  # noqa: E402


def panel(n_units=60, n_treat=12, T=12, effect=0.0, seed=0, drop=0.1):
    rng = np.random.default_rng(seed)
    rows = []
    a = rng.normal(0, 1, n_units)
    g = rng.normal(0, 0.3, T)
    for m in range(n_units):
        e_m = rng.normal(0, 0.3)                       # cluster shock, shared over time
        for t in range(T):
            if rng.random() < drop:
                continue
            tr, post = m < n_treat, t >= 8
            y = a[m] + g[t] + effect * tr * post + e_m * post + rng.normal(0, 0.2)
            rows.append({"mid": m, "t": t, "zlfn": tr, "post": post, "y": y, "w": 1 + (m % 3)})
    return pd.DataFrame(rows)


def test_projection_matches_dummy_regression():
    d = panel(n_units=15, n_treat=4, T=12, effect=0.5, seed=1, drop=0.2)
    X = (d["zlfn"] & d["post"]).astype(float).to_numpy()
    f = bl.fit(d["y"], X, d[["mid", "t"]], d["w"], d["mid"])
    D = np.column_stack([X, pd.get_dummies(d["mid"]).to_numpy(float), pd.get_dummies(d["t"], drop_first=True).to_numpy(float)])
    W = d["w"].to_numpy()
    b = np.linalg.lstsq(D * np.sqrt(W)[:, None], d["y"].to_numpy() * np.sqrt(W), rcond=None)[0]
    assert f["b"][0] == pytest.approx(b[0], abs=1e-9)


def test_did_recovers_effect():
    d = panel(n_units=200, n_treat=40, effect=0.3, seed=2)
    r = bl.did(d, "y", B=199, ci=False)
    assert r["beta"] == pytest.approx(0.3, abs=0.1)
    assert r["p_wild"] < 0.05


def test_wild_bootstrap_size_with_few_treated_clusters():
    rej = 0
    reps = 60
    for s in range(reps):
        d = panel(n_units=60, n_treat=8, effect=0.0, seed=100 + s)
        rej += bl.did(d, "y", B=199, ci=False)["p_wild"] < 0.10
    assert rej / reps < 0.2            # nominal 10%; generous bound for 60 replications


def test_ci_contains_truth_and_estimate():
    d = panel(n_units=80, n_treat=15, effect=0.2, seed=5)
    r = bl.did(d, "y", B=199, ci=True)
    assert r["lo90"] < r["beta"] < r["hi90"]
    assert r["lo90"] < 0.2 < r["hi90"]


def test_event_study_no_pretrend():
    d = panel(n_units=120, n_treat=30, effect=0.4, seed=7)
    es, p = bl.event_study(d, "y", ref=7, B=199, pre=list(range(7)))
    pre = es[es["t"] < 7]["beta"]
    post = es[es["t"] >= 8]["beta"]
    assert pre.abs().max() < 0.25 and post.mean() == pytest.approx(0.4, abs=0.15)
    assert p > 0.01


def test_range_allocation():
    import importlib
    r = importlib.import_module("06_ranges")
    # a range wholly inside one bin
    s = r.shares_of_interval(0.0, 0.5)
    assert s[0] == pytest.approx(1.0) and s.sum() == pytest.approx(1.0)
    # a range crossing M: 0.58 to 1.16 M (code 3 in the control group, 2019)
    s = r.shares_of_interval(0.58, 1.16)
    assert s.sum() == pytest.approx(1.0)
    assert s[:3].sum() == pytest.approx((1.0 - 0.58) / 0.58)
    # a point at M falls in [1.0, 1.2)
    s = r.shares_of_interval(1.0, 1.0)
    assert s[3] == 1.0
