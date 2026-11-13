"""Study 9.2, step 2: experience-earnings profiles by type of job (pre-analysis plan §§4-5).

    python empirics/code/enoe/profiles/02_profiles.py

Reads empirics/data/raw/enoe_interim/profiles_cs.parquet and writes aggregate tables to
empirics/output/enoe/profiles/:
  profiles.csv     coefficients and heights by experience bin, for each group and method
                   (cross-section; HLT with flat spot 30-39 and 35-39), with bootstrap intervals
  heights.csv      the headline: height at 20-24 years by group and method
  composition.csv  national height decomposed into flatter informal profiles and composition
  nonresponse.csv  share of the baseline sample reporting positive hourly earnings
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
NBOOT_CS, NBOOT_HLT, SEED = 199, 99, 20261113


def groups(d):
    """(name, frame) pairs: the baseline, its split by job type, and the variants of plan §2."""
    base = pl.baseline(d)
    g = [("all (baseline)", base),
         ("formal", base[base["formality"] == "formal"]),
         ("informal", base[base["formality"] == "informal"])]
    for s in sorted(base["sector6"].dropna().unique()):
        g.append((f"sector: {s}", base[base["sector6"] == s]))
    for f in ["formal", "informal"]:
        for s in ["manufacturing", "commerce"]:
            g.append((f"{f}, {s}", base[(base["formality"] == f) & (base["sector6"] == s)]))
    for z in ["micro and small", "medium and large"]:
        g.append((f"establishments: {z}", base[base["size2"] == z]))
    g += [("women (baseline otherwise)", pl.baseline(d, sex=2)),
          ("men, all hours", pl.baseline(d, fulltime=False)),
          ("own-account men, all hours", pl.baseline(d, fulltime=False, pos=3)),
          ("baseline, ages ending in 0 or 5 removed", base[~base["heaped"]])]
    return g


def interval(draws, b):
    v = [np.exp(x[b]) - 1 for x in draws if b in x.index]
    return (np.percentile(v, 5), np.percentile(v, 95)) if v else (np.nan, np.nan)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    d = pl.prepare(pd.read_parquet(INTERIM / "profiles_cs.parquet"))

    # non-response (plan §5): share reporting positive hourly earnings in the baseline sample
    b0 = pl.baseline(d)
    nr = (b0.groupby(["year", "formality"]).apply(lambda x: np.average(x["earn_ok"], weights=x["w"]), include_groups=False)
          .rename("share_reporting").reset_index())
    nrb = (b0.groupby(["bin", "formality"]).apply(lambda x: np.average(x["earn_ok"], weights=x["w"]), include_groups=False)
           .rename("share_reporting").reset_index().assign(year="all"))
    nonresp = pd.concat([nr, nrb])
    nonresp.to_csv(OUT / "nonresponse.csv", index=False)
    gap = nrb.pivot(index="bin", columns="formality", values="share_reporting")
    max_gap = float((gap["formal"] - gap["informal"]).abs().max())
    print(f"largest formal-informal gap in reporting within an experience bin: {max_gap:.3f}")

    rows, coefs = [], {}
    for name, g in groups(d):
        g = g.dropna(subset=["lw"])
        if len(g) < 5000:
            print(f"[skip] {name}: {len(g)} observations")
            continue
        for method, fn, nb in [("cross-section", pl.cross_section, NBOOT_CS),
                               ("HLT, flat spot 30-39", lambda x: pl.hlt(x, ("30-34", "35-39")), NBOOT_HLT),
                               ("HLT, flat spot 35-39", lambda x: pl.hlt(x, ("35-39",)), 0)]:
            if method.startswith("HLT") and name not in ("all (baseline)", "formal", "informal",
                                                         "baseline, ages ending in 0 or 5 removed"):
                continue
            c = fn(g)
            coefs[(name, method)] = c
            draws = pl.psu_bootstrap(g, fn, nb, SEED) if nb else []
            for b in c.index:
                lo, hi = interval(draws, b) if draws else (np.nan, np.nan)
                rows.append({"group": name, "method": method, "bin": b, "coef": c[b], "height": np.exp(c[b]) - 1,
                             "lo90": lo, "hi90": hi, "n": len(g)})
            print(f"{name:45s} {method:22s} height 20-24: {np.exp(c['20-24']) - 1:.3f} (n={len(g):,})")
    prof = pd.DataFrame(rows)
    prof.to_csv(OUT / "profiles.csv", index=False)
    prof[prof["bin"] == "20-24"].to_csv(OUT / "heights.csv", index=False)

    comp = []
    for method in ["cross-section", "HLT, flat spot 30-39"]:
        cb = {"formal": coefs[("formal", method)], "informal": coefs[("informal", method)]}
        r = pl.composition(pl.baseline(d).dropna(subset=["lw"]), cb)
        comp.append({"method": method, **r, "max_reporting_gap": max_gap})
    pd.DataFrame(comp).to_csv(OUT / "composition.csv", index=False)


if __name__ == "__main__":
    main()
