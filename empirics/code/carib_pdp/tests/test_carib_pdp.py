"""Checks for the Caribbean PDP report figures (D-072): data identities, consistency of the
pooled decomposition with the lp pipeline, chart parts, and the tracked-change helper.
This project's modules import their own config.py; they are loaded with this folder first on
sys.path and any other project's 'config' set aside."""
import importlib
import importlib.util
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from lxml import etree

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
DATA = ROOT / "empirics" / "output" / "carib_pdp" / "data"
LOCAL = ["config", "charts", "specs", "texts"]


@pytest.fixture(scope="module")
def mods():
    saved = {m: sys.modules.pop(m) for m in LOCAL if m in sys.modules}
    sys.path.insert(0, str(HERE))
    try:
        loaded = {m: importlib.import_module(m) for m in LOCAL}
        spec = importlib.util.spec_from_file_location("carib_pdp_insert", HERE / "05_insert_docx.py")
        ins = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ins)
        loaded["insert"] = ins
        yield loaded
    finally:
        sys.path.remove(str(HERE))
        for m in LOCAL:
            sys.modules.pop(m, None)
        sys.modules.update(saved)


def test_types_cover_caribbean16(mods):
    c = mods["config"]
    assert sorted(c.TYPE_OF) == sorted(c.CARIBBEAN16)
    assert sum(len(v) for v in c.TYPES.values()) == 16


def test_terms_add_up():
    g = pd.read_csv(DATA / "g1_decomposition.csv")
    assert np.allclose(g["within_pp"] + g["struct_pp"], g["growth_pp"], atol=1e-9)
    assert np.allclose(g["static_pp"] + g["dynamic_pp"], g["struct_pp"], atol=1e-9)


def test_country_terms_match_lp_outputs():
    g = pd.read_csv(DATA / "g1_decomposition.csv")
    lp = pd.read_csv(ROOT / "empirics" / "output" / "carib_lp" / "grid_A" / "main.csv")
    m = g[(g["unit"] == "country") & (g["base"] == "initial")].merge(lp, on=["iso3", "period"], suffixes=("", "_lp"))
    assert len(m) == 24
    assert np.allclose(m["struct_pp"], m["struct_pp_lp"]) and np.allclose(m["growth_pp"], m["growth_pp_lp"])


def test_single_country_pool_reproduces_country_terms(mods):
    """Pooling one country must give that country's own decomposition (initial-year prices)."""
    summ = mods["config"].load_lp("07_lac_summary")
    panel = summ.load_panel("A")
    lp = pd.read_csv(ROOT / "empirics" / "output" / "carib_lp" / "grid_A" / "main.csv").set_index(["iso3", "period"])
    for iso in ("JAM", "BHS", "GUY"):
        r, _ = summ.pooled_period(panel, [iso], 2000, 2019, "initial")
        assert r["struct"] == pytest.approx(lp.loc[(iso, "2000–2019"), "struct_pp"], abs=1e-9)
        assert r["growth"] == pytest.approx(lp.loc[(iso, "2000–2019"), "growth_pp"], abs=1e-9)


def test_cuba_never_pooled():
    g = pd.read_csv(DATA / "g1_decomposition.csv", keep_default_na=False)
    assert not g.loc[g["unit"] == "type", "members"].str.contains("CUB").any()
    s = pd.read_csv(DATA / "g2_sectors_types.csv")
    assert not s["members"].str.contains("CUB").any()


def test_sector_shares_and_relative_productivity():
    s = pd.read_csv(DATA / "g2_sectors_types.csv")
    assert np.allclose(s.groupby("type")["emp_share_pct"].sum(), 100)
    # employment-weighted mean of relative productivity is 1 by construction
    w = s.assign(x=s["emp_share_pct"] / 100 * s["rel_lp"]).groupby("type")["x"].sum()
    assert np.allclose(w, 1)


def test_texts_and_specs_build(mods):
    t = mods["texts"].figure_texts()
    assert t["graph1"]["title"].startswith("Caribbean (12 countries)")
    assert t["graph2"]["title"].startswith("Caribbean (11 countries)")
    p = mods["texts"].report_paragraphs()
    assert "34.5 percent" in p["3.2_after"][1]
    specs = mods["specs"].build_specs()
    for sp in specs.values():
        assert all(len(v) == len(sp.categories) for v in sp.series.values())


def test_word_chart_parts_are_schema_friendly(mods):
    specs = mods["specs"].build_specs()
    xml, xlsx = mods["charts"].word_chart_parts(specs["graph2b"])
    root = etree.fromstring(xml)
    c = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
    assert all(int(e.get("val")) >= 0 for e in root.iter(c + "axId"))
    assert root.find(f".//{c}valAx/{c}scaling/{c}logBase").get("val") == "10"
    assert root.find(f".//{c}catAx/{c}crossesAt").get("val") == "1.0"
    assert zipfile.ZipFile(io.BytesIO(xlsx)).testzip() is None


def test_tracked_replace(mods):
    ins = mods["insert"]
    W = ins.W
    p = etree.fromstring(f'<w:p xmlns:w="{ins.NS["w"]}"><w:r><w:t>Its database covers 20 countries, </w:t></w:r>'
                         '<w:r><w:t>against 367 in Brazil.</w:t></w:r></w:p>')
    ins.tracked_replace(p, "against 367 in Brazil.", "against 367 in Brazil (graph 4).", ins.Ids(0))
    assert p.find(f".//{W}del") is None                     # pure insertion: nothing deleted
    assert "".join(t.text for t in p.iter(W + "t")) == "Its database covers 20 countries, against 367 in Brazil (graph 4)."
    p = etree.fromstring(f'<w:p xmlns:w="{ins.NS["w"]}"><w:r><w:t>In an economy of 100 workers, five is five percent.</w:t></w:r></w:p>')
    ins.tracked_replace(p, "In an economy of 100 workers, five is five percent.", "In Saint Lucia, five is 0.1 percent.", ins.Ids(0))
    kept = "".join(t.text for t in p.iter(W + "t"))
    deleted = "".join(t.text for t in p.iter(W + "delText"))
    assert kept == "In Saint Lucia, five is 0.1 percent."
    assert deleted.strip() and "Saint" not in deleted
