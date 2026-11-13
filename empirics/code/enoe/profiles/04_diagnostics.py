"""Study 9.2, step 4 (exploratory, not in the pre-analysis plan; D-051): why the Heckman-Lochner-
Taber estimates are implausible. (a) Cross-sectional profiles by sub-period; (b) HLT on 2005-2018,
before the large real increases in the minimum wage from 2019, which raised entry wages relative
to those of experienced workers and so violate the flat-spot assumption over 2005-2025;
(c) earnings reporting by experience bin over time.

    python empirics/code/enoe/profiles/04_diagnostics.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import profiles_lib as pl  # noqa: E402
from enoe_config import INTERIM, OUTPUT_ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "profiles"
PERIODS = [(2005, 2009), (2010, 2014), (2015, 2019), (2020, 2025)]


def main():
    d = pl.prepare(pd.read_parquet(INTERIM / "profiles_cs.parquet"))
    base = pl.baseline(d)
    rows = []
    for a, b in PERIODS:
        x = base[base["year"].between(a, b)].dropna(subset=["lw"])
        for name, g in [("all (baseline)", x), ("formal", x[x["formality"] == "formal"]),
                        ("informal", x[x["formality"] == "informal"])]:
            c = pl.cross_section(g)
            rows.append({"analysis": "cross-section by period", "period": f"{a}-{b}", "group": name,
                         "height_20_24": np.exp(c["20-24"]) - 1, "n": len(g)})
    x = base[base["year"] <= 2018].dropna(subset=["lw"])
    for name, g in [("all (baseline)", x), ("formal", x[x["formality"] == "formal"]),
                    ("informal", x[x["formality"] == "informal"])]:
        for method, fn in [("cross-section", pl.cross_section), ("HLT, flat spot 30-39", pl.hlt)]:
            c = fn(g)
            rows.append({"analysis": f"2005-2018: {method}", "period": "2005-2018", "group": name,
                         "height_20_24": np.exp(c["20-24"]) - 1, "n": len(g)})
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "diagnostics.csv", index=False)
    rep = (base.assign(period=pd.cut(base["year"], [2004, 2009, 2014, 2019, 2025],
                                      labels=["2005-2009", "2010-2014", "2015-2019", "2020-2025"]))
           .groupby(["period", "bin"], observed=True)
           .apply(lambda g: np.average(g["earn_ok"], weights=g["w"]), include_groups=False)
           .rename("share_reporting").reset_index())
    rep.to_csv(OUT / "reporting_by_experience.csv", index=False)
    print(out.round(3).to_string(index=False))
    print(rep.pivot(index="bin", columns="period", values="share_reporting").round(2))


if __name__ == "__main__":
    main()
