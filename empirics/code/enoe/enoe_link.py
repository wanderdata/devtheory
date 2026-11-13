"""Linking ENOE respondents across consecutive quarters (pre-analysis plan §3).

A person is identified by KEY within a quarter; between consecutive quarters the visit number
N_ENT rises by one. A link is accepted only if sex is the same, age changes by -1 to +2 years,
and both the origin and the destination key are unique.
"""
import numpy as np
import pandas as pd

from enoe_config import KEY


def unique_keys(df, key=KEY):
    """Keep rows whose key is unique within the quarter; return (kept, number dropped)."""
    dup = df.duplicated(key, keep=False)
    return df[~dup], int(dup.sum())


def link(a, b, key=KEY):
    """Link quarter a to the next quarter b. Returns the merged pairs (suffixes _0 and _1, with
    the original row labels in _row_0 and _row_1) and a dict of diagnostics: candidates,
    accepted, rejected for sex or age, and the match rate among people in a who were not in
    their last (fifth) visit."""
    a = a.assign(_row=a.index)
    b = b.assign(_row=b.index)
    a, da = unique_keys(a, key)
    b, db = unique_keys(b, key)
    m = a.merge(b, on=key, suffixes=("_0", "_1"))
    m = m[m["n_ent_1"] == m["n_ent_0"] + 1]
    ok_sex = m["sex_0"] == m["sex_1"]
    dage = m["eda_1"] - m["eda_0"]
    ok_age = dage.between(-1, 2)
    eligible = int((a["n_ent"] < 5).sum())
    diag = {"origin": len(a), "eligible": eligible, "dup_origin": da, "dup_dest": db,
            "candidates": len(m), "bad_sex": int((~ok_sex).sum()), "bad_age": int((ok_sex & ~ok_age).sum())}
    m = m[ok_sex & ok_age]
    diag["accepted"] = len(m)
    diag["match_rate"] = len(m) / eligible if eligible else np.nan
    return m.reset_index(drop=True), diag


def chain(quarters, key=KEY):
    """Link a list of consecutive quarterly frames. Returns a long panel (one row per person and
    quarter, with a person id `pid` and the quarter's position `pos` in the list) and the
    diagnostics of each link. A person keeps an id only through accepted links, so two people
    who share a key at different points of the rotation never get the same id."""
    frames, diags = [], []
    prev, next_id = None, 0
    for i, q in enumerate(quarters):
        q = q.reset_index(drop=True).copy()
        pid = pd.Series(-1, index=q.index)
        if prev is not None:
            m, d = link(prev, q, key)
            d["from"] = i - 1
            diags.append(d)
            pid.loc[m["_row_1"].to_numpy()] = prev.loc[m["_row_0"].to_numpy(), "pid"].to_numpy()
        new = pid == -1
        pid[new] = np.arange(next_id, next_id + int(new.sum()))
        next_id += int(new.sum())
        q["pid"], q["pos"] = pid.astype(int), i
        frames.append(q)
        prev = q.drop(columns=["pos"])
    return pd.concat(frames, ignore_index=True), pd.DataFrame(diags)


def wide(panel, cols):
    """One row per person with columns `col_pos` for each requested column and position."""
    w = panel.pivot_table(index="pid", columns="pos", values=cols, aggfunc="first", dropna=False)
    w.columns = [f"{c}_{p}" for c, p in w.columns]
    want = [f"{c}_{p}" for c in cols for p in sorted(panel["pos"].unique())]
    return w.reindex(columns=want)
