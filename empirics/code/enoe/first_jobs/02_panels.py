"""Study 9.5, step 2: five-interview histories of young people who had never worked and were not
employed at their first interview (pre-analysis plan §2).

    python empirics/code/enoe/first_jobs/02_panels.py

For every quarter t whose next four quarters are available within the same period, persons at
their first interview (n_ent = 1) aged 15-29, not employed and never having worked, are linked
through t+1, ..., t+4 with the study 9.1 linkage. Writes the uncommitted cohorts.parquet (one row
per person: controls at the first interview, state and job at each later interview) and
empirics/output/enoe/first_jobs/linkage.csv.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parent))

import importlib  # noqa: E402

import pandas as pd  # noqa: E402

import enoe_link  # noqa: E402
from enoe_config import KEY  # noqa: E402

ex = importlib.import_module("01_extract")
TMP, OUT = ex.TMP, ex.OUT
CONTROLS = ["ent", "eda", "sex", "par_c", "anios_esc", "cs_p17", "hh_formal", "hh_informal", "hh_adults", "urban", "upm", "fac",
            "year", "q"]
TRACK = ["state", "never", "pos_ocu", "ambito2", "rama_est2", "ingocup", "hrsocup", "salario"]


def load(y, q):
    f = TMP / f"q_{y}_{q}.parquet"
    return pd.read_parquet(f) if f.exists() else None


def follow(start, frames):
    """Link the cohort `start` (rows of the first quarter) through the next frames."""
    cur = start.copy()
    out = start[CONTROLS + TRACK].add_suffix("_1").reset_index(drop=True)
    out["linked_1"] = True
    pos = pd.Series(range(len(start)), index=start.index)          # row of `out` for each row of `cur`
    diags = []
    for v, b in enumerate(frames, start=2):
        key = KEY + (["tipo"] if "tipo" in cur.columns and "tipo" in b.columns else [])
        m, d = enoe_link.link(cur, b, key)
        d["visit"] = v
        diags.append(d)
        rows = pos.loc[m["_row_0"].to_numpy()].to_numpy()
        for c in TRACK:
            out.loc[rows, f"{c}_{v}"] = m[f"{c}_1"].to_numpy()
        out[f"linked_{v}"] = False
        out.loc[rows, f"linked_{v}"] = True
        cur = b.loc[m["_row_1"].to_numpy()].copy()
        pos = pd.Series(rows, index=cur.index)
    return out, diags


def main():
    cohorts, diags = [], []
    for era, qs in ex.ERAS.items():
        cache = {}
        for i, (y, q) in enumerate(qs):
            window = qs[i:i + 5]
            if len(window) < 5:
                break
            frames = [cache.get(w) if w in cache else cache.setdefault(w, load(*w)) for w in window]
            if any(f is None for f in frames):
                continue
            f0 = frames[0]
            start = f0[(f0["n_ent"] == 1) & f0["eda"].between(15, 29) & (f0["state"] == "N") & f0["never"]]
            out, d = follow(start, frames[1:])
            out["era"], out["start"] = era, f"{y}Q{q}"
            cohorts.append(out)
            for x in d:
                x.update({"start": f"{y}Q{q}", "era": era})
            diags += d
            cache.pop(window[0], None)
            print(y, q, len(start), int(out["linked_5"].sum()), flush=True)
    c = pd.concat(cohorts, ignore_index=True)
    c.to_parquet(TMP / "cohorts.parquet", index=False)
    pd.DataFrame(diags).to_csv(OUT / "linkage.csv", index=False)
    print(len(c), "persons;", int(c["linked_5"].sum()), "linked to the fifth interview")
    return 0


if __name__ == "__main__":
    sys.exit(main())
