"""Jobs in Mexico: which jobs carry productivity and upward mobility? (Streamlit app, WP09)

Run locally:   streamlit run apps/jobs_mexico/app.py
Streamlit Community Cloud: main file path = apps/jobs_mexico/app.py
"""
import streamlit as st

st.set_page_config(page_title="Jobs in Mexico", page_icon="🪜", layout="wide")

pages = {
    "Overview": [st.Page("views/overview.py", title="The programme", default=True)],
    "Studies": [
        st.Page("views/s1_ladders.py", title="9.1 Which jobs are rungs?", url_path="rungs"),
        st.Page("views/s2_profiles.py", title="9.2 Which jobs build skills?", url_path="skills"),
    ],
}
st.navigation(pages).run()
