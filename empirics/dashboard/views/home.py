import streamlit as st

from lib import countries, footer, load_labour, not_covered, scope, scope_info

info = scope_info()
st.title(f"Labour productivity and structural change: {info['label']}")
st.markdown("**Paul Wander** · Division of Production, Productivity and Management, UN-ECLAC")
other = "Caribbean" if scope() == "lac" else "Latin America and the Caribbean"
st.markdown(
    f"""
Sectoral labour productivity and structural change for {info['blurb']}, 1991–2024: **{len(countries())}
countries with sector employment data**. The data are built from UN national accounts (value added by sector)
and ILO employment by economic activity. The full method is in the devtheory working paper WP05.

The **Region** selector at the top of the sidebar switches every page between Latin America and the
Caribbean and the Caribbean; you are now viewing **{info['label']}** (switch to *{other}* there).

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
- three price bases for those decompositions (chained, initial-year, final-year), with a note on how they differ;
- static and dynamic parts of structural change;
- robustness checks;
- the McMillan–Rodrik regression slope;
- productivity dispersion across sectors;
- a data-quality view.

**Choices that apply throughout**
- Two sector grids, analysed separately and never mixed. **A**: 7 sectors. **B**: 5 sectors, with all services combined.
- Employment comes from **ILO modelled estimates** by default. National survey data are available as an
  alternative; they have gaps between survey years. Surveys that do not cover the whole country (urban-only
  surveys, for example Argentina's) are not used, because their sector shares understate agriculture.
- Value added is in **constant 2020 US dollars** in the baseline pages. The extended pages use additive prices.
- The pooled regional aggregate adds up countries' value added and employment, so large economies dominate it.
  In the Latin America and the Caribbean view, Venezuela and Cuba are left out of it by default because their
  US-dollar levels are not comparable; they can be added in the sidebar.
"""
    + (f"\n**Not covered:** {', '.join(not_covered())} (no sector employment data).\n" if not_covered() else "")
)
if load_labour() is None:
    st.info("Output per hour and the employment-rate charts need ILO labour-market series. They show "
            "\"data pending\" until those files are added.")
footer()
