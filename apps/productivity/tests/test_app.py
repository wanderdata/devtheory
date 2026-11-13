"""Smoke test: every page of the productivity app loads without an exception, in both regions."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")
PAGES = ["views/home.py", "views/ref_regional.py", "views/ref_sectors.py", "views/ref_labour.py",
         "views/ref_country.py", "views/ext_periods.py", "views/ext_annual.py", "views/ext_structure.py",
         "views/ext_working_age.py", "views/ext_ladder.py", "views/ext_data.py"]


@pytest.mark.parametrize("scope", ["lac", "carib"])
@pytest.mark.parametrize("page", PAGES)
def test_page_loads(scope, page):
    at = AppTest.from_file(APP, default_timeout=180)
    at.session_state["scope"] = scope
    at.run()
    at.switch_page(page).run()
    assert not at.exception, at.exception[0].message if at.exception else ""
