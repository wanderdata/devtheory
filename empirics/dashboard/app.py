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
    "Reference analysis (ECLAC format)": [
        st.Page("views/ref_regional.py", title="Regional productivity"),
        st.Page("views/ref_sectors.py", title="Sectors and structural change"),
        st.Page("views/ref_labour.py", title="Employment"),
        st.Page("views/ref_country.py", title="Country profile"),
    ],
    "Extended analysis (beyond the reference)": [
        st.Page("views/ext_periods.py", title="Anchored period decompositions"),
        st.Page("views/ext_annual.py", title="Annual decomposition, additive prices"),
        st.Page("views/ext_structure.py", title="Reallocation and productivity gaps"),
        st.Page("views/ext_data.py", title="Data quality and coverage"),
    ],
}
st.navigation(pages).run()
