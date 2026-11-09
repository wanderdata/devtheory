"""Labour productivity and structural change in Latin America and the Caribbean
(Streamlit dashboard).

Run locally:   streamlit run empirics/dashboard/app.py
Streamlit Community Cloud: main file path = empirics/dashboard/app.py

The region (Latin America and the Caribbean, or the Caribbean) is chosen once in
the sidebar and applies to every page; it is kept per session in
st.session_state["scope"].
"""
import streamlit as st

from lib import SCOPES

st.set_page_config(page_title="LAC Labour Productivity", page_icon="📈", layout="wide")

st.sidebar.selectbox(
    "Region", list(SCOPES), format_func=lambda s: SCOPES[s]["label"], key="scope",
    help="Latin America and the Caribbean: the 33 member States of ECLAC in the region. "
         "Caribbean: the 16 member States served by ECLAC's Port of Spain office (includes Cuba, "
         "the Dominican Republic and Haiti). Every page uses the region chosen here.")

pages = {
    "Overview": [
        st.Page("views/home.py", title="About this dashboard", default=True),
    ],
    "Baseline (McMillan & Rodrik)": [
        st.Page("views/ref_regional.py", title="Regional productivity", url_path="regional"),
        st.Page("views/ref_sectors.py", title="Sectors and structural change", url_path="sectors"),
        st.Page("views/ref_labour.py", title="Employment", url_path="employment"),
        st.Page("views/ref_country.py", title="Country profile", url_path="country"),
    ],
    "Extended analysis": [
        st.Page("views/ext_periods.py", title="Period decompositions", url_path="periods"),
        st.Page("views/ext_annual.py", title="Annual decomposition, additive prices", url_path="annual"),
        st.Page("views/ext_structure.py", title="Reallocation and productivity gaps", url_path="reallocation"),
        st.Page("views/ext_data.py", title="Data quality and coverage", url_path="data-quality"),
    ],
}
st.navigation(pages).run()
