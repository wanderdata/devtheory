"""Jobs in Mexico: which jobs carry productivity and upward mobility? (Streamlit app, WP09)

Run locally:   streamlit run apps/jobs_mexico/app.py
Streamlit Community Cloud: main file path = apps/jobs_mexico/app.py
"""
import streamlit as st

st.set_page_config(page_title="Jobs in Mexico", page_icon="🪜", layout="wide")

pages = {
    "Overview": [st.Page("views/overview.py", title="The programme", default=True)],
    "Studies": [
        st.Page("views/s1_ladders.py", title="9.1 Job transitions by sector, establishment size and formality", url_path="rungs"),
        st.Page("views/s2_profiles.py", title="9.2 Experience–earnings profiles by type of job", url_path="skills"),
        st.Page("views/s3_ladder.py", title="9.3 Productivity ladder with formal and informal segments", url_path="ladder"),
        st.Page("views/s4_border.py", title="9.4 The 2019 minimum-wage increase in the northern border zone", url_path="border"),
        st.Page("views/s5_first_jobs.py", title="9.5 First jobs and employment three quarters later", url_path="first-jobs"),
        st.Page("views/s6_states.py", title="9.6 Job mobility and growth across states", url_path="states"),
        st.Page("views/s7_state_productivity.py", title="9.7 Labour productivity growth by state and activity",
                url_path="state-productivity"),
        st.Page("views/s8_minimum_wage_bite.py", title="9.8 Minimum-wage increases of 2019–2024 by state and activity",
                url_path="minimum-wage"),
    ],
}
st.navigation(pages).run()
