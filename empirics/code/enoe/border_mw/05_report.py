"""Study 9.4, step 5: results.md, applying the decision rules of the pre-analysis plan (§§1, 6)
to the outputs of steps 3 and 4.

    python empirics/code/enoe/border_mw/05_report.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from enoe_config import OUTPUT_ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "border_mw"
LABELS = {
    "lnw": "Log hourly earnings, wage employees 16-65",
    "emp_rate": "Employment rate, 15+",
    "formal_rate": "Formal employment rate, 15+",
    "informal_rate": "Informal employment rate, 15+",
    "formal_share": "Formal share of employment",
    "i_to_f": "Informal to formal, quarterly rate",
    "n_to_f": "Not employed to formal, quarterly rate",
    "f_to_i": "Formal to informal, quarterly rate",
    "f_to_n": "Formal to not employed, quarterly rate",
    "i_to_n": "Informal to not employed, quarterly rate",
    "below_m": "Share of reporting wage employees below the new minimum",
    "missing": "Wage employees below the new minimum, per person 15+",
    "excess": "Wage employees at 1.0-1.5 times the new minimum, per person 15+",
    "i_missing": "Informal wage employees below the new minimum, per person 15+",
    "i_excess": "Informal wage employees at 1.0-1.5 times, per person 15+",
    "f_missing": "Formal wage employees below the new minimum, per person 15+",
    "f_excess": "Formal wage employees at 1.0-1.5 times, per person 15+",
    "we_rate": "Wage employees 16-65, per person 15+",
    "report": "Share of wage employees reporting earnings",
    "hours": "Weekly hours, wage employees",
    "lnw_own": "Log hourly earnings, own-account workers",
}


def table(df, cols):
    out = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    for _, r in df.iterrows():
        out += "| " + " | ".join(str(r[c]) for c in cols) + " |\n"
    return out


def fmt(x, k=4):
    return "" if pd.isna(x) else f"{x:+.{k}f}"


def judge(d, pre, unreliable):
    """Decision rules of plan §1, with §6: an outcome with a pre-trend (p < 0.10) or, for the earnings
    bins, a differential change in reporting above 3 points cannot support or reject a proposition."""
    m = d[d["spec"] == "main"].set_index("outcome")
    out = {}
    lnw, emp = m.loc["lnw"], m.loc["emp_rate"]
    miss, exc = m.loc["missing", "beta"], m.loc["excess", "beta"]
    ratio = exc / -miss if miss < 0 else np.nan
    ok_w, ok_b = "lnw" not in unreliable, not ({"missing", "excess"} & unreliable)
    sup = ok_w and ok_b and (lnw["lo90"] > 0) and (emp["lo90"] > -0.015) and (ratio >= 0.7)
    rej = (emp["beta"] <= -0.01 and emp["hi90"] < 0) or (ok_w and lnw["beta"] < 0.02 and lnw["lo90"] <= 0 <= lnw["hi90"])
    out["P31"] = ("supported" if sup else "rejected" if rej else "inconclusive",
                  f"log earnings {lnw['beta']:+.3f} [{lnw['lo90']:+.3f}, {lnw['hi90']:+.3f}]; employment rate "
                  f"{emp['beta']:+.4f} [{emp['lo90']:+.4f}, {emp['hi90']:+.4f}]; excess/missing = "
                  f"{ratio:.2f}" if np.isfinite(ratio) else "excess/missing undefined (no missing jobs)")
    i2f, fr = m.loc["i_to_f"], m.loc["formal_rate"]
    sup = (i2f["lo90"] > 0) and not (fr["hi90"] < 0)
    rej = i2f["hi90"] < 0.10 * pre["i_to_f"]
    out["P32"] = ("supported" if sup else "rejected" if rej else "inconclusive",
                  f"informal to formal {i2f['beta']:+.4f} [{i2f['lo90']:+.4f}, {i2f['hi90']:+.4f}] against a "
                  f"pre-period rate of {pre['i_to_f']:.4f} (10% = {0.1 * pre['i_to_f']:.4f}); formal employment rate "
                  f"{fr['beta']:+.4f} [{fr['lo90']:+.4f}, {fr['hi90']:+.4f}]")
    im = m.loc["i_missing"]
    ok = "i_missing" not in unreliable
    sup = ok and im["hi90"] < 0
    rej = ok and im["lo90"] > -0.25 * pre["i_missing"]
    out["P33"] = ("supported" if sup else "rejected" if rej else "inconclusive",
                  f"informal jobs below the new minimum {im['beta']:+.4f} [{im['lo90']:+.4f}, {im['hi90']:+.4f}] per "
                  f"person 15+, against a pre-period mass of {pre['i_missing']:.4f} (a quarter = "
                  f"{0.25 * pre['i_missing']:.4f})")
    return out


def main():
    d = pd.read_csv(OUT / "did.csv")
    pre = pd.read_csv(OUT / "pre_means.csv", index_col=0)["pre_mean_zone"]
    pt = pd.read_csv(OUT / "pretrend.csv").set_index("outcome")["p_pretrend_wild"]
    bins = pd.read_csv(OUT / "bins.csv")
    link = pd.read_csv(OUT / "linkage.csv")
    rep_beta = d[(d["spec"] == "main") & (d["outcome"] == "report")]["beta"].iloc[0]
    unreliable = {o for o, p in pt.items() if p < 0.10}
    if abs(rep_beta) > 0.03:
        unreliable |= {"missing", "excess", "i_missing", "i_excess", "below_m"}
    j = judge(d, pre, unreliable)
    m = d[d["spec"] == "main"].copy()
    m["label"] = m["outcome"].map(LABELS)
    m["pre-trend p"] = m["outcome"].map(pt).map(lambda x: "" if pd.isna(x) else f"{x:.2f}")
    for c in ["beta", "lo90", "hi90"]:
        m[c] = m[c].map(fmt)
    m["p (wild)"] = m["p_wild"].map(lambda x: f"{x:.3f}")
    m["pre-period mean, zone"] = m["pre_mean_zone"].map(lambda x: f"{x:.4f}")
    rep = m.set_index("outcome")
    txt = ["# Study 9.4 — results (generated; do not edit)\n",
           "Generated by `empirics/code/enoe/border_mw/05_report.py`. Plan: "
           "`papers/WP09_jobs_mexico/9.4_border_minimum_wage/00_pre_analysis_plan.md`.\n",
           f"Treated municipalities: {int(d[d['spec'] == 'main']['treated_clusters'].iloc[0])}; clusters in the main "
           f"specification: {int(d[d['spec'] == 'main']['clusters'].iloc[0])}. Linkage across consecutive quarters: "
           f"{link['match_rate'].min():.3f}-{link['match_rate'].max():.3f} of eligible persons.\n",
           "## Propositions\n"]
    for k, (v, why) in j.items():
        txt.append(f"- **{k}: {v}.** {why}.")
    txt.append(f"\nRule §6, non-reporting: differential change in earnings reporting {rep_beta:+.4f} "
               f"({'above' if abs(rep_beta) > 0.03 else 'within'} the 3-point threshold).")
    bad = [o for o, p in pt.items() if p < 0.10]
    txt.append(f"Rule §6, pre-trends (joint wild bootstrap p < 0.10): {', '.join(bad) if bad else 'none'}.")
    txt.append(f"Outcomes treated as unreliable for the propositions: {', '.join(sorted(unreliable)) or 'none'}.\n")
    mm = d[d["spec"] == "main"].set_index("outcome")["beta"]
    norep = mm["f_norep"] + mm["i_norep"]
    txt.append("## Exploratory: bounds for missing jobs under non-reporting (D-055)\n")
    txt.append(f"Missing jobs below the new minimum: {mm['missing']:+.4f} per person 15+; rise in wage employees not "
               f"reporting earnings: {norep:+.4f}. If every additional non-reporter earned below the new minimum, missing "
               f"jobs would be {mm['missing'] + norep:+.4f}; if none did, {mm['missing']:+.4f}. Excess jobs at 1.0-1.5 times: "
               f"{mm['excess']:+.4f}.\n")
    ex = d[d["spec"].str.startswith("exploratory")]
    if len(ex):
        ex = ex.assign(label=ex["outcome"].map(LABELS).fillna(ex["outcome"]), b=ex["beta"].map(fmt), lo=ex["lo90"].map(fmt),
                       hi=ex["hi90"].map(fmt), p=ex["p_wild"].map(lambda x: f"{x:.3f}"))
        txt.append("## Exploratory: pre-period from 2017Q3 (D-055)\n")
        txt.append(table(ex, ["label", "b", "lo", "hi", "p"]))
    txt.append("## Main specification\n")
    txt.append(table(m, ["label", "beta", "lo90", "hi90", "p (wild)", "pre-period mean, zone", "pre-trend p"]))
    txt.append("\n## Robustness (estimate and wild bootstrap p)\n")
    r = d[d["outcome"].isin(["lnw", "emp_rate", "formal_rate", "formal_share", "i_to_f", "missing", "excess", "i_missing"])]
    piv = r.assign(cell=r["beta"].map(lambda x: f"{x:+.4f}") + " (" + r["p_wild"].map(lambda x: f"{x:.2f}") + ")") \
        .pivot(index="spec", columns="outcome", values="cell").reset_index()
    txt.append(table(piv, list(piv.columns)))
    txt.append("\n## Earnings bins (main specification, monthly, per person 15+)\n")
    b = bins[bins["measure"] == "monthly"].copy()
    b["beta"] = b["beta"].map(lambda x: f"{x:+.5f}")
    b["pre"] = b["pre_mean_zone"].map(lambda x: f"{x:.5f}")
    b["p"] = b["p_wild"].map(lambda x: f"{x:.3f}")
    txt.append(table(b, ["formality", "bin", "beta", "p", "pre"]))
    (OUT / "results.md").write_text("\n".join(txt) + "\n")
    print("\n".join(txt[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
