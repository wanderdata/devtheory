# ENOE studies (WP09, Jobs in Mexico)

Programme overview: [`papers/WP09_jobs_mexico/README.md`](../../../papers/WP09_jobs_mexico/README.md). Decisions D-046 onward. Microdata never enter this repository: the quarterly zips are release assets of `wanderdata/enoe_data` and are downloaded into the uncommitted `empirics/data/raw/enoe/`. Only aggregate tables are committed, in `empirics/output/enoe/<study>/`. These pipelines are not run in CI; their code is tested on synthetic data in `tests/`.

## Shared

| File | Role |
|---|---|
| `enoe_config.py` | Paths, panel windows (2018Q4–2019Q4, 2023Q1–2024Q1), annual cross-sections (first quarters 2005–2025), person key, size and formality labels |
| `enoe_io.py` | Finds and reads INEGI's quarterly tables (CSV, zipped or not) whatever the release's file naming |
| `enoe_link.py` | Links respondents across consecutive quarters (unique key, visit number +1, same sex, age change −1 to +2) and assigns person ids |
| `00_fetch.py` | Downloads the CSV zips the studies need through the GitHub REST API and writes a SHA-256 manifest |
| `run_all.py` | Fetch, then each study's `run_all.py` |

## Study 9.1 — Which jobs are rungs? (`ladders/`)

Plan and paper in `papers/WP09_jobs_mexico/9.1_job_ladders/`.

| Step | Output |
|---|---|
| `01_link.py` | Linked panels (uncommitted) and `link_diagnostics.csv` |
| `02_flows.py` | Flows, rates by job cell, Shapley decompositions with robustness variants, manufacturing vs services, transitions, earnings growth |
| `03_report.py` | `results.md` |

## Study 9.2 — Which jobs build skills? (`profiles/`)

Plan and paper in `papers/WP09_jobs_mexico/9.2_experience_profiles/`.

| Step | Output |
|---|---|
| `01_extract.py` | Annual cross-sections (uncommitted) |
| `02_profiles.py` | Cross-sectional and HLT profiles with bootstrap intervals, composition decomposition, earnings reporting |
| `03_panel.py` | Within-person synthetic profiles from the 9.1 panels |
| `04_diagnostics.py` | Exploratory: profiles by period, HLT on 2005–2018, reporting by experience |
| `05_report.py` | `results.md` |
| `profiles_lib.py` | Experience, sample rules, sparse weighted regressions, HLT restriction, composition decomposition |

## Study 9.3 — A productivity ladder for Mexico (`productivity_ladder/`)

Plan and paper in `papers/WP09_jobs_mexico/9.3_productivity_ladder/`. Uses WP08's `empirics/code/lp/ladder.py` and `decompose.py` and the UN sector panel `empirics/data/processed/lac_lp/panel_7sector.csv`.

| Step | Output |
|---|---|
| `01_extract.py` | `cells.csv`: weighted employment, labour income and population 15+ by year × quarter × sector × formality × size (aggregates only, committed) |
| `02_ladder.py` | `segments.csv`, `verdicts.csv`, `decomposition.csv`, `ladders.csv`, `incidence.csv` |
| `03_report.py` | `results.md` |

## Study 9.4 — The 2019 border minimum wage (`border_mw/`)

Plan and paper in `papers/WP09_jobs_mexico/9.4_border_minimum_wage/`. Main sample: sampling units observed in 2016–2018 (INEGI enlarged the sample in the border zone only, in 2019Q1; D-054).

| Step | Output |
|---|---|
| `00_geo.py` | Municipal boundaries (CONABIO 2020, downloaded to the uncommitted `empirics/data/raw/geo_mx/`), ZLFN list matched to INEGI codes, distance to the zone's edge: `municipalities.csv`, `municipalities.geojson` |
| `01_extract.py` | Persons and links between consecutive quarters, 2016Q1–2020Q1 (uncommitted); `linkage.csv` |
| `02_cells.py` | Municipality × quarter cells by sample and group; six-state cells in `cells.csv` |
| `03_did.py` | `did.csv`, `event.csv`, `pretrend.csv`, `bins.csv`, `pre_means.csv` |
| `04_maps.py` | `map_values.csv` (levels, net changes, empirical Bayes), `rd_bins.csv` |
| `05_report.py` | `results.md`, applying the plan's decision rules |
| `border_lib.py` | Two-way FE regressions, CR1 variances, restricted wild cluster bootstrap |

## Study 9.5 — Where careers start (`first_jobs/`)

Plan and paper in `papers/WP09_jobs_mexico/9.5_first_jobs/`. Needs every CSV quarter: `python empirics/code/enoe/00_fetch.py --all-csv`.

| Step | Output |
|---|---|
| `01_extract.py` | Cached extracts of persons aged 15–30 per quarter, with household variables and the never-worked answer (uncommitted; two processes); `stock.csv` |
| `02_panels.py` | Five-interview histories of never-worked, non-employed 15–29-year-olds (uncommitted); `linkage.csv` |
| `03_estimates.py` | `composition.csv`, `transitions.csv`, `estimates.csv`, `oster.csv`, `earnings.csv`, `checks.csv` |
| `04_report.py` | `results.md`, applying the plan's decision rules |
