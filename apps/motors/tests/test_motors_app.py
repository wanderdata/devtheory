"""Smoke test: every page of the motors app loads without an exception."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")
PAGES = ["views/home.py", "views/q1_still.py", "views/q2_lac.py", "views/q3_conditions.py", "views/q4_sectors.py",
         "views/robustness.py", "views/replication.py", "views/data.py"]


@pytest.mark.parametrize("page", PAGES)
def test_page_loads(page):
    at = AppTest.from_file(APP, default_timeout=180)
    at.run()
    at.switch_page(page).run()
    assert not at.exception, at.exception[0].message if at.exception else ""


def _values(v):
    """Plotly arrays come as lists or, for numbers, as {'dtype': ..., 'bdata': base64}."""
    import base64

    import numpy as np
    if isinstance(v, dict) and "bdata" in v:
        return list(np.frombuffer(base64.b64decode(v["bdata"]), dtype=np.dtype(v["dtype"])))
    return list(v) if isinstance(v, list) else []


@pytest.mark.parametrize("page", PAGES)
def test_charts_have_drawable_axes(page):
    """Guard against blank charts (the overview chart was blank on 2026-11-09): every chart must
    have data points, and a chart mixing legend-only traces (no values) with category labels must
    declare its axis as categorical, or Plotly guesses a numeric axis and draws nothing."""
    import json
    at = AppTest.from_file(APP, default_timeout=180)
    at.run()
    at.switch_page(page).run()
    for el in at.get("plotly_chart"):
        fig = json.loads(el.proto.spec)
        traces = fig.get("data", [])
        pts = [v for t in traces for k in ("x", "y", "z") for v in _values(t.get(k)) if v is not None]
        assert pts, f"{page}: a chart has no data points"
        for ax in ("x", "y"):
            empty = [t for t in traces if t.get(ax) is not None and all(v is None for v in _values(t.get(ax)))]
            cat = any(any(isinstance(v, str) for v in _values(t.get(ax))) for t in traces)
            if empty and cat:
                typ = fig.get("layout", {}).get(f"{ax}axis", {}).get("type")
                assert typ == "category", f"{page}: legend-only traces with an untyped categorical {ax} axis"
