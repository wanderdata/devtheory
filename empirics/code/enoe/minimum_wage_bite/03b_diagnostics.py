"""Study 9.8, step 3b: diagnostics added after the main estimates were seen (D-069).

    python empirics/code/enoe/minimum_wage_bite/03b_diagnostics.py [--B 999]

The event studies of step 3 show, for several outcomes, coefficients for 2015-2017 of the same sign as
those after 2019, with 2018 alone at zero. Because the bite and the 2018 outcomes come from the same
ENOE sample, a cell whose 2018 sample happened to contain more low-paid workers has both a higher bite
and lower 2018 wages and formality, and reverts in other years. Two diagnostics:
  1. event studies with the bite measured in 2017Q1-Q3 (bite17), with 2018 as base year and with
     2015-2016 as base years (mean of the 2015-2016 coefficients set to zero by reporting differences);
  2. event studies excluding agriculture, where employment fell and value added did not.
Output: empirics/output/enoe/minimum_wage_bite/diagnostics.csv, event_diagnostics.csv
"""
import argparse
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
_s = importlib.util.spec_from_file_location("did98", HERE.parent / "03_did.py")
did = importlib.util.module_from_spec(_s)
_s.loader.exec_module(did)
OUT = did.OUT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=999)
    a = ap.parse_args()
    d = did.load()
    m = d[d["n18"] >= 100]
    specs = {"bite measured in 2017": (m, {"treat": "bite17"}),
             "excluding agriculture": (m[m["group"] != "Agriculture, forestry and fishing"], {}),
             "bite measured in 2017, excluding agriculture":
                 (m[m["group"] != "Agriculture, forestry and fishing"], {"treat": "bite17"})}
    rows, evs = [], []
    for name, (dd, kw) in specs.items():
        for y in ["w_all", "lemp", "formal", "lprod", "lva", "w_informal"]:
            r, ev = did.estimate(dd, y, B=a.B, **kw)
            pre = ev[ev["year"].isin([2015, 2016, 2017])]["beta"].mean()
            rows.append({"specification": name, "outcome": y, "post": r["post"], "lo90": r["lo90"], "hi90": r["hi90"],
                         "p_pretrend": r["p_pretrend"], "mean_pre_2015_2017": pre, "post_minus_pre": r["post"] - pre})
            ev["specification"] = name
            evs.append(ev)
            print(name, y, round(r["post"], 3), round(r["p_pretrend"], 3), round(pre, 3), flush=True)
    pd.DataFrame(rows).to_csv(OUT / "diagnostics.csv", index=False, float_format="%.6f")
    pd.concat(evs).to_csv(OUT / "event_diagnostics.csv", index=False, float_format="%.6f")


if __name__ == "__main__":
    main()
