# ENOE job ladders in Mexico (WP09)

Design and tests are fixed in [`papers/WP09_job_ladders_mexico/00_pre_analysis_plan.md`](../../../papers/WP09_job_ladders_mexico/00_pre_analysis_plan.md) (D-046). Origin: RG01, paper 3 (Donovan, Lu & Schoellman 2023).

| File | Role |
|---|---|
| `enoe_config.py` | Paths, windows (2018Q4–2019Q4, 2023Q1–2024Q1), age range, person key, size and formality labels |
| `enoe_io.py` | Finds and reads INEGI's quarterly tables (CSV, zipped or not) whatever the file-naming convention of the release |
| `enoe_link.py` | Links respondents across consecutive quarters (unique key, visit number +1, same sex, age change −1 to +2) and assigns person ids |
| `enoe_flows.py` | Labour-market states and job cells, rates, upward transitions, R² and Shapley decomposition |
| `00_fetch.py` | Downloads the quarterly zips from the release assets of `wanderdata/enoe_data` into `empirics/data/raw/enoe/` and writes a SHA-256 manifest |
| `01_link.py` | Applies the sample rules and links each window; linked microdata go to the uncommitted `empirics/data/raw/enoe_interim/` |
| `02_flows.py` | Writes aggregate tables only to `empirics/output/enoe/` |
| `tests/test_enoe.py` | File-name matching, linking rules, rates and decomposition on synthetic panels with ENOE's variable names |

Microdata never enter this repository. INEGI's codes for `ambito2` and the urban definition from `cd_a` are to be checked against the file description before results are used (OQ-63).
