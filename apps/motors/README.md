# Development motors dashboard (WP07)

Streamlit app presenting the update of Szirmai & Verspagen (2015): is manufacturing still the engine of growth, was it ever in Latin America and the Caribbean, which conditions make it work, and do services or other sectors play the role? It displays results computed by [`empirics/code/motors/`](../../empirics/code/motors/README.md); it estimates nothing itself.

**Run locally:** `streamlit run apps/motors/app.py` · **Streamlit Community Cloud:** repository `wanderdata/devtheory`, branch `main`, main file `apps/motors/app.py`, Python 3.12+ (dependencies in this folder's `requirements.txt`).

| Section | Page | Content |
|---|---|---|
| Overview | Findings at a glance | The four answers, with robustness verdicts read live from the outputs; one chart of every sector's slope by period across all specifications |
| The four questions | 1. Is manufacturing still a motor? | Slope by subperiod; 20-year rolling windows; marginal effect over schooling × income gap |
| | 2. Was it ever a motor in LAC? | LAC vs rest slopes by subperiod; Kaldor's first law by decade |
| | 3. Why only in some contexts? | Seven pre-specified conditions with predicted signs and verdicts |
| | 4. Other candidate motors | UN sector groups by subperiod; ETD 12 sectors by output and employment share; Caribbean tourism proxy |
| How solid is it? | Robustness | Specification curve over 192 specifications for each headline estimate |
| | Replication | S&V's coefficients next to ours in three samples, with verdicts |
| | Data and method | Sources, variables, estimators, samples, departures from the plan; coverage |

Conventions: every chart has a data table and a caption; findings are stated with their robustness verdict; the page text is checked against the outputs before release. Shared theme: [`apps/common/theme.py`](../common/theme.py).
