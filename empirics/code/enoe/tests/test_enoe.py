"""Tests for the ENOE study's code on synthetic data with ENOE's variable names (no microdata
are committed). They check file-name matching, linking rules, states, rates and the
decomposition against cases with known answers."""
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import enoe_io  # noqa: E402
import enoe_flows as flows  # noqa: E402
import enoe_link as link  # noqa: E402
from enoe_config import KEY  # noqa: E402


# ------------------------------------------------------------- file names ---

@pytest.mark.parametrize("name,year,q,ok", [
    ("sdemt419.csv", 2019, 4, True),
    ("SDEMT419.CSV", 2019, 4, True),
    ("ENOE_SDEMT119.csv", 2019, 1, True),
    ("ENOEN_SDEMT123.csv", 2023, 1, True),
    ("conjunto_de_datos_sdem_enoe_2023_1t.csv", 2023, 1, True),
    ("conjunto_de_datos_sdem_enoe_2023_2t.csv", 2023, 1, False),
    ("sdemt4190.csv", 2019, 4, False),
    ("coe1t419.csv", 2019, 4, False),
    ("sdemt419.dbf", 2019, 4, False),
])
def test_file_names(name, year, q, ok):
    assert enoe_io._match(name, "sdem", year, q) is ok


def test_read_from_zip(tmp_path):
    df = pd.DataFrame({"CD_A": [1], "ENT": [9], "EDA": [30]})
    with zipfile.ZipFile(tmp_path / "enoe_2019_trim4_csv.zip", "w") as z:
        z.writestr("ENOE_SDEMT419.csv", df.to_csv(index=False))
        z.writestr("ENOE_COE1T419.csv", "x\n1\n")
    out = enoe_io.read("sdem", 2019, 4, raw=tmp_path)
    assert list(out.columns[:3]) == ["cd_a", "ent", "eda"] and out["year"].iloc[0] == 2019


# ---------------------------------------------------------------- linking ---

def person(i, n_ent, eda, sex=1, **kw):
    r = dict(cd_a=1, ent=9, con=100 + i // 10, v_sel=1, n_hog=1, h_mud=0, n_ren=i % 10 + 1,
             n_ent=n_ent, eda=eda, sex=sex, clase2=1, rama_est2=3, ambito2=6, emp_ppal=2, fac_tri=100)
    r.update(kw)
    return r


def test_link_rules():
    a = pd.DataFrame([person(0, 1, 30), person(1, 2, 40), person(2, 3, 50), person(3, 5, 60),
                      person(4, 2, 25)])
    b = pd.DataFrame([person(0, 2, 30),            # same age: ok
                      person(1, 3, 41),            # ok
                      person(2, 4, 50, sex=2),     # sex changes: rejected
                      person(4, 3, 29)])           # age +4: rejected
    # person 3 was in the fifth visit: not eligible
    m, d = link.link(a, b)
    assert set(m["n_ren"]) == {1, 2}
    assert d["eligible"] == 4 and d["accepted"] == 2 and d["bad_sex"] == 1 and d["bad_age"] == 1
    assert d["match_rate"] == pytest.approx(0.5)


def test_link_requires_next_visit_and_unique_keys():
    a = pd.DataFrame([person(0, 1, 30), person(1, 1, 30), person(1, 1, 31)])   # person 1 duplicated
    b = pd.DataFrame([person(0, 3, 30), person(1, 2, 30)])                     # person 0 skips a visit
    m, d = link.link(a, b)
    assert len(m) == 0 and d["dup_origin"] == 2


def test_chain_follows_sequences():
    q = [pd.DataFrame([person(0, 1 + t, 30), person(1, 2 + t, 40)]) for t in range(3)]
    q[2] = q[2][q[2]["n_ren"] == 1]                                            # person 1 leaves after visit 3
    panel, diags = link.chain(q)
    assert len(diags) == 2
    w = link.wide(panel, ["eda"])
    assert w.notna().sum(axis=1).sort_values().tolist() == [2, 3]


def test_chain_does_not_join_different_people_with_the_same_key():
    # person A is in visits 4-5 in quarters 0-1; a new dwelling reuses the key from quarter 2 (visit 1)
    q0 = pd.DataFrame([person(0, 4, 30)])
    q1 = pd.DataFrame([person(0, 5, 30)])
    q2 = pd.DataFrame([person(0, 1, 55, sex=2)])
    panel, _ = link.chain([q0, q1, q2])
    assert panel["pid"].nunique() == 2
    assert panel.loc[panel["pos"] == 2, "pid"].iloc[0] != panel.loc[panel["pos"] == 0, "pid"].iloc[0]


# ----------------------------------------------------------------- flows ---

def test_state_and_rates():
    df = pd.DataFrame({"clase2": [1, 1, 2, 1], "rama_est2": [3, 3, 3, 5], "ambito2": [6, 1, 6, 4],
                       "emp_ppal": [2, 1, 2, 1]})
    s = flows.state(df)
    assert s.iloc[0] == "3|large|formal" and s.iloc[1] == "3|micro, no premises|informal" and s.iloc[2] == "N"
    o = pd.Series(["A", "A", "A", "B", "N"])
    d = pd.Series(["A", "N", "B", "N", "A"])
    r = flows.rates(o, d, pd.Series([1, 1, 2, 1, 1.0]), o)
    assert r.loc["A", "exit"] == pytest.approx(0.25) and r.loc["A", "persist"] == pytest.approx(0.25)
    assert r.loc["B", "exit"] == 1.0 and "N" not in r.index


def test_upward():
    rank = {"low": 1, "mid": 2, "high": 3}
    up = flows.upward(pd.Series(["low", "mid", "mid", "high", "x"]), pd.Series(["mid", "low", "N", "high", "low"]), rank)
    assert up.iloc[:4].tolist() == [1.0, 0.0, 0.0, 0.0] and np.isnan(up.iloc[4])


def test_decomposition_identifies_the_dimension_that_matters():
    rng = np.random.default_rng(0)
    n = 20000
    sector = rng.integers(0, 5, n)
    sizeform = rng.integers(0, 6, n)
    p = 0.05 + 0.10 * sizeform / 5                 # outcome depends on size x formality only
    y = (rng.random(n) < p).astype(float)
    d = flows.decompose(y, sector, sizeform, np.ones(n))
    assert d["shapley_sizeform"] > 10 * max(d["shapley_sector"], 1e-6)
    assert d["shapley_sector"] + d["shapley_sizeform"] == pytest.approx(d["r2_both"])


# ------------------------------------------------------- pipeline smoke ---

def synthetic_panel(n=3000, seed=1):
    """Five quarters of a rotating panel where informal and micro jobs churn more, by design."""
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        v1 = rng.integers(1, 6)                       # visit at the first quarter
        formal, size, sector = rng.integers(1, 3), rng.choice([1, 4, 6]), rng.integers(1, 6)
        emp = True
        for t in range(5):
            if v1 + t > 5:
                break
            p_exit = 0.02 if (formal == 2 and size == 6) else 0.15
            if t > 0:
                emp = (rng.random() > p_exit) if emp else (rng.random() < 0.3)
            rows.append(dict(cd_a=1 + i % 3, ent=1 + i % 4, con=i, v_sel=1, n_hog=1, h_mud=0, n_ren=1,
                             n_ent=v1 + t, pos=t, eda=30, sex=1, clase2=1 if emp else 2, rama_est2=sector,
                             ambito2=size, emp_ppal=formal, fac_tri=100.0, upm=i // 10, n_inf=1,
                             ing_x_hrs=20.0 * formal * size, pos_ocu=1, p3r_anio=2010, p3r_mes=1))
    df = pd.DataFrame(rows)
    return [df[df["pos"] == t].drop(columns="pos") for t in range(5)]


def test_pipeline_on_synthetic_panel():
    import importlib
    f2 = importlib.import_module("02_flows")
    panel, diags = link.chain(synthetic_panel())
    assert (diags["match_rate"] > 0.99).all()
    p = f2.prepare(panel)
    q = f2.quarterly_rates(p, "test")
    assert q["exit_rate"].between(0, 1).all()
    w = f2.annual(p)
    assert len(w) and w["exit_y"].isin([0, 1]).all()
    cells = f2.by_cell(w, "sizeform")
    big = cells.set_index("sizeform")
    assert big.loc["large|formal", "exit_y"] < big.loc["micro, no premises|informal", "exit_y"]
    r = f2.boot_decomp(w, "exit_y", nboot=20)
    assert r["shapley_sizeform"] > r["shapley_sector"] and r["diff_lo90"] > 0
    m = f2.misreport(p)
    assert (m["size_changes"] == 0).all() and (m["formality_changes"] == 0).all()
