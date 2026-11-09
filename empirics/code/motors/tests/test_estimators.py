"""Validation of the Hausman–Taylor implementation (OQ-49).

Cornwell–Rupert PSID wage panel (595 individuals x 7 years), as distributed with R's plm
package (`Wages`, via the Rdatasets repository). Reference HT estimates: Baltagi, Econometric
Analysis of Panel Data, Table 7.4; Stata xthtaylor manual example (same data and
specification). Reference values recorded from memory; the match to 4-5 significant digits on
all 13 coefficients is the validation.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from estimators import hausman_taylor  # noqa: E402

DATA = HERE.parents[2] / "empirics" / "data" / "source" / "validation" / "plm_Wages.csv"
REF = {"const": 2.9127, "wks": 0.000837, "south": 0.00744, "smsa": -0.04183, "married": -0.02985,
       "exp": 0.11313, "exp2": -0.000419, "bluecol": -0.02071, "ind": 0.01360, "union": 0.03278,
       "fem": -0.13092, "black": -0.28575, "ed": 0.13794}


def test_hausman_taylor_reproduces_published_estimates():
    w = pd.read_csv(DATA)
    w["id"], w["t"] = (w["rownames"] - 1) // 7, (w["rownames"] - 1) % 7
    for c in ["bluecol", "south", "smsa", "married", "union", "black"]:
        w[c] = (w[c] == "yes").astype(float)
    w["fem"], w["exp2"] = (w["sex"] == "female").astype(float), w["exp"] ** 2
    r = hausman_taylor(w, "lwage", x1=["bluecol", "south", "smsa", "ind"],
                       x2=["exp", "exp2", "wks", "married", "union"], z1=["fem", "black"], z2=["ed"],
                       entity="id", time="t")
    for k, v in REF.items():
        assert r.params[k] == pytest.approx(v, abs=5e-5), k
    assert r.se["ed"] == pytest.approx(0.0212, abs=5e-4)
