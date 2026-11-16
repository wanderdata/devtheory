"""Study 9.6, step 2: one-year histories (first to fifth interview) of persons aged 16-65
(pre-analysis plan §2).

    python empirics/code/enoe/states/02_panels.py

For every starting quarter whose next four quarters are available within the same period, persons
at their first interview are linked through the fifth with the study 9.1 linkage. Writes the
uncommitted panels.parquet (state, sector and log hourly earnings at the first and fifth
interviews) and empirics/output/enoe/states/linkage.csv.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import pandas as pd  # noqa: E402

import enoe_link  # noqa: E402
from enoe_config import INTERIM, KEY, OUTPUT_ROOT  # noqa: E402

OUT = OUTPUT_ROOT / "states"
TMP = INTERIM / "states"
ERAS = {"2005-2019": [(y, q) for y in range(2005, 2020) for q in (1, 2, 3, 4)],
        "2022-": [(y, q) for y in range(2022, 2027) for q in (1, 2, 3, 4)]}
FIRST = ["ent_i", "eda", "sex", "anios_esc", "state", "rama_est2", "lnw", "fac", "upm", "urban"]
LAST = ["state", "rama_est2", "lnw"]


def load(y, q):
    f = TMP / f"q_{y}_{q}.parquet"
    return pd.read_parquet(f) if f.exists() else None


def follow(start, frames):
    """Link `start` through `frames`; returns first-interview columns, fifth-interview columns
    (suffix _5) for those linked at every step, and the diagnostics."""
    cur = start.assign(_id=range(len(start)))
    diags = []
    for v, b in enumerate(frames, start=2):
        key = KEY + (["tipo"] if "tipo" in cur.columns and "tipo" in b.columns else [])
        m, d = enoe_link.link(cur, b, key)
        d["visit"] = v
        diags.append(d)
        nxt = b.loc[m["_row_1"].to_numpy()].copy()
        nxt["_id"] = m["_id"].to_numpy()          # only the cohort frame has _id, so no suffix
        cur = nxt
    out = start[FIRST].reset_index(drop=True)
    out["linked_5"] = False
    fifth = cur.set_index("_id")[LAST].add_suffix("_5")
    out = out.join(fifth)
    out.loc[fifth.index, "linked_5"] = True
    return out, diags


def main():
    parts, diags = [], []
    for era, qs in ERAS.items():
        cache = {}
        for i, (y, q) in enumerate(qs):
            window = qs[i:i + 5]
            if len(window) < 5:
                break
            frames = [cache[w] if w in cache else cache.setdefault(w, load(*w)) for w in window]
            if any(f is None for f in frames):
                continue
            f0 = frames[0]
            start = f0[(f0["n_ent"] == 1) & f0["eda"].between(16, 65)]
            out, d = follow(start, frames[1:])
            out["era"], out["start_year"], out["start_q"] = era, y, q
            parts.append(out)
            for x in d:
                x.update({"start": f"{y}Q{q}", "era": era})
            diags += d
            cache.pop(window[0], None)
            print(y, q, len(start), int(out["linked_5"].sum()), flush=True)
    p = pd.concat(parts, ignore_index=True)
    p.to_parquet(TMP / "panels.parquet", index=False)
    pd.DataFrame(diags).to_csv(OUT / "linkage.csv", index=False)
    print(len(p), "persons;", int(p["linked_5"].sum()), "linked to the fifth interview")
    return 0


if __name__ == "__main__":
    sys.exit(main())
