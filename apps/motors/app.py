"""Development motors: is manufacturing (still) the engine of growth? (Streamlit app, WP07)

Run locally:   streamlit run apps/motors/app.py
Streamlit Community Cloud: main file path = apps/motors/app.py
"""
import streamlit as st

st.set_page_config(page_title="Development Motors", page_icon="⚙️", layout="wide")

pages = {
    "Overview": [st.Page("views/home.py", title="Findings at a glance", default=True)],
    "The four questions": [
        st.Page("views/q1_still.py", title="1. Is manufacturing still a motor?", url_path="still-a-motor"),
        st.Page("views/q2_lac.py", title="2. Was it ever a motor in LAC?", url_path="lac"),
        st.Page("views/q3_conditions.py", title="3. Why only in some contexts?", url_path="conditions"),
        st.Page("views/q4_sectors.py", title="4. Other candidate motors", url_path="other-motors"),
    ],
    "How solid is it?": [
        st.Page("views/robustness.py", title="Robustness: every specification", url_path="robustness"),
        st.Page("views/replication.py", title="Replicating Szirmai & Verspagen", url_path="replication"),
        st.Page("views/data.py", title="Data and method", url_path="data"),
    ],
}
st.navigation(pages).run()
