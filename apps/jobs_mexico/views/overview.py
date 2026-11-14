"""Overview of the Jobs in Mexico programme (WP09)."""
import streamlit as st

from jobs_lib import AUTHOR, footer

st.title("Jobs in Mexico")
st.markdown(f"**Paul Wander** · Division of Production, Productivity and Management, UN-ECLAC · devtheory WP09")
st.markdown(
    "Cross-country work on \"motors\" of development looks for sectors whose expansion raises growth. In this "
    "project that search found no sector that reliably plays the role (WP07), and sector averages hide most of the "
    "variation in productivity (WP06, WP08). This programme moves to the level of the **job**: which jobs, held by "
    "which workers, carry productivity growth, skill accumulation and upward mobility?\n\n"
    "Mexico comes first because its labour-force survey (ENOE) follows the same dwellings for five quarters, measures "
    "formality consistently and has public quarterly microdata from 2005 onward.")

st.subheader("Studies")
st.markdown(
    "| Study | Question | Status |\n|---|---|---|\n"
    "| **9.1 Which jobs are rungs?** | Do sector or firm size and formality better predict whether a job leads to "
    "stable, better-paid work within a year? | Draft results |\n"
    "| **9.2 Which jobs build skills?** | Are Mexico's flat experience–earnings profiles general, or concentrated in "
    "some types of job? | Results |\n"
    "| **9.3 A productivity ladder for Mexico** | Do the verdicts of the ladder of the working-age population change when "
    "sectors are split into formal and informal steps? | Results |\n"
    "| **9.4 The 2019 border minimum wage** | Did doubling the minimum wage in the northern border zone change formal "
    "hiring and moves out of informality? | Results |\n"
    "| **9.5 Where careers start** | What are young workers' first jobs, and where do they lead? | Results |\n"
    "| 9.6 States | Which states have more rungs, and does that track state growth? | Possible |")
st.markdown(
    "Each study has a pre-analysis plan written before its estimates, a paper and a page in this app. All results "
    "are descriptive unless a page says otherwise. Papers and plans are in `papers/WP09_jobs_mexico/` of the "
    "[devtheory repository](https://github.com/wanderdata/devtheory).")
footer()
