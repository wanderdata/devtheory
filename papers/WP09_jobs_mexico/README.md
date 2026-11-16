# WP09 — Jobs in Mexico

*Paul Wander. Programme overview, updated 2026-11-16.*

## Question

Earlier work in this project looked for sectors that act as motors of development and found none whose role holds up across specifications (WP07); it also found that sector averages conceal most of the variation in productivity (WP06, WP08). This programme takes the job as the unit of analysis and asks which jobs, held by which workers, are associated with stable employment, earnings growth with experience and transitions to formal or better-paid work.

Mexico comes first because its labour-force survey (ENOE) has a five-quarter rotating panel, a formality measure that is consistent over time, and public quarterly microdata from 2005 onward.

## Studies

| Study | Question | Data | Status | Outputs |
|---|---|---|---|---|
| 9.1 Job transitions by sector, establishment size and formality | Does the sector of a job, or the size and formality of the establishment, better predict exit from employment and moves to better-paid job cells within a year? | ENOE panels 2018–19, 2023–24 | Draft paper | [plan](9.1_job_ladders/00_pre_analysis_plan.md) · [paper](9.1_job_ladders/01_paper.md) · app page 9.1 |
| 9.2 Experience–earnings profiles by type of job | Are Mexico's flat experience–earnings profiles general, or concentrated in some types of job? | ENOE first quarters 2005–2025; panels of 9.1 | Draft paper | [plan](9.2_experience_profiles/00_pre_analysis_plan.md) · [paper](9.2_experience_profiles/01_paper.md) · app page 9.2 |
| 9.3 Productivity ladder with formal and informal segments | Do WP08's dominance verdicts change when sectors are split into formal and informal segments? | ENOE, all quarters of 2005, 2008, 2019, 2024; UN national accounts | Draft paper | [plan](9.3_productivity_ladder/00_pre_analysis_plan.md) · [paper](9.3_productivity_ladder/01_paper.md) · app page 9.3 |
| 9.4 The 2019 minimum-wage increase in the northern border zone | Did the 2019 package change employment, the earnings distribution and transitions out of informality? | ENOE, every quarter 2016Q1–2020Q1; CONABIO/INEGI municipal boundaries | Draft paper | [plan](9.4_border_minimum_wage/00_pre_analysis_plan.md) · [paper](9.4_border_minimum_wage/01_paper.md) · app page 9.4 |
| 9.5 First jobs and employment three quarters later | What are young people's first jobs, and how are they related to formal employment three quarters later? | ENOE, every quarter 2005–2019 and 2022–2026 (70 five-quarter panels) | Draft paper | [plan](9.5_first_jobs/00_pre_analysis_plan.md) · [paper](9.5_first_jobs/01_paper.md) · app page 9.5 |
| 9.6 Job mobility and growth across states | How much do states differ in job mobility at given workforce composition, and is mobility related to growth? | ENOE 2005–2026 one-year panels; INEGI PIBE base 2018 | Draft paper | [plan](9.6_states/00_pre_analysis_plan.md) · [paper](9.6_states/01_paper.md) · app page 9.6 |
| 9.7 Labour productivity growth by state and activity | Where did non-oil labour productivity grow, through which channels, and did earnings and formality follow? | PIBE base 2018 by state and activity, 2003–2024; ENOE every quarter 2005–2024 | Plan | [plan](9.7_state_productivity/00_pre_analysis_plan.md) |

Synthesis: [Jobs and productive development in Mexico: findings of six studies, 2005–2026](00_synthesis.md) (draft v0.1).

## Common elements

INEGI's quarterly zips are kept unchanged as release assets of `wanderdata/enoe_data` and downloaded by `empirics/code/enoe/00_fetch.py`; microdata never enter the devtheory repository. Shared code in `empirics/code/enoe/` reads the files whatever INEGI's naming convention, links people across quarters and holds the configuration. Each study has one folder for code (`empirics/code/enoe/<study>/`) and one for outputs (`empirics/output/enoe/<study>/`), and one page in the app `apps/jobs_mexico/`.

Each study has a pre-analysis plan committed before its estimates and amended only with dated entries. Papers are written for outside readers, with procedural notes in an annex, following the style rules in decision D-062. Decisions for the programme start at D-046.
