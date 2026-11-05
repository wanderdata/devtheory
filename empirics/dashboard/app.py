"""Caribbean labour productivity dashboard (Streamlit).

Run locally:   streamlit run empirics/dashboard/app.py
Streamlit Community Cloud: main file path = empirics/dashboard/app.py
"""
import streamlit as st

st.set_page_config(page_title="Caribbean Labour Productivity", page_icon="📈", layout="wide")

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
        st.Page("views/ext_periods.py", title="Anchored period decompositions", url_path="periods"),
        st.Page("views/ext_annual.py", title="Annual decomposition, additive prices", url_path="annual"),
        st.Page("views/ext_structure.py", title="Reallocation and productivity gaps", url_path="reallocation"),
        st.Page("views/ext_data.py", title="Data quality and coverage", url_path="data-quality"),
    ],
}
st.navigation(pages).run()
