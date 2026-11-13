# WP09 — Jobs in Mexico

*Paul Wander. Programme overview, updated 2026-11-13.*

## Question

Earlier work in this project looked for "motors" of development at the level of sectors and found none that hold up (WP07). It also found that sector averages hide most of the variation in productivity (WP06, WP08). This programme moves to the level of the job: which jobs, held by which workers, carry productivity growth, skill accumulation and upward mobility?

Mexico comes first because its labour-force survey (ENOE) offers:
- a five-quarter rotating panel;
- a consistent formality measure;
- quarterly microdata from 2005 onward, all public.

## Studies

| Study | Question | Data | Status | Outputs |
|---|---|---|---|---|
| **9.1 Which jobs are rungs?** | Do sector or firm size and formality better predict whether a job leads to stable, better-paid work within a year? | ENOE panels 2018–19, 2023–24 | Draft paper | [plan](9.1_job_ladders/00_pre_analysis_plan.md) · [paper](9.1_job_ladders/01_paper.md) · app page 9.1 |
| **9.2 Which jobs build skills?** | Are Mexico's flat experience–earnings profiles general, or concentrated in some types of job? | ENOE first quarters 2005–2025; panels of 9.1 | In progress | [plan](9.2_experience_profiles/00_pre_analysis_plan.md) · app page 9.2 |
| 9.3 A productivity ladder for Mexico | Do WP08's verdicts change when sectors are split into formal and informal steps? | ENOE 2005–2025; INEGI informal-economy accounts | Planned | — |
| 9.4 The 2019 border minimum wage | Did doubling the minimum wage in the northern border zone change formal hiring and moves out of informality? | ENOE 2017–2021, border cities vs others | Planned | — |
| 9.5 Where careers start | What are young workers' first jobs, and where are they a year later? | ENOE panels | Possible | — |
| 9.6 States | Which states have more rungs, and does that track state growth? | ENOE + state accounts | Possible | — |

## Common elements

- **Data.** INEGI's quarterly zips are kept unchanged as release assets of `wanderdata/enoe_data` and downloaded by `empirics/code/enoe/00_fetch.py`. Microdata never enter the devtheory repository.
- **Shared code** in `empirics/code/enoe/`:
  - reading files whatever INEGI's naming convention;
  - linking people across quarters;
  - configuration.
- **One folder per study** for code (`empirics/code/enoe/<study>/`) and outputs (`empirics/output/enoe/<study>/`).
- **App.** `apps/jobs_mexico/`, with one page per study.
- **Conventions:**
  - a pre-analysis plan before each study's estimates, amended only with dated entries;
  - papers written for outside readers, with procedural notes in an annex;
  - decisions D-046 onward.
