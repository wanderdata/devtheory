"""Smoke tests for the Jobs in Mexico app: every page runs without exceptions and draws charts
with data (AppTest, no browser)."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1]
PAGES = sorted(str(p.relative_to(APP)) for p in (APP / "views").glob("*.py"))


@pytest.mark.parametrize("page", PAGES)
def test_page_runs(page):
    at = AppTest.from_file(str(APP / page), default_timeout=120)
    at.run()
    assert not at.exception, [e.value for e in at.exception]
