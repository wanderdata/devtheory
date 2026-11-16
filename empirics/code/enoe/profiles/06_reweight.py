"""Study 9.2, step 6: profiles reweighted for earnings non-response (pre-analysis plan §5; added
after the independent audit found that the rule is triggered by year and experience bin, D-064).

    python empirics/code/enoe/profiles/06_reweight.py

Plan §5: if earnings reporting differs by more than 15 points between formal and informal workers
in the same experience bin, profile comparisons are reported raw and reweighted on the probability
of reporting (age, schooling, sex, state). The baseline sample is men, so sex is constant. The
probability is a logit on year x formality, five-year age groups, single years of schooling and
state, estimated on the baseline sample; reporters are weighted by the survey weight divided by
the fitted probability (trimmed below at 0.05). Outputs in empirics/output/enoe/profiles/:
  nonresponse_year_bin.csv  reporting share by year x experience bin x formality, and the gap
  reweighted_heights.csv    heights at 20-24 years, raw and reweighted, with bootstrap intervals
                            for the three main groups
  reweighted_composition.csv  the composition decomposition on reweighted profiles
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
NBOOT, SEED = 49, 20261116


def _sparse_dummies(values):
    from scipy import sparse
    codes, cats = pd.factorize(pd.Series(values, dtype=object).map(str), sort=True)
    n = len(codes)
    m = sparse.csr_matrix((np.ones(n), (np.arange(n), codes)), shape=(n, len(cats)))
    return m[:, 1:]


def reporting_weights(b, iters=25):
    """Fitted probability of reporting positive hourly earnings: weighted logit on year x formality,
    five-year age groups, single years of schooling and state, fitted by iteratively reweighted least
    squares on a sparse design (a dense design does not fit in the workspace's memory)."""
    from scipy import sparse
    age = pd.cut(b["eda"], range(15, 70, 5), right=False).astype(str)
    blocks = [sparse.csr_matrix(np.ones((len(b), 1)))]
    for v in [b["year"].astype(str) + "_" + b["formality"], age, b["school"].fillna(-1).astype(int), b["ent"]]:
        blocks.append(_sparse_dummies(v.to_numpy()))
    X = sparse.hstack(blocks).tocsr()
    y = b["earn_ok"].to_numpy(float)
    sw = (b["w"] / b["w"].mean()).to_numpy(float)
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = X @ beta
        mu = 1 / (1 + np.exp(-eta))
        v = np.clip(mu * (1 - mu), 1e-9, None)
        z = eta + (y - mu) / v
        Wv = sw * v
        A = (X.T.multiply(Wv)).tocsr() @ X
        new = np.linalg.solve(A.toarray() + 1e-8 * np.eye(X.shape[1]), X.T @ (Wv * z))
        if np.max(np.abs(new - beta)) < 1e-7:
            beta = new
            break
        beta = new
    p = 1 / (1 + np.exp(-(X @ beta)))
    return np.clip(p, 0.05, 1.0)


def main():
    d = pl.prepare(pd.read_parquet(INTERIM / "profiles_cs.parquet"))
    b = pl.baseline(d)
    b = b[b["formality"].notna()].copy()

    # the rule by year and experience bin
    nr = (b.groupby(["year", "bin", "formality"])
          .apply(lambda x: np.average(x["earn_ok"], weights=x["w"]), include_groups=False).rename("share").reset_index())
    g = nr.pivot_table(index=["year", "bin"], columns="formality", values="share").reset_index()
    g["gap"] = g["formal"] - g["informal"]
    g.to_csv(OUT / "nonresponse_year_bin.csv", index=False, float_format="%.4f")
    print(f"cells with |gap| > 0.15: {(g['gap'].abs() > 0.15).sum()} of {len(g)}; max {g['gap'].abs().max():.3f}")

    b["p_report"] = reporting_weights(b)
    rw = b.assign(w=b["w"] / b["p_report"])
    groups = [("all (baseline)", None), ("formal", ("formality", "formal")), ("informal", ("formality", "informal"))]
    for s in sorted(b["sector6"].dropna().unique()):
        groups.append((f"sector: {s}", ("sector6", s)))
    rows, coefs = [], {}
    for name, sel in groups:
        for label, frame in [("raw", b), ("reweighted for non-response", rw)]:
            x = frame if sel is None else frame[frame[sel[0]] == sel[1]]
            x = x.dropna(subset=["lw"])
            c = pl.cross_section(x)
            coefs[(name, label)] = c
            lo = hi = np.nan
            if name in ("all (baseline)", "formal", "informal"):
                draws = pl.psu_bootstrap(x, pl.cross_section, NBOOT, SEED)
                v = [np.exp(dd["20-24"]) - 1 for dd in draws]
                lo, hi = np.percentile(v, 5), np.percentile(v, 95)
            rows.append({"group": name, "weights": label, "height_20_24": np.exp(c["20-24"]) - 1, "lo90": lo, "hi90": hi,
                         "n": len(x)})
            print(f"{name:40s} {label:30s} {np.exp(c['20-24']) - 1:.3f}", flush=True)
    pd.DataFrame(rows).to_csv(OUT / "reweighted_heights.csv", index=False, float_format="%.4f")
    comp = []
    for label, frame in [("raw", b), ("reweighted for non-response", rw)]:
        cb = {"formal": coefs[("formal", label)], "informal": coefs[("informal", label)]}
        comp.append({"weights": label, **pl.composition(frame.dropna(subset=["lw"]), cb)})
    pd.DataFrame(comp).to_csv(OUT / "reweighted_composition.csv", index=False, float_format="%.5f")
    print(pd.DataFrame(comp).round(4).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
