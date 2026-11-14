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
        st.Page("views/s3_ladder.py", title="9.3 A productivity ladder for Mexico", url_path="ladder"),
        st.Page("views/s4_border.py", title="9.4 The 2019 border minimum wage", url_path="border"),
        st.Page("views/s5_first_jobs.py", title="9.5 Where careers start", url_path="first-jobs"),
    ],
}
st.navigation(pages).run()
