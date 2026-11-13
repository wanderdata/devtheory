"""Tests for study 9.2 functions on synthetic data with known experience, time and cohort effects."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "profiles"))

import profiles_lib as pl  # noqa: E402


def test_experience_rule():
    e = pl.experience([30, 30, 40], [9, 16, 12])
    assert e.tolist() == [12, 8, 22]          # age-18 below 12 years; age-school-6 from 12


def synthetic_cs(time_trend=0.02, cohort_trend=0.0, seed=0, n=120000):
    """Repeated cross-sections with experience effects that rise to 0.5 log points at 20-24 and are
    flat from 30 years on, a time trend in wages, and optional cohort effects."""
    rng = np.random.default_rng(seed)
    year = rng.integers(2005, 2026, n)
    age = rng.integers(18, 59, n)
    school = np.full(n, 9.0)
    exp = age - 18
    prof = np.minimum(exp, 30) / 30 * 0.6                 # rises until 30, then flat
    cohort = year - age
    lw = prof + time_trend * (year - 2005) + cohort_trend * (cohort - 1960) + rng.normal(0, 0.3, n)
    d = pd.DataFrame({"year": year, "eda": age, "anios_esc": school, "ing_x_hrs": np.exp(lw), "hrsocup": 45,
                      "pos_ocu": 1, "ambito2": 6, "emp_ppal": 2, "rama_est2": 3, "clase2": 1, "sex": 1,
                      "w": 1.0, "ent": 1, "psu": rng.integers(0, 500, n).astype(str)})
    return pl.prepare(d), prof, exp


def true_bin(prof, exp, b):
    lo = int(b.split("-")[0])
    return float(np.mean(prof[(exp >= lo) & (exp < lo + 5)]) - np.mean(prof[exp < 5]))


def test_cross_section_recovers_profile_without_cohort_effects():
    d, prof, exp = synthetic_cs(cohort_trend=0.0)
    c = pl.cross_section(pl.baseline(d))
    assert c["20-24"] == pytest.approx(true_bin(prof, exp, "20-24"), abs=0.01)


def test_hlt_recovers_profile_with_cohort_effects_where_cross_section_fails():
    d, prof, exp = synthetic_cs(time_trend=0.02, cohort_trend=0.01)
    base = pl.baseline(d)
    truth = true_bin(prof, exp, "20-24")
    cs = pl.cross_section(base)["20-24"]
    h = pl.hlt(base)["20-24"]
    assert abs(h - truth) < 0.03
    assert abs(cs - truth) > abs(h - truth)      # cohort effects bias the cross-section


def test_composition_identity():
    rng = np.random.default_rng(1)
    rows = []
    for b, s_inf in [("0-4", 0.6), ("20-24", 0.4)]:
        for f, lvl in [("formal", 0.0 if b == "0-4" else 0.8), ("informal", -0.2 if b == "0-4" else 0.1)]:
            k = int(10000 * (s_inf if f == "informal" else 1 - s_inf))
            rows.append(pd.DataFrame({"bin": b, "formality": f, "lw": lvl + rng.normal(0, 0.01, k), "w": 1.0}))
    d = pd.concat(rows)
    r = pl.composition(d, {"formal": pd.Series({"20-24": 0.8}), "informal": pd.Series({"20-24": 0.3})})
    m = d.groupby("bin").apply(lambda x: x["lw"].mean(), include_groups=False)
    assert r["national_log"] == pytest.approx(m["20-24"] - m["0-4"], abs=1e-3)
    for o in ("1", "2"):
        assert r[f"within_order{o}"] + r[f"composition_order{o}"] == pytest.approx(r["national_log"] - r["formal_log"])


def test_dummies_match_numeric_levels():
    d = pl.dummies(pd.Series([2005, 2006, 2005]), [2006])
    assert d[:, 0].tolist() == [0.0, 1.0, 0.0]
