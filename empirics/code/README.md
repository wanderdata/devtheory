# Phase 2 code

One folder per empirical project. Each has a `config.py`, numbered steps, a `run_all.py` that rebuilds every output, and a README. Shared country codes, names and ECLAC groupings live in [`../common/countries.py`](../common/countries.py); projects import them rather than keeping their own lists.

| Folder | What | Paper |
|---|---|---|
| [`lp/`](lp/README.md) | Sectoral labour productivity (UN national accounts + ILO employment) and McMillan–Rodrik decompositions, for the Caribbean (`LP_SCOPE=carib`) and for Latin America and the Caribbean (`LP_SCOPE=lac`) | WP05, WP06 |

Dependencies are pinned in [`requirements.txt`](../../requirements.txt) at the repository root. Tests: `pytest` from the repository root.
