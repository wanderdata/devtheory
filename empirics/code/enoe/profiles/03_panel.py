"""Study 9.2, step 3: within-person earnings growth by experience (pre-analysis plan §4.3 and
amendment of 2026-11-13).

    python empirics/code/enoe/profiles/03_panel.py

Uses the linked panels of study 9.1 (empirics/data/raw/enoe_interim/<window>.parquet). Sample: men
who are full-time private-sector wage employees with positive hourly earnings at the first and
fifth visits and the same formality status at both. Annual growth of log hourly earnings by
experience bin at the first visit; the time effect is the mean growth of workers in the flat
spot (30-39 years) of the same formality status and window. The synthetic height at 20 years is
the sum over the bins 0-4 ... 15-19 of 5 x (growth in the bin - flat-spot growth).

Writes empirics/output/enoe/profiles/panel_growth.csv and panel_heights.csv.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ladders"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import enoe_link  # noqa: E402
import profiles_lib as pl  # noqa: E402
from enoe_config import INTERIM, OUTPUT_ROOT, WINDOWS  # noqa: E402

OUT = OUTPUT_ROOT / "profiles"
NBOOT, SEED = 199, 20261113
COLS = ["eda", "sex", "anios_esc", "ing_x_hrs", "hrsocup", "pos_ocu", "ambito2", "emp_ppal", "clase2", "fac_tri",
        "ent", "upm"]
BELOW = ["0-4", "5-9", "10-14", "15-19"]
FLAT = ["30-34", "35-39"]


def sample(panel):
    p = panel.copy()
    for c in COLS:
        if c in p.columns and c not in ("ent", "upm"):
            p[c] = pd.to_numeric(p[c], errors="coerce")
    w = enoe_link.wide(p, [c for c in COLS if c in p.columns])
    ok = pd.Series(True, index=w.index)
    for t in (0, 4):
        ok &= ((w[f"clase2_{t}"] == 1) & (w[f"pos_ocu_{t}"] == 1) & (w[f"ambito2_{t}"] != 7)
               & (w[f"sex_{t}"] == 1) & (w[f"hrsocup_{t}"] >= 35) & (w[f"ing_x_hrs_{t}"] > 0))
    ok &= w["emp_ppal_0"] == w["emp_ppal_4"]
    x = w[ok].copy()
    school = x["anios_esc_0"].where(x["anios_esc_0"].between(0, 24))
    x["exp"] = pl.experience(x["eda_0"], school)
    x = x[x["exp"].between(0, 40) & school.notna()]
    x["bin"] = pd.cut(x["exp"], pl.BINS + [41], right=False, labels=pl.LABELS + ["35-39"], ordered=False).astype(str)
    x["g"] = np.log(x["ing_x_hrs_4"] / x["ing_x_hrs_0"])
    x["formality"] = x["emp_ppal_0"].map({1: "informal", 2: "formal"})
    x["w"], x["psu"], x["year"], x["ent"] = x["fac_tri_0"], x["upm_0"].astype(str), 0, x["ent_0"].astype(str)
    return x


def synthetic(x):
    m = x.groupby("bin").apply(lambda g: np.average(g["g"], weights=g["w"]), include_groups=False)
    f = x[x["bin"].isin(FLAT)]
    flat = np.average(f["g"], weights=f["w"])
    h = 5 * sum(m.get(b, np.nan) - flat for b in BELOW)
    return pd.Series({"20-24": h, **{f"growth {b}": m.get(b, np.nan) for b in pl.LABELS}, "growth flat": flat})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, hs = [], []
    for win in WINDOWS:
        f = INTERIM / f"{win}.parquet"
        if not f.exists():
            continue
        x = sample(pd.read_parquet(f))
        for typ, g in [("all stayers", x), ("formal", x[x["formality"] == "formal"]),
                       ("informal", x[x["formality"] == "informal"])]:
            s = synthetic(g)
            draws = pl.psu_bootstrap(g, synthetic, NBOOT, SEED)
            v = [np.exp(dr["20-24"]) - 1 for dr in draws]
            hs.append({"window": win, "group": typ, "n": len(g), "log_height": s["20-24"],
                       "height": np.exp(s["20-24"]) - 1, "lo90": np.percentile(v, 5), "hi90": np.percentile(v, 95),
                       "flat_spot_growth": s["growth flat"]})
            for b in pl.LABELS:
                nb = int((g["bin"] == b).sum())
                rows.append({"window": win, "group": typ, "bin": b, "n": nb, "mean_growth": s[f"growth {b}"]})
            print(f"{win} {typ:12s} n={len(g):,} synthetic height 20-24: {np.exp(s['20-24']) - 1:.3f}")
    pd.DataFrame(rows).to_csv(OUT / "panel_growth.csv", index=False)
    pd.DataFrame(hs).to_csv(OUT / "panel_heights.csv", index=False)


if __name__ == "__main__":
    main()
