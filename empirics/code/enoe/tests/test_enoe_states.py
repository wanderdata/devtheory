"""Tests for study 9.6: the sparse state-effects estimator recovers known state rates at the
average composition, the signal share is near one when states truly differ and near zero when
they do not, and the PIBE loader adds up to the national total."""
import importlib
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "states"))



def _load(name, file):
    """Load by path under a unique name: other studies also have a module called 03_estimates."""
    spec = importlib.util.spec_from_file_location(name, HERE / "states" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gdp = _load("states_gdp", "gdp.py")
est = _load("states_03_estimates", "03_estimates.py")


def synth(effects, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for ent, a in effects.items():
        age = rng.integers(16, 66, n)
        x = (age > 30).astype(float)
        p = np.clip(a + 0.05 * x, 0, 1)
        rows.append(pd.DataFrame({"ent_i": ent, "age": age, "older": x, "y": (rng.random(n) < p).astype(float),
                                  "fac": 1.0, "cl": [f"{ent}_{i % 200}" for i in range(n)]}))
    return pd.concat(rows, ignore_index=True)


def test_state_effects_recover_rates():
    eff = {1: 0.05, 2: 0.10, 3: 0.20}
    d = synth(eff)
    t = est.state_effects(d, "y", ["older"]).set_index("ent")
    xbar = d["older"].mean()
    for ent, a in eff.items():
        assert t.loc[ent, "theta"] == pytest.approx(a + 0.05 * xbar, abs=0.02)
        assert 0 < t.loc[ent, "se"] < 0.02


def test_signal_share():
    rng = np.random.default_rng(1)
    real = pd.DataFrame({"theta": rng.normal(0.12, 0.03, 32), "se": 0.004})
    noise = pd.DataFrame({"theta": rng.normal(0.12, 0.004, 32), "se": 0.004})
    assert est.signal(real)["signal_share"] > 0.9
    assert est.signal(noise)["signal_share"] < 0.4


def test_pibe_adds_up():
    g = gdp.state_gdp()
    assert g["ent"].nunique() == 32 and g["year"].min() == 1980
    nat = g.groupby("year")["gdp"].sum()
    assert nat.loc[2018] == pytest.approx(24176670.379, rel=1e-6)    # national GDP 2018, millions of 2018 pesos
