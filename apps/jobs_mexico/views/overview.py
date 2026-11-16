"""Overview of the Jobs in Mexico programme (WP09)."""
import streamlit as st

from jobs_lib import AUTHOR, footer

st.title("Jobs in Mexico")
st.markdown("Paul Wander · Division of Production, Productivity and Management, UN-ECLAC · devtheory WP09")
st.markdown(
    "Cross-country work on sectors as motors of development looks for sectors whose expansion raises aggregate "
    "growth. In this project that search found no sector that reliably plays the role (WP07), and sector averages "
    "conceal most of the variation in productivity (WP06, WP08). This programme takes the job as the unit of analysis "
    "and asks which jobs, held by which workers, are associated with stable employment, earnings growth with "
    "experience and transitions to formal or better-paid work.\n\n"
    "Mexico is studied first because its labour-force survey (ENOE) interviews the same dwellings in five consecutive "
    "quarters, measures formality consistently and has public quarterly microdata from 2005 onward.")

st.subheader("Studies")
st.markdown(
    "| Study | Question | Status |\n|---|---|---|\n"
    "| 9.1 Job transitions by sector, establishment size and formality | Does the sector of a job, or the size and "
    "formality of the establishment, better predict exit from employment and moves to better-paid job cells within a "
    "year? | Draft paper |\n"
    "| 9.2 Experience–earnings profiles by type of job | Are Mexico's flat experience–earnings profiles general, or "
    "concentrated in some types of job? | Draft paper |\n"
    "| 9.3 Productivity ladder with formal and informal segments | Do the stochastic-dominance verdicts of WP08 change "
    "when sectors are split into formal and informal segments? | Draft paper |\n"
    "| 9.4 The 2019 minimum-wage increase in the northern border zone | Did the 2019 package change employment, the "
    "earnings distribution and transitions out of informality? | Draft paper |\n"
    "| 9.5 First jobs and employment three quarters later | What are young people's first jobs, and how are they "
    "related to formal employment three quarters later? | Draft paper |\n"
    "| 9.6 Job mobility and growth across states | How much do states differ in job mobility at given workforce "
    "composition, and is mobility related to growth? | Draft paper |\n"
    "| 9.7 Labour productivity growth by state and activity | Where did non-oil labour productivity grow, through "
    "which channels, and did formality and pay move with it? | Draft paper |\n"
    "| 9.8 Minimum-wage increases of 2019–2024 by state and activity | How did wages, employment, formality and value "
    "added per worker respond where the increases reached more workers? | Draft paper |")
st.markdown(
    "Each study has a pre-analysis plan written before its estimates, a paper and a page in this application. "
    "Results are descriptive unless a page states an identifying assumption. The studies were checked by an "
    "independent audit in November 2026, whose corrections are recorded in the project's decision log (D-064). "
    "Papers and plans are in `papers/WP09_jobs_mexico/` of the "
    "[devtheory repository](https://github.com/wanderdata/devtheory).")
footer()
