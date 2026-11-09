# motors: development motors (WP07)

Replication and update of Szirmai & Verspagen (2015): does a sector's share of value added predict subsequent growth of GDP per head, when, where and under which conditions? Design fixed in advance in [`papers/WP07_development_motors/00_literature_and_plan.md`](../../../papers/WP07_development_motors/00_literature_and_plan.md) (D-037); write-up in [`WP07_development_motors.md`](../../../papers/WP07_development_motors/WP07_development_motors.md).

**Run everything:** `python empirics/code/motors/run_all.py` (about a minute). Tests: `pytest empirics/code/motors`.

| Step | What | Output (`empirics/output/motors/`, `empirics/data/processed/motors/`) |
|---|---|---|
| `estimators.py` | RE/FE/BE (linearmodels); Hausman–Taylor implemented here, validated on the Cornwell–Rupert wage panel (`tests/test_estimators.py`) | — |
| `01_build_panel.py` | Annual country data and five- and ten-year panels: PWT 11.0 growth, income gap, human capital; UN AMA shares from 1970, GGDC 10-Sector before (ratio-spliced, rescaled); Barro–Lee; openness; undervaluation; latitude-based temperate instrument (D-038) | `annual.csv`, `panel5.csv`, `panel10.csv`, `countries.csv` |
| `02_replicate.py` | S&V Tables 2–4 in three samples, with verdicts against S&V | `replication/` |
| `03_questions.py` | Q1 subperiods, rolling windows, marginal-effect surfaces; Q2 LAC slopes and Kaldor's first law; Q3 moderators | `questions/` |
| `04_sectors.py` | Q4 UN sector groups, ETD 12 sectors (value added and employment), Caribbean tourism proxy | `sectors/` |
| `05_speccurve.py` | 192 specifications for every headline estimate, with verdicts | `speccurve/` |
| `models.py`, `config.py` | Specification, samples (D-039), slope shifts, marginal effects; settings | — |

Samples: *main* (population ≥ 1 million, pre-specified), *excl_cpe* (without former planned economies), *core* (also without commodity exporters), *developing* (core without the 21 advanced economies). Findings require agreement between main and core.
