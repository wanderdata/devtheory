"""Smoke test: every page of the productivity app loads without an exception, in both regions."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")
PAGES = ["views/home.py", "views/explainer_unbalanced.py", "views/ref_regional.py", "views/ref_sectors.py", "views/ref_labour.py",
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


def test_explainer_presets_update_the_model():
    """Choosing a preset on the explainer page resets the controls and changes the results."""
    at = AppTest.from_file(APP, default_timeout=180)
    at.run()
    at.switch_page("views/explainer_unbalanced.py").run()
    slope = [m for m in at.metric if m.label.startswith("Relative-price slope")][0]
    assert slope.value == "-1.00"
    at.selectbox(key="ub_preset").set_value("Dual economy: informal wage gap and segmented wages").run()
    assert not at.exception
    assert at.slider(key="ub_rho").value == 0.45
    slope = [m for m in at.metric if m.label.startswith("Relative-price slope")][0]
    assert slope.value == "-0.50"
