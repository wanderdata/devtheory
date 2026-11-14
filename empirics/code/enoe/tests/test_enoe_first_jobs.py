"""Tests for study 9.5: classification of entry types, the Oster sensitivity formula, and the
linking of a cohort through five interviews on a synthetic panel."""
import importlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "first_jobs"))
sys.path.append(str(HERE / "border_mw"))

est = importlib.import_module("03_estimates")
pan = importlib.import_module("02_panels")


def test_entry_types():
    state = np.array(["F", "I", "I", "I", "I", "N", "U"])
    pos = np.array([1, 1, 1, 3, 4, np.nan, 1])
    amb = np.array([6, 4, 2, 2, 3, np.nan, 4])
    t = est.entry_type(state, pos, amb)
    assert list(t) == ["formal", "informal wage, premises", "informal wage, other", "informal own-account or unpaid",
                       "informal own-account or unpaid", "not employed", "other"]


def test_oster_delta_zero_when_no_movement_needed():
    # coefficient does not move with controls: infinite robustness is not returned as a number
    assert np.isnan(est.oster_delta(0.1, 0.01, 0.1, 0.2, 0.26))
    # coefficient halves when R2 rises from 0.01 to 0.21; Rmax 0.31 -> delta = 0.05*0.2/(0.05*0.1) = 2
    assert est.oster_delta(0.10, 0.01, 0.05, 0.21, 0.31) == pytest.approx(2.0)


def frame(n_ent, ids, eda, states, year):
    k = len(ids)
    d = pd.DataFrame({"cd_a": "01", "ent": "09", "con": [str(i) for i in ids], "v_sel": "1", "n_hog": "1", "h_mud": "0",
                      "n_ren": "01", "n_ent": n_ent, "sex": 1, "eda": eda, "state": states, "never": True, "pos_ocu": 1,
                      "ambito2": 4, "rama_est2": 3, "ingocup": 5000.0, "hrsocup": 40, "salario": 3000.0, "par_c": 301,
                      "anios_esc": 9, "cs_p17": 2, "hh_formal": 1, "hh_informal": 0, "hh_adults": 2, "urban": True,
                      "upm": "u1", "fac": 100.0, "year": year, "q": 1})
    return d


def test_follow_links_through_five_interviews():
    f1 = frame(1, [1, 2, 3], [16, 17, 18], ["N", "N", "N"], 2010)
    f2 = frame(2, [1, 2], [16, 17], ["I", "N"], 2010)        # person 3 lost
    f3 = frame(3, [1, 2], [16, 17], ["I", "F"], 2010)
    f4 = frame(4, [1, 2], [17, 18], ["F", "F"], 2010)
    f5 = frame(5, [1, 2], [17, 25], ["F", "F"], 2011)        # person 2 fails the age check at 5
    out, d = pan.follow(f1, [f2, f3, f4, f5])
    assert list(out["linked_2"]) == [True, True, False]
    assert list(out["linked_5"]) == [True, False, False]
    assert out.loc[0, "state_2"] == "I" and out.loc[0, "state_5"] == "F"
    assert out.loc[1, "state_3"] == "F"
