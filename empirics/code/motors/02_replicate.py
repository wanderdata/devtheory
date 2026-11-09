"""Step 1: replicate Szirmai & Verspagen (2015), 1950-2005 (periods starting 1950-2000).

Writes empirics/output/motors/replication/:
    table2.csv   RE, FE, HT, BE without interactions (S&V Table 2)
    table3.csv   HT with MANxRELUS and MANxEDU (S&V Table 3)
    table4.csv   HT with subperiod slope shifts 1950-70, 1970-90, 1990-2005 (S&V Table 4)
    comparison.csv   our key coefficients next to S&V's, with a verdict per item (D-037 criteria)
"""
import pandas as pd

from config import OUTPUT, SUBPERIODS_SV
from models import add_terms, fit, load_panel, sample, tidy

OUT = OUTPUT / "replication"

# S&V published values (Tables 2-4), from the published article (L120)
SV = {
    ("table2", "HT", "MAN"): 0.045, ("table2", "RE", "MAN"): 0.045, ("table2", "FE", "MAN"): 0.065,
    ("table2", "BE", "MAN"): 0.063, ("table2", "HT", "RELUS"): -7.181,
    ("table3", "(2) +MANxREL", "MAN"): 0.087, ("table3", "(2) +MANxREL", "MANxREL"): -0.118,
    ("table3", "(3) +MANxREL+MANxEDU", "MAN"): -0.020, ("table3", "(3) +MANxREL+MANxEDU", "MANxREL"): -0.241,
    ("table3", "(3) +MANxREL+MANxEDU", "MANxEDU"): 0.027,
    ("table4", "(1) no interactions", "MAN[1950–70]"): -0.029, ("table4", "(1) no interactions", "MAN[1970–90]"): 0.056,
    ("table4", "(1) no interactions", "MAN[1990–2005]"): 0.035,
    ("table4", "(3) interactions", "MANxREL[1950–70]"): -0.428, ("table4", "(3) interactions", "MANxREL[1970–90]"): -0.318,
    ("table4", "(3) interactions", "MANxREL[1990–2005]"): -0.441,
    ("table4", "(3) interactions", "MANxEDU[1950–70]"): 0.048, ("table4", "(3) interactions", "MANxEDU[1970–90]"): 0.024,
    ("table4", "(3) interactions", "MANxEDU[1990–2005]"): 0.030,
}
SV_SIG = {("table2", "HT", "MAN"): True, ("table2", "RE", "MAN"): True, ("table2", "FE", "MAN"): False,
          ("table2", "BE", "MAN"): True, ("table2", "HT", "RELUS"): True,
          ("table3", "(2) +MANxREL", "MAN"): True, ("table3", "(2) +MANxREL", "MANxREL"): True,
          ("table3", "(3) +MANxREL+MANxEDU", "MAN"): False, ("table3", "(3) +MANxREL+MANxEDU", "MANxREL"): True,
          ("table3", "(3) +MANxREL+MANxEDU", "MANxEDU"): True,
          ("table4", "(1) no interactions", "MAN[1950–70]"): False, ("table4", "(1) no interactions", "MAN[1970–90]"): True,
          ("table4", "(1) no interactions", "MAN[1990–2005]"): False,
          ("table4", "(3) interactions", "MANxREL[1950–70]"): True, ("table4", "(3) interactions", "MANxREL[1970–90]"): True,
          ("table4", "(3) interactions", "MANxREL[1990–2005]"): True,
          ("table4", "(3) interactions", "MANxEDU[1950–70]"): True, ("table4", "(3) interactions", "MANxEDU[1970–90]"): True,
          ("table4", "(3) interactions", "MANxEDU[1990–2005]"): True}


def subperiod_masks(d, subs):
    return {lab: d["period"].isin(list(r)) for lab, r in subs.items()}


def replicate(p, sname):
    d = sample(p, sname, start=1950, end=2000, edu="EDU")
    t2 = []
    for est in ["RE", "FE", "HT", "BE"]:
        dd, terms = add_terms(d)
        t2.append(tidy(fit(dd, terms, est), est, {"sample": sname}))
    t3 = []
    for lab, inter in [("(1) base", ()), ("(2) +MANxREL", ("REL",)), ("(3) +MANxREL+MANxEDU", ("REL", "EDU"))]:
        dd, terms = add_terms(d, interactions=inter)
        t3.append(tidy(fit(dd, terms, "HT"), lab, {"sample": sname}))
    t4 = []
    for lab, inter in [("(1) no interactions", ()), ("(2) +MANxREL", ("REL",)), ("(3) interactions", ("REL", "EDU"))]:
        dd, terms = add_terms(d, interactions=inter, slope_groups=subperiod_masks(d, SUBPERIODS_SV))
        t4.append(tidy(fit(dd, terms, "HT"), lab, {"sample": sname}))
    return pd.concat(t2), pd.concat(t3), pd.concat(t4)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    p = load_panel()
    allt = {"table2": [], "table3": [], "table4": []}
    rows = []
    for sname in ["main", "excl_cpe", "core"]:
        t2, t3, t4 = replicate(p, sname)
        for k, t in zip(allt, (t2, t3, t4)):
            allt[k].append(t)
        tabs = {"table2": t2.set_index(["model", "term"]), "table3": t3.set_index(["model", "term"]),
                "table4": t4.set_index(["model", "term"])}
        for (tab, model, term), sv in SV.items():
            r = tabs[tab].loc[(model, term)]
            ours_sig = r["p"] < 0.10
            same_sign = (r["coef"] > 0) == (sv > 0)
            verdict = ("replicated" if same_sign and ours_sig == SV_SIG[(tab, model, term)]
                       else "same sign, different significance" if same_sign else "different sign")
            rows.append({"sample": sname, "table": tab, "model": model, "term": term, "sv_coef": sv,
                         "sv_significant": SV_SIG[(tab, model, term)], "coef": r["coef"], "se": r["se"],
                         "p": r["p"], "verdict": verdict, "nobs": int(r["nobs"]), "ncountries": int(r["ncountries"])})
    for k, v in allt.items():
        pd.concat(v).to_csv(OUT / f"{k}.csv", index=False)
    comp = pd.DataFrame(rows)
    comp.to_csv(OUT / "comparison.csv", index=False)
    print(comp.pivot_table(index=["table", "model", "term"], columns="sample", values="verdict", aggfunc="first",
                           sort=False).to_string())


if __name__ == "__main__":
    main()
