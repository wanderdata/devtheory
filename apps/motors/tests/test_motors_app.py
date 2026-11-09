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
