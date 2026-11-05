import streamlit as st

from lib import COUNTRIES, NOT_COVERED, footer, load_labour

st.title("Caribbean labour productivity")
st.markdown("**Paul Wander** · Division of Production, Productivity and Management, UN-ECLAC")
st.markdown(
    f"""
Sectoral labour productivity and structural change for the **{len(COUNTRIES)} Caribbean member states of ECLAC's
Port of Spain office with sector employment data**, 1991–2024. The data are built from UN national accounts
(value added by sector) and ILO employment by economic activity. The full method is in the devtheory working paper WP05.

The dashboard has two separate parts.

**Baseline analysis (following McMillan & Rodrik).** The standard analysis of productivity and structural
change, following McMillan and Rodrik (2011), with a labour-market complement:
- productivity levels, rankings and annual change;
- the annual within/between decomposition (McMillan–Rodrik);
- relative sector productivity and employment shares, and sector productivity trends;
- sector contributions to the within-sector and structural-change components;
- the employment rate and its split into participation and unemployment;
- one-page country profiles.

**Extended analysis.** Additions to the baseline, described on each page:
- multi-year decompositions graded by how close their endpoints are to real survey years;
- additive prices;
- static and dynamic parts of structural change;
- robustness checks;
- the McMillan–Rodrik regression slope;
- productivity dispersion across sectors;
- a data-quality view.

**Choices that apply throughout**
- Two sector grids, analysed separately and never mixed. **A**: 7 sectors. **B**: 5 sectors, with all services combined.
- Employment comes from **ILO modelled estimates** by default. National survey data are available as an alternative; they have gaps between survey years.
- Value added is in **constant 2020 US dollars** in the baseline pages. The extended pages use additive initial-year prices.

**Not covered:** {", ".join(NOT_COVERED)} (no sector employment data).
"""
)
if load_labour() is None:
    st.info("Output per hour and the employment-rate charts need ILO labour-market series. They show "
            "\"data pending\" until those files are added.")
footer()
